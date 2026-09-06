# Post-mortem: a takeaway that names the variables and states no finding

Paired spec: `chart-takeaway-without-magnitude-ANALYSIS-SPEC.yaml`

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

A bar chart named "Integrations installed, by experiment arm" with the takeaway
"Installs per account by arm" — a different string from the name, so the
identical-to-name branch does not fire, but a string that still contains no number
and no comparison.

## Why it was wrong

The takeaway is meant to be the sentence the reader leaves with. "Installs per
account by arm" is a topic, not a sentence: it carries no magnitude (0.12), no
direction (higher), no comparison (than control). Wilke (2019, ch.22 §22.1) notes
that "short sentences making a clear assertion can serve as titles"; this one asserts
nothing. The check's heuristic — a digit, a percent sign, or one of a fixed list of
comparison words — is a deliberately crude structural proxy for "states a finding",
and this fixture is the case it exists for: a takeaway that is present, distinct from
the name, and empty of content.

## Source

Wilke, C.O. (2019), *Fundamentals of Data Visualization*, O'Reilly — ch.22 §22.1
(*Figure titles and captions*), re-read against the online edition on 2026-09-06. The
digit-or-comparison-token heuristic is DSX's own structural criterion
(`COMPARISON_TOKENS` in `dsx/checks/viz.py`), recorded as such.

## Which code catches it

`DSX-VIZ-064` (MEDIUM) — `_check_labelling` in `dsx/checks/viz.py` fires on a
non-blank takeaway, distinct from the name, that contains neither a digit nor a
comparison token. MEDIUM does not block at the default HIGH threshold of
`dsx gate verify` / `dsx gate ship`; the corpus measures it in the MEDIUM stratum under
`--block-on MEDIUM`, reported beside the headline pair. Measured 2026-09-06: plan and
execute exit 0; verify and ship exit 0 at the default threshold with `DSX-VIZ-064` as
the only finding above INFO; exit 1 under `--block-on MEDIUM`. No new finding code is
minted.
