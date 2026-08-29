# LOOP-LEDGER — v2.3 Test Catalog

Source of truth for the autonomous loop. One checkbox = one unit.
Check a box ONLY with its gate evidence pasted in the Log (one line; long
evidence to `LOOP-LEDGER-ARCHIVE.md`).

**Scope source:** `.planning/research/V2.3-V2.4-SCOPE.md` (2026-08-29) and
`.planning/REQUIREMENTS.md` (22 requirements, REQ-P17-01 … REQ-P20-04). Both
carry full goals, citations, doctrine dispositions and ordering constraints —
**this milestone needs execution, not a fresh scoping round.**

**Predecessors:** v2.2 Analytic Surface shipped 2026-08-29 (tag `v2.2.0`);
v2.0.0 shipped 2026-08-28 (tag `v2.1.0`). Loop artifacts archived at
`.planning/milestones/v2.2-LOOP-*`, `v2.2-HUMAN-QUEUE.md`, and `v2.0.0-*`.

## Ordering rationale

Phases run in numeric order **17 → 18 → 19 → 20**: Phase 17 is the foundation
every later unit reads (`estimand_kind` vocabulary, Boschloo repair, D-12a
dispositions, D-06 pre-allocated ranges) and hard-blocks 18/19; Phase 20 is
terminal calibration and consumes every new code. The D-05 human reads are the
long pole (~15–20), so their evidence packs are filed at S0 — before Phase 17
even plans — exactly the v2.2 HQ-8 pattern that worked.

**Standing v2.3 rules (from the brief §5, repeated because they bind every unit):**
routing keys read DECLARED fields only; doc table and `recommend_test` change in
the same commit; new codes only from the pre-allocated ranges; effect-size bands
are conventions, never thresholds.

## S0 — Milestone bootstrap

- [ ] S0-1 Verify GSD state points at v2.3 (STATE.md frontmatter `milestone: v2.3`,
  `current_phase: 17`, progress 0/4) and `gsd-tools query init.milestone-op`
  resolves it (4 phases, 0 complete); `.planning/phases/` is empty (v2.2 dirs
  archived). Gate: command output pasted.
- [ ] S0-2 Re-verify the inherited scope against the live tree before planning on
  it: per-requirement verdict table (still-valid / already-satisfied /
  contradicted) written to `.planning/v2.3-SCOPE-RECHECK.md`. Key premises to
  re-confirm: `fisher_exact` still at `dsx/checks/stats.py:65` and `boschloo_exact`
  absent from `NONPARAMETRIC_TESTS`; `QUESTION_TYPES` still the closed 5-key list;
  the `time_to_event` fallthrough still unconditional; live catalogue count
  re-measured (do NOT assume 260). Gate: the recheck file with evidence.
- [ ] S0-3 File the **Phase 18 D-05 citation evidence pack** to HUMAN-QUEUE
  (correlation + agreement codes and effect-size band sources: Cohen 1960/1968,
  Fleiss 1971, Hayes & Krippendorff 2007 worked value, Shrout & Fleiss 1979,
  McGraw & Wong 1996, Koo & Li 2016, Feinstein & Cicchetti 1990, Landis & Koch
  1977, Bland & Altman 1986, Fisher 1921). Per-citation table: locator, the exact
  formulation/value the check will cite, confirmed-by-loop vs
  UNVERIFIED-for-human split. **Do not sign — D-05 is a human read.**
- [ ] S0-4 File the **Phase 19 D-05 citation evidence pack** to HUMAN-QUEUE
  (Greenhouse & Geisser 1959 + Maxwell & Delaney 2004 ch.11-12; Hamed & Rao 1998;
  Armitage 1955 / Cochran 1954; Campbell 2007; Davidson & MacKinnon 2000; Efron
  1987; Games & Howell 1976; Hayter 1986; Zimmerman 2004; Hoenig & Heisey 2001;
  Lakens 2022; Brown, Cai & DasGupta 2001; Newcombe 1998; McCullagh & Nelder 1989
  §6.2; Wilson 2015). Same format. **Do not sign.**

## S1 — Phase 17: Foundation — repairs and spec vocabulary (5 requirements)

- [ ] S1-1 Discuss (assumptions mode + persona round); `17-CONTEXT.md` written.
  Must settle: final `estimand_kind` vocabulary name/members; the D-12a
  disposition table (REQ-P17-03) for every Phase 18/19 gate check; the D-06 range
  pre-allocation plan keyed to the live count.
- [ ] S1-2 Plan (plan-checker must pass).
- [ ] S1-3 Execute all plans (Boschloo reconciliation + pinned regression test;
  `estimand_kind` vocabulary additive with D-08 fixture extension; fallthrough
  regression test; range pre-allocation note committed).
- [ ] S1-4 Code review + fixes; verification `passed` (goal-backward vs
  REQ-P17-01..05; REQ-P17-05 zero-new-codes asserted by set-identity diff).
- [ ] S1-5 `/gsd-secure-phase 17` verified + `/gsd-validate-phase 17` compliant.
  End-of-phase security sign-off + UAT batched to HUMAN-QUEUE (non-blocking
  until S5-2).

## S2 — Phase 18: Correlation, association and agreement (6 requirements)

- [ ] S2-1 Discuss + persona round; `18-CONTEXT.md`. D-06 numbering from the
  pre-allocated ranges (veto window filed to HUMAN-QUEUE, non-blocking). Blocked
  until S1-5 AND the S0-3 evidence pack is human-answered for every code that
  ships a citation (codes whose citations are not confirmed are NOT in hand).
- [ ] S2-2 Plan (plan-checker must pass). Single-writer waves: `dsx/checks/stats.py`
  and `references/test-selection.md` change in the same plan/commit, always.
- [ ] S2-3 Execute all plans (rows + gates + mathx bands + APA wiring).
- [ ] S2-4 Code review + fixes; verification `passed` (REQ-P18-01..06; the
  no-autoswitch extension test green).
- [ ] S2-5 `/gsd-secure-phase 18` + `/gsd-validate-phase 18`; sign-off batched.

## S3 — Phase 19: RM, trend, categorical, resampling, post-hoc (7 requirements)

- [ ] S3-1 Discuss + persona round; `19-CONTEXT.md`. D-06 numbering from ranges
  (veto window). Blocked until S1-5 AND the S0-4 pack is answered for shipping
  codes. This is the largest phase — the discuss should confirm the wave split
  keeps every file single-writer.
- [ ] S3-2 Plan (plan-checker must pass).
- [ ] S3-3 Execute all plans (rows incl. DEPRECATED routing-off entries; negative
  gates; doc/code lockstep per commit).
- [ ] S3-4 Code review + fixes; verification `passed` (REQ-P19-01..07).
- [ ] S3-5 `/gsd-secure-phase 19` + `/gsd-validate-phase 19`; sign-off batched.

## S4 — Phase 20: Calibration and reporting close (4 requirements)

- [ ] S4-1 Discuss (light — calibration shape is Phase-12-precedented);
  `20-CONTEXT.md`.
- [ ] S4-2 Plan (plan-checker must pass).
- [ ] S4-3 Execute (known-bad fixtures per new code; catch-rate/FPR re-baseline;
  D-08 silence; no-autoswitch full coverage; the REQ-P20-04 doc/code agreement
  test).
- [ ] S4-4 Code review + fixes; verification `passed` (REQ-P20-01..04).
- [ ] S4-5 `/gsd-secure-phase 20` + `/gsd-validate-phase 20`; sign-off batched.

## S5 — Close-out

- [ ] S5-1 `/gsd-audit-uat` cross-phase sweep. **Do NOT accept the CLI's "All
  Clear"** — it under-reports via TWO known defects (heading-level mismatch AND
  the `-VERIFICATION` filename filter); hand-check every phase's VERIFICATION.md.
- [ ] S5-2 Drain HUMAN-QUEUE (the only permitted blocking wait).
- [ ] S5-3 `/gsd-extract-learnings`.
- [ ] S5-4 `/gsd-audit-milestone` — must reach `passed`.
- [ ] S5-5 `/gsd-complete-milestone` — **NOT headless-safe** (interactive
  prompts + `git rm REQUIREMENTS.md`); runs in an interactive session per
  operator approval. Hand-verify the CLI's generated accomplishments and the
  archived REQUIREMENTS checkboxes (both were wrong at v2.2 close and needed
  correction).
- [ ] S5-6 Ship: merge to `main` **by explicit branch name**
  (`git merge --no-ff gsd/v2.3.0-test-catalog`, verified on a throwaway branch
  first, full suite + `scripts/check.sh` green BEFORE touching `main`) and tag
  `v2.3.0`. **Never** the framework's alphabetical `gsd/*` auto-detect (stale
  branches would be picked); **never** `/gsd-pr-branch` (cherry-pick chain fails
  on long branches); **never** force-move a published tag. Outward-facing —
  queue to HUMAN-QUEUE for the operator, do not self-approve.

## Log

(append one line per firing: `YYYY-MM-DDTHH:MMZ | unit | outcome | evidence`.
Keep the most recent ~15–20; archive older entries to `LOOP-LEDGER-ARCHIVE.md`.)

2026-08-29T21:30Z | milestone-open | v2.3 opened by operator direction in an interactive session: scope researched (6-agent workflow: 2 repo mappers, 3 domain researchers, 1 adversarial critic — journal preserved), .planning/research/V2.3-V2.4-SCOPE.md + REQUIREMENTS.md (REQ-P17-01..P20-04) + ROADMAP.md (Phases 17-20 active, 21-24 queued) written; STATE.md repointed (v2.3, phase 17, 0/4); v2.2 loop artifacts archived to .planning/milestones/v2.2-LOOP-*, v2.2-HUMAN-QUEUE.md; this ledger + LOOP-BRIEF + HUMAN-QUEUE rewritten for v2.3; branch gsd/v2.3.0-test-catalog created from main; firing script repointed + usage-limit backoff added (weekly reset Wednesday 13:00 UTC = 10:00 São Paulo; 5h-window = 60-min hold). Operator directive of record: token limits WILL hit this week — firings log one line and stop on limit errors, the wrapper owns pacing and self-resumes. Next = S0-1. | .planning/research/V2.3-V2.4-SCOPE.md; scripts/run-ceremony-firing.ps1
