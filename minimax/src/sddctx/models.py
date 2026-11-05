"""Shared typed records for indexing, context assembly and task state."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Asset:
    project_key: str
    asset_id: str
    kind: str
    path: str
    title: str
    symbol: str
    content: str
    content_hash: str
    version: int = 1


@dataclass(frozen=True)
class SearchHit:
    asset: Asset
    score: float


@dataclass
class TaskState:
    task_id: str
    objective: str
    completed: list[str] = field(default_factory=list)
    pending: list[str] = field(default_factory=list)
    verifications: list[dict[str, Any]] = field(default_factory=list)
    last_dev_run: dict[str, Any] | None = None
    updated_at: str = ""
    citation: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ContextItem:
    kind: str
    path: str
    title: str
    symbol: str
    version: int
    score: float
    content: str

    @property
    def source(self) -> str:
        return self.path

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class BuiltContext:
    task: str
    project_key: str
    specs: list[ContextItem]
    code: list[ContextItem]
    tests: list[ContextItem]
    state: TaskState | None
    state_error: str | None
    query_trace: list[dict[str, Any]]

    def to_dict(self, include_content: bool = True) -> dict[str, Any]:
        def item_dict(item: ContextItem) -> dict[str, Any]:
            payload = item.to_dict()
            if not include_content:
                payload.pop("content", None)
            return payload

        return {
            "task": self.task,
            "project_key": self.project_key,
            "specs": [item_dict(item) for item in self.specs],
            "code": [item_dict(item) for item in self.code],
            "tests": [item_dict(item) for item in self.tests],
            "state": self.state.to_dict() if self.state else None,
            "state_error": self.state_error,
            "query_trace": self.query_trace,
        }
