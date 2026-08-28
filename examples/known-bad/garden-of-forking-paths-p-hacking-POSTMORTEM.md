# Post-mortem: a garden-of-forking-paths / p-hacking miss

Paired spec: `garden-of-forking-paths-p-hacking-ANALYSIS-SPEC.yaml`

Coverage class (REQ-P12-01): a documented p-hacking / garden-of-forking-paths
case.

## What was concluded

A lifecycle-marketing team reported that a personalised onboarding-email subject
line raised 14-day trial-to-paid conversion by 0.7 percentage points, p = 0.041,
and declared it ready to ship. The spec presents one primary outcome, one
comparison, one pre-declared test, and a computed effect with a confidence
interval — a clean, single-hypothesis experiment.

## Why it was wrong

The single reported result was selected from a large, undisclosed space of
analyses. The analyst tried alternative conversion windows (7-day, 14-day,
30-day), alternative subgroups (by plan tier, by acquisition channel, by region),
and alternative covariate adjustments, and reported the one specification that
crossed p < 0.05. None of that search is visible in the spec: `comparisons_looked_at`
is 1 and no `multiplicity.family` is declared, so the reported p-value is the
p-value of the winning path only.

This is the "garden of forking paths": when the choice of analysis is contingent
on the data, a nominal p-value no longer controls the error rate it appears to
control, even when the analyst runs only one analysis, because a *different*
dataset would have sent them down a *different* fork (Gelman, A. and Loken, E.
(2014), "The Statistical Crisis in Science", American Scientist volume 102 issue
6 page 460 — locator UNVERIFIED, page/section pending the pre-registered D-05
verbatim-quote human read at the Phase-12 UAT round). The general result that a
handful of undisclosed researcher degrees of freedom is sufficient to drive the
false-positive rate far above the nominal level is documented in Simmons, J. P.,
Nelson, L. D. and Simonsohn, U. (2011), "False-Positive Psychology",
Psychological Science volume 22 issue 11 pages 1359-1366 (DOI
10.1177/0956797611417632 — page/section locator UNVERIFIED). A concrete,
publicly documented instance is the Cornell Food and Brand Lab work, where the
lead author's own account of slicing one dataset into many analyses in search of
significance (Wansink, B. (2016), "The Grad Student Who Never Said No", personal
blog) was followed by a re-analysis cataloguing the resulting statistical
inconsistencies (van der Zee, T., Anaya, J. and Brown, N. J. L. (2017), "Statistical
heartburn: an attempt to digest four pizza publications from the Cornell Food and
Brand Lab", BMC Nutrition volume 3 article 54 — locator UNVERIFIED) and by
multiple retractions.

## Why a declaration-only gate misses it

The forking was never disclosed as a comparison family, so the shipped
undisclosed-multiplicity catch `DSX-EXP-051` has no signal to fire on:
`comparisons_looked_at` (1) does not exceed the reported test count (1), which is
exactly the analyst's incentive — report one path, disclose one comparison.
Catching this requires the currently-unwritten frequentist
**specification-sensitivity** check — does the conclusion survive alternative model
specifications — the frequentist half of `brief.md` §6.5 item 1 (prior
justification and prior sensitivity / specification sensitivity). Until that check
exists, this case is a miss; its catch-attribution (`absent_code: DSX-EXP-051`,
`promotes_backlog_item`: the §6.5 item-1 row) lives in the paired
`garden-of-forking-paths-p-hacking-ATTRIBUTION.yaml` sidecar, not in the spec, so
`frame_digest` is unperturbed (placement precedent 11.2 D-08, `dsx/decisions.py`
lines 99-121).

## Incidental gaps

At `dsx gate verify`/`ship` this fixture also blocks on the shared
corpus-completeness gaps every hand-authored fixture carries — `DSX-CLM-031`,
`DSX-COH-031`, `DSX-DEC-001`, `DSX-MET-040`, `DSX-NAR-001`, `DSX-REP-030` and
`DSX-REP-050` — none of which is the encoded defect. See `_INCIDENTAL_GAP_CODES`
in `tests/test_known_bad_corpus.py`.
