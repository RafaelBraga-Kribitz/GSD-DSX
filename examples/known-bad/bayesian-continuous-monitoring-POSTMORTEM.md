# Post-mortem: a weakly informative prior does not control the false-positive rate under continuous peeking

Paired spec: `bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml`

This is the Bayesian half of Phase 9's atomic monitoring pair — its frequentist
counterpart is `frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml`. D-06
requires both halves to have a committed target so a half-shipped Phase 9 is
harder to fudge.

## What was concluded

An experimentation-platform team ran a Bayesian A/B test on a checkout
conversion change, refreshing the posterior daily over a 26-day window. They
placed a weakly informative prior on the conversion-rate difference and
believed that prior alone was sufficient to keep the decision procedure's
false-positive rate controlled even though the posterior was checked every
day. As soon as P(treatment > control) crossed 0.95 on any single day's
refresh, they shipped treatment to 100% of traffic.

## Why it was wrong

The posterior distribution itself is a valid summary of belief at every
single look, under any stopping rule — that much is true, and it is the
statement the team's assumption half-remembers. But the **error rate of a
decision procedure built on that posterior is not automatically controlled**
just because the posterior is valid. "Stop and ship the first time
P(treatment > control) crosses 0.95" is a stopping rule, and stopping rules
have their own long-run error properties independent of whether the
posterior computation at each look was correct. A weakly informative prior
delays how quickly the posterior odds can drift toward the threshold — it
does not cap the probability that continuous monitoring eventually crosses it
by chance alone. Brief.md section 6.5 names this the single most
load-bearing misconception in this domain, and it is the exact defect this
fixture is built to encode.

## Which formulation this fixture encodes

The reference value in this post-mortem is the **prior-averaged** bound, not
the point-null / law-of-iterated-logarithm formulation, and the two are not
interchangeable. Ville's martingale inequality states that for a nonnegative
martingale starting at 1 (which a prior-averaged likelihood ratio process
is), the probability it *ever* crosses a fixed threshold `k` is at most
`1/k`. At the `P(B>A) > 0.95` decision threshold used in this spec, the
corresponding posterior-odds threshold is `K = 19` (since `19/20 = 0.95`),
and the prior-averaged Ville bound is `1/19 ≈ 0.0526`, commonly rounded and
reported as **0.05**. That is the sense in which "the false-positive rate can
be bounded" under continuous monitoring — it requires a pre-registered,
calibrated threshold analysis using this bound, which this fixture's
`fallback_rule` explicitly states was never done. This is **not** the
point-null / law-of-iterated-logarithm formulation, under which the error
rate of naive continuous testing grows without a useful ceiling over an
unbounded horizon. Both are correct statements about different quantities; a
fixture built against one and checked against the other reads as an
implementation bug for a day rather than a formulation question in five
minutes (brief.md section 6.5, T-6-17). The same formulation note is
commented directly in the paired spec file so a future reader hits the
formulation question immediately rather than debugging a number mismatch.

## Source

Deng, A., Lu, J. & Chen, S. (2016), "Continuous Monitoring of A/B Tests
without Pain: Optional Stopping in Bayesian Testing", IEEE International
Conference on Data Science and Advanced Analytics (DSAA) 2016, Theorem 1 —
the martingale (Ville's inequality) argument bounding the probability that a
prior-averaged posterior-odds process ever crosses a fixed threshold,
establishing that a calibrated threshold — not the prior's informativeness
alone — is what controls the false-positive rate under continuous
monitoring.

Vendor blogs, Medium posts and tool marketing are inadmissible under D-05 in
either direction — this source is not one; it is the same primary paper
`brief.md` section 7 anchors `DSX-PAR-011` to.

## Which absent code would have caught it

`DSX-PAR-011` (Phase 9) — no code in this codebase adjudicates the
combination of `inference.paradigm: bayesian` with continuous monitoring and
no declared threshold calibration today; Phase 6 only checks that both
blocks are present and their fields are legal vocabulary members. Phase 9's
`DSX-PAR-011` is scoped to block exactly this combination via a seeded,
reproducible simulation against the prior-averaged Ville bound documented
above — that simulation lives under `tests/`, never on the gate path (D-02,
REQ-P9-07), and is Phase 9's work, not this phase's.
