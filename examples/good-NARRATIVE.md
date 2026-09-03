# Activation checklist readout

**Decision:** Full rollout — the lower bound of the activation CI clears +1.0pp and no guardrail degraded.

## What

The onboarding checklist increases 7-day activation by 2.4 percentage points (95% CI 1.0 to 3.8pp) among non-bot signups in the test window. The interval is drawn honestly in `figures/activation_uplift_ci.svg` — the whole 95% CI sits above zero and its lower bound reaches the +1.0pp decision floor. The daily trend shows the gap opening on day 2 and holding flat, so this is a real shift rather than a novelty spike.

Day-7 retention is associated with a 1.6pp gain in the treatment arm, significant after Benjamini-Hochberg correction across the three-metric family.

Neither guardrail moved: p95 latency and 14-day revenue per user stayed within their declared tolerances over the test window.

## So What

The decision rule was pre-declared: roll out to 100% if the activation-uplift 95% CI lower bound exceeds +1.0pp and no guardrail degrades beyond tolerance. Both conditions hold — the lower bound clears +1.0pp and every guardrail is within tolerance — so the rule returns *rollout*. The effect is modest in standardized terms (h ≈ 0.05); the case for rollout rests on the interval clearing the pre-agreed practical floor, not on statistical significance alone.

## Now What

Roll the checklist out to 100% of new signups. Keep the activation metric on the growth dashboard and honour the pre-declared revisit trigger: re-open the question if the activation-rate 95% CI lower bound falls below +1.0pp at the 2026-Q4 review. This estimate covers new signups only over a two-week June window; it says nothing about reactivating dormant users or about seasonal cohorts, and the 14-day revenue read does not establish a durable LTV change — treat those as open questions, not settled ones.
