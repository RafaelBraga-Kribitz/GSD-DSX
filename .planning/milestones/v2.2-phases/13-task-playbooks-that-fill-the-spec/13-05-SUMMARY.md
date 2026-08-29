---
phase: 13-task-playbooks-that-fill-the-spec
plan: 05
type: execute
status: complete
requirements: [REQ-P13-06]
files_modified:
  - tests/fixtures/finding-codes-phase12.md
  - tests/test_finding_catalogue_invariant.py
---

# 13-05 Summary — catalogue scope-bound certification (zero new codes, by diff)

Wave-2 phase-wide certification that Phase 13 mints ZERO new `DSX-*` codes. Rides
BOTH the existing count invariant AND a new set-identity diff (D-07), closing the
mint-one/drop-one swap hole a count alone leaves open.

## Task 1 — freeze the Phase-12 snapshot fixture

Confirmed `python scripts/gen-finding-catalogue.py --check` exits 0 (the shipped
`references/finding-codes.md` is the generator's current output — safe to freeze;
the DSX-CLM-020/021/COH-030/PAR-002/SPEC-070/VAL-021/VAL-060 double-declare warnings
are the known shipped-tree noise, --check still exit 0). Then byte-copied
`references/finding-codes.md` → `tests/fixtures/finding-codes-phase12.md` with `cp`
(verified `cmp` IDENTICAL, not hand-authored). The snapshot enumerates exactly 256
distinct `DSX-*` codes, set-identical to the current catalogue.

## Task 2 — extend the invariant test with the set-identity diff

Extended `tests/test_finding_catalogue_invariant.py` (D-07), leaving
`_EXPECTED_TOTAL = 256` and the existing count method untouched:
- Added module-level `_SNAPSHOT_PATH = ROOT / "tests" / "fixtures" / "finding-codes-phase12.md"`.
- Added `test_code_set_is_set_identical_to_phase12_snapshot`: parses distinct
  `DSX-*` SETS from both catalogue and snapshot using the SAME CRLF-safe,
  non-line-anchored `_ROW_RE` (no parser drift), asserts `current_set == snapshot_set`,
  and on failure reports `added` (minted since Phase 12) and `removed` (dropped).

## Gate evidence (re-run by orchestrator)

- Task 1: **PASS** — `--check` exit 0; snapshot = 256 codes, set-identical to current.
- Task 2: **PASS** — `python -m unittest tests.test_finding_catalogue_invariant -v`
  runs **2 tests, both OK** (D-18 count invariant + D-07 set-identity diff);
  `--check` exit 0; `_SNAPSHOT_PATH` and `_EXPECTED_TOTAL = 256` present.
- Scope fence: only `tests/` touched (new fixture + extended test); nothing under
  `dsx/` or `scripts/`; `_EXPECTED_TOTAL` unchanged.

## Phase-wide certification (REQ-P13-06)

This plan is the proof that plans 13-01…13-04's `enforced` zero-mint prohibitions
hold against the final tree: catalogue stays at 256, code SET unchanged from the
Phase-12 baseline. Phase 13 mints and drops zero `DSX-*` codes.
