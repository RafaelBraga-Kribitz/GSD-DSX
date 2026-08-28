---
phase: 09-monitoring-discipline-symmetric-dsx-par
plan: 04
subsystem: contract
tags: [dsx-par, paradigm-symmetry, known-bad-corpus, monitoring-discipline, tdd]

# Dependency graph
requires:
  - phase: 09-monitoring-discipline-symmetric-dsx-par (plan 09-01)
    provides: references/paradigm-symmetry.md, tests/test_known_bad_corpus.py::_EXPECTED_CAUGHT_DEFECTS (seeded empty)
  - phase: 09-monitoring-discipline-symmetric-dsx-par (plan 09-03)
    provides: dsx/frame/paradigm.py::_MONITORING_DISCIPLINE, DSX-PAR-010/DSX-PAR-011 shipped at CRITICAL, tests/test_known_bad_corpus.py::_EXPECTED_CAUGHT_DEFECTS filled in for both monitoring fixtures
provides:
  - four corrected corpus files (two ANALYSIS-SPEC.yaml headers, two POSTMORTEM.md) describing the shipped DSX-PAR-010/DSX-PAR-011 pair instead of an absent one
  - tests/test_known_bad_corpus.py::test_paradigm_symmetry_audit_enumerates_both_halves — the positive-content test underneath references/paradigm-symmetry.md
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Positive-content test derives its required substrings from the code's own data structure (_MONITORING_DISCIPLINE) at runtime rather than hard-coding them, so a clearing declaration added to the code without being added to the audit fails the suite instead of passing as unchecked prose"

key-files:
  created: []
  modified:
    - examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml
    - examples/known-bad/frequentist-uncontrolled-continuous-POSTMORTEM.md
    - examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml
    - examples/known-bad/bayesian-continuous-monitoring-POSTMORTEM.md
    - tests/test_known_bad_corpus.py

key-decisions:
  - "Only comment/prose lines were touched in the two ANALYSIS-SPEC.yaml files — every YAML key and value is byte-identical to before, matching the plan's explicit instruction that both fixtures already trigger their code with no field change"
  - "The Bayesian post-mortem's citation attribution was corrected in the same pass (D-10): Deng, Lu & Chen (2016) Theorem 1 states an optional-stopping equality that licenses the 1/(K+1) bound under known prior odds, not the bound itself — the bound is unnumbered prose immediately after Theorem 1 and again at Section 3.2. Both the 'Which formulation this fixture encodes' and 'Source' sections now cite Theorem 1 for what licenses the figure and Section 3.2 for the number, matching references/paradigm-symmetry.md's own already-correct phrasing"
  - "The new test reads dsx.frame.paradigm._MONITORING_DISCIPLINE at import time and iterates its rows, rather than pinning a literal list of expected codes/fields — this is what makes the test catch drift in the direction that matters (a clearing declaration added to the code without a matching audit update), per the plan's explicit fail-first requirement"

requirements-completed: [REQ-P9-01, REQ-P9-02, REQ-P9-06]

coverage:
  - id: D1
    description: "Neither monitoring fixture's spec header nor its post-mortem still claims that nothing in this repository adjudicates its defect today; each names the exact finding code and the exact gate points at which it now exits 1"
    requirement: "REQ-P9-01"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::test_every_spec_passes_the_critical_threshold_gate_points"
        status: pass
      - kind: other
        ref: "grep -c DSX-PAR-010 examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml -> 3; grep -c DSX-PAR-011 examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml -> 3"
        status: pass
    human_judgment: false
  - id: D2
    description: "references/paradigm-symmetry.md is covered by a positive-content test comparing its enumerated clearing declarations against dsx.frame.paradigm._MONITORING_DISCIPLINE's actual clearing fields"
    requirement: "REQ-P9-06"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::test_paradigm_symmetry_audit_enumerates_both_halves"
        status: pass
      - kind: other
        ref: "fail-first proof: temporarily removed all three occurrences of alpha_spending from references/paradigm-symmetry.md -> test failed with AssertionError naming 'alpha_spending' and paradigm 'frequentist'; git checkout -- references/paradigm-symmetry.md restored the file -> full 15/15 suite green again"
        status: pass
    human_judgment: false
  - id: D3
    description: "Every pre-existing text guard in tests/test_known_bad_corpus.py stays green; no retired gate over-claim and no retired bound misattribution reintroduced; content matching is whitespace-normalized (CRLF-safe)"
    requirement: "REQ-P9-02"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::test_no_corpus_file_repeats_a_retired_gate_overclaim, test_no_corpus_file_misattributes_the_prior_averaged_bound, test_bayesian_postmortem_states_the_deng_bound_and_its_value"
        status: pass
      - kind: other
        ref: "sh scripts/check.sh -> 447 tests green, all checks passed"
        status: pass
    human_judgment: false

duration: ~50min
completed: 2026-08-12
status: complete
---

# Phase 9 Plan 4: Corrected known-bad corpus and a positive-content test under the symmetry audit Summary

**Rewrote the two monitoring fixtures' spec headers and post-mortems to state what `DSX-PAR-010`/`DSX-PAR-011` now catch instead of claiming the defect is still unadjudicated, corrected the Bayesian post-mortem's Theorem-1-vs-§3.2 citation attribution (D-10), and added a positive-content test that derives its required substrings from `dsx.frame.paradigm._MONITORING_DISCIPLINE` at runtime so a clearing declaration added to the code without being added to `references/paradigm-symmetry.md` fails the suite.**

## Performance

- **Duration:** ~50 min
- **Completed:** 2026-08-12
- **Tasks:** 3 completed
- **Files modified:** 5 (2 ANALYSIS-SPEC.yaml headers, 2 POSTMORTEM.md, 1 test module)

## Accomplishments

- Both known-bad monitoring fixtures' `ANALYSIS-SPEC.yaml` header comments now state that `DSX-PAR-010`/`DSX-PAR-011` (CRITICAL) block `dsx gate plan` and `dsx gate execute`, name the specific clearing declaration each fixture is missing (`alpha_spending`/`threshold_calibration` for the frequentist fixture, `prior_justification`/`threshold_calibration` for the Bayesian one), and state that no field changed to make the fixture trip the check — only comment lines were touched, every YAML key and value is byte-identical to before
- Both `POSTMORTEM.md` files' "which absent code would have caught it" sections became "which code catches it" — naming the shipped code, its CRITICAL severity, both gate points, and one added sentence naming the counterpart fixture and its code (the corpus-level statement of the atomicity constraint)
- The Bayesian post-mortem's citation was corrected to match D-10/09-CONTEXT.md: Deng, Lu & Chen (2016) Theorem 1 states the optional-stopping *equality* that licenses the bound under known prior odds and any proper stopping time; the `1/(K+1)` bound itself is unnumbered prose immediately after Theorem 1 and again, in its operational "at most" form, at §3.2 — citing Theorem 1 alone for the number would be a locator error. Both the "Which formulation this fixture encodes" and "Source" sections now carry the corrected two-part citation. The three positive assertions (`1/(K+1)`, `1/20 = 0.05`, `Theorem 1`) all remain stated
- `tests/test_known_bad_corpus.py::test_paradigm_symmetry_audit_enumerates_both_halves` — a new positive-content test, in the module's existing whitespace-normalized idiom, that reads `references/paradigm-symmetry.md` and asserts it still names, for every row of `dsx.frame.paradigm._MONITORING_DISCIPLINE` (read at runtime, not hard-coded): the row's finding code, every one of the row's clearing declarations, all three controlled peeking policies (`sequential_obf`, `sequential_pocock`, `always_valid`), and both reference-value anchors (`0.142`, `0.05`)
- Full suite green: 15/15 corpus tests, `sh scripts/check.sh` — 447 tests, all checks passed

## Fail-First Proof (required by the plan; reported here, not committed)

Before committing Task 3, the new test's teeth were proven directly against the working copy:

1. Removed all three occurrences of `alpha_spending` from `references/paradigm-symmetry.md` (the table row and the two prose mentions — a partial single-occurrence edit was tried first and did **not** turn the test red, because the string still appeared twice more in the document; all three had to go for a true fail-first proof).
2. Ran `python3 -m unittest tests.test_known_bad_corpus.TestKnownBadCorpus.test_paradigm_symmetry_audit_enumerates_both_halves -v` — **FAILED**, with `AssertionError: 'alpha_spending' not found in ... : paradigm-symmetry.md no longer names the clearing declaration 'alpha_spending' for paradigm 'frequentist'`.
3. Restored the file with `git checkout -- references/paradigm-symmetry.md` (the file was never staged or committed with the redaction).
4. Re-ran the full module — **15/15 green**, including the new test.

The temporary edit was never committed; `git status --short references/paradigm-symmetry.md` was empty before Task 3's commit.

## Task Commits

Each task was committed atomically:

1. **Task 1: Correct the two fixture spec headers** - `5254c2a` (docs)
2. **Task 2: Correct the two post-mortems** - `0972fdd` (docs)
3. **Task 3: Positive-content test underneath the symmetry audit (TDD, fail-first proven)** - `ec281e4` (test)

**Plan metadata:** commit pending (this SUMMARY.md, applied per worktree-mode rules — STATE.md/ROADMAP.md are owned by the orchestrator)

## Files Created/Modified

- `examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml` — header comment rewritten (comment lines only)
- `examples/known-bad/frequentist-uncontrolled-continuous-POSTMORTEM.md` — "which absent code" section rewritten
- `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` — header comment rewritten (comment lines only)
- `examples/known-bad/bayesian-continuous-monitoring-POSTMORTEM.md` — "which absent code" section, "Which formulation" section, and "Source" section rewritten
- `tests/test_known_bad_corpus.py` — `_MONITORING_DISCIPLINE` import, three new module-level constants (`SYMMETRY_AUDIT_PATH`, `_CONTROLLED_PEEKING_POLICIES`, `_SYMMETRY_AUDIT_REFERENCE_VALUES`), one new test method

## Decisions Made

- Kept every YAML field in both `ANALYSIS-SPEC.yaml` files untouched, exactly as the plan required — `git diff` on both files shows only comment-line changes, no key or value changed
- Corrected the Bayesian post-mortem's Deng-citation attribution in the same pass as the "which code catches it" rewrite, since D-10/09-CONTEXT.md flagged this fixture's citation as already carrying the misattribution the corpus's negative guards (`_RETIRED_BOUND_MISATTRIBUTIONS`) exist to catch a *return* of, not the specific "Theorem 1 states 1/(K+1) directly" phrasing this file still had until now — bringing it in line with `references/paradigm-symmetry.md`'s own already-correct two-part citation
- Derived the new test's required substrings from `_MONITORING_DISCIPLINE` at runtime rather than a hard-coded literal list, per the plan's explicit instruction — this is what makes the test catch a future clearing declaration added to the code without a matching audit update, proven by the fail-first exercise above
- Used whitespace normalization (not line matching) in the new test, matching the module's existing idiom and this repository's CRLF-checkout rule (`.claude/CLAUDE.md`)

## Deviations from Plan

### Auto-fixed Issues

None. Plan executed exactly as written, including the fail-first proof procedure.

**Note on the fail-first proof:** the plan's example of removing "one clearing declaration" turned out to require removing *all* occurrences of that declaration's field name from the document, not just its table-row mention, because the audit prose repeats each field name in two other places (the "structural facts" list and the "cheapest dishonest fix" paragraph). A single-occurrence edit did not turn the test red on the first attempt; this is documented above rather than treated as a deviation, since the plan's intent (prove the test has teeth) was satisfied once the redaction was complete.

**Total deviations:** 0
**Impact on plan:** None.

## Issues Encountered

None.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- All four known-bad corpus files under `examples/known-bad/` now describe the tool's real behaviour for the monitoring pair; the interference fixture (`examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml`) still correctly states its defect is unadjudicated — `DSX-INT-010` is Phase 8's code, not this plan's, and is out of scope here
- `references/paradigm-symmetry.md` is now machine-checked against `dsx.frame.paradigm._MONITORING_DISCIPLINE` rather than trusted as prose
- This plan touched no file owned by concurrent plan 09-05 (`dsx/frame/paradigm.py`, `tests/test_dsx.py`, `references/finding-codes.md`)
- No blockers

---
*Phase: 09-monitoring-discipline-symmetric-dsx-par*
*Completed: 2026-08-12*

## Self-Check: PASSED

- FOUND commit: 5254c2a (Task 1)
- FOUND commit: 0972fdd (Task 2)
- FOUND commit: ec281e4 (Task 3)
- FOUND: examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml modified in 5254c2a
- FOUND: examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml modified in 5254c2a
- FOUND: examples/known-bad/frequentist-uncontrolled-continuous-POSTMORTEM.md modified in 0972fdd
- FOUND: examples/known-bad/bayesian-continuous-monitoring-POSTMORTEM.md modified in 0972fdd
- FOUND: tests/test_known_bad_corpus.py modified in ec281e4
- python3 -m unittest tests.test_known_bad_corpus -v -> 15/15 green
- sh scripts/check.sh -> 447 tests green, all checks passed
