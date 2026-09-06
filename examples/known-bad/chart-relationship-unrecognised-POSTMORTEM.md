# Post-mortem: a relationship name outside the vocabulary

Paired spec: `chart-relationship-unrecognised-ANALYSIS-SPEC.yaml`

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

The same installs-per-account bar chart, fully declared, with
`relationship: comparision` — a misspelling of `comparison`.

## Why it was wrong

A closed vocabulary is only closed if a value outside it is reported rather than
quietly accepted. Had the check treated an unrecognised relationship as "no
relationship" and moved on, a typo would buy the same silence as an honest omission,
and the mark-versus-relationship test would never run. The declaration is present,
so the author believed the step was done; the finding exists to say that it was not.
This is the same out-of-vocabulary discipline the corpus already exercises for
`interference.risk` and `triggering.analysis_population` (plans 08-07/08-08, 08-09):
a misspelt member must never clear a check by being unrecognisable.

## Source

DSX's own contract criterion: the ten relationship keys of `RELATIONSHIP_CHARTS` plus
the Wilke-sourced `uncertainty` key form a closed set (`references/chart-selection.md`,
`references/chart-catalog.md`). No perceptual claim is made by this fixture.

## Which code catches it

`DSX-VIZ-011` (MEDIUM) — `_check_relationship_match` in `dsx/checks/viz.py` looks the
declared value up in `RELATIONSHIP_CHARTS` and reports a non-member, naming the
allowed set. MEDIUM does not block at the default HIGH threshold of `dsx gate verify`
/ `dsx gate ship`; the corpus measures it in the MEDIUM stratum under
`--block-on MEDIUM`, reported beside the headline pair. Measured 2026-09-06: plan and
execute exit 0; verify and ship exit 0 at the default threshold with `DSX-VIZ-011` as
the only finding above INFO; exit 1 under `--block-on MEDIUM`. No new finding code is
minted.
