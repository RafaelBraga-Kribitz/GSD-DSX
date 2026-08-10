---
phase: 06-contract-extension-decision-record-paradigm-manifest
plan: 04
subsystem: docs
tags: [readme, project-md, reversals, migration, suppressions, d-05]

# Dependency graph
requires:
  - phase: 06-contract-extension-decision-record-paradigm-manifest (plan 03)
    provides: "dsx/suppressions.py DSX-SPEC-070 and scripts/gen-finding-catalogue.py --check (Citation:/Reference value:/Structural criterion:/# D-05: <CODE>) — cited by name in the README additions"
provides:
  - ".planning/REVERSALS.md with the D-14 reversal-record template, the defined SELF-001 convention, and REV-001 transcribed from brief.md"
  - "README.md 'Migrating a pre-v2.0.0 spec' section documenting suppressions[] as the interim/grandfather path with its authority requirement"
  - "README.md 'Known limits' section stating the frame-that-lies-passes caveat as a claim about the tool"
  - "README.md 'Two tiers of evidentiary rigour' subsection naming the D-05 citation/test-linkage convention"
  - "PROJECT.md version rationale corrected to match D-10's CRITICAL/plan gate point"
affects: [06-05, 06-06, 06-07, 06-08, 06-09, 06-10, phase-07, phase-08, phase-09, phase-10, phase-11, phase-12]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "REV-NNN sequential, never-reused reversal-record ids, filed before/with the reversing change"
    - "Two-tier evidentiary-rigour framing (v2.0.0 codes cited + tested; pre-existing codes allow-listed and shrinking)"

key-files:
  created:
    - .planning/REVERSALS.md
  modified:
    - README.md
    - .planning/PROJECT.md

key-decisions:
  - "PROJECT.md's version-rationale amendment is not filed as a D-14 reversal — the sentence sits outside both brief.md section 4's D-table and PROJECT.md's M-table (per 06-CONTEXT.md D-10's explicit ACTION note), so it was corrected with a scoped edit instead"
  - "Known limits and the D-05 two-tier subsection were split into two headings (## Known limits, ### Two tiers of evidentiary rigour) rather than one undifferentiated section, since they are two separate claims a reader should not conflate"

patterns-established:
  - "REVERSALS.md as the durable home for D-14 reversal records, distinct from and never overlapping SELF-001's undetectable-by-construction residual gap"

requirements-completed: [REQ-P6-14, REQ-P6-15]

coverage:
  - id: D1
    description: ".planning/REVERSALS.md exists with the D-14 template (Reversed/New evidence/What would have made the original correct/What did not change), a defined SELF-001 convention, and REV-001 transcribed as a worked entry"
    requirement: "REQ-P6-14"
    verification:
      - kind: other
        ref: "python3 -c \"...\" checking REV-001, SELF-001, and all four D-14 field headings are present in .planning/REVERSALS.md, len(text) > 800"
        status: pass
    human_judgment: true
    rationale: "Mechanical check confirms the required strings exist; whether the template is genuinely copyable without consulting brief.md and whether SELF-001 is defined (not merely mentioned) is a prose-quality judgment per the plan's own <verify><human-check> requirement."
  - id: D2
    description: "README documents suppressions[] + authority as the pre-v2.0.0 migration path, naming DSX-SPEC-070, without softening the authority requirement into a suggestion or presenting suppression as an alternative to filling the frame"
    requirement: "REQ-P6-15"
    verification:
      - kind: other
        ref: "python3 -c \"...\" checking suppressions[], authority, DSX-SPEC-070 are all present in README.md in migration context"
        status: pass
    human_judgment: true
    rationale: "The plan's own must_haves mark this verification: backstop (README prose quality is a judgement the verifier cannot confirm with explicit evidence) and carries an explicit prohibition against softening the authority requirement — string presence does not prove tone; a human read of the section is required."
  - id: D3
    description: "README states the known limit (a frame that lies passes) plainly, distinct from the dsx-ml-integrity-auditor design-notes paragraph, and states the two tiers of D-05 evidentiary rigour with the Citation:/Reference value:/Structural criterion:/# D-05: <CODE> convention and gen-finding-catalogue.py --check as the enforcement mechanism"
    requirement: "REQ-P6-15"
    verification:
      - kind: other
        ref: "python3 -c \"...\" checking '## Known limits', 'a frame that lies passes', 'gen-finding-catalogue.py', 'Citation:', 'Structural criterion:', '# D-05:' are present"
        status: pass
    human_judgment: true
    rationale: "backstop verification per must_haves; string presence confirms the content exists, not that it reads as plain/unsoftened/unburied prose to a reader who has not read brief.md."
  - id: D4
    description: "PROJECT.md's version rationale no longer states the frame block becomes required at verify/ship; it now states required from plan, matching D-10's CRITICAL severity"
    requirement: "REQ-P6-15"
    verification:
      - kind: unit
        ref: "python3 -c \"assert 'required at verify/ship' not in PROJECT.md and 'required from plan' in PROJECT.md\""
        status: pass
      - kind: other
        ref: "git diff --stat .planning/PROJECT.md — confined to the version-rationale sentence (2 lines changed)"
        status: pass
    human_judgment: false

# Metrics
duration: 15min
completed: 2026-08-07
status: complete
---

# Phase 6 Plan 4: Reversal Ledger and Documentation Deliverables Summary

**Created `.planning/REVERSALS.md` with the D-14 reversal template and SELF-001 convention, documented the `suppressions[]` migration path and the known limit in README.md, and corrected PROJECT.md's version rationale to match D-10's CRITICAL/plan gate point — three files, zero code.**

## Performance

- **Duration:** ~15 min
- **Completed:** 2026-08-07T22:23:55Z
- **Tasks:** 2
- **Files modified:** 3 (1 created, 2 modified)

## Accomplishments

- `.planning/REVERSALS.md` created with a preamble scoping which decisions require a reversal record, a copyable D-14 template (id/date, Reversed, New evidence, What would have made the original correct, What did not change), a fully defined `SELF-001` convention (what triggers it, that it is a convention not a gate check per M-05, and the acknowledged enforcement gap from `brief.md` section 6.6 item 3), and `REV-001` transcribed as the first real entry.
- README.md gained a `### Migrating a pre-v2.0.0 spec` section under `## The contract`, naming `suppressions[]` + `authority` as the interim path, cross-referencing the existing `### Finding suppressions` section rather than duplicating its YAML, and stating plainly that a suppression is an attributable decision, not a way to make a finding disappear (satisfying the plan's prohibition).
- README.md gained a `## Known limits` section stating "a frame that lies passes" as a claim about the tool, explicitly distinguished from the `dsx-ml-integrity-auditor` design-notes paragraph (which covers misdeclared pipeline code, not an internally-coherent-but-false frame).
- README.md gained a `### Two tiers of evidentiary rigour` subsection naming the `Citation:`, `Reference value:`/`Structural criterion:`, and `# D-05: <CODE>` conventions, and `scripts/gen-finding-catalogue.py --check` as the mechanism enforcing tier one.
- `.planning/PROJECT.md`'s version rationale corrected from "required at verify/ship" to "required from plan", with a scoped two-line edit that leaves no superseded wording behind.

## Task Commits

Each task was committed atomically:

1. **Task 1: Create .planning/REVERSALS.md with the D-14 template and the SELF-001 convention (REQ-P6-14)** - `11f9181` (docs)
2. **Task 2: Document the migration path, the known limit and the two tiers of D-05 rigour (REQ-P6-15)** - `b14e2ff` (docs)

_Both tasks are documentation-only; TDD mode is active project-wide but these tasks are exempt per the doc-only carve-out (no `<behavior>` block, no source files touched)._

## Files Created/Modified

- `.planning/REVERSALS.md` - D-14 reversal template, SELF-001 convention definition, REV-001 worked entry
- `README.md` - Migration section, Known limits section, D-05 two-tier subsection
- `.planning/PROJECT.md` - Version-rationale sentence corrected to match D-10's gate point

## Decisions Made

- The PROJECT.md version-rationale correction was made as a plain scoped edit, not filed as a `REV-NNN` reversal record, per 06-CONTEXT.md's explicit note that the rationale sentence sits outside both `brief.md` section 4's D-table and PROJECT.md's M-table.
- Split the known-limit statement and the D-05 tiers into two separate headings (`## Known limits` / `### Two tiers of evidentiary rigour`) rather than one section, since they are distinct claims (tool honesty caveat vs. catalogue evidentiary bar) that a reader should not conflate.
- Kept the "a frame that lies passes" sentence on a single unwrapped line in the README source so the literal phrase matches the plan's mechanical verification command (a markdown line-wrap would otherwise split the phrase across a newline and fail the substring check even though it renders identically).

## Deviations from Plan

None - plan executed exactly as written. Both README and PROJECT.md edits match the plan's `<action>` instructions verbatim; no Rule 1-4 auto-fixes were needed since this plan touches no code path.

## Issues Encountered

During drafting, the mechanical verification script for both README.md ("a frame that lies passes") and PROJECT.md ("required from plan") initially failed because the literal target phrases were split across a markdown line-wrap or interrupted by a backtick-wrapped word (`` required from `plan` `` broke the substring match on "required from plan"). Resolved by rewording to keep both target phrases as unbroken literal substrings while preserving the intended meaning; re-ran the plan's own verification commands until both passed.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- REQ-P6-14 and REQ-P6-15 are complete; the `.planning/REVERSALS.md` ledger is seeded and ready to receive future `REV-NNN` entries from any phase that reverses a D-table/M-table decision.
- README now documents the migration path before Phase 6's `DSX-SPEC-080/081` land at CRITICAL severity from `plan` onward (shipped in earlier Phase 6 plans this wave), so users hitting the new blocking findings have a documented, attributable interim path.
- The `# D-05: <CODE>` test-linkage convention is now documented publicly, binding Phases 7-12 as they add new finding codes.
- No blockers for the remaining Phase 6 plans (05-10) or for Phase 7 onward.

---
*Phase: 06-contract-extension-decision-record-paradigm-manifest*
*Completed: 2026-08-07*

## Self-Check: PASSED

- FOUND: .planning/REVERSALS.md
- FOUND: README.md (modified)
- FOUND: .planning/PROJECT.md (modified)
- FOUND: 11f9181 (git log confirms)
- FOUND: b14e2ff (git log confirms)
