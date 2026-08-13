---
phase: 08-interference-triggering-stability-dsx-int
reviewed: 2026-08-13T00:00:00Z
depth: deep
review_type: re-review of gap closure (08-07)
diff_range: e397aa4..8f2933a
files_reviewed: 5
files_reviewed_list:
  - dsx/frame/interference.py
  - tests/test_frame_interference.py
  - tests/test_known_bad_corpus.py
  - tests/test_dsx.py
  - examples/bad-ANALYSIS-SPEC.yaml
findings:
  critical: 2
  warning: 2
  info: 2
  total: 6
status: issues_found
---

# Phase 8: Code Review Report — gap closure (plan 08-07) re-review

**Reviewed:** 2026-08-13T00:00:00Z
**Depth:** deep
**Scope:** `git diff e397aa4..8f2933a -- dsx/ tests/ examples/` (commits `21cdc04`, `f669607`, `7c5cfec`)
**Files Reviewed:** 5
**Status:** issues_found

## Summary

The landed change does what it says on the one field it touches. Every previously-open item is
genuinely closed, and I proved each one mechanically rather than reading the summary:

| Prior finding | Verdict | Evidence |
|---|---|---|
| CR-01 (out-of-vocab `mitigation` bypass) | **Closed** for the `mitigation` field | Reverting only the `mitigation_absent` hunk turns both new tests red (`FAILED (failures=2)`); with the fix, the mutated fixture exits 1 naming `DSX-INT-010` where it previously exited 0 |
| WR-01 (INT-030 verify/ship prose-only) | **Closed** | Sabotaging `fired = not_adjusted` → `fired = False` turns `test_weak_identification_mmm_fixture_blocks_verify_and_ship_naming_int_030` red at both `verify` and `ship` |
| WR-02 (tautological dilution test) | **Partially closed** — see WR-02 below | The rewrite can fail (proven), but still never calls `mathx.diluted_effect` |
| WR-03 (`type: null` decision-trail gap) | **Closed** | Absent key, `null`, `""`, `"   "` and `[]` now all emit one identical skip record; reverting the hunk turns the new test red |
| WR-04 (`_TARGET_DEFECT_CODES` on-disk guard) | **Closed** | Subset guard present and correctly shaped; `_slugs` is glob-based, no CRLF exposure |
| IN-01 | Deferred by decision — not re-raised | Recorded in `08-07-PLAN.md` `<deferrals>` |
| IN-02 | **Closed** | Arrow-comment convention matches the file's 15 other attributions; `dsx.loader.load` still parses the block correctly; `gate plan` still names `DSX-INT-010` |

I also independently verified the executor's documented deviation, and **the executor is right**:
`python3 -m dsx validate --spec examples/bad-ANALYSIS-SPEC.yaml` exits 1 both before and after the
IN-02 comment edit, with a byte-identical finding-code set
(`DSX-SPEC-010, -026, -033, -081, -082, -085`). The plan's acceptance criterion was wrong; the
executor's note is accurate and is not a finding.

Disjointness holds, and for the right reason. `_check_interference_unaddressed` now fires on
`normalized_mitigation == "none" or not in INTERFERENCE_MITIGATIONS`;
`_check_interference_mitigation_admissibility` still guards on the exact complement
(`!= "none" and in INTERFERENCE_MITIGATIONS`), computed from an identical normalization expression
(`interference.py:186` vs `:300`). The two predicates are mutually exclusive by construction, not by
early return. I confirmed this empirically across 22 input classes — `none`, absent, `null`, an
admissible in-vocabulary value, an inadmissible in-vocabulary value, an out-of-vocabulary near-miss,
`int`, `bool` (both `True` and `False`), `list`, `dict`, and case/whitespace/hyphen/space variants of
a valid value — and no input produced both codes. No false positives either: the unedited
`templates/ANALYSIS-SPEC.yaml` and `examples/good-ANALYSIS-SPEC.yaml` both still exit 0 at
`gate plan`, `sh scripts/check.sh` prints `all checks passed`,
`python3 scripts/gen-finding-catalogue.py --check` prints `finding catalogue is current`, and
`python3 -m unittest discover -s tests` reports `Ran 531 tests ... OK (skipped=2)`.

**What is still wrong is that the fix was applied to one field, not to the failure mode.** The
principle the new docstring now asserts in writing — "a mitigation the vocabulary does not contain
cannot be admissible for any risk … treating a misspelling as a declared mitigation made a typo the
cheapest way past this CRITICAL-threshold gate" — is contradicted twelve lines above it by the
`risk` guard, and again in `_check_triggering_dilution`'s `analysis_population` guard. Both are
reachable on committed fixtures with a one-character edit, and both exit 0 at `dsx gate plan`.
Misspelling `mitigation` is no longer cheaper than honesty; misspelling `risk` still is. Separately,
the new gate-level test that is supposed to prove `DSX-SPEC-082` fires *beside* `DSX-INT-010` cannot
fail — the commit that added the test also added the literal string `DSX-SPEC-082` to
`DSX-INT-010`'s own `detail` text, so the assertion is satisfied by prose the same commit wrote.

No new regex or line-oriented parsing was introduced anywhere in the diff (`_mutate_interference`
round-trips through `dsx.loader.load` + `json.dumps`, not text editing), so there is no CRLF
exposure. No citation was invented: the new test comment restates claims already carried verbatim by
`dsx.mathx.diluted_effect`'s existing `Reference value:` paragraph, which I read and cross-checked.

## Critical Issues

### CR-01: The bypass moved one field up — an out-of-vocabulary `interference.risk` still clears `dsx gate plan` with a declared risk, no mitigation and no residual note

**File:** `dsx/frame/interference.py:176-181` (the guard the fix did not touch), in the same function
as the fix at `:187-190`

**Issue:** The fix made an unrecognised `mitigation` count as absent. It left the identically-shaped
guard on `risk` unchanged:

```python
risk = get(frame, "interference.risk")
normalized_risk = normalize(risk) if not is_blank(risk) else "none"
if normalized_risk == "none" or normalized_risk not in INTERFERENCE_RISKS:
    # DSX-SPEC-082 territory (out-of-vocabulary) or the honestly-declared
    # no-risk case; either way there is nothing for this check to judge.
    return
```

`_check_interference_mitigation_admissibility:294-297` carries the same guard. So an
out-of-vocabulary `risk` value returns early from **both** helpers, leaving `DSX-SPEC-082` (HIGH) as
the only finding — below `GATE_THRESHOLDS["plan"] == "CRITICAL"` (`dsx/cli.py`). This is the exact
trace the old CR-01 documented, re-run against the `risk` field.

Reproduced against the committed known-bad fixture (`gate plan`, three variants of
`examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml`, real command output):

```
BASELINE mitigation: none | exit 1 | [... 'DSX-INT-010' ... 'DSX-SPEC-082']
MITIGATION TYPO           | exit 1 | [... 'DSX-INT-010' ... 'DSX-SPEC-082']   <- the fix works
RISK TYPO (shared_buget)  | exit 0 | [...              no DSX-INT-* at all ]  <- still open
```

`gate execute` also exits 0 for the risk-typo variant; `verify` and `ship` block only because their
threshold reaches HIGH and picks up `DSX-SPEC-082`. That is the identical bypass window the previous
CR-01 described.

The inline comment on the `risk` guard ("either way there is nothing for this check to judge") now
directly contradicts the docstring the same commit added twelve lines below it, which states the
opposite policy for `mitigation`. One of the two is wrong, and the module currently ships both.

**Fix:** Apply the same vocabulary-membership-as-declaration treatment to the risk guard. An
unrecognised risk string is not `none` — the author declared *something* — so it should be
adjudicated rather than dropped, exactly as an unrecognised mitigation now is. Because
`_RISK_MITIGATION_MAP` has no cell for it, `admissible_listed` degrades correctly to
`(none admissible)` via the existing `.get(normalized_risk, ())`:

```python
# dsx/frame/interference.py, _check_interference_unaddressed
risk = get(frame, "interference.risk")
normalized_risk = normalize(risk) if not is_blank(risk) else "none"
if normalized_risk == "none":
    # The honestly-declared no-risk case; nothing to judge.
    return
# An out-of-vocabulary risk string is NOT nothing: the author declared a risk
# and spelled it wrong. Dropping it here makes a typo in `risk` cheaper at the
# CRITICAL-threshold gate than writing `risk: none` honestly — the same failure
# mode the mitigation branch below was fixed for. DSX-SPEC-082 still fires
# independently for the vocabulary violation itself.
```

`_check_interference_mitigation_admissibility:296` must keep its `not in INTERFERENCE_RISKS` return
(it has no admissibility cell to consult), which preserves disjointness: an unrecognised risk would
then fire DSX-INT-010 only.

Add regression tests mirroring the ones that closed the mitigation half:
`test_out_of_vocabulary_risk_with_no_mitigation_and_blank_residual_still_fires_int_010`
(`_causal_spec(risk="shared_buget")`) and a gate-level variant asserting exit 1.

### CR-02: The same typo-defeats-the-gate hole is open on `triggering.analysis_population`, defeating DSX-INT-030

**File:** `dsx/frame/interference.py:406-408` (in `_check_triggering_dilution`, the function this
diff edited at `:428-436`)

**Issue:**

```python
population = get(triggering, "analysis_population")
normalized_population = normalize(population) if not is_blank(population) else ""
if normalized_population != "eligible":
    return
```

`ANALYSIS_POPULATIONS` is a closed vocabulary (`{"eligible", "triggered"}`), so an out-of-vocabulary
value is a spec defect, not a declaration of `triggered`. The guard treats it as neither: it returns
before the judgment point, and DSX-INT-030 never fires. `DSX-SPEC-082` (HIGH) fires alone and the
CRITICAL-threshold gates pass.

Reproduced against the committed fixture (`examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml`,
real command output):

```
baseline                                    | exit 1 | DSX-INT-030 present: True
population TYPO (eligible -> eligable)      | exit 0 | DSX-INT-030 present: False
```

The gate output still names `analysis_population` (via `DSX-SPEC-082`), so the operator is told the
string is wrong — but the CRITICAL check the fixture exists to demonstrate is silenced, and
`dsx gate plan` exits 0. This is the same class as CR-01 and it is the second CRITICAL check in this
module a one-character edit can defeat.

I am scoring this Critical on impact rather than diff proximity: the guard predates 08-07, but
`_check_triggering_dilution` is inside the reviewed diff, and the policy the fix's own docstring now
states covers it.

**Fix:** Distinguish "declared something outside the vocabulary" from "declared `triggered`". Fail
closed for the former, matching the mitigation branch:

```python
population = get(triggering, "analysis_population")
normalized_population = normalize(population) if not is_blank(population) else ""
if normalized_population == "triggered" or not normalized_population:
    # Honestly declared as the triggered population, or not declared at all
    # (DSX-SPEC-08x territory) — nothing for this check to adjudicate.
    return
# "eligible" or any unrecognised string: an out-of-vocabulary value is a
# misspelling, not a declaration of `triggered`, and must not be cheaper at the
# gate than writing `analysis_population: eligible` honestly.
```

Add a regression test for `analysis_population="eligable"` asserting DSX-INT-030 fires, and a
gate-level variant asserting exit 1. Update the docstring's firing condition and the
`DecisionRecord.rule` text, both of which currently say `is 'eligible'`.

## Warnings

### WR-01: The new gate-level test's `DSX-SPEC-082` assertion cannot fail — the same commit put the literal string into `DSX-INT-010`'s own detail text

**File:** `tests/test_frame_interference.py:491` (assertion), caused by
`dsx/frame/interference.py:207-211` (detail text added in the same commit, `f669607`)

**Issue:** `test_out_of_vocabulary_mitigation_variant_blocks_plan_naming_both_int_010_and_spec_082`
ends with:

```python
self.assertEqual(code, 1)
self.assertIn("DSX-INT-010", out + err)
self.assertIn("DSX-SPEC-082", out + err)
```

Its comment states the purpose explicitly: "DSX-SPEC-082 must still fire beside DSX-INT-010 — the
vocabulary violation and the unaddressed risk are different facts about the same spec, not a double
report of one." Commit `f669607` also appended this sentence to every DSX-INT-010 finding's `detail`:

> "If the declared mitigation string is not a recognised member of INTERFERENCE_MITIGATIONS,
> **DSX-SPEC-082** also fires on the same input — …"

`out + err` is the rendered text report, which prints `detail`. So the string `DSX-SPEC-082` is in
the output whenever `DSX-INT-010` fires at all — which is the only branch this test reaches.

Proven, real output, comparing the JSON finding list against the text output for the same fixture:

```
UNMUTATED (mitigation: none)          exit=1  real DSX-SPEC-082 findings=0  substring in output=True
MUTATED (mitigation: buget_isolation) exit=1  real DSX-SPEC-082 findings=1  substring in output=True
```

The unmutated fixture produces **zero** `DSX-SPEC-082` findings yet still satisfies the assertion.
If `DSX-SPEC-082` stopped firing for `interference.mitigation` entirely, this test would stay green.

This matters beyond a weak test. This assertion is the sole mechanical evidence for the plan's third
must-have truth ("DSX-SPEC-082 keeps firing independently … reported as two findings, not one defect
reported twice") and for 08-VERIFICATION.md's third `missing:` entry. That guarantee is currently
unasserted — which is precisely the disease the previous review's WR-02 named and this plan set out
to cure.

The secondary effect is worth noting too: putting a finding code inside another finding's `detail`
makes every text-substring assertion in the suite unreliable in both directions. The negative
counterpart at `tests/test_frame_interference.py:363-402`
(`assertNotIn("DSX-INT-030", out.getvalue() + err.getvalue())`) will silently start failing the day
any check's detail text names DSX-INT-030.

**Fix:** Assert against structured findings, not rendered text. `_gate_findings`-style JSON capture
already exists in `tests/test_known_bad_corpus.py:332-353`; use the same shape here:

```python
code, out, err = self._run(
    ["gate", "plan", "--spec", str(spec_path), "--phase-dir", phase_dir, "--json"]
)
self.assertEqual(code, 1)
report = json.loads(err or out)
by_code = {f["code"]: f for f in report["findings"]}
self.assertIn("DSX-INT-010", by_code)
self.assertEqual(by_code["DSX-INT-010"]["severity"], "CRITICAL")
self.assertIn("DSX-SPEC-082", by_code)
# the two findings are about the same field, and are two findings, not one
self.assertEqual(
    by_code["DSX-INT-010"]["where"], "spec.validity_frame.interference.mitigation"
)
```

Consider also making `DSX-INT-010`'s `detail` name the code only when it is actually true (see
IN-01), which removes the source of the contamination.

### WR-02: The rewritten dilution test still never calls `mathx.diluted_effect`; its only novel assertion is a docstring substring grep

**File:** `tests/test_dsx.py:163-178`

**Issue:** `test_diluted_effect_is_scoped_to_additive_metrics_not_the_counterexamples_ratio_metric`
is a real improvement on the tautology it replaced — I confirmed it turns red when `"ratio"` is added
to `_ADDITIVE_METRIC_TYPES`. But the disease the original WR-02 named (a test whose name claims more
than its body asserts) is reduced, not eliminated:

- Nothing in the body touches `mathx.diluted_effect`'s *behaviour*, despite the name. The function is
  never called. It cannot be — `diluted_effect(effect, rate)` takes two floats and has no metric-type
  parameter — but that means the name asserts a scope boundary the function does not enforce and the
  test does not check.
- The two partition assertions are almost entirely subsumed by
  `tests/test_frame_interference.py:320-328`
  (`test_additive_and_ratio_metric_type_partitions_are_subsets_disjoint_and_proper`), which already
  proves the two sets are disjoint subsets of `METRIC_TYPES`, plus
  `test_ratio_scope_boundary_ratio_metric_produces_no_finding` (`:257-261`), which proves the
  behaviour end-to-end. The only thing this test adds that no other test has is the docstring grep.
- The docstring assertions are documentation checks living in a `TestMath` behaviour class, and they
  are substring-loose: `assertIn("-26", docstring)` would pass on any text containing `-26`.

**Fix:** Either rename it to what it actually guards — e.g.
`test_ratio_metric_type_stays_outside_the_additive_partition_and_the_reference_pair_is_recorded` —
or, better, move the two partition assertions out (they belong beside their siblings in
`tests/test_frame_interference.py`) and keep only the docstring-provenance assertion under an honest
name such as `test_diluted_effect_docstring_still_records_the_published_counterexample_pair`. If the
scope boundary is meant to be enforced rather than documented, the enforcement point is
`_ADDITIVE_METRIC_TYPES` and it is already tested; `diluted_effect` itself has no boundary to assert.

## Info

### IN-01: `DSX-INT-010`'s `detail` names `DSX-SPEC-082` unconditionally, including in the common case where it did not fire

**File:** `dsx/frame/interference.py:207-211`

**Issue:** The sentence is emitted for every DSX-INT-010 finding, including the honest
`mitigation: none` case that all four committed fixtures and the template use. In that case no
`DSX-SPEC-082` finding exists (verified: the unmutated `interference-shared-budget` fixture produces
zero), so the operator reading the report sees a code named in the detail that appears nowhere in the
finding list. The sentence is grammatically hedged ("If the declared mitigation string is not …"), so
it is not a false claim — but it is unconditional noise on the majority path, and it is what makes
WR-01's assertion vacuous.

**Fix:** Emit it only when it is true, e.g. build the detail with a conditional suffix keyed on
`normalized_mitigation not in INTERFERENCE_MITIGATIONS`. That also removes the string from the output
of the common case, so a text-substring assertion on `DSX-SPEC-082` would become meaningful again.

### IN-02: `assertIn("-26", docstring)` fails under `python -OO`

**File:** `tests/test_dsx.py:175-178`

**Issue:** `python3 -OO` strips docstrings; `mathx.diluted_effect.__doc__` is then `None`, the
`or ""` fallback yields an empty string, and all three `assertIn` calls fail. Verified:

```
$ python3 -OO -c "from dsx import mathx; print('doc under -OO:', repr(mathx.diluted_effect.__doc__))"
doc under -OO: None
```

Nothing in this repo currently runs tests under `-OO`, so this is informational only.

**Fix:** Guard with `@unittest.skipIf(mathx.diluted_effect.__doc__ is None, "docstrings stripped")`,
or read the reference pair from a module-level constant rather than from `__doc__`.

---

_Reviewed: 2026-08-13T00:00:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep — re-review of gap closure `e397aa4..8f2933a`_
