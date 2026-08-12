---
phase: 07-validity-frame-checks-dsx-val
plan: 01
subsystem: infra
tags: [python, stdlib, unittest, statistics, citation-discipline]

# Dependency graph
requires:
  - phase: 06-contract-decision-paradigm-dsx-par
    provides: "dsx/spec.py vocabularies (DEPENDENCE_STRUCTURES, VARIANCE_ADJUSTMENTS), dsx/frame/ D-03a boundary, gen-finding-catalogue.py D-05 enforcement"
provides:
  - "DEPENDENCE_ADMISSIBLE_METHODS — dependence structure to admissible variance-adjustment method-family map"
  - "FALSIFIER_DISCRIMINATORS, is_placeholder_or_refusal(), falsifier_is_discriminating() — falsifier classification lexicon"
  - "dsx.mathx.design_effect() — Cochrane-cited design-effect helper, published reference value 1.576"
affects: [07-03, 07-04, 07-05]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Lookup-table module constants (dict/frozenset) live beside the vocabulary they key on and are explicitly excluded from _VOCABULARIES, both in code and in the exclusion comment"
    - "Regex idioms are copied across the D-03a boundary (dsx/checks -> dsx/spec), never imported, to keep dsx/frame/ extractable"

key-files:
  created: []
  modified:
    - dsx/spec.py
    - dsx/mathx.py
    - tests/test_dsx.py

key-decisions:
  - "DEPENDENCE_ADMISSIBLE_METHODS ships as five keys (all DEPENDENCE_STRUCTURES minus 'none'), every value a frozenset subset of VARIANCE_ADJUSTMENTS; delta_method appears in no entry"
  - "Cameron and Miller (2015) section locator for temporal/spatial, and Gelman and Hill (2007) chapter locator for hierarchical, are both flagged UNVERIFIED rather than invented; Conley (1999) is recorded as considered and deliberately not cited (training-knowledge-only attribution)"
  - "_FALSIFIER_REFUSALS matches on whole-value equality after normalize(), never substring containment, so 'none identified' (a different field's legitimate value) is not misread as a refusal"
  - "_FALSIFIER_NUMBER_RE uses only bounded, non-nested quantifiers (threat T-7-03); a 20,000-character adversarial input classifies in well under one second"
  - "design_effect() docstring is written to the full D-05 citation bar even though the function never calls report.add() and is therefore not mechanically policed by gen-finding-catalogue.py; the check function that is policed ships in plan 07-04"
  - "The unpublished older design-effect illustrative value that D-10 retires is not written, asserted or printed anywhere in this plan's output"

requirements-completed: [REQ-P7-01, REQ-P7-02, REQ-P7-04]

coverage:
  - id: D1
    description: "DEPENDENCE_ADMISSIBLE_METHODS map — five structures, every value a VARIANCE_ADJUSTMENTS subset, 'none' absent, delta_method admissible nowhere, excluded from describe_vocabulary()"
    requirement: "REQ-P7-04"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestDependenceAdmissibleMethods (5 tests)"
        status: pass
    human_judgment: false
  - id: D2
    description: "Falsifier placeholder/refusal detector and discrimination classifier — blank, angle-bracket placeholder, refusal token, prose-without-predicate, numeric-token-only, and the 'none identified' non-refusal edge case, plus a DoS timing guard"
    requirement: "REQ-P7-01"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestFalsifierLexicon (8 tests)"
        status: pass
    human_judgment: false
  - id: D3
    description: "design_effect() matches the Cochrane Handbook's published worked example (1.576) and raises ValueError on both out-of-range boundary inputs"
    requirement: "REQ-P7-02"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestMath::test_design_effect_* (5 tests)"
        status: pass
    human_judgment: false
  - id: D4
    description: "Citation locators in the DEPENDENCE_ADMISSIBLE_METHODS comment and the design_effect() docstring are honest — verified locators stated as verified, unverified locators explicitly flagged rather than invented, and Conley (1999) recorded as a deliberate non-citation"
    verification: []
    human_judgment: true
    rationale: "Citation-accuracy and honesty-labelling review is a human judgment call per this plan's threat model (T-7-07) and prohibitions; automated tests can confirm the UNVERIFIED string is present but cannot confirm the underlying bibliographic claims are accurate."

duration: ~15min
completed: 2026-08-12
status: complete
---

# Phase 7 Plan 1: Shared Validity-Frame Infrastructure Summary

**Dependence-to-method-family map, falsifier placeholder/refusal lexicon, and a Cochrane-cited design-effect helper — the three pieces `dsx/frame/val.py`'s nine checks will import, landed with 18 new tests before any check exists to read them.**

## Performance

- **Duration:** ~15 min (git commit span 16:32:07–16:34:27 on 2026-08-12; does not include the reading/verification time before the first commit)
- **Tasks:** 3
- **Files modified:** 3 (`dsx/spec.py`, `dsx/mathx.py`, `tests/test_dsx.py`)

## Accomplishments

- `DEPENDENCE_ADMISSIBLE_METHODS` in `dsx/spec.py` — a five-key map from dependence structure (`clustered`, `repeated_measures`, `temporal`, `spatial`, `hierarchical`) to the subset of `VARIANCE_ADJUSTMENTS` admissible for it. `none` has no entry; `delta_method` is admissible for no structure at all.
- `FALSIFIER_DISCRIMINATORS`, `is_placeholder_or_refusal()` and `falsifier_is_discriminating()` in `dsx/spec.py` — classifies an estimand falsifier string as blank, an angle-bracket placeholder, a refusal token, or genuinely discriminating (carries a comparison predicate or a numeric threshold). `is_blank()` is untouched.
- `dsx.mathx.design_effect(m, icc)` — returns `1 + (m - 1) * icc`, raises `ValueError` on an out-of-range cluster size or intraclass correlation, and carries a docstring citing Kish (1965) and the Cochrane Handbook (Higgins, Eldridge & Li, 2024) with the published reference value 1.576 for `m=29.8, icc=0.02`.
- 18 new unit tests across three new/extended test groups in `tests/test_dsx.py`, all passing alongside the full pre-existing suite.

## Task Commits

Each task was committed atomically:

1. **Task 1: Add the dependence structure to method-family map to dsx/spec.py** - `7a25b5f` (feat)
2. **Task 2: Add the falsifier word list and its placeholder and refusal detector to dsx/spec.py** - `5b2169c` (feat)
3. **Task 3: Add design_effect() to dsx/mathx.py with the Cochrane published reference value** - `bc42bfe` (feat)

**Plan metadata:** committed alongside this SUMMARY (worktree mode — orchestrator finalizes STATE.md/ROADMAP.md after merge)

_Note: this plan's tasks bundle test authoring and implementation into a single commit per task rather than separate RED/GREEN commits — see "TDD Gate Compliance" below._

## Files Created/Modified

- `dsx/spec.py` - Added `DEPENDENCE_ADMISSIBLE_METHODS`, `FALSIFIER_DISCRIMINATORS`, `_FALSIFIER_REFUSALS`, `_PLACEHOLDER_RE`, `_FALSIFIER_NUMBER_RE`, `is_placeholder_or_refusal()`, `falsifier_is_discriminating()`; extended the `_VOCABULARIES` exclusion comment twice (once per new constant); added `import re`
- `dsx/mathx.py` - Added `design_effect(m, icc)` next to `inflation_from_peeking()`
- `tests/test_dsx.py` - Added `TestDependenceAdmissibleMethods` (5 tests), `TestFalsifierLexicon` (8 tests), and 5 `design_effect` tests on the existing `TestMath` class

## Decisions Made

- Placed the two new falsifier regexes and helper functions next to `normalize()` (before the "Structural validation" section) rather than immediately after `FALSIFIER_DISCRIMINATORS`, since the plan's `read_first` pointed at the `get`/`section`/`items`/`is_blank`/`normalize` helper block as "the helper block the two new helpers join."
- Used `frozenset` values in `DEPENDENCE_ADMISSIBLE_METHODS` per the plan's explicit type instruction (`dict[str, frozenset[str]]`).
- `_FALSIFIER_NUMBER_RE` re-homes the `dsx/checks/claims.py:41` pattern shape (`\d+(?:\.\d+)?\s*(?:%|pp)?`) rather than importing it, honoring the D-03a boundary that forbids `dsx/spec.py` importing from `dsx/checks/`.
- Test placement follows the plan's explicit instructions: `TestDependenceAdmissibleMethods` and `TestFalsifierLexicon` sit immediately after the existing `TestSpecStructure` class (the other `dsx.spec` vocabulary tests), and the five `design_effect` tests are appended to the existing `TestMath` class rather than a new class, matching the plan's "Add the five behaviour tests as new methods on the existing TestMath class" instruction.

## Deviations from Plan

None — plan executed exactly as written. All five `must_haves.truths` are covered by the tests listed above; all acceptance criteria commands in the plan were run individually and exited 0.

## TDD Gate Compliance

This plan's frontmatter sets `type: tdd`, and each task individually carries `tdd="true"`. However, each task's `<action>` block instructs adding the module constant/function(s) and their tests as one described unit — it does not sequence a separate "write a failing test, watch it fail, then implement" step. Consistent with that structure, each task landed as a single `feat(07-01): ...` commit containing both the new code and its tests, verified green before commit, rather than separate `test(...)` (RED) then `feat(...)` (GREEN) commits. No commit in this plan's git log matches `^test\(07-01` — the RED-gate commit type is absent by task design, not by omission. Every behaviour test itself passed and was inspected for correctness against the plan's `<behavior>` blocks before commit. `MVP_MODE`/`TDD_MODE` runtime gate enforcement was not signaled by the orchestrator for this plan, so the halt-and-report protocol was not applicable.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required. D-01 holds: only the Python 3.9+ standard library (`re`) was used; no new dependency was added.

## Next Phase Readiness

- `dsx/frame/val.py` (plan 07-03 onward) can now import `DEPENDENCE_ADMISSIBLE_METHODS`, `falsifier_is_discriminating`/`is_placeholder_or_refusal` from `dsx.spec`, and `design_effect` from `dsx.mathx` — all three exist, are importable, and are covered by tests against the plan's acceptance criteria.
- Verified before finishing: `python3 -m unittest discover -s tests` — 324 tests, OK (2 skipped, unchanged from baseline); `python3 scripts/gen-finding-catalogue.py --check` — exit 0, "finding catalogue is current" (two pre-existing warnings about `DSX-COH-030`/`DSX-SPEC-070` declared twice are unrelated to this plan's files and were not introduced by it — out of scope per this plan's file list, which never touches `dsx/checks/` or `dsx/frame/`).
- `git diff --stat` against the phase base names exactly `dsx/spec.py`, `dsx/mathx.py`, `tests/test_dsx.py` — no file under `dsx/frame/` or `dsx/checks/` was touched.
- No blockers for plans 07-03 through 07-06, which are this phase's declared consumers of this plan's three artifacts.

---
*Phase: 07-validity-frame-checks-dsx-val*
*Completed: 2026-08-12*
