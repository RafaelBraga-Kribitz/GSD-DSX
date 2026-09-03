# 24-REVIEW — Phase 24 code review

**Reviewer:** autonomous ceremony orchestrator (opus / high, brief §3 code-review routing).
**Date:** 2026-09-03. **Unit:** S4-4 (code review + fixes).
**Verdict: PASS — zero code fixes.**

**Scope:** the five Phase-24 execute commits `d78c338` (24-01 exemplar upgrade) ·
`11e2df7` (`.gitattributes` seal-durability fix) · `d0fa3aa` (24-01 repro-path
regression fix) · `5de04e9` (24-02 bad-chart fixtures + MEDIUM stratum) · `29006fe`
(24-03 verify-not-build). Scope isolated with `git diff 08a65bf 29006fe -- . ':(exclude).planning'`
— 22 files, +1391 / −16. Every changed source hunk and every new test module was read
in full. `git diff dsx/` across the whole phase is **EMPTY** — no gate/library code was
touched (the calibration phase mints nothing and mutates no frozen surface, by design).

| File | Change | Verdict |
|---|---|---|
| `examples/analysis/charts.py` | new generator (+145; sole matplotlib importer, off gate path) | PASS |
| `examples/figures/*.svg` ×3 | re-rendered + sealed (bar, trend, **new** CI figure) | PASS |
| `.gitattributes` | +6 (`examples/figures/*.svg binary` — seal survives checkout) | PASS |
| `examples/good-ANALYSIS-SPEC.yaml` | +37 (3rd `visuals[]` uncertainty entry + refreshed seals) | PASS |
| `examples/good-FIGURE-MANIFEST.yaml` | +6 (uncertainty row + `matplotlib_version: 3.11.1`, additive) | PASS |
| `examples/good-NARRATIVE.md` | rewrite → strict What / So What / Now What | PASS |
| `examples/good-REPRO-REPORT.md` | new (machine block `activation_rate: 0.024`) | PASS |
| `examples/known-bad/chart-*-{ANALYSIS-SPEC.yaml,POSTMORTEM.md}` ×4 | new bad-chart fixtures | PASS |
| `tests/test_known_bad_corpus.py` | +118 (MEDIUM stratum + `block_on` thread) | PASS |
| `tests/test_selection_heuristic_docs.py` | +16 (both-directions live-dict drift guard) | PASS |
| `tests/test_dsx.py` `test_frame_val.py` `test_causal_verb_golden.py` | registry rows (measured) | PASS |

## Risk 1 — matplotlib reaching the hermetic gate path

The phase's defining risk: Phase 23 introduced matplotlib as an analyst-side dependency;
Phase 24 is the first code to actually *import and call* it (`examples/analysis/charts.py`).
**Closed by construction and structurally pinned.**

- `charts.py` lives in `examples/analysis/`, outside the `dsx/` AST closure the hermetic
  guard walks, and is imported by no `GATE_PROFILES` module. It imports the helper from
  `templates/` by path (`sys.path.insert`), not the gate.
- Confirmed by the guard itself: `tests.test_gate_path_hermetic` → **2 OK** with
  `matplotlib` in `FORBIDDEN` (the Phase-23 D-P23-03 structural guard). A regression that
  pulled a render dependency onto the gate path would fail here.
- `matplotlib.use("Agg")` is set before `pyplot` import — headless, no display backend.

## Risk 2 — exemplar number integrity (a portfolio artifact skeptics will check)

Every load-bearing number in the exemplar reconciles across five surfaces; **nothing is
invented in the renderer.**

- `charts.py` constants — `UPLIFT=0.024`, `CI_LOW=0.0101`, `CI_HIGH=0.0384`,
  `BASELINE_RATE=0.310`, `DECISION_FLOOR=0.010` — match `good-ANALYSIS-SPEC.yaml`
  `results.tests[0]` (`effect: 0.024`, `ci: [0.0101, 0.0384]`), `design.baseline_rate: 0.31`,
  and the `decision.decision_rule` (CI lower bound > +1.0pp) exactly.
- `good-REPRO-REPORT.md` machine block `activation_rate: 0.024` == `results.tests[0].effect`
  (inside DSX-REP-061's rel_tol).
- `good-NARRATIVE.md` states 2.4pp, 95% CI 1.0–3.8pp, and is **honest about magnitude**:
  "The effect is modest in standardized terms (h ≈ 0.05); the case for rollout rests on
  the interval clearing the pre-agreed practical floor, not on statistical significance."
  The CI lower bound (1.01pp) clears the +1.0pp floor — accurate, not overstated. The
  Now-What section names the generalisation limits (new signups only, two-week June window,
  no durable-LTV claim) rather than burying them.
- The uncertainty figure (`render_uplift_ci`) draws asymmetric error bars from the *actual*
  CI arms (`[UPLIFT-CI_LOW],[CI_HIGH-UPLIFT]`) and annotates the +1.0pp decision floor —
  it visualises the decision rule, not a decoration.

## Risk 3 — fixture authenticity (manual-only read, discharged here per 24-VALIDATION §Manual-Only)

Each bad-chart fixture must be a *substantively* bad chart choice (not a mere schema trip),
and each POSTMORTEM must name the code that actually fires. Read all four POSTMORTEMs +
specs. **Confirmed genuine.**

- `chart-gauge-single-kpi` → `DSX-VIZ-001` (gauge): POSTMORTEM correctly separates Few 2006
  §3.2/§6.2.1.1 (space-inefficient, context-free) from DSX's *own* "the maximum is arbitrary"
  reasoning — matching the `BANNED_TYPES["gauge"]` provenance discipline exactly.
- `chart-word-cloud-text` → `DSX-VIZ-001` (word_cloud); `chart-radar-multimetric` →
  `DSX-VIZ-001` (radar, pre-existing banned control).
- `chart-uncertainty-mark-misuse` → `DSX-VIZ-071` **MEDIUM**: the subtle one — declares
  `uncertainty_mark: gradient_band`, a plausible non-member, and the POSTMORTEM correctly
  names the HQ-27 D-2 trap (`confidence_band`/`graded_confidence_band` are real Wilke §5.6
  members; `gradient_band` is not). Genuinely a bad chart *choice*, not a typo dressed up.
- Each fixture is a copy of a proven-clean `good-corpus/*` control + exactly one bad
  `visuals[]` entry, so the only off-clean finding is the intended one (incidental
  `DSX-VIZ-010`/`-014` MEDIUM only, below the HIGH tier).

## Risk 4 — catch-rate/FPR headline honesty (no inflation by adding easy catches)

The corpus discipline forbids folding new catches into the headline miss-rate/FPR. **Held.**

- The new MEDIUM stratum (`_MEDIUM_TARGET_DEFECT_CODES` + `block_on="MEDIUM"` threaded
  through `_gate_findings`) is a *fourth* readout reported BESIDE the (miss-rate, FPR) pair,
  with an explicit byte-identity re-assertion that the pair is unchanged after the MEDIUM
  stratum runs (`test_stratified_catch_rate_and_fpr_report`, the two new invariance asserts).
- `block_on` defaults to `None`: every pre-Phase-24 `_gate_findings` call is byte-for-byte
  unchanged, so the CRITICAL/HIGH strata are provably untouched.
- The three banned fixtures join `_HIGH_TARGET_DEFECT_CODES` (read LIVE, D-09) — their
  catches are measured, not lifted from a stored ledger. Re-run: **47 OK**.

## Risk 5 — verify-not-build integrity (zero mint, snapshots unmutated)

REQ-P24-03's whole point: prove 24-01/24-02 added nothing to the vocabulary or code. **Held.**

- `gen-finding-catalogue.py --check` → **exit 0, catalogue current @276**; set-identity 276→276.
- Audit-prereq pins (`test_viz_vocabulary_invariant` len==11 / uncertainty-set / BANNED_TYPES==7;
  `test_chart_catalog_invariant` BANNED_TYPES equality) re-run green, **unmutated** — 32 OK
  with `test_doc_code_agreement`.
- 24-03's one edit (`test_selection_heuristic_docs.py`, +16) tightens a real, plan-checker-approved
  drift gap: the doc's relationship vocabulary now binds to the LIVE `RELATIONSHIP_CHARTS`
  **both directions**, not only transitively via the len==11 pin. 7 OK.

## Deviations reviewed (recorded loudly in the summaries, verified honest here)

- **24-02's three tree-wide registry rows** (`test_dsx.py` count 19→23, `test_frame_val.py`
  4×`set()`, `test_causal_verb_golden.py` 4 golden entries) go beyond the plan's named
  `files_modified`, but each is a registry that iterates *every* committed spec and *requires*
  a per-fixture entry. Each value was **measured** against the fixture as committed (comments
  record the method + date), not guessed. Correct and necessary — omitting them would red the
  suite. No threshold softened.
- **24-01's repro-path regression** (`good-REPRO-REPORT.md` path written repo-root-relative,
  not spec-dir-relative) was caught and fixed *within* the phase (commit `d0fa3aa`) after the
  author verified against the good-fixture-gating tests rather than trusting the single ship
  exit code. Honest record; the underlying phase_dir-vs-resolve_root asymmetry in `dsx/cli.py`/
  `repro.py` is a real latent inconsistency correctly ruled out of the exemplar-only scope
  (documented, not silently ignored) — see the follow-up note below.

## Verification-methodology finding (NOT a code defect — carry to S4-5 / S5)

The exemplar's ship acceptance is **trail-sensitive** and must be run correctly to reproduce
the 24-01 evidence — this is a re-run *procedure* note, not a defect in the shipped tree:

- `dsx gate ship --spec examples/good-ANALYSIS-SPEC.yaml` **alone** on an empty trail exits
  **2** ("no plan-time frame lock recorded — `dsx gate plan` has never run") — ship legitimately
  requires a recorded plan header to reconcile against.
- Run after the full test suite, `examples/DECISIONS.jsonl` carries a stray plan header with a
  *different* frame digest (test fixtures gate the same spec_id), so ship false-fails with
  CRITICAL `DSX-PRE-020` + HIGH `DSX-PRE-041`. This is the documented stray-`DECISIONS.jsonl`
  class of false failure (HUMAN-QUEUE standing notes), not a real defect.
- The correct acceptance is the full sequence on a clean, isolated trail:
  `dsx gate plan → execute → verify → ship`, all against a swept `examples/DECISIONS.jsonl`.
  Re-run this way: **plan/execute/verify/ship all exit 0**, ship = `CRITICAL=0 HIGH=0 MEDIUM=3
  LOW=0 INFO=1` — exactly the 24-01 claim. The 3 MEDIUM are the pre-existing `DSX-STA-011`
  negligible-effect-size findings in the untouched `results` block (non-blocking at HIGH).

**Recommendation for S5 milestone audit:** sweep every `DECISIONS.jsonl` and gate the exemplar
as a fresh plan→ship sequence; never trust a bare `dsx gate ship` run interleaved with the suite.

## Outcome

Zero code fixes. All five phase risks are closed by construction and confirmed by
orchestrator-re-run gates (evidence in `24-VERIFICATION.md`). The one substantive finding is
a verification-*procedure* note (trail hygiene for the exemplar ship gate), recorded above and
carried to S4-5/S5. **PASS.**
