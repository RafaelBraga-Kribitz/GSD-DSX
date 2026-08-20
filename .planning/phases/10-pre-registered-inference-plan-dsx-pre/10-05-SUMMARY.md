---
phase: 10-pre-registered-inference-plan-dsx-pre
plan: 05
subsystem: testing
tags: [known-bad-corpus, fixture, post-mortem, dsx-pre, citation]

# Dependency graph
requires:
  - phase: 10-pre-registered-inference-plan-dsx-pre (plan 02)
    provides: "DSX-PRE-010/DSX-PRE-030 findings in dsx/frame/prereg.py, PREREG_FACTS registry"
  - phase: 10-pre-registered-inference-plan-dsx-pre (plan 04)
    provides: "prereg registered in GATE_PROFILES[\"verify\"]/[\"ship\"] only; tests/_trail_seed.py::seed_plan_header"
provides:
  - "examples/known-bad/post-hoc-procedure-switch-ANALYSIS-SPEC.yaml — a committed fixture whose substitution (fishers_exact for a declared two_proportion_z branch) is strictly more conservative and still blocks DSX-PRE-030, proving REQ-P10-04's no-merit-consultation claim by fixture rather than by a second finding code"
  - "examples/known-bad/post-hoc-procedure-switch-POSTMORTEM.md — the two-source argument (Gelman & Loken 2014 p.463; Simmons, Nelson & Simonsohn 2011 p.1365) for why a more-conservative substitution is still a new researcher degree of freedom"
  - "tests/test_known_bad_corpus.py: _TARGET_DEFECT_CODES[\"post-hoc-procedure-switch\"] = {\"verify\": \"DSX-PRE-030\"}, _EXPECTED_CAUGHT_DEFECTS[\"post-hoc-procedure-switch\"] = frozenset()"
  - "tests/test_known_bad_corpus.py::test_post_hoc_procedure_switch_fixture_blocks_verify_and_ship_naming_pre_030 — dedicated verify/ship coverage the generic corpus test cannot reach, asserting both branch labels appear in the finding detail and no DSX-PRE- code fires at plan/execute"
  - "tests/test_frame_val.py: _EXPECTED_VAL_CODES[\"post-hoc-procedure-switch-ANALYSIS-SPEC.yaml\"] = set() (Rule 1 fix, not in this plan's declared files_modified)"
affects: [10-06-dsx-pre]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A verify-and-ship-only fixture's ANALYSIS-SPEC keeps design/analysis power inputs measured against dsx.mathx.sample_size_two_proportions rather than copied from a sibling fixture — an under-powered planned_n_per_arm fires DSX-EXP-006 (CRITICAL) at plan even when the fixture's own target defect lives entirely in a family absent from the plan gate profile"
    - "A verify/ship-only fixture must avoid any field that resolves to a file relative to the fixture's own directory (narrative.path, reproducibility.entrypoint, data[].profile_path) — the corpus harness gates every fixture from a fresh tempfile.TemporaryDirectory(), so a present-but-unresolvable path fires a different, undocumented finding code (DSX-NAR-010, DSX-REP-031, DSX-DQ-001 CRITICAL) than an absent field's already-documented one (DSX-NAR-001, DSX-REP-030); omitting the field entirely is the safe pattern every sibling fixture already uses"

key-files:
  created:
    - examples/known-bad/post-hoc-procedure-switch-ANALYSIS-SPEC.yaml
    - examples/known-bad/post-hoc-procedure-switch-POSTMORTEM.md
  modified:
    - tests/test_known_bad_corpus.py
    - tests/test_frame_val.py

key-decisions:
  - "The fixture keeps design.data[].assertions (and data[].profile_path) unset entirely — data.py's DSX-DQ-001 is CRITICAL and registered at execute, and any assertions block with an unresolvable profile_path would have blocked dsx gate execute, breaking the corpus's exit-0 guarantee at both CRITICAL-threshold points."
  - "planned_n_per_arm raised from an initial 5,200 to 7,400 after measuring dsx.mathx.sample_size_two_proportions(0.24, 0.02, 0.05, 0.80) == 7,358 — an underpowered design fires DSX-EXP-006 (CRITICAL) at plan, which would have broken the fixture's required exit-0 behaviour at that gate point; not caught by re-reading the plan, only by running the real gate."
  - "narrative:, reproducibility: and visuals: blocks are omitted entirely rather than populated with good-ANALYSIS-SPEC.yaml's values verbatim, because those values only resolve relative to examples/ (the good fixture's own directory) and the corpus harness always gates from a fresh temporary directory — omission produces the already-documented DSX-NAR-001/DSX-REP-030 incidental gaps instead of new, undocumented DSX-NAR-010/DSX-REP-031 findings."
  - "analysis.test is set to the literal fishers_exact (not the stats-vocabulary spelling fisher_exact), matching the exact term tests/test_frame_prereg.py already established for this phase's synthetic no-merit-consultation specs. This produces one incidental DSX-STA-041 (HIGH) at verify/ship — already a member of _INCIDENTAL_GAP_CODES from the bayesian-continuous-monitoring fixture — rather than an undocumented code."

requirements-completed: [REQ-P10-03, REQ-P10-04]

coverage:
  - id: D1
    description: "A committed known-bad fixture whose substitution (fishers_exact for a declared two_proportion_z branch) is strictly more conservative still clears dsx gate plan/execute and blocks dsx gate verify/ship naming DSX-PRE-030 among CRITICAL findings, with no DSX-PRE-010 or DSX-PRE-020 finding present."
    requirement: "REQ-P10-04"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py#test_post_hoc_procedure_switch_fixture_blocks_verify_and_ship_naming_pre_030"
        status: pass
      - kind: unit
        ref: "tests/test_known_bad_corpus.py#test_every_spec_blocks_only_on_its_target_defect_at_critical_threshold_points"
        status: pass
      - kind: other
        ref: "python bin/dsx validate --spec examples/known-bad/post-hoc-procedure-switch-ANALYSIS-SPEC.yaml (exit 0)"
        status: pass
    human_judgment: false
  - id: D2
    description: "The fixture is registered in the per-gate-point _TARGET_DEFECT_CODES map and carries the empty _EXPECTED_CAUGHT_DEFECTS entry the corpus-completeness test requires; no DSX-PRE- code is in _INCIDENTAL_GAP_CODES."
    requirement: "REQ-P10-03"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py#test_expected_caught_defects_keys_match_the_corpus_on_disk"
        status: pass
      - kind: unit
        ref: "tests/test_known_bad_corpus.py#test_incidental_allowlist_names_no_slugs_own_target_code"
        status: pass
      - kind: other
        ref: "python -c \"import tests.test_known_bad_corpus as m; print(m._TARGET_DEFECT_CODES['post-hoc-procedure-switch'])\" prints {'verify': 'DSX-PRE-030'}"
        status: pass
    human_judgment: false
  - id: D3
    description: "The post-mortem argues the case from the two phase-verified sources at their verified locators, names DSX-PRE-030 as the catch, and states the Gelman & Loken article carries no numbered sections, tables or theorems."
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py#test_every_postmortem_names_a_catch_attribution_finding_code"
        status: pass
      - kind: other
        ref: "grep for DSX-PRE-030, Gelman, Simmons, 10.1177/0956797611417632, and the no-numbered-structure sentence in the postmortem"
        status: pass
    human_judgment: false
  - id: D4
    description: "Full suite green, sh scripts/check.sh passes, finding catalogue current — no assertion weakened."
    verification:
      - kind: other
        ref: "python -m unittest discover -s tests -q"
        status: pass
      - kind: other
        ref: "sh scripts/check.sh"
        status: pass
      - kind: other
        ref: "python scripts/gen-finding-catalogue.py --check"
        status: pass
    human_judgment: false

# Metrics
duration: ~35min
completed: 2026-08-20
status: complete
---

# Phase 10 Plan 05: The post-hoc-procedure-switch known-bad fixture pair Summary

**A new committed known-bad fixture whose executed procedure (`fishers_exact`) is strictly more conservative than the branch its pre-registered fallback rule selects (`two_proportion_z`) still blocks `dsx gate verify`/`ship` naming `DSX-PRE-030` — the first fixture in this corpus to prove REQ-P10-04's no-merit-consultation claim against a real gate run rather than a synthetic report, with a dedicated test covering the verify/ship-only points the generic corpus test cannot reach.**

## Performance

- **Duration:** ~35 min
- **Completed:** 2026-08-20
- **Tasks:** 2
- **Files modified:** 4 (2 created: the fixture pair; 2 modified: `tests/test_known_bad_corpus.py`, `tests/test_frame_val.py`)

## Accomplishments

- `examples/known-bad/post-hoc-procedure-switch-ANALYSIS-SPEC.yaml`: a full-shape, structurally clean fixture (`dsx validate` exits 0 with zero findings at every severity) declaring a fallback rule (`comparisons_looked_at > 4 -> two_proportion_z, Holm adjustment across the comparison family`) that resolves cleanly against `results.comparisons_looked_at: 5`, and an executed `analysis.test: fishers_exact` that differs from the resolved branch. Clears `dsx gate plan`/`execute` (both exit 0, verified against a fresh temporary phase directory), blocks `dsx gate verify`/`ship` (both exit 1) naming `DSX-PRE-030` as the sole CRITICAL finding, with the finding's `detail` naming both `two_proportion_z` and `fishers_exact` verbatim.
- `examples/known-bad/post-hoc-procedure-switch-POSTMORTEM.md`: narrates the post-hoc switch in plain domain language, then argues from the two sources verified for this phase — Gelman & Loken (2014) p.463 (a p-value requires the same-analysis-under-different-data claim, which a post-hoc choice breaks) and Simmons, Nelson & Simonsohn (2011) p.1365 (the substitution is itself a new researcher degree of freedom, unrepaired by choosing the "stricter" option) — and cites the two verified prevalence figures (Claesen et al. 2021, Goldacre et al. 2019) as context only, never as a property of this fixture's specific defect.
- `tests/test_known_bad_corpus.py`: `_TARGET_DEFECT_CODES` gains `"post-hoc-procedure-switch": {"verify": "DSX-PRE-030"}`; `_EXPECTED_CAUGHT_DEFECTS` gains the corpus-completeness key with an explanatory comment; new dedicated test `test_post_hoc_procedure_switch_fixture_blocks_verify_and_ship_naming_pre_030` proves verify/ship both block naming `DSX-PRE-030` with both branch labels present in the (whitespace-normalized) detail text, and that `plan`/`execute` produce no `DSX-PRE-` finding at all, `subTest`-ed over the gate point.
- `tests/test_frame_val.py` (Rule 1 fix, discovered by running the full suite, not named in this plan): `_EXPECTED_VAL_CODES` gains the measured empty-set entry for the new fixture — its own corpus-completeness guard globs `examples/known-bad/` independently of `test_known_bad_corpus.py` and failed loudly on the undocumented fixture.

## Task Commits

Each task was committed atomically:

1. **Task 1: The post-hoc-procedure-switch fixture pair** - `14ddafc` (feat)
2. **Task 2: Corpus registration and the dedicated verify-and-ship test** - `43f4c16` (test)

_No TDD RED/GREEN split — Task 2 (`tdd="true"`) was implemented with behavior and tests landing together, verified green before commit, matching the pattern established in plans 01-04._

## Files Created/Modified

- `examples/known-bad/post-hoc-procedure-switch-ANALYSIS-SPEC.yaml` - New fixture: pre-registered fallback rule resolving to `two_proportion_z`, executed `fishers_exact`
- `examples/known-bad/post-hoc-procedure-switch-POSTMORTEM.md` - New post-mortem arguing the no-merit-repair case from Gelman & Loken (2014) and Simmons, Nelson & Simonsohn (2011)
- `tests/test_known_bad_corpus.py` - `_TARGET_DEFECT_CODES` and `_EXPECTED_CAUGHT_DEFECTS` entries; new dedicated test
- `tests/test_frame_val.py` - `_EXPECTED_VAL_CODES` measured empty-set entry for the new fixture (Rule 1)

## Decisions Made

- **`data[].assertions`/`profile_path` omitted entirely.** `dsx/checks/dq.py::DSX-DQ-001` is CRITICAL and registered at `execute`; any assertions block whose `profile_path` cannot resolve from a fresh temporary phase directory (which every known-bad fixture is gated from) would have blocked `dsx gate execute`, breaking this fixture's required exit-0 guarantee at that CRITICAL-threshold point. No sibling fixture in the corpus declares assertions on a data source either — confirmed by reading `frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml` before writing this one.
- **`planned_n_per_arm` raised from an initial 5,200 to 7,400**, after `dsx gate plan` against the first draft fired `DSX-EXP-006` (CRITICAL, underpowered design) — measured `dsx.mathx.sample_size_two_proportions(0.24, 0.02, 0.05, 0.80) == 7,358` and set the design's sample size above that. Found by running the real gate, not by re-reading the plan; the plan's own read_first list did not name this check.
- **`narrative:`, `reproducibility:` and `visuals:` blocks omitted entirely**, rather than cloned verbatim from `good-ANALYSIS-SPEC.yaml` as the plan's literal "full-shape clone" language might suggest. Good's values for those blocks (`good-NARRATIVE.md`, `analysis/activation_readout.py`, `figures/*.svg`) only resolve relative to `examples/`, the good fixture's own directory — the corpus harness (`tests/test_known_bad_corpus.py::_gate_findings`) always gates from a fresh `tempfile.TemporaryDirectory()`, so keeping those paths verbatim would have produced *unresolvable-path* findings (`DSX-NAR-010`, `DSX-REP-031`), which are **not** in `_INCIDENTAL_GAP_CODES`, rather than the already-documented *missing-field* findings (`DSX-NAR-001`, `DSX-REP-030`) every sibling fixture already produces by omitting the same blocks. Confirmed by reading `dsx/checks/narrative.py` and `dsx/checks/repro.py` directly, then verifying the actual finding set against a real `dsx gate verify` run.
- **`analysis.test: fishers_exact`, matching the plan's literal instruction and `tests/test_frame_prereg.py`'s existing convention for this phase's synthetic no-merit specs**, rather than the stats-vocabulary canonical spelling `fisher_exact`. This produces one incidental `DSX-STA-041` (HIGH) at verify/ship — already a documented member of `_INCIDENTAL_GAP_CODES` (measured against the `bayesian-continuous-monitoring` fixture) — confirmed by reading `dsx/checks/stats.py::recommend_test` and running the real gate against the drafted fixture before committing.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] `dsx gate plan` blocked on `DSX-EXP-006` (underpowered design) in the first draft**
- **Found during:** Task 1, verifying the acceptance criterion "`dsx gate plan` exits 0" against the drafted fixture
- **Issue:** `planned_n_per_arm: 5,200` was underpowered for the declared `baseline_rate: 0.24`, `mde: 0.02`, `alpha: 0.05`, `power: 0.80` — `dsx/checks/design.py`'s power check fired `DSX-EXP-006` at CRITICAL, blocking the gate point this fixture is required to clear cleanly.
- **Fix:** Measured the required sample size directly (`dsx.mathx.sample_size_two_proportions(0.24, 0.02, 0.05, 0.80) == 7,358`) and raised `design.planned_n_per_arm` to 7,400, with `analysis.n_per_group`/`results.observed_n` updated to match.
- **Files modified:** `examples/known-bad/post-hoc-procedure-switch-ANALYSIS-SPEC.yaml`
- **Verification:** `dsx gate plan` now exits 0 with zero CRITICAL findings against a fresh temporary phase directory
- **Committed in:** `14ddafc` (Task 1)

**2. [Rule 1 - Bug] `tests/test_frame_val.py`'s own corpus-completeness guard, not named in this plan, failed on the new fixture**
- **Found during:** Task 2, running `python -m unittest discover -s tests -q` after registering the fixture in `tests/test_known_bad_corpus.py`
- **Issue:** `tests/test_frame_val.py::TestValFixtureMatrix::test_discovered_fixture_set_equals_the_expected_dictionarys_key_set` globs `examples/known-bad/` independently and requires every discovered fixture to have an entry in its own `_EXPECTED_VAL_CODES` map (measured `DSX-VAL-*` codes, never guessed). The new fixture had no entry.
- **Fix:** Ran `dsx.frame.val.check()` against the loaded fixture (measured: empty set — every `validity_frame` sub-block is clean), added `"post-hoc-procedure-switch-ANALYSIS-SPEC.yaml": set()` with a comment following the module's existing measured-value convention.
- **Files modified:** `tests/test_frame_val.py`
- **Verification:** `python -m unittest tests.test_frame_val -q` and the full suite both pass; the measured value (not a guess) matches `dsx.frame.val.check()`'s real output
- **Committed in:** `43f4c16` (Task 2)

---

**Total deviations:** 2 auto-fixed (1 blocking underpowered-design fix, 1 bug in an additional corpus-completeness guard the plan's read_first list did not name). Both are mechanical — measured values applied where the plan required a value to be chosen, and a pre-existing invariant repaired rather than weakened. No `DSX-PRE-*` code added to `_INCIDENTAL_GAP_CODES`, no corpus assertion relaxed.
**Impact on plan:** No scope creep, no architectural change. Both fixes are exactly the class the plan's own "not asserted to be exhaustive" caveat (inherited from plan 04's precedent) anticipates.

## Issues Encountered

None beyond the two auto-fixed items above, both resolved on the first iteration.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- The corpus now carries a second verify-and-ship-only target-defect entry (`weak-identification-mmm`'s `DSX-INT-030` was the first), proving the per-gate-point `_TARGET_DEFECT_CODES` shape generalises cleanly to a second family.
- REQ-P10-04 (no-merit-consultation) is now proven by a committed fixture and a real gate run, not merely by the synthetic unit tests plan 02 already carries (`TestNoMeritConsultation`) — the two are complementary, not redundant: the unit tests prove the property in isolation, this fixture proves it survives the full gate pipeline.
- Full suite green at 622/622 (up from 621 at fork — 1 new test), `sh scripts/check.sh` passes printing `all checks passed`, `python scripts/gen-finding-catalogue.py --check` exits 0 (only the pre-existing, not-mine-to-fix `DSX-SPEC-070`/`DSX-VAL-021`/`DSX-VAL-060`/`DSX-COH-030`/`DSX-PAR-002` duplicate-text warnings remain, per this plan's prior-wave context).
- No blockers. Plan 10-06 (README/brief citation work, running in parallel in a sibling worktree) touches none of this plan's files.

## Self-Check: PASSED

- FOUND: examples/known-bad/post-hoc-procedure-switch-ANALYSIS-SPEC.yaml
- FOUND: examples/known-bad/post-hoc-procedure-switch-POSTMORTEM.md
- FOUND: tests/test_known_bad_corpus.py (_TARGET_DEFECT_CODES, _EXPECTED_CAUGHT_DEFECTS, dedicated test)
- FOUND: tests/test_frame_val.py (_EXPECTED_VAL_CODES entry)
- FOUND: 14ddafc (Task 1 commit)
- FOUND: 43f4c16 (Task 2 commit)

---
*Phase: 10-pre-registered-inference-plan-dsx-pre*
*Completed: 2026-08-20*
