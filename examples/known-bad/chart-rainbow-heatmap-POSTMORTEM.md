# Post-mortem: a rainbow scale on a continuous measure

Paired spec: `chart-rainbow-heatmap-ANALYSIS-SPEC.yaml`

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

An editor team drew focused minutes by hour of day and weekday as a heatmap, coloured
with a rainbow scale from blue through green and yellow to red.

## Why it was wrong

A rainbow scale is not monotonic in lightness. Wilke (2019, ch.19 §19.2) describes the
problem directly: "The rainbow scale is highly non-monotonic. It has regions where
colors change very slowly and others when colors change rapidly" — lightness runs
from medium-dark to light to very dark and back, with long stretches of little change
followed by narrow bands of large change. On a smooth surface such as minutes by
hour, the reader sees boundaries where the scale's lightness jumps, not where the
data change. A perceptually uniform sequential scale (viridis, cividis, magma) makes
equal steps in the data look like equal steps in colour.

## Source

Wilke, C.O. (2019), *Fundamentals of Data Visualization*, O'Reilly — ch.19 §19.2
(*Using non-monotonic color scales to encode data values*), re-read against the online
edition on 2026-09-06. The IEEE paper commonly cited for this point (Borland and
Taylor 2007) was not reachable for locator verification at the time of writing and is
therefore not cited here.

## Which code catches it

`DSX-VIZ-052` (MEDIUM) — `_check_color` in `dsx/checks/viz.py` fires on
`scale_type: rainbow`. MEDIUM does not block at the default HIGH threshold of
`dsx gate verify` / `dsx gate ship`; the corpus measures it in the MEDIUM stratum under
`--block-on MEDIUM`, reported beside the headline pair. Measured 2026-09-06: plan and
execute exit 0; verify and ship exit 0 at the default threshold with `DSX-VIZ-052` as
the only finding above INFO; exit 1 under `--block-on MEDIUM`. No new finding code is
minted.
