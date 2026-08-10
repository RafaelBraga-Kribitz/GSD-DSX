---
phase: 06-contract-extension-decision-record-paradigm-manifest
plan: 01
subsystem: contract
tags: [yaml-parser, closed-vocabulary, dsx-spec, tdd]

# Dependency graph
requires: []
provides:
  - "dsx/loader.py `_NULL` no longer treats the literal `none` as a null token — matches PyYAML/YAML 1.1 semantics"
  - "PEEKING_POLICIES gains `uncontrolled_continuous`, distinct from `always_valid`"
  - "Ten new closed vocabularies in dsx/spec.py: IDENTIFICATION_STRENGTHS, CONSTRAINT_SOURCES, DEPENDENCE_STRUCTURES, INTERFERENCE_RISKS, INTERFERENCE_MITIGATIONS, MISSINGNESS_MECHANISMS, ANALYSIS_POPULATIONS, DECLARATION_POINTS, PARADIGMS, PARADIGM_JUSTIFICATIONS"
  - "_VOCABULARIES registry — single source behind describe_vocabulary(), dict-backed vocabularies dump as key-sorted description dicts, set-backed ones as sorted lists"
affects: [06-02, 06-03, 06-04, 06-05, 06-06, 06-07, 06-08, 06-09, 06-10]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Closed vocabulary = name->description dict, registered once in _VOCABULARIES, dumped generically by describe_vocabulary() — the object each shape validator imports is the exact object dumped (D-05)"
    - "TDD RED/GREEN per behavior-adding task: failing test commit, then minimal-diff implementation commit"

key-files:
  created: []
  modified:
    - dsx/loader.py
    - dsx/spec.py
    - tests/test_dsx.py

key-decisions:
  - "PEEKING_POLICIES.uncontrolled_continuous ships in Phase 6 (not deferred to Phase 9) per CONTEXT.md D-01, so the REQ-P6-13 Bayesian continuous-monitoring fixture can declare it without tripping DSX-SPEC-042"
  - "describe_vocabulary() now emits dict-backed vocabularies (including the three pre-existing ones: question_types, identification_strategies, peeking_policies) as full key-sorted description dicts instead of sorted()-on-dict key lists — no consumer depended on the old key-list shape"
  - "dependence.method_family_required defines no parallel vocabulary; reuses VARIANCE_ADJUSTMENTS verbatim (M-09)"
  - "dsx/checks/design.py left untouched — DSX-EXP-060's (\"\", \"fixed_horizon\") gate already lets any new PEEKING_POLICIES member fall through with no code change (M-01), proven by a parametrised disjointness test (D-08)"

patterns-established:
  - "New frame/inference vocabularies are always name->description dicts (D-04) — no set-backed exceptions"

requirements-completed: [REQ-P6-01, REQ-P6-05, REQ-P6-06]

coverage:
  - id: D1
    description: "dsx/loader.py _NULL no longer treats the literal 'none' as a null token; null/~/empty-scalar still parse as None; bundled parser agrees with PyYAML"
    requirement: "REQ-P6-01"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestLoader::test_bare_none_is_a_string_not_null"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestLoader::test_bare_none_matches_pyyaml"
        status: pass
    human_judgment: false
  - id: D2
    description: "PEEKING_POLICIES gains uncontrolled_continuous, distinct from always_valid, with DSX-EXP-060's trigger set unchanged and pinned by a parametrised disjointness test"
    requirement: "REQ-P6-05"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure::test_uncontrolled_continuous_peeking_policy_exists"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestDesign::test_dsx_exp_060_fires_only_for_empty_and_fixed_horizon"
        status: pass
    human_judgment: false
  - id: D3
    description: "Ten new closed vocabularies and a _VOCABULARIES registry backing a byte-stable, coverage-complete describe_vocabulary()"
    requirement: "REQ-P6-06"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure::test_vocabularies_registry_covers_the_dump"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure::test_describe_vocabulary_is_byte_stable"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure::test_peeking_policies_dump_is_a_description_dict"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure::test_missingness_mechanisms_has_exactly_four_members_no_none"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py::TestSpecStructure::test_paradigms_and_paradigm_justifications"
        status: pass
    human_judgment: false

duration: 25min
completed: 2026-08-07
status: complete
---

# Phase 6 Plan 01: Loader null-token fix and vocabulary registry Summary

**`dsx/loader.py` `_NULL` stops swallowing the literal `none`; `dsx/spec.py` gains ten new closed vocabularies, an `uncontrolled_continuous` peeking policy, and a registry-driven `describe_vocabulary()` that stops discarding descriptions**

## Performance

- **Duration:** ~25 min
- **Completed:** 2026-08-07T21:55Z
- **Tasks:** 2 (both TDD, each RED then GREEN)
- **Files modified:** 3 (`dsx/loader.py`, `dsx/spec.py`, `tests/test_dsx.py`)

## Accomplishments
- `dsx/loader.py`'s `_NULL` set now contains exactly `{"", "null", "~"}` — the literal `none` parses as the string `"none"` for scalars and flow-list elements, matching PyYAML/YAML 1.1 null semantics, while `null`, `~` and the empty scalar still parse as `None`. Six new regression behaviors covered, including a PyYAML-agreement test that skips cleanly when PyYAML is absent.
- `PEEKING_POLICIES` gains `uncontrolled_continuous` ("interim looks continue with no sequential correction and no anytime-valid method — the error rate is not controlled"), and `always_valid`'s description was tightened to name what actually controls the error rate. A parametrised test proves `DSX-EXP-060` still fires only for `""` and `fixed_horizon` across every `PEEKING_POLICIES` member, with zero changes to `dsx/checks/design.py`.
- Ten new closed vocabularies landed in `dsx/spec.py`, every one a `name->description` dict per D-04: `IDENTIFICATION_STRENGTHS`, `CONSTRAINT_SOURCES`, `DEPENDENCE_STRUCTURES`, `INTERFERENCE_RISKS`, `INTERFERENCE_MITIGATIONS`, `MISSINGNESS_MECHANISMS` (exactly 4 members, no `none`, per locked decision R-02), `ANALYSIS_POPULATIONS`, `DECLARATION_POINTS`, `PARADIGMS`, `PARADIGM_JUSTIFICATIONS` (7 members, no ranking, per D-12 symmetry). `dependence.method_family_required` was deliberately given no parallel vocabulary — it reuses the existing `VARIANCE_ADJUSTMENTS` set (M-09).
- `describe_vocabulary()` was rewritten around a single `_VOCABULARIES` registry (23 entries: 13 pre-existing + 10 new) that the `dsx vocab` CLI's `cmd_vocab` continues to call unmodified. Dict-backed vocabularies now dump as key-sorted description dicts (not just sorted key lists); set-backed vocabularies still dump as sorted lists; `chart_capabilities` stays special-cased exactly as before. The dump is byte-stable across repeated calls, verified by a dedicated test.

## Task Commits

Each task was TDD (RED then GREEN), committed atomically:

1. **Task 1: Drop the non-standard null token from the loader (REQ-P6-01)**
   - `2e46fa1` (test) — failing regression tests for the bare-`none` loader bug
   - `6af4590` (feat) — `_NULL` set corrected to `{"", "null", "~"}`
2. **Task 2: Add the uncontrolled-continuous peeking policy and the vocabulary registry (REQ-P6-05, REQ-P6-06)**
   - `e4f344d` (test) — failing tests for the vocabulary registry, `uncontrolled_continuous`, and the `DSX-EXP-060` disjointness property
   - `64326f8` (feat) — ten new vocabularies, `PEEKING_POLICIES.uncontrolled_continuous`, `_VOCABULARIES` registry, registry-driven `describe_vocabulary()`

**Plan metadata:** committed separately by the final-commit step below.

## Files Created/Modified
- `dsx/loader.py` — `_NULL` set literal corrected; `_scalar()` unchanged (its `if lowered in _NULL` test was already correct once the set was right)
- `dsx/spec.py` — `PEEKING_POLICIES` gains `uncontrolled_continuous`, ten new vocabulary constants, `_VOCABULARIES` registry, `describe_vocabulary()` rewritten as a registry loop
- `tests/test_dsx.py` — six new `TestLoader` behaviors, six new `TestSpecStructure` tests (registry coverage/identity, byte-stability, peeking dump shape, `uncontrolled_continuous` presence, `MISSINGNESS_MECHANISMS`/`PARADIGMS`/`PARADIGM_JUSTIFICATIONS` existence), one parametrised `TestDesign` disjointness test — all additive, no deletions in the pre-existing `TestCLI` range (804-839)

## Decisions Made
- Extended the registry-driven dump shape to all dict-backed vocabularies uniformly (not just `peeking_policies`) — `question_types` and `identification_strategies` now also dump as full key-sorted description dicts instead of `sorted(dict)` key lists. Verified no test or CLI consumer depended on the old key-list shape (grep found none), so this is a safe simplification rather than a special case for `peeking_policies` alone.
- Kept both RED commits scoped to only the behaviors under test in that task, using module-level imports for symbols that already existed (`PEEKING_POLICIES`, `describe_vocabulary`) and local imports inside individual test methods for the brand-new `_VOCABULARIES`/`MISSINGNESS_MECHANISMS`/`PARADIGMS`/`PARADIGM_JUSTIFICATIONS` symbols — this kept the RED-phase failures scoped to only the new tests rather than breaking test-file collection for the whole suite.

## Deviations from Plan

None - plan executed exactly as written. Both tasks' `<acceptance_criteria>` commands were run verbatim post-implementation and all passed; `git diff --stat dsx/checks/design.py` is empty at every checkpoint.

## Issues Encountered
- `/tmp` was not writable in this environment (Windows Git Bash `Permission denied`); redirected the `dsx vocab` verification command's output to the session scratchpad directory instead. No code or test impact.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- The `_NULL` fix unblocks every later Phase 6 plan that reads a `validity_frame:` field declaring `none` (`dependence.structure`, `interference.risk`, `interference.mitigation`, `identification.constraint_source`) — those fields will now parse as the intended string, not silently collapse to `None`.
- The ten new vocabularies and the `_VOCABULARIES` registry are ready for `_validate_validity_frame_shape()` / `_validate_inference_shape()` (plan 06-02+) to import and validate against directly.
- `uncontrolled_continuous` is available for the REQ-P6-13 Bayesian continuous-monitoring known-bad fixture without tripping `DSX-SPEC-042`.
- No blockers for 06-02.

---
*Phase: 06-contract-extension-decision-record-paradigm-manifest*
*Completed: 2026-08-07*

## Self-Check: PASSED

All modified files confirmed present on disk (`dsx/loader.py`, `dsx/spec.py`, `tests/test_dsx.py`,
this SUMMARY). All four task commits (`2e46fa1`, `6af4590`, `e4f344d`, `64326f8`) confirmed present
in git history.
