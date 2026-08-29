---
phase: 15
phase_name: "CUPED and BI declaration checks (new codes, D-05)"
project: "gsd-dsx"
generated: "2026-08-29"
counts:
  decisions: 6
  lessons: 3
  patterns: 4
  surprises: 2
missing_artifacts:
  - "UAT.md"
---

# Phase 15 Learnings: CUPED and BI declaration checks (new codes, D-05)

## Decisions

### Exactly two finding codes minted: DSX-EXP-070 (CRITICAL) and DSX-MET-021 (HIGH)
D-01: the persona round (Architect + Statistician, both opus/high) was unanimous that
Phase 15 mints exactly two codes — `DSX-EXP-070` for the CUPED post-treatment-covariate
check and `DSX-MET-021` for the changing-denominator check. Survivorship-bias is not
minted. REQ-P15-01/03/05/06/07 mint nothing. Catalogue moves 258 → 260 additively; the
orchestrator re-verified the pre-phase baseline (`gen-finding-catalogue.py --check`
exit 0 at 258, both new codes absent by grep) before minting.

**Rationale:** Two codes are the genuinely free, citation-backed slots the D-05 primary-source reads support; a third (survivorship) lacked a transferable citation.
**Source:** 15-CONTEXT.md

---

### DSX-EXP-070 (CUPED covariate timing) is CRITICAL, cites Deng et al. 2013 WSDM
D-02: `DSX-EXP-070` lives in `dsx/checks/design.py`, dispatched from the always-run
`design.check()` tail (not the causal-gated frame), keyed on
`normalize(variance_adjustment) == "cuped"`. Fires CRITICAL when
`design.cuped.covariate_timing` is `post_treatment` or any unrecognised/absent value;
stays silent only on `pre_experiment`. Severity CRITICAL is forced by REQ-P15-02's own
wording ("exits 1 at `dsx gate plan`") — no `GATE_THRESHOLDS`/`GATE_PROFILES` edit
needed since `plan`/`execute` already block at CRITICAL. Citation is Deng, Xu, Kohavi &
Walker (2013), WSDM '13, DOI 10.1145/2433396.2433413 — explicitly NOT the Unified
Framework playbook snippet.

**Rationale:** A correctness field at a CRITICAL gate must not let a typo or omission be cheaper than declaring `post_treatment` honestly (INT-010/INT-030 doctrine); keeping the vocab strictly two-valued avoids false-flagging a valid covariate.
**Source:** 15-CONTEXT.md

---

### DSX-MET-021 (changing denominator) is HIGH not CRITICAL, and lives in MET not INT
D-03: the round's one split. The Statistician argued CRITICAL (sibling to the CRITICAL
Simpson code `DSX-MET-030`); the Architect argued HIGH. The orchestrator adopted HIGH
because a declaration-only check can only evidence that bucket allocation *shifted*, not
that the pooled result's sign actually *reversed* — claiming CRITICAL would overstate
what the declaration proves. It also placed the check in `dsx/checks/metrics.py` (runs
unconditionally) rather than `dsx/frame/interference.py` (causal-gated, only active for
`question_type ∈ {causal, prescriptive}` or `design.kind == experiment`), because the
REQ-P15-03 target is a descriptive/diagnostic BI spec that would silently skip an INT
code. Cites Crook, Frasca, Kohavi & Longbotham (2009), KDD '09, DOI
10.1145/1557019.1557139, §6 "Pitfall 4".

**Rationale:** MET-030 is CRITICAL because it detects the *realised* reversal from declared segment effects; MET-021 detects only the precondition, and the sibling denominator code `DSX-MET-020` is also HIGH, so HIGH is catalogue-consistent. Reliability also favours HIGH (avoids over-blocking legitimate cohort comparisons that differ in size but not definition).
**Source:** 15-CONTEXT.md

---

### REQ-P15-04 ships PARTIAL, loud — survivorship-bias code is not minted
D-05: the requirement as worded expects both survivorship and changing-denominator
checks to ship. Per operator-answered HQ-8 ("Brown et al. 1992 does not transfer — leave
unshipped"), Phase 15 ships only the changing-denominator half. This is compliant with
REQ-P15-04's own escape clause ("a code without a citation does not ship and stays in
§6.5") but must be recorded loudly, never as a bare checkmark. A falsifiable D-13 entry
condition is defined for future promotion: an admissible D-05 source must give an
operationalisable *declared-field* criterion for cohort/funnel survivor-conditioning
(explicitly not Brown et al. 1992, whose mechanism is a computed-quantity defect), plus
a documented M5-corpus failure case not already caught by `DSX-VAL-050`.

**Rationale:** Brown et al. 1992's persistence-statistic mechanism is a computed-quantity defect, not a declared-field criterion, so it cannot support a declaration-only gate check.
**Source:** 15-CONTEXT.md

---

### D-06 numbering and D-09 allowlisting are by exact code, never by prefix
D-08/D-09: the additive invariant rebaseline bumps `_EXPECTED_TOTAL` 258→260 and adds
both new codes to `_MINTED_CODES`, while `_SNAPSHOT_TOTAL` stays 256 and the byte-frozen
`tests/fixtures/finding-codes-phase12.md` is never mutated. Separately,
`DSX-EXP-070`/`DSX-MET-021` are added to `_D05_ALLOWLIST_CODES` as exact strings, never
as `DSX-EXP-`/`DSX-MET-` prefixes — those are legacy families with pre-existing uncited
members, and a prefix add would drag them into D-05 enforcement and fail the build red.

**Rationale:** Exact-code allowlisting scopes the new D-05 citation obligation to only the codes that actually earned a primary-source citation this phase, following the precedent of `DSX-SPEC-080..086` and `DSX-ML-043`.
**Source:** 15-CONTEXT.md

---

### CUPED worked value pins ρ²=25% (the derived identity), not the ~50% Bing headline
D-06: the test/docstring constant asserts the analytic identity `variance reduction =
ρ²` at `ρ=0.5 → 25%` (variance ratio 0.75) because it is the paper's own derived result.
The empirical ~50% Bing headline (ρ≈0.707) is kept only as docstring context, never
asserted as the worked value, because it is empirical rather than a derived identity.

**Rationale:** A test should pin the citable, reproducible mathematical identity rather than an empirical outcome that depends on unstated context.
**Source:** 15-CONTEXT.md

---

## Lessons

### A cross-phase byte-anchor SHA must be updated in the same commit that changes the anchored file
Plan 15-04 legitimately added `_check_cuped` to `dsx/checks/design.py`, which is pinned
by a CRLF-normalised SHA-256 anchor in
`tests/test_frame_val.py::test_design_checks_py_content_is_unmodified_since_phase_start`
(the REQ-P7-03 guard). The 15-04 feature commit did not update the anchor alongside the
code change, so the full suite — deferred from S4-3 and run at S4-4 code review — failed
with `a4f296c2… != f18056a6…`. The fix recomputed the hash independently, updated the
constant, and added a dated rationale comment; this is the anchor's own documented
escape hatch, used three times before (S0-6a and twice in Phase 11.3).

**Context:** Caught only because the full suite was re-run at code review rather than trusted from the plan's own (narrower, task-scoped) verification; the guard's behavioural invariant was confirmed untouched (the three VAL/EXP disjointness tests passed pre-fix).
**Source:** REVIEW.md

---

### Keep reference arithmetic off the gate path entirely, even when it is trivial
The CUPED math (`cuped_theta`, `cuped_variance_reduction` — θ and 1−ρ²) lives only in
`dsx/mathx.py`, is pure and stdlib-only, carries a `# D-05:` test marker, and is verified
by AST inspection to never be imported by `dsx/checks/design.py`. The gate check itself
computes nothing — it only reads a declared `covariate_timing` string. This mirrors the
existing `dsx.mathx.diluted_effect` ↔ INT-030 precedent.

**Context:** Declaration-only gate checks (D-01/D-02 doctrine) must not import pandas/scipy/numpy or perform data computation, even to validate a formula the check's own docstring cites — the arithmetic exists solely so the cited identity is testable/documented, not so the check can compute it.
**Source:** 15-04-SUMMARY.md, 15-CONTEXT.md

---

### Requirement wording and severity claims can silently conflate two different requirements
Part of the Statistician's CRITICAL argument for `DSX-MET-021` relied on "exits 1 at
`dsx gate plan`" — but that plan-blocking clause actually belongs to REQ-P15-02 (CUPED),
not REQ-P15-04 (changing-denominator), which only requires the defect to "block its own
bad fixture" (satisfied at HIGH, verify/ship). The orchestrator caught and named this as
a premise conflation before adopting HIGH.

**Context:** Cross-checking a severity argument against the literal text of the requirement it claims to satisfy — rather than against a same-milestone sibling requirement — surfaced a borrowed-justification error before it shipped.
**Source:** 15-CONTEXT.md

---

## Patterns

### Wave-ordered execution so a vocabulary keystone lands before its consumer
`15-01` (adds `cuped` to `VARIANCE_ADJUSTMENTS` and the `CUPED_COVARIATE_TIMINGS`
vocabulary) runs alone in wave 1, strictly before `15-04` (`depends_on: [15-01]`, wave
2), which imports `CUPED_COVARIATE_TIMINGS` for the `DSX-EXP-070` check. Landing them in
the other order would mean a `variance_adjustment: cuped` spec draws a stray
`DSX-SPEC-044` (MEDIUM) and the pre-experiment PASS fixture is not clean.

**When to use:** Any phase where a new check keys on a vocabulary value — mint the vocabulary member in an earlier wave than the check that dispatches on it, and make the dependency explicit via `depends_on` so single-writer-per-wave still holds.
**Source:** 15-CONTEXT.md, 15-01-PLAN.md, 15-04-PLAN.md

---

### Single, final catalogue regen point after all mint sites exist
Both `report.add` sites (`DSX-MET-021` in 15-02, `DSX-EXP-070` in 15-04) are added
first, deliberately leaving the catalogue "intentionally stale." Plan 15-02 and 15-04
explicitly instruct NOT to run `gen-finding-catalogue.py --check` or the invariant test
in those plans, since asserting catalogue currency there would fail spuriously. Plan
15-06 (`depends_on: [15-02, 15-04]`, wave 3) is the sole, final regen point —
`--write` then `--check` exit 0 at 260 — and the sole writer of
`tests/test_finding_catalogue_invariant.py`'s rebaseline. The byte-frozen Phase-12
snapshot (`tests/fixtures/finding-codes-phase12.md`, `_SNAPSHOT_TOTAL = 256`) is never
mutated; the additive expected set becomes `snapshot ∪ {REP-060, REP-061, EXP-070,
MET-021}`.

**When to use:** Any phase minting more than one finding code across parallel/staged plans — mint first, regenerate once at the end in a dedicated plan that depends on every mint site, and keep the historical snapshot frozen with the rebaseline expressed as an additive union.
**Source:** 15-CONTEXT.md, 15-02-PLAN.md, 15-04-PLAN.md, 15-06-PLAN.md, 15-06-SUMMARY.md

---

### Declaration-only checks proven disjoint from a sibling code via a bidirectional fixture test
`DSX-MET-021` (reads `results.cohort_comparisons`, fires on allocation/sampling-rate
spread between cohorts) had to be proven provably disjoint from the pre-existing
`DSX-MET-020` (reads `results.period_comparisons`, fires on count-magnitude drift
between periods) — named as "THE key trap" in 15-CONTEXT.md. The test suite
(`tests/test_cohort_denominator.py`) asserts disjointness in both directions: a
period-drift spec fires only MET-020, and a cohort mix-shift spec fires only MET-021,
with no double-report on either fixture.

**When to use:** Any new check placed near a sibling check with a similar-sounding surface (same finding family, adjacent code number, related domain concept like "denominator") — write an explicit bidirectional fixture test proving each fixture fires only its own code, not just that each code fires on its own fixture.
**Source:** 15-CONTEXT.md, 15-02-SUMMARY.md

---

### Extend the canonical good fixture additively and prove silence at every gate threshold
`examples/good-ANALYSIS-SPEC.yaml` was extended (never replaced) with a `cohort_grain`
label, a `cuped:` block declaring `pre_experiment`, a well-behaved
`cohort_comparisons[]` entry (equal rates AND `reweighted: true` — belt-and-suspenders),
and a monotone `funnel_steps[]`. Every new key stays top-level under
`results`/`metrics`/`design`, never inside `validity_frame.exclusions`, so
`frame_digest` is unchanged. `tests/test_good_fixture_phase15.py` asserts the extended
fixture passes every gate at every threshold (plan/execute/verify/ship, exit_code 0) and
that both new codes stay silent on it, while the pre-existing golden suite
(`test_causal_verb_golden`) stays green — proving the fixture was extended, not
replaced.

**When to use:** Any phase adding new declaration-surface fields to the spec schema — extend the single canonical good fixture in place, keep new keys out of any strict-key/digest-sensitive block, and assert zero new findings at every gate threshold rather than trusting that "the fixture still passes" implies silence on the new checks specifically.
**Source:** 15-CONTEXT.md, 15-05-SUMMARY.md, 15-05-PLAN.md

---

## Surprises

### The full suite, not the plan's own narrower verification, was what caught the stale byte anchor
Plans 15-02 and 15-04 each ran their own scoped verification (unit tests, AST checks,
`git status --porcelain` on specific paths) and reported clean. The cross-phase
byte-anchor staleness in `dsx/checks/design.py` only surfaced when the full suite
(`sh scripts/check.sh`) was re-run at S4-4 code review — a check that was explicitly
deferred from S4-3 to that later unit. Had the full suite not been re-run independently
at review time, the stale anchor would have shipped.

**Impact:** Confirms the value of re-running the full gate suite at a dedicated review checkpoint rather than trusting per-plan scoped verification to compose correctly across plans that touch the same anchored file from different phases.
**Source:** REVIEW.md

---

### REQ-P15-04's "PARTIAL" status was pre-consented, not a review-time surprise to the operator
Unusually, the partial satisfaction of REQ-P15-04 was not discovered during execution —
it was decided and operator-consented (via answered HQ-8) at the S4-1 discuss stage,
before any plan was written, and then carried forward faithfully through 15-02's
summary, the S4-4 verification, and the S4-4 code review, each restating the same
"changing-denominator shipped; survivorship deferred to §6.5" framing without ever
softening it into a bare checkmark.

**Impact:** Shows the loud-partial-status discipline held across the whole phase lifecycle (context → plan → summary → verification → review) rather than degrading at any single handoff.
**Source:** 15-CONTEXT.md, 15-02-SUMMARY.md, VERIFICATION.md, REVIEW.md

---
