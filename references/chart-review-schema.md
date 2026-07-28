# Chart Review Schema (dsx-chart-review-v1)

Output contract for `dsx-viz-critic` / skill `dsx-chart-audit`.
Deterministic structure; stochastic only for PNG perception and ranked alternatives.

File: `{phase_dir}/CHART-REVIEW.md`

## Frontmatter

```yaml
---
schema: dsx-chart-review-v1
capability: dsx
exhibit: ALL|<chart_id>
phase: <phase id or null>
audited_at: <ISO-8601 date>
tier_a_checks: [viz, smells, figures]   # dsx check names actually run
gates:
  A: Pass|Fail
  B: Pass|Fail
  C: Pass|Fail
  D: Pass|Fail
final_assessment: Approved|ApprovedWithRevisions|SignificantReworkNeeded|RejectAndRebuild
scores:
  analytical_framing: 1|2|3|4
  analytical_logic: 1|2|3|4
  data_confidence: 1|2|3|4
  statistical_integrity: 1|2|3|4
  visualization_quality: 1|2|3|4
  communication_quality: 1|2|3|4
  confidence_in_correctness: 1|2|3|4
---
```

Scores are **1–4 only**. Free-form `X/10` is forbidden.

| Score | Meaning |
|------:|---------|
| 1 | Invalid for publish |
| 2 | Notable gaps |
| 3 | Minor issues only |
| 4 | Survives falsification with cited evidence |

Every score needs ≥1 evidence bullet.

## Gate proxies (deterministic)

| Gate | Fail when |
|------|-----------|
| A | Open `DSX-COH-*` CRITICAL/HIGH, empty decision, or `DSX-SPEC-010` |
| B | Open `DSX-CLM-*` / `DSX-CAU-*` / `DSX-STA-*` / `DSX-NAR-*` / `DSX-DEC-*` / `DSX-COH-031` / `DSX-EXP-051` at CRITICAL/HIGH |
| C | Open `DSX-VIZ-001`, `DSX-VIZ-010`–`014` at CRITICAL/HIGH |
| D | Open `DSX-VIZ-020+`, `DSX-FIG-*`, `DSX-SMELL-*`, `DSX-DQ-*`, `DSX-CODE-*`, `DSX-REP-050+` at CRITICAL/HIGH |

Suppressed findings (ANALYSIS-SPEC `suppressions[]`) do **not** fail gates.

## Final assessment decision table

First matching row wins:

| Condition | Assessment |
|-----------|------------|
| Gate A, B, or C Fail | `RejectAndRebuild` |
| Gate D Fail | `SignificantReworkNeeded` |
| Any Critical Analytical/Data/Code/Statistical issue (agent) | `SignificantReworkNeeded` |
| Any Critical Visual/Communication **or** Moderate Analytical/Data/Code/Statistical | `ApprovedWithRevisions` |
| All gates Pass and only Minor/none | `Approved` |

## Body (fixed H2 order)

1. `## Executive Verdict`
2. `## Gate Results` (A–D)
3. `## Overall Scores` (table with Evidence)
4. `## Existence Checklist` (necessary vs table/stat; feeds Gate A narrative)
5. `## Critical Issues` / `## Moderate Issues` / `## Minor Issues` — each line cites `DSX-*` or `UNMAPPED`
6. `## Better Chart Options` (max 3; or `None`)
7. `## Required Fixes (Upstream First)` — order: Question → Logic → Chart Type → Evidence → Data → Code → Stats → Plot → Visual
8. `## Per-Exhibit Disposition` (multi-exhibit)
9. `## Final Assessment`
10. `## CHART AUDIT COMPLETE`

## Orchestrator validation

- Frontmatter `schema: dsx-chart-review-v1`
- No substring `X/10`
- Ends with `## CHART AUDIT COMPLETE`
- Finding lines include `DSX-` or `UNMAPPED`
