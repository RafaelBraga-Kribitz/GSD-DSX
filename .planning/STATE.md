---
gsd_state_version: 1.0
milestone: v2.6
milestone_name: Exploration Depth and Backlog Evidence
current_phase: 28
current_phase_name: Evidence case — magnitude no test computed
status: in-progress — S4-3 Task 1 DONE (D-13 measurement; VERDICT LIVE MISS independently re-verified). S4-3 box UNCHECKED — mint (Tasks 2/3/4B) + Plan 28-02 fixture promotion remain. Spawned gsd-executor (adaptive, WRITE-ONLY, Task 1 only) → frozen D-28-01 collision spike + 28-MEASUREMENT.md (VERDICT: LIVE MISS first line). Orchestrator INDEPENDENTLY re-ran the four-point protocol on real 3.12.10 (repo=fact): reproduced the table byte-for-byte — DSX-CLM-033 SILENT at verify/ship (27/18 clear via ×100 bridge: test A effect 0.27, test B effect 0.18), HONEST swap no-toggle (nothing catches), BREAK swap DSX-CLM-033 fires (metric-blind, silence IS the miss); no stray DECISIONS.jsonl. §6.5 item 8 entry condition MET; DSX-CLM-034 mint authorized. LOUD FLAG for 28-02: DSX-COH-001 (CRITICAL, coherence.py) fires at plan/verify/ship — inherent to the frozen association-claim-under-descriptive-question shape, swap-INVARIANT → incidental per D-28-02 (NOT a catch), BUT the fixture is blocked at ship by it, so 28-02 _EXPECTED_CAUGHT_DEFECTS cannot be frozenset() (S4-1 note assumed empty): next firing reconciles the caught-incidental-plus-missed-target encoding before promotion (frozen design stands, guardrail 1). Spike+measurement committed (plain git, no stray branch; dsx/ byte-untouched, mints nothing). Stopped at Task-1 sub-boundary (executor ~14.75m, past the ~12-min cap). PRIOR: S4-2 DONE (Phase 28 plan-checker gate PASSED; both plans corrected + gated). gsd-plan-checker (haiku, adaptive) FAILED on ONE real BLOCKER — 28-01 Task 1 <done> (:195) routed a VERDICT:CAUGHT to "Task 4 branch B" (the LIVE-MISS handoff-to-28-02 path) instead of Branch A (the CAUGHT no-mint terminal), the WR-01-class misroute 28-RESEARCH.md:430 warned of (a literal executor on CAUGHT would skip the no-mint closure record AND wrongly proceed to fixture promotion). Orchestrator did NOT trust the verdict — confirmed the defect against the code (Task 4 Branch A=CAUGHT :321, Branch B=LIVE MISS :329; grep proved :195 the ONLY misrouted pointer), applied the single §5 repair (:195 "branch B"→"Branch A — the CAUGHT branch"; a mechanically-forced cross-ref fix, no design change), re-checked → VERIFICATION PASSED (12 invariants). Orchestrator re-verified the gate itself (repo=fact): REQ IDs in frontmatter (28-01 P28-01/02, 28-02 P28-01/03); NO dq.py/REQUIREMENTS/STATE/ROADMAP in either files_modified; deps 28-01 wave1[] / 28-02 wave2[28-01]; threat_model + Artifacts x2; live baselines re-measured catalogue Total 277 + spec len(paths),43@test_dsx.py:583 (plans move 277→278/43→44 conditional on the live miss); D-05 Wilkinson-alone + exact-code _D05_ALLOWLIST_CODES; DSX-CLM-034 OUT of _SECTION_65_BACKLOG_CODES; frozen id 6.5-item-8-magnitude-without-computed-effect@test_known_bad_corpus.py:853; fixture declares no supported_by (MISS holds). Corrected 28-01 + ledger/STATE committed (plain git, no stray branch). Next = S4-3 (execute: D-13 measure live at all 4 gate points FIRST → 28-MEASUREMENT.md VERDICT; then only on LIVE MISS the DSX-CLM-034 mint (28-01 Tasks 2-4) + fixture promotion (28-02); a CAUGHT verdict is a valid no-mint terminal).
stopped_at: "S3-5 DONE (box checked) → Phase 27 complete (3/6 phases). Both verify:post gates re-run by the orchestrator on real Python 3.12.10 (NOT trusted from a subagent). secure-phase 27: State B (no prior SECURITY.md); register from 2/2 PLAN <threat_model> blocks = 12 threats (8 HIGH / 3 MEDIUM / 1 LOW-accept), ASVS L1, block_on=high → auditor short-circuit; each re-gated at its locator → SECURED, threats_open:0, 12/12 CLOSED — T-27-03 (HIGH) docstring+# D-05: marker state 'secondary-corroborated, primary PDF paywalled', no first-hand claim (grep 0); T-27-01 (HIGH) fixture declares no feature_provenance block (grep 0) + dsx validate PASS CRITICAL=0 (honest miss); T-27-04 catalogue --check current + exactly one DSX-ML-034 CRITICAL row (finding-codes.md:163); T-27-02a/02b count pins 277 / spec 43; T-27-06 DSX-ML-034 out of _SECTION_65_BACKLOG_CODES; T-27-07 sidecar id a frozen _SECTION_65_ITEM_IDS member (:852); T-27-08 exact allowlist code (:209); T-27-09 dq.py byte-frozen (empty diff dd930af..HEAD); T-27-10 golden test_causal_verb_golden 6 OK; T-27-11 install.mjs --check self-test passed; T-27-SC accept (entrypoint read as text, never executed). 27-SECURITY.md written status:verified (technical; Approval unsigned per §4.4). validate-phase 27: State A; 3/3 REQ (P27-01/02/03) COVERED by named unittest tests, 0 MISSING → nyquist_compliant:true; phase module (test_ml_feature_provenance + test_known_bad_corpus) re-run 60 tests OK; full suite 1599 OK; 27-VALIDATION.md status:validated, per-task map green, sign-off filled. Human sign-off + UAT batched as HQ-43 (non-blocking until S7-2). Zero code/gate touched this unit (only .planning artifacts). [SUPERSEDED — see `status` + `last_activity_desc`: S4-1 discuss done; S4-2 full 2-plan set authored + committed but UNGATED as of 22:39Z 2026-09-07; next = S4-2 plan-checker gate + orchestrator re-verify.]"
last_updated: "2026-09-07T23:31:00.000Z"
last_activity: 2026-09-07
last_activity_desc: "S4-3 Task 1 firing (23:31Z): the D-13 measure-first act. gsd-executor (adaptive, WRITE-ONLY, 28-01 Task 1 only) built the frozen D-28-01 collision spike + 28-MEASUREMENT.md (VERDICT: LIVE MISS first line). Orchestrator did NOT trust it — read the spike (matches frozen shape, ×100 collision 0.27→27/0.18→18), read MEASURE.py (drives the REAL dsx gate on fresh tempdirs, seeds entrypoint + plan header like _gate_findings), and RE-RAN it on real 3.12.10 → reproduced the four-point table byte-for-byte: validate=0, plan/verify/ship=1 CRITICAL DSX-COH-001 only, execute=0; DSX-CLM-033 SILENT at verify/ship; HONEST swap (27→15,18→9) no-toggle (nothing catches); BREAK swap (27→33,18→44) DSX-CLM-033 fires (metric-blind ⇒ collision-silence is the miss); no stray DECISIONS.jsonl. LIVE MISS confirmed ⇒ §6.5 item 8 entry condition MET, DSX-CLM-034 mint authorized. FLAG: DSX-COH-001 fires (association claim under descriptive question, inherent to the frozen shape, swap-invariant → incidental per D-28-02) but blocks the fixture at ship, so 28-02 _EXPECTED_CAUGHT_DEFECTS cannot be frozenset() — reconcile before promotion. Committed spike+measurement (plain git, no stray branch), pushed. S4-3 box UNCHECKED (Tasks 2/3/4B + Plan 28-02 remain). Next = S4-3 continue (LIVE MISS branch mint + promotion). PRIOR — S4-2 GATE firing (23:04Z): ran gsd-plan-checker (haiku, adaptive) on the committed 28-01/28-02 → VERIFICATION FAILED on ONE real BLOCKER (28-01 Task 1 :195 mislabeled the CAUGHT route as 'Task 4 branch B' = the LIVE-MISS handoff, instead of Branch A the CAUGHT no-mint terminal; WR-01-class misroute per 28-RESEARCH.md:430). Did NOT trust the verdict — confirmed the defect real against the code (Task 4 Branch A=CAUGHT :321, Branch B=LIVE MISS :329; grep proved :195 the ONLY misrouted pointer), applied the single §5 repair (:195 'branch B'→'Branch A — the CAUGHT branch'), re-checked (same agent context) → VERIFICATION PASSED (12 invariants). Orchestrator re-verified the gate itself: REQ IDs in frontmatter, NO dq.py/tracking in either files_modified, deps wave1[]/wave2[28-01], threat_model+Artifacts x2, live baselines catalogue 277 + spec 43, D-05 Wilkinson-alone + exact-code allowlist, DSX-CLM-034 out of _SECTION_65_BACKLOG_CODES, frozen id verified @test_known_bad_corpus.py:853, MISS holds (no supported_by). Committed corrected 28-01 + ledger/STATE (plain git, no stray branch), pushed. Ledger ~35 entries — trim-to-archive light unit still pending (flagged 5x). Next = S4-3 execute (D-13 measure-first)."
progress:
  total_phases: 6
  completed_phases: 3
  total_plans: 12
  completed_plans: 10
  percent: 50
---

# Project state

**Status:** v2.6 Exploration Depth and Backlog Evidence — ACTIVE (opened 2026-09-06 by operator direction, HQ-39); branch `gsd/v2.6.0-exploration-depth`; ships as tag `v2.6.0`
**Progress:** [██████████░░░░░░░░░░░] v2.6 — 3/6 phases (✅25 hermetic profile depth → ✅26 per-skill read contracts → ✅27 feature-origin-only leak case (COMPLETE — DSX-ML-034 minted, corpus MISS fixture, secure 12/12 CLOSED, validate nyquist_compliant:true, suite 1599 OK) → 🔄28 magnitude-no-test case (S4-1 discuss + S4-2 plan gate PASSED + S4-3 Task 1 D-13 measurement = VERDICT LIVE MISS, re-verified; next = S4-3 continue: DSX-CLM-034 mint + Plan 28-02 promotion, reconciling the DSX-COH-001 incidental) → 29 subgroup-harm case → 30 calibration re-baseline)
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

Phase: 28 — Evidence case, magnitude no test computed (S4-1 discuss + S4-2 plan gate PASSED + S4-3 Task 1 D-13 measurement DONE = VERDICT LIVE MISS, independently re-verified; next = S4-3 continue — the conditional DSX-CLM-034 mint + Plan 28-02 fixture promotion)
Plan: 28-01 (tdd, wave1 — D-13 measure-live + conditional DSX-CLM-034 mint) + 28-02 (execute, wave2 — promote fixture + wire harness, LIVE-MISS branch only), both committed + plan-checker-gated (S4-2 DONE). Design frozen in 28-CONTEXT.md: collision/mislabel case shape (the claim's 27/18 are the REAL reported numbers of OTHER metrics so existing DSX-CLM-033 clears on full union-membership logic while no test computed the claimed metric), fixture declares NO claims[].supported_by → stays a MISS (DSX-CLM-034 declaration-gated, silent → attribution not detection, Phase-27 precedent). Reserved DSX-CLM-034 (03x next-free-in-family; live catalogue 277, CLM-034 grep=0 free). Vocabulary (plan input): claims[].supported_by (metric-name string, opt-in) + claims[].rounding (int sig-figs, default 2, ×100 scale bridge). Wilkinson & TFSI 1999 = motivating principle only (docstring enforces the traceability corollary, not "report an effect size"). Harness names for S4-2: spec count 43→44, catalogue 277→278, sidecar promotes_backlog_item=6.5-item-8-magnitude-without-computed-effect (frozen id verified test_known_bad_corpus.py:853) — all conditional on a live miss.
Status: In-progress — NOT all-blocked. S4-1 (discuss) + S4-2 (plan) DONE; S4-3 Task 1 (the D-13 measure-first act) DONE = **VERDICT LIVE MISS**, independently re-verified by the orchestrator against the real gate (four-point table reproduced byte-for-byte on 3.12.10; DSX-CLM-033 silent-on-collision / fires-on-break ⇒ metric-blind ⇒ its silence is the miss; HONEST swap catches nothing). §6.5 item 8 entry condition MET; the conditional DSX-CLM-034 mint is authorized. S4-3 box UNCHECKED (only Task 1 landed). **Open flag for Plan 28-02:** DSX-COH-001 (CRITICAL, coherence.py) fires at plan/verify/ship — inherent to the frozen association-claim-under-descriptive-question shape, swap-INVARIANT → an incidental per D-28-02 (not a catch of the target defect), but it blocks the fixture at ship, so 28-02's _EXPECTED_CAUGHT_DEFECTS cannot be frozenset() (the S4-1 plan-input note assumed empty, Phase-27 pure-miss style); the next firing reconciles the caught-incidental-plus-missed-target encoding before promotion (the frozen design stands — guardrail 1). D-05 for Phase 28 already resolved (HQ-40 40c/40d — Wilkinson alone). Next = S4-3 continue (LIVE MISS branch): Task 2 RED + Task 3 GREEN mint (DSX-CLM-034 + Wilkinson D-05 docstring + catalogue 277→278 + two count pins) + Task 4 Branch B → Plan 28-02 fixture promotion.
Last activity: 2026-09-07 (23:31Z) — Phase 28 S4-3 Task 1 (D-13 measurement). gsd-executor (adaptive, WRITE-ONLY, Task 1 only) built the frozen D-28-01 collision spike + 28-MEASUREMENT.md (VERDICT: LIVE MISS). Orchestrator did NOT trust it — read the spike (frozen shape, ×100 collision), read MEASURE.py (real dsx gate, fresh tempdirs, _gate_findings-style seeding), and re-ran it on real 3.12.10 → table reproduced byte-for-byte (validate=0; plan/verify/ship=1 CRITICAL DSX-COH-001 only; execute=0; DSX-CLM-033 silent at verify/ship; HONEST swap no-toggle; BREAK swap DSX-CLM-033 fires). LIVE MISS confirmed; DSX-COH-001-incidental flagged for 28-02. Committed spike+measurement (plain git, no stray branch; dsx/ byte-untouched), pushed. Next = S4-3 continue (mint + promotion).

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
