---
phase: 09-monitoring-discipline-symmetric-dsx-par
verified: 2026-08-13T00:30:00Z
status: gaps_found
score: 5/7 must-haves verified
behavior_unverified: 0
overrides_applied: 0
gaps:
  - truth: "A committed audit (references/paradigm-symmetry.md) accurately records the cheapest dishonest satisfaction path for each half of the DSX-PAR-010/DSX-PAR-011 pair (ROADMAP Phase 9 Success Criterion 5, REQ-P9-06)."
    status: failed
    reason: >
      dsx/spec.py::is_blank() has no branch for int/float/bool — it returns
      False (i.e. "not blank" / "declared") for any numeric or boolean value,
      including 0, 0.0 and False. dsx/frame/paradigm.py::_blank_clearing_declarations
      reuses is_blank() unmodified as the sole predicate deciding whether
      DSX-PAR-010/DSX-PAR-011 fire. Consequence, confirmed by direct execution:
      declaring `inference.alpha_spending: 0`, `inference.prior_justification: false`,
      or the shared `inference.threshold_calibration: 0` clears the CRITICAL pair
      with literally zero declared content, on both paradigms equally. This is
      cheaper than the "one free-text declaration" references/paradigm-symmetry.md
      documents (lines 67-71) as the cheapest dishonest fix — so the committed
      audit's own headline claim is inaccurate, even though the escape is equally
      cheap on both paradigms (D-12 symmetry itself is not broken).
    artifacts:
      - path: "dsx/spec.py:369-376"
        issue: "is_blank() falls through to `return False` for int/float/bool, so a bare 0 or False is never treated as blank."
      - path: "dsx/frame/paradigm.py:94-104"
        issue: "_blank_clearing_declarations() delegates entirely to is_blank(), inheriting the numeric/boolean gap for the three clearing declarations (alpha_spending, prior_justification, threshold_calibration)."
      - path: "references/paradigm-symmetry.md:67-82"
        issue: "Documents 'type any non-blank string' as the cheapest dishonest fix; does not mention or account for the cheaper bare-0/False escape."
    missing:
      - "Either restrict the three clearing declarations to non-blank *strings* specifically (dsx/frame/paradigm.py::_blank_clearing_declarations, or a shared dsx.spec.is_blank_text() helper), or amend references/paradigm-symmetry.md to document the actual cheapest path and make an explicit, reasoned decision to accept it."
      - "A regression test pinning that a bare 0/0.0/False value in any of the three clearing declarations does NOT clear DSX-PAR-010/DSX-PAR-011, once the fix lands."
  - truth: "DSX-PAR-011's operator-facing output (the shipped finding text and the known-bad fixture's own comment) attributes the 1/(K+1) bound the same way the docstring and the audit document do — never directly to 'Theorem 1' (ROADMAP Phase 9 Success Criterion 3)."
    status: failed
    reason: >
      dsx/frame/paradigm.py's own docstring (lines 149-155) and
      references/paradigm-symmetry.md (lines 138-141) both explicitly state that
      Theorem 1 licenses the prior-averaged bound under optional stopping but does
      NOT itself state 1/(K+1) — the bound is unnumbered prose at Section 3.2, and
      "citing Theorem 1 alone for the number 1/(K+1) would be a locator error."
      Despite that, the actual `detail=` text DSX-PAR-011 emits at gate time
      (dsx/frame/paradigm.py:244-253, confirmed by direct execution) reads "Under
      the prior-averaged formulation (Deng, Lu & Chen 2016, Theorem 1), the risk
      of false discovery ... is bounded by 1/(K+1)" — committing exactly the
      locator error the same function's docstring warns against three sentences
      earlier. The known-bad fixture
      examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml (lines
      29-31) repeats the identical error: "Deng, Lu & Chen (2016) Theorem 1 caps
      the false-discovery risk of stopping at a posterior-odds threshold K at
      1/(K+1)." The paired POSTMORTEM.md and references/paradigm-symmetry.md get
      the distinction right, so this is an internal self-contradiction across the
      shipped artifact set, not a matter of an unclear source. This directly
      undermines the intent of Success Criterion 3 ("so a mismatch reads as a
      formulation question in five minutes, not an implementation bug for a day")
      — a plausible-but-wrong citation in the operator-facing text is worse than
      no citation, because it reads as authoritative.
    artifacts:
      - path: "dsx/frame/paradigm.py:244-253"
        issue: "DSX-PAR-011's shipped detail= text ties the 1/(K+1) number to 'Theorem 1' in one clause."
      - path: "examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml:29-31"
        issue: "Fixture's own 'Formulation note' comment attributes the 1/(K+1) cap directly to Theorem 1."
    missing:
      - "Rephrase dsx/frame/paradigm.py's DSX-PAR-011 detail= string to attribute the number the same way the docstring/audit do (Theorem 1 licenses; unnumbered prose / Section 3.2 states the bound) — the reviewer's suggested fix (09-REVIEW.md CR-02) does this."
      - "Correct the identical wording in examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml's Formulation note comment to match the POSTMORTEM.md's already-correct phrasing."
human_verification:
  - test: "Confirm the DSX-PAR-002 scope decision (membership-free presence/requiredness only, closed-vocabulary membership left to the pre-existing DSX-SPEC-085) is an acceptable reading of ROADMAP Success Criterion 4's wording ('DSX-PAR-002 validates paradigm_justification against the closed vocabulary')."
    expected: "A human decision on whether the literal roadmap wording is satisfied by the two-code split, or whether DSX-PAR-002 itself should also test membership."
    why_human: "This is a values/scope judgment about roadmap wording versus shipped design, not a code defect — independent verification (see narrative below) found no input where the combined system lets a bogus paradigm_justification pass silently; DSX-SPEC-085 always catches a non-blank, non-member justification, regardless of design.peeking_policy or whether DSX-PAR-002 also fires. The split is deliberately documented in dsx/frame/paradigm.py's and DSX-PAR-002's own docstrings to avoid double-firing (D-08)."
---

# Phase 9: Monitoring discipline, symmetric (`DSX-PAR-*`) Verification Report

**Phase Goal:** Uncontrolled continuous monitoring blocks under both paradigms, neither half can be
escaped by retyping `paradigm`, and neither half is cheaper to satisfy dishonestly than the other.
Three checks, symmetric by construction.

**Verified:** 2026-08-13T00:30:00Z
**Status:** gaps_found
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths (ROADMAP Success Criteria 1–5)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | A frequentist spec declaring `uncontrolled_continuous` with no `alpha_spending`/sequential method exits `1` at `dsx gate plan` naming `DSX-PAR-010`, reusing `inflation_from_peeking()`, `DSX-EXP-060` unchanged | ✓ VERIFIED | Ran `python3 -m dsx gate plan --spec examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml --json`: exit `1`, CRITICAL codes = `['DSX-PAR-010']`. `git diff HEAD~20 -- dsx/checks/design.py dsx/cli.py` empty. Disjointness across every `PEEKING_POLICIES` member confirmed by direct execution (only `uncontrolled_continuous` fires `DSX-PAR-010`; only `fixed_horizon`/empty fire `DSX-EXP-060`, never both). `dsx.mathx.inflation_from_peeking()` is the only inflation table (grep confirms no second table). |
| 2 | `bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` exits `1` naming `DSX-PAR-011`; a test asserts `1/(K+1)` at `K=19` = `0.05`, traced to Deng, Lu & Chen (2016), distinct from Ville's `1/k` (`≈0.0526`) | ✓ VERIFIED | Ran the fixture through the real gate: exit `1`, CRITICAL codes = `['DSX-PAR-011']`. `tests/test_par_monitoring_simulation.py::test_boundary_arithmetic_is_exact_in_binary64` and `::test_villes_inequality_is_a_different_bound_over_a_different_event` both pass (ran directly). `tests/test_dsx.py::TestPhase9MonitoringDiscipline::test_dsx_par_011_reference_value_boundary_arithmetic` passes. |
| 3 | `DSX-PAR-011`'s docstring states it asserts prior-averaged, not point-null/LIL, and the fixture comments the theorem its number traces to, in a way that reads as a formulation question, not an implementation bug | ✗ FAILED | Docstring itself (dsx/frame/paradigm.py:149-173) is correct and precise. But the **shipped, operator-facing `detail=` text** (lines 244-253) and the **known-bad fixture's own comment** (bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml:29-31) both attribute the `1/(K+1)` bound directly to "Theorem 1" — the exact locator error the docstring warns against three sentences earlier. Confirmed by direct execution and file read. See gap below. |
| 4 | Switching `paradigm` cannot buy a pass in either direction (asserted by test both ways); `DSX-PAR-002` validates `paradigm_justification` against the closed vocabulary, no reason ranked above another | ⚠ VERIFIED with a documented scope note | `test_retyping_frequentist_fixture_to_bayesian_yields_dsx_par_011_not_010` and the reverse both pass (ran directly). `DSX-PAR-002` itself is membership-free (requiredness only); `DSX-SPEC-085` owns membership. Independently verified (not just trusting the review) that no input lets a bogus, non-blank `paradigm_justification` pass silently — `DSX-SPEC-085` fires unconditionally whenever `inference:` is non-empty and the field is non-blank and non-member, regardless of `DSX-PAR-002`'s trigger conditions. The 14-case cross product (`PARADIGM_JUSTIFICATIONS` × `PARADIGMS`) is a genuine runtime iteration, not hard-coded, and passes. Routed to human verification below purely as a wording-vs-scope judgment call, not a functional gap. |
| 5 | Both codes ship together at identical severity; a committed audit records the cheapest dishonest satisfaction path for each half; the simulation lives under `tests/`, seeded, reproducible, never on the gate path | ✗ FAILED | Atomicity confirmed: both codes shipped in the single commit `df20ef6`, both severity `CRITICAL` (confirmed via `references/finding-codes.md` and direct `check()` call). Simulation requirement fully met: `tests/test_par_monitoring_simulation.py` is seeded (`random.Random(_SEED)`), reproducible (`test_determinism_same_seed_same_summary_statistic` passes), and an AST-walking test (`test_no_module_under_dsx_imports_from_tests`) mechanically proves no `dsx/` module imports `tests`. **But** the committed audit's "cheapest dishonest path" claim is not accurate — see gap below (`is_blank()` numeric/boolean gap). |

**Score:** 5/7 must-haves verified (2 FAILED — see gaps below; both scoped to Success Criteria 3 and 5)

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `dsx/frame/paradigm.py::_MONITORING_DISCIPLINE` | dict keyed by every `PARADIGMS` member | ✓ VERIFIED | `set(_MONITORING_DISCIPLINE) == set(PARADIGMS)` confirmed by direct execution: `True` |
| `dsx/frame/paradigm.py::_check_monitoring_discipline` | emits DSX-PAR-010/011 at CRITICAL | ✓ VERIFIED | Confirmed via real gate runs against both known-bad fixtures |
| `dsx/frame/paradigm.py::_blank_clearing_declarations` | shared clearing predicate | ✓ VERIFIED, but see gap 1 | Exists, shared, but inherits `is_blank()`'s numeric/boolean gap |
| `dsx/frame/paradigm.py::_check_paradigm_justification` | DSX-PAR-002 requiredness, HIGH | ✓ VERIFIED | Confirmed via direct execution and `references/finding-codes.md` |
| `references/paradigm-symmetry.md` | committed symmetry audit | ✓ EXISTS, ⚠ inaccurate in one respect | See gap 1 |
| `tests/test_par_monitoring_simulation.py` | seeded, reproducible, off gate path | ✓ VERIFIED | 7/7 tests pass when run directly; AST-scanner test proves no `dsx/` import |
| `references/finding-codes.md` rows for `DSX-PAR-002`/`010`/`011` | non-placeholder, correct severities | ✓ VERIFIED | `DSX-PAR-002` HIGH, `DSX-PAR-010`/`011` CRITICAL, both present |

### Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| `dsx/frame/paradigm.py` | `dsx/mathx.py::inflation_from_peeking` | `from ..mathx import inflation_from_peeking` | ✓ WIRED | Confirmed by import and by the emitted `DSX-PAR-010` detail text carrying the function's own computed values |
| `_MONITORING_DISCIPLINE` | `dsx.spec.PARADIGMS` | set-equality contract test | ✓ WIRED | `test_monitoring_discipline_map_is_symmetric_across_paradigms` passes |
| `_NOT_SHIPPED` | `dsx/frame/paradigm.py::check()` | removal of `DSX-PAR-010`/`011`/`002` entries | ✓ WIRED | `_NOT_SHIPPED` now contains only `DSX-INT-`, `DSX-PRE-`, `DSX-ADM-` — confirmed by direct inspection |
| `tests/test_par_monitoring_simulation.py` | `dsx/` (gate path) | AST import scanner | ✓ NOT_WIRED (by design — this is the correct/required state per REQ-P9-07) | `test_no_module_under_dsx_imports_from_tests` passes |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Frequentist known-bad fixture blocks `dsx gate plan` naming `DSX-PAR-010` | `python3 -m dsx gate plan --spec examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml --json` | exit 1, CRITICAL=`['DSX-PAR-010']` | ✓ PASS |
| Bayesian known-bad fixture blocks `dsx gate plan` naming `DSX-PAR-011` | `python3 -m dsx gate plan --spec examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml --json` | exit 1, CRITICAL=`['DSX-PAR-011']` | ✓ PASS |
| Good fixture passes at all four gate points | `python3 -m dsx gate {plan,execute,verify,ship} --spec examples/good-ANALYSIS-SPEC.yaml` | all exit 0 | ✓ PASS |
| `dsx audit --json` is deterministic | two consecutive runs on `examples/bad-ANALYSIS-SPEC.yaml` | byte-identical stdout and stderr | ✓ PASS |
| `is_blank(0)`/`is_blank(False)` bug reproduces (CR-01) | direct `paradigm.check()` call with `alpha_spending: 0` / `prior_justification: false` | only `DSX-PAR-001`/`DSX-PAR-002` fire — `DSX-PAR-010`/`011` cleared | ✗ FAIL (confirms gap 1) |
| Full test suite | `sh scripts/check.sh` | 457 tests, `OK (skipped=2)`, catalogue current, gate contract and determinism pass | ✓ PASS |

### Probe Execution

Not applicable — no `scripts/*/tests/probe-*.sh` convention in this project; verification was performed directly against the real `dsx` gate CLI and test suite (see Behavioral Spot-Checks above).

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|---|---|---|---|---|
| REQ-P9-01 | 09-03 | `DSX-PAR-010` blocks frequentist uncontrolled monitoring, reuses `inflation_from_peeking()` | ✓ SATISFIED | Gate run + `git diff` empty on `dsx/checks/design.py` |
| REQ-P9-02 | 09-03 | `DSX-PAR-011` blocks Bayesian uncontrolled monitoring, asserts `1/(K+1)` bound | ✓ SATISFIED | Gate run + `tests/test_par_monitoring_simulation.py` boundary test |
| REQ-P9-03 | 09-03 | Docstring states prior-averaged not point-null/LIL; fixture traces theorem | ✗ BLOCKED | Docstring correct; fixture comment and shipped finding text misattribute the bound to Theorem 1 — see gap 2 |
| REQ-P9-04 | 09-05 | `DSX-PAR-002` validates `paradigm_justification` against closed vocabulary, symmetric | ? NEEDS HUMAN (scope) | Functionally complete via `DSX-PAR-002` + `DSX-SPEC-085` split; wording-vs-scope judgment routed to human verification |
| REQ-P9-05 | 09-03 | Neither code escaped by retyping `paradigm`, both directions | ✓ SATISFIED | Both retype tests pass |
| REQ-P9-06 | 09-01/09-04 | Documented audit records cheapest dishonest path per half | ✗ BLOCKED | Audit's claim is inaccurate — see gap 1 |
| REQ-P9-07 | 09-02 | Simulation seeded, reproducible, never on gate path | ✓ SATISFIED | 7/7 simulation tests pass; AST-scanner proves isolation |

No orphaned requirements — `REQUIREMENTS.md` lists all seven `REQ-P9-*` IDs and each is claimed by exactly one plan's frontmatter.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---|---|---|---|
| `dsx/spec.py` | 369-376 | `is_blank()` has no numeric/boolean branch | 🛑 Blocker (in this phase's load-bearing usage) | Enables gap 1 — see `09-REVIEW.md` CR-01 |
| `dsx/frame/paradigm.py` | 244-253 | Finding `detail=` text misattributes a citation locator | 🛑 Blocker | See gap 2 — `09-REVIEW.md` CR-02 |
| `dsx/frame/paradigm.py` | 206 | `as_number(get(spec, "design.alpha")) or 0.05` — falsy-`or` default silently replaces a declared `alpha: 0` | ⚠ Warning | `09-REVIEW.md` WR-01; does not affect any ROADMAP Success Criterion since the two reference-value anchors (0.142/0.248) are unaffected — narrow edge case |
| `references/finding-codes.md` | 354 | Catalogue generator drops one of `DSX-PAR-002`'s two distinct trigger messages (last-write-wins dedup) | ⚠ Warning | `09-REVIEW.md` WR-02; documentation completeness only, `--check` still exits 0 |
| `dsx/frame/paradigm.py` | 493-503 | `DSX-PAR-001`'s counterfactual hard-codes `other_paradigms[0]`, correct only while `PARADIGMS` has exactly 2 members | ⚠ Warning | `09-REVIEW.md` WR-03; latent, not exercised today |

No `TBD`/`FIXME`/`XXX` unresolved debt markers found in the phase's modified files.

### Human Verification Required

### 1. `DSX-PAR-002` scope versus ROADMAP Success Criterion 4's literal wording

**Test:** Read ROADMAP.md Phase 9 Success Criterion 4 ("`DSX-PAR-002` validates `paradigm_justification` against the closed vocabulary with no reason ranked above another") against the shipped split, where `DSX-PAR-002` is deliberately membership-free (presence/requiredness only) and `DSX-SPEC-085` (pre-existing, Phase 6) owns closed-vocabulary membership.
**Expected:** A decision on whether the roadmap wording is satisfied by the two-code split (the substantive property — no bogus justification passes, no reason ranked above another — holds end to end) or whether the roadmap wording should be read literally and `DSX-PAR-002` itself needs a membership check.
**Why human:** This is a values/scope call about how loosely to read the roadmap's prose versus the plan's own explicit, reasoned design decision (documented in `09-05-PLAN.md`'s `<resolved_open_questions>` and the function's own docstring) to avoid double-firing (D-08). Independent verification found no input where the combined system lets a bogus, non-blank `paradigm_justification` pass silently.

## Gaps Summary

Two CRITICAL-severity code-review findings (`09-REVIEW.md` CR-01, CR-02) were independently
reproduced against the live codebase (not merely trusted from the review) and both bear directly on
specific ROADMAP Phase 9 Success Criteria:

1. **CR-01** (`is_blank()`'s numeric/boolean gap) undermines Success Criterion 5 / REQ-P9-06. The
   committed symmetry audit (`references/paradigm-symmetry.md`) documents "type any non-blank string"
   as the cheapest dishonest escape from `DSX-PAR-010`/`DSX-PAR-011`. In fact a bare `0`, `0.0`, or
   `False` in any of the three clearing declarations (`alpha_spending`, `prior_justification`,
   `threshold_calibration`) clears the CRITICAL pair with zero declared content — cheaper than what
   the audit records, and undocumented. This does **not** break the D-12 cost-symmetry property itself
   (the escape is equally cheap on both paradigms), but it does mean the audit's own headline claim
   about the cheapest path is factually stale/wrong, which is what Success Criterion 5 specifically
   requires it to get right.

2. **CR-02** (Theorem 1 misattribution) undermines Success Criterion 3. The module's own docstring and
   the committed audit correctly distinguish "Theorem 1 licenses the bound under optional stopping"
   from "the bound `1/(K+1)` itself is unnumbered prose at Section 3.2" — and explicitly warn that
   citing Theorem 1 alone for the number would be a locator error. Despite that warning appearing three
   sentences earlier in the same function, the actual finding text `DSX-PAR-011` emits at gate time,
   and the known-bad fixture's own comment, both commit exactly that locator error. This is an internal
   self-contradiction in the shipped, operator-facing artifacts (the paired POSTMORTEM.md gets it
   right), directly undermining Success Criterion 3's stated purpose of making a mismatch "read as a
   formulation question in five minutes, not an implementation bug for a day."

Both gaps are narrow, mechanical fixes (rewording, and either a stricter blank predicate or an honest
audit update) — they do not require re-architecting the symmetric pair, which is otherwise genuinely
well-built: the atomicity requirement (D-12), both-directions retype tests, the 14-case
`DSX-PAR-002` symmetry proof, the off-gate-path seeded simulation, and the full 457-test suite (`sh
scripts/check.sh`) all independently verify clean. Neither gap is a regression risk for a later phase —
both are isolated to this phase's own files.

---

_Verified: 2026-08-13T00:30:00Z_
_Verifier: Claude (gsd-verifier)_
