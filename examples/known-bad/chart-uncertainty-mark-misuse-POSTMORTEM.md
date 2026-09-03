# Post-mortem: an uncertainty figure declaring a mark outside the vocabulary

Paired spec: `chart-uncertainty-mark-misuse-ANALYSIS-SPEC.yaml`

One of the first **bad-chart-choice** fixtures (Phase 24, GA-2), and the one that
exercises the MEDIUM stratum. Unlike the three banned-type fixtures, this one does
**not** block at the default HIGH gate threshold — it fires a single MEDIUM finding.
The underlying spec is a copy of the clean
`examples/good-corpus/freq-continuous-timeontask` control and clears every gate
point at the default threshold exactly like its base.

## What was concluded

An editor team plotted the focused-editing uplift as an uncertainty figure —
`relationship: uncertainty`, an estimate with an interval around it — but declared
the interval mark as `uncertainty_mark: gradient_band`.

## Why it was wrong

`gradient_band` is not a member of the closed uncertainty vocabulary. The chart is
otherwise well-formed: it declares `relationship: uncertainty`, a
`data_input_type: interval-range` that admits `error_bars`, and it does show its
uncertainty (so it does not trip `DSX-VIZ-070`). The single defect is the mark name.
Wilke's §5.6 names ten uncertainty marks — `error_bars`, `graded_error_bars`,
`error_bars_2d`, `confidence_strips`, `eye`, `half_eye`, `quantile_dot_plot`,
`confidence_band`, `graded_confidence_band`, `fitted_draws`. Note the trap:
`confidence_band` and `graded_confidence_band` are real members; the plausible-
sounding `gradient_band` is not one of them. Picking a name outside the vocabulary
means the figure is not one the reader has a learned decoding for, and it cannot be
checked against the paradigm-symmetry guarantee the vocabulary carries.

## Source

Wilke, C.O. (2019), *Fundamentals of Data Visualization*, O'Reilly — ch.5 §5.6 (the
ten-mark uncertainty vocabulary) and ch.16 §16.2 (frequentist/Bayesian paradigm
symmetry). This is the same source `RELATIONSHIP_CHARTS["uncertainty"]` in
`dsx/checks/viz.py` is built from. The "gradient CI band is not Wilke's term"
correction is HQ-27 decision D-2 (signed 2026-09-03).

## Which code catches it

`DSX-VIZ-071` (MEDIUM) — `_check_uncertainty_vocabulary` looks the declared
`uncertainty_mark` up against `RELATIONSHIP_CHARTS["uncertainty"]` (membership only,
no computed threshold) and reports a non-member. Because it is MEDIUM it does **not**
block at the default HIGH threshold; the corpus catches it in a dedicated MEDIUM
stratum run under `--block-on MEDIUM`, and reports that catch rate **beside** the
headline miss-rate/FPR, never folded into it. `DSX-VIZ-071` is the code Phase 22
minted; this fixture mints **no** new code.
