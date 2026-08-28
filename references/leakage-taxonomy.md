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
the least visible. A wide candidate roster searched by grid or random search and
then combined into a stacking or voting ensemble is this failure at
model-selection scale: the search across candidates is a preprocessing decision
surface, and folding the survivors into an ensemble is an iterative selection
informed by whatever data produced the comparison scores. It is filed here,
under type 3, with an explicit cross-reference to type 7 ("Test-set
contamination through iteration") rather than given a type of its own, because
it is both at once.

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

A related note on discretisation: binning a continuous column is information
loss, not a neutral encoding choice. When the binning decision is made because a
hypothesis test computed over the full, unsplit frame found a relationship, the
choice compounds a target-adjacent feature decision (type 1, target leakage)
with a preprocessing leak (type 3, preprocessing leakage) in a single step — the
test that decided the resolution touched the frame the split exists to protect.
`references/The AI Data Scientist.md` (Akimov, Nwadike, Iklassov & Takáč,
arXiv:2508.18113v1, §2.3) states this directly: a continuous age column was
kept continuous rather than bucketed because the paper's own hypothesis-testing
stage found a strong numeric relationship, and the same section's Table 2 shows
the binning idiom (`bucketed_Age` via `pd.cut`) in active use elsewhere in the
pipeline.

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
