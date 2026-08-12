---
phase: 07-validity-frame-checks-dsx-val
plan: 07
subsystem: testing
tags: [dsx, validity-frame, marketing-mix-model, corpus-fixtures, ast-based-testing, citation-verification]

requires:
  - phase: 07-validity-frame-checks-dsx-val
    provides: All ten DSX-VAL-* codes shipped (plans 07-03 through 07-06), including DSX-VAL-040/041 (plan 07-05)
provides:
  - The fourth known-bad corpus fixture (examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml), opposite polarity from its three siblings
  - A named-exception resolution (_EXPECTED_PLAN_BLOCKERS) for the corpus test's blanket gate-clearance assertion
  - An AST-derived regression guard proving DSX-VAL-*'s citation/reference-value/test-marker/catalogue obligations independent of the build script
affects: [phase-verification, future-corpus-fixtures-whose-target-code-ships-in-phase]

tech-stack:
  added: []
  patterns:
    - "Named-exception dictionary (module-level constant + docstring) to narrow a blanket test assertion without deleting it, pairing the narrowing with a stronger positive assertion"
    - "AST-parsed function/code enumeration in tests, so a test's coverage list cannot silently drift from the module it tests"

key-files:
  created:
    - examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml
    - examples/known-bad/weak-identification-mmm-POSTMORTEM.md
  modified:
    - tests/test_known_bad_corpus.py
    - tests/test_frame_val.py

key-decisions:
  - "Corpus-conflict resolution: Option A (named exception dictionary _EXPECTED_PLAN_BLOCKERS in tests/test_known_bad_corpus.py) — pre-decided by the human before this plan ran; executed as specified."
  - "The new fixture's incidental ship-gate gaps (DSX-CLM-031, DSX-COH-031, DSX-MET-040, DSX-NAR-001, DSX-REP-030) were engineered to match the existing _INCIDENTAL_GAP_CODES set exactly, rather than adding new entries — verified by running dsx gate ship against the fixture and diffing its CRITICAL/HIGH findings against the existing allow-list before committing."
  - "design.kind: observational with design.identification: regression_adjustment (rather than design.kind: experiment) — MMM is not randomized data; regression_adjustment is classified 'weak' in dsx.spec.IDENTIFICATION_STRATEGIES, consistent with the encoded validity_frame.identification.strength: weak defect, and avoids DSX-CAU-011 (both required needs — covariates, sensitivity_analysis — are declared)."
  - "Citation for the post-mortem: Chan, D. & Perry, M. (2017), 'Challenges and Opportunities in Media Mix Modeling' (Google Inc.) — fetched and read the primary PDF in full during this session (network access was available via Bash/curl) rather than relying on training-data recall; author names, year, title and venue were confirmed directly against the document, and three passages (sections 4.1.1, 4.1.2, 4.2) were quoted from the document itself, not paraphrased from memory."

requirements-completed: [REQ-P7-05]

coverage:
  - id: D1
    description: "examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml exists, blocks dsx gate plan naming DSX-VAL-040, and clears dsx gate execute"
    requirement: "REQ-P7-05"
    verification:
      - kind: integration
        ref: "tests/test_frame_val.py#TestValGateIntegration.test_weak_identification_mmm_fixture_blocks_gate_plan_naming_val_040"
        status: pass
      - kind: integration
        ref: "tests/test_frame_val.py#TestValGateIntegration.test_weak_identification_mmm_fixture_clears_gate_execute"
        status: pass
    human_judgment: false
  - id: D2
    description: "The corpus's blanket plan/execute gate-clearance assertion is narrowed by a named exception (_EXPECTED_PLAN_BLOCKERS) that carries a positive counterpart, not deleted; glob discovery and the incidental-gap allow-list guard are preserved"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py#TestKnownBadCorpus.test_every_spec_passes_the_critical_threshold_gate_points"
        status: pass
      - kind: unit
        ref: "tests/test_known_bad_corpus.py#TestKnownBadCorpus.test_ship_gate_findings_are_all_documented_incidental_corpus_gaps"
        status: pass
      - kind: unit
        ref: "tests/test_known_bad_corpus.py#TestKnownBadCorpus.test_incidental_allowlist_names_no_target_family_code"
        status: pass
    human_judgment: false
  - id: D3
    description: "Every DSX-VAL-* code carries a Citation: line, a Reference value:/Structural criterion: line, and a test marker, proven by an AST-parsed test rather than a hand-written list; every emitted code appears in the rendered catalogue"
    requirement: "REQ-P7-05"
    verification:
      - kind: unit
        ref: "tests/test_frame_val.py#TestValCitationObligations.test_every_finding_emitting_function_has_citation_and_reference_value_lines"
        status: pass
      - kind: unit
        ref: "tests/test_frame_val.py#TestValCitationObligations.test_every_emitted_code_has_a_test_marker_under_tests"
        status: pass
      - kind: unit
        ref: "tests/test_frame_val.py#TestValCitationObligations.test_every_emitted_code_appears_in_the_rendered_catalogue"
        status: pass
      - kind: other
        ref: "python3 scripts/gen-finding-catalogue.py --check"
        status: pass
    human_judgment: false
  - id: D4
    description: "The post-mortem's source is a real, verified, primary/peer-reviewed publication describing weak identification in a marketing-mix model, and the two project-defined partitions plus the unverified citation locators are honestly disclosed rather than presented as published results"
    verification: []
    human_judgment: true
    rationale: "Whether a citation is genuinely admissible under D-05, and whether a docstring's honesty disclosure reads as adequate, are judgment calls this plan's own human-check step assigns to a human reader — see the 'Human Judgment Items' section below for exactly which files and passages to read."

# Metrics
duration: ~70min
completed: 2026-08-12
status: complete
---

# Phase 7 Plan 7: Weak-identification MMM fixture and corpus gate-conflict resolution Summary

**Fourth known-bad corpus fixture (opposite polarity: blocks `dsx gate plan` on `DSX-VAL-040`), a named-exception resolution to the corpus test's blanket gate-clearance assertion, and an AST-derived citation-obligation regression guard for the whole `DSX-VAL-*` family.**

## Performance

- **Duration:** ~70 min
- **Completed:** 2026-08-12T17:44:12Z
- **Tasks:** 2 (both complete)
- **Files modified:** 4 (2 created, 2 modified), across 2 commits

## Accomplishments

- Created `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` — a marketing-mix-model fixture whose sole encoded defect is `validity_frame.identification.strength: weak` paired with `constraint_source: none`, which is `DSX-VAL-040`'s exact trigger. `dsx gate plan` exits 1 naming `DSX-VAL-040`; `dsx gate execute` exits 0 (the `val` check is not in that gate profile); `dsx validate` exits 0. Confirmed programmatically that the fixture's `DSX-VAL-*` code set is exactly `{"DSX-VAL-040"}` — every other validity-frame sub-block is clean.
- Wrote the paired `POSTMORTEM.md`, citing Chan, D. & Perry, M. (2017), "Challenges and Opportunities in Media Mix Modeling" (Google Inc.) — a primary technical report fetched and read in full during this session (author, year, title and venue confirmed directly against the document; three specific passages quoted, not paraphrased from training-data recall).
- Resolved the corpus-test conflict per this plan's pre-recorded decision (Option A): added `_EXPECTED_PLAN_BLOCKERS` to `tests/test_known_bad_corpus.py` mapping the new fixture to `DSX-VAL-040`, narrowed `test_every_spec_passes_the_critical_threshold_gate_points` and `test_ship_gate_findings_are_all_documented_incidental_corpus_gaps` to carry a positive counterpart for listed fixtures, and added the exact code `DSX-VAL-040` (not the family prefix) to `_TARGET_CODE_FAMILIES` — verified the plan 07-05 `DSX-VAL-041` allow-list entry stays legal.
- Added the fixture to `tests/test_frame_val.py`'s `_EXPECTED_VAL_CODES` matrix and a new `TestValGateIntegration` class proving ROADMAP Success Criterion 1 directly against the committed fixture (not a synthetic clone).
- Added `TestValCitationObligations` to `tests/test_frame_val.py`: AST-parses `dsx/frame/val.py` to derive (never hand-list) every function that calls `report.add(...)`, then asserts each carries a `Citation:` line and a `Reference value:`/`Structural criterion:` line, that every emitted code has a `# D-05: <CODE>` test marker under `tests/`, and that every emitted code appears in `references/finding-codes.md`.

## Task Commits

1. **Task 1: Create the weak-identification fixture and its post-mortem, and resolve the corpus test conflict in one commit** - `581e20e` (feat)
2. **Task 2: Prove the phase's citation and coverage obligations are met, by command rather than by inspection** - `a8121a1` (test)

_Note: both tasks' changes to `tests/test_frame_val.py` were split into their respective commits (Task 1's fixture-matrix entry and `TestValGateIntegration`; Task 2's `TestValCitationObligations`) so each commit matches its task's own `<files>` declaration and acceptance criteria exactly — verified `git show --stat 581e20e` names all four Task-1 files in that one commit._

## Files Created/Modified

- `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` - The fourth corpus fixture; sole defect `validity_frame.identification` (weak/none)
- `examples/known-bad/weak-identification-mmm-POSTMORTEM.md` - Paired post-mortem citing Chan & Perry (2017)
- `tests/test_known_bad_corpus.py` - `_EXPECTED_PLAN_BLOCKERS`, narrowed gate/ship assertions, `_TARGET_CODE_FAMILIES` gains the exact code `DSX-VAL-040`
- `tests/test_frame_val.py` - `_EXPECTED_VAL_CODES` entry, `TestValGateIntegration`, `TestValCitationObligations`

## Decisions Made

See `key-decisions` in the frontmatter above. In brief: the corpus-conflict resolution (Option A) was pre-decided by the human before this plan ran and executed as specified; the fixture's design/identification shape and its incidental ship-gate gaps were chosen to reuse the existing `_INCIDENTAL_GAP_CODES` set exactly rather than expanding it; the citation was independently verified against the primary document rather than taken from training-data recall, because network access via `Bash`/`curl` was available in this environment.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Corrected the plan's own acceptance-criteria import path**
- **Found during:** Task 1 verification
- **Issue:** The plan's acceptance criteria snippet reads `from dsx.spec import load`, but `load` is defined in `dsx.loader`, not `dsx.spec` (`dsx.spec` has no `load` export). Running the snippet as written raises `ImportError`.
- **Fix:** Ran the equivalent check with the correct import (`from dsx.loader import load`), which is what every other fixture-loading test in this repository already uses (`tests/test_frame_val.py`, `tests/test_known_bad_corpus.py`). No source or test code was changed for this — it is a defect in the plan's own snippet, not in the codebase.
- **Files modified:** None (verification-only; documented here per this plan's own precedent for plan-text defects, e.g. the `IntEnum.__str__` note in this plan's `<project_constraints>`).
- **Verification:** `python3 -c "from dsx.frame import val; from dsx.loader import load; r = val.check(load('examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml')); assert {x.code for x in r.findings if x.code.startswith('DSX-VAL')} == {'DSX-VAL-040'}"` exits 0.
- **Committed in:** N/A (no code change; documented as a deviation because the plan's acceptance criterion, taken literally, would fail for a reason unrelated to the fixture's correctness).

---

**Total deviations:** 1 auto-fixed (1 plan-text defect, not a code defect)
**Impact on plan:** No scope creep. The underlying assertion (the fixture's `DSX-VAL-*` code set is exactly `{"DSX-VAL-040"}`) was proven true; only the plan's own import statement needed correcting.

## Issues Encountered

None beyond the deviation above. The citation-verification step (see Human Judgment Items) required network access via `Bash`/`curl`, which was available in this environment; the primary PDF was fetched, read in full via the `Read` tool's PDF support, and its metadata cross-checked against the hosting page's `citation_*` meta tags before it was used.

## Human Judgment Items

This plan carries two things no test can settle, per its own instructions. Both are ready for the verification step to check directly.

**1. Are the two project-defined partitions disclosed as project-defined in the shipped docstrings?**

Read these two docstrings in `dsx/frame/val.py`:
- `_check_estimand_completeness` (lines ~560-585): states the five-field estimand decomposition (`quantity`, `population`, `contrast`, `time_window`, `falsifier`) is "this project's own grouping, adopted for decidability, not asserted as a published result."
- `_check_identification` (lines ~903-937): states the four-against-one partition of `CONSTRAINT_SOURCES` into parameter-scale-informing members and `none` "is project-defined" and that "no published source draws it."

Both disclosures were already present in the codebase before this plan ran (shipped by plan 07-03 and plan 07-05 respectively) — this plan did not need to add or modify either docstring, only rely on them being accurate, which the `TestValCitationObligations` regex assertions confirm structurally (a `Citation:` line and a `Reference value:`/`Structural criterion:` line exist) without confirming the disclosure's honesty in prose, which is exactly the judgment call being handed here.

**2. Are the unverified citation locators labelled unverified rather than invented?**

Read these docstrings/module-level citation constants in `dsx/frame/val.py` and `dsx/mathx.py`:
- `dsx/mathx.py`'s `design_effect` (and `dsx/frame/val.py`'s `_UNIT_TRIAD_CITATION`): "The section number inside Kish for the formula itself is UNVERIFIED — the page numbers above were confirmed, the section number was not. Do not invent one."
- `dsx/frame/val.py`'s `_DEPENDENCE_CITATION` (used by `_check_dependence`): "The exact section locator inside Cameron and Miller and the exact chapter locator inside Gelman and Hill are both UNVERIFIED — author, year, title and venue were confirmed for each; the internal locators were not."
- `dsx/frame/val.py`'s `_IDENTIFICATION_CITATION` (used by `_check_identification`): "Whether the typeset MDPI journal version uses the same section numbers as the arXiv final version is UNVERIFIED."

All three were already present before this plan ran. **New in this plan:** the weak-identification-mmm `POSTMORTEM.md`'s citation to Chan & Perry (2017) is presented as fully verified, not as an unverified locator — the primary PDF was fetched and read in full during this session (network access via `Bash`/`curl` was available), and the specific section numbers cited (4.1.1, 4.1.2, 4.2) were confirmed by direct reading of the document's own section headings, not inferred or guessed. A human should still spot-check the postmortem's "Source" section against this claim: it names the exact fetch URLs used and states the verification was performed "during this phase," which is the honest and checkable form this plan's own instructions require.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- All five plan-07 success criteria and all nine `REQ-P7-*` requirements now have code, a citing test, and (for `REQ-P7-05`) a corpus fixture proving the roadmap's own success criterion end to end.
- `dsx/checks/design.py` remains unmodified across the whole phase (confirmed via `git status --short` showing no change to that file, and via `tests/test_frame_val.py`'s `test_design_checks_py_content_is_unmodified_since_phase_start` passing).
- The corpus now documents, for the first time, a fixture whose target code ships in the same phase as the fixture — future phases (8 onward) that add fixtures for not-yet-shipped codes should watch for this same conflict and can reuse `_EXPECTED_PLAN_BLOCKERS` as the precedent.
- No blockers for phase verification. The two Human Judgment Items above are the only items this plan hands to a human rather than a test.

## Requirements Coverage (nine `REQ-P7-*` identifiers)

| Requirement | Satisfied by (code) | Satisfied by (test) | Command that proves it |
|---|---|---|---|
| REQ-P7-01 | `dsx/frame/val.py::_check_estimand_completeness` (DSX-VAL-010), `::_check_estimand_falsifiability` (DSX-VAL-011) | `tests/test_frame_val.py::TestValEstimand` | `python3 -m unittest tests.test_frame_val.TestValEstimand -v` |
| REQ-P7-02 | `dsx/frame/val.py::_check_unit_triad` (DSX-VAL-020), `dsx/mathx.py::design_effect` | `tests/test_frame_val.py::TestValUnits.test_units_020_detail_carries_the_deff_formula_and_illustration_wording` | `python3 -m unittest tests.test_frame_val.TestValUnits -v` |
| REQ-P7-03 | `dsx/frame/val.py::_check_unit_triad` vs. `dsx/checks/design.py::_check_units` (unmodified) | `tests/test_frame_val.py::TestValExpUnitsDisjointness` | `python3 -m unittest tests.test_frame_val.TestValExpUnitsDisjointness -v` |
| REQ-P7-04 | `dsx/frame/val.py::_check_dependence` (DSX-VAL-030), `dsx.spec.DEPENDENCE_ADMISSIBLE_METHODS`/`VARIANCE_ADJUSTMENTS` | `tests/test_frame_val.py::TestValDependenceIdentification` | `python3 -m unittest tests.test_frame_val.TestValDependenceIdentification -v` |
| REQ-P7-05 | `dsx/frame/val.py::_check_identification` (DSX-VAL-040/041) | `tests/test_frame_val.py::TestValDependenceIdentification`, `::TestValGateSeverity`, `::TestValGateIntegration` (this plan) | `python3 -m unittest tests.test_frame_val.TestValGateIntegration tests.test_frame_val.TestValGateSeverity -v`; `python3 -m dsx.cli gate plan --spec examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` |
| REQ-P7-06 | `dsx/frame/val.py::_check_sampling_frame` (DSX-VAL-050) | `tests/test_frame_val.py::TestValSamplingMissingnessMeasurement` (claim-population/selection-risk tests) | `python3 -m unittest tests.test_frame_val.TestValSamplingMissingnessMeasurement -v` |
| REQ-P7-07 | `dsx/frame/val.py::_check_missingness` (DSX-VAL-060), `_MISSINGNESS_METHOD_VALIDITY` | `tests/test_frame_val.py::TestValSamplingMissingnessMeasurement` (missingness tests) | `python3 -m unittest tests.test_frame_val.TestValSamplingMissingnessMeasurement -v` |
| REQ-P7-08 | `dsx/frame/val.py::_check_measurement` (DSX-VAL-070); second clause deliberately unadjudicated per D-06 (see the comment directly above `_check_measurement`) | `tests/test_frame_val.py::TestValSamplingMissingnessMeasurement` (measurement tests) | `python3 -m unittest tests.test_frame_val.TestValSamplingMissingnessMeasurement -v` |
| REQ-P7-09 | `dsx/frame/val.py` (no code path reads `inference.paradigm`, D-11) | `tests/test_frame_boundary.py::TestFrameParadigmReadBoundary` | `python3 -m unittest tests.test_frame_boundary -v` |

No checkbox in `.planning/REQUIREMENTS.md` or `.planning/ROADMAP.md` was changed by this plan — per this project's working agreement, marking a requirement complete is the verification step's job.

## Observed Command Output

```
$ python3 -m unittest discover -s tests
warning: DSX-SPEC-070 declared twice with different text
warning: DSX-VAL-021 declared twice with different text
warning: DSX-VAL-060 declared twice with different text
warning: DSX-COH-030 declared twice with different text
...
----------------------------------------------------------------------
Ran 419 tests in 3.157s

OK (skipped=2)
```

```
$ python3 scripts/gen-finding-catalogue.py --check
warning: DSX-COH-030 declared twice with different text
warning: DSX-SPEC-070 declared twice with different text
warning: DSX-VAL-021 declared twice with different text
warning: DSX-VAL-060 declared twice with different text
finding catalogue is current
```
(The `declared twice with different text` warnings are pre-existing legacy-code duplicates unrelated to this plan's changes — none name a `DSX-VAL-*` code this plan touched, and the catalogue itself is confirmed current with exit 0.)

```
$ python3 -m dsx.cli gate plan --spec examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml
... [CRITICAL] DSX-VAL-040  weak identification declared with no constraint ...
gate:plan: BLOCK (blocking at CRITICAL) — CRITICAL=1 HIGH=1 MEDIUM=2 LOW=0 INFO=1
$ echo $?
1
```

```
$ python3 -m dsx.cli gate execute --spec examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml
gate:execute: PASS (blocking at CRITICAL) — CRITICAL=0 HIGH=1 MEDIUM=1 LOW=1 INFO=1
$ echo $?
0
```

Baseline gate commands, confirmed unchanged:

| Command | Exit |
|---|---|
| `dsx gate plan/execute/verify/ship --spec examples/good-ANALYSIS-SPEC.yaml` | 0 / 0 / 0 / 0 |
| `dsx gate plan --spec examples/bad-ANALYSIS-SPEC.yaml` | 1 |
| `dsx gate plan --spec templates/ANALYSIS-SPEC.yaml` | 0 |
| `dsx gate ship --spec templates/ANALYSIS-SPEC.yaml` | 1 |

---
*Phase: 07-validity-frame-checks-dsx-val*
*Completed: 2026-08-12*

## Self-Check: PASSED

- FOUND: examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml
- FOUND: examples/known-bad/weak-identification-mmm-POSTMORTEM.md
- FOUND: tests/test_known_bad_corpus.py
- FOUND: tests/test_frame_val.py
- FOUND: 581e20e (feat(07-07): add weak-identification-mmm fixture and resolve corpus gate conflict)
- FOUND: a8121a1 (test(07-07): add AST-derived citation-obligation regression guard for DSX-VAL-*)
