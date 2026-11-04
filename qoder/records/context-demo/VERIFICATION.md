# records/context-demo/ 验证记录

日期：2026-11-04 · Windows · 默认新口径 `SDDCTX_PROJECT_KEY=qoder-sdd` /
`SEEKDB_DATABASE=qoder_sdd`。本文件为文字记录，历史 JSON/log 文件未被改写。
本流程不需要 MiniMax/LLM API key；本记录不包含任何密钥或凭据。

## 命令与结果

### 1. 离线上下文演示（步骤 4 编码修复后的真实复跑）

```bash
.venv\Scripts\python.exe scripts/run_context_demo.py
```

结果：**exit 0**。终端摘要字段（与 `summary.json` 一致）：

- `active_assets`: `17`
- `context_items`: `specs=9, code=3, tests=3`
- `required_source_check`: `pass=11, miss=0, total=11`
- PowerContext 任务状态写入后，`--resume-only` 子进程在**独立操作系统进程**
  中重新加载 Memory 并重建了 `records/context-demo/resume-context.md`；
  写入产生的 `memory_ref` revision 为 `2`
- `requires_minimax_key`: `false`（全程未联系 MiniMax）

### 2. 模块测试

```bash
set PYTHONPATH=src && .venv\Scripts\python.exe -m pytest tests -q
```

结果：**20 passed, 1 skipped**（skipped 为默认关闭的 seekdb 集成用例）。
含本提交新增的 `tests/test_context_demo.py`（纯函数与 `-X utf8 -B` 子进程
参数断言）。

### 3. seekdb 集成测试

```bash
set SDDCTX_RUN_INTEGRATION=1 && set PYTHONPATH=src && .venv\Scripts\python.exe -m pytest -q tests/test_seekdb_integration.py
```

结果：**1 passed**。

### 4. 体检

```bash
.venv\Scripts\sddctx.exe doctor
```

结果：**PASS** seekdb `127.0.0.1:2881/qoder_sdd, assets=17`；
**PASS** PowerContext `saved_task=True`。本地体检时 MiniMax key 已配置，
但其值不写入记录；本演示及其他上下文流程均未使用该 key（仅
`sddctx dev` 需要）。

## 证据路径

- `records/context-demo/context.md` · 构建的开发上下文
- `records/context-demo/context.json` · 含 `query_trace` 的原始输出
- `records/context-demo/context.check.md` · 11/11 PASS 校验
- `records/context-demo/resume-context.md` · 独立子进程重建的恢复上下文
- `records/context-demo/resume-context.check.md` · 恢复后再次校验
- `records/context-demo/summary.json` · 上述字段的结构化摘要
- 运行时的新增 SQL/状态日志行追加在 `records/db-query-log.md` 与
  `records/powercontext-log.md` 末尾（既有历史行未改动）

## 与历史证据的关系

本记录属于**新的 context-only 可运行路径**。`records/verify/` 中的
`before-target`/`before-regression` 两份结构化结果仍是**历史改前证据**
（`minimax-sdd` 口径），两者互不替代；MiniMax 仅为可选运行时改码模型。
