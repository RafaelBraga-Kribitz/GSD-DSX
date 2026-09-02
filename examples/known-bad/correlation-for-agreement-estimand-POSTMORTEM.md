# Post-mortem: correlation-for-agreement-estimand

**Target finding code:** DSX-STA-051 (HIGH) — a correlation coefficient declared
for an agreement estimand.

## The encoded defect

The `analysis:` block declares `test: pearson_correlation` (a member of the
CORRELATION_FAMILY) with `estimand_kind: agreement`. A correlation coefficient
measures association, not chance-corrected agreement or method bias. Correlation
is high whenever two raters or methods move together even under a constant
offset — precisely the disagreement that kappa/ICC exist to detect.

## Why it routes to exactly one code

The fixture declares only the fields needed to fire DSX-STA-051 and is mutually
exclusive on `analysis.test` with the other four Phase-18 fixtures. It OMITS
`operand_scale` so DSX-STA-050 stays silent, and it OMITS `analysis.outcome_type`
so DSX-STA-041 never fires. `test` is not icc/kappa, so DSX-STA-060/061/062 are
out of scope. The measured ship finding set is exactly `{DSX-STA-051}`.

## The remedy

Route to kappa/ICC for an agreement estimand (or Bland-Altman for method
comparison); redeclare `estimand_kind` if an association reading was intended.
