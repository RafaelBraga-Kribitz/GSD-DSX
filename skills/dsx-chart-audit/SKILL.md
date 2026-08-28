---
name: dsx-chart-audit
description: "Standalone adversarial chart/figure audit: run deterministic viz/smells/figures checks, then spawn dsx-viz-critic to write CHART-REVIEW.md. Use for retroactive figure review without a full experiment/ML readout. Triggers: 'audit this figure', 'is this chart honest', 'review this chart' — routes intent without GSD phase names."
argument-hint: "[--phase-dir <path>] [--publish-disposition]"
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Agent
---

<objective>
Produce a schema-valid CHART-REVIEW.md for the phase's declared visuals
(or on-disk figures referenced by ANALYSIS-SPEC), after deterministic dsx checks.
</objective>

<process>

1. Resolve `PHASE_DIR` from `--phase-dir` or the current GSD phase.

2. **Deterministic first:**
   ```bash
   dsx check viz smells figures --phase-dir "$PHASE_DIR" --verbose
   ```
   Record open CRITICAL/HIGH codes (minus ANALYSIS-SPEC `suppressions[]`).

3. **Spawn `dsx-viz-critic`** with:
   - ANALYSIS-SPEC.yaml (if present)
   - `references/chart-review-schema.md` + `templates/CHART-REVIEW.md`
   - figure artifacts / PNGs / SVGs listed in `visuals[]`
   - instruction to write `$PHASE_DIR/CHART-REVIEW.md`

4. **Validate output:**
   - Contains `schema: dsx-chart-review-v1`
   - Does **not** contain `X/10`
   - Ends with `## CHART AUDIT COMPLETE`
   - Finding lines cite `DSX-` or `UNMAPPED`

5. If `--publish-disposition` is set and the host project has a disposition
   template (e.g. EPRA `reports/analytics/chart_audit_disposition_TEMPLATE.md`),
   copy verdicts into a dated disposition file citing `DSX-*` codes. Otherwise skip.

6. Surface Final Assessment + Gate A–D to the user. Do not edit product chart code
   in this skill — fixes are a separate execute plan.

</process>

<references>
@references/chart-review-schema.md
@templates/CHART-REVIEW.md
@agents/dsx-viz-critic.md
</references>
