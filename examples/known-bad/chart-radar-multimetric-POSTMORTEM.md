# Post-mortem: multi-metric comparison shown on a radar chart

Paired spec: `chart-radar-multimetric-ANALYSIS-SPEC.yaml`

One of the first **bad-chart-choice** fixtures (Phase 24, GA-2), and the banned-type
control the discuss round called for: a pre-existing banned mark (radar) rather than
one of the two newly-banned marks (gauge, word_cloud). The underlying spec is a copy
of the clean `examples/good-corpus/freq-continuous-aov` control and clears both
CRITICAL-threshold gate points exactly like its base.

## What was concluded

A commerce team compared order-value metrics across regions on a radar (spider)
chart — each region a polygon over a shared set of radial axes, the polygons
overlaid so readers could "see which region is biggest".

## Why it was wrong

A radar chart encodes each value as distance along its own spoke, then fills the
enclosed polygon. Two things break. First, the filled area grows with the *square*
of the values, so a region that is uniformly a little higher looks dramatically
larger than the difference warrants. Second, the shape — and therefore the visual
impression of "big" — depends entirely on the arbitrary order the axes are placed
around the circle; reorder the spokes and the same numbers make a different polygon.
Neither the area nor the shape is a faithful reading of the data. A grouped or
faceted bar chart (or a dot plot per metric) compares the same regions on a stable
position encoding.

## Source

Duan, R. et al. (2023), *Journal of Clinical Epidemiology* 156:85–94, Introduction
(DOI 10.1016/j.jclinepi.2023.02.020) — the peer-reviewed statement of both the
area-proportional-to-the-square-of-the-value and the area-depends-on-axis-order
criticisms, recorded in `dsx/checks/viz.py` `BANNED_TYPES["radar"]` (HQ-27 Tier-3,
signed 2026-09-03).

## Which code catches it

`DSX-VIZ-001` (HIGH) — `radar` is a pre-existing member of `BANNED_TYPES`, so
`_check_banned` refuses it at `dsx gate verify` and `dsx gate ship`, routing to the
**existing** `DSX-VIZ-001` shared by every banned mark. No new code is minted. The
incidental MEDIUM findings (`DSX-VIZ-010`, `DSX-VIZ-014`) are below the HIGH block
threshold and are not the encoded defect.
