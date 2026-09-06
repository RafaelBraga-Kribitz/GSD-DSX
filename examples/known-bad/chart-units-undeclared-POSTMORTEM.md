# Post-mortem: an axis with no units

Paired spec: `chart-units-undeclared-ANALYSIS-SPEC.yaml`

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

The installs-per-account bar chart, fully declared, with no `units`. The y-axis read
"1.68" and "1.80" and nothing else.

## Why it was wrong

A number without its unit is not a measurement. Currency, percentage, count and index
all look alike on an unlabelled axis, and a reader who assumes the wrong one takes
away the wrong story with full confidence. Wilke (2019, ch.22 §22.2) treats this as
basic practice: for every numerical variable "the relevant titles not only state the
variables shown but also the units in which the variables are measured. This is good
practice and should be done whenever possible." The takeaway sentence carried the
unit here; the axis did not, and the axis is what gets screenshotted.

## Source

Wilke, C.O. (2019), *Fundamentals of Data Visualization*, O'Reilly — ch.22 §22.2
(*Axis and legend titles*), re-read against the online edition on 2026-09-06.

## Which code catches it

`DSX-VIZ-061` (HIGH) — `_check_labelling` in `dsx/checks/viz.py` fires on a blank
`units`. HIGH blocks at `dsx gate verify` and `dsx gate ship`; the corpus measures it
in the HIGH stratum. Measured 2026-09-06: plan and execute exit 0; verify and ship
exit 1 with `DSX-VIZ-061` as the only finding above INFO. No new finding code is
minted.
