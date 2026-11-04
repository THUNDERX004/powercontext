from __future__ import annotations

from pathlib import Path

from sddctx.context_demo import (
    build_demo_summary,
    context_counts,
    demo_paths,
    resume_command,
    summarize_check_lines,
)
from sddctx.models import BuiltContext, ContextItem


def _item(kind: str, path: str) -> ContextItem:
    return ContextItem(
        kind=kind, path=path, title=path, symbol="", version=1, score=1.0, content="x"
    )


def _context() -> BuiltContext:
    return BuiltContext(
        task="demo",
        project_key="qoder-sdd",
        specs=[_item("spec_entry", "specs/S.md#S-1")],
        code=[_item("code", "sample-project/src/a.py"), _item("code", "sample-project/src/b.py")],
        tests=[],
        state=None,
        state_error=None,
        query_trace=[],
    )


def test_demo_paths_are_all_under_records_context_demo(tmp_path: Path) -> None:
    paths = demo_paths(tmp_path)
    assert paths["dir"] == tmp_path / "records" / "context-demo"
    for name, path in paths.items():
        if name == "dir":
            continue
        assert path.parent == paths["dir"], name
        assert not path.exists()


def test_summarize_check_lines_counts_pass_and_miss() -> None:
    lines = [
        "- PASS 规格: a",
        "- PASS 代码: b",
        "- MISS 测试: c",
        "not a result line",
    ]
    assert summarize_check_lines(lines) == {"pass": 2, "miss": 1, "total": 3}


def test_summarize_check_lines_all_pass_matches_task_definition_scale() -> None:
    lines = ["- PASS 项: x"] * 11
    summary = summarize_check_lines(lines)
    assert summary == {"pass": 11, "miss": 0, "total": 11}


def test_context_counts_reports_sizes_per_kind() -> None:
    assert context_counts(_context()) == {"specs": 1, "code": 2, "tests": 0}


def test_resume_command_is_self_invocation_with_utf8_flags(tmp_path: Path) -> None:
    script = tmp_path / "run_context_demo.py"
    argv = resume_command(script)
    assert argv[0]  # python executable
    assert argv[1:4] == ["-X", "utf8", "-B"]
    assert argv[4] == str(script.resolve())
    assert argv[-1] == "--resume-only"
    assert len(argv) == 6


def test_build_demo_summary_shape_and_offline_guarantee() -> None:
    summary = build_demo_summary(
        project_key="qoder-sdd",
        seekdb_database="qoder_sdd",
        active_assets=17,
        counts={"specs": 8, "code": 3, "tests": 3},
        check={"pass": 11, "miss": 0, "total": 11},
        citation={"memory_ref": {"revision": 1}},
        resume={"task_id": "catalog-year-filter"},
    )
    assert summary["requires_minimax_key"] is False
    assert summary["project_key"] == "qoder-sdd"
    assert summary["seekdb_database"] == "qoder_sdd"
    assert summary["active_assets"] == 17
    assert summary["context_items"] == {"specs": 8, "code": 3, "tests": 3}
    assert summary["required_source_check"] == {"pass": 11, "miss": 0, "total": 11}
    assert summary["powercontext_citation"] == {"memory_ref": {"revision": 1}}
    assert summary["resume"] == {"task_id": "catalog-year-filter"}
