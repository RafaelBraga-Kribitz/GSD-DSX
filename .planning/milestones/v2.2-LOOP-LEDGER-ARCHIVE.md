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
2026-08-28T17:55Z | S1-2 | DONE — Phase 13 planned; 5-plan set (13-01..05) passes the plan-checker gate. Reconcile-first at HEAD `2ad38c4` found TWO ledger/repo disagreements, both corrected (repo is the fact): (1) S1-1's "ROADMAP repoint is a prerequisite for S1-2" is FALSE — plan-phase uses `init.plan-phase` (→`phase_found:true`, plan_count 3), not `init.phase-op` (still false); no repoint done, none needed for planning. Open for S1-3: check execute-phase's init verb before assuming a repoint. (2) The prior S1-2 firing was interrupted mid-generation — left 3 untracked drafts (13-01 forward-refs phantom 13-04/05) with **13-03 truncated on disk** (1 of 2 tasks, no closing sections); REQ-P13-03/-04/-05/-06 uncovered. Resolution: kept the 3 good drafts; `gsd-planner` (opus) authored the missing 13-04 (tier D-05 + executor D-06) & 13-05 (catalogue set-diff D-07) and repaired 13-03 (added dsx-narrate What/So What/Now What, D-04, no `DSX-NAR` mint). Gate: independent `gsd-plan-checker` (opus) → **REVISE** (1 blocker B1: 13-01 Task 3 registered only cohort+funnel, not root-cause+segment → SC1 fail) → **1 repair** → orchestrator re-verified (13-01 Task 3 now appends+asserts all four names; sole manifest writer; 3 tasks whole). Checker also PASSED coverage SC2–6, gate-path purity D-01/D-02, D-04/D-08, waves, single-writer. 4 non-blocking nits (verify-block robustness) logged for S1-3/S1-4. Next unblocked = S1-3 (execute all Phase 13 plans). | evidence: `.planning/LOOP-LEDGER-ARCHIVE.md#S1-2`; plans `13-0{1..5}-PLAN.md`
2026-08-28T18:33Z | S1-3 (partial, 2/5) | Phase 13 execution started; 2 of 5 plans executed, orchestrator-verified, pushed. **Reconcile-first** at HEAD `d99891d` (branch up-to-date w/ origin): ledger==repo. `d99891d` = interactive HQ-8 verdict commit (cite1 CUPED + cite3 changing-denominator confirmed at locator; cite2 survivorship does-not-transfer → unshipped) — already in HUMAN-QUEUE "Answered", no firing Log owed. **CLOSED the S1-1/S1-2 "ROADMAP repoint" open item as a query-syntax artifact, not a real blocker:** `init execute-phase --phase 13` passes the phase as `args[2]='--phase'` → `phase_found:false`; the POSITIONAL form `init execute-phase 13` → `phase_found:true`, 5 plans, all 6 REQ ids. Root-caused in gsd-tools source (`init-command-router.cjs:34`) + a direct `cmdInitExecutePhase` call. **No ROADMAP edit made** — single-writer file protected from a speculative restructure. **Ceremony execution decisions (loud, operational — non-scope, no persona round):** (a) STAY on ceremony branch, SKIP GSD `handle_branching` (it would fork `gsd/v2.2-analytic-surface` off `origin/main`, orphaning S0/S1); (b) sequential no-worktree executors (`worktree.baseRef=head` so worktrees would be brief-compliant, but sequential direct-commit is simpler+safer headless, no merge-back); (c) executors forbidden from touching STATE/ROADMAP/REQUIREMENTS/LOOP/HUMAN → orchestrator single-writer preserved. **Plans done:** 13-01 (skills `dsx-cohort`+`dsx-funnel` + `capability.json` registers all 4 playbooks; `6c17955`,`716151c`,`b1bc21e`) + 13-02 (skills `dsx-root-cause`+`dsx-segment`; `e5e9a98`,`7c27aef`,`81eb538`). Both **orchestrator-verified**: only `skills/*` + `capability.json` touched, valid JSON w/ 4 skills, zero `dsx/` or tracking-file changes, no new `DSX-*` codes (catalogue file untouched), verify blocks green. Stopped at a clean plan boundary per §1 pacing cap (2 executors + heavy diagnosis). **For S1-4:** confirm every `DSX-*` code the new skills CITE actually exists in `references/finding-codes.md` (skills cite codes in prose; authenticity is an S1-4 / 13-05-catalogue concern, not an execution gate). Next = resume S1-3 at **13-03**. git: branch `gsd/v2.2.0-analytic-surface`, pushed to origin (0 ahead / 0 unpushed after this sync commit).
2026-08-28T19:30Z | S1-4 | DONE — Phase 13 code review + verification, both PASS. Reconcile-first OK at HEAD `bf5748e` (branch up-to-date w/ origin; git log == ledger, last entry was the S1-3 sync commit — no correction). **Loud op-decision (non-scope, consistent w/ S1-3):** ran the review DIRECTLY as orchestrator (opus/high, §3) rather than spawning `gsd-code-reviewer` — the diff is small/bounded (skill md + 1 py test + 1 json + 1 fixture) and I re-ran every gate myself (brief §5, not subagent-trusted). **Review = PASS, 0 blocking, 0 auto-fix (nothing to fix).** Load-bearing checks for a skill-only phase: (1) citation authenticity — all **21/21** cited `DSX-*` codes exist in `references/finding-codes.md`, zero dangling; (2) locator fidelity — spot-checked `dsx/spec.py:22-28`, `spec.py:1046-1055`, `dsx/checks/design.py:362-412` all accurate; (3) file refs — `docs/gsd-tiers.md`+`scripts/gsd-tier.ps1` exist, tier table matches the doc's Tier0/1/2 (`enforce` off/on/on + `mode=interactive`@T2); (4) D-01 gate-path pure — 0 `dsx/`|`scripts/*.py` edits (git diff --stat); (5) D-07/REQ-P13-06 zero-mint by set-identity diff (`added=[] removed=[]`, 256); (6) D-02 router discipline + D-08 Coherence-not-Cohort caveat present; the 4 carried S1-2 nits all resolved (nit1 errs-safe & moot; nit2 narrate cites exactly 1 DSX-NAR; nit3 tier block prints not mutates; nit4 chart-admissibility hand-read = clean). **Verification = PASSED, 6/6** REQ-P13-01..06 goal-backward (each mapped to a re-run gate or read locator, incl. REQ-P13-04 "matching docs/gsd-tiers.md" cross-checked). **Gate:** `sh scripts/check.sh` = *all checks passed* (Ran **1222** tests OK; catalogue current; capability conformant 13 skills; gate contract; determinism); `unittest tests.test_finding_catalogue_invariant -v` = 2 OK. Artifacts written: `REVIEW.md` + `VERIFICATION.md` in the phase dir. Stopped at S1-4 boundary per §1 pacing (heavy opus/high review unit). Next unblocked = S1-5 (`/gsd-secure-phase 13` + `/gsd-validate-phase 13`). git: branch `gsd/v2.2.0-analytic-surface`, pushed to origin (0 ahead / 0 unpushed after this commit). | evidence: `13-.../REVIEW.md`, `13-.../VERIFICATION.md`
2026-08-28T19:22Z | S1-5 | DONE — Phase 13 secure + validate, both PASS; Phase 13 ceremony (S1) complete. Reconcile-first OK at HEAD `f4d5e9b` (branch up-to-date w/ origin; git log == ledger — S1-4 was the last landed commit, no correction). **Load-bearing gate verification (all real commands, brief §5 — never trusted from a report):** confirmed `init.phase-op 13` (POSITIONAL) resolves `phase_found:true`/phase_dir/5 plans — the `--phase 13` flag-form false-negative (S1-1) is a query-syntax artifact, not a ROADMAP-repoint blocker; no repoint made. Confirmed both step hooks ACTIVE via `render-hooks verify:post` `activeHooks[]` (my first parser looked for the wrong key `hooks` → false "disabled"; corrected): `secure-phase`(when security_enforcement=true) + `validate-phase`(when nyquist_validation=true); config asvs_level 1, block_on high, text_mode true. **SECURE = SECURED, threats_open: 0** — State B, 14-threat register consolidated from 5 plans' `<threat_model>` blocks (`register_authored_at_plan_time:true`); asvs1 L1 short-circuit (no auditor); 14/14 CLOSED by orchestrator re-gate: zero `dsx/`|`scripts/` edits (git diff --stat empty → T-13-02/04/07/10/08-code); anti-parallel-advice grep 0 lines on cohort/funnel/root-cause/segment/executor (T-13-01/03/09); catalogue set-identity `added=[] removed=[]` + 256 + `--check` exit 0 (T-13-05/11/12/13, D-04/D-07); scope-analysis emits gsd-tier.ps1 & no config-set (T-13-08 D-05); 0 dangling of 28 cited codes. **VALIDATE = nyquist_compliant: true, 0 gaps** — State B; 6/6 REQ COVERED. **Loud op-decision (§4 rigour>flexibility, no scope/mint → no persona round, no escalation):** rather than mark 5 of 6 requirements manual-only, crystallised the phase's deterministic invariants into a standing test `tests/test_phase13_playbooks.py` (8 tests: skills-exist+registered, citation authenticity, router discipline, hypothesis register, What/So What/Now What, tier routing + advisory-boundary, .py entrypoint) — REQ-P13-01..05 now automated-COVERED; REQ-P13-06 stays on `test_finding_catalogue_invariant`. Gate: `sh scripts/check.sh` = all checks passed (**Ran 1230 tests OK**, 1222→+8; catalogue current 256; capability conformant 13 skills; gate contract; determinism). Two manual-only items (semantic/prose fidelity) do NOT reduce compliance (underlying behaviours automated). **Queued to HUMAN-QUEUE:** batched Phase 13 end-of-phase security sign-off (D-05/§4-cat-4) + UAT round — non-blocking until S5-2. Artifacts: `13-SECURITY.md`, `13-VALIDATION.md`, `tests/test_phase13_playbooks.py`. **S1 (Phase 13) is now fully complete (S1-1..S1-5).** Stopped after this one unit per firing instruction. Next unblocked = S2-1 (Phase 14 discuss). git: branch `gsd/v2.2.0-analytic-surface`, pushed to origin (0 ahead / 0 unpushed after this commit). | evidence: `13-SECURITY.md`, `13-VALIDATION.md`
2026-08-28T18:48Z | S1-3 (complete) | DONE — Phase 13 execution finished; all 5 plans executed, orchestrator-verified, pushed. Reconcile-first OK at HEAD `52fcf49` (branch up-to-date w/ origin; git log confirmed exactly the 13-01/13-02 commits the ledger claimed — no correction). **Loud op-decision (non-scope):** executed the remaining 3 plans DIRECTLY as orchestrator rather than spawning executors — they are surgical markdown/test edits with exact line anchors + exact grep/test verify blocks I re-ran myself; faster within the §1 pacing cap, keeps me single-writer, and I gate every plan. 13-03 `ac5bae9`: dsx-explore-data hypothesis-register mapping (untested belief→assumptions[] via DSX-COH-030/031; promoted test→design.multiplicity.family[]→results.tests[] via DSX-EXP-050..053, rides EDA.md ledgers, no new field) + dsx-narrate What/So What/Now What over the 5-part structure (Now What cites DSX-COH-040 + DSX-CLM-080; distinct DSX-NAR=1, template-only). 13-04 `74c62da`: dsx-scope-analysis <ceremony_tier> advisory table lookup→T0(dsx.enforce=false)/ad-hoc→T1(true)/full→T2(true,interactive), emits `pwsh scripts/gsd-tier.ps1 -Tier N`, cites docs/gsd-tiers.md, no config-set (D-05) + executor.md scripts/*.py-over-notebook bullet citing DSX-REP-040 + DSX-CODE, ordering-fidelity-not-leakage, suffix-neutral (D-06); anti-parallel-advice grep clean. 13-05 `affe761`: byte-copied references/finding-codes.md→tests/fixtures/finding-codes-phase12.md (cmp IDENTICAL, 256 codes) + CRLF-safe set-identity diff in test_finding_catalogue_invariant.py (current_set==phase12_set, added/removed reporting, reuses _ROW_RE, _EXPECTED_TOTAL untouched). **Gate evidence:** every plan verify block re-run green; `unittest tests.test_finding_catalogue_invariant -v`=2 tests OK; `gen-finding-catalogue.py --check` exit 0; catalogue 256 phase-wide; zero `dsx/`|`scripts/` edits (scope fence green each plan). Stopped at S1-3 boundary per §1 pacing — did NOT start S1-4 (heavier: full-suite + gsd-code-review, opus/high). Next = S1-4. git: branch `gsd/v2.2.0-analytic-surface`, pushed to origin (0 ahead / 0 unpushed after the sync commit). | evidence: 13-0{3,4,5}-SUMMARY.md; commits ac5bae9,74c62da,affe761

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

## S4-2 — Phase 15 plan (full evidence)

**Firing 2026-08-29 (S4-2).** Reconcile-first at HEAD `8d91d96` (branch up-to-date with
origin, nothing unpushed) found ledger == repo — S4-1 (Phase 15 discuss, `15-CONTEXT.md`
+ D-06 mint `DSX-EXP-070`/`DSX-MET-021`) was the last landed commit, no correction owed.

**Method.** Spawned `gsd-planner` (opus, §3) to author the plan set from `15-CONTEXT.md`
(D-01..D-09 + the 12 traps) + REQUIREMENTS REQ-P15-01..07, then the independent
`gsd-plan-checker` (opus — §3 override of the profile's haiku `checker_model`) as the gate.
Orchestrator ground-truthed the baseline first (brief §5): `--check` exit 0 @258;
`VARIANCE_ADJUSTMENTS` = 4 members @`spec.py:264` (no `cuped`); `DSX-MET-020` /
`_check_denominator_drift` reads `results.period_comparisons` @`metrics.py:189-201`;
`_D05_ALLOWLIST_CODES` exact-code frozenset @`gen-finding-catalogue.py:146` (prefixes = PAR/
VAL/INT/PRE/ADM/CRV, no EXP/MET); invariant `_EXPECTED_TOTAL=258`/`_SNAPSHOT_TOTAL=256`;
`DSX-EXP-070`/`DSX-MET-021` grep-0 in the catalogue (both genuinely free).

**Plan set (6 plans):**
| Plan | Wave | depends_on | requirements | Files (product) |
|---|---|---|---|---|
| 15-01 | 1 | [] | REQ-P15-01 | `dsx/spec.py` (`cuped`→VARIANCE_ADJUSTMENTS + `CUPED_COVARIATE_TIMINGS`), `tests/test_cuped_vocab.py` |
| 15-02 | 1 | [] | REQ-P15-04 | `dsx/checks/metrics.py` (mint MET-021 HIGH), `tests/test_cohort_denominator.py` |
| 15-03 | 1 | [] | REQ-P15-05, REQ-P15-06 | `templates/APA-TABLE-research.md`, `tests/test_apa_template.py`, `tests/test_no_shapiro_autoswitch.py` |
| 15-04 | 2 | [15-01] | REQ-P15-02 | `dsx/mathx.py` (θ/ρ² ref impl), `dsx/checks/design.py` (mint EXP-070 CRITICAL), `tests/test_cuped.py` |
| 15-05 | 3 | [15-01,15-02,15-04] | REQ-P15-03 | `examples/good-ANALYSIS-SPEC.yaml`, `tests/test_good_fixture_phase15.py` |
| 15-06 | 3 | [15-02,15-04] | REQ-P15-07 | `scripts/gen-finding-catalogue.py`, `references/finding-codes.md`, `tests/test_finding_catalogue_invariant.py` |

**Gate = REVISE (1 blocker) → 1 repair → PASS.**

Blocker (checker, confirmed by orchestrator): 15-02 Task 1's `<verify>` did
`body=ast.get_source_segment(src,f); assert 'period_comparisons' not in body`, but the same
task's `<action>` prescribes a `Structural criterion:` docstring line naming
`results.period_comparisons` — and `get_source_segment` returns the whole function
*including its docstring*, so `'period_comparisons' not in body` is False and the verify is
unpassable on a faithful implementation. 15-02 is the sole plan delivering REQ-P15-04
(MET-021), so a stuck verify would block the phase mid-execution.

Repair (checker's preferred option b): scoped the negative scan to code string-constants,
excluding the docstring by node identity —
`docn = f.body[0].value if <first stmt is a str Expr> else None; codestrs = ' '.join(str
constants in ast.walk(f) where n is not docn); assert 'cohort_comparisons' in codestrs and
'period_comparisons' not in codestrs`. Also reworded prohibition #3's prose to match
("function CODE (docstring excluded, by node identity)").

Orchestrator re-verification of the repair (brief §5 — empirical, not reasoned): built a
faithful synthetic `_check_cohort_denominator_shift` (docstring names `period_comparisons`,
code reads only `cohort_comparisons`) and ran both verifies — OLD **fails** (blocker
reproduced), NEW **passes**; the untouched downstream asserts (single `report.add`, literal
message, `DSX-MET-021`, `HIGH`, no pandas/scipy/numpy) still hold. Temp harness deleted.

Orchestrator re-verification of the checker's PASS claims (frontmatter-level, from disk):
- Coverage union == exactly {REQ-P15-01..07}: 01→15-01, 02→15-04, 03→15-05, 04→15-02,
  05+06→15-03, 07→15-06 — each requirement owned once, none invented, none uncovered.
- Single-writer-per-wave: wave-1 (15-01 spec.py / 15-02 metrics.py / 15-03 templates+2 tests)
  pairwise file-disjoint; 15-04 sole wave-2; wave-3 (15-05 examples+test / 15-06 generator+
  catalogue+invariant) disjoint. `spec.py` only 15-01, `design.py` only 15-04, `metrics.py`
  only 15-02. Every `depends_on` → strictly earlier wave; no cycles / forward refs.
- Trap #12: `cuped ∈ VARIANCE_ADJUSTMENTS` lands wave 1 (15-01) before both CUPED PASS
  fixtures (15-04 wave 2 `depends_on:[15-01]`, 15-05 wave 3) — no stray DSX-SPEC-044 window.
- Two mints only: EXP-070 CRITICAL (`design.py`, keyed on `variance_adjustment==cuped`,
  pre_experiment→ok / post_treatment|unrecognised|absent→fire) + MET-021 HIGH (`metrics.py`,
  reads `results.cohort_comparisons`, disjoint from MET-020 by a both-directions test). No
  survivorship code. No `GATE_THRESHOLDS`/`GATE_PROFILES` edit.
- D-08 additive rebaseline lives only in 15-06 (`_EXPECTED_TOTAL` 258→260, `_MINTED_CODES`
  += EXP-070,MET-021, `_SNAPSHOT_TOTAL` stays 256, frozen snapshot untouched, catalogue
  REGENERATED via `--write` not hand-edited). D-09 exact-code allowlist, not prefix.
- Catalogue-staleness window (mints wave 1/2, regen wave 3) judged SAFE: 15-02/04/05 verify
  blocks explicitly do NOT run `--check`/the invariant; the invariant reads the catalogue
  FILE (stays 258 until 15-06's `--write`), so nothing goes red mid-phase.

**Non-blocking nits (from the checker; carried to S4-3/S4-4, none blocks execution):**
1. 15-02 prohibition #3 prose reworded with the fix (done this unit).
2. 15-05 Task 2 uses `tests.test_causal_verb_golden` as a regression anchor — confirm at
   execute time that golden keys on finding codes only, not `report.ok` message lines.
3. 15-04 gate-plan exit test baselines on the *unmutated* good fixture (pre-Phase-15, no
   cuped block) — holds at wave 2; the in-memory deepcopy injection is self-contained.

Agents: planner `ad746fb00d5a99e52`; checker `a8d9950bfa667aa3b`.
