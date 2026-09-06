# Post-mortem: a chart that never says which relationship it shows

Paired spec: `chart-relationship-undeclared-ANALYSIS-SPEC.yaml`

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

A platform team declared a bar chart of installs per account by arm with a type, a
data signature, a zero baseline, units, a takeaway and a source — everything except
the `relationship` the reader is meant to extract from it.

## Why it was wrong

The chart type follows from the relationship, not the other way round. Without a
declared relationship there is nothing for the encoding check to compare the mark
against: `bar` is admissible for a comparison, a ranking, a part-to-whole and several
other relationships, and each of those licenses a different reading. A chart whose
author cannot say what comparison it makes has skipped the step that decides whether
the mark is honest. This is the "why before how" ordering that
`references/question-taxonomy.md` records from Munzner's task abstraction (2014,
ch.3): the task is fixed first, and the idiom is chosen to serve it.

## Source

Munzner, T. (2014), *Visualization Analysis and Design*, CRC Press, ch.3 (task
abstraction), as already recorded in `references/question-taxonomy.md`. The rule that
`relationship` is a required declaration is DSX's own contract criterion
(`references/chart-selection.md`), not a perceptual finding.

## Which code catches it

`DSX-VIZ-010` (MEDIUM) — `_check_relationship_match` in `dsx/checks/viz.py` reports a
visual with no `relationship` and returns before the mark-versus-relationship test can
run. Because it is MEDIUM it does not block at the default HIGH threshold of
`dsx gate verify` / `dsx gate ship`; the corpus measures it in the MEDIUM stratum under
`--block-on MEDIUM`, reported beside the headline miss-rate/FPR pair, never folded into
it. Measured 2026-09-06: plan and execute exit 0; verify and ship exit 0 at the default
threshold with `DSX-VIZ-010` as the only finding above INFO; exit 1 under
`--block-on MEDIUM`. No new finding code is minted.
