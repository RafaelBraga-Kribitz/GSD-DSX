---
schema: dsx-chart-review-v1
capability: dsx
exhibit: ALL
phase: 11.3-reporting-completeness
audited_at: "2026-08-27"
tier_a_checks: [viz, smells, figures]
gates:
  A: Fail
  B: Fail
  C: Fail
  D: Fail
final_assessment: RejectAndRebuild
scores:
  analytical_framing: 1
  analytical_logic: 1
  data_confidence: 1
  statistical_integrity: 1
  visualization_quality: 1
  communication_quality: 1
  confidence_in_correctness: 1
---

## Executive Verdict

D-13 boundary fixture: every judgement field below (`gates.A-D`, `scores.*`,
`final_assessment`, and this verdict prose) is deliberately flipped to its worst possible
value relative to `examples/good-CHART-REVIEW.md`. Structure is otherwise byte-identical in
shape: same schema tag, the mandated 1-4 scale throughout, the terminal sentinel, and every
finding line either absent or tokenised. The four `DSX-CRV-*` codes must fire identically to
the good fixture (i.e. none of them) because they read structure only, never this content.

## Gate Results

### Gate A: Question Validity

Fail

### Gate B: Analytical Logic

Fail

### Gate C: Chart-Type Validity

Fail

### Gate D: Data / Plot Integrity

Fail

## Overall Scores

| Dimension | Score | Evidence |
|-----------|------:|----------|
| Analytical Framing | 1 | Deliberately worst-case value for the D-13 boundary test. |
| Analytical Logic | 1 | Deliberately worst-case value for the D-13 boundary test. |
| Data Confidence | 1 | Deliberately worst-case value for the D-13 boundary test. |
| Statistical Integrity | 1 | Deliberately worst-case value for the D-13 boundary test. |
| Visualization Quality | 1 | Deliberately worst-case value for the D-13 boundary test. |
| Communication Quality | 1 | Deliberately worst-case value for the D-13 boundary test. |
| Confidence in Correctness | 1 | Deliberately worst-case value for the D-13 boundary test. |

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

- None

## Minor Issues

- None

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
8. Plot Construction: (none)
9. Visual Design: (none)

## Per-Exhibit Disposition

| Exhibit | Verdict | Notes |
|---------|---------|-------|
| activation_uplift_bar | RejectAndRebuild | Deliberately worst-case value for the D-13 boundary test. |
| daily_activation_trend | RejectAndRebuild | Deliberately worst-case value for the D-13 boundary test. |

## Final Assessment

**Assessment:** RejectAndRebuild

**Decision-table row:** Gate A, B, or C Fail -> RejectAndRebuild.

**Justification:** Deliberately worst-case verdict prose for the D-13 boundary test — dsx
must never let this paragraph, or any field above it, change which DSX-CRV-* codes fire.

## CHART AUDIT COMPLETE
