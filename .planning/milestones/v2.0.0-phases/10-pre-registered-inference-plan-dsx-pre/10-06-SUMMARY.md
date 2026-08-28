---
phase: 10-pre-registered-inference-plan-dsx-pre
plan: 06
subsystem: testing
tags: [documentation, citation, known-limits, provenance, dsx-frame]

# Dependency graph
requires:
  - phase: 10-pre-registered-inference-plan-dsx-pre (plan 02)
    provides: "DSX-PRE-010/DSX-PRE-030 remedies whose README half this plan writes"
  - phase: 10-pre-registered-inference-plan-dsx-pre (plan 03)
    provides: "DSX-PRE-020 remedy and the content-lock exit-2 behaviour this plan documents"
  - phase: 10-pre-registered-inference-plan-dsx-pre (plan 04)
    provides: "prereg registered in GATE_PROFILES; tests/_trail_seed.py::seed_plan_header"
provides:
  - "README.md ### subsection naming the four things the declared-versus-executed reconciliation cannot see (declared_at self-declaration, analysis.test plan-time scaffolding, the content-lock ordering limit, the missing-lock exit-2 case), plus the PREREG_FACTS mini-language paragraph"
  - "brief.md section 7 Gelman and Loken (2014) citation anchor with both locator warnings intact, plus Simmons/Nelson/Simonsohn (2011) and Nosek/Ebersole/DeHaven/Mellor (2018) secondary sources"
  - ".planning/STATE.md Phase 10 open-items block records the three DSX-PRE-* codes as shipped, the brief.md anchor as resolved, and the two planner-discretion decisions (set-membership content lock, real-gate-invocation trail scoping)"
  - "tests/test_frame_prereg.py::TestDocumentedLimits (8 tests) pinning every documented limit and both Gelman/Loken locator flags against silent regression"
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "TestDocumentedLimits drives real firings of DSX-PRE-020/030 and reads the remedy off the emitted Finding, rather than asserting against dsx/frame/prereg.py's source text directly — the remedy is what an operator actually sees"
    - "Test 5 iterates sorted(PREREG_FACTS) rather than hard-coding three fact names, making the registry and its documentation a live link instead of a second copy that can drift"
    - "_normalize_whitespace collapses all whitespace runs (including CRLF) to a single space before every substring check, copied from the existing idiom in tests/test_known_bad_corpus.py, per the project's line-ending rule"

key-files:
  created: []
  modified:
    - README.md
    - brief.md
    - .planning/STATE.md
    - tests/test_frame_prereg.py

key-decisions:
  - "The new README subsection is titled to name the subject (what the declared-versus-executed reconciliation cannot see), not the feature name, matching the plan's instruction and the surrounding section's honest register"
  - "brief.md's new entry uses comma-separated 'volume 102, issue 6, pages 460-465' rather than the surrounding entries' 'volume X issue Y, pages A to B' shape, so the acceptance-required literal `460-465` (hyphenated) is present verbatim rather than only as 'to'-joined prose"
  - "STATE.md's Task 3 edits are confined to the existing 'Open items to resolve at phase discuss' block: two lines amended in place (numbering resolution, brief.md anchor) and one line appended (the two planner-discretion decisions) — no restructuring, no tracking/progress field touched, per this plan's explicit shared-file split with the orchestrator"
  - "Coverage deliverables D1-D3 below are marked human_judgment: true even though every automated check passes, because no test can judge whether the README/brief prose reads as an honest limit rather than a boast (the plan's own flagged_assumption) or verify brief.md/STATE.md prose content by any means other than a human read — the phase's manual-verification list carries that judgment, not this SUMMARY"

patterns-established:
  - "A documentation-only plan can still carry a coverage block: deterministic literal/substring checks route to unit verification (D4), while the prose-quality judgment each of them enables routes to human_judgment: true with a stated rationale (D1-D3), rather than omitting coverage entirely"

requirements-completed: [REQ-P10-02]

coverage:
  - id: D1
    description: "README.md's ### subsection states, in the surrounding section's honest register, the four things the DSX-PRE reconciliation cannot see: declared_at is an unverifiable operator self-declaration (post_data legal and silent by design), analysis.test is plan-time scaffolding not a property of the field, the content lock is change detection with no ordering enforced between the four gate points, and a missing plan-time header stops verify/ship at exit 2 with the suppressions[] route named; plus a paragraph naming the closed PREREG_FACTS set and pointing at `dsx vocab`."
    requirement: "REQ-P10-02"
    verification:
      - kind: unit
        ref: "tests/test_frame_prereg.py#TestDocumentedLimits (tests 1-5)"
        status: pass
    human_judgment: true
    rationale: "The substring tests prove the sentences exist, not that they read as honest limits rather than a boast — a substring match cannot judge tone. The plan's own flagged_assumption carries this reading on the phase's manual-verification list, not on an automated check."
  - id: D2
    description: "brief.md section 7 carries the Gelman and Loken (2014) citation anchor (page 460 and page 463 locators, both locator warnings intact — no numbered sections/tables/theorems, the selection-function symbol sourced from the unpublished 2013 Columbia working paper as notation only) plus the Simmons/Nelson/Simonsohn (2011) and Nosek/Ebersole/DeHaven/Mellor (2018) secondary sources, each scoped so neither is promoted into the primary anchor."
    requirement: "REQ-P10-02"
    verification:
      - kind: other
        ref: "grep -o for the literals Gelman, American Scientist, 460-465, Menstrual Cycles and Voting, 10.1177/0956797611417632, 10.1073/pnas.1708274114, and the no-numbered-sections sentence, each found exactly once in brief.md"
        status: pass
    human_judgment: true
    rationale: "No test in the suite asserts brief.md's prose content — the acceptance criteria were checked by direct grep at execution time, not by a regression-proof test. Whether the citation's scope notes read correctly (and not as fabricated locators) is a human judgement, per the plan's prohibitions on tidying the locator warnings away."
  - id: D3
    description: ".planning/STATE.md's Phase 10 open-items block records the three DSX-PRE-* codes as shipped (each naming the fact it owns and the plan that shipped it), records the brief.md citation anchor as resolved, and adds one line recording the two decisions left to the planner's discretion (content-lock set membership; real-gate-invocation trail scoping)."
    requirement: "REQ-P10-02"
    verification:
      - kind: other
        ref: "grep -o for DSX-PRE-010/-020/-030, 'set membership', and 'scoped to a real' in .planning/STATE.md, each present; git diff confirms edits are confined to the existing open-items block"
        status: pass
    human_judgment: true
    rationale: "STATE.md is project narrative, not code under test; correctness of the recorded resolution is judged by reading, and the orchestrator (single writer for tracking fields) reviews this content edit before the phase closes."
  - id: D4
    description: "tests/test_frame_prereg.py::TestDocumentedLimits (8 tests) pins every documented limit and both Gelman/Loken locator flags: the Known limits heading precedes declared_at, the self-declaration sentence, the analysis.test scaffolding sentence, the no-ordering-between-gate-points sentence, every PREREG_FACTS name (sourced from the registry, not hard-coded), a real DSX-PRE-030 firing's remedy, a real DSX-PRE-020 firing's remedy, and both locator flags in dsx/frame/prereg.py's docstrings."
    requirement: "REQ-P10-02"
    verification:
      - kind: unit
        ref: "python -m unittest tests.test_frame_prereg.TestDocumentedLimits -v (8/8 pass)"
        status: pass
      - kind: unit
        ref: "python -m unittest discover -s tests -q (629/629 pass)"
        status: pass
    human_judgment: false

# Metrics
duration: ~10min
completed: 2026-08-20
status: complete
---

# Phase 10 Plan 06: The README half of REQ-P10-02, the citation anchor, and the numbering resolution Summary

**README's `## Known limits` gains a subsection naming what the `DSX-PRE-*` declared-versus-executed reconciliation cannot see (an operator self-declaration, plan-time scaffolding, an unenforced gate-point ordering, and a missing-lock exit-2), `brief.md` section 7 gains the Gelman and Loken (2014) citation anchor with both locator warnings intact, and `STATE.md` records Phase 10's numbering as shipped — all pinned by eight new substring tests that drive real findings rather than reading source text.**

## Performance

- **Duration:** ~10 min
- **Started:** 2026-08-20T03:36:00+02:00 (approximate, first read)
- **Completed:** 2026-08-20T03:42:08+02:00
- **Tasks:** 3
- **Files modified:** 4 (README.md, brief.md, .planning/STATE.md, tests/test_frame_prereg.py)

## Accomplishments

- README.md gains one `###` subsection, placed between the concurrent-invocations limit and `### Two tiers of evidentiary rigour`, titled to name the subject rather than the feature. Four paragraphs cover `declared_at`, `analysis.test`, the content lock, and the missing-lock exit-2 case, plus a closing paragraph naming the closed `PREREG_FACTS` set and `dsx vocab` as its machine-readable source. No `Reference value:`-style number and no prevalence figure presented as this tool's behaviour, per the task's explicit prohibition.
- `tests/test_frame_prereg.py::TestDocumentedLimits` (8 tests): asserts the README heading/literal structure, the self-declaration and scaffolding sentences, the no-ordering sentence, every `PREREG_FACTS` name (sourced from the registry itself), a real `DSX-PRE-030` firing's remedy text, a real `DSX-PRE-020` firing's remedy text, and both Gelman/Loken locator flags in `dsx/frame/prereg.py`.
- `brief.md` section 7 gains the Gelman and Loken (2014) entry (pages 460 and 463 locators, both warnings intact) plus the Simmons/Nelson/Simonsohn (2011) and Nosek/Ebersole/DeHaven/Mellor (2018) secondary sources, each with its own scope note — an addition where section 7 named no pre-registration source before, not a brief-D-14 reversal.
- `.planning/STATE.md`'s Phase 10 open-items block amended: the numbering line now records all three codes as shipped (naming the fact each owns and the plan that shipped it), the brief.md-anchor line now records itself resolved, and one new line records the two decisions this phase settled at the planner's discretion (content-lock set membership, real-gate-invocation trail scoping).

## Task Commits

Each task was committed atomically:

1. **Task 1: The README known-limits subsection and the fact-registry surface** - `e37db84` (docs)
2. **Task 2: Assert the documented limits exist, so they cannot silently regress** - `1411b7b` (test)
3. **Task 3: The brief's reference-source anchor and the STATE.md numbering resolution** - `3a7baa1` (docs)

_No TDD RED/GREEN split — Task 2 (`tdd="true"`) was authored with the test class written directly against the already-landed README/source text from Task 1, then verified green before commit; there was no prior-landed behavior to drive a RED phase against, since the assertions are substring checks against prose, not a code path under development._

## Files Created/Modified

- `README.md` - New `### What the declared-versus-executed reconciliation cannot see` subsection under `## Known limits`
- `brief.md` - Section 7 gains the Gelman and Loken (2014) anchor plus two scoped secondary sources
- `.planning/STATE.md` - Phase 10 open-items block: two lines amended, one line appended
- `tests/test_frame_prereg.py` - New `TestDocumentedLimits` class (8 tests) plus a shared `_normalize_whitespace` helper

## Decisions Made

- **The README subsection title names the subject, not the feature** — "What the declared-versus-executed reconciliation cannot see" — per the task's literal instruction and the register the surrounding "Concurrent `dsx gate` invocations are not supported" subsection already sets.
- **brief.md's new entry departs slightly from the surrounding entries' `pages X to Y` prose shape**, using `pages 460-465` (hyphenated) instead, because the plan's acceptance criteria require the literal substring `460-465` to exist verbatim in the file — a wording choice made to satisfy an explicit, testable requirement rather than a stylistic preference.
- **STATE.md edits are confined to the existing open-items block**, per this plan's explicit shared-file split with the orchestrator: two existing lines were amended in place and one new line appended; no tracking/progress field (Current Position, Performance Metrics, phase-status) was touched, and `.planning/ROADMAP.md`/`.planning/REQUIREMENTS.md` were left untouched entirely, as instructed.
- **Coverage deliverables D1-D3 are marked `human_judgment: true`** despite every automated check passing, because the plan's own `flagged_assumptions` entry states plainly that a substring match proves the sentences exist, not that they read as honest limits to a human — that reading is carried on the phase's manual-verification list, and this SUMMARY does not pre-empt it.

## Deviations from Plan

None — plan executed exactly as written. The `brief.md` page-range formatting choice above is a wording decision made to satisfy the plan's own literal acceptance criterion, not a deviation from it.

## Issues Encountered

One process note, not a defect: the phase's shared scratchpad directory (`.../scratchpad/`) already held commit-message files from a prior plan's execution (`commit-msg-task1.txt`, `commit-msg-task2.txt`), which the write tool required reading before overwrite. Read and overwrote each with this plan's own commit message before use; no effect on the commits themselves (verified by `git log -1` after each commit).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- ROADMAP Success Criterion 4's README half is now written and pinned by test, alongside plans 02/03's finding-remedy half. `brief.md` section 7 carries the pre-registration anchor it lacked. `.planning/STATE.md` records the shipped code assignments and the two planner-discretion decisions — this plan's own Task 3 edit, confined to the open-items block per the orchestrator's shared-file split.
- Full suite green at 629/629 (up from 621 at this plan's start — 8 new tests, all in `TestDocumentedLimits`), `sh scripts/check.sh` prints `all checks passed` (finding catalogue current, capability manifest conformant, gate contract and determinism both green), `python scripts/gen-finding-catalogue.py --check` exits 0. Only the pre-existing, not-this-plan's-to-fix double-declaration warnings (`DSX-COH-030`, `DSX-PAR-002`, `DSX-SPEC-070` x3, `DSX-VAL-021`, `DSX-VAL-060`) remain, unchanged from plan 04's baseline.
- Per this plan's explicit instructions, `.planning/ROADMAP.md` and `.planning/REQUIREMENTS.md` were **not** touched, and no tracking/progress field in `.planning/STATE.md` was written — those remain for the orchestrator to update after this wave merges.
- No blockers.

## Self-Check: PASSED

- FOUND: README.md (### subsection present, verified by TestDocumentedLimits tests 1-4)
- FOUND: brief.md (Gelman/Loken entry, verified by direct grep for all required literals)
- FOUND: .planning/STATE.md (three DSX-PRE-* literals and both decision lines, verified by direct grep)
- FOUND: tests/test_frame_prereg.py (TestDocumentedLimits, 8/8 tests passing)
- FOUND: e37db84 (Task 1 commit)
- FOUND: 1411b7b (Task 2 commit)
- FOUND: 3a7baa1 (Task 3 commit)

---
*Phase: 10-pre-registered-inference-plan-dsx-pre*
*Completed: 2026-08-20*
