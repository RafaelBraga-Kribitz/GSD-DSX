---
phase: 09-monitoring-discipline-symmetric-dsx-par
plan: 02
subsystem: testing
tags: [citation, d-05, unittest, simulation, monte-carlo, ast-scanner, mathx]

# Dependency graph
requires:
  - phase: 06-contract-decision-paradigm-manifest-m1
    provides: dsx/mathx.py::inflation_from_peeking(), dsx/frame/paradigm.py's Citation:/unverified-locator docstring convention, tests/test_frame_boundary.py's AST-scanner idiom
provides:
  - inflation_from_peeking() docstring carrying a full Armitage, McPherson & Rowe (1969) citation with an explicit unverified-locator flag
  - tests/test_par_monitoring_simulation.py — seeded, stdlib-only, sub-second simulation proving DSX-PAR-010's point-null formulation and DSX-PAR-011's prior-averaged formulation are different results
  - AST-based proof that no module under dsx/ imports from tests/ (REQ-P9-07's location enforcement)
affects: [09-01, 09-03, 09-04, 09-05, verify-phase-09]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Evidence-only test module: a tests/ file that is neither wired into the gate path nor into dsx/, self-contained simulation + assertions, proven never-reachable by an AST scan"
    - "Guaranteed-not-statistical monotonicity: reusing one cached path per trial across a look ladder so a monotone-trend assertion holds by construction rather than by sampling luck"

key-files:
  created:
    - tests/test_par_monitoring_simulation.py
  modified:
    - dsx/mathx.py

key-decisions:
  - "Single commit for Task 2 rather than a RED/GREEN/REFACTOR sequence — the deliverable IS the test file (no separate implementation module to fail against first); documented as a deviation below"
  - "Prior-averaged simulation uses a 1:1 prior over H0/H1 with sequential Gaussian log-likelihood-ratio updating (mirrors Deng, Lu & Chen 2016's setup) rather than a literal SPRT stand-in, so the FDR-vs-1/(K+1) property is tested against the actual mechanism the citation describes"
  - "Seed literal 1969 (Armitage et al.'s publication year) chosen for auditability, not randomness"

patterns-established:
  - "AST scan for dsx/ -> tests/ isolation, widening test_frame_boundary.py's dsx/frame/ -> dsx.checks scanner to the whole dsx/ tree against the tests package"

requirements-completed: [REQ-P9-07]

coverage:
  - id: D1
    description: "inflation_from_peeking() docstring upgraded to a full D-05 citation (Armitage, McPherson & Rowe 1969) with an explicit unverified-locator flag; no executable line changed"
    requirement: REQ-P9-07
    verification:
      - kind: unit
        ref: "tests/test_par_monitoring_simulation.py#test_inflation_from_peeking_docstring_carries_the_full_citation"
        status: pass
      - kind: other
        ref: "python3 scripts/gen-finding-catalogue.py --check"
        status: pass
    human_judgment: false
  - id: D2
    description: "Seeded stdlib simulation proves the point-null (monotone trend, no fixed ceiling) and prior-averaged (fixed 1/(K+1) ceiling at K=19) formulations behave differently, runs under one second, and asserts nothing under dsx/ imports tests/"
    requirement: REQ-P9-07
    verification:
      - kind: unit
        ref: "python3 -m unittest tests.test_par_monitoring_simulation -v (7 tests, all pass)"
        status: pass
      - kind: unit
        ref: "python3 -m unittest discover -s tests -q (426 tests, exit 0)"
        status: pass
      - kind: other
        ref: "sh scripts/check.sh (all sections pass)"
        status: pass
    human_judgment: false

duration: 15min
completed: 2026-08-12
status: complete
---

# Phase 09 Plan 02: Citation upgrade + seeded monitoring-discipline simulation Summary

**`inflation_from_peeking()` now carries a full Armitage, McPherson & Rowe (1969) citation with an honest unverified-locator flag, and a new stdlib-only seeded unittest module proves DSX-PAR-010's point-null trend and DSX-PAR-011's prior-averaged 1/(K+1) ceiling are genuinely different results.**

## Performance

- **Duration:** ~15 min
- **Started:** 2026-08-12T23:02:37+02:00 (prior commit on branch)
- **Completed:** 2026-08-12T23:16:50+02:00
- **Tasks:** 2 completed
- **Files modified:** 2

## Accomplishments

- `dsx/mathx.py::inflation_from_peeking()`'s docstring names Armitage, P., McPherson, C. K. & Rowe, B. C. (1969), "Repeated Significance Tests on Accumulating Data", JRSS Series A 132(2):235-244, DOI 10.2307/2343787 — naming the normal, known-variance, equal-group-size case at two-sided nominal alpha 0.05 — with an explicit statement that no table or page number was verified (subscriber-only source) and that the six anchors are verified by independent quadrature + Monte Carlo, not by citation.
- `tests/test_par_monitoring_simulation.py` created: a seeded (`random.Random(1969)`), stdlib-only (`unittest`, `random`, `math`, `ast`, `pathlib`, `sys`), sub-second (0.2s) unittest module with 7 tests, discovered automatically by `scripts/check.sh`'s default glob with no configuration change.
- Point-null formulation: naive-crossing fraction across a fixed look ladder (1, 2, 5, 10, 20) is proven nondecreasing by simulation structure (one cached Brownian path per trial reused across the ladder), with no fixed ceiling asserted.
- Prior-averaged formulation: observed false-discovery rate among trials that stopped and rejected is at or below `1/(19+1) = 0.05` plus a 3-standard-error one-sided Monte Carlo margin.
- Boundary arithmetic pinned exactly: `1/(19+1)==0.05`, `1/(24+1)==0.04`, `1/(15+1)==0.0625`, and Ville's `1/19` (~0.0526) shown strictly greater than `1/(19+1)`, never a rounding of the same number.
- AST scan proves no `.py` file under `dsx/` imports `tests` or any submodule of it, absolute or relative — the first mechanical enforcement of REQ-P9-07's location boundary.
- Determinism test: two runs from freshly constructed `random.Random(1969)` generators produce identical summary statistics.
- `# D-05: DSX-PAR-011` marker present, satisfying `gen-finding-catalogue.py --check`'s test-marker requirement for the DSX-PAR-011 reference value.

## Task Commits

Each task was committed atomically:

1. **Task 1: Upgrade inflation_from_peeking()'s docstring to a full citation with an honest locator flag** - `bd9af2e` (docs)
2. **Task 2: Seeded stdlib simulation proving the two formulations differ** - `e481814` (test)

**Plan metadata:** (this commit, made after this SUMMARY)

## Files Created/Modified

- `dsx/mathx.py` - `inflation_from_peeking()`'s docstring upgraded with `Citation:` and `Reference value:` lines and an explicit unverified-locator flag; no executable line changed
- `tests/test_par_monitoring_simulation.py` - new seeded stdlib-only simulation module (7 tests) proving the point-null / prior-averaged formulations differ, pinning boundary arithmetic, and enforcing the dsx/ -> tests/ isolation boundary

## Decisions Made

- **Single commit for the TDD-flagged Task 2, not RED/GREEN/REFACTOR.** The plan marks Task 2 `tdd="true"`, but the task's sole deliverable is the test file itself — there is no separate implementation module for the tests to fail against first (the "implementation" is the simulation logic embedded in the test module's own helper functions). Writing the file, running it, and confirming all 7 tests pass in one pass mirrors the shape of `tests/test_frame_boundary.py` and `tests/test_known_bad_corpus.py`, the two existing test-artifact-as-deliverable modules in this repo, both committed as single `test(...)` commits. Documented here rather than forcing an artificial RED phase (e.g. asserting against a not-yet-written helper) that would add no evidentiary value.
- **Prior-averaged simulation design:** 1:1 prior over H0/H1, sequential Gaussian log-likelihood-ratio accumulation (`effect*x - 0.5*effect^2` per draw), stop the first time posterior log-odds reach `log(19)`. This directly instantiates the martingale-based optional-stopping mechanism Deng, Lu & Chen (2016) describe, rather than a generic SPRT stand-in, so the FDR bound is tested against the actual formulation DSX-PAR-011 cites.
- **Seed `1969`** (Armitage et al.'s publication year) — a literal, memorable, non-clock integer, consistent with D-14's "never `random.seed()`, never wall-clock time" requirement.
- **Effect size 2.0 and max_looks=60** for the prior-averaged simulation, chosen so H1 trials converge quickly (expected ~1.5 looks) keeping the whole module's runtime at ~0.2s while still producing >100 rejecting trials (typically ~3000+) for a statistically meaningful FDR estimate.

## Deviations from Plan

### Auto-fixed Issues

None — no bugs, missing functionality, or blocking issues were found; both tasks matched the plan's `<action>` specifications directly.

### Noted Discrepancies in the Plan's Own Acceptance Criteria (not fixed — pre-existing / out of scope)

**1. [Scope boundary] Task 1's second acceptance command has a pre-existing floating-point false negative**
- **Found during:** Task 1 verification
- **Issue:** The plan's acceptance criterion `f(5)==0.142, f(20)==0.248, f(1)==0.05` expects `True True True`, but `f(20)` and `f(1)` print `False` because `value * alpha / 0.05` (the function's existing, unmodified return expression) does not round-trip exactly to the anchor value in IEEE-754 binary64 for those two inputs (e.g. `0.248 * 0.05 / 0.05 == 0.24800000000000003`).
- **Verified pre-existing:** Confirmed via `git stash` that this floating-point behavior is identical on the pre-edit file — it is not caused by the docstring change, and Task 1 explicitly forbids touching the return expression ("Do not change... the return expression"). Per the deviation rules' scope boundary, this is out of scope for this plan and was not fixed.
- **Impact:** None on `f(5)==0.142`, which does hold exactly (confirmed `True`) and is the only anchor value the plan's other, mechanically-verified acceptance criteria (docstring content, `gen-finding-catalogue.py --check`, `unittest discover`) depend on.
- **Not filed as a blocker:** this is an acceptance-criterion authoring artifact in PLAN.md, not a defect in the shipped code.

**2. [Scope boundary] "Running the module twice in separate processes produces identical output" includes unittest's own wall-clock timing line**
- **Found during:** Task 2 verification
- **Issue:** `python3 -m unittest tests.test_par_monitoring_simulation -v` run twice produces byte-identical output except for the `Ran 7 tests in 0.XXXs` line, which unittest always prints with the actual elapsed wall-clock time.
- **Verified:** All 7 test names, docstrings, `ok` results, and the final `OK` status are identical between runs; only the timing line differs. The module's own `test_determinism_same_seed_same_summary_statistic` test (a stricter, in-process equality assertion on the actual simulated statistics) passes and is the mechanically meaningful determinism proof.
- **Not fixed:** out of scope — this is `unittest`'s own stdlib behavior, not something this plan's code controls, and not a correctness concern.

---

**Total deviations:** 0 auto-fixed. 2 noted, pre-existing/out-of-scope acceptance-criteria imprecisions in PLAN.md, neither affecting the shipped code's correctness.
**Impact on plan:** None on scope. Both tasks' actual `<done>` criteria (docstring content, simulation behavior, boundary proofs, isolation proof) are met and independently verified.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `DSX-PAR-011`'s reference value (`1/(K+1)` at `K=19`) now has both a docstring-adjacent citation trail (via `dsx/mathx.py`) and an independent, seeded simulation proof — ready for `09-03`/`09-04`/`09-05` (or whichever plans ship the `DSX-PAR-010`/`DSX-PAR-011` checks themselves) to cite this simulation as evidence without re-deriving it.
- `tests/test_par_monitoring_simulation.py` established a second, wider AST-scan boundary (all of `dsx/` -> `tests/`, vs. `test_frame_boundary.py`'s narrower `dsx/frame/` -> `dsx.checks`) — later phases adding new `dsx/` submodules inherit this check automatically via `rglob("*.py")`, no wiring needed.
- No blockers for other Phase 9 plans: this plan touches no file and introduces no symbol any other Phase 9 plan reads (confirmed no overlap with 09-01's scope at plan-authoring time).

---
*Phase: 09-monitoring-discipline-symmetric-dsx-par*
*Completed: 2026-08-12*
