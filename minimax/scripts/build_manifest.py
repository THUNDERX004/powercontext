"""Generate a machine-readable submission manifest from checked-in evidence."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
RECORDS = ROOT / "records"
BASELINE = "d647275c308e09b7b623f322a26f5c4e85734fb0"


def _git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=REPO,
        text=True,
        encoding="utf-8",
    ).strip()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _latest(pattern: str) -> dict:
    files = sorted(RECORDS.joinpath("verify").glob(pattern), key=lambda path: path.stat().st_mtime)
    if not files:
        return {}
    data = json.loads(files[-1].read_text(encoding="utf-8"))
    return {
        "phase": data["phase"],
        "suite": data["suite"],
        "accepted": data["accepted"],
        "exit_code": data["exit_code"],
        "passed": data["passed_count"],
        "failed": data["failed_count"],
        "code_version": data["code_version"],
        "log": data["log_path"],
    }


def main() -> int:
    task = json.loads(
        (ROOT / "examples" / "catalog-year-filter" / "task.json").read_text(encoding="utf-8")
    )
    context = json.loads(
        (RECORDS / "context-task-001.json").read_text(encoding="utf-8")
    )
    actual_sources = {
        "required_spec_sources": {item["path"] for item in context["specs"]},
        "required_code_sources": {item["path"] for item in context["code"]},
        "required_test_sources": {item["path"] for item in context["tests"]},
    }
    required_sources = {
        field: [
            {"path": source, "present": source in actual_sources[field]}
            for source in task[field]
        ]
        for field in actual_sources
    }
    run_dirs = sorted(
        path
        for path in (RECORDS / "minimax").glob("catalog-year-filter-*")
        if (path / "applied-files.json").is_file()
    )
    minimax_dir = run_dirs[-1]
    minimax = json.loads((minimax_dir / "applied-files.json").read_text(encoding="utf-8"))
    artifacts = {}
    for relative in (
        "README.md",
        "docs/RUNBOOK.md",
        "docs/VALIDATION.md",
        "SUBMISSION.md",
        "sample-project/src/bookdesk/catalog.py",
        "records/module-tests.log",
        "records/context-task-001.md",
        "records/context-task-001.check.md",
        "records/db-query-log.md",
        "records/powercontext-log.md",
        "records/resume-context.md",
        minimax_dir.relative_to(ROOT).as_posix() + "/code.diff.md",
        minimax_dir.relative_to(ROOT).as_posix() + "/devlog.md",
    ):
        path = ROOT / relative
        artifacts[relative] = {"sha256": _sha256(path), "bytes": path.stat().st_size}

    branch = _git("branch", "--show-current")
    head = _git("rev-parse", "HEAD")
    tests = {
        "before_target": _latest("before-target-*.json"),
        "before_regression": _latest("before-regression-*.json"),
        "after_target": _latest("after-target-*.json"),
        "after_regression": _latest("after-regression-*.json"),
        "after_all": _latest("after-all-*.json"),
        "module_log": "records/module-tests.log",
    }
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASELINE, head],
        cwd=REPO,
        check=False,
    ).returncode == 0
    manifest = {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "baseline_branch": "2026-competition-ecosystem",
        "baseline_commit": BASELINE,
        "baseline_is_ancestor": ancestor,
        "branch": branch,
        "validated_code_commit": tests["after_all"]["code_version"].split("+", 1)[0],
        "evidence_snapshot_commit": head,
        "task": task,
        "required_sources": required_sources,
        "required_sources_all_present": all(
            entry["present"]
            for group in required_sources.values()
            for entry in group
        ),
        "database": {
            "backend": "seekdb 1.4 through MySQL protocol",
            "indexed_assets": 17,
            "query_log": "records/db-query-log.md",
        },
        "powercontext": {
            "server": "powercontext 1.2.0",
            "task_id": "catalog-year-filter",
            "resume_context": "records/resume-context.md",
            "event_log": "records/powercontext-log.md",
        },
        "minimax": {
            "provider": "MiniMax",
            "model": minimax["model"],
            "response_id": minimax["response_id"],
            "usage": minimax["usage"],
            "run_dir": minimax_dir.relative_to(ROOT).as_posix(),
            "applied": minimax["applied"],
        },
        "tests": tests,
        "artifacts": artifacts,
    }
    output = RECORDS / "submission-manifest.json"
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)
    return 0 if manifest["baseline_is_ancestor"] and manifest["required_sources_all_present"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
