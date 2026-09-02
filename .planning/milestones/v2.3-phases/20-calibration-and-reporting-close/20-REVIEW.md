# 20-REVIEW — Phase 20 code review

**Reviewer:** autonomous ceremony orchestrator (opus / high, brief §3 code-review routing).
**Date:** 2026-09-02. **Unit:** S4-4 (code review + fixes).
**Scope:** the Phase-20 execute diff `0013ea3..HEAD` (the S4-2 plan-done commit to HEAD) —
30 files, +2886 / −16. **Production code is byte-frozen** (`git diff 0013ea3..HEAD` touches
NO file under `dsx/`, `scripts/`, or `references/`): Phase 20 mints zero codes, so the whole
diff is test modules + known-bad/good-corpus fixtures + a 7-line silent addition to
`examples/good-ANALYSIS-SPEC.yaml`. The review therefore targets the one risk a
calibration/close phase actually carries — **false-pass risk in the new test code**: a test
that looks like a proof but passes vacuously. Every new/changed test module read in full.

## Files reviewed

| File | Change | Verdict |
|---|---|---|
| `tests/test_doc_code_agreement.py` | new (428→427) — REQ-P20-04 two-tier doc/code cross-check + exhaustiveness net | PASS (1 fix applied, LOW-1 below) |
| `tests/test_known_bad_corpus.py` | +226 — the live HIGH verify/ship calibration stratum (D-03/D-09) + FPR-noise-disjointness guard | PASS |
| `tests/test_phase20_zero_mint_close.py` | new (155) — REQ-P20-02 zero-mint / catalogue-close (5 oracles) | PASS |
| `tests/test_no_shapiro_autoswitch.py` | +82 — REQ-P20-03 category-complete dataless-router enumeration (anti-vacuity) | PASS |
| `tests/test_time_to_event_fallthrough.py` | +46 — REQ-P20-03 terminal-fallthrough / terminal-outcome-row regression | PASS |
| `tests/test_causal_verb_golden.py` | +39 — measured re-baseline: 3 valid controls (∅) + 5 known-bad singletons | PASS |
| `tests/test_dsx.py` | count 14→19 (five new known-bad fixtures, each a valid estimand) | PASS |
| `tests/test_frame_val.py` | `_EXPECTED_VAL_CODES` += 5 measured empty sets (defect is in `analysis:`, not the frame) | PASS |
| `examples/good-ANALYSIS-SPEC.yaml` | +7 — two in-vocab silent new-family fields (`sphericity_correction: unconditional_gg`, `power_reporting_type: a_priori`), D-08 | PASS |
| 5 × `examples/known-bad/*` fixtures (spec+narrative+postmortem) | five Phase-18 PRESENT fixtures, one per DSX-STA-05x code | PASS |
| 3 × `examples/good-corpus/valid-*` fixtures (spec+narrative) | one valid negative control per Phase-18 routing family | PASS |

## Findings

### LOW-1 — dead local variable `dist_key` (FIXED)

`tests/test_doc_code_agreement.py`, `test_decision_table_cell_equality_and_boschloo`:
`dist_key = "censored" if dist in DASHES else dist` was assigned but never read — an
early-draft artifact (the censored/time-to-event row is handled by the explicit
`if dist in DASHES: kwargs = {}` branch, so the `DIST["censored"]` lookup `dist_key` was
meant to feed is dead). Behaviour-neutral wart, the same class as the S3-4 dead-import and
S1-4 missing-`Any` findings. **Fix applied this unit:** the line removed; the module still
parses and the 15-row cell-equality assertion is byte-identical in behaviour
(`test_doc_code_agreement` 8/8 green after the fix, full suite unchanged at 1462).

## Adversarial false-pass probes (the portfolio-standard core) — all CLEARED

1. **Could the HIGH calibration stratum pass without the codes firing?** No. The stratum's
   own `high_catch_rate` bound (`0.0 ≤ x ≤ 1.0`) is deliberately weak, but the sibling
   `test_high_stratum_target_codes_fire_and_are_named` asserts, per (slug, point), that the
   code `in fired_high` read **LIVE** from `self._gate_findings` (never
   `_GOLDEN_SHIP_FINDINGS`), AND is named in the fixture's `POSTMORTEM.md`, AND is disjoint
   from `_INCIDENTAL_GAP_CODES`. A code that stopped firing turns that sibling red. **D-09
   no-self-reference honoured:** the golden ledger / incidental-allowlist identifiers appear
   only in plain-English prose in this method, never read — so the catch is genuinely live.
2. **Could the HIGH readout silently move the (miss-rate, FPR) headline?** No —
   `_headline((2,5),(1,4),(3,10)) == (0.25,0.3)` and `_ABSENT_PARTITION_FLOOR == 3` asserted
   unmoved, plus `headline == _headline(present, absent, fpr)` recomputed after the stratum:
   proves the HIGH catch is a THIRD readout beside the pair, not folded into it (D-06).
3. **Could the doc/code cross-check pass by silently failing to parse a row?** No —
   `test_skiplist_exhaustive` asserts `bound == 31`, `rows ≥ 40`, and that EVERY pipe-row is
   either bound or explicitly skip-listed; `boschloo_seen` guarantees the proportion/2/no
   Boschloo cell was actually reached. A dropped/renamed row → RED, not a lenient pass.
4. **Could the no-autoswitch proof pass vacuously after a rename?** No —
   `test_enumeration_is_non_vacuous_and_covers_every_new_category` requires the `dir()`-based
   set to be a superset of the eight known routers and to include `recommend_test`; a rename
   that emptied the set turns it red.
5. **Could the FPR be deflated by absorbing a real DSX-STA false positive as tempdir noise?**
   No — `test_fpr_noise_allowlist_is_disjoint_from_the_dsx_sta_family` structurally forbids
   any `DSX-STA-*` key in `_FPR_TEMPDIR_NOISE_CODES`.
6. **Do the five known-bad fixtures fire EXACTLY one code each (no spurious ADM/PRE/NAR)?**
   Yes — the golden ship-set in `test_causal_verb_golden` is a measured singleton per fixture
   ({DSX-STA-050…062}); the `inference.primary_procedure` omission (a measured deviation,
   recorded at S4-3) is what keeps admissibility `not_declared` so each set is its one target.

## Security / correctness

Declaration-only test code: stdlib `re`/`pathlib`/`importlib.util`/`inspect`, all reads
`encoding="utf-8"`, all line-splitting `r"\r?\n"` (CRLF-safe). No data path, no user-supplied
regex, no network, no package install. The generator is imported via `importlib.util` so its
`__main__` guard does not execute (module constants only). Clean.

## Verdict

**PASS — 1 LOW finding, fixed this unit.** The Phase-20 test surface is a genuine set of
runnable oracles with explicit anti-false-pass controls, not decorative coverage. Production
code and the catalogue are byte-frozen (275). Proceed to verification.
