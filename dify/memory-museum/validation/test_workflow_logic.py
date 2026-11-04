from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any, Callable

import yaml


ROOT = Path(__file__).resolve().parents[1]
DSL_PATH = ROOT / "dsl" / "memory-museum.yml"


def _load_nodes() -> dict[str, dict[str, Any]]:
    document = yaml.safe_load(DSL_PATH.read_text(encoding="utf-8"))
    return {
        str(node["id"]): node for node in document["workflow"]["graph"]["nodes"]
    }


def _load_main(nodes: dict[str, dict[str, Any]], node_id: str) -> Callable[..., dict]:
    namespace: dict[str, Any] = {"__name__": f"memory_museum_{node_id}"}
    exec(str(nodes[node_id]["data"]["code"]), namespace)
    return namespace["main"]


class WorkflowLogicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.nodes = _load_nodes()

    def test_privacy_guard_accepts_normal_memory(self) -> None:
        main = _load_main(self.nodes, "privacy_guard")
        result = main("我把一片香菜忘在冰箱冷冻层，第二天它硬得像书签。")
        self.assertTrue(result["allowed"])
        self.assertIn("香菜", result["memory_text"])
        self.assertEqual(result["reason"], "")

    def test_privacy_guard_blocks_credentials_and_private_identifiers(self) -> None:
        main = _load_main(self.nodes, "privacy_guard")
        blocked = [
            "api_key: sk-this-should-not-be-stored",
            "我的邮箱是 someone@example.com",
            "手机号 13800138000",
            "身份证 11010519491231002X",
            "",
            "长" * 1201,
        ]
        for value in blocked:
            with self.subTest(value=value[:20]):
                result = main(value)
                self.assertFalse(result["allowed"])
                self.assertTrue(result["reason"])
                self.assertEqual(result["memory_text"], "")

    def test_curation_input_distinguishes_ready_empty_and_error(self) -> None:
        main = _load_main(self.nodes, "curation_input")
        ready = main(
            "一片香菜",
            True,
            "success",
            {"content": "旧展品：《一片香菜的最后晚餐》"},
        )
        empty = main("另一片香菜", True, "empty", {"content": None})
        error = main("第三片香菜", False, "error", {})
        self.assertEqual(ready["recall_state"], "echo_found")
        self.assertEqual(empty["recall_state"], "fresh_gallery")
        self.assertEqual(error["recall_state"], "memory_unavailable")

    def test_parse_exhibit_builds_json_encoded_plugin_inputs(self) -> None:
        main = _load_main(self.nodes, "parse_exhibit")
        model_output = json.dumps(
            {
                "exhibit_title": "《香菜的最后晚餐》",
                "era": "冰箱纪·第一次结霜",
                "artifacts": ["香菜", "冷冻层", "绿色书签"],
                "curator_note": "它没有坏，只是选择了另一种时间。",
                "visitor_echo": "它会在下一次结霜时认出你。",
                "echo_kind": "fresh",
                "echo_reference": "",
            },
            ensure_ascii=False,
        )
        result = main(model_output, "我把一片香菜忘在冰箱冷冻层。")
        self.assertEqual(result["memory_kind"], "memory_museum_exhibit")
        self.assertIn("香菜", result["memory_text"])
        self.assertEqual(
            json.loads(result["reason_json"]),
            "访客主动提交一件个人记忆，应用将其策展并保存为可再次检索的馆藏。",
        )
        self.assertLessEqual(len(json.loads(result["memory_description_json"])), 190)
        self.assertIn("新入藏", result["answer_markdown"])

    def test_parse_exhibit_has_safe_fallback(self) -> None:
        main = _load_main(self.nodes, "parse_exhibit")
        result = main("这不是 JSON", "一件没写完的小事")
        self.assertEqual(result["memory_kind"], "memory_museum_exhibit")
        self.assertIn("《一件还在路上的小事》", result["answer_markdown"])
        self.assertIn("一件没写完的小事", result["memory_text"])

    def test_finalize_reports_real_artifact_or_honest_failure(self) -> None:
        main = _load_main(self.nodes, "finalize")
        success = main(
            "展签",
            True,
            "success",
            {
                "changed": True,
                "records": [
                    {
                        "artifact": {
                            "family": "atomic-memory",
                            "artifact_id": "art_test",
                            "revision": 1,
                        }
                    }
                ],
            },
        )
        unknown = main("展签", False, "unknown", {})
        error = main("展签", False, "error", {})
        self.assertIn("art_test", success["final_answer"])
        self.assertIn("没有返回确定的写入结果", unknown["final_answer"])
        self.assertIn("入藏未成功", error["final_answer"])


if __name__ == "__main__":
    unittest.main()
