---
phase: 08-interference-triggering-stability-dsx-int
reviewed: 2026-08-13T00:00:00Z
depth: deep
review_type: gap-closure round (plans 08-08/08-09), scoped to two files
diff_range: 6321bdfe274d76a0288461347fbe1d04728d8a4e..HEAD
files_reviewed: 2
files_reviewed_list:
  - dsx/frame/interference.py
  - tests/test_frame_interference.py
findings:
  critical: 1
  warning: 0
  info: 0
  total: 1
status: issues_found
---

# Phase 8: Code Review Report — gap-closure round (plans 08-08/08-09)

**Reviewed:** 2026-08-13T00:00:00Z
**Depth:** deep
**Files Reviewed:** 2
**Status:** issues_found

## Summary

I read both files in full, ran `python3 -m unittest discover -s tests` (536 tests, OK, 2 skipped)
and `sh scripts/check.sh` (all checks passed) to ground every claim below against the running code,
not against the commit messages.

The two things this round explicitly set out to fix are genuinely fixed, and I reproduced both
mechanically rather than trusting the summary:

- The `interference.risk` guard in `_check_interference_unaddressed` (`DSX-INT-010`) now only
  exempts the literal `none`. `risk="shared_buget"` with `mitigation="none"` and a blank
  `residual_note` fires `DSX-INT-010`/CRITICAL and `dsx gate plan` exits 1, where it exited 0 before
  this round.
- The `triggering.analysis_population` guard in `_check_triggering_dilution` (`DSX-INT-030`) now
  only exempts `triggered` or an absent value. `analysis_population="eligable"` fires
  `DSX-INT-030`/CRITICAL and `dsx gate plan` exits 1, where it exited 0 before this round.
- The prior review's WR-01 (vacuous `DSX-SPEC-082 in (out+err)` substring assertion, made vacuous
  because `DSX-INT-010`'s own `detail` names `DSX-SPEC-082` unconditionally) is closed: the new
  `_gate_findings` helper asserts against the parsed `--json` finding list, and I confirmed no other
  finding in this codebase quotes the literal strings `DSX-INT-010` or `DSX-INT-030` inside its own
  `detail` text (`grep -rn "DSX-INT-010\|DSX-INT-030" dsx/` returns only `dsx/frame/interference.py`),
  so none of the remaining substring assertions in this file (e.g.
  `test_committed_fixture_blocks_plan_naming_int_010`,
  `test_committed_triggering_dilution_fixture_blocks_plan_naming_int_030`) share WR-01's disease.
- Docstrings, `DecisionRecord.rule` text and code agree for both fixed guards — I compared each
  triplet line by line; the firing condition is stated identically in all three places for both
  `_check_interference_unaddressed` and `_check_triggering_dilution`.
- No new regex or line-anchored pattern was added anywhere in the diff, so there is no new CRLF
  exposure to flag.

What is **not** fixed is the underlying failure class itself, only the two narrow reproduction cases
that were tested against. `_check_interference_mitigation_admissibility` (`DSX-INT-011`) was
deliberately left untouched, on the documented rationale (`08-08-PLAN.md` T-8-18/T-8-27,
`08-08-SUMMARY.md`) that forcing a judgment there for an out-of-vocabulary risk "would make
`DSX-INT-011` double-report what `DSX-INT-010` now reports." I tested that claim directly — see
CR-01 below — and it is false. Because it is false, a live, one-character-typo bypass of the same
`dsx gate plan` CRITICAL threshold remains, on the same field, for a case none of this round's new
tests exercise.

## Critical Issues

### CR-01: An out-of-vocabulary `interference.risk`, paired with any *recognised* mitigation, still clears `dsx gate plan` with zero `DSX-INT-*` findings — the risk-guard fix only closed the "no mitigation declared" half of the bypass

**File:** `dsx/frame/interference.py:311-314` (`_check_interference_mitigation_admissibility`'s risk
guard, unedited by this round, in the function this round's docstring and disjointness argument both
depend on)

**Issue:** This round's fix to `_check_interference_unaddressed` correctly makes an unrecognised
`risk` string fall through to judgment instead of being treated as `none`. But `DSX-INT-010` only
fires when the *mitigation* side is also absent, `none`, or unrecognised
(`mitigation_absent = normalized_mitigation == "none" or normalized_mitigation not in
INTERFERENCE_MITIGATIONS`). If a spec pairs a misspelled `risk` with a real, recognised,
non-`none` mitigation string, `mitigation_absent` is `False`, so `DSX-INT-010` stays silent — and
`_check_interference_mitigation_admissibility` (`DSX-INT-011`) returns before its judgment point for
*any* risk not in `INTERFERENCE_RISKS`, recognised mitigation or not:

```python
risk = get(frame, "interference.risk")
normalized_risk = normalize(risk) if not is_blank(risk) else "none"
if normalized_risk == "none" or normalized_risk not in INTERFERENCE_RISKS:
    return
```

Reproduced directly against `interference.check()` (no gate machinery involved):

```
risk=shared_buget (typo of shared_budget), mitigation=geo_split, residual_note=""
  -> interference.check() findings: set()          # neither DSX-INT-010 nor DSX-INT-011 fires

risk=shared_budget (spelled correctly), mitigation=geo_split, residual_note=""
  -> interference.check() findings: {'DSX-INT-011'} # correctly caught: geo_split is not
                                                      # admissible for shared_budget
```

A single misspelled character in `risk` is the entire difference between "correctly caught,
CRITICAL, blocks `plan`" and "not adjudicated at all." Reproduced at the gate level against a
mutated copy of the committed `interference-shared-budget-ANALYSIS-SPEC.yaml` fixture:

```
$ dsx gate plan --spec <mutated: risk=shared_buget, mitigation=budget_isolation, residual_note=""> --json
exit code: 0
DSX-SPEC-082 HIGH  spec.validity_frame.interference.risk   (below GATE_THRESHOLDS["plan"] == "CRITICAL")
DSX-EXP-040 MEDIUM ...
DSX-MET-040 HIGH   ...
DSX-PAR-001 INFO   ...
```

No `DSX-INT-*` finding of any kind. `08-VERIFICATION.md`'s truth statement for this gap ("A declared
interference risk other than none, with no admissible mitigation and no residual note, is blocked at
`dsx gate plan` no matter which `INTERFERENCE_*` field carries the typo") is not actually established
by the fix or the new tests — every risk-typo test this round added
(`test_out_of_vocabulary_risk_with_no_mitigation_and_blank_residual_still_fires_int_010`,
`test_out_of_vocabulary_risk_variant_blocks_plan_naming_both_int_010_and_spec_082`) pairs the typo'd
`risk` with `mitigation="none"` — the one sub-case where the fixed `_check_interference_unaddressed`
guard is sufficient on its own. None pairs it with a mitigation that is present and recognised, which
is exactly the sub-case that routes to the untouched `_check_interference_mitigation_admissibility`
guard instead.

The rationale on record for leaving that guard alone is also directly falsifiable, not just
unproven. `08-08-PLAN.md` (T-8-18) and `08-08-SUMMARY.md` both state the reason is that judging an
out-of-vocabulary risk in `_check_interference_mitigation_admissibility` "would make DSX-INT-011
double-report what DSX-INT-010 now reports." I swept 400 `(risk, mitigation, residual_note)`
combinations, including every documented risk/mitigation vocabulary member, several typo'd
near-misses, blanks and `None`, through both the shipped `DSX-INT-010` predicate and a
minimally-changed `DSX-INT-011` predicate (only the `normalized_risk not in INTERFERENCE_RISKS`
clause removed, letting `_RISK_MITIGATION_MAP.get(normalized_risk, frozenset())` degrade to an empty
admissible set exactly the way `_check_interference_unaddressed`'s own `admissible_listed` already
does): **zero combinations produced both findings at once.** Disjointness does not depend on that
clause — `DSX-INT-010` fires only when the mitigation is absent/`none`/unrecognised, and the modified
`DSX-INT-011` would fire only when it is present/recognised/non-`none`; those two conditions are
already mutually exclusive on the mitigation dimension alone, independent of risk vocabulary
membership.

This is the same class of defect the project brief calls out as the highest severity in this
codebase: an input silently not judged at a CRITICAL-threshold gate, requiring only a one-character
typo to trigger, on a fixture already committed to the corpus to demonstrate the opposite.

**Fix:** Drop the `or normalized_risk not in INTERFERENCE_RISKS` clause from
`_check_interference_mitigation_admissibility`'s guard, matching the treatment this round already
applied on the `DSX-INT-010` side, and letting the existing `.get(normalized_risk, frozenset())`
degrade correctly (it already prints `(none admissible)` for exactly this case via the shared
`admissible_listed` pattern used in both functions):

```python
# dsx/frame/interference.py, _check_interference_mitigation_admissibility
risk = get(frame, "interference.risk")
normalized_risk = normalize(risk) if not is_blank(risk) else "none"
if normalized_risk == "none":
    return
```

Update the function's docstring accordingly — it currently states DSX-INT-011 "requires a real,
recognised risk," which after this change is no longer true, and the disjointness paragraph in
`_check_interference_unaddressed`'s own docstring ("DSX-INT-011's own risk guard returns before its
judgment point for exactly that input, because `_RISK_MITIGATION_MAP` has no admissibility cell for a
risk it does not contain") should be corrected too — that clause is not, in fact, why the guard
returns early today (the guard is an explicit `not in INTERFERENCE_RISKS` check, never reaching the
map for this input); after the fix above it becomes accurate for a different reason worth restating
in its own terms.

Add a regression test pairing an out-of-vocabulary `risk` with a real, recognised, `INTERFERENCE_RISKS`-inadmissible mitigation (e.g. `risk="shared_buget"`, `mitigation="geo_split"`) and asserting `DSX-INT-011` fires — the sub-case none of this round's new tests cover, and the one that falsifies the "double-report" rationale on record for leaving this function alone.

---

_Reviewed: 2026-08-13T00:00:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep — gap-closure round, scoped to `dsx/frame/interference.py` and `tests/test_frame_interference.py`_
