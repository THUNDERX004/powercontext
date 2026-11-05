from __future__ import annotations

from pathlib import Path

import pytest
from sddctx.config import Settings


@pytest.fixture()
def settings(tmp_path: Path) -> Settings:
    home = tmp_path / "minimax"
    (home / "specs").mkdir(parents=True)
    (home / "sample-project" / "src" / "demo").mkdir(parents=True)
    (home / "sample-project" / "tests").mkdir(parents=True)
    return Settings(
        home=home,
        project_key="test-project",
        seekdb_host="127.0.0.1",
        seekdb_port=2881,
        seekdb_user="root",
        seekdb_password="",
        seekdb_database="minimax_sdd_test",
        powercontext_url="http://127.0.0.1:8000",
        powercontext_token=None,
        minimax_api_key="test-key",
        minimax_base_url="https://api.minimaxi.com/v1",
        minimax_model="MiniMax-M3.1-Flash",
        minimax_temperature=0.2,
        minimax_max_tokens=1024,
    )
