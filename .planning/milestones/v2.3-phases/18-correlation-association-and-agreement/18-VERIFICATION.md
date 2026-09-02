---
phase: 18
unit: S2-4
verdict: PASSED
requirements_verified: [REQ-P18-01, REQ-P18-02, REQ-P18-03, REQ-P18-04, REQ-P18-05, REQ-P18-06]
gate_rerun_by_orchestrator: true
full_suite: "Ran 1367 tests OK"
catalogue_total: 265
---

# 18-VERIFICATION — Phase 18 goal-backward verification

**Verifier:** autonomous ceremony orchestrator (opus / high, brief §3 verification routing).
**Date:** 2026-09-02. **Unit:** S2-4 (verification `passed`).
**Method:** goal-backward against REQ-P18-01..06 — for each requirement, the delivered
artifact and the gate that proves it, re-run by the orchestrator (not trusted from a
subagent report). All commands run from a clean tree (stray `DECISIONS.jsonl` cleared per
the HUMAN-QUEUE standing note).

## Phase goal

Correlation / association / agreement rows keyed on the DECLARED `estimand_kind`; two new
declaration-only gates (correlation scale/kind match; agreement declaration completeness);
report-only effect-size convention bands that never block; the no-autoswitch invariant
extended to the new category. Five new HIGH codes (DSX-STA-050/051/060/061/062); catalogue
260→265 by set-identity.

## Requirement-by-requirement verdict

### REQ-P18-01 — Correlation decision-table rows (doc + `recommend_test`, lockstep) — ✅ PASS
- `recommend_association` routes the three association kinds to their acceptable
  coefficients: `linear_association → {pearson_correlation, point_biserial}` (fisher_z CI),
  `monotone_association → {spearman_correlation, kendall_tau_b}`, `nominal_association →
  {phi, cramers_v}` (`dsx/checks/stats.py` `_ASSOCIATION_ROUTES`). Distance/partial
  correlation ship catalog/pointer-only (`mathx.CONVENTION_CATALOG`
  `distance_correlation`/`partial_correlation`, no numeric band — D-13 conditions unmet).
- Doc mirror present in `references/test-selection.md` (`AssociationDocMirrorTest`).
- **Gate:** `test_declared_association_routing` routing + doc-mirror tests green.

### REQ-P18-02 — Agreement / reliability rows — ✅ PASS
- Kappa family, ICC (model,type,definition) triple vocabulary (`spec.py` `ICC_MODELS`/
  `ICC_TYPES`/`ICC_DEFINITIONS`), Krippendorff α pinned level-keyed
  (`mathx.KRIPPENDORFF_REFERENCE` 0.7598@ordinal), Bland-Altman for `method_comparison`,
  Cronbach→omega pointer row (`CONVENTION_CATALOG.cronbach_to_omega`).
- **Gate:** `test_effect_size_kind` (Krippendorff pin + catalog-only presence) + doc mirror
  green.

### REQ-P18-03 — Gate: correlation scale/kind match — ✅ PASS
- **DSX-STA-050** (HIGH) fires for `pearson_correlation` against a declared-`ordinal`
  operand; point-biserial and declared-`dichotomous` operands whitelisted (D-03).
- **DSX-STA-051** (HIGH) fires for any `CORRELATION_FAMILY` coefficient declared for an
  `agreement`/`method_comparison` estimand (routes to kappa/ICC/Bland-Altman).
- Declaration-only (no data read); citation rests on the internal Phase-17 estimand/scale
  definitions with no fabricated locator (D-07 not-in-hand disposition).
- **Gate:** `test_correlation_scale_kind_gate` 8/8 (incl. Pitfall-1 no-false-041).

### REQ-P18-04 — Gate: agreement declaration completeness — ✅ PASS
- **DSX-STA-060** (HIGH): ICC without a complete, in-vocabulary (model,type,definition)
  triple — presence + membership only; combination-coherence deferred as candidate
  DSX-STA-063 (D-05).
- **DSX-STA-061** (HIGH): weighted kappa without recognised weights — `isinstance` branch
  before normalize; an explicit matrix is accepted, a string is checked against
  {linear, quadratic} (Pitfall 5).
- **DSX-STA-062** (HIGH): kappa family missing either **p_pos** OR **p_neg** — both
  required, the HQ-16-corrected Feinstein-Cicchetti Part II reading (D-04), not the stale
  "raw agreement + prevalence" paraphrase.
- **Gate:** `test_agreement_completeness_gate` 13/13.

### REQ-P18-05 — Effect-size convention bands, never blocking — ✅ PASS
- Bands live in `dsx/mathx.py` report-only tables: Landis-Koch `KAPPA_BANDS` (pinned,
  convention-labelled, edge-tie a labeled choice), Krippendorff 0.7598@ordinal pin;
  ICC (Koo-Li)/Kendall's W/dCor/partial/Cronbach→omega catalog-only with no numeric
  boundary and no fabricated locator.
- **Firewall:** `EFFECT_SIZE_KINDS` stays exactly `{d, h, r}` and is disjoint from
  `REPORT_ONLY_EFFECT_KINDS`; `interpret_effect` still raises for a convention kind — so a
  convention can never be adjudicated as a blocking band (D-06).
- Wired only into the ungated `templates/APA-TABLE-research.md`, which mints no finding code
  (`test_template_mints_no_finding_code`).
- **Gate:** `test_effect_size_kind` firewall + pin + catalog-only + template tests green.

### REQ-P18-06 — No-autoswitch invariant extends to this category — ✅ PASS
- `recommend_association`'s signature is exactly `["estimand_kind"]` — dataless, no `data`/
  `n`/distribution parameter — a *stronger* per-function anti-two-stage proof than the
  grep-style precedent (`test_signature_is_exactly_estimand_kind_dataless`).
- The existing decision-surface grep (`test_no_shapiro_autoswitch`
  `test_no_normality_test_call_on_the_decision_surface`, scanning all of `dsx/`) covers the
  new stats.py code for the absence of any normality/data-inspection call.
- **Gate:** both tests green.

## Gate re-run by the orchestrator (clean tree)

- Full suite: `python -m unittest discover -s tests -q` → **Ran 1367 tests … OK**.
- Catalogue: `python scripts/gen-finding-catalogue.py --check` → **exit 0**, "finding
  catalogue is current", **Total: 265** (set-identity 260 + 5; DSX-STA-050/051/060/061/062
  each present exactly once).
- Cross-plan seam oracle `test_report_only_kappa_fires_neither_011_nor_012_and_reports_ok`
  **RUNS** (not skipped) and passes — 18-A↔18-B seam live.

**Verdict: PASSED — all six REQ-P18-01..06 delivered and gate-proven from a clean tree.**
Phase 18 code review (S2-4) complete; next unit S2-5 (`/gsd-secure-phase 18` +
`/gsd-validate-phase 18`).
