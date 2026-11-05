# `minimax`: Spec-grounded context for continuous evolution

This directory is a self-contained 2026 OceanBase competition submission for
the MiniMax challenge. The baseline is
`oceanbase/powercontext@d647275c308e09b7b623f322a26f5c4e85734fb0` on branch
`2026-competition-ecosystem`.

`sddctx` answers a concrete engineering question:

> For this development task, which effective specifications, source symbols,
tests, and previously completed work should an AI coding assistant see?

It then gives that context to MiniMax, applies the returned source replacement,
and records before/after tests. The validation business project is a small
book catalog whose `min_year` filter is intentionally absent at the initial
snapshot.

## Architecture

```text
specs/ + sample-project/src/ + sample-project/tests/
             |
             | sddctx import
             v
     seekdb engineering_assets
     (asset metadata + SPACE full-text index)
             |
             | MATCH ... AGAINST, per asset kind
             v
     context builder ----> PowerContext task Memory
             |                       ^
             |                       |
             v                       |
 MiniMax chat completion --> full-file patch --> tests
             |                       |
             +---- evidence ---------+
```

### Responsibility split

| Technology | Actual role | Entry point |
| --- | --- | --- |
| seekdb 1.4 MySQL protocol | Stores all specification, source, and test assets. The task context is produced from returned `MATCH ... AGAINST` rows. Asset changes increment `version`. | `src/sddctx/seekdb_store.py` |
| PowerContext 1.2.0 | Stores task objective, completed/pending items, MiniMax run metadata, and verification summaries as scope Memory. A new process reloads it and rebuilds context. | `src/sddctx/state.py` |
| MiniMax M3.1 Flash API | Receives the selected context and returns complete replacement source files; only the generated file is written to `sample-project/src`. | `src/sddctx/agent.py` |

## Selection method

The task and every asset are normalized deterministically. English identifiers
are lowercased and split into components; Chinese text is represented as
single-character and adjacent-bigram tokens. This makes Chinese search work
with seekdb's space tokenizer without application-side final-answer matching.

For each of `spec_entry`, `code`, and `test`, `sddctx` executes a native seekdb
full-text query and ranks returned rows using the database score plus a small
bonus for task identifiers found in the source text. The selected rows carry
their real path, symbol, version, score, and content into the context output.
No answer sources are hard-coded in the context builder.

## CLI contract

`sddctx import` writes specs, source, and tests to seekdb.

`sddctx context --task TEXT --check TASK_JSON` prints the development context
and validates required source paths.

`sddctx dev --task TEXT --task-id ID` builds context, calls MiniMax, applies
generated files only under `sample-project/src/`, and writes request, response,
snapshot, manifest, development log, and diff.

`sddctx verify --phase before|after --suite target|regression|all --expect pass|fail`
runs the same tests from an explicit command, records exit code plus code hash,
and writes the result to PowerContext.

`sddctx status` and `sddctx resume` demonstrate cross-process task-state reuse.

## Acceptance mapping

| Required item | Evidence |
| --- | --- |
| Runs from instructions | `docs/RUNBOOK.md`; dependencies, seekdb, PowerContext, initialization, CLI and tests are all included |
| MiniMax participates | `records/minimax/<run>/` contains task, selected context, request, response, changed files and diff |
| Context is correct and dynamic | `context --check` verifies every required source; `scripts/spec_update_demo.py` changes and re-imports a spec |
| Database is used | `records/db-query-log.md` records SQL, analyzed query, returned row counts and elapsed time |
| State is reusable | task state is stored in PowerContext; `sddctx resume` launches a new process and rebuilds context |
| Code change is effective | `records/verify/` records target failure before the change and target, regression, and full-suite passes after it |

## Local quick start

See [RUNBOOK.md](docs/RUNBOOK.md) for Linux/macOS and Windows commands.
The shortest path after both services are running and `.env` is configured is:

```bash
uv pip install --python .venv/bin/python -e ".[dev]"
.venv/bin/sddctx doctor
.venv/bin/python scripts/run_demo.py
```

The checked-in business source is the post-MiniMax version. `scripts/run_demo.py`
first restores the recorded pre-MiniMax snapshot, so the target failure remains
reproducible; use `sddctx restore-sample` to do that restore explicitly.

Detailed expected results and reset steps are in
[VALIDATION.md](docs/VALIDATION.md).
