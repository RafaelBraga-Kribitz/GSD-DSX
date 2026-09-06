# Post-mortem: a ranking chart sorted alphabetically

Paired spec: `chart-alphabetical-ranking-ANALYSIS-SPEC.yaml`

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

An editor team ranked editor surfaces by focused minutes per session on a horizontal
bar chart — declaring `relationship: ranking` — and listed the surfaces in
alphabetical order.

## Why it was wrong

A ranking chart exists to show the order, and alphabetical order hides it. Wilke
(2019, ch.6 §6.1) states the rule for bars: "If the bars represent unordered
categories, order them by ascending or descending data values", with the one
exception that a natural ordering (time, an ordered factor) should be kept. Editor
surfaces have no natural order, so the bars belong in value order; sorted
alphabetically the reader must scan every bar to find the leader the takeaway names.
The check accepts `by_value` and any declared natural order, and fires only on
`alphabetical`, `arbitrary` or `source_order` — the three orderings that encode
nothing.

## Source

Wilke, C.O. (2019), *Fundamentals of Data Visualization*, O'Reilly — ch.6 §6.1
(*Bar plots*; the ordering rule and its natural-order exception), re-read against the
online edition on 2026-09-06.

## Which code catches it

`DSX-VIZ-080` (LOW) — `_check_ordering` in `dsx/checks/viz.py` fires on a bar,
horizontal bar or dot plot whose `category_order` is `alphabetical`, `arbitrary` or
`source_order`. LOW does not block at any default gate threshold; the corpus measures
it in the LOW stratum under `--block-on LOW`, a readout reported beside the headline
pair, added with these fixtures because no LOW-tier code had a fixture before.
Measured 2026-09-06: plan and execute exit 0; verify and ship exit 0 at the default
threshold with `DSX-VIZ-080` as the only finding above INFO; exit 1 under
`--block-on LOW`. No new finding code is minted.
