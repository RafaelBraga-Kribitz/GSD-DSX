# Post-mortem: full-frame cleaning and hypothesis testing above an honest split

Paired spec: `full-frame-cleaning-ANALYSIS-SPEC.yaml`
Paired entrypoint: `full-frame-cleaning-entrypoint.py`

## What was concluded

A retention-analytics team built a churn-risk model to flag at-risk bank customers
for a retention-outreach experiment. The model's pipeline followed the published
reference implementation of an autonomous data-science agent — "The AI Data
Scientist" (Akimov, F., Nwadike, M. S., Iklassov, Z. and Takáč, M. (2025),
arXiv:2508.18113v1) — stage for stage, in the paper's own order: a Data Cleaning
Subagent (Section 2.1) imputes a numeric column with its own full-frame mean and
filters rows by a spread statistic; a Hypothesis Subagent (Section 2.2, Table 1)
cross-tabulates a candidate feature against the target and runs a chi-square test;
a Preprocessing Subagent (Section 2.3, Table 2) fits a `StandardScaler` and reports
it as a per-feature transformation. The team declared the whole pipeline's
preprocessing boundary honestly — `model.preprocessing_fit_on: train_only` — and
split the data before training with `train_test_split`. The model was reported and
used to select the flagged population, with no selection ledger recorded for the
one algorithm they tried.

## Why it was wrong

Three of the reproduction's own stages, transcribed faithfully from the paper,
compute a statistic over rows the model's later test split was never supposed to
see, or fit a transform on the full frame after the split rather than the training
frame the split produced.

First, the paper's Data Cleaning Subagent runs "before" any split exists in its own
pipeline diagram — the imputation value (a column's own mean) and the outlier
threshold (a quantile of another column) are both computed over the entire frame,
so a value derived in part from what will later become the test rows leaks into
the number every training row is filled with or filtered against. This is
full-frame preprocessing leakage in Kaufman et al.'s formulation: a statistic
"legitimate" for the training frame becomes illegitimate the moment it is computed
across a boundary the split is supposed to enforce (Kaufman, S., Rosset, S.,
Perlich, C. and Stitelman, O. (2012), "Leakage in Data Mining: Formulation,
Detection, and Avoidance," ACM Transactions on Knowledge Discovery from Data,
6(4), Article 15, DOI 10.1145/2382577.2382579).

Second, the paper's Hypothesis Subagent forms and tests a hypothesis — here, a
chi-square test of a candidate feature against the target — over the same
full, unsplit frame, before any split exists. A test statistic computed against
the target on rows that will later be held out is target leakage into the
feature-selection process: the "validated" hypothesis that a later stage builds a
feature from was validated in part using rows the eventual model is scored
against, so the test's own significance is contaminated by exactly the rows it is
later asked to generalise to (same citation).

Third, the reproduction's Preprocessing Subagent fits its `StandardScaler` after
the split exists in the code — but fits it on the full frame (`data[['Age']]`),
not on the training frame the split produced (`X_train`). A scaler's mean and
variance are themselves statistics with the same legitimacy boundary as the
cleaning stage's imputation value: fitting them on the full frame carries
test-row information into every transformed training value (same citation).

The specification's own `model.preprocessing_fit_on: train_only` declaration is
true and not contradicted by any of this — it describes the *model's* declared
whole-pipeline boundary, a field this corpus's prior fixtures already gate. What
it does not, and structurally cannot, describe is what the *entrypoint source*
actually does at each of its own stages. That is exactly the requirement this
fixture demonstrates: an honest whole-pipeline declaration and a leaking
entrypoint are not mutually exclusive, and only a scan of the entrypoint's own
text — not a reconciliation against a declared field — catches this fixture's
defect.

Finally, the model's algorithm is declared with no selection ledger at all: no
candidates evaluated, no configuration count, no selection basis. A gradient-
boosting model was apparently just tried once and reported, or many candidates
were tried and only the choice survives in the specification — the specification
cannot distinguish those two very different claims from each other, which is
exactly the account Cawley and Talbot's result says model-selection bias
depends on (Cawley, G.C. and Talbot, N.L.C. (2010), "On Over-fitting in Model
Selection and Subsequent Selection Bias in Performance Evaluation," Journal of
Machine Learning Research, 11, pages 2079 to 2107).

## What the gate saw before this phase, and what it sees now

Before Phase 11.1, this shape passed with zero findings at every severity: the
entrypoint scan (`dsx/checks/code.py`) had no full-frame-cleaning check, no
statistical-test-sees-target check, and no fit-after-split check whose lexicon
covered a bare full-frame subscript like `data[['Age']]`; the machine-learning
check (`dsx/checks/ml.py`) had no selection-ledger check at all. Measured
directly against this repository's pre-phase-11.1 corpus-harness state (a fresh
temporary directory as `--phase-dir`, with no entrypoint-seeding step): running
`dsx gate execute` against `examples/good-ANALYSIS-SPEC.yaml` under that
condition fires `DSX-REP-031` ("declared entrypoint does not exist") because the
harness cannot even resolve a fixture's own entrypoint against a fresh temporary
directory — and the `code` check's own findings are empty regardless of what the
entrypoint source contains, for every fixture in the corpus, because none of them
declares one. This fixture's own entrypoint could not have been checked before
plan 11.1-08's corpus-harness extension (`tests/test_known_bad_corpus.py`,
`_seed_entrypoint`) existed to seed it into the temporary directory the harness
gates against.

After this phase, measured directly against this committed fixture and
entrypoint (`--phase-dir` seeded with the entrypoint file at the same relative
path the specification declares, as the corpus harness now does automatically):

| Gate point | Exit code | CRITICAL findings | Notable HIGH findings |
|---|---|---|---|
| `dsx validate` | 0 | — | — |
| `dsx gate plan` | 0 | — | `DSX-MET-040` |
| `dsx gate execute` | 1 | `DSX-CODE-020`, `DSX-CODE-021`, `DSX-CODE-030` | `DSX-ML-090` |
| `dsx gate verify` | 1 | `DSX-CODE-020`, `DSX-CODE-021`, `DSX-CODE-030` | `DSX-CLM-031`, `DSX-COH-031`, `DSX-MET-040`, `DSX-ML-090` |
| `dsx gate ship` | 1 | `DSX-CODE-020`, `DSX-CODE-021`, `DSX-CODE-030` | `DSX-CLM-031`, `DSX-COH-031`, `DSX-MET-040`, `DSX-ML-090`, `DSX-NAR-001` |

`dsx gate plan` and `dsx gate execute` were run with a fresh `tempfile.mkdtemp()`
as `--phase-dir` with the entrypoint copied to the same relative path beforehand
(what the corpus harness now automates); `dsx gate verify` and `dsx gate ship`
additionally had a plan-time decision-trail header seeded first (the same
precondition every other fixture in this corpus needs from Phase 10 onward). The
`DSX-CLM-031`, `DSX-COH-031`, `DSX-MET-040` and `DSX-NAR-001` findings are
corpus-completeness gaps this fixture shares with its siblings — an
unresolvable evidence pointer, an unchecked assumption, a warehouse metric with
no declared SQL, and a missing `narrative.path` — not this fixture's own
encoded defect; see `tests/test_known_bad_corpus.py::_INCIDENTAL_GAP_CODES`.
`DSX-EXP-040` (MEDIUM, present at plan/verify/ship) and `DSX-REP-010`/
`DSX-REP-011` (MEDIUM/LOW, present at execute/verify/ship) sit below the HIGH
threshold the ship-completeness test enforces and are not separately
accounted for.

## The code that catches it

Three codes from the entrypoint scan (`dsx/checks/code.py`, Phase 11.1 plan
11.1-01/11.1-03) and one from the machine-learning check (`dsx/checks/ml.py`,
Phase 11.1 plan 11.1-06) together catch this reproduction, at `dsx gate execute`
(the `code` and `ml` check families are registered there;
`dsx/cli.py::GATE_PROFILES`):

- **`DSX-CODE-020`** (CRITICAL) — the full-frame mean imputation
  (`data['Age'].fillna(data['Age'].mean())`) fires this: the co-occurring
  `.fillna(`/`.mean(` idiom on one line, before the first split marker.
- **`DSX-CODE-021`** (CRITICAL) — the scaler fitted on the full frame after the
  split (`scaler.fit_transform(data[['Age']])`) fires this: a `.fit_transform(`
  call at or after the split whose first-argument token (`data[['Age']]`) does
  not start with a recognised training-frame name.
- **`DSX-CODE-030`** (CRITICAL) — the chi-square test referencing the declared
  target before the split (`chi2_contingency(contingency_table)`, with
  `data['Exited']` referenced on the immediately preceding line) fires this: a
  statistical-test call whose argument text, within a bounded lookback window,
  references `model.target`, before the first split marker.
- **`DSX-ML-090`** (HIGH) — the declared `model.algorithm` (`gradient_boosting`)
  with no `model.selection_ledger` at all fires this: every one of the ledger's
  three declared fields (candidates evaluated, configurations tried, selection
  basis) is missing.

The spread-based row filter (`data[data['Balance'] < data['Balance'].quantile(0.99)]`)
also matches `DSX-CODE-020`'s pattern, but `dsx/checks/code.py` reports only the
first matching line per code, so it does not produce a second finding — the
defect it encodes is still caught by the same code, at the earlier-firing line.

`dsx gate plan` clears (exit 0) because neither the `code` nor the `ml` check
family is registered at the `plan` gate point (`dsx/cli.py::GATE_PROFILES`):
there is nothing at plan to catch an entrypoint's own leakage or a missing
selection ledger, regardless of what the entrypoint or the model block declare.
