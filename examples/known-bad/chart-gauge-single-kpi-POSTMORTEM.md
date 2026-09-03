# Post-mortem: a single KPI shown on a radial gauge

Paired spec: `chart-gauge-single-kpi-ANALYSIS-SPEC.yaml`

This is one of the first **bad-chart-choice** fixtures in the corpus (Phase 24,
GA-2). Every earlier fixture encodes a bad *analysis* choice; these four encode a
bad *visual* choice on top of an otherwise clean, gate-passing analysis. The
underlying spec is a copy of the clean `examples/good-corpus/freq-count-installs`
control — it clears `dsx gate plan` and `dsx gate execute` exactly like its base —
so the only thing wrong with it is the one chart in `visuals[]`.

## What was concluded

An activation team reported "integrations installed per account" as a single
number on a radial gauge — a needle sweeping a coloured arc from an unlabelled
minimum to an unlabelled maximum, the current value called out in the centre.

## Why it was wrong

A gauge spends most of its ink on a circular form that carries no data, gives the
reader no context for the single number it shows (no baseline, no trend, no
comparison), and leaves its own scale — where the arc starts, where it ends, what
"good" is — unstated. The reader cannot tell whether 1.8 installs is strong or
weak, because the maximum the needle is measured against is arbitrary. A single
number is read faster as a labelled number with its comparison beside it; a small
multiple or a bullet chart delivers the same KPI with a target and a baseline in
the same space.

## Source

Few, S. (2006), *Information Dashboard Design*, O'Reilly — §3.2 / §6.2.1.1, the
critique of radial gauges as space-inefficient and context-free (HQ-27 T3-GAUGE,
signed 2026-09-03). The specific "the maximum is arbitrary" argument is **DSX's
own reasoning**, not Few's, and is recorded as such in `dsx/checks/viz.py`
`BANNED_TYPES["gauge"]`.

## Which code catches it

`DSX-VIZ-001` (HIGH) — `gauge` is a live member of `BANNED_TYPES` in
`dsx/checks/viz.py`, so `_check_banned` refuses it as a distorting/context-free
mark at the HIGH-threshold gate points, `dsx gate verify` and `dsx gate ship`.
The fixture routes to the **existing** `DSX-VIZ-001` (shared by all banned marks) —
no new finding code is minted for it. Its two incidental MEDIUM findings
(`DSX-VIZ-010` no relationship declared, `DSX-VIZ-014` no `data_input_type`) are
below the HIGH block threshold and are not what the fixture exists to demonstrate.
