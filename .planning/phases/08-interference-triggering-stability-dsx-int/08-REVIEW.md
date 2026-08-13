---
phase: 08-interference-triggering-stability-dsx-int
reviewed: 2026-08-13T00:00:00Z
depth: deep
files_reviewed: 19
files_reviewed_list:
  - dsx/cli.py
  - dsx/frame/interference.py
  - dsx/frame/paradigm.py
  - dsx/mathx.py
  - dsx/spec.py
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
  critical: 1
  warning: 4
  info: 2
  total: 7
status: issues_found
---

# Phase 8: Code Review Report

**Reviewed:** 2026-08-13T00:00:00Z
**Depth:** deep
**Files Reviewed:** 19
**Status:** issues_found

## Summary

`dsx/frame/interference.py` (DSX-INT-010/011/030/040), the new `dsx.mathx.diluted_effect`
helper, and the accompanying corpus fixtures/tests are, on the whole, carefully built:
the malformed-shape hardening is real and mechanically proven (AST scan for `try`/`except`,
a full malformed-shape matrix), the DSX-INT-010/DSX-INT-030 disjointness claims hold up
under trace, the additive/ratio metric partition is a correct, tested subset of
`METRIC_TYPES`, and the `weak-identification-mmm` fixture's newly-added DSX-INT-030
co-firing is a real, deliberate, well-documented second defect rather than a false
positive.

That said, adversarial tracing through the admissibility logic surfaced one real gate
bypass: **an out-of-vocabulary `interference.mitigation` value silently defeats both
DSX-INT-010 and DSX-INT-011**, so a spec with a declared, unaddressed interference risk
can clear `dsx gate plan` (CRITICAL threshold) just by misspelling the mitigation field —
exactly the "cheapest way past the gate" failure mode this codebase is explicit about
avoiding elsewhere (e.g. `dsx/frame/paradigm.py`'s D-10 commentary). No test exercises
this path. Three further items degrade confidence in the corpus's own guarantees and
test coverage without being runtime bugs: a documented-but-unenforced positive claim in
`tests/test_known_bad_corpus.py`, a tautological unit test in `tests/test_dsx.py` that
never calls the function it claims to verify, and an asymmetry between the corpus's two
per-fixture expectation maps' completeness guards.

## Critical Issues

### CR-01: DSX-INT-010/DSX-INT-011 are both silently bypassed by an out-of-vocabulary `interference.mitigation` value

**File:** `dsx/frame/interference.py:172` (also `dsx/frame/interference.py:277`)

**Issue:** `_check_interference_unaddressed` only treats a mitigation as "absent" when it
normalizes to the literal string `"none"`:

```python
normalized_mitigation = normalize(mitigation) if not is_blank(mitigation) else "none"
mitigation_absent = normalized_mitigation == "none"
```

`_check_interference_mitigation_admissibility` independently requires the mitigation to
already be a *recognised* member of `INTERFERENCE_MITIGATIONS` before it will judge
admissibility at all:

```python
if normalized_mitigation == "none" or normalized_mitigation not in INTERFERENCE_MITIGATIONS:
    return
```

Trace a spec that declares a real risk (`interference.risk: shared_budget`), a
**misspelled** mitigation (`interference.mitigation: buget_isolation`, missing the `d`),
and a blank `residual_note`:

- `_check_interference_unaddressed`: `normalized_mitigation = "buget_isolation"` ≠
  `"none"` ⇒ `mitigation_absent = False` ⇒ `unaddressed = False`. **DSX-INT-010 does not
  fire.**
- `_check_interference_mitigation_admissibility`: `"buget_isolation" not in
  INTERFERENCE_MITIGATIONS` ⇒ the guard returns immediately. **DSX-INT-011 does not
  fire.**
- The only finding produced anywhere is `dsx/spec.py`'s `DSX-SPEC-082`
  (`validity_frame.interference.mitigation 'buget_isolation' is not recognised`), which
  is **HIGH**, not CRITICAL — and `GATE_THRESHOLDS["plan"] == "CRITICAL"`
  (`dsx/cli.py:107-112`), so `dsx gate plan` **exits 0**.

The result: a spec with a declared, structurally unaddressed interference risk (no
working mitigation, no residual note — functionally identical to the
`interference-shared-budget` known-bad fixture) clears the CRITICAL-threshold `plan`
gate purely because the mitigation string doesn't exactly match a vocabulary entry. A
single typo is strictly *safer*, gate-wise, than honestly writing `mitigation: none`.
This is the inverse of `dsx/frame/paradigm.py`'s explicit D-10 guarantee ("an
unsupported or undeclared paradigm must not be the cheapest way past the gate") applied
to the interference family. No test in `tests/test_frame_interference.py` exercises an
out-of-vocabulary `interference.mitigation` on a real, declared risk — the gap is
untested as well as unfixed.

**Fix:** Treat "not a recognised, admissible-in-principle mitigation" as equivalent to
"absent" for DSX-INT-010's purposes, so an out-of-vocabulary mitigation still leaves the
risk judged unaddressed (DSX-SPEC-082 keeps firing independently for the vocabulary
violation itself — the two findings describe different facts and are not a double
report of the same defect):

```python
# dsx/frame/interference.py, _check_interference_unaddressed
mitigation = get(frame, "interference.mitigation")
residual_note = get(frame, "interference.residual_note")
normalized_mitigation = normalize(mitigation) if not is_blank(mitigation) else "none"
mitigation_absent = (
    normalized_mitigation == "none"
    or normalized_mitigation not in INTERFERENCE_MITIGATIONS
)
residual_missing = is_placeholder_or_refusal(residual_note)
unaddressed = mitigation_absent and residual_missing
```

Add a regression test (e.g. `test_out_of_vocabulary_mitigation_with_blank_residual_still_fires_int_010`)
asserting `DSX-INT-010` fires for `_causal_spec(mitigation="buget_isolation")`.

## Warnings

### WR-01: The "weak-identification-mmm blocks on DSX-INT-030 at verify/ship" guarantee is never mechanically checked

**File:** `tests/test_known_bad_corpus.py:135` (also `:392-425`, `:427-468`)

**Issue:** `_TARGET_DEFECT_CODES["weak-identification-mmm"]` carries `{"plan":
"DSX-VAL-040", "verify": "DSX-INT-030"}`, and the surrounding commentary (lines 105-133)
extensively documents this as a "resolved fragility" — DSX-INT-030 is claimed to fire
for this fixture at plan, verify and ship. But:

- `test_every_spec_blocks_only_on_its_target_defect_at_critical_threshold_points`
  (the only test that calls `_classify_target_defect` with a real gate run) iterates
  `for point in _CRITICAL_THRESHOLD_POINTS`, and `_CRITICAL_THRESHOLD_POINTS = ("plan",
  "execute")` (line 53) — `"verify"` is never one of the `point` values passed in, so
  the `"verify": "DSX-INT-030"` entry is never used to positively assert that DSX-INT-030
  actually appears among the CRITICAL findings at any real gate invocation.
- `test_ship_gate_findings_are_all_documented_incidental_corpus_gaps` (lines 427-468)
  only checks the *complement* direction — that every CRITICAL/HIGH finding produced at
  `ship` is *allowed* (documented or the fixture's own target code). It does not assert
  that DSX-INT-030 is *present*. If a future change silently stopped DSX-INT-030 from
  firing for this fixture (e.g. the CR-01 fix applied incorrectly, or a regression in
  the additive-metric loop), `blocking` would simply shrink and this test would keep
  passing.
- `test_incidental_allowlist_names_no_slugs_own_target_code` (line 479) has the same
  one-directional shape: it only forbids a target code from being in
  `_INCIDENTAL_GAP_CODES`, it never asserts the code was actually observed firing.

No test anywhere under `tests/` invokes `dsx gate verify` or `dsx gate ship` against
`weak-identification-mmm-ANALYSIS-SPEC.yaml` and asserts `"DSX-INT-030"` is among the
returned findings (confirmed by grep across `tests/`). The positive half of this
fixture's documented guarantee is asserted only in prose.

**Fix:** Add a positive gate-level test mirroring
`tests/test_frame_val.py::TestValGateIntegration`, e.g.:

```python
def test_weak_identification_mmm_fixture_blocks_verify_and_ship_naming_int_030(self):
    for point in ("verify", "ship"):
        code, findings = self._gate_findings(
            ROOT / "examples" / "known-bad" / "weak-identification-mmm-ANALYSIS-SPEC.yaml",
            point,
        )
        self.assertEqual(code, 1)
        self.assertIn(
            "DSX-INT-030", {f["code"] for f in findings if f["severity"] == "CRITICAL"}
        )
```

### WR-02: `test_diluted_effect_naive_and_true_values_differ_for_time_to_success` never calls `dsx.mathx.diluted_effect`

**File:** `tests/test_dsx.py:162-170`

**Issue:** The test's name and docstring claim to assert "the additive-only scope
boundary REQ-P8-04 demands" against the published Deng & Hu counterexample, but the body
is:

```python
def test_diluted_effect_naive_and_true_values_differ_for_time_to_success(self):
    # Deng & Hu (2015) section 2.1: ...
    naive_msec = -18.0
    true_msec = -26.0
    self.assertNotEqual(naive_msec, true_msec)
```

This never invokes `mathx.diluted_effect` (or any other code under test). It is a
tautology — `-18.0 != -26.0` is true regardless of anything in the repository — so it
provides zero verification of `diluted_effect`'s scope boundary despite its name
implying otherwise (matches the phase-context concern: "any place a test asserts
something weaker than its docstring claims").

**Fix:** Either delete the test (the comment can move to
`dsx.mathx.diluted_effect`'s docstring, where the same UNVERIFIED-inputs caveat is
already stated), or make it actually exercise the boundary it claims to check, e.g.
assert that `diluted_effect` is undefined/inapplicable for a ratio-typed dilution
scenario by pointing at `interference._RATIO_METRIC_TYPES`/`_ADDITIVE_METRIC_TYPES`
directly rather than restating two hardcoded literals.

### WR-03: DSX-INT-030's metric-type loop treats an explicit `type: null` differently from an absent `type` key

**File:** `dsx/frame/interference.py:403-425`

**Issue:**

```python
mtype = normalize(metric.get("type", ""))
if not mtype:
    ... append a "skip: no declared type" DecisionRecord ...
    continue
```

`metric.get("type", "")` only returns the `""` default when the `type` key is entirely
absent. If a metric declares `type: null` in YAML (parses to Python `None`, key present),
`metric.get("type", "")` returns `None`, and `normalize(None)` is `str(None).strip()
.lower()` → the truthy string `"none"`. `if not mtype:` is then `False`, so this metric
skips the documented "no declared type" path (and its `DecisionRecord`) entirely, falls
through the `if mtype in _ADDITIVE_METRIC_TYPES:` check (false, since `"none"` isn't a
member), and lands silently in the "ignored" branch with **no decision record at all** —
contradicting the docstring's claim that "one `DecisionRecord` naming the skip and its
reason is appended for each" undeclared-type metric. No finding is produced either way,
so this is a decision-trail completeness gap rather than an incorrect block/pass, but it
is a real behavioral inconsistency between two inputs (`type` absent vs. `type: null`)
that should be identical under the check's own stated model.

**Fix:**

```python
raw_type = metric.get("type")
mtype = normalize(raw_type) if not is_blank(raw_type) else ""
```

so an explicit `null`/blank `type` is treated identically to an absent one.

### WR-04: `_TARGET_DEFECT_CODES` has no on-disk completeness guard, unlike its sibling map

**File:** `tests/test_known_bad_corpus.py:134-138` (contrast with `:490-502`)

**Issue:** `_EXPECTED_CAUGHT_DEFECTS` is protected by
`test_expected_caught_defects_keys_match_the_corpus_on_disk`, which fails loudly if the
map's keys and the fixtures discovered by glob ever diverge (a fixture added without an
entry, or an entry naming a fixture no longer on disk). `_TARGET_DEFECT_CODES` — the
other of the two maps `_effective_target_map()` combines, and the one carrying the
point-scoped `DSX-VAL-040`/`DSX-INT-010`/`DSX-INT-030` guarantees — has no equivalent
test. If `weak-identification-mmm-ANALYSIS-SPEC.yaml` (or either of the other two keyed
fixtures) were ever renamed or removed, the corresponding `_TARGET_DEFECT_CODES` entry
would become an orphaned, silently-inert dict entry: `_classify_target_defect` would
simply find no matching slug on disk, the renamed fixture would default to "clears
cleanly" in `test_every_spec_blocks_only_on_its_target_defect_at_critical_threshold_points`,
and the loss of the `DSX-VAL-040 at plan` guarantee would go unnoticed by any test —
precisely the "silently weakened guarantee" failure mode this module's own comments
(lines 90-138, 244-253) are otherwise careful to call out and guard against for the
sibling map.

**Fix:** Add a symmetrical guard, e.g.:

```python
def test_target_defect_codes_keys_are_a_subset_of_the_corpus_on_disk(self):
    disk_slugs = _slugs(f"*{SPEC_SUFFIX}", SPEC_SUFFIX)
    stale = set(_TARGET_DEFECT_CODES) - disk_slugs
    self.assertEqual(
        stale, set(),
        f"_TARGET_DEFECT_CODES names fixture(s) no longer on disk: {sorted(stale)}",
    )
```

## Info

### IN-01: Quoted-string YAML booleans silently defeat the strict identity checks

**File:** `dsx/frame/interference.py:390-396`, `:558-564`

**Issue:** Both `dilution_adjusted is not True` and `novelty_primacy_assessed is not
True` are deliberate, documented identity comparisons (never `is_blank()`) so that the
literal boolean `false` still fires. That same strictness means a *quoted* YAML scalar
(`dilution_adjusted: "true"`, parsed as the Python string `"true"`, not the boolean)
also fails the `is not True` test and fires the check, even though the operator's intent
was clearly "yes, adjusted." This is a pre-existing, codebase-wide convention (the same
pattern appears for other boolean fields outside this module) rather than something
introduced by Phase 8, and the failure mode is "check fires when it arguably shouldn't"
rather than a silent pass, so it is low risk — noted for awareness, not required to fix
in this phase.

### IN-02: `examples/bad-ANALYSIS-SPEC.yaml` now also encodes a live DSX-INT-010 defect, undocumented in its own comments

**File:** `examples/bad-ANALYSIS-SPEC.yaml:224-228`

**Issue:** This pre-Phase-8 general-purpose "bad" fixture declares
`interference.risk: shared_budget`, `mitigation: none`, `residual_note: ""` — the exact
shape `_check_interference_unaddressed` fires on. Since Phase 8 shipped, `dsx gate plan`
against this fixture now also blocks on `DSX-INT-010` in addition to its originally
documented codes, but the fixture's own inline comments (which carefully attribute every
other declared defect to a code, e.g. "`DSX-SPEC-082`", "`COH-031`") say nothing about
this one. This is not a functional bug — the finding is a correct catch of a genuinely
undocumented interference risk in the fixture, and no test asserts an exhaustive finding
set for this file — but the comment block is now stale relative to the fixture's actual
behavior.

**Fix:** Add a one-line comment at `examples/bad-ANALYSIS-SPEC.yaml:224-228` noting the
DSX-INT-010 attribution, matching the file's existing convention for every other
deliberately-encoded defect.

---

_Reviewed: 2026-08-13T00:00:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep_
