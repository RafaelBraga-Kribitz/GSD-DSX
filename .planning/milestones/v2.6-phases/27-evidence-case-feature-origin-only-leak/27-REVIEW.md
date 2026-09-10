---
phase: 27-evidence-case-feature-origin-only-leak
reviewed: 2026-09-07T00:00:00Z
depth: deep
diff_base: dd930af
files_reviewed: 16
files_reviewed_list:
  - dsx/checks/ml.py
  - examples/known-bad/feature-origin-only-leak-ANALYSIS-SPEC.yaml
  - examples/known-bad/feature-origin-only-leak-ATTRIBUTION.yaml
  - examples/known-bad/feature-origin-only-leak-POSTMORTEM.md
  - examples/known-bad/feature-origin-only-leak-entrypoint.py
  - references/finding-codes.md
  - scripts/gen-finding-catalogue.py
  - tests/test_causal_verb_golden.py
  - tests/test_dsx.py
  - tests/test_finding_catalogue_invariant.py
  - tests/test_frame_val.py
  - tests/test_gen_finding_catalogue.py
  - tests/test_known_bad_corpus.py
  - tests/test_ml_feature_provenance.py
  - tests/test_p19_categorical_rows.py
  - tests/test_phase20_zero_mint_close.py
findings:
  blocker: 0
  critical: 0
  warning: 1
  info: 2
  total: 3
status: issues_found
---

# Phase 27: Code Review Report

**Reviewed:** 2026-09-07
**Depth:** deep (cross-file: catalogue generator, D-05 enforcement, corpus/golden/count harness, live gate run)
**Files Reviewed:** 16 source/test files in `dd930af..HEAD`
**Status:** issues_found (0 HIGH, 1 MEDIUM, 2 LOW)

## Summary

The DSX-ML-034 mint is sound and honest. I dumped every diff, read the full
`_check_feature_provenance` in context, ran the check's own unit suite, the
catalogue `--check` (D-05 enforcement), and the corpus / golden-ship / count
harness (712 tests + 2111 subtests green), and re-derived the six load-bearing
invariants against the code rather than the SUMMARY files. All six HOLD.

No BLOCKER and no HIGH findings. The check is deliberately narrow —
declaration-only "attribution, not detection" — which is documented candidly and
is not a crippled-to-fake-a-miss design. The one MEDIUM is a genuine robustness
gap: the branch structure silently clears any `available_at` value that is not a
literal recognised token (including missing / null / typo'd), so an omitted
availability is *more permissive* than an honest `unknown`, which is a trivial
one-character bypass of the `unknown`→HIGH intent. The docstring also overstates
this as a "membership test", which the code does not actually enforce.

## Load-bearing invariants — verdicts

**1. DSX-ML-034 D-05 compliance — HOLDS.**
`dsx/checks/ml.py:547-562` carries a `Citation:` line (Kaufman, Rosset, Perlich &
Stitelman 2012, TKDD 6(4) art. 15, DOI `10.1145/2382577.2382579` — DOI verified
correct) and a `Structural criterion:` line (`ml.py:563`). The `# D-05: DSX-ML-034`
marker is present in `tests/test_ml_feature_provenance.py:20`, and the code is in
`_D05_ALLOWLIST_CODES` (`scripts/gen-finding-catalogue.py:209`) by exact code, not
prefix. `python scripts/gen-finding-catalogue.py --check` exits 0 ("finding
catalogue is current"). Wording is correct on the citation-honesty axis: the
docstring says "secondary-corroborated across independent indexes; the primary ACM
Digital Library PDF was paywalled and was not read first-hand in this session, so
no section or page locator is asserted (do not invent one)" (`ml.py:559-562`) and
the test marker echoes "secondary-corroborated, primary PDF paywalled". No
first-hand primary-PDF read is claimed anywhere; no page/section locator is
invented. NOT an overclaim.

**2. Catalogue set-identity 276 -> 277 — HOLDS.**
Exactly one new row (`references/finding-codes.md:163`, DSX-ML-034 CRITICAL). Total
line 276->277 (`finding-codes.md:16`). Count pins updated consistently and in
lockstep: `test_finding_catalogue_invariant.py` `_EXPECTED_TOTAL` 276->277 + method
renamed to `_stays_at_277` + `_MINTED_CODES` gains `DSX-ML-034`;
`test_p19_categorical_rows.py` 277; `test_phase20_zero_mint_close.py` 277;
`test_dsx.py` spec count 42->43; `test_gen_finding_catalogue.py` pins both
declarations. Two `report.add("DSX-ML-034")` sites only (`ml.py:588`, `ml.py:607`);
last-in-AST-order wins the single catalogue row and it rendered CRITICAL as
intended. Live catalogue `--check` green.

**3. DSX-ML-034 OUT of `_SECTION_65_BACKLOG_CODES` — HOLDS.**
`tests/test_known_bad_corpus.py:832-837` contains only DSX-PAR-020/021/022/030.
DSX-ML-034 is absent. The invariant test at `:1620` asserts
`_SECTION_65_BACKLOG_CODES & catalogue == set()` and passes — since DSX-ML-034 now
ships in the catalogue, its presence in the backlog set would fail that test; it is
correctly not there. Minted, not reserved.

**4. `dsx/checks/dq.py` byte-frozen — HOLDS.**
`git diff dd930af..HEAD -- dsx/checks/dq.py` is empty. The mint lives in `ml.py`.
Profiler-is-a-producer rule respected.

**5. Fixture stays a MISS (honest, not crippled) — HOLDS.**
`examples/known-bad/feature-origin-only-leak-ANALYSIS-SPEC.yaml` declares no
`feature_provenance` / `available_at` key (grep: no match), so
`_check_feature_provenance` hits the early return at `ml.py:576` and emits nothing.
The golden-ship set is `{DSX-CLM-031, DSX-COH-031, DSX-MET-040, DSX-NAR-001}` with
DSX-ML-034 deliberately absent (`test_causal_verb_golden.py:171-173`);
`_EXPECTED_CAUGHT_DEFECTS["feature-origin-only-leak"] = frozenset()`
(`test_known_bad_corpus.py:550`); `_EXPECTED_VAL_CODES[...] = set()`
(`test_frame_val.py:1473`). The gap is structural and honest: the check reads a
declaration the honest fixture never makes; it is not a detector throttled to feign
silence. The ATTRIBUTION sidecar's `promotes_backlog_item:
6.5-item-7-feature-provenance` is a member of `_SECTION_65_ITEM_IDS`
(`test_known_bad_corpus.py:852`) and `absent_code: DSX-ML-034` is now in the
validated union, so the miss-falsifiability assertion (absent_code must fire
NOWHERE CRITICAL) passes. All corpus/frame/golden tests green.

**6. `_check_feature_provenance` correctness + wiring — HOLDS (with the MEDIUM below).**
Wired into the ml dispatch at `ml.py:149`, so it can fire in production; the ml
check runs at `plan` and `execute` where CRITICAL blocks (per 27-MEASUREMENT.md),
so an `after_prediction` declaration is reachable and gate-effective. It implements
the cited legitimacy criterion as an `available_at` disposition test
(after_prediction -> CRITICAL, unwaived unknown -> HIGH, before/at -> clear).
False-positive risk is near-zero (it only fires on a self-incriminating
declaration). The one defect is the robustness gap in MED-01 — a false-*negative*
on off-vocabulary/omitted values — not a wiring or logic failure on the recognised
tokens. The firing unit tests (`test_after_prediction_fires_critical`,
`test_unknown_without_waiver_fires_high`) exercise real behaviour and would fail if
the branch logic were wrong, so the suite is not tautological.

## Warnings (MEDIUM)

### WR-01: Off-vocabulary / missing / null `available_at` is silently cleared — an omitted value is more permissive than an honest `unknown`

**File:** `dsx/checks/ml.py:578-625`
**Issue:** `available_at = normalize(entry.get("available_at", ""))` then a chain of
equality branches: `== "unknown"` (HIGH), `== "after_prediction"` (CRITICAL),
`in ("before_prediction","at_prediction")` (ok). There is no terminal `else`.
Consequently every value that is not one of those four recognised tokens is
silently dropped — no finding, no `ok`:
- an entry that **omits** `available_at` → `normalize("")` = `""` → silent;
- an entry with `available_at:` **null** in YAML → `entry.get(...,"")` returns
  `None` → `normalize(None)` = `"none"` → silent;
- a **typo'd** self-incriminating value, e.g. `available_at: post_prediction` or
  `after-pred` → silent.

This inverts the intended incentive: an analyst who honestly writes `unknown` is
flagged HIGH, but one who simply leaves `available_at` off the entry (or typos it)
sails through with zero findings. That is a one-token bypass of the entire
`unknown`→HIGH attribution the check exists to provide. It also contradicts the
docstring, which asserts (`ml.py:563-565`) DSX-ML-034 is "a membership test of each
entry's declared, normalised available_at value against that closed vocabulary" —
the code performs *selected-member equality*, not membership, so out-of-vocabulary
values are neither cleared as legitimate nor flagged as unattested.
**Why it matters:** the phase's own frame — "attribution, not detection; a frame
that lies passes" — is defensible for a spec that omits the whole block. But here
a spec that *does* declare the block, per-feature, and then leaves one entry's
availability blank or misspelled is exactly the case the check claims to attribute,
and it escapes. The gap is inside the declared surface the check owns.
**Fix:** add a terminal branch so any non-empty unrecognised token, and the
empty/null case, are treated as unattested — i.e. routed through the same
waiver-suppressible HIGH path as `unknown` (or a distinct "unrecognised
available_at" HIGH). Sketch:
```python
        if available_at == "after_prediction":
            report.add("DSX-ML-034", "CRITICAL", ...)   # keep CRITICAL last for the catalogue row
        elif available_at in ("before_prediction", "at_prediction"):
            report.ok(f"feature '{feature}' declared available_at '{available_at}'")
        elif entry.get("waiver"):
            report.ok(f"feature '{feature}' available_at '{available_at or 'unattested'}' waived")
        else:
            # unknown, blank, null, or off-vocabulary all mean "not attested"
            report.add("DSX-ML-034", "HIGH",
                f"Feature '{feature}' has no attested available_at "
                f"(declared: {available_at or 'missing'!r})", ...)
```
Note the reorder puts CRITICAL last to preserve the last-write-wins catalogue row
disposition documented at `ml.py:580-585`; if you keep the current order instead,
regenerate `references/finding-codes.md` and re-check the rendered severity. Add
unit cases for missing-key, null, and a typo'd token.

## Info (LOW)

### IN-01: `waiver` truthiness is not validated as a justification

**File:** `dsx/checks/ml.py:587`
**Issue:** `not entry.get("waiver")` suppresses the `unknown`→HIGH finding on *any*
truthy value, so `waiver: true` (a bare boolean with no rationale) silences the
finding even though the remedy text (`ml.py:598-601`) asks the analyst to "record a
waiver justifying the unknown". A waiver with no justifying content defeats the
audit purpose of the waiver.
**Why it matters:** low — it is a self-declaration surface and the standing "a
frame that lies passes" limit already applies. But `waiver: true` is a weaker bar
than the intent.
**Fix:** optionally require the waiver to be a non-empty string (or a
`{by, date, rationale}` shape) before it suppresses; emit the HIGH otherwise. If
the bare-boolean contract is intentional, tighten the remedy wording to say so.

### IN-02: Source-order code comment says the CRITICAL branch is "nested one level deeper" — it is not

**File:** `dsx/checks/ml.py:583`
**Issue:** the comment states the `after_prediction`/CRITICAL branch is written
"SECOND (nested one level deeper)". In the actual code the HIGH `if` (`:587`) and
the CRITICAL `elif` (`:606`) are siblings at the same indentation inside the `for`
loop — the CRITICAL branch is second in source order but *not* nested deeper. The
load-bearing fact (last-in-source wins the single catalogue row → CRITICAL renders)
is correct and verified against `references/finding-codes.md`; only the
"nested one level deeper" phrasing is wrong.
**Why it matters:** purely a comment accuracy issue; a future editor trusting the
comment could misjudge the control flow. No behavioural impact.
**Fix:** drop "(nested one level deeper)"; the branch is a sibling `elif`, second in
source order.

## Observations (not defects)

- The falsifiability of *this* miss is structurally weaker than the three prior
  miss sidecars: because DSX-ML-034 is declaration-only, it is silent-by-construction
  on any spec lacking a `feature_provenance` block, so the "fires NOWHERE CRITICAL"
  assertion passes regardless of whether the underlying leak is real. This is
  disclosed candidly in the ATTRIBUTION sidecar and SUMMARY ("attribution, not
  detection"), and the *detection* gap it motivates (§6.5 item 7) remains a genuine
  miss. Recorded for the record; not a code defect.
- `examples/known-bad/feature-origin-only-leak-entrypoint.py` is never executed by
  the gate (read as text only); it is syntactically valid and internally coherent
  (`train_score`/`test_score` computed, temporal split precedes fit). Runnability is
  not a gate requirement here, so no finding.

---

_Reviewed: 2026-09-07_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep_
