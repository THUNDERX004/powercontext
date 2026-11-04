from __future__ import annotations

import pytest

from sddctx.agent import MiniMaxError, parse_file_blocks, validate_target
from sddctx.config import Settings


def test_parse_complete_file_blocks() -> None:
    response = """<file path="sample-project/src/demo/catalog.py">
```python
value = 1
```
</file>
"""
    assert parse_file_blocks(response) == [
        ("sample-project/src/demo/catalog.py", "value = 1\n")
    ]


def test_parse_rejects_plain_diff() -> None:
    assert parse_file_blocks("--- a/file.py\n+++ b/file.py") == []


def test_validate_target_accepts_source_path(settings: Settings) -> None:
    target = validate_target(settings, "sample-project/src/demo/catalog.py")
    assert target.is_relative_to(settings.sample_project_dir / "src")


@pytest.mark.parametrize(
    "path",
    [
        "../outside.py",
        "sample-project/tests/test_catalog.py",
        "sample-project/src/../../outside.py",
        "other/file.py",
    ],
)
def test_validate_target_rejects_unsafe_paths(settings: Settings, path: str) -> None:
    with pytest.raises(MiniMaxError):
        validate_target(settings, path)
