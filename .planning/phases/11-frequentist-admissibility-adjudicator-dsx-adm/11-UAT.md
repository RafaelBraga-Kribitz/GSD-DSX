---
status: testing
phase: 11-frequentist-admissibility-adjudicator-dsx-adm
source: [11-VERIFICATION.md]
started: 2026-08-22T19:08:21Z
updated: 2026-08-22T19:08:21Z
---

## Current Test

number: 1
name: Read each of families.yaml's 14 family entries' citation string against its real source (T-11-13/T-11-14)
expected: |
  The cited work exists, actually supports the named estimator family, and locator_status
  (verified/unverified) matches whether the specific locator (chapter/section/page) was
  actually confirmed.
awaiting: user response

## Tests

### 1. Citation authenticity for all 14 families.yaml entries (T-11-13/T-11-14)
expected: |
  The cited work exists, actually supports the named estimator family, and locator_status
  (verified/unverified) matches whether the specific locator (chapter/section/page) was
  actually confirmed.
why_human: No parser can confirm a citation string names a real, correctly-quoted source that
  supports the claim attached to it. Explicitly still-open per 11-04-SUMMARY.md ("has not yet
  been performed") and 11-VALIDATION.md's Manual-Only Verifications table.
result: [pending]

### 2. DSX-ADM-010 finding wording does not overstate ranking strength
expected: |
  Uniform-domination language (Boschloo-over-Fisher) is used only where the source states a
  uniform result; hedged/default-preference orderings (Welch-over-Student, CV3-over-CV1,
  interacted-over-unadjusted) are worded as preferences, not dominations.
why_human: Only a reader can tell a uniform domination from a hedged reliability ordering apart
  in prose -- a test can assert the strength field is a valid enum value, not that the rendered
  sentence honestly reflects the source at that strength.
result: [pending]

### 3. references/test-selection.md's corrected Fisher/Boschloo row and Lydersen footnote read correctly
expected: |
  The row no longer prescribes Fisher's exact as the small-cell fallback and the citation reads
  as an accurate, non-overstated summary.
why_human: 11-01-PLAN.md Task 2's own human-check requires this read; 11-01-SUMMARY.md records
  human_judgment true without recording that the read was performed.
result: [pending]

### 4. brief.md's two D-29 locators (Kohavi Tang Xu; Cameron Miller) read at the strength the evidence supports
expected: |
  The Kohavi locator reads as verified; the Cameron and Miller locator reads as
  manuscript-verified with the numbering caveat intact and unambiguous.
why_human: 11-01-PLAN.md Task 3's own human-check requires this read; 11-01-SUMMARY.md records
  human_judgment true without recording that the read was performed.
result: [pending]

## Summary

total: 4
passed: 0
issues: 0
pending: 4
skipped: 0
blocked: 0

## Gaps
