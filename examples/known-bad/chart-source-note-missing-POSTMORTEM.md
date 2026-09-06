# Post-mortem: a chart with no source note

Paired spec: `chart-source-note-missing-ANALYSIS-SPEC.yaml`

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

The installs-per-account bar chart, fully declared, with no `source` — no dataset
name and no period anywhere on the figure.

## Why it was wrong

Charts travel without their documents. The one that ends up in a slide six months
later, cropped and pasted, carries only what was printed on it; a chart with no
source note cannot be traced to the extract, the period or the definition that
produced it, and cannot be reproduced or retired when the data change. This is the
visual counterpart of the spec's `data[].source` and `period` declarations: the
numbers are provenance-bound in the contract and should stay so on the artifact. The
finding is LOW because nothing about the chart's geometry or encoding is wrong; it
is a reproducibility gap, not a distortion.

## Source

DSX's own reproducibility criterion (`references/narrative-discipline.md`; the
`data[]` provenance fields of `templates/ANALYSIS-SPEC.yaml`). No external perceptual
source is claimed for this fixture.

## Which code catches it

`DSX-VIZ-062` (LOW) — `_check_labelling` in `dsx/checks/viz.py` fires on a blank
`source`. LOW does not block at any default gate threshold; the corpus measures it in
the LOW stratum under `--block-on LOW`, a readout reported beside the headline pair,
added with these fixtures because no LOW-tier code had a fixture before. Measured
2026-09-06: plan and execute exit 0; verify and ship exit 0 at the default threshold
with `DSX-VIZ-062` as the only finding above INFO; exit 1 under `--block-on LOW`. No
new finding code is minted.
