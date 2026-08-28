---
phase: 09-monitoring-discipline-symmetric-dsx-par
plan: 07
subsystem: infra
tags: [dsx, gate, citation-correctness, tdd, gap-closure]

# Dependency graph
requires:
  - phase: 09-monitoring-discipline-symmetric-dsx-par
    provides: "09-03 (DSX-PAR-010/011 monitoring-discipline pair) and 09-04 (its known-bad fixtures), whose shipped attribution this plan corrects; 09-06 (the same emission block's remedy= rewrite), sequenced first only to avoid a merge conflict inside one function"
provides:
  - "dsx/frame/paradigm.py::DSX-PAR-011 detail= — the citation parenthetical names Deng, Lu & Chen (2016) only; a separate sentence gives Theorem 1 its correct licensing role, transcribed from the already-correct docstring/post-mortem/audit wording"
  - "examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml's Formulation note, corrected to the same three-part attribution"
  - "tests/test_known_bad_corpus.py::_RETIRED_LOCATOR_ERRORS — a committed guard against this specific locator error returning through any file in the known-bad corpus"
affects: [09-VERIFICATION, gap-closure]

# Tech tracking
tech-stack:
  added: []
  patterns: ["Asserting on the emitted finding's detail= string rather than grepping the source file — the operator reads the emitted string, and a source grep would pass on a docstring that never reaches a user"]

key-files:
  created: []
  modified:
    - dsx/frame/paradigm.py
    - examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml
    - tests/test_dsx.py
    - tests/test_known_bad_corpus.py

key-decisions:
  - "assumption_delta_decision: no-change, as authored in the plan — this plan edits prose and one string literal, introduces no new representation, and demotes nothing."

patterns-established: []

requirements-completed: [REQ-P9-03]

coverage:
  - id: D1
    description: "DSX-PAR-011's emitted detail= string names Deng, Lu & Chen (2016) as the source of the prior-averaged formulation without pairing the theorem number with the 1/(K+1) parenthetical, and states separately that Theorem 1 licenses the bound under optional stopping while the bound itself is unnumbered prose at Section 3.2."
    requirement: "REQ-P9-03"
    verification:
      - kind: unit
        ref: "tests/test_dsx.py::TestPhase9MonitoringDiscipline::test_dsx_par_011_detail_attributes_the_bound_without_a_locator_error"
        status: pass
      - kind: e2e
        ref: "python3 -m dsx gate plan --spec examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml --json"
        status: pass
    human_judgment: false
  - id: D2
    description: "The known-bad Bayesian fixture's Formulation note comment carries the same three-part attribution as the paired POSTMORTEM.md, including the explicit locator-error sentence, with no YAML key or value changed."
    requirement: "REQ-P9-03"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::TestKnownBadCorpus::test_bayesian_fixture_states_the_corrected_attribution"
        status: pass
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::TestKnownBadCorpus::test_no_corpus_file_commits_the_theorem_1_locator_error"
        status: pass
    human_judgment: false
  - id: D3
    description: "The corpus-wide negative guard (_RETIRED_LOCATOR_ERRORS) stops the retired 'YYYY, Theorem 1' and 'Theorem 1 caps' phrasings from returning through any file under examples/known-bad/, without touching the pre-existing _RETIRED_BOUND_MISATTRIBUTIONS/_RETIRED_OVERCLAIMS/_BOUND_CLAIM_DOCUMENTS guards."
    requirement: "REQ-P9-03"
    verification:
      - kind: unit
        ref: "python3 -m unittest tests.test_known_bad_corpus -v"
        status: pass
      - kind: other
        ref: "git diff tests/test_known_bad_corpus.py shows _RETIRED_BOUND_MISATTRIBUTIONS, _RETIRED_OVERCLAIMS and _BOUND_CLAIM_DOCUMENTS unchanged"
        status: pass
    human_judgment: false

# Metrics
duration: ~25min
completed: 2026-08-13
status: complete
---

# Phase 9 Plan 07: Correct DSX-PAR-011's Theorem 1 locator error Summary

**The two shipped, operator-facing artifacts that paired `1/(K+1)` directly with "Theorem 1" — the `DSX-PAR-011` `detail=` string and the known-bad Bayesian fixture's own Formulation note — now attribute the bound the same way the module's own docstring, `references/paradigm-symmetry.md` and the paired POSTMORTEM.md already do: Theorem 1 licenses the bound under optional stopping; the number itself is unnumbered prose at Section 3.2.**

## Performance

- **Tasks:** 3
- **Files modified:** 3 (`dsx/frame/paradigm.py`, one known-bad fixture, two test files)
- **Duration:** ~25 min

## Accomplishments

- Closed the gap `09-VERIFICATION.md` recorded as a FAILED truth for ROADMAP Phase 9 Success Criterion 3 / REQ-P9-03: `DSX-PAR-011`'s emitted `detail=` string no longer reads `(Deng, Lu & Chen 2016, Theorem 1)` — the locator error the module's own docstring three sentences earlier warns against committing.
- `dsx/frame/paradigm.py`'s `DSX-PAR-011` emission now reads: `"...formulation (Deng, Lu & Chen 2016), the risk of false discovery ... is bounded by 1/(K+1) = 1/20 = 0.05 at K = 19 — a fixed reference anchor, never a computation over any operator-declared value. Theorem 1 licenses that bound under optional stopping with known prior odds; the bound itself is unnumbered prose following Theorem 1 and again in the paper's Section 3.2."` — transcribed from the already-correct docstring/POSTMORTEM/audit wording, not re-derived.
- `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml`'s Formulation note comment block now makes the identical three-part attribution, including the explicit "citing Theorem 1 alone for the number 1/(K+1) would be a locator error" sentence. Comment lines only — every YAML key and value is byte-identical to before.
- Added a committed negative guard (`_RETIRED_LOCATOR_ERRORS`, scoped to `examples/known-bad/` only — deliberately not folded into `_RETIRED_BOUND_MISATTRIBUTIONS`, which also runs against `brief.md`, `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md`, three documents that legitimately carry the corrected form) plus a positive-content test, so the locator error cannot return silently through this fixture or any future sibling.

## Task Commits

Each task was committed atomically:

1. **Task 1: RED — pin the corrected attribution in both shipped artifacts** — `e1af0fb` (test)
2. **Task 2: GREEN — correct DSX-PAR-011's emitted detail text** — `cc7b677` (feat)
3. **Task 3: Correct the known-bad fixture's Formulation note** — `4ffc9dd` (docs)

**Plan metadata:** committed alongside this summary (below).

_No separate `refactor(09-07)` commit — none was needed; both GREEN tasks were minimal on the first pass._

## TDD Gate Compliance

RED confirmed before any source change: `python3 -m unittest tests.test_dsx.TestPhase9MonitoringDiscipline tests.test_known_bad_corpus -v` reported exactly three failing test methods (each with one or more failed `subTest` assertions, never a collection/import/syntax error):

```text
FAIL: test_dsx_par_011_detail_attributes_the_bound_without_a_locator_error (tests.test_dsx.TestPhase9MonitoringDiscipline...)
AssertionError: 'Section 3.2' not found in '...Under the prior-averaged formulation (Deng, Lu & Chen 2016, Theorem 1), the risk...'
...
FAIL: test_no_corpus_file_commits_the_theorem_1_locator_error (tests.test_known_bad_corpus.TestKnownBadCorpus...) (file='bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml', retired='Theorem 1 caps')
AssertionError: 'Theorem 1 caps' unexpectedly found in '...Deng, Lu & Chen (2016) Theorem 1 caps the false-discovery risk...'
...
FAIL: test_bayesian_fixture_states_the_corrected_attribution (tests.test_known_bad_corpus.TestKnownBadCorpus...) (required='locator error')
AssertionError: 'locator error' not found in '...'
Ran 44 tests in 0.673s
FAILED (failures=9)
```

(9 individual `subTest` failures across those 3 test methods — the test-count contract in the acceptance criteria is "exactly three test methods fail," which held: `test_dsx_par_011_detail_attributes_the_bound_without_a_locator_error`, `test_no_corpus_file_commits_the_theorem_1_locator_error`, `test_bayesian_fixture_states_the_corrected_attribution`.)

GREEN confirmed after Task 2: `python3 -m unittest tests.test_dsx.TestPhase9MonitoringDiscipline -v` — `Ran 24 tests in 0.177s`, `OK`. GREEN confirmed after Task 3: `python3 -m unittest tests.test_known_bad_corpus -v` — `Ran 20 tests in 0.489s`, `OK`. Git log order verified: `test(09-07)` at `e1af0fb` precedes `feat(09-07)` at `cc7b677` precedes `docs(09-07)` at `4ffc9dd`.

## Files Created/Modified

- `dsx/frame/paradigm.py` — Rewrote only the `DSX-PAR-011` `detail=` string (verified by `git diff` — no change to title, severity, `where`, `remedy` or `DecisionRecord`). The citation parenthetical now names authors and year only; a new trailing sentence gives Theorem 1 its licensing role and names the two unnumbered-prose locations (immediately following Theorem 1, and Section 3.2).
- `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` — Rewrote the "Formulation note (T-6-17)" comment block to the same three-part attribution. `git diff` confirms only `#` comment lines changed; no YAML key or value was added, removed or changed.
- `tests/test_dsx.py` — Added `test_dsx_par_011_detail_attributes_the_bound_without_a_locator_error` to `TestPhase9MonitoringDiscipline`, asserting on the emitted finding's whitespace-normalized `detail`. No existing test method was modified (confirmed by `git diff` showing `test_arbitrary_decision_threshold_string_produces_identical_finding_text` and `test_dsx_par_011_reference_value_boundary_arithmetic` untouched).
- `tests/test_known_bad_corpus.py` — Added `_RETIRED_LOCATOR_ERRORS = ("2016, Theorem 1", "Theorem 1 caps")`, a corpus-wide negative guard (`test_no_corpus_file_commits_the_theorem_1_locator_error`), and a fixture-scoped positive-content test (`test_bayesian_fixture_states_the_corrected_attribution`). `_RETIRED_BOUND_MISATTRIBUTIONS`, `_RETIRED_OVERCLAIMS` and `_BOUND_CLAIM_DOCUMENTS` are unchanged, confirmed by `git diff`.

## Decisions Made

None beyond the plan's own `<assumption_delta_decision>` (no-change) — implemented exactly as specified, not relitigated.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed a self-inflicted line-wrap that reintroduced the "1/20 = 0.05" split across a comment-line boundary**
- **Found during:** Task 3, first draft of the fixture's Formulation note
- **Issue:** The first draft wrapped `... K = 19 and the bound is 1/20 =` at end of line, continuing `0.05 exactly.` on the next `# `-prefixed comment line. Because each YAML comment line carries a literal `#` prefix, whitespace-normalization (`" ".join(text.split())`) does not remove that `#` — it collapses to `...1/20 = # 0.05...`, breaking the required substring `1/20 = 0.05` and failing `test_bayesian_fixture_states_the_corrected_attribution`. This is exactly the CRLF/line-wrap fragility the plan's `<threat_model>` (T-9-20) and its whitespace-normalization requirement exist to guard against — caught by the guard itself, not missed by it.
- **Fix:** Rewrapped the paragraph so `1/(K+1)`, `1/20 = 0.05`, `unnumbered prose`, `Section 3.2`, `locator error` and `0.0526` each stay within one comment line.
- **Files modified:** `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml`
- **Verification:** `python3 -m unittest tests.test_known_bad_corpus -v` — `Ran 20 tests in 0.489s`, `OK`.
- **Committed in:** `4ffc9dd` (Task 3 commit — the defect never left the working tree in a committed state)

---

**Total deviations:** 1 auto-fixed (1 self-caught bug, corrected before the task's commit — never shipped in a broken state)
**Impact on plan:** No scope creep; the fix is exactly the wording correction the task specifies, just re-wrapped to survive the repository's own CRLF/comment-prefix structure.

## Issues Encountered

The line-number references in the plan's `<read_first>` blocks were stale by the amount the baseline note warned about (`09-06` had already shifted `dsx/frame/paradigm.py` by roughly +13 lines by the time this plan ran). Trusted the file over the plan's line numbers throughout, per the plan's own `<verified_baseline>` instruction — no functional impact, noted here for completeness.

`sh scripts/check.sh` continues to produce the same seven pre-existing "declared twice with different text" warnings (`DSX-COH-030`, `DSX-PAR-002`, `DSX-SPEC-070` x3, `DSX-VAL-021`, `DSX-VAL-060`) already documented as non-blocking, out-of-scope informational noise in `09-06-SUMMARY.md`. None of the three files this plan touches declares any of those seven codes; not fixed, per the SCOPE BOUNDARY rule.

## Verification (mandatory, all re-run after the final commit)

1. `python3 -m dsx gate plan --spec examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml --json` — exit `1`, CRITICAL codes exactly `['DSX-PAR-011']`. The emitted `detail=`:
   > "design.peeking_policy is uncontrolled_continuous: interim looks continue with no sequential correction and no anytime-valid method. Under the prior-averaged formulation (Deng, Lu & Chen 2016), the risk of false discovery at a P(B>A) > 0.95 decision threshold is bounded by 1/(K+1) = 1/20 = 0.05 at K = 19 — a fixed reference anchor, never a computation over any operator-declared value. Theorem 1 licenses that bound under optional stopping with known prior odds; the bound itself is unnumbered prose following Theorem 1 and again in the paper's Section 3.2."
2. `python3 -m dsx gate plan --spec examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml --json` — exit `1`, CRITICAL codes exactly `['DSX-PAR-010']` (unchanged).
3. `python3 -m dsx gate plan/execute/verify/ship --spec examples/good-ANALYSIS-SPEC.yaml` — exit `0` at all four gate points.
4. `sh scripts/check.sh` — `Ran 526 tests in 5.053s`, `OK (skipped=2)`; finding catalogue current (`python3 scripts/gen-finding-catalogue.py --check` exits `0`, `git diff references/finding-codes.md` is empty); capability manifest conformant (`dsx` v2.0.0, 2 steps, 5 contributions, 5 gates, 9 skills, 6 agents, 13 config keys); gate contract and determinism checks pass. Baseline was 523 tests (after plan 09-06's merge); the 3 new tests from this plan (one in `test_dsx.py`, two in `test_known_bad_corpus.py`) account for the delta to 526.
5. `git diff dsx/frame/paradigm.py` confirms the change is scoped to the `DSX-PAR-011` `detail=` argument only.
6. `git diff examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` confirms the change is scoped to `#` comment lines only — no YAML key or value added, removed or changed.

## Next Phase Readiness

This closes the last open gap `09-VERIFICATION.md` recorded for REQ-P9-03 / ROADMAP Phase 9 Success Criterion 3. Plan 09-06 (the other gap-closure plan in this wave, scoped to REQ-P9-06) touches the same function but a disjoint part of it (the `remedy=` strings and the clearing predicate) and has no ordering dependency in the other direction. With both 09-06 and 09-07 complete, every truth `09-VERIFICATION.md` scored FAILED for Phase 9 has a corresponding gap-closure plan executed and verified.

---
*Phase: 09-monitoring-discipline-symmetric-dsx-par*
*Completed: 2026-08-13*

## Self-Check: PASSED

- FOUND: `.planning/phases/09-monitoring-discipline-symmetric-dsx-par/09-07-SUMMARY.md`
- FOUND: `e1af0fb` (test RED)
- FOUND: `cc7b677` (feat GREEN)
- FOUND: `4ffc9dd` (docs — fixture Formulation note)
- FOUND: `dsx/frame/paradigm.py`
- FOUND: `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml`
