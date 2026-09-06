# Post-mortem: an association between two measures drawn as a line

Paired spec: `chart-correlation-drawn-as-line-ANALYSIS-SPEC.yaml`

One of the nineteen **DSX-VIZ coverage fixtures** added 2026-09-06 to close the
post-ship audit's escalated item 2 (`.planning/POST-SHIP-AUDIT-2026-09.md`): before
them, 17 of the family's 21 codes had never fired against a constructed case. Phase
24 (GA-2 / S4-1) had deliberately scoped chart fixtures to the codes minted in v2.4;
the operator reversed that scoping by direction on 2026-09-06, so every pre-existing
`DSX-VIZ-*` code now has a fixture whose sole purpose is to fire it. The underlying
spec is a copy of the clean `examples/good-corpus/freq-continuous-timeontask` control
— it clears `dsx gate plan` and `dsx gate execute` exactly like its base — so the only
thing wrong with it is the one chart in `visuals[]`.

## What was concluded

An editor team wanted to show how focused minutes relate to session length across
sessions. They declared `relationship: correlation` and drew it as a `line` chart —
session length on the x-axis, focused minutes on the y-axis, one line joining the
points in the order the rows came out of the warehouse.

## Why it was wrong

A line asserts an ordering. Wilke (2019, ch.13 §13.1) states the condition directly:
line graphs "are appropriate whenever one variable imposes an ordering on the data" —
each point has one neighbour before it and one after. Two measurements taken on the
same session impose no such ordering on the other sessions; the line simply follows
row order, and the reader decodes a trajectory that does not exist. The association
between two quantitative variables reads from a scatter plot (Wilke ch.12 §12.1: "we
will normally use a scatter plot"), or from a hexbin or heatmap when the points are
dense. The data signature was honest — `bivariate-simple` admits a line — which is
exactly why this needs a relationship-level check and not only a data-type one.

## Source

Wilke, C.O. (2019), *Fundamentals of Data Visualization*, O'Reilly — ch.12 §12.1
(scatter plots for the relationship between two quantitative variables) and ch.13
§13.1 (a line is licensed by a variable that imposes an ordering). Both locators
re-read against the online edition on 2026-09-06.

## Which code catches it

`DSX-VIZ-012` (HIGH) — `_check_relationship_match` in `dsx/checks/viz.py` finds `line`
outside `RELATIONSHIP_CHARTS["correlation"]` (`scatter`, `hexbin`, `heatmap`) and names
the admissible marks. HIGH blocks at `dsx gate verify` and `dsx gate ship`; the corpus
measures it in the HIGH stratum. Its sibling `DSX-VIZ-013` stays silent here on
purpose, because the data signature does admit a line — the two checks are
complementary, not redundant. Measured 2026-09-06: plan and execute exit 0; verify
and ship exit 1 with `DSX-VIZ-012` as the only finding above INFO. No new finding code
is minted.
