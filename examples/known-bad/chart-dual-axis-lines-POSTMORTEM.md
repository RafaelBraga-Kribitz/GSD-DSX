# Post-mortem: two series on two y-axes

Paired spec: `chart-dual-axis-lines-ANALYSIS-SPEC.yaml`

One of the nineteen **DSX-VIZ coverage fixtures** added 2026-09-06 to close the
post-ship audit's escalated item 2 (`.planning/POST-SHIP-AUDIT-2026-09.md`): before
them, 17 of the family's 21 codes had never fired against a constructed case. Phase
24 (GA-2 / S4-1) had deliberately scoped chart fixtures to the codes minted in v2.4;
the operator reversed that scoping by direction on 2026-09-06, so every pre-existing
`DSX-VIZ-*` code now has a fixture whose sole purpose is to fire it. The underlying
spec is a copy of the clean `examples/good-corpus/freq-continuous-timeontask` control
— it clears `dsx gate plan` and `dsx gate execute` exactly like its base — so the only
thing wrong with it is the one chart in `visuals[]`.

## What was concluded

An editor team plotted focused minutes per session and sessions per day on one
chart, one line each, with a second y-axis on the right for the session count. Both
lines "rose about 10%" over the fortnight, and the chart was read as showing that the
two moved together.

## Why it was wrong

The relative scaling of two independent y-axes is a free choice, so any two series
can be made to cross, diverge or track each other by picking the scales. The reader
infers a relationship that the chart did not establish and could not have. The
honest alternatives are two aligned panels sharing the x-axis, both series indexed
to a common base, or the ratio plotted directly if the ratio is the quantity of
interest. This fixture declares a plain `line` with `dual_axis: true` rather than the
banned `dual_axis_line` type, so that `DSX-VIZ-030` — the field-level check — is
exercised on its own rather than pre-empted by the banned-type refusal.

## Source

Muth, L.C. (2018), *Why not to use two axes, and what to use instead*, Datawrapper
blog — as amended July 2026, when Datawrapper carved out expert audiences (finance)
while still holding that general audiences misread dual axes. This is the same
citation `BANNED_TYPES["dual_axis_line"]` carries (HQ-27 T3-4 / D-4, signed
2026-09-03); the unconditional position for the general-audience default this project
assumes is DSX's own, recorded as such.

## Which code catches it

`DSX-VIZ-030` (HIGH) — `_check_dual_axis` in `dsx/checks/viz.py` fires on any visual
declaring `dual_axis: true`. HIGH blocks at `dsx gate verify` and `dsx gate ship`; the
corpus measures it in the HIGH stratum. Measured 2026-09-06: plan and execute exit 0;
verify and ship exit 1 with `DSX-VIZ-030` as the only finding above INFO. No new
finding code is minted.
