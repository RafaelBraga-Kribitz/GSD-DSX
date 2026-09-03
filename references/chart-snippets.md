# Chart snippets — one worked figure per function, routed to the gate

A per-function-category cookbook: for each function on the
[`references/chart-catalog.md`](chart-catalog.md) Function axis, one minimal,
copy-ready snippet that builds a figure, finalises it with the DSX house helper
(`templates/dsx_plotstyle.py`), writes it deterministically, and **names the
finding codes that govern its correctness — by code, never by re-deriving the
rule.**

**This document describes and demonstrates; it does not adjudicate.** The gate
reads the live Python vocabulary in `dsx/checks/viz.py`, `dsx/checks/figures.py`
and `dsx/checks/smells.py`, never this file. Each "Gate-enforced:" line *routes*
to a code so an author never re-states (and so never drifts from) the real rule.
Numeric limits — how many pie slices angle can encode, how many categorical hues
stay distinguishable — live only in `viz.py`; a snippet cites the governing code
by name and describes the constraint qualitatively, never the number. The routing
is machine-checked by `tests/test_snippet_catalog_routing.py`: every cited code
must exist in [`references/finding-codes.md`](finding-codes.md), and no snippet
may restate a live `viz.py` threshold.

Every snippet assumes the house style is active and Lato is registered — both are
handled at import time by `templates/dsx_plotstyle.py`:

```python
import matplotlib.pyplot as plt
from templates.dsx_plotstyle import finalise_figure, direct_label, save_deterministic
plt.style.use("styles/dsx-urban.mplstyle")  # house default; register_fonts() ran at import
```

`finalise_figure`'s `source` keyword is **mandatory with no default** — omitting
it is a `TypeError` at call binding, which is the signature-level mirror of
`DSX-VIZ-062` (a figure must cite its source). `save_deterministic` **writes
only**; it never hashes — `dsx seal` stays the single hashing authority (see
Sealing workflow).

Codes shared by every finalised, sealed figure below: `DSX-VIZ-060` /
`DSX-VIZ-063` / `DSX-VIZ-064` (takeaway title present, strong, not the chart
name), `DSX-VIZ-061` (units declared), `DSX-VIZ-062` (source note — the mandatory
`source=` kwarg), `DSX-FIG-011` (artifact carries a seal) and `DSX-FIG-010` (the
sealed bytes match). They are listed once here and not repeated per snippet.

## Sealing workflow

`save_deterministic` and `dsx seal` are two separate steps on purpose (GA-2): the
helper writes byte-reproducible SVG; `dsx seal` (stdlib `hashlib`) is the single
authority that computes the hash you paste into the spec.

```python
path = save_deterministic(fig, "figures/revenue-by-region.svg", metadata={"Date": None})
# then, once, at the shell — the ONLY hasher:
#   dsx seal figures/revenue-by-region.svg
# paste the printed digest into spec.visuals[].svg_sha256, and set
# chart_id / artifact_path / generator / a shared run_id across a readout's figures.
```

`metadata={"Date": None}` is required, not optional: it suppresses matplotlib's
per-render `datetime.today()` timestamp so a second render is byte-identical (the
helper merges it in for you). Gate-enforced: `DSX-FIG-011` (an `artifact_path`
without `svg_sha256` fails), `DSX-FIG-010` (a seal that no longer matches the
bytes fails), `DSX-FIG-020` (a glyph renderer without a seal fails).

## Change over Time

Representative mark: `line` (multi-series trend). Prefer labelling each line at
its end over a legend that grows with the series count.

```python
fig, ax = plt.subplots()
for name, series in series_by_name.items():
    ax.plot(series.index, series.values, label=name)
direct_label(ax)  # label each line at its terminal point instead of a legend
finalise_figure(
    fig,
    title="Northern demand overtook Southern in Q3",
    source="ISO load archive, 2019–2024",
)
save_deterministic(fig, "figures/demand-by-region.svg", metadata={"Date": None})
```

Gate-enforced: `DSX-VIZ-010` / `DSX-VIZ-011` (relationship declared and
recognised), `DSX-VIZ-012` (relationship↔mark admissible), `DSX-VIZ-050` (when the
series count outgrows what distinct hues can separate, this flags it — reach for
`direct_label` rather than more colours). See the full Change over Time mark set
in [`references/chart-catalog.md`](chart-catalog.md).

## Magnitude

Representative mark: `bar` (a value compared across categories). Length encodes
the value, so the axis must start at zero.

```python
fig, ax = plt.subplots()
ax.bar(categories, values)
ax.set_ylim(bottom=0)  # length marks read from a zero baseline
finalise_figure(
    fig,
    title="Region B shipped twice Region A's volume",
    source="Fulfilment ledger, FY2024 (MWh)",
)
save_deterministic(fig, "figures/volume-by-region.svg", metadata={"Date": None})
```

Gate-enforced: `DSX-VIZ-020` (a truncated y-axis on a length-encoded chart is
CRITICAL), `DSX-VIZ-021` (baseline declared), `DSX-VIZ-013` (data-signature↔mark
admissible). See the full Magnitude mark set in
[`references/chart-catalog.md`](chart-catalog.md).

## Distribution

Representative mark: `histogram` (the shape of one variable). State the bin basis
and the units in the title/source, not a caption the gate cannot read.

```python
fig, ax = plt.subplots()
ax.hist(observations, bins="auto")
finalise_figure(
    fig,
    title="Settlement latency clusters under 40 ms with a long right tail",
    source="Gateway telemetry, 2024-Q4 (milliseconds)",
)
save_deterministic(fig, "figures/latency-distribution.svg", metadata={"Date": None})
```

Gate-enforced: `DSX-VIZ-012` / `DSX-VIZ-013` (mark admissible for a distribution
signature), `DSX-VIZ-061` (units — the axis is in real units, declared). See the
full Distribution mark set (`box`, `density`, `ecdf`, `strip`, `violin`, …) in
[`references/chart-catalog.md`](chart-catalog.md).

## Correlation

Representative mark: `scatter` (two continuous variables). Do not imply a trend
line the data does not support; if you add one, cite its method.

```python
fig, ax = plt.subplots()
ax.scatter(x_values, y_values, alpha=0.5)
finalise_figure(
    fig,
    title="Price and load move together only above the 90th percentile",
    source="Day-ahead market, 2023–2024 (€/MWh vs MW)",
)
save_deterministic(fig, "figures/price-vs-load.svg", metadata={"Date": None})
```

Gate-enforced: `DSX-VIZ-012` (relationship↔mark admissible), `DSX-VIZ-051`
(never red/green as the sole distinction if you split by a category),
`DSX-VIZ-050` (categorical colour count for any category split — route to the code,
do not hard-code a maximum). See the full Correlation mark set in
[`references/chart-catalog.md`](chart-catalog.md).

## Ranking

Representative mark: `bump` (rank movement over time). Order the categories by the
quantity being ranked, not alphabetically.

```python
fig, ax = plt.subplots()
for name, ranks in rank_by_name.items():
    ax.plot(periods, ranks, marker="o", label=name)
ax.invert_yaxis()  # rank 1 sits at the top
direct_label(ax)
finalise_figure(
    fig,
    title="Supplier C climbed from 5th to 1st over four quarters",
    source="Award ledger, 2024 (rank of 12)",
)
save_deterministic(fig, "figures/supplier-rank.svg", metadata={"Date": None})
```

Gate-enforced: `DSX-VIZ-080` (categories ordered meaningfully, not by label),
`DSX-VIZ-012` (relationship↔mark admissible). See the full Ranking mark set in
[`references/chart-catalog.md`](chart-catalog.md).

## Part-to-whole

Representative mark: `pie` (shares of a single total). Angle is a weak channel —
keep the number of wedges within what angle can actually separate.

```python
fig, ax = plt.subplots()
ax.pie(shares, labels=labels)
finalise_figure(
    fig,
    title="Baseload is three-fifths of the generation mix",
    source="Dispatch stack, 2024 (share of total MWh)",
)
save_deterministic(fig, "figures/generation-mix.svg", metadata={"Date": None})
```

Gate-enforced: `DSX-VIZ-040` (enforces the wedge-count limit — route to the code;
the maximum lives only in `viz.py`, never restate it here). When shares outgrow
what a pie can carry, switch to a `bar` (Magnitude) rather than adding wedges. See
the full Part-to-whole mark set (`donut`, `treemap`, `waffle`, `circle_pack`, …) in
[`references/chart-catalog.md`](chart-catalog.md).

## Deviation

Representative mark: `diverging_bar` (signed difference from a reference). Anchor
the bars on a shared zero and keep the two directions perceptually symmetric.

```python
fig, ax = plt.subplots()
ax.barh(categories, deltas)  # signed values, diverging from 0
ax.axvline(0, color="black", linewidth=0.8)
finalise_figure(
    fig,
    title="Four regions came in under budget; two ran over",
    source="Variance report, FY2024 (€ vs plan)",
)
save_deterministic(fig, "figures/budget-variance.svg", metadata={"Date": None})
```

Gate-enforced: `DSX-VIZ-020` (length marks read from a zero baseline — here the
shared zero the divergence is measured from), `DSX-VIZ-051` (if you colour the two
directions, do not make red/green the sole cue). See the full Deviation mark set in
[`references/chart-catalog.md`](chart-catalog.md).

## Flow

Representative mark: `sankey` (quantity moving between stages). Width encodes
volume; conserve the total across the diagram.

```python
from matplotlib.sankey import Sankey
fig, ax = plt.subplots()
Sankey(ax=ax, flows=flows, labels=stage_labels).finish()
finalise_figure(
    fig,
    title="A fifth of intake is lost before settlement",
    source="Pipeline trace, 2024 (share of intake volume)",
)
save_deterministic(fig, "figures/intake-flow.svg", metadata={"Date": None})
```

Gate-enforced: `DSX-VIZ-012` (relationship↔mark admissible for a flow),
`DSX-VIZ-061` (the flow's units declared). See the full Flow mark set (`chord`,
`funnel`, …) in [`references/chart-catalog.md`](chart-catalog.md).

## Spatial

Representative mark: `choropleth` (a value shaded across regions). Use a
sequential (or diverging) scale — never a rainbow ramp for a continuous value.

```python
fig, ax = plt.subplots()
regions.plot(column="value", cmap="viridis", ax=ax)  # perceptually uniform, not rainbow
finalise_figure(
    fig,
    title="Curtailment concentrates in the north-west corridor",
    source="Grid operator, 2024 (MWh curtailed)",
)
save_deterministic(fig, "figures/curtailment-map.svg", metadata={"Date": None})
```

Gate-enforced: `DSX-VIZ-052` (a rainbow scale on a continuous variable is
flagged — use a perceptually uniform ramp), `DSX-VIZ-050` (categorical colour
count if the map is categorical rather than continuous). See the full Spatial mark
set (`cartogram`, `symbol_map`, …) in
[`references/chart-catalog.md`](chart-catalog.md).

## Uncertainty

Representative mark: `error_bars` (the default; one of Wilke's ten §5.6 members).
Show uncertainty wherever you show an estimate — pick the mark from the ten under
the Uncertainty function in [`references/chart-catalog.md`](chart-catalog.md).

```python
fig, ax = plt.subplots()
ax.errorbar(x_values, estimates, yerr=ci_half_widths, fmt="o", capsize=3)
finalise_figure(
    fig,
    title="The Q4 lift is real but its interval still straddles zero for Region A",
    source="Bootstrap over 2024 settlements (95% CI, €/MWh)",
)
save_deterministic(fig, "figures/lift-with-ci.svg", metadata={"Date": None})
```

Gate-enforced: `DSX-VIZ-070` (an estimate shown without any uncertainty is
flagged), `DSX-VIZ-071` (the uncertainty mark must be a recognised Wilke §5.6
member). See the full Uncertainty mark set in
[`references/chart-catalog.md`](chart-catalog.md).
