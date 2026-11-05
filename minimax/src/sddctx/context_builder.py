"""Build a source-grounded development context from seekdb query results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sddctx.analyzer import extract_identifiers
from sddctx.config import Settings
from sddctx.models import BuiltContext, ContextItem, SearchHit, TaskState
from sddctx.seekdb_store import SeekDBStore
from sddctx.state import PowerContextState, StateError


def _identifier_bonus(hit: SearchHit, identifiers: list[str]) -> float:
    if not identifiers:
        return 0.0
    haystack = f"{hit.asset.path}\n{hit.asset.symbol}\n{hit.asset.content}".casefold()
    matches = sum(1 for identifier in identifiers if identifier.casefold() in haystack)
    return min(matches * 0.75, 3.0)


def _select(
    store: SeekDBStore,
    task: str,
    *,
    kind: str,
    limit: int,
    purpose: str,
) -> list[ContextItem]:
    identifiers = extract_identifiers(task)
    hits = store.search(task, (kind,), limit=max(limit * 3, limit), purpose=purpose)
    ranked = sorted(
        ((hit, hit.score + _identifier_bonus(hit, identifiers)) for hit in hits),
        key=lambda item: (-item[1], item[0].asset.path),
    )
    selected: list[ContextItem] = []
    seen: set[str] = set()
    for hit, score in ranked:
        if hit.asset.asset_id in seen:
            continue
        seen.add(hit.asset.asset_id)
        selected.append(
            ContextItem(
                kind=hit.asset.kind,
                path=hit.asset.path,
                title=hit.asset.title,
                symbol=hit.asset.symbol,
                version=hit.asset.version,
                score=round(score, 4),
                content=hit.asset.content,
            )
        )
        if len(selected) >= limit:
            break
    return selected


def build_context(settings: Settings, task: str, *, with_state: bool = True) -> BuiltContext:
    store = SeekDBStore(settings)
    specs = _select(store, task, kind="spec_entry", limit=10, purpose="context:spec")
    code = _select(store, task, kind="code", limit=6, purpose="context:code")
    tests = _select(store, task, kind="test", limit=6, purpose="context:test")
    state: TaskState | None = None
    state_error: str | None = None
    if with_state:
        try:
            state = PowerContextState(settings).load("catalog-year-filter")
        except StateError as error:
            state_error = str(error)
    return BuiltContext(
        task=task,
        project_key=settings.project_key,
        specs=specs,
        code=code,
        tests=tests,
        state=state,
        state_error=state_error,
        query_trace=store.query_log.entries,
    )


def required_sources(context: BuiltContext, task_definition: dict[str, Any]) -> tuple[bool, list[str]]:
    actual = {
        "required_spec_sources": {item.path for item in context.specs},
        "required_code_sources": {item.path for item in context.code},
        "required_test_sources": {item.path for item in context.tests},
    }
    lines: list[str] = []
    ok = True
    labels = {
        "required_spec_sources": "规格",
        "required_code_sources": "代码",
        "required_test_sources": "测试",
    }
    for field, label in labels.items():
        for source in task_definition.get(field, []):
            found = source in actual[field]
            ok = ok and found
            lines.append(f"- {'PASS' if found else 'MISS'} {label}: `{source}`")
    return ok, lines


def context_markdown(context: BuiltContext) -> str:
    lines = [
        f"# SDD Development Context: {context.task}",
        "",
        f"- Project: `{context.project_key}`",
        "",
        "## Applicable specification entries",
        "",
    ]
    for item in context.specs:
        lines.extend(
            [
                f"### [{item.title}] `{item.path}` (v{item.version}, score={item.score})",
                "",
                item.content,
                "",
            ]
        )
    lines.extend(["## Relevant code", ""])
    for item in context.code:
        lines.extend(
            [
                f"### `{item.path}` (v{item.version}, score={item.score})",
                f"Symbols: `{item.symbol}`",
                "",
                "```python",
                item.content.rstrip(),
                "```",
                "",
            ]
        )
    lines.extend(["## Verification tests", ""])
    for item in context.tests:
        lines.extend(
            [
                f"### `{item.path}` (v{item.version}, score={item.score})",
                f"Symbols: `{item.symbol}`",
                "",
                "```python",
                item.content.rstrip(),
                "```",
                "",
            ]
        )
    lines.extend(["## Task state (PowerContext)", ""])
    if context.state:
        state = context.state
        lines.extend(
            [
                f"- task_id: `{state.task_id}`",
                f"- objective: {state.objective}",
                f"- completed: {json.dumps(state.completed, ensure_ascii=False)}",
                f"- pending: {json.dumps(state.pending, ensure_ascii=False)}",
                f"- verifications: `{len(state.verifications)}`",
                f"- updated_at: `{state.updated_at}`",
            ]
        )
    elif context.state_error:
        lines.append(f"- PowerContext unavailable: {context.state_error}")
    else:
        lines.append("- No saved task state.")
    return "\n".join(lines).rstrip() + "\n"


def write_context(path: Path, context: BuiltContext) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(context_markdown(context), encoding="utf-8")


__all__ = ["build_context", "context_markdown", "required_sources", "write_context"]
