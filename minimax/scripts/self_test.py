"""Run module tests and write a command/exit-code log for submission review."""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sddctx.config import Settings
from sddctx.verifier import code_version


def main() -> int:
    command = [sys.executable, "-m", "pytest", "-q", "tests", "--basetemp", str(ROOT / ".pytest-tmp")]
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(ROOT / "src")
    environment["PYTHONUTF8"] = "1"
    environment["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=180,
        check=False,
        env=environment,
    )
    output = (proc.stdout or "") + (proc.stderr or "")
    log = (
        "# Module self-test\n\n"
        f"- executed_at: `{datetime.now(UTC).isoformat(timespec='seconds')}`\n"
        f"- cwd: `{ROOT}`\n"
        f"- command: `{' '.join(command)}`\n"
        f"- code_version: `{code_version(Settings.load())}`\n"
        f"- exit_code: `{proc.returncode}`\n\n"
        "```text\n"
        f"{output.rstrip()}\n"
        "```\n"
    )
    path = ROOT / "records" / "module-tests.log"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(log, encoding="utf-8")
    print(output, end="")
    print(f"log: {path}")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
