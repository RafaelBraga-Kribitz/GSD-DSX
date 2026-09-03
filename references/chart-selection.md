# Chart selection

The relationship determines the chart. Choosing a chart type first and fitting
data to it is how pie charts happen.

See `references/chart-catalog.md` for the full citable vocabulary — every mark
with its function, data signature and perceptual channel.

| Relationship | Default | Also works | Avoid |
|---|---|---|---|
| comparison across categories | horizontal bar, sorted by value | dot plot, bullet | pie, radar |
| trend over time | line | area, sparkline, slope | bar, unless periods are discrete |
| part to whole | stacked bar | treemap, waffle | pie beyond 5 slices |
| distribution | histogram | box, violin, ECDF, strip | bar of means |
| correlation | scatter | hexbin, heatmap | dual-axis line |
| ranking | dot plot | horizontal bar, slope, bump | 3D anything |
| deviation from target | diverging bar | waterfall, dumbbell | gauge |
| flow | sankey | funnel, chord | stacked bar |
| geographic | choropleth | symbol map, cartogram | 3D map |
| composition over time | stacked area | stacked bar, stream | pie per period |
| uncertainty | error bars | other Wilke §5.6 marks (confidence strips, graded/gradient bands, eye, half-eye, quantile dot plot, fitted draws) | a point estimate with no interval |

The uncertainty row draws on Wilke's *Uncertainty* category (2019, ch.5 §5.6).

## Encoding accuracy

Readers decode these elementary channels with decreasing accuracy. The order is
Cleveland & McGill's (1984), and it is **six ranks with ties**, not a single
strict chain — three of the ranks hold more than one channel, and the paper
states there is not enough information to separate them (p.536 for the list,
p.537 for the tie caveat):

1. Position on a common scale
2. Position on non-aligned scales
3. Length, direction/slope, angle — *tied*
4. Area
5. Volume, curvature — *tied*
6. Shading, colour saturation — *tied*

"Density" is **not** one of these channels: it does not appear in the 1984
paper, so no rank is claimed for it.

Put the most important quantity in the most accurate channel available. This is
why a sorted bar chart beats a pie for nearly every comparison, and why 3D
always loses — it converts an accurate channel into an inaccurate one and adds
occlusion.

## Selection heuristic

Five layers take a question to a defensible chart. Layer 1 (question → task)
lives in `references/question-taxonomy.md`, citing Munzner's task taxonomy
(2014, ch.3 — Actions × Targets). Layers 2–5 are route-and-cite pointers into
surfaces that already exist — there is no separate decision tree to drift:

- **L2 — pick the relationship.** The nine function categories of the *Financial
  Times Visual Vocabulary* (2016, attributed to the FT), plus the eleventh
  **uncertainty** function (Wilke §5.6). Use the relationship table above and
  `references/chart-catalog.md`.
- **L3 — pick an admissible mark.** A mark must sit in both the relationship and
  its data signature. See `references/chart-catalog.md`'s three axes (function,
  data signature, perceptual channel); the gate enforces admissibility through
  DSX-VIZ-012 (relationship↔mark) and DSX-VIZ-013 (data-signature↔mark).
- **L4 — check the encoding channel.** Confirm the most important quantity sits
  in the most accurate channel available — the corrected rank list under
  "Encoding accuracy" above.
- **L5 — show uncertainty.** Route the uncertainty-mark choice to the ten Wilke
  §5.6 members (`references/chart-catalog.md`, Uncertainty function); the gate
  enforces this through DSX-VIZ-070 (property check) and DSX-VIZ-071 (vocabulary
  check).

## Non-negotiables

- **Zero baseline on anything length-encoded.** Bars, areas, waterfalls. The
  reader is decoding length; truncation breaks the proportionality. If the
  interesting variation is small, plot the difference or the percentage change on
  a position-encoded chart instead.
- **Never two y-axes.** The relative scaling is arbitrary, so any two series can
  be made to appear correlated. Use aligned panels sharing an x-axis, or index
  both series to a common base.
- **Show uncertainty wherever you show an estimate.** A point estimate drawn as a
  solid bar reads as a fact, and differences inside the noise get acted on.
- **Colourblind-safe palettes.** Roughly 8% of men cannot separate red from
  green. If colour carries meaning, add a redundant channel — shape, position,
  direct labels.
- **Perceptually uniform scales for continuous values.** Viridis, cividis, magma.
  Rainbow scales invent boundaries where the data is smooth.
- **Units, period and source on every chart.** Charts get screenshotted into
  Slack without their context.

## The title

The most-read element. Spending it on variable names wastes it.

- Weak: "Revenue by region"
- Strong: "EMEA revenue fell 12% while every other region grew"

If you cannot write the strong version, the chart is not ready — you have not
decided what it argues.

## Subtraction

Gridlines, borders, drop shadows, legends replaceable by direct labels, a third
dimension encoding nothing. Every removal makes the remaining marks easier to
read. Do this last, after the encoding is correct.
