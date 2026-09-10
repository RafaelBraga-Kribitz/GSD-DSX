# Plan 30-01 — SUMMARY (S6-3 Wave 1: measurement + readout)

**Status: COMPLETE.** Measured LIVE 2026-09-10 on the real 3.12.10 interpreter
(`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`, `Python 3.12.10`).
Zero codes minted; no frozen surface changed.

## What was done

1. **`_measure_readout.py` copied forward + adapted** from the Phase-12 template
   (`.planning/milestones/v2.0.0-phases/12-calibration/_measure_readout.py`). Body copied
   forward unchanged except (a) an `assert (ROOT / "tests" / "test_known_bad_corpus.py").exists()`
   at import (ROOT resolves via `parents[3]` — the new file sits three levels below repo root,
   same depth as the template; the assertion passed, so no index adjustment was needed), and
   (b) one appended read-only `out["target"]` block that measures the corpus's one `kind: target`
   sidecar's firing code (DSX-COH-041) severity at all four gate points **without touching the
   PRESENT-partition denominator**. The ABSENT loop's `kind != "miss"` guard already excludes the
   target sidecar; the PRESENT loop's `_CRITICAL_THRESHOLD_POINTS` axis was NOT widened.

2. **Ran the companion LIVE** and confirmed all forced construction facts (GA-2):
   - headline `miss_rate == 1.0`; ABSENT `denom == 5`, `misses == 5`
   - headline `fpr == 0.0`; FPR `denom == 15`
   - `absent_floor == 3` (misses 5 ≥ 3, floor holds comfortably)
   - the two NEW misses `DSX-ML-034` (feature-origin-only-leak) and `DSX-CLM-034`
     (magnitude-without-computed-effect) each `fires_at_any_severity: false`
   - `out["target"]`: `DSX-COH-041` fires **CRITICAL at plan / verify / ship**, silent at execute
     (coherence not in the execute gate profile)
   - PRESENT partition `10 / 10` caught (100%), including the new DSX-COH-041 plan cell

3. **Ran the durable reproducer of record** `test_stratified_catch_rate_and_fpr_report` on the
   real interpreter — **OK** (8.3s) over the 42+15 corpus; it independently asserts the
   independent PRESENT/ABSENT denominators, the 5-case ABSENT floor ≥ 3, and the
   target-present-invariance proof.

4. **Wrote `30-READOUT.md`** mirroring `12-READOUT.md`: headline pair → stratified PRESENT/ABSENT
   → FPR /15 (one-sided 95% upper bound ≈ 0.181, not a point estimate) → per-family friction
   (RAW and NET) → limits → **Statistician review placeholder** (deferred to S6-3/S6-4 per GA-1).
   Every number transcribed from the companion JSON; none estimated. The Task-3 verify grep gate
   (`5/5`, `0/15`, `0.18`) passed.

## Measured numbers (the terminal re-baseline)

| Quantity | Value |
|---|---|
| Miss-rate (ABSENT) | 1.0 = 5/5 (construction invariant; evidential content = 5× `fires_at_any_severity: false`) |
| FPR (good-control) | 0.0 = 0/15 (one-sided 95% upper bound ≈ 0.181; denom moved 12 → 15) |
| PRESENT partition | 10/10 caught |
| ABSENT floor | 3 (met at 5) |
| Friction | raw 101, net 69, cells 74; raw rate ≈ 1.36/cell, net rate ≈ 0.93/cell |
| DSX-COH-041 profile | CRITICAL @ plan/verify/ship; silent @ execute |
| Live catalogue count observed | 279 (readout context; authoritative set-identity gate runs in plan 30-02) |

## Frozen surfaces

`git status --porcelain dsx/ examples/ references/` after the companion run showed **only** the
operator-local untracked `references/The AI Data Scientist.md` (leave-untouched set) — **no**
tracked `dsx/`, `examples/`, or `references/` file modified. The companion is read-only and shells
`dsx gate` in a fresh tempdir off the gate path.

## Next

S6-3 continues at plan 30-02 (wave 2, `depends_on: [30-01]`): refresh `brief.md §6.5` calibration
backdrop + the literature doc to these measured numbers, add the REQ-P30-02 corpus-count agreement
test, and run the full REQ-P30-02 audit battery + REQ-P30-03 zero-mint (279 → 279) on the final
tree. The S6-3 ledger box stays UNCHECKED until Wave 2 completes and its gate passes.
