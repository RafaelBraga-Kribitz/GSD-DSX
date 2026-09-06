# Post-mortem: an estimate drawn without its uncertainty

Paired spec: `chart-estimates-without-uncertainty-ANALYSIS-SPEC.yaml`

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

An editor team drew the focused-editing uplift per arm as a dot plot of two point
estimates — declaring `shows_estimates: true` and `shows_uncertainty: false` — with no
interval, no band and no error bar. The spec's own `results.tests[]` carries a 95%
interval of 0.8 to 2.0 minutes; the chart showed 1.4 and nothing else.

## Why it was wrong

An estimate is a number with a spread, and drawing only the number turns a range into
a fact. Wilke (2019, ch.16) devotes §16.2 to visualizing the uncertainty of point
estimates — error bars, graded error bars, confidence strips and the rest of the
vocabulary this project's `RELATIONSHIP_CHARTS["uncertainty"]` is built from — and
adds the condition that comes with them: "Whenever you visualize uncertainty with
error bars, you must specify what quantity and/or confidence level the error bars
represent." The consequence DSX names in the finding — that differences well inside
the noise will be acted on — is DSX's own phrasing of why the rule matters for a
decision readout, not a quotation.

## Source

Wilke, C.O. (2019), *Fundamentals of Data Visualization*, O'Reilly — ch.16 §16.2
(*Visualizing the uncertainty of point estimates*), the same chapter
`references/chart-catalog.md` cites for the uncertainty vocabulary (HQ-27); section
title and the error-bar condition re-read against the online edition on 2026-09-06.

## Which code catches it

`DSX-VIZ-070` (HIGH) — `_check_uncertainty` in `dsx/checks/viz.py` fires when a visual
declares `shows_estimates: true` without `shows_uncertainty: true`. It is the
property-level complement of `DSX-VIZ-071` (which checks the *name* of a declared
mark); this fixture and `chart-uncertainty-mark-misuse` between them cover both. HIGH
blocks at `dsx gate verify` and `dsx gate ship`; the corpus measures it in the HIGH
stratum. Measured 2026-09-06: plan and execute exit 0; verify and ship exit 1 with
`DSX-VIZ-070` as the only finding above INFO. No new finding code is minted.
