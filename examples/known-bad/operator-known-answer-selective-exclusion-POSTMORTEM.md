# Post-mortem: an operator-known-answer control — undisclosed selective exclusion

Paired spec: `operator-known-answer-selective-exclusion-ANALYSIS-SPEC.yaml`

Coverage class (REQ-P12-01): an analysis whose answer is now known — a
known-answer positive control the operator holds the corrected result for.

## What was concluded

A macro-research team reported that mean annual real GDP growth in the high public
debt regime (public-debt-to-GDP above 90%) is 3.9 percentage points lower (95% CI
1.6 to 6.2pp) than in the lower-debt regime across the postwar advanced economies,
and proposed a 90% debt threshold as a fiscal guideline. The spec presents a
single clean threshold contrast over the full declared country-year panel.

## Why it was wrong

The headline gap is a property of two undisclosed analyst choices, not of the debt
threshold: (a) a set of country-year observations was dropped from the
above-threshold average, and (b) growth was averaged by country and then across
countries, rather than pooling country-years. Neither is declared as an exclusion
rule or an alternative-specification comparison. The most prominent documented
instance is Reinhart, C. M. and Rogoff, K. S. (2010), "Growth in a Time of Debt",
American Economic Review volume 100 issue 2 pages 573-578 (DOI
10.1257/aer.100.2.573 — page/section locator UNVERIFIED, pending the
pre-registered D-05 verbatim-quote human read at the Phase-12 UAT round).

The answer is now known because the analysis was reproduced from the original
spreadsheet: Herndon, T., Ash, M. and Pollin, R. (2014), "Does high public debt
consistently stifle economic growth? A critique of Reinhart and Rogoff",
Cambridge Journal of Economics volume 38 issue 2 pages 257-279 (DOI
10.1093/cje/bet075 — locator UNVERIFIED). Correcting the selective exclusion, the
weighting choice, and a spreadsheet error, the stark above-90% contraction became
a modest, positive average growth figure — the conclusion did not survive the
alternative specifications. This case is adopted as a known-answer positive
control: the corrected answer is externally established, so the tool's verdict on
it can be scored against ground truth.

## Why a declaration-only gate misses it

Because the exclusions and the weighting are not declared, the shipped
exclusion-justification catch `DSX-VAL-080` (exclusion rule declared without a
justification) has nothing to fire on — there is no declared exclusion to demand a
justification for. Catching this requires the currently-unwritten frequentist
**specification-sensitivity** check — does the conclusion survive putting the
dropped observations back and averaging the other way — the frequentist half of
`brief.md` §6.5 item 1 (prior justification and prior sensitivity /
specification sensitivity). Until that check exists, this case is a miss; its
catch-attribution (`absent_code: DSX-VAL-080`, `promotes_backlog_item`: the §6.5
item-1 row) lives in the paired
`operator-known-answer-selective-exclusion-ATTRIBUTION.yaml` sidecar, not in the
spec, so `frame_digest` is unperturbed (placement precedent 11.2 D-08,
`dsx/decisions.py` lines 99-121).

## Incidental gaps

At `dsx gate verify`/`ship` this fixture also blocks on the shared
corpus-completeness gaps every hand-authored fixture carries — `DSX-CLM-031`,
`DSX-MET-040`, `DSX-NAR-001`, `DSX-REP-030` and `DSX-REP-050` — none of which is
the encoded defect. See `_INCIDENTAL_GAP_CODES` in
`tests/test_known_bad_corpus.py`.
