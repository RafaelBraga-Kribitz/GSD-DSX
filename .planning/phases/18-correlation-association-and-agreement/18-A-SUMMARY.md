---
phase: 18-correlation-association-and-agreement
plan: A
subsystem: statistics / declaration-only gate library
tags: [statistics, routing-table, correlation, agreement, finding-codes, declaration-gate, anti-two-stage]
requires:
  - Phase 17 estimand_kind six-member vocabulary (dsx/spec.py ESTIMAND_KINDS)
  - Phase 17 D-06 pre-allocated code ranges (050-059, 060-069)
  - Plan 18-B mathx.REPORT_ONLY_EFFECT_KINDS (cross-plan seam; present on this branch)
provides:
  - recommend_association(estimand_kind) — dataless routing (REQ-P18-01/06)
  - DSX-STA-050/051/060/061/062 — five HIGH declaration-only finding codes
  - ICC_MODELS/ICC_TYPES/ICC_DEFINITIONS/KAPPA_WEIGHT_TOKENS/OPERAND_SCALES closed vocabularies
  - Association/agreement section in references/test-selection.md
  - regenerated references/finding-codes.md at 265 codes
affects:
  - dsx/checks/stats.py (recommend_association, _check_declared_association, DSX-STA-012 seam)
  - dsx/spec.py (five vocabularies + _VOCABULARIES registration)
  - scripts/gen-finding-catalogue.py (_D05_ALLOWLIST_CODES)
tech-stack:
  added: []
  patterns:
    - dataless string->set routing lookup (anti-two-stage proof via inspect.signature)
    - gate body split by predicate group for per-function D-05 docstring resolution
    - isinstance-before-normalize for a field spanning enum + structural type (weights)
    - defensive getattr(module, attr, default) for a cross-plan seam inert-until-merge
key-files:
  created:
    - tests/test_declared_association_routing.py
    - tests/test_correlation_scale_kind_gate.py
    - tests/test_agreement_completeness_gate.py
    - .planning/phases/18-correlation-association-and-agreement/18-A-SUMMARY.md
  modified:
    - dsx/checks/stats.py
    - dsx/spec.py
    - references/test-selection.md
    - references/finding-codes.md
    - scripts/gen-finding-catalogue.py
    - tests/test_finding_catalogue_invariant.py
decisions:
  - "recommend_association is dataless (signature == [estimand_kind]) — the mechanical anti-two-stage proof, stronger than a data-accepting branch (REQ-P18-06)"
  - "Field shapes resolved per OQ-1/2/3: analysis.operand_scale (closed vocab, in _MEMBERSHIP_FIELDS); analysis.icc.{model,type,definition}; flat analysis.weights/p_pos/p_neg"
  - "DSX-STA-062 requires BOTH p_pos AND p_neg (D-04, HQ-16-corrected Feinstein-Cicchetti Part II), not raw-agreement+prevalence"
  - "Five codes added by exact name to _D05_ALLOWLIST_CODES, never the DSX-STA- prefix (~40 uncited legacy codes)"
  - "DSX-STA-012 seam reads mathx.REPORT_ONLY_EFFECT_KINDS via getattr with empty default — inert until 18-B, active on merge; EFFECT_SIZE_KINDS never widened"
metrics:
  duration: ~35m
  completed: 2026-09-01
  tasks: 3
  files_created: 4
  files_modified: 6
  tests_added: 26
status: complete
---

# Phase 18 Plan A: Correlation, association and agreement routing + gates Summary

Delivered the dataless `recommend_association` routing function, the five-code declaration-only gate `_check_declared_association` (DSX-STA-050/051/060/061/062, all HIGH), the closed sub-vocabularies those codes read, the `references/test-selection.md` doc mirror, and the regenerated finding catalogue at 265 codes — plus the DSX-STA-012 report-only effect-size seam that consults Plan 18-B's `mathx.REPORT_ONLY_EFFECT_KINDS` without widening the blocking band domain.

## What was built

**Task 1 — vocabularies, doc mirror, D-05 allowlist (commit `03c0327`).**
- `dsx/spec.py`: `ICC_MODELS`, `ICC_TYPES`, `ICC_DEFINITIONS`, `KAPPA_WEIGHT_TOKENS`, `OPERAND_SCALES` closed vocabularies with Shrout-Fleiss 1979 / McGraw-Wong 1996 citation comments; all five registered in `_VOCABULARIES` so `dsx vocab` discovers them.
- `references/test-selection.md`: new `## Association / agreement` section — the human mirror of `recommend_association` (correlation + agreement rows keyed on declared `estimand_kind`), the DSX-STA-050/051 scale/kind doctrine, and catalog-only pointer rows (distance correlation, partial correlation, Cronbach → McDonald ω) with no invented boundary or fabricated locator (D-07).
- `scripts/gen-finding-catalogue.py`: the five codes added by exact name to `_D05_ALLOWLIST_CODES` with a dated Phase-18 comment (NOT the `DSX-STA-` prefix — ~40 uncited legacy codes). Inert at this stage; `--check` stayed 0 at 260.

**Task 2 (TDD) — routing + gate + catalogue (commit `a8ac933`).**
- `recommend_association(estimand_kind)` — dataless normalize-then-lookup over `_ASSOCIATION_ROUTES`; returns `{tests, effect_size, citation}`; raises `ValueError` for agreement/method_comparison/ordered_trend.
- `_check_declared_association` dispatching to `_check_correlation_scale_kind` (050/051) and `_check_agreement_completeness` (060/061/062), each with its own attributable D-05 docstring (per-function resolution, 18-RESEARCH.md Pattern 1). Wired at BOTH `check()` call sites (not-tests early return + post-loop return).
- `operand_scale` registered in `_MEMBERSHIP_FIELDS` (DSX-STA-040 reuse — zero new code for the recognition half).
- D-03 whitelist (050 fires only for Pearson vs declared-ordinal; point_biserial and dichotomous never fire), Pitfall-5 isinstance branch on `weights` (explicit matrix accepted, never stringified), D-04 both-companions rule for 062.
- `references/finding-codes.md` regenerated (not hand-edited) to 265, in the SAME commit as the report.add sites (D-08 lockstep).
- RED confirmed (27 errors + 2 failures) before implementation; GREEN = all 30 tests across the four modules pass; `--check` exits 0 at 265.

**Task 3 — DSX-STA-012 report-only seam (commit `0381a2e`).**
- `from .. import mathx` (existing name imports kept). New `elif kind in getattr(mathx, "REPORT_ONLY_EFFECT_KINDS", frozenset())` branch: a report-only kind is recognised via `report.ok(...)` naming the labeled convention, firing NEITHER DSX-STA-011 nor DSX-STA-012 (REQ-P18-05). `EFFECT_SIZE_KINDS` untouched; `dsx/mathx.py` never edited (18-B owns it).

## Verification evidence (verbatim outputs captured)

- Task 1 inline check: `vocab+doc+allowlist OK`; `gen-finding-catalogue.py --check` exit 0 at 260.
- Task 2: RRED (27 errors / 2 failures) → GREEN (`Ran 30 tests ... OK`); `--check` exit 0; `**Total: 265 codes.**`; all five codes present in the catalogue.
- Task 3: `tests.test_good_fixture_phase15` + `tests.test_known_bad_corpus` (48 tests) OK; canonical fixtures silent on all five new codes; `tests.test_effect_size_kind` (21 tests) OK — the 18-B seam oracle `test_report_only_kappa_fires_neither_011_nor_012_and_reports_ok` RAN and PASSED (not skipped).
- Full suite (Wave-1 merge gate, 18-B present): `Ran 1366 tests ... OK`.
- `inspect.signature(recommend_association)` == `['estimand_kind']` (REQ-P18-06 proof).
- `mathx.EFFECT_SIZE_KINDS` == `['d','h','r']` (untouched).
- `git diff HEAD~3 HEAD -- examples/ dsx/mathx.py templates/APA-TABLE-research.md tests/test_effect_size_kind.py` → empty (no forbidden file edited).

## Deviations from Plan

None functional. One honesty-driven adjustment inside the permitted file `tests/test_finding_catalogue_invariant.py`: beyond the plan-named `_EXPECTED_TOTAL` (260→265) and `_MINTED_CODES` (+5 codes), the two test-method names and their assertion messages that literally said "260" were updated to "265" so the human-facing prose does not contradict the assertions (repo CLAUDE.md verification-honesty). `_SNAPSHOT_TOTAL` (256) and `tests/fixtures/finding-codes-phase12.md` remain byte-frozen (D-08 trap #3 respected).

## Cross-plan seam note

The DSX-STA-012 report-only branch is the single semantic seam with Plan 18-B (18-CONTEXT.md D-08). It reads `mathx.REPORT_ONLY_EFFECT_KINDS` via `getattr` with an empty-frozenset default: inert if 18-B is absent, active once merged. On this branch 18-B is already present, so the seam is validated live — kappa fires neither DSX-STA-011 nor DSX-STA-012 and emits a `report.ok` naming the convention.

## Known Stubs

None. No hardcoded empty values flowing to output; every gate reads declared spec fields. The catalog-only pointer rows (dCor, partial correlation, ICC/Kendall's-W bands, Cronbach→ω) are intentional named-without-boundary entries per D-07 not-in-hand disposition, documented in the doc mirror as such — not stubs.

## Threat Flags

None. This plan adds only declaration-only string/structure membership guards on the `analysis:` block — no new network endpoint, no auth path, no file access, no schema change at a trust boundary. All STRIDE register mitigations (T-18-A-01..05) are implemented: exact normalize-equality membership, isinstance-before-normalize on `weights`, exact-name D-05 allowlist enforcement, in-commit catalogue regeneration, and presence-only D-07 citation for the not-in-hand doctrinal scale reference.

## Self-Check: PASSED
- Created files exist: tests/test_declared_association_routing.py, tests/test_correlation_scale_kind_gate.py, tests/test_agreement_completeness_gate.py — all present.
- Commits exist: 03c0327, a8ac933, 0381a2e — all on branch gsd/v2.3.0-test-catalog.
- Catalogue at 265; D-05 build gate exit 0; full suite 1366 tests OK.
