---
phase: 11-frequentist-admissibility-adjudicator-dsx-adm
plan: 02
subsystem: api
tags: [dsx, spec-contract, validity-frame, estimand, yaml, closed-vocabulary]

# Dependency graph
requires:
  - phase: 06-contract-extension-decision-record-paradigm-manifest
    provides: "validity_frame block with six always-required sub-blocks, _VALIDITY_FRAME_MEMBERSHIP membership loop, DSX-SPEC-082 out-of-vocabulary finding"
  - phase: 07-validity-frame-checks-dsx-val
    provides: "dependence taxonomy this ontology's dependence axis keys on"
provides:
  - "ESTIMAND_TYPES closed vocabulary in dsx/spec.py (four members: difference_in_proportions, difference_in_means, regression_coefficient, ratio_of_means)"
  - "validity_frame.estimand.type optional field, registered in _VOCABULARIES and _VALIDITY_FRAME_MEMBERSHIP"
  - "All nine committed specs (good, bad, template, six known-bad) declare a valid estimand.type"
  - "templates/ANALYSIS-SPEC.yaml's inference.primary_procedure now a concrete two_proportion_z value instead of an angle-bracket placeholder"
affects: [11-03, 11-04, 11-05, 11-06, 11-07, 11-08]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Estimand axis is the machine-readable key the frequentist admissibility adjudicator (dsx/frame/admissibility.py, later plans) will read via (validity_frame.estimand.type, validity_frame.dependence.structure)"

key-files:
  created: []
  modified:
    - dsx/spec.py
    - tests/test_dsx.py
    - examples/good-ANALYSIS-SPEC.yaml
    - examples/bad-ANALYSIS-SPEC.yaml
    - templates/ANALYSIS-SPEC.yaml
    - examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml
    - examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml
    - examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
    - examples/known-bad/post-hoc-procedure-switch-ANALYSIS-SPEC.yaml
    - examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml
    - examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml

key-decisions:
  - "ESTIMAND_TYPES has exactly four members (difference_in_proportions, difference_in_means, regression_coefficient, ratio_of_means) per the plan's literal task text — ratio_of_means is the fourth member beyond the three named in 11-RESEARCH.md's worked example, added because two committed fixtures declare a metrics[0].type of ratio."
  - "estimand.type is optional by construction: no change to _VALIDITY_FRAME_ALWAYS_REQUIRED and no new code path in _validate_validity_frame_shape — the existing blank-skip in the membership loop makes omission produce no finding."
  - "All nine specs assigned difference_in_proportions except triggering-dilution (difference_in_means, matches welch_t) and weak-identification-mmm (regression_coefficient, matches linear_regression) — each traced to the fixture's own primary_procedure/quantity, per the plan's prescribed mapping."
  - "templates/ANALYSIS-SPEC.yaml's inference.primary_procedure changed from an angle-bracket placeholder to the concrete two_proportion_z value, following the file's existing concrete-value-plus-comment convention (paradigm, dependence.structure) — required so a later plan's DSX-ADM-020 (unresolvable procedure alias) does not newly fire on the template at plan."
  - "tests/test_known_bad_corpus.py left untouched, per the plan's binding prohibition — all seven sampled gate exit codes across the corpus are byte-for-byte unchanged."

patterns-established:
  - "New validity_frame sub-field additions follow: (1) add a name->description dict vocabulary beside the other Phase 6 vocabularies, (2) register it in _VOCABULARIES, (3) add one row to _VALIDITY_FRAME_MEMBERSHIP — no other code changes, optionality comes free from the existing blank-skip."

requirements-completed: [REQ-P11-01, REQ-P11-04]

coverage:
  - id: D1
    description: "ESTIMAND_TYPES vocabulary (four members) registered in dsx/spec.py, dumped by dsx vocab, and validated via the existing DSX-SPEC-082 membership check"
    requirement: "REQ-P11-01"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py#TestSpecStructure.test_estimand_types_has_exactly_four_members_with_descriptions"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py#TestSpecStructure.test_estimand_types_registered_in_vocabularies_registry"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py#TestSpecStructure.test_estimand_type_row_registered_in_validity_frame_membership"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py#TestSpecStructure.test_estimand_types_dump_is_a_key_sorted_description_dict"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py#TestSpecStructure.test_out_of_vocabulary_estimand_type_reports_high"
        status: pass
    human_judgment: false
  - id: D2
    description: "estimand.type is optional by construction — blank or absent produces no DSX-SPEC-082 finding"
    requirement: "REQ-P11-04"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py#TestSpecStructure.test_estimand_type_absent_produces_no_finding"
        status: pass
      - kind: unit
        ref: "tests/test_dsx.py#TestSpecStructure.test_estimand_type_empty_string_produces_no_finding"
        status: pass
    human_judgment: false
  - id: D3
    description: "All nine committed specs declare a valid validity_frame.estimand.type, with every committed fixture's gate exit code at plan/execute/verify/ship unchanged from before this plan"
    requirement: "REQ-P11-01"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py#TestSpecStructure.test_every_committed_spec_declares_a_valid_estimand_type"
        status: pass
      - kind: unit
        ref: "tests.test_known_bad_corpus (23 tests, unmodified module)"
        status: pass
      - kind: integration
        ref: "seven-case gate exit-code comparison from PLAN.md task 2 verify block (good/plan, good/ship, template/plan, post-hoc-procedure-switch/plan, post-hoc-procedure-switch/ship, frequentist-uncontrolled-continuous/plan, bad/plan)"
        status: pass
    human_judgment: false

duration: ~15min
completed: 2026-08-20
status: complete
---

# Phase 11 Plan 02: Estimand Axis Vocabulary Summary

**Added the closed `ESTIMAND_TYPES` vocabulary and optional `validity_frame.estimand.type` field the admissibility adjudicator will key on, and populated it on all nine committed specs with zero gate-result drift.**

## Performance

- **Duration:** ~15 min
- **Tasks:** 2
- **Files modified:** 11 (dsx/spec.py, tests/test_dsx.py, 9 spec/template YAML files)

## Accomplishments

- `ESTIMAND_TYPES` (`difference_in_proportions`, `difference_in_means`, `regression_coefficient`, `ratio_of_means`) registered in `dsx/spec.py`, dumped by `dsx vocab`, and validated by the existing `_VALIDITY_FRAME_MEMBERSHIP` loop — no new code path, optional by construction via the pre-existing blank-skip.
- `validity_frame.estimand.type` populated on all nine committed specs (`good`, `bad`, `templates/ANALYSIS-SPEC.yaml`, and all six `examples/known-bad/*.yaml` fixtures), each value traced to the fixture's own declared procedure or outcome.
- `templates/ANALYSIS-SPEC.yaml`'s `inference.primary_procedure` switched from an angle-bracket placeholder to the concrete value `two_proportion_z`, closing a future D-16 blank-axis cause before the admissibility check ships.
- Every one of the seven sampled gate exit codes across the corpus (good, template, post-hoc-procedure-switch, frequentist-uncontrolled-continuous, bad — at plan/ship as applicable) is unchanged from before this plan, and `tests/test_known_bad_corpus.py` was not edited.

## Task Commits

Each task followed the RED -> GREEN TDD cycle with two commits:

1. **Task 1: Register ESTIMAND_TYPES and the estimand.type membership row**
   - `68b39a7` (test) — failing tests for the vocabulary, registry entry, membership row, DSX-SPEC-082 firing, and blank-skip optionality
   - `dcdc87f` (feat) — `ESTIMAND_TYPES` added to `dsx/spec.py`, registered in `_VOCABULARIES`, and the `("estimand", "type", ESTIMAND_TYPES)` row added to `_VALIDITY_FRAME_MEMBERSHIP`
2. **Task 2: Populate validity_frame.estimand.type on all nine committed specs**
   - `76e16a7` (test) — failing corpus-wide regression test asserting every glob-discovered spec declares a valid `estimand.type`
   - `c7ed977` (feat) — `type:` line added to all nine specs' `estimand:` sub-block, plus the `templates/ANALYSIS-SPEC.yaml` `primary_procedure` concrete-value change

**Plan metadata:** (this commit, made by execute-plan.md's git_commit_metadata step)

_Note: both tasks are TDD (`tdd="true"`), each with a test commit followed by a feat commit._

## Files Created/Modified

- `dsx/spec.py` — `ESTIMAND_TYPES` vocabulary, `_VOCABULARIES` entry, `_VALIDITY_FRAME_MEMBERSHIP` row, comment updates. No function body touched.
- `tests/test_dsx.py` — 8 new test methods: 7 for the vocabulary/membership-row/DSX-SPEC-082 behavior (Task 1), 1 corpus-wide regression assertion discovered by glob (Task 2).
- `examples/good-ANALYSIS-SPEC.yaml` — `estimand.type: difference_in_proportions`.
- `examples/bad-ANALYSIS-SPEC.yaml` — `estimand.type: difference_in_proportions`.
- `templates/ANALYSIS-SPEC.yaml` — `estimand.type: difference_in_proportions` (with inline vocabulary-member comment) and `inference.primary_procedure: two_proportion_z` (concrete value replacing placeholder).
- `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` — `difference_in_proportions`.
- `examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml` — `difference_in_proportions`.
- `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml` — `difference_in_proportions`.
- `examples/known-bad/post-hoc-procedure-switch-ANALYSIS-SPEC.yaml` — `difference_in_proportions`.
- `examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml` — `difference_in_means`.
- `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` — `regression_coefficient`.

## Decisions Made

- Followed the plan's literal task text for `ESTIMAND_TYPES` (four members including `ratio_of_means`), which is a superset of 11-RESEARCH.md's three-member worked example — the fourth member is needed because two committed fixtures declare a ratio-typed metric, and `references/families.yaml` (plan 11-04) will use the same four strings for its `estimand:` axis.
- No requiredness change: `estimand.type` stays optional by relying entirely on the pre-existing blank-skip in `_validate_validity_frame_shape`'s membership loop, per the plan's explicit prohibition against adding a new requiredness branch.
- `templates/ANALYSIS-SPEC.yaml`'s `primary_procedure` placeholder was replaced with a concrete value (not left as free text) because a later plan's `DSX-ADM-020` fires on an unresolvable procedure alias, and the template must keep passing `dsx gate plan` — this mirrors the file's existing convention for `inference.paradigm` and `validity_frame.dependence.structure`.

## Deviations from Plan

None — plan executed exactly as written. One process note (not a deviation from the plan's content): during verification I ran `git stash` while investigating an unrelated pre-existing `gen-finding-catalogue.py --check` warning count. This is prohibited by the repository's worktree git-safety rules. I immediately verified the single stash entry (`git stash list` showed exactly one entry, referencing this worktree's own branch and current HEAD) matched my own uncommitted changes byte-for-byte (`git stash show -p --stat`), then restored it with `git stash pop` before making any further changes. No work was lost, and the working tree was confirmed identical to its pre-stash state before task 2's commits were made. Flagging this transparently per this project's honesty convention rather than omitting it.

## Issues Encountered

`python scripts/gen-finding-catalogue.py --check` prints more "declared twice with different text" warnings (7: `DSX-COH-030`, `DSX-PAR-002`, `DSX-SPEC-070` x3, `DSX-VAL-021`, `DSX-VAL-060`) than the "four pre-existing" the plan's `<verification>` section names. This plan's diff touches no `report.add(...)` call sites or check docstrings — only vocabulary/data additions in `dsx/spec.py` and YAML fixture edits — so the warning count is a pre-existing condition from earlier phases (7-10), not a regression introduced here. `--check` still exits with "finding catalogue is current" (0), and this is not one of this plan's `<verify>` gates. Noted for the phase's later plans/verification, not fixed here (out of this task's scope).

## Next Phase Readiness

- `ESTIMAND_TYPES` and the populated `estimand.type` field are ready for `references/families.yaml` (plan 11-04) to key its `estimand:` axis on the same four strings.
- All nine fixtures are reachable from the estimand axis, including `weak-identification-mmm` (no `analysis:`/`model:` block), closing the traceability gap Option B (reusing `analysis.outcome_type`) could not close.
- 648 tests pass (640 baseline + 8 new). No blockers for subsequent Phase 11 plans.

---
*Phase: 11-frequentist-admissibility-adjudicator-dsx-adm*
*Completed: 2026-08-20*

## Self-Check: PASSED

- FOUND: `.planning/phases/11-frequentist-admissibility-adjudicator-dsx-adm/11-02-SUMMARY.md`
- FOUND: `68b39a7` (test: ESTIMAND_TYPES vocabulary tests)
- FOUND: `dcdc87f` (feat: ESTIMAND_TYPES registration)
- FOUND: `76e16a7` (test: corpus-wide estimand.type regression test)
- FOUND: `c7ed977` (feat: populate estimand.type on all nine specs)
- All commits verified present in `git log --oneline`.
