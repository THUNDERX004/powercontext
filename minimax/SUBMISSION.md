# Submission checklist

## Baseline

- Official branch: `2026-competition-ecosystem`
- Official baseline commit: `d647275c308e09b7b623f322a26f5c4e85734fb0`
- Submission directory: `minimax/`

## Required demonstration

Task: add an inclusive `min_year` filter to `Catalog.search` without changing
keyword search, tag filtering, archived visibility, ordering, or stored data.

Expected selected sources:

- five `SPEC-002` behavior entries;
- two `SPEC-001` compatibility and ordering entries;
- `sample-project/src/bookdesk/catalog.py`;
- `sample-project/src/bookdesk/models.py`;
- both target and regression test files.

These exact sources are asserted by
`examples/catalog-year-filter/task.json` and
`records/context-task-001.check.md`.

## Evidence

| Requirement | Artifact |
| --- | --- |
| Runnable from clean instructions | `docs/RUNBOOK.md`, `records/module-tests.log` |
| MiniMax participated | `records/minimax/catalog-year-filter-20261105T023544Z/` |
| Context correctness and spec refresh | `records/context-task-001.*`, `records/spec-update-demo/` |
| seekdb/OceanBase used | `records/db-query-log.md`, 17 indexed assets |
| PowerContext state reused | `records/powercontext-log.md`, `records/resume-context.md` |
| Effective code change | `records/minimax/.../code.diff.md`, `records/verify/` |

Observed results:

- before target: `3 passed, 4 failed` for the intentionally missing behavior;
- before regression: `5 passed`;
- after target: `7 passed`;
- after regression: `5 passed`;
- after full business suite: `12 passed`;
- module and real seekdb integration tests: `15 passed`.

MiniMax model: `MiniMax-M3.1-Flash`.

The response ID, usage counters, full context, raw response, pre-change source,
generated file hash, and unified diff are stored in the successful MiniMax run
directory. The API key is not stored in any artifact.

## Reproduce

Follow `docs/RUNBOOK.md`. To replay only the validation:

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -e ".[dev]"
cp env.example .env
# Fill seekdb and MiniMax credentials.
.venv/bin/powercontext server run --env-file powercontext.env  # separate terminal
.venv/bin/sddctx doctor
.venv/bin/python scripts/run_demo.py
```

The checked-in business source is the post-MiniMax version. Restore the initial
snapshot with:

```bash
git checkout -- minimax/sample-project
```
