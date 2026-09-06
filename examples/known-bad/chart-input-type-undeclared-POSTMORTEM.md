# Post-mortem: a chart with no data signature declared

Paired spec: `chart-input-type-undeclared-ANALYSIS-SPEC.yaml`

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

The installs-per-account bar chart, declared with its relationship, zero baseline,
units, takeaway and source — but no `data_input_type`.

## Why it was wrong

The relationship says what comparison the reader should make; the data signature says
what column pattern the mark is reading. The two checks catch different mistakes. A
mark can suit the relationship and still be wrong for the data — a line for two
unordered measures, a bar for a single value — and only the input-type matrix sees
that. Leaving the signature undeclared switches that matrix off for the chart, so a
chart that passes the relationship test looks fully checked when half the check
never ran. The gauge, radar and word-cloud fixtures already fire this code
incidentally; this fixture isolates it, on a chart whose only defect is the missing
declaration.

## Source

DSX's own contract criterion: `data_input_type` is a required declaration drawn from
the closed `DATA_INPUT_TYPES` family names or the IT001–IT040 inventory
(`references/data-input-types.md`, `references/input-type-inventory.md`). No perceptual
claim is made by this fixture.

## Which code catches it

`DSX-VIZ-014` (MEDIUM) — `_check_input_type_matrix` in `dsx/checks/viz.py` reports a
visual with a chart type but no `data_input_type`, and returns before the matrix can
run. MEDIUM does not block at the default HIGH threshold of `dsx gate verify` /
`dsx gate ship`; the corpus measures it in the MEDIUM stratum under
`--block-on MEDIUM`, reported beside the headline pair. Measured 2026-09-06: plan and
execute exit 0; verify and ship exit 0 at the default threshold with `DSX-VIZ-014` as
the only finding above INFO; exit 1 under `--block-on MEDIUM`. No new finding code is
minted.
