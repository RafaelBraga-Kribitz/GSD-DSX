---
gsd_state_version: 1.0
milestone: v2.6
milestone_name: Exploration Depth and Backlog Evidence
current_phase: 27
current_phase_name: Evidence case — feature-origin-only leak
status: in-progress — S3-5 DONE (Phase 27 COMPLETE: secure SECURED threats_open:0 12/12 CLOSED + validate nyquist_compliant:true 3/3 REQ COVERED; 27-SECURITY.md + 27-VALIDATION.md written; sign-off batched HQ-43, non-blocking until S7-2); next = S4-1 (Phase 28 discuss, unblocked by HQ-40 — cite Wilkinson & TFSI 1999 alone)
stopped_at: "S3-5 DONE (box checked) → Phase 27 complete (3/6 phases). Both verify:post gates re-run by the orchestrator on real Python 3.12.10 (NOT trusted from a subagent). secure-phase 27: State B (no prior SECURITY.md); register from 2/2 PLAN <threat_model> blocks = 12 threats (8 HIGH / 3 MEDIUM / 1 LOW-accept), ASVS L1, block_on=high → auditor short-circuit; each re-gated at its locator → SECURED, threats_open:0, 12/12 CLOSED — T-27-03 (HIGH) docstring+# D-05: marker state 'secondary-corroborated, primary PDF paywalled', no first-hand claim (grep 0); T-27-01 (HIGH) fixture declares no feature_provenance block (grep 0) + dsx validate PASS CRITICAL=0 (honest miss); T-27-04 catalogue --check current + exactly one DSX-ML-034 CRITICAL row (finding-codes.md:163); T-27-02a/02b count pins 277 / spec 43; T-27-06 DSX-ML-034 out of _SECTION_65_BACKLOG_CODES; T-27-07 sidecar id a frozen _SECTION_65_ITEM_IDS member (:852); T-27-08 exact allowlist code (:209); T-27-09 dq.py byte-frozen (empty diff dd930af..HEAD); T-27-10 golden test_causal_verb_golden 6 OK; T-27-11 install.mjs --check self-test passed; T-27-SC accept (entrypoint read as text, never executed). 27-SECURITY.md written status:verified (technical; Approval unsigned per §4.4). validate-phase 27: State A; 3/3 REQ (P27-01/02/03) COVERED by named unittest tests, 0 MISSING → nyquist_compliant:true; phase module (test_ml_feature_provenance + test_known_bad_corpus) re-run 60 tests OK; full suite 1599 OK; 27-VALIDATION.md status:validated, per-task map green, sign-off filled. Human sign-off + UAT batched as HQ-43 (non-blocking until S7-2). Zero code/gate touched this unit (only .planning artifacts). Next = S4-1 (Phase 28 discuss) — unblocked by HQ-40 (cite Wilkinson & TFSI 1999 alone, drop JARS); S4-1 needs its own §4 persona round + D-13 measurement spike first, as S3-1 did for Phase 27."
last_updated: "2026-09-07T18:01:00.000Z"
last_activity: 2026-09-07
last_activity_desc: "Phase 27 S3-5 DONE → Phase 27 COMPLETE (3/6 phases). Both verify:post gates re-gated by the orchestrator on real 3.12.10: secure-phase → SECURED, threats_open:0, 12/12 CLOSED (27-SECURITY.md status:verified); validate-phase → nyquist_compliant:true, 3/3 REQ COVERED, phase module 60/60 + full suite 1599 OK (27-VALIDATION.md status:validated). Sign-off batched HQ-43 (non-blocking until S7-2). Next = S4-1 (Phase 28 discuss)."
progress:
  total_phases: 6
  completed_phases: 3
  total_plans: 10
  completed_plans: 10
  percent: 50
---

# Project state

**Status:** v2.6 Exploration Depth and Backlog Evidence — ACTIVE (opened 2026-09-06 by operator direction, HQ-39); branch `gsd/v2.6.0-exploration-depth`; ships as tag `v2.6.0`
**Progress:** [██████████░░░░░░░░░░░] v2.6 — 3/6 phases (✅25 hermetic profile depth → ✅26 per-skill read contracts → ✅27 feature-origin-only leak case (COMPLETE — DSX-ML-034 minted, corpus MISS fixture, secure 12/12 CLOSED, validate nyquist_compliant:true, suite 1599 OK) → 🔄28 magnitude-no-test case (next = S4-1 discuss) → 29 subgroup-harm case → 30 calibration re-baseline)
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

Phase: 27 — Evidence case, feature-origin-only leak (S3-4 DONE — code review + verification passed; next = S3-5 secure/validate)
Plan: 27-01 + 27-02 EXECUTED + ORCHESTRATOR-VERIFIED (real 3.12.10). Wave 1: DSX-ML-034 minted in dsx/checks/ml.py (CRITICAL available_at=after_prediction / HIGH unknown-no-waiver; early-return when the block is absent; D-05 Kaufman docstring honest — secondary-corroborated, paywalled, not read first-hand); catalogue 276→277. Wave 2: the measured LIVE MISS promoted into the committed corpus fixture examples/known-bad/feature-origin-only-leak-* (SPEC+entrypoint+POSTMORTEM+ATTRIBUTION), NO feature_provenance block (stays a MISS — DSX-ML-034 silent); 3 glob-discovered harness maps each gained one MISS entry (caught=frozenset(), val=set(), golden={CLM-031,COH-031,MET-040,NAR-001} — live-re-measured, DSX-ML-034 absent); spec count 42→43; DSX-ML-034 kept OUT of _SECTION_65_BACKLOG_CODES; brief §6.5 item 7 rewritten (LIVE MISS + DSX-ML-034). Full suite 1596 OK; gen-finding-catalogue.py --check exit 0 (Total 277); node install.mjs --check exit 0; dq.py byte-frozen; no stray branch.
Status: In-progress — NOT all-blocked. S3-4 checked (code review + verification passed, orchestrator re-ran gates green). Next = S3-5 (secure/validate; sign-off batched to HUMAN-QUEUE, non-blocking until S7-2), which completes Phase 27; then S4-1 (Phase 28 discuss — HQ-40 Wilkinson row ANSWERED, needs its own D-13 measurement spike + persona round).
Last activity: 2026-09-07 — Phase 27 S3-4 DONE. gsd-code-reviewer (opus) → 27-REVIEW.md 0B/0H/1M/2L, 6/6 invariants HOLD; WR-01 (unattested available_at silently cleared — one-token bypass) FIXED + 3 regression tests + _CANONICAL_DECLARATIONS pin updated, L-02 comment fixed, L-01 accepted; orchestrator re-ran gates on real 3.12.10 (suite 1599 OK, catalogue 277 with CRITICAL row preserved, dq.py frozen, install --check passed). 27-VERIFICATION.md passed (3/3 REQ MET). Next = S3-5 (secure/validate).

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
