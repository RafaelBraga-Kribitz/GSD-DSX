# Streamlined signup form readout

**Audience:** Head of Growth
**Decision:** ship the streamlined form if posterior mass above +1.0pp is at least 0.95.

## Headline

The streamlined signup form raises account creation by 2.4 percentage
points (credible interval 1.3 to 3.5pp) among non-bot visitors in
the test window.

Posterior mass above the +1.0pp floor is 0.99, so the decision rule recommends
shipping. No guardrail degraded over the two-week window.

## Limitations

This estimates the effect for new visitors only and says nothing about returning
users. The posterior is conditional on the weakly-informative priors declared in
the spec; a flat-prior sensitivity check did not move the decision.
