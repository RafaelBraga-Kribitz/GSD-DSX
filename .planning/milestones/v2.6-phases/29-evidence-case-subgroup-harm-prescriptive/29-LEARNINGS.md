---
phase: 29
phase_name: "Evidence case — subgroup harm under a prescriptive recommendation"
project: "gsd-dsx"
generated: "2026-09-10"
counts:
  decisions: 9
  lessons: 6
  patterns: 6
  surprises: 5
missing_artifacts:
  - "UAT.md"
---

# Phase 29 Learnings: Evidence case — subgroup harm under a prescriptive recommendation

## Decisions

### D-29-00 — Harness-polarity correction: this fixture is a TARGET, not a Phase-27/28 permanent miss
This is the load-bearing finding of the phase's discuss round. REQ-P29-03 fixes the check as "missing row → CRITICAL": the check fires on the *absence* of a `decision.subgroup_harm[]` row given the *presence* of an opposing segment already declared in `results.segments[]` — there is no opt-in pointer to omit, unlike Phase 27's `feature_provenance` and Phase 28's `supported_by`, which stay permanent misses because they are declaration-gated on an opt-in pointer the honest fixture omits. Consequence: once DSX-COH-041 ships, it fires CRITICAL on the honestly-declared fixture — a genuine *detection*, not mere *attribution*. The fixture wires as `_TARGET_DEFECT_CODES[slug]` (present/caught at plan/verify/ship), not a `kind: miss` sidecar with `absent_code` — the corpus's first `kind: target`, and the inverse of the Phase 27/28 permanent-miss polarity. This forced the harness to carry point-scoped `_TARGET_DEFECT_CODES` + an empty `_EXPECTED_CAUGHT_DEFECTS` + a new closed vocabulary `("miss", "caught", "target")` rather than the CONTEXT's literal frozenset wiring (see Surprises).

**Rationale:** REQ-P29-03's check design structurally cannot be pointer-gated without defeating the requirement; the harness must reflect a real catch, not an attribution-only miss.
**Source:** 29-CONTEXT.md

---

### D-29-01 — Segment-harm floor: `decision.subgroup_harm_floor`, integer absolute n, default 0
The field is a non-negative integer absolute n in the `decision` block. Default when absent is 0 (unanimous, both personas) — no escape by omission; to *not* disposition an opposing segment, the analyst must affirmatively declare a floor above that segment's n, a single auditable, challengeable integer. A declared floor may only raise the bar, never lower it (the D-28-03 "may tighten, never loosen" precedent applied to a floor). The rejected alternative (declaration-gated-silent, mirroring Phase 27/28) was rejected because it reproduces the exact gap the check exists to close.

**Rationale:** DSX-COH-041 detects from `results.segments` alone (no pointer needed), so the stronger un-gameable default is available and taken; corpus-safety of default 0 was verified (not assumed) against every good-corpus spec.
**Source:** 29-CONTEXT.md

---

### D-29-02 — Frozen four-segment case shape (slug `subgroup-harm-without-disposition`)
Built as a minimal-perturbation clone of a causal+experiment good spec (no good `prescriptive` fixture exists to clone): question_type causal→prescriptive, claim retyped prescriptive, `results.segments[]` = 3 positive segments (A n=4000 +5.0pp, B n=3000 +4.0pp, C n=2000 +3.0pp) + 1 minority opposing segment (D n=1000 −6.0pp), positive n-weighted `overall_effect` = +3.2pp, floor declared 500, and `decision.subgroup_harm[]` omitted entirely as the sole defect. D is a material, decision-changing harm (n=1000 ≫ floor 500) — explicitly not shaved toward triviality to manufacture a miss.

**Rationale:** The structural opposite of the existing `prescriptive-churn-recommendation` fixture (which keeps the question descriptive to make a prescriptive *claim* an overreach); here the question is genuinely prescriptive and clears the ceiling on the merits, so the only residual is the undispositioned harm.
**Source:** 29-CONTEXT.md

---

### D-29-03 — One code, two severities for the disposition ladder
`decision.subgroup_harm[]` = `{segment, effect, ci, n, disposition, rationale}`, `disposition ∈ {accept | exclude | mitigate}`. Opposing segment ≥ floor with no matching row → CRITICAL; a matching `accept` row with blank/missing rationale → HIGH; an unknown disposition value or a row missing a required key was recommended (S5-2 to confirm) → CRITICAL (no valid disposition = silence). The two firing conditions are per-segment mutually exclusive, keeping the ladder legible (precedent: DSX-COH-030 is already one code at two severities).

**Rationale:** Matches REQ-P29-03's singular "number" requirement while covering both the missing-declaration and the empty-declaration evasion.
**Source:** 29-CONTEXT.md

---

### D-29-04 — Reserved code `DSX-COH-041` (04x decision-obligation tier)
Live-catalogue re-measured (not assumed): Total 278, DSX-COH-041 free. The 04x tier is the decision-block-completeness tier (040 = revisit_when missing); `subgroup_harm[]` is the same kind of obligation, so it is a direct sibling of 040. Tie-break recorded: the Architect voted DSX-COH-041 on tier-placement rigour; the Statistician named DSX-COH-050 only as "next round number" and explicitly deferred to the veto window — resolved by rigour > reliability > flexibility, consistent with Phase 28's fill-the-tier D-06 precedent.

**Rationale:** Follows the established "fill the tier before opening a new one" numbering discipline.
**Source:** 29-CONTEXT.md

---

### D-29-05 — D-05 honesty: Gail & Simon (1985) is the motivating definition, never the mechanism
Gail & Simon (1985), *Testing for qualitative interactions between treatment effects and patient subsets*, Biometrics 41(2):361–372, PMID 4027319 (HQ-40 row 40e, human-confirmed at PubMed). MAY claim: it is the motivating definition of a qualitative/crossover interaction (opposite-sign treatment effects across subsets) — what motivates when a segment counts as harmed. MUST NOT claim: that it authorises the enforcement mechanic — their paper is a likelihood-ratio test; the minted check computes no statistic on the gate path (D-02) and enforces only the declaration. Bounded-catch honesty: DSX-COH-041 buys attribution over honestly-declared segments, not detection of hidden harm — a spec that omits the harmed segment, lies about the sign, or declares a gamed floor above D's n still passes.

**Rationale:** Mirrors the Phase 28 D-28-05 citation-honesty discipline exactly; prevents laundering a motivating definition into an asserted mechanism.
**Source:** 29-CONTEXT.md

---

### REQ-P29-02 documented public case: Obermeyer et al. (2019), confirmed at abstract + metadata grade only
Obermeyer, Powers, Vogeli & Mullainathan (2019), "Dissecting racial bias in an algorithm used to manage the health of populations," Science 366(6464):447–453, DOI 10.1126/science.aax2342, was designated as the REQ-P29-02 documented public case (a positive aggregate accuracy metric masking material racial harm in a minority subgroup). Confirmed via Crossref (publisher metadata) + Semantic Scholar (verbatim abstract); the full-text PDF was retrieved but could not be rendered in-environment, so no full-body read is claimed — explicitly recorded as "abstract + authoritative metadata confirmed," never implying the body was read. The boundary is stated explicitly: Obermeyer is a label-bias/allocation-fairness case, not a Gail & Simon opposite-sign treatment contrast; the two sources fill REQ-P29-02's two distinct roles (real-world motivation vs enforcement definition) and neither is asked to do the other's job.

**Rationale:** This is phase research, not a D-05 human read (the D-05 source, Gail & Simon, was already closed at S5-1); "not found" would have been a valid recorded outcome, but the case was found and its confirmation grade honestly bounded.
**Source:** 29-RESEARCH.md

---

### Harness wiring resolution: point-scoped `_TARGET_DEFECT_CODES`, empty `_EXPECTED_CAUGHT_DEFECTS`
The frozen CONTEXT's literal instruction — `_EXPECTED_CAUGHT_DEFECTS[slug] = frozenset({DSX-COH-041})` AND `_TARGET_DEFECT_CODES[slug] = DSX-COH-041 at plan/verify/ship` — cannot both hold: `_EXPECTED_CAUGHT_DEFECTS` applies its frozenset at both `_CRITICAL_THRESHOLD_POINTS` (plan AND execute), but the `coherence` family is absent from execute, so DSX-COH-041 never fires there. Resolution (mirroring the existing `prescriptive-churn-recommendation` fixture exactly): the catch lives point-scoped in `_TARGET_DEFECT_CODES` (plan/verify/ship); `_EXPECTED_CAUGHT_DEFECTS[slug] = frozenset()` (empty, required only for key-parity).

**Rationale:** A mechanism clarification, not a design change — the D-29-00 intent ("PRESENT/caught, not an absent miss") is fully honored either way.
**Source:** 29-02-PLAN.md

---

### `kind: target` taught to the ATTRIBUTION sidecar as a new closed-vocabulary value
The closed-vocabulary assertion in `test_attribution_sidecars_reference_valid_codes_and_items` was extended from `("miss", "caught")` to `("miss", "caught", "target")`. A distinct `target` value (rather than reusing `caught`) was chosen deliberately: the five existing caught fixtures carry no sidecar (pure catches), while this fixture is a hybrid — caught AND a §6.5-backlog promotion needing a sidecar to carry `promotes_backlog_item` — so a first-class value makes the dual role legible and machine-checkable. The `absent_code` field name is reused as schema legacy; for `kind: target` it names the code that fires (asserted present by the falsifiability non-miss branch), not one that is absent.

**Rationale:** Matches the CONTEXT's D-29-00 language ("wires as a TARGET") while keeping the existing sidecar schema intact.
**Source:** 29-02-PLAN.md

---

## Lessons

### A frozen plan's enumerated behaviours can under-specify a recommendation it inherited
The S5-2 plan (29-01-PLAN.md) enumerated only the two REQ-P29-03 severities in its RED/GREEN task behaviour bullets, but neither carried forward nor explicitly rejected the discuss round's own D-29-03 recommendation that "an unknown disposition value or a row missing a required key → CRITICAL." The resulting implementation let a content-free `- segment: D` row (no/invalid disposition) silence the CRITICAL entirely — the check's "force disclosure" guarantee defeated by a declaration that discloses nothing. Caught only at code review (HG-01).

**Context:** A frozen design decision is not automatically preserved through to an executable plan's behaviour bullets; each bullet must be checked against every SETTLED recommendation, not just the requirement text.
**Source:** 29-REVIEW.md

---

### A borrowed guard's rationale does not automatically transfer to the new check's semantics
The `len(segments) < 2: return` early-return was copied verbatim from `_check_simpsons_paradox`, where ≥2 segments are needed to compare segments *against each other* for a reversal. The new check instead compares each segment's sign against the declared `overall_effect` independently, so its semantics need only 1 segment — but the copied guard silenced a lone declared opposing segment (MD-01), an evasion (drop the aligned segments, declare only the harmed one) the frozen design never intended.

**Context:** Mirroring an existing check's guard/mould for code-shape consistency is good practice, but each guard's *rationale* must be re-derived for the new check's actual predicate, not copied wholesale.
**Source:** 29-REVIEW.md

---

### An "un-gameable default" claim must be checked against every field the trigger reads, not just the floor
D-29-01 stated the default floor of 0 gives "no escape by omission." But the implementation computed `above_floor = n is not None and n >= floor`, so a declared opposing segment that simply omitted `n` escaped detection at any floor, including the strict default (MD-02) — an evasion not listed in the docstring's bounded-catch boundary.

**Context:** A structural/declaration-only check's soundness claims are only as strong as the field-presence handling of every input the trigger reads; each optional field needs its own omission-escape analysis, not just the one the design narrative focuses on.
**Source:** 29-REVIEW.md

---

### D-05 citation honesty requires stating the bounded-catch limit explicitly, not just correctly
Even with a correctly-scoped citation (Gail & Simon as motivating definition only), the honesty discipline requires the docstring to enumerate exactly which evasions the check does and does not catch. The code review found the three fixed evasions (HG-01/MD-01/MD-02) were "not listed in the docstring's bounded-catch paragraph" even before the fixes — meaning the original bounded-catch statement was narrower than the check's actual (buggy) permissiveness.

**Context:** A bounded-catch honesty statement is not just about the citation's scope; it must be re-verified against the check's actual behaviour at every code-review pass, since implementation gaps silently widen what "honestly passes."
**Source:** 29-REVIEW.md

---

### A crashed firing can leave a later-stage artifact missing without invalidating the earlier work
`29-VALIDATION.md` records that "No planner-seeded VALIDATION.md existed (the crashed 12:38Z S5-5 firing wrote `29-SECURITY.md` but not this file)" — validate-phase authored the file directly from the frozen CONTEXT and the plans' task structure rather than treating the crash as a reason to redo prior work. Correspondingly, `29-01-SUMMARY.md` does not exist even though the phase's mint work (measurement, code, tests, catalogue) clearly landed and was independently re-verified downstream (29-REVIEW.md, 29-VERIFICATION.md).

**Context:** A missing SUMMARY/report file after a crash is not itself evidence the underlying work is missing or wrong — the recovery path is to independently re-verify the artifacts that do exist on disk/in the repo rather than assume total loss.
**Source:** 29-VALIDATION.md

---

### Independent re-verification of subagent claims caught real gaps a trusted report would have missed
The orchestrator explicitly did not trust the `gsd-code-reviewer` subagent's findings or the plan's own claims, re-running every gate on real Python 3.12.10 and re-reading the frozen design before dispositioning HG-01/MD-01/MD-02. This surfaced that the S5-2 plan itself (not just the implementation) had under-specified a settled recommendation (HG-01), which a purely code-level review might have framed as "matches spec."

**Context:** For a portfolio project held to a sceptical-statistician bar, cross-checking a review's findings against the frozen decisions document — not just against the code — is what distinguishes a real defect from a spec-compliant-but-wrong implementation.
**Source:** 29-REVIEW.md

---

## Patterns

### Measure-first (D-13): record the live verdict from a fresh tempdir before authoring any mint code
Task 1 of the mint plan builds the frozen fixture, runs the full gate protocol (validate/plan/execute/verify/ship) from a fresh `tempfile.TemporaryDirectory()`, and writes a MEASUREMENT.md whose first content line is an explicit `VERDICT: LIVE MISS` or `VERDICT: CAUGHT` — produced before any check code exists. Every subsequent task is conditional on that recorded verdict, with explicit branch routing (Branch A no-mint terminal vs Branch B mint path) rather than an implicit "mint by default."

**When to use:** Any phase whose purpose is to justify minting a new finding code from a claimed corpus gap — the verdict must be measured against the *current* gate, not assumed from the design discussion.
**Source:** 29-01-PLAN.md, 29-MEASUREMENT.md

---

### Swap-still-fires counterfactual to separate a real catch from an incidental finding
After measuring the defect fixture, re-run a variant with the target's polarity flipped (here, segment D's effect flipped from opposing to aligned) and diff the CRITICAL/HIGH residual sets. A code that stops firing under the swap is a real catch tied to the defect; a code that still fires is incidental (documented, not credited). Applied twice in this phase: once pre-mint (nothing toggles — confirming a clean live miss) and once post-mint on the promoted fixture (DSX-COH-041 disappears under the swap, DSX-STA-011 MEDIUM persists as swap-invariant).

**When to use:** Whenever attributing a gate finding to a specific fixture defect, especially before wiring a harness map or crediting a catch.
**Source:** 29-CONTEXT.md, 29-MEASUREMENT.md, 29-02-SUMMARY.md

---

### Orphan-adoption recovery: independently re-verify crashed-firing artifacts rather than redo them
Where a prior firing crashed mid-loop (the 12:38Z S5-5 firing that produced 29-SECURITY.md but not 29-VALIDATION.md; the 29-01 mint work that landed without a 29-01-SUMMARY.md), the recovery path taken was to adopt the artifacts already on disk and independently re-verify them against the frozen design and the live gate (re-running the full suite, re-checking the catalogue, re-reading the code) rather than discard and redo the work from scratch.

**When to use:** When resuming after an interrupted/crashed automated firing where committed or uncommitted work already exists — verify what's there before assuming it must be rebuilt. (Distinct from operator/human-authored work, which is held rather than adopted.)
**Source:** 29-VALIDATION.md, 29-REVIEW.md, 29-SECURITY.md

---

### `kind: target` sidecar for a fixture that is both a caught defect and a backlog promotion
A dedicated ATTRIBUTION sidecar `kind` value distinct from the existing `miss`/`caught` values, used when a fixture both (a) is genuinely caught by a live code at a gate point and (b) promotes a specific `_SECTION_65_ITEM_IDS` backlog item. The `absent_code` field is reused (schema legacy) but its assertion inverts: for `target`, the named code is asserted PRESENT (fires CRITICAL live) rather than absent.

**When to use:** When a new finding code retires a documented backlog gap by genuinely detecting the defect the gap named, as opposed to an attribution-only sidecar for a defect that remains undetected by design.
**Source:** 29-02-PLAN.md

---

### Point-scoped target-defect map vs both-points expected-caught map
When a check family is registered at only a subset of gate points (here `coherence` at plan/verify/ship, absent from execute), a fixture's catch must be recorded in the point-scoped map (`_TARGET_DEFECT_CODES`), not the map that applies uniformly across both CRITICAL-threshold points (`_EXPECTED_CAUGHT_DEFECTS`) — the latter would wrongly demand the code fire at execute and fail the critical-threshold test.

**When to use:** Whenever wiring a new corpus fixture's catch into the harness for a check whose family is not registered at every gate point.
**Source:** 29-02-PLAN.md

---

### Strict-tightening fixes at code review, applied solo without a persona fork when unambiguous
HG-01/MD-01/MD-02 were all fixed by narrowing an over-permissive branch of a freshly-minted check to align with the already-SETTLED/FROZEN design (D-29-01/D-29-03) — never widening or reshaping the frozen fixture itself. Because each fix implemented an existing settled recommendation or an unambiguous contradiction between code and frozen design (not a new judgment call), the orchestrator applied them directly with a loud recorded rationale, citing the same precedent as a prior phase's equivalent fix (Phase 27 WR-01), rather than spinning up a second persona-round discussion.

**When to use:** When a code-review finding shows implementation diverging from an already-frozen decision (not from ambiguity in the decision itself) — fix directly and record the rationale rather than reopening design discussion.
**Source:** 29-REVIEW.md

---

## Surprises

### The phase produces the corpus's first `kind: target` fixture — the inverse of every prior evidence-case phase
Phase 27 and Phase 28 both minted checks that are declaration-gated on an opt-in pointer the honest fixture omits, so their fixtures stay permanent misses (`kind: miss`, `absent_code`, "attribution not detection" — the minted check never fires on the honest fixture). Phase 29's REQ-P29-03 design is structurally different: the check detects from already-declared fields with no opt-in pointer to omit, so once minted it genuinely catches the honest fixture. This is explicitly called out in the CONTEXT as diverging from the mirrored Phase-27/28 pattern and as FORCED by the requirement, not chosen.

**Impact:** Required inventing new harness machinery (a `kind: target` sidecar value, point-scoped target-defect wiring) rather than reusing the Phase 27/28 miss machinery, and inverted the intuition that a newly-discovered gap phase always ships an attribution-only miss.
**Source:** 29-CONTEXT.md

---

### The frozen CONTEXT's own harness-wiring instruction was internally contradictory once live code was read
The CONTEXT prescribed both `_EXPECTED_CAUGHT_DEFECTS[slug] = frozenset({DSX-COH-041})` AND `_TARGET_DEFECT_CODES[slug] = DSX-COH-041 at plan/verify/ship`. Live verification at plan-authoring time showed these cannot both hold, because `_EXPECTED_CAUGHT_DEFECTS` applies uniformly across both CRITICAL-threshold points (plan and execute) while `coherence` (and therefore DSX-COH-041) is absent from execute — so the literal frozen instruction, if implemented as written, would have failed the critical-threshold test.

**Impact:** Even a carefully persona-verified, twice-independently-grounded frozen design can contain a mechanism-level inconsistency that only surfaces when the plan author reads the actual harness code; the resolution was recorded as a mechanism clarification (not a design reopening) precisely because the underlying intent was unambiguous.
**Source:** 29-02-PLAN.md

---

### The existing gate actively reassures on the exact defect the phase targets
Measurement showed that at 1-of-4 opposing segments, not only were `DSX-MET-030`/`031` silent, but the `else` branch of `_check_simpsons_paradox` emitted `report.ok("segment effects are directionally consistent with the aggregate")` — an INFO finding observed at every gate point. The existing check does not merely fail to catch the harm; it produces an affirmatively reassuring message on a book that hides a −6.0pp minority harm.

**Impact:** Strengthens the case that the ≥half rule is structurally, not just incidentally, blind to minority harm, and that the gap is a genuine analytical risk (a positive-looking gate signal) rather than a benign silence.
**Source:** 29-MEASUREMENT.md

---

### A check that passed all its specified unit tests still had three silent-evasion gaps at code review
Despite `test_subgroup_harm_disposition.py` covering seven behaviour bullets and passing GREEN, the code-reviewer found three ways to silence the CRITICAL finding that were outside the specified test matrix: a content-free disposition row, a lone declared opposing segment, and an omitted `n` field. None of these were vacuous-test findings — the existing tests were confirmed non-vacuous (asserting both count and severity) — the gaps were genuinely unspecified behaviour paths.

**Impact:** Demonstrates that "all specified behaviours pass" is not equivalent to "all evasions of the frozen design's stated guarantees are closed" — the review's cross-file/live-probe depth (not just running the shipped test suite) was what surfaced these before ship.
**Source:** 29-REVIEW.md

---

### REQ-P29-02's two source obligations turned out to require two distinct real-world papers, not one
The requirement text ("documented public case where an average benefit masked subgroup harm, found with a primary source") could plausibly have been satisfied by Gail & Simon (1985) alone (it also illustrates qualitative interaction on real breast-cancer trial data). Instead, the research explicitly kept the enforcement-definition role (Gail & Simon) and the documented-public-case role (Obermeyer et al. 2019) separate, stating neither source is asked to do the other's job — a stricter reading than the minimum needed to close the requirement.

**Impact:** Produces a more defensible evidentiary record for a sceptical-statistician bar (two independently-confirmed primary sources at their honest respective confirmation grades) at the cost of additional research effort beyond the already-closed D-05 citation.
**Source:** 29-RESEARCH.md

---
