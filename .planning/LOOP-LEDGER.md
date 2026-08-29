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

- [x] S0-1 Verify GSD state points at v2.3 (STATE.md frontmatter `milestone: v2.3`,
  `current_phase: 17`, progress 0/4) and `gsd-tools query init.milestone-op`
  resolves it (4 phases, 0 complete); `.planning/phases/` is empty (v2.2 dirs
  archived). Gate: command output pasted. → evidence in LOOP-LEDGER-ARCHIVE.md `## S0-1`
- [x] S0-2 Re-verify the inherited scope against the live tree before planning on
  it: per-requirement verdict table (still-valid / already-satisfied /
  contradicted) written to `.planning/v2.3-SCOPE-RECHECK.md`. Key premises to
  re-confirm: `fisher_exact` still at `dsx/checks/stats.py:65` and `boschloo_exact`
  absent from `NONPARAMETRIC_TESTS`; `QUESTION_TYPES` still the closed 5-key list;
  the `time_to_event` fallthrough still unconditional; live catalogue count
  re-measured (do NOT assume 260). Gate: the recheck file with evidence.
  → `.planning/v2.3-SCOPE-RECHECK.md`: all 5 premises CONFIRMED at locators, count re-measured = 260, all 22 reqs still-valid.
- [x] S0-3 File the **Phase 18 D-05 citation evidence pack** to HUMAN-QUEUE
  (correlation + agreement codes and effect-size band sources: Cohen 1960/1968,
  Fleiss 1971, Hayes & Krippendorff 2007 worked value, Shrout & Fleiss 1979,
  McGraw & Wong 1996, Koo & Li 2016, Feinstein & Cicchetti 1990, Landis & Koch
  1977, Bland & Altman 1986, Fisher 1921). Per-citation table: locator, the exact
  formulation/value the check will cite, confirmed-by-loop vs
  UNVERIFIED-for-human split. **Do not sign — D-05 is a human read.**
  → filed as HQ-16 (HUMAN-QUEUE.md): 11 citations, 6 groups keyed to the two Phase 18
  gate codes + band sources; all 11 locators corroborated across multiple independent
  sources; two load-bearing reads flagged (Krippendorff α=0.743 worked value w/ the
  0.734 book-typo trap; Landis-Koch/Koo-Li band boundaries). NOT signed — human read owed.
- [x] S0-4 File the **Phase 19 D-05 citation evidence pack** to HUMAN-QUEUE
  (Greenhouse & Geisser 1959 + Maxwell & Delaney 2004 ch.11-12; Hamed & Rao 1998;
  Armitage 1955 / Cochran 1954; Campbell 2007; Davidson & MacKinnon 2000; Efron
  1987; Games & Howell 1976; Hayter 1986; Zimmerman 2004; Hoenig & Heisey 2001;
  Lakens 2022; Brown, Cai & DasGupta 2001; Newcombe 1998; McCullagh & Nelder 1989
  §6.2; Wilson 2015). Same format. **Do not sign.**
  → filed as HQ-17 (HUMAN-QUEUE.md): 16 citations in 7 groups keyed to the REQ-P19-01…07
  gates; every locator corroborated across ≥2 independent sources; 7 load-bearing reads
  flagged (esp. McCullagh-Nelder §6.2 UNCONFIRMED → ships chapter-granular; Hayter 1986
  JASA vs the 1984 Annals decoy; Newcombe Paper B 873-890/SIM779). NOT signed — human read owed.

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

2026-08-29T21:35Z | S0-4 | PASS — Phase 19 D-05 citation evidence pack filed to HUMAN-QUEUE as HQ-17 (non-blocking; NOT signed — D-05 is a human read). 16 citations in 7 groups keyed to the REQ-P19-01…07 gates; every bibliographic locator corroborated across ≥2 independent sources (Crossref / publisher / PubMed / DOI-resolver / citation-index) via 4 parallel research agents. 7 load-bearing reads flagged: McCullagh-Nelder "§6.2" UNCONFIRMED (secondary cites give p.206 / §6.3.2 → ships CHAPTER-granular per brief §5); Hayter 1986 = JASA 81(396):1000-1004, NOT the 1984 Annals Tukey-Kramer decoy; Newcombe = Paper B (SiM 17(8):873-890, DOI …SIM779, PMID 9595617), not the single-proportion Paper A (857-872/SIM777); Davidson-MacKinnon B = 399/1499 recommended vs 19/99 exactness-floor (don't conflate); Brown-Cai-DasGupta n≤40 cutoff is secondary-source-only; Campbell 2007 = revalidated N-1 (Egon Pearson originated it), cite "argued for" not "invented"; Greenhouse-Geisser = 1959 Psychometrika, not the reversed-author 1958 Annals paper. TIMESTAMP CORRECTION: real UTC via `date -u` = 21:35Z; prior S0-1..S0-3 Log times (22:00-22:40Z) ran ~2.5h ahead of the actual git commit times (S0-3 committed 20:14Z) — those were estimated, this one is measured, hence the Log appears to step backward here. S0 bootstrap now COMPLETE (S0-1..S0-4 all done); next unblocked unit = S1-1 (Phase 17 discuss). | HUMAN-QUEUE.md `### HQ-17`
2026-08-29T22:40Z | S0-3 | PASS — Phase 18 D-05 citation evidence pack filed to HUMAN-QUEUE as HQ-16 (non-blocking; NOT signed — D-05 is a human read). 11 citations grouped into 6 sets keyed to the granularity ruling (read-per-CODE): A Fisher 1921 (Pearson Fisher-z CI); B Cohen 1960/1968 + Fleiss 1971 + Hayes-Krippendorff 2007; C Shrout-Fleiss 1979 + McGraw-Wong 1996 (ICC triple); D Bland-Altman 1986; E Feinstein-Cicchetti 1990 (kappa companion gate); F Landis-Koch 1977 + Koo-Li 2016 (bands=conventions). All 11 bibliographic locators corroborated across ≥2 independent sources (venue/vol/pages/DOI-or-PMID). Loop caught: Krippendorff worked value = α 0.743 (0.734 in the textbook is a known typo) — the one load-bearing numeric-fixture read; Landis-Koch has TWO 1977 Biometrics papers, bands are in 33(1):159-174 not 33(2):363-374; McGraw-Wong 1996 has a published erratum; Koo-Li band VALUES not confirmed by search (candidate-only). Per brief §5, any fixture/band unconfirmed at source ships catalog-only/convention-labelled. Next = S0-4 (Phase 19 pack → HQ-17). | HUMAN-QUEUE.md `### HQ-16`
2026-08-29T22:10Z | S0-2 | PASS — inherited scope re-verified against live tree; `.planning/v2.3-SCOPE-RECHECK.md` written. All 5 load-bearing premises CONFIRMED at locators: fisher_exact fallback at stats.py:65; boschloo_exact absent from NONPARAMETRIC_TESTS (stats.py:23-26); doc side still names Boschloo (test-selection.md:10 + [^1] Lydersen-Fagerland-Laake 2009) — divergence genuinely live; QUESTION_TYPES closed 5-key (spec.py:22-28) + estimand_kind absent everywhere; time_to_event fallthrough unconditional (stats.py:128-129). Catalogue RE-MEASURED = 260 codes (matches checked-in finding-codes.md; = REQ-P17-05 baseline). All 22 reqs still-valid, none satisfied/contradicted — execution, not re-scoping. Next = S0-3. | .planning/v2.3-SCOPE-RECHECK.md
2026-08-29T22:00Z | S0-1 | PASS — GSD state points at v2.3: STATE.md frontmatter milestone v2.3 / current_phase 17 / progress 0/4; `node gsd-tools.cjs query init.milestone-op` resolves (phase_count 4, completed_phases 0, all_phases_complete false, exit 0); .planning/phases/ empty (only .gitkeep, v2.2 dirs archived). Note: gsd-tools not on Bash PATH — invoke via `node ~/.claude/gsd-core/bin/gsd-tools.cjs`. Next = S0-2. | LOOP-LEDGER-ARCHIVE.md `## S0-1`
2026-08-29T21:30Z | milestone-open | v2.3 opened by operator direction in an interactive session: scope researched (6-agent workflow: 2 repo mappers, 3 domain researchers, 1 adversarial critic — journal preserved), .planning/research/V2.3-V2.4-SCOPE.md + REQUIREMENTS.md (REQ-P17-01..P20-04) + ROADMAP.md (Phases 17-20 active, 21-24 queued) written; STATE.md repointed (v2.3, phase 17, 0/4); v2.2 loop artifacts archived to .planning/milestones/v2.2-LOOP-*, v2.2-HUMAN-QUEUE.md; this ledger + LOOP-BRIEF + HUMAN-QUEUE rewritten for v2.3; branch gsd/v2.3.0-test-catalog created from main; firing script repointed + usage-limit backoff added (weekly reset Wednesday 13:00 UTC = 10:00 São Paulo; 5h-window = 60-min hold). Operator directive of record: token limits WILL hit this week — firings log one line and stop on limit errors, the wrapper owns pacing and self-resumes. Next = S0-1. | .planning/research/V2.3-V2.4-SCOPE.md; scripts/run-ceremony-firing.ps1
