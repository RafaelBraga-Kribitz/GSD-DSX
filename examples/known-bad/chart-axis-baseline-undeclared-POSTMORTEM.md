# Post-mortem: a bar chart that never says where its axis starts

Paired spec: `chart-axis-baseline-undeclared-ANALYSIS-SPEC.yaml`

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

The installs-per-account bar chart, fully declared except for the axis: neither
`y_axis_starts_at_zero` nor `y_axis_min` is present.

## Why it was wrong

The truncation check (`DSX-VIZ-020`) can only adjudicate a declaration. A bar chart
that declares nothing about its baseline is not known to be honest — it is unknown,
and an unknown that reads as a pass is how the CRITICAL check gets silently switched
off for exactly the charts most likely to need it. The finding is deliberately LOW:
it is not evidence of a distortion, only of a chart whose proportionality nobody has
vouched for. Its job is to make "declare the baseline" a visible step rather than a
convention.

## Source

DSX's own contract criterion — a companion to `DSX-VIZ-020`'s doctrine (Wilke 2019,
ch.17 §17.1: bars on a linear scale always start at zero), applied to the declaration
rather than to the geometry. No independent perceptual claim is made by this fixture.

## Which code catches it

`DSX-VIZ-021` (LOW) — `_check_axis_truncation` in `dsx/checks/viz.py` reports a
length-encoded mark with no `y_axis_starts_at_zero` declaration. LOW does not block
at any default gate threshold; the corpus measures it in the LOW stratum under
`--block-on LOW`, a readout reported beside the headline pair, added with these
fixtures because no LOW-tier code had a fixture before. Measured 2026-09-06: plan and
execute exit 0; verify and ship exit 0 at the default threshold with `DSX-VIZ-021` as
the only finding above INFO; exit 1 under `--block-on LOW`. No new finding code is
minted.
