---
phase: 09-monitoring-discipline-symmetric-dsx-par
plan: 03
subsystem: contract
tags: [dsx-par, paradigm-symmetry, monitoring-discipline, finding-catalogue, tdd]

# Dependency graph
requires:
  - phase: 09-monitoring-discipline-symmetric-dsx-par (plan 09-01)
    provides: references/paradigm-symmetry.md, the three coined inference: fields (threshold_calibration, prior_justification, decision_threshold), empty tests/test_known_bad_corpus.py::_EXPECTED_CAUGHT_DEFECTS
  - phase: 09-monitoring-discipline-symmetric-dsx-par (plan 09-02)
    provides: dsx.mathx.inflation_from_peeking()'s full D-05 citation, tests/test_par_monitoring_simulation.py's seeded proof of the two formulations
provides:
  - dsx/frame/paradigm.py::_MONITORING_DISCIPLINE, _blank_clearing_declarations, _check_monitoring_discipline, _UNCONTROLLED_POLICY
  - DSX-PAR-010 (frequentist) and DSX-PAR-011 (bayesian) — both CRITICAL, both shipped in the same commit range
  - tests/test_dsx.py::TestPhase9MonitoringDiscipline — the full behavioural specification for the pair
  - tests/test_known_bad_corpus.py::_EXPECTED_CAUGHT_DEFECTS filled in for both monitoring fixtures
  - references/finding-codes.md regenerated with both new rows
affects: [09-04, 09-05]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Data-driven per-paradigm map (_MONITORING_DISCIPLINE) evaluated by one shared predicate (_blank_clearing_declarations) as the mechanical proof of a D-12 symmetric pair's cost equality — same idiom Phase 6's _PARADIGM_CONDITIONAL already established"
    - "Undeclared-paradigm case selects the union of every conditional row instead of none, closing an escape at CRITICAL without spending a new finding code"

key-files:
  created: []
  modified:
    - dsx/frame/paradigm.py
    - dsx/frame/__init__.py
    - tests/test_dsx.py
    - tests/test_known_bad_corpus.py
    - references/finding-codes.md

key-decisions:
  - "Both codes ship from one function, _check_monitoring_discipline, whose single docstring carries both codes' Citation:/Reference value: lines — the catalogue's docstring resolver walks up to the nearest enclosing FunctionDef, so splitting into two functions would have bought nothing and one function keeps the shared-predicate symmetry visible in one place"
  - "The undeclared-paradigm escape (Question 1 in the plan's resolved_open_questions) is closed by having the undeclared case select every row of _MONITORING_DISCIPLINE, not by spending a new finding code — preserves brief D-10 (declaring a paradigm never adds a finding, only ever removes one) and DSX-PAR-002 stays HIGH exactly as D-02 locks it"
  - "DSX-PAR-011 performs no numeric comparison on the gate path (Question 2) — presence-only, mirroring DSX-PAR-010's own presence-only shape; the 1/(K+1) figure is asserted only as a fixed reference-value string in the docstring, a unit test, and the seeded simulation from 09-02, never computed from any operator-declared value"

requirements-completed: [REQ-P9-01, REQ-P9-02, REQ-P9-03, REQ-P9-05]

coverage:
  - id: D1
    description: "DSX-PAR-010 fires at CRITICAL for the frequentist known-bad fixture at dsx gate plan, DSX-PAR-011 fires at CRITICAL for the bayesian known-bad fixture, both in the same commit range at identical severity"
    requirement: "REQ-P9-01"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestPhase9MonitoringDiscipline::test_frequentist_known_bad_fixture_blocks_plan_with_dsx_par_010"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestPhase9MonitoringDiscipline::test_bayesian_known_bad_fixture_blocks_plan_with_dsx_par_011"
        status: pass
      - kind: other
        ref: "python3 -c \"from dsx.frame.paradigm import _MONITORING_DISCIPLINE as m, _NOT_SHIPPED as n; from dsx.spec import PARADIGMS; print(set(m)==set(PARADIGMS), len({len(v[1]) for v in m.values()})==1, 'DSX-PAR-010' not in n, 'DSX-PAR-011' not in n, 'DSX-PAR-002' in n)\" -> True True True True True"
        status: pass
    human_judgment: false
  - id: D2
    description: "Neither half is escaped by retyping inference.paradigm to the other member of PARADIGMS — asserted in both directions against the real committed fixtures"
    requirement: "REQ-P9-05"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestPhase9MonitoringDiscipline::test_retyping_frequentist_fixture_to_bayesian_yields_dsx_par_011_not_010"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestPhase9MonitoringDiscipline::test_retyping_bayesian_fixture_to_frequentist_yields_dsx_par_010_not_011"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestPhase9MonitoringDiscipline::test_monitoring_discipline_map_is_symmetric_across_paradigms"
        status: pass
    human_judgment: false
  - id: D3
    description: "DSX-PAR-010's finding detail reuses dsx.mathx.inflation_from_peeking() directly (0.142 at five looks, 0.248 at twenty at nominal alpha 0.05) — no second inflation table exists anywhere in the codebase"
    requirement: "REQ-P9-01"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestPhase9MonitoringDiscipline::test_dsx_par_010_reference_values_reuse_inflation_from_peeking"
        status: pass
      - kind: other
        ref: "git diff dsx/checks/design.py dsx/cli.py -> empty (no second table module touched)"
        status: pass
    human_judgment: false
  - id: D4
    description: "DSX-PAR-011's docstring states the prior-averaged (not point-null/law-of-iterated-logarithm) formulation, the 1/(K+1) == 1-p identity at p=0.95, and names Ville's 1/k as a different result over a different conditioning event; no arithmetic is performed on any operator-declared value on the gate path, including a decision_threshold string crafted with format/shell metacharacters"
    requirement: "REQ-P9-03"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestPhase9MonitoringDiscipline::test_dsx_par_011_reference_value_boundary_arithmetic"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestPhase9MonitoringDiscipline::test_arbitrary_decision_threshold_string_produces_identical_finding_text"
        status: pass
      - kind: other
        ref: "python3 scripts/gen-finding-catalogue.py --check -> exit 0 (D-05 Citation:/Reference value: lines present for both codes)"
        status: pass
    human_judgment: false
  - id: D5
    description: "The two peeking codes (DSX-PAR-010, DSX-EXP-060) never both fire against the same spec across every PEEKING_POLICIES member; a spec with no design:/inference: block or a blank peeking_policy triggers neither code; dsx audit --json is byte-identical across two runs"
    requirement: "REQ-P9-01"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestPhase9MonitoringDiscipline::test_dsx_par_010_and_dsx_exp_060_are_disjoint_across_every_peeking_policy"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestPhase9MonitoringDiscipline::test_neither_code_fires_for_a_non_uncontrolled_peeking_policy"
        status: pass
      - kind: other
        ref: "sh scripts/check.sh -> all checks passed (447 tests, catalogue current, gate contract, determinism)"
        status: pass
    human_judgment: false

duration: ~55min
completed: 2026-08-12
status: complete
---

# Phase 9 Plan 3: Symmetric DSX-PAR-010/DSX-PAR-011 monitoring-discipline pair Summary

**Shipped `DSX-PAR-010` (frequentist) and `DSX-PAR-011` (bayesian) — both CRITICAL, both from one data-driven `_MONITORING_DISCIPLINE` map evaluated by one shared clearing predicate — closing the paradigm-retype and undeclared-paradigm escapes without spending a new finding code.**

## Performance

- **Duration:** ~55 min
- **Completed:** 2026-08-12
- **Tasks:** 3 completed (RED / GREEN / repair-and-regenerate)
- **Files modified:** 5 (dsx/frame/paradigm.py, dsx/frame/__init__.py, tests/test_dsx.py, tests/test_known_bad_corpus.py, references/finding-codes.md)

## Accomplishments

- `dsx/frame/paradigm.py::_MONITORING_DISCIPLINE` — a dict keyed by every member of `PARADIGMS`, each row naming its finding code and its tuple of clearing declarations (`threshold_calibration` shared by both rows; `alpha_spending`/`prior_justification` paradigm-specific), with a contract test proving `set(_MONITORING_DISCIPLINE) == set(PARADIGMS)`, equal tuple lengths, and `threshold_calibration` present in every row
- `_blank_clearing_declarations()` — the single predicate every clearing declaration for every paradigm is evaluated by, the mechanical proof that neither half is cheaper to satisfy dishonestly than the other (brief D-12)
- `_check_monitoring_discipline()` — triggers on `design.peeking_policy == "uncontrolled_continuous"` only, never reads `results.interim_looks` (D-04, keeps the trigger readable at `dsx gate plan`), and selects every row when no paradigm is declared or an unrecognised one is named, closing the undeclared-paradigm escape at CRITICAL without a new finding code
- `DSX-PAR-010` reuses `dsx.mathx.inflation_from_peeking()` directly — 0.142 at five looks, 0.248 at twenty, at nominal alpha 0.05; no second table
- `DSX-PAR-011`'s docstring carries the full Deng, Lu & Chen (2016) citation, states the prior-averaged formulation explicitly (not point-null/law-of-iterated-logarithm), the `1/(K+1) == 1-p` identity at `p = 0.95`, and the Ville `1/k` contrast — with a behavioural test proving an arbitrary `decision_threshold` string (containing brace/percent/dollar/backtick/semicolon characters) produces byte-identical finding text to a blank one
- Both known-bad fixtures now block `dsx gate plan` with their own code, and both retype directions (frequentist fixture retyped to `bayesian`, and vice versa) produce the *other* code and not the original — proving REQ-P9-05 structurally rather than by two hand-written assertions
- `dsx/frame/paradigm.py::check()`'s undeclared-paradigm manifest branch now selects the union of every `_PARADIGM_CONDITIONAL` row (matching the pair's real behaviour) instead of none, with updated detail/counterfactual text
- `dsx/frame/__init__.py`'s D-03a boundary prose now names `dsx.mathx` as a permitted pure-computation import
- `tests/test_dsx.py::TestPhase6ParadigmManifest::test_applied_prefixes_have_codes_and_not_shipped_prefixes_have_none` repaired into a strictly stronger, two-directional assertion (not-shipped prefixes resolve to zero known codes; not-selected-for-this-paradigm prefixes now resolve to at least one)
- `tests/test_known_bad_corpus.py::_EXPECTED_CAUGHT_DEFECTS` filled in for both monitoring fixtures
- `references/finding-codes.md` regenerated: two new CRITICAL rows, non-placeholder titles, D-05 citation/reference-value/test-marker checks pass
- Full suite green: 447 tests, `sh scripts/check.sh` exits 0, `dsx audit --json` determinism holds

## Task Commits

Each task was committed atomically, following the plan's RED/GREEN/repair structure:

1. **Task 1 RED: failing tests for both halves before either exists** - `0a2e536` (test)
2. **Task 2 GREEN: implement the symmetric monitoring-discipline pair** - `df20ef6` (feat)
3. **Task 3: repair the two invariants the pair changes, regenerate catalogue** - `026d557` (test)

**Plan metadata:** commit pending (this SUMMARY.md, applied per worktree-mode rules — STATE.md/ROADMAP.md are owned by the orchestrator)

## Files Created/Modified

- `dsx/frame/paradigm.py` — `_UNCONTROLLED_POLICY`, `_MONITORING_DISCIPLINE`, `_blank_clearing_declarations()`, `_check_monitoring_discipline()` added; `_NOT_SHIPPED` loses its `DSX-PAR-010`/`DSX-PAR-011` entries; `check()` now calls the new helper and the undeclared-paradigm manifest branch selects the union of every conditional row
- `dsx/frame/__init__.py` — D-03a boundary prose amended to name `dsx.mathx` as a permitted pure-computation import
- `tests/test_dsx.py` — new `TestPhase9MonitoringDiscipline` class (18 tests); `TestPhase6ParadigmManifest::test_applied_prefixes_have_codes_and_not_shipped_prefixes_have_none` repaired into a two-directional assertion
- `tests/test_known_bad_corpus.py` — `_EXPECTED_CAUGHT_DEFECTS` filled in for `frequentist-uncontrolled-continuous` and `bayesian-continuous-monitoring`
- `references/finding-codes.md` — regenerated; two new rows under `DSX-PAR-*`, total code count 221 -> 223

## Decisions Made

- Both codes emitted from one function (`_check_monitoring_discipline`) rather than two, so the catalogue's docstring resolver (which walks up to the nearest enclosing `FunctionDef`) finds both codes' `Citation:`/`Reference value:` material in one place — matches the plan's explicit instruction that a function emitting both codes must carry both codes' citation material in its own docstring
- The undeclared-paradigm escape (plan's resolved Question 1) is closed by having the undeclared case select every row of `_MONITORING_DISCIPLINE`, never by spending a new finding code — preserves brief D-10 (an honest declaration never costs more than silence) and leaves `DSX-PAR-002` at HIGH exactly as D-02 locks it (that code ships separately in plan 09-05)
- `DSX-PAR-011` performs no numeric comparison on the gate path (plan's resolved Question 2) — presence-only, symmetric with `DSX-PAR-010`'s own presence-only shape. The `1/(K+1)` figure lives only in the docstring's `Reference value:` line, a pinned unit test, and the seeded simulation from 09-02, never as a computation over `inference.decision_threshold` or any other operator-declared value

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] `_check_monitoring_discipline`'s initial docstring formatting did not satisfy `gen-finding-catalogue.py`'s D-05 regexes**
- **Found during:** Task 3 (`python3 scripts/gen-finding-catalogue.py --check`)
- **Issue:** The docstring originally wrote `Citation (DSX-PAR-010): ...` and `Reference value (DSX-PAR-010): ...` — the code parenthetical between the label and the colon broke `gen-finding-catalogue.py`'s anchored regexes (`^\s*Citation:\s*\S` and `^\s*(?:Reference value|Structural criterion):\s*\S`), which require the literal label immediately followed by a colon
- **Fix:** Reworded to `Citation: (DSX-PAR-010) ...` and `Reference value: (DSX-PAR-010) ...` — content unchanged, now matches the regex, `--check` passes
- **Files modified:** `dsx/frame/paradigm.py`
- **Verification:** `python3 scripts/gen-finding-catalogue.py --check` exits 0; `sh scripts/check.sh` exits 0
- **Committed in:** `026d557` (Task 3 commit)

---

**Total deviations:** 1 auto-fixed (Rule 1, docstring formatting only — no change in citation content, reference values, or behaviour)
**Impact on plan:** None on scope or correctness. The fix was purely mechanical (regex-literal alignment) and is exactly the kind of trap the plan itself flagged ("this trap already bit plan 06-07").

## Issues Encountered

None beyond the deviation above.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `DSX-PAR-010`/`DSX-PAR-011` are now the fully shipped, atomic, symmetric pair the phase exists to deliver — plan 09-04 (the corpus/simulation-facing work) and plan 09-05 (`DSX-PAR-002`'s HIGH-severity requiredness half) can now build against a working, tested pair rather than a design document
- `tests/test_known_bad_corpus.py::_EXPECTED_CAUGHT_DEFECTS` still has two empty entries (`interference-shared-budget`, `weak-identification-mmm`) — untouched by this plan, unrelated to Phase 9's monitoring pair
- No blockers

---
*Phase: 09-monitoring-discipline-symmetric-dsx-par*
*Completed: 2026-08-12*
