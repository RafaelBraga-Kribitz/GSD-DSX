---
phase: 06-contract-extension-decision-record-paradigm-manifest
plan: 02
subsystem: infra
tags: [decision-record, jsonl, crash-safety, stdlib-only, dataclasses]

requires:
  - phase: 06-01
    provides: loader `_NULL` fix and `dsx/spec.py` vocabulary registry (unrelated substrate, same wave)
provides:
  - "`dsx/decisions.py` — stdlib-only decision-record schema, crash-safe append, tolerant reader, invocation identity, frame digest, path resolution, report collection"
  - "`DecisionRecord`/`InvocationHeader` frozen dataclasses ready for plan 06-06 (structural validators) and 06-09 (gate wiring) to populate"
affects: [06-06, 06-09]

tech-stack:
  added: []
  patterns:
    - "Frozen dataclass + to_dict() mirroring dsx/findings.py::Finding's idiom"
    - "Append-only JSONL with flush()+os.fsync() per line; tolerant line-by-line reader that skips unparseable lines instead of raising"
    - "Deterministic identifiers derived from file contents (record counting), never uuid/clock"

key-files:
  created: [dsx/decisions.py, tests/test_decisions.py]
  modified: []

key-decisions:
  - "invocation_id is the grouping-anchor field name, not run_id (D-15) — confirmed no collision with DSX-SMELL-013's visuals[].run_id via grep before committing"
  - "frame_digest lives on InvocationHeader only, once per invocation, not on every DecisionRecord — it is a property of the run, not of any individual choice"
  - "decisions_path() reuses the caller's already-resolved root rather than re-implementing find_spec()'s search loop"

patterns-established:
  - "Per-task RED/GREEN TDD cycle within a single execute-type plan: test(06-02) commit precedes each feat(06-02) commit, one pair per task"

requirements-completed: [REQ-P6-07]

coverage:
  - id: D1
    description: "DecisionRecord/InvocationHeader schema, append() crash-safe emitter (flush+fsync), read_all() tolerant reader"
    requirement: "REQ-P6-07"
    verification:
      - kind: unit
        ref: "tests/test_decisions.py#TestDecisions (9 Task-1 tests: to_dict field coverage, record_type, round-trip, ordering, truncated-tail tolerance, blank-line tolerance, missing-path empty list, determinism)"
        status: pass
    human_judgment: false
  - id: D2
    description: "next_invocation_id() deterministic file-derived counter, frame_digest() sha256 scoped to validity_frame/inference, decisions_path(), collect_from_report()"
    requirement: "REQ-P6-07"
    verification:
      - kind: unit
        ref: "tests/test_decisions.py#TestDecisions (10 Task-2 tests: invocation-id monotonicity/stability, digest shape/scope/key-order invariance, path shape, report-collection ordering and empty case)"
        status: pass
    human_judgment: false

duration: 6min
completed: 2026-08-08
status: complete
---

# Phase 6 Plan 2: Decision-Record Substrate Summary

**Stdlib-only `dsx/decisions.py` — the first write path in a read-only codebase: crash-safe JSONL append via flush()+os.fsync(), a tolerant line-by-line reader, and deterministic invocation/frame-digest identity, with no caller wired yet.**

## Performance

- **Duration:** 6 min
- **Started:** 2026-08-07T23:57:25Z (immediately following 06-01)
- **Completed:** 2026-08-08T00:03:22Z
- **Tasks:** 2 completed
- **Files created:** 2 (`dsx/decisions.py`, `tests/test_decisions.py`)

## Accomplishments

- `DecisionRecord` (11 fields: the 10 brief-5.5 fields + `invocation_id`) and `InvocationHeader`
  (4 fields, the per-run grouping anchor) as frozen dataclasses with `to_dict()` mirroring
  `dsx/findings.py::Finding`'s idiom, `record_type` set to `"decision"`/`"invocation"` respectively
- `append()` writes one `json.dumps(..., sort_keys=True)` line, `flush()`s, `os.fsync()`s — a
  completed line survives a crashed run (T-6-05 mitigation)
- `read_all()` skips blank lines and any unparseable trailing line inside
  `try/except json.JSONDecodeError: continue` — a crash-tail never fails the whole file
  (T-6-02 mitigation)
- `next_invocation_id()` counts `record_type == "invocation"` records already in the file — no
  `uuid`, no clock read, byte-identical input produces byte-identical output
- `frame_digest()` — sha256 hex digest over `{"validity_frame": ..., "inference": ...}` only,
  `sort_keys=True` makes it key-order invariant; unaffected by edits elsewhere in the spec
- `decisions_path()` and `collect_from_report()` complete the substrate: path resolution reuses
  the caller's already-computed root, report collection flattens each sub-report's `decisions`
  list out of a merged `Report.context` in `merge()`'s iteration order
- Module docstring is the normative D-19 append contract: file name, location, JSONL format,
  required fields, both `layer` values, and the statement that a dsx agent may begin appending
  `layer: "stochastic"` entries with no further code change
- 19 tests in `tests/test_decisions.py`, all passing; full suite (`python3 -m unittest discover -s
  tests`) at 189 tests, 2 pre-existing skips, 0 failures

## Task Commits

Each task followed the RED → GREEN TDD cycle (per-task, within this `type="execute"` plan):

1. **Task 1: Decision-record schema, crash-safe append, tolerant reader**
   - `81cdc8b` test(06-02): add failing tests for decision-record schema and crash-safe append
   - `af9b5d7` feat(06-02): implement decision-record schema and crash-safe append/tolerant reader
2. **Task 2: Invocation identity, frame digest, path resolution, report collection**
   - `869d52f` test(06-02): add failing tests for invocation identity, frame digest, path resolution, report collection
   - `935a167` feat(06-02): implement invocation identity, frame digest, decisions path, report collection

No REFACTOR commit was needed — GREEN implementations were minimal and required no cleanup pass.

**Plan metadata:** pending (final `docs(06-02)` commit below)

## Files Created/Modified

- `dsx/decisions.py` - Decision-record schema, crash-safe append, tolerant reader, invocation
  identity, frame digest, path resolution, report collection. Stdlib-only (json, os, dataclasses,
  pathlib, typing, hashlib, `__future__`).
- `tests/test_decisions.py` - 19 `unittest` tests, `tempfile.TemporaryDirectory()`-based, no
  mocking, following `tests/test_dsx.py`'s existing assertion style.

## Decisions Made

- `invocation_id` chosen over `run_id` per D-15; collision check performed (`grep -rn
  "invocation_id" dsx/ tests/ templates/ examples/ references/ --include='*.py' --include='*.yaml'
  --include='*.md'`, excluding this plan's own two new files) returned no matches before
  committing.
- `frame_digest` placed on `InvocationHeader` only, not on every `DecisionRecord` — it is a
  property of the invocation (which spec, at which content), not of any individual choice made
  during it.
- No `next_decision_id()` function was added — `DecisionRecord.id` remains caller-supplied
  (plan 06-06 populates records; this plan builds substrate only), matching the plan's exact
  export list.

## Deviations from Plan

None - plan executed exactly as written. RED/GREEN discipline was applied at task granularity
(rather than once for the whole plan) since the plan's frontmatter `type` is `execute`, not `tdd`,
and both tasks individually carry `tdd="true"`.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `dsx/decisions.py` exists as a stdlib-only, crash-safe substrate with no caller yet, exactly as
  scoped — plan 06-06 will populate records from the structural validators via
  `report.context.setdefault("decisions", [])`, and plan 06-09 will wire `append()`/`read_all()`
  into the gate CLI and `dsx explain`.
- `dsx/checks/` untouched this plan (`git status --porcelain dsx/checks/` reports no changes,
  D-13 preserved).
- `python3 -m dsx gate plan --spec examples/good-ANALYSIS-SPEC.yaml` still exits 0 — no caller
  added, gate behavior unchanged as expected.

---
*Phase: 06-contract-extension-decision-record-paradigm-manifest*
*Completed: 2026-08-08*

## Self-Check: PASSED

- FOUND: dsx/decisions.py
- FOUND: tests/test_decisions.py
- FOUND commit: 81cdc8b (test(06-02): decision-record schema tests)
- FOUND commit: af9b5d7 (feat(06-02): decision-record schema implementation)
- FOUND commit: 869d52f (test(06-02): invocation identity/digest/collection tests)
- FOUND commit: 935a167 (feat(06-02): invocation identity/digest/collection implementation)
