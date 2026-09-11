---
gsd_state_version: 1.0
milestone: v2.6
milestone_name: Exploration Depth and Backlog Evidence
status: shipped — v2.6 closed 2026-09-10 (tag `v2.6.0`); v2.6.1 patch (the post-ship liabilities pass) shipped 2026-09-11 (tag `v2.6.1`); no milestone open; the ceremony loop is PAUSED (`.planning/loop-logs/.paused`) until v2.7 opens
stopped_at: "v2.6.1 shipped 2026-09-11: chore/v2.6.1-liabilities merged into main by explicit branch name (--no-ff, rehearsed on a throwaway branch), verified on main and in a fresh clone, tagged v2.6.1 on the merge commit, branch deleted. Nothing open; loop paused; next is opening v2.7 interactively."
last_updated: "2026-09-11T14:09:00.000Z"
last_activity: 2026-09-11
last_activity_desc: "v2.6.1 shipped: ruff + markdownlint adopted and clean, timing pins redesigned on verification evidence, catalogue rows complete, version 2.6.1 everywhere with a test, records backfilled, branch hygiene done, cloud job stopped. Suite 1633 OK on main and in a fresh clone."
progress:
  total_phases: 6
  completed_phases: 6
  total_plans: 16
  completed_plans: 16
  percent: 100
current_phase: 30
current_phase_name: Calibration re-baseline (terminal — milestone shipped)
---

# Project state

**Status:** v2.6 Exploration Depth and Backlog Evidence — **SHIPPED 2026-09-10** (tag
`v2.6.0`, merge commit on `main`); **v2.6.1 SHIPPED 2026-09-11** (patch: the post-ship
liabilities pass, tag `v2.6.1` on its merge commit). **No milestone is open.**
**Progress:** [████████████████████] v2.6 — 6/6 phases, 16/16 plans, 18/18 requirements
Met, milestone audit `passed`; catalogue 279 (zero-mint terminal phase verified);
corpus 42 known-bad + 15 good-control; full suite 1633 OK on the real interpreter (v2.6.1).
**Predecessors:** v2.5.0 and v2.4.1 SHIPPED 2026-09-06 interactively (`ad43ec6`,
`07d3db0`); v2.4 Visual Excellence SHIPPED 2026-09-03 (`v2.4.0`); v2.3 Test Catalog
SHIPPED 2026-09-02 (`v2.3.0`); v2.2 Analytic Surface SHIPPED 2026-08-29 (`v2.2.0`);
v2.0.0 DSX Validity Frame SHIPPED 2026-08-28 (`v2.1.0`). Archives under
`.planning/milestones/` — v2.6's are `v2.6-ROADMAP.md`, `v2.6-REQUIREMENTS.md`,
`v2.6-MILESTONE-AUDIT.md`, `v2.6-LOOP-LEDGER.md`, `v2.6-LOOP-LEDGER-ARCHIVE.md`,
`v2.6-HUMAN-QUEUE.md` and `v2.6-phases/`.

**Loop control:** the autonomous ceremony is **PAUSED** (`.planning/loop-logs/.paused`,
set 2026-09-10 for the interactive close-out). It has nothing to do until a new milestone
exists. `scripts/run-ceremony-firing.ps1` `$Branch` still names
`gsd/v2.6.0-exploration-depth`; its branch guard would abort safely on `main` even if
un-paused. `.planning/LOOP-BRIEF.md` is the v2.6 contract and is rewritten at the next
open; the v2.6 ledger and queue are archived (see above) — there is no active
`LOOP-LEDGER.md` / `HUMAN-QUEUE.md` until v2.7 writes its own.

**Usage-limit posture (proven 2026-08-30 through 2026-09-10):** the firing wrapper
detects limit hits, backs off gracefully, and re-probes every 30 minutes during any
hold to catch an early release. Firings must not retry in a loop — log one line and
stop; the wrapper owns the pacing.

## Project Reference

See: .planning/PROJECT.md (updated 2026-09-10; the Key Decisions table there is the full
decision log, v2.6-01 … v2.6-06 added at this close)

**Core value:** Gate analytical work on validity before the data is touched.
**Current focus:** none open. Candidate scope for v2.7 — every item entry-conditioned
under D-13 (`.planning/ROADMAP.md` `## Next`): `SEED-003` (analyst conduct, notebook
execution integrity, share-vs-risk quantity kinds; medium question settled 2026-09-10),
`SEED-001` E-27 … E-31, `SEED-002`'s producer-side residue, growing the good-control
corpus past 15, brief §6.5 items 1–6.

## Current Position

Phase: none — v2.6 shipped, v2.7 not opened
Plan: —
Status: Between milestones; loop paused by operator switch
Last activity: 2026-09-10 — v2.6 close-out (sign-offs, archive, merge, tag)

## Performance Metrics

v2.6: 6 phases, 16 plans, 113 commits, 176 files changed (+46823/-917),
2026-09-06 → 2026-09-10 (four calendar days of ceremony time; paused 2026-09-08 → 2026-09-10
for travel). Three firings crashed mid-unit and were recovered by orphan adoption.
v2.4: 4 phases, 11 plans, 54 commits, 113 files changed (+15324/-161), 2026-09-02 → 2026-09-03.
v2.3, v2.2, and v2.0.0 velocity are archived with their milestone artifacts.

## Accumulated Context

### Decisions

Full decision log: PROJECT.md Key Decisions. Standing v2.6 decisions, all recorded there:

- **Evidence phases measure first (D-13, applied three times)** — a corpus case is
  run at all four gate points before any check is designed; a caught case closes
  with no mint. All three v2.6 cases were genuine live misses.
- **The profiler is a producer, never a gate** — Phase 25's new keys are provably
  inert to the DQ gate; a gate reading them is a separate D-02/D-06 decision.
- **Attribution-only mints say so in their docstrings** (`DSX-ML-034`, `DSX-CLM-034`);
  `DSX-COH-041` is a real catch and the corpus's first `kind: target`.
- **D-05 honesty over corroboration** — Kaufman shipped labelled secondary-corroborated
  and was upgraded to a first-hand read at close, history kept.
- **Crashed-firing orphans are adopted only after independent re-verification.**
- **Close-out is interactive with the framework's four documented defects bypassed
  by hand** (explicit branch name; plain git; generated records read before commit;
  verification files read directly).

### Pending Todos

None. v2.7 scope is a decision, not a todo — see `SEED-003` and ROADMAP `## Next`.

### Blockers/Concerns

None open. The one soft spot carried forward is a scope observation, not a defect:
the good-control corpus (15 specs) gives a thin false-positive denominator
(one-sided 95 % upper bound ≈0.181 on 0/15); growing it is a v2.7 candidate.

## Deferred Items

Carried forward from earlier closes — captured future ideas, not gaps:

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| seed | SEED-001-deepen-dsx-explore-data-eda-protocol | E-26 shipped in v2.6 Phase 26 (HQ-39); E-27 … E-31 still deferred with their entry conditions | 2026-08-28 |
| seed | SEED-002-grow-data-profile-hermetic-eda-artifacts | Core shipped in v2.6 Phase 25 (HQ-39, reversing HQ-38); residue = a producer-side `parse_health` block (SEED-003 AC-20) | 2026-08-28 |
| seed | SEED-003-analyst-conduct-and-notebook-integrity | Planted 2026-09-10; dormant by design until v2.7 opens with matching scope; six gate candidates (D-13 entry-conditioned), six skill/reference items, one profiler item; medium question settled (two media, explicit boundary) | 2026-09-10 |
| seed | SEED-004-decisions-jsonl-concurrent-writers | Planted 2026-09-11 (v2.6.1 liabilities pass); the recorded WR-02 limitation — concurrent `dsx gate` runs against one root can share an invocation id — with three candidate designs and the test obligations; dormant until a scope actually races two gates on one root | 2026-09-11 |

Acknowledged at the v2.6 milestone close (`gsd-tools query audit-open`, 2026-09-10) — the
seeds above are genuinely deferred; plus one item the CLI flags as open that is **not**
actually open:

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| context-question | 25-CONTEXT.md "open questions" (3 bullets: the D-01 nested-map veto window, the HQ-40 row 40a note, the frozen-vocabulary risk) | **false positive** — all three are non-blocking veto windows / notes closed by silence or by HQ-40 (answered 2026-09-07); the CLI text-matches bold bullet markers that are never rewritten once resolved. Same standing blind spot as at the v2.4 close (21/22/23-CONTEXT.md). | 2026-09-10 |

## Session Continuity

Last session: 2026-09-10 (interactive, the operator present). Resumed the paused loop after
travel; it ran Phase 29's remainder, all of Phase 30 and S7-1/S7-3/S7-4 unattended.
Then interactively: answered the analyst-method evaluation (SEED-003), signed
HQ-41..46 after independent re-verification, upgraded the Kaufman citation to a
first-hand read from the operator-supplied PDF, archived the milestone with the
CLI's generated records hand-corrected (its accomplishment extraction produced
fragments for the fourth consecutive close; its STATE rewrite regressed the
counters), merged into `main` by explicit branch name and tagged `v2.6.0`.
The first merge into `main` was discarded after the post-merge suite failed; five
release defects were fixed on the branch (`e52d7da`, `0f61eb5`), proven green in a fresh clone,
and the merge redone on the fixed tip before tagging.
Stopped at: v2.6 shipped; loop paused; nothing open.
Resume file: None.

2026-09-11 (interactive): post-ship liabilities pass on `chore/v2.6.1-liabilities`
(from `main` = `v2.6.0`): ruff adopted and clean (`348ca6e`), timing pins moved to
scaling-ratio assertions (`40d96f2`; an adversarial verification then found the helper
biased under machine load — redesign in progress), 47 archived summaries backfilled
with `requirements-completed:` plus the missing `29-01-SUMMARY.md` and `SEED-004`
(`b922f76`), markdownlint adopted on the live surface and clean (`530d5bf`), branch
hygiene executed (Operator Next Steps below). Merge to `main` and tag `v2.6.1` only on
the operator's go.

## Operator Next Steps

- **Open v2.7 (interactive):** `/gsd-new-milestone` with scope from `SEED-003` and
  ROADMAP `## Next`; write the new `LOOP-BRIEF.md` / `LOOP-LEDGER.md` /
  `HUMAN-QUEUE.md`; cut `gsd/v2.7.0-<slug>` from `main`; repoint `$Branch` in
  `scripts/run-ceremony-firing.ps1` **before** removing `.planning/loop-logs/.paused`
  — the v2.6 branch it still names was deleted on 2026-09-11 (merged; branch
  hygiene), so an un-paused firing would abort at the wrapper's branch guard.
- **Two kinds of local file stay untracked:** `references/The AI Data Scientist.md`
  (a full-text clipping of an arXiv paper — do not commit) and the `.claude/`,
  `.vscode/`, `graphify-out/` operator files.
- **Branch hygiene done 2026-09-11 (operator: Option A).** Every merged milestone
  branch was deleted locally and on origin; the stale agent worktree was removed
  (its 150-line uncommitted test edit, already in `main` under the same names, is
  kept under `archive/worktree-agent-a9a54fddf75afc02f`); the two unmerged
  `cursor/*` one-commit drafts are kept under `archive/cursor-*` tags. The remote
  `gsd/v2.0.0-dsx-validity-frame` carried 49 no-op `docs(loop)` commits written by a
  **cloud-scheduled Claude Code job** that kept firing the retired v2.0.0 brief every
  ~4 h from 2026-09-01 to 2026-09-11 08:13Z; the operator stopped the job, the tip is
  kept under `archive/v2.0.0-cloud-firings`, and the branch is deleted. If that branch
  reappears on origin, the job is not off.
- **Stamp records from `date -u`**, never from the session's local date — the
  project's convention is UTC and the two diverged at this close.
