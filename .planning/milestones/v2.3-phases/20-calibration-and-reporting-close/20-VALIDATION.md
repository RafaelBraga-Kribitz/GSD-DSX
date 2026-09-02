---
phase: 20
slug: calibration-and-reporting-close
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-09-02
validated: 2026-09-02
---

# Phase 20 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Phase 20 is the terminal calibration-and-reporting close: it mints **zero** codes
> (catalogue stays **275**) and adds only test/fixture code (production `dsx/`,
> `scripts/`, `references/` byte-frozen). Two waves per D-07: Wave 1 = structural
> guards (20-C no-autoswitch + fallthrough / 20-D doc-code agreement), Wave 2 =
> calibration (20-A catch-rate/FPR / 20-B good-fixture + zero-mint close).
> **All oracles below re-run green by the orchestrator from a clean tree at S4-5
> (2026-09-02): full suite 1462 OK, catalogue `--check` "current" @275, 77 targeted
> Phase-20 tests OK, production byte-frozen (zero-mint structural).**

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib `unittest` (NO pytest anywhere in this repo) |
| **Config file** | none — discovered via `unittest discover -s tests` |
| **Quick run command** | `python -m unittest tests.<module_name> -v` |
| **Full suite command** | `python -m unittest discover -s tests -q` |
| **Estimated runtime** | ~41s full suite (measured this session, 1462 tests) |
| **Python** | 3.12.10 (verified this session) |

---

## Sampling Rate

- **After every task commit:** the single new/extended test module the task touched
  (e.g. `python -m unittest tests.test_known_bad_corpus -v`), **plus**
  `python -m unittest tests.test_phase20_zero_mint_close -v` on any task touching the
  catalogue-close invariant.
- **After every plan wave:** `python -m unittest discover -s tests -q`. **Both waves
  assert catalogue == 275** (Phase 20 mints no codes); the Wave-2 merge gate additionally
  asserts the four Wave-2 modules run together green (20-A's golden entry still matches
  20-B's extended fixture).
- **Before `/gsd-verify-work`:** `scripts/check.sh` in full — exercises
  `scripts/gen-finding-catalogue.py --check` (still current at 275) and the good/bad
  fixture gate smoke test at all four gate points.
- **Max feedback latency:** ~41 seconds (full suite).

---

## Per-Task Verification Map

Bound at REQ granularity across the D-07 wave split (Wave 1 = 20-C structural guards +
20-D doc-code agreement, catalogue stays 275; Wave 2 = 20-A calibration + 20-B good-fixture
extension + zero-mint close, catalogue stays 275). Phase 20 mints zero codes.

| Req / Proof | Plan | Wave | Behavior (oracle) | Test Type | Automated Command | Status |
|---|---|---|---|---|---|---|
| REQ-P20-01 | 20-A | 2 | Five PRESENT known-bad fixtures fire the five Phase-18 codes (each exactly its own singleton {DSX-STA-050/051/060/061/062}); `test_known_bad_corpus.py` extended; the stratified catch rate + FPR re-measured (CRITICAL pair unmoved + a live HIGH verify/ship third readout reading `_gate_findings`, never `_GOLDEN_SHIP_FINDINGS` = D-09; FPR denom 12→15); anchor (0.25,0.3) + floor 3 frozen; only `_GOLDEN_SHIP_FINDINGS` moved | integration + structural | `python -m unittest tests.test_known_bad_corpus -v` | ✅ green (re-run 2026-09-02) |
| REQ-P20-02 | 20-B | 2 | The good fixture is EXTENDED not replaced (D-08) with silent in-vocab new-family fields, stays silent at every threshold (fires none of the fifteen), four-code golden baseline preserved; catalogue regen additive, Phase-12 256 snapshot byte-frozen, total exactly 275; the fifteen codes in `_D05_ALLOWLIST_CODES` by exact string; 123-onward reserve absent (max code 122) | unit + catalogue | `python -m unittest tests.test_causal_verb_golden tests.test_phase20_zero_mint_close -v` | ✅ green (re-run 2026-09-02) |
| REQ-P20-03 | 20-C | 1 | The no-autoswitch structural proof is CATEGORY-COMPLETE (dynamic `inspect.signature` enumeration proves every `recommend_*` except `recommend_test` is dataless; anti-vacuity superset of the eight new-category names); the fallthrough-position regression is green after all Phase-18/19 row additions (code side: last `return _rec(` is log_rank; doc side: terminal decision-table outcome row is time-to-event) | unit, structural | `python -m unittest tests.test_no_shapiro_autoswitch tests.test_time_to_event_fallthrough -v` | ✅ green (re-run 2026-09-02) |
| REQ-P20-04 | 20-D | 1 | A read-only doc/code agreement test binds `references/test-selection.md` to `recommend_test` (Tier-1 strict cell-equality of all 15 decision rows + the Boschloo fallback pinned in `['alternatives']`) and to the six `recommend_*` mirror tables (Tier-2 honest set-membership), with a visible enumerated skip-list + exhaustiveness net (all 57 data rows accounted: 31 bound + 26 skip-listed) so the Boschloo divergence class is structurally prevented, not just repaired; negative control (welch_t vs engine welch_anova) confirms it catches divergence | cross-check (build/CI) | `python -m unittest tests.test_doc_code_agreement -v` | ✅ green (re-run 2026-09-02) |
| Zero-mint close proof | 20-B | 2 | live catalogue declared total == **275** (unchanged from Phase-19 close); production `dsx/`+`scripts/`+`references/` byte-frozen; the absent 123-onward reserve is the zero-mint tell | catalogue + structural | `python scripts/gen-finding-catalogue.py --check` + `git diff 0013ea3..HEAD -- dsx scripts references` | ✅ green / empty (re-run 2026-09-02) |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements (test files — all NEW or EXTENDED; all now exist and green)

- [x] `tests/test_known_bad_corpus.py` — EXTENDED (REQ-P20-01): five Phase-18 PRESENT fixtures + the single calibration harness extended with a live HIGH verify/ship stratum (severity-param `_classify_target_defect` default CRITICAL, `_HIGH_TARGET_DEFECT_CODES`, `_gate_findings` live never `_GOLDEN_SHIP_FINDINGS` = D-09); three valid good-corpus controls + FPR-disjointness guard
- [x] `tests/test_causal_verb_golden.py` — EXTENDED (REQ-P20-02): good fixture extended with silent in-vocab new-family fields, four-code golden baseline preserved (6/6)
- [x] `tests/test_phase20_zero_mint_close.py` — NEW (REQ-P20-02): 5 oracles (catalogue 275 / Phase-12 256 snapshot frozen-and-subset / fifteen codes allowlisted by exact string / 123-onward reserve absent / good silent)
- [x] `tests/test_no_shapiro_autoswitch.py` — EXTENDED (REQ-P20-03): `NoAutoswitchEveryNewCategoryTest` (dynamic `dir()` enumeration; anti-vacuity superset)
- [x] `tests/test_time_to_event_fallthrough.py` — EXTENDED (REQ-P20-03): `TimeToEventFallthroughPositionTest` (code + doc terminal-position pin)
- [x] `tests/test_doc_code_agreement.py` — NEW (REQ-P20-04): 8 tests, Tier-1 cell-equality + Tier-2 set-membership + skip-list + exhaustiveness net
- [x] No framework install needed — stdlib `unittest` confirmed working (baseline `--check` green this session, Python 3.12.10)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Zero-mint intent confirmed (Phase 20 is terminal calibration; the fifteen Phase-18/19 gate codes' D-05 citations are already answered via HQ-16 + HQ-17) | REQ-P20-01…04 | D-05 human read (brief §4 item 1) — already answered; Phase 20 mints no new code, so no new D-05 read is owed | HQ-16 (11 citations) + HQ-17 (16 citations) answered 2026-09-01; Phase 20 adds no citation obligation |
| No fabricated numeric ships in a fixture or a calibration anchor | REQ-P20-01 | the portfolio hard-code prohibition | The anchor `_headline((2,5),(1,4),(3,10))==(0.25,0.3)` + floor 3 are measured invariants, not invented thresholds; effect-size bands stay conventions (D-08) |

*All programmatic behaviors above have automated verification; the only manual items are the zero-mint/citation intent (HQ-16/HQ-17-answered) and the hard-code prohibition, both the standing portfolio bar, not a code oracle.*

---

## Validation Sign-Off (set at S4-5 `/gsd-validate-phase 20`, 2026-09-02)

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references (the new/extended test modules)
- [x] No watch-mode flags
- [x] Feedback latency < 60s (full suite ~41s)
- [x] `nyquist_compliant: true` set in frontmatter (after execute + validate)

**Approval:** NYQUIST-COMPLIANT 2026-09-02 (orchestrator, State A audit). All 4 requirements
(REQ-P20-01…04) have automated verification: every mapped oracle re-run green by the orchestrator
from a clean tree (stray `DECISIONS.jsonl` cleared first per the HUMAN-QUEUE standing note) —
77 targeted Phase-20 tests OK (`test_known_bad_corpus` + `test_causal_verb_golden` +
`test_phase20_zero_mint_close` + `test_doc_code_agreement` + `test_no_shapiro_autoswitch` +
`test_time_to_event_fallthrough`) + `gen-finding-catalogue.py --check` "current" @275 + production
byte-frozen (`git diff 0013ea3..HEAD -- dsx scripts references` empty, zero-mint structural), all
inside a full suite of **1462 OK**. Phase 20 mints zero codes (catalogue stays 275; the absent
123-onward reserve is the tell). Two manual-only items (zero-mint/citation intent — HQ-16/HQ-17-
answered — and the hard-code prohibition) are the standing portfolio bar, not code oracles.
Zero gaps → no nyquist-auditor spawn required (workflow §3). `nyquist_compliant: true`,
`status: validated`.

---

## Validation Audit 2026-09-02

| Metric | Count |
|--------|-------|
| Requirements | 4 (REQ-P20-01…04) |
| COVERED (automated, green) | 4 |
| PARTIAL | 0 |
| MISSING | 0 |
| Manual-only (zero-mint/citation intent + hard-code prohibition) | 2 (HQ-16/HQ-17-answered) |
| Gaps found | 0 |
| Resolved | 0 (none to resolve — all oracles present and green) |
| Escalated | 0 |

State A audit: every mapped oracle re-run by the orchestrator from a clean tree (brief §5;
stray `DECISIONS.jsonl` ledgers cleared first per the HUMAN-QUEUE standing note). No new test
files generated — the Wave-0 modules (two new + four extended) already exist and pass.
`nyquist_compliant: true`, `status: validated`.
