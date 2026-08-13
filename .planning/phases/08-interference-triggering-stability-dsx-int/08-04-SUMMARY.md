---
phase: 08-interference-triggering-stability-dsx-int
plan: 04
subsystem: gate-checks
tags: [dsx-frame, interference, triggering, dilution, deng-hu, decision-record, catalogue, gated-backlog]
status: complete

# Dependency graph
requires:
  - phase: 08-interference-triggering-stability-dsx-int
    plan: "08-01"
    provides: "dsx.mathx.diluted_effect(delta_triggered, user_trigger_rate) — the additive-metric dilution kernel this plan's docstring points at by name, never calls (D-09)"
  - phase: 08-interference-triggering-stability-dsx-int
    plan: "08-02"
    provides: "_TARGET_DEFECT_CODES + _classify_target_defect() in tests/test_known_bad_corpus.py, and the committed triggering-dilution fixture pair this plan's gate-level tests measure against"
  - phase: 08-interference-triggering-stability-dsx-int
    plan: "08-03"
    provides: "dsx/frame/interference.py's check() dispatcher, _RISK_MITIGATION_MAP, DecisionRecord emission idiom, and dsx.spec.needs_causal_block — this plan's third helper is wired into the same dispatcher"
provides:
  - "dsx/frame/interference.py: DSX-INT-030 (an additive metric analysed on the eligible population with no declared dilution adjustment), CRITICAL, gated on dsx.spec.needs_causal_block"
  - "_ADDITIVE_METRIC_TYPES ({count, sum, average}) and _RATIO_METRIC_TYPES ({ratio, rate}) — a partition over dsx.spec.METRIC_TYPES, referenced not coined (D-11)"
  - "brief.md section 6.5's sixth gated-backlog row: ratio-metric dilution, entry condition rewritten from a false access premise to the real per-user-data blocker (D-12)"
  - "tests/test_frame_interference.py: 15 new tests (36 total) covering the fire condition, both ratio/rate scope-boundary escapes, the undeclared-type skip record, mixed-metric detail naming, malformed-shape degradation, and four gate-level proofs"
  - "tests/test_known_bad_corpus.py: triggering-dilution -> {plan: DSX-INT-030} in _TARGET_DEFECT_CODES, plus a documentation-content test guarding the new brief.md row"
affects: ["08-05-stability-check", "08-06-phase-close-out"]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Partition constant over an existing closed vocabulary (dsx.spec.METRIC_TYPES), following the DEPENDENCE_ADMISSIBLE_METHODS placement precedent — referenced, not registered in _VOCABULARIES, not coined as a parallel taxonomy"
    - "Per-metric skip DecisionRecord (no report.add) for an unclassifiable declaration, plus one overall fire/clear DecisionRecord emitted only when there is something concrete to adjudicate — kept the two record kinds from colliding when a spec's only metric carries no declared type (Test 7)"
    - "Documentation-content test asserting presence of pinned substrings in a corrected row, proven to fail when the row is removed and restored before commit — same idiom as test_bayesian_postmortem_states_the_deng_bound_and_its_value"

key-files:
  created: []
  modified:
    - dsx/frame/interference.py
    - tests/test_frame_interference.py
    - tests/test_known_bad_corpus.py
    - references/finding-codes.md
    - brief.md

key-decisions:
  - "DSX-INT-030's firing condition does NOT gate on expected_trigger_rate — 08-CONTEXT.md's D-09 states the condition as exactly two triggering-block fields (analysis_population, dilution_adjusted) plus D-11's additive-metric-type test, with no materiality/trigger-rate clause, and the plan's own action text lists only those three conditions"
  - "Consequence, anticipated by 08-02's own fragility note and confirmed by measurement: weak-identification-mmm (Phase 7 fixture, expected_trigger_rate: 1.0) now also blocks on DSX-INT-030 at plan/verify/ship alongside its own DSX-VAL-040 — documented via a second key (\"verify\": \"DSX-INT-030\") in its _TARGET_DEFECT_CODES entry rather than by adding a trigger-rate exemption to the check"
  - "The overall DSX-INT-030 fire/clear DecisionRecord is emitted only when at least one additive metric was found to adjudicate — not unconditionally at the population==eligible judgment point — so a spec whose only metric carries no declared type produces exactly one decision record (the skip record), matching Test 7"

requirements-completed: [REQ-P8-03, REQ-P8-04]

coverage:
  - id: D1
    description: "DSX-INT-030 fires CRITICAL on an additive metric (count/sum/average) analysed on the eligible population with dilution_adjusted not true; clears when dilution_adjusted is true, when analysis_population is triggered, or when every declared metric is ratio/rate/percentile/index"
    requirement: "REQ-P8-03"
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py::TestTriggeringDilution (15 tests)"
        status: pass
      - kind: unit
        ref: "tests/test_frame_interference.py -k triggering"
        status: pass
      - kind: unit
        ref: "tests/test_frame_interference.py -k ratio_scope (2 tests)"
        status: pass
    human_judgment: false
  - id: D2
    description: "A metric with no declared type produces no finding and exactly one decision record naming the skip and its reason; a mixed-metric spec (1 ratio + 2 additive) produces exactly one DSX-INT-030 finding naming both additive metrics by name"
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py::TestTriggeringDilution::test_metric_with_no_declared_type_produces_no_finding_and_one_skip_decision_record"
        status: pass
      - kind: unit
        ref: "tests/test_frame_interference.py::TestTriggeringDilution::test_mixed_metrics_one_ratio_two_additive_produces_one_finding_naming_both_additive"
        status: pass
    human_judgment: false
  - id: D3
    description: "_ADDITIVE_METRIC_TYPES and _RATIO_METRIC_TYPES are each subsets of dsx.spec.METRIC_TYPES, disjoint from each other, and their union is a proper subset (percentile/index unadjudicated)"
    requirement: "REQ-P8-04"
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py::TestTriggeringDilution::test_additive_and_ratio_metric_type_partitions_are_subsets_disjoint_and_proper"
        status: pass
      - kind: other
        ref: "python3 -c \"...\" prints ['average','count','sum'] ['rate','ratio'] ['index','percentile']"
        status: pass
    human_judgment: false
  - id: D4
    description: "Gate-level: committed triggering-dilution fixture exits 1 at plan naming DSX-INT-030 and exits 0 at execute; good fixture, template and both monitoring fixtures never name DSX-INT-030 at plan; good fixture clears ship"
    requirement: "REQ-P8-03"
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py::TestTriggeringDilution::test_committed_triggering_dilution_fixture_blocks_plan_naming_int_030"
        status: pass
      - kind: unit
        ref: "tests/test_frame_interference.py::TestTriggeringDilution::test_committed_triggering_dilution_fixture_clears_execute"
        status: pass
      - kind: unit
        ref: "tests/test_frame_interference.py::TestTriggeringDilution::test_good_and_monitoring_fixtures_and_template_still_clear_plan"
        status: pass
      - kind: unit
        ref: "tests/test_frame_interference.py::TestTriggeringDilution::test_good_fixture_clears_ship_resolving_sibling_artifacts_from_its_own_directory"
        status: pass
    human_judgment: false
  - id: D5
    description: "brief.md section 6.5 carries a sixth row naming ratio-metric dilution, with an entry condition naming the per-user-data requirement of Formula (3) rather than the access premise research proved false; a documentation-content test guards it and was shown to fail when the row was removed"
    requirement: "REQ-P8-04"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::TestKnownBadCorpus::test_brief_states_the_ratio_metric_dilution_entry_condition_as_a_falsifiable_blocker"
        status: pass
      - kind: other
        ref: "row temporarily deleted, test re-run, observed 3 subTest AssertionErrors ('Ratio-metric dilution for trigger analysis' / 'Formula (3)' / 'per-unit trigger and outcome data reaching the gate' not found), row restored, git diff brief.md confirmed clean single-row addition"
        status: pass
    human_judgment: false
  - id: D6
    description: "brief.md section 6.5's entry-condition cell contains no wording asserting the paper or Formula (3) is unobtainable"
    requirement: "REQ-P8-04"
    verification:
      - kind: other
        ref: "grep -iE 'unobtainable|unavailable|cannot be obtained|not obtainable' on the new row — no match"
        status: pass
    human_judgment: false
  - id: D7
    description: "python3 scripts/gen-finding-catalogue.py --check exits 0 with DSX-INT-030 carrying a Citation: line, a Structural criterion: line, and a linked # D-05: DSX-INT-030 test marker"
    requirement: "REQ-P8-03"
    verification:
      - kind: other
        ref: "python3 scripts/gen-finding-catalogue.py --check"
        status: pass
    human_judgment: false
  - id: D8
    description: "The brief.md section 6.5 entry condition names a falsifiable blocker rather than restating the access premise research proved false — backstop, no test can decide falsifiability"
    verification: []
    human_judgment: true
    rationale: "Plan's own <verification> block marks this a backstop must-have: falsifiability of a stated blocker is a judgment call, not a mechanically decidable property. The executor read the committed row (brief.md:376) and confirms it names per-unit trigger/outcome data reaching the gate as the blocker, states plainly the paper is freely available and the equation readable today (access was never the blocker), and states the item may be permanently out of scope under the determinism doctrine rather than promising eventual delivery."

# Metrics
duration: ~55min
completed: 2026-08-13
---

# Phase 8 Plan 04: Triggering/dilution check (DSX-INT-030) Summary

**Shipped `DSX-INT-030` — an additive metric (count/sum/average) analysed on the eligible population with no declared dilution adjustment, cited to Deng & Hu (2015) Formula (1) and scoped away from ratio/rate metrics by a partition over `dsx.spec.METRIC_TYPES` — and rewrote `brief.md` section 6.5's ratio-metric dilution row to name the real per-user-data blocker instead of the access premise research proved false.**

## Performance

- **Duration:** ~55 min
- **Completed:** 2026-08-13T10:57:17Z
- **Tasks:** 2 completed
- **Files modified:** 5

## Accomplishments

- `dsx/frame/interference.py` gained `_ADDITIVE_METRIC_TYPES` (`{count, sum, average}`) and `_RATIO_METRIC_TYPES` (`{ratio, rate}`) — a partition over the existing `dsx.spec.METRIC_TYPES`, not a coined parallel vocabulary, matching the `DEPENDENCE_ADMISSIBLE_METHODS` placement precedent
- A new private helper, `_check_triggering_dilution`, fires `DSX-INT-030` at CRITICAL when `validity_frame.triggering.analysis_population` is `eligible`, `dilution_adjusted` is not the literal boolean `True` (a deliberate identity comparison, never `is_blank` — `is_blank(False)` is `False`), and at least one declared metric's normalized type is additive. One finding per spec, naming every additive metric by name and type. A metric with no declared type is skipped (not adjudicated) with one `DecisionRecord` per skip; the overall fire/clear judgment record is emitted only when there is at least one additive metric to judge, so an all-undeclared-type spec produces exactly one decision record
- Wired into the `check()` dispatcher after the two existing helpers; still gated on `needs_causal_block(spec)` and an absent/malformed `validity_frame`
- `references/finding-codes.md` regenerated (227 codes); `python3 scripts/gen-finding-catalogue.py --check` confirms `DSX-INT-030` carries both required docstring lines and the test marker
- `tests/test_frame_interference.py` gained 15 tests (`TestTriggeringDilution`, 36 total in the module), covering all 13 named behaviours plus the two additional gate-level fixture-safety proofs
- `tests/test_known_bad_corpus.py::_TARGET_DEFECT_CODES` gained `"triggering-dilution": {"plan": "DSX-INT-030"}`
- `brief.md` section 6.5 gained a sixth gated-backlog row naming ratio-metric dilution, with an entry condition that names Formula (3)'s per-user-data requirement — not the "obtained from primary source" premise `08-CONTEXT.md`'s D-12 established is false — and a documentation-content test (`test_brief_states_the_ratio_metric_dilution_entry_condition_as_a_falsifiable_blocker`) guarding it, proven to fail with the row removed and restored before commit

## Task Commits

Each task was committed atomically:

1. **Task 1: Ship DSX-INT-030 with the additive metric partition and the undeclared-type skip record** - `36ff448` (feat)
2. **Task 2: Write the ratio-metric dilution row in the gated backlog and the test that guards it** - `c1a7307` (docs)

**Plan metadata:** commit deferred to orchestrator merge (worktree mode — STATE.md/ROADMAP.md not touched by this agent)

## Files Created/Modified

- `dsx/frame/interference.py` - `_ADDITIVE_METRIC_TYPES`/`_RATIO_METRIC_TYPES` constants, `_check_triggering_dilution` helper, dispatcher wiring, module docstring updated to say three of four codes now ship
- `tests/test_frame_interference.py` - `TestTriggeringDilution` (15 tests): fire condition, dilution_adjusted=true clear, triggered-population clear, ratio/rate scope boundary (2 tests), percentile unadjudicated, undeclared-type skip record, mixed-metric detail naming, partition-contract test, descriptive-spec skip, malformed-shape degradation, and 4 gate-level fixture proofs
- `tests/test_known_bad_corpus.py` - `triggering-dilution` and `weak-identification-mmm`'s `"verify"` key added to `_TARGET_DEFECT_CODES`; new documentation-content test for the `brief.md` row
- `references/finding-codes.md` - regenerated, `DSX-INT-030` row added to the `DSX-INT-*` table, total 227
- `brief.md` - section 6.5 gated-backlog table gained a sixth row (ratio-metric dilution)

## Decisions Made

**1. `DSX-INT-030` does not gate on `expected_trigger_rate`.** The plan's own action text states the firing condition as exactly three checks — `analysis_population == eligible`, `dilution_adjusted is not True`, at least one additive metric — with no fourth, materiality-based condition. `08-CONTEXT.md` D-09 independently confirms this: "`DSX-INT-030` adjudicates declarations only: is `triggering.analysis_population == "eligible"` and `dilution_adjusted` not true," naming only those two triggering-block fields plus D-11's additive-metric test. The orchestrator's pre-flight context flagged this as a live decision point (08-02's own fragility note on `weak-identification-mmm`), to be decided deliberately rather than discovered as a surprise failure. Decision: implement exactly what D-09 and the plan's action text state, with no trigger-rate exemption.

**2. Consequence, measured and handled.** `weak-identification-mmm` (a Phase 7 fixture declaring `analysis_population: eligible`, `dilution_adjusted: false`, `metrics[0].type: sum`, `expected_trigger_rate: 1.0`) now blocks on `DSX-INT-030` at `plan`/`verify`/`ship` alongside its existing `DSX-VAL-040`. Measured directly (`dsx gate ship --json`) rather than assumed. `DSX-INT-030` correctly names a second, genuine defect this fixture happens to also encode (an additive metric analysed on the eligible population with no adjustment declared is true regardless of the trigger rate being 1.0 by construction) — not a false positive, and not fixed by editing the fixture's own honestly-declared scenario. Documented via a second dict key (`"verify": "DSX-INT-030"`) in `weak-identification-mmm`'s `_TARGET_DEFECT_CODES` entry, alongside its existing `"plan": "DSX-VAL-040"`, so `_own_target_codes()` (which flattens every point's value for a slug into one set, regardless of which key holds it) documents the code for the ship-completeness test without needing a frozenset value or any change to `_own_target_codes()`/`_effective_target_map()` — both left exactly as plan 08-02/09-01 shipped them, per the orchestrator's explicit instruction not to fold them away.

**3. The overall DSX-INT-030 decision record is conditional on having something to judge.** The plan's action text says to append "the helper's own adjudication record at its key judgment point, as the two existing helpers do," but Test 7 (a spec whose only metric has no declared type) requires exactly one decision record — the skip record. Resolved by emitting the overall fire/clear record only when at least one additive metric was found (i.e., there is a real judgment to record), not unconditionally at the `analysis_population == eligible` checkpoint. A spec with zero additive metrics (all skip-typed, or all ratio/percentile/etc.) produces zero or more skip records and no overall record.

**4. `test_good_fixture_clears_ship` needed no `--phase-dir`.** `dsx/cli.py::cmd_gate` resolves relative evidence/profile paths from `args.phase_dir or path.parent`. My first draft of this gate-level test passed a temporary `--phase-dir`, which made `resolve_root` a throwaway tempdir instead of `examples/` — the good fixture's sibling artifacts (`DATA-PROFILE.yaml`, figures, narrative, entrypoint) live next to it under `examples/`, so the ship gate failed on unrelated `DSX-DQ-001`/`DSX-CLM-031`/`DSX-FIG-001`/etc. findings, not `DSX-INT-030`. Fixed by matching the plan's own acceptance-criteria invocation exactly (`dsx gate ship --spec examples/good-ANALYSIS-SPEC.yaml`, no `--phase-dir`) — this is a test-authoring correction (Rule 1), not a check-logic change.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking issue] `weak-identification-mmm` newly blocks on `DSX-INT-030`**
- **Found during:** Task 1, running the full suite after implementing the check
- **Issue:** Per Decision 1 above, not gating on `expected_trigger_rate` (as D-09 and the plan's action text both specify) makes `weak-identification-mmm` — flagged as a live fragility risk in plan 08-02's own corpus comment — start firing `DSX-INT-030` at `plan`/`verify`/`ship`. Without a corpus map update, `test_ship_gate_findings_are_all_documented_incidental_corpus_gaps` fails (undocumented CRITICAL finding).
- **Fix:** Added `"verify": "DSX-INT-030"` to `weak-identification-mmm`'s existing `_TARGET_DEFECT_CODES` entry (see Decision 2). No change to `_own_target_codes()`, `_effective_target_map()`, or `_EXPECTED_CAUGHT_DEFECTS` — both maps left exactly as 08-02/09-01 shipped them, per the orchestrator's explicit instruction.
- **Files modified:** `tests/test_known_bad_corpus.py`
- **Verification:** `python3 -m unittest tests.test_known_bad_corpus -v` — 18/18 pass; `python3 -m unittest discover -s tests` — 502/502 pass
- **Committed in:** `36ff448` (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (Rule 3, blocking issue — anticipated and pre-flagged by the orchestrator's pre-flight context, not a surprise)
**Impact on plan:** Necessary to keep the corpus's own stated guarantees true against the check as specified by D-09 and the plan's own action text. No scope creep — the fixture's `_TARGET_DEFECT_CODES` entry gained one key, nothing else changed.

## Issues Encountered

None beyond the deviation above and the test-authoring correction documented in Decision 4 (not a deviation from the plan — a correction to a test I wrote in this same plan, caught and fixed before commit).

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `DSX-INT-030` ships and is fully wired: registered via the existing `interference` check in `plan`/`verify`/`ship` gate profiles (unchanged from plan 08-03), reachable in `known_codes()`, documented in `references/finding-codes.md`.
- Three of the four `DSX-INT-*` codes now ship (`DSX-INT-010`, `DSX-INT-011`, `DSX-INT-030`); only `DSX-INT-040` (novelty/primacy) remains for plan 08-05.
- `brief.md` section 6.5's D-18 deliverable (four artifacts for REQ-P8-04) is complete: the rewritten row, the docstring's additive-only scope paragraph, the ratio-scope-boundary test, and the documentation-content test guarding the row.
- **Carried-forward, not a defect:** `bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` and `frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml` both exit 1 at `dsx gate plan` — measured and confirmed to be exclusively `DSX-PAR-010`/`DSX-PAR-011` (Phase 9's already-shipped monitoring pair, merged onto this branch before Wave 3 ran), never `DSX-INT-030`. This is the same pre-existing, out-of-scope discrepancy plan 08-03's own SUMMARY already documented for `DSX-INT-010`/`DSX-INT-011`; the plan's literal "exits 0" acceptance-criteria wording is stale relative to the merged tree, but the substantive guarantee this plan owns (the ratio-metric scope boundary holds; `DSX-INT-030` never fires on either monitoring fixture) is verified directly via `--json` finding-code inspection and via `tests/test_frame_interference.py::TestTriggeringDilution::test_good_and_monitoring_fixtures_and_template_still_clear_plan`, which asserts `DSX-INT-030` specifically is absent rather than asserting a bare exit code.
- Baseline preserved: 486 tests before this plan, 502 after (+15 new in `test_frame_interference.py`, +1 new in `test_known_bad_corpus.py`), none weakened, skipped, or deleted (`skipped=2` unchanged, pre-existing). `sh scripts/check.sh` passes end to end.

---
*Phase: 08-interference-triggering-stability-dsx-int*
*Completed: 2026-08-13*
