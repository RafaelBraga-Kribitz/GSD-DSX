# LOOP-LEDGER — v2.2 Analytic Surface

Source of truth for the autonomous loop. One checkbox = one unit.
Check a box ONLY with its gate evidence pasted in the Log.

**Scope source:** `.planning/ROADMAP.md` "Queued milestone — v2.2 Analytic Surface
(Phases 13–16)" and `.planning/REQUIREMENTS.md` "Queued — Milestone v2.2"
(23 requirements, REQ-P13-01 … REQ-P16-04). Both were written at v2.0.0 planning
time and carry full goals, success criteria, dependencies and ordering constraints —
**this milestone does not need a fresh scoping round; it needs execution.**

**Research backing:** `.planning/research/SURFACE.md` (2026-08-26). Per that file
and `brief.md` §6.5, comparison-repo READMEs are **not** admissible D-05 sources.

**Predecessor:** v2.0.0 DSX Validity Frame — shipped 2026-08-28, tag `v2.1.0`,
merged to `main`. Its loop artifacts are archived at
`.planning/milestones/v2.0.0-LOOP-{LEDGER,LEDGER-ARCHIVE}.md` and
`v2.0.0-HUMAN-QUEUE{,-ARCHIVE}.md`.

## Ordering rationale (read before reordering anything)

Phases are executed **13 → 14 → 16 → 15**, not in numeric order. This is deliberate
and satisfies every declared dependency:

- Phase 13 soft-blocks 14 (slash aliases must cover the new task skills) and
  soft-blocks 15 (the new spec fields want a skill that fills them) — so 13 is first.
- Phase 16 hard-depends only on Phase 12, which shipped — so it is free to run early.
- **Phase 15 is the only phase that mints new finding codes and therefore the only
  one carrying a D-05 human-read gate and a D-06 irreversible-numbering veto.**
  Running it last maximises the work the loop can complete without the operator,
  and its citation evidence pack is prepared up front (S0-3) so the operator can
  answer asynchronously while 13/14/16 build.

## S0 — Milestone bootstrap

- [x] S0-1 Point GSD state at the new milestone: `STATE.md` frontmatter (`milestone: v2.2`, `milestone_name: Analytic Surface`, `status: executing`, `current_phase: 13`, progress reset to 0/4 phases), body reconciled. Gate: `gsd-tools query init.milestone-op` resolves the new milestone without error; `.planning/phases/` exists and is empty (v2.0.0 dirs are archived, not deleted). — **DONE 2026-08-28T15:02Z:** frontmatter already at v2.2 (from milestone-transition `33dc7de`); body reconciled to a 79-line GSD-template digest (v2.0.0 history collapsed to archive pointers — full record in `MILESTONES.md` + `.planning/milestones/v2.0.0-*`). Gate green: `init.milestone-op` exit 0 (v2.2 / Analytic Surface / phase_count 4 / completed_phases 0 / phases_dir_exists true); `.planning/phases/` = `.gitkeep` only. See Log.
- [x] S0-2 Verify the inherited v2.2 scope is still true against the shipped v2.0.0 tree before planning anything on it. — **DONE 2026-08-28:** all 23 requirements re-read against live code; verdict = **23/23 still-valid, 0 amendments** (none already-satisfied/contradicted/obsolete), so no §4 loud amendment and no HUMAN-QUEUE escalation. Gate met: per-requirement verdict table + premise evidence in `.planning/v2.2-SCOPE-RECHECK.md`. Key confirmations: 5 new skills absent; `VARIANCE_ADJUSTMENTS` = exactly 4 named members (`dsx/spec.py:264`); gate path pure (no pandas/scipy in `dsx/frame`,`dsx/checks`); no `shapiro` in `skills/`|`dsx/`; `brief.md §6.5` + fixtures present; `gen-finding-catalogue.py --check` exit 0. See Log.
- [x] S0-3 Prepare the Phase 15 D-05 citation evidence pack EARLY and file it as HQ-8, so the operator can answer while 13/14/16 build. Covers: Deng, Xu, Kohavi & Walker (2013) WSDM CUPED — exact formulation + a published worked value (REQ-P15-02); and the survivorship-bias / changing-denominator candidate citations (REQ-P15-04). Gate: `HUMAN-QUEUE.md` HQ-8 contains a per-citation evidence table with locators and a clear statement of what is confirmed vs unverified. **Do not sign it — D-05 requires the human read.** — **DONE 2026-08-28:** HQ-8 assembled with 3 per-citation evidence tables (CUPED HIGH / survivorship MEDIUM / changing-denominator MEDIUM), each carrying locator (DOI+pages), the formulation/defect to confirm, and an explicit Confirmed-by-loop vs Unverified/Open-D05 split. **Not signed** (D-05 = human read). Flagged the changing-denominator↔Deng&Hu-2015 out-of-scope boundary (brief line 450) so S4 doesn't re-mint. D-06 numbering left to S4-1. Gate met by construction. See Log.

## S1 — Phase 13: Task playbooks that fill the spec (skill-only, 6 requirements)

- [x] S1-1 Discuss (assumptions mode + persona round); `13-CONTEXT.md` written. — **DONE 2026-08-28T15:51Z:** Architect-led + Auditor 2-persona round (opus/high, §4) settled D-01..D-08. 256-code baseline re-verified by orchestrator (`--check` exit 0, distinct-code grep = 256). Locks: 4 pure prompt-guidance skills + `capability.json` append, no gate-path touch (D-01); field→gate contract table, route-and-cite, no parallel advice (D-02); hypothesis register → `assumptions[]`/`multiplicity.family`→`results.tests[]` (D-03); What/So What/Now What = template-only, no `DSX-NAR` mint (D-04); advisory tier routing lookup/ad-hoc/full→Tier 0/1/2 (D-05); executor `scripts/*.py` bullet citing `DSX-REP-040` (D-06); **REQ-P13-06 asserted by set-identity diff vs a frozen Phase-12 snapshot, not count alone** (D-07, tie-break rigour>reliability); zero mint, `DSX-COH-*`=Coherence-not-Cohort caveat (D-08). **Pre-req for S1-2:** ROADMAP active-milestone repoint (v2.2 still under "## Queued milestone"; `init phase-op --phase 13`→`phase_found:false`) — structural, not a scope change. Gate met: `.planning/phases/13-task-playbooks-that-fill-the-spec/13-CONTEXT.md` (21.8 KB, 6 sections, D-01..D-08). See Log.
- [ ] S1-2 Plan (plan-checker must pass).
- [ ] S1-3 Execute all plans.
- [ ] S1-4 Code review + auto-fix; verification `passed`.
- [ ] S1-5 `/gsd-secure-phase 13` verified + `/gsd-validate-phase 13` compliant. **Scope bound (REQ-P13-06): the catalogue must contain no new codes vs the Phase 12 catalogue — assert by diff, not by review. A skill that "needs" a new code is a Phase 15 item, not a Phase 13 exception.**

## S2 — Phase 14: Compounding and data onboarding (6 requirements)

- [ ] S2-1 Discuss; `14-CONTEXT.md` written. **Open item to settle here, do not decide silently:** REQ-P14-05 is conditional — if GSD Core exposes no overlay hooks, the requirement is satisfied by a documented skip in the operating guide, NOT by inventing a hook channel. Verify against the installed GSD Core and record which branch was taken.
- [ ] S2-2 Plan (plan-checker must pass).
- [ ] S2-3 Execute all plans.
- [ ] S2-4 Code review + auto-fix; verification `passed`.
- [ ] S2-5 `/gsd-secure-phase 14` verified + `/gsd-validate-phase 14` compliant (REQ-P14-06: no new blocking codes).

## S3 — Phase 16: Re-run verification, off the gate path (4 requirements)

- [ ] S3-1 Discuss; `16-CONTEXT.md` written. **Open item to settle here, do not decide silently:** REQ-P16-02 requires `dsx gate` to check `REPRO-REPORT.md` exists and that named numbers overlap — that check needs a finding code, but the ROADMAP calls Phase 15 "the only v2.2 phase that extends the gate catalogue." Resolve explicitly: either extend the existing `DSX-REP-*` family (Phase 4) and amend the ROADMAP's "only" claim with a recorded note, or move the gate half to Phase 15. **Whichever is chosen is a D-06 irreversible numbering decision if a new code is minted — record it loudly and queue it to HUMAN-QUEUE for the veto window.**
- [ ] S3-2 Plan (plan-checker must pass).
- [ ] S3-3 Execute all plans.
- [ ] S3-4 Code review + auto-fix; verification `passed`. **Hard constraint (REQ-P16-02/-04, D-01/D-02): the gate path must never import pandas/scipy or execute the analysis entrypoint. A test must assert this. If a future change "simplifies" by calling the entrypoint from `dsx gate`, the phase is failed, not done.**
- [ ] S3-5 `/gsd-secure-phase 16` verified + `/gsd-validate-phase 16` compliant.

## S4 — Phase 15: CUPED and BI declaration checks (7 requirements, new codes + D-05)

- [ ] S4-1 Discuss; `15-CONTEXT.md` written. Persona round assigns the new numeric codes (D-06 irreversible) and records them loudly for the veto window. Ordering constraint: REQ-P15-01 before REQ-P15-02 (`cuped` must be a legal vocabulary member before a check can require it).
- [ ] S4-2 Plan (plan-checker must pass).
- [ ] S4-3 Execute all plans. **D-05 bar: a code whose citation is not in hand at implement time does NOT ship — it stays in `brief.md` §6.5 rather than being invented.**
- [ ] S4-4 Code review + auto-fix; verification `passed`; queue the phase's D-05 reads + D-06 veto window to HUMAN-QUEUE (evidence pack from S0-3 already filed as HQ-8; extend it with anything minted during execution).
- [ ] S4-5 `/gsd-secure-phase 15` verified + `/gsd-validate-phase 15` compliant; `gen-finding-catalogue.py --check` exits 0 on the new codes; both canonical fixtures still satisfy D-08 (REQ-P15-07).

## S5 — Close-out

- [ ] S5-1 `/gsd-audit-uat` cross-phase sweep. **Do NOT accept the CLI's "All Clear" as evidence** — it under-reports (see Standing framework notes in `HUMAN-QUEUE.md`); cross-check each phase's VERIFICATION.md by hand.
- [ ] S5-2 Drain HUMAN-QUEUE (the only permitted blocking wait).
- [ ] S5-3 `/gsd-extract-learnings`.
- [ ] S5-4 `/gsd-audit-milestone` — must reach `passed`.
- [ ] S5-5 `/gsd-complete-milestone`.
- [ ] S5-6 Ship: merge to `main` and tag. **Precedent from v2.0.0 (do not repeat its cost):** `/gsd-pr-branch`'s per-commit cherry-pick chain does NOT survive a long ceremony branch — it hit recurring modify/delete and structural-file conflicts and was abandoned. Ship by direct 3-way merge into `main` (`git merge --no-ff`), verified on a throwaway branch first with the full suite + `scripts/check.sh` green BEFORE touching `main`. Tag the next free version (`v2.2.0`); **never force-move a published tag.** Merge and tag are outward-facing — queue to HUMAN-QUEUE for the operator, do not self-approve.

## Log

(append one line per firing: `YYYY-MM-DDTHH:MMZ | unit | outcome | evidence`. Keep
the most recent ~20; archive older entries to `LOOP-LEDGER-ARCHIVE.md` per brief §5.)

2026-08-28T14:40Z | milestone-transition | v2.0.0 SHIPPED (merged to main `c81fc6b`, tag `v2.1.0` pushed, both verified on origin); v2.2 Analytic Surface opened on branch `gsd/v2.2.0-analytic-surface`; loop repointed | v2.0.0 loop artifacts archived to `.planning/milestones/v2.0.0-LOOP-*`; suite 1221 OK + `scripts/check.sh` all checks passed on the merged tree before push
2026-08-28T15:02Z | S0-1 | DONE — GSD state reconciled onto v2.2. Reconcile OK first: HEAD `33dc7de`, branch up-to-date with origin, ledger==repo (no correction needed). Frontmatter already at v2.2/Analytic Surface/executing/current_phase 13/0-of-4 from the transition commit; body was still 198 lines of v2.0.0 detail contradicting it, so reconciled to a 79-line GSD-template digest — v2.0.0 history preserved in `MILESTONES.md` + `.planning/milestones/v2.0.0-*`, not deleted. | Gate `node ~/.claude/gsd-core/bin/gsd-tools.cjs query init.milestone-op` exit 0: milestone_version v2.2, milestone_name "Analytic Surface", phase_count 4, completed_phases 0, phases_dir_exists true; `.planning/phases/` = `.gitkeep` only; STATE.md 79 lines (< 100-line template cap). Next unblocked = S0-2.
2026-08-28T16:20Z | S0-3 | DONE — Phase 15 D-05 citation evidence pack assembled into HUMAN-QUEUE.md HQ-8 (prepared, NOT signed — D-05 is the human read). Reconcile OK first: HEAD `541c5b9`, branch up-to-date with origin, ledger==repo (no correction). Pack = 3 per-citation tables with locators + confirmed/unverified split: (1) CUPED — Deng/Xu/Kohavi/Walker 2013 WSDM pp.123–132 DOI 10.1145/2433396.2433413; formulation Ŷ_cv=Ȳ−θ(X̄−E[X]), θ=Cov/Var, Var-reduction 1−ρ²; worked value = 1−ρ² identity (fixture/docstring, not gate-path per D-02) + paper's ≈50 % Bing headline; HIGH, only exact eq#/page left for the read. (2) Survivorship — Brown/Goetzmann/Ibbotson/Ross 1992 RFS 5(4):553–580 DOI 10.1093/rfs/5.4.553 (+ Elton/Gruber/Blake 1996); MEDIUM, open question = does the finance criterion transfer to a cohort/funnel declaration check (else stays §6.5). (3) Changing-denominator — Crook/Frasca/Kohavi/Longbotham 2009 KDD pp.1105–1114 DOI 10.1145/1557019.1557139 (+ Kohavi/Tang/Xu 2020 book); MEDIUM, flagged the out-of-scope boundary vs Deng&Hu-2015 dilution (brief line 450) so S4 won't re-mint. D-06 numbering left to S4-1; no code assigned. No §4 persona round needed (evidence-gathering, not a decision). Sources corroborated across independent web results 2026-08-28; not a D-05 sign-off. Gate met: HQ-8 has per-citation table + locators + confirmed-vs-unverified. Next unblocked = S1-1 (Phase 13 discuss). | evidence: `.planning/HUMAN-QUEUE.md` HQ-8
2026-08-28T15:51Z | S1-1 | DONE — Phase 13 discuss complete; `13-CONTEXT.md` written. Reconcile OK first: HEAD `bdf7393`, branch up-to-date with origin, ledger==repo (S0-1/2/3 all landed, no correction). Ran an **Architect-led (`dsx-analysis-architect`) + Auditor (`dsx-ml-integrity-auditor`) 2-persona round** (both opus/high, concurrent, §4), tie-break rigour>reliability>flexibility — the relevant 2 for a skill-only spec-shape phase. Orchestrator independently re-verified the load-bearing baseline before trusting it: `references/finding-codes.md` Total = **256**, distinct-`DSX-*` grep = **256**, `gen-finding-catalogue.py --check` exit **0** (DSX-VAL-060 double-declare = known shipped-tree noise); `test_finding_catalogue_invariant.py` `_EXPECTED_TOTAL=256` present; narrate `SKILL.md` has 0 "so what", executor fragment has 0 script-preference → both REQ-P13-03/-05 confirmed additive. 8 loud/vetoable decisions D-01..D-08 recorded in CONTEXT (full rationale + citations there). Genuine tie-break made: REQ-P13-06 "assert by diff" → **set-identity diff vs a frozen Phase-12 code-set snapshot**, not count-only (count passes a mint-one/drop-one swap; the ledger says "by diff, not by review"). No §4 escalation (mints nothing, no scope change, non-destructive). No D-05/D-06 owed by Phase 13. **Flagged for S1-2:** ROADMAP still has v2.2 phases under "## Queued milestone" (`:52`) while active `## Milestones`/`## Phases` (`:15`/`:20`) show v2.0.0, so `init phase-op --phase 13`→`phase_found:false`; S1-2 must promote the section to active before `/gsd-plan-phase 13` resolves (structural repoint, requirements unchanged). Gate met: `.planning/phases/13-task-playbooks-that-fill-the-spec/13-CONTEXT.md`. Next unblocked = S1-2 (plan Phase 13; do the ROADMAP repoint first). | evidence: `13-CONTEXT.md`
2026-08-28T15:40Z | S0-2 | DONE — v2.2 scope rechecked against shipped v2.0.0 tree. Reconcile OK first: HEAD `4ae156f`, branch up-to-date with origin, ledger==repo (no correction). All 23 reqs (REQ-P13-01…P16-04) re-read against live code via direct grep/ls/Read + a real `gen-finding-catalogue.py --check` (exit 0). Verdict **23/23 still-valid, 0 amendments** → no §4 loud amendment, no HUMAN-QUEUE escalation; milestone needs execution, not re-scoping. Evidence: 5 target skills (`dsx-{cohort,funnel,root-cause,segment,reproduce}`) absent; `VARIANCE_ADJUSTMENTS` = exactly the 4 named members no `cuped` (`dsx/spec.py:264`); `dsx vocab` present; gate path pure (no pandas/scipy in `dsx/frame`|`dsx/checks`); no `shapiro` in `skills/`|`dsx/`; `test-selection.md` order matches REQ-P15-06; `brief.md §6.5` + D-08 fixtures present. Recorded (non-amendments): `DSX-REP-*` already exists (11 codes) → material to S3-1; pre-existing double-declare warnings (DSX-SPEC-070/VAL-021/VAL-060) are shipped-tree noise, --check still exit 0 → don't misread at S4-5. Full verdict table: `.planning/v2.2-SCOPE-RECHECK.md`. Next unblocked = S0-3 (Phase 15 D-05 evidence pack → HQ-8).
