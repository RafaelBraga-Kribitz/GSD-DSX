# Post-mortem: a feature-origin-only leak under an innocuous name

Paired spec: `feature-origin-only-leak-ANALYSIS-SPEC.yaml`
Paired entrypoint: `feature-origin-only-leak-entrypoint.py`

## What was concluded

A retention-analytics team built a churn-risk model to flag at-risk customers for a
retention-outreach experiment. The specification is honest on every axis a gate-path
check can read: a temporal split with disjoint declared train and test periods,
`model.preprocessing_fit_on: train_only`, a complete `model.selection_ledger` (three
candidates evaluated, twenty-four configurations tried, selected on validation), a
baseline beaten by 133%, honest `train_score` *and* `test_score` with the gap inside
tolerance, and a declared isotonic calibration. The paired entrypoint is deliberately
clean — a forward-chaining `TimeSeriesSplit` precedes the pipeline `fit(X_train, ...)`;
there is no full-frame imputation, no scaler fitted on the full frame after the split,
and no statistical test that references the target before the split. The model flagged
the at-risk population and was reported and used.

## Why it was wrong

One feature is a leak. `account_health_index` — an innocuous name that matches none of
the ten `LEAKAGE_PATTERNS` the `ml` check screens against — is recomputed nightly from
account activity that *includes the outcome window*. Its training-time value is
therefore not the value that would exist at the declared prediction moment: it carries
information about the outcome the model is asked to predict, backwards across the
temporal boundary the split is supposed to enforce. This is a feature-provenance leak
in Kaufman et al.'s formulation — a quantity "legitimate" at scoring time becomes
illegitimate the moment it is derived, in part, from what happens after the prediction
is made (Kaufman, S., Rosset, S., Perlich, C. and Stitelman, O. (2012), "Leakage in
Data Mining: Formulation, Detection, and Avoidance," ACM Transactions on Knowledge
Discovery from Data, 6(4), Article 15, DOI 10.1145/2382577.2382579).

Crucially, nothing in the specification, and no scan of the entrypoint's own text, can
see this. The defect does not live in a declared field (every declaration is true) and
it does not live in the entrypoint (which is genuinely clean). It lives entirely in how
`account_health_index` was *constructed upstream* — a fact that only a per-feature
origin declaration could expose, and this honest spec declares none. The leak is
attributable **only** through feature origin.

## What the gate saw — the four-point measured verdict

Measured directly against this committed fixture and entrypoint. Each gate point run
from a fresh `tempfile.TemporaryDirectory()` as `--phase-dir`, the entrypoint seeded
into it, and a plan-time decision header seeded first for verify/ship — exactly what
the corpus harness (`tests/test_known_bad_corpus.py`) automates. CRITICAL/HIGH only:

| Gate point | Exit code | CRITICAL findings | HIGH findings |
|---|---|---|---|
| `dsx validate` | 0 | — | — |
| `dsx gate plan` | 0 | — | `DSX-MET-040` |
| `dsx gate execute` | 0 | — | — |
| `dsx gate verify` | 1 | — | `DSX-CLM-031`, `DSX-COH-031`, `DSX-MET-040` |
| `dsx gate ship` | 1 | — | `DSX-CLM-031`, `DSX-COH-031`, `DSX-MET-040`, `DSX-NAR-001` |

This is the **D-27-02 entry-condition test**: the two gate points where the `ml` and
`code` leakage-detection checks are registered (`dsx/cli.py::GATE_PROFILES`) — `plan`
and `execute` — both exit 0. The `ml` check ran fully and emitted zero findings; its
leakage screen inspected all seven features including `account_health_index` and
positively cleared them ("7 features screened, no leakage patterns matched"). This is a
positive clearance, not a check that failed to run. **A live miss.**

## The swap-still-fires counterfactual

An honest-swap variant — identical except `account_health_index` is replaced by the
honestly-available `avg_session_minutes` — was re-measured at every one of the five gate
points and produced the **identical** CRITICAL/HIGH finding-code set. No code fires for
the leaky spec that does not also fire for the honest one, so **no residual code is a
catch of the feature-origin leak** — each is incidental to it.

The four verify/ship residuals — `DSX-CLM-031` (an unresolvable evidence pointer),
`DSX-COH-031` (an unchecked assumption), `DSX-MET-040` (a warehouse metric with no
declared SQL) and `DSX-NAR-001` (a missing `narrative.path`) — are the documented
swap-invariant `_INCIDENTAL_GAP_CODES` this fixture shares with its sibling
`full-frame-cleaning`, all HIGH corpus-completeness gaps, none about feature origin.

## The code that now attributes it

`DSX-ML-034`, minted in plan 27-01 under D-05 (Kaufman 2012, TKDD), is the code that
attributes this miss. It reads a declared per-feature origin list and fires CRITICAL
when a feature is available only after the prediction moment, HIGH when its availability
is declared unknown without a waiver. Because it is a declaration-only check —
attribution, not detection — and this honest spec declares no such list, `DSX-ML-034`
correctly stays silent against this fixture at every gate point. The paired
`feature-origin-only-leak-ATTRIBUTION.yaml` records `DSX-ML-034` as the `absent_code`:
the code that *should* attribute the miss but, on an honest spec that declares nothing
false, has nothing to fire on. A spec that lies in the origin list would be caught; this
one does not lie, so it passes — which is exactly the requirement this fixture
demonstrates.
