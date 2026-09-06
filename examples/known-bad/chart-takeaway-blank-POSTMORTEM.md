# Post-mortem: a chart with no takeaway at all

Paired spec: `chart-takeaway-blank-ANALYSIS-SPEC.yaml`

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

The installs-per-account bar chart, fully declared, with no `takeaway` — the chart
was to be titled with its variable name and left for the reader to interpret.

## Why it was wrong

A chart is an argument, and the title is where the argument is stated. Wilke (2019,
ch.22 §22.1) puts the title's job plainly: "to accurately convey to the reader what
the figure is about, what point it makes", and notes that "short sentences making a
clear assertion can serve as titles". A blank takeaway means the author has not
decided what the chart shows; every reader will decide differently, and the one who
decides wrong has no sentence to be corrected by. DSX's house rule — the takeaway is
the sentence you want remembered — is stricter than Wilke's "can serve as"; it is
recorded as DSX's own.

## Source

Wilke, C.O. (2019), *Fundamentals of Data Visualization*, O'Reilly — ch.22 §22.1
(*Figure titles and captions*), re-read against the online edition on 2026-09-06. The
requirement that every visual carry a takeaway sentence is DSX's own narrative
discipline (`references/narrative-discipline.md`).

## Which code catches it

Two codes, from one blank field. `_check_labelling` in `dsx/checks/viz.py` emits
`DSX-VIZ-060` (MEDIUM, "has no takeaway title") **and** `DSX-VIZ-063` (HIGH, "takeaway
is blank or identical to the chart name") whenever `takeaway` is blank — the HIGH code
is what blocks, the MEDIUM one names the missing element. This fixture is the corpus's
first two-tier catch: `DSX-VIZ-063` is its HIGH target (blocks at `dsx gate verify` /
`dsx gate ship`, measured in the HIGH stratum) and `DSX-VIZ-060` is its MEDIUM target
(measured under `--block-on MEDIUM`, beside the headline pair). `DSX-VIZ-063`'s other
branch — a takeaway that repeats the chart name — is isolated by the sibling fixture
`chart-takeaway-repeats-name`. Measured 2026-09-06: plan and execute exit 0; verify and
ship exit 1 with exactly these two findings above INFO. No new finding code is minted.
