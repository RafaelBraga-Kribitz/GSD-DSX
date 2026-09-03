---
phase: 22
unit: S2-4
verdict: PASSED
requirements_verified: [REQ-P22-01, REQ-P22-02, REQ-P22-03, REQ-P22-04, REQ-P22-05]
gate_rerun_by_orchestrator: true
full_suite: "Ran 1495 tests OK (40.5s)"
catalogue_total: 276
minted_codes: [DSX-VIZ-071]
minted_not: [DSX-VIZ-072]
set_identity_baseline: dc34a75^
set_identity_expected: "Phase-12 snapshot (256) ∪ _MINTED_CODES (incl. DSX-VIZ-071) = 276"
review_findings_fixed: []
perceptual_criterion_test: "tests.test_chart_catalog_invariant.test_perceptual_tie_break_structural_criterion GREEN"
---

# 22-VERIFICATION — Phase 22 goal-backward verification

**Verifier:** autonomous ceremony orchestrator (opus / high, brief §3 verification routing).
**Date:** 2026-09-03. **Unit:** S2-4 (verification `passed`).
**Method:** goal-backward against REQ-P22-01..05 — for each requirement, the delivered artifact
and the gate that proves it, **re-run by the orchestrator on the final tree** (`217cf68`), not
trusted from the S2-3 inline reports. All commands run from a clean tree (stray root/nested
`DECISIONS.jsonl` cleared before the suite per the standing note). The requirement text is read
**as amended by the four HQ-27 binding decisions D-1…D-4** — where the original REQ named chart
types that the independent primary-source pass proved do not exist (REQ-P22-02's "fan chart" /
"gradient CI band"; REQ-P22-05's implied strict `length > angle` order), the signed decision is
the contract, not the erroneous literal. Prefer the smaller provable claim (brief §5).

## Phase goal

Ship the catalog spine (a merged three-axis chart catalog conformant with the live vocabulary),
the **uncertainty** function family as an 11th relationship key, faceting as an orthogonal
declaration, and the 5-layer question→chart heuristic as route-and-cite edits — extending the
gate by exactly one D-05-cited code (DSX-VIZ-071), additively.

## Requirement-by-requirement verdict

### REQ-P22-01 — merged three-axis chart catalog (band 75–90), per-entry citation → **PASS**

- **Delivered:** `references/chart-catalog.md` — 81 rows (60 `dsx_admissible` **generated** from
  the live `_mark_universe()` so conformance is by construction, 14 `reference_only`, 7 `refusal`),
  each with function + data_signature + perceptual_channel + citation, plus a fenced-json payload
  carrying `rows` and `perceptual_ranks`.
- **Gate re-run:** `tests.test_chart_catalog_invariant` **8 OK** — row count in band (81 ∈ 75–90);
  every row has three axes + a non-empty citation; the dsx_admissible rows **set-equal**
  `_mark_universe()` in both directions (loaded by path — single source of truth, not a copy);
  reference-only rows sit **outside** the universe (cannot widen the gate); non-vacuity anchors
  (≥60 rows; bar/line/scatter/error_bars present). Per-entry citation **authenticity** is the D-05
  human read (HQ-27, signed with corrections) — this requirement delivers the conformant,
  three-axis, cited structure, which is met. D-3 honored: FT nine-category axis attributed, own
  descriptions, no vendored blurbs; forbidden-source guard (`test_no_citation_draws_on_a_forbidden_source`)
  green (Abela / Graph-Selection-Matrix / Mackinlay / Few-2013 / Information-Graphics / cardinality
  all absent).

### REQ-P22-02 — uncertainty family enters the vocabulary (11th key), D-12a-clean → **PASS**

- **Delivered (as amended by D-2):** `RELATIONSHIP_CHARTS` gains an 11th key `"uncertainty"` = the
  ten Wilke §5.6 marks (`error_bars`, `graded_error_bars`, `error_bars_2d`, `confidence_strips`,
  `eye`, `half_eye`, `quantile_dot_plot`, `confidence_band`, `graded_confidence_band`,
  `fitted_draws`) — NOT the original REQ's "fan chart / gradient CI band", which D-2 proved are not
  Wilke's terms. The set is D-12a-clean by construction (spans frequentist + Bayesian marks
  symmetrically, Wilke §16.2). Rippled: `viz.py` (key + `_check_uncertainty_vocabulary`),
  `spec.py` (`CHART_CAPABILITIES["interval-range"]`, GA-2 no new input-type id),
  `skills/dsx-visualize/SKILL.md` (step 1 10→11, step 6 routes to the ten members),
  `references/chart-selection.md` (uncertainty relationship row), `dsx/data/input_types.json`
  (regenerated). The property check DSX-VIZ-070 is retained as a complementary surface.
- **Gate re-run:** `tests.test_viz_vocabulary_invariant` **16 OK** (incl.
  `test_uncertainty_is_the_eleventh_relationship_key`); `tests.test_selection_heuristic_docs`
  `test_skill_enumerates_eleven_relationships` GREEN. Phase-21 every-mark-has-a-home invariant
  stays green (the ten marks are capability-homed).

### REQ-P22-03 — faceting as an orthogonal `facet_by` declaration; smells route to it → **PASS**

- **Delivered:** the plan-checked design (S2-2) — `facet_by` ships as a declaration, **not** a new
  chart type or spec field: it appears in no `RELATIONSHIP_CHARTS`/`CHART_CAPABILITIES` value and no
  `BANNED_TYPES` key, and the DSX-SMELL-007 (`_check_atoms_under_density`) remedy string routes to
  it ("split the data into small multiples with a `facet_by` declaration … orthogonal to the mark").
- **Gate re-run:** `test_facet_by_is_orthogonal_not_a_chart_type` (facet_by leaks into no
  chart-type map) + `test_density_smell_remedy_routes_to_facet_by` (remedy string names facet_by)
  GREEN inside the 16-test invariant module. No new code (routing reuses the existing
  DSX-SMELL-007).

### REQ-P22-04 — 5-layer heuristic as route-and-cite edits, no parallel decision tree → **PASS**

- **Delivered:** L1 question→task pointer in `references/question-taxonomy.md` citing Munzner ch.3
  and routing onward to `chart-selection.md`; L2–L5 (relationship→mark→encoding→uncertainty) threaded
  into `references/chart-selection.md`, pointing at `chart-catalog.md` and gate codes
  DSX-VIZ-012/013/070/071 (all verified live in `viz.py` before citing). No standalone
  decision-tree document created.
- **Gate re-run:** `tests.test_selection_heuristic_docs` **6 OK** — both surfaces point at
  `chart-catalog.md`; L1 cites Munzner and routes onward; the no-parallel-decision-tree name-pattern
  guard finds no offending file under `references/`; no forbidden heuristic citations (Abela /
  Few's Graph Selection Matrix, per Research OQ-1 option (a)).

### REQ-P22-05 — gate extended with a D-05-cited code; perceptual tie-break asserted as a named structural criterion → **PASS**

- **Delivered:** `_check_uncertainty_vocabulary` mints **DSX-VIZ-071** (MEDIUM) with a `Citation:`
  docstring line (Wilke §5.6 + §16.2) and a `Structural criterion:` line, allowlisted by exact code
  in `_D05_ALLOWLIST_CODES`; `finding-codes.md` regenerated (Total 276, DSX-VIZ-071 row). The
  perceptual tie-break (D-1) is encoded in `chart-catalog.md`'s `perceptual_ranks` as a
  six-rank-with-ties map and asserted as a **pure ordering criterion, no computation**.
- **Gate re-run:**
  - `tests.test_uncertainty_vocabulary` **3 OK** — non-member fires DSX-VIZ-071, member does not,
    absent field is silent.
  - `tests.test_chart_catalog_invariant.test_perceptual_tie_break_structural_criterion` **GREEN** —
    `density` absent from the ranks; `length == angle` asserted **both ways** (never a strict `<`);
    the monotone chain `position_common ≤ position_nonaligned ≤ length ≤ area ≤ volume ≤ shading`
    uses `≤` throughout (ties legal); every catalog row's channel is a defined rank. This is D-1's
    corrected form — the unsupported `length > angle` link is not asserted.
  - `python scripts/gen-finding-catalogue.py --check` → **"finding catalogue is current"** (exit 0)
    @ **Total: 276 codes** — D-05 enforcement for DSX-VIZ-071 passes.
  - **Set-identity (additive-mint proof):** `tests.test_finding_catalogue_invariant` proves the live
    code set == `Phase-12 snapshot (256) ∪ _MINTED_CODES` with `_MINTED_CODES` now including
    DSX-VIZ-071 → 276, symmetric difference over the prior 275 baseline = `added={DSX-VIZ-071},
    removed={}` (additive-only). `DSX-VIZ-072` deliberately not minted (HQ-30 / GA-3).

## Orchestrator gate evidence (clean tree, final state `217cf68`, this unit)

- `python -m unittest tests.test_chart_catalog_invariant` → **Ran 8 tests OK** (incl. the
  perceptual structural-criterion).
- `python -m unittest tests.test_uncertainty_vocabulary` → **Ran 3 tests OK** (DSX-VIZ-071 gate).
- `python -m unittest tests.test_selection_heuristic_docs` → **Ran 6 tests OK** (REQ-P22-04).
- `python -m unittest tests.test_viz_vocabulary_invariant` → **Ran 16 tests OK** (11th key + facet
  orthogonality + smell routing).
- `python -m unittest tests.test_finding_catalogue_invariant tests.test_p19_categorical_rows
  tests.test_phase20_zero_mint_close` → **Ran 13 tests OK** (count + set-identity + lockstep pins).
- `python scripts/gen-finding-catalogue.py --check` → "finding catalogue is current" (exit 0),
  **Total: 276 codes** (8 pre-existing `declared twice` warnings for CLM/COH/PAR/SPEC/VAL codes
  Phase 22 never touched — non-fatal, see 22-REVIEW OBS-2).
- `python -m unittest discover -s tests` → **Ran 1495 tests OK** (40.5s; clean tree — the two
  `explain` tests pass, no stray root `DECISIONS.jsonl`).

## Human Verification Required

Per-entry citation **authenticity** in `chart-catalog.md` and the DSX-VIZ-071 / refusal-row
citations are D-05 human reads — already tracked under **HQ-27** (signed 2026-09-03 with
corrections D-1…D-4, eight items explicitly left unverified). No new UAT steps: Phase 22 has no
user-facing runtime behaviour beyond the automated gates above; its acceptance test **is** the
suite. End-of-phase security sign-off is filed at S2-5.

## Verdict

**PASSED** — all five requirements delivered with orchestrator-re-run oracles; the uncertainty
family is a narrowing membership gate on a new optional field, faceting is a proven-orthogonal
declaration, the catalog conforms to the live vocabulary by construction, the heuristic is
route-and-cite with no second surface, and the single mint (DSX-VIZ-071) is additive by
set-identity (275→276). Zero review fixes needed. Ready for S2-5 (`/gsd-secure-phase 22` +
`/gsd-validate-phase 22`).
