from __future__ import annotations

import json

from sddctx.context_builder import context_markdown, required_sources
from sddctx.models import BuiltContext, ContextItem, TaskState


def _item(kind: str, path: str) -> ContextItem:
    return ContextItem(
        kind=kind,
        path=path,
        title=path,
        symbol="",
        version=2,
        score=1.5,
        content=f"content for {path}",
    )


def test_context_contains_sources_and_powercontext_state() -> None:
    context = BuiltContext(
        task="demo",
        project_key="test",
        specs=[_item("spec_entry", "specs/S.md#S-1")],
        code=[_item("code", "sample-project/src/a.py")],
        tests=[_item("test", "sample-project/tests/test_a.py")],
        state=TaskState(
            task_id="task",
            objective="demo",
            completed=["import"],
            pending=["verify"],
            updated_at="2026-01-01T00:00:00Z",
        ),
        state_error=None,
        query_trace=[],
    )
    markdown = context_markdown(context)
    assert "specs/S.md#S-1" in markdown
    assert "sample-project/src/a.py" in markdown
    assert "sample-project/tests/test_a.py" in markdown
    assert 'completed: ["import"]' in markdown
    assert "pending" in markdown


def test_required_sources_compares_exact_paths() -> None:
    context = BuiltContext(
        task="demo",
        project_key="test",
        specs=[_item("spec_entry", "specs/S.md#S-1")],
        code=[_item("code", "sample-project/src/a.py")],
        tests=[],
        state=None,
        state_error=None,
        query_trace=[],
    )
    definition = json.loads(
        '{"required_spec_sources":["specs/S.md#S-1"],'
        '"required_code_sources":["sample-project/src/a.py"],'
        '"required_test_sources":["sample-project/tests/test_a.py"]}'
    )
    ok, lines = required_sources(context, definition)
    assert not ok
    assert sum(line.startswith("- PASS") for line in lines) == 2
    assert any(line.startswith("- MISS") for line in lines)
