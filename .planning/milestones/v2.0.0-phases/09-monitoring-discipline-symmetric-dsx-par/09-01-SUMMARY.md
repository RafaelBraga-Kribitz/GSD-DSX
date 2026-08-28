---
phase: 09-monitoring-discipline-symmetric-dsx-par
plan: 01
subsystem: contract
tags: [dsx-spec, paradigm-symmetry, inference-fields, known-bad-corpus, dsx-par]

# Dependency graph
requires:
  - phase: 06-contract-decision-paradigm-manifest
    provides: PARADIGMS, PARADIGM_JUSTIFICATIONS, _INFERENCE_FIELDS (six-member), describe_vocabulary(), dsx/frame/paradigm.py's DSX-PAR-001 manifest, PEEKING_POLICIES.uncontrolled_continuous
provides:
  - references/paradigm-symmetry.md — the committed, pre-code symmetry audit for DSX-PAR-010/DSX-PAR-011 (D-15, REQ-P9-06)
  - _INFERENCE_FIELDS extended to nine members (threshold_calibration, prior_justification, decision_threshold)
  - describe_vocabulary()["inference_fields"] — the discovery mechanism for the new fields (D-05)
  - templates/ANALYSIS-SPEC.yaml's inference: scaffold declaring all nine fields
  - tests/test_known_bad_corpus.py::_EXPECTED_CAUGHT_DEFECTS — empty per-fixture map, read by both corpus gate tests
affects: [09-02, 09-03, 09-04, 09-05]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Free-text-scalar clearing declarations, evaluated by one shared blank-check predicate, as the mechanism that makes a D-12 symmetric pair's cost-of-dishonest-satisfaction provable rather than merely code-existence provable"
    - "Per-fixture expected-caught-defect map (dict[str, frozenset[str]]) as the general, both-gate-point form of a known-bad fixture's target-check assertion, coexisting with the narrower single-code plan-only _EXPECTED_PLAN_BLOCKERS exception from plan 07-07"

key-files:
  created:
    - references/paradigm-symmetry.md
  modified:
    - README.md
    - dsx/spec.py
    - templates/ANALYSIS-SPEC.yaml
    - tests/test_dsx.py
    - tests/test_known_bad_corpus.py

key-decisions:
  - "The audit is written before either DSX-PAR-010 or DSX-PAR-011 exists, so it constrains what later Phase 9 plans build rather than describing it after the fact (D-15, PITFALLS.md Pitfall 7)"
  - "threshold_calibration, prior_justification and decision_threshold are all free-text scalars, never a {method:, sims:, fpr:} sub-dict — giving every clearing declaration on both paradigms the same shape and the same blank-check predicate is what makes the D-12 cost-symmetry claim mechanically provable"
  - "_EXPECTED_CAUGHT_DEFECTS is additive to, not a replacement for, the existing _EXPECTED_PLAN_BLOCKERS mechanism (added by plan 07-07, after this plan was drafted) — the two express genuinely different scopes: a single code blocking at plan only vs. a set of codes blocking at every CRITICAL-threshold gate point"

requirements-completed: [REQ-P9-02, REQ-P9-06]

coverage:
  - id: D1
    description: "references/paradigm-symmetry.md exists, is committed outside .planning/, and enumerates both DSX-PAR-010/DSX-PAR-011 clearing conditions, the honest fix, the cheapest dishonest fix, the equal cost of that fix on both sides, the gate's known limit, the undeclared-paradigm case, and the 0.142/0.05 reference values with the 1/(K+1) vs 1/k distinction"
    requirement: "REQ-P9-06"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::TestKnownBadCorpus (13 pre-existing tests, all green against the new file's absence of retired phrasing)"
        status: pass
      - kind: other
        ref: "grep -c paradigm-symmetry README.md >= 1; grep of the six required terms (DSX-PAR-010, DSX-PAR-011, alpha_spending, prior_justification, threshold_calibration, sequential_obf, sequential_pocock, always_valid, 0.142, 0.05, 1/(K+1), 1/k) in references/paradigm-symmetry.md"
        status: pass
    human_judgment: false
  - id: D2
    description: "_INFERENCE_FIELDS is a nine-member tuple (paradigm, paradigm_justification, declared_at, primary_procedure, alpha_spending, fallback_rule, threshold_calibration, prior_justification, decision_threshold); the drift guard asserts that literal"
    requirement: "REQ-P9-02"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure::test_inference_fields_constant_matches_req_p6_04"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure::test_describe_vocabulary_inference_fields_matches_the_constant"
        status: pass
    human_judgment: false
  - id: D3
    description: "dsx vocab exposes an inference_fields key listing all nine field names, including the three new ones, and the template's inference: scaffold declares all three new fields while still clearing dsx gate plan"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure::test_template_validity_frame_and_inference_round_trip"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestCLI::test_template_validity_frame_and_inference_pass_gate_plan"
        status: pass
      - kind: other
        ref: "./bin/dsx vocab | inference_fields key contains threshold_calibration, prior_justification, decision_threshold"
        status: pass
    human_judgment: false
  - id: D4
    description: "tests/test_known_bad_corpus.py::_EXPECTED_CAUGHT_DEFECTS exists, keyed by all four corpus fixtures, every entry empty, and is read by both the plan/execute gate-points test and the ship-gate undocumented-findings test; sh scripts/check.sh is green"
    requirement: "REQ-P9-06"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::TestKnownBadCorpus::test_expected_caught_defects_keys_match_the_corpus_on_disk"
        status: pass
      - kind: other
        ref: "sh scripts/check.sh"
        status: pass
    human_judgment: false

duration: 20min
completed: 2026-08-12
status: complete
---

# Phase 9 Plan 1: Symmetry audit, inference-field coinage, empty corpus map Summary

**Committed the pre-code `DSX-PAR-010`/`DSX-PAR-011` symmetry audit, extended `_INFERENCE_FIELDS` to nine members with `dsx vocab` discovery, and seeded an empty per-fixture expected-caught-defect map in the known-bad corpus suite — no new finding codes ship yet.**

## Performance

- **Duration:** ~20 min
- **Completed:** 2026-08-12
- **Tasks:** 3 completed
- **Files modified:** 6 (1 created, 5 modified)

## Accomplishments
- `references/paradigm-symmetry.md` — a hand-written, committed audit stating the exact clearing conditions, honest-vs-cheapest-dishonest fix, known limit, undeclared-paradigm handling, and the `0.142`/`1/(K+1)=0.05` reference values (with the Deng-Theorem-1-vs-Ville distinction) for the not-yet-built `DSX-PAR-010`/`DSX-PAR-011` pair — written first so it constrains later Phase 9 plans rather than describing them
- `_INFERENCE_FIELDS` extended from six to nine members (`threshold_calibration`, `prior_justification`, `decision_threshold`), with no change to `_INFERENCE_MEMBERSHIP` or `_VOCABULARIES` — all three remain free-text scalars with no closed vocabulary
- `describe_vocabulary()["inference_fields"]` — a second special case (alongside `chart_capabilities`) giving `dsx vocab` visibility into all nine field names, since there is no unknown-key check under `inference:`
- `templates/ANALYSIS-SPEC.yaml`'s `inference:` scaffold now declares all nine fields; the template still clears `dsx gate plan`
- `tests/test_known_bad_corpus.py::_EXPECTED_CAUGHT_DEFECTS` — a per-fixture, empty-today map read by both restructured corpus gate tests, plus a new drift guard tying its keys to the fixtures on disk

## Task Commits

Each task was committed atomically (Task 2 followed the TDD RED/GREEN cycle):

1. **Task 1: Write the paradigm symmetry audit before any check exists** - `27d0b5d` (docs)
2. **Task 2 RED: failing tests for the three new inference: fields** - `2ae2118` (test)
2. **Task 2 GREEN: coin the three new inference: fields and make them discoverable** - `7ea829c` (feat)
3. **Task 3: Introduce the per-fixture expected-caught-defect map, empty** - `02b1cc3` (test)

**Plan metadata:** commit pending (this SUMMARY + STATE/ROADMAP, applied centrally by the orchestrator after wave merge)

## Files Created/Modified
- `references/paradigm-symmetry.md` - New committed audit: clearing-condition table, honest/cheapest-dishonest fix, known limit, undeclared-paradigm case, reference values
- `README.md` - One paragraph linking "Two tiers of evidentiary rigour" to the new audit
- `dsx/spec.py` - `_INFERENCE_FIELDS` extended to nine members; `describe_vocabulary()` gains `inference_fields`
- `templates/ANALYSIS-SPEC.yaml` - `inference:` scaffold gains `threshold_calibration`, `prior_justification`, `decision_threshold`
- `tests/test_dsx.py` - Nine-member drift-guard literal; two new tests; existing template round-trip test's expected key set widened (Rule 1)
- `tests/test_known_bad_corpus.py` - `_EXPECTED_CAUGHT_DEFECTS` constant; both gate-points/ship tests rewired to read it; one new key-coverage test

## Decisions Made
- Wrote the symmetry audit as the design constraint, in the present tense, describing what Phase 9 is committed to build — not a report of measured behavior (D-15)
- Kept `threshold_calibration`/`prior_justification`/`decision_threshold` as scalars, never a sub-dict, so the D-12 cost-symmetry claim reduces to "same predicate, same field shape" rather than requiring per-field inspection
- Did not touch `_INFERENCE_MEMBERSHIP` or `_VOCABULARIES` — none of the three new fields carries a closed vocabulary (D-08 scope stays with `PARADIGM_JUSTIFICATIONS`)
- Kept the new `_EXPECTED_CAUGHT_DEFECTS` mechanism additive alongside the pre-existing `_EXPECTED_PLAN_BLOCKERS` (introduced by plan 07-07, after this plan's context was drafted) rather than merging or replacing it — see Deviations below

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Widened `test_template_validity_frame_and_inference_round_trip`'s expected inference-key set**
- **Found during:** Task 2 (GREEN implementation)
- **Issue:** An existing test pinned the template's `inference:` key set to the old six-field literal; extending the template to nine fields (as the task requires) made this pre-existing, in-scope test fail
- **Fix:** Widened the expected `set` literal to include `threshold_calibration`, `prior_justification`, `decision_threshold`
- **Files modified:** tests/test_dsx.py
- **Verification:** `python3 -m unittest tests.test_dsx -v` — 251 tests, all green
- **Committed in:** `7ea829c` (Task 2 GREEN commit)

**2. [Rule 3 - Blocking, structural] `tests/test_known_bad_corpus.py` had already been restructured once by plan 07-07 (`_EXPECTED_PLAN_BLOCKERS`), before this plan's `<read_first>` line numbers were valid**
- **Found during:** Task 3 planning
- **Issue:** The plan's task 3 was drafted against an earlier version of `tests/test_known_bad_corpus.py` (before Phase 7's plan 07-07 shipped `_EXPECTED_PLAN_BLOCKERS`, a narrower plan-only, single-code exception for the `weak-identification-mmm` fixture). Introducing `_EXPECTED_CAUGHT_DEFECTS` exactly as specified, without accounting for the existing mechanism, risked silently regressing that fixture's already-shipped `DSX-VAL-040` block-at-plan assertion
- **Fix:** Kept `_EXPECTED_PLAN_BLOCKERS` untouched and added `_EXPECTED_CAUGHT_DEFECTS` as an independent, additive mechanism in both restructured tests — the two express genuinely different scopes (one code blocking at `plan` only vs. a set of codes expected at every CRITICAL-threshold point, matching how `DSX-PAR-010`/`DSX-PAR-011`'s `paradigm` check family, unlike `val`, is registered at both `plan` and `execute`)
- **Files modified:** tests/test_known_bad_corpus.py
- **Verification:** `python3 -m unittest tests.test_known_bad_corpus -v` — 14 tests, all green (13 pre-existing + 1 new); `sh scripts/check.sh` green
- **Committed in:** `02b1cc3` (Task 3 commit)

---

**Total deviations:** 2 auto-fixed (1 Rule 1 test-widening, 1 Rule 3 structural accommodation)
**Impact on plan:** Both were necessary to keep the full suite green while landing the plan's actual required shape. No scope creep — no new finding codes, no new check logic, no touches to `_INCIDENTAL_GAP_CODES`, `_TARGET_CODE_FAMILIES`, `test_incidental_allowlist_names_no_target_family_code`, `_INFERENCE_MEMBERSHIP`, or `_VOCABULARIES`.

## Issues Encountered
None beyond the two deviations above.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Plans 09-02 through 09-05 can now build `DSX-PAR-010`/`DSX-PAR-011`/`DSX-PAR-002` against a locked clearing-condition contract (`references/paradigm-symmetry.md`) and a discoverable, coined field set (`_INFERENCE_FIELDS`, `dsx vocab`)
- Whichever plan ships each half of the atomic pair must, in the same commit: remove that code's `_NOT_SHIPPED` entry in `dsx/frame/paradigm.py`, flip that fixture's `_EXPECTED_CAUGHT_DEFECTS` entry from `frozenset()` to the shipped code(s), and update the fixture's header/post-mortem "nothing adjudicates it today" prose (per this plan's `_EXPECTED_CAUGHT_DEFECTS` comment and the phase's `<code_context>`)
- No blockers

---
*Phase: 09-monitoring-discipline-symmetric-dsx-par*
*Completed: 2026-08-12*

## Self-Check: PASSED

- FOUND: references/paradigm-symmetry.md
- FOUND: .planning/phases/09-monitoring-discipline-symmetric-dsx-par/09-01-SUMMARY.md
- FOUND commit: 27d0b5d (Task 1)
- FOUND commit: 2ae2118 (Task 2 RED)
- FOUND commit: 7ea829c (Task 2 GREEN)
- FOUND commit: 02b1cc3 (Task 3)
- FOUND commit: 910fc41 (SUMMARY.md)
