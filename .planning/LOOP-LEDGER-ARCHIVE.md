# LOOP-LEDGER-ARCHIVE — v2.2 Analytic Surface

Overflow evidence and archived Log entries, kept off the hot-path `LOOP-LEDGER.md`
(brief §5). Each `## <unit-id>` holds the full evidence a checkbox line only points at.

## Log (archived)

Oldest-first. Moved off the hot-path `LOOP-LEDGER.md` Log per brief §5; full firing history preserved here, never deleted.

2026-08-28T14:40Z | milestone-transition | v2.0.0 SHIPPED (merged to main `c81fc6b`, tag `v2.1.0` pushed, both verified on origin); v2.2 Analytic Surface opened on branch `gsd/v2.2.0-analytic-surface`; loop repointed | v2.0.0 loop artifacts archived to `.planning/milestones/v2.0.0-LOOP-*`; suite 1221 OK + `scripts/check.sh` all checks passed on the merged tree before push
2026-08-28T15:02Z | S0-1 | DONE — GSD state reconciled onto v2.2. Reconcile OK first: HEAD `33dc7de`, branch up-to-date with origin, ledger==repo (no correction needed). Frontmatter already at v2.2/Analytic Surface/executing/current_phase 13/0-of-4 from the transition commit; body was still 198 lines of v2.0.0 detail contradicting it, so reconciled to a 79-line GSD-template digest — v2.0.0 history preserved in `MILESTONES.md` + `.planning/milestones/v2.0.0-*`, not deleted. | Gate `node ~/.claude/gsd-core/bin/gsd-tools.cjs query init.milestone-op` exit 0: milestone_version v2.2, milestone_name "Analytic Surface", phase_count 4, completed_phases 0, phases_dir_exists true; `.planning/phases/` = `.gitkeep` only; STATE.md 79 lines (< 100-line template cap). Next unblocked = S0-2.
2026-08-28T15:40Z | S0-2 | DONE — v2.2 scope rechecked against shipped v2.0.0 tree. Reconcile OK first: HEAD `4ae156f`, branch up-to-date with origin, ledger==repo (no correction). All 23 reqs (REQ-P13-01…P16-04) re-read against live code via direct grep/ls/Read + a real `gen-finding-catalogue.py --check` (exit 0). Verdict **23/23 still-valid, 0 amendments** → no §4 loud amendment, no HUMAN-QUEUE escalation; milestone needs execution, not re-scoping. Evidence: 5 target skills (`dsx-{cohort,funnel,root-cause,segment,reproduce}`) absent; `VARIANCE_ADJUSTMENTS` = exactly the 4 named members no `cuped` (`dsx/spec.py:264`); `dsx vocab` present; gate path pure (no pandas/scipy in `dsx/frame`|`dsx/checks`); no `shapiro` in `skills/`|`dsx/`; `test-selection.md` order matches REQ-P15-06; `brief.md §6.5` + D-08 fixtures present. Recorded (non-amendments): `DSX-REP-*` already exists (11 codes) → material to S3-1; pre-existing double-declare warnings (DSX-SPEC-070/VAL-021/VAL-060) are shipped-tree noise, --check still exit 0 → don't misread at S4-5. Full verdict table: `.planning/v2.2-SCOPE-RECHECK.md`. Next unblocked = S0-3 (Phase 15 D-05 evidence pack → HQ-8).
2026-08-28T15:51Z | S1-1 | DONE — Phase 13 discuss complete; `13-CONTEXT.md` written. Reconcile OK first: HEAD `bdf7393`, branch up-to-date with origin, ledger==repo (S0-1/2/3 all landed, no correction). Ran an **Architect-led (`dsx-analysis-architect`) + Auditor (`dsx-ml-integrity-auditor`) 2-persona round** (both opus/high, concurrent, §4), tie-break rigour>reliability>flexibility — the relevant 2 for a skill-only spec-shape phase. Orchestrator independently re-verified the load-bearing baseline before trusting it: `references/finding-codes.md` Total = **256**, distinct-`DSX-*` grep = **256**, `gen-finding-catalogue.py --check` exit **0** (DSX-VAL-060 double-declare = known shipped-tree noise); `test_finding_catalogue_invariant.py` `_EXPECTED_TOTAL=256` present; narrate `SKILL.md` has 0 "so what", executor fragment has 0 script-preference → both REQ-P13-03/-05 confirmed additive. 8 loud/vetoable decisions D-01..D-08 recorded in CONTEXT (full rationale + citations there). Genuine tie-break made: REQ-P13-06 "assert by diff" → **set-identity diff vs a frozen Phase-12 code-set snapshot**, not count-only (count passes a mint-one/drop-one swap; the ledger says "by diff, not by review"). No §4 escalation (mints nothing, no scope change, non-destructive). No D-05/D-06 owed by Phase 13. **Flagged for S1-2:** ROADMAP still has v2.2 phases under "## Queued milestone" (`:52`) while active `## Milestones`/`## Phases` (`:15`/`:20`) show v2.0.0, so `init phase-op --phase 13`→`phase_found:false`; S1-2 must promote the section to active before `/gsd-plan-phase 13` resolves (structural repoint, requirements unchanged). Gate met: `.planning/phases/13-task-playbooks-that-fill-the-spec/13-CONTEXT.md`. Next unblocked = S1-2 (plan Phase 13; do the ROADMAP repoint first). | evidence: `13-CONTEXT.md`
2026-08-28T16:20Z | S0-3 | DONE — Phase 15 D-05 citation evidence pack assembled into HUMAN-QUEUE.md HQ-8 (prepared, NOT signed — D-05 is the human read). Reconcile OK first: HEAD `541c5b9`, branch up-to-date with origin, ledger==repo (no correction). Pack = 3 per-citation tables with locators + confirmed/unverified split: (1) CUPED — Deng/Xu/Kohavi/Walker 2013 WSDM pp.123–132 DOI 10.1145/2433396.2433413; formulation Ŷ_cv=Ȳ−θ(X̄−E[X]), θ=Cov/Var, Var-reduction 1−ρ²; worked value = 1−ρ² identity (fixture/docstring, not gate-path per D-02) + paper's ≈50 % Bing headline; HIGH, only exact eq#/page left for the read. (2) Survivorship — Brown/Goetzmann/Ibbotson/Ross 1992 RFS 5(4):553–580 DOI 10.1093/rfs/5.4.553 (+ Elton/Gruber/Blake 1996); MEDIUM, open question = does the finance criterion transfer to a cohort/funnel declaration check (else stays §6.5). (3) Changing-denominator — Crook/Frasca/Kohavi/Longbotham 2009 KDD pp.1105–1114 DOI 10.1145/1557019.1557139 (+ Kohavi/Tang/Xu 2020 book); MEDIUM, flagged the out-of-scope boundary vs Deng&Hu-2015 dilution (brief line 450) so S4 won't re-mint. D-06 numbering left to S4-1; no code assigned. No §4 persona round needed (evidence-gathering, not a decision). Sources corroborated across independent web results 2026-08-28; not a D-05 sign-off. Gate met: HQ-8 has per-citation table + locators + confirmed-vs-unverified. Next unblocked = S1-1 (Phase 13 discuss). | evidence: `.planning/HUMAN-QUEUE.md` HQ-8

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

## S2-2 — Phase 14 plan (full evidence)

**Firing 2026-08-28 (S2-2).** Reconcile-first at HEAD `ba6a218` (branch up-to-date with
origin) found ledger == repo — S2-1 (Phase 14 discuss) was the last landed commit, no
correction owed.

**Method.** Spawned `gsd-planner` (opus via adaptive, §3) to author the plan set from
`14-CONTEXT.md` + ROADMAP §Phase 14 + REQUIREMENTS REQ-P14-01..06, then the independent
`gsd-plan-checker` (opus) as the gate. Orchestrator re-verified every load-bearing claim
itself (brief §5) — not trusted from either subagent — at both frontmatter and plan-body
level.

**Plan set (5 plans):**
| Plan | Wave | requirements | Files (product) |
|---|---|---|---|
| 14-01 | 1 | REQ-P14-01 | `docs/dsx/learnings/{README.md,2026-08-28-<exemplar>.md}`, `skills/dsx-scope-analysis/SKILL.md` (plan:pre learnings search), `capabilities/dsx/fragments/researcher.md` |
| 14-02 | 1 | REQ-P14-02 | `templates/DATA-DICTIONARY.md`, `skills/dsx-explore-data/SKILL.md` |
| 14-03 | 1 | REQ-P14-03 | `templates/DISCLOSURE-research.md`, `skills/dsx-narrate/SKILL.md` |
| 14-05 | 1 | REQ-P14-06 | `tests/test_gate_path_hermetic.py` |
| 14-04 | 2 | REQ-P14-04, REQ-P14-05 | `docs/operating-guide.md`, all 13 DSX skills' `description` frontmatter, `.claude/commands/{dsx-scope,dsx-eda}.md` |

**Planner discretion decisions (loud, §4 — no mint, no scope change, vetoable via daily summary):**
- REQ-P14-01 producer = existing `gsd-extract-learnings` (referenced, never edited); DSX ships
  only the dated home, fixed schema, one seeded exemplar. Keeps 14-01 off the `dsx-narrate`
  file so wave-1 single-writer holds.
- `.claude/commands/*.md` shims = shipped (2: `dsx-scope`, `dsx-eda`), explicitly optional /
  Claude-Code-only / non-load-bearing sugar; alias table is the portable path.
- `tests/test_gate_path_hermetic.py` = shipped (14-05): asserts no pandas/scipy/numpy/csv in
  the import closure of any `GATE_PROFILES` module and `dsx.profiler` not in `dsx.checks.dq`'s
  closure — a standing guard above the current implicit purity.

**Gate = PASS (independent `gsd-plan-checker`), 0 blocking.** Orchestrator re-verified:
- Requirements union == exactly {REQ-P14-01..06} (per-plan frontmatter extracted from disk).
- Single-writer-per-wave holds: wave-1 plans (01/02/03/05) pairwise file-disjoint
  (scope-analysis vs explore-data vs narrate vs tests); 14-04 sole wave-2 plan,
  `depends_on: [14-01,14-02,14-03]`, re-edits the three shared skills' `description` only.
- Gate-path purity: no `dsx/**/*.py` and no `capability.json` in any `files_modified`
  (`researcher.md` is a prompt fragment, same class 13-04 edited). Every `report.add` mention
  in the plans is a prohibition/explanation, never an ADD intent. `data_storage` appears only
  inside a negative guardrail grep; no `capability.json aliases` key.
- REQ-P14-05 documented-skip fidelity: 14-04 carries the four D-06 honesty claims in force
  (`FileChanged`x5, `config.json`x3, `supported:["*"]`x8, `DSX-DQ-001`x13, "hooks stays []"x12);
  no `FileChanged` binding.
- 14-05 gate is real: `gen-finding-catalogue.py --check && unittest ...invariant &&
  git status --porcelain -- dsx/ empty && grep -c report.add dsx/cli.py -eq 0`.

**3 non-blocking nits carried to S2-3/S2-4 (from the checker; none blocks execution):**
1. REQ-P14-03 "golden" (D-04) ships as a *by-construction* structural guarantee (guard on
   the literal `research` value), not a runnable golden test — defensible for a prompt skill
   (a real golden needs a non-deterministic LLM run). 14-03's verification block should state
   the substitution explicitly at execute time.
2. 14-04 Task 1 automated grep covers D-06 claims 2/3/4 + `DSX-DQ-001` but under-asserts
   claim (1) (portable floor has no file-drop event) and the exact `--pk/--time` flags of the
   analyst-invoked `dsx profile` command — the task *action* mandates both, so execution
   produces them; only the machine-check is looser. Optional tighten at execute.
3. 14-01 Task 2's `-e '- Grep'/'- Glob'` conjunct checks pre-existing tool grants (regression
   guard) rather than the new search step; the `docs/dsx/learnings` + `searched dated
   learnings` conjuncts carry the real positive assertion. Harmless.

Agents: planner `a6082e0cfaaabaa6c`; checker `ab0e4c082146f3169`.
