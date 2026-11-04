"""Offline, context-only demo for reviewers — requires no MiniMax/LLM API key.

Steps (evidence written fresh under records/context-demo/):
  1. import specs, code and tests into seekdb (native FULLTEXT assets);
  2. build the catalog task context and validate all required sources;
  3. save task progress to PowerContext Memory;
  4. reload it in a separate OS process (``--resume-only`` child) and rebuild
     the resume context from the saved objective;
  5. print a concise summary and store summary.json.

Run: ``.venv/bin/python scripts/run_context_demo.py``
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sddctx.config import Settings
from sddctx.context_builder import build_context, required_sources, write_context
from sddctx.context_demo import (
    COMPLETED_STEPS,
    OBJECTIVE,
    PENDING_STEPS,
    TASK_ID,
    build_demo_summary,
    context_counts,
    demo_paths,
    resume_command,
    summarize_check_lines,
)
from sddctx.importer import run_import
from sddctx.state import PowerContextState, StateError

DEFINITION_PATH = ROOT / "examples" / "catalog-year-filter" / "task.json"


def _definition() -> dict:
    return json.loads(DEFINITION_PATH.read_text(encoding="utf-8"))


def _check_report(title: str, lines: list[str]) -> str:
    return f"# {title}\n\n" + "\n".join(lines) + "\n"


def resume_child(settings: Settings) -> int:
    """Runs in a separate OS process launched by main(); reads PowerContext only."""
    paths = demo_paths(settings.home)
    state = PowerContextState(settings).load(TASK_ID)
    if state is None:
        print(f"[resume] no saved task state for {TASK_ID}", file=sys.stderr)
        return 1
    objective = state.objective or _definition()["task"]
    context = build_context(settings, objective, with_state=True)
    ok, lines = required_sources(context, _definition())
    write_context(paths["resume_md"], context)
    paths["resume_check_md"].write_text(
        _check_report("Context source check (resume)", lines), encoding="utf-8"
    )
    check = summarize_check_lines(lines)
    revision = ((state.citation or {}).get("memory_ref") or {}).get("revision")
    print(
        json.dumps(
            {
                "task_id": state.task_id,
                "objective": objective,
                "completed": state.completed,
                "pending": state.pending,
                "memory_revision": revision,
                "check": check,
                "resume_context": paths["resume_md"].relative_to(settings.home).as_posix(),
            },
            ensure_ascii=False,
        )
    )
    return 0 if ok else 1


def main() -> int:
    settings = Settings.load()
    if "--resume-only" in sys.argv:
        try:
            return resume_child(settings)
        except StateError as error:
            print(f"[resume] PowerContext error: {error}", file=sys.stderr)
            return 2

    paths = demo_paths(settings.home)
    paths["dir"].mkdir(parents=True, exist_ok=True)
    task = _definition()["task"]

    print("[1/5] import engineering assets into seekdb")
    try:
        imported = run_import(settings)
    except Exception as error:
        print(f"[BLOCKED] seekdb unavailable ({settings.seekdb_database}): {error}", file=sys.stderr)
        return 2
    print(
        f"      active assets: {imported.total} "
        f"(project_key={settings.project_key}, db={settings.seekdb_database})"
    )

    print("[2/5] build development context and check required sources")
    context = build_context(settings, task, with_state=True)
    ok, lines = required_sources(context, _definition())
    write_context(paths["context_md"], context)
    paths["context_json"].write_text(
        json.dumps(context.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    paths["check_md"].write_text(_check_report("Context source check", lines), encoding="utf-8")
    check = summarize_check_lines(lines)
    if not ok:
        print(f"[FAILED] {check['miss']} required source(s) missing; see {paths['check_md']}")
        return 1
    print(f"      required sources: {check['pass']}/{check['total']} PASS")

    print("[3/5] save task progress to PowerContext")
    try:
        state = PowerContextState(settings).update(
            TASK_ID,
            objective=OBJECTIVE,
            complete=COMPLETED_STEPS,
            pending=PENDING_STEPS,
        )
    except StateError as error:
        print(
            f"[BLOCKED] PowerContext unavailable ({settings.powercontext_url}): {error}. "
            "Steps 1-2 evidence is already under records/context-demo/.",
            file=sys.stderr,
        )
        return 2

    print("[4/5] reload state in a separate OS process and rebuild resume context")
    child = subprocess.run(
        resume_command(Path(__file__)),
        cwd=ROOT,
        capture_output=True,
        text=True,
        # The child prints UTF-8 (enforced by -X utf8); decode it explicitly
        # so the parent never depends on the Windows legacy ANSI code page.
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if child.returncode != 0:
        print(f"[FAILED] resume child exited {child.returncode}: {child.stderr.strip()}", file=sys.stderr)
        return 1
    try:
        resume = json.loads(child.stdout.strip().splitlines()[-1])
    except (AttributeError, IndexError, ValueError):
        print(f"[FAILED] resume child stdout was not JSON: {child.stdout!r}", file=sys.stderr)
        return 1

    print("[5/5] summary")
    summary = build_demo_summary(
        project_key=settings.project_key,
        seekdb_database=settings.seekdb_database,
        active_assets=imported.total,
        counts=context_counts(context),
        check=check,
        citation=state.citation,
        resume=resume,
    )
    paths["summary_json"].write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(
        f"evidence: {paths['dir'].relative_to(ROOT).as_posix()}/ "
        f"(context.md, context.json, context.check.md, "
        f"resume-context.md, resume-context.check.md, summary.json)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
