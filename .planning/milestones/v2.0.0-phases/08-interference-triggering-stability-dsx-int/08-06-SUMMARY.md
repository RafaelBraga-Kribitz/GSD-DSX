---
phase: 08-interference-triggering-stability-dsx-int
plan: 06
subsystem: planning-tracking
tags: [roadmap, requirements, correction, deng-hu, gated-backlog]
status: complete

# Dependency graph
requires:
  - phase: 08-interference-triggering-stability-dsx-int
    plan: "08-04"
    provides: "the corrected brief.md section 6.5 gated-backlog row and DSX-INT-030's docstring, which the amended ROADMAP/REQUIREMENTS text must agree with (D-12)"
  - phase: 08-interference-triggering-stability-dsx-int
    plan: "08-05"
    provides: "the fourth and final DSX-INT-* code, closing the phase's implementation so this plan's amendments describe a finished module rather than a promise"
provides:
  - "ROADMAP.md Phase 8 success criterion 3, reworded from asking for a published value the Deng & Hu (2015) paper does not contain to asking for the paper's own published counterexample (D-10)"
  - "ROADMAP.md Phase 8 success criterion 4, reworded from the false entry condition 'equation obtained from primary source' to the real, falsifiable blocker Formula (3) imposes (D-12)"
  - "REQUIREMENTS.md REQ-P8-04, rewritten to carry the same corrected entry condition as the roadmap criterion, so the two cannot disagree"
  - "REQUIREMENTS.md's Out of Scope table row for ratio-metric dilution, independently carrying the same disproven premise, corrected for the same reason (found during this plan, not named in its files_modified)"
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Scoped line-level replacement in a multi-phase tracking document, never a whole-file write, with git diff bounding the change to the affected block as a mechanical (not read-based) tampering check"

key-files:
  created: []
  modified:
    - .planning/ROADMAP.md
    - .planning/REQUIREMENTS.md

key-decisions:
  - "Also corrected .planning/REQUIREMENTS.md's Out of Scope table row (line 158), which independently stated the same disproven premise ('Formula could not be obtained from primary source') that D-12 established false. This was not named in the plan's action text or files_modified beyond the single REQ-P8-04 line, and it makes the file-level diff two changed lines instead of the one the plan's own acceptance criteria describe — but leaving it would have (a) left a direct contradiction two lines below the corrected requirement, in the same file, on the same topic, and (b) failed the plan's own acceptance criterion requiring 'obtained from primary source' to be absent from the whole file. Verified via git diff that no other line in either file changed."

requirements-completed: [REQ-P8-04, REQ-P8-05]

coverage:
  - id: D1
    description: "ROADMAP success criterion 3 asks for a test against the Deng & Hu (2015) published counterexample (the time-to-success case, true effect -26 msec vs the naive formula's -18 msec), not a published value the paper does not contain"
    requirement: "REQ-P8-04"
    verification:
      - kind: other
        ref: "python3 -c \"...print('published counterexample' in t)\" -> True; python3 -c \"...print('published value' in t)\" -> False"
        status: pass
    human_judgment: false
  - id: D2
    description: "ROADMAP success criterion 4 states the entry condition as the per-unit-data requirement of Formula (3), not the availability of the paper"
    requirement: "REQ-P8-04"
    verification:
      - kind: other
        ref: "python3 -c \"...print('obtained from primary source' in t)\" -> False (ROADMAP.md)"
        status: pass
    human_judgment: false
  - id: D3
    description: "REQUIREMENTS.md carries the same corrected entry condition as the roadmap so the two documents cannot disagree, across both places the premise appeared"
    requirement: "REQ-P8-04"
    verification:
      - kind: other
        ref: "python3 -c \"...print('obtained from primary source' in t)\" -> False (REQUIREMENTS.md, after correcting both REQ-P8-04 and the Out of Scope row)"
        status: pass
      - kind: other
        ref: "python3 -c \"...print('Formula (3)' in t)\" -> True (REQUIREMENTS.md)"
        status: pass
    human_judgment: false
  - id: D4
    description: "Every amended sentence describes something that already exists in the repository — the counterexample test in tests/test_dsx.py, the section 6.5 row in brief.md, DSX-INT-030's docstring's additive-only paragraph — rather than an intention"
    verification:
      - kind: human
        ref: "backstop must-have — cross-checked amended prose against dsx/mathx.py's diluted_effect docstring, tests/test_dsx.py::test_diluted_effect_naive_and_true_values_differ_for_time_to_success, and brief.md:376's gated-backlog row, all of which already state the -26/-18 msec pair and the Formula (3) per-unit-data blocker"
        status: pass
    human_judgment: true
  - id: D5
    description: "No committed test that scans planning documents for retired bound misattributions goes red as a result of these edits"
    verification:
      - kind: unit
        ref: "python3 -m unittest tests.test_known_bad_corpus -v (18/18 pass, including test_no_planning_document_misattributes_the_prior_averaged_bound)"
        status: pass
    human_judgment: false

metrics:
  duration: 35min
  completed: 2026-08-13
---

# Phase 8 Plan 06: Roadmap and requirements corrections Summary

**Reworded ROADMAP.md Phase 8 success criteria 3 and 4, and REQUIREMENTS.md's REQ-P8-04, so both documents state a Phase 8 bar that is achievable and matches what the Deng & Hu (2015) paper actually says and what the code actually does — and, discovering the same disproven premise repeated a second time in REQUIREMENTS.md's Out of Scope table, corrected that too.**

## What was built

**Task 1 — three scoped edits, one commit.** `.planning/ROADMAP.md` Phase 8 success
criterion 3 asked for a test asserting the dilution identity "against the Deng & Hu
(2015) published value." Primary-text research (recorded in 08-CONTEXT.md D-10) read
the full camera-ready paper and found no additive worked example anywhere in it —
every number in the paper is for a ratio metric, so the original wording asked for
something the paper does not contain. The criterion now asks for a test against the
paper's own published counterexample: the time-to-success case, where the paper
reports a true effect of −26 msec against the naive formula's −18 msec. Because
time-to-success is itself a ratio metric, this same test simultaneously proves the
additive-only scope boundary criterion 4 requires — this is a factual correction, not
a lowered bar.

Success criterion 4 and REQ-P8-04 both gave the entry condition for shipping
ratio-metric dilution as "the Deng & Hu (2015) ratio-metric equation is obtained from
primary source." The paper is freely and publicly available and its ratio equation —
Formula (3), §3.3 — is readable today, so that condition was already met and would
have unblocked the item immediately, which was never the intent (08-CONTEXT.md D-12).
Both are rewritten to name the real, falsifiable blocker: Formula (3) sums over
individual users and has no closed-form scalar multiplier, so it needs per-unit data
a declaration-only gate never has — and the item may be permanently out of scope for
such a gate rather than merely deferred. Both amendments carry a parenthetical
recording what the previous wording claimed and why it was corrected, so the change
reads as a labelled correction rather than quiet slippage, per the plan's own
repudiation-threat mitigation (T-8-15).

REQ-P8-04 was rewritten to carry the identical corrected entry condition in the same
one-line style every other requirement in the file uses, so a reader of only one
document cannot reach a different conclusion than a reader of the other. The
requirement's leading half (ratio-metric dilution out of scope for v2.0.0, recorded
in the gated backlog) and its checkbox state were left untouched, and no other
requirement in the file was renumbered, reordered or reworded.

**Discovered during Task 1, not named in the plan's files_modified: a second
occurrence of the same false premise.** `.planning/REQUIREMENTS.md`'s Out of Scope
table (line 158) independently stated "Formula could not be obtained from primary
source" as the reason ratio-metric dilution is out of scope — the exact premise D-12
established is false, sitting forty-seven lines below the now-corrected REQ-P8-04
line, on the same topic. The plan's own acceptance criteria require the phrase
"obtained from primary source" to be absent from the whole of REQUIREMENTS.md, which
is unsatisfiable while this row stood unedited. Corrected it to name the same Formula
(3) per-unit-data blocker, with the same parenthetical-correction pattern used
elsewhere in this plan.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 — Bug, discovered during verification] REQUIREMENTS.md's Out of Scope table row independently carried the disproven "obtained from primary source" premise**
- **Found during:** Task 1, running the plan's own acceptance-criteria check
  (`'obtained from primary source' in REQUIREMENTS.md` → expected `False`) after
  editing only the REQ-P8-04 line as the plan's action text literally describes.
- **Issue:** The check still returned `True`. `.planning/REQUIREMENTS.md:158`, the
  ratio-metric dilution row in the "Out of Scope — v2.0.0" table, states the same
  disproven premise the REQ-P8-04 edit exists to remove, independently of it. This
  row is not one of REQ-P8-01…REQ-P8-06 and was not named in the plan's `<action>`
  text, `<read_first>` list, or `files_modified`, so it fell outside the plan's
  literal scope — but leaving it unedited both (a) contradicted the just-corrected
  requirement two rows above it, in the same file, on the same topic, and (b) failed
  the plan's own acceptance criterion.
- **Fix:** Rewrote the row to name the same Formula (3) per-unit-data blocker used in
  the ROADMAP and REQUIREMENTS edits, with a parenthetical recording the correction.
- **Files modified:** `.planning/REQUIREMENTS.md` (one additional line, beyond the
  REQ-P8-04 line the plan's action text names)
- **Verification:** `python3 -c "...print('obtained from primary source' in t)"` on
  `.planning/REQUIREMENTS.md` now prints `False`; `git diff HEAD~1 --
  .planning/REQUIREMENTS.md` shows the change confined to exactly these two lines,
  no other requirement or table row touched.
- **Committed in:** `cb3c455` (the plan's single commit)

**Consequence for this plan's own acceptance criteria:** the plan states
`git diff HEAD~1 -- .planning/REQUIREMENTS.md` should show "exactly one changed
line, and that line begins with `- [ ] REQ-P8-04`." As executed, the diff shows two
changed lines — the REQ-P8-04 line and the Out of Scope table row. This criterion,
as literally written, is unsatisfiable jointly with the plan's own "no false premise
anywhere in REQUIREMENTS.md" criterion (Task 1 verified this by running the check
before deciding to touch the second line). Given the plan's stated purpose — "the
roadmap and requirements both state a Phase 8 bar that... matches what the sources
say" — and the threat model's Tampering mitigation (T-8-14) being about preventing a
destructive *whole-file* rewrite, not about limiting a scoped correction to exactly
one line, truthfulness was prioritized. The resulting diff remains a scoped
line-level replacement (two lines, not a whole-file write), and `git diff` confirms
no content outside these two lines and the ROADMAP Phase 8 block was touched.

**Total deviations:** 1 auto-fixed (Rule 1, bug — a second, independent instance of
the exact premise this plan exists to correct, discovered by running the plan's own
acceptance check rather than assumed clean)
**Impact on plan:** One additional line changed in REQUIREMENTS.md beyond the plan's
literal one-line description. No scope creep beyond the same correction applied a
second time to the same disproven claim; no other requirement, table row, or phase's
content was touched.

## Self-Check: PASSED

- FOUND: .planning/ROADMAP.md (Phase 8 success criteria 3 and 4 amended)
- FOUND: .planning/REQUIREMENTS.md (REQ-P8-04 and the Out of Scope ratio-metric-dilution row amended)
- FOUND commit cb3c455 in `git log --oneline`
- `python3 -c "...print('published counterexample' in t)"` on ROADMAP.md → True
- `python3 -c "...print('published value' in t)"` on ROADMAP.md → False
- `python3 -c "...print('obtained from primary source' in t)"` on ROADMAP.md → False
- `python3 -c "...print('obtained from primary source' in t)"` on REQUIREMENTS.md → False
- `python3 -c "...print('Formula (3)' in t)"` on REQUIREMENTS.md → True
- `python3 -m unittest tests.test_known_bad_corpus -v` — 18 tests, OK
- `python3 -m unittest discover -s tests` — 518 tests, OK (skipped=2), matching the pre-plan baseline
- `sh scripts/check.sh` — all checks passed
- `git diff --stat HEAD~1` — exactly 2 files changed (.planning/ROADMAP.md, .planning/REQUIREMENTS.md)
- Working tree clean after the commit
