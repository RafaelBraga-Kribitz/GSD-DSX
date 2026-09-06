# Post-mortem: red versus green as the only distinction

Paired spec: `chart-red-green-only-ANALYSIS-SPEC.yaml`

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

The installs-per-account bar chart, with the control bar red and the treatment bar
green, and nothing else — no direct labels, no shape, no position cue — to tell the
two arms apart.

## Why it was wrong

Wilke (2019, ch.19 §19.3) gives the prevalence: "Approximately 8% of males and 0.5%
of females suffer from some sort of color-vision deficiency", and for the most common
forms red and green "become nearly indistinguishable for deutans or protans". For
those readers a chart whose only distinction is red-versus-green carries no
information at all — not a degraded chart, an empty one. The fix is a redundant
encoding (direct labels, shape, position) or a colourblind-safe pair such as
blue/orange. The check clears the moment `redundant_encoding` is declared, because
then colour is no longer the only channel.

## Source

Wilke, C.O. (2019), *Fundamentals of Data Visualization*, O'Reilly — ch.19 §19.3
(*Not designing for color-vision deficiency*), re-read against the online edition on
2026-09-06; the prevalence figures in `DSX-VIZ-051`'s detail text are Wilke's.

## Which code catches it

`DSX-VIZ-051` (HIGH) — `_check_color` in `dsx/checks/viz.py` fires on a `palette` of
`red_green` (or its aliases) with no `redundant_encoding`. HIGH blocks at
`dsx gate verify` and `dsx gate ship`; the corpus measures it in the HIGH stratum.
Measured 2026-09-06: plan and execute exit 0; verify and ship exit 1 with
`DSX-VIZ-051` as the only finding above INFO. No new finding code is minted.
