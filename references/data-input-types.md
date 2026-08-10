# Data input types → chart capabilities

Closed vocabulary for `visuals[].data_input_type`. When set, `visuals[].type`
must be in the admissible set (`dsx vocab` → `chart_capabilities`).

There are two levels of precision, and `data_input_type` accepts either:

- **Coarse families** — the table below. Use when the column signature is
  obvious and you only need the broad shape.
- **Inventory ids `IT001`–`IT040`** — see
  [input-type-inventory.md](input-type-inventory.md). Use when the shape is
  specific enough to matter. This is the more precise declaration and narrows
  the permitted marks further.

Ask the lookup rather than guessing:

```bash
dsx charts IT005 --relationship comparison   # → bar, bullet, dot_plot, horizontal_bar
dsx charts --list                            # → the whole catalogue
```

| ID | Typical signature | Primary marks (dsx names) |
|---|---|---|
| `bivariate-simple` | numeric × numeric | line, scatter, area, bar |
| `bivariate-dual` | x + two y series | line, grouped_bar, area |
| `trivariate` | x, y, z | scatter, bubble, heatmap |
| `categorical-value` | category × value | bar, horizontal_bar, pie, waffle |
| `categorical-multi` | category × several values | grouped_bar, stacked_bar, slope |
| `time-series` | time × value(s) | line, area, sparkline, stacked_area |
| `interval-range` | category × interval | box, violin, bullet, dot_plot |
| `grouped-categorical` | group × category × value | grouped_bar, stacked_bar, heatmap |
| `composition` | parts of a whole | stacked_bar, pie, treemap, waffle |
| `hierarchical` | nested parts | treemap, sunburst |
| `matrix` | row × column × value | heatmap, chord |
| `event-time` | events on a timeline | line, scatter, funnel, timeline |

## How to use

1. Name the **relationship** (comparison, trend, …) — still required.
2. Name the **data_input_type** from the table.
3. Pick `type` from the intersection of relationship admissibility and this matrix.
4. Run `dsx check viz`.

Adapted from the Deterministic Data Visualization Framework input-type schema;
dsx mark names stay underscored to match `RELATIONSHIP_CHARTS`.
