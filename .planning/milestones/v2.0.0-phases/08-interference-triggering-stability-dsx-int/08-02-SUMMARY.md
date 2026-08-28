---
phase: 08-interference-triggering-stability-dsx-int
plan: 02
subsystem: testing
tags: [pytest, unittest, yaml-fixtures, gate-corpus, validity-frame]

# Dependency graph
requires:
  - phase: 06-contract-extension-decision-record-paradigm-manifest
    provides: the validity_frame.interference/triggering/stability sub-blocks and their vocabularies, and the known-bad corpus discipline (full-shape clones, one defect per fixture)
  - phase: 07-validity-frame-checks-dsx-val
    provides: dsx/frame/val.py (DSX-VAL-*), the weak-identification-mmm fixture and its _EXPECTED_PLAN_BLOCKERS-era corpus entry
provides:
  - "_TARGET_DEFECT_CODES: a per-fixture (slug -> {gate_point: code}) target-defect map in tests/test_known_bad_corpus.py, replacing the family-prefix allow-list that could express at most one code per family"
  - "_classify_target_defect(): a parameterised classification helper, proven against fabricated inputs, that plans 08-03/08-04/09-x add one map entry each to"
  - "examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml + POSTMORTEM.md: the fourth known-bad fixture pair, the one DSX-INT-030 will be measured against"
  - "honest stability declarations (novelty_primacy_assessed: true, non-blank evidence) on all five committed known-bad fixtures, so none of them collides with DSX-INT-040 once it ships"
affects: [08-03-interference-mitigation-admissibility, 08-04-triggering-dilution-check, 08-05-stability-check, 09-monitoring-discipline-symmetric-dsx-par]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Per-fixture target-defect map (dict[slug][gate_point] -> code) replacing a family-prefix allow-list, once a code family ships more than one member"
    - "Two-proofs discipline applied to a corpus classification helper: real-fixture assertions plus a synthetic-input TestCase (mirrors tests/test_frame_boundary.py)"

key-files:
  created:
    - examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml
    - examples/known-bad/triggering-dilution-POSTMORTEM.md
  modified:
    - examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
    - examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml
    - examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml
    - examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml
    - tests/test_known_bad_corpus.py
    - tests/test_frame_val.py

key-decisions:
  - "_TARGET_DEFECT_CODES is not committed literally empty: it carries weak-identification-mmm -> {plan: DSX-VAL-040}, migrated from Phase 7's now-deleted _EXPECTED_PLAN_BLOCKERS, because that code already ships in this milestone and a literally-empty map would have silently dropped its existing block guarantee"
  - "weak-identification-mmm's stability block was also fixed (novelty_primacy_assessed: true), beyond the plan's named three fixtures, because it independently violated this plan's own must_have truth and would have collided with DSX-INT-040 identically to the three named fixtures"
  - "triggering-dilution's incidental gaps at ship (DSX-MET-040, DSX-CLM-031, DSX-REP-030, DSX-COH-031, DSX-NAR-001) were all already members of _INCIDENTAL_GAP_CODES from sibling fixtures — no new allow-list entries were needed"

requirements-completed: [REQ-P8-03, REQ-P8-05]

coverage:
  - id: D1
    description: "Three existing known-bad fixtures (interference-shared-budget, bayesian-continuous-monitoring, frequentist-uncontrolled-continuous) declare novelty_primacy_assessed: true with a non-blank evidence pointer, no other field changed"
    requirement: "REQ-P8-05"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::TestKnownBadCorpus::test_every_spec_blocks_only_on_its_target_defect_at_critical_threshold_points"
        status: pass
    human_judgment: false
  - id: D2
    description: "Corpus rewritten from family-prefix allow-list to per-fixture target-defect map (_TARGET_DEFECT_CODES + _classify_target_defect), proven against fabricated inputs"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::TestClassifyTargetDefectHelper (2 tests)"
        status: pass
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::TestKnownBadCorpus::test_incidental_allowlist_names_no_slugs_own_target_code"
        status: pass
    human_judgment: false
  - id: D3
    description: "triggering-dilution fixture pair committed: validates, clears plan/execute, declares the DSX-INT-030 pattern, and its measured ship-gate incidental gaps are all documented"
    requirement: "REQ-P8-03"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::TestKnownBadCorpus (full module, 15 tests)"
        status: pass
      - kind: other
        ref: "dsx gate ship --json against a fresh temp phase-dir: 5 HIGH findings, all pre-existing members of _INCIDENTAL_GAP_CODES"
        status: pass
    human_judgment: false

# Metrics
duration: ~40min
completed: 2026-08-12
status: complete
---

# Phase 8 Plan 2: Known-bad corpus safety pre-load Summary

**Rewrote the known-bad corpus's family-prefix guarantee into a per-fixture target-defect map, fixed four fixtures' dishonest stability declarations, and committed the triggering-dilution fixture pair DSX-INT-030 will be measured against.**

## Performance

- **Duration:** ~40 min
- **Completed:** 2026-08-12
- **Tasks:** 3 planned + 1 deviation task
- **Files modified:** 8 (5 fixture YAML/MD files created or edited, 3 test files edited)

## Accomplishments

- All five committed `examples/known-bad/` fixtures now declare `stability.novelty_primacy_assessed: true` with a non-blank `stability.evidence` pointer — none of them will trip `DSX-INT-040` as a second, undocumented defect once it ships (plan 08-05)
- `tests/test_known_bad_corpus.py`'s corpus guarantee is now a per-fixture `_TARGET_DEFECT_CODES` map (`slug -> {gate_point: code}`) instead of a family-prefix allow-list that could express at most one code per family — proven to fire against fabricated inputs, not just real fixtures
- Fourth known-bad fixture pair committed: `triggering-dilution-ANALYSIS-SPEC.yaml`/`POSTMORTEM.md`, encoding the additive-metric-on-eligible-population dilution pattern `DSX-INT-030` (plan 08-04) will catch, with its ship-gate incidental gaps measured from a real gate run rather than predicted

## Task Commits

Each task was committed atomically:

1. **Task 1: Declare the stability block honestly on all three existing known-bad fixtures** - `26c2992` (fix)
2. **Task 2: Replace the corpus's family-prefix guarantee with a per-fixture target-defect map** - `b03fe0a` (refactor)
3. **Task 3: Commit the triggering-dilution fixture pair and document its measured incidental gaps** - `e2cf266` (feat)
4. **Deviation: Declare honest stability on weak-identification-mmm too** - `23b053e` (fix)

**Plan metadata:** (final commit hash recorded after this SUMMARY is committed)

## Files Created/Modified

- `examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml` - new fourth known-bad fixture, full-shape clone declaring the DSX-INT-030 dilution pattern
- `examples/known-bad/triggering-dilution-POSTMORTEM.md` - its sibling post-mortem, names DSX-INT-030, cites Deng & Hu (2015) Formula (1)
- `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml` - stability.novelty_primacy_assessed false->true, evidence filled in
- `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` - same fix
- `examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml` - same fix
- `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` - same fix (deviation, see below)
- `tests/test_known_bad_corpus.py` - `_TARGET_DEFECT_CODES` + `_classify_target_defect()` replace `_TARGET_CODE_FAMILIES`/`_EXPECTED_PLAN_BLOCKERS`; three tests rewritten; `TestClassifyTargetDefectHelper` added
- `tests/test_frame_val.py` - `_EXPECTED_VAL_CODES` gained a `triggering-dilution-ANALYSIS-SPEC.yaml: set()` entry (deviation, see below)

## Decisions Made

- **`_TARGET_DEFECT_CODES` was not committed literally empty.** The plan's action text said to commit it empty with only a comment naming future additions, written against `08-CONTEXT.md`'s assumption that no `DSX-INT-*`/`DSX-VAL-*` code had yet shipped against any corpus fixture. Live-tree measurement showed `weak-identification-mmm -> DSX-VAL-040` already ships (Phase 7, plan 07-07) via the now-deleted `_EXPECTED_PLAN_BLOCKERS` dict. A literally empty map would have silently dropped that fixture's existing "must block at plan" guarantee — the map defaults absent entries to "clears cleanly," the opposite of what that fixture needs. Migrated the one entry instead.
- **`weak-identification-mmm`'s stability block was fixed too, beyond the plan's named three fixtures.** See Deviations below.
- **The classification helper takes the target map as a parameter, never reads the module constant directly** — the load-bearing design choice that makes the synthetic-input proof possible without touching the filesystem or the real gate, per the plan's own instruction.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug/stale plan assumption] `_TARGET_DEFECT_CODES` could not be committed empty**
- **Found during:** Task 2
- **Issue:** The plan instructed committing `_TARGET_DEFECT_CODES` empty. Measurement showed `weak-identification-mmm -> DSX-VAL-040` already ships in this milestone (Phase 7, plan 07-07), previously encoded via `_EXPECTED_PLAN_BLOCKERS`, which this plan's rewrite deletes. An empty map would have silently stopped enforcing that fixture's existing "must block dsx gate plan" guarantee.
- **Fix:** Migrated the one entry (`"weak-identification-mmm": {"plan": "DSX-VAL-040"}`) into `_TARGET_DEFECT_CODES`, with a comment explaining the migration and citing the same guarantee `_EXPECTED_PLAN_BLOCKERS` made.
- **Files modified:** `tests/test_known_bad_corpus.py`
- **Committed in:** `b03fe0a` (Task 2 commit)

**2. [Rule 3 - Blocking issue] `tests/test_frame_val.py` broke on the new fixture**
- **Found during:** Task 3, running the full suite after committing the new fixture
- **Issue:** `TestValFixtureMatrix::test_discovered_fixture_set_equals_the_expected_dictionarys_key_set` discovers every known-bad fixture by glob and requires a measured entry in `_EXPECTED_VAL_CODES`. The new `triggering-dilution-ANALYSIS-SPEC.yaml` tripped its loud-failure guard (by design — it exists precisely to catch an un-examined new fixture).
- **Fix:** Ran `dsx.frame.val.check()` against the loaded fixture directly, confirmed the empty result (`set()` — no `DSX-VAL-*` code fires, since `identification`/`dependence`/`units`/`sampling_frame`/`missingness`/`measurement` are all populated the same way the good fixture's are), and added `"triggering-dilution-ANALYSIS-SPEC.yaml": set()` with a measurement comment.
- **Files modified:** `tests/test_frame_val.py`
- **Verification:** `python3 -m unittest discover -s tests` exits 0 (421 tests)
- **Committed in:** `e2cf266` (Task 3 commit)

**3. [Rule 1 - Bug/stale plan assumption] `weak-identification-mmm` also violated the plan's own must_have truth**
- **Found during:** Final plan-level verification pass, checking `must_haves.truths`: "Every fixture under `examples/known-bad/` declares `stability.novelty_primacy_assessed` as `true`..."
- **Issue:** `08-CONTEXT.md`'s corrections block (correction 4) enumerated exactly three colliding fixtures, found by scanning the live tree at planning time. `weak-identification-mmm` (Phase 7's own fixture, plan 07-07) independently declared `novelty_primacy_assessed: false` with a blank `evidence` too — apparently not re-scanned during this phase's collision analysis. It would have identically collided with `DSX-INT-040` the moment plan 08-05 ships it.
- **Fix:** Applied Task 1's exact pattern: `stability.novelty_primacy_assessed` false->true, `stability.evidence` filled with a non-blank pointer. `stability.window` and every `identification.*` field (that fixture's own encoded `DSX-VAL-040` defect) are untouched — verified by `git diff --stat` (2 lines changed) and a grep for `identification:`/`strength:`/`constraint_source:` in the diff (no match).
- **Files modified:** `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml`
- **Verification:** `dsx validate` still exits 0; full suite still 421 tests, green
- **Committed in:** `23b053e`

**4. [Documentation, no code change] A second, live fragility risk recorded**
- **Found during:** Writing the deviation-3 fix, while re-measuring `weak-identification-mmm`'s `validity_frame.triggering` block for the stability edit
- **Observation:** `weak-identification-mmm` declares `analysis_population: eligible`, `dilution_adjusted: false`, and `metrics[0].type: sum` (additive) — three of `DSX-INT-030`'s structural conditions as `D-01` states them, literally. It escapes only because `expected_trigger_rate` is `1.0` (the whole eligible population is triggered by construction, a national weekly aggregate with no eligibility gate below full coverage), which mathematically means there is nothing to dilute — but `D-01`'s stated trigger condition does not name a `trigger_rate < 1.0` gate explicitly, even though this plan's own `triggering-dilution` fixture (`expected_trigger_rate: 0.41`) treats materiality as load-bearing.
- **Action:** Recorded as a second fragility-note bullet beside the existing one in `tests/test_known_bad_corpus.py`, flagged for plan 08-04's implementation to resolve (either the check gates on `trigger_rate < 1.0`, making this fixture safe by construction, or it does not, and 08-04 needs a `_TARGET_DEFECT_CODES` entry for it). Not fixed unilaterally — editing `weak-identification-mmm`'s triggering block would touch a Phase 7 fixture's own honestly-declared scenario for a risk that has not yet materialised into an actual gate finding.
- **Files modified:** `tests/test_known_bad_corpus.py` (comment only)
- **Committed in:** `23b053e`

---

**Total deviations:** 4 (2 auto-fixed bugs/stale-assumption corrections, 1 blocking-issue fix, 1 documentation-only forward flag)
**Impact on plan:** All four were necessary to keep the corpus's own stated guarantees true against live state, and to prevent the full suite going red. No scope creep beyond what the plan's own must_have truths and existing test invariants required.

## Issues Encountered

None beyond the deviations above.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `_TARGET_DEFECT_CODES` exists, is exercised by real fixtures and by the synthetic-proof `TestClassifyTargetDefectHelper`, and documents exactly which slug/gate-point entries plans 08-03 (`interference-shared-budget -> DSX-INT-010 at plan`), 08-04 (`triggering-dilution -> DSX-INT-030 at plan`) and a later Phase 9 plan (the two monitoring fixtures) must add — each a one-entry addition, not a test-suite redesign.
- `triggering-dilution-ANALYSIS-SPEC.yaml`/`POSTMORTEM.md` are committed and green at `plan`/`execute`; plan 08-04 has a real fixture to measure `DSX-INT-030` against the moment the code exists.
- No fixture in the corpus carries an unassessed novelty/primacy declaration; `DSX-INT-040` (plan 08-05) can ship without a second corpus rewrite.
- **Carried-forward risk for plan 08-04:** `weak-identification-mmm` satisfies three of `DSX-INT-030`'s structural conditions (additive metric, eligible population, `dilution_adjusted: false`) and escapes only via `expected_trigger_rate: 1.0`. Plan 08-04's implementer should check this fixture's actual `dsx gate plan` result once the check exists, not assume it is safe.

---
*Phase: 08-interference-triggering-stability-dsx-int*
*Completed: 2026-08-12*

## Self-Check: PASSED

All created/modified files confirmed present on disk (`examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml`, `examples/known-bad/triggering-dilution-POSTMORTEM.md`, `tests/test_known_bad_corpus.py`, `tests/test_frame_val.py`, `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml`). All four task commits confirmed in `git log` (`26c2992`, `b03fe0a`, `e2cf266`, `23b053e`).
