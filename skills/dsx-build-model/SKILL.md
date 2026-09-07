---
name: dsx-build-model
description: "Build a predictive model with leakage prevention designed in rather than audited for. Use for any classification, regression or forecasting task. Triggers: 'build a model', 'predict <y> from <extract.csv>', 'train a classifier' — routes intent without GSD phase names."
argument-hint: "[--task <type>] [--target <column>] [--time <column>]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
---

<objective>
A model whose offline score predicts its production score. Everything below
exists to close the gap between those two numbers.
</objective>

<inputs>
**Read `EDA.md` front-matter first when it exists** in the phase directory — a model
designs leakage prevention in from the profile's measured suspects, dependence structure
and categorical cardinality rather than auditing for it after the split is drawn.

EDA front-matter keys read:
- `leakage_suspects[]`
- `grain.implied_dependence.structure`
- `grain.implied_dependence.cluster_var`
- `segments_candidates[]`

DATA-PROFILE keys read (the fallback source when EDA is absent):
- `columns[].n_unique`
- `columns[].dtype`
- `columns[].categorical`
- `unit.rows_per_unit`
- `time.column`
- `time.max_gap_days`

These set: `model.features_excluded_for_leakage` (from the leakage suspects), the split type — temporal, grouped, or `grouped_temporal` (from the dependence structure, cluster variable and time column), the `entity_column` (from the cluster variable and rows-per-unit), and the encoding policy (from categorical cardinality and dtype).
Also consult (EDA prose, not front-matter): section 4 Wide categoricals — the policy recommendation informing the encoding choice.
When absent: no `EDA.md` → record `eda_artifact: none` and source the leakage-suspect, dependence and cardinality facts from the DATA-PROFILE keys above; where the profile is also absent, declare each with `computed_by` honesty rather than asserting a clean split.
</inputs>

<order_of_operations>
The sequence is not stylistic. Each step makes the next one checkable.

1. **Define the prediction moment.** When does the model run in production, and
   what is known at that instant? Every leakage decision resolves against this
   one sentence. Write it into `model.prediction_time_definition` first.

2. **Split before anything else.** Before profiling, before imputation, before
   feature engineering. Temporal data gets a time-ordered split; repeated
   entities get a grouped split; both get `grouped_temporal`.

3. **Establish the baseline.** `majority_class`, `last_value`, `seasonal_naive`,
   or the current rules engine. Score it. A model that never beat this was never
   evaluated.

4. **Choose the primary metric before training.** For an imbalanced target,
   accuracy and ROC-AUC both flatter. Use PR-AUC or balanced accuracy. For
   regression, pair R² with an error metric in the target's own units. If that
   primary metric is an error measure — RMSE, MAE, MAPE, log loss — declare
   `model.metric_direction: lower_is_better`. The gate compares scores but does
   not guess which way they point, so leaving it out makes a halved error read
   as a loss against the baseline.

5. **Build features inside a pipeline.** Every transform fitted on the training
   fold only. This is not a style preference — a scaler fitted on the full frame
   leaks test statistics and never raises an error.

6. **Tune on validation, never on test.** The test set is touched once, at the
   end, at a threshold already chosen on validation.

7. **Calibrate if the probabilities drive decisions.** Tree ensembles rank well
   and calibrate badly. A "70% risk" bucket that contains 40% actual events
   breaks every expected-value calculation built on it.

</order_of_operations>

<verification>
```bash
dsx check ml repro code --phase-dir <phase-dir> --verbose
```
Screens the declared configuration **and** the entrypoint for fit-before-split
smells (`DSX-CODE-*`). Fix fit-before-split before arguing with the auditor.
Then spawn `dsx-ml-integrity-auditor` to verify the code matches the declaration
— the spec is a claim, and claims get audited.
</verification>

<report>
Report both scores side by side, always: model and baseline, train and test. A
single number invites the reader to assume the comparison was favourable.
</report>

<references>
@references/leakage-taxonomy.md
</references>
