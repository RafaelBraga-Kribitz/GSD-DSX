# Post-mortem: kappa-missing-companions

**Target finding code:** DSX-STA-062 (HIGH) — a kappa declared without its
p_pos/p_neg companions.

## The encoded defect

The `analysis:` block declares `test: cohens_kappa` but OMITS both
`analysis.p_pos` and `analysis.p_neg`. Feinstein & Cicchetti (1990) Part I
documents two paradoxes an omnibus kappa can hide (high raw agreement with low
kappa under skewed prevalence, and asymmetric marginals); Part II recommends
reporting the separate positive and negative agreement proportions alongside it.
Both p_pos and p_neg are required, not either one.

## Why it routes to exactly one code

The fixture declares only the fields needed to fire DSX-STA-062 and is mutually
exclusive on `analysis.test` with the other four Phase-18 fixtures. `cohens_kappa`
is NOT `weighted_kappa`, so DSX-STA-061 is out of scope; `test` is not icc, so
DSX-STA-060 is out of scope; not a CORRELATION_FAMILY member, so DSX-STA-051
stays silent; `analysis.outcome_type` is OMITTED so DSX-STA-041 never fires. The
measured ship finding set is exactly `{DSX-STA-062}`.

## The remedy

Declare both `analysis.p_pos` and `analysis.p_neg` alongside the kappa.
