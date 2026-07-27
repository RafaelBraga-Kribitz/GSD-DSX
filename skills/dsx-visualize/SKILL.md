---
name: dsx-visualize
description: "Choose and build charts whose encoding matches the relationship and whose geometry is proportional to the numbers. Use when producing any chart, dashboard or figure."
argument-hint: "[--relationship <type>] [--audit <file>]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
---

<objective>
A chart that makes the argument the data supports, and no larger one.
</objective>

<method>

1. **Name the relationship before the chart type.** comparison, trend,
   part_to_whole, distribution, correlation, deviation, ranking, flow,
   geographic, composition_over_time. The relationship determines the chart;
   choosing a chart first and fitting data to it is how pie charts happen.

2. **Write the takeaway as a sentence.** If you cannot state what the reader
   should conclude, the chart is not ready. That sentence becomes the title —
   "EMEA revenue fell 12% while every other region grew", not "Revenue by region".

3. **Pick the encoding.** Position and length are read accurately; angle, area
   and colour saturation are not. Reserve colour for categories or highlighting,
   and never as the only channel carrying a distinction.

4. **Fix the baseline.** Bars, areas and anything encoding length start at zero.
   Lines and scatters encode position and may be zoomed — label the axis so.

5. **Show uncertainty wherever you show an estimate.** A point estimate drawn as
   a solid bar reads as a fact, and differences well inside the noise get acted
   on.

6. **Subtract.** Remove gridlines, borders, legends replaceable by direct labels,
   and any third dimension. Each removal makes the rest easier to read.

7. **Audit.** `dsx check viz --phase-dir <phase-dir> --verbose`, then spawn
   `dsx-viz-critic` for the judgement the linter cannot make.

</method>

<hard_rules>
- Never a truncated baseline on a bar or area chart.
- Never two y-axes. The relative scaling is arbitrary, so any two series can be
  made to look related.
- Never a pie beyond five slices, and never in 3D.
- Never red/green as the sole distinction — roughly 8% of men cannot read it.
- Never a rainbow scale for a continuous variable; it invents boundaries.
- Never a chart without units, period and source. Charts travel without context.
</hard_rules>

<references>
@references/chart-selection.md
</references>
