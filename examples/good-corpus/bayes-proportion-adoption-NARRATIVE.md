# Guided tour readout

**Audience:** Head of Product
**Decision:** ship the guided tour if posterior mass above +1.0pp is at least 0.95.

## Headline

The guided tour raises feature adoption by 2.6 percentage points
(credible interval 1.5 to 3.7pp) among non-bot new users in the test window.

Posterior mass above the +1.0pp floor is 0.99, so the decision rule recommends
shipping. No guardrail degraded over the two-week window.

## Limitations

This estimates adoption within 14 days only and says nothing about sustained use.
The posterior is conditional on the weakly-informative priors declared in the spec.
