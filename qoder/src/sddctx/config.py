"""Runtime configuration loaded exclusively from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _env(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    return default if value is None or not value.strip() else value.strip()


def _env_int(name: str, default: int) -> int:
    value = _env(name)
    return default if value is None else int(value)


def _env_float(name: str, default: float) -> float:
    value = _env(name)
    return default if value is None else float(value)


def load_env_file(path: Path) -> None:
    """Load a small dotenv file without overriding the process environment."""
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.strip()
        value = value.strip().strip('"').strip("'")
        if name and name not in os.environ:
            os.environ[name] = value


@dataclass(frozen=True)
class Settings:
    home: Path
    project_key: str
    seekdb_host: str
    seekdb_port: int
    seekdb_user: str
    seekdb_password: str
    seekdb_database: str
    powercontext_url: str
    powercontext_token: str | None
    minimax_api_key: str | None
    minimax_base_url: str
    minimax_model: str
    minimax_temperature: float
    minimax_max_tokens: int

    @classmethod
    def load(cls) -> "Settings":
        default_home = Path(__file__).resolve().parents[2]
        home = Path(_env("SDDCTX_HOME", str(default_home)) or default_home).resolve()
        load_env_file(Path(_env("SDDCTX_ENV_FILE", str(home / ".env")) or home / ".env"))
        return cls(
            home=home,
            project_key=_env("SDDCTX_PROJECT_KEY", "qoder-sdd") or "qoder-sdd",
            seekdb_host=_env("SEEKDB_HOST", "127.0.0.1") or "127.0.0.1",
            seekdb_port=_env_int("SEEKDB_PORT", 2881),
            seekdb_user=_env("SEEKDB_USER", "root") or "root",
            seekdb_password=_env("SEEKDB_PASSWORD", "") or "",
            seekdb_database=_env("SEEKDB_DATABASE", "qoder_sdd") or "qoder_sdd",
            powercontext_url=_env("SDDCTX_POWERCONTEXT_URL", "http://127.0.0.1:8000")
            or "http://127.0.0.1:8000",
            powercontext_token=_env("SDDCTX_POWERCONTEXT_TOKEN"),
            minimax_api_key=_env("SDDCTX_MINIMAX_API_KEY", os.environ.get("MINIMAX_API_KEY")),
            minimax_base_url=_env(
                "SDDCTX_MINIMAX_BASE_URL", "https://api.minimaxi.com/v1"
            )
            or "https://api.minimaxi.com/v1",
            minimax_model=_env("SDDCTX_MINIMAX_MODEL", "MiniMax-M3.1-Flash")
            or "MiniMax-M3.1-Flash",
            minimax_temperature=_env_float("SDDCTX_MINIMAX_TEMPERATURE", 0.2),
            minimax_max_tokens=_env_int("SDDCTX_MINIMAX_MAX_TOKENS", 16384),
        )

    @property
    def specs_dir(self) -> Path:
        return self.home / "specs"

    @property
    def sample_project_dir(self) -> Path:
        return self.home / "sample-project"

    @property
    def records_dir(self) -> Path:
        return self.home / "records"

    @property
    def db_query_log(self) -> Path:
        return self.records_dir / "db-query-log.md"

    @property
    def powercontext_log(self) -> Path:
        return self.records_dir / "powercontext-log.md"


def redact(secret: str | None) -> str:
    if not secret:
        return "<unset>"
    if len(secret) <= 8:
        return "***"
    return f"{secret[:4]}...{secret[-4:]}(redacted)"
