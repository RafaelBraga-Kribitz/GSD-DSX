---
phase: 16-re-run-verification-off-the-gate-path
plan: 01
status: complete
requirements: [REQ-P16-02]
---

# 16-01 SUMMARY — reproduce-report gate check + the phase's only catalogue mint

## What shipped
- **`dsx/checks/repro.py`** — added `_check_reproduce_report(spec, repro, report, phase_dir)`,
  called strict-only from `check()`'s `if strict:` branch immediately after `_check_repro_lock`.
  Emits **DSX-REP-060** (HIGH) when `reproducibility.reproduce_report` is declared but the named
  `REPRO-REPORT.md` is missing, and **DSX-REP-061** (HIGH) when the report is present but its
  declared lead-metric number does not overlap `results.tests[0]` (`math.isclose`, rel_tol 1e-2).
  Opt-in on the field (never entrypoint-presence, D-02), early-returns on empty `results.tests`,
  honest `status: skipped`/`unable` short-circuits 061 (D-11), reads only the numeric block + status
  (never a verdict line, D-04). Imports added: `math`, `re` (stdlib only) — no pandas/scipy/numpy/csv,
  no subprocess/runpy/os/exec (D-01). Both message strings are fixed plain literals so the catalogue
  row text renders exactly.
- **`references/finding-codes.md`** — regenerated to **258 codes** (256 → +DSX-REP-060/061).
- **`tests/test_finding_catalogue_invariant.py`** — additive D-08 rebaseline: `_EXPECTED_TOTAL` 256→258,
  new `_SNAPSHOT_TOTAL = 256` (byte-frozen anchor size) and `_MINTED_CODES = {060, 061}`; count test
  renamed to `test_finding_catalogue_stays_at_258_codes`; set-identity test renamed to
  `test_code_set_is_phase12_snapshot_plus_the_phase16_mint`, comparing `current == snapshot ∪ {060,061}`
  with the snapshot-length leg anchored to `_SNAPSHOT_TOTAL` (256). Phase-12 snapshot fixture untouched.
- **`tests/test_reproduce_report.py`** (new) — 7 stdlib-only behavioural tests proving all four
  firing/silence conditions incl. the D-11 SKIPPED short-circuit and the D-04 verdict-agnostic 061.

## Gate evidence (all re-run by the orchestrator, brief §5)
- Task 1: AST import-purity scan OK (`_check_reproduce_report` present; no forbidden import); `tests.test_gate_path_hermetic` 2 OK.
- Task 2: `tests.test_reproduce_report` 7 tests OK; required 4 methods present.
- Task 3: `gen-finding-catalogue.py --check` exit 0 ("finding catalogue is current"); `tests.test_finding_catalogue_invariant` 2 OK; grep Total:258 / REP-060 / REP-061 all present; `git status --porcelain tests/fixtures/finding-codes-phase12.md` empty (byte-frozen).

## Deviation (plan-vs-tool grounding)
The plan's Task 3 said "run `python scripts/gen-finding-catalogue.py` (no --check)" to rewrite the
catalogue. The installed generator writes the file **only** with `--write` (bare invocation prints to
stdout). Used the grounded `--write` invocation; result verified by `--check` exit 0. Pre-existing
double-declare warnings (DSX-CLM-020/021, COH-030, PAR-002, SPEC-070, VAL-021/060) are shipped-tree
noise (S0-2) — exit code unaffected.
