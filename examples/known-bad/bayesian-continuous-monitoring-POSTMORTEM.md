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
interchangeable. Deng, Lu & Chen (2016) Theorem 1 states an optional-stopping
*equality* under known prior odds, for any proper stopping time — that is
what licenses treating the figure below as valid under continuous peeking,
not a fixed final look. The bound itself, that stopping at a posterior-odds
threshold `K` caps the false-discovery risk at `1/(K+1)`, is unnumbered prose
immediately following Theorem 1 and again, in its operational "at most" form,
in the paper's Section 3.2; citing Theorem 1 alone for the number `1/(K+1)`
would be a locator error. At the `P(B>A) > 0.95` decision threshold used in
this spec, the corresponding
posterior-odds threshold is `K = 19` (since `19/20 = 0.95`), and the bound is
`1/20 = 0.05` exactly. That is the sense in which "the false-positive rate can
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

**Do not substitute Ville's inequality for the theorem above.** Ville's
martingale inequality separately states that a nonnegative martingale starting
at 1 crosses a fixed threshold `k` with probability at most `1/k`, which at
`k = 19` gives `1/19 ≈ 0.0526`. That is a different bound from a different
result: `0.0526` is not `0.05` rounded, and Deng's Theorem 1 argues from the
likelihood ratio and the Bayesian promise rather than invoking Ville by name.
An earlier revision of this file attributed the `1/k` form to Theorem 1 and
reconciled the resulting gap with the word "rounded". Both statements were
individually true, which is why the conflation survived review — the defect
was the attribution, not either bound.

## Source

Deng, A., Lu, J. & Chen, S. (2016), "Continuous Monitoring of A/B Tests
without Pain: Optional Stopping in Bayesian Testing", IEEE International
Conference on Data Science and Advanced Analytics (DSAA) 2016. Theorem 1
states the optional-stopping equality — a likelihood-ratio / change-of-measure
argument — that licenses the bound under known prior odds and any proper
stopping time; the bound itself, that stopping at a posterior-odds threshold
`K` caps the false-discovery risk at `1/(K+1)`, is unnumbered prose
immediately following Theorem 1 and again, in its operational "at most" form,
in the paper's Section 3.2. Together they establish that a calibrated
threshold — not the prior's informativeness alone — is what controls the
false-positive rate under continuous monitoring.

Vendor blogs, Medium posts and tool marketing are inadmissible under D-05 in
either direction — this source is not one; it is the same primary paper
`brief.md` section 7 anchors `DSX-PAR-011` to.

## Which code catches it

`DSX-PAR-011` (CRITICAL) now blocks exactly this combination — a Bayesian
paradigm declared alongside continuous monitoring with no declared threshold
calibration — at both CRITICAL-threshold gate points, `dsx gate plan` and
`dsx gate execute`. It fires whenever `design.peeking_policy` normalizes to
`uncontrolled_continuous` and neither `inference.prior_justification` nor
`inference.threshold_calibration` is declared; this fixture declares
neither, and required no field change to trip the check the day it shipped.
The check itself is presence-only on the gate path — no statistic or
posterior is computed there — while a separate, seeded, reproducible
simulation against the prior-averaged `1/(K+1)` bound documented above lives
under `tests/`, never on the gate path (D-02, REQ-P9-07). Phase 6 checked
only that the `design:` and `inference:` blocks were present and their
fields legal vocabulary members — it never adjudicated the combination
itself.

This is the Bayesian half of the atomic pair; its frequentist counterpart,
`frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml`, blocks the same
two gate points on `DSX-PAR-010`, shipped in the same commit range at the
same CRITICAL severity.
