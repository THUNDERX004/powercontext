from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict, deque
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


EXPECTED_PLUGIN_FILE_SHA256 = (
    "1c9157b2d3fa6732842191b411f957abbee3879991d70a43da064ad6fab0ebc3"
)
EXPECTED_PLUGIN_CHECKSUM = (
    "47a05503b8aa301ef9ea4d319384ba922634061658fb390848d44d0d54ba1ae1"
)


def _check(
    checks: list[dict[str, Any]],
    name: str,
    condition: bool,
    detail: str,
) -> None:
    checks.append({"name": name, "ok": bool(condition), "detail": detail})
    if not condition:
        raise AssertionError(f"{name}: {detail}")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _edges_by_source(edges: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in edges:
        index[str(edge["source"])].append(edge)
    return index


def _reachable_targets(
    edges_by_source: dict[str, list[dict[str, Any]]],
    start: str,
) -> set[str]:
    visited = {start}
    queue = deque([start])
    while queue:
        source = queue.popleft()
        for edge in edges_by_source.get(source, []):
            target = str(edge["target"])
            if target not in visited:
                visited.add(target)
                queue.append(target)
    return visited


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the Memory Museum Dify submission.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "evidence"
        / "submission-validation.json",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    dsl_path = root / "dsl" / "memory-museum.yml"
    plugin_path = root / "plugin" / "powercontext-0.0.1.difypkg"
    checks: list[dict[str, Any]] = []
    evidence: dict[str, Any] = {
        "schema": "memory-museum.submission-validation.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "checks": checks,
        "result": "running",
    }

    try:
        _check(checks, "dsl_exists", dsl_path.is_file(), str(dsl_path))
        _check(checks, "plugin_exists", plugin_path.is_file(), str(plugin_path))

        dsl_text = dsl_path.read_text(encoding="utf-8")
        document = yaml.safe_load(dsl_text)
        _check(checks, "dsl_yaml", isinstance(document, dict), "DSL parses as a mapping")
        _check(checks, "app_kind", document.get("kind") == "app", "kind must be app")
        _check(
            checks,
            "dsl_version",
            document.get("version") == "0.3.1",
            "DSL version must be 0.3.1",
        )
        _check(
            checks,
            "chatflow_mode",
            document.get("app", {}).get("mode") == "advanced-chat",
            "application mode must be advanced-chat",
        )

        workflow = document["workflow"]
        graph = workflow["graph"]
        nodes = graph["nodes"]
        edges = graph["edges"]
        node_by_id = {str(node["id"]): node for node in nodes}
        _check(
            checks,
            "unique_node_ids",
            len(node_by_id) == len(nodes),
            f"{len(nodes)} nodes",
        )

        target_types = {
            str(edge["source"]): node_by_id[str(edge["source"])]["data"]["type"]
            for edge in edges
            if str(edge["source"]) in node_by_id
        }
        for edge in edges:
            source = str(edge["source"])
            target = str(edge["target"])
            _check(
                checks,
                f"edge_endpoints_{edge['id']}",
                source in node_by_id and target in node_by_id,
                f"{source} -> {target}",
            )
            _check(
                checks,
                f"edge_source_type_{edge['id']}",
                edge["data"]["sourceType"] == node_by_id[source]["data"]["type"],
                f"edge declares {edge['data']['sourceType']}",
            )
            _check(
                checks,
                f"edge_target_type_{edge['id']}",
                edge["data"]["targetType"] == node_by_id[target]["data"]["type"],
                f"edge declares {edge['data']['targetType']}",
            )

        edge_index = _edges_by_source(edges)
        reachable = _reachable_targets(edge_index, "start")
        _check(
            checks,
            "success_path",
            {"answer", "prepare_context", "remember_memory", "finalize"}.issubset(
                reachable
            ),
            "normal path reaches both PowerContext tools and final answer",
        )
        _check(
            checks,
            "privacy_path",
            "privacy_answer" in reachable,
            "blocked-input branch reaches its answer",
        )

        branch = node_by_id["privacy_branch"]["data"]
        _check(
            checks,
            "privacy_branch",
            branch.get("type") == "if-else"
            and branch.get("cases", [{}])[0].get("case_id") == "true",
            "boolean true/false branch is present",
        )
        branch_handles = {str(edge["sourceHandle"]) for edge in edge_index["privacy_branch"]}
        _check(
            checks,
            "privacy_handles",
            {"true", "false"}.issubset(branch_handles),
            "IF/ELSE has both branch edges",
        )

        tool_nodes = [
            node
            for node in nodes
            if node.get("data", {}).get("type") == "tool"
            and str(node["data"].get("plugin_id", "")).startswith(
                "knqiufan/powercontext"
            )
        ]
        tool_names = sorted(str(node["data"].get("tool_name")) for node in tool_nodes)
        _check(
            checks,
            "powercontext_tools",
            tool_names == ["pc_prepare_context", "pc_remember"],
            f"found {tool_names}",
        )
        for node in tool_nodes:
            data = node["data"]
            _check(
                checks,
                f"plugin_identity_{node['id']}",
                data.get("provider_id") == "knqiufan/powercontext/powercontext"
                and data.get("plugin_unique_identifier")
                == f"knqiufan/powercontext:0.0.1@{EXPECTED_PLUGIN_CHECKSUM}",
                "provider and plugin unique identifier are pinned",
            )

        llm_nodes = [
            node for node in nodes if node.get("data", {}).get("type") == "llm"
        ]
        _check(checks, "single_llm", len(llm_nodes) == 1, f"{len(llm_nodes)} LLM node")
        code_nodes = [
            node for node in nodes if node.get("data", {}).get("type") == "code"
        ]
        for node in code_nodes:
            compile(str(node["data"]["code"]), str(node["id"]), "exec")
        _check(
            checks,
            "code_nodes_compile",
            len(code_nodes) == 4,
            f"{len(code_nodes)} Python code nodes compile",
        )
        llm_context = llm_nodes[0]["data"].get("context", {})
        _check(
            checks,
            "context_before_llm",
            llm_context.get("enabled") is True
            and llm_context.get("variable_selector")
            == ["prepare_context", "result", "content"],
            "LLM context is connected to the prepared PowerContext content",
        )

        dependencies = document.get("dependencies", [])
        dependency_values = [
            item.get("value", {}).get("plugin_unique_identifier")
            or item.get("value", {}).get("marketplace_plugin_unique_identifier")
            for item in dependencies
        ]
        _check(
            checks,
            "powercontext_dependency",
            f"knqiufan/powercontext:0.0.1@{EXPECTED_PLUGIN_CHECKSUM}"
            in dependency_values,
            "PowerContext dependency is pinned",
        )
        _check(
            checks,
            "model_dependency",
            any(
                str(value).startswith("langgenius/openai_api_compatible:0.0.68@")
                for value in dependency_values
            ),
            "OpenAI-compatible model plugin is pinned",
        )

        secret_patterns = {
            "OpenAI-like secret": r"\bsk-[A-Za-z0-9_-]{20,}\b",
            "literal bearer token": r"Authorization:\s*Bearer\s+(?!<|TOKEN|replace)[A-Za-z0-9._-]{16,}",
            "literal PowerContext token": r"POWERCONTEXT_SERVER_AUTH_TOKEN=(?!replace-)[^\s#]{16,}",
        }
        found_secrets = [
            label
            for label, pattern in secret_patterns.items()
            if re.search(pattern, dsl_text, flags=re.IGNORECASE)
        ]
        _check(
            checks,
            "no_embedded_secrets",
            not found_secrets,
            "no credential-shaped values in DSL"
            if not found_secrets
            else f"found {found_secrets}",
        )

        actual_sha = _sha256(plugin_path)
        _check(
            checks,
            "plugin_file_sha256",
            actual_sha == EXPECTED_PLUGIN_FILE_SHA256,
            actual_sha,
        )

        evidence["dsl"] = {
            "path": str(dsl_path.relative_to(root)),
            "sha256": _sha256(dsl_path),
            "node_count": len(nodes),
            "edge_count": len(edges),
        }
        evidence["plugin"] = {
            "path": str(plugin_path.relative_to(root)),
            "file_sha256": actual_sha,
            "dify_plugin_checksum": EXPECTED_PLUGIN_CHECKSUM,
        }
        evidence["result"] = "passed"
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(
            json.dumps(
                {
                    "result": "passed",
                    "checks": len(checks),
                    "nodes": len(nodes),
                    "edges": len(edges),
                    "output": str(args.output),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except Exception as error:
        evidence["result"] = "failed"
        evidence["error"] = str(error)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Submission validation failed: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
