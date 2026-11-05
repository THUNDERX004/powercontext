"""Apply MiniMax-generated full-file replacements inside the sample project."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

from sddctx.config import Settings
from sddctx.context_builder import build_context, context_markdown
from sddctx.minimax_client import MiniMaxClient, MiniMaxError, save_exchange
from sddctx.state import PowerContextState, StateError

_FILE_BLOCK = re.compile(
    r'<file\s+path="(?P<path>[^"]+)">\s*```(?:python)?\s*\n(?P<body>.*?)\n```\s*</file>',
    re.DOTALL,
)

SYSTEM_PROMPT = """You are the implementation step in a Spec-Driven Development loop.
Implement only the requested behavior. Preserve existing public interfaces and
all applicable specifications. Return only complete file replacements using:

<file path="sample-project/src/package/file.py">
```python
<complete file content>
```
</file>

Never return a diff or a partial file. Do not modify tests. Do not write outside
sample-project/src/. Keep the output minimal and deterministic."""


@dataclass(frozen=True)
class AppliedFile:
    path: str
    sha256: str
    bytes_written: int
    existed: bool


def parse_file_blocks(content: str) -> list[tuple[str, str]]:
    return [
        (match.group("path").strip().replace("\\", "/"), match.group("body").rstrip() + "\n")
        for match in _FILE_BLOCK.finditer(content)
    ]


def validate_target(settings: Settings, raw_path: str) -> Path:
    posix = PurePosixPath(raw_path)
    if posix.is_absolute() or ".." in posix.parts:
        raise MiniMaxError(f"unsafe output path: {raw_path}")
    if posix.parts[:2] != ("sample-project", "src"):
        raise MiniMaxError(f"output path must be under sample-project/src: {raw_path}")
    target = (settings.home / Path(*posix.parts)).resolve()
    allowed = (settings.sample_project_dir / "src").resolve()
    if not target.is_relative_to(allowed):
        raise MiniMaxError(f"resolved output path escapes sample-project/src: {raw_path}")
    if target.suffix != ".py":
        raise MiniMaxError(f"only Python source files may be changed: {raw_path}")
    return target


def _safe_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".sddctx.tmp")
    temporary.write_text(content, encoding="utf-8", newline="\n")
    os.replace(temporary, path)


def _write_diff(run_dir: Path, snapshots: dict[str, Path], settings: Settings) -> Path:
    import difflib

    lines = [f"# Code diff: {run_dir.name}", ""]
    for raw_path, before_path in sorted(snapshots.items()):
        target = settings.home / raw_path
        before = before_path.read_text(encoding="utf-8") if before_path.is_file() else ""
        after = target.read_text(encoding="utf-8") if target.is_file() else ""
        lines.extend(
            [
                f"## `{raw_path}`",
                "",
                "```diff",
                *difflib.unified_diff(
                    before.splitlines(),
                    after.splitlines(),
                    fromfile=f"a/{raw_path}",
                    tofile=f"b/{raw_path}",
                    lineterm="",
                ),
                "```",
                "",
            ]
        )
    path = run_dir / "code.diff.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def run_dev(settings: Settings, task: str, task_id: str) -> Path:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_dir = settings.records_dir / "minimax" / f"{task_id}-{stamp}"
    run_dir.mkdir(parents=True, exist_ok=True)

    context = build_context(settings, task, with_state=True)
    markdown = context_markdown(context)
    (run_dir / "context.md").write_text(markdown, encoding="utf-8")
    (run_dir / "context.json").write_text(
        json.dumps(context.to_dict(include_content=True), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    user_prompt = (
        f"# Development task\n\n{task}\n\n"
        "# Selected development context\n\n"
        f"{markdown}\n\n"
        "Return complete replacement files in the required <file> format."
    )
    response = MiniMaxClient(settings).chat(SYSTEM_PROMPT, user_prompt)
    save_exchange(
        run_dir,
        settings,
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response=response,
    )

    blocks = parse_file_blocks(response.content)
    if not blocks:
        raise MiniMaxError(
            f"No complete <file> blocks found in MiniMax output. Inspect {run_dir / 'minimax-response.md'}."
        )

    snapshot_dir = run_dir / "before"
    snapshots: dict[str, Path] = {}
    applied: list[AppliedFile] = []
    for raw_path, content in blocks:
        target = validate_target(settings, raw_path)
        if raw_path not in snapshots:
            snapshot = snapshot_dir / Path(raw_path)
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            if target.is_file():
                snapshot.write_bytes(target.read_bytes())
            snapshots[raw_path] = snapshot
        existed = target.is_file()
        _safe_write(target, content)
        encoded = content.encode("utf-8")
        applied.append(
            AppliedFile(
                path=raw_path,
                sha256=hashlib.sha256(encoded).hexdigest(),
                bytes_written=len(encoded),
                existed=existed,
            )
        )

    manifest = {
        "task_id": task_id,
        "task": task,
        "model": response.model,
        "response_id": response.response_id,
        "usage": response.usage,
        "applied": [asdict(item) for item in applied],
    }
    (run_dir / "applied-files.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    diff_path = _write_diff(run_dir, snapshots, settings)
    (run_dir / "devlog.md").write_text(
        "# MiniMax development record\n\n"
        f"- Task: {task}\n"
        f"- Model: `{response.model}`\n"
        f"- Response ID: `{response.response_id}`\n"
        f"- Usage: `{json.dumps(response.usage, ensure_ascii=False)}`\n"
        f"- Context: `context.md`\n"
        f"- Raw request/response: `minimax-request.json`, `minimax-response.md`\n"
        f"- Diff: `{diff_path.name}`\n\n"
        "## Applied files\n\n"
        + "\n".join(f"- `{item.path}` sha256 `{item.sha256[:16]}...`" for item in applied)
        + "\n",
        encoding="utf-8",
    )
    try:
        state_client = PowerContextState(settings)
        state = state_client.load(task_id) or state_client.update(
            task_id,
            objective=task,
            complete=["构建开发上下文", "修改前目标测试因功能缺失而失败"],
            pending=["运行目标及回归测试"],
        )
        state.last_dev_run = {
            "model": response.model,
            "response_id": response.response_id,
            "run_dir": run_dir.relative_to(settings.home).as_posix(),
            "applied": [asdict(item) for item in applied],
        }
        minimax_item = "使用 MiniMax 修改代码"
        if minimax_item not in state.completed:
            state.completed.append(minimax_item)
        state.pending = [item for item in state.pending if item != minimax_item]
        state_client.save(state)
    except (StateError, OSError) as error:
        (run_dir / "state-warning.txt").write_text(str(error), encoding="utf-8")
    return run_dir


__all__ = ["MiniMaxError", "parse_file_blocks", "run_dev", "validate_target"]
