---
status: testing
phase: 09-monitoring-discipline-symmetric-dsx-par
source: [09-VERIFICATION.md]
started: 2026-08-13T15:10:00Z
updated: 2026-08-13T15:10:00Z
---

## Current Test

number: 1
name: `DSX-PAR-002` scope versus ROADMAP Success Criterion 4's literal wording
expected: |
  A decision on whether the literal roadmap wording — "`DSX-PAR-002` validates
  `paradigm_justification` against the closed vocabulary with no reason ranked above
  another" — is satisfied by the shipped two-code split, or whether `DSX-PAR-002`
  itself should also test closed-vocabulary membership.
awaiting: user response

## Tests

### 1. `DSX-PAR-002` scope versus ROADMAP Success Criterion 4's literal wording

expected: A human decision on whether the two-code split satisfies the roadmap wording, or whether `DSX-PAR-002` needs its own membership check.
result: [pending]

**What shipped.** `DSX-PAR-002` is deliberately membership-free — it checks presence and
requiredness only. Closed-vocabulary membership is owned by `DSX-SPEC-085`, which
pre-dates this phase (Phase 6). The split is documented in
[dsx/frame/paradigm.py](dsx/frame/paradigm.py)'s docstring and in `09-05-PLAN.md`'s
`<resolved_open_questions>`, and its stated reason is to avoid double-firing (decision D-08).

**What the roadmap says.** Success Criterion 4 reads "`DSX-PAR-002` validates
`paradigm_justification` against the closed vocabulary with no reason ranked above another"
— naming `DSX-PAR-002` specifically as the code that does the validating.

**What is not in question.** The substantive property holds end to end. Verified
independently across two verification cycles: there is no input where the combined system
lets a bogus, non-blank `paradigm_justification` pass silently. `DSX-SPEC-085` fires
unconditionally whenever `inference:` is non-empty and the field is non-blank and
non-member, regardless of `design.peeking_policy` or whether `DSX-PAR-002` also fires. The
14-case cross product (`PARADIGM_JUSTIFICATIONS` × `PARADIGMS`) is a genuine runtime
iteration, not hard-coded, and passes. No reason is ranked above another.

**Why this needs a human.** It is a values and scope judgment — how literally to read the
roadmap's prose against the plan's explicit, reasoned design decision — not a code defect.
`git diff 4c983fa..HEAD` shows zero changes to `DSX-PAR-002`'s check logic during gap
closure, so nothing about this item's facts moved this cycle.

**The two answers and what each costs:**

- **Accept the split** (roadmap wording reads as intent, not as an implementation
  assignment). Costs nothing now. Locks in that a future reader of Success Criterion 4 has
  to follow a pointer to `DSX-SPEC-085` to see where membership is enforced. Consider
  amending the roadmap wording so the criterion names both codes.
- **Require membership in `DSX-PAR-002` itself** (roadmap wording reads literally). Costs a
  change to `_check_paradigm_justification` plus a decision about D-08 double-firing —
  either accept two findings for one defect, or add suppression logic between the two codes.

## Summary

total: 1
passed: 0
failed: 0
pending: 1
