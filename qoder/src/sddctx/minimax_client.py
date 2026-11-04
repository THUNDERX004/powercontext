"""Minimal MiniMax OpenAI-compatible chat client."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from sddctx.config import Settings, redact


class MiniMaxError(RuntimeError):
    pass


@dataclass(frozen=True)
class ChatResponse:
    content: str
    model: str
    usage: dict[str, Any]
    finish_reason: str | None
    response_id: str | None
    raw: dict[str, Any]


class MiniMaxClient:
    def __init__(self, settings: Settings) -> None:
        if not settings.minimax_api_key:
            raise MiniMaxError(
                "MiniMax API key is not configured. Set SDDCTX_MINIMAX_API_KEY or MINIMAX_API_KEY."
            )
        self.settings = settings

    def chat(self, system_prompt: str, user_prompt: str) -> ChatResponse:
        endpoint = self.settings.minimax_base_url.rstrip("/") + "/chat/completions"
        payload = {
            "model": self.settings.minimax_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": self.settings.minimax_temperature,
            "max_tokens": self.settings.minimax_max_tokens,
            "stream": False,
        }
        headers = {
            "Authorization": f"Bearer {self.settings.minimax_api_key}",
            "Content-Type": "application/json",
        }
        body: dict[str, Any]
        for attempt in range(3):
            try:
                response = httpx.post(endpoint, json=payload, headers=headers, timeout=600.0)
                if response.status_code in {429, 500, 502, 503, 504} and attempt < 2:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                if response.status_code >= 400:
                    raise MiniMaxError(
                        f"MiniMax HTTP {response.status_code}: {response.text[:1000]}"
                    )
                body = response.json()
                break
            except MiniMaxError:
                raise
            except (httpx.HTTPError, json.JSONDecodeError) as error:
                if attempt < 2:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                raise MiniMaxError(f"MiniMax request failed: {error}") from error
        else:
            raise MiniMaxError("MiniMax request exhausted retries")

        choices = body.get("choices") or []
        if not choices:
            raise MiniMaxError("MiniMax response has no choices")
        message = choices[0].get("message") or {}
        content = message.get("content") or ""
        if not str(content).strip():
            raise MiniMaxError("MiniMax response content is empty")
        return ChatResponse(
            content=str(content),
            model=str(body.get("model") or self.settings.minimax_model),
            usage=dict(body.get("usage") or {}),
            finish_reason=choices[0].get("finish_reason"),
            response_id=body.get("id"),
            raw=body,
        )


def save_exchange(
    run_dir: Path,
    settings: Settings,
    *,
    system_prompt: str,
    user_prompt: str,
    response: ChatResponse,
) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    request = {
        "base_url": settings.minimax_base_url,
        "model": settings.minimax_model,
        "temperature": settings.minimax_temperature,
        "max_tokens": settings.minimax_max_tokens,
        "api_key": redact(settings.minimax_api_key),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    (run_dir / "minimax-request.json").write_text(
        json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    safe_raw = dict(response.raw)
    safe_raw.pop("api_key", None)
    (run_dir / "minimax-response.json").write_text(
        json.dumps(safe_raw, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (run_dir / "minimax-response.md").write_text(
        "# MiniMax response\n\n"
        f"- model: `{response.model}`\n"
        f"- response_id: `{response.response_id}`\n"
        f"- finish_reason: `{response.finish_reason}`\n"
        f"- usage: `{json.dumps(response.usage, ensure_ascii=False)}`\n\n"
        "## Content\n\n"
        f"{response.content}\n",
        encoding="utf-8",
    )


__all__ = ["ChatResponse", "MiniMaxClient", "MiniMaxError", "save_exchange"]
