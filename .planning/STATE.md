---
gsd_state_version: 1.0
milestone: v2.6
milestone_name: Exploration Depth and Backlog Evidence
current_phase_name: Evidence case — feature-origin-only leak
status: in-progress — S3-1 partial (design settled, mint parked on Kaufman)
stopped_at: S3-1 PARTIAL (box UNCHECKED). §4 persona round on the OPEN QUESTION resolved: dsx-ml-integrity-auditor + dsx-analysis-architect (opus, parallel, grounded) BOTH voted YES — the citation-independent D-13 measurement spike on Phase 27's feature-origin-only-leak case IS extractable ahead of the HQ-40 Kaufman read. Verified structurally at dsx/checks/ml.py: every ml check is a spec-DECLARATION check reading model.*/results.* off the parsed spec — none open the extract or inspect actual values, so the feature-origin defect is invisible to the gate; the measurement's dependency graph excludes Kaufman entirely (ml.py cites Saito–Rehmsmeier/-043, Varma–Simon/-052-053, Cawley–Talbot/-090-092, NOT Kaufman). Kaufman attaches ONLY to the docstring of a mint that happens ONLY on a live miss. 27-CONTEXT.md written with the citation-independent design SETTLED+FROZEN (D-27-01 case shape: churn fixture, innocuous `account_health_index` recomputed nightly from the outcome window, honest declarations incl. both train_score+test_score; D-27-02 pass/fail rule with the swap-still-fires incidental-code counterfactual + the DSX-ML-060/061/053/080 watch list) and the mint PARKED on HQ-40 row 40b (feature_provenance vocab DRAFT-only, active DSX-ML-034 mint parked). D-27-03: reserved absent_code = DSX-ML-034 (RESERVE-INACTIVE; next-free-IN-FAMILY in the 03x leakage sub-family, live catalogue re-measured: 030-033 occupied, gap 034-039, global max 092; 093 rejected by family placement); D-06 veto window OPEN, silence=accept. Re-scope of the BLOCK (not a requirement) recorded loudly, not escalated. Next = S3-3 measurement spike: build the D-27-01 fixture + MEASURE at all four gate points from a fresh tempdir, apply the D-27-02 rule (caught → no-mint close, Kaufman moot; live miss → stop at the mint boundary, hold for HQ-40 40b).
last_updated: "2026-09-07T09:40:00.000Z"
last_activity: 2026-09-07
last_activity_desc: Phase 27 S3-1 partial — §4 persona round resolved the OPEN QUESTION (both YES: measurement spike is citation-independent); 27-CONTEXT.md written (design SETTLED/FROZEN, mint PARKED on Kaufman, DSX-ML-034 reserved RESERVE-INACTIVE with an open D-06 veto window); box left UNCHECKED. Next = S3-3 measurement spike.
progress:
  total_phases: 6
  completed_phases: 2
  total_plans: 8
  completed_plans: 8
  percent: 33
current_phase: 27
---

# Project state

**Status:** v2.6 Exploration Depth and Backlog Evidence — ACTIVE (opened 2026-09-06 by operator direction, HQ-39); branch `gsd/v2.6.0-exploration-depth`; ships as tag `v2.6.0`
**Progress:** [██████░░░░░░░░░░░░░░░] v2.6 — 2/6 phases (✅25 hermetic profile depth → ✅26 per-skill read contracts → 🔄27 feature-origin-only leak case (S3-1 partial) → 28 magnitude-no-test case → 29 subgroup-harm case → 30 calibration re-baseline)
**Predecessors:** v2.5.0 and v2.4.1 SHIPPED 2026-09-06 interactively (`ad43ec6`, `07d3db0`); v2.4 Visual Excellence SHIPPED 2026-09-03 (tag `v2.4.0`); v2.3 Test Catalog SHIPPED 2026-09-02 (`v2.3.0`); v2.2 Analytic Surface SHIPPED 2026-08-29 (`v2.2.0`); v2.0.0 DSX Validity Frame SHIPPED 2026-08-28 (`v2.1.0`). Archives under `.planning/milestones/`.

**Loop control:** the autonomous ceremony drives this milestone from S0-1 onward per
`.planning/LOOP-BRIEF.md` and `.planning/LOOP-LEDGER.md` (18 requirements, stages
S0–S7). The pause flag was removed at open; `scripts/run-ceremony-firing.ps1`
`$Branch` points at `gsd/v2.6.0-exploration-depth`. S7-5 (`/gsd-complete-milestone`)
and S7-6 (ship) run interactively per the ledger's own design.

**Usage-limit posture (proven 2026-08-30 through 2026-09-03):** the firing
wrapper detects limit hits, backs off gracefully, and re-probes every 30 minutes
during any hold to catch an early release rather than blindly waiting the full
computed window. Firings must not retry in a loop — log one line and stop; the
wrapper owns the pacing.

## Project Reference

See: .planning/PROJECT.md (updated 2026-09-03; Key Decisions table there is the full decision log)

**Core value:** Gate analytical work on validity before the data is touched.
**Current focus:** v2.6 Exploration Depth and Backlog Evidence — Phase 25 (hermetic
profile depth) is first. Scope in `.planning/research/V2.6-SCOPE.md`; requirements
REQ-P25-01 … REQ-P30-03 in `.planning/REQUIREMENTS.md`. The one rule that shapes the
milestone: Phases 27–29 measure their corpus case live before any check is designed,
and a case the gate already catches closes its phase with no mint (D-13).

## Current Position

Phase: 27 — Evidence case, feature-origin-only leak (S3-1 discuss PARTIAL; box UNCHECKED)
Plan: none yet. S3-1 §4 persona round resolved the OPEN QUESTION — both personas YES: the D-13 measurement spike is citation-independent of the pending Kaufman read. 27-CONTEXT.md written (design SETTLED/FROZEN; mint PARKED on Kaufman; DSX-ML-034 reserved RESERVE-INACTIVE, D-06 veto window open).
Status: In-progress — the milestone is NOT all-blocked. The citation-independent design+measurement path is open; only the mint (its Kaufman docstring + active DSX-ML-034 code) is blocked on HQ-40 row 40b. Next = S3-3 measurement spike (build fixture + measure four gate points, fresh tempdir).
Last activity: 2026-09-07 — Phase 27 S3-1 partial: persona round (auditor + architect, both YES); 27-CONTEXT.md written; DSX-ML-034 reserved; box left UNCHECKED

## Performance Metrics

v2.4: 4 phases, 11 plans, 54 commits, 113 files changed (+15324/-161), 2026-09-02 → 2026-09-03.
v2.3, v2.2, and v2.0.0 velocity are archived with their milestone artifacts.

## Accumulated Context

### Decisions

Full decision log: PROJECT.md Key Decisions. Standing v2.4 decisions (carried from the original v2.3/v2.4 scoping, operator-directed 2026-08-29, re-confirmed at open):

- **The chart catalog is citable, not exhaustive-for-its-own-sake** — union of five named taxonomies (FT Visual Vocabulary, Wilke, Graphic Continuum, DVC, Datawrapper) after synonym merge and principled exclusions, target band 75–90 entries.
- **License audit is a plan-review gate, not an afterthought** — dsx-538/dsx-urban forked or built from permissively-licensed sources; dsx-econ/dsx-bbc reimplemented from published doctrine only, never porting GPL code (bbplot) or embedding an unlicensed PDF (the 2017 Economist styleguide).
- **Faceting is a declaration, not a chart type** — `facet_by` orthogonal to the mark, per the scope research's completeness-critic finding.
- **Contingency:** split Phase 23–24 off as v2.5 if the D-05 queue materially outruns cadence (expected lighter than v2.3's — ~8–12 reads vs 27).

### Pending Todos

None beyond the ledger.

### Blockers/Concerns

**The milestone is NOT all-blocked.** The S3-1 §4 persona round (auditor + architect,
both YES) established that Phase 27's D-13 measurement spike is **citation-independent**
of the pending Kaufman read: only the *mint* (its Kaufman docstring + active DSX-ML-034
code) is blocked on HQ-40 row 40b. The next firing runs the **S3-3 measurement spike**
(build the D-27-01 fixture, measure all four gate points from a fresh tempdir) — a case
the existing gate catches closes Phase 27 with no mint and moots Kaufman; a live miss
stops cleanly at the mint boundary and holds for HQ-40 40b. S4-1 (Wilkinson/JARS) and
S5-1 (Gail & Simon) remain blocked on their HQ-40 rows; the same citation-independent
measurement-spike pattern may apply to Phases 28–29 and should be evaluated per-phase.

## Deferred Items

Carried forward from v2.0.0 close — captured future ideas, not gaps:

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| seed | SEED-001-deepen-dsx-explore-data-eda-protocol | E-26 promoted into v2.6 Phase 26 (HQ-39); E-27 … E-31 still deferred with their entry conditions | 2026-08-28 |
| seed | SEED-002-grow-data-profile-hermetic-eda-artifacts | PROMOTED into v2.6 Phase 25 by operator direction (HQ-39, reversing HQ-38 the same day) | 2026-08-28 |

Acknowledged at v2.4 milestone close (`gsd_run query audit-open`, 2026-09-03) — the two
seeds above, genuinely deferred; plus 3 items the CLI flags as open that are **not**
actually open:

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| context-question | 21-CONTEXT.md open questions (HQ-28) | **false positive** — HQ-28 answered 2026-09-03 (accepted, no veto); the CLI text-matches "open question" bullet markers in CONTEXT.md, which are never rewritten once the linked HUMAN-QUEUE item resolves. Standing CLI blind spot, same class as `/gsd-audit-uat`'s documented under-reporting. | 2026-09-03 |
| context-question | 22-CONTEXT.md open questions (HQ-30) | same false positive — HQ-30 answered 2026-09-03 (accepted, no veto) | 2026-09-03 |
| context-question | 23-CONTEXT.md open questions (HQ-32) | same false positive — HQ-32 answered 2026-09-03 (accepted, no veto) | 2026-09-03 |

## Session Continuity

Last session: 2026-09-06 (interactive). Shipped v2.4.1 (`07d3db0`) and v2.5.0
(`ad43ec6`); recorded HQ-38 (hold SEED-002); then, on operator direction, opened
v2.6 with both halves (HQ-39, reversing HQ-38): scope document, 18 requirements,
roadmap Phases 25–30, brief/ledger/queue rewritten, v2.4 loop artifacts archived,
wrapper repointed, pause flag removed.
Stopped at: milestone open committed and pushed on `gsd/v2.6.0-exploration-depth`;
the ceremony's next firing starts at S0-1.
Resume file: None — the loop reads `LOOP-LEDGER.md`'s Log.

## Operator Next Steps

- **Nothing blocks the loop today.** S0-3 will file the v2.6 D-05 citation evidence
  pack as HQ-40 (Hyndman & Fan 1996; Kaufman et al. 2012; Wilkinson & TFSI 1999 /
  APA JARS 2018; Gail & Simon 1985). Phases 25–26 do not wait on it; Phases 27–29
  do, row by row. Answer it in an interactive session when convenient.

- **S7-5 / S7-6 are interactive** (`/gsd-complete-milestone`, merge by explicit
  branch name, tag `v2.6.0`), as at every prior close.

- **Two kinds of local file stay untracked:** `references/The AI Data Scientist.md`
  (a full-text clipping of an arXiv paper — do not commit) and the `.claude/`,
  `.vscode/`, `graphify-out/` operator files.

- The stale agent worktree at `.claude/worktrees/agent-a9a54fddf75afc02f` is fully
  merged into `main`; `git worktree remove` it at leisure.
