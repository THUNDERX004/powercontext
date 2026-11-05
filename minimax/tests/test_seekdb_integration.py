from __future__ import annotations

import os
from dataclasses import replace

import pytest
from sddctx.config import Settings
from sddctx.models import Asset
from sddctx.seekdb_store import SeekDBStore, sha256_text


@pytest.mark.skipif(
    os.environ.get("SDDCTX_RUN_INTEGRATION") != "1",
    reason="set SDDCTX_RUN_INTEGRATION=1 with a reachable seekdb",
)
def test_seekdb_fulltext_roundtrip() -> None:
    settings = replace(Settings.load(), project_key="test:seekdb-integration")
    store = SeekDBStore(settings)
    store.initialize()
    content = "Catalog.search min_year filters Book.published_year inclusively"
    store.upsert(
        Asset(
            project_key=settings.project_key,
            asset_id="test:integration.py",
            kind="code",
            path="sample-project/src/integration.py",
            title="integration",
            symbol="Catalog.search min_year",
            content=content,
            content_hash=sha256_text(content),
        )
    )
    hits = store.search("min_year", ("code",), 5, "integration:search")
    assert hits
    assert hits[0].asset.path == "sample-project/src/integration.py"
    store.delete_missing(settings.project_key, [])
