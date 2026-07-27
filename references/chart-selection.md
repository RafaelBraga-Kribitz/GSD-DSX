# Chart selection

The relationship determines the chart. Choosing a chart type first and fitting
data to it is how pie charts happen.

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

## Encoding accuracy

Readers decode these channels with decreasing accuracy:

position on a common scale → length → angle → area → colour saturation → volume

Put the most important quantity in the most accurate channel available. This is
why a sorted bar chart beats a pie for nearly every comparison, and why 3D
always loses — it converts an accurate channel into an inaccurate one and adds
occlusion.

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
