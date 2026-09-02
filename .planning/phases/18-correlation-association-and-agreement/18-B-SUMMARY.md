---
phase: 18-correlation-association-and-agreement
plan: B
subsystem: statistics / effect-size conventions
tags: [statistics, effect-size, conventions, report-only, mathx, firewall]
requires:
  - "mathx.EFFECT_SIZE_KINDS / interpret_effect (the frozen {d,h,r} blocking domain, left byte-unchanged)"
  - "dsx.checks.stats.check (existing DSX-STA-011/012 magnitude guard, consumed read-only by the seam oracle)"
provides:
  - "mathx.REPORT_ONLY_EFFECT_KINDS — the report-only recognition set the DSX-STA-012 branch (Plan 18-A) consults"
  - "mathx.KAPPA_BANDS + KAPPA_BANDS_CITATION — Landis & Koch 1977 kappa bands, pinned as a labeled convention"
  - "mathx.KRIPPENDORFF_REFERENCE + KRIPPENDORFF_REFERENCE_CITATION — level-keyed reference values (ordinal 0.7598)"
  - "mathx.CONVENTION_CATALOG — named catalog-only entries (ICC/Koo-Li, Kendall's W, dCor, partial, Cronbach->omega)"
  - "mathx.label_convention_band(kind, value) — report-only labeler, never fed into DSX-STA-011"
  - "templates/APA-TABLE-research.md convention-band note (ungated wiring point; mints no finding code)"
affects:
  - "Plan 18-A dsx/checks/stats.py DSX-STA-012 branch (imports REPORT_ONLY_EFFECT_KINDS) — the ONE cross-plan seam"
tech-stack:
  added: []
  patterns:
    - "report-only registry + labeling function structurally separate from the blocking band domain (D-06)"
    - "level-keyed reference table so a value always carries its level of measurement (D-07)"
    - "catalog-only named entries with no numeric boundary and no fabricated locator (D-07)"
    - "guarded cross-plan seam oracle (unittest.skipUnless) — green in isolation, enforced post-merge"
key-files:
  created: []
  modified:
    - dsx/mathx.py
    - templates/APA-TABLE-research.md
    - tests/test_effect_size_kind.py
decisions:
  - "EFFECT_SIZE_KINDS stays exactly frozenset({d,h,r}) and interpret_effect is byte-unchanged — the D-06 firewall, asserted by an equality (not subset) test"
  - "The report-only bands live in a separate mathx surface consulted only by the DSX-STA-012 recognition branch and the ungated template; no finding code is minted"
  - "Landis-Koch edge-tie handling is a labeled convention choice (lower band takes the tie), not claimed as the paper's exact wording"
  - "The report-only-firing seam oracle is guarded (skipUnless a live-seam probe) so this plan is green in isolation with the oracle SKIPPED"
metrics:
  duration: "~15 min"
  completed: 2026-09-01
  tasks: 2
  files: 3
status: complete
---

# Phase 18 Plan B: Correlation/Agreement Effect-Size Conventions Summary

Report-only correlation/agreement magnitude bands (kappa, ICC, Kendall's W, Krippendorff) added to `dsx/mathx.py` as labeled conventions that are recognised but never used as blocking thresholds — the blocking band domain `EFFECT_SIZE_KINDS` stays frozen at `{d, h, r}`, the bands are wired only into the ungated APA template, and the one cross-plan report-only-firing behaviour is pinned by a guarded seam oracle.

## What was built

**Task 1 — report-only registry and convention-band tables in `dsx/mathx.py` (TDD: RED → GREEN → REFACTOR).**
- `REPORT_ONLY_EFFECT_KINDS = frozenset({"kappa","icc","kendalls_w","phi","cramers_v","tau_b","rho"})` — the recognition set the DSX-STA-012 branch (Plan 18-A) consults, deliberately disjoint from the blocking `EFFECT_SIZE_KINDS`.
- `KAPPA_BANDS` (+ `KAPPA_BANDS_CITATION`) — Landis & Koch (1977), *Biometrics* 33(1):159–174, pinned as a labeled convention; edge-tie handling labeled a convention choice (lower band takes the tie), not the paper's exact wording.
- `KRIPPENDORFF_REFERENCE` (+ `KRIPPENDORFF_REFERENCE_CITATION`) — level-keyed: `ordinal → 0.7598` (HQ-16 B4), `nominal → 0.4765`, `interval → 0.7574`, `ratio → 0.6621`. The value always carries its level; the ordinal value is reachable only by asking for the ordinal level (a level-free lookup returns `None`).
- `CONVENTION_CATALOG` — named catalog-only entries for ICC/Koo-Li, Kendall's W (carrying the explicit "no band citation exists" note), distance correlation, partial correlation, and Cronbach → McDonald omega; each named with NO numeric boundary and NO fabricated locator.
- `label_convention_band(kind, value)` — a report-only labeler distinct from `interpret_effect`; returns the Landis-Koch label for `kappa` and a "convention, no gated boundary" label otherwise, and never raises (so it can never masquerade as a blocking guard).
- `EFFECT_SIZE_KINDS` and `interpret_effect` are byte-unchanged (verified by diff: additions only).

**Task 2 — ungated APA template wiring + report-only seam oracle.**
- `templates/APA-TABLE-research.md` gained a "labeled conventions, never blocking" section presenting the Landis-Koch kappa bands, the level-carrying Krippendorff value (0.7598 @ ordinal), and the named catalog-only pointers (ICC/Koo-Li, Kendall's W boundary-free), with the "conventions never block" statement in prose. The template mints no finding code (asserted structurally by a no-`DSX-*-code` test).
- `tests/test_effect_size_kind.py` gained the report-only-firing seam oracle: `effect_size_kind = kappa` on a significant result must fire neither DSX-STA-011 nor DSX-STA-012 and must yield a `report.ok` (a `passed_checks` entry) naming the convention. It is guarded with `unittest.skipUnless(_report_only_seam_is_live(), ...)` — a live-seam probe — so it SKIPS in isolation and enforces at the Wave-1 merge with Plan 18-A's `stats.py` branch.

## Verification evidence

**Task 1 RED (before implementing mathx symbols):** `Ran 18 tests ... FAILED (failures=1, errors=18)`. The 18 errors/1 fail were exactly the new-symbol assertions (`AttributeError: module 'dsx.mathx' has no attribute 'REPORT_ONLY_EFFECT_KINDS' / 'KRIPPENDORFF_REFERENCE' / 'label_convention_band' / 'CONVENTION_CATALOG'`). The firewall test (`test_effect_size_kinds_is_exactly_d_h_r`) and `test_interpret_effect_still_rejects_a_report_only_kind` PASSED — expected, since they protect the existing frozen state (not an unexpected RED-phase pass).

**Task 1 GREEN:** `Ran 18 tests ... OK`; inline check printed `firewall+registry+pin OK` (EFFECT_SIZE_KINDS exactly `{d,h,r}`; registry subset+disjoint; `KRIPPENDORFF_REFERENCE['ordinal']==0.7598`). REFACTOR removed a dead duplicate return branch in `label_convention_band`; re-run `Ran 18 tests ... OK`.

**Task 2 RED:** `test_template_names_the_conventions ... FAIL` (template lacked the note); `test_report_only_kappa_fires_neither_011_nor_012_and_reports_ok ... skipped` (seam absent in isolation).

**Task 2 GREEN:** `Ran 21 tests ... OK (skipped=1)`; template verify printed `template wiring OK`.

**Full suite (regression check):** `Ran 1338 tests in 36.731s ... OK (skipped=1)`. The only skip is this plan's seam oracle. The `DSX-SPEC-070 / DSX-VAL-021 / DSX-VAL-060 declared twice` warnings are pre-existing and unrelated to the three files this plan touched.

## Cross-plan seam (validated at the Wave-1 merge)

The report-only-firing behaviour (`effect_size_kind: kappa` fires neither DSX-STA-011 nor DSX-STA-012 and yields a `report.ok` naming the convention) is produced by **Plan 18-A's** DSX-STA-012 branch in `dsx/checks/stats.py` consulting **this plan's** `REPORT_ONLY_EFFECT_KINDS`. This plan owns the registry (mathx side) and the pinning test; 18-A owns the consuming branch. The seam oracle is SKIPPED in isolation (probe finds current `stats.py` still fires DSX-STA-012 for `kappa`) and ENFORCES after the Wave-1 merge. This is a recorded residual, not a silent drop.

## Deviations from Plan

None affecting behaviour. One in-plan correction during Task 2: an initial draft of the template note referenced the internal finding code `DSX-STA-011` in prose, which the plan's own "mints no finding code" requirement (and this plan's `test_template_mints_no_finding_code` assertion) forbids — the reference was reworded to "the tool's blocking magnitude guard (via `mathx.interpret_effect`)" so the template carries no `DSX-*` code literal. This kept the structural "conventions never block" enforcement intact.

## Known Stubs

None. All symbols are wired: the registry is consumed by the (guarded) seam oracle, the bands/reference/catalog are presented in the template, and `label_convention_band` is exercised by the Landis-Koch and catalog tests. Catalog-only entries are intentionally boundary-free per D-07 (a D-05 read is owed before any ICC/Koo-Li or Kendall's W numeric band ships) — documented, not a stub.

## Threat Flags

None. This plan adds only report-only convention data plus one ungated template note — no data path, no gate path, no new I/O surface, no new dependency. The three STRIDE mitigations from the plan's register hold: EFFECT_SIZE_KINDS byte-unchanged (T-18-B-01), only 0.7598@ordinal and Landis-Koch pinned while ICC/Koo-Li and Kendall's W ship catalog-only (T-18-B-02), and the guarded seam oracle detects registry↔branch drift post-merge (T-18-B-03).

## Self-Check: PASSED

- `dsx/mathx.py` — FOUND, additions only (EFFECT_SIZE_KINDS/interpret_effect byte-unchanged, verified by diff).
- `templates/APA-TABLE-research.md` — FOUND, convention note present (Landis, 0.7598, ordinal, kappa; no DSX-* code).
- `tests/test_effect_size_kind.py` — FOUND, 21 tests (18 Task-1 + seam oracle skipped + 2 template).
- Commit `fdd8617` — FOUND (Task 1). Commit `9647387` — FOUND (Task 2).
- Branch `gsd/v2.3.0-test-catalog` before first and after last commit — CONFIRMED.
