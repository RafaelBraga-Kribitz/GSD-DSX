---
name: dsx-review-analysis
description: "Adversarial end-to-end review of an analysis before it ships. Use before any readout, and when reviewing someone else's work."
argument-hint: "[--phase <N>] [--report <file>]"
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Agent
---

<objective>
Find the reason this analysis is wrong before a stakeholder does.
</objective>

<process>

1. **Run the deterministic audit.** Its findings are facts, not opinions:
   ```bash
   dsx audit --phase-dir <phase-dir> --verbose --report <phase-dir>/DATA-REVIEW.md
   ```

2. **Spawn the specialists in parallel** for the judgement code cannot make:
   - `dsx-statistician` — magnitude, generalisation, alternative explanations
   - `dsx-ml-integrity-auditor` — if a model was built, verify code matches spec
   - `dsx-metric-steward` — if numbers will be compared to an existing source
   - `dsx-viz-critic` — if charts ship

3. **Apply the five questions** to the headline claim:
   - Would this reverse under a reasonable alternative specification?
   - Does the design license the verb used?
   - Is the effect large enough to matter to the declared decision?
   - Does the sample represent the population the decision covers?
   - How many comparisons were *actually* looked at, including exploratory cuts?
     (`results.comparisons_looked_at` vs `design.multiplicity.family`)

4. **Null discipline.** A "no effect" interpretation needs CI-in-bounds / TOST
   or `detectable_mde` (`DSX-STA-020`/`021`). Quote finding codes unmodified.

5. **Resolve every claim** to SUPPORTED, OVERSTATED, UNSUPPORTED or
   INCONCLUSIVE. "Inconclusive" is a legitimate verdict and frequently the
   correct one — reaching for "unsupported" when the study was underpowered is
   its own error.

</process>

<verdict>
- **CRITICAL or HIGH findings open** → blocked. The ship gate will stop it anyway.
- **MEDIUM findings** → ship with the limitation stated explicitly in the
  narrative, not buried in an appendix.
- **Clean** → say what was checked. A clean review is only worth something if it
  lists its coverage.
</verdict>
