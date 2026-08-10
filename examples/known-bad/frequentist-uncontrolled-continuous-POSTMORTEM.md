# Post-mortem: continuous monitoring under a fixed-horizon frequentist test

Paired spec: `frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml`

This is the frequentist half of Phase 9's atomic monitoring pair — its Bayesian
counterpart is `bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml`. D-06 requires
both halves to have a committed target so a half-shipped Phase 9 is harder to fudge.

## What was concluded

An e-commerce team ran a randomized experiment on a new checkout flow, watching
a daily-refreshed dashboard that recomputed a two-proportion z-test p-value
against the accumulating data. On the fourth of five daily checks, the running
p-value crossed 0.05. The team stopped there, concluded the new checkout flow
significantly reduced cart abandonment by 2.1 percentage points, and shipped it.

## Why it was wrong

The design declared `peeking_policy: uncontrolled_continuous` — interim looks
continue with no sequential correction (no O'Brien-Fleming or Pocock boundary)
and no anytime-valid method (no mSPRT / confidence sequence). The team then
analysed the data with an ordinary fixed-horizon test statistic
(`two_proportion_z`) at every look and stopped the first time it crossed the
nominal alpha of 0.05. Repeatedly testing the same accumulating data against a
fixed-horizon threshold inflates the true type-I error far above the nominal
rate: at a nominal alpha of 0.05 with 5 interim looks, the true Type-I error is
approximately **0.142** — nearly three times the nominal rate. This spec
declares `results.interim_looks: 5`, and `dsx.mathx.inflation_from_peeking(5)`
already tabulates and returns exactly `0.142` in this codebase, so the
reference value in this post-mortem is grounded in code that predates this
fixture, not invented for it.

Note that `DSX-EXP-060` (the existing check for peeking under a *declared
fixed-horizon* design) does **not** fire on this spec, and is not supposed to:
its trigger is the literal tuple `("", "fixed_horizon")`, disjoint by
construction from `uncontrolled_continuous` (M-01, D-08). A parametrised
disjointness test landed in plan 06-01 pins this property so a future widening
of `_check_peeking` cannot make it silently double-fire once Phase 9's
`DSX-PAR-010` ships (T-6-18).

## Source

Armitage, P., McPherson, C.K. & Rowe, B.C. (1969), "Repeated significance
tests on accumulating data", *Journal of the Royal Statistical Society Series
A*, 132(2), 235–244 — the original published result establishing the Type-I
error inflation under repeated naive significance testing on accumulating
data, which is the result `dsx.mathx.inflation_from_peeking` tabulates.
Reference value stated explicitly: **at a nominal alpha of 0.05 with 5 interim
looks, the true Type-I error is approximately 0.142.**

## Which absent code would have caught it

`DSX-PAR-010` (Phase 9) — no code in this codebase adjudicates the
combination of `inference.paradigm: frequentist` with an uncontrolled
continuous-monitoring `design.peeking_policy` today; Phase 6 only checks that
both blocks are present and their fields are legal vocabulary members. Phase
9 is scoped to block exactly this combination: a frequentist paradigm
declared alongside continuous monitoring with no sequential correction and no
anytime-valid method.
