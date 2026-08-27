# Post-mortem: a retracted field experiment resting on fabricated data

Paired spec: `retracted-fabricated-field-experiment-ANALYSIS-SPEC.yaml`

Coverage class (REQ-P12-01): a retracted paper carrying a published post-mortem /
retraction notice.

## What was concluded

A field-experiments lab reported that a single face-to-face canvassing
conversation durably raised the share of respondents who warmed toward a
stigmatised group by 6.2 percentage points (95% CI 4.1 to 8.3pp), sustained to a
nine-month follow-up, from a well-powered randomised design. The spec declares
strong randomised identification, a computed effect, an internally consistent
inference plan, and a clean validity frame.

## Why it was wrong

The follow-up survey waves the durable effect rests on were never collected — the
respondent-level panel was fabricated. The most prominent documented instance of
this exact failure is LaCour, M. J. and Green, D. P. (2014), "When contact
changes minds: An experiment on transmission of support for gay equality",
Science volume 346 issue 6215 pages 1366-1369 (DOI 10.1126/science.1256151 —
page/section locator UNVERIFIED, pending the pre-registered D-05 verbatim-quote
human read at the Phase-12 UAT round). The published post-mortem that exposed the
fabrication is Broockman, D., Kalla, J. and Aronow, P. (2015), "Irregularities in
LaCour (2014)" (working paper, Stanford University — locator UNVERIFIED), which
showed the reported survey data was statistically indistinguishable from a
recycled, noise-perturbed public dataset rather than freshly collected responses.
The paper was retracted by its senior author; the retraction notice is Science
volume 348 issue 6239 page 1100 (2015 — locator UNVERIFIED).

The point of the fixture is not that this specific study is re-encoded verbatim,
but that its failure mode — a clean, well-powered, correctly-specified analysis
whose *data does not exist* — is invisible to any check that reads only the
declaration.

## Why a declaration-only gate misses it

No shipped check can tell a plausibly-declared data extract from a fabricated
one. The nearest existing provenance code, `DSX-REP-020` (data source cannot be
pinned to a specific extract), does not fire, because a plausible warehouse source
and period are declared — the fabrication is downstream of what the declaration
exposes. Attributing this miss requires the provenance/origin work tracked by
`brief.md` §6.5 item 7 (per-feature / per-source origin, method, fitted-on,
motivating result): verifying that a declared extract corresponds to real
collected data, which a declaration-only gate structurally cannot do. Until that
work ships, this case is a miss; its catch-attribution (`absent_code:
DSX-REP-020`, `promotes_backlog_item`: the §6.5 item-7 row) lives in the paired
`retracted-fabricated-field-experiment-ATTRIBUTION.yaml` sidecar, not in the spec,
so `frame_digest` is unperturbed (placement precedent 11.2 D-08,
`dsx/decisions.py` lines 99-121).

## Incidental gaps

At `dsx gate verify`/`ship` this fixture also blocks on the shared
corpus-completeness gaps every hand-authored fixture carries — `DSX-CLM-031`,
`DSX-COH-031`, `DSX-DEC-001`, `DSX-MET-040`, `DSX-NAR-001`, `DSX-REP-030` and
`DSX-REP-050` — none of which is the encoded defect. See `_INCIDENTAL_GAP_CODES`
in `tests/test_known_bad_corpus.py`.
