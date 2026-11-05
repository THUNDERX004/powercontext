"""seekdb-backed engineering asset store."""

from __future__ import annotations

import contextlib
import hashlib
import json
import time
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pymysql
from pymysql.cursors import DictCursor

from sddctx.analyzer import analyze_text
from sddctx.config import Settings
from sddctx.models import Asset, SearchHit

ASSET_TABLE = "engineering_assets"
FTS_INDEX = "ft_engineering_assets_search"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class QueryLog:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.entries: list[dict[str, Any]] = []

    def write(
        self,
        *,
        purpose: str,
        sql: str,
        parameters: Any,
        rows: list[dict[str, Any]] | list[tuple[Any, ...]] | int,
        duration_ms: float,
    ) -> None:
        safe_parameters = json.dumps(parameters, ensure_ascii=False, default=str)
        if len(safe_parameters) > 1200:
            safe_parameters = safe_parameters[:1200] + "..."
        entry = {
            "purpose": purpose,
            "sql": " ".join(sql.split()),
            "parameters": safe_parameters,
            "duration_ms": round(duration_ms, 3),
            "rows": rows if isinstance(rows, int) else len(rows),
        }
        self.entries.append(entry)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        header = "" if self.path.exists() else (
            "# seekdb 查询记录\n\n"
            "由 `sddctx` 自动追加。参数中的资产正文只记录长度，不写入日志。\n\n"
        )
        with self.path.open("a", encoding="utf-8") as handle:
            if header:
                handle.write(header)
            handle.write(f"## {entry['purpose']}\n\n")
            handle.write(f"```sql\n{entry['sql']}\n```\n\n")
            handle.write(
                f"- 参数：`{safe_parameters}`\n"
                f"- 返回行数：`{entry['rows']}`\n"
                f"- 耗时：`{entry['duration_ms']} ms`\n\n"
            )


class SeekDBStore:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.query_log = QueryLog(settings.db_query_log)

    def _connect(self, *, database: str | None = None) -> pymysql.Connection:
        return pymysql.connect(
            host=self.settings.seekdb_host,
            port=self.settings.seekdb_port,
            user=self.settings.seekdb_user,
            password=self.settings.seekdb_password,
            database=database,
            charset="utf8mb4",
            cursorclass=DictCursor,
            autocommit=True,
            connect_timeout=10,
        )

    @contextlib.contextmanager
    def connection(self) -> Iterator[pymysql.Connection]:
        connection = self._connect(database=self.settings.seekdb_database)
        try:
            yield connection
        finally:
            connection.close()

    def initialize(self) -> None:
        database = self.settings.seekdb_database.replace("`", "``")
        with self._connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{database}` "
                "DEFAULT CHARACTER SET utf8mb4"
            )
        with self.connection() as connection, connection.cursor() as cursor:
            started = time.perf_counter()
            cursor.execute(
                f"""
                    CREATE TABLE IF NOT EXISTS `{ASSET_TABLE}` (
                        project_key VARCHAR(128) NOT NULL,
                        asset_id VARCHAR(255) NOT NULL,
                        kind VARCHAR(32) NOT NULL,
                        path VARCHAR(768) NOT NULL,
                        title VARCHAR(512) NOT NULL DEFAULT '',
                        symbol VARCHAR(1024) NOT NULL DEFAULT '',
                        content MEDIUMTEXT NOT NULL,
                        content_hash CHAR(64) NOT NULL,
                        version INT NOT NULL DEFAULT 1,
                        imported_at VARCHAR(64) NOT NULL,
                        searchable_text MEDIUMTEXT NOT NULL,
                        PRIMARY KEY (project_key, asset_id),
                        KEY ix_asset_kind (project_key, kind)
                    ) DEFAULT CHARSET=utf8mb4
                    """
            )
            self.query_log.write(
                purpose="initialize:create-table",
                sql=f"CREATE TABLE IF NOT EXISTS {ASSET_TABLE}",
                parameters={"database": self.settings.seekdb_database},
                rows=0,
                duration_ms=(time.perf_counter() - started) * 1000,
            )
            cursor.execute(
                """
                    SELECT COUNT(*) AS count
                    FROM information_schema.statistics
                    WHERE table_schema = %s
                      AND table_name = %s
                      AND index_name = %s
                    """,
                (self.settings.seekdb_database, ASSET_TABLE, FTS_INDEX),
            )
            if int(cursor.fetchone()["count"]) == 0:
                started = time.perf_counter()
                cursor.execute(
                    f"CREATE FULLTEXT INDEX `{FTS_INDEX}` "
                    f"ON `{ASSET_TABLE}` (searchable_text) WITH PARSER SPACE"
                )
                self.query_log.write(
                    purpose="initialize:create-fulltext-index",
                    sql=f"CREATE FULLTEXT INDEX {FTS_INDEX}",
                    parameters={"table": ASSET_TABLE},
                    rows=0,
                    duration_ms=(time.perf_counter() - started) * 1000,
                )

    def upsert(self, asset: Asset) -> str:
        searchable = analyze_text(
            f"{asset.title} {asset.symbol} {asset.path} {asset.content}"
        )
        imported_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        with self.connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                f"""
                    SELECT content_hash, version
                    FROM `{ASSET_TABLE}`
                    WHERE project_key=%s AND asset_id=%s
                    """,
                (asset.project_key, asset.asset_id),
            )
            existing = cursor.fetchone()
            if existing and existing["content_hash"] == asset.content_hash:
                return "unchanged"
            if existing:
                started = time.perf_counter()
                cursor.execute(
                    f"""
                        UPDATE `{ASSET_TABLE}`
                        SET kind=%s, path=%s, title=%s, symbol=%s, content=%s,
                            content_hash=%s, version=version+1,
                            imported_at=%s, searchable_text=%s
                        WHERE project_key=%s AND asset_id=%s
                        """,
                    (
                        asset.kind,
                        asset.path,
                        asset.title,
                        asset.symbol,
                        asset.content,
                        asset.content_hash,
                        imported_at,
                        searchable,
                        asset.project_key,
                        asset.asset_id,
                    ),
                )
                action = "updated"
            else:
                started = time.perf_counter()
                cursor.execute(
                    f"""
                        INSERT INTO `{ASSET_TABLE}`
                        (project_key, asset_id, kind, path, title, symbol, content,
                         content_hash, version, imported_at, searchable_text)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,1,%s,%s)
                        """,
                    (
                        asset.project_key,
                        asset.asset_id,
                        asset.kind,
                        asset.path,
                        asset.title,
                        asset.symbol,
                        asset.content,
                        asset.content_hash,
                        imported_at,
                        searchable,
                    ),
                )
                action = "inserted"
            self.query_log.write(
                purpose=f"import:{action}:{asset.path}",
                sql=(
                    f"INSERT/UPDATE {ASSET_TABLE}"
                    if not existing
                    else f"UPDATE {ASSET_TABLE} SET content_hash, version=version+1"
                ),
                parameters={
                    "project_key": asset.project_key,
                    "asset_id": asset.asset_id,
                    "path": asset.path,
                    "version": 1 if not existing else int(existing["version"]) + 1,
                    "content_chars": len(asset.content),
                },
                rows=1,
                duration_ms=(time.perf_counter() - started) * 1000,
            )
        return action

    def delete_missing(self, project_key: str, keep_asset_ids: list[str]) -> int:
        keep = set(keep_asset_ids)
        with self.connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                f"SELECT asset_id FROM `{ASSET_TABLE}` WHERE project_key=%s",
                (project_key,),
            )
            stale = [row["asset_id"] for row in cursor.fetchall() if row["asset_id"] not in keep]
            for asset_id in stale:
                cursor.execute(
                    f"DELETE FROM `{ASSET_TABLE}` WHERE project_key=%s AND asset_id=%s",
                    (project_key, asset_id),
                )
        return len(stale)

    def count(self) -> int:
        with self.connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                f"SELECT COUNT(*) AS count FROM `{ASSET_TABLE}` WHERE project_key=%s",
                (self.settings.project_key,),
            )
            return int(cursor.fetchone()["count"])

    def search(self, text: str, kinds: tuple[str, ...], limit: int, purpose: str) -> list[SearchHit]:
        analyzed = analyze_text(text)
        if not analyzed or not kinds:
            return []
        placeholders = ",".join(["%s"] * len(kinds))
        sql = f"""
            SELECT project_key, asset_id, kind, path, title, symbol, content,
                   content_hash, version,
                   MATCH(searchable_text) AGAINST(%s) AS score
            FROM `{ASSET_TABLE}`
            WHERE project_key=%s
              AND kind IN ({placeholders})
              AND MATCH(searchable_text) AGAINST(%s)
            ORDER BY score DESC, path, asset_id
            LIMIT %s
        """
        params: tuple[Any, ...] = (analyzed, self.settings.project_key, *kinds, analyzed, limit)
        started = time.perf_counter()
        with self.connection() as connection, connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
        duration = (time.perf_counter() - started) * 1000
        self.query_log.write(
            purpose=purpose,
            sql=sql,
            parameters={
                "analyzed_query": analyzed,
                "project_key": self.settings.project_key,
                "kinds": kinds,
                "limit": limit,
            },
            rows=rows,
            duration_ms=duration,
        )
        return [
            SearchHit(
                asset=Asset(
                    project_key=row["project_key"],
                    asset_id=row["asset_id"],
                    kind=row["kind"],
                    path=row["path"],
                    title=row["title"],
                    symbol=row["symbol"],
                    content=row["content"],
                    content_hash=row["content_hash"],
                    version=int(row["version"]),
                ),
                score=float(row["score"]),
            )
            for row in rows
        ]
