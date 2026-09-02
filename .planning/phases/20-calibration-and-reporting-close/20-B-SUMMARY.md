---
phase: 20-calibration-and-reporting-close
plan: B
wave: 2
requirements: [REQ-P20-02]
status: complete
mints_codes: 0
catalogue_total: 275
good_fixture_baseline_preserved: true
files_touched: [examples/good-ANALYSIS-SPEC.yaml, tests/test_phase20_zero_mint_close.py, references/finding-codes.md]
---

# 20-B SUMMARY — zero-mint catalogue close + good-fixture silent extension (REQ-P20-02)

Wave-2 catalogue-close plan (depends_on 20-C, 20-D). Delivers **REQ-P20-02**. **Zero
finding codes minted; catalogue stays 275; both frozen snapshots unmutated.** Executed
inline on the ceremony branch `gsd/v2.3.0-test-catalog` by the orchestrator (never
`handle_branching`, per the standing HUMAN-QUEUE branch-safety rule). Two atomic commits
(`142267e` Task 1, `8af492f` Task 2).

## What was built

**Task 1 — the canonical good fixture extended, not replaced (D-08).**
`examples/good-ANALYSIS-SPEC.yaml`'s `analysis:` block gains two silent, in-vocabulary,
non-triggering new-family scalar declarations that exercise the Wave-2 families' happy
path and provably stay silent:

- `sphericity_correction: unconditional_gg` — DSX-STA-070 fires ONLY on
  `mauchly_conditional` (verified at `dsx/checks/stats.py:1092`), so `unconditional_gg`
  is silent; it is a member of `SPHERICITY_CORRECTIONS`, so the DSX-STA-040 membership
  gate is silent.
- `power_reporting_type: a_priori` — DSX-STA-111 fires ONLY on `observed`/`post_hoc`
  (verified at `dsx/checks/stats.py:1289`), so `a_priori` is silent; it is a member of
  `POWER_REPORTING_TYPES`, so DSX-STA-040 is silent.

Neither field interacts with `outcome_type`/`test`/`estimand_kind`, so the fixture's
CRITICAL/HIGH ship set is preserved exactly at its four-code baseline
`{DSX-CLM-031, DSX-DQ-001, DSX-FIG-001, DSX-NAR-010}` (all tempdir-artifact noise) — the
baseline that 20-A's `tests/test_causal_verb_golden.py` pins. This plan reads that golden
test and preserves its entry; it does not edit it (the documented cross-plan read-only
invariant). No existing field removed or replaced; no trigger value declared; no
`report.add` site added.

**Task 2 — the zero-mint / catalogue-close oracle.**
`tests/test_phase20_zero_mint_close.py` (stdlib-only: `unittest`, `re`, `pathlib`,
`importlib.util`; CRLF-safe, `encoding="utf-8"`) turns the D-01 "mints zero codes" claim
into five runnable oracles:

1. `references/finding-codes.md` declares **275**.
2. `tests/fixtures/finding-codes-phase12.md` declares **256** and its parsed code-set is
   a **subset** of the current catalogue (the catalogue only grows additively — nothing
   frozen was dropped or renamed).
3. All fifteen milestone codes (Phase-18 050/051/060/061/062 + Phase-19
   070/080/081/090/100/110/111/120/121/122) are in
   `gen-finding-catalogue.py::_D05_ALLOWLIST_CODES` **by exact string**, and `"DSX-STA-"`
   is **not** in `_D05_ALLOWLIST_PREFIXES` (a prefix add would obligate ~40 uncited
   legacy DSX-STA codes — the exact-code path is deliberate). Loaded via
   `importlib.util` so the generator's `__main__` guard never runs.
4. The reserve band from **123 upward** (constructed from a numeric range, never
   hard-coded) is **absent** from the catalogue; the highest DSX-STA code is **122** —
   the deliberate zero-mint tell, mirroring REQ-P19-03's absent 06x decade.
5. The good fixture fires **none** of the fifteen at ship (read-only silence proof).

`references/finding-codes.md` was regenerated via `--write` as a **no-op diff** (zero
`report.add` sites this phase); `scripts/gen-finding-catalogue.py` is **unchanged**
(the allowlist already carried all fifteen by exact string — REQ-P20-02's allowlist
clause is a VERIFY, not a change). `tests/fixtures/finding-codes-phase12.md` is
byte-frozen (`git diff` empty).

## Gate (Task-level, re-run by orchestrator)

- Task 1: `python -m unittest tests.test_causal_verb_golden` → **6 OK** (four-code
  baseline preserved); acceptance oracle prints "good fixture extended … fires none of
  the fifteen; golden baseline preserved".
- Task 2: `python scripts/gen-finding-catalogue.py --check` → "finding catalogue is
  current" @275; `python -m unittest tests.test_phase20_zero_mint_close` → **5 OK**;
  inline oracle prints "275; snapshot 256; fifteen allowlisted by exact string;
  123-onward reserve unused; good silent".

## S4-3 Wave-2 MERGE GATE (re-run by orchestrator from a clean tree)

Both waves now landed — merge gate green:

- Full suite `python -m unittest discover -s tests -q` → **Ran 1462 tests OK**
  (Wave-1+20-A baseline 1457 + 5 new zero-mint tests; the "declared twice" warnings are
  pre-existing legacy, none Phase-20; the two `explain` tests passed — no stray root
  `DECISIONS.jsonl`).
- `gen-finding-catalogue.py --check` → "finding catalogue is current" @**275**.
- `validate-capability.py` → conformant.
- Gate contract (via `bin/dsx`, `DSX_PYTHON=python`): good spec **passes** at
  plan/execute/verify/ship; bad spec **blocks** at all four; missing-spec exit **2**;
  audit output **deterministic**.
- The four Wave-2 acceptance modules run together —
  `test_causal_verb_golden + test_phase20_zero_mint_close + test_doc_code_agreement`
  **19 OK**, `test_known_bad_corpus` (calibration harness + no-autoswitch + fixtures)
  **47 OK** — so 20-A's golden entry still matches 20-B's extended fixture (the
  cross-plan invariant holds at merge).
- Branch confirmed `gsd/v2.3.0-test-catalog` before and after.

## S4-3 status after this plan

Wave 1: **20-C ✅** (REQ-P20-03) **∥ 20-D ✅** (REQ-P20-04). Wave 2: **20-A ✅**
(REQ-P20-01) **∥ 20-B ✅** (REQ-P20-02). Wave-2 merge gate **GREEN**. **S4-3 COMPLETE**
— all four plans landed, catalogue stays 275, zero codes minted this phase. Next: S4-4
(code review + verification, REQ-P20-01..04).
