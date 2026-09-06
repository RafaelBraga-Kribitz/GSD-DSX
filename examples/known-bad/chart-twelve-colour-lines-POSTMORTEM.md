# Post-mortem: twelve categories, twelve hues

Paired spec: `chart-twelve-colour-lines-ANALYSIS-SPEC.yaml`

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

An editor team plotted focused minutes per day for twelve editor surfaces on one
chart, one distinct hue per surface, with a twelve-entry legend.

## Why it was wrong

Colour as a categorical encoding stops working well before twelve. Wilke (2019, ch.19
§19.1) gives the rule of thumb: "Qualitative color scales work best when there are
three to five different categories that need to be colored. Once we reach eight to
ten different categories or more, the task of matching colors to categories becomes
too burdensome to be useful." The chart's own takeaway — one surface moved, eleven
did not — is the argument for the fix: highlight the one that matters, grey the rest,
or use small multiples. DSX's cut of seven (`MAX_CATEGORICAL_COLORS`) sits inside
Wilke's band and is DSX's own choice of where to draw it.

## Source

Wilke, C.O. (2019), *Fundamentals of Data Visualization*, O'Reilly — ch.19 §19.1
(*Encoding too much or irrelevant information*), re-read against the online edition
on 2026-09-06. The specific threshold of seven is DSX's own, recorded as such.

## Which code catches it

`DSX-VIZ-050` (MEDIUM) — `_check_color` in `dsx/checks/viz.py` fires when
`color_count` exceeds `MAX_CATEGORICAL_COLORS`. MEDIUM does not block at the default
HIGH threshold of `dsx gate verify` / `dsx gate ship`; the corpus measures it in the
MEDIUM stratum under `--block-on MEDIUM`, reported beside the headline pair. Measured
2026-09-06: plan and execute exit 0; verify and ship exit 0 at the default threshold
with `DSX-VIZ-050` as the only finding above INFO; exit 1 under `--block-on MEDIUM`.
No new finding code is minted.
