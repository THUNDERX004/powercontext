from __future__ import annotations

from sddctx.config import Settings
from sddctx.importer import collect_assets


def test_collect_assets_splits_spec_entries_and_indexes_python(
    settings: Settings,
) -> None:
    (settings.specs_dir / "SPEC-001-demo.md").write_text(
        "# Demo spec\n\n- SPEC-001-1: first rule\n- SPEC-001-2: second rule\n",
        encoding="utf-8",
    )
    source_dir = settings.sample_project_dir / "src" / "demo"
    (source_dir / "__init__.py").write_text("", encoding="utf-8")
    (source_dir / "catalog.py").write_text(
        '"""Demo catalog."""\n\nclass Catalog:\n    def search(self, min_year=None):\n        return min_year\n',
        encoding="utf-8",
    )
    (settings.sample_project_dir / "tests" / "test_catalog.py").write_text(
        "def test_search():\n    assert True\n",
        encoding="utf-8",
    )

    assets = collect_assets(settings)
    kinds = [asset.kind for asset in assets]
    assert kinds.count("spec") == 1
    assert kinds.count("spec_entry") == 2
    assert kinds.count("code") == 2
    assert kinds.count("test") == 1
    catalog = next(asset for asset in assets if asset.path.endswith("catalog.py"))
    assert "Catalog" in catalog.symbol
    assert "search" in catalog.symbol
