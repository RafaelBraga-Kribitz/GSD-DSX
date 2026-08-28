---
phase: 07-validity-frame-checks-dsx-val
plan: 04
subsystem: infra
tags: [python, stdlib, unittest, design-effect, gate, citation-discipline]

# Dependency graph
requires:
  - phase: 07-validity-frame-checks-dsx-val (plan 03)
    provides: "dsx/frame/val.py's check(spec) dispatcher, DecisionRecord emission pattern, TestFrameParadigmReadBoundary D-11 proof"
  - phase: 07-validity-frame-checks-dsx-val (plan 01)
    provides: "dsx.mathx.design_effect(m, icc) — the Cochrane Handbook worked-example helper"
provides:
  - "dsx/frame/val.py — _check_unit_triad (DSX-VAL-020, CRITICAL) and _check_unit_drift (DSX-VAL-021, HIGH)"
  - "templates/ANALYSIS-SPEC.yaml repaired: unified unit placeholders so dsx init keeps clearing dsx gate plan"
  - "examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml repaired: declared clustered dependence + cluster_robust so the fixture blocks only on its own interference defect"
  - "TestValExpUnitsDisjointness — structural proof (REQ-P7-03) that DSX-VAL-020 and DSX-EXP-021 read disjoint field sets and never both fire"
affects: [07-05, 07-06]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Each unit judgment point (triad, drift) emits its own DecisionRecord, gated purely on the relevant sub-block being a dict — a units-bearing spec now appends two decision records (triad + drift), one per judgment, matching the estimand judgment's precedent from plan 07-03 but requiring the plan's own Task-1 decision-record test to filter by choice prefix once Task 2 landed a second record"
    - "Disjointness between two checks proven by construction, not observation: build a spec, run both checks, edit only one block, re-run, assert the untouched check's code set is unchanged — stronger than asserting today's fixtures merely don't overlap"
    - "A shipped module's content pinned with a CRLF-normalised sha256 hash as a test constant, so a silent edit to a file this phase must not touch fails a test instead of only a documentation claim"

key-files:
  created: []
  modified:
    - dsx/frame/val.py
    - tests/test_frame_val.py
    - templates/ANALYSIS-SPEC.yaml
    - examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
    - references/finding-codes.md

key-decisions:
  - "DSX-VAL-020's finder emits its own DecisionRecord (gated on units being a dict) and DSX-VAL-021's finder emits a second, separate DecisionRecord (also gated on units being a dict) — two judgment points, two records, per plan 07-03's 'one record per judgment point, not per finding' pattern. This meant the Task 1 test asserting 'exactly one decision record' for a units-bearing spec had to be rewritten in Task 2's commit to filter decisions by choice prefix ('unit triad:'), since after Task 2 a units-bearing spec always appends two records, not one."
  - "DSX-VAL-020's detail text calls dsx.mathx.design_effect(29.8, 0.02) = 1.576 (the Cochrane Handbook's own worked example) and states in the same sentence that the number is a fixed illustration, never a figure computed from the author's spec — the contract has no cluster-size or intraclass-correlation field anywhere to compute one from (D-02, D-11)."
  - "DSX-VAL-021 does pure agreement detection only (D-09): validity_frame.units.assignment vs design.randomization_unit, and validity_frame.units.analysis vs design.analysis_unit. No ordering, no judgment of whether a mismatch is handled — that stays with DSX-EXP-021 (design's own pair) and DSX-VAL-020 (validity frame's own pair). Disjointness is achieved by reading disjoint field sets, not by suppression logic between the two checks."
  - "The interference-shared-budget known-bad fixture's dependence block was completed rather than merely defanged: structure=clustered and cluster_var=user were added alongside method_family_required=cluster_robust, because impressions nested inside users is a real clustered structure and leaving structure=none beside a declared method family would have been internally incoherent (a second, accidental defect for plan 07-05's dependence check to trip on)."

requirements-completed: [REQ-P7-02, REQ-P7-03]

coverage:
  - id: D1
    description: "DSX-VAL-020 (CRITICAL): fires when validity_frame.units.observation is finer than units.assignment (D-08 plain string inequality) and dependence.method_family_required is blank; does not fire when either unit is blank, when the two units match, or when a method family is declared; detail quantifies the consequence via dsx.mathx.design_effect's Cochrane worked value (1.576), explicitly labelled a fixed illustration"
    requirement: "REQ-P7-02"
    verification:
      - kind: unit
        ref: "tests/test_frame_val.py::TestValUnits::test_finer_observation_with_no_method_family_fires_critical_units_020, test_finer_observation_with_declared_method_family_produces_no_units_020, test_matching_observation_and_assignment_produces_no_units_020_regardless_of_method, test_blank_observation_or_blank_assignment_produces_no_units_020, test_same_unit_named_two_ways_fires_units_020_with_alignment_remedy, test_units_020_detail_carries_the_deff_formula_and_illustration_wording, test_malformed_units_subblock_produces_no_finding_and_does_not_raise, test_unit_triad_judgment_point_appends_exactly_one_decision_record"
        status: pass
    human_judgment: false
  - id: D2
    description: "templates/ANALYSIS-SPEC.yaml's three unit placeholders unified to one string, so dsx init's scaffold copy still clears dsx gate plan after DSX-VAL-020 ships; ship still fails (scaffold proof intact)"
    requirement: "REQ-P7-02"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestCLI::test_template_validity_frame_and_inference_pass_gate_plan, test_template_validates_structurally_as_a_scaffold; tests/test_dsx.py::TestSpecStructure::test_template_validity_frame_and_inference_round_trip, test_template_vocabulary_placeholders_are_legal_members"
        status: pass
    human_judgment: false
  - id: D3
    description: "examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml repaired (structure=clustered, cluster_var=user, method_family_required=cluster_robust) so it blocks only on its own encoded interference defect, not on pseudo-replication"
    requirement: "REQ-P7-02"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::TestKnownBadCorpus::test_every_spec_passes_the_critical_threshold_gate_points, test_ship_gate_findings_are_all_documented_incidental_corpus_gaps, test_incidental_allowlist_names_no_target_family_code"
        status: pass
    human_judgment: false
  - id: D4
    description: "DSX-VAL-021 (HIGH): fires once per disagreeing pair (validity_frame.units.assignment vs design.randomization_unit; validity_frame.units.analysis vs design.analysis_unit) with normalised comparison; skips whenever either side of a pair is blank; never fires on either canonical fixture or any known-bad corpus fixture"
    requirement: "REQ-P7-03"
    verification:
      - kind: unit
        ref: "tests/test_frame_val.py::TestValUnits::test_assignment_vs_randomization_unit_disagreement_fires_high_units_021, test_analysis_vs_design_analysis_unit_disagreement_fires_units_021, test_both_pairs_agreeing_produces_no_units_021, test_blank_design_randomization_unit_produces_no_units_021, test_blank_validity_frame_assignment_produces_no_units_021, test_units_021_normalises_case_and_whitespace_before_comparing, test_units_021_never_fires_on_the_canonical_or_corpus_fixtures"
        status: pass
    human_judgment: false
  - id: D5
    description: "DSX-VAL-020 and DSX-EXP-021 (dsx/checks/design.py, unmodified) never both fire on one spec: proven against the current bad fixture, against a constructed unit-triad-only defect, across every fixture in the repository, and by construction (editing one block never changes the other check's code set); dsx/checks/design.py's content is pinned to a recorded sha256 hash"
    requirement: "REQ-P7-03"
    verification:
      - kind: unit
        ref: "tests/test_frame_val.py::TestValExpUnitsDisjointness (6 tests)"
        status: pass
    human_judgment: false
  - id: D6
    description: "Citation text (Kish 1965, Cochrane Handbook v6.5, Hernan & Robins 2020) and the UNVERIFIED-locator/fixed-illustration honesty disclosures in both new docstrings are accurate and not laundered from a plausible-sounding but uncited source"
    verification: []
    human_judgment: true
    rationale: "Citation-accuracy review is a human judgment call per this plan's threat model (T-7-04) and prohibitions; automated tests confirm the Citation:/Reference value:/Structural criterion: regex markers and the '# D-05: <CODE>' test markers are present, but cannot confirm the underlying bibliographic claims are accurate."

duration: ~5min
completed: 2026-08-12
status: complete
---

# Phase 7 Plan 4: DSX-VAL-020/021 Unit Triad and Unit Drift Checks Summary

**`dsx/frame/val.py` gains the unit triad (`DSX-VAL-020`, CRITICAL — pseudo-replication with no method family, quantified via `dsx.mathx.design_effect`'s Cochrane worked value 1.576) and unit drift (`DSX-VAL-021`, HIGH — validity-frame vs design-block unit disagreement), landing in the same commits as repairs to the template and the interference known-bad fixture that the new check would otherwise have broken, plus a structural proof that `DSX-VAL-020` and `DSX-EXP-021` can never both fire on one defect.**

## Performance

- **Duration:** ~5 min (git commit span 17:04:14–17:09:26 on 2026-08-12; does not include the reading/design time before the first commit)
- **Tasks:** 3
- **Files modified:** 5 (`dsx/frame/val.py`, `tests/test_frame_val.py`, `templates/ANALYSIS-SPEC.yaml`, `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml`, `references/finding-codes.md`)

## Accomplishments

- `DSX-VAL-020` (CRITICAL): fires when `validity_frame.units.observation` is finer than `units.assignment` (D-08 plain string inequality — the fields carry no closed, orderable vocabulary) and `dependence.method_family_required` is blank. Its `detail` states the design-effect formula in words and symbols, calls `dsx.mathx.design_effect(29.8, 0.02)` to get the Cochrane Handbook's own worked value (1.576), and says in the same sentence that this is a fixed illustration — the contract has no cluster-size or intraclass-correlation field anywhere to compute a real one from (D-02, D-11). Its remedy names both accepted ways out: align the two unit names, or declare a method family.
- `DSX-VAL-021` (HIGH): pure agreement detection (D-09) between two field pairs — `validity_frame.units.assignment` vs `design.randomization_unit`, and `validity_frame.units.analysis` vs `design.analysis_unit`. Fires once per disagreeing pair, skips whenever either side is blank, and makes no judgment about whether a mismatch is handled (that stays with `DSX-EXP-021` and `DSX-VAL-020` respectively).
- `templates/ANALYSIS-SPEC.yaml`'s three unit placeholders (previously three different strings — a literal `DSX-VAL-020` trigger) are unified into one placeholder naming a single grain, with a comment stating the values are an example to replace. `dsx init`'s scaffold copy still clears `dsx gate plan`; `dsx gate ship` on the raw template still fails (scaffold proof intact).
- `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml`'s dependence block (previously `structure: none`, empty `cluster_var`, empty `method_family_required` — a literal `DSX-VAL-020` trigger) is completed to `structure: clustered`, `cluster_var: user`, `method_family_required: cluster_robust` — an honest declaration (impressions nested inside users is a real clustered structure), not a suppression. The fixture now blocks only on its own encoded interference defect, per the corpus's stated guarantee.
- `TestValExpUnitsDisjointness` (Task 3, REQ-P7-03): proves the current bad fixture trips `DSX-EXP-021` and not `DSX-VAL-020`; a constructed spec whose validity frame trips the unit triad while its design block's two units agree trips `DSX-VAL-020` and not `DSX-EXP-021`; no fixture in the repository (both canonical fixtures, the template, and every known-bad corpus file) ever trips both codes; editing only one block's fields never changes the other check's fired-code set (proof by construction, not observation); and `dsx/checks/design.py`'s content is pinned to a recorded, CRLF-normalised sha256 hash so a silent edit to that unmodified-by-Phase-7 file fails a test.
- `references/finding-codes.md` regenerated after each task; now carries `DSX-VAL-020` and `DSX-VAL-021` in the "Validity frame" section.

## Task Commits

Each task was committed atomically:

1. **Task 1: Ship DSX-VAL-020, and repair the template and the interference fixture in the same commit** - `8da2a8d` (feat)
2. **Task 2: Ship DSX-VAL-021, the unit drift axis** - `689ae2b` (feat)
3. **Task 3: Prove DSX-VAL-020 and DSX-EXP-021 cannot both fire on one defect** - `7299b46` (test)

**Plan metadata:** committed alongside this SUMMARY (worktree mode — orchestrator finalizes STATE.md/ROADMAP.md after merge)

_Note: per this plan's `tdd="true"` task structure (matching plans 07-01 and 07-03's precedent), each task's `<action>` describes adding the check/repair/test code as one unit rather than a separate RED-then-GREEN pair, so Tasks 1 and 2 landed as single verified-green `feat` commits and Task 3 as a single `test` commit. See "TDD Gate Compliance" below._

## Files Created/Modified

- `dsx/frame/val.py` - Added `_check_unit_triad()` (`DSX-VAL-020`) and `_check_unit_drift()` (`DSX-VAL-021`), each wired into `check()`'s dispatcher with its own gated `DecisionRecord` emission; added `_UNIT_TRIAD_ICC`/`_UNIT_TRIAD_M`/`_UNIT_TRIAD_CITATION`/`_UNIT_DRIFT_CITATION` module constants; imported `design_effect` from `dsx.mathx`; updated the module docstring's code-count description
- `tests/test_frame_val.py` - `TestValUnits` (14 tests: 8 for `DSX-VAL-020` including the D-05 marker, 7 for `DSX-VAL-021` including the D-05 marker and a real-fixture-loading no-collision test — one test method's assertion was rewritten mid-plan, see Deviations); `TestValExpUnitsDisjointness` (6 tests: the two directional-firing proofs, the whole-corpus scan, the two construction-based edit-isolation proofs, and the pinned content-hash proof); imports `dsx.checks.design`, `copy`, `hashlib`
- `templates/ANALYSIS-SPEC.yaml` - Unit placeholders unified to `<user_id>` across `observation`/`assignment`/`analysis`, with an explanatory comment; `design:` block's `randomization_unit`/`analysis_unit` untouched (still `null`, so Task 2's drift check has nothing to compare against the scaffold)
- `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml` - `dependence.structure`, `dependence.cluster_var`, `dependence.method_family_required` completed; header comment extended to explain the repair and cross-reference D-14
- `references/finding-codes.md` - Regenerated twice (once per new code); now lists `DSX-VAL-020` (CRITICAL) and `DSX-VAL-021` (HIGH)

## Decisions Made

- Each unit judgment point emits its own `DecisionRecord`, matching plan 07-03's "one record per judgment point, not per finding" pattern extended to two judgment points instead of one. This is a deliberate departure from folding both unit checks into a single shared record the way the estimand pair does — the two unit checks read genuinely different field sets (`validity_frame` only, vs `validity_frame` + `design`), so a single combined record would have mixed two judgments' inputs together.
- `DSX-VAL-020`'s detail text states the design-effect illustration is drawn from the Cochrane Handbook's own published worked example (`ICC=0.02, m=29.8 → 1.576`), never as a number computed from the spec — matching D-10/D-11's correction that the earlier, unpublished `3.45` value must not ship.
- The interference fixture's repair completed the dependence block honestly (`structure: clustered`, `cluster_var: user`) rather than only setting `method_family_required` — leaving `structure: none` beside a declared method family would have been internally incoherent and would have handed plan 07-05's dependence check (`DSX-VAL-030`) a second, accidental defect to trip on in this same fixture.
- `TestValExpUnitsDisjointness`'s Behaviour 4 (editing only one block never changes the other check's code set) is the structural core of REQ-P7-03: it is what makes the disjointness guarantee hold for specs not yet written, not just for the fixtures on disk today.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Task 1's "exactly one decision record" test broke once Task 2 landed a second judgment-point record**

- **Found during:** Task 2, while wiring `_check_unit_drift`'s decision record into `check()`
- **Issue:** Task 1's `test_units_judgment_point_appends_exactly_one_decision_record` asserted `len(decisions) == 1` for any spec carrying a `units` dict. Task 2 (as the plan requires) adds a second `DecisionRecord` for the drift judgment point, gated on the same `isinstance(units, dict)` condition — so after Task 2, a units-bearing spec always appends two records, and the Task 1 test's exact-count assertion would fail.
- **Fix:** Renamed the test to `test_unit_triad_judgment_point_appends_exactly_one_decision_record` and rewrote its assertion to filter `decisions` by `choice.startswith("unit triad:")` before counting, so it verifies the triad judgment's own record count and shape regardless of how many other judgment-point records also fired. No change to `_check_unit_triad`'s logic or the triad decision record's content.
- **Files modified:** `tests/test_frame_val.py` (test only, no production-code change)
- **Verification:** `python3 -m unittest tests.test_frame_val -v -k units` — all 14 `TestValUnits` tests pass after the rewrite; full suite (362 tests) confirmed green afterward.
- **Committed in:** `689ae2b` (Task 2 commit, alongside the new drift check and its own tests)

---

**Total deviations:** 1 auto-fixed (1 bug, test-only)
**Impact on plan:** No production-code behavior changed. The fix corrects a test assertion that was scoped too narrowly to "as of Task 1" state and would otherwise have made Task 2's own commit fail its own inherited test suite.

## Issues Encountered

- **Plan acceptance-criteria one-liners using `str(f[0].severity)=='CRITICAL'`/`=='HIGH'` do not hold in this environment's Python (3.14.6).** `Finding.severity` is `dsx.findings.Severity`, an `IntEnum`; since Python 3.11, `IntEnum.__str__` prints the underlying int value (`str(Severity.CRITICAL) == '50'`), not the member name. This affects the literal acceptance-criteria commands for both `DSX-VAL-020` and `DSX-VAL-021` (and will affect the same pattern already written into plans 07-05 and 07-06's PLAN.md files). No shipped code or test anywhere in the repository relies on `str(Severity.X)` — confirmed by grep before treating this as a real defect — so this is a documentation artifact in the plan's own verification commands, not a code bug to fix. Verified the underlying claim genuinely holds using the form the rest of the test suite already uses: `finding.severity == Severity.CRITICAL` and `finding.severity.label == 'CRITICAL'`, both of which pass. Flagging here so a downstream reader of plans 07-05/07-06 isn't surprised when the same literal one-liner "fails" despite the check being correct — the fix, if wanted, is a `Severity.__str__` override, which is out of this plan's scope (an architectural change to shared infrastructure, not a two-helper-function unit check).

## User Setup Required

None - no external service configuration required. D-01 holds: only the Python 3.9+ standard library, plus the already-shipped `dsx.mathx.design_effect` (itself stdlib-only), was used across all three tasks; no new dependency was added.

## Next Phase Readiness

- `dsx/frame/val.py`'s `check()` dispatcher now calls four private helpers (`_check_estimand_completeness`, `_check_estimand_falsifiability`, `_check_unit_triad`, `_check_unit_drift`); plans 07-05 (dependence, identification) and 07-06 (sampling frame, missingness, measurement) add the remaining five as one call each, per the established pattern.
- Verified before finishing: `python3 -m unittest discover -s tests` — 362 tests, OK (2 skipped, same 2 as baseline); `python3 scripts/gen-finding-catalogue.py --check` — exit 0, "finding catalogue is current" (the pre-existing `DSX-COH-030`/`DSX-SPEC-070` double-declaration warnings are unchanged from the 07-03 baseline; a new `DSX-VAL-021` double-declaration warning appears because `_check_unit_drift` calls `report.add("DSX-VAL-021", ...)` twice with two different titles for its two comparison pairs — the same shape as the pre-existing `DSX-SPEC-070` pattern, and it does not affect D-05 enforcement since both call sites share one docstring).
- `python3 -m dsx.cli gate plan|execute|verify|ship --spec examples/good-ANALYSIS-SPEC.yaml` all exit 0; `gate plan --spec templates/ANALYSIS-SPEC.yaml` exits 0 (the `dsx init` regression holds); `gate ship --spec templates/ANALYSIS-SPEC.yaml` exits 1 (scaffold proof intact); `gate plan --spec examples/bad-ANALYSIS-SPEC.yaml` output names `DSX-EXP-021` and does not name `DSX-VAL-020`.
- `python3 -m unittest tests.test_known_bad_corpus -v` — 13 tests, OK; the interference fixture's repaired dependence block introduces no new incidental gap (no addition to `_INCIDENTAL_GAP_CODES` was needed).
- `git diff --stat -- dsx/checks/` returns nothing across all three of this plan's commits — `dsx/checks/design.py` and the rest of the legacy checks package remain untouched, and `TestValExpUnitsDisjointness::test_design_checks_py_content_is_unmodified_since_phase_start` now guards this mechanically going forward within Phase 7.
- No blockers for plans 07-05/07-06, which are this phase's declared consumers of `dsx/frame/val.py`'s four-helper dispatcher.

## TDD Gate Compliance

This plan's frontmatter sets `type: tdd`, and each task individually carries `tdd="true"`. Consistent with plans 07-01 and 07-03's precedent, Tasks 1 and 2's `<action>` describe adding the check/repair/test code as one unit rather than a separate RED-then-GREEN sequence, so each landed as a single verified-green `feat` commit rather than a `test(...)`/`feat(...)` pair. Task 3 is itself entirely a test addition (no new production code), so it committed as a single `test` commit. Every test in all three tasks was written against the plan's `<behavior>` blocks, run, and confirmed passing before its task's commit. No commit in this plan's git log matches a bare `^test\(07-04` immediately followed by production code in the same commit for Tasks 1/2, by task design.

---
*Phase: 07-validity-frame-checks-dsx-val*
*Completed: 2026-08-12*

## Self-Check: PASSED

- FOUND: dsx/frame/val.py
- FOUND: tests/test_frame_val.py
- FOUND: templates/ANALYSIS-SPEC.yaml
- FOUND: examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
- FOUND: references/finding-codes.md
- FOUND: .planning/phases/07-validity-frame-checks-dsx-val/07-04-SUMMARY.md
- FOUND commit 8da2a8d (Task 1)
- FOUND commit 689ae2b (Task 2)
- FOUND commit 7299b46 (Task 3)
