---
phase: 17-foundation-repairs-and-spec-vocabulary
plan: 01
subsystem: testing
tags: [statistics, routing-table, boschloo, doc-code-reconciliation]

requires:
  - phase: 17-foundation-repairs-and-spec-vocabulary
    provides: "D-04 reconcile-to-doc decision (17-CONTEXT.md)"
provides:
  - "recommend_test two-proportion small-expected-cell alternative names boschloo_exact (not fisher_exact)"
  - "boschloo_exact is a member of NONPARAMETRIC_TESTS (fisher_exact retained)"
  - "doc<->code regression pin binding references/test-selection.md's Boschloo name to the emitted alternative (down payment on REQ-P20-04)"
affects: [18-correlation-association-agreement, 20-calibration-and-reporting-close]

tech-stack:
  added: []
  patterns:
    - "doc<->code regression pin: whitespace-collapsed CRLF-safe read of a reference doc asserting it names what the routing table emits"

key-files:
  created:
    - tests/test_boschloo_reconciliation.py
  modified:
    - dsx/checks/stats.py

key-decisions:
  - "Reconcile-to-doc (D-04): fixed the code to match the already-correct doc; references/test-selection.md left byte-unedited."
  - "Additive membership: boschloo_exact joins NONPARAMETRIC_TESTS; fisher_exact kept as the correct 3-plus-group sparse-cell alternative (line 69 untouched)."

patterns-established:
  - "Pattern: a divergence class is pinned by a regression test the moment it is reconciled, so it cannot recur silently."

requirements-completed: [REQ-P17-01]

coverage:
  - id: D1
    description: "recommend_test('proportion', 2) names boschloo_exact as the small-expected-cell alternative (primary stays two_proportion_z); boschloo_exact in NONPARAMETRIC_TESTS with fisher_exact retained."
    requirement: "REQ-P17-01"
    verification:
      - kind: unit
        ref: "tests/test_boschloo_reconciliation.py#test_two_proportion_alternative_names_boschloo_exact + test_boschloo_exact_added_without_dropping_fisher_exact"
        status: pass
    human_judgment: false
  - id: D2
    description: "Doc<->code pin: references/test-selection.md still names Boschloo, bound to the code by a regression test so the divergence cannot recur silently."
    requirement: "REQ-P17-01"
    verification:
      - kind: unit
        ref: "tests/test_boschloo_reconciliation.py#test_doc_still_names_boschloo"
        status: pass
    human_judgment: false

duration: 2min
completed: 2026-09-01
status: complete
---

# Phase 17 — Plan 01: Boschloo doc/code reconciliation Summary

**Reconciled the live Boschloo doc/code divergence (D-04) by fixing the routing table to match the already-correct reference doc, pinned by a new regression test — zero new finding codes.**

## Performance

- **Duration:** ~2 min
- **Started:** 2026-09-01T21:28Z
- **Completed:** 2026-09-01T21:30Z
- **Tasks:** 2 (RED test, GREEN reconcile)
- **Files modified:** 2 (1 created, 1 edited)

## Accomplishments
- `recommend_test("proportion", 2)` now names `boschloo_exact (any expected cell < 5)` as the small-expected-cell alternative; the primary returned test stays `two_proportion_z`.
- `boschloo_exact` added to `NONPARAMETRIC_TESTS` additively — `fisher_exact` retained as the correct 3-plus-group sparse-cell alternative (line 69 untouched).
- New `tests/test_boschloo_reconciliation.py` pins the two-proportion alternative, the membership, and a CRLF-safe doc<->code binding (`references/test-selection.md` still names Boschloo).

## Task Commits

1. **Task 1 (RED): failing Boschloo reconciliation test** - `c2c91cd` (test)
2. **Task 2 (GREEN): reconcile code to doc** - `99622fe` (fix)

_TDD: RED proved teeth (2 divergence assertions failed, doc-pin passed pre-edit); GREEN turned all three green._

## Files Created/Modified
- `tests/test_boschloo_reconciliation.py` - New regression module (BoschlooReconciliationTest): 3 assertions, stdlib unittest, CRLF-safe.
- `dsx/checks/stats.py` - `boschloo_exact` added to `NONPARAMETRIC_TESTS`; two-proportion alternative swapped fisher→boschloo.

## Decisions Made
None beyond the plan — executed exactly as written (D-04 reconcile-to-doc).

## Deviations from Plan
None - plan executed exactly as written.

## Issues Encountered
None. (Baseline full suite green at 1312 tests before edits; catalogue invariant green at 260 codes after — zero new codes minted.)

## Gate Evidence (orchestrator-run)
- `python3 -m unittest tests.test_boschloo_reconciliation -v` → RED (2 fail, doc-pin ok) at commit `c2c91cd`; GREEN (3/3 ok) at `99622fe`.
- `python3 -m unittest tests.test_finding_catalogue_invariant -v` → GREEN, 260 codes by set identity (no report.add touched).
- `references/test-selection.md` byte-unedited (git status shows only stats.py modified in the GREEN commit).

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- REQ-P17-01 delivered. `stats.py` ready for the Wave-2 (17-03) DSX-STA-040 widening, which depends on this plan (single-writer on `stats.py`).

---
*Phase: 17-foundation-repairs-and-spec-vocabulary*
*Completed: 2026-09-01*
