# Spec Context — 2026 OceanBase 大赛 Qoder 赛道提交清单

## 作品信息

- 作品名：Spec Context / 规格上下文（`sddctx`）
- 作品目录：`qoder/`
- 代码分支：`codex/qoder-contextpack`
- 代码仓库：<https://github.com/THUNDERX004/powercontext/tree/codex/qoder-contextpack>
- 官方基线：`oceanbase/powercontext@d647275c308e09b7b623f322a26f5c4e85734fb0`，
  分支 `2026-competition-ecosystem`
- Qoder 账号显示名：`Thundery`
- Qoder UID：`01a1a55f-8428-7228-b2b4-f13575e1d293`
- 项目网站：待 Qoder Sites 发布后填写

## 一句话介绍

Spec Context 为 AI 编程任务自动组装**当前有效的规格、源码符号、测试与历史进展**，
把“先找对上下文，再让模型改代码”变成可审计、可恢复的工作流。

## 现场体验

前置条件：

1. seekdb 1.4+ 可通过 MySQL 协议访问；
2. Python 3.11+；
3. 按 `docs/RUNBOOK.md` 安装依赖并从 `env.example` 创建 `.env`；
4. 启动 PowerContext Server。

无需任何大模型 API key 的主流程：

```powershell
cd qoder
uv venv .venv --python 3.12
uv pip install --python .venv\Scripts\python.exe -e ".[dev]"
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -X utf8 -B scripts\run_context_demo.py
```

预期结果：

- `qoder_sdd` 中导入 17 个活跃资产；
- 规格/代码/测试上下文规模为 `9 / 3 / 3`；
- 必需来源检查 `11/11 PASS`；
- 任务状态写入 PowerContext，并由独立子进程重新读取；
- 新证据写入 `records/context-demo/`。

## 验收证据

- 运行说明：`docs/RUNBOOK.md`
- 验证样例：`docs/VALIDATION.md`
- 实跑记录：`records/context-demo/VERIFICATION.md`
- 结构化摘要：`records/context-demo/summary.json`
- seekdb 查询审计：`records/context-demo/context.json` 与
  `records/db-query-log.md`
- PowerContext 复用：`records/context-demo/resume-context.md` 与
  `records/powercontext-log.md`
- Qoder 开发记录：`records/qoder/README.md`
- Qoder 原始 CLI 会话：`records/qoder/session-a3e6ee24-6912-4efd-be39-e0811593e66b.jsonl`
- 项目网站源码：`site/`

## 技术分工

| 技术 | 在作品中的作用 |
| --- | --- |
| Qoder | 读取仓库证据并实现静态作品网站、无模型密钥演示、测试与 Windows 编码修复 |
| seekdb 1.4 | 存储规格、代码和测试资产；用 `MATCH … AGAINST` 原生全文检索选择真实上下文 |
| PowerContext 1.2.0 | 保存任务目标、完成项、待办项与验证摘要；独立进程恢复后重建上下文 |
| MiniMax M3.1 Flash | 可选运行时改码模型，仅用于完整 agent 演示；不是 Qoder 开发要求的替代品 |

## 可复现测试

模块测试：

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -X utf8 -B -m pytest -q tests --basetemp=.pytest-tmp\submission
```

最近实测：`20 passed, 1 skipped`。启用 seekdb 集成用例后，
`tests/test_seekdb_integration.py` 为 `1 passed`。

## 提交前检查

- [ ] 将本分支推送到 `origin`
- [ ] 用 Qoder Sites 发布 `site/` 并设置“任何人都可访问”
- [ ] 将公开站点 URL 回填到本文件、README 和网站
- [ ] 用无痕窗口确认站点未登录可访问
- [ ] 上传网站 URL、仓库 URL、运行说明、验证样例、Qoder 开发记录和 Qoder UID
