---
phase: 08-interference-triggering-stability-dsx-int
reviewed: 2026-08-14T00:00:00Z
depth: deep
files_reviewed: 19
files_reviewed_list:
  - dsx/cli.py
  - dsx/frame/interference.py
  - dsx/frame/paradigm.py
  - dsx/mathx.py
  - dsx/spec.py
  - examples/bad-ANALYSIS-SPEC.yaml
  - examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml
  - examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml
  - examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
  - examples/known-bad/interference-shared-budget-POSTMORTEM.md
  - examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml
  - examples/known-bad/triggering-dilution-POSTMORTEM.md
  - examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml
  - references/finding-codes.md
  - scripts/gen-finding-catalogue.py
  - tests/test_dsx.py
  - tests/test_frame_boundary.py
  - tests/test_frame_interference.py
  - tests/test_frame_val.py
  - tests/test_known_bad_corpus.py
findings:
  critical: 0
  warning: 2
  info: 1
  total: 3
status: issues_found
---

# Phase 08: Code Review Report

**Reviewed:** 2026-08-14T00:00:00Z
**Depth:** deep
**Files Reviewed:** 19 (test_frame_val.py counted; test_frame_val.py itself has no interference-family content but was read as required)
**Status:** issues_found

## Summary

Plan 08-10's change to `dsx/frame/interference.py` drops the risk-vocabulary
short-circuit from `_check_interference_mitigation_admissibility`'s guard,
leaving only the `risk == "none"` exemption. I traced the full
risk-state × mitigation-state truth table by hand (blank/none/recognised/
unrecognised on both axes) against both `_check_interference_unaddressed`
(DSX-INT-010) and `_check_interference_mitigation_admissibility`
(DSX-INT-011), and confirmed:

- The two codes are provably disjoint: DSX-INT-010 requires
  `mitigation_absent` (mitigation blank, `"none"`, or not a member of
  `INTERFERENCE_MITIGATIONS`); DSX-INT-011's guard returns unless the
  mitigation is present, recognised, and non-`"none"` — the exact logical
  complement. No risk-side condition can make both true at once.
- The out-of-vocabulary-risk-with-real-mitigation gap the plan set out to
  close is closed: `_RISK_MITIGATION_MAP.get(normalized_risk, frozenset())`
  degrades an unrecognised risk to an empty admissible set, so any
  recognised, non-`none` mitigation is unconditionally inadmissible for it
  and DSX-INT-011 fires.
- Every `DecisionRecord.rule` string in the module (DSX-INT-010, -011, -030,
  -040) matches its function's actual firing condition — I checked each one
  against the code line by line, not just against the docstring prose.
- `dsx/frame/interference.py` reads no code path through `inference.paradigm`
  (confirmed by re-reading the module and by running
  `tests/test_frame_boundary.py::TestFrameParadigmReadBoundary`).
- Ran the full suite (`python -m unittest discover -s tests`): 540 tests,
  OK. Ran `scripts/gen-finding-catalogue.py --check`-equivalent inspection by
  hand against `references/finding-codes.md`: all four `DSX-INT-*` titles and
  severities match the `report.add(...)` call sites exactly.
- Checked every `examples/known-bad/*-ANALYSIS-SPEC.yaml` fixture's
  `validity_frame.interference` block against the new guard: none of them
  declares a recognised, non-`none` mitigation paired with an unrecognised
  risk, so none is newly affected by this change (all either have
  `mitigation: none` or `risk: none`) — the fixture corpus's existing
  `_TARGET_DEFECT_CODES`/`_EXPECTED_CAUGHT_DEFECTS` expectations in
  `tests/test_known_bad_corpus.py` stay accurate.

No BLOCKER-class defect found in the reviewed diff. Two WARNING-level
quality issues found (both real, reachable code paths, not hypothetical),
and one INFO-level style nit.

## Warnings

### WR-01: DSX-INT-011's remedy text is self-contradictory for an out-of-vocabulary risk

**File:** `dsx/frame/interference.py:349-366`

**Issue:** When `_check_interference_mitigation_admissibility` fires against
an unrecognised `interference.risk` string (a typo, e.g. `shared_buget`)
paired with a recognised, channel-inadmissible mitigation, `admissible` is
the empty frozenset (`_RISK_MITIGATION_MAP.get(normalized_risk,
frozenset())` has no cell for an out-of-vocabulary key), so
`admissible_listed` becomes the literal string `"(none admissible)"`. The
`remedy` field then renders as:

```text
Declare a mitigation admissible for 'shared_buget': (none admissible).
```

This instructs the operator to do the one thing the same sentence says is
impossible, and gives no alternative. `_check_interference_unaddressed`
(DSX-INT-010) has the identical `admissible_listed or "(none admissible)"`
substitution at line 230 but at least appends `"— or write a residual_note
stating plainly what interference remains unaddressed and why it is
accepted"` as a real escape hatch; DSX-INT-011's remedy has no equivalent
fallback clause. This is a real, reachable path — it is exactly what fires
in `tests/test_frame_interference.py::test_out_of_vocabulary_risk_with_real_mitigation_still_fires_int_011`
and its gate-level sibling — the test asserts the finding fires and its
`where`, but never asserts on `remedy` text, so the confusing message
shipped without a test catching it.

**Fix:** Branch the remedy on whether `admissible` is empty, and point the
operator at the real fix (correct the risk spelling — DSX-SPEC-082 already
flags the vocabulary violation separately) instead of an impossible
instruction:

```python
if admissible:
    remedy = (
        f"Declare a mitigation admissible for {normalized_risk!r}: "
        f"{admissible_listed}."
    )
else:
    remedy = (
        f"{normalized_risk!r} is not a recognised interference risk (see "
        "DSX-SPEC-082), so no mitigation can be admissible for it — correct "
        "the spelling to a member of INTERFERENCE_RISKS, or declare "
        "interference.risk: none if no interference risk actually applies."
    )
```

### WR-02: `design.alpha: 0` is silently replaced by the 0.05 default in the monitoring-discipline check

**File:** `dsx/frame/paradigm.py:219`

**Issue:**

```python
alpha = as_number(get(spec, "design.alpha")) or 0.05
```

`as_number(0)` returns `0.0`, and `0.0 or 0.05` evaluates to `0.05` in
Python because `0.0` is falsy — an explicitly declared `design.alpha: 0`
is silently discarded and replaced by the default, identically to an
undeclared `design.alpha`. This only affects the DSX-PAR-010 reference-value
text (the `inflated_alpha_at_5_looks`/`_at_20_looks` figures and the
"at a nominal alpha of {alpha:.2f}" sentence), never the finding's
fire/no-fire decision, so it is not a blocking-severity defect — but it is a
genuine correctness gap in output the operator reads to judge the size of
the problem. `alpha: 0` is not a meaningful significance level in practice,
so the practical blast radius is small, but the code has no guard rejecting
it either, so the silent substitution is the only thing standing between a
malformed declaration and a wrong number in a CRITICAL finding's own detail
text.

**Fix:** Use an explicit `None` check instead of `or`:

```python
raw_alpha = as_number(get(spec, "design.alpha"))
alpha = raw_alpha if raw_alpha is not None else 0.05
```

## Info

### IN-01: Inconsistent empty-collection default style between the two admissible-set lookups

**File:** `dsx/frame/interference.py:210` and `dsx/frame/interference.py:350`

**Issue:** `_check_interference_unaddressed`'s remedy computes
`_RISK_MITIGATION_MAP.get(normalized_risk, ())` (bare tuple default), while
`_check_interference_mitigation_admissibility`'s judgment point computes
`_RISK_MITIGATION_MAP.get(normalized_risk, frozenset())` (frozenset
default) three lines later for the same map. Both are iterated by
`sorted(...)` so the behavioural difference is nil, but the inconsistency
reads as accidental rather than deliberate, in a module whose whole style is
otherwise scrupulously explicit about typed defaults.

**Fix:** Use `frozenset()` in both call sites for consistency with the
module's declared type alias (`"dict[str, frozenset[str]]"` at line 62).

---

_Reviewed: 2026-08-14T00:00:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep_
