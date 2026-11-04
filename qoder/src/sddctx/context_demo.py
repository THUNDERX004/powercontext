"""Pure helpers for the offline context-only demo (scripts/run_context_demo.py).

No I/O here: the script composes these with seekdb, PowerContext, and subprocess.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from sddctx.models import BuiltContext

DEMO_DIR_NAME = "context-demo"
TASK_ID = "catalog-year-filter"
OBJECTIVE = "为 Catalog.search 增加 min_year 年份下限筛选并验证兼容性"
COMPLETED_STEPS = ["导入规格、代码和测试资料", "构建并校验开发上下文"]
PENDING_STEPS = ["跨进程 resume 恢复任务状态（本演示到此完成）"]


def demo_paths(home: Path) -> dict[str, Path]:
    """Fresh evidence paths under records/context-demo/; never touches history."""
    base = Path(home) / "records" / DEMO_DIR_NAME
    return {
        "dir": base,
        "context_md": base / "context.md",
        "context_json": base / "context.json",
        "check_md": base / "context.check.md",
        "resume_md": base / "resume-context.md",
        "resume_check_md": base / "resume-context.check.md",
        "summary_json": base / "summary.json",
    }


def context_counts(context: BuiltContext) -> dict[str, int]:
    return {
        "specs": len(context.specs),
        "code": len(context.code),
        "tests": len(context.tests),
    }


def summarize_check_lines(lines: list[str]) -> dict[str, int]:
    passed = sum(1 for line in lines if line.startswith("- PASS"))
    missed = sum(1 for line in lines if line.startswith("- MISS"))
    return {"pass": passed, "miss": missed, "total": passed + missed}


def resume_command(script_path: Path) -> list[str]:
    """argv that launches this same script as a separate OS process.

    -X utf8 forces UTF-8 child stdio (Windows otherwise emits the legacy ANSI
    code page and Chinese JSON breaks); -B suppresses __pycache__ side effects.
    """
    return [
        sys.executable,
        "-X",
        "utf8",
        "-B",
        str(Path(script_path).resolve()),
        "--resume-only",
    ]


def build_demo_summary(
    *,
    project_key: str,
    seekdb_database: str,
    active_assets: int,
    counts: dict[str, int],
    check: dict[str, int],
    citation: dict[str, Any] | None,
    resume: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "demo": "context-only (offline, no MiniMax/LLM key)",
        "requires_minimax_key": False,
        "project_key": project_key,
        "seekdb_database": seekdb_database,
        "active_assets": active_assets,
        "context_items": counts,
        "required_source_check": check,
        "powercontext_citation": citation,
        "resume": resume,
    }
