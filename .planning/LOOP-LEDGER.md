# LOOP-LEDGER — v2.6 Exploration Depth and Backlog Evidence

Source of truth for the autonomous loop. One checkbox = one unit.
Check a box ONLY with its gate evidence pasted in the Log (one line; long
evidence to `LOOP-LEDGER-ARCHIVE.md`).

**Scope source:** `.planning/research/V2.6-SCOPE.md` (2026-09-06) and
`.planning/REQUIREMENTS.md` (18 requirements, REQ-P25-01 … REQ-P30-03). Both carry
the live-tree facts, the D-05 citation candidates (UNVERIFIED until the human read),
the ordering and the contingency — **this milestone needs execution, not a fresh
scoping round.**

**Predecessors:** v2.4 Visual Excellence shipped 2026-09-03 (tag `v2.4.0`); v2.4.1
and v2.5.0 shipped interactively 2026-09-06; v2.3 shipped 2026-09-02 (`v2.3.0`);
v2.2 shipped 2026-08-29 (`v2.2.0`); v2.0.0 shipped 2026-08-28 (`v2.1.0`). Loop
artifacts archived at `.planning/milestones/v2.4-LOOP-*`, `v2.4-HUMAN-QUEUE.md`, and
earlier milestones' equivalents.

## Ordering rationale

Phases run in numeric order **25 → 26 → 27 → 28 → 29 → 30**: Phase 25 produces the
profile keys Phase 26's read contracts name (hard block); Phases 27–29 are
independent evidence cases run sequentially on one branch; Phase 30 is terminal and
re-baselines calibration with the new cases classified. The human reads (5–6 D-05
items across Phases 25, 27, 28, 29) are the longest pole — filed as one evidence pack
at S0-3 so the operator reads asynchronously while Phase 25 builds.

**Standing v2.6 rules (from the brief §5, repeated because they bind every unit):**
the profiler is a producer, never a gate — `dsx/checks/dq.py`, the assertion
vocabulary and the gate profiles stay byte-unchanged, and existing profile keys and
values are byte-stable; every evidence phase MEASURES its corpus case live before any
check is designed, and a case the gate already catches closes the phase with no mint;
every skill/template/reference edit is mirrored by `node install.mjs` and
`--check` must pass; every minted code carries D-05 (citation confirmed by a human
read + structural criterion + `# D-05:` test marker + exact-code allowlist entry).

## S0 — Milestone bootstrap

- [x] S0-1 Verify GSD state points at v2.6 (STATE.md frontmatter `milestone: v2.6`,
  `current_phase: 25`, progress 0/6) and `gsd-tools query init.milestone-op`
  resolves it (6 phases, 0 complete); `.planning/phases/` is empty (v2.4 dirs
  archived). Gate: command output pasted. **DONE 2026-09-06** — STATE.md fm
  `milestone: v2.6` / `current_phase: 25` / `total_phases: 6, completed_phases: 0,
  percent: 0`; `init.milestone-op` → `milestone_version: v2.6, phase_count: 6,
  completed_phases: 0, all_phases_complete: false`; `.planning/phases/` holds only
  `.gitkeep`.
- [x] S0-2 Re-verify the scope against the live tree before planning on it:
  per-requirement verdict table (still-valid / already-satisfied / contradicted)
  written to `.planning/v2.6-SCOPE-RECHECK.md`. Premises to re-confirm from
  V2.6-SCOPE.md §2: the profiler's output keys; the DQ assertion vocabulary; the
  explore-skill step ids that name profiler-absent numbers; the five skills with no
  read step; `LEAKAGE_PATTERNS` count; `DSX-MET-030/031` thresholds; the corpus
  counts (39 / 15) and harness obligations; `_SECTION_65_ITEM_IDS` holds items 7, 8,
  9; live catalogue count re-measured (do NOT assume 276). Gate: the recheck file
  with evidence. **DONE 2026-09-06** — `.planning/v2.6-SCOPE-RECHECK.md`: 13 §2
  premises re-measured, all confirmed; 18/18 requirements still-valid (5 conditional
  per D-13), 0 already-satisfied, 0 contradicted. Live catalogue = 276
  (`gen-finding-catalogue.py --check` "current" + 276 rows counted). Two cosmetic
  discrepancies noted (scope's `time_column` is the profile's `time.column`, not a
  DQ assertion key; `source_path` omitted from §2 list) — neither touches a gate.
- [x] S0-3 File the **v2.6 D-05 citation evidence pack** to HUMAN-QUEUE as one item:
  Hyndman & Fan 1996 (which type `statistics.quantiles` implements — with the
  Python documentation locator); Kaufman et al. 2012 TKDD (legitimacy condition;
  confirm the author list at the locator); Wilkinson & TFSI 1999 and APA JARS–Quant
  2018 (which one states the operational rule); Gail & Simon 1985 (the
  qualitative-interaction definition). Per-citation table: locator, the exact claim
  the code will cite, confirmed-by-loop vs UNVERIFIED-for-human split. **Do not sign
  — D-05 is a human read.** The documented subgroup-harm case is a Phase 29 research
  deliverable, not part of this pack. **DONE 2026-09-06** — filed as HQ-40 (5 rows
  40a–40e), UNSIGNED. Confirmed-by-loop column grounded on live measurement (Python
  3.12.10 `quantiles` reference values; `LEAKAGE_PATTERNS`=10 name-only; MET-030/031
  all/≥half thresholds); primary-source claims left UNVERIFIED for the human read.
  Blocks recorded row-by-row (Kaufman→S3-1, Wilkinson/JARS→S4-1, Gail&Simon→S5-1).

## S1 — Phase 25: Hermetic profile depth (3 requirements)

- [x] S1-1 Discuss (assumptions mode + persona round); `25-CONTEXT.md` written.
  Must settle: the exact new key names and nesting in `DATA-PROFILE.yaml`
  (additive under `columns[]`, `time`, plus new `unit` and `target` blocks); the
  quantile type and `sd` definition; the `--unit`/`--target` CLI flags; the
  byte-stability guard's shape (regenerate the two committed example profiles and
  diff on existing keys); the explicit exclusions (null cross-tabs, outlier
  taxonomy, invariants, robust metric recomputes). **DONE 2026-09-06** —
  `.planning/phases/25-hermetic-profile-depth/25-CONTEXT.md`: 4 decisions (D-01
  nesting; D-02 stat defs; D-03 CLI flags; D-04 guard) + named exclusions + full
  edge vocabulary + fixture reference values. Architect + Statistician persona
  round (opus, parallel); 3 divergences resolved by rigour>reliability>flexibility
  (quantile=inclusive/type-7; edge-period grain=ISO-week; share_at_hour_00=null on
  date-only). Zero codes; guard = Option B fixtures + recorded REQ-P25-02
  interpretation (flagged for plan-gate ratification).
- [x] S1-2 Plan (plan-checker must pass). Research verifies the Hyndman & Fan type
  mapping against the Python docs and the paper before any test asserts a number.
  **DONE 2026-09-07** — 4 plans written (`25-01`…`25-04`-PLAN.md), 4 sequential waves,
  TDD-typed statistic plans + execute close-out. `gsd-planner` (opus) → `## PLANNING
  COMPLETE`; `gsd-plan-checker` (haiku, per adaptive) → `## VERIFICATION PASSED`
  (15 dimensions). Orchestrator **re-verified the gate itself** (brief mandate): grep
  confirms REQ-P25-01/02/03 all in frontmatter; D-01/D-02 in all 4, D-03 in 25-03,
  D-04 in 25-01/25-04; D-02 quantile pinned `method='inclusive'` = H&F type 7 with
  hand-computed reference values (`sd=3.0276503540974917`, `q1=3.25`); `<threat_model>`
  + `<artifacts_this_phase_produces>` in all 4; single-writer prohibition in all 4;
  all 13 spec-less-probe edges authored as covered truths (0 backstop, no silent drop);
  27 byte-stability/catalogue markers. §13a decision-coverage-plan **false-blocked**
  (`could-not-parse` on `- **D-04 — …**` — the documented parser mismatch, HUMAN-QUEUE
  standing note); overridden via the confirmed Dim-7 + independent grep. dsx plan:post
  gate exits 0 (require_spec disabled — this is engineering, not analysis). VALIDATION.md
  seeded; planner corrected its framework field (unittest, not pytest — verified no
  pyproject/pytest.ini; `scripts/check.sh` = `unittest discover`).
- [ ] S1-3 Execute all plans (profiler growth; fixture CSVs + reference-value tests;
  determinism test; template/reference/skill ripple; installer re-sync).
- [ ] S1-4 Code review + fixes; verification `passed` (REQ-P25-01..03; byte-stable
  existing keys proven; `dsx/checks/dq.py` byte-identical; 276 → 276 set-identity).
- [ ] S1-5 `/gsd-secure-phase 25` verified + `/gsd-validate-phase 25` compliant.
  End-of-phase security sign-off + UAT batched to HUMAN-QUEUE (non-blocking until
  S7-2).

## S2 — Phase 26: Per-skill read contracts (3 requirements)

- [ ] S2-1 Discuss + persona round; `26-CONTEXT.md`. Must settle: the per-skill
  key mapping (V2.6-SCOPE.md §3 Phase 26 table is the starting proposal, not the
  decision); the read-step's fixed heading so the repo-integrity test can find it;
  the fallback wording. Blocked until S1-5.
- [ ] S2-2 Plan (plan-checker must pass).
- [ ] S2-3 Execute all plans (five skill edits; the repo-integrity test; installer
  re-sync).
- [ ] S2-4 Code review + fixes; verification `passed` (REQ-P26-01..03; `git diff
  --stat -- dsx/` empty for the phase; `node install.mjs --check` passes).
- [ ] S2-5 `/gsd-secure-phase 26` + `/gsd-validate-phase 26`; sign-off batched.

## S3 — Phase 27: Evidence case — feature-origin-only leak (3 requirements)

- [ ] S3-1 Discuss + persona round; `27-CONTEXT.md`. Must settle: the case's exact
  shape (which innocuous column, which pre-joined source, which honest declarations)
  and the pass/fail rule for "live miss"; the reserved `absent_code` number for the
  sidecar (D-06 persona round, recorded with a veto window); the provenance
  declaration's field vocabulary IF the miss is live. Blocked until S0-3's Kaufman
  row is human-answered for the citation the code would carry.
- [ ] S3-2 Plan (plan-checker must pass).
- [ ] S3-3 Execute: build and MEASURE the case first (all four points, fresh
  tempdir, recorded); then, only if a live miss, the declaration + check + D-05 +
  harness entries; otherwise the no-mint record.
- [ ] S3-4 Code review + fixes; verification `passed` (REQ-P27-01..03).
- [ ] S3-5 `/gsd-secure-phase 27` + `/gsd-validate-phase 27`; sign-off batched.

## S4 — Phase 28: Evidence case — magnitude no test computed (3 requirements)

- [ ] S4-1 Discuss + persona round; `28-CONTEXT.md`. Must settle: the case's claim
  text and test roster; which existing checks must be shown to clear (`DSX-CLM-070`,
  `DSX-STA-012`, `DSX-NAR-*`); the rounding-tolerance rule; the reserved number.
  Blocked until S0-3's Wilkinson/JARS row is human-answered.
- [ ] S4-2 Plan (plan-checker must pass).
- [ ] S4-3 Execute: measure first, then (if live miss) `supported_by` + overlap
  check + D-05 + harness; otherwise the no-mint record.
- [ ] S4-4 Code review + fixes; verification `passed` (REQ-P28-01..03).
- [ ] S4-5 `/gsd-secure-phase 28` + `/gsd-validate-phase 28`; sign-off batched.

## S5 — Phase 29: Evidence case — subgroup harm under a prescriptive recommendation (3 requirements)

- [ ] S5-1 Discuss + persona round; `29-CONTEXT.md`. Must settle: the segment
  floor's declaration; the case's four-segment shape; the disposition vocabulary;
  the reserved number. Blocked until S0-3's Gail & Simon row is human-answered.
- [ ] S5-2 Plan (plan-checker must pass). Research must find — or record as not
  found — a documented public case with a primary source where an average benefit
  masked subgroup harm (REQ-P29-02); "not found" is a valid, recorded outcome.
- [ ] S5-3 Execute: measure first, then (if live miss AND source confirmed AND case
  found) `decision.subgroup_harm[]` + check + D-05 + harness; otherwise the no-mint
  record with the half-met condition stated.
- [ ] S5-4 Code review + fixes; verification `passed` (REQ-P29-01..03).
- [ ] S5-5 `/gsd-secure-phase 29` + `/gsd-validate-phase 29`; sign-off batched.

## S6 — Phase 30: Calibration re-baseline (3 requirements)

- [ ] S6-1 Discuss (light — calibration shape is Phase-12/20/24-precedented);
  `30-CONTEXT.md`.
- [ ] S6-2 Plan (plan-checker must pass).
- [ ] S6-3 Execute (re-measure headline + strata with the new cases classified;
  §6.5 rows 7–9 rewritten; literature record updated; prerequisites green).
- [ ] S6-4 Code review + fixes; verification `passed` (REQ-P30-01..03).
- [ ] S6-5 `/gsd-secure-phase 30` + `/gsd-validate-phase 30`; sign-off batched.

## S7 — Close-out

- [ ] S7-1 `/gsd-audit-uat` cross-phase sweep. **Do NOT accept the CLI's "All
  Clear"** — known under-reporting defects documented in HUMAN-QUEUE's Standing
  framework notes; hand-check every phase's `NN-VERIFICATION.md`.
- [ ] S7-2 Drain HUMAN-QUEUE (the only permitted blocking wait).
- [ ] S7-3 `/gsd-extract-learnings`.
- [ ] S7-4 `/gsd-audit-milestone` — must reach `passed`.
- [ ] S7-5 `/gsd-complete-milestone` — **NOT headless-safe** (interactive prompts +
  `git rm REQUIREMENTS.md`); runs in an interactive session per operator approval.
  Hand-verify the CLI's generated accomplishments and the archived REQUIREMENTS
  checkboxes (wrong at every close so far — expect the same defect class again).
- [ ] S7-6 Ship: merge to `main` **by explicit branch name**
  (`git merge --no-ff gsd/v2.6.0-exploration-depth`, verified on a throwaway
  branch first, full suite + `scripts/check.sh` green BEFORE touching `main`)
  and tag `v2.6.0` on the merge commit. **Never** the framework's alphabetical
  `gsd/*` auto-detect (six stale `gsd/*` branches would be picked instead).

## Log

Format: `YYYY-MM-DDTHH:MMZ | unit | outcome | evidence pointer`. Most recent ~15–20
entries here; older entries move to `LOOP-LEDGER-ARCHIVE.md` (never deleted).

2026-09-06T20:45Z | milestone-open | v2.6 opened interactively by operator direction (HQ-39, reversing HQ-38): branch `gsd/v2.6.0-exploration-depth` cut from `main` at `d2f0140`; v2.4 loop artifacts archived to `.planning/milestones/v2.4-LOOP-LEDGER*.md` and `v2.4-HUMAN-QUEUE.md`; LOOP-BRIEF/LEDGER/QUEUE rewritten; REQUIREMENTS.md (18) + ROADMAP.md (Phases 25–30) + PROJECT.md + STATE.md written; wrapper `$Branch` repointed; `.paused` removed. Next = S0-1. | V2.6-SCOPE.md; REQUIREMENTS.md
2026-09-06T22:20Z | milestone-open (follow-up) | First firing (22:04Z) died in 5 s: the headless `claude -p` inherited the interactive session's `/model` choice (a Fable-tier model) via ~/.claude/settings.json, and the npm `claude` on the task's PATH is 2.1.218, which refuses it. Fixed in the wrapper, not in settings: `scripts/run-ceremony-firing.ps1` now pins `--model $Model` ($Model = 'opus', the brief's orchestration-grade alias), proven with a PROBE-OK on the same binary. The loop's model is now a recorded decision of the script, independent of the operator's terminal. Next = S0-1. | scripts/run-ceremony-firing.ps1; .planning/loop-logs/firing-20260906-220427.log
2026-09-06T22:35Z | S0-1 | DONE — GSD state confirmed at v2.6 against repo. Reconciled ledger vs repo first: HEAD `4905e32` on `gsd/v2.6.0-exploration-depth`, up to date with origin, only operator-local untracked files — ledger accurate, no correction. STATE.md fm + `init.milestone-op` (v2.6 / 6 phases / 0 complete) + empty `.planning/phases/` all agree. Next = S0-2. | ledger S0-1 evidence
2026-09-06T22:50Z | S0-2 | DONE — scope re-verified live, executable as written; no re-scoping round. 13 §2 premises re-measured (profiler still shallow-only; dq.py vocab+codes frozen; 5 skills 0 read-cues; LEAKAGE_PATTERNS=10; MET-030 all-oppose / MET-031 >=half so 1-of-4 fires neither → P29 gap real; corpus 39/15; §6.5 ids hold items 7/8/9; catalogue LIVE=276; spec count=42). 18/18 reqs still-valid, 0 already-satisfied, 0 contradicted. 2 cosmetic scope-table nits noted. Next = S0-3. | .planning/v2.6-SCOPE-RECHECK.md
2026-09-06T23:02Z | S0-3 | DONE — D-05 citation evidence pack filed as HQ-40 (rows 40a–40e), UNSIGNED per D-05. Loop prepared the confirmed-by-loop split on live evidence only (Python 3.12.10 quantile reference values; LEAKAGE_PATTERNS name-only; MET thresholds); every primary-source claim left UNVERIFIED for the human read. Non-blocking for P25–26; Kaufman→S3-1, Wilkinson/JARS→S4-1, Gail&Simon→S5-1. **S0 bootstrap complete; next = S1-1 (Phase 25 discuss).** | HUMAN-QUEUE.md HQ-40
2026-09-06T22:42Z | clock-note | The three S0 log timestamps ran ~45m fast (S0-3 says 23:02Z but committed 22:15Z UTC per `git %cI`). Reverting to real UTC from `date -u`, verifiable against commit times; this and later entries may read earlier than the inflated S0-3 line. | git log %cI
2026-09-06T22:42Z | S1-1 | DONE — Phase 25 discuss complete; `25-CONTEXT.md` written (`.planning/phases/25-hermetic-profile-depth/`). Persona round: dsx-analysis-architect + dsx-statistician (opus, parallel, grounded so no re-exploration). Converged on nesting, CLI shape, guard, edge conventions; 3 divergences resolved by rigour>reliability>flexibility — (1) quantile method = **inclusive/H&F type-7** (byte-agrees with pandas/numpy/R the sceptical reader cross-checks; overrides HQ-40 40a's parenthetical exclusive lean — human read confirms the type *number*); (2) edge-period grain = **ISO-week** not day (day-grain fires "partial" near-constantly on event extracts); (3) `share_at_hour_00` = **null on date-only** (excludes date-only from denominator). D-04 guard = Option B (fixture CSVs + reference-value/determinism/pre-existing-key-golden tests; example profiles byte-invariant), with a recorded REQ-P25-02 interpretation flagged for S1-2 plan-gate ratification (operationalises, does not reword). Zero codes minted → no HQ D-06 veto item owed; design decisions vetoable via CONTEXT (silence=accept). Next = S1-2 (Phase 25 plan; pins the H&F type against the paper). | .planning/phases/25-hermetic-profile-depth/25-CONTEXT.md
2026-09-07T01:36Z | S1-2 (research sub-stage; box stays UNCHECKED) | Phase 25 RESEARCH.md written+committed `1f8a052` (pushed; reconciled against repo per the standing note — HEAD on canonical `gsd/v2.6.0-exploration-depth`, no stray branch, tree clean but the operator-local untracked). `gsd-phase-researcher` on **sonnet** (adaptive profile, not overridden). Findings (all in RESEARCH.md): inclusive = **H&F type-7** / exclusive = type-6, triangulated from the INSTALLED CPython 3.12.10 `statistics.py` source comments (R6/R7, quotes H&F) + R type-6/7 formula identity — primary-source authenticity stays HQ-40 40a's human read (non-blocking: definition test, no mint); `mean`/`stdev` exact-Fraction ⇒ order-independent & cross-platform byte-stable (`fmean` excluded); D-04 REQ-P25-02 interp = **PASS + add an explicit example-profile byte-diff test**; DQ gate reads 6 named keys via `.get()` so it ignores new keys (prove by test, don't assume); `Counter.most_common()` tie order = CSV row order, a real determinism pitfall vs the frozen count-desc/string-asc rule. `## Validation Architecture` @L666 ⇒ next firing can mint VALIDATION.md. Stopped at the ~12-min pacing cap — planner+checker is the next chunk, not started to avoid an auto-compaction mid-gate. **Resume: re-run `/gsd-plan-phase 25` (has_research=true ⇒ auto-uses RESEARCH.md) → `gsd-planner` (opus) → `gsd-plan-checker` gate; S1-2 checks ONLY when plan-checker passes.** | .planning/phases/25-hermetic-profile-depth/25-RESEARCH.md; 1f8a052
2026-09-07T02:58Z | S1-3 (plan 25-01 of 4; box stays UNCHECKED) | Plan 25-01 executed by `gsd-executor` (sonnet, §3 routing) + **gates re-run by orchestrator** on real interpreter (3.12.10). Reconciled: HEAD `a100f00`, 6 atomic commits, **no stray branch**, only operator-local untracked. Hermetic module 14/14 OK; independent `statistics.quantiles` check = q1 3.25/median 5.5/q3 7.75, sd `3.0276503540974917` (matches pins); **full suite 1542 OK**; two explain tests did NOT false-fail. Code read-confirmed: inclusive/type-7 quantiles, sample stdev, explicit `sorted((-count,level))`. FINDING for S1-4 (test-efficacy, not a bug): `test_top10_tie_boundary` is non-discriminating — m,n both count 5 ⇒ `share_top10`=104/109 invariant to tie-break; string-asc among equal-count levels is unobservable in the aggregate. Stopped at plan boundary (~12-min pacing cap; executor alone ~10 min). **Resume: execute plan 25-02** (wave 2, time+unit blocks). | LOOP-LEDGER-ARCHIVE.md ## S1-3; 25-01-SUMMARY.md; a100f00
2026-09-07T03:22Z | S1-3 (plan 25-02 of 4; box stays UNCHECKED) | Plan 25-02 executed by `gsd-executor` (sonnet, §3 routing) + **gates re-run by orchestrator** on real 3.12.10. Reconciled: HEAD `bb82a66`, 4 atomic commits (`e2068a5`→`bb82a66`), **no stray branch**, ahead 4 of origin, only operator-local untracked. `git diff --stat 825d7fe..HEAD` = `dsx/profiler.py` + 8 fixtures + tests + SUMMARY only — **no `dsx/checks/*` touched** ⇒ 276→276 by construction. Gates: TestTimeBlock+Determinism **14 OK** (incl. pre-existing-key golden ⇒ frozen time.min/max/max_gap_days byte-unchanged, + 2 determinism tests); TestUnitBlock **6 OK**; **full suite 1560 OK** (+18 vs 1542; only pre-existing catalogue warnings, explain tests did NOT false-fail). p95 pinned `80.8` (type-7 on [1,2,3,4,100]); new time keys gated on `--time` so golden keeps its 4-key shape (accepted). Stopped at plan boundary (~12-min cap). **Resume: execute plan 25-03** (CLI `--unit`/`--target` flags), then 25-04 (ripple + installer re-sync), then S1-3 checks. | LOOP-LEDGER-ARCHIVE.md ## S1-3 (plan 25-02 slice); 25-02-SUMMARY.md; bb82a66
2026-09-07T02:35Z | S1-2 | DONE — Phase 25 planned; plan-checker PASSED; gate re-verified by orchestrator. Ran `/gsd-plan-phase 25` end-to-end: seeded 25-VALIDATION.md (Nyquist draft; ## Validation Architecture present @RESEARCH L666), ran the §7.95 spec-less edge probe (13 applicable edges → planner authored all 13 as covered must_haves), spawned `gsd-planner` (opus) → 4 plans across 4 waves, then `gsd-plan-checker` (haiku, adaptive — NOT overridden; §3 table is for the loop's direct spawns, and the design decision was opus's so the sonnet-class-design rule holds; this config gated v2.3/v2.4 to passed). Re-verified myself: REQ-P25-01/02/03 covered; D-01..D-04 covered; D-02 quantile=inclusive/type-7 with hand-computed ref values; threat_model + artifacts sections + single-writer prohibition in all 4; 27 byte-stability/catalogue markers. §13a decision-coverage FALSE-BLOCKED (could-not-parse on `- **D-04 — …**`, documented parser mismatch) → overridden per HUMAN-QUEUE standing note via confirmed Dim-7 + grep. dsx plan:post exits 0 (require_spec disabled — engineering, not analysis). Did NOT auto-advance to execute despite auto_advance=true — unit boundary (S1-3 is a separate unit). Reconciled: no stray branch, canonical HEAD. Persona/routing decisions recorded loudly (no D-06 mint owed — zero codes). Non-blocking flags carried: HQ-40 40a still pending (definition test, non-blocking); 2 vetoable additive keys (numeric `n`, per-week `n`) silence=accept; `rows_per_unit.p95` literal pinned at execute. **Next = S1-3 (execute all 4 plans).** | .planning/phases/25-hermetic-profile-depth/25-0{1,2,3,4}-PLAN.md; 25-VALIDATION.md
