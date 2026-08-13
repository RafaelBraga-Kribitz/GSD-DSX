---
phase: 08-interference-triggering-stability-dsx-int
plan: 08
subsystem: gate
tags: [python, stdlib, dsx-frame, interference, sutva, gap-closure, tdd]

# Dependency graph
requires:
  - phase: 08-03
    provides: DSX-INT-010/011 (_check_interference_unaddressed, _check_interference_mitigation_admissibility)
  - phase: 08-07
    provides: "the mitigation-field precedent fix (commit f669607) this plan mirrors on the risk field"
provides:
  - "DSX-INT-010 fires when interference.risk is out-of-vocabulary, not just when it is literally 'none' or absent — closes 08-VERIFICATION.md gap 1 / 08-REVIEW.md CR-01's second instance"
  - "DSX-SPEC-082 confirmed to keep firing independently beside DSX-INT-010 on the same out-of-vocabulary-risk input"
  - "Module-level _gate_findings(spec_path, point) helper in tests/test_frame_interference.py, reusable by any future gate-level structured-findings assertion in that module"
affects: [10, 11, 12]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Vocabulary-membership-as-absence, applied to the risk field to match the mitigation-field precedent from 08-07: an unrecognised enum-like string is treated as equivalent to 'not declared' for the purposes of a CRITICAL-threshold check"
    - "Structured-findings gate-level test assertion (parsed --json finding list, keyed by code) rather than a rendered-text substring assertion, closing the WR-01 vacuous-assertion failure mode for this specific test"

key-files:
  created: []
  modified:
    - dsx/frame/interference.py
    - tests/test_frame_interference.py

key-decisions:
  - "Fix scoped to _check_interference_unaddressed's risk guard only; _check_interference_mitigation_admissibility's own risk guard (line 296, unchanged) deliberately left alone so DSX-INT-010/DSX-INT-011 stay disjoint by construction for the out-of-vocabulary-risk case — verified via a git diff acceptance check showing no hunk inside that function"
  - "_check_triggering_dilution not touched — that guard is plan 08-09's scope, confirmed by a git diff acceptance check"
  - "Gate-level regression test asserts against the parsed --json finding list, keyed by code, rather than rendered report text, because DSX-INT-010's own detail text names DSX-SPEC-082 unconditionally (the WR-01 failure mode 08-REVIEW.md documented for the mitigation-field variant of this same test)"

patterns-established:
  - "RED-then-GREEN across two commits for a critical bypass fix (Task 1 test-only commit, Task 2 fix-only commit), matching the shape 08-07 established for the mitigation-field sibling defect"

requirements-completed: [REQ-P8-01, REQ-P8-02]

coverage:
  - id: D1
    description: "An out-of-vocabulary interference.risk value (e.g. shared_buget) with no mitigation and a blank residual_note fires DSX-INT-010 (CRITICAL) instead of silently bypassing it"
    requirement: "REQ-P8-01"
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py#TestInterferenceUnaddressed.test_out_of_vocabulary_risk_with_no_mitigation_and_blank_residual_still_fires_int_010"
        status: pass
      - kind: integration
        ref: "tests/test_frame_interference.py#TestInterferenceGateLevel.test_out_of_vocabulary_risk_variant_blocks_plan_naming_both_int_010_and_spec_082"
        status: pass
      - kind: manual_procedural
        ref: "python3 -m dsx gate plan --spec <mutated shared-budget fixture, risk: shared_buget> --json — exit 1, DSX-INT-010/CRITICAL + DSX-SPEC-082/HIGH (where: spec.validity_frame.interference.risk)"
        status: pass
    human_judgment: false
  - id: D2
    description: "DSX-INT-011 stays disjoint from DSX-INT-010 after the fix, for the out-of-vocabulary-risk case, proven from the structured finding list and from a git diff showing _check_interference_mitigation_admissibility unedited"
    requirement: "REQ-P8-02"
    verification:
      - kind: integration
        ref: "tests/test_frame_interference.py#TestInterferenceGateLevel.test_out_of_vocabulary_risk_variant_blocks_plan_naming_both_int_010_and_spec_082 (asserts DSX-INT-011 absent from by_code)"
        status: pass
      - kind: other
        ref: "git diff HEAD~1 -- dsx/frame/interference.py shows no hunk inside _check_interference_mitigation_admissibility or _check_triggering_dilution"
        status: pass
    human_judgment: false
  - id: D3
    description: "No collateral damage to 08-VERIFICATION.md truths 2, 4, 5, 6, 7 (risk/mitigation distinctness, ratio-metric scope boundary, novelty/primacy severity split, paradigm-read boundary, known-bad corpus guards)"
    verification:
      - kind: unit
        ref: "python3 -m unittest discover -s tests — 533 tests, OK (skipped=2); sh scripts/check.sh — all checks passed; python3 scripts/gen-finding-catalogue.py --check — exit 0"
        status: pass
    human_judgment: false

duration: ~25min
completed: 2026-08-13
status: complete
---

# Phase 08 Plan 08: Interference risk out-of-vocabulary gate-bypass closure Summary

**Closed the second instance of the 08-REVIEW.md CR-01 gate-bypass class — an out-of-vocabulary `interference.risk` string (e.g. `shared_buget`) no longer clears `dsx gate plan` for a declared, unmitigated interference risk — with a RED-then-GREEN commit pair mirroring plan 08-07's fix on the adjacent `mitigation` field.**

## Performance

- **Duration:** ~25 min
- **Completed:** 2026-08-13
- **Tasks:** 2
- **Files modified:** 2 (`tests/test_frame_interference.py`, `dsx/frame/interference.py`)

## Accomplishments

- Reproduced 08-VERIFICATION.md's first failed truth with two failing regression tests (unit-level and gate-level) before touching production code — both confirmed to fail for the documented reason (empty finding set at unit level; exit code 0 at gate level), and no other test in the 531-test baseline suite broke.
- Fixed `_check_interference_unaddressed`'s risk guard in `dsx/frame/interference.py`: only the honestly-declared `risk: none` case now short-circuits the judgment; an out-of-vocabulary risk string falls through and is adjudicated, with `_RISK_MITIGATION_MAP.get(normalized_risk, ())`'s existing fallback naturally degrading to `(none admissible)` remedy text.
- Confirmed by `git diff` that `_check_interference_mitigation_admissibility` (DSX-INT-011) and `_check_triggering_dilution` (DSX-INT-030, plan 08-09's scope) are both byte-for-byte unedited — disjointness between DSX-INT-010 and DSX-INT-011 for the out-of-vocabulary-risk case holds by construction, not by re-derivation.
- Added a module-level `_gate_findings(spec_path, point)` helper (moved from `TestKnownBadCorpus._gate_findings`'s shape) so the new gate-level test asserts against the parsed `--json` structured finding list rather than rendered report text — avoiding the WR-01 vacuous-assertion failure mode 08-REVIEW.md documented for the mitigation-field variant of this same test, since `DSX-INT-010`'s own `detail` text names `DSX-SPEC-082` unconditionally.
- Restated the docstring's firing-condition and disjointness paragraphs, the risk-guard's inline comment, and the `DecisionRecord.rule` text so the decision trail matches the corrected code, without reproducing the removed `normalized_risk not in INTERFERENCE_RISKS` expression anywhere except the one surviving occurrence inside `_check_interference_mitigation_admissibility`.
- Re-confirmed all five must-not-regress truths from 08-VERIFICATION.md (risk/mitigation distinctness, ratio-metric scope boundary, novelty/primacy severity split, paradigm-read boundary, known-bad corpus guards) with real command output, plus `sh scripts/check.sh` and `python3 scripts/gen-finding-catalogue.py --check`.

## Task Commits

Each task was committed atomically, with the RED (test) commit landing before the GREEN (fix) commit:

1. **Task 1: Write the two failing out-of-vocabulary-risk regression tests, asserting on structured findings** — `eb8ae4c` (test)
2. **Task 2: Adjudicate an unrecognised interference risk instead of dropping it, so DSX-INT-010 fires again** — `cf4da61` (fix)

**Plan metadata:** commit created after this summary via the SDK's `commit` verb — see final commit in git log.

## Files Created/Modified

- `tests/test_frame_interference.py` — module-level `_gate_findings(spec_path, point)` helper added after `codes()`; `test_out_of_vocabulary_risk_with_no_mitigation_and_blank_residual_still_fires_int_010` added to `TestInterferenceUnaddressed`; `test_out_of_vocabulary_risk_variant_blocks_plan_naming_both_int_010_and_spec_082` added to `TestInterferenceGateLevel`
- `dsx/frame/interference.py` — `_check_interference_unaddressed`'s risk guard now short-circuits only on the literal `none`; docstring firing-condition and disjointness paragraphs, the guard's inline comment, and the `DecisionRecord.rule` field restated to match

## Decisions Made

- The fix is scoped to `_check_interference_unaddressed`'s risk guard alone; `_check_interference_mitigation_admissibility`'s own risk guard (line 296) is deliberately left untouched, because `_RISK_MITIGATION_MAP` has no admissibility cell for an unrecognised risk and judging there would double-report what DSX-INT-010 now reports. Verified via a `git diff HEAD~1` acceptance check showing no hunk inside that function.
- `_check_triggering_dilution` is not touched — its `analysis_population` guard is plan 08-09's scope (gap 2 of 08-VERIFICATION.md), verified via the same `git diff` check.
- The gate-level regression test reads the structured `--json` finding list via the new `_gate_findings` helper rather than `self._run`'s rendered text, matching the shape `08-REVIEW.md`'s WR-01 recommends and mirroring `TestKnownBadCorpus._gate_findings`'s existing idiom rather than inventing a new one.

## Deviations from Plan

### Notes (not auto-fixed — pre-existing plan/reality discrepancy, informational)

**1. Plan acceptance criterion for truth 6 states `python3 -m unittest tests.test_frame_boundary.TestFrameParadigmReadBoundary` runs eight tests; actual observed count is six.**

- **Found during:** Task 2, no-collateral-damage proof of truth 6 (paradigm-read boundary)
- **Issue:** The plan's acceptance criteria (and 08-VERIFICATION.md's own truth 6 evidence line, "Re-ran `tests/test_frame_boundary.py::TestFrameParadigmReadBoundary` (8 tests)") both state eight tests. Reading the class directly (`tests/test_frame_boundary.py:204`) shows six `test_*` methods defined, and running the class confirms `Ran 6 tests in ... OK`. This is a pre-existing count discrepancy in the verifier's own report, not something this plan's diff touched — `git diff` confirms `tests/test_frame_boundary.py` is not among the two files this plan modified.
- **Resolution:** Not fixed — out of this plan's scope (`prohibitions` names no test-count reconciliation as in-scope, and the file itself is untouched by either of this plan's two commits). The substantive claim the criterion protects — the paradigm-read boundary still holds after this plan's edit — is verified: all six tests pass, `OK`, no collateral damage. Documented here per the project's "Verification Before Claiming" working agreement rather than silently reporting "eight tests" as observed when it was not.
- **Verification:** `python3 -m unittest tests.test_frame_boundary.TestFrameParadigmReadBoundary -v` — 6 tests, all `ok`, `OK` overall.
- **Files modified:** none (informational only)
- **Committed in:** n/a — no code change associated with this note

---

**Total deviations:** 0 auto-fixed; 1 documented pre-existing plan/reality discrepancy (informational, out of scope, does not affect the fix's correctness)
**Impact on plan:** None on the CR-01 fix or its disjointness/no-collateral-damage acceptance criteria — every other acceptance criterion for both tasks passed exactly as written, verified with real command output pasted below.

## Real command output (Verification Before Claiming)

Baseline before Task 1 (matches the verifier's own observation):
```
$ python3 -m unittest discover -s tests
Ran 531 tests in 5.111s
OK (skipped=2)
```

Task 1 end state — exactly two failures, both named for the out-of-vocabulary-risk case:
```
$ python3 -m unittest tests.test_frame_interference -k out_of_vocabulary_risk
Ran 2 tests in 0.047s
FAILED (failures=2)

$ python3 -m unittest discover -s tests
Ran 533 tests in 5.020s
FAILED (failures=2, skipped=2)
```
(Both failing test identifiers contained `out_of_vocabulary_risk`: one `AssertionError: 0 != 1` from the empty finding set at unit level, one `AssertionError: 0 != 1` from `code` vs expected `1` at gate level.)

Task 2 end state — full suite green:
```
$ python3 -m unittest tests.test_frame_interference -k out_of_vocabulary_risk
Ran 2 tests in 0.051s
OK

$ python3 -m unittest tests.test_frame_interference -k out_of_vocabulary
Ran 4 tests in 0.096s
OK

$ python3 -m unittest tests.test_frame_interference
Ran 57 tests in 0.991s
OK

$ python3 -m unittest discover -s tests
Ran 533 tests in 5.321s
OK (skipped=2)
```

Guard-count pin:
```
$ python3 -c "src=open('dsx/frame/interference.py',encoding='utf-8').read(); print(src.count('normalized_risk not in INTERFERENCE_RISKS'))"
1
```

Hand reproduction of the gate bypass, mutating the committed shared-budget fixture's `interference.risk` from `shared_budget` to `shared_buget` (mitigation left at `none`, `residual_note` left blank), against a fresh temporary copy with `--phase-dir` pointed at a fresh temp dir:
```
exit: 1
DSX-INT-010 in output: True
DSX-SPEC-082 in output: True
DSX-INT-010 severity: CRITICAL
DSX-SPEC-082 severity/where: HIGH spec.validity_frame.interference.risk
DSX-INT-010 remedy: Declare a mitigation admissible for the declared risk — for 'shared_buget', one of: (none admissible) — or write a residual_note stating plainly what interference remains unaddressed and why it is accepted.
```
Before this task the same mutation produced exit 0 with no `DSX-INT-*` finding at all (per 08-VERIFICATION.md's own reproduction).

Unchanged baseline and clean fixtures:
```
$ python3 -m dsx gate plan --spec examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
exit 1, DSX-INT-010/CRITICAL — unchanged from committed baseline

$ python3 -m dsx gate plan --spec examples/good-ANALYSIS-SPEC.yaml
exit 0

$ python3 -m dsx gate plan --spec templates/ANALYSIS-SPEC.yaml
exit 0
```

No-collateral-damage checks (08-VERIFICATION.md truths 2, 4, 5, 6, 7):
```
$ python3 -m unittest tests.test_frame_interference -k mitigation
Ran 10 tests in 0.111s
OK

Truth 2 (unit-level distinctness, via interference.check() directly):
shared_budget+cluster_randomisation codes: {'DSX-INT-011'}   DSX-INT-011 present: True  DSX-INT-010 present: False
marketplace+cluster_randomisation codes: set()

$ python3 -m unittest tests.test_dsx -k dilut
Ran 5 tests in 0.000s
OK

$ python3 -m unittest tests.test_frame_interference -k ratio_scope
Ran 2 tests in 0.000s
OK

$ python3 -m unittest tests.test_frame_interference -k stability
Ran 11 tests in 0.359s
OK

$ python3 -m unittest tests.test_frame_boundary.TestFrameParadigmReadBoundary -v
Ran 6 tests in 0.019s
OK   (see Deviations note above — plan/verifier stated 8, actual is 6, pre-existing)

$ python3 -m unittest tests.test_frame_interference tests.test_known_bad_corpus
Ran 79 tests in 1.529s
OK

$ sh scripts/check.sh
...
all checks passed

$ python3 scripts/gen-finding-catalogue.py --check
finding catalogue is current
```

Scope and hygiene:
```
$ git diff --stat HEAD~1
 dsx/frame/interference.py | 71 +++++++++++++++++++++++++++++------------------
 1 file changed, 44 insertions(+), 27 deletions(-)

$ git diff HEAD~1 -- dsx/frame/interference.py | grep -c "^@@.*_check_interference_mitigation_admissibility\|^@@.*_check_triggering_dilution"
0

$ git log --oneline -2
cf4da61 fix(08-08): adjudicate an unrecognised interference risk instead of dropping it
eb8ae4c test(08-08): add failing out-of-vocabulary-risk regression tests

$ git status --short
(clean)

$ git diff --stat HEAD~2 -- .planning/phases/08-interference-triggering-stability-dsx-int/
(empty — no .planning/ file touched by this plan's two commits)
```

## Issues Encountered

None.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- 08-VERIFICATION.md's first failed truth is true again, pinned by a test that fails without the fix: a declared interference risk other than none, with no admissible mitigation and no residual note, is blocked at `dsx gate plan` regardless of which `interference` field carries the typo.
- `DSX-SPEC-082` still fires independently beside `DSX-INT-010` on the same input, proven from the structured finding list.
- `DSX-INT-010` and `DSX-INT-011` remain disjoint for the out-of-vocabulary-risk case, with `_check_interference_mitigation_admissibility` provably unedited via `git diff`.
- Gap 1 of 08-VERIFICATION.md is closed. Gap 2 (`triggering.analysis_population` out-of-vocabulary bypass on `_check_triggering_dilution`, CR-02) and WR-01's weak `DSX-SPEC-082` text-substring assertion remain — deliberately deferred to plan 08-09, which touches the same file and must not share a wave with this one.
- Full suite: 533 tests (531 baseline + 2 new), `OK (skipped=2)`. `sh scripts/check.sh`: `all checks passed`. `python3 scripts/gen-finding-catalogue.py --check`: `finding catalogue is current`.

---
*Phase: 08-interference-triggering-stability-dsx-int*
*Completed: 2026-08-13*
