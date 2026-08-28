---
phase: 09-monitoring-discipline-symmetric-dsx-par
verified: 2026-08-13T15:00:00Z
status: passed
score: 7/7 must-haves verified
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: 5/7
  gaps_closed:
    - "A committed audit (references/paradigm-symmetry.md) accurately records the cheapest dishonest satisfaction path for each half of the DSX-PAR-010/DSX-PAR-011 pair (ROADMAP Success Criterion 5, REQ-P9-06)."
    - "DSX-PAR-011's operator-facing output (the shipped finding text and the known-bad fixture's own comment) attributes the 1/(K+1) bound the same way the docstring and the audit document do — never directly to 'Theorem 1' (ROADMAP Success Criterion 3)."
  gaps_remaining: []
  regressions: []
human_verification:
  - test: "Confirm the DSX-PAR-002 scope decision (membership-free presence/requiredness only, closed-vocabulary membership left to the pre-existing DSX-SPEC-085) is an acceptable reading of ROADMAP Success Criterion 4's wording ('DSX-PAR-002 validates paradigm_justification against the closed vocabulary')."
    expected: "A human decision on whether the literal roadmap wording is satisfied by the two-code split, or whether DSX-PAR-002 itself should also test membership."
    why_human: "This is a values/scope judgment about roadmap wording versus shipped design, not a code defect — carried forward unchanged from the initial verification. Re-confirmed this cycle: git diff 4c983fa..HEAD shows zero changes to DSX-PAR-002's check logic, so nothing about this item's facts moved during gap closure. Independent verification (this cycle and the last) found no input where the combined system lets a bogus, non-blank paradigm_justification pass silently — DSX-SPEC-085 always catches it."
    result: pass
    decision: accept the split
    decided: 2026-08-13T15:25:00Z
    notes: "Roadmap wording reads as intent, not an implementation assignment. ROADMAP SC 4 and REQ-P9-04 amended to name both codes."
---

# Phase 9: Monitoring discipline, symmetric (`DSX-PAR-*`) Verification Report

**Phase Goal:** Uncontrolled continuous monitoring blocks under both paradigms, neither half can be
escaped by retyping `paradigm`, and neither half is cheaper to satisfy dishonestly than the other.
Three checks, symmetric by construction — deliberately not "the Bayesian phase".

**Verified:** 2026-08-13T15:00:00Z
**Status:** passed
**Re-verification:** Yes — after gap closure (plans 09-06, 09-07)

> **Status reconciled 2026-08-24 (loop S0-7 / audit GAP-PROC-04):** This header originally read `human_needed`. The single human-verification item (the `DSX-PAR-002` scope question) was resolved at UAT on 2026-08-13 — decision **accept the split**, recorded inline in the frontmatter (`result: pass`, `decided: 2026-08-13T15:25:00Z`) and in the Gaps Summary below ("Frontmatter status is now `passed`"). Header reconciled to `passed` so frontmatter and body agree.

## What changed since the prior report

Two gap-closure plans executed since the initial verification (`gaps_found`, 5/7):

- **09-06** added `dsx/spec.py::is_blank_text` (a new, separately-named text-only blank
  predicate; `is_blank` itself left byte-identical — confirmed by `git diff 4c983fa..HEAD --
  dsx/spec.py` showing zero change inside `is_blank`'s body) and rerouted
  `dsx/frame/paradigm.py::_blank_clearing_declarations` through it. This closes Gap 1
  (REQ-P9-06 / Success Criterion 5).
- **09-07** rewrote `DSX-PAR-011`'s emitted `detail=` string and the known-bad Bayesian
  fixture's Formulation note so neither pairs "Theorem 1" with the `1/(K+1)` number in one
  clause. This closes Gap 2 (REQ-P9-03 / Success Criterion 3).

Both gaps were re-verified this cycle by direct execution against the live code — not by
reading the plans, the summaries, or `09-REVIEW.md`'s own "CLOSED" verdicts, all of which were
corroborated rather than trusted. Additionally, per this re-verification's own instructions, the
five previously-passing truths were re-checked for regression, since both gap-closure plans
touched the two load-bearing files (`dsx/spec.py`, `dsx/frame/paradigm.py`) for the whole phase.
No regression found.

## Goal Achievement

### Observable Truths (ROADMAP Success Criteria 1–5)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | A frequentist spec declaring `uncontrolled_continuous` with no `alpha_spending`/sequential method exits `1` at `dsx gate plan` naming `DSX-PAR-010`, reusing `inflation_from_peeking()`, `DSX-EXP-060` unchanged | ✓ VERIFIED (regression-checked) | Re-ran `python3 -m dsx gate plan --spec examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml --json`: exit `1`, CRITICAL codes = `['DSX-PAR-010']`, `inflated_alpha_at_5_looks=0.142`/`at_20_looks=0.248` unchanged. `git diff 4c983fa..HEAD --stat -- dsx/checks/design.py dsx/cli.py` is empty — neither file touched by gap closure. |
| 2 | `bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` exits `1` naming `DSX-PAR-011`; a test asserts `1/(K+1)` at `K=19` = `0.05`, traced to Deng, Lu & Chen (2016), distinct from Ville's `1/k` (`≈0.0526`) | ✓ VERIFIED (regression-checked) | Re-ran the fixture: exit `1`, CRITICAL codes = `['DSX-PAR-011']`. `python3 -m unittest tests.test_dsx.TestPhase9MonitoringDiscipline -v`: 24/24 pass, including `test_dsx_par_011_reference_value_boundary_arithmetic`. |
| 3 | `DSX-PAR-011`'s docstring states it asserts prior-averaged, not point-null/LIL, and the fixture comments the theorem its number traces to, in a way that reads as a formulation question, not an implementation bug | ✓ VERIFIED (gap closed) | Read the **live emitted** `detail=` text by direct execution (not the source line): `"...Under the prior-averaged formulation (Deng, Lu & Chen 2016), the risk of false discovery ... is bounded by 1/(K+1) = 1/20 = 0.05 at K = 19 ... Theorem 1 licenses that bound under optional stopping with known prior odds; the bound itself is unnumbered prose following Theorem 1 and again in the paper's Section 3.2."` — `'2016, Theorem 1'` (the locator error) is absent; `'Theorem 1 licenses'`, `'unnumbered prose'`, `'Section 3.2'` are present. Fixture's Formulation note re-read directly: contains `'locator error'`, `'Section 3.2'`, `'unnumbered prose'`; does not contain `'2016, Theorem 1'` or `'Theorem 1 caps'`. `test_dsx_par_011_detail_attributes_the_bound_without_a_locator_error`, `test_no_corpus_file_commits_the_theorem_1_locator_error` and `test_bayesian_fixture_states_the_corrected_attribution` all pass. |
| 4 | Switching `paradigm` cannot buy a pass in either direction (asserted by test both ways); `DSX-PAR-002` validates `paradigm_justification` against the closed vocabulary, no reason ranked above another | ⚠ VERIFIED with a documented scope note (unchanged) | `test_retyping_frequentist_fixture_to_bayesian_yields_dsx_par_011_not_010` and the reverse both re-ran and pass. `git diff 4c983fa..HEAD -- dsx/frame/paradigm.py` shows no hunk touching `_check_paradigm_justification` (`DSX-PAR-002`'s logic) — the scope split (membership-free `DSX-PAR-002` + closed-vocabulary `DSX-SPEC-085`) is byte-for-byte unchanged from the initial verification. Routed to human verification below, carried forward unchanged — not a functional gap. |
| 5 | Both codes ship together at identical severity; a committed audit records the cheapest dishonest satisfaction path for each half; the simulation lives under `tests/`, seeded, reproducible, never on the gate path | ✓ VERIFIED (gap closed) | Both codes still `CRITICAL` (confirmed via `finding-codes.md` and direct `check()` calls). **Audit accuracy re-verified by direct execution**, not by reading the audit text alone: ran a 48-case matrix (both paradigms × 3 clearing fields × 8 non-text values — `0`, `0.0`, `False`, `True`, `[]`, `{}`, `[0]`, `{'a':1}`) against the live `dsx.frame.paradigm.check()` — the CRITICAL pair fired in **all 48 cases**, i.e. the previously-cheaper bare-`0`/`False`/container escape no longer clears either half. A genuine non-blank string (including the literal `"0"`) still clears, confirming the audit's "one free-text declaration" floor is now actually the cheapest path. `references/paradigm-symmetry.md`'s new "What does not clear either half" section, read directly, states this history and the closed rule accurately. Simulation requirement unchanged and re-confirmed: `tests/test_par_monitoring_simulation.py` still seeded/reproducible/off-gate-path (not touched by gap closure — outside the `4c983fa..HEAD` diff). |

**Score:** 5/5 ROADMAP Success Criteria verified; both prior FAILED truths (3 and 5) now VERIFIED. Success Criterion 4 accepted at UAT 2026-08-13 (split stands; wording amended).

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `dsx/spec.py::is_blank_text` | new text-only blank predicate | ✓ VERIFIED | Exists, directly below `is_blank`; confirmed by direct import and execution over the full type domain (11 blank cases, 2 non-blank cases) matching the plan's `must_haves.truths` exactly. |
| `dsx/spec.py::is_blank` | unchanged for all other call sites | ✓ VERIFIED | `git diff 4c983fa..HEAD -- dsx/spec.py` shows zero change inside `is_blank`'s body; direct execution confirms `is_blank(0)==is_blank(0.0)==is_blank(False)==is_blank(True)==False`, unchanged. |
| `dsx/frame/paradigm.py::_blank_clearing_declarations` | routed through `is_blank_text` | ✓ VERIFIED | Source confirms single call to `is_blank_text`; behavior confirmed by the 48-case matrix above. |
| `dsx/frame/paradigm.py::_MONITORING_DISCIPLINE` | dict keyed by every `PARADIGMS` member, D-12 symmetric | ✓ VERIFIED | `set(_MONITORING_DISCIPLINE) == set(PARADIGMS)` re-confirmed `True`; both rows carry 2-tuple clearing-field lists, same shape. |
| `references/paradigm-symmetry.md` | committed symmetry audit, now accurate | ✓ VERIFIED (gap closed) | New "What does not clear either half" section read directly; states the closed hole, the pinning test, and the corrected cheapest-path claim. |
| `dsx/frame/paradigm.py::DSX-PAR-011 detail=` | attribution matches docstring/audit, no locator error | ✓ VERIFIED (gap closed) | Live emitted text read directly (see truth 3 above). |
| `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` Formulation note | matches corrected attribution | ✓ VERIFIED (gap closed) | Read directly (see truth 3 above); YAML keys/values unchanged (`git diff` — comment lines only, matches SUMMARY claim). |
| `tests/test_dsx.py::TestPhase9MonitoringDiscipline` | full type-domain + attribution regression coverage | ✓ VERIFIED | 24/24 tests pass when run directly (was 18 pre-gap-closure). |
| `tests/test_known_bad_corpus.py::_RETIRED_LOCATOR_ERRORS` + guards | prevents the locator error returning | ✓ VERIFIED | 20/20 tests pass; guard tuple confirmed present and applied corpus-wide. |
| `tests/test_par_monitoring_simulation.py` | seeded, reproducible, off gate path | ✓ VERIFIED (unchanged) | Outside the gap-closure diff range; not re-run individually this cycle since `sh scripts/check.sh`'s 526-test pass includes it and neither touched file could affect it. |

### Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| `dsx/frame/paradigm.py::_blank_clearing_declarations` | `dsx/spec.py::is_blank_text` | direct call | ✓ WIRED | Single call site; confirmed by source read and by the 48-case behavioral matrix. |
| `is_blank_text` | every other module | must not leak | ✓ CONFIRMED ISOLATED | `grep -rn "is_blank_text" dsx/` returns matches only in `dsx/spec.py` (definition) and `dsx/frame/paradigm.py` (one use) — no other module imports or calls it. |
| `references/paradigm-symmetry.md` | executed behavior of `dsx.frame.paradigm.check` | asserted by test, not inspection | ✓ WIRED | `test_paradigm_symmetry_audit_enumerates_both_halves` passes; audit's claims independently re-verified by direct execution (48-case matrix), not merely by reading the test. |
| the emitted `DSX-PAR-011` `detail` | the module's own docstring / audit / POSTMORTEM.md attribution | same wording, same "licenses" verb | ✓ WIRED | Live `detail=` text read directly and compared substring-for-substring against the required phrases. |
| `dsx/frame/paradigm.py` | `dsx/mathx.py::inflation_from_peeking` | import | ✓ WIRED (unchanged) | Untouched by gap closure; re-confirmed via live gate run showing `0.142`/`0.248` anchors. |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| 48-case bare-`0`/`False`/container escape matrix (both paradigms × 3 fields × 8 non-text values) | direct `paradigm.check()` calls, this session | CRITICAL pair fires on all 48 | ✓ PASS |
| Non-blank string (incl. literal `"0"`) still clears | direct `paradigm.check()` calls, this session | clears both halves as expected | ✓ PASS |
| `is_blank` unaffected for numeric/boolean scalars | direct `is_blank()` calls, this session | `False` for `0`, `0.0`, `False`, `True` — unchanged | ✓ PASS |
| Frequentist known-bad fixture blocks `dsx gate plan` naming `DSX-PAR-010` | `python3 -m dsx gate plan --spec examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml --json` | exit 1, CRITICAL=`['DSX-PAR-010']` | ✓ PASS |
| Bayesian known-bad fixture blocks `dsx gate plan` naming `DSX-PAR-011` | `python3 -m dsx gate plan --spec examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml --json` | exit 1, CRITICAL=`['DSX-PAR-011']` | ✓ PASS |
| Good fixture passes at all four gate points | `python3 -m dsx gate {plan,execute,verify,ship} --spec examples/good-ANALYSIS-SPEC.yaml` | all exit 0 | ✓ PASS |
| Live `DSX-PAR-011` `detail=` text no longer misattributes citation | direct `paradigm.check()` call, printed `detail` | locator error absent, correct attribution present | ✓ PASS |
| Known-bad fixture Formulation note corrected | direct file read + substring check | locator error absent, correct attribution present | ✓ PASS |
| `TestPhase9MonitoringDiscipline` full class | `python3 -m unittest tests.test_dsx.TestPhase9MonitoringDiscipline -v` | 24/24 pass | ✓ PASS |
| `test_known_bad_corpus` full module | `python3 -m unittest tests.test_known_bad_corpus -v` | 20/20 pass | ✓ PASS |
| Full test suite | `sh scripts/check.sh` | 526 tests, `OK (skipped=2)`, catalogue current, gate contract and determinism pass | ✓ PASS |

### Probe Execution

Not applicable — no `scripts/*/tests/probe-*.sh` convention in this project; verification was
performed directly against the real `dsx` gate CLI and test suite (see Behavioral Spot-Checks
above).

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|---|---|---|---|---|
| REQ-P9-01 | 09-03 | `DSX-PAR-010` blocks frequentist uncontrolled monitoring, reuses `inflation_from_peeking()` | ✓ SATISFIED | Gate run + `git diff` empty on `dsx/checks/design.py` |
| REQ-P9-02 | 09-03 | `DSX-PAR-011` blocks Bayesian uncontrolled monitoring, asserts `1/(K+1)` bound | ✓ SATISFIED | Gate run + boundary-arithmetic test pass |
| REQ-P9-03 | 09-03/09-07 | Docstring states prior-averaged not point-null/LIL; fixture traces theorem correctly | ✓ SATISFIED (gap closed by 09-07) | Live `detail=` text and fixture note both re-read directly; locator error absent, correct attribution present in both |
| REQ-P9-04 | 09-05 | `DSX-PAR-002` validates `paradigm_justification` against closed vocabulary, symmetric | ✓ SATISFIED (human: accept the split) | Functionally complete via `DSX-PAR-002` + `DSX-SPEC-085` split; UAT 2026-08-13 accepted D-08; ROADMAP SC 4 and REQ-P9-04 amended to name both codes |
| REQ-P9-05 | 09-03 | Neither code escaped by retyping `paradigm`, both directions | ✓ SATISFIED | Both retype tests re-ran and pass |
| REQ-P9-06 | 09-01/09-04/09-06 | Documented audit records cheapest dishonest path per half | ✓ SATISFIED (gap closed by 09-06) | 48-case matrix confirms no cheaper escape than one free-text declaration; audit text re-read directly and matches |
| REQ-P9-07 | 09-02 | Simulation seeded, reproducible, never on gate path | ✓ SATISFIED | Outside gap-closure diff; part of the passing 526-test suite |

No orphaned requirements — `REQUIREMENTS.md` lists all seven `REQ-P9-*` IDs and each is claimed
by exactly one plan's frontmatter (REQ-P9-01/02/03/05/06 are each claimed by more than one plan
across the phase's waves, which is expected — the gap-closure plans 09-06/09-07 re-claim the
requirements whose truths they complete).

**Note on `.planning/REQUIREMENTS.md`'s own status column:** at the time of this verification it
still shows REQ-P9-01 through REQ-P9-05 as "Pending" and only REQ-P9-06/07 as "Complete" (lines
210–216). This is stale tracking-file state, not a code gap — REQUIREMENTS.md is single-writer,
updated serially by the orchestrator after a phase is accepted, and this phase has not yet been
marked complete in that file. Every one of REQ-P9-01 through REQ-P9-05 is independently confirmed
satisfied above by direct execution against the live codebase, not by that table. Flagged here so
the orchestrator updates it when this phase closes.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---|---|---|---|
| `dsx/frame/paradigm.py` | 112-113 | `_blank_clearing_declarations`'s new docstring (added by 09-06) overstates what `is_blank()` used to say about *empty* lists/mappings — claims `is_blank` would call "any" list/mapping present, true only for non-empty ones (`is_blank([])`/`is_blank({})` were already `True`) | ⚠ Warning (internal comment only) | `09-REVIEW.md` WR-04, newly surfaced by this gap-closure round. Re-confirmed directly this cycle: `is_blank([]) == True`, `is_blank({}) == True`. Not operator-facing (it's a private-function docstring, never emitted in any finding text), does not affect any ROADMAP Success Criterion, and does not affect the correctness of the code it describes — `is_blank_text([])` and `is_blank_text({})` are both correctly `True` regardless of the docstring's imprecision. Judged not to defeat any Success Criterion. |

Carried forward from the initial verification, unfixed by design (per both gap-closure plans'
`<flagged_assumptions>`, judged not to reach any Success Criterion, and independently re-confirmed
here that neither has moved):

| File | Line | Pattern | Severity | Impact |
|---|---|---|---|---|
| `dsx/frame/paradigm.py` | ~206 | `as_number(get(spec, "design.alpha")) or 0.05` — falsy-`or` default silently replaces a declared `alpha: 0` | ⚠ Warning | `09-REVIEW.md` WR-01; narrow edge case, does not affect any Success Criterion |
| `references/finding-codes.md` | ~354 | Catalogue generator drops one of `DSX-PAR-002`'s two distinct trigger messages | ⚠ Warning | `09-REVIEW.md` WR-02; documentation completeness only |
| `dsx/frame/paradigm.py` | ~493-503 | `DSX-PAR-001`'s counterfactual hard-codes `other_paradigms[0]`, correct only while `PARADIGMS` has exactly 2 members | ⚠ Warning | `09-REVIEW.md` WR-03; latent, not exercised today |

No `TBD`/`FIXME`/`XXX` unresolved debt markers found in any file modified by this phase or its
gap-closure plans.

### Human Verification Required

Resolved at UAT 2026-08-13: accept the split. `DSX-PAR-002` stays membership-free;
`DSX-SPEC-085` owns closed-vocabulary membership. ROADMAP Success Criterion 4 and
REQ-P9-04 now name both codes.

### 1. `DSX-PAR-002` scope versus ROADMAP Success Criterion 4's literal wording

**Test:** Read ROADMAP.md Phase 9 Success Criterion 4 ("`DSX-PAR-002` validates
`paradigm_justification` against the closed vocabulary with no reason ranked above another")
against the shipped split, where `DSX-PAR-002` is deliberately membership-free
(presence/requiredness only) and `DSX-SPEC-085` (pre-existing, Phase 6) owns closed-vocabulary
membership.
**Expected:** A decision on whether the roadmap wording is satisfied by the two-code split (the
substantive property — no bogus justification passes, no reason ranked above another — holds end
to end) or whether the roadmap wording should be read literally and `DSX-PAR-002` itself needs a
membership check.
**Why human:** Carried forward unchanged from the initial verification — this is a values/scope
call about how loosely to read the roadmap's prose versus the plan's own explicit, reasoned design
decision (documented in `09-05-PLAN.md`'s `<resolved_open_questions>` and the function's own
docstring) to avoid double-firing (D-08). Re-confirmed this cycle that `DSX-PAR-002`'s check logic
is byte-identical to the version already judged against at the initial verification (`git diff
4c983fa..HEAD -- dsx/frame/paradigm.py` shows no hunk touching `_check_paradigm_justification`),
so nothing about the underlying facts changed — only the two independently-blocking gaps this
round closed. Independent verification (this cycle and the last) found no input where the
combined system lets a bogus, non-blank `paradigm_justification` pass silently.

## Gaps Summary

None. Both truths the initial verification (`5/7`) scored FAILED are now independently confirmed
CLOSED by direct execution against the live codebase this cycle — not by trusting
`09-REVIEW.md`'s own "CLOSED" verdicts or the plans' SUMMARY claims, both of which were
corroborated rather than inherited:

1. **Gap 1 (REQ-P9-06 / Success Criterion 5) — CLOSED.** A 48-case matrix (both paradigms × 3
   clearing fields × `0`, `0.0`, `False`, `True`, `[]`, `{}`, `[0]`, `{'a':1}`) run against the
   live `dsx.frame.paradigm.check()` this session confirms the CRITICAL pair fires in every case —
   the previously cheaper bare-value escape is closed. `is_blank()` is confirmed byte-identical by
   `git diff`, and `is_blank_text` is confirmed used nowhere outside `dsx/frame/paradigm.py`, so
   the fix carries no blast radius into the ~130+ other `is_blank()` call sites. The committed
   audit's "What does not clear either half" section, read directly, now states the closed rule
   accurately.

2. **Gap 2 (REQ-P9-03 / Success Criterion 3) — CLOSED.** The **live emitted** `DSX-PAR-011`
   `detail=` text, read by direct execution rather than from source, no longer pairs "2016" with
   "Theorem 1" in the clause that states the number; a separate sentence correctly attributes
   Theorem 1's licensing role. The known-bad fixture's Formulation note carries the identical
   corrected attribution. Both are pinned by new regression tests and a corpus-wide negative guard
   against the retired phrasing returning through any known-bad fixture.

Regression check on the five previously-passing truths (required because both gap-closure plans
touched the phase's two load-bearing files, `dsx/spec.py` and `dsx/frame/paradigm.py`): all five
re-verified clean by direct execution this cycle — the frequentist/Bayesian gate runs, the
retype-both-directions tests, the `DSX-PAR-002`/`DSX-SPEC-085` split (confirmed untouched by diff),
`_MONITORING_DISCIPLINE`'s D-12 symmetry, and the full 526-test suite (`sh scripts/check.sh`) all
pass. No regression found.

The remaining human-judgment scope question — `DSX-PAR-002` versus Success Criterion 4's
literal wording — was decided at UAT 2026-08-13: accept the split. Frontmatter status is
now `passed`. ROADMAP Success Criterion 4 and REQ-P9-04 were amended to name both codes.

One new, non-behavioral finding surfaced during gap closure (`09-REVIEW.md` WR-04: a docstring
added by 09-06 slightly overstates `is_blank()`'s pre-existing behavior for *empty* containers).
Independently confirmed this cycle (`is_blank([])`/`is_blank({})` are both already `True`, so the
docstring's "even though `is_blank` itself would call it present" is imprecise for that one case).
Fixed at UAT close: the docstring now distinguishes bare scalars (where `is_blank` and
`is_blank_text` diverge) from containers (empty already blank under `is_blank`; non-empty
blank only under `is_blank_text`). Internal-only; no behavioral change.

---

_Verified: 2026-08-13T15:00:00Z_
_Verifier: Claude (gsd-verifier)_
