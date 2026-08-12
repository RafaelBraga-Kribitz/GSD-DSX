---
phase: 07-validity-frame-checks-dsx-val
plan: 02
subsystem: docs
tags: [citations, D-05, D-10, D-17, brief.md, research]

# Dependency graph
requires:
  - phase: 06-contract-extension-decision-record-paradigm-manifest
    provides: the D-05 mechanical citation-enforcement mechanism (gen-finding-catalogue.py --check) and the dsx/frame/paradigm.py unverified-locator precedent this plan follows
provides:
  - "brief.md section 7 extended with six sources Phase 7 code will cite (ICH E9(R1), Hernan and Robins 2016, Popper, Kish 1965, Cochrane Handbook, Cronbach and Meehl 1955)"
  - "Lohr and Little and Rubin editions pinned to their 2021/2019 third editions"
  - "scripts/check_brief_refs.py — mechanical verifier for the section-7 extension"
  - "the corrected, Cochrane-sourced 1.576 design-effect worked example in .planning/research/FEATURES.md, replacing the unpublished 3.45 value"
affects: [07-01, 07-03, 07-04, 07-05, 07-06]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "brief.md section 7 flowing-paragraph citation convention extended, not converted to a list"
    - "unverified-locator labelling inline in the citation sentence itself (Kish section number, GSB typeset-vs-preprint numbering, Gelman and Hill chapter locator, Cameron and Miller section locator)"

key-files:
  created:
    - scripts/check_brief_refs.py
  modified:
    - brief.md
    - .planning/research/FEATURES.md

key-decisions:
  - "Verification script normalizes whitespace before substring matching, because brief.md's flowing-paragraph convention hard-wraps citation strings across line breaks (e.g. 'White and\\r\\nCarlin (2010)')"
  - "The D-10 correction note in FEATURES.md names the retired value (3.45) but not the literal false-citation strings ('Donner & Klar', '16.3.4'), so the file satisfies both 'name the retired value' and 'no longer contains those literal strings' simultaneously"
  - "Mayo (2018) and Conley (1999) are not added to brief.md section 7 — Mayo was never present there and this plan carries no instruction to add it; Conley is explicitly excluded per D-17 (training-knowledge-only attribution)"
  - "The UN handbook cross-check value (ICC 0.05, cluster size 17 -> 1.80) is omitted from FEATURES.md — the plan permits it only if the executor can name the handbook's full title, which was not independently verifiable in this plan's scope"

requirements-completed: [REQ-P7-02, REQ-P7-05]

coverage:
  - id: D1
    description: "brief.md section 7 lists every source a Phase 7 docstring will cite (six new sources), pins the Lohr and Little and Rubin editions, and labels four locators unverified"
    requirement: "REQ-P7-05"
    verification:
      - kind: unit
        ref: "scripts/check_brief_refs.py"
        status: pass
    human_judgment: false
  - id: D2
    description: "the unsourced 3.45 design-effect worked example in .planning/research/FEATURES.md is replaced with the Cochrane Handbook's own published value (1.576), and the retired value survives only inside an explicit D-10 correction note"
    requirement: "REQ-P7-02"
    verification:
      - kind: unit
        ref: "tests.test_known_bad_corpus (python3 -m unittest tests.test_known_bad_corpus -v)"
        status: pass
      - kind: other
        ref: "python3 -c \"... assert 'Worked published example' not in t or '1.576' in t.split(...)[1][:600]\""
        status: pass
    human_judgment: false

duration: ~35min
completed: 2026-08-12
status: complete
---

# Phase 7 Plan 02: brief.md citation-ledger extension and FEATURES.md D-10 correction Summary

**Extended brief.md section 7 with six new D-05 citation sources and two pinned editions, and replaced the unpublished 3.45 design-effect worked example in .planning/research/FEATURES.md with the Cochrane Handbook's own 1.576 value.**

## Performance

- **Duration:** ~35 min
- **Completed:** 2026-08-12
- **Tasks:** 2
- **Files modified:** 3 (2 edited, 1 created)

## Accomplishments

- `brief.md` section 7 now names all six sources Phase 7's `DSX-VAL-*` checks will cite: International Council for Harmonisation (2019) E9(R1) addendum, Hernan and Robins (2016) journal article, Popper (1959/2002), Kish (1965), Higgins/Eldridge/Li (2024) Cochrane Handbook, and Cronbach and Meehl (1955)
- Pinned the two previously edition-unpinned entries: Lohr to the 2021 third edition, Little and Rubin to the 2019 third edition, each with chapter/section locators
- Extended the Gelman and Hill entry (year, publisher) and the Gelman, Simpson and Betancourt entry (both section locators, cited by number and title) and added Cameron and Miller (2015) — four locators flagged `unverified` per D-05's "flag, never invent" rule
- Created `scripts/check_brief_refs.py`, a mechanical verifier asserting every required citation string is present, `Conley` is absent, at least three `unverified` labels exist, and both editions are pinned
- Corrected `.planning/research/FEATURES.md`'s design-effect worked example: replaced the unpublished `ICC=0.05, m=50 -> 3.45` value (misattributed to Donner & Klar 2000 and a Cochrane Handbook section that does not print it) with the Cochrane Handbook's own `ICC=0.02, m=29.8 -> 1.576` value, recomputed the accompanying interval-narrowness figure to `~1.26x`, and added an explicit correction note naming decision D-10

## Task Commits

Each task was committed atomically:

1. **Task 1: Extend brief.md section 7 with the six Phase 7 sources and pin two editions** - `2b12c80` (docs)
2. **Task 2: Correct the unsourced design-effect worked example in the research file** - `1a0b16c` (fix)

**Plan metadata:** committed alongside this SUMMARY (see final commit in worktree log)

## Files Created/Modified

- `brief.md` - Section 7 extended with six new citation sentences, two editions pinned, four locators explicitly flagged unverified
- `.planning/research/FEATURES.md` - Design-effect worked example replaced with the Cochrane Handbook's own 1.576 value; a D-10 correction note added; the reasoning-onward paragraph relabelled as arithmetic illustration; Testability/Confidence notes and the table-stakes summary row updated to match
- `scripts/check_brief_refs.py` - New verification helper (created because it did not already exist) asserting the section-7 extension is complete

## Decisions Made

- Verification-script whitespace normalization: `brief.md`'s flowing-paragraph convention hard-wraps at roughly 100 columns, so a citation string like "White and Carlin (2010)" can be split across a line break in the raw file. `scripts/check_brief_refs.py` collapses whitespace runs before substring matching rather than requiring exact-line-adjacent text, so line-wrapping is never mistaken for missing content.
- FEATURES.md correction note wording: named the retired value (`3.45`) once, as the plan's action text requires, but did not repeat the literal false-citation strings `Donner & Klar` or `16.3.4` — this satisfies both the "name the retired value" instruction and the acceptance criteria requiring those two literal strings be absent from the file.
- Did not add Mayo (2018) to brief.md — it was never present in section 7 and this plan's task carries no instruction to add it, only a prohibition against attaching a section number to it if referenced elsewhere.
- Omitted the optional United Nations household-survey cross-check value (ICC 0.05, cluster size 17 -> 1.80) from FEATURES.md, per the plan's own instruction to omit it unless the handbook's full title can be named — it could not be independently verified within this plan's scope.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Table-stakes summary row in FEATURES.md still asserted the retired 3.45 value**
- **Found during:** Task 2 self-check (grep for stray `3.45`/`Donner & Klar`/`16.3.4` occurrences across the file)
- **Issue:** A summary table row at `.planning/research/FEATURES.md:428` (outside the passage the task's `<read_first>` scoped to) independently asserted "worked example (ICC=0.05,m=50->3.45) are settled", which would have reintroduced the retired value as a second, undisclosed appearance outside the explicit correction note — violating the plan's own done criterion that "the retired value appears only inside an explicit note explaining its removal"
- **Fix:** Updated the row to reference the corrected `ICC=0.02,m=29.8->1.576, D-10` value
- **Files modified:** `.planning/research/FEATURES.md`
- **Verification:** `python3 -c "... '3.45' not in ..."` style grep confirms `3.45` now appears only inside the correction note; full test suite still green
- **Committed in:** `1a0b16c` (Task 2 commit)

**2. [Rule 1 - Bug] Testability and Confidence notes still referenced the retired ICC=0.05/m=50 worked example**
- **Found during:** Task 2, while replacing the "Worked published example" passage
- **Issue:** The `<action>` block scoped its instruction to the "Worked published example" passage and the immediately following reasoning paragraph, but two adjacent notes ("Testability" and "Confidence") also named the retired `ICC=0.05, m=50 -> 3.45` combination as the basis for the unit test and the confidence rating — leaving the file internally inconsistent with the replacement above it and reintroducing the retired value as the file's stated test oracle
- **Fix:** Updated both notes to reference the Cochrane Handbook's own `ICC=0.02, m=29.8 -> 1.576` worked example instead
- **Files modified:** `.planning/research/FEATURES.md`
- **Verification:** Full test suite green; `python3 -m unittest tests.test_known_bad_corpus -v` green
- **Committed in:** `1a0b16c` (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (both Rule 1 — internal-consistency bugs directly caused by the D-10 correction this task performs)
**Impact on plan:** Both fixes are within the plan's own stated goal (no sentence in the file should claim publication for a computed illustration, and the retired value should appear only inside the explicit note). No scope creep — no file outside `.planning/research/FEATURES.md` was touched by these fixes.

## Issues Encountered

- The verification script's first draft used exact substring matching, which failed against the raw file because `brief.md`'s line-wrapping split two required citation strings ("White and Carlin (2010)", "Cronbach and Meehl (1955)") across line breaks. Resolved by normalizing whitespace before matching (see Decisions Made above). No test or acceptance criterion had to be weakened to reach this fix — the underlying content was already correct; only the checker's string-matching was too strict.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `brief.md` section 7 now anchors every citation plans 07-03 through 07-06 will need for their `DSX-VAL-0NN` docstrings — no further section-7 extension should be required for the rest of Phase 7.
- `.planning/research/FEATURES.md` no longer carries an unsourced number a later agent could reintroduce into shipped code or a docstring.
- `dsx/mathx.py::design_effect()` (owned by plan 07-01, run in parallel) should assert `design_effect(29.8, 0.02) == 1.576` to match the value now anchored in both `brief.md` and `.planning/research/FEATURES.md` — this plan did not verify that function directly because plan 07-01 executes in a separate worktree and the function did not yet exist in this worktree at execution time; the value itself was taken from the plan's own specification, which both plans share.
- Full suite green: `python3 -m unittest discover -s tests` -> 306 tests OK; `python3 scripts/gen-finding-catalogue.py --check` -> exit 0.

---
*Phase: 07-validity-frame-checks-dsx-val*
*Completed: 2026-08-12*
