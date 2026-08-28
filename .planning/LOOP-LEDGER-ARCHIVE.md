# LOOP-LEDGER-ARCHIVE — v2.2 Analytic Surface

Overflow evidence and archived Log entries, kept off the hot-path `LOOP-LEDGER.md`
(brief §5). Each `## <unit-id>` holds the full evidence a checkbox line only points at.

## S1-2 — Phase 13 plan (full evidence)

**Firing 2026-08-28T17:55Z.** Reconcile-first at HEAD `2ad38c4` (branch up-to-date with
origin) surfaced **two ledger/repo disagreements**, both corrected here (repo is the fact):

1. **The S1-1-flagged "ROADMAP repoint prerequisite" for S1-2 is FALSE for planning.**
   S1-1 recorded that `init phase-op --phase 13` → `phase_found:false` (v2.2 phases sit
   under `## Queued milestone`) blocks `/gsd-plan-phase 13`. But plan-phase does not use
   that verb — its workflow (`gsd-core/workflows/plan-phase.md §1`) calls
   `query init.plan-phase`. Measured this firing: `init.plan-phase 13` →
   `phase_found:true`, `phase_dir:.planning/phases/13-task-playbooks-that-fill-the-spec`,
   `has_context:true`, `plan_count:3`; and `roadmap.get-phase 13` → `found:true` (the
   `### Phase 13` heading parses fine even under "Queued milestone"). So **no ROADMAP
   repoint was needed for S1-2**, and none was done (a full active-milestone restructure
   is a bigger single-writer edit that should not be done speculatively). **Open for S1-3:**
   verify whether `/gsd-execute-phase 13`'s own init verb resolves phase 13 before assuming
   a repoint is needed; `init.phase-op --phase 13` is still `phase_found:false`, so any
   command keyed to *that* verb (not `init.plan-phase`) will need the repoint first.

2. **The prior S1-2 firing was interrupted mid-generation.** It left three untracked,
   internally-inconsistent plan drafts: `13-01/02/03-PLAN.md` (13-01 forward-references
   plans "13-04" and "13-05" that were never written), and **`13-03` was truncated on
   disk** (103 lines, 1 of its 2 tasks, ending mid-`<automated>`, missing Task 2 +
   threat_model/verification/success_criteria/output). STATE showed `total_plans:0`,
   "Resume file: None" — no record of the attempt. Requirements REQ-P13-03/-04/-05/-06
   were therefore uncovered.

**Resolution (preserve good work, don't discard):** kept the three good CONTEXT-faithful
drafts; spawned `gsd-planner` (opus, §3 planning routing) to (a) author the two missing
plans `13-04` (REQ-P13-04 tier routing D-05 + REQ-P13-05 executor bullet D-06) and
`13-05` (REQ-P13-06 catalogue set-diff D-07), and (b) repair the truncated `13-03`
(added Task 2 = dsx-narrate What/So What/Now What per D-04, template-only no `DSX-NAR`
mint; plus the four closing sections). Then spawned an independent `gsd-plan-checker`
(opus, §3 plan-check routing) over all five as the S1-2 gate — given the artifacts, not
the orchestrator's conclusions, so the gate is meaningful.

**Gate result — gsd-plan-checker verdict: REVISE → (1 repair) → PASS.**
- Coverage table it returned: SC1→13-01+13-02+13-01T3 register; SC2→13-03T1; SC3→13-03T2;
  SC4→13-04T1; SC5→13-04T2; SC6→13-05. Scope-bound (REQ-P13-06), gate-path purity
  (D-01/D-02), D-04/D-08 caveats, wave ordering and single-writer discipline all held.
- **One blocking finding B1:** 13-01 Task 3 (sole `capability.json` writer) registered only
  `dsx-cohort`+`dsx-funnel`; `dsx-root-cause`+`dsx-segment` (authored by 13-02, which
  correctly never touches the manifest) were left unregistered → SC1/REQ-P13-01
  ("…are registered in capabilities/dsx/capability.json") would fail. Verified by the
  checker against the live manifest (9 skills, none of the four new).
- **Repair (one attempt, §5):** sent B1 back to `gsd-planner`; it updated 13-01 Task 3 to
  append+assert all four names, and fixed every place the two-name assumption leaked
  (must_haves truth #3, objective, artifacts, key_link, verification, success_criteria,
  threat_model prose). Single-writer preserved (13-01 stays sole manifest writer).
- **Orchestrator re-verification (not trusted from the subagent report, brief rigor bar):**
  `13-01` Task 3 `<action>` appends all four; `<acceptance_criteria>` and
  `<verify><automated>` both assert
  `all(n in s for n in ('dsx-cohort','dsx-funnel','dsx-root-cause','dsx-segment'))`;
  root-cause/segment now appear 9× each in 13-01; 13-01 remains the only `files_modified`
  writer of `capability.json`; 13-01 structurally whole (3 tasks, all sections).

**Final set (all five structurally complete; requirements union = REQ-P13-01…06):**
| Plan | wave | depends_on | requirements | files_modified |
|---|---|---|---|---|
| 13-01 | 1 | [] | REQ-P13-01 | skills/dsx-cohort, skills/dsx-funnel, capabilities/dsx/capability.json |
| 13-02 | 1 | [] | REQ-P13-01 | skills/dsx-root-cause, skills/dsx-segment |
| 13-03 | 1 | [] | REQ-P13-02,-03 | skills/dsx-explore-data, skills/dsx-narrate |
| 13-04 | 1 | [] | REQ-P13-04,-05 | skills/dsx-scope-analysis, capabilities/dsx/fragments/executor.md |
| 13-05 | 2 | [13-01,13-02,13-03,13-04] | REQ-P13-06 | tests/fixtures/finding-codes-phase12.md, tests/test_finding_catalogue_invariant.py |

Every file written by exactly one plan (single-writer safe). 13-05 (phase-wide
catalogue certification) is wave 2, depends on the wave-1 plans.

**Non-blocking nits from the checker — carry into S1-3 execute / S1-4 review (not gate blockers):**
1. **Anti-parallel-advice verify over-rejects** in 13-01/13-02/13-04: the form
   `! ( grep -hEi '<thresholds>' FILE | grep -q 'DSX-\|.' )` — `grep -q 'DSX-\|.'` matches
   *any* non-empty line (the `.` alternative), so it fails on a threshold line **even when
   attributed to a `DSX-` code on the same line**, contradicting the `<acceptance_criteria>`
   (`… | grep -v 'DSX-'`) which permits attributed thresholds. Errs safe (over-rejects, no
   false-pass), but can force an avoidable execute-time revision if an executor writes an
   attributed number. Fix at execute: make verify match acceptance
   (`grep -Ei '<thresholds>' FILE | grep -v 'DSX-' | grep -q . && exit 1 || exit 0`) or
   tighten acceptance prose to "no threshold numbers at all."
2. **13-03 Task 2 `DSX-NAR` count check** asserts exactly one distinct `DSX-NAR` code
   (`… | sort -u | wc -l -eq 1`), which false-fails if the shipped `dsx-narrate/SKILL.md`
   already cites a second `DSX-NAR` code. Low risk (CONTEXT asserts only `DSX-NAR-030` at
   :55) — executor should confirm the pre-edit baseline is 1.
3. **13-04 Task 1 anti-mutation check** greps only literal `config-set`; a different mutator
   invocation would slip past. Consider also asserting no bare `workflow.`/`mode=` assignment
   command in the tier block.
4. **Chart-admissibility (D-02) has no automated catch** — prose like "only X marks allowed"
   is caught only by manual read (as stated in the plan). Acceptable; flag for S1-4 review.

Agents: planner `aa1e8433ad6f1cdee` (author 13-04/05, repair 13-03, apply B1);
checker `afceb3a3939e06940` (independent gate).
