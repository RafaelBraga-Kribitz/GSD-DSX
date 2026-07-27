# Causal identification

A causal claim needs a strategy that rules out confounding. There are only a few,
each with assumptions the data cannot verify — which is precisely why they must
be declared and argued rather than assumed.

| Strategy | Strength | Core assumption | Must declare |
|---|---|---|---|
| randomized experiment | strong | randomization worked | randomization unit, allocation, SRM check |
| regression discontinuity | moderate | no manipulation of the running variable near the cutoff | running variable, cutoff, density test |
| difference-in-differences | moderate | parallel trends absent treatment | pre-period trend evidence |
| instrumental variable | moderate | the instrument affects Y only through X | instrument, exclusion restriction argument, first-stage strength |
| synthetic control | moderate | the donor pool reproduces the pre-period | donor pool, pre-period fit |
| front-door | moderate | a fully-mediating variable, unconfounded | the mediator |
| matching | weak | every confounder is observed | covariates, sensitivity analysis |
| regression adjustment | weak | every confounder is observed and correctly specified | covariates, sensitivity analysis |

## Why matching and regression adjustment are "weak"

Both identify a causal effect only under conditional ignorability: given the
covariates you included, treatment is as good as random. This is untestable, and
in most business settings it is false — people who complete onboarding differ
from people who do not in motivation, which no table records.

Using them is not forbidden. Using them without saying so is. When you do:

1. State the assumption in the deliverable, not the appendix.
2. Run a sensitivity analysis: how strong would an unmeasured confounder have to
   be to erase the effect? (E-value, Rosenbaum bounds.) If the answer is "not very",
   say that.
3. Hedge the wording. "Conditional on the observed covariates, we estimate…"

## The confounders that recur

- **Selection into treatment.** Users who adopt a feature were already more
  engaged. This inflates almost every observational feature-impact estimate.
- **Time.** Anything trending — seasonality, a concurrent launch, a pricing
  change, a macro shift.
- **Survivorship.** Analysing accounts that are still active conditions on the
  outcome.
- **Regression to the mean.** Targeting the worst-performing segment guarantees
  apparent improvement without any intervention.

## When no strategy applies

Say so, and convert the deliverable. "We cannot establish whether X causes Y with
observational data. Here is the association, here are the plausible confounders,
and here is the experiment that would settle it — it needs N users for W weeks."

That is a more useful artefact than a coefficient nobody should act on.
