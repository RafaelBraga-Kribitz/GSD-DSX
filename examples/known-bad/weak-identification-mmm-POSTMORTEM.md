# Post-mortem: weak identification in a marketing-mix model

Paired spec: `weak-identification-mmm-ANALYSIS-SPEC.yaml`

## What was concluded

A marketing-analytics team fit a national weekly regression marketing-mix model (MMM)
over three years of data (156 weekly observations) to estimate the effect of TV
advertising spend on online revenue, alongside five other channels and a set of
control variables (price promotions, seasonality, competitor TV spend, search
spend, social spend, display spend). The fitted TV-spend coefficient was positive
and the team concluded that each additional dollar of weekly TV spend increased
weekly online revenue by a stated amount, and recommended raising the TV budget
allocation by 15%.

## Why it was wrong

The model's only source of identifying variation was regression adjustment for the
observed covariates above — there was no randomization, no instrument, no
discontinuity, and no external constraint (no informative prior, no penalisation, no
design restriction, no hierarchical pooling) anchoring the TV coefficient's scale.
Two failures compound in exactly this situation, both documented in the cited
report rather than asserted here from first principles.

First, correlated media spend. Advertisers routinely move channel budgets together
— raising TV spend in the same weeks they raise search and social spend, in
response to the same seasonal or promotional calendar. When the input variables a
regression conditions on are highly correlated, the coefficient estimates carry
high variance and the model cannot reliably attribute the outcome to one channel
over another: two response surfaces with very different slopes with respect to a
given channel can each fit the observed data equally well, because the data
contains little information about what happens when one channel moves
independently of the others (Chan & Perry (2017), section 4.1.2, "Correlated input
variables").

Second, selection bias from omitted demand. When a channel's spend is targeted or
timed in response to an unobserved demand signal that also drives the outcome —
budgets raised ahead of an anticipated high-demand period, for instance — and that
demand signal is not in the model, the model has no way to separate the channel's
true effect from the confound (Chan & Perry (2017), section 4.2, "Selection bias").
A regression-adjustment identification strategy with no external constraint gives
the coefficient nothing to anchor it against either failure: the point estimate
that was reported as "the effect of TV spend" cannot be distinguished, from the
data as collected, from an artifact of collinear channel budgets or from
demand-driven confounding.

The report's own worked example of model uncertainty (section 4.3.2) shows five
equally plausible model specifications, each fit to the same weekly national data
and each achieving R² of 0.98-0.99, disagreeing by up to 50% on predicted sales and
by more on how budget should be allocated across channels — despite fitting the
observed data equally well. A single point estimate reported without this
uncertainty, and without a design-based or externally constrained identification
strategy, overstates what the model can actually support.

## Source

Chan, D. & Perry, M. (2017), "Challenges and Opportunities in Media Mix Modeling",
Google Inc. — a Google Research technical report (not a vendor blog, a marketing
post, or product documentation; it is an academic-style technical report with an
abstract, numbered sections, and a references list, hosted at
research.google/pubs/challenges-and-opportunities-in-media-mix-modeling/, PDF at
storage.googleapis.com/gweb-research2023-media/pubtools/3803.pdf). The author
names, publication year, exact title and venue were confirmed directly against the
primary PDF and the hosting page's citation metadata during this phase (fetched and
read in full, 2026-08-12) — not inferred from a secondary reference to it.

Cited passages, confirmed by direct reading of the primary document:

- Section 4.1.1 ("Limited amount of data"), page 6: "A typical MMM dataset,
  consisting of three years of national weekly data is only 156 data points" —
  the fixture's own data window (156 weeks) is drawn directly from this report's
  own stated typical case, not invented independently of it.
- Section 4.1.2 ("Correlated input variables"), page 6: describes how highly
  correlated media-spend inputs produce high-variance coefficient estimates and
  "bad attribution of sales to the ad channel," illustrated by two fitted response
  surfaces with different slopes that both fit the same correlated data equally
  well.
- Section 4.2 ("Selection bias"), pages 8-9: identifies omitted, unobservable
  demand as "perhaps represents the largest hurdle to MMMs providing valid
  estimates of advertising effectiveness," including the seasonality and ad-targeting
  sub-cases.
- Section 4.3.2 ("Model uncertainty"), pages 10-11: the five-model worked example
  showing R²=0.98-0.99 for all five while their sales and budget-allocation
  conclusions disagree by up to 50%.

Vendor blogs, Medium posts and tool marketing are inadmissible under D-05 in either
direction — the cited source is a primary technical report, not any of those.

## The code that catches it

`DSX-VAL-040` (Phase 7, this phase — the first fixture in this corpus for which the
target code ships in the same phase as the fixture; see `dsx/frame/val.py`'s
`_check_identification`). It fires at CRITICAL severity, blocking from `dsx gate
plan` onward, whenever `validity_frame.identification.strength` normalizes to
`weak` and `validity_frame.identification.constraint_source` normalizes to `none`
— exactly the combination this fixture declares: a regression-adjustment
identification strategy (`design.identification: regression_adjustment`, itself
classified `weak` in `dsx.spec.IDENTIFICATION_STRATEGIES`) with no external
constraint informing the coefficient's scale. `dsx gate execute` still exits 0 on
this fixture, because the `val` check that emits `DSX-VAL-040` is registered in the
plan, verify and ship gate profiles but not in execute (`dsx/cli.py`'s
`GATE_PROFILES`).
