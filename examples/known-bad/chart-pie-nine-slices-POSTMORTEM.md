# Post-mortem: a nine-slice pie

Paired spec: `chart-pie-nine-slices-ANALYSIS-SPEC.yaml`

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

An editor team showed the share of sessions by editor surface as a pie with nine
slices. One slice (the document editor, 41%) was obvious; the other eight, none above
15%, were read by legend lookup.

## Why it was wrong

A pie is read by angle. In Cleveland & McGill's (1984) ranking of elementary
perceptual tasks, angle sits in the third rank (tied with length and direction),
while the end of a bar against a common axis is read by position along a common
scale — the first rank. Wilke (2019, ch.10) makes the practical case: pies "work well
when the goal is to emphasize simple fractions, such as one-half, one-third, or
one-quarter", and struggle "when the whole is broken into many pieces", where
side-by-side bars let the reader compare the fractions directly (§10.2). Nine slices,
eight of them small and adjacent, is the case where the reader cannot rank them and
the chart becomes a legend-matching exercise. The threshold of five slices is DSX's
own cut, recorded as `MAX_PIE_SLICES`; neither source states a number.

## Source

Cleveland, W.S. and McGill, R. (1984), *Graphical Perception: Theory, Experimentation,
and Application to the Development of Graphical Methods*, *JASA* 79:531–554 — p.536
list, p.537 tie caveat (the locator `references/chart-catalog.md` already carries,
verified at HQ-27). Wilke, C.O. (2019), *Fundamentals of Data Visualization*, ch.10
§10.1–§10.2, re-read against the online edition on 2026-09-06.

## Which code catches it

`DSX-VIZ-040` (MEDIUM) — `_check_slice_count` in `dsx/checks/viz.py` fires on a pie,
donut, waffle or treemap whose `category_count` exceeds `MAX_PIE_SLICES`. MEDIUM does
not block at the default HIGH threshold of `dsx gate verify` / `dsx gate ship`; the
corpus measures it in the MEDIUM stratum under `--block-on MEDIUM`, reported beside
the headline pair. Measured 2026-09-06: plan and execute exit 0; verify and ship exit 0
at the default threshold with `DSX-VIZ-040` as the only finding above INFO; exit 1
under `--block-on MEDIUM`. No new finding code is minted.
