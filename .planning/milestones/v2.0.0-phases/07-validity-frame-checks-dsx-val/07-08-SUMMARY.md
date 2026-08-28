---
phase: 07-validity-frame-checks-dsx-val
plan: 08
subsystem: testing
tags: [citation-honesty, d-05, kish, dsx-val-020, brief.md, ast-parsing]

# Dependency graph
requires:
  - phase: 07-validity-frame-checks-dsx-val
    provides: dsx/frame/val.py's DSX-VAL-020 unit-triad check and its Kish (1965) citation, dsx/mathx.py's design_effect(), brief.md section 7's citation ledger
provides:
  - "TestKishCitationCoherence: a package-wide, AST-derived invariant that no Kish citation under dsx/ may name a section locator and also claim only page numbers were confirmed, and that every Kish citation under dsx/ names the identical locator set"
  - "dsx/frame/val.py, dsx/mathx.py and brief.md agreeing on one Kish (1965) locator set: section 8.2, page 258 (design-effect definition), pages 161-162 (intraclass correlation)"
  - "gap G-07-4 (07-UAT.md test 4) closed"
affects: [07-validity-frame-checks-dsx-val UAT closure, any future dsx/*.py citing Kish]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "AST-derived citation-coherence test: collect string constants mentioning a source name by walking every *.py under a package with ast.parse/ast.walk, extract a bounded 'clause' with a lazy regex up to the first semicolon, then compare locator sets across sites rather than hand-listing files"
    - "Pages-only detector as a family of compiled regex patterns (not one exact string), each carrying a comment naming the real wording it derives from, plus a 'sentinel object distinct from empty set' for the unparseable case"

key-files:
  created: []
  modified:
    - tests/test_frame_val.py
    - dsx/frame/val.py
    - dsx/mathx.py
    - brief.md

key-decisions:
  - "Reading B (remedy_decision: reading_b, pinned by the user at UAT close 2026-08-12): kept section 8.2 as a confirmed Kish locator in dsx/frame/val.py and narrowed the disclosure, rather than deleting section 8.2 to match dsx/mathx.py's under-citing"
  - "brief.md corrected in the same commit as the code (plan's Option A), so the citation ledger and the shipped code state the same thing about the same source"

patterns-established:
  - "Package-wide citation-locator coherence checks belong in tests/, derived by AST walk, not enforced by a hand-written file list — a future citation site is covered automatically"

requirements-completed: [REQ-P7-02]

coverage:
  - id: D1
    description: "TestKishCitationCoherence added to tests/test_frame_val.py (3 assertions, 2 module-level helpers) and observed failing against the unfixed tree before any production file was touched"
    requirement: "REQ-P7-02"
    verification:
      - kind: unit
        ref: "tests/test_frame_val.py::TestKishCitationCoherence (3 tests, all FAIL at commit adc1ad2)"
        status: pass
      - kind: unit
        ref: "python3 -m unittest tests.test_frame_val.TestKishCitationCoherence -v (3/3 pass at commit cb074c4)"
        status: pass
    human_judgment: false
  - id: D2
    description: "Kish (1965) citation reconciled across dsx/frame/val.py (two sites), dsx/mathx.py and brief.md: section 8.2 kept as a confirmed locator, disclosure narrowed to flag only the design-effect formula's section number as unverified, no new bibliographic claim added"
    requirement: "REQ-P7-02"
    verification:
      - kind: unit
        ref: "tests/test_frame_val.py::TestKishCitationCoherence (3/3 pass)"
        status: pass
      - kind: other
        ref: "python3 scripts/gen-finding-catalogue.py --check (exit 0)"
        status: pass
      - kind: other
        ref: "python3 scripts/check_brief_refs.py (exit 0)"
        status: pass
    human_judgment: true
    rationale: "Whether the reworded disclosure states only what 07-DISCUSSION-LOG.md:102-103 and 07-CONTEXT.md:284/303-304 record, and no more, is a citation-accuracy judgment call this plan's own threat model (T-7-18) and human-check step assign to a human reader — automated tests confirm the Citation:/Reference value:/Structural criterion: shapes and the locator-set/pages-only-claim invariants, but cannot confirm the underlying bibliographic claim is exactly what the research log supports."

duration: ~25min
completed: 2026-08-14
status: complete
---

# Phase 07 Plan 08: Kish citation coherence (gap G-07-4) Summary

**Reconciled dsx/frame/val.py, dsx/mathx.py and brief.md onto one Kish (1965) locator set (section 8.2, page 258, pages 161-162), narrowed the honesty disclosure to name only the design-effect formula's section number as unverified, and added an AST-derived cross-file invariant test that would have caught the original contradiction.**

## Performance

- **Duration:** ~25 min
- **Tasks:** 2 completed
- **Files modified:** 4 (`tests/test_frame_val.py`, `dsx/frame/val.py`, `dsx/mathx.py`, `brief.md`)

## Accomplishments

- Added `TestKishCitationCoherence` (3 assertions, 2 module-level AST helpers) to `tests/test_frame_val.py`, proven to fail against the unfixed tree in its own commit before any production file changed
- Reworded `dsx/frame/val.py`'s `_UNIT_TRIAD_CITATION` constant and `_check_unit_triad` docstring: kept `section 8.2, page 258` (the confirmed locator), replaced the false "only the page numbers above were confirmed" clause with an accurate three-part disclosure
- Raised `dsx/mathx.py`'s `design_effect` docstring up to the same locator set and disclosure (it previously omitted section 8.2 entirely)
- Corrected `brief.md` section 7's Kish sentence to carry the same locators and narrowed disclosure, so the citation ledger and the shipped code agree
- Closed gap G-07-4 (07-UAT.md test 4, severity major)

## Task Commits

Two commits, in the order the plan's `key_links` require:

1. **Task 1: Write the three citation-coherence assertions and prove they fail against the tree as it stands** — `adc1ad2` (test) — touches only `tests/test_frame_val.py`
2. **Task 2: Reconcile the Kish citation across the three code sites and the citation ledger** — `cb074c4` (fix) — touches only `dsx/frame/val.py`, `dsx/mathx.py`, `brief.md`

## Observed RED gate (Task 1, commit adc1ad2, before any production file was touched)

```
python3 -m unittest tests.test_frame_val.TestKishCitationCoherence -v

test_brief_md_citation_ledger_does_not_claim_pages_were_the_only_kish_locators ... FAIL
test_every_kish_citation_in_the_dsx_package_names_the_same_locators ... FAIL
test_no_kish_citation_both_names_a_section_and_claims_pages_only ... FAIL

FAIL: test_brief_md_citation_ledger_does_not_claim_pages_were_the_only_kish_locators
AssertionError: Lists differ: ['only the page numbers',
 '(?:only|nothing but)(?:\\s+the)?\\s+pages?[^.;]*confirmed'] != []
: brief.md still claims pages were the only confirmed Kish locators
  (matched pattern(s): ['only the page numbers', '(?:only|nothing but)...'])

FAIL: test_every_kish_citation_in_the_dsx_package_names_the_same_locators
AssertionError: 2 != 1 : the dsx package's Kish citations do not all name the same locators:
  [('page', '161-162'), ('page', '258'), ('section', '8.2')]:
    ['dsx/frame/val.py:79', 'dsx/frame/val.py:667']
  [('page', '161-162'), ('page', '258')]:
    ['dsx/mathx.py:457']

FAIL: test_no_kish_citation_both_names_a_section_and_claims_pages_only
AssertionError: Lists differ: [... 4 items ...] != []
  dsx/frame/val.py:79 names a section locator ([('page', '161-162'), ('page', '258'),
    ('section', '8.2')]) and also matches the pages-only pattern 'only the page numbers'
  dsx/frame/val.py:79 ... matches '(?:only|nothing but)(?:\s+the)?\s+pages?[^.;]*confirmed'
  dsx/frame/val.py:667 names a section locator (...) and also matches 'only the page numbers'
  dsx/frame/val.py:667 ... matches '(?:only|nothing but)(?:\s+the)?\s+pages?[^.;]*confirmed'

Ran 3 tests in 0.212s
FAILED (failures=3)
```

All three assertions fail as predicted by the plan: assertion 1 fails on both `val.py` sites
(the constant and the docstring), assertion 2 fails because `val.py` names a section locator
and `mathx.py` does not, assertion 3 fails on `brief.md`. Zero errors — all three are genuine
assertion failures, not exceptions.

## Observed GREEN gate (Task 2, commit cb074c4)

```
python3 -m unittest tests.test_frame_val.TestKishCitationCoherence -v
test_brief_md_citation_ledger_does_not_claim_pages_were_the_only_kish_locators ... ok
test_every_kish_citation_in_the_dsx_package_names_the_same_locators ... ok
test_no_kish_citation_both_names_a_section_and_claims_pages_only ... ok
Ran 3 tests in 0.222s
OK
```

## Test and subtest counts

- **Before Task 1** (pre-plan baseline): 540 tests under `python3 -m unittest discover -s tests`
  (derived: 543 after Task 1 minus the 3 new tests Task 1 adds).
- **After Task 1** (commit adc1ad2, tree unfixed): 543 tests, 3 failures (`TestKishCitationCoherence`),
  0 errors.
- **After Task 2** (commit cb074c4, tree fixed): `python3 -m unittest discover -s tests` — 543 tests,
  0 failures, 0 errors (2 skipped, pre-existing and unrelated to this plan).
  `PYTHONPATH=. pytest tests/ -q` — 543 tests, **929 subtests**, all passed, 0 failures
  (pytest required `PYTHONPATH=.` in this environment — no `conftest.py`/`pyproject.toml` sets
  the import root, and `python3 -m unittest discover` normally supplies it implicitly via `-m`
  invocation from the repository root; this is an environment quirk, not a plan deviation, and
  every acceptance-criteria command in the plan itself was run and passed under this same
  `PYTHONPATH=.` invocation).

## Build-check exit codes

- `python3 scripts/gen-finding-catalogue.py --check` → **exit 0** — "finding catalogue is current"
  (pre-existing "declared twice with different text" warnings for unrelated codes print but do not
  affect the exit code; none name `DSX-VAL-020` or Kish)
- `python3 scripts/check_brief_refs.py` → **exit 0** — all 14 checks `[ok]`, including
  `contains 'Kish (1965)'` and `contains 'unverified' at least 3 times (found 4)`

## Gate CLI checks

- `python3 -m dsx.cli gate plan/execute/verify/ship --spec examples/good-ANALYSIS-SPEC.yaml` — all exit 0
- `python3 -m dsx.cli gate plan --spec examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` —
  exit 1, `DSX-VAL-040` present in output (unaffected by this plan, confirms no regression)
- `git status --porcelain dsx/checks/design.py` — no output (pinned content hash untouched)

## The four edited passages (quoted in full)

**1. `dsx/frame/val.py` — `_UNIT_TRIAD_CITATION` (module constant, lines 78-85):**

> Kish, L. (1965), Survey Sampling, section 8.2, page 258 (design-effect definition) and pages
> 161-162 (intraclass correlation); Higgins, J.P.T., Eldridge, S. and Li, T. (2024), Cochrane
> Handbook for Systematic Reviews of Interventions version 6.5, sections 23.1.4 and 23.1.4.1.
> Section 8.2 was confirmed for the design-effect definition; no section number was confirmed
> for the design-effect formula itself, and that locator is UNVERIFIED — do not invent one.

**2. `dsx/frame/val.py` — `_check_unit_triad` docstring `Citation:` paragraph (lines 671-677):**

> Citation: Kish, L. (1965), Survey Sampling, section 8.2, page 258 (design-effect definition)
> and pages 161-162 (intraclass correlation); Higgins, J.P.T., Eldridge, S. and Li, T. (2024),
> Cochrane Handbook for Systematic Reviews of Interventions version 6.5, sections 23.1.4 and
> 23.1.4.1. Section 8.2 was confirmed for the design-effect definition; no section number was
> confirmed for the design-effect formula itself, and that locator is UNVERIFIED — do not
> invent one.
>
> (The `Structural criterion:` line and the fixed-illustration / naming-inconsistency paragraphs
> that follow are unchanged from before this plan.)

**3. `dsx/mathx.py` — `design_effect` docstring `Citation:` paragraph (lines 461-468):**

> Citation: Kish, L. (1965), Survey Sampling, section 8.2, page 258 (design-effect definition)
> and pages 161-162 (intraclass correlation); Higgins, J.P.T., Eldridge, S. and Li, T. (2024),
> Cochrane Handbook for Systematic Reviews of Interventions version 6.5, sections 23.1.4 and
> 23.1.4.1.
> Section 8.2 was confirmed for the design-effect definition; no section number was confirmed
> for the design-effect formula itself, and that locator is UNVERIFIED — do not invent one.
> Reference value: an intraclass correlation of 0.02 and an average cluster size of 29.8 yield
> 1.576 — the Cochrane Handbook's own published worked example.

**4. `brief.md` — section 7's Kish sentence:**

> Kish (1965), *Survey Sampling*, section 8.2 and page 258 for the design-effect definition and
> pages 161 to 162 for the intraclass correlation (the source for `DSX-VAL-020`; section 8.2 was
> confirmed for the design-effect definition, and a section number for the design-effect formula
> itself is unverified).

Cross-check against `07-DISCUSSION-LOG.md:102-103` — "Kish (1965) §8.2 p. 258 confirmed for the
Deff definition and pp. 161-162 for the ICC, but no *section* number for the formula — flagged
UNVERIFIED" — all four passages above assert exactly this and nothing more: section 8.2 and page
258 confirmed for the definition, pages 161-162 confirmed for the ICC, only a section number for
the formula itself unverified. No new bibliographic claim was added.

## Gap G-07-4 status

**Closed.** The unit-triad citation's Kish locator and its UNVERIFIED disclosure now agree with
each other (no site both names a section and claims pages were the only confirmed locators) and
with the phase's own research ledger (`07-DISCUSSION-LOG.md:102-103`, `07-CONTEXT.md:284`). Reading
B, pinned by the user at UAT close 2026-08-12, was implemented: section 8.2 was kept, not deleted,
and `dsx/mathx.py` was raised up to the same locator set rather than `dsx/frame/val.py` being
lowered to match it.

## Decisions Made

- Kept `section 8.2` in `dsx/frame/val.py` and raised `dsx/mathx.py` up to it, per the plan's
  `remedy_decision: reading_b` (pinned by the user, not re-litigated here).
- Corrected `brief.md` in the same commit as the code (plan's Option A / default), so the citation
  ledger and the shipped code do not disagree.
- Used one identical narrowed-disclosure wording across both `dsx/frame/val.py` sites and
  `dsx/mathx.py`'s docstring, and a stylistically-adapted but semantically-identical version in
  `brief.md`'s flowing-paragraph prose, so all four sites assert the same three facts (section 8.2
  confirmed for the definition; no section confirmed for the formula; do not invent one).

## Deviations from Plan

None — plan executed exactly as written. One environment note (not a deviation): this machine's
default `python3` has no `pytest` installed; a second Python 3.12 installation on the same machine
does, but required `PYTHONPATH=.` to import the `dsx` package (no `conftest.py`/`pyproject.toml`
exists in this repository to set the import root for pytest specifically — `python3 -m unittest
discover` supplies the equivalent implicitly via its own `-m` module-invocation mechanics). Every
`pytest`-based acceptance criterion in the plan was run and passed under `PYTHONPATH=.`; no test,
source or config file was changed to work around this.

## Issues Encountered

None.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

Gap G-07-4 is closed. All 36 UAT tests for Phase 07 now have a passing/closed status (35 passed at
UAT, 1 issue now remediated). Phase 07 verification (`human_needed` per STATE.md, citation-
admissibility judgment) can proceed — the D2 coverage entry above flags the same human-judgment
scope UAT test 4 already used. No other outstanding work in this plan.

**Reminder to orchestrator:** this plan did not touch `.planning/REQUIREMENTS.md`,
`.planning/STATE.md` or `.planning/ROADMAP.md` (confirmed via `git status --porcelain` on all
three, no output). `REQ-P7-02` should be marked complete and Phase 07's gap G-07-4 marked closed
by the orchestrator after this worktree merges.

---
*Phase: 07-validity-frame-checks-dsx-val*
*Completed: 2026-08-14*
