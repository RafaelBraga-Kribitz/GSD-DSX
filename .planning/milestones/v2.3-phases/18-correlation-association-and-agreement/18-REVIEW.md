# 18-REVIEW — Phase 18 code review

**Reviewer:** autonomous ceremony orchestrator (opus / high, brief §3 code-review routing).
**Date:** 2026-09-02. **Unit:** S2-4 (code review + fixes).
**Scope:** the phase-18 source/test/template/doc diff `a266a9b..HEAD` (the Phase-17-close
commit to HEAD) — every line read in full (1003 insertions across 12 files).

## Files reviewed

| File | Change | Verdict |
|---|---|---|
| `dsx/checks/stats.py` | `recommend_association` (dataless) + `_check_declared_association` → `_check_correlation_scale_kind` (050/051) + `_check_agreement_completeness` (060/061/062); `CORRELATION_FAMILY` + `_ASSOCIATION_ROUTES`; `operand_scale` joined `_MEMBERSHIP_FIELDS`; DSX-STA-012 report-only seam | PASS (1 fix applied, LOW-1 below) |
| `dsx/mathx.py` | `REPORT_ONLY_EFFECT_KINDS`, `KAPPA_BANDS` (Landis-Koch), `KRIPPENDORFF_REFERENCE` (0.7598@ordinal), `CONVENTION_CATALOG`, `label_convention_band` — all report-only, disjoint from `EFFECT_SIZE_KINDS` | PASS |
| `dsx/spec.py` | `ICC_MODELS`/`ICC_TYPES`/`ICC_DEFINITIONS`/`KAPPA_WEIGHT_TOKENS`/`OPERAND_SCALES` + `_VOCABULARIES` registration | PASS |
| `references/test-selection.md` | association/agreement doc mirror (65 lines) | PASS |
| `references/finding-codes.md` | regen in-commit (5 new codes, D-08 lockstep) | PASS |
| `scripts/gen-finding-catalogue.py` | +13 lines (new-code emission) | PASS |
| `templates/APA-TABLE-research.md` | convention bands wired into the ungated template (mints no code) | PASS |
| `tests/test_declared_association_routing.py` | new (7 tests → 8 after fix) | PASS |
| `tests/test_correlation_scale_kind_gate.py` | new (8 tests) | PASS |
| `tests/test_agreement_completeness_gate.py` | new (13 tests) | PASS |
| `tests/test_effect_size_kind.py` | +186 (firewall + pins + catalog-only + seam oracle) | PASS |
| `tests/test_finding_catalogue_invariant.py` | count 260→265, snapshot/minted-codes | PASS |

## Findings

### LOW-1 — `CORRELATION_FAMILY` drift risk (FIXED)

`dsx/checks/stats.py` defines `CORRELATION_FAMILY` (the set DSX-STA-051 keys on) as a
standalone literal, and separately defines `_ASSOCIATION_ROUTES` whose three
acceptable-coefficient sets union to the *same* six coefficients. The module comment
claims the two "cannot drift" — but they are two independent literals, and nothing
enforced the equality. Under permanent D-06 code numbering a future contributor could add
a coefficient to a route (or to the family) without the other, silently diverging
DSX-STA-051's firing set from `recommend_association`'s routing table. Verified the two
are **currently equal** (both = `{pearson_correlation, spearman_correlation, kendall_tau_b,
point_biserial, phi, cramers_v}`).

**Fix applied:** added `CorrelationFamilyInvariantTest.test_family_equals_union_of_route_coefficient_sets`
to `tests/test_declared_association_routing.py` — the codebase's own invariant-test idiom
(cf. the EFFECT_SIZE_KINDS firewall test and the dataless-signature test). Locks the
"cannot drift" claim with a checkable oracle rather than a comment. Test-only change; mints
no code; catalogue count unaffected.

## Adversarially probed, cleared with no finding

- **DSX-STA-062 vs `p_pos = 0.0`** — `is_blank` (spec.py:688) returns `False` for any
  numeric (only `None` / empty-string / empty-container are blank), so a legitimate
  `p_pos: 0.0` / `p_neg: 0.0` is treated as present and does **not** false-fire. No bug.
- **DSX-STA-060 `normalize()` on a non-string icc sub-field** — `normalize` (spec.py:728)
  does `str(value)` first, so `icc.model: 123` yields `"123"` (out-of-vocab → fires
  correctly), never an `AttributeError`. No crash path.
- **DSX-STA-012 report-only seam** — the `elif kind in getattr(mathx,
  "REPORT_ONLY_EFFECT_KINDS", frozenset())` branch sits correctly inside
  `if p < alpha and standardized is not None`, between the `EFFECT_SIZE_KINDS` (011) and
  the unrecognised-kind (012) branches, so a report-only kind is recognised (report.ok)
  only on a significant standardized result and never suppresses a legitimate 011/012. The
  `getattr` default is now inert-redundant (both plans merged) but harmless.
- **`fleiss_kappa` in the DSX-STA-062 predicate** — this is an explicit recorded decision
  (18-CONTEXT.md D-02: `test ∈ {cohens_kappa, weighted_kappa, fleiss_kappa}`), tested by
  `test_fires_for_fleiss_kappa_missing_both`. Not scope drift; not a review finding.
- **Non-dict `icc` with `test != "icc"`** — presence is defined as "an `icc` dict, or
  `test == icc`" (the docstring says so); a non-dict truthy `icc` is outside the declared
  contract and is not the normal declaration path. Within the stated presence semantics;
  noted, not a defect.
- **Security** — every new gate is declaration-only string/`isinstance`/dict-lookup
  comparison against `ANALYSIS-SPEC.yaml`; no data compute path, no user-controlled regex
  (contrast the bounded falsifier regexes already hardened for T-7-03), no injection
  surface. Clean.

## Gate re-run by the orchestrator (clean tree, stray `DECISIONS.jsonl` cleared)

- Targeted Phase-18 suite (`test_declared_association_routing`,
  `test_correlation_scale_kind_gate`, `test_agreement_completeness_gate`,
  `test_effect_size_kind`, `test_no_shapiro_autoswitch`): **53 OK** pre-fix; the new
  invariant test **1 OK** → 54.
- Full suite `python -m unittest discover -s tests -q`: **Ran 1367 tests … OK** (1366 +
  the 1 invariant test).
- `python scripts/gen-finding-catalogue.py --check`: **exit 0**, "finding catalogue is
  current", **Total: 265**; the three `declared twice` warnings are pre-existing legacy
  codes (DSX-SPEC-070, DSX-VAL-021, DSX-VAL-060) — none Phase 18.
- Seam oracle `test_report_only_kappa_fires_neither_011_nor_012_and_reports_ok` **RUNS**
  (not skipped) and passes — the 18-A↔18-B cross-plan seam is live post-merge.

**Verdict: PASS.** One LOW finding, fixed additively; no correctness, security, or
lockstep defect. Ready for verification.
