---
phase: 24
slug: portfolio-exemplar-viz-calibration
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-09-03
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
| _(pending — planner writes task IDs at S4-2; map filled at S4-5)_ | | | | | | ⬜ |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky.*

---

## Wave 0 Requirements (candidate — planner confirms in PLAN.md)

Test surfaces the plan is expected to create or extend (RED before GREEN where a new
assertion is added; the exemplar upgrade is verified through the **existing** gate, not a
new bespoke test):

- [ ] `tests/test_known_bad_corpus.py` — **extend** (not new): register each new
  bad-chart fixture in `_EXPECTED_CAUGHT_DEFECTS` (total-equality, `:1199`) and the
  HIGH ones in `_HIGH_TARGET_DEFECT_CODES` (`:505`); the `DSX-VIZ-071` MEDIUM fixture
  needs the new MEDIUM-stratum handling (`--block-on MEDIUM` threaded into `_gate_findings`,
  reported **beside** the headline, never folded in — 24-RESEARCH §Risks P1). REQ-P24-02.
- [ ] `examples/known-bad/<slug>-ANALYSIS-SPEC.yaml` + `<slug>-POSTMORTEM.md` ×4 —
  first bad-*chart*-choice fixtures (gauge / word_cloud / banned-control → `DSX-VIZ-001`
  HIGH; uncertainty-mark-misuse → `DSX-VIZ-071` MEDIUM). REQ-P24-02.
- [ ] Exemplar upgrade artifacts (REQ-P24-01) — verified by the **existing** viz/figures/
  repro checks passing on `examples/good-ANALYSIS-SPEC.yaml` at `dsx gate ship`, not a new
  test: third `visuals[]` uncertainty entry + re-sealed `svg_sha256` ×3 + matching manifest
  row + `good-REPRO-REPORT.md` + What/So What/Now What `good-NARRATIVE.md` +
  authored `examples/analysis/charts.py` (style-layer render).
- [ ] REQ-P24-03 verification surfaces — `tests/test_doc_code_agreement.py`,
  `tests/test_selection_heuristic_docs.py`, `tests/test_viz_vocabulary_invariant.py`
  (`len==11` / uncertainty-set / `BANNED_TYPES==7` pins), `tests/test_chart_catalog_invariant.py`
  (BANNED_TYPES equality) — **verify green, do not mutate**; close the one narrow
  chart-selection live-dict binding gap ONLY if the plan-checker rules it real
  (24-RESEARCH Q3). `scripts/gen-finding-catalogue.py --check` exit 0 @276.
- [ ] Framework install: **none** — stdlib `unittest` is the project convention.
- [ ] Off-gate-path discipline: the catch-rate/FPR re-baseline and any new corpus
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

> Checked at S4-5 (`/gsd-validate-phase 24`). Draft seed leaves these unchecked.

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags — all commands single-shot `unittest` / `dsx gate` / `--check`
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter (flipped at S4-5 after gap analysis)

**Approval:** _pending — set at S4-5 by the validate-phase orchestrator._
