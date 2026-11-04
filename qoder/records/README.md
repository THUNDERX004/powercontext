# Evidence index

- `context-task-001.md` and `.json`: selected specification, code, test, and
  task-state context.
- `context-task-001.check.md`: exact required-source comparison.
- `db-query-log.md`: SQL, analyzed query, row count and elapsed time.
- `powercontext-log.md`: scope creation/reuse, Memory writes, searches, and
  citations.
- `verify/`: historical before-change target/regression test logs and
  structured summaries.
- `minimax/`: request, response, selected context, before snapshot, applied-file
  hashes, development log and unified diff when the optional runtime model path
  is run; the current repository keeps the selected-context snapshot.
- `context-demo/`: the successful Windows context-only run, its cross-process
  resume, structured summary, and verification record.
- `qoder/`: Qoder development/publication summary and raw CLI session records.
- `resume-context.md`: context rebuilt by a new process from PowerContext.
- `spec-update-demo/`: evidence that re-importing changed specification content
  changes subsequent context output.
