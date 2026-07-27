# Activation checklist readout

**Decision:** Full rollout — the lower bound of the activation CI clears +1.0pp and no guardrail degraded.

## Answer

The onboarding checklist increases 7-day activation by 2.4 percentage points (95% CI 1.0 to 3.8pp) among non-bot signups in the test window.

Day-7 retention is associated with a 1.6pp gain in the treatment arm, significant after Benjamini-Hochberg correction across the three-metric family.

Neither guardrail moved: p95 latency and 14-day revenue per user stayed within their declared tolerances over the test window.

## Limits (up front)

- Estimates the effect for new signups only; says nothing about reactivating dormant users.
- Measured over two weeks in June; seasonal cohorts may respond differently.
- Revenue effect is measured at 14 days and does not establish a durable LTV change.

## Method

Randomized experiment on new non-bot signups, 2026-06-01 to 2026-06-14. Full power and SRM details are in ANALYSIS-SPEC.yaml.
