"""Run the end-to-end validation workflow from a clean business-project snapshot."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sddctx.agent import run_dev
from sddctx.config import Settings
from sddctx.context_builder import build_context, required_sources, write_context
from sddctx.importer import run_import
from sddctx.state import PowerContextState
from sddctx.verifier import run_verify


def main() -> int:
    settings = Settings.load()
    definition = json.loads(
        (ROOT / "examples" / "catalog-year-filter" / "task.json").read_text(encoding="utf-8")
    )
    task_id = definition["task_id"]
    task = definition["task"]

    imported = run_import(settings)
    print(
        f"[1/7] import: inserted={imported.inserted}, updated={imported.updated}, "
        f"unchanged={imported.unchanged}, total={imported.total}"
    )

    context = build_context(settings, task, with_state=True)
    ok, lines = required_sources(context, definition)
    write_context(settings.records_dir / "context-task-001.md", context)
    (settings.records_dir / "context-task-001.json").write_text(
        json.dumps(context.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (settings.records_dir / "context-task-001.check.md").write_text(
        "# Context source check\n\n" + "\n".join(lines) + "\n", encoding="utf-8"
    )
    if not ok:
        print("Required context sources are missing; see context-task-001.check.md")
        return 1
    print("[2/7] context: all required sources present")

    before_target = run_verify(
        settings, task_id=task_id, phase="before", suite="target", expect="fail"
    )
    before_regression = run_verify(
        settings, task_id=task_id, phase="before", suite="regression", expect="pass"
    )
    if not before_target.accepted or not before_regression.accepted:
        print("[3/7] before verification rejected")
        return 1
    print("[3/7] before verification: target failed for behavior; regression passed")

    state_client = PowerContextState(settings)
    state_client.update(
        task_id,
        objective=task,
        complete=["导入规格、代码和测试资料", "构建开发上下文", "修改前目标测试失败"],
        pending=["使用 MiniMax 修改代码", "运行目标及回归测试"],
    )
    print("[4/7] PowerContext: initial task state saved")

    if not settings.minimax_api_key:
        print(
            "[BLOCKED] SDDCTX_MINIMAX_API_KEY is not configured. "
            "Set it in minimax/.env, then rerun this script from a clean sample-project."
        )
        return 2
    run_dir = run_dev(settings, task, task_id)
    print(f"[5/7] MiniMax: applied modification, evidence={run_dir.relative_to(ROOT).as_posix()}")

    run_import(settings)
    after_target = run_verify(
        settings, task_id=task_id, phase="after", suite="target", expect="pass"
    )
    after_regression = run_verify(
        settings, task_id=task_id, phase="after", suite="regression", expect="pass"
    )
    after_all = run_verify(settings, task_id=task_id, phase="after", suite="all", expect="pass")
    if not (after_target.accepted and after_regression.accepted and after_all.accepted):
        print("[6/7] after verification rejected")
        return 1
    print("[6/7] after verification: target, regression and full suite passed")

    restored = state_client.load(task_id)
    resumed = build_context(settings, restored.objective if restored else task, with_state=True)
    write_context(settings.records_dir / "resume-context.md", resumed)
    print("[7/7] PowerContext: saved state reloaded into records/resume-context.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
