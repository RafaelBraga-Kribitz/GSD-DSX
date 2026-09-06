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

- [ ] S0-1 Verify GSD state points at v2.6 (STATE.md frontmatter `milestone: v2.6`,
  `current_phase: 25`, progress 0/6) and `gsd-tools query init.milestone-op`
  resolves it (6 phases, 0 complete); `.planning/phases/` is empty (v2.4 dirs
  archived). Gate: command output pasted.
- [ ] S0-2 Re-verify the scope against the live tree before planning on it:
  per-requirement verdict table (still-valid / already-satisfied / contradicted)
  written to `.planning/v2.6-SCOPE-RECHECK.md`. Premises to re-confirm from
  V2.6-SCOPE.md §2: the profiler's output keys; the DQ assertion vocabulary; the
  explore-skill step ids that name profiler-absent numbers; the five skills with no
  read step; `LEAKAGE_PATTERNS` count; `DSX-MET-030/031` thresholds; the corpus
  counts (39 / 15) and harness obligations; `_SECTION_65_ITEM_IDS` holds items 7, 8,
  9; live catalogue count re-measured (do NOT assume 276). Gate: the recheck file
  with evidence.
- [ ] S0-3 File the **v2.6 D-05 citation evidence pack** to HUMAN-QUEUE as one item:
  Hyndman & Fan 1996 (which type `statistics.quantiles` implements — with the
  Python documentation locator); Kaufman et al. 2012 TKDD (legitimacy condition;
  confirm the author list at the locator); Wilkinson & TFSI 1999 and APA JARS–Quant
  2018 (which one states the operational rule); Gail & Simon 1985 (the
  qualitative-interaction definition). Per-citation table: locator, the exact claim
  the code will cite, confirmed-by-loop vs UNVERIFIED-for-human split. **Do not sign
  — D-05 is a human read.** The documented subgroup-harm case is a Phase 29 research
  deliverable, not part of this pack.

## S1 — Phase 25: Hermetic profile depth (3 requirements)

- [ ] S1-1 Discuss (assumptions mode + persona round); `25-CONTEXT.md` written.
  Must settle: the exact new key names and nesting in `DATA-PROFILE.yaml`
  (additive under `columns[]`, `time`, plus new `unit` and `target` blocks); the
  quantile type and `sd` definition; the `--unit`/`--target` CLI flags; the
  byte-stability guard's shape (regenerate the two committed example profiles and
  diff on existing keys); the explicit exclusions (null cross-tabs, outlier
  taxonomy, invariants, robust metric recomputes).
- [ ] S1-2 Plan (plan-checker must pass). Research verifies the Hyndman & Fan type
  mapping against the Python docs and the paper before any test asserts a number.
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
