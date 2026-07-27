---
name: dsx-design-experiment
description: "Design an A/B test or quasi-experiment with the power arithmetic done first. Use before launching any experiment, and when reading out one that has finished."
argument-hint: "[--baseline <rate>] [--mde <effect>] [--readout] [--phase <N>]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
---

<objective>
Design mode: a fully specified experiment whose sample size is derived, not
guessed. Readout mode: an honest reading of one that has run.
</objective>

<design_mode>

1. **Get the smallest effect that would change the decision.** Not the effect you
   hope for — the one below which you would do nothing. Ask if it is not given.

2. **Compute the sample.** This is arithmetic, not negotiation:
   ```bash
   dsx power --baseline 0.31 --mde 0.02 --alpha 0.05 --power 0.8
   ```
   If the required sample exceeds available traffic in the available window, that
   is the finding. Raise the MDE, extend the window, or do not run the test.
   Running underpowered produces an uninterpretable null and burns the window.

3. **Fix the units.** Randomization unit and analysis unit. When they differ,
   declare `variance_adjustment: cluster_robust` — otherwise the standard errors
   understate the noise and the test manufactures significance.

4. **Declare the family and the correction.** Every metric you will test. Three
   metrics at alpha 0.05 with no correction carries a 14% chance of at least one
   false positive.

5. **Declare the peeking policy before launch.** `fixed_horizon` means one look.
   If you want to stop early, choose `sequential_obf` now — you cannot adopt it
   retroactively after peeking.

6. **Declare guardrails.** At minimum one health metric and one revenue metric.
   A treatment that lifts activation while doubling latency is a loss.

7. **Run duration in whole weeks**, minimum one, to cover the weekly cycle and
   let novelty effects decay.

</design_mode>

<readout_mode>

Order matters — each step can stop the readout:

1. **SRM first.** `dsx check design` runs a chi-square on the observed split. A
   p below 0.001 means the assignment mechanism is broken. **Stop.** Do not read
   the effect; find the bug. SRM is never noise you can adjust away.
2. **Guardrails second.** A primary-metric win with a guardrail regression is not
   a win.
3. **Primary metric third**, with its interval, against the pre-declared rule.
4. **Segments last, and labelled exploratory.** Segment effects are
   hypothesis-generating unless the segmentation was pre-registered.

Then apply the decision rule as written. If the result sits between "significant"
and "practically meaningful", the rule already said what to do — follow it.
</readout_mode>

<references>
@references/experiment-pitfalls.md
@references/test-selection.md
</references>
