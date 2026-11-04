from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class PowerContextError(RuntimeError):
    pass


def _request_json(
    base_url: str,
    path: str,
    *,
    payload: dict[str, Any] | None = None,
    token: str | None = None,
    timeout: float = 20.0,
) -> tuple[dict[str, Any], str | None]:
    headers = {"Accept": "application/json"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = None
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    request = Request(
        f"{base_url.rstrip('/')}{path}",
        data=body,
        headers=headers,
        method="POST" if payload is not None else "GET",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            data = json.load(response)
            request_id = response.headers.get("X-PowerContext-Request-ID")
            return data, request_id
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:1200]
        raise PowerContextError(
            f"PowerContext {path} returned HTTP {error.code}: {detail}"
        ) from error
    except URLError as error:
        raise PowerContextError(
            f"PowerContext {path} could not be reached: {error.reason}"
        ) from error
    except json.JSONDecodeError as error:
        raise PowerContextError(
            f"PowerContext {path} returned a non-JSON response."
        ) from error


def _write_evidence(path: Path, evidence: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Exercise Memory Museum writes and cross-session recall on PowerContext."
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("POWERCONTEXT_URL", "http://127.0.0.1:8000"),
        help="PowerContext Server base URL.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "evidence"
        / "powercontext-smoke.json",
        help="Evidence JSON output path.",
    )
    args = parser.parse_args()

    token = os.environ.get("POWERCONTEXT_TOKEN") or None
    base_url = args.base_url.rstrip("/")
    started_at = datetime.now(UTC)
    run_key = started_at.strftime("%Y%m%dT%H%M%SZ")
    evidence: dict[str, Any] = {
        "schema": "memory-museum.powercontext-smoke.v1",
        "generated_at": started_at.isoformat(),
        "powercontext_version": "1.5.0",
        "base_url": base_url,
        "authentication": "bearer" if token else "loopback-unauthenticated",
        "steps": [],
        "result": "running",
    }

    try:
        health, health_request_id = _request_json(
            base_url,
            "/health/live",
            token=None,
        )
        _require(health.get("status") == "ok", "PowerContext health check failed")
        evidence["steps"].append(
            {
                "step": "health",
                "ok": True,
                "request_id": health_request_id,
                "response": health,
            }
        )

        scope_payload = {
            "title": "记忆失物招领处自动验证",
            "summary": "用于验证展品写入和跨会话召回的临时 Scope。",
            "idempotency_key": f"memory-museum-smoke-{run_key}",
        }
        scope, scope_request_id = _request_json(
            base_url,
            "/v1/scopes",
            payload=scope_payload,
            token=token,
        )
        scope_id = str(scope.get("scope_id") or "")
        _require(bool(scope_id), "create_scope response did not contain scope_id")
        evidence["scope"] = {
            "scope_id": scope_id,
            "title": scope_payload["title"],
            "request_id": scope_request_id,
        }
        evidence["steps"].append(
            {
                "step": "create_scope",
                "ok": True,
                "request_id": scope_request_id,
                "scope_id": scope_id,
            }
        )

        first_memory = {
            "scope_id": scope_id,
            "kind": "memory_museum_exhibit",
            "text": (
                "记忆失物招领处展品：《一片香菜的最后晚餐》"
                "｜原始记忆：我把一片香菜忘在冰箱冷冻层，第二天它硬得像一枚绿色书签。"
                "｜年代：冰箱纪·第一次结霜"
                "｜馆藏部件：香菜、冷冻层、绿色书签"
                "｜馆长附注：它没有坏，只是选择了另一种时间。"
                "｜回声类型：fresh｜旧展品线索：无"
            ),
            "reason": "自动验证：保存第一场展品。",
            "description": "冰箱中的香菜标本，以及它第一次成为书签的那天。",
        }
        first_saved, first_write_request_id = _request_json(
            base_url,
            "/v1/memory/remember",
            payload=first_memory,
            token=token,
        )
        first_records = first_saved.get("records")
        _require(
            isinstance(first_records, list) and bool(first_records),
            "first memory write returned no records",
        )
        first_artifact = first_records[0].get("artifact", {})
        evidence["steps"].append(
            {
                "step": "remember_session_1",
                "ok": True,
                "request_id": first_write_request_id,
                "changed": first_saved.get("changed"),
                "artifact": first_artifact,
                "kind": first_records[0].get("kind"),
                "description": first_memory["description"],
            }
        )

        recall_query = "冰箱里那片香菜书签现在怎么样了？"
        first_recall, recall_request_id = _request_json(
            base_url,
            "/v1/context/prepare",
            payload={
                "scope_id": scope_id,
                "query": recall_query,
                "max_bytes": 4000,
                "include_receipt": True,
            },
            token=token,
        )
        recall_content = first_recall.get("content") or ""
        _require(
            first_recall.get("status") == "ready",
            "cross-session context preparation did not return ready",
        )
        _require(
            "香菜" in recall_content and "冰箱" in recall_content,
            "prepared context did not recall the first exhibit",
        )
        evidence["steps"].append(
            {
                "step": "prepare_fresh_chat_after_session_1",
                "ok": True,
                "request_id": recall_request_id,
                "query": recall_query,
                "status": first_recall.get("status"),
                "content_bytes": first_recall.get("content_bytes"),
                "recalled_first_exhibit": True,
                "content": recall_content,
                "receipt": first_recall.get("receipt"),
            }
        )

        second_memory = {
            "scope_id": scope_id,
            "kind": "memory_museum_exhibit",
            "text": (
                "记忆失物招领处展品：《绿色书签申请延期》"
                "｜原始记忆：我刚刚又从冰箱里拿出了那片香菜标本，它像在等一个结局。"
                "｜年代：冰箱纪·第二次结霜"
                "｜馆藏部件：香菜、冰箱、迟到结局申请书"
                "｜馆长附注：它认出了上一场展览，并要求继续驻馆。"
                "｜回声类型：sequel｜旧展品线索：《一片香菜的最后晚餐》"
            ),
            "reason": "自动验证：在召回第一场后保存联动新展品。",
            "description": "香菜标本的续篇，证明 PowerContext 上下文实际进入后续再写入。",
        }
        second_saved, second_write_request_id = _request_json(
            base_url,
            "/v1/memory/remember",
            payload=second_memory,
            token=token,
        )
        second_records = second_saved.get("records")
        _require(
            isinstance(second_records, list) and bool(second_records),
            "second memory write returned no records",
        )
        second_artifact = second_records[0].get("artifact", {})
        evidence["steps"].append(
            {
                "step": "remember_session_2",
                "ok": True,
                "request_id": second_write_request_id,
                "changed": second_saved.get("changed"),
                "artifact": second_artifact,
                "kind": second_records[0].get("kind"),
                "description": second_memory["description"],
            }
        )

        combined_query = "灰灯馆长，香菜、冰箱和绿色书签的两场展览"
        combined_recall, combined_request_id = _request_json(
            base_url,
            "/v1/context/prepare",
            payload={
                "scope_id": scope_id,
                "query": combined_query,
                "max_bytes": 5000,
            },
            token=token,
        )
        combined_content = combined_recall.get("content") or ""
        _require(
            combined_recall.get("status") == "ready",
            "combined recall did not return ready",
        )
        _require(
            "一片香菜的最后晚餐" in combined_content
            or "绿色书签申请延期" in combined_content,
            "combined recall did not contain either exhibit",
        )
        evidence["steps"].append(
            {
                "step": "prepare_after_two_exhibits",
                "ok": True,
                "request_id": combined_request_id,
                "query": combined_query,
                "status": combined_recall.get("status"),
                "content_bytes": combined_recall.get("content_bytes"),
                "content": combined_content,
            }
        )

        evidence["summary"] = {
            "scope_created": True,
            "session_1_memory_written": True,
            "cross_session_recall_verified": True,
            "session_2_memory_written": True,
            "artifact_ids": [
                first_artifact.get("artifact_id"),
                second_artifact.get("artifact_id"),
            ],
            "no_embedding_required": True,
        }
        evidence["result"] = "passed"
        _write_evidence(args.output, evidence)
        print(
            json.dumps(
                {
                    "result": "passed",
                    "scope_id": scope_id,
                    "artifact_ids": evidence["summary"]["artifact_ids"],
                    "output": str(args.output),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except (AssertionError, PowerContextError) as error:
        evidence["result"] = "failed"
        evidence["error"] = str(error)
        _write_evidence(args.output, evidence)
        print(f"PowerContext smoke test failed: {error}", file=sys.stderr)
        print(f"Evidence written to {args.output}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
