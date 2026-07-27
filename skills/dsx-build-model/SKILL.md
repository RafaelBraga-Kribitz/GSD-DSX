---
name: dsx-build-model
description: "Build a predictive model with leakage prevention designed in rather than audited for. Use for any classification, regression or forecasting task."
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
   regression, pair R² with an error metric in the target's own units.

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
dsx check ml repro --phase-dir <phase-dir> --verbose
```
Screens the declared configuration. Then spawn `dsx-ml-integrity-auditor` to
verify the code matches the declaration — the spec is a claim, and claims get
audited.
</verification>

<report>
Report both scores side by side, always: model and baseline, train and test. A
single number invites the reader to assume the comparison was favourable.
</report>

<references>
@references/leakage-taxonomy.md
</references>
