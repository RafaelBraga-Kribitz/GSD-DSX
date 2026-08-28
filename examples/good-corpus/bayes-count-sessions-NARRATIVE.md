# Streak widget readout

**Audience:** Head of Engagement
**Decision:** ship the streak widget if posterior mass above +0.10 is at least 0.95.

## Headline

The streak widget raises weekly sessions by 0.22 per active user
(credible interval 0.13 to 0.31) in the test window.

Posterior mass above the +0.10 floor is 0.99, so the decision rule recommends
shipping. No guardrail degraded over the two-week window.

## Limitations

This counts sessions, not time spent or actions taken per session. The posterior is
conditional on the weakly-informative priors declared in the spec.
