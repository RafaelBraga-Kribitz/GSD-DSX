# Post-mortem: weighted-kappa-missing-weights

**Target finding code:** DSX-STA-061 (HIGH) — a weighted kappa declared without
recognised weights.

## The encoded defect

The `analysis:` block declares `test: weighted_kappa` but OMITS `weights`. A
weighted kappa needs a declared weighting scheme — the string `linear` or
`quadratic`, or an explicit weight matrix. An unweighted kappa is a different
statistic and should be declared as `cohens_kappa`.

## Why it routes to exactly one code

The fixture declares only the fields needed to fire DSX-STA-061 and is mutually
exclusive on `analysis.test` with the other four Phase-18 fixtures. It DOES
declare `analysis.p_pos` and `analysis.p_neg`, so DSX-STA-062 is satisfied and
stays silent; `test` is not icc, so DSX-STA-060 is out of scope; not a
CORRELATION_FAMILY member, so DSX-STA-051 stays silent; `analysis.outcome_type`
is OMITTED so DSX-STA-041 never fires. The measured ship finding set is exactly
`{DSX-STA-061}`.

## The remedy

Declare `analysis.weights` as `linear`, `quadratic`, or an explicit weight matrix.
