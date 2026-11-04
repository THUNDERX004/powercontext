"""PowerContext-backed task progress and verification state."""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from typing import Any

from sddctx.config import Settings
from sddctx.models import TaskState

_SCOPE_PREFIX = "sddctx"
_TASK_QUERY = "sddctx task-state"


class StateError(RuntimeError):
    """PowerContext is unavailable or returned an invalid response."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class PowerContextState:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._scope_id: str | None = None

    def _client(self):
        from powercontext.client import PowerContextClient

        return PowerContextClient(
            self.settings.powercontext_url,
            token=self.settings.powercontext_token,
            timeout=30.0,
            allow_insecure_http=True,
        )

    def _log(self, action: str, payload: dict[str, Any]) -> None:
        path = self.settings.powercontext_log
        path.parent.mkdir(parents=True, exist_ok=True)
        header = "" if path.exists() else (
            "# PowerContext 状态写入与复用记录\n\n"
            "由 `sddctx` 自动追加。记录仅包含任务摘要与 Memory 引用，不包含凭据。\n\n"
        )
        with path.open("a", encoding="utf-8") as handle:
            if header:
                handle.write(header)
            handle.write(f"## {_now()} — {action}\n\n")
            handle.write("```json\n")
            handle.write(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
            handle.write("\n```\n\n")

    async def _ensure_scope(self, client) -> str:
        from powercontext.http import CreateScopeRequest, ScopeQueryField

        if self._scope_id:
            return self._scope_id
        title = f"{_SCOPE_PREFIX}:{self.settings.project_key}"
        page = await client.list_scopes(query=title, query_field=ScopeQueryField.TITLE, limit=20)
        for descriptor in page.items:
            if descriptor.title == title:
                self._scope_id = descriptor.scope_id
                self._log("scope.reuse", {"scope_id": descriptor.scope_id, "title": title})
                return descriptor.scope_id
        created = await client.create_scope(
            CreateScopeRequest(
                title=title,
                summary="SDD task progress and verification state",
                idempotency_key=f"sddctx-scope-{self.settings.project_key}",
            )
        )
        self._scope_id = created.scope_id
        self._log("scope.create", {"scope_id": created.scope_id, "title": title})
        return created.scope_id

    async def _save(self, state: TaskState) -> dict[str, Any]:
        from powercontext.http import RememberMemoryRequest

        state.updated_at = _now()
        payload = state.to_dict()
        payload.pop("citation", None)
        text = json.dumps(
            {"query_key": f"{_TASK_QUERY} {state.task_id}", **payload},
            ensure_ascii=False,
            separators=(",", ":"),
        )
        if len(text.encode("utf-8")) > 8192:
            raise StateError("task state exceeds PowerContext's 8192-byte Memory limit")
        async with self._client() as client:
            scope_id = await self._ensure_scope(client)
            response = await client.remember_memory(
                RememberMemoryRequest(
                    scope_id=scope_id,
                    kind="sdd-task-state",
                    text=text,
                    reason=f"SDD task state: {state.task_id}",
                )
            )
        citation = (
            response.entry.citation.model_dump(mode="json")
            if response.entry is not None and response.entry.citation is not None
            else None
        )
        self._log(
            "memory.remember",
            {
                "scope_id": scope_id,
                "task_id": state.task_id,
                "completed": state.completed,
                "pending": state.pending,
                "verification_count": len(state.verifications),
                "citation": citation,
            },
        )
        state.citation = citation
        return citation or {}

    async def _load(self, task_id: str) -> TaskState | None:
        from powercontext.http import SearchMemoryRequest

        async with self._client() as client:
            scope_id = await self._ensure_scope(client)
            response = await client.search_memory(
                SearchMemoryRequest(
                    scope_id=scope_id,
                    query=f"{_TASK_QUERY} {task_id}",
                    limit=50,
                    mode="fts",
                )
            )
        candidates: list[TaskState] = []
        for hit in response.hits:
            entry = getattr(hit, "entry", hit)
            text = getattr(entry, "text", None) or ""
            try:
                payload = json.loads(text)
            except (TypeError, json.JSONDecodeError):
                continue
            if not isinstance(payload, dict) or payload.get("query_key") != f"{_TASK_QUERY} {task_id}":
                continue
            payload.pop("query_key", None)
            state = TaskState(
                task_id=str(payload.get("task_id", task_id)),
                objective=str(payload.get("objective", "")),
                completed=list(payload.get("completed", [])),
                pending=list(payload.get("pending", [])),
                verifications=list(payload.get("verifications", [])),
                last_dev_run=payload.get("last_dev_run"),
                updated_at=str(payload.get("updated_at", "")),
            )
            citation = getattr(entry, "citation", None)
            if citation is not None:
                state.citation = citation.model_dump(mode="json")
            candidates.append(state)
        candidates.sort(key=lambda item: item.updated_at, reverse=True)
        state = candidates[0] if candidates else None
        self._log(
            "memory.search",
            {
                "scope_id": scope_id,
                "task_id": task_id,
                "query": f"{_TASK_QUERY} {task_id}",
                "hit_count": len(candidates),
                "selected_updated_at": state.updated_at if state else None,
            },
        )
        return state

    def save(self, state: TaskState) -> dict[str, Any]:
        try:
            return asyncio.run(self._save(state))
        except StateError:
            raise
        except Exception as error:
            raise StateError(f"PowerContext unavailable at {self.settings.powercontext_url}: {error}") from error

    def load(self, task_id: str) -> TaskState | None:
        try:
            return asyncio.run(self._load(task_id))
        except StateError:
            raise
        except Exception as error:
            raise StateError(f"PowerContext unavailable at {self.settings.powercontext_url}: {error}") from error

    def update(
        self,
        task_id: str,
        *,
        objective: str | None = None,
        complete: list[str] | None = None,
        pending: list[str] | None = None,
    ) -> TaskState:
        state = self.load(task_id) or TaskState(task_id=task_id, objective=objective or "")
        if objective:
            state.objective = objective
        for item in complete or []:
            if item not in state.completed:
                state.completed.append(item)
            if item in state.pending:
                state.pending.remove(item)
        for item in pending or []:
            if item not in state.pending and item not in state.completed:
                state.pending.append(item)
        self.save(state)
        return state

    def add_verification(self, task_id: str, result: dict[str, Any]) -> TaskState:
        state = self.load(task_id) or TaskState(task_id=task_id, objective="")
        state.verifications = [
            item
            for item in state.verifications
            if not (
                item.get("suite") == result.get("suite")
                and item.get("phase") == result.get("phase")
            )
        ]
        state.verifications.append(result)
        label = f"{result.get('phase')} {result.get('suite')}"
        is_final_all_suite = (
            result.get("phase") == "after"
            and result.get("suite") == "all"
            and bool(result.get("accepted"))
        )
        if is_final_all_suite:
            if "运行目标及回归测试" not in state.completed:
                state.completed.append("运行目标及回归测试")
            state.pending = [item for item in state.pending if item != "运行目标及回归测试"]
        elif not result.get("accepted") and "运行目标及回归测试" not in state.pending:
            state.pending.append("运行目标及回归测试")
        self._log("verification.attach", {"task_id": task_id, "result": label})
        self.save(state)
        return state


__all__ = ["PowerContextState", "StateError"]
