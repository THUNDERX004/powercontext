"""Command-line entry point for the SDD context manager."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from sddctx import __version__
from sddctx.agent import MiniMaxError, run_dev
from sddctx.config import Settings, redact
from sddctx.context_builder import (
    build_context,
    context_markdown,
    required_sources,
    write_context,
)
from sddctx.importer import run_import
from sddctx.seekdb_store import SeekDBStore
from sddctx.state import PowerContextState, StateError
from sddctx.verifier import run_verify

TASK_ID = "catalog-year-filter"
DEFAULT_TASK = (
    "为 Catalog.search 增加 min_year 年份下限筛选：按 Book.published_year "
    "包含边界，并保持关键词、标签、归档选项与既有排序行为不变。"
)


def _settings() -> Settings:
    return Settings.load()


def _print_import(settings: Settings) -> int:
    result = run_import(settings)
    print(
        f"Imported {result.inserted} new, {result.updated} updated, "
        f"{result.unchanged} unchanged, {result.removed} removed; "
        f"{result.total} active assets."
    )
    print(f"Query audit: {settings.db_query_log}")
    return 0


def cmd_import(_args: argparse.Namespace) -> int:
    return _print_import(_settings())


def cmd_context(args: argparse.Namespace) -> int:
    settings = _settings()
    context = build_context(settings, args.task, with_state=not args.no_state)
    text = context_markdown(context)
    if args.out:
        write_context(Path(args.out), context)
    if args.json:
        print(
            json.dumps(
                context.to_dict(include_content=not args.no_content),
                ensure_ascii=False,
                indent=2,
            )
        )
    elif not args.check:
        print(text)
    if args.check:
        definition = json.loads(Path(args.check).read_text(encoding="utf-8"))
        ok, lines = required_sources(context, definition)
        report = "# Context source check\n\n" + "\n".join(lines) + "\n"
        if args.out:
            Path(args.out).with_suffix(".check.md").write_text(report, encoding="utf-8")
        print(report, file=sys.stderr if ok else sys.stdout)
        return 0 if ok else 1
    return 0


def cmd_dev(args: argparse.Namespace) -> int:
    settings = _settings()
    try:
        run_dir = run_dev(settings, args.task, args.task_id)
    except MiniMaxError as error:
        print(f"MiniMax development failed: {error}", file=sys.stderr)
        return 2
    print(f"MiniMax modification applied. Evidence: {run_dir}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    settings = _settings()
    result = run_verify(
        settings,
        task_id=args.task_id,
        phase=args.phase,
        suite=args.suite,
        expect=args.expect,
    )
    print(result.detail)
    print(f"log: {result.log_path}")
    print(f"code_version: {result.code_version}")
    return 0 if result.accepted else 1


def cmd_status(args: argparse.Namespace) -> int:
    settings = _settings()
    client = PowerContextState(settings)
    try:
        state = client.update(
            args.task_id,
            objective=args.objective,
            complete=args.complete,
            pending=args.pending,
        )
    except StateError as error:
        print(f"PowerContext error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(state.to_dict(), ensure_ascii=False, indent=2))
    return 0


def cmd_resume(args: argparse.Namespace) -> int:
    settings = _settings()
    try:
        state = PowerContextState(settings).load(args.task_id)
    except StateError as error:
        print(f"PowerContext error: {error}", file=sys.stderr)
        return 2
    if state is None:
        print(f"No saved task state for {args.task_id}", file=sys.stderr)
        return 1
    context = build_context(settings, state.objective or DEFAULT_TASK, with_state=True)
    output = settings.records_dir / "resume-context.md"
    write_context(output, context)
    print(
        json.dumps(
            {
                "task_id": state.task_id,
                "completed": state.completed,
                "pending": state.pending,
                "verifications": len(state.verifications),
                "last_dev_run": state.last_dev_run,
                "resume_context": output.relative_to(settings.home).as_posix(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def cmd_doctor(_args: argparse.Namespace) -> int:
    settings = _settings()
    failures = 0
    print("# sddctx doctor")
    try:
        store = SeekDBStore(settings)
        store.initialize()
        count = store.count()
        print(
            f"PASS seekdb: {settings.seekdb_host}:{settings.seekdb_port}/"
            f"{settings.seekdb_database}, assets={count}"
        )
    except Exception as error:
        failures += 1
        print(f"FAIL seekdb: {error}")
    try:
        state = PowerContextState(settings)
        current = state.load(TASK_ID)
        print(f"PASS PowerContext: {settings.powercontext_url}, saved_task={bool(current)}")
    except Exception as error:
        failures += 1
        print(f"FAIL PowerContext: {error}")
    key_state = "configured" if settings.minimax_api_key else "missing (only dev requires it)"
    print(f"{'PASS' if settings.minimax_api_key else 'WARN'} MiniMax key: {key_state}")
    print(
        f"PASS MiniMax endpoint: {settings.minimax_base_url} "
        f"model={settings.minimax_model} key={redact(settings.minimax_api_key)}"
    )
    return 1 if failures else 0


def cmd_reset(args: argparse.Namespace) -> int:
    settings = _settings()
    if not args.yes:
        answer = input(
            f"This deletes {settings.seekdb_database} project rows and generated evidence. "
            "Continue? [y/N] "
        )
        if answer.casefold() != "y":
            print("Cancelled.")
            return 0
    store = SeekDBStore(settings)
    store.initialize()
    with store.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT asset_id FROM engineering_assets WHERE project_key=%s",
                (settings.project_key,),
            )
            assets = [row["asset_id"] for row in cursor.fetchall()]
    store.delete_missing(settings.project_key, [])
    for path in (
        settings.db_query_log,
        settings.powercontext_log,
        settings.records_dir / "resume-context.md",
    ):
        path.unlink(missing_ok=True)
    for directory in (
        settings.records_dir / "verify",
        settings.records_dir / "minimax",
    ):
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)
    print(f"Removed {len(assets)} asset rows and generated evidence.")
    print("Reset business code separately with git checkout -- qoder/sample-project.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sddctx",
        description="Ground development tasks in evolving specs, code, tests, and saved task state.",
    )
    parser.add_argument("--version", action="version", version=f"sddctx {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    command = sub.add_parser("import", help="Import specs, code and tests into seekdb")
    command.set_defaults(func=cmd_import)

    command = sub.add_parser("context", help="Build a source-grounded development context")
    command.add_argument("--task", default=DEFAULT_TASK)
    command.add_argument("--out")
    command.add_argument("--json", action="store_true")
    command.add_argument("--no-content", action="store_true")
    command.add_argument("--no-state", action="store_true")
    command.add_argument("--check", metavar="TASK_JSON")
    command.set_defaults(func=cmd_context)

    command = sub.add_parser("dev", help="Ask MiniMax to apply the task to sample-project")
    command.add_argument("--task", default=DEFAULT_TASK)
    command.add_argument("--task-id", default=TASK_ID)
    command.set_defaults(func=cmd_dev)

    command = sub.add_parser("verify", help="Run tests and save verification evidence")
    command.add_argument("--task-id", default=TASK_ID)
    command.add_argument("--phase", required=True, choices=("before", "after"))
    command.add_argument("--suite", required=True, choices=("target", "regression", "all"))
    command.add_argument("--expect", required=True, choices=("pass", "fail"))
    command.set_defaults(func=cmd_verify)

    command = sub.add_parser("status", help="Save or update task progress in PowerContext")
    command.add_argument("--task-id", default=TASK_ID)
    command.add_argument("--objective")
    command.add_argument("--complete", nargs="*")
    command.add_argument("--pending", nargs="*")
    command.set_defaults(func=cmd_status)

    command = sub.add_parser("resume", help="Read saved state and rebuild the context")
    command.add_argument("--task-id", default=TASK_ID)
    command.set_defaults(func=cmd_resume)

    command = sub.add_parser("doctor", help="Check seekdb, PowerContext and MiniMax configuration")
    command.set_defaults(func=cmd_doctor)

    command = sub.add_parser("reset", help="Remove indexed assets and generated evidence")
    command.add_argument("--yes", action="store_true")
    command.set_defaults(func=cmd_reset)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
