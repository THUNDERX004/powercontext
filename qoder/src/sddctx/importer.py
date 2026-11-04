"""Collect specifications, source files and tests into seekdb."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path

from sddctx.config import Settings
from sddctx.models import Asset
from sddctx.seekdb_store import SeekDBStore, sha256_text

_SPEC_ENTRY = re.compile(r"^- (?P<id>SPEC-\d{3}-\d+):\s*(?P<body>.+)$", re.MULTILINE)


@dataclass(frozen=True)
class ImportResult:
    files: int
    inserted: int
    updated: int
    unchanged: int
    removed: int
    total: int


def _title_for_python(source: str) -> str:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ""
    return (ast.get_docstring(tree) or "").splitlines()[0] if ast.get_docstring(tree) else ""


def _symbols_for_python(source: str) -> str:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ""
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.append(node.name)
    return ", ".join(dict.fromkeys(names))


def collect_assets(settings: Settings) -> list[Asset]:
    assets: list[Asset] = []
    project_key = settings.project_key

    for path in sorted(settings.specs_dir.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        relative = path.relative_to(settings.home).as_posix()
        title = next((line.lstrip("# ").strip() for line in content.splitlines() if line.startswith("#")), path.stem)
        assets.append(
            Asset(
                project_key=project_key,
                asset_id=f"spec:{relative}",
                kind="spec",
                path=relative,
                title=title,
                symbol="",
                content=content,
                content_hash=sha256_text(content),
            )
        )
        for match in _SPEC_ENTRY.finditer(content):
            entry_id = match.group("id")
            body = match.group("body").strip()
            assets.append(
                Asset(
                    project_key=project_key,
                    asset_id=f"spec-entry:{relative}#{entry_id}",
                    kind="spec_entry",
                    path=f"{relative}#{entry_id}",
                    title=entry_id,
                    symbol=entry_id,
                    content=body,
                    content_hash=sha256_text(body),
                )
            )

    for folder, kind in (("src", "code"), ("tests", "test")):
        root = settings.sample_project_dir / folder
        for path in sorted(root.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            content = path.read_text(encoding="utf-8")
            relative = path.relative_to(settings.home).as_posix()
            assets.append(
                Asset(
                    project_key=project_key,
                    asset_id=f"{kind}:{relative}",
                    kind=kind,
                    path=relative,
                    title=_title_for_python(content) or path.name,
                    symbol=_symbols_for_python(content),
                    content=content,
                    content_hash=sha256_text(content),
                )
            )
    return assets


def run_import(settings: Settings) -> ImportResult:
    store = SeekDBStore(settings)
    store.initialize()
    assets = collect_assets(settings)
    counts = {"inserted": 0, "updated": 0, "unchanged": 0}
    for asset in assets:
        counts[store.upsert(asset)] += 1
    removed = store.delete_missing(settings.project_key, [asset.asset_id for asset in assets])
    return ImportResult(
        files=sum(
            1
            for path in settings.home.rglob("*")
            if path.is_file()
            and (settings.specs_dir in path.parents or settings.sample_project_dir in path.parents)
            and path.suffix in {".md", ".py"}
        ),
        inserted=counts["inserted"],
        updated=counts["updated"],
        unchanged=counts["unchanged"],
        removed=removed,
        total=store.count(),
    )
