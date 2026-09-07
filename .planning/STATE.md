---
gsd_state_version: 1.0
milestone: v2.6
milestone_name: Exploration Depth and Backlog Evidence
current_phase: 27
current_phase_name: Evidence case — feature-origin-only leak
status: in-progress — S3-3 Wave 1 of 2 DONE (Phase 27 plan 27-01 executed + orchestrator-verified: DSX-ML-034 minted, catalogue 277, full suite 1596 OK); box UNCHECKED; resume at Wave 2 (27-02 fixture+harness)
stopped_at: "S3-3 Wave 1 of 2 DONE (box S3-3 stays UNCHECKED — checks only when both waves land + full suite re-run green). Plan 27-01 (mint DSX-ML-034) executed by gsd-executor (adaptive/sonnet, §3 routing); ALL GATES re-run by the orchestrator on the real 3.12.10 interpreter (C:/Users/Benutzer1/AppData/Local/Programs/Python/Python312/python.exe — NB python312 is NOT a command on this machine; python3 is the 3.14 stub). Verified: 4 atomic commits (336560d RED → 3d63c09 GREEN → df766dd catalogue → 4c2f84c SUMMARY) on canonical gsd/v2.6.0-exploration-depth, no stray branch (ancestry filter over baseline dd930af); only dsx/checks/ml.py under dsx/ (+98), dq.py byte-frozen (empty diff); NO REQUIREMENTS/STATE/ROADMAP edits by the executor. RED confirmed exit 1; GREEN 6/6; full suite 1596 OK (1590+6, two explain tests did NOT false-fail); gen-finding-catalogue.py --check EXIT 0 ('catalogue is current', D-05 gate green); catalogue Total 277, exactly one DSX-ML-034 row at CRITICAL (L163), byte-deterministic; D-05 honesty phrase present in ml.py docstring (Citation: Kaufman 2012 + 'secondary-corroborated ... paywalled ... not read first-hand' + Structural criterion:) AND the # D-05: DSX-ML-034 test marker — no first-hand PDF claim, no invented locator; early-return guard on model.get('feature_provenance'). DEVIATION (honestly disclosed, both legitimate lockstep moves not weakenings, both outside plan files_modified): the plan research §E under-counted the count/set pins — the executor also moved test_p19_categorical_rows.py::_EXPECTED_TOTAL 276→277 and added DSX-ML-034 to test_gen_finding_catalogue.py::_CANONICAL_DECLARATIONS (both severity tuples) + _MINTED_CODES; each verified as a required move, no property weakened. The DSX-ML-034 'declared twice' stderr warning is by-design (two report.add sites → generator dedupes to one CRITICAL row; non-failing) per RISK 3 / 27-RESEARCH. Not pushed by the executor; orchestrator pushes after verifying. Next = S3-3 Wave 2 (27-02 fixture promotion + harness maps + brief §6.5 rewrite + installer re-sync; depends_on 27-01 satisfied)."
last_updated: "2026-09-07T16:43:00.000Z"
last_activity: 2026-09-07
last_activity_desc: "Phase 27 S3-3 Wave 1 of 2 DONE (box UNCHECKED). Plan 27-01 executed + orchestrator-verified on real 3.12.10: DSX-ML-034 minted (CRITICAL after_prediction / HIGH unknown-no-waiver), catalogue 276→277 (all 4 count/set pins moved in lockstep), full suite 1596 OK, --check exit 0, dq.py frozen, D-05 marker honest. Next = S3-3 Wave 2 (27-02)."
progress:
  total_phases: 6
  completed_phases: 2
  total_plans: 10
  completed_plans: 9
  percent: 33
---

# Project state

**Status:** v2.6 Exploration Depth and Backlog Evidence — ACTIVE (opened 2026-09-06 by operator direction, HQ-39); branch `gsd/v2.6.0-exploration-depth`; ships as tag `v2.6.0`
**Progress:** [██████░░░░░░░░░░░░░░░] v2.6 — 2/6 phases (✅25 hermetic profile depth → ✅26 per-skill read contracts → 🔄27 feature-origin-only leak case (S3-3 Wave 1/2 done — 27-01 mint DSX-ML-034 executed + orchestrator-verified, suite 1596 OK, catalogue 277; box unchecked, resume Wave 2 = 27-02) → 28 magnitude-no-test case → 29 subgroup-harm case → 30 calibration re-baseline)
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

Phase: 27 — Evidence case, feature-origin-only leak (S3-3 Wave 1/2 done — 27-01 mint executed + verified; box UNCHECKED; resume Wave 2 = 27-02)
Plan: 27-01 EXECUTED + ORCHESTRATOR-VERIFIED (real 3.12.10). DSX-ML-034 minted in dsx/checks/ml.py (CRITICAL available_at=after_prediction / HIGH unknown-no-waiver; early-return when the block is absent; D-05 Kaufman docstring honest — secondary-corroborated, paywalled, not read first-hand). Catalogue regenerated 276→277 (one CRITICAL row, byte-deterministic); all 4 count/set pins moved in lockstep (_EXPECTED_TOTAL ×2, phase-20 assert, p19 pin) + DSX-ML-034 added to _MINTED_CODES / _CANONICAL_DECLARATIONS / _D05_ALLOWLIST_CODES. Full suite 1596 OK; gen-finding-catalogue.py --check exit 0; dq.py byte-frozen; no stray branch. 27-02 (fixture+harness / wave 2 depends_on 27-01) NOT yet executed.
Status: In-progress — NOT all-blocked. S3-3 Wave 1 verified; the box checks only when Wave 2 (27-02) also lands + the full suite re-runs green. Next = S3-3 Wave 2 (execute 27-02: promote spike/ → known-bad corpus fixture + POSTMORTEM + ATTRIBUTION sidecar; wire 4 harness maps; spec count 42→43; rewrite brief §6.5 item 7; node install.mjs + --check), then S3-4 review, S3-5 secure/validate.
Last activity: 2026-09-07 — Phase 27 S3-3 Wave 1/2 DONE (box UNCHECKED): 27-01 mint DSX-ML-034 executed by gsd-executor + orchestrator re-verified every gate on real 3.12.10 (suite 1596 OK, catalogue 277, --check exit 0, dq.py frozen, D-05 marker honest). Two under-counted count pins found + moved in lockstep (disclosed). Next = S3-3 Wave 2 (27-02).

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

**The milestone is NOT all-blocked; Phase 27's mint is now UNBLOCKED.** HQ-40 is
**ANSWERED** (all five D-05 rows read at their locators, 2026-09-07). Row 40b (Kaufman
2012 TKDD) CONFIRMED — secondary-corroborated, ACM primary PDF paywalled — with operator
direction "proceed with `DSX-ML-034`". Combined with the already-measured LIVE MISS
(`27-MEASUREMENT.md`), this closed S3-1 and clears the whole Phase 27 mint pipeline. Next
= **S3-2** (plan the mint: promote the `spike/` fixture into a committed corpus fixture,
add the ATTRIBUTION sidecar with `absent_code: DSX-ML-034` + `promotes_backlog_item:
6.5-item-7-…`, and the harness entries). **S3-3 must keep the `# D-05:` marker honest**
("secondary-corroborated, primary PDF paywalled" — no first-hand PDF claim). HQ-40 also
unblocked **S4-1** (Phase 28 — cite Wilkinson & TFSI 1999 alone, drop JARS 40d) and
**S5-1** (Phase 29 — Gail & Simon confirmed); those phases still need their own D-13
measurement spikes (each a §4 persona round first, as Phase 27 had).

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
