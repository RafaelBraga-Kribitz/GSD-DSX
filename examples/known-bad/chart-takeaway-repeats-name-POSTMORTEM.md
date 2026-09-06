# Post-mortem: a takeaway that repeats the chart's name

Paired spec: `chart-takeaway-repeats-name-ANALYSIS-SPEC.yaml`

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

The installs-per-account bar chart, with `name: "Installs per account by arm"` and
`takeaway: "Installs per account by arm"` — the takeaway field filled in, with the
chart's own label.

## Why it was wrong

Filling the takeaway with the variable label satisfies the form and defeats the
purpose. A label says what was plotted; a takeaway says what was found. Wilke (2019,
ch.22 §22.1) gives the title the job of conveying "what point it makes", and a label
makes no point. This fixture exists separately from `chart-takeaway-blank` because the
check has two branches — blank, and identical-to-name — and a blank takeaway also
trips the MEDIUM "no takeaway title" code, whereas this one does not: the field is
present, non-empty, and worthless.

## Source

Wilke, C.O. (2019), *Fundamentals of Data Visualization*, O'Reilly — ch.22 §22.1
(*Figure titles and captions*), re-read against the online edition on 2026-09-06. The
requirement that the takeaway differ from the chart name is DSX's own narrative
discipline (`references/narrative-discipline.md`).

## Which code catches it

`DSX-VIZ-063` (HIGH) — `_check_labelling` in `dsx/checks/viz.py` fires when the
takeaway, case-folded and stripped, equals the chart's `name`. HIGH blocks at
`dsx gate verify` and `dsx gate ship`; the corpus measures it in the HIGH stratum.
Measured 2026-09-06: plan and execute exit 0; verify and ship exit 1 with
`DSX-VIZ-063` as the only finding above INFO — and, unlike the blank-takeaway sibling,
no `DSX-VIZ-060`. No new finding code is minted.
