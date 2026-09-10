---
phase: 27
phase_name: Evidence case — feature-origin-only leak
milestone: v2.6
unit: S3-3 (D-13 measurement spike — citation-independent portion)
measured: 2026-09-07
interpreter: CPython 3.12.10 (real)
verdict: LIVE MISS — §6.5 item 7 entry condition MET; mint PARKED on HQ-40 row 40b (Kaufman)
codes_minted: 0
---

# Phase 27 — MEASUREMENT (D-13 measured-first, S3-3 spike)

This records the **citation-independent** four-point measurement the prior firing's
persona round (D-27-00) authorised ahead of the Kaufman read. The case shape
(D-27-01) and the pass/fail rule (D-27-02) were **frozen in `27-CONTEXT.md` before
this measurement began** (guardrail 1: FREEZE-BEFORE-MEASURE); nothing here edits
them. Reproduce with:

```
python .planning/phases/27-evidence-case-feature-origin-only-leak/spike/feature-origin-leak-MEASURE.py
```

## Fixture (spike, NOT a committed corpus fixture)

`spike/feature-origin-leak-ANALYSIS-SPEC.yaml` + `spike/feature-origin-leak-entrypoint.py`.
The non-model blocks are cloned wholesale from the measured-passing sibling
`examples/known-bad/full-frame-cleaning-ANALYSIS-SPEC.yaml`, so the incidental
corpus-gap profile matches a known baseline and the **only** new property under test
is feature origin. The model block is honest and complete on every axis a check can
read — temporal split with disjoint declared periods, `preprocessing_fit_on:
train_only`, a complete `selection_ledger`, a beaten baseline, honest `train_score`
AND `test_score`, declared calibration — and the entrypoint has **no** code-defect
idiom (a recognised `TimeSeriesSplit` precedes the pipeline `fit(X_train, …)`; no
full-frame cleaning, no scaler-before-split, no test-sees-target). The leaky column
`account_health_index` matches **none** of the 10 `LEAKAGE_PATTERNS`; the defect
lives in how it was constructed upstream (recomputed nightly from activity that
includes the outcome window), which no gate-path check can see.

## Four-point measurement — LEAKY spec (`account_health_index`), verbatim

Each gate point run from a fresh `tempfile.TemporaryDirectory()` as `--phase-dir`,
entrypoint seeded into it, plan-time decision header seeded for verify/ship (exactly
what `tests/test_known_bad_corpus.py::_gate_findings` automates). CRITICAL/HIGH only.

| Gate point | Exit | CRITICAL | HIGH |
|---|---|---|---|
| `dsx validate` | 0 | — | — |
| `dsx gate plan` | 0 | — | `DSX-MET-040` |
| `dsx gate execute` | 0 | — | — |
| `dsx gate verify` | 1 | — | `DSX-CLM-031`, `DSX-COH-031`, `DSX-MET-040` |
| `dsx gate ship` | 1 | — | `DSX-CLM-031`, `DSX-COH-031`, `DSX-MET-040`, `DSX-NAR-001` |

**`plan` and `execute` — the two gate points where the `ml` and `code` leakage-
detection checks are registered (`dsx/cli.py::GATE_PROFILES`) — both exit 0.** The
`ml` check ran fully and emitted **zero findings**; its passed-checks include, verbatim:

```
OK | temporal data uses 'temporal' split
OK | train and test periods are disjoint
OK | preprocessing fitted on train_only
OK | 7 features screened, no leakage patterns matched   ← the leaky column, positively cleared
OK | primary metric 'pr_auc' suits a 18.0% minority class
OK | model beats baseline by 133.3%
OK | model selection basis declared: 'validation'
OK | train/test gap 0.030 within tolerance
OK | calibration addressed
```

This is a **positive clearance**, not a check that failed to run: the leakage screen
inspected all 7 features including `account_health_index` and declared them clean.

## D-27-02 swap-still-fires counterfactual (applied by literal code)

Re-measured an honest-swap variant, identical except `account_health_index` →
the honestly-available `avg_session_minutes`. Result at every one of the five points:
**identical CRITICAL/HIGH finding-code set** (see the `_swap` run in `MEASURE.py`
output). No code fires for the leaky spec that does not also fire for the honest one
⇒ **no residual code is a catch of the feature-origin leak**; each is incidental to it.

The four verify/ship residuals — `DSX-CLM-031` (unresolvable evidence pointer),
`DSX-COH-031` (unchecked assumption), `DSX-MET-040` (warehouse metric with no
declared SQL), `DSX-NAR-001` (missing `narrative.path`) — are exactly the documented
`_INCIDENTAL_GAP_CODES` of the sibling `full-frame-cleaning` fixture, all HIGH
corpus-completeness gaps, none about feature origin.

## Verdict

**LIVE MISS.** All four gate points return a pass verdict on the merits of the target
defect (validate/plan/execute clean; verify/ship blocked only by swap-invariant
documented corpus-gap codes). After subtracting those, nothing flags the
feature-origin leak. Per D-27-02 this is the **§6.5 item 7 entry condition MET** — a
real, documented gap: an honest, well-formed churn spec whose one defect (a feature
whose value depends on the outcome window, under an innocuous name) sails through the
entire `ml`/`code` leakage-detection surface.

## What this unit did NOT do (hard stop at the mint boundary — guardrail 3)

The measurement confirms a live miss, so per D-27-02 and guardrails 2–3 the firing
**stops at the mint boundary**. It did NOT: author the `model.feature_provenance[]`
check, write its Kaufman docstring, activate `DSX-ML-034`, or add any harness entry.
All of that stays **PARKED on HQ-40 row 40b (Kaufman 2012 TKDD)** — a D-05 human read.
The `DSX-ML-034` reserve (D-27-03) and its D-06 veto window are unchanged.

**Phase 27 is now blocked on HQ-40 row 40b for everything downstream** (S3-1
completion, S3-2 plan of the mint, the S3-3 mint, S3-4, S3-5). The citation-
independent measurement — the one thing that could be settled without the read — is
done and recorded here.
