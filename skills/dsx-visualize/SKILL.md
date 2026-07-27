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
A chart that makes the argument the data supports, and no larger one — sealed
so the gate can prove the bytes match the declaration.
</objective>

<method>

1. **Name the relationship before the chart type.** comparison, trend,
   part_to_whole, distribution, correlation, deviation, ranking, flow,
   geographic, composition_over_time.

2. **Name the data_input_type.** See `references/data-input-types.md` / `dsx vocab`.
   The mark must sit in both the relationship list and the input-type matrix.

3. **Write the takeaway as a sentence with a magnitude or comparison.** Not the
   chart name. That sentence becomes the title.

4. **Pick the encoding.** Position and length first; never stack when
   `series_role: scenario` — only `component` stacks.

5. **Write the artifact**, then seal it:
   ```bash
   dsx seal figures/<name>.svg
   ```
   Paste into `visuals[].svg_sha256`. Set `chart_id`, `artifact_path`, `generator`,
   and a shared `run_id` across figures from the same readout.

6. **Show uncertainty** wherever you show an estimate.

7. **Audit.**
   ```bash
   dsx check viz smells figures --phase-dir <phase-dir> --verbose
   ```
   Then spawn `dsx-viz-critic` for judgement the linter cannot make.

</method>

<hard_rules>
- Never a truncated baseline on a bar or area chart.
- Never two y-axes.
- Never a pie beyond five slices, and never in 3D.
- Never red/green as the sole distinction.
- Never a rainbow scale for a continuous variable.
- Never ship an `artifact_path` without `svg_sha256`.
- Never stack scenario / alternative series.
</hard_rules>

<references>
@references/chart-selection.md
@references/data-input-types.md
@references/viz-smells.md
</references>
