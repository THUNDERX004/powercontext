"""Demonstrate that a changed specification is visible after re-import."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sddctx.config import Settings
from sddctx.context_builder import build_context, context_markdown
from sddctx.importer import run_import

TASK = (
    "为 Catalog.search 增加 min_year 年份下限筛选，验证更新后的规格内容被重新读取"
)
MARKER = "续演验证标记-2026"


def main() -> int:
    settings = Settings.load()
    spec_path = settings.specs_dir / "SPEC-002-书目录查询.md"
    original = spec_path.read_text(encoding="utf-8")
    output_dir = settings.records_dir / "spec-update-demo"
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        marker_line = (
            "- SPEC-002-2: 提供 `min_year` 时，只返回出版年份大于或等于 `min_year` "
            f"的书籍；等于边界时必须返回。{MARKER}：本句变更后重新导入，上下文必须读取新内容。"
        )
        lines = original.splitlines()
        updated = "\n".join(
            marker_line if line.startswith("- SPEC-002-2:") else line for line in lines
        ) + "\n"
        spec_path.write_text(updated, encoding="utf-8")
        run_import(settings)
        context = build_context(settings, TASK, with_state=False)
        matches = [
            item
            for item in context.specs
            if item.path.endswith("#SPEC-002-2") and MARKER in item.content
        ]
        markdown = context_markdown(context)
        (output_dir / "context-after-update.md").write_text(markdown, encoding="utf-8")
        result = {
            "marker": MARKER,
            "entry_found": bool(matches),
            "entry_version": matches[0].version if matches else None,
            "entry_source": matches[0].path if matches else None,
            "content": matches[0].content if matches else None,
        }
        (output_dir / "result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if matches else 1
    finally:
        spec_path.write_text(original, encoding="utf-8")
        run_import(settings)


if __name__ == "__main__":
    raise SystemExit(main())
