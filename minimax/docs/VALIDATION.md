# Validation sample

## Task definition

`examples/catalog-year-filter/task.json` contains the task description and all
required context sources.

**What changes:** `Catalog.search(..., min_year=<year>)` must return only books
whose `published_year` is greater than or equal to the supplied year.

**What must remain:** the default call, keyword search, all requested tags,
archived visibility, sorting, and the stored catalog remain unchanged.

## Initial data

- Business project: `sample-project/`
- Specifications: `specs/SPEC-001-工程约束.md` and
  `specs/SPEC-002-书目录查询.md`
- Code to inspect: `sample-project/src/bookdesk/catalog.py` and `models.py`
- Target tests: `sample-project/tests/test_catalog_year_filter.py`
- Regression tests: `sample-project/tests/test_catalog_regression.py`
- Fixture: six books spanning 2017-2023, one archived book, shared ratings,
  multiple tags, and deterministic tie-breaking.

The initial `catalog.py` accepts `min_year` in the signature but intentionally
ignores only the filtering behavior. This yields behavioral assertion failures,
not import, dependency, or service failures.

## Expected pre-change result

Command:

```bash
sddctx verify --phase before --suite target --expect fail
sddctx verify --phase before --suite regression --expect pass
```

Expected:

- target: `4 failed, 3 passed`, accepted as the expected behavioral failure;
- regression: `5 passed`;
- both logs contain command, working directory, exit code, test counts and Git
  commit/code-tree hash.

## Expected context

The `--check examples/catalog-year-filter/task.json` invocation must report
`PASS` for:

- five `SPEC-002` entries and two compatibility/ordering `SPEC-001` entries;
- `catalog.py` and `models.py`;
- both target and regression test files.

The markdown and JSON output include the actual version and source path for
every item. The database query audit includes the analyzed query and returned
row count for each kind.

## Expected post-change result

MiniMax receives the selected context and returns a complete replacement for
`sample-project/src/bookdesk/catalog.py`. After re-import:

```bash
sddctx verify --phase after --suite target --expect pass
sddctx verify --phase after --suite regression --expect pass
sddctx verify --phase after --suite all --expect pass
```

Expected:

- target: `7 passed`;
- regression: `5 passed`;
- all: `12 passed`.

The code diff, before snapshot, MiniMax request/response, applied file hashes,
and test logs are under `records/`.

## Specification update test

Run:

```bash
python scripts/spec_update_demo.py
```

The script temporarily changes `SPEC-002-2` to include a unique marker,
re-imports, and verifies that the changed version appears in context.
It writes `records/spec-update-demo/context-after-update.md` and `result.json`,
then restores the checked-in specification and re-imports it.

This proves that the output follows the current database content rather than a
fixed candidate list.

## State reuse test

After initial task setup:

```bash
sddctx status \
  --objective "为 Catalog.search 增加 min_year 年份下限筛选" \
  --complete "导入规格、代码和测试资料" \
  --pending "使用 MiniMax 修改代码"
sddctx resume
```

`resume` runs in a new OS process, loads the PowerContext Memory entry, writes
the recovered completed/pending/verification state, and rebuilds the context
from the saved objective. The write/search operations are recorded in
`records/powercontext-log.md`.

## Reset and rerun

```bash
git checkout -- minimax/sample-project
sddctx reset --yes
sddctx import
python scripts/run_demo.py
```

If PowerContext state must start empty, stop its server, remove
`.sddctx-data/powercontext`, and start it again.
