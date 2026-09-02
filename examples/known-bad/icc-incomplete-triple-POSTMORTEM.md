# Post-mortem: icc-incomplete-triple

**Target finding code:** DSX-STA-060 (HIGH) — an ICC declared without a complete
(model, type, definition) triple.

## The encoded defect

The `analysis:` block declares `test: icc` with an `icc:` mapping that carries
`model: two_way_random` and `type: single` but OMITS `definition`. An ICC value
is uninterpretable without all three members: the model
(one_way_random / two_way_random / two_way_mixed), the type (single / average),
and the definition (consistency / absolute_agreement).

## Why it routes to exactly one code

The fixture declares only the fields needed to fire DSX-STA-060 and is mutually
exclusive on `analysis.test` with the other four Phase-18 fixtures. `test` is not
a kappa-family test, so DSX-STA-061/062 are out of scope; `test` is not a
CORRELATION_FAMILY member, so DSX-STA-051 stays silent; `analysis.outcome_type`
is OMITTED so DSX-STA-041 never fires. The measured ship finding set is exactly
`{DSX-STA-060}`.

## The remedy

Declare all three of `analysis.icc.model`, `.type`, and `.definition`.
