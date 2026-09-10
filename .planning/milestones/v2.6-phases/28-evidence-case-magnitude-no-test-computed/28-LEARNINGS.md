---
phase: 28
phase_name: "Evidence case — magnitude no test computed"
project: "gsd-dsx"
generated: "2026-09-10"
counts:
  decisions: 8
  lessons: 5
  patterns: 5
  surprises: 4
missing_artifacts:
  - "UAT.md"
---

# Phase 28 Learnings: Evidence case — magnitude no test computed

## Decisions

### D-28-00: the scope's literal case is already caught — freeze the collision construction instead
The V2.6-SCOPE.md §Phase 28 starting proposal was a claim asserting "a magnitude on metric C that appears in no test." Both personas (Statistician + Architect, independently) found that this literal case is already caught by the existing `DSX-CLM-033` (CRITICAL, numeric-overlap check): a claim quoting numbers for a metric no test reports matches nothing in the union of test numbers, so `DSX-CLM-033` fires CRITICAL — a NO-MINT close. The only honest live-miss seam is the collision/mislabel construction: the claim's numbers (27/18) are the REAL reported numbers of OTHER metrics (tests A/B), so they coincide within `DSX-CLM-033`'s 5% tolerance window and the check clears on its full union-membership logic while no test computed the claimed metric. This is a REFINEMENT driven by the measured behaviour of an existing check, NOT a manufactured miss (D-13).

**Rationale:** The scope's literal wording, if measured as-is, would produce a no-mint control result and waste the phase; the collision construction documents a real, structural gap (`DSX-CLM-033` is metric-blind — it checks number-membership globally, not per-metric binding) that mirrors the commonest real-world magnitude defect (copy-from-the-wrong-row error).
**Source:** 28-CONTEXT.md

---

### D-28-01: fixture shape frozen before measurement
The corpus case is a churn-style, descriptive/observational fixture (keeping causal-identification and `decision.replay` obligations off the spec). Two `results.tests[]` entries on OTHER metrics (`revenue_per_user` effect 0.27, `activation_rate` effect 0.18) both clear the stats reporting contract; one `association`-typed claim on churn (never computed) whose literals 27/18 coincide with tests A/B; no `claims[].supported_by` declared (keeps the fixture an honest MISS for the not-yet-minted check).

**Rationale:** Frozen before any measurement per guardrail 1 (FREEZE-BEFORE-MEASURE); a no-miss outcome at S4-3 would be a valid terminal, never a licence to re-shape.
**Source:** 28-CONTEXT.md

---

### D-28-02: pass/fail rule for "live miss" — swap-still-fires counterfactual applied by literal code
LIVE MISS requires all four gate points (plan/execute/verify/ship) to return ship/pass on the merits, with nothing flagging the uncomputed-magnitude defect after subtracting documented incidental corpus-gap codes. "Incidental" is determined by a literal-code swap test, never narrative: a blocking code counts as incidental only if it still fires when the claim's collision numbers are swapped for numbers that genuinely appear in the cited test.

**Rationale:** Removes any temptation to narratively wave away a blocking finding as "incidental" — the swap counterfactual is mechanically applied and recorded verbatim (Variant 1 honest swap, Variant 2 break swap) before interpretation.
**Source:** 28-CONTEXT.md, 28-MEASUREMENT.md

---

### D-28-04: reserved code `DSX-CLM-034` placed in-family (03x traceability tier)
Both personas independently reached `DSX-CLM-034` as the next-free slot in the `DSX-CLM` 03x (evidence-pointer/overlap) family, rejecting a global-next `DSX-CLM-090`+ as wrong family placement. Reserved, not minted, until a live miss is confirmed.

**Rationale:** A claim→cited-test numeric-traceability check is the direct refinement of 033 (union → cited test) and a traceability sibling of 030–032, so it belongs in 03x rather than a disconnected global-next slot.
**Source:** 28-CONTEXT.md

---

### D-28-05: Wilkinson & TFSI (1999) cited as MOTIVATING PRINCIPLE only, never as the mechanism
HQ-40 rows 40c/40d resolved: cite Wilkinson & TFSI (1999) alone (JARS-Quant dropped as weaker/hedged). Wilkinson mandates reporting effect sizes and intervals for primary outcomes; the minted check enforces a declaration-level traceability corollary (text-to-declared-number overlap, never a recomputation). The docstring must state the check enforces the corollary, not the literal "report an effect size" rule, and must record the bounded-catch honesty: `DSX-CLM-034` catches the collision only via the stray number outside the cited test, not via metric-identity — a claim whose both numbers happened to sit in the one cited test would still pass.

**Rationale:** Prevents over-claiming a citation's authority — using a paper's general principle to imply it mandates a specific numeric-overlap mechanism it never specifies.
**Source:** 28-CONTEXT.md, 28-REVIEW.md (T-28-01 in 28-SECURITY.md)

---

### D-28-06: `DSX-COH-001` encoded as a per-fixture, point-scoped incidental (Option A)
Post-measurement, the frozen fixture was found to fire `DSX-COH-001` (CRITICAL, claim-type-vs-question-strength ladder) at plan/verify/ship — a different property than the magnitude→test traceability defect, but a code that is ALSO `prescriptive-churn-recommendation`'s own legitimate target, so it could not go in the global incidental list (would launder another fixture's real target) or this fixture's own-target map (would falsely credit a catch). Both personas converged on Option A: a new `_PER_FIXTURE_INCIDENTAL_CODES: dict[str, dict[str, frozenset[str]]]` map, read ONLY by the two completeness tests, never by `_own_target_codes`/`_effective_target_map`. Rejected: B (reshape/re-type the claim — voids the frozen design), C (declare COH-001 a second target — a semantic lie), D2 (carve COH-001 out of the anti-laundering guard — guts it).

**Rationale:** The existing two-bucket harness model (global-incidental XOR own-target, kept disjoint) could not express "incidental here, target there" — this was the corpus's first incidental that collides with another fixture's target.
**Source:** 28-CONTEXT.md, 28-02-SUMMARY.md

---

### DSX-CLM-034 severity finalised HIGH
Persona round leaned HIGH (sitting `DSX-CLM-034` in the 030–032 traceability tier, all HIGH, reserving CRITICAL for `DSX-CLM-033`'s fabrication-grade "matches nothing anywhere"). S4-2/S4-3 finalised HIGH against REQ-P28-02's text; at verify/ship the threshold is HIGH, so HIGH loses no enforcement.

**Rationale:** A legible, non-overlapping severity ladder — 034 is `supported_by`-gated (declaration required to even run), 033 reads no `supported_by` and is unconditional, so they cannot double-fire on the same number against the same test.
**Source:** 28-CONTEXT.md, 28-01-SUMMARY.md

---

### Code-review WR-01/IN-01/IN-02 dispositions
WR-01 (MEDIUM: catalogue-count invariant test named/documented "277" while enforcing 278) and IN-02 (LOW: stale mint enumeration in a docstring) were FIXED immediately as test-doc-only edits, no assertion or behaviour change. IN-01 (LOW: `DSX-CLM-034` folds a claim's own declared `ci` into `claim_numbers` via the shared extractor but not into `reference`, unlike `DSX-CLM-033`, creating a latent false-positive path for a future spec that declares both `supported_by` and a divergent own `claim.ci`) was ACCEPTED and tracked rather than fixed, because its correct resolution is a genuine opposed design judgment (mirror DSX-CLM-033's self-consistency treatment vs. keep the stricter cite-only trace) — deferred to a recorded decision rather than a rushed solo behavior change on a minted check.

**Rationale:** Distinguishes documentation drift (safe to fix inline) from a substantive design fork on a just-minted check (requires its own persona round, not a reviewer's unilateral call).
**Source:** 28-REVIEW.md, 28-VERIFICATION.md

---

## Lessons

### D-13 measure-first prevented a wasted mint on the literal scope shape
Had the phase proceeded directly to designing a check for the scope's literal wording ("magnitude in no test"), it would have built a check for a case `DSX-CLM-033` already catches — a wasted mint. Reading the code first (both personas, independently) surfaced that the only live-miss seam was the collision construction, and the S4-3 measurement (VERDICT: LIVE MISS, recorded before any mint code was written) confirmed the prediction rather than assuming it.

**Context:** The persona round explicitly labelled its LIVE MISS prediction "NOT a substitute for measurement" — D-13 requires the four-point measurement to run first, with a no-miss outcome being a valid, honest terminal.
**Source:** 28-CONTEXT.md, 28-MEASUREMENT.md

---

### A check's clearance-by-construction can be more informative than its clearance-by-absence
`DSX-CLM-033` is measured SILENT on the collision fixture — not because it didn't run, but because it ran fully and cleared via the ×100 scale bridge (27→test A effect, 18→test B effect). The break-swap counterfactual (numbers absent from any test) makes `DSX-CLM-033` START firing, proving its silence on the DEFECT fixture is caused by the numeric collision, not by any verification that churn was computed. This "silence caused by clearance, not absence" pattern is exactly what makes the case an honest live miss rather than a bug in the fixture.

**Context:** Verified against the D-28-02 pass/fail rule's swap-still-fires counterfactual, applied by literal code at all five gate points for both the honest swap and the break swap.
**Source:** 28-MEASUREMENT.md

---

### A single passing full-suite run can hide multiple lockstep count pins
The plan and orchestrator baselines named only two catalogue-count pins to move 277→278 (`test_finding_catalogue_invariant.py`, `test_phase20_zero_mint_close.py`). The full suite surfaced a THIRD lockstep pin (`tests/test_p19_categorical_rows.py:83`) that also asserts the catalogue total and would have silently drifted if only the plan's named pins were updated.

**Context:** Documented as Deviation 1 in 28-01-SUMMARY.md; caught only because the executor ran the full suite rather than trusting the plan's enumerated pin list.
**Source:** 28-01-SUMMARY.md

---

### A test's name and docstring can silently diverge from its enforced assertion
`test_finding_catalogue_stays_at_277_codes` had its docstring and failure message asserting "277" while its actual assertion used `_EXPECTED_TOTAL = 278` — a green, correctly-enforcing test whose name and prose actively mislead a future reader into believing the catalogue is still at 277.

**Context:** Found by code review (WR-01) as a direct violation of the phase's own "count pins moved to 278 in lockstep" discipline — the numeric pin moved, but the human-facing name/docstring did not.
**Source:** 28-REVIEW.md

---

### Citation-precision errors in a frozen document need not re-open the decision they support
28-RESEARCH.md found five line-range discrepancies in 28-CONTEXT.md's code citations (e.g., `dsx/pct_base.py:56-72` vs the actual function start at line 50; `claims.py:667-675` vs the actual `DSX-STA-021`/`DSX-STA-020` fire sites at `:710`/`:726`). All were reported loudly as required, but none were load-bearing — the described *behaviour* at each locator was correct, only the line anchor was off by a few lines.

**Context:** Demonstrates that a frozen design decision can tolerate citation drift as long as the substantive claim it supports remains verified correct against the live tree.
**Source:** 28-RESEARCH.md

---

## Patterns

### Declaration-gated static check (DSX-REP-061 mould)
`DSX-CLM-034` follows the same shape as the Phase 27 `DSX-ML-034`/`DSX-REP-061` precedent: an additive, optional field (`claims[].supported_by`) that gates the check entirely — absent field means the check stays silent (buys attribution, not detection). This keeps a fixture that omits the field an honest MISS rather than forcing a false catch.

**When to use:** Any check whose defect can only be verified when the author has explicitly declared a traceability/provenance pointer; the check should never infer the pointer or penalize its absence beyond staying silent.
**Source:** 28-CONTEXT.md, 28-01-SUMMARY.md

---

### `_PER_FIXTURE_INCIDENTAL_CODES` anti-laundering guard via default-empty parameter
`_classify_target_defect` gained a defaulted `incidental: frozenset[str] = frozenset()` param. With the default empty set, the no-expected branch collapses to provably byte-identical behaviour for every existing call site (`exit_code != 0 and matched and matched <= incidental` reduces to `False` when `incidental` is empty) — only the specific (slug, point) pairs named in the new map are loosened. A companion static guard forces every per-fixture incidental entry to be some OTHER slug's declared target in `_effective_target_map()`, so the mechanism is strictly narrower than the global incidental list, never a general escape hatch.

**When to use:** Extending a shared classifier/gate function with a new allowance while guaranteeing zero behaviour change for all pre-existing callers — default the new parameter to the identity value for the old behaviour, then add a static "no free lunch" guard proving the new parameter can't be abused as an unconstrained escape hatch.
**Source:** 28-CONTEXT.md, 28-02-SUMMARY.md, 28-REVIEW.md

---

### Swap-still-fires counterfactual for classifying "incidental" vs "catch"
To decide whether a blocking finding is a genuine catch of the target defect or an unrelated incidental gap, rewrite ONLY the defect-relevant literals (here, the claim's percent numbers) to a value that would make the defect honest, and re-run the full gate. If a code's fire status flips (stops firing), it was a catch of the defect; if it stays invariant across DEFECT/HONEST/BREAK variants, it targets an orthogonal property and is a documented incidental.

**When to use:** Whenever a known-bad corpus fixture fires a blocking code beyond the code(s) the design intends it to test, and the team needs a mechanical (not narrative) way to decide whether that extra fire is part of the "catch" or an unrelated "incidental gap."
**Source:** 28-CONTEXT.md, 28-MEASUREMENT.md

---

### Measure-first mint boundary (D-13) with reserved-but-inactive code numbers
A code number (`DSX-CLM-034`) can be reserved and frozen in the design document (with a D-06 veto window) WITHOUT being minted — the vocabulary, check function, docstring, and catalogue row are all withheld until a dedicated measurement task (run from a fresh isolated tempdir, against the real interpreter) records a verbatim four-point verdict. Only a confirmed LIVE MISS unlocks the RED→GREEN mint tasks; a CAUGHT verdict is a valid no-mint close.

**When to use:** Any phase whose entire premise is "does an existing check already catch this case" — defer all authoring work until the measurement is complete and recorded, so no code is minted based on a prediction.
**Source:** 28-CONTEXT.md, 28-MEASUREMENT.md

---

### Separate new function over branching an existing shared function
`_check_supported_by_traceability` was authored as a brand-new function in `claims.py`, dispatched separately from `_check_numeric_overlap` (which backs the uncited `DSX-CLM-033`), rather than as a branch inside the existing function.

**When to use:** When minting a new check whose citation/honesty obligations differ from an existing check that shares similar logic — keeping them as separate functions avoids forcing a docstring rewrite of a function shared with a differently-sourced check and avoids diluting either check's citation provenance.
**Source:** 28-RESEARCH.md (Assumption A2), 28-SECURITY.md (T-28-03)

---

## Surprises

### The scope's own literal wording was already dead on arrival
The phase's starting proposal (a claim whose magnitude "appears in no test") turned out to be a case the codebase already handles via `DSX-CLM-033`'s union-membership logic — discovered only by both personas independently reading the check code rather than trusting the scope text. The phase had to pivot its entire target case (to the collision/mislabel construction) before any design work could proceed.

**Impact:** Without the D-13/measure-first discipline and the code-grounded persona round, the phase risked minting a redundant check for an already-caught defect — the literal scope shape was preserved only as the "no-mint control."
**Source:** 28-CONTEXT.md

---

### A CRITICAL check's full, correct execution can be exactly what produces the miss
`DSX-CLM-033` doesn't fail to run or get skipped on the collision fixture — it runs its complete union-membership logic and correctly clears, because the claim's numbers genuinely do match real reported numbers (just for the wrong metric). The "bug" in coverage is produced by the check working exactly as designed on a case its design never anticipated (metric-blind matching), not by any malfunction.

**Impact:** Reframes how a live miss should be diagnosed in this codebase — not "which check failed to run" but "which check's correct, full-logic behaviour still leaves a gap because it was never designed to verify this specific property (metric binding, not just numeric membership)."
**Source:** 28-MEASUREMENT.md, 28-CONTEXT.md (D-28-00)

---

### A frozen, minimal fixture triggered an unrelated CRITICAL that also belonged to another fixture's target
The D-28-01 fixture design didn't anticipate that its association-typed claim under a descriptive question would trip `DSX-COH-001` — and that this same code was already the legitimate target of a different existing fixture (`prescriptive-churn-recommendation`). This was the corpus's first case of an incidental fire colliding with another fixture's own target, which the existing two-bucket harness model (global-incidental XOR own-target) had no way to express.

**Impact:** Required a new harness mechanism (`_PER_FIXTURE_INCIDENTAL_CODES`, D-28-06) with its own anti-laundering guards rather than a one-line allowlist edit — turning what looked like harness plumbing into a full persona-round decision.
**Source:** 28-CONTEXT.md (D-28-06)

---

### A green test's name and docstring had been lying about the number it enforced
`test_finding_catalogue_stays_at_277_codes` passed on every run while actually enforcing 278 — its name and prose were stale from before the count pin moved. This was found only by a deep code review reading the test body against its own name/docstring, not by any automated gate (the assertions themselves were correct, so nothing red-failed).

**Impact:** A future maintainer grepping for "277" and seeing this test green would have been actively misled into believing the catalogue was still at 277 when it was at 278 — a class of drift that passing tests alone cannot catch.
**Source:** 28-REVIEW.md (WR-01)
