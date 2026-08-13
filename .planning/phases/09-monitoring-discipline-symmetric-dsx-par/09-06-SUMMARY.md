---
phase: 09-monitoring-discipline-symmetric-dsx-par
plan: 06
subsystem: infra
tags: [dsx, gate, spec-validation, tdd]

# Dependency graph
requires:
  - phase: 09-monitoring-discipline-symmetric-dsx-par
    provides: "09-03 (DSX-PAR-010/011 monitoring-discipline pair) and 09-04 (its known-bad fixtures), both of which this plan closes a gap in"
provides:
  - "dsx/spec.py::is_blank_text — a text-only blank predicate, separate from is_blank"
  - "dsx/frame/paradigm.py::_blank_clearing_declarations routed through is_blank_text, closing the numeric/boolean clearing hole in DSX-PAR-010/DSX-PAR-011"
  - "A corrected references/paradigm-symmetry.md whose cheapest-dishonest-path claim is true of the shipped code"
affects: [09-VERIFICATION, gap-closure]

# Tech tracking
tech-stack:
  added: []
  patterns: ["Genuine runtime cross-product test over a data-driven map (_MONITORING_DISCIPLINE x clearing_fields x value domain) via subTest, matching the existing fourteen-case DSX-PAR-002 idiom"]

key-files:
  created: []
  modified:
    - dsx/spec.py
    - dsx/frame/paradigm.py
    - tests/test_dsx.py
    - references/paradigm-symmetry.md
    - templates/ANALYSIS-SPEC.yaml

key-decisions:
  - "Option A (new is_blank_text helper, is_blank left byte-identical) — already resolved in the plan's <resolved_decision>, implemented as written. Not relitigated."

patterns-established:
  - "Text-only blank predicate (is_blank_text) as the deliberate second tier below the general is_blank, reserved for free-text-only declaration fields."

requirements-completed: [REQ-P9-06]

coverage:
  - id: D1
    description: "A bare 0, 0.0, False, True, empty/non-empty list, or empty/non-empty mapping in inference.alpha_spending, inference.prior_justification, or inference.threshold_calibration no longer clears DSX-PAR-010/DSX-PAR-011; a non-blank string (including the literal string \"0\") still clears; dsx.spec.is_blank is unchanged for all four scalar types."
    requirement: "REQ-P9-06"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestPhase9MonitoringDiscipline::test_non_text_and_blank_values_never_clear_either_half"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestPhase9MonitoringDiscipline::test_non_blank_string_still_clears"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestPhase9MonitoringDiscipline::test_single_character_string_zero_still_clears"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestPhase9MonitoringDiscipline::test_is_blank_unchanged_for_numeric_and_boolean_scalars"
        status: pass
      - kind: e2e
        ref: "tests/test_dsx.py::TestPhase9MonitoringDiscipline::test_numeric_threshold_calibration_blocks_plan_with_both_codes"
        status: pass
    human_judgment: false
  - id: D2
    description: "references/paradigm-symmetry.md states the closed hole by name (new 'What does not clear either half' section), the cheapest-dishonest-path claim is true of the shipped code, and the audit still enumerates both halves against _MONITORING_DISCIPLINE at runtime; templates/ANALYSIS-SPEC.yaml's scaffold comments state the same rule."
    requirement: "REQ-P9-06"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::TestKnownBadCorpus::test_paradigm_symmetry_audit_enumerates_both_halves"
        status: pass
      - kind: other
        ref: "python3 -c \"...whitespace-normalized substring check for ['What does not clear either half','is_blank_text','a number, a boolean','DSX-PAR-010','DSX-PAR-011','alpha_spending','prior_justification','threshold_calibration','sequential_obf','sequential_pocock','always_valid','0.142','0.05']\" -> ok"
        status: pass
    human_judgment: false

# Metrics
duration: ~15min
completed: 2026-08-13
status: complete
---

# Phase 9 Plan 06: Close the numeric/boolean clearing hole in the monitoring pair Summary

**`dsx.spec.is_blank_text` replaces `is_blank` as the clearing predicate for DSX-PAR-010/DSX-PAR-011, so a bare `0`, `0.0` or `False` no longer clears the CRITICAL pair with zero declared content, and `references/paradigm-symmetry.md` now states that fact instead of an audit claim the code contradicted.**

## Performance

- **Duration:** ~15 min
- **Tasks:** 3
- **Files modified:** 5

## Accomplishments

- Closed the gap `09-VERIFICATION.md` scored as a FAILED truth for ROADMAP Phase 9 Success Criterion 5 / REQ-P9-06: declaring `inference.threshold_calibration: 0` (or `0.0`, `False`, `True`, any list, any mapping) on an uncontrolled-continuous design no longer clears `DSX-PAR-010`/`DSX-PAR-011`.
- Added `dsx/spec.py::is_blank_text` as a new, separately named predicate — `dsx.spec.is_blank` itself is byte-identical to before (confirmed by `git diff` showing no change inside its body, plus a positive test that `is_blank(0)` is still `False`).
- Rerouted `dsx/frame/paradigm.py::_blank_clearing_declarations` through `is_blank_text`, updated both `DSX-PAR-010`/`DSX-PAR-011` remedy strings, the third `_MONITORING_DISCIPLINE` structural fact, and the `_INFERENCE_FIELDS` comment in `dsx/spec.py` to name the new predicate.
- Rewrote `references/paradigm-symmetry.md`'s "The honest fix versus the cheap fix" section and added a new "What does not clear either half" section naming every non-clearing value class and the closed history. Updated `templates/ANALYSIS-SPEC.yaml`'s scaffold comments to state the same rule (comment lines only — no YAML key or value changed).

## Task Commits

Each task was committed atomically:

1. **Task 1: RED — pin the type domain of all three clearing declarations** - `e56955c` (test)
2. **Task 2: GREEN — add is_blank_text and route the clearing predicate through it** - `51379cc` (feat)
3. **Task 3: Make the committed audit and the operator-facing template state what the code now does** - `22bbbd9` (docs)

**Plan metadata:** committed alongside this summary (below).

## TDD Gate Compliance

RED confirmed before any implementation: `python3 -m unittest tests.test_dsx.TestPhase9MonitoringDiscipline -v` ran 23 tests (18 pre-existing + 5 new) with **25 assertion failures**, every one naming a paradigm, a field and a value — zero collection/import/syntax errors. Recorded output (representative sample):

```text
FAIL: test_non_text_and_blank_values_never_clear_either_half (...) (paradigm='frequentist', field='alpha_spending', value='0')
AssertionError: 'DSX-PAR-010' not found in {'DSX-PAR-002', 'DSX-PAR-001'}
...
FAIL: test_numeric_threshold_calibration_blocks_plan_with_both_codes (...)
AssertionError: 'DSX-PAR-010' not found in {'DSX-SPEC-001', 'DSX-SPEC-020', 'DSX-SPEC-080'}
Ran 23 tests in 0.183s
FAILED (failures=25)
```

GREEN confirmed after Task 2: `python3 -m unittest tests.test_dsx.TestPhase9MonitoringDiscipline -v` — `Ran 23 tests in 0.213s`, `OK`. Git log order verified: `test(09-06)` at `e56955c` precedes `feat(09-06)` at `51379cc` precedes `docs(09-06)` at `22bbbd9`. No separate `refactor(09-06)` commit — none was needed; Task 2's implementation was minimal on the first pass.

## Files Created/Modified

- `dsx/spec.py` - Added `is_blank_text(value)` directly below `is_blank`; updated the `_INFERENCE_FIELDS` comment to name it. `is_blank` itself unchanged.
- `dsx/frame/paradigm.py` - Added `is_blank_text` to the `from ..spec import` list; `_blank_clearing_declarations` now calls `is_blank_text` instead of `is_blank`; updated its docstring, the third `_MONITORING_DISCIPLINE` structural-fact comment, and both `DSX-PAR-010`/`DSX-PAR-011` `remedy=` strings.
- `tests/test_dsx.py` - Added five tests to `TestPhase9MonitoringDiscipline`: a runtime cross-product over `_MONITORING_DISCIPLINE` and its `clearing_fields` tuples against an 11-value non-clearing domain, two clearing counter-assertions (non-blank string, literal `"0"`), an `is_blank`-unchanged blast-radius test, and an end-to-end `dsx gate plan` test against a numeric `threshold_calibration`. No existing test method was modified.
- `references/paradigm-symmetry.md` - Clearing-conditions table and structural fact 3 now say "non-blank text value" / name `is_blank_text`. New "What does not clear either half" section. "The honest fix versus the cheap fix" section states the one-free-text-declaration cost is a floor, not an overstatement.
- `templates/ANALYSIS-SPEC.yaml` - Comment lines above and on `threshold_calibration`/`prior_justification` now state the non-blank-text-value rule. No YAML key or value changed.

## Decisions Made

None beyond the plan's own `<resolved_decision>` (Option A: new `is_blank_text` helper, `is_blank` untouched) — implemented exactly as specified, not relitigated.

## Deviations from Plan

None — plan executed exactly as written. The one wording adjustment worth noting: while satisfying the acceptance-criteria substring check for `references/paradigm-symmetry.md` (requiring the literal substring `"a number, a boolean"` to survive whitespace normalization), an initial draft used a parenthetical `(int or float)` between "number" and "boolean" that broke the substring match on the first attempt; caught immediately by running the acceptance command and fixed in the same task before committing. Not tracked as a numbered deviation because it never left the working tree in a broken state and no commit carried the defect.

## Issues Encountered

None. `sh scripts/check.sh` produces seven pre-existing "declared twice with different text" warnings (`DSX-COH-030`, `DSX-PAR-002`, `DSX-SPEC-070` x3, `DSX-VAL-021`, `DSX-VAL-060`) on both the unit-test run and the finding-catalogue-currency check. These predate this plan's changes — none of the five files this plan touches declares any of those seven codes — and the catalogue-currency step still exits `0` ("finding catalogue is current"), so they are non-blocking and out of this plan's scope (SCOPE BOUNDARY rule). Not fixed; noted here for visibility, not filed to `deferred-items.md` since they are informational warnings on an already-passing check rather than a discovered defect requiring a fix decision.

## Verification (mandatory, all re-run after the final commit)

- `python3 -m dsx gate plan --spec examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml --json` — exit `1`, CRITICAL codes exactly `['DSX-PAR-010']`.
- `python3 -m dsx gate plan --spec examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml --json` — exit `1`, CRITICAL codes exactly `['DSX-PAR-011']`.
- `python3 -m dsx gate plan/execute/verify/ship --spec examples/good-ANALYSIS-SPEC.yaml` — exit `0` at all four.
- `sh scripts/check.sh` — `Ran 523 tests in 5.5s`, `OK (skipped=2)`; finding catalogue current; capability manifest conformant (`dsx` v2.0.0, 2 steps, 5 contributions, 5 gates, 9 skills, 6 agents, 13 config keys); gate contract and determinism checks pass. Baseline was 518 tests before this plan (Phase 8 merge); the 5 new `TestPhase9MonitoringDiscipline` tests account for the delta to 523.
- `git diff dsx/spec.py` confirms zero change inside the body of `is_blank`.
- Every existing spec in `examples/` and `templates/` was surveyed for behavior change: only `templates/ANALYSIS-SPEC.yaml`'s clearing fields are declared as `null` (already blank under both `is_blank` and `is_blank_text`, so unaffected), and the known-bad/good fixtures' clearing fields are all either blank or non-blank strings — none used a bare number, boolean, list or mapping — so no fixture's finding set changed as a result of this plan beyond the one intended consequence: a non-empty list or mapping in a clearing field now also fails to clear, which is pinned by the new type-domain test and stated in the rewritten audit.

## Next Phase Readiness

This closes the last open gap `09-VERIFICATION.md` recorded for REQ-P9-06 / ROADMAP Phase 9 Success Criterion 5. Plan 09-07 (the other gap-closure plan in this wave, scoped to `REQ-P9-03`) is independent of this plan's files and has no ordering dependency on it.

---
*Phase: 09-monitoring-discipline-symmetric-dsx-par*
*Completed: 2026-08-13*

## Self-Check: PASSED

- FOUND: `.planning/phases/09-monitoring-discipline-symmetric-dsx-par/09-06-SUMMARY.md`
- FOUND: `e56955c` (test RED)
- FOUND: `51379cc` (feat GREEN)
- FOUND: `22bbbd9` (docs — audit and template)
- FOUND: `625731f` (docs — this summary)
