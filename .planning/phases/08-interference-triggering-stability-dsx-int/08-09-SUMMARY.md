---
phase: 08-interference-triggering-stability-dsx-int
plan: 09
subsystem: gate
tags: [python, stdlib, dsx-frame, interference, dilution, gap-closure, tdd]

# Dependency graph
requires:
  - phase: 08-04
    provides: DSX-INT-030 (_check_triggering_dilution, the additive-metric partition)
  - phase: 08-08
    provides: "the module-level _gate_findings(spec_path, point) helper in tests/test_frame_interference.py, reused by every gate-level assertion in this plan"
provides:
  - "DSX-INT-030 fires when triggering.analysis_population is out-of-vocabulary, not just when it is literally 'eligible' — closes 08-VERIFICATION.md gap 2 / 08-REVIEW.md CR-02"
  - "DSX-SPEC-082 confirmed to keep firing independently beside DSX-INT-030 on the same out-of-vocabulary-population input"
  - "Vocabulary contract test pinning dsx.spec.ANALYSIS_POPULATIONS to exactly its two members, so a future third member turns a test red instead of silently widening what DSX-INT-030 adjudicates"
  - "08-REVIEW.md WR-01 closed: the gate-level DSX-SPEC-082 assertion (mitigation-field variant) now reads the structured finding list and is demonstrated, by mutation proof, to go red on a control input where DSX-SPEC-082 does not fire"
affects: [10, 11, 12]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Vocabulary-membership-as-declaration, applied to the triggering.analysis_population field to match the mitigation-field precedent from 08-07 and the risk-field precedent from 08-08: an unrecognised enum-like string is adjudicated, not treated as equivalent to a recognised member"
    - "Structured-findings gate-level test assertion (parsed --json finding list, keyed by code) rather than a rendered-text substring assertion, applied to both the population guard's new test and the mitigation guard's existing test, closing the WR-01 vacuous-assertion failure mode"

key-files:
  created: []
  modified:
    - dsx/frame/interference.py
    - tests/test_frame_interference.py

key-decisions:
  - "Guard fix mirrors 08-REVIEW.md CR-02's proposed shape exactly: the early return names the two not-adjudicated cases (population == 'triggered', or empty/absent/blank) and everything else — 'eligible' or an unrecognised string — falls through to the judgment point. No membership test against ANALYSIS_POPULATIONS is added inside the guard itself; the vocabulary is instead pinned by a separate contract test named in the guard's comment"
  - "test_good_and_monitoring_fixtures_and_template_still_clear_plan's exit-code assertion is pinned per-fixture (0 for good/template, 1 for the two monitoring fixtures) rather than uniformly 0 as the plan's <behavior> block stated — real reproduction showed the two monitoring fixtures are legitimately blocked by DSX-PAR-010/DSX-PAR-011 (Phase 9, CRITICAL), unrelated to DSX-INT-030. Documented as a deviation, not silently weakened to force a pass — see Deviations section"
  - "_check_interference_unaddressed and _check_interference_mitigation_admissibility are untouched — verified by git diff hunk inspection on every commit in this plan"

patterns-established:
  - "RED-then-GREEN-then-tighten across three commits for a critical bypass fix plus a companion weak-assertion fix (Task 1 test-only commit, Task 2 fix-only commit, Task 3 test-only commit), extending the two-commit shape 08-07/08-08 established"

requirements-completed: [REQ-P8-03]

coverage:
  - id: D1
    description: "An out-of-vocabulary triggering.analysis_population value (e.g. eligable) with an otherwise-firing additive metric and dilution_adjusted: false fires DSX-INT-030 (CRITICAL) instead of silently bypassing it"
    requirement: "REQ-P8-03"
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py#TestTriggeringDilution.test_out_of_vocabulary_analysis_population_still_fires_int_030"
        status: pass
      - kind: integration
        ref: "tests/test_frame_interference.py#TestTriggeringDilution.test_out_of_vocabulary_analysis_population_variant_blocks_plan_naming_int_030"
        status: pass
      - kind: manual_procedural
        ref: "python3 -m dsx gate plan --spec <mutated triggering-dilution fixture, analysis_population: eligable> --json — exit 1, DSX-INT-030/CRITICAL + DSX-SPEC-082/HIGH (where: spec.validity_frame.triggering.analysis_population)"
        status: pass
    human_judgment: false
  - id: D2
    description: "An honestly-declared triggered population, and a genuinely absent/blank/whitespace-only population, are all still skipped by DSX-INT-030 — no over-widening of the corrected guard"
    requirement: "REQ-P8-03"
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py#TestTriggeringDilution.test_triggered_population_produces_no_finding_whatever_dilution_adjusted_says"
        status: pass
      - kind: manual_procedural
        ref: "interference.check() by hand on absent, empty-string, and whitespace-only analysis_population — all three produce codes() == set()"
        status: pass
    human_judgment: false
  - id: D3
    description: "The docstring's firing condition and the DecisionRecord.rule text both describe the corrected condition, so the dsx explain decision trail matches the code"
    verification:
      - kind: other
        ref: "dsx/frame/interference.py:378-388 (docstring) and :548-552 (DecisionRecord.rule), both read and pasted verbatim into this summary's Real command output section"
        status: pass
    human_judgment: false
  - id: D4
    description: "The vocabulary the corrected guard is keyed to is held by a contract test, so a future third ANALYSIS_POPULATIONS member turns a test red instead of silently widening what DSX-INT-030 adjudicates"
    requirement: "REQ-P8-03"
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py#TestTriggeringDilution.test_analysis_populations_vocabulary_is_exactly_eligible_and_triggered"
        status: pass
    human_judgment: false
  - id: D5
    description: "08-REVIEW.md WR-01 closed: the mitigation-field DSX-SPEC-082 gate assertion reads structured findings and is proven, by mutation, to fail on a control input where DSX-SPEC-082 genuinely does not fire"
    verification:
      - kind: integration
        ref: "tests/test_frame_interference.py#TestInterferenceGateLevel.test_out_of_vocabulary_mitigation_variant_blocks_plan_naming_both_int_010_and_spec_082"
        status: pass
      - kind: manual_procedural
        ref: "mutation proof: temporarily changing the mutation to mitigation: none makes the test fail on assertIn('DSX-SPEC-082', by_code); reverting to buget_isolation restores green — both outputs pasted below"
        status: pass
    human_judgment: false
  - id: D6
    description: "No collateral damage to 08-VERIFICATION.md truths 2, 4, 5, 6, 7 (risk/mitigation distinctness, ratio-metric scope boundary, novelty/primacy severity split, paradigm-read boundary, known-bad corpus guards)"
    verification:
      - kind: unit
        ref: "python3 -m unittest discover -s tests — 536 tests, OK (skipped=2); sh scripts/check.sh — all checks passed; python3 scripts/gen-finding-catalogue.py --check — finding catalogue is current"
        status: pass
    human_judgment: false

duration: ~35min
completed: 2026-08-13
status: complete
---

# Phase 08 Plan 09: Triggering-population out-of-vocabulary gate-bypass closure and WR-01 test tightening Summary

**Closed 08-VERIFICATION.md's second failed truth — an out-of-vocabulary `triggering.analysis_population` string (e.g. `eligable`) no longer bypasses `DSX-INT-030` — with a RED-then-GREEN commit pair mirroring plans 08-07/08-08's fix shape, then tightened the one remaining weak-assertion warning (08-REVIEW.md WR-01) with a mutation-proven structured-findings rewrite.**

## Performance

- **Duration:** ~35 min
- **Completed:** 2026-08-13
- **Tasks:** 3
- **Files modified:** 2 (`tests/test_frame_interference.py`, `dsx/frame/interference.py`)

## Accomplishments

- Reproduced 08-VERIFICATION.md's second failed truth with two failing regression tests (unit-level and gate-level) before touching production code, plus a passing vocabulary contract test — both regression tests confirmed to fail for the documented reason (0 findings at unit level, exit code 0 at gate level), and no other test in the 533-test baseline suite broke.
- Fixed `_check_triggering_dilution`'s population guard in `dsx/frame/interference.py`: the early return now names only the two cases with nothing to adjudicate — the population being the member `triggered`, or being empty (absent, explicit null, blank, or whitespace-only) — so `eligible` and any out-of-vocabulary string both fall through to the judgment point.
- Confirmed by `git diff` on every commit in this plan that `_check_interference_unaddressed` and `_check_interference_mitigation_admissibility` are byte-for-byte unedited, and that the `dilution_adjusted is not True` identity comparison and its comment are untouched.
- Corrected the docstring's firing-condition sentence and the `DecisionRecord.rule` text so the `dsx explain` decision trail describes the corrected condition rather than the one the code no longer implements.
- Closed 08-REVIEW.md WR-01: rewrote `test_out_of_vocabulary_mitigation_variant_blocks_plan_naming_both_int_010_and_spec_082` (and its negative counterpart `test_good_and_monitoring_fixtures_and_template_still_clear_plan`) to assert against the parsed `--json` structured finding list instead of rendered report text, and ran the mutation proof the task requires: with the mutation temporarily set to the fixture's honest committed mitigation value, the DSX-SPEC-082 assertion genuinely fails; reverted to the misspelled value, it passes again.
- Re-confirmed all five must-not-regress truths from 08-VERIFICATION.md (risk/mitigation distinctness, ratio-metric scope boundary, novelty/primacy severity split, paradigm-read boundary, known-bad corpus guards) with real command output, plus `sh scripts/check.sh` and `python3 scripts/gen-finding-catalogue.py --check`.

## Task Commits

Each task was committed atomically, RED before GREEN before the WR-01 tightening:

1. **Task 1: Write the two failing out-of-vocabulary-population tests and the vocabulary contract test** — `a864d6f` (test)
2. **Task 2: Adjudicate an unrecognised analysis population instead of reading it as triggered** — `ef9fc65` (fix)
3. **Task 3: Make the DSX-SPEC-082 gate assertions able to fail, and prove the whole tree is green** — `12d5c56` (test)

**Plan metadata:** commit created after this summary via the SDK's `commit` verb — see final commit in git log.

## Files Created/Modified

- `tests/test_frame_interference.py` — `ANALYSIS_POPULATIONS` added to the existing `from dsx.spec import ...` line; module-level `_mutated_triggering_fixture(tmp, **overrides)` helper added after `_triggering_causal_spec`; `test_out_of_vocabulary_analysis_population_still_fires_int_030` and `test_analysis_populations_vocabulary_is_exactly_eligible_and_triggered` added to `TestTriggeringDilution`; `test_out_of_vocabulary_analysis_population_variant_blocks_plan_naming_int_030` added to `TestTriggeringDilution`; `test_out_of_vocabulary_mitigation_variant_blocks_plan_naming_both_int_010_and_spec_082` and `test_good_and_monitoring_fixtures_and_template_still_clear_plan` rewritten to assert on structured findings (both keep their names)
- `dsx/frame/interference.py` — `_check_triggering_dilution`'s population guard inverted so the early return names only `triggered`/empty; docstring firing-condition paragraph and `DecisionRecord.rule` field restated to match

## Decisions Made

- The guard fix applies 08-REVIEW.md CR-02's proposed shape exactly, without adding a membership test against `ANALYSIS_POPULATIONS` inside the guard itself — the vocabulary is instead pinned by a separate contract test (`test_analysis_populations_vocabulary_is_exactly_eligible_and_triggered`) named in the guard's inline comment, per the plan's explicit instruction not to make the guard enumerate the vocabulary it does not need to consult.
- `test_good_and_monitoring_fixtures_and_template_still_clear_plan`'s exit-code assertion is pinned per-fixture rather than uniformly `0`. Real reproduction showed the two monitoring fixtures (`bayesian-continuous-monitoring`, `frequentist-uncontrolled-continuous`) do not clear `plan` — each is legitimately blocked by its own unrelated CRITICAL finding (`DSX-PAR-011` / `DSX-PAR-010`, shipped in Phase 9, after this test was written in `feat(08-04)`, commit `36ff448`). The original assertion never checked exit codes, so this drift went unnoticed until this task added the check the plan requires. See Deviations below — not auto-fixed to match the plan's literal claim, since that claim does not match the committed tree.
- The gate-level population regression test reads the structured `--json` finding list via `_gate_findings` (plan 08-08's helper) rather than rendered text, matching the shape 08-REVIEW.md CR-02/WR-01 both recommend.

## Deviations from Plan

### Notes (not auto-fixed — pre-existing plan/reality discrepancy, informational)

**1. `test_good_and_monitoring_fixtures_and_template_still_clear_plan`'s two monitoring fixtures do not clear `plan`; the plan's `<behavior>` block states they do.**

- **Found during:** Task 3, rewriting the negative WR-01 counterpart to assert an exit code it never checked before.
- **Issue:** The plan's Task 3 `<behavior>` block states: "for each of the four fixtures, the exit code is 0 and DSX-INT-030 is not among the finding codes. It still passes for all four." Running `_gate_findings` against `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` and `examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml` at `plan` shows both exit `1`: the bayesian fixture is blocked by `DSX-PAR-011` (CRITICAL), the frequentist fixture by `DSX-PAR-010` (CRITICAL) — both unrelated to `DSX-INT-030`, which is genuinely absent from both finding lists. `git log -S` on the test name confirms it was written in `feat(08-04)` (commit `36ff448`), before Phase 9 shipped `DSX-PAR-010`/`DSX-PAR-011`. The original assertion (`assertNotIn("DSX-INT-030", out+err)`, no exit-code check) tolerated this silently the entire time.
- **Resolution:** Not fixed — `DSX-PAR-010`/`DSX-PAR-011` and the two monitoring fixtures belong to Phase 9, entirely out of this plan's `files_modified` and `prohibitions`. The rewritten test pins the real, observed per-fixture exit code (`0` for good/template, `1` for the two monitoring fixtures, each annotated with the CRITICAL code responsible) rather than asserting a uniform `0` that does not hold — strictly stronger than the original assertion on the dimension this test actually protects (DSX-INT-030 absence for all four), and honest about the rest. Per the project's "Verification Before Claiming" working agreement and the plan's own instruction ("If either rewrite turns red, that is a real finding about the codebase... Do not weaken the assertion to make it pass"), this is documented here rather than silently asserting something false.
- **Verification:** `python3 -m unittest tests.test_frame_interference -k still_clear_plan -v` — 1 test, `ok`. Per-fixture exit codes confirmed by direct `_gate_findings` reproduction, pasted below.
- **Files modified:** `tests/test_frame_interference.py` (part of Task 3's commit)
- **Committed in:** `12d5c56` (Task 3 commit)

---

**Total deviations:** 0 auto-fixed; 1 documented pre-existing plan/reality discrepancy (informational, out of scope, does not affect the population-guard fix or WR-01's correctness)
**Impact on plan:** None on the CR-02 fix or the WR-01 mutation-proof acceptance criteria — every other acceptance criterion for all three tasks passed exactly as written, verified with real command output pasted below.

## Real command output (Verification Before Claiming)

Baseline before Task 1 (matches this plan's Task 1 requirement to confirm rather than assume):
```
$ python3 -m unittest discover -s tests
Ran 533 tests in 5.063s
OK (skipped=2)
```

Task 1 end state — exactly two failures, both named for the out-of-vocabulary-population case:
```
$ python3 -m unittest tests.test_frame_interference -k out_of_vocabulary_analysis_population
FF
FAIL: test_out_of_vocabulary_analysis_population_still_fires_int_030
    AssertionError: 0 != 1
FAIL: test_out_of_vocabulary_analysis_population_variant_blocks_plan_naming_int_030
    AssertionError: 0 != 1
Ran 2 tests in 0.050s
FAILED (failures=2)

$ python3 -m unittest tests.test_frame_interference -k test_analysis_populations_vocabulary_is_exactly_eligible_and_triggered
Ran 1 test in 0.000s
OK

$ python3 -m unittest discover -s tests
Ran 536 tests in 5.112s
FAILED (failures=2, skipped=2)

$ python3 -m unittest tests.test_known_bad_corpus
Ran 22 tests in 0.562s
OK

$ git status --short
 M tests/test_frame_interference.py   (examples/known-bad/... unmodified)
```

Task 2 end state — full suite green:
```
$ python3 -m unittest tests.test_frame_interference -k out_of_vocabulary_analysis_population
Ran 2 tests in 0.053s
OK

$ python3 -m unittest tests.test_frame_interference -k triggering
Ran 3 tests in 0.055s
OK

$ python3 -m unittest tests.test_frame_interference
Ran 60 tests in 1.012s
OK

$ python3 -m unittest discover -s tests
Ran 536 tests in 5.085s
OK (skipped=2)

$ python3 -m unittest tests.test_known_bad_corpus
Ran 22 tests in 0.568s
OK
```

Absent/blank/whitespace-only population, by hand (interference.check() directly, three shapes):
```
absent:     set()
empty:      set()
whitespace: set()
```

Corrected docstring firing-condition paragraph, read and pasted verbatim:
```
Fires unless the declared ``validity_frame.triggering.analysis_population``
is the member ``triggered`` or is not declared at all — so ``eligible``
and any unrecognised string both reach the judgment — provided
``validity_frame.triggering.dilution_adjusted`` is not the literal
boolean ``True`` and at least one declared top-level ``metrics`` entry
has a normalized ``type`` that is a member of ``_ADDITIVE_METRIC_TYPES``.
A population string the closed two-member vocabulary does not contain is
a misspelling, not a declaration of ``triggered``, and reading it as
``triggered`` would make a typo the cheapest way past a
CRITICAL-threshold gate.
```

Corrected `DecisionRecord.rule` text, read and pasted verbatim:
```
DSX-INT-030 fires unless triggering.analysis_population is
the member 'triggered' or is not declared at all, provided
triggering.dilution_adjusted is not the literal boolean
True and at least one declared metric's normalized type is
a member of _ADDITIVE_METRIC_TYPES.
```

Hand reproduction of the gate bypass, mutating a temporary copy of the committed triggering-dilution fixture's `triggering.analysis_population` from `eligible` to `eligable`:
```
MUTATED (eligable) exit: 1
DSX-INT-030 present: True CRITICAL
DSX-SPEC-082 present: True HIGH spec.validity_frame.triggering.analysis_population
```
Before this task the same mutation produced exit 0 with no `DSX-INT-030` finding at all (08-VERIFICATION.md's own reproduction).

Unchanged baseline and clean fixtures:
```
$ python3 -m dsx gate plan --spec examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml
exit 1, DSX-INT-030 present — unchanged from committed baseline

$ python3 -m dsx gate execute --spec examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml
exit 0

$ python3 -m dsx gate plan --spec examples/good-ANALYSIS-SPEC.yaml
exit 0

$ python3 -m dsx gate plan --spec templates/ANALYSIS-SPEC.yaml
exit 0

$ python3 -m dsx gate plan --spec examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
exit 1, DSX-INT-010 present, DSX-INT-030 absent — declares analysis_population: triggered, still correctly skipped
```

Scope and hygiene (Task 2):
```
$ git diff HEAD~0 -- dsx/frame/interference.py | grep -c "^@@"
3   (all three hunks inside _check_triggering_dilution; none in
     _check_interference_unaddressed or _check_interference_mitigation_admissibility)

$ git diff -- dsx/frame/interference.py | grep -A2 -B2 "dilution_adjusted is not True"
(no output — line and its comment unchanged)
```

Task 3 mutation proof — the point of the task:
```
# Mutation temporarily changed from mitigation="buget_isolation" to mitigation="none"
$ python3 -m unittest tests.test_frame_interference.TestInterferenceGateLevel.test_out_of_vocabulary_mitigation_variant_blocks_plan_naming_both_int_010_and_spec_082 -v
FAIL: test_out_of_vocabulary_mitigation_variant_blocks_plan_naming_both_int_010_and_spec_082
    AssertionError: 'DSX-SPEC-082' not found in {'DSX-EXP-040': ..., 'DSX-MET-040': ...,
    'DSX-PAR-001': ..., 'DSX-INT-010': {...'severity': 'CRITICAL'...}}
Ran 1 test in 0.053s
FAILED (failures=1)

# Mutation reverted to mitigation="buget_isolation"
$ python3 -m unittest tests.test_frame_interference.TestInterferenceGateLevel.test_out_of_vocabulary_mitigation_variant_blocks_plan_naming_both_int_010_and_spec_082 -v
ok
Ran 1 test in 0.052s
OK
```
The unmutated (honest `mitigation: none`) input genuinely produces zero `DSX-SPEC-082` findings — confirming the assertion can now go red on exactly the input WR-01 identified as making the old substring assertion vacuous.

Task 3 negative-counterpart exit codes, by hand:
```
good-ANALYSIS-SPEC.yaml:                                exit 0, DSX-INT-030 absent
templates/ANALYSIS-SPEC.yaml:                           exit 0, DSX-INT-030 absent
bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml:       exit 1 (DSX-PAR-011 CRITICAL), DSX-INT-030 absent
frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml:  exit 1 (DSX-PAR-010 CRITICAL), DSX-INT-030 absent
```

No-collateral-damage checks (08-VERIFICATION.md truths 2, 4, 5, 6, 7), run once across both gap fixes:
```
$ python3 -m unittest tests.test_frame_interference -k mitigation
Ran 10 tests in 0.114s
OK

Truth 2 (unit-level distinctness, via interference.check() directly):
shared_budget+cluster_randomisation codes: {'DSX-INT-011'}
marketplace+cluster_randomisation codes: set()

$ python3 -m unittest tests.test_dsx -k dilut
Ran 5 tests in 0.000s
OK

$ python3 -m unittest tests.test_frame_interference -k ratio_scope
Ran 2 tests in 0.000s
OK

Truth 5 (novelty/primacy severity split, hand reproduction on a copy of good-ANALYSIS-SPEC.yaml
with novelty_primacy_assessed: false):
plan exit: 0   DSX-INT-040 in output: True
verify exit: 1   DSX-INT-040 in output: True

$ python3 -m unittest tests.test_frame_boundary.TestFrameParadigmReadBoundary -v
Ran 6 tests in 0.018s
OK   (pre-existing plan/verifier count discrepancy already documented in
      08-08-SUMMARY.md — stated 8, actual 6, unrelated to this plan's diff)

$ python3 -m unittest tests.test_frame_interference tests.test_known_bad_corpus
Ran 82 tests in 1.597s
OK

$ sh scripts/check.sh
...
all checks passed

$ python3 scripts/gen-finding-catalogue.py --check
finding catalogue is current
```

Scope and hygiene, whole plan:
```
$ python3 -c "print(open('tests/test_frame_interference.py',encoding='utf-8').read().count('_gate_findings'))"
6

$ python3 -c "print('spec.validity_frame.interference.mitigation' in open('tests/test_frame_interference.py',encoding='utf-8').read())"
True

$ git diff --stat HEAD~1   (Task 3 commit)
 tests/test_frame_interference.py | 86 ++++++++++++++++++++++++++++++----------
 1 file changed, 64 insertions(+), 22 deletions(-)

$ git status --short
(clean)

$ git status --short examples/ templates/
(clean — no fixture touched)

$ git status --short tests/test_known_bad_corpus.py
(clean — byte-identical to committed state)

$ git diff --stat -- .planning/phases/08-interference-triggering-stability-dsx-int/08-01-PLAN.md \
    .../08-02-PLAN.md .../08-03-PLAN.md .../08-04-PLAN.md .../08-05-PLAN.md \
    .../08-06-PLAN.md .../08-07-PLAN.md .../08-08-PLAN.md
(empty — all eight prior plan files byte-identical to committed state)

$ git log --oneline -3
12d5c56 test(08-09): assert DSX-SPEC-082/DSX-INT-030 gate tests against structured findings
ef9fc65 fix(08-09): adjudicate an unrecognised analysis population instead of reading it as triggered
a864d6f test(08-09): add failing out-of-vocabulary-population regression tests
```

## Issues Encountered

None.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- 08-VERIFICATION.md's second failed truth is true again, pinned by a test that fails without the fix: `DSX-INT-030` blocks eligible-population analysis of an additive metric with no dilution adjustment declared, no matter how `triggering.analysis_population` is spelled.
- An honestly declared `triggered` population, and a genuinely absent, empty, or whitespace-only one, are all still skipped — proven by hand for all three shapes.
- `DSX-SPEC-082` still fires independently beside `DSX-INT-030` on the same out-of-vocabulary-population input, proven from the structured finding list, with `where` pinned to `spec.validity_frame.triggering.analysis_population`.
- The docstring and the `DecisionRecord.rule` text both describe the corrected condition, so `dsx explain` gives an operator a true account of why a spec blocked.
- 08-REVIEW.md WR-01 is closed: the `DSX-SPEC-082` gate assertion for the mitigation-field case reads structured findings and is demonstrated, by mutation, to go red on a control input where that finding genuinely does not fire.
- Both gaps 08-VERIFICATION.md scored (risk-field bypass in plan 08-08, population-field bypass here) are closed. Phase 8 is ready for re-verification — this plan's own `<verification>` block reproduces every check the next verification pass would run, with real output recorded above.
- Full suite: 536 tests (533 baseline + 3 new), `OK (skipped=2)`. `sh scripts/check.sh`: `all checks passed`. `python3 scripts/gen-finding-catalogue.py --check`: `finding catalogue is current`.
- `.planning/REQUIREMENTS.md`, `.planning/STATE.md` and `.planning/ROADMAP.md` are untouched by this plan (single-writer files per project convention; the orchestrator updates them after this wave merges).

---
*Phase: 08-interference-triggering-stability-dsx-int*
*Completed: 2026-08-13*

## Self-Check: PASSED

- FOUND: `tests/test_frame_interference.py`
- FOUND: `dsx/frame/interference.py`
- FOUND: `.planning/phases/08-interference-triggering-stability-dsx-int/08-09-SUMMARY.md`
- FOUND commit `a864d6f` (test(08-09): add failing out-of-vocabulary-population regression tests)
- FOUND commit `ef9fc65` (fix(08-09): adjudicate an unrecognised analysis population instead of reading it as triggered)
- FOUND commit `12d5c56` (test(08-09): assert DSX-SPEC-082/DSX-INT-030 gate tests against structured findings)
