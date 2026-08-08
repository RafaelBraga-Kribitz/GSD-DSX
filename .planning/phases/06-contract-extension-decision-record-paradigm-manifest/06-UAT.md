---
status: testing
phase: 06-contract-extension-decision-record-paradigm-manifest
source: [06-VERIFICATION.md]
started: 2026-08-08T12:00:00Z
updated: 2026-08-08T12:00:00Z
---

## Current Test

number: 1
name: REVERSALS.md D-14 template is copyable and SELF-001 is defined, not merely named
expected: |
  Template contains all four D-14 fields (Date, Reversed, New evidence, What would have
  made the original correct, What did not change) with self-explanatory prompts; the
  SELF-001 section states the exact triggering condition (an empty or reasoning-restating
  New evidence field) rather than just naming the convention.
awaiting: user response

## Tests

### 1. REVERSALS.md D-14 template is copyable and SELF-001 is defined, not merely named
expected: Read `.planning/REVERSALS.md`'s D-14 template block and confirm a future author could copy it and fill it without consulting brief.md. Template contains all four D-14 fields (Date, Reversed, New evidence, What would have made the original correct, What did not change) with self-explanatory prompts; SELF-001 section states the exact triggering condition (an empty or reasoning-restating New evidence field) rather than just naming the convention.
why_human: Deferred from 06-04-PLAN.md Task 3's `<human-check>` block — prose-copyability and definitional-completeness judgment, not mechanically checkable. The plan's own SUMMARY recorded this as an unresolved `human_judgment: true` item rather than confirming it.
result: [pending]

### 2. README.md suppressions[] migration and known-limit prose reads as intended
expected: Read the README.md sections added by 06-04 documenting `suppressions[]` migration and the "a frame that lies passes" known limit. The authority requirement reads as a requirement, not a suggestion; the known limit is stated plainly, not softened or buried; the two D-05 rigor tiers are legible without having read brief.md.
why_human: Deferred from 06-04-PLAN.md Task 4's `<human-check>` block — a prose-clarity/tone judgment the plan's own SUMMARY recorded as unresolved (`human_judgment: true`) rather than self-certified.
result: [pending]

### 3. Interference post-mortem cites a real, verifiable failure pattern
expected: Read `examples/known-bad/interference-shared-budget-POSTMORTEM.md` and confirm it names a real, verifiable documented failure pattern with a checkable primary source, not a synthetic narrative written to fit the fixture. The cited source (Hernán & Robins or equivalent primary work named in the post-mortem) is real, the chapter/section locator is accurate, and the described failure pattern is a genuine documented phenomenon rather than invented to match the fixture's encoded defect.
why_human: Deferred from 06-08-PLAN.md Task 1's `<human-check>` block — citation/provenance verification against a primary source is outside what grep/static analysis can confirm. The plan's own SUMMARY flagged the locator as unverified and recorded this as `human_judgment: true`.
result: [pending]

### 4. Bayesian post-mortem states the Ville's-inequality formulation without conflation
expected: Read both known-bad post-mortems (bayesian-continuous-monitoring, frequentist-uncontrolled-continuous) and confirm the Bayesian one states the prior-averaged (Ville's-inequality) formulation unambiguously without conflating it with the point-null/law-of-iterated-logarithm result, and that both cite verifiable primary works. The Deng, Lu & Chen (2016) citation is real and Theorem 1 supports the stated Ville-bound claim (K=19, 1/19≈0.0526); the post-mortem's own text is internally consistent with this and does not slide into the different point-null formulation.
why_human: Deferred from 06-08-PLAN.md Task 2's `<human-check>` block — domain-correctness / citation-accuracy judgment the plan's own SUMMARY recorded as unresolved (`human_judgment: true`) rather than confirming.
result: [pending]

## Summary

total: 4
passed: 0
issues: 0
pending: 4
skipped: 0
blocked: 0

## Gaps
