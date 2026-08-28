---
phase: 06-contract-extension-decision-record-paradigm-manifest
plan: 05
subsystem: contract
tags: [yaml-fixtures, closed-vocabulary, dsx-spec, tdd, validity-frame, inference]

# Dependency graph
requires:
  - phase: 06-01
    provides: "dsx/loader.py _NULL fix (literal `none` parses as a string) and the ten new closed vocabularies + _VOCABULARIES registry in dsx/spec.py"
provides:
  - "examples/good-ANALYSIS-SPEC.yaml carries all ten validity_frame sub-blocks and the six inference fields, still exits 0 at all four gate points"
  - "examples/bad-ANALYSIS-SPEC.yaml carries a partial validity_frame (4 of 10 sub-blocks) and an out-of-vocabulary membership defect on each new axis, still exits 1 at plan and ship"
  - "templates/ANALYSIS-SPEC.yaml scaffolds both blocks in full with honest placeholders, still passes dsx validate and dsx gate plan"
  - "Six new tests pinning the round-trip contract (TestSpecStructure x4, TestCLI x2)"
affects: [06-06, 06-07, 06-08, 06-09, 06-10]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "New contract surface lands as inert fixture/template data before any validator reads it — suite stays green at every task boundary because validate_structure() does not reject unknown top-level keys"
    - "TDD RED/GREEN for the template task (data-adjacent behavior, not pure fixture edit): failing round-trip test commit, then minimal template-scaffolding commit"

key-files:
  created: []
  modified:
    - examples/good-ANALYSIS-SPEC.yaml
    - examples/bad-ANALYSIS-SPEC.yaml
    - templates/ANALYSIS-SPEC.yaml
    - tests/test_dsx.py

key-decisions:
  - "Good fixture uses cluster_robust (not brief §5.1's cluster_robust_or_mixed) for dependence.method_family_required, and none (not informative_priors_from_lift_tests) for identification.constraint_source — both brief values are illegal under M-09's VARIANCE_ADJUSTMENTS reuse and CONSTRAINT_SOURCES respectively; copying them verbatim would have tripped DSX-SPEC-082 once 06-06 lands"
  - "Bad fixture's validity_frame declares estimand, units, identification, interference (omitting dependence, sampling_frame, missingness, measurement from the always-required six, and triggering, stability from the causal-only four) — satisfies D-11's per-sub-block finding branch with margin"
  - "Template's claims[0].type placeholder was retyped from association to descriptive (Rule 1 auto-fix): it exceeded the template's default question_type: descriptive under DSX-COH-001's claim-ceiling check, blocking dsx gate plan on the unedited template independent of validity_frame/inference"
  - "Template's vocabulary-typed placeholders use the honest descriptive/observational defaults given in the plan (strength: weak, constraint_source: none, structure: none, risk: none, mitigation: none, missingness.mechanism: not_assessed, analysis_population: eligible, paradigm: frequentist, declared_at: pre_data)"

patterns-established:
  - "Validity-frame / inference blocks append at the end of ANALYSIS-SPEC.yaml files rather than interleaving with existing sections — extends without reordering, keeping D-08's 'extend, not replace' contract mechanically obvious in the diff"

requirements-completed: [REQ-P6-02, REQ-P6-04, REQ-P6-12]

coverage:
  - id: D1
    description: "Good fixture round-trips all ten validity_frame sub-blocks and the six inference fields; every vocabulary-typed value is a legal member; none-valued fields stay strings; the fixture exits 0 at plan/execute/verify/ship"
    requirement: "REQ-P6-02"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure::test_good_fixture_none_frame_fields_round_trip_as_strings"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestCLI::test_good_fixture_passes_every_gate"
        status: pass
    human_judgment: false
  - id: D2
    description: "Bad fixture carries a partial validity_frame plus out-of-vocabulary defects on the validity_frame and inference axes, gains no peeking-axis defect, and still blocks at plan and ship"
    requirement: "REQ-P6-12"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestCLI::test_bad_fixture_blocks_at_plan"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestCLI::test_bad_fixture_blocks_at_ship"
        status: pass
    human_judgment: false
  - id: D3
    description: "templates/ANALYSIS-SPEC.yaml scaffolds both new blocks in full with honest placeholders, round-trips through the loader, and still passes dsx validate and dsx gate plan (dsx gate ship still blocks on its remaining placeholders, unchanged)"
    requirement: "REQ-P6-04"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure::test_template_validity_frame_and_inference_round_trip"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure::test_template_vocabulary_placeholders_are_legal_members"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestCLI::test_template_validity_frame_and_inference_pass_dsx_validate"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestCLI::test_template_validity_frame_and_inference_pass_gate_plan"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestCLI::test_template_validates_structurally_as_a_scaffold"
        status: pass
    human_judgment: false
  - id: D4
    description: "No spec under examples/ or templates/ declares inference.stopping_rule, the field M-02 removed"
    requirement: "REQ-P6-12"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure::test_no_shipped_spec_declares_removed_stopping_rule_field"
        status: pass
    human_judgment: false

duration: 20min
completed: 2026-08-08
status: complete
---

# Phase 6 Plan 05: Fixture and template extension for validity_frame / inference Summary

**`examples/good-ANALYSIS-SPEC.yaml` and `examples/bad-ANALYSIS-SPEC.yaml` gain the full `validity_frame:`/`inference:` contract surface (extended, not replaced) and `templates/ANALYSIS-SPEC.yaml` scaffolds both blocks in full — all three still pass their pre-existing gate contracts, and nothing reads the new fields yet**

## Performance

- **Duration:** ~20 min
- **Completed:** 2026-08-08T00:35Z
- **Tasks:** 3 (Task 3 was TDD: RED then GREEN)
- **Files modified:** 4 (`examples/good-ANALYSIS-SPEC.yaml`, `examples/bad-ANALYSIS-SPEC.yaml`, `templates/ANALYSIS-SPEC.yaml`, `tests/test_dsx.py`)

## Accomplishments

- `examples/good-ANALYSIS-SPEC.yaml` now declares all ten `validity_frame` sub-blocks (`estimand`, `units`, `identification`, `dependence`, `interference`, `triggering`, `stability`, `sampling_frame`, `missingness`, `measurement`) because it declares `question_type: causal` and `design.kind: experiment`. It also declares the six `inference` fields (`paradigm`, `paradigm_justification`, `declared_at`, `primary_procedure`, `alpha_spending`, `fallback_rule`) with no `stopping_rule` field. Every vocabulary-typed value is a legal member of its `dsx/spec.py` constant; `interference.risk`, `interference.mitigation` and `identification.constraint_source` all round-trip as the string `"none"` — the direct proof that 06-01's loader fix works end to end. The fixture still exits 0 at `plan`, `execute`, `verify` and `ship`.
- `examples/bad-ANALYSIS-SPEC.yaml` now declares a deliberately incomplete `validity_frame` (`estimand`, `units`, `identification`, `interference` present; `dependence`, `sampling_frame`, `missingness`, `measurement`, `triggering`, `stability` omitted) and an `inference` block whose `paradigm` is legal but `paradigm_justification` is not — targets for 06-06's per-sub-block `DSX-SPEC-081` findings and its `DSX-SPEC-082`/`DSX-SPEC-085` membership findings. `identification.strength: extremely_strong` is a second membership-check target. `design.peeking_policy` stays `fixed_horizon` (D-07: no peeking-axis defect added here) and no `stopping_rule` field was declared. The fixture still exits 1 at `plan` and at `ship`, and every pre-existing defect in the file is untouched.
- `templates/ANALYSIS-SPEC.yaml` scaffolds both blocks in full (D-12): every sub-block present, closed vocabularies commented inline in the template's existing style, honest angle-bracket prompts for free-text fields (so `dsx init` output still fails Phase 7/8 content checks on purpose). Vocabulary-typed fields default to the honest descriptive/observational choice named in the plan (`strength: weak`, `constraint_source: none`, `structure: none`, `risk: none`, `mitigation: none`, `missingness.mechanism: not_assessed`, `analysis_population: eligible`, `paradigm: frequentist`, `declared_at: pre_data`). `design.peeking_policy`'s comment now lists `uncontrolled_continuous` alongside the existing four members.
- Six new tests pin the round-trip contract: four in `TestSpecStructure` (template round-trip shape, vocabulary-placeholder legality, good-fixture none-string round-trip, no-`stopping_rule` structural guard scanning every `examples/`/`templates/` spec) and two in `TestCLI` (`dsx validate` and `dsx gate plan` both exit 0 on the scaffolded template), the latter reusing `self._run` per the existing convention.

## Task Commits

1. **Task 1: Extend the good fixture with a clean validity_frame and inference block (REQ-P6-02, REQ-P6-04, REQ-P6-12)**
   - `cd052cf` (feat) — all ten `validity_frame` sub-blocks + six `inference` fields, all legal vocabulary members
2. **Task 2: Extend the bad fixture with structural defects on the new axes only (REQ-P6-12, D-07)**
   - `e170d13` (feat) — partial `validity_frame`, out-of-vocabulary defects on both new axes, no peeking-axis change
3. **Task 3: Scaffold both blocks in the spec template and pin the round-trip (REQ-P6-02, REQ-P6-04, D-12)** — TDD RED then GREEN:
   - `bc2f28e` (test) — six failing round-trip tests (RED: `KeyError: 'validity_frame'` against the unscaffolded template)
   - `737cbf4` (feat) — template scaffolding + Rule 1 fix to `claims[0].type` (GREEN: all six tests pass, full suite 212/212)

**Plan metadata:** committed separately by the final-commit step below.

## Files Created/Modified

- `examples/good-ANALYSIS-SPEC.yaml` — appended `validity_frame:` and `inference:` blocks after `limitations:`; no existing key reordered, renamed or deleted
- `examples/bad-ANALYSIS-SPEC.yaml` — appended `validity_frame:` and `inference:` blocks after `assumptions:`; every pre-existing defect and inline comment untouched
- `templates/ANALYSIS-SPEC.yaml` — appended `validity_frame:` and `inference:` blocks before the Suppressions section; updated `peeking_policy`'s inline comment to include `uncontrolled_continuous`; retyped the default `claims[0].type` placeholder from `association` to `descriptive` (Rule 1)
- `tests/test_dsx.py` — six new test methods (four in `TestSpecStructure`, two in `TestCLI`), all additive; `git diff -U0` shows two pure-insertion hunks (`+312,0 → +313,74` and `+1091,0 → +1166,12`), confirming the pre-existing `_run` helper and the three D-08 fixture tests (`test_good_fixture_passes_every_gate`, `test_bad_fixture_blocks_at_plan`, `test_bad_fixture_blocks_at_ship`) were not modified

## Decisions Made

- Used `cluster_robust` (not brief §5.1's `cluster_robust_or_mixed`) for the good fixture's `dependence.method_family_required`, and `none` (not `informative_priors_from_lift_tests`) for `identification.constraint_source` — both brief values are illegal under M-09's reuse of `VARIANCE_ADJUSTMENTS` and under `CONSTRAINT_SOURCES` respectively. This was flagged in the plan itself as a deliberate deviation from brief wording, not something this plan re-litigated.
- Bad fixture's `validity_frame` keeps four sub-blocks present (`estimand`, `units`, `identification`, `interference`) and omits six, giving 06-06's per-sub-block finding logic six distinct `DSX-SPEC-081` targets across both the always-required and causal-only tiers, with margin beyond the plan's "at least two" / "at least one" minimums.
- Rule 1 auto-fix: the template's placeholder `claims[0].type: association` exceeded the template's own default `question_type: descriptive` under `dsx/checks/coherence.py`'s `DSX-COH-001` claim-ceiling check (`CLAIM_STRENGTH["association"]=1 > QUESTION_STRENGTH["descriptive"]=0`). This blocked `dsx gate plan` on the unedited template regardless of the validity_frame/inference work and was required for Task 3's acceptance criteria. Retyped to `descriptive`, which matches the template's own default question_type. `dsx gate ship` still blocks on the template's many remaining placeholders — unchanged behavior (verified by the pre-existing `test_template_validates_structurally_as_a_scaffold`, still passing).
- Template's vocabulary-typed placeholders use exactly the nine honest defaults specified in the plan text, rather than inventing new ones — keeps the scaffold decision auditable against the plan.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Template's default claim type exceeded its default question_type**
- **Found during:** Task 3 (GREEN phase — `dsx gate plan --spec templates/ANALYSIS-SPEC.yaml` returned exit 1 with `DSX-COH-001` even before any validity_frame/inference content was added)
- **Issue:** `templates/ANALYSIS-SPEC.yaml`'s placeholder claim declared `type: association` while the template's default `question_type: descriptive` only licenses claim strength 0; `association` is strength 1, tripping a CRITICAL `DSX-COH-001` finding at every `plan`-gate invocation of the unedited template. This predates Phase 6 and is unrelated to `validity_frame`/`inference`, but it blocked Task 3's acceptance criterion that `dsx gate plan` exit 0 on the scaffolded template.
- **Fix:** Retyped the placeholder to `type: descriptive`, matching the template's own default `question_type`.
- **Files modified:** `templates/ANALYSIS-SPEC.yaml`
- **Verification:** `dsx gate plan --spec templates/ANALYSIS-SPEC.yaml` now exits 0; `dsx gate ship --spec templates/ANALYSIS-SPEC.yaml` still exits 1 (pre-existing `test_template_validates_structurally_as_a_scaffold` still passes, confirming the scaffold still cannot be shipped unedited).
- **Committed in:** `737cbf4` (part of the Task 3 GREEN commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 — bug fix)
**Impact on plan:** Necessary for Task 3's stated acceptance criteria; zero scope creep — the fix is a one-token change to a pre-existing placeholder value, unrelated to any check family this phase ships.

## Issues Encountered

None beyond the Rule 1 fix above.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- 06-06 can now build `_validate_validity_frame_shape()` and `_validate_inference_shape()` against fixtures that already carry the exact shape those validators expect: the good fixture will produce none of the three new codes (`DSX-SPEC-080/081/082`), and the bad fixture is pre-loaded with six missing-sub-block targets, one `validity_frame` membership defect, and one `inference` membership defect.
- `templates/ANALYSIS-SPEC.yaml` is ready to keep passing `dsx gate plan` once 06-06's CRITICAL shape checks land, since every always-required and causal-conditional sub-block is already present with a legal (if honest-placeholder) value.
- No blockers for 06-06. `git diff --stat dsx/` is empty at every checkpoint — this plan touched no `dsx/` source, exactly as scoped.

---
*Phase: 06-contract-extension-decision-record-paradigm-manifest*
*Completed: 2026-08-08*

## Self-Check: PASSED

All modified files confirmed present on disk (`examples/good-ANALYSIS-SPEC.yaml`,
`examples/bad-ANALYSIS-SPEC.yaml`, `templates/ANALYSIS-SPEC.yaml`, `tests/test_dsx.py`, this
SUMMARY). All four task commits (`cd052cf`, `e170d13`, `bc2f28e`, `737cbf4`) confirmed present
in git history.
