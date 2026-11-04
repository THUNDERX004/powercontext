# `qoder`: Spec-grounded context for continuous evolution

This directory (`qoder/`) is a self-contained 2026 OceanBase competition
submission for the Qoder track. The baseline is
`oceanbase/powercontext@d647275c308e09b7b623f322a26f5c4e85734fb0` on branch
`2026-competition-ecosystem`; this submission is developed on branch
`codex/qoder-contextpack`.

`sddctx` answers a concrete engineering question:

> For this development task, which effective specifications, source symbols,
tests, and previously completed work should an AI coding assistant see?

It can then give that context to the optional runtime code model (MiniMax
M3.1 Flash), apply the returned source replacement, and record before/after
tests. The validation business project is a small book catalog whose
`min_year` filter is intentionally absent at the initial snapshot.
Context selection itself requires no model key: `scripts/run_context_demo.py`
demonstrates import, retrieval, context check, and cross-process resume
entirely offline from the MiniMax API.

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
 MiniMax chat completion --> full-file patch --> tests   (MiniMax = optional
             |                       |                   runtime code model)
             +---- evidence ---------+
```

### Responsibility split

| Technology | Actual role | Entry point |
| --- | --- | --- |
| seekdb 1.4 MySQL protocol | Stores all specification, source, and test assets. The task context is produced from returned `MATCH ... AGAINST` rows. Asset changes increment `version`. | `src/sddctx/seekdb_store.py` |
| PowerContext 1.2.0 | Stores task objective, completed/pending items, MiniMax run metadata, and verification summaries as scope Memory. A new process reloads it and rebuilds context. | `src/sddctx/state.py` |
| MiniMax M3.1 Flash API (optional runtime code model) | Receives the selected context and returns complete replacement source files; only the generated file is written to `sample-project/src`. Not required by any other command. | `src/sddctx/agent.py` |

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
| Required runnable path: the offline context workflow | `scripts/run_context_demo.py` exited `0` on Windows, 2026-11-04: 17 active assets in `qoder_sdd`, context specs/code/tests = 9/3/3, 11/11 required sources PASS, task state saved to PowerContext (memory revision `2`) and reloaded by a separate child process that rebuilt `records/context-demo/resume-context.md`. No MiniMax/LLM key. See `records/context-demo/VERIFICATION.md` |
| Runs from instructions | `docs/RUNBOOK.md`; dependencies, seekdb, PowerContext, initialization, CLI and tests are all included |
| Database is used | `records/db-query-log.md` records SQL, analyzed query, returned row counts and elapsed time for historical and new runs; `sddctx doctor` passed seekdb `qoder_sdd, assets=17` (VERIFICATION.md) |
| Context is correct and dynamic | `context --check` verifies every required source (`records/context-demo/context.check.md`, historical `records/context-task-001.check.md`); `scripts/spec_update_demo.py` changes and re-imports a spec |
| State is reusable | task state is stored in PowerContext; the new run's `--resume-only` child is a separate OS process; historical `sddctx resume` evidence stays in `records/powercontext-log.md` and `records/resume-context.md` |
| Tests pass | module suite: 20 passed, 1 skipped (gated integration case); with `SDDCTX_RUN_INTEGRATION=1`: 1 passed (both 2026-11-04, `records/context-demo/VERIFICATION.md`) |
| MiniMax — optional runtime evidence, not a required path | MiniMax is only the runtime code model behind `sddctx dev`; its run directory (`records/minimax/<run>/`) is designed to hold task, selected context, request, response, changed files and diff. Present in the repo today: the selected context (`catalog-year-filter-20261104T061318Z/`) |
| Code change evidence (historical, before-change baseline) | `records/verify/` holds the two before-phase structured results (target behavioral failure accepted; regression pass) produced under the earlier `minimax-sdd` naming; post-change expectations are stated in `docs/VALIDATION.md`. Historical JSON/log files are not rewritten |

## Local quick start

See [RUNBOOK.md](docs/RUNBOOK.md) for Linux/macOS and Windows commands.
The shortest path after both services are running and `.env` is configured is:

```bash
uv pip install --python .venv/bin/python -e ".[dev]"
.venv/bin/sddctx doctor
.venv/bin/python scripts/run_context_demo.py
.venv/bin/python scripts/run_demo.py
```

The offline demo requires seekdb and PowerContext only — no MiniMax/LLM key.
It writes fresh evidence under `records/context-demo/` (context, check report,
resume context, summary) and demonstrates cross-process task-state reuse.
These files were produced by the successful Windows run of 2026-11-04; see
`records/context-demo/VERIFICATION.md`.

## Qoder track notes

- Development session log: `records/qoder/README.md` (Qoder CLI session, tasks,
  produced paths).
- Project website: `site/` (plain HTML/CSS/JS, no external dependencies; not
  yet published to Qoder Sites).
- New-run defaults for this submission: `SDDCTX_PROJECT_KEY=qoder-sdd`,
  `SEEKDB_DATABASE=qoder_sdd`. Historical evidence already under `records/`
  keeps the values in effect when it was produced (`minimax-sdd`,
  `minimax_sdd`); it is not rewritten.
- MiniMax appears only as the optional runtime code model behind `sddctx dev`.

The sample source is deliberately in its pre-change state. Running the demo
will make MiniMax implement `min_year`; use Git to restore and repeat.

Detailed expected results and reset steps are in
[VALIDATION.md](docs/VALIDATION.md).
