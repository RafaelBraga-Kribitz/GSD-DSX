---
phase: 16-re-run-verification-off-the-gate-path
plan: 04
status: complete
requirements: [REQ-P16-04]
---

# 16-04 SUMMARY — static AST no-entrypoint-execution guard

## What shipped
- **`tests/test_no_entrypoint_execution.py`** (new, stdlib-only) — the execution-detecting complement
  to `test_gate_path_hermetic.py`. `_execution_primitives(source)` AST-walks source and flags the
  execution family (`subprocess.*`, `os.system`/`popen`/`exec*`/`spawn*`/`posix_spawn*`,
  `runpy.run_path`/`run_module`, dynamic `importlib.import_module`, bare `exec`/`eval`/dynamic
  `compile`/`__import__`), excluding the `ast` and `re` roots so `ast.parse`/`walk`/`unparse` and
  `re.compile` are not mistaken for execution (D-09). `test_no_gate_module_executes_the_entrypoint`
  scans every `dsx/checks/*.py` + `dsx/frame/*.py`, asserts the named scan set is non-empty and
  includes `code.py` + `repro.py` (the latter now carrying 16-01's `_check_reproduce_report`), asserts
  every scanned path is under those two dirs, and finds zero execution primitives on the real tree.
  Positive control flags `subprocess.run`/`runpy.run_path`/`os.system`/`exec`; negative control leaves
  `ast.*`/`re.compile` unflagged.

## Why distinct from the import-hermetic test
`subprocess`/`runpy`/`os` are stdlib, so they pass an import-closure check silently. This test catches
the *call*, which the hermetic test structurally cannot (Auditor T3 / D-01/D-09).

## Gate evidence (all re-run by the orchestrator, brief §5)
- `python -m unittest tests.test_no_entrypoint_execution` → **3 tests OK** (real-tree scan clean, positive control flags, negative control clean).
- AST import-purity of the test file OK (no pandas/scipy/numpy); the 4 required functions/methods present.
- Integration: Phase-16 modules together (reproduce + invariant + no-execution + hermetic) → **14 tests OK**; catalogue `--check` exit 0 at 258; only `dsx/checks/repro.py` changed under `dsx/` (16-02/03/04 gate-path-pure); `scripts/` untouched.
