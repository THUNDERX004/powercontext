# Runbook

## 1. Prerequisites

- Python 3.11 or newer; Python 3.12 is recommended.
- `uv` 0.8 or newer.
- seekdb 1.4.0+ reachable through the MySQL protocol, or OceanBase with
  `FULLTEXT` index support and `WITH PARSER SPACE`.
- PowerContext Server 1.2.0, installed from this project's pinned dependency.
- A MiniMax API key and access to `MiniMax-M3.1-Flash`.
- Git for restoring initial data and recording code versions.

All commands begin in the submission directory:

```bash
cd powercontext/minimax
```

## 2. Install

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -e ".[dev]"
```

On Windows, use `.venv\Scripts\python.exe` in place of `.venv/bin/python` and
`.venv\Scripts\sddctx.exe` in place of `.venv/bin/sddctx`.

Version pins are declared in `pyproject.toml`; the validation environment used
PowerContext `1.2.0`, PyMySQL `1.1.2`, httpx `0.28.1`, pytest `9.2.0`, and
seekdb `1.4.0.0`.

## 3. Start seekdb

If a seekdb service is already available at `127.0.0.1:2881`, skip this step.
A disposable local instance can be started with:

```bash
docker run -d \
  --name minimax-seekdb \
  -p 2881:2881 \
  -e ROOT_PASSWORD=replace-me \
  -v minimax-seekdb-data:/var/lib/seekdb \
  oceanbase/seekdb:latest
```

Wait until `mysql -h127.0.0.1 -P2881 -uroot -preplace-me -e "SELECT 1"` works.
The application creates the `minimax_sdd` database, asset table, and full-text
index during `sddctx import`.

## 4. Configure secrets

```bash
cp env.example .env
```

Replace `SEEKDB_PASSWORD` and `SDDCTX_MINIMAX_API_KEY`. Never commit `.env`.
The application loads `minimax/.env` automatically; explicit process
environment variables take precedence.

Configuration:

| Variable | Meaning |
| --- | --- |
| `SEEKDB_HOST`, `SEEKDB_PORT` | seekdb MySQL endpoint |
| `SEEKDB_USER`, `SEEKDB_PASSWORD` | database login |
| `SEEKDB_DATABASE` | isolated application database |
| `SDDCTX_POWERCONTEXT_URL` | PowerContext HTTP endpoint |
| `SDDCTX_MINIMAX_API_KEY` | MiniMax bearer token |
| `SDDCTX_MINIMAX_BASE_URL` | defaults to `https://api.minimaxi.com/v1` |
| `SDDCTX_MINIMAX_MODEL` | defaults to `MiniMax-M3.1-Flash` |

## 5. Start PowerContext

Run it in a separate terminal:

```bash
.venv/bin/powercontext server run --env-file powercontext.env
```

`powercontext.env` stores its own state under `.sddctx-data/powercontext` and
listens only on `127.0.0.1:8000`. A new terminal is not a module restart; stop
and restart the server only when demonstrating persistence across service
restarts.

## 6. Initialize and inspect

```bash
.venv/bin/sddctx import
.venv/bin/sddctx context \
  --out records/context-task-001.md \
  --check examples/catalog-year-filter/task.json
```

Expected: import reports 17 active assets at the initial snapshot; context
check reports `PASS` for all 11 required specification, code and test sources.

`sddctx context --json` returns raw `query_trace` entries. The same queries are
appended to `records/db-query-log.md`.

## 7. Run the validation task

From a clean business-code snapshot:

```bash
.venv/bin/python scripts/run_demo.py
```

The script performs:

1. import engineering assets;
2. build and check development context;
3. record target failure and regression success before modification;
4. write initial task state to PowerContext;
5. call MiniMax and apply complete source files;
6. re-import changed source and record target/regression/full-suite success;
7. reload saved PowerContext state and rebuild `records/resume-context.md`.

MiniMax is required for step 5. If the key is absent, steps 1-4 still leave
verifiable evidence, and the script exits `2` before changing business code.

## 8. Test commands

Module:

```bash
PYTHONPATH=src .venv/bin/python -m pytest tests
```

Business target:

```bash
cd sample-project
PYTHONPATH=src ../.venv/bin/python -m pytest -q tests/test_catalog_year_filter.py
cd ..
```

Business regression:

```bash
cd sample-project
PYTHONPATH=src ../.venv/bin/python -m pytest -q tests/test_catalog_regression.py
cd ..
```

Integration test against a reachable seekdb:

```bash
SDDCTX_RUN_INTEGRATION=1 PYTHONPATH=src \
  .venv/bin/python -m pytest -q tests/test_seekdb_integration.py
```

## 9. Reset

Restore the intentionally incomplete business source:

```bash
git checkout -- minimax/sample-project
.venv/bin/sddctx reset --yes
```

This removes the current project's indexed rows and generated records. It does
not stop services or remove PowerContext's scope. To clear all task state, stop
PowerContext, remove `.sddctx-data/powercontext`, and restart it.

## 10. Known limits

- The sample is deliberately in-memory; database storage is used for the
  context module's engineering assets, not the business project's runtime data.
- The official API endpoint and model may change. They are configuration, not
  hard-coded into context selection or tests.
- The generated-file protocol intentionally allows writes only under
  `sample-project/src/`; test modification is rejected.
- `MATCH ... AGAINST` requires seekdb/OceanBase support for `FULLTEXT`.
