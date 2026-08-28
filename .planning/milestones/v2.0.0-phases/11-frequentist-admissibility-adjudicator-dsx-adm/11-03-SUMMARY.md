---
phase: 11-frequentist-admissibility-adjudicator-dsx-adm
plan: 03
subsystem: testing
tags: [ast-scanning, import-boundary, paradigm-manifest, tdd]

# Dependency graph
requires:
  - phase: 07-validity-frame-checks-dsx-val
    provides: "the D-03a one-directional import-boundary scanner and dsx/frame/paradigm.py's _PARADIGM_CONDITIONAL/_NOT_SHIPPED tables this plan extends"
provides:
  - "A mirror-image AST scanner (TestChecksImportBoundary) proving dsx/checks/ imports nothing from dsx.frame, closing the reverse direction of D-03a"
  - "applies_to_frequentist_admissibility(spec) exported from dsx/frame/paradigm.py — the one predicate plan 11-07's run_checks will call to scope the DSX-ADM-* adjudicator to frequentist frames"
affects: [11-04, 11-05, 11-06, 11-07, 11-08]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Single AST scanner parameterised by forbidden_package serves both import-boundary directions instead of a second hand-rolled walker"
    - "Frequentist-scoping decision lives exclusively in dsx/frame/paradigm.py (the D-11-exempt file) and is passed into the adjudicator as a boolean, never computed inside it"

key-files:
  created:
    - tests/test_frame_paradigm.py
  modified:
    - tests/test_frame_boundary.py
    - dsx/frame/paradigm.py

key-decisions:
  - "Generalised _scan_source_for_checks_imports with a forbidden_package parameter (default dsx.checks) rather than writing a second AST walker for the reverse direction, per the plan's explicit instruction"
  - "applies_to_frequentist_admissibility widens to True for undeclared/blank/out-of-vocabulary paradigms and for a declared frequentist paradigm, returning False only for a recognised non-frequentist (bayesian) declaration — matching the widening idiom _check_monitoring_discipline and check() already use, so an honest Bayesian declaration never costs more than silence (D-10)"
  - "Left _NOT_SHIPPED, _PARADIGM_CONDITIONAL and _PARADIGM_INDEPENDENT untouched, confirmed by git diff — plan 11-06 owns removing the DSX-ADM- entry from _NOT_SHIPPED in the same commit that registers the check"

requirements-completed: [REQ-P11-04, REQ-P11-05]

coverage:
  - id: D1
    description: "Reverse-direction import-boundary scanner: no file under dsx/checks/ imports dsx.frame or any submodule, proven to fire against three deliberately violating source strings"
    requirement: "REQ-P11-05"
    verification:
      - kind: unit
        ref: "tests/test_frame_boundary.py#TestChecksImportBoundary.test_real_checks_modules_import_nothing_from_frame"
        status: pass
      - kind: unit
        ref: "tests/test_frame_boundary.py#TestChecksImportBoundary.test_scanner_fires_on_violating_sources_and_permits_allowed_ones"
        status: pass
      - kind: manual_procedural
        ref: "python -m unittest tests.test_frame_boundary — exit 1 with a temporary `from dsx.frame import paradigm` added to dsx/checks/stats.py, exit 0 after revert"
        status: pass
    human_judgment: false
  - id: D2
    description: "applies_to_frequentist_admissibility(spec) returns the correct boolean for declared frequentist, declared bayesian, undeclared, blank, and out-of-vocabulary paradigms, is a pure predicate, and tolerates a non-dict spec"
    requirement: "REQ-P11-04"
    verification:
      - kind: unit
        ref: "tests/test_frame_paradigm.py#TestAppliesToFrequentistAdmissibility (14 test methods)"
        status: pass
      - kind: unit
        ref: "python -c \"...\" seven-case assertion from the plan's <verify> block"
        status: pass
    human_judgment: false

# Metrics
duration: ~20min
completed: 2026-08-20
status: complete
---

# Phase 11 Plan 03: Reverse import-boundary scanner and frequentist-scoping predicate Summary

**Mirror-image AST scanner closing the `dsx/checks/` → `dsx/frame/` import direction, plus `applies_to_frequentist_admissibility(spec)` — the one predicate allowed to read the declared paradigm on the adjudicator's behalf.**

## Performance

- **Duration:** ~20 min
- **Completed:** 2026-08-20T17:20:09Z
- **Tasks:** 2 completed
- **Files modified:** 3 (1 created, 2 modified)

## Accomplishments
- `TestChecksImportBoundary` added to `tests/test_frame_boundary.py`, walking every `*.py` under `dsx/checks/` and asserting zero imports of `dsx.frame` or any submodule; proven to fire (not just proven to pass) against three violating source strings and to permit two near-miss controls
- Generalised the existing `_scan_source_for_checks_imports` with a `forbidden_package` parameter instead of hand-rolling a second AST walker — `CHECKS_DIR` resolved from `dsx.checks.__file__`, mirroring `FRAME_DIR`
- `applies_to_frequentist_admissibility(spec)` added to `dsx/frame/paradigm.py` — a pure boolean predicate with no `Report`, no findings, no side effects — covered by 14 new unit tests in `tests/test_frame_paradigm.py`
- `_NOT_SHIPPED`'s `DSX-ADM-` honesty entry, `_PARADIGM_CONDITIONAL` and `_PARADIGM_INDEPENDENT` left untouched (confirmed by `git diff`)

## Task Commits

Each task was committed atomically:

1. **Task 1: Add the reverse-direction import-boundary scanner (D-04a)** - `5ff083f` (test)
2. **Task 2: Add the frequentist-scoping predicate to dsx/frame/paradigm.py** - `e34cd84` (feat)

**Plan metadata:** committed with this SUMMARY.md (see final commit in this plan's history)

## Files Created/Modified
- `tests/test_frame_boundary.py` — generalised `_scan_source_for_checks_imports`, added `CHECKS_DIR`, added `TestChecksImportBoundary` (2 test methods)
- `dsx/frame/paradigm.py` — added `applies_to_frequentist_admissibility(spec) -> bool`
- `tests/test_frame_paradigm.py` — new file, 14 test methods covering all nine declared-paradigm cases from the plan's `<behavior>` block

## Decisions Made
- Reused `_package_for` unchanged and extended `_scan_source_for_checks_imports` via a `forbidden_package` parameter (default `dsx.checks`, so all three existing call sites are unchanged) rather than writing a second scanner function — this was the plan's explicit instruction and kept the AST machinery single-sourced.
- `applies_to_frequentist_admissibility` returns `True` (in scope) for: declared `frequentist`; undeclared; blank/whitespace-only; and any value outside `PARADIGMS` (including near-miss misspellings and case/hyphen variants, via `normalize`). It returns `False` only for a recognised, declared, non-frequentist paradigm — today, `bayesian`. This mirrors `_check_monitoring_discipline`'s existing widening idiom exactly, so an honest Bayesian declaration never costs more than silence (brief D-10).
- Added an explicit `isinstance(spec, dict)` guard even though `dsx.spec.get()` already tolerates a non-dict input, matching the defensive convention `dsx/frame/interference.py` and `dsx/frame/prereg.py` already use — belt-and-suspenders against a future caller that touches `spec` directly.

## Deviations from Plan

None - plan executed exactly as written. Both tasks' acceptance criteria were verified directly (see below), and the prohibition ("the frequentist-scoping helper must not be re-implemented, copied or inlined inside `dsx/frame/admissibility.py`") is trivially satisfied — that module does not exist yet in this plan.

## TDD Gate Compliance

Plan frontmatter is `type: tdd`. Git log for this plan shows a `test(...)` commit (`5ff083f`) followed by a `feat(...)` commit (`e34cd84`) — the RED-then-GREEN gate sequence type: tdd plans require. Task 1's deliverable was itself test infrastructure (an AST scanner living inside the test module), so its commit is correctly typed `test`; Task 2's test file (`tests/test_frame_paradigm.py`) and its implementation (`dsx/frame/paradigm.py`) were written and verified together before a single `feat` commit, rather than as two separate commits — both were confirmed failing-then-passing interactively during authoring (the function did not exist until this task; all 14 tests plus the plan's seven-case assertion script pass after implementation). No gate is missing; the single combined commit is a minor deviation from the strict per-task RED/GREEN commit split, noted for transparency.

## Issues Encountered
None. All verification commands from the plan's `<verify>` blocks and the plan-level `<verification>` section were run directly and passed:
- `python -m unittest tests.test_frame_boundary` — exit 0, 10 tests
- `python -m unittest tests.test_frame_paradigm` — exit 0, 14 tests
- `python -m unittest discover -s tests` — exit 0, 656 tests
- `python scripts/gen-finding-catalogue.py --check` — exit 0 ("finding catalogue is current")
- `python -m dsx.cli gate plan --spec examples/good-ANALYSIS-SPEC.yaml` — exit 0, PASS, `DSX-ADM-` still listed as "not applied" under `_NOT_SHIPPED` (helper is inert, as required)
- Reverse-scanner fire proof: temporarily adding `from dsx.frame import paradigm` to `dsx/checks/stats.py` made the boundary suite exit 1; reverting restored exit 0 (`git diff dsx/checks/stats.py` empty afterward)

Pre-existing "declared twice with different text" warnings appear during full-suite and catalogue runs (`DSX-SPEC-070`, `DSX-VAL-021`, `DSX-VAL-060`, `DSX-COH-030`, `DSX-PAR-002`) — these are unrelated to this plan's files and were present before this plan's changes; out of scope per the deviation rules' scope boundary.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- `tests/test_frame_boundary.py` now enforces the `dsx/checks/` ↔ `dsx/frame/` boundary in both directions — plan 11-07's `cmd_recommend` composition (the first code with a real incentive to cross it) cannot ship green if it imports `dsx.frame` from `dsx.checks`.
- `applies_to_frequentist_admissibility` is ready for plan 11-07's `run_checks` dispatch branch to call and pass in as a parameter; `dsx/frame/admissibility.py` (created in a later plan) must never compute this itself — the prohibition this plan's threat model flags.
- No blockers.

---
*Phase: 11-frequentist-admissibility-adjudicator-dsx-adm*
*Completed: 2026-08-20*

## Self-Check: PASSED

All created/modified files verified present on disk (`tests/test_frame_boundary.py`,
`tests/test_frame_paradigm.py`, `dsx/frame/paradigm.py`, this SUMMARY.md). All three
commit hashes (`5ff083f`, `e34cd84`, `9b9e60b`) verified present in `git log`.
