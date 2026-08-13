# Post-mortem: triggered-versus-eligible dilution on an upsell prompt

Paired spec: `triggering-dilution-ANALYSIS-SPEC.yaml`

## What was concluded

A growth-monetization team ran a randomized experiment on an in-product upsell
prompt shown during checkout. The prompt is only shown to a session once that
session reaches a specific step in the checkout flow — most eligible sessions
never get that far and never see the prompt at all. The team measured revenue
per session averaged across every eligible checkout session in the test window
(not only the sessions that actually reached and saw the prompt), found a lift
of $0.34 per eligible session, and concluded the upsell prompt should be rolled
out to 100% of eligible sessions.

## Why it was wrong

Only the sessions that actually reached the prompt could possibly be affected
by it — a session that never got to the checkout step where the prompt appears
behaves identically in treatment and control, because it never encountered
anything the treatment changed. Averaging the revenue effect across the whole
eligible population, when only a fraction of that population was ever
triggered, does not report "the effect of the prompt." It reports the effect
diluted by the share of the eligible population that never triggered — the
untriggered majority contributes a true effect of exactly zero to the average,
which pulls the overall estimate toward zero relative to the effect on the
sessions that were actually exposed.

The published formula for exactly this arithmetic, for an additive metric
(count, sum or average — never a ratio metric, see below):

    Delta_overall = Delta_triggered x (N_triggered / N_eligible)

The team's declared `expected_trigger_rate` is 0.41 — fewer than half of
eligible sessions ever reach the prompt. Reading $0.34 as "the effect of the
prompt" without adjusting for that trigger rate understates the effect the
prompt actually has on the sessions it can affect by roughly the same factor:
an unadjusted $0.34 measured across the whole eligible population corresponds
to an effect on the *triggered* subpopulation of roughly $0.34 / 0.41 =~ $0.83
— more than double what the naive, undiluted reading suggests. The team's
declaration carries no dilution adjustment (`dilution_adjusted: false`) and no
statement of which population the reported number describes, so the $0.34
figure is silently ambiguous between "the effect on everyone eligible" (true,
but understates what the prompt does to a session it actually reaches) and
"the effect of being shown the prompt" (false, because most of the eligible
population was never shown anything).

`dsx.mathx.diluted_effect` is this project's reference implementation of the
arithmetic above — it is never called from the gate path (D-09): the gate
adjudicates the *declaration* (is an additive metric analysed on the eligible
population with no adjustment recorded?), not the number itself. Computing a
test statistic or an effect size on the gate path is out of scope by design
(`.planning/REQUIREMENTS.md`, the gate-path computation exclusion) — that work
belongs to the analysis itself, not to a check that runs before the data is
touched.

**Scope note, load-bearing:** this pattern applies only to additive metrics —
count, sum and average — where the untriggered population's true contribution
to the aggregate is exactly zero and the dilution factor is a simple linear
scalar. A ratio metric (this project's `type: ratio` or `type: rate`) does not
dilute this way: its dilution equation has no closed-form scalar multiplier
and needs per-user data a declaration-only gate never has (`brief.md` section
6.5, REQ-P8-04). `DSX-INT-030` fires only on the additive partition; a ratio
metric under otherwise-identical triggering conditions is unadjudicated by
this check, by design, not by omission.

## Source

Deng, A. & Hu, V. (2015), "Diluted Treatment Effect Estimation for Trigger
Analysis in Online Controlled Experiments", WSDM '15, pp. 349-358 — the
camera-ready is freely available at
`https://alexdeng.github.io/public/files/wsdm2015-dilution.pdf`; ACM DL DOI
10.1145/2684822.2685307. Formula (1) in section 2.1 states the additive
dilution equation as printed:
`Delta_overall = Delta_Tr x N_Tr / N` (their `N_Tr / N` is this project's
`expected_trigger_rate`; their paper's own `TR` denotes an unrelated per-user
denominator trigger rate defined in section 3.3, not the population trigger
rate used here — the two are not the same quantity despite the similar name).
Preconditions stated in the paper and reproduced in this fixture's defect:
additivity of the metric, no treatment effect for untriggered users, and no
effect of the treatment on who triggers. The paper's own worked counterexample
(section 2.1) — a ratio metric, true effect -26 msec, naive-formula estimate
-18 msec — is the reference value this project's test suite checks the
additive/ratio scope boundary against; it is not reproduced here because it
describes the ratio case this fixture and `DSX-INT-030` deliberately do not
cover.

Vendor blogs, Medium posts and tool marketing are inadmissible under D-05 in
either direction — the cited source is a peer-reviewed conference paper, not
either of those.

## Which absent code would have caught it

`DSX-INT-030` (Phase 8, plan 08-04) — no code in this codebase adjudicates
`validity_frame.triggering` today; Phase 6 only checks that the block is
present and its fields are legal vocabulary members (`dsx/spec.py`'s
`_validate_validity_frame_shape`), so nothing in this repository names the
dilution defect today: the fixture clears `dsx validate` and both
CRITICAL-threshold gate points, `dsx gate plan` and `dsx gate execute`, with
no finding attributable to that defect. The fixture does block at `dsx gate
verify` and `dsx gate ship` (both exit 1), on the corpus-completeness gaps
named in the paired ANALYSIS-SPEC.yaml header and tracked in
`tests/test_known_bad_corpus.py`'s `_INCIDENTAL_GAP_CODES` — none of which is
the dilution defect. Phase 8 is scoped to block an additive metric
(`metrics[].type` in `{count, sum, average}`) analysed on the `eligible`
population (`validity_frame.triggering.analysis_population: eligible`) with
`dilution_adjusted` not `true` — precisely the combination this fixture
declares.
