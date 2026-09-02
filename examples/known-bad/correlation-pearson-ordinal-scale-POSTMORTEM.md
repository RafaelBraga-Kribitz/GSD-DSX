# Post-mortem: correlation-pearson-ordinal-scale

**Target finding code:** DSX-STA-050 (HIGH) — Pearson correlation declared against
a declared-ordinal operand.

## The encoded defect

The `analysis:` block declares `test: pearson_correlation` with
`operand_scale: ordinal` and a non-agreement `estimand_kind: linear_association`.
Pearson's r assumes a linear, interval-or-better scale. An ordinal operand with
more than two ordered levels (the ">2 levels" whitelist boundary — a two-level
operand would be declared `dichotomous`, point-biserial's home, and is whitelisted)
is exactly the case the coefficient is not licensed for.

## Why it routes to exactly one code

The fixture declares only the fields needed to fire DSX-STA-050 and is mutually
exclusive on `analysis.test` with the other four Phase-18 fixtures. It keeps
`estimand_kind` a non-agreement kind so DSX-STA-051 stays silent, and it OMITS
`analysis.outcome_type`, so the declared-test check early-returns and DSX-STA-041
never fires. The measured ship finding set is exactly `{DSX-STA-050}`.

## The remedy

Redeclare `estimand_kind` as `monotone_association` and use
`spearman_correlation` or `kendall_tau_b`.
