# Chart catalog — the merged, citable visual vocabulary

A single reference for every chart mark DSX will recommend, refuse, or merely
document. It is **citable, not exhaustive-for-its-own-sake**: 60 DSX-admissible
marks (the live gate vocabulary), 7 refusal rows (one per banned type), and
14 reference-only rows that fill genuine gaps across the function axis without
widening what the gate admits — 81 rows in all.

**This document describes; it does not adjudicate.** The gate reads the live Python
vocabulary in `dsx/checks/viz.py` and `dsx/spec.py`, never this file. Its correctness
is machine-checked by `tests/test_chart_catalog_invariant.py`: every admissible mark
appears exactly once, every refusal row is backed by a live ban, and the perceptual
rank data obeys the Cleveland–McGill ordering.

## The three axes

- **Function** — the nine-category axis of the *Financial Times Visual Vocabulary*
  (2016), attributed to the FT: <https://github.com/ft-interactive/chart-doctor/tree/main/visual-vocabulary>.
  All descriptions here are **our own**. The FT's own repo is internally
  inconsistent about its license: `visual-vocabulary/README.md` states
  "Copyright © The Financial Times Limited, all rights reserved," while the
  poster image itself (`poster.png`) prints "© Financial Times 2016-2019. This
  work is licensed under a Creative Commons Attribution-ShareAlike 4.0
  International License" in its own footer — confirmed by direct inspection of
  both, 2026-09 post-ship audit. We rely on neither claim: nothing is copied
  from the poster or README regardless (own descriptions only), and no claim of
  *exhaustiveness* rests on it (the poster disclaims that in its own words).
  Wilke's **Uncertainty** category (2019 §5.6) is carried as an eleventh
  function for the ten uncertainty marks.
- **Data signature** — a DSX input-type shape (a `CHART_CAPABILITIES` family, or an
  `IT0NN` inventory id) describing the column pattern the mark reads.
- **Perceptual channel** — the elementary channel the mark uses to encode its value,
  ranked by **Cleveland & McGill (1984)**, *JASA* 79:531–554 (p.536 list; p.537 tie
  caveat). The ranking has **ties**: ranks 3, 5 and 6 each hold more than one channel,
  and the 1984 paper states there is not enough information to separate them. The
  `density` channel does **not** appear in that paper and is absent here.

## Provenance note — one lineage, not three

The FT Visual Vocabulary, the Graphic Continuum and the Data Visualisation Catalogue
are **not independent authorities**: Ribecca authored both the Graphic Continuum and
the Data Visualisation Catalogue, and the FT poster credits the Graphic Continuum as
its inspiration. Rows here are cited to a single named source; no row claims
independent triangulation across that shared lineage. Genuinely independent support
comes from Cleveland & McGill (perception) and Wilke (uncertainty).

## Catalog

| Function | Mark / name | Data signature | Perceptual channel | Flag | Citation |
|---|---|---|---|---|---|
| Change over Time | `area` | bivariate-simple | length | dsx_admissible | FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark |
| Magnitude | `bar` | bivariate-simple | length | dsx_admissible | FT Visual Vocabulary 2016, Magnitude (function axis, D-3, HQ-27); DSX admissible mark |
| Magnitude | `big_number` | single-value | position_common | dsx_admissible | FT Visual Vocabulary 2016, Magnitude (function axis, D-3, HQ-27); DSX admissible mark |
| Distribution | `box` | interval-range | position_common | dsx_admissible | FT Visual Vocabulary 2016, Distribution (function axis, D-3, HQ-27); DSX admissible mark |
| Correlation | `bubble` | trivariate | area | dsx_admissible | FT Visual Vocabulary 2016, Correlation (function axis, D-3, HQ-27); DSX admissible mark |
| Magnitude | `bullet` | categorical-value | length | dsx_admissible | FT Visual Vocabulary 2016, Magnitude (function axis, D-3, HQ-27); DSX admissible mark |
| Ranking | `bump` | categorical-multi | direction | dsx_admissible | FT Visual Vocabulary 2016, Ranking (function axis, D-3, HQ-27); DSX admissible mark |
| Magnitude | `butterfly` | IT011 | length | dsx_admissible | FT Visual Vocabulary 2016, Magnitude (function axis, D-3, HQ-27); DSX admissible mark |
| Change over Time | `candlestick` | financial-ohlc | position_common | dsx_admissible | FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark |
| Spatial | `cartogram` | geospatial | area | dsx_admissible | FT Visual Vocabulary 2016, Spatial (function axis, D-3, HQ-27); DSX admissible mark |
| Flow | `chord` | matrix | length | dsx_admissible | FT Visual Vocabulary 2016, Flow (function axis, D-3, HQ-27); DSX admissible mark |
| Spatial | `choropleth` | geospatial | colour_saturation | dsx_admissible | FT Visual Vocabulary 2016, Spatial (function axis, D-3, HQ-27); DSX admissible mark |
| Part-to-whole | `circle_pack` | hierarchical | area | dsx_admissible | FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark |
| Magnitude | `column` | bivariate-simple | length | dsx_admissible | FT Visual Vocabulary 2016, Magnitude (function axis, D-3, HQ-27); DSX admissible mark |
| Change over Time | `column_range` | financial-ohlc | position_common | dsx_admissible | FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark |
| Uncertainty | `confidence_band` | interval-range | position_common | dsx_admissible | Wilke 2019, Fundamentals of Data Visualization, ch.5 §5.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070 |
| Uncertainty | `confidence_strips` | interval-range | position_common | dsx_admissible | Wilke 2019, Fundamentals of Data Visualization, ch.5 §5.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070 |
| Distribution | `density` | interval-range | area | dsx_admissible | FT Visual Vocabulary 2016, Distribution (function axis, D-3, HQ-27); DSX admissible mark |
| Deviation | `diverging_bar` | categorical-value | length | dsx_admissible | FT Visual Vocabulary 2016, Deviation (function axis, D-3, HQ-27); DSX admissible mark |
| Part-to-whole | `donut` | categorical-value | angle | dsx_admissible | FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark |
| Magnitude | `dot_plot` | categorical-value | position_common | dsx_admissible | FT Visual Vocabulary 2016, Magnitude (function axis, D-3, HQ-27); DSX admissible mark |
| Deviation | `dumbbell` | categorical-multi | position_common | dsx_admissible | FT Visual Vocabulary 2016, Deviation (function axis, D-3, HQ-27); DSX admissible mark |
| Distribution | `ecdf` | interval-range | position_common | dsx_admissible | FT Visual Vocabulary 2016, Distribution (function axis, D-3, HQ-27); DSX admissible mark |
| Uncertainty | `error_bars` | interval-range | position_common | dsx_admissible | Wilke 2019, Fundamentals of Data Visualization, ch.5 §5.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070 |
| Uncertainty | `error_bars_2d` | interval-range | position_common | dsx_admissible | Wilke 2019, Fundamentals of Data Visualization, ch.5 §5.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070 |
| Uncertainty | `eye` | interval-range | position_common | dsx_admissible | Wilke 2019, Fundamentals of Data Visualization, ch.5 §5.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070 |
| Uncertainty | `fitted_draws` | interval-range | position_common | dsx_admissible | Wilke 2019, Fundamentals of Data Visualization, ch.5 §5.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070 |
| Flow | `funnel` | event-time | length | dsx_admissible | FT Visual Vocabulary 2016, Flow (function axis, D-3, HQ-27); DSX admissible mark |
| Change over Time | `gantt` | event-time | length | dsx_admissible | FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark |
| Uncertainty | `graded_confidence_band` | interval-range | position_common | dsx_admissible | Wilke 2019, Fundamentals of Data Visualization, ch.5 §5.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070 |
| Uncertainty | `graded_error_bars` | interval-range | position_common | dsx_admissible | Wilke 2019, Fundamentals of Data Visualization, ch.5 §5.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070 |
| Magnitude | `grouped_bar` | bivariate-dual | length | dsx_admissible | FT Visual Vocabulary 2016, Magnitude (function axis, D-3, HQ-27); DSX admissible mark |
| Uncertainty | `half_eye` | interval-range | position_common | dsx_admissible | Wilke 2019, Fundamentals of Data Visualization, ch.5 §5.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070 |
| Correlation | `heatmap` | trivariate | colour_saturation | dsx_admissible | FT Visual Vocabulary 2016, Correlation (function axis, D-3, HQ-27); DSX admissible mark |
| Correlation | `hexbin` | trivariate | colour_saturation | dsx_admissible | FT Visual Vocabulary 2016, Correlation (function axis, D-3, HQ-27); DSX admissible mark |
| Distribution | `histogram` | interval-range | length | dsx_admissible | FT Visual Vocabulary 2016, Distribution (function axis, D-3, HQ-27); DSX admissible mark |
| Magnitude | `horizontal_bar` | bivariate-simple | length | dsx_admissible | FT Visual Vocabulary 2016, Magnitude (function axis, D-3, HQ-27); DSX admissible mark |
| Part-to-whole | `icicle` | hierarchical | area | dsx_admissible | FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark |
| Distribution | `kde` | interval-range | area | dsx_admissible | FT Visual Vocabulary 2016, Distribution (function axis, D-3, HQ-27); DSX admissible mark |
| Change over Time | `line` | bivariate-simple | position_common | dsx_admissible | FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark |
| Change over Time | `multi_line` | bivariate-dual | position_common | dsx_admissible | FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark |
| Change over Time | `ohlc_bar` | financial-ohlc | position_common | dsx_admissible | FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark |
| Part-to-whole | `pie` | categorical-value | angle | dsx_admissible | FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark |
| Distribution | `population_pyramid` | IT011 | length | dsx_admissible | FT Visual Vocabulary 2016, Distribution (function axis, D-3, HQ-27); DSX admissible mark |
| Uncertainty | `quantile_dot_plot` | interval-range | position_common | dsx_admissible | Wilke 2019, Fundamentals of Data Visualization, ch.5 §5.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070 |
| Flow | `sankey` | matrix | length | dsx_admissible | FT Visual Vocabulary 2016, Flow (function axis, D-3, HQ-27); DSX admissible mark |
| Correlation | `scatter` | bivariate-simple | position_common | dsx_admissible | FT Visual Vocabulary 2016, Correlation (function axis, D-3, HQ-27); DSX admissible mark |
| Change over Time | `slope` | categorical-multi | direction | dsx_admissible | FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark |
| Change over Time | `sparkline` | time-series | position_common | dsx_admissible | FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark |
| Change over Time | `stacked_area` | time-series | length | dsx_admissible | FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark |
| Part-to-whole | `stacked_bar` | categorical-multi | length | dsx_admissible | FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark |
| Change over Time | `stream` | time-series | length | dsx_admissible | FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark |
| Distribution | `strip` | interval-range | position_common | dsx_admissible | FT Visual Vocabulary 2016, Distribution (function axis, D-3, HQ-27); DSX admissible mark |
| Part-to-whole | `sunburst` | hierarchical | angle | dsx_admissible | FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark |
| Spatial | `symbol_map` | geospatial | area | dsx_admissible | FT Visual Vocabulary 2016, Spatial (function axis, D-3, HQ-27); DSX admissible mark |
| Change over Time | `timeline` | event-time | position_common | dsx_admissible | FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark |
| Part-to-whole | `treemap` | composition | area | dsx_admissible | FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark |
| Distribution | `violin` | interval-range | area | dsx_admissible | FT Visual Vocabulary 2016, Distribution (function axis, D-3, HQ-27); DSX admissible mark |
| Part-to-whole | `waffle` | categorical-value | area | dsx_admissible | FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark |
| Part-to-whole | `waterfall` | composition | length | dsx_admissible | FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark |
| Deviation | `surplus_deficit_filled_line` | time-series | length | reference_only | FT Visual Vocabulary 2016, Deviation (reference-only; D-3, HQ-27) |
| Deviation | `spine_chart` | categorical-value | length | reference_only | FT Visual Vocabulary 2016, Deviation (reference-only; D-3, HQ-27) |
| Correlation | `connected_scatterplot` | bivariate-simple | position_common | reference_only | FT Visual Vocabulary 2016, Correlation (reference-only; D-3, HQ-27) |
| Distribution | `contour` | trivariate | shading | reference_only | Wilke 2019 ch.18 (2D distributions; reference-only; T2-2, HQ-27) |
| Ranking | `lollipop` | categorical-value | position_common | reference_only | FT Visual Vocabulary 2016, Ranking (reference-only; D-3, HQ-27) |
| Distribution | `beeswarm` | interval-range | position_common | reference_only | FT Visual Vocabulary 2016, Distribution (reference-only; D-3, HQ-27) |
| Distribution | `ridgeline` | interval-range | area | reference_only | Wilke 2019 ch.9 (ridgeline plots; reference-only; T2-2, HQ-27) |
| Change over Time | `calendar_heatmap` | time-series | colour_saturation | reference_only | FT Visual Vocabulary 2016, Change over Time (reference-only; D-3, HQ-27) |
| Change over Time | `priestley_timeline` | event-time | length | reference_only | FT Visual Vocabulary 2016, Change over Time (reference-only; D-3, HQ-27) |
| Magnitude | `marimekko` | composition | area | reference_only | FT Visual Vocabulary 2016, Magnitude (reference-only; D-3, HQ-27) |
| Part-to-whole | `voronoi` | hierarchical | area | reference_only | FT Visual Vocabulary 2016, Part-to-whole (reference-only; D-3, HQ-27) |
| Spatial | `dot_map` | geospatial | position_common | reference_only | FT Visual Vocabulary 2016, Spatial (dot density; reference-only; D-3, HQ-27) |
| Spatial | `flow_map` | geospatial | length | reference_only | FT Visual Vocabulary 2016, Spatial (flow map; reference-only; D-3, HQ-27) |
| Flow | `network_diagram` | matrix | position_nonaligned | reference_only | FT Visual Vocabulary 2016, Flow (network; reference-only; D-3, HQ-27) |
| Magnitude | `3d_bar` | categorical-value | volume | refusal | Munzner 2014 ch.6 (no unjustified 3D); Tufte 1983 (chartjunk) — HQ-27 T2-6/T3-3 |
| Change over Time | `3d_line` | time-series | volume | refusal | Munzner 2014 ch.6 (no unjustified 3D); Tufte 1983 (chartjunk) — HQ-27 T2-6/T3-3 |
| Part-to-whole | `3d_pie` | categorical-value | volume | refusal | Munzner 2014 ch.6 (no unjustified 3D); Tufte 1983 (chartjunk) — HQ-27 T2-6/T3-3 |
| Correlation | `dual_axis_line` | bivariate-dual | position_common | refusal | Muth 2018 (Datawrapper), as amended July 2026 — HQ-27 T3-4/D-4; Datawrapper carved out expert audiences, the unconditional ban is DSX's own general-audience position; see also DSX-VIZ-030 |
| Magnitude | `gauge` | single-value | angle | refusal | Few 2006 (Information Dashboard Design) §3.2 / §6.2.1.1 — HQ-27 T3-GAUGE; arbitrary-maximum criticism is DSX's own, not Few's |
| Magnitude | `radar` | categorical-multi | area | refusal | Duan et al. 2023 (J Clin Epidemiol 156:85-94), Introduction — area-vs-axis-order and area-proportional-to-square-of-value criticisms; HQ-27 Tier-3 |
| Magnitude | `word_cloud` | categorical-value | area | refusal | Jacob Harris, 'Word clouds considered harmful', Nieman Journalism Lab 2011-10-13 — HQ-27; editorial rationale, not perceptual |

## Machine-readable payload

```json
{
  "perceptual_ranks": {
    "position_common": 1,
    "position_nonaligned": 2,
    "length": 3,
    "direction": 3,
    "angle": 3,
    "area": 4,
    "volume": 5,
    "curvature": 5,
    "shading": 6,
    "colour_saturation": 6
  },
  "rows": [
    {
      "mark": "area",
      "function": "Change over Time",
      "description": "A area mark.",
      "data_signature": "bivariate-simple",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "bar",
      "function": "Magnitude",
      "description": "Amounts across categories, encoded as length from a zero baseline.",
      "data_signature": "bivariate-simple",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Magnitude (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "big_number",
      "function": "Magnitude",
      "description": "A big number mark.",
      "data_signature": "single-value",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Magnitude (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "box",
      "function": "Distribution",
      "description": "A box mark.",
      "data_signature": "interval-range",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Distribution (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "bubble",
      "function": "Correlation",
      "description": "A bubble mark.",
      "data_signature": "trivariate",
      "perceptual_channel": "area",
      "citation": "FT Visual Vocabulary 2016, Correlation (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "bullet",
      "function": "Magnitude",
      "description": "A bullet mark.",
      "data_signature": "categorical-value",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Magnitude (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "bump",
      "function": "Ranking",
      "description": "A bump mark.",
      "data_signature": "categorical-multi",
      "perceptual_channel": "direction",
      "citation": "FT Visual Vocabulary 2016, Ranking (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "butterfly",
      "function": "Magnitude",
      "description": "A butterfly mark.",
      "data_signature": "IT011",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Magnitude (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "candlestick",
      "function": "Change over Time",
      "description": "A candlestick mark.",
      "data_signature": "financial-ohlc",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "cartogram",
      "function": "Spatial",
      "description": "A cartogram mark.",
      "data_signature": "geospatial",
      "perceptual_channel": "area",
      "citation": "FT Visual Vocabulary 2016, Spatial (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "chord",
      "function": "Flow",
      "description": "A chord mark.",
      "data_signature": "matrix",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Flow (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "choropleth",
      "function": "Spatial",
      "description": "A value per region, encoded as fill colour on a map.",
      "data_signature": "geospatial",
      "perceptual_channel": "colour_saturation",
      "citation": "FT Visual Vocabulary 2016, Spatial (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "circle_pack",
      "function": "Part-to-whole",
      "description": "A circle pack mark.",
      "data_signature": "hierarchical",
      "perceptual_channel": "area",
      "citation": "FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "column",
      "function": "Magnitude",
      "description": "A column mark.",
      "data_signature": "bivariate-simple",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Magnitude (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "column_range",
      "function": "Change over Time",
      "description": "A column range mark.",
      "data_signature": "financial-ohlc",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "confidence_band",
      "function": "Uncertainty",
      "description": "A confidence band mark.",
      "data_signature": "interval-range",
      "perceptual_channel": "position_common",
      "citation": "Wilke 2019, Fundamentals of Data Visualization, ch.5 \u00a75.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070",
      "flag": "dsx_admissible"
    },
    {
      "mark": "confidence_strips",
      "function": "Uncertainty",
      "description": "A confidence strips mark.",
      "data_signature": "interval-range",
      "perceptual_channel": "position_common",
      "citation": "Wilke 2019, Fundamentals of Data Visualization, ch.5 \u00a75.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070",
      "flag": "dsx_admissible"
    },
    {
      "mark": "density",
      "function": "Distribution",
      "description": "A density mark.",
      "data_signature": "interval-range",
      "perceptual_channel": "area",
      "citation": "FT Visual Vocabulary 2016, Distribution (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "diverging_bar",
      "function": "Deviation",
      "description": "A diverging bar mark.",
      "data_signature": "categorical-value",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Deviation (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "donut",
      "function": "Part-to-whole",
      "description": "A donut mark.",
      "data_signature": "categorical-value",
      "perceptual_channel": "angle",
      "citation": "FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "dot_plot",
      "function": "Magnitude",
      "description": "A dot plot mark.",
      "data_signature": "categorical-value",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Magnitude (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "dumbbell",
      "function": "Deviation",
      "description": "A dumbbell mark.",
      "data_signature": "categorical-multi",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Deviation (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "ecdf",
      "function": "Distribution",
      "description": "A ecdf mark.",
      "data_signature": "interval-range",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Distribution (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "error_bars",
      "function": "Uncertainty",
      "description": "A point estimate with an interval showing its uncertainty.",
      "data_signature": "interval-range",
      "perceptual_channel": "position_common",
      "citation": "Wilke 2019, Fundamentals of Data Visualization, ch.5 \u00a75.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070",
      "flag": "dsx_admissible"
    },
    {
      "mark": "error_bars_2d",
      "function": "Uncertainty",
      "description": "A error bars 2d mark.",
      "data_signature": "interval-range",
      "perceptual_channel": "position_common",
      "citation": "Wilke 2019, Fundamentals of Data Visualization, ch.5 \u00a75.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070",
      "flag": "dsx_admissible"
    },
    {
      "mark": "eye",
      "function": "Uncertainty",
      "description": "A eye mark.",
      "data_signature": "interval-range",
      "perceptual_channel": "position_common",
      "citation": "Wilke 2019, Fundamentals of Data Visualization, ch.5 \u00a75.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070",
      "flag": "dsx_admissible"
    },
    {
      "mark": "fitted_draws",
      "function": "Uncertainty",
      "description": "A fitted draws mark.",
      "data_signature": "interval-range",
      "perceptual_channel": "position_common",
      "citation": "Wilke 2019, Fundamentals of Data Visualization, ch.5 \u00a75.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070",
      "flag": "dsx_admissible"
    },
    {
      "mark": "funnel",
      "function": "Flow",
      "description": "A funnel mark.",
      "data_signature": "event-time",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Flow (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "gantt",
      "function": "Change over Time",
      "description": "A gantt mark.",
      "data_signature": "event-time",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "graded_confidence_band",
      "function": "Uncertainty",
      "description": "A graded confidence band mark.",
      "data_signature": "interval-range",
      "perceptual_channel": "position_common",
      "citation": "Wilke 2019, Fundamentals of Data Visualization, ch.5 \u00a75.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070",
      "flag": "dsx_admissible"
    },
    {
      "mark": "graded_error_bars",
      "function": "Uncertainty",
      "description": "A graded error bars mark.",
      "data_signature": "interval-range",
      "perceptual_channel": "position_common",
      "citation": "Wilke 2019, Fundamentals of Data Visualization, ch.5 \u00a75.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070",
      "flag": "dsx_admissible"
    },
    {
      "mark": "grouped_bar",
      "function": "Magnitude",
      "description": "A grouped bar mark.",
      "data_signature": "bivariate-dual",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Magnitude (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "half_eye",
      "function": "Uncertainty",
      "description": "A half eye mark.",
      "data_signature": "interval-range",
      "perceptual_channel": "position_common",
      "citation": "Wilke 2019, Fundamentals of Data Visualization, ch.5 \u00a75.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070",
      "flag": "dsx_admissible"
    },
    {
      "mark": "heatmap",
      "function": "Correlation",
      "description": "A value over two categorical axes, encoded as colour intensity.",
      "data_signature": "trivariate",
      "perceptual_channel": "colour_saturation",
      "citation": "FT Visual Vocabulary 2016, Correlation (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "hexbin",
      "function": "Correlation",
      "description": "A hexbin mark.",
      "data_signature": "trivariate",
      "perceptual_channel": "colour_saturation",
      "citation": "FT Visual Vocabulary 2016, Correlation (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "histogram",
      "function": "Distribution",
      "description": "The shape of one numeric variable, binned into counts.",
      "data_signature": "interval-range",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Distribution (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "horizontal_bar",
      "function": "Magnitude",
      "description": "A horizontal bar mark.",
      "data_signature": "bivariate-simple",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Magnitude (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "icicle",
      "function": "Part-to-whole",
      "description": "A icicle mark.",
      "data_signature": "hierarchical",
      "perceptual_channel": "area",
      "citation": "FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "kde",
      "function": "Distribution",
      "description": "A kde mark.",
      "data_signature": "interval-range",
      "perceptual_channel": "area",
      "citation": "FT Visual Vocabulary 2016, Distribution (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "line",
      "function": "Change over Time",
      "description": "A quantity's path over an ordered domain, read as position.",
      "data_signature": "bivariate-simple",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "multi_line",
      "function": "Change over Time",
      "description": "A multi line mark.",
      "data_signature": "bivariate-dual",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "ohlc_bar",
      "function": "Change over Time",
      "description": "A ohlc bar mark.",
      "data_signature": "financial-ohlc",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "pie",
      "function": "Part-to-whole",
      "description": "A single set of parts of a whole, encoded as angle.",
      "data_signature": "categorical-value",
      "perceptual_channel": "angle",
      "citation": "FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "population_pyramid",
      "function": "Distribution",
      "description": "A population pyramid mark.",
      "data_signature": "IT011",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Distribution (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "quantile_dot_plot",
      "function": "Uncertainty",
      "description": "A quantile dot plot mark.",
      "data_signature": "interval-range",
      "perceptual_channel": "position_common",
      "citation": "Wilke 2019, Fundamentals of Data Visualization, ch.5 \u00a75.6 (D-2, HQ-27); DSX gate DSX-VIZ-071/070",
      "flag": "dsx_admissible"
    },
    {
      "mark": "sankey",
      "function": "Flow",
      "description": "A sankey mark.",
      "data_signature": "matrix",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Flow (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "scatter",
      "function": "Correlation",
      "description": "Two paired numeric variables, one point per observation.",
      "data_signature": "bivariate-simple",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Correlation (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "slope",
      "function": "Change over Time",
      "description": "A slope mark.",
      "data_signature": "categorical-multi",
      "perceptual_channel": "direction",
      "citation": "FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "sparkline",
      "function": "Change over Time",
      "description": "A sparkline mark.",
      "data_signature": "time-series",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "stacked_area",
      "function": "Change over Time",
      "description": "A stacked area mark.",
      "data_signature": "time-series",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "stacked_bar",
      "function": "Part-to-whole",
      "description": "A stacked bar mark.",
      "data_signature": "categorical-multi",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "stream",
      "function": "Change over Time",
      "description": "A stream mark.",
      "data_signature": "time-series",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "strip",
      "function": "Distribution",
      "description": "A strip mark.",
      "data_signature": "interval-range",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Distribution (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "sunburst",
      "function": "Part-to-whole",
      "description": "A sunburst mark.",
      "data_signature": "hierarchical",
      "perceptual_channel": "angle",
      "citation": "FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "symbol_map",
      "function": "Spatial",
      "description": "A symbol map mark.",
      "data_signature": "geospatial",
      "perceptual_channel": "area",
      "citation": "FT Visual Vocabulary 2016, Spatial (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "timeline",
      "function": "Change over Time",
      "description": "A timeline mark.",
      "data_signature": "event-time",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Change over Time (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "treemap",
      "function": "Part-to-whole",
      "description": "Nested parts of a whole, encoded as rectangle area.",
      "data_signature": "composition",
      "perceptual_channel": "area",
      "citation": "FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "violin",
      "function": "Distribution",
      "description": "A violin mark.",
      "data_signature": "interval-range",
      "perceptual_channel": "area",
      "citation": "FT Visual Vocabulary 2016, Distribution (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "waffle",
      "function": "Part-to-whole",
      "description": "A waffle mark.",
      "data_signature": "categorical-value",
      "perceptual_channel": "area",
      "citation": "FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "mark": "waterfall",
      "function": "Part-to-whole",
      "description": "A waterfall mark.",
      "data_signature": "composition",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Part-to-whole (function axis, D-3, HQ-27); DSX admissible mark",
      "flag": "dsx_admissible"
    },
    {
      "name": "surplus_deficit_filled_line",
      "function": "Deviation",
      "description": "Fills against a reference line to show running surplus/deficit over time.",
      "data_signature": "time-series",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Deviation (reference-only; D-3, HQ-27)",
      "flag": "reference_only"
    },
    {
      "name": "spine_chart",
      "function": "Deviation",
      "description": "Two opposed magnitudes per category, split about a central axis.",
      "data_signature": "categorical-value",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Deviation (reference-only; D-3, HQ-27)",
      "flag": "reference_only"
    },
    {
      "name": "connected_scatterplot",
      "function": "Correlation",
      "description": "A scatter whose points are joined in time order, showing a path.",
      "data_signature": "bivariate-simple",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Correlation (reference-only; D-3, HQ-27)",
      "flag": "reference_only"
    },
    {
      "name": "contour",
      "function": "Distribution",
      "description": "A two-dimensional density shown as nested level curves.",
      "data_signature": "trivariate",
      "perceptual_channel": "shading",
      "citation": "Wilke 2019 ch.18 (2D distributions; reference-only; T2-2, HQ-27)",
      "flag": "reference_only"
    },
    {
      "name": "lollipop",
      "function": "Ranking",
      "description": "A ranked value shown as a dot at the end of a thin stem.",
      "data_signature": "categorical-value",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Ranking (reference-only; D-3, HQ-27)",
      "flag": "reference_only"
    },
    {
      "name": "beeswarm",
      "function": "Distribution",
      "description": "Every observation as a point, jittered to avoid overlap.",
      "data_signature": "interval-range",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Distribution (reference-only; D-3, HQ-27)",
      "flag": "reference_only"
    },
    {
      "name": "ridgeline",
      "function": "Distribution",
      "description": "Stacked, slightly overlapping density curves, one per group.",
      "data_signature": "interval-range",
      "perceptual_channel": "area",
      "citation": "Wilke 2019 ch.9 (ridgeline plots; reference-only; T2-2, HQ-27)",
      "flag": "reference_only"
    },
    {
      "name": "calendar_heatmap",
      "function": "Change over Time",
      "description": "A daily value laid out on a calendar grid, encoded as colour.",
      "data_signature": "time-series",
      "perceptual_channel": "colour_saturation",
      "citation": "FT Visual Vocabulary 2016, Change over Time (reference-only; D-3, HQ-27)",
      "flag": "reference_only"
    },
    {
      "name": "priestley_timeline",
      "function": "Change over Time",
      "description": "Durations as bars positioned along a shared time axis.",
      "data_signature": "event-time",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Change over Time (reference-only; D-3, HQ-27)",
      "flag": "reference_only"
    },
    {
      "name": "marimekko",
      "function": "Magnitude",
      "description": "A mosaic of tiles whose two dimensions both encode magnitude.",
      "data_signature": "composition",
      "perceptual_channel": "area",
      "citation": "FT Visual Vocabulary 2016, Magnitude (reference-only; D-3, HQ-27)",
      "flag": "reference_only"
    },
    {
      "name": "voronoi",
      "function": "Part-to-whole",
      "description": "A plane partitioned into cells by nearest-point regions.",
      "data_signature": "hierarchical",
      "perceptual_channel": "area",
      "citation": "FT Visual Vocabulary 2016, Part-to-whole (reference-only; D-3, HQ-27)",
      "flag": "reference_only"
    },
    {
      "name": "dot_map",
      "function": "Spatial",
      "description": "One dot per event at its location, showing spatial density.",
      "data_signature": "geospatial",
      "perceptual_channel": "position_common",
      "citation": "FT Visual Vocabulary 2016, Spatial (dot density; reference-only; D-3, HQ-27)",
      "flag": "reference_only"
    },
    {
      "name": "flow_map",
      "function": "Spatial",
      "description": "Movement between places, encoded as line width along routes.",
      "data_signature": "geospatial",
      "perceptual_channel": "length",
      "citation": "FT Visual Vocabulary 2016, Spatial (flow map; reference-only; D-3, HQ-27)",
      "flag": "reference_only"
    },
    {
      "name": "network_diagram",
      "function": "Flow",
      "description": "Entities as nodes and relations as edges, laid out for structure.",
      "data_signature": "matrix",
      "perceptual_channel": "position_nonaligned",
      "citation": "FT Visual Vocabulary 2016, Flow (network; reference-only; D-3, HQ-27)",
      "flag": "reference_only"
    },
    {
      "name": "3d_bar",
      "function": "Magnitude",
      "description": "Refused: 3D bars distort length with perspective and occlude the back rows.",
      "data_signature": "categorical-value",
      "perceptual_channel": "volume",
      "citation": "Munzner 2014 ch.6 (no unjustified 3D); Tufte 1983 (chartjunk) \u2014 HQ-27 T2-6/T3-3",
      "flag": "refusal",
      "banned_type": "3d_bar",
      "banning_code": "DSX-VIZ-001"
    },
    {
      "name": "3d_line",
      "function": "Change over Time",
      "description": "Refused: 3D lines make position unreadable without adding information.",
      "data_signature": "time-series",
      "perceptual_channel": "volume",
      "citation": "Munzner 2014 ch.6 (no unjustified 3D); Tufte 1983 (chartjunk) \u2014 HQ-27 T2-6/T3-3",
      "flag": "refusal",
      "banned_type": "3d_line",
      "banning_code": "DSX-VIZ-001"
    },
    {
      "name": "3d_pie",
      "function": "Part-to-whole",
      "description": "Refused: 3D pie exaggerates the slices nearest the viewer.",
      "data_signature": "categorical-value",
      "perceptual_channel": "volume",
      "citation": "Munzner 2014 ch.6 (no unjustified 3D); Tufte 1983 (chartjunk) \u2014 HQ-27 T2-6/T3-3",
      "flag": "refusal",
      "banned_type": "3d_pie",
      "banning_code": "DSX-VIZ-001"
    },
    {
      "name": "dual_axis_line",
      "function": "Correlation",
      "description": "Refused: Two y-scales let any pair of series be made to look correlated.",
      "data_signature": "bivariate-dual",
      "perceptual_channel": "position_common",
      "citation": "Muth 2018 (Datawrapper), as amended July 2026 \u2014 HQ-27 T3-4/D-4; Datawrapper carved out expert audiences, the unconditional ban is DSX's own general-audience position; see also DSX-VIZ-030 (_check_dual_axis)",
      "flag": "refusal",
      "banned_type": "dual_axis_line",
      "banning_code": "DSX-VIZ-001"
    },
    {
      "name": "gauge",
      "function": "Magnitude",
      "description": "Refused: A radial gauge wastes space with its circular form, gives no context for the single number, and leaves its scale unlabelled. (The arbitrary-maximum criticism is DSX's own reasoning, not Few's.)",
      "data_signature": "single-value",
      "perceptual_channel": "angle",
      "citation": "Few 2006 (Information Dashboard Design) \u00a73.2 / \u00a76.2.1.1 \u2014 HQ-27 T3-GAUGE; arbitrary-maximum criticism is DSX's own, not Few's",
      "flag": "refusal",
      "banned_type": "gauge",
      "banning_code": "DSX-VIZ-001"
    },
    {
      "name": "radar",
      "function": "Magnitude",
      "description": "Refused: Radar area scales with the square of the value and depends on axis order.",
      "data_signature": "categorical-multi",
      "perceptual_channel": "area",
      "citation": "Duan et al. 2023 (J Clin Epidemiol 156:85-94), Introduction \u2014 area-vs-axis-order and area-proportional-to-square-of-value criticisms; HQ-27 Tier-3",
      "flag": "refusal",
      "banned_type": "radar",
      "banning_code": "DSX-VIZ-001"
    },
    {
      "name": "word_cloud",
      "function": "Magnitude",
      "description": "Refused: A word cloud supports only the crudest textual analysis: it sizes words by raw length/frequency rather than meaning, strips context, and carries no narrative.",
      "data_signature": "categorical-value",
      "perceptual_channel": "area",
      "citation": "Jacob Harris, 'Word clouds considered harmful', Nieman Journalism Lab 2011-10-13 \u2014 HQ-27; editorial rationale, not perceptual",
      "flag": "refusal",
      "banned_type": "word_cloud",
      "banning_code": "DSX-VIZ-001"
    }
  ]
}
```
