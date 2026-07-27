# Visualization smells

Chart_Audit Framework smells A–M, split into **deterministic gates** (declared
fields on `visuals[]`) and **agent checklist** items that need notebook/code
judgement.

## Gated in dsx (`DSX-SMELL-*`)

| Smell | Code | Declaration |
|---|---|---|
| **B** Dead / broadcast series | `DSX-SMELL-002` | `within_group_std: 0` (or ≈0) |
| **G** Atoms under a density | `DSX-SMELL-007` | distribution + density/kde/violin + `atomicity: true` or `n_unique ≤ 5` |
| **I** Stacked scenarios | `DSX-SMELL-009` | `type: stacked_*` + `series_role: scenario` |
| **J** Missing categories | `DSX-SMELL-010` | `expected_categories` length ≠ `category_count` |
| **K** Self-correlation | `DSX-SMELL-011` | `ratio_of_x: true` or encodings y looks like `*/x` |
| **M** Cross-artifact drift | `DSX-SMELL-013` | differing `run_id` across visuals |

## Agent checklist (not coded in 1.2.0)

Use these in `dsx-viz-critic` after `dsx check viz smells figures` is clean:

| Smell | Look for |
|---|---|
| **A** | Walk-forward / OOS series is a different object than in-sample; no `observed=` on last latent reused as forecast |
| **C** | Interval label, column name, and table header agree on HDI vs quantile and the same run id |
| **D** | Rank charts where category spread ≲ a few SE — rank may be index noise |
| **E** | Systematic term ≈ 0 vs noise; difference is Monte Carlo noise |
| **F** | GeoJSON with ~5 pts/feature = bbox placeholders; colormap domain vs value range |
| **H** | Values clipped to a cap (`np.minimum(…, 1.0)`); contacts ≤ population |
| **L** | Closed-form / pre-data early window labelled synthetic/prior, not inference |

Source: Chart_Audit Framework `code-smells.md`.
