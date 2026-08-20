---
phase: 11-frequentist-admissibility-adjudicator-dsx-adm
plan: 01
subsystem: docs
tags: [requirements, roadmap, citations, D-05, D-27, D-29, test-selection, brief]

# Dependency graph
requires:
  - phase: 07-validity-frame-checks-dsx-val
    provides: the dependence taxonomy REQ-P11-01's amendment reasoning refers to
provides:
  - REQ-P11-01 and ROADMAP Phase 11 Success Criterion 1 amended from "25-35" to "14" families, with the D-02 reason recorded
  - references/test-selection.md's proportion|2|no fallback corrected from Fisher's exact to Boschloo's exact test, cited (D-27)
  - brief.md section 7 carries both D-29 locators (Kohavi Ch. 22; Cameron & Miller Section VI) with verification status stated
affects: [11-04, 11-08]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Footnote citation convention added to references/test-selection.md ([^1] below the table) — the file's first citation, following the locator_status honesty convention already used in dsx/frame/paradigm.py and dsx/spec.py"

key-files:
  created: []
  modified:
    - .planning/REQUIREMENTS.md
    - .planning/ROADMAP.md
    - references/test-selection.md
    - brief.md

key-decisions:
  - "REQ-P11-01's checkbox and traceability row stay 'Pending' — this plan amends the requirement's text, it does not complete it (per the plan's own instruction)"
  - "The D-27 fix goes in a footnote below the table rather than a longer table cell, keeping the table's column widths readable"
  - "The Kohavi and Cameron & Miller brief.md updates edit the existing citation sentences in place rather than appending new paragraphs, so the file does not carry two contradictory statements about the same locator"

patterns-established: []

requirements-completed: []

coverage:
  - id: D1
    description: "REQ-P11-01 and ROADMAP Phase 11 Success Criterion 1 amended from 25-35 to 14 families, with the amended-from value and the D-02 reason recorded in both documents"
    requirement: "REQ-P11-01"
    verification:
      - kind: other
        ref: "python -c assertion script in 11-01-PLAN.md Task 1 <verify> block"
        status: pass
    human_judgment: false
  - id: D2
    description: "references/test-selection.md's proportion|2|no small-expected-cell fallback no longer prescribes Fisher's exact test; it names Boschloo's exact test, cited to Lydersen, Fagerland & Laake (2009) section 9"
    verification:
      - kind: other
        ref: "python -c assertion script in 11-01-PLAN.md Task 2 <verify> block; python -m unittest discover -s tests (640 tests, OK)"
        status: pass
    human_judgment: true
    rationale: "Plan Task 2's <human-check> requires a human to confirm the replacement sentence reads correctly to a practitioner and that the Lydersen section-9 locator is stated at the strength the source supports — a judgment the automated regex/literal checks cannot make."
  - id: D3
    description: "brief.md section 7 carries the Kohavi, Tang & Xu Chapter 22 locator (verified) and the Cameron & Miller Section VI locator (manuscript-verified, with the Section VIII-to-XI typeset-numbering caveat)"
    verification:
      - kind: other
        ref: "python -c assertion script in 11-01-PLAN.md Task 3 <verify> block"
        status: pass
    human_judgment: true
    rationale: "Plan Task 3's <human-check> requires a human to confirm each locator is stated at the strength the evidence supports — a judgment call the literal-substring check cannot make."

duration: ~20min
completed: 2026-08-20
status: complete
---

# Phase 11 Plan 01: Requirement amendment and citation corrections Summary

**Amended REQ-P11-01/ROADMAP SC1 from 25-35 to 14 families (D-02), replaced test-selection.md's Fisher's-exact fallback with Boschloo's exact test cited to Lydersen et al. 2009 (D-27), and folded two resolved locators (Kohavi Ch. 22; Cameron & Miller Section VI) into brief.md section 7 (D-29)**

## Performance

- **Duration:** ~20 min
- **Completed:** 2026-08-20
- **Tasks:** 3
- **Files modified:** 4 (`.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `references/test-selection.md`, `brief.md`)

## Accomplishments

- `REQ-P11-01` now states 14 estimator families (not 25-35), with an amendment note naming the amended-from value and the D-02 traceability reason directly beneath it. The requirement's checkbox and traceability row stay "Pending" — the text is amended, the requirement is not completed.
- `ROADMAP.md` Phase 11 Success Criterion 1 states 14 families with a parenthetical naming the D-02 amendment.
- `references/test-selection.md`'s `proportion | 2 | no` row no longer prescribes "Fisher exact if any expected cell < 5" — it names Boschloo's unconditional exact test, with a new footnote citing Lydersen, Fagerland & Laake (2009), *Statistics in Medicine* 28(7):1159-1175, section 9 (verified). This is the file's first citation.
- `brief.md` section 7 now states the Kohavi, Tang & Xu shared-budget interference locator as Chapter 22, *Leakage and Interference between Variants*, pages 226-234, verified — closing the flag recorded in `06-08-SUMMARY.md` and `06-VERIFICATION.md`.
- `brief.md` section 7 now states the Cameron & Miller (2015) few-clusters locator as Section VI, *Few Clusters* (with Section II for the estimator, Section IV for the clustering dimension), partially closing the flag recorded in `07-01-SUMMARY.md`, carrying the caveat that the accepted manuscript's numbering jumps from Section VIII to Section XI and the typeset journal numbering may differ.

## Task Commits

Each task was committed atomically:

1. **Task 1: Amend REQ-P11-01 and ROADMAP Success Criterion 1 to the delivered family count** - `c4846a3` (docs)
2. **Task 2: Correct the Fisher's exact fallback in references/test-selection.md (D-27)** - `50b8cf9` (fix)
3. **Task 3: Fold the two resolved locators into brief.md section 7 (D-29)** - `a458de0` (docs)

**Plan metadata:** SUMMARY.md commit (see below)

## Files Created/Modified

- `.planning/REQUIREMENTS.md` - REQ-P11-01 amended to 14 families with an amendment note naming D-02
- `.planning/ROADMAP.md` - Phase 11 Success Criterion 1 amended to 14 families with a D-02 parenthetical
- `references/test-selection.md` - proportion|2|no fallback corrected to Boschloo's exact test, cited via a new footnote
- `brief.md` - Kohavi Ch. 22 and Cameron & Miller Section VI locators folded into section 7, each with its verification status stated

## Decisions Made

- REQ-P11-01's checkbox and traceability row (`| REQ-P11-01 | Phase 11 | Pending |`) are left unchanged — this plan amends the requirement's text, per its own explicit instruction, and does not complete it.
- The D-27 replacement citation lives in a markdown footnote below the table rather than inside the narrow table cell, keeping the table's prose register and column widths intact.
- Both brief.md D-29 additions edit the existing Kohavi and Cameron & Miller sentences in place (adding a locator clause to each) rather than appending new paragraphs, so the file never states two versions of the same fact.

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered

- `python scripts/gen-finding-catalogue.py --check` prints two more "declared twice with different text" warnings (`DSX-COH-030`, `DSX-PAR-002`) than the plan's `<verification>` section names (which expects only `DSX-SPEC-070` twice, `DSX-VAL-021`, `DSX-VAL-060`). The check still exits 0 ("finding catalogue is current") and the test suite still reports 640 tests OK, so this is a drift in the plan's stated baseline, not a build failure — and this plan touches no code that could cause it. Logged to `deferred-items.md` in this phase directory rather than fixed, per the scope-boundary rule (out of scope for a documentation-only plan).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `references/families.yaml` (plan 11-04) can now cite "14 families" without contradicting `REQUIREMENTS.md`/`ROADMAP.md` — the D-02 amendment closes that gap ahead of 11-04.
- `references/test-selection.md`'s corrected Boschloo-over-Fisher ordering is available for 11-04 to state the same preference in `families.yaml`'s ranking notes, per the plan's key_links requirement.
- The two `references/test-selection.md` proportion rows (`no`/`yes`) remain distinct after the D-27 edit — confirmed by grep count (one row each) — so no merge occurred.
- No blockers for 11-02 through 11-08.

---
*Phase: 11-frequentist-admissibility-adjudicator-dsx-adm*
*Completed: 2026-08-20*
