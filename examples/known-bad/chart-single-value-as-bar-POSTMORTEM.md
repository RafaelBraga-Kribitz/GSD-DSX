# Post-mortem: one number drawn as a one-bar bar chart

Paired spec: `chart-single-value-as-bar-ANALYSIS-SPEC.yaml`

One of the nineteen **DSX-VIZ coverage fixtures** added 2026-09-06 to close the
post-ship audit's escalated item 2 (`.planning/POST-SHIP-AUDIT-2026-09.md`): before
them, 17 of the family's 21 codes had never fired against a constructed case. Phase
24 (GA-2 / S4-1) had deliberately scoped chart fixtures to the codes minted in v2.4;
the operator reversed that scoping by direction on 2026-09-06, so every pre-existing
`DSX-VIZ-*` code now has a fixture whose sole purpose is to fire it. The underlying
spec is a copy of the clean `examples/good-corpus/freq-count-installs` control — it
clears `dsx gate plan` and `dsx gate execute` exactly like its base — so the only
thing wrong with it is the one chart in `visuals[]`.

## What was concluded

A platform team had one number to report — installs per account for the fortnight —
and drew it as a bar chart with a single bar, declaring the data signature honestly
as `single-value` and the relationship as `comparison`.

## Why it was wrong

A bar encodes a comparison between bars. With one bar there is nothing to compare it
against, so the chart borrows the visual grammar of a comparison to present a number
that has no comparator on the page. The `single-value` data signature admits only
marks that do not imply a relationship — a big number, a bullet (which carries its
own target and baseline), or a sparkline (which carries its own history). This is the
same reasoning recorded in `dsx/spec.py` for excluding gauges from that family: the
honest marks for a single number are the ones that do not pretend to be a chart.
The relationship check is silent here because `bar` is a legitimate comparison mark —
the defect is that the *data* cannot support the relationship the mark claims.

## Source

DSX's own capability matrix (`CHART_CAPABILITIES["single-value"]` in `dsx/spec.py`;
`references/data-input-types.md`). The "no comparator on the page" argument is DSX's
own reasoning, recorded as such; no external perceptual source is claimed for it.

## Which code catches it

`DSX-VIZ-013` (HIGH) — `_check_input_type_matrix` in `dsx/checks/viz.py` finds `bar`
outside the marks the declared `data_input_type` admits and names the admissible set.
This is the "declared but conflicting" branch of the matrix; the other branch
(an unrecognised `data_input_type` string) shares the code and is covered by inline
unit tests. HIGH blocks at `dsx gate verify` and `dsx gate ship`; the corpus measures
it in the HIGH stratum. Measured 2026-09-06: plan and execute exit 0; verify and ship
exit 1 with `DSX-VIZ-013` as the only finding above INFO. No new finding code is
minted.
