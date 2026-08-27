# Help-center revamp readout

**Audience:** Head of Support
**Decision:** ship the revamp if posterior mass above +0.05 is at least 0.95.

## Headline

The help-center revamp raises self-serve resolutions by 0.11 per active
account (credible interval 0.06 to 0.16) in the test window.

Posterior mass above the +0.05 floor is 0.99, so the decision rule recommends
shipping. No guardrail degraded over the two-week window.

## Limitations

This counts self-serve resolutions, not deflected agent contacts. The posterior is
conditional on the weakly-informative priors declared in the spec.
