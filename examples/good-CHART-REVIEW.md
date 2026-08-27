---
schema: dsx-chart-review-v1
capability: dsx
exhibit: ALL
phase: 11.3-reporting-completeness
audited_at: "2026-08-27"
tier_a_checks: [viz, smells, figures]
gates:
  A: Pass
  B: Pass
  C: Pass
  D: Pass
final_assessment: ApprovedWithRevisions
scores:
  analytical_framing: 4
  analytical_logic: 4
  data_confidence: 3
  statistical_integrity: 4
  visualization_quality: 3
  communication_quality: 3
  confidence_in_correctness: 4
---

## Executive Verdict

Both exhibits support the stated activation-lift claim with a defensible chart-type choice;
one moderate labelling gap keeps this from a clean Approved.

## Gate Results

### Gate A: Question Validity

Pass

### Gate B: Analytical Logic

Pass

### Gate C: Chart-Type Validity

Pass

### Gate D: Data / Plot Integrity

Pass

## Overall Scores

| Dimension | Score | Evidence |
|-----------|------:|----------|
| Analytical Framing | 4 | Question, decision and chart_required all present and mutually consistent. |
| Analytical Logic | 4 | Bar-vs-baseline framing matches the causal claim's comparison. |
| Data Confidence | 3 | Manifest coverage confirmed; one caption omits the sample window. |
| Statistical Integrity | 4 | CI band rendered matches the declared effect and interval. |
| Visualization Quality | 3 | Proportional bar geometry; axis truncation on the trend chart is a minor issue. |
| Communication Quality | 3 | Title states the finding; legend omits units on one exhibit. |
| Confidence in Correctness | 4 | Byte seal matches disk; manifest and visuals[] agree. |

## Existence Checklist

- question: does the new onboarding flow lift week-1 activation?
- decision: ship the flow to 100% of new signups if lift is material
- chart_required: true
- table_better: false
- single_stat_better: false
- verdict: Necessary

## Critical Issues

- None

## Moderate Issues

- [COMMUNICATION] `daily_activation_trend` y-axis does not start at zero, exaggerating the visual slope of an already-significant trend — DSX-VIZ-021

## Minor Issues

- [COMMUNICATION] `activation_uplift_bar` legend omits the unit ("percentage points") — UNMAPPED

## Better Chart Options

- None

## Required Fixes (Upstream First)

1. Analytical Question: (none)
2. Analytical Logic: (none)
3. Chart Type: (none)
4. Missing Evidence: (none)
5. Data Quality: (none)
6. Code Quality: (none)
7. Statistical Issues: (none)
8. Plot Construction: rebase `daily_activation_trend`'s y-axis at zero or add a visible break.
9. Visual Design: add a unit label to `activation_uplift_bar`'s legend.

## Per-Exhibit Disposition

| Exhibit | Verdict | Notes |
|---------|---------|-------|
| activation_uplift_bar | ApprovedWithRevisions | Legend unit label missing. |
| daily_activation_trend | ApprovedWithRevisions | Y-axis truncation overstates the trend. |

## Final Assessment

**Assessment:** ApprovedWithRevisions

**Decision-table row:** All gates Pass and only Minor/none -> Approved; the one Moderate
communication issue (DSX-VIZ-021) moves this row down to ApprovedWithRevisions per the
"Any Critical Visual/Communication or Moderate Analytical/Data/Code/Statistical" row.

**Justification:** Both exhibits are structurally sound and support the claim; the two
labelling defects are cosmetic, not analytical, and are fully enumerated above.

## CHART AUDIT COMPLETE
