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

- [ ] S0-1 Point GSD state at the new milestone: `STATE.md` frontmatter (`milestone: v2.2`, `milestone_name: Analytic Surface`, `status: executing`, `current_phase: 13`, progress reset to 0/4 phases), body reconciled. Gate: `gsd-tools query init.milestone-op` resolves the new milestone without error; `.planning/phases/` exists and is empty (v2.0.0 dirs are archived, not deleted).
- [ ] S0-2 Verify the inherited v2.2 scope is still true against the shipped v2.0.0 tree before planning anything on it — re-read each of the 23 requirements and each phase's success criteria against the live code, and record any that the shipped v2.0.0 already satisfied, contradicted, or made obsolete. Gate: a written per-requirement verdict (still-valid / already-satisfied / needs-amendment) in `.planning/phases/13-.../13-CONTEXT.md` or a standalone `v2.2-SCOPE-RECHECK.md`; any amendment is loud (§4) and recorded, never silent.
- [ ] S0-3 Prepare the Phase 15 D-05 citation evidence pack EARLY and file it as HQ-8, so the operator can answer while 13/14/16 build. Covers: Deng, Xu, Kohavi & Walker (2013) WSDM CUPED — exact formulation + a published worked value (REQ-P15-02); and the survivorship-bias / changing-denominator candidate citations (REQ-P15-04). Gate: `HUMAN-QUEUE.md` HQ-8 contains a per-citation evidence table with locators and a clear statement of what is confirmed vs unverified. **Do not sign it — D-05 requires the human read.**

## S1 — Phase 13: Task playbooks that fill the spec (skill-only, 6 requirements)

- [ ] S1-1 Discuss (assumptions mode + persona round); `13-CONTEXT.md` written.
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
