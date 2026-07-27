# Experiment pitfalls

Ordered by how much damage each does when it goes unnoticed.

## Sample ratio mismatch

The observed split differs from the intended one by more than chance. `dsx check
design` runs a chi-square at p < 0.001.

**SRM is never noise you can adjust away.** It means the assignment mechanism is
broken — bot filtering applied to one arm, redirect loss, a logging drop, a
bucketing bug. Whatever caused the imbalance also correlates with the outcome, so
the treatment effect is confounded by it.

**On SRM: stop. Do not read the results.** Find the defect and re-run.

## Underpowering

Running a test that cannot detect the effect that matters. The result is an
uninterpretable null, which then gets reported as "no effect" — the exact
opposite of what the data says.

Compute the sample before launching: `dsx power --baseline <p> --mde <d>`. If the
required sample is unavailable, that is a finding to raise now, not a constraint
to quietly absorb.

## Peeking

Repeatedly testing accumulating data inflates the type-I error. At alpha 0.05,
five looks pushes the true false-positive rate to roughly 14%; ten looks to 19%.

Choose the policy *before* launch. `fixed_horizon` means one analysis at the
pre-declared sample. To stop early, use O'Brien-Fleming or always-valid inference
— but the boundary has to be set in advance. It cannot be adopted retroactively
after peeking.

## Unit mismatch

Randomizing on user and analysing on session treats correlated observations as
independent. Standard errors shrink, the test statistic inflates, and noise
becomes significant.

Either aggregate the metric to the randomization unit, or declare
`variance_adjustment: cluster_robust`.

## Multiple comparisons

Three metrics at alpha 0.05 with no correction carries a 14% chance of at least
one false positive; five metrics, 23%. Declare the family and the correction in
advance — Benjamini-Hochberg for discovery, Holm when a false positive is
expensive.

The declared family is usually smaller than the number of comparisons actually
looked at. Segment cuts count.

## Novelty and primacy

Users respond to change itself. Novelty inflates early treatment effects; primacy
depresses them when the change disrupts a learned habit. Both decay.

Run at least one full week, in whole-week multiples, and plot the effect by day.
A gap that opens on day 1 and closes by day 5 is novelty, not value.

## Interference

The stable-unit assumption fails when units affect each other — marketplaces
(treatment users take supply from control users), social features, shared
budgets. Standard A/B analysis is biased, usually toward overstating the effect.

Use cluster randomization (by geography, by market) or a switchback design.

## Guardrail blindness

A treatment that lifts the primary metric while degrading latency, error rate,
margin or a downstream funnel step is a loss. Declare guardrails before launch —
at minimum one health metric and one revenue metric — and read them before the
primary.

## HARKing

Hypothesising after the results are known. Choosing the segment, the metric or
the cut-off once you have seen which one is significant converts an exploratory
finding into a confirmatory claim it cannot support.

The defence is mechanical: write the decision rule and the metric family in
`ANALYSIS-SPEC.yaml` before launch, and let the gate hold you to it.
