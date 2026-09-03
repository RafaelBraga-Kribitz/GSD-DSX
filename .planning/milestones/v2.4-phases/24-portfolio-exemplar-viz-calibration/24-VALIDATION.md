---
phase: 24
slug: portfolio-exemplar-viz-calibration
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-09-03
validated: 2026-09-03
---

# Phase 24 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Seed authored by plan-phase (S4-2) from `24-RESEARCH.md` (enforcement surfaces,
> corpus harness extension points, doc/code-agreement direction analysis).
> The Per-Task map is filled by the planner (task IDs do not exist until PLAN.md is
> written); the gap analysis + `nyquist_compliant` flip happen at validate-phase (S4-5).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib `unittest` (every module in `tests/` uses `unittest.TestCase`) |
| **Config file** | none — tests run via `python -m unittest`; no `pytest.ini`/`unittest.cfg` |
| **Quick run command** | `python -m unittest tests.test_<module> -v` (the specific module a task touches) |
| **Full suite command** | `python -m unittest discover -s tests` |
| **Estimated runtime** | ~41 seconds (Phase 23 close measured 41.4s / 1507 tests) |

---

## Sampling Rate

- **After every task commit:** Run the specific test module(s) that task touches
  (`python -m unittest tests.test_known_bad_corpus -v`, etc.).
- **After every plan wave:** Run `python -m unittest discover -s tests` **plus**
  `python scripts/gen-finding-catalogue.py --check` (catches any accidental mint —
  D-06 requires set-identity 276→276).
- **Exemplar-specific (REQ-P24-01):** after re-rendering figures, `dsx seal` each SVG
  then `dsx gate ship --spec examples/good-ANALYSIS-SPEC.yaml` must exit 0 (proves the
  re-styled, re-sealed, uncertainty-figured exemplar still passes every gate at every
  threshold — the capstone's own acceptance test). `DSX-FIG-010` CRITICAL guards a
  stale seal; `DSX-REP-060/061` HIGH guard the REPRO-REPORT lead number.
- **Before `/gsd-verify-work`:** Full suite green from a **clean tree** (sweep any stray
  `DECISIONS.jsonl` first — standing note: two `explain` tests false-fail otherwise) and
  `gen-finding-catalogue.py --check` exit 0 @276.
- **Max feedback latency:** ~41 seconds (full suite).

---

## Per-Task Verification Map

> Filled at S4-5 (`/gsd-validate-phase 24`) against the finalized plan/wave task set.
> Every row's automated command is RE-RUN GREEN by the orchestrator at validate time
> (not trusted from execute reports). Any `⚠️ flaky` / `❌ red` row → spawn
> `gsd-nyquist-auditor` for that requirement.

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | Status |
|---------|------|------|-------------|-----------|-------------------|--------|
| Task 1 — charts.py render through style layer | 24-01 | 1 | REQ-P24-01 | auto | `python -m dsx gate ship --spec examples/good-ANALYSIS-SPEC.yaml` (exit 0, CRITICAL=0 HIGH=0) + `python -m unittest tests.test_gate_path_hermetic` | ✅ |
| Task 2 — 3rd uncertainty `visuals[]` + re-seal ×3 + manifest | 24-01 | 1 | REQ-P24-01 | auto | `python -m dsx gate ship …` — `DSX-FIG-010`/`DSX-FIG-011` (CRITICAL stale-seal) silent | ✅ |
| Task 3 — What/So What/Now What narrative + REPRO-REPORT | 24-01 | 1 | REQ-P24-01 | auto | `python -m dsx gate ship …` — `DSX-REP-06x` (HIGH lead-number) silent | ✅ |
| Task 1 — 3 banned-type HIGH fixtures + POSTMORTEMs | 24-02 | 1 | REQ-P24-02 | auto | `python -m unittest tests.test_known_bad_corpus` (banned → `DSX-VIZ-001` sole HIGH; incidental-gap guard) | ✅ |
| Task 2 — `DSX-VIZ-071` MEDIUM uncertainty-mark-misuse fixture | 24-02 | 1 | REQ-P24-02 | auto | `python -m unittest tests.test_known_bad_corpus` (MEDIUM under `--block-on MEDIUM`; not a `kind:miss`) | ✅ |
| Task 3 — MEDIUM stratum re-baseline beside the headline | 24-02 | 1 | REQ-P24-02 | auto | `python -m unittest tests.test_known_bad_corpus` (headline (miss-rate, FPR) byte-invariant) | ✅ |
| Task 1 — verify audit prereqs + set-identity 276→276 | 24-03 | 2 | REQ-P24-03 | auto | `python -m unittest tests.test_doc_code_agreement tests.test_selection_heuristic_docs tests.test_viz_vocabulary_invariant tests.test_chart_catalog_invariant` + `gen-finding-catalogue.py --check` exit 0 @276 | ✅ |
| Task 2 — close chart-selection live-dict binding gap | 24-03 | 2 | REQ-P24-03 | auto | `python -m unittest tests.test_selection_heuristic_docs` (both-directions `RELATIONSHIP_CHARTS` set-equality) | ✅ |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky. Every row re-run GREEN by the orchestrator on the clean final tree `ef13b27` at validate time (not trusted from execute reports): seven mitigation modules = 90 tests OK; full exemplar `plan→execute→verify→ship` all exit 0 (CRITICAL=0 HIGH=0, MEDIUM=3 = pre-existing `DSX-STA-011`); `gen-finding-catalogue.py --check` exit 0 @276; full suite 1508 OK / 45.5s.*

---

## Nyquist Gap Analysis (S4-5)

| Requirement | Coverage | Evidence | Verdict |
|-------------|----------|----------|---------|
| REQ-P24-01 — portfolio exemplar upgraded in place (style layer, one real-CI uncertainty figure, sealed manifest, What/So What/Now What narrative, REPRO-REPORT) | **COVERED** | The capstone is verified through the **existing** gate, not a new bespoke test: `dsx gate ship` exits 0 with CRITICAL=0 HIGH=0 (`DSX-FIG-010` re-seal guard + `DSX-REP-061` lead-number guard both silent), and `test_gate_path_hermetic` keeps matplotlib off the gate path. The full `plan→execute→verify→ship` sequence passes on a swept trail. | ✅ COVERED |
| REQ-P24-02 — first bad-chart-choice fixtures + catch-rate/FPR re-baseline | **COVERED** | `tests.test_known_bad_corpus` GREEN across all strata: 3 banned-type fixtures → `DSX-VIZ-001` sole HIGH; the `DSX-VIZ-071` MEDIUM fixture fires only under `--block-on MEDIUM`; the MEDIUM stratum is reported BESIDE the headline with a byte-invariance assertion on (miss-rate, FPR). Two Manual-Only rows (fixture authenticity, re-baseline honesty) are judgment reads confirmed at code review (S4-4), not uncovered automation. | ✅ COVERED |
| REQ-P24-03 — selection-surface doc/code agreement verified (verify-not-build) | **COVERED** | `test_doc_code_agreement` (test-selection.md) + `test_selection_heuristic_docs` (chart-selection.md, now with both-directions `RELATIONSHIP_CHARTS` binding) + `test_viz_vocabulary_invariant` + `test_chart_catalog_invariant` all GREEN with no pin mutated; catalogue current @276, set-identity 276→276. | ✅ COVERED |

**Result: 3/3 COVERED, 0 PARTIAL, 0 MISSING → `nyquist_compliant: true`.** No `gsd-nyquist-auditor` spawn required (no red/flaky/partial row).

---

## Wave 0 Requirements (candidate — planner confirms in PLAN.md)

Test surfaces the plan is expected to create or extend (RED before GREEN where a new
assertion is added; the exemplar upgrade is verified through the **existing** gate, not a
new bespoke test):

- [x] `tests/test_known_bad_corpus.py` — **extend** (not new): register each new
  bad-chart fixture in `_EXPECTED_CAUGHT_DEFECTS` (total-equality, `:1199`) and the
  HIGH ones in `_HIGH_TARGET_DEFECT_CODES` (`:505`); the `DSX-VIZ-071` MEDIUM fixture
  needs the new MEDIUM-stratum handling (`--block-on MEDIUM` threaded into `_gate_findings`,
  reported **beside** the headline, never folded in — 24-RESEARCH §Risks P1). REQ-P24-02.
- [x] `examples/known-bad/<slug>-ANALYSIS-SPEC.yaml` + `<slug>-POSTMORTEM.md` ×4 —
  first bad-*chart*-choice fixtures (gauge / word_cloud / banned-control → `DSX-VIZ-001`
  HIGH; uncertainty-mark-misuse → `DSX-VIZ-071` MEDIUM). REQ-P24-02.
- [x] Exemplar upgrade artifacts (REQ-P24-01) — verified by the **existing** viz/figures/
  repro checks passing on `examples/good-ANALYSIS-SPEC.yaml` at `dsx gate ship`, not a new
  test: third `visuals[]` uncertainty entry + re-sealed `svg_sha256` ×3 + matching manifest
  row + `good-REPRO-REPORT.md` + What/So What/Now What `good-NARRATIVE.md` +
  authored `examples/analysis/charts.py` (style-layer render).
- [x] REQ-P24-03 verification surfaces — `tests/test_doc_code_agreement.py`,
  `tests/test_selection_heuristic_docs.py`, `tests/test_viz_vocabulary_invariant.py`
  (`len==11` / uncertainty-set / `BANNED_TYPES==7` pins), `tests/test_chart_catalog_invariant.py`
  (BANNED_TYPES equality) — **verify green, do not mutate**; close the one narrow
  chart-selection live-dict binding gap ONLY if the plan-checker rules it real
  (24-RESEARCH Q3). `scripts/gen-finding-catalogue.py --check` exit 0 @276.
- [x] Framework install: **none** — stdlib `unittest` is the project convention.
- [x] Off-gate-path discipline: the catch-rate/FPR re-baseline and any new corpus
  predicate stay stdlib-only; matplotlib is only imported by the exemplar generator
  (`examples/analysis/charts.py`), never on the gate path (`test_gate_path_hermetic.FORBIDDEN`).

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Per-fixture chart-defect **authenticity** — that each bad-chart fixture is a genuinely-bad chart choice (not merely a schema trip), and each POSTMORTEM correctly names why the chart is wrong | REQ-P24-02 | Judgment about whether a chart choice is *substantively* bad (vs a mechanical gate trip) is a design read; the automated side proves only that the declared code fires. Non-D-05 (no external source) → recorded in the fixture POSTMORTEMs, confirmed at code review (S4-4), not escalated. | Read each `<slug>-POSTMORTEM.md`; confirm the stated chart-choice defect matches the tripped code and the fixture would mislead a real reader. |
| Catch-rate / FPR **re-baseline honesty** — the MEDIUM stratum is reported beside the headline and never folded into it; the headline (miss-rate over ABSENT, FPR) stays invariant to adding caught fixtures | REQ-P24-02 | The corpus discipline forbids inflating the headline by adding easy catches; verified by the D-06-invariance assertions (`:1746`, `:1806`) plus a read of the report structure. | Confirm `test_stratified_catch_rate_and_fpr_report` keeps HIGH/MEDIUM strata separate from the headline and the headline value is unchanged by the new fixtures. |

*The exemplar upgrade (REQ-P24-01) and the doc/code-agreement verification (REQ-P24-03)
are fully automated (existing gates + invariant pins above) — no manual-only rows.*

---

## Validation Sign-Off

> Checked at S4-5 (`/gsd-validate-phase 24`).

- [x] All tasks have `<automated>` verify or Wave 0 dependencies — all 8 tasks (type=auto) mapped above
- [x] Sampling continuity: no 3 consecutive tasks without automated verify — every task has a green module/gate
- [x] Wave 0 covers all MISSING references — none MISSING; all 3 requirements COVERED
- [x] No watch-mode flags — all commands single-shot `unittest` / `dsx gate` / `--check`
- [x] Feedback latency < 60s — full suite 45.5s; targeted modules ≤14s
- [x] `nyquist_compliant: true` set in frontmatter (flipped at S4-5 after gap analysis)

**Approval:** validated 2026-09-03 — `nyquist_compliant: true`, `wave_0_complete: true`, 3/3 requirements REQ-P24-01..03 COVERED (0 MISSING / 0 PARTIAL). Per-Task map re-run GREEN by the orchestrator on the clean final tree `ef13b27` (not trusted from the 24-01/24-02/24-03 execute reports): seven mitigation modules = 90 tests OK, the full exemplar `dsx gate plan→execute→verify→ship` sequence all exit 0 on a swept trail (CRITICAL=0 HIGH=0, MEDIUM=3 = pre-existing `DSX-STA-011`), `gen-finding-catalogue.py --check` exit 0 @276, full suite 1508 OK / 45.5s. Two Manual-Only rows (per-fixture chart-defect authenticity, catch-rate/FPR re-baseline honesty) are design/judgment reads discharged at code review S4-4 — non-D-05, not escalated. No `gsd-nyquist-auditor` spawn required.
