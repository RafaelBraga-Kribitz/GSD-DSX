---
phase: 20
unit: S4-4
verdict: PASSED
requirements_verified: [REQ-P20-01, REQ-P20-02, REQ-P20-03, REQ-P20-04]
gate_rerun_by_orchestrator: true
full_suite: "Ran 1462 tests OK"
catalogue_total: 275
minted_codes: []
production_code_byte_frozen: true
---

# 20-VERIFICATION — Phase 20 goal-backward verification

**Verifier:** autonomous ceremony orchestrator (opus / high, brief §3 verification routing).
**Date:** 2026-09-02. **Unit:** S4-4 (verification `passed`).
**Method:** goal-backward against REQ-P20-01..04 — for each requirement, the delivered
artifact and the gate that proves it, re-run by the orchestrator (not trusted from a subagent
report). All commands run from a clean tree (stray `DECISIONS.jsonl` cleared per the
HUMAN-QUEUE standing note). The LOW-1 fix from `20-REVIEW.md` (dead `dist_key` removed) is
included in every rerun.

## Phase goal

Terminal calibration + reporting close. Turn "the fifteen new Phase-18/19 codes are catchable
and the doc/code seam cannot silently drift" into runnable oracles, **minting zero new codes**
(catalogue stays 275, production code byte-frozen). Concretely: known-bad fixtures for every
new blocking code with the stratified catch-rate / FPR re-baselined where the codes actually
fire; the good fixture extended-not-replaced and silent; the no-autoswitch proof made
category-complete; and a doc/code agreement cross-check that structurally prevents the
Boschloo divergence class.

## Requirement-by-requirement verdict

### REQ-P20-01 — known-bad fixtures for every new blocking code; harness extended; catch-rate/FPR re-baselined → **PASS**

- **Delivered:** five dedicated PRESENT known-bad fixtures
  (`correlation-pearson-ordinal-scale`, `correlation-for-agreement-estimand`,
  `icc-incomplete-triple`, `weighted-kappa-missing-weights`, `kappa-missing-companions`),
  one per Phase-18 code (050/051/060/061/062 — the five that fired nowhere in `examples/`
  before). `tests/test_known_bad_corpus.py` **extended** with a live HIGH verify/ship
  stratum: `_classify_target_defect` gains a `severity="CRITICAL"` default (every pre-Phase-20
  call byte-identical, D-03), `_HIGH_TARGET_DEFECT_CODES` declares the expected cell, and the
  stratum re-derives its catch LIVE via `self._gate_findings` filtered to HIGH — NEVER from
  `_GOLDEN_SHIP_FINDINGS` (D-09). FPR denominator 12→15 via three valid good-corpus controls;
  `_FPR_TEMPDIR_NOISE_CODES` proven disjoint from the DSX-STA family (D-05).
- **Gate re-run:** `tests.test_known_bad_corpus` + `tests.test_causal_verb_golden` green
  (inside the targeted 77 OK and the full 1462 OK). The golden ship-set is a measured
  singleton per fixture; `test_high_stratum_target_codes_fire_and_are_named` positively
  verifies each DSX-STA-05x fires live at verify/ship AND is named in its POSTMORTEM.
- **Re-baseline honesty (D-06):** the synthetic anchor `_headline((2,5),(1,4),(3,10)) ==
  (0.25,0.3)` and `_ABSENT_PARTITION_FLOOR == 3` asserted unmoved; the HIGH readout is a
  third readout beside (miss-rate, FPR), not folded into it.

### REQ-P20-02 — good fixture extended-not-replaced and silent; additive regen; new codes allowlisted as exact strings → **PASS**

- **Delivered:** `examples/good-ANALYSIS-SPEC.yaml` gains two in-vocabulary silent fields
  (`sphericity_correction: unconditional_gg`, `power_reporting_type: a_priori`) — not
  replaced; its four-code ship baseline is preserved. `tests/test_phase20_zero_mint_close.py`
  (new, 5 oracles) proves: catalogue declares 275; the Phase-12 snapshot declares 256 and is
  a SUBSET of the current catalogue (additive-only); all fifteen milestone codes are in
  `_D05_ALLOWLIST_CODES` by EXACT string and `DSX-STA-` is NOT an allowlisted prefix; the
  123-onward reserve is absent and `max(DSX-STA) == 122`; the good fixture fires none of the
  fifteen.
- **Gate re-run:** `tests.test_phase20_zero_mint_close` 5/5 green; `gen-finding-catalogue.py
  --check` → "finding catalogue is current" @275. Zero `report.add` sites added (production
  byte-frozen).

### REQ-P20-03 — no-autoswitch covers every new category; fallthrough-position regression green → **PASS**

- **Delivered:** `tests/test_no_shapiro_autoswitch.py` gains `NoAutoswitchEveryNewCategoryTest`
  — a `dir()`-based enumeration of every `recommend_*` router with an anti-vacuity superset
  guard (must cover the eight new-category routers + `recommend_test`), proving each
  new-category router is dataless (no `data`/`n`/distribution parameter). `recommend_test` is
  the one legacy declared-shape router, explicitly pinned as the exception.
  `tests/test_time_to_event_fallthrough.py` gains `TimeToEventFallthroughPositionTest` —
  code-side: the terminal `return _rec(` names `log_rank`; doc-side: the decision table's
  terminal outcome row is time-to-event (block bounded by the next `##`, not the `[^1]`
  in-cell footnote trap).
- **Gate re-run:** both modules green (inside the 77 OK and 1462 OK).

### REQ-P20-04 — doc/code agreement test binds test-selection.md to recommend_test; Boschloo divergence structurally prevented → **PASS**

- **Delivered:** `tests/test_doc_code_agreement.py` (new) — a read-only cross-check (not a
  generated mirror; ~280 lines of `test-selection.md` are irreducible prose, D-02). Tier 1:
  strict cell-equality of all 15 Decision-table rows to `recommend_test(...)['test']`, with
  the **Boschloo fallback asserted present** in the proportion/2/no `['alternatives']` — the
  exact cell the divergence class lived in — and a `boschloo_seen` reachability guard. Tier 2:
  honest set-membership of the six `recommend_*` mirror tables. Anti-false-pass:
  `test_skiplist_exhaustive` proves all pipe rows are bound (31) or explicitly skip-listed.
- **Gate re-run:** `tests.test_doc_code_agreement` 8/8 green (after LOW-1 fix). No divergence
  surfaced → `references/test-selection.md` and `dsx/checks/stats.py` remain byte-frozen.

## Orchestrator gate evidence (clean tree, this unit)

- `python scripts/gen-finding-catalogue.py --check` → "finding catalogue is current" @275
  (the 9 `declared twice` warnings are pre-existing legacy, none Phase-20).
- `python -m unittest -q tests.test_doc_code_agreement tests.test_phase20_zero_mint_close
  tests.test_known_bad_corpus tests.test_no_shapiro_autoswitch
  tests.test_time_to_event_fallthrough tests.test_causal_verb_golden` → **Ran 77 tests OK**.
- `python -m unittest discover -s tests -q` → **Ran 1462 tests OK** (the two `explain` tests
  passed → no stray root `DECISIONS.jsonl`).
- `git diff 0013ea3..HEAD -- dsx scripts references` → **empty** (production + catalogue
  byte-frozen; zero codes minted).

## Verdict

**PASSED** — all four requirements delivered with re-run oracles; production code and the
catalogue byte-frozen at 275; one LOW review finding fixed. Ready for S4-5
(`/gsd-secure-phase 20` + `/gsd-validate-phase 20`).
