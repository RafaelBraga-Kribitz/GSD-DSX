# Leakage taxonomy

Leakage is information in training that will not exist at prediction time. It
produces excellent offline metrics and a model that fails in production, and it
never raises an error.

## The one question

*Would this feature hold this value at the moment the model runs in production?*

Not "does the column exist" — would it hold this content. A `status` field
containing "cancelled" only after cancellation leaks, even though the column is
always present.

Answering requires a prediction-time definition. Write it before building
features: `model.prediction_time_definition`.

## Types, by how often they occur

**1. Target leakage.** A feature computed from, or populated by, the outcome.
`cancellation_reason`, `days_to_churn`, `refund_amount`, `closed_at`. Screened by
`dsx check ml` against a pattern lexicon, but the lexicon only catches names.

**2. Temporal leakage.** A random split on time-ordered data puts future rows in
training. Also: aggregates over the full history, joins to tables updated after
the prediction point, "next month" features.

**3. Preprocessing leakage.** A scaler, imputer, encoder or feature selector
fitted before the split. The test set's mean, its category vocabulary, or its
correlation with the target has entered training. This is the most common bug and
the least visible.

**4. Group leakage.** The same entity in both train and test. The model memorises
the entity rather than the pattern, so the score is an upper bound that will not
hold for new entities.

**5. Duplicate leakage.** Exact or near-duplicate rows spanning the split.
Deduplicate before splitting, not after.

**6. Resampling leakage.** SMOTE or oversampling applied before the split copies
rows across the boundary.

**7. Test-set contamination through iteration.** Every look at the test set that
informs a modelling choice turns it into a validation set. After twenty
iterations the final score is optimistic by an unknown amount.

## Detection signals

Ranked by reliability. None proves leakage; all warrant tracing the feature to
its source table and its populated-at timestamp.

1. A feature whose name references the outcome or a time after it.
2. Test performance above train performance.
3. One feature dominating importance on a problem known to be hard.
4. AUC above 0.95 on behavioural prediction.
5. Performance degrading sharply on the most recent time slice.
6. Beating a strong domain expert by a wide margin on the first attempt.

## Prevention beats detection

- Split first, before anything else touches the data.
- Every transform inside a pipeline, fitted per fold.
- Write the prediction-time definition before writing features.
- Maintain an explicit exclusion list with a justification per feature.
- Evaluate on the most recent time slice as a final check, even for non-temporal
  problems. It approximates production drift better than a random holdout.
