from __future__ import annotations

import json

import sddctx.agent as agent_module
from sddctx.config import Settings
from sddctx.minimax_client import ChatResponse
from sddctx.models import BuiltContext, ContextItem, TaskState


def test_dev_pipeline_records_and_applies_minimax_file(
    settings: Settings, monkeypatch
) -> None:
    source = settings.sample_project_dir / "src" / "demo" / "catalog.py"
    source.write_text("def search(min_year=None):\n    return []\n", encoding="utf-8")
    item = ContextItem(
        kind="code",
        path="sample-project/src/demo/catalog.py",
        title="catalog",
        symbol="search",
        version=1,
        score=1.0,
        content=source.read_text(encoding="utf-8"),
    )
    context = BuiltContext(
        task="implement filter",
        project_key=settings.project_key,
        specs=[],
        code=[item],
        tests=[],
        state=TaskState(task_id="task", objective="implement filter"),
        state_error=None,
        query_trace=[],
    )
    replacement = (
        '<file path="sample-project/src/demo/catalog.py">\n'
        "```python\n"
        "def search(min_year=None):\n"
        "    return [min_year]\n"
        "```\n"
        "</file>"
    )

    class StubClient:
        def __init__(self, _settings: Settings) -> None:
            pass

        def chat(self, system_prompt: str, user_prompt: str) -> ChatResponse:
            assert "complete replacement" in user_prompt
            return ChatResponse(
                content=replacement,
                model="MiniMax-test",
                usage={"total_tokens": 10},
                finish_reason="stop",
                response_id="resp-test",
                raw={"id": "resp-test", "model": "MiniMax-test"},
            )

    class StubState:
        def __init__(self, _settings: Settings) -> None:
            self.state = TaskState(task_id="task", objective="implement filter")

        def load(self, _task_id: str) -> TaskState:
            return self.state

        def update(self, *_args, **_kwargs) -> TaskState:
            return self.state

        def save(self, state: TaskState) -> dict:
            self.state = state
            return {}

    monkeypatch.setattr(agent_module, "build_context", lambda *_args, **_kwargs: context)
    monkeypatch.setattr(agent_module, "MiniMaxClient", StubClient)
    monkeypatch.setattr(agent_module, "PowerContextState", StubState)

    run_dir = agent_module.run_dev(settings, "implement filter", "task")
    assert "return [min_year]" in source.read_text(encoding="utf-8")
    assert (run_dir / "before" / "sample-project" / "src" / "demo" / "catalog.py").is_file()
    assert "return [min_year]" in (run_dir / "code.diff.md").read_text(encoding="utf-8")
    manifest = json.loads((run_dir / "applied-files.json").read_text(encoding="utf-8"))
    assert manifest["model"] == "MiniMax-test"
    assert manifest["response_id"] == "resp-test"
