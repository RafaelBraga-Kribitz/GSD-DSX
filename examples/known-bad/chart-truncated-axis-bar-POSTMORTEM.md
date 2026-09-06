# Post-mortem: a bar chart whose y-axis starts at 1.5

Paired spec: `chart-truncated-axis-bar-ANALYSIS-SPEC.yaml`

One of the nineteen **DSX-VIZ coverage fixtures** added 2026-09-06 to close the
post-ship audit's escalated item 2 (`.planning/POST-SHIP-AUDIT-2026-09.md`), and the
one the audit named first: `DSX-VIZ-020` is the **only CRITICAL code in the
visualization family**, and until this fixture it had never been constructed. Phase
24 (GA-2 / S4-1) had deliberately scoped chart fixtures to the codes minted in v2.4;
the operator reversed that scoping by direction on 2026-09-06. The underlying spec
is a copy of the clean `examples/good-corpus/freq-count-installs` control — it clears
`dsx gate plan` and `dsx gate execute` exactly like its base — so the only thing wrong
with it is the one chart in `visuals[]`.

## What was concluded

A platform team plotted installs per account for the two arms as a bar chart. The
control bar sat at about 1.68 and the treatment bar at 1.80, so to "make the
difference visible" the y-axis was started at 1.5. The treatment bar now stood
roughly 1.7 times the height of the control bar, for an uplift of 0.12 on a base of
1.68 — about 7%.

## Why it was wrong

A bar encodes its value as length from the baseline; that is the whole contract of
the mark. Wilke (2019, ch.17 §17.1) states the rule without qualification: "Bars on a
linear scale should always start at 0." The chapter names the underlying principle —
the sizes of shaded areas must be proportional to the data values they represent —
and attributes the term *principle of proportional ink* to Bergstrom and West (2016).
Starting the axis at 1.5 keeps the numbers honest and makes the geometry lie: the
reader's eye compares lengths, and the lengths now say "nearly double" where the data
say "seven percent". If the interesting variation is small, the honest chart plots the
difference itself, or uses a position-encoded mark (a dot plot, a line) whose axis
may legitimately float.

## Source

Wilke, C.O. (2019), *Fundamentals of Data Visualization*, O'Reilly — ch.17 §17.1
(*Visualizations along linear axes*): "Bars on a linear scale should always start at
0"; the principle of proportional ink attributed there to Bergstrom, C.T. and West, J.
(2016), *The Principle of Proportional Ink*, callingbullshit.org. Locators re-read
against the online edition on 2026-09-06.

## Which code catches it

`DSX-VIZ-020` (CRITICAL) — `_check_axis_truncation` in `dsx/checks/viz.py` fires on a
length-encoded mark whose `y_axis_starts_at_zero` is `false` or whose `y_axis_min` is
above zero, naming the declared minimum. The `viz` family is registered at
`dsx gate verify` and `dsx gate ship` only, so this CRITICAL fires at those two points
and cannot fire at plan or execute — the same point-scoped shape as
`post-hoc-procedure-switch`'s `DSX-PRE-030`, and recorded the same way in
`_TARGET_DEFECT_CODES`. Measured 2026-09-06: plan and execute exit 0; verify and ship
exit 1 with `DSX-VIZ-020` as the only finding above INFO. No new finding code is
minted.
