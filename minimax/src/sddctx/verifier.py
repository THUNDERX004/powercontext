"""Run target/regression tests and persist verification evidence."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from sddctx.config import Settings
from sddctx.state import PowerContextState, StateError


@dataclass(frozen=True)
class VerifyResult:
    accepted: bool
    detail: str
    log_path: Path
    code_version: str


def code_version(settings: Settings) -> str:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=settings.home.parent,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        commit = proc.stdout.strip() if proc.returncode == 0 else "unknown"
    except OSError:
        commit = "unknown"
    digest = hashlib.sha256()
    src = settings.sample_project_dir / "src"
    for path in sorted(src.rglob("*.py")):
        digest.update(path.relative_to(settings.home).as_posix().encode("utf-8"))
        normalized = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
        digest.update(normalized.encode("utf-8"))
    return f"{commit}+tree:{digest.hexdigest()[:16]}"


def _summarize(output: str) -> tuple[int, int]:
    passed = sum(int(value) for value in re.findall(r"(\d+) passed", output))
    failed = sum(int(value) for value in re.findall(r"(\d+) failed", output))
    return passed, failed


def run_verify(
    settings: Settings,
    *,
    task_id: str,
    phase: str,
    suite: str,
    expect: str,
) -> VerifyResult:
    if suite == "target":
        tests = ["tests/test_catalog_year_filter.py"]
    elif suite == "regression":
        tests = ["tests/test_catalog_regression.py"]
    elif suite == "all":
        tests = ["tests"]
    else:
        raise ValueError(f"unknown suite: {suite}")

    command = [sys.executable, "-m", "pytest", "-q", *tests]
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(settings.sample_project_dir / "src")
    environment["PYTHONUTF8"] = "1"
    environment["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        command,
        cwd=settings.sample_project_dir,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=180,
        check=False,
        env=environment,
    )
    output = (proc.stdout or "") + (proc.stderr or "")
    verify_dir = settings.records_dir / "verify"
    verify_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    log_path = verify_dir / f"{phase}-{suite}-{stamp}.log"
    log_path.write_text(
        f"$ {' '.join(command)}\n"
        f"cwd={settings.sample_project_dir}\n"
        f"exit_code={proc.returncode}\n\n{output}",
        encoding="utf-8",
    )
    passed, failed = _summarize(output)
    command_failed = proc.returncode != 0
    expected_failure = expect == "fail"
    accepted = command_failed if expected_failure else not command_failed
    # A collection/import error cannot count as an expected feature failure.
    if expected_failure and (
        re.search(r"\b\d+ error", output, re.IGNORECASE)
        or passed == 0
        or failed == 0
    ):
        accepted = False
    detail = (
        f"exit={proc.returncode}, passed={passed}, failed={failed}, expect={expect}"
        if accepted
        else f"Unexpected result: exit={proc.returncode}, passed={passed}, failed={failed}, expect={expect}"
    )
    version = code_version(settings)
    result = {
        "task_id": task_id,
        "phase": phase,
        "suite": suite,
        "command": command,
        "cwd": str(settings.sample_project_dir),
        "exit_code": proc.returncode,
        "passed_count": passed,
        "failed_count": failed,
        "expected": expect,
        "accepted": accepted,
        "detail": detail,
        "log_path": log_path.relative_to(settings.home).as_posix(),
        "code_version": version,
        "executed_at": datetime.now(UTC).isoformat(timespec="seconds"),
    }
    (verify_dir / f"{phase}-{suite}-{stamp}.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    try:
        PowerContextState(settings).add_verification(task_id, result)
    except (StateError, OSError) as error:
        (log_path.parent / f"{phase}-{suite}-{stamp}.state-warning.txt").write_text(
            str(error), encoding="utf-8"
        )
    return VerifyResult(accepted, detail, log_path, version)
