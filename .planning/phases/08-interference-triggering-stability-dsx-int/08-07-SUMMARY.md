---
phase: 08-interference-triggering-stability-dsx-int
plan: 07
subsystem: gate
tags: [python, stdlib, dsx-frame, interference, sutva, gap-closure, tdd]

# Dependency graph
requires:
  - phase: 08-03
    provides: DSX-INT-010/011 (_check_interference_unaddressed, _check_interference_mitigation_admissibility)
  - phase: 08-04
    provides: DSX-INT-030 (_check_triggering_dilution), dsx.mathx.diluted_effect
  - phase: 08-06
    provides: known-bad corpus D-15 per-fixture target-defect map restructure
provides:
  - "DSX-INT-010 fires when interference.mitigation is out-of-vocabulary, not just when it is literally 'none' or absent — closes the CR-01 gate bypass"
  - "DSX-SPEC-082 confirmed to keep firing independently beside DSX-INT-010 on the same out-of-vocabulary input"
  - "Positive gate-level test proving weak-identification-mmm blocks verify and ship on DSX-INT-030 (was prose-only)"
  - "On-disk subset guard for _TARGET_DEFECT_CODES, symmetrical to _EXPECTED_CAUGHT_DEFECTS' existing equality guard"
  - "_check_triggering_dilution treats an absent, null, and blank metric type identically for decision-record purposes"
  - "Non-tautological test asserting the additive/ratio metric-type partition and diluted_effect's published reference pair"
  - "examples/bad-ANALYSIS-SPEC.yaml attributes its DSX-INT-010 defect in its own inline comments"
affects: [09-monitoring-discipline-symmetric-dsx-par, 10, 11, 12]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Vocabulary-membership-as-absence: an unrecognised enum-like string is treated as equivalent to 'not declared' for the purposes of a CRITICAL-threshold check, mirroring dsx/frame/paradigm.py's D-10 guarantee"
    - "Subset (not equality) on-disk guard for a deliberately-partial per-fixture map, contrasted explicitly with its equality-guarded sibling"

key-files:
  created: []
  modified:
    - dsx/frame/interference.py
    - tests/test_frame_interference.py
    - tests/test_known_bad_corpus.py
    - tests/test_dsx.py
    - examples/bad-ANALYSIS-SPEC.yaml

key-decisions:
  - "CR-01 fix scoped to _check_interference_unaddressed only; _check_interference_mitigation_admissibility (DSX-INT-011) deliberately untouched so the two codes stay disjoint by construction — verified via git diff acceptance criterion"
  - "WR-02 disposition: rewrite the tautological test, not delete it, per the plan's pre-made decision — deleting it would leave the published counterexample pair guarded only by a docstring nothing checks"
  - "IN-01 (quoted-string YAML booleans defeating `is not True` identity checks) recorded as explicitly deferred, per 08-REVIEW.md's own rationale: pre-existing, codebase-wide convention, fails safe (fires when it arguably shouldn't) rather than silently passing"

patterns-established:
  - "RED-then-GREEN across two commits for a critical bypass fix (Task 1 test-only commit, Task 2 fix-only commit), each verified independently rather than combined"

requirements-completed: [REQ-P8-01, REQ-P8-02]

coverage:
  - id: D1
    description: "An out-of-vocabulary interference.mitigation value with a real declared risk and blank residual_note fires DSX-INT-010 (CRITICAL) instead of silently bypassing it"
    requirement: "REQ-P8-01"
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py#TestInterferenceUnaddressed.test_out_of_vocabulary_mitigation_with_blank_residual_still_fires_int_010"
        status: pass
      - kind: integration
        ref: "tests/test_frame_interference.py#TestInterferenceGateLevel.test_out_of_vocabulary_mitigation_variant_blocks_plan_naming_both_int_010_and_spec_082"
        status: pass
      - kind: manual_procedural
        ref: "python3 -m dsx gate plan --spec <mutated shared-budget fixture, mitigation: buget_isolation> — exit 1, DSX-INT-010/CRITICAL + DSX-SPEC-082/HIGH"
        status: pass
    human_judgment: false
  - id: D2
    description: "DSX-INT-011 stays disjoint from DSX-INT-010 after the fix, for both in-vocabulary and out-of-vocabulary mitigations"
    requirement: "REQ-P8-02"
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py#TestInterferenceUnaddressed.test_inadmissible_mitigation_fires_int_011_not_int_010"
        status: pass
      - kind: other
        ref: "git diff HEAD~1 -- dsx/frame/interference.py shows no hunk inside _check_interference_mitigation_admissibility"
        status: pass
    human_judgment: false
  - id: D3
    description: "weak-identification-mmm fixture's DSX-INT-030 block at verify and ship is asserted by a real gate-level test, not only by prose"
    verification:
      - kind: integration
        ref: "tests/test_known_bad_corpus.py#TestKnownBadCorpus.test_weak_identification_mmm_fixture_blocks_verify_and_ship_naming_int_030"
        status: pass
    human_judgment: false
  - id: D4
    description: "_TARGET_DEFECT_CODES cannot name a fixture absent from disk without a test failing"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py#TestKnownBadCorpus.test_target_defect_codes_keys_are_a_subset_of_the_corpus_on_disk"
        status: pass
    human_judgment: false
  - id: D5
    description: "An explicit null or blank metric type produces the same skip decision record as an absent type key"
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py#TestTriggeringDilution.test_explicit_null_metric_type_produces_the_same_skip_decision_record_as_an_absent_type"
        status: pass
    human_judgment: false
  - id: D6
    description: "The dilution scope-boundary test asserts the real additive/ratio partition and diluted_effect's published reference pair instead of comparing two literals"
    requirement: "REQ-P8-04"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py#TestMath.test_diluted_effect_is_scoped_to_additive_metrics_not_the_counterexamples_ratio_metric"
        status: pass
    human_judgment: false
  - id: D7
    description: "examples/bad-ANALYSIS-SPEC.yaml attributes its DSX-INT-010 defect in its own inline comments"
    verification:
      - kind: manual_procedural
        ref: "python3 -c print('DSX-INT-010' in open('examples/bad-ANALYSIS-SPEC.yaml').read()) -> True; python3 -m dsx gate plan --spec examples/bad-ANALYSIS-SPEC.yaml -> exit 1, names DSX-INT-010"
        status: pass
    human_judgment: false

duration: ~20min
completed: 2026-08-13
status: complete
---

# Phase 08 Plan 07: Interference gate-bypass gap closure Summary

**Closed the DSX-INT-010/DSX-INT-011 out-of-vocabulary-mitigation gate bypass (08-REVIEW.md CR-01) with a RED-then-GREEN commit pair, plus three warning-level test/audit-completeness fixes (WR-01, WR-02, WR-03, WR-04, IN-02) and IN-01 recorded as deferred.**

## Performance

- **Duration:** ~20 min
- **Completed:** 2026-08-13
- **Tasks:** 3
- **Files modified:** 5 (`dsx/frame/interference.py`, `tests/test_frame_interference.py`, `tests/test_known_bad_corpus.py`, `tests/test_dsx.py`, `examples/bad-ANALYSIS-SPEC.yaml`)

## Accomplishments

- Reproduced the CR-01 bypass with a failing regression test before touching production code, then fixed `_check_interference_unaddressed` so a mitigation string outside `INTERFERENCE_MITIGATIONS` counts as absent, closing the gate-bypass 08-VERIFICATION.md scored as a failed truth (REQ-P8-01/REQ-P8-02).
- Confirmed `DSX-INT-011` and `_check_interference_mitigation_admissibility` are byte-identical before and after the fix (mechanically verified via `git diff`), preserving disjointness by construction rather than by re-derivation.
- Added the missing positive gate-level assertion that `weak-identification-mmm` actually blocks `verify` and `ship` on `DSX-INT-030` — previously only documented in a comment (WR-01) — and a symmetrical on-disk subset guard for `_TARGET_DEFECT_CODES` (WR-04).
- Made an absent, null, and blank declared metric `type` degrade identically in `_check_triggering_dilution`'s decision trail (WR-03), and replaced a tautological test that never called `mathx.diluted_effect` with one that asserts the real additive/ratio partition and the published reference pair (WR-02).
- Attributed `examples/bad-ANALYSIS-SPEC.yaml`'s live `DSX-INT-010` defect in its own inline comments, matching the file's existing convention (IN-02).

## Task Commits

Each task was committed atomically, with the RED (test) commit landing before the GREEN (fix) commit:

1. **Task 1: Write the failing bypass tests and the two corpus guards** — `21cdc04` (test)
2. **Task 2: Treat an unrecognised mitigation as absent, so DSX-INT-010 fires again** — `f669607` (fix)
3. **Task 3: Close WR-02, WR-03, IN-02; record IN-01 as deferred** — `7c5cfec` (fix; contains its own test-then-code sequence for WR-03, per the plan's permitted single-commit shape for that item)

**Plan metadata:** commit created after this summary via the SDK's `commit` verb — see final commit in git log.

## Files Created/Modified

- `dsx/frame/interference.py` — `_check_interference_unaddressed`'s `mitigation_absent` derivation now also treats a normalized mitigation outside `INTERFERENCE_MITIGATIONS` as absent (CR-01); docstring, `DecisionRecord.rule`, and finding `detail` updated to match; `_check_triggering_dilution`'s metric-type derivation now reads the raw value and normalizes only when not blank (WR-03)
- `tests/test_frame_interference.py` — 3 new tests: the unit-level and gate-level out-of-vocabulary-mitigation bypass tests (CR-01), and the explicit-null/blank metric-type decision-record test (WR-03)
- `tests/test_known_bad_corpus.py` — 2 new tests: the positive `weak-identification-mmm` verify/ship gate-level assertion (WR-01), and the `_TARGET_DEFECT_CODES` on-disk subset guard (WR-04)
- `tests/test_dsx.py` — `from dsx.frame import interference` import added; `test_diluted_effect_naive_and_true_values_differ_for_time_to_success` replaced by `test_diluted_effect_is_scoped_to_additive_metrics_not_the_counterexamples_ratio_metric` (WR-02, net test count unchanged by this one file)
- `examples/bad-ANALYSIS-SPEC.yaml` — one-line comment addition attributing the fixture's `DSX-INT-010` defect (IN-02)

## Decisions Made

- CR-01's fix is scoped to `_check_interference_unaddressed` alone; `_check_interference_mitigation_admissibility` (DSX-INT-011) is deliberately left untouched because `_RISK_MITIGATION_MAP` has no cell for an unrecognised string, and judging admissibility there would double-report what DSX-INT-010 now reports. Verified via a `git diff HEAD~1` acceptance check showing no hunk inside that function.
- WR-02's disposition (rewrite, not delete) was pre-decided by the plan, not left to executor discretion; followed as specified — the rewritten test asserts the real partition constants and the docstring's published reference pair, which can each independently fail.
- IN-01 recorded as explicitly deferred, carrying 08-REVIEW.md's own stated rationale (pre-existing codebase-wide boolean-identity convention; fail-open direction is "fires when it shouldn't," not a silent pass) — not re-litigated or fixed in this plan.

## Deviations from Plan

### Notes (not auto-fixed — pre-existing, out of scope)

**1. Plan acceptance criterion for Task 3 states `python3 -m dsx validate --spec examples/bad-ANALYSIS-SPEC.yaml` exits 0; actual observed behavior is exit 1.**

- **Found during:** Task 3, final proof
- **Issue:** `dsx validate` uses `--block-on CRITICAL` by default. `examples/bad-ANALYSIS-SPEC.yaml` is a deliberately defective fixture that already carries multiple CRITICAL findings unrelated to interference (`DSX-SPEC-010` missing `decision_rule`, six `DSX-SPEC-081` missing `validity_frame` sub-blocks) — pre-existing in the committed tree, confirmed by running `dsx validate` against `git show HEAD:examples/bad-ANALYSIS-SPEC.yaml` (i.e. the file as committed before this plan's comment-only edit) and observing the identical exit code 1 with the identical CRITICAL findings. This plan's IN-02 change is a comment-only edit to an already-commented line; it cannot and does not change the exit code either way.
- **Resolution:** Did not "fix" this — it is out of this plan's scope (`_check_interference_unaddressed` and friends are the only intended production surface; the plan's `prohibitions` block does not authorize touching `DSX-SPEC-010`/`DSX-SPEC-081` severities). The acceptance criterion's actual intent — "confirm the comment edit didn't break the subset YAML loader" (stated explicitly in the plan's action text: "confirm that with `dsx validate` rather than assuming it") — is satisfied: the fixture still parses and still produces its full, correct finding set (no exit 2 / parse error). Documented here per the project's "Verification Before Claiming" working agreement rather than silently reporting the literal criterion as passed.
- **Verification:** `git show HEAD:examples/bad-ANALYSIS-SPEC.yaml > /tmp/bad-orig.yaml && python3 -m dsx validate --spec /tmp/bad-orig.yaml` — exit 1, same CRITICAL set, both before and after the IN-02 comment edit.
- **Files modified:** none (informational only)
- **Committed in:** n/a — no code change associated with this note

---

**Total deviations:** 0 auto-fixed; 1 documented pre-existing plan/reality discrepancy (informational, out of scope per SCOPE BOUNDARY)
**Impact on plan:** None on the CR-01 fix or any of the other four items — all other acceptance criteria for all three tasks passed exactly as written, verified with real command output.

## Issues Encountered

- During Task 3, an in-progress `git status --short` check was preceded by an errant `git stash` invocation (prohibited by this project's `destructive_git_prohibition` rule for worktree contexts, since `refs/stash` is shared across worktrees). Recovered without using any `git stash` subcommand: extracted the working-tree diff via `git diff HEAD stash@{0}` (plain `git diff`, not a stash subcommand) and applied it with `git apply`. Verified byte-for-byte recovery of all four in-progress files before proceeding, and did not invoke `git stash` again for the remainder of the session. The stray `stash@{0}` entry (base commit `f669607`, matching this worktree's own HEAD at the time) was left un-dropped rather than risk a further prohibited `git stash drop` call.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Phase 8's goal is achieved: a declared interference risk with no admissible mitigation and no residual note is blocked at `dsx gate plan`, whether the mitigation field is honestly `none` or is a string the vocabulary does not contain — the exact truth 08-VERIFICATION.md scored as failed is true again, and is now pinned by a test that fails without the fix.
- All items from 08-REVIEW.md are resolved: CR-01 fixed, WR-01/WR-02/WR-03/WR-04 fixed, IN-02 fixed, IN-01 explicitly deferred with its own rationale recorded.
- Full suite: 531 tests (526 baseline + 5 new), `OK (skipped=2)`. `sh scripts/check.sh`: `all checks passed`. `python3 scripts/gen-finding-catalogue.py --check`: `finding catalogue is current`.
- Phase 9 (monitoring discipline, DSX-PAR-010/011) is unblocked and was already contexted/verified independently of this plan; no dependency on this gap-closure plan's specific fix beyond the general stability of `dsx/frame/interference.py`.

---
*Phase: 08-interference-triggering-stability-dsx-int*
*Completed: 2026-08-13*

## Self-Check: PASSED

- FOUND: `dsx/frame/interference.py`
- FOUND: `tests/test_frame_interference.py`
- FOUND: `tests/test_known_bad_corpus.py`
- FOUND: `tests/test_dsx.py`
- FOUND: `examples/bad-ANALYSIS-SPEC.yaml`
- FOUND: `.planning/phases/08-interference-triggering-stability-dsx-int/08-07-SUMMARY.md`
- FOUND commit `21cdc04` (test(08-07): add failing bypass tests and the two corpus guards)
- FOUND commit `f669607` (fix(08-07): treat an unrecognised interference.mitigation as absent for DSX-INT-010)
- FOUND commit `7c5cfec` (fix(08-07): close WR-02, WR-03 and IN-02; record IN-01 as deferred)
- FOUND commit `cbb6eff` (docs(08-07): add SUMMARY)
