VERDICT: LIVE MISS

<!--
phase: 28
phase_name: Evidence case — magnitude no test computed
milestone: v2.6
unit: S4-3 (D-13 measurement — the mint boundary)
measured: 2026-09-07
interpreter: CPython 3.12.10 (real; C:/Users/Benutzer1/AppData/Local/Programs/Python/Python312/python.exe)
verdict: LIVE MISS — brief section 6.5 item 8 entry condition MET; proceed to the RED/GREEN mint tasks
codes_minted: 0 (this unit mints nothing; Task 1 is the measurement only)
-->

# Phase 28 — MEASUREMENT (D-13 measured-first, S4-3)

This records the four-point measurement the frozen design (D-28-00..05) authorised.
The case shape (D-28-01) and the pass/fail rule (D-28-02) were **frozen in
`28-CONTEXT.md` before this measurement began** (guardrail 1: FREEZE-BEFORE-MEASURE);
nothing here edits them. The measurement mints nothing (guardrail 2/3). Reproduce with:

```
C:/Users/Benutzer1/AppData/Local/Programs/Python/Python312/python.exe \
  .planning/phases/28-evidence-case-magnitude-no-test-computed/spike/magnitude-no-test-computed-MEASURE.py
```

## Fixture (spike, NOT a committed corpus fixture)

`spike/magnitude-no-test-computed-ANALYSIS-SPEC.yaml` +
`spike/magnitude-no-test-computed-NARRATIVE.md` +
`spike/magnitude-no-test-computed-entrypoint.py`.

A descriptive/observational churn readout (`question_type: descriptive`,
`design.kind: observational`, so the causal-identification and `decision.replay`
obligations stay off — D-28-01). Two `results.tests[]` entries are computed, both on
metrics **other than churn**:

- **A** `metric: revenue_per_user` — `effect: 0.27`, `ci: [0.15, 0.39]`, `p_value: 0.002`,
  `effect_size_kind: d`, `standardized_effect: 0.45`, non-null `interpretation`.
- **B** `metric: activation_rate` — `effect: 0.18`, `ci: [0.09, 0.27]`, `p_value: 0.004`,
  `effect_size_kind: d`, `standardized_effect: 0.38`, non-null `interpretation`.

One **`association`-typed** claim on **churn (metric C, which NO test computes)**, text
verbatim:

> Customers holding fewer than two products churn at 27% against 18% for the rest of the book, over the 2026-Q2 window.

`base_n: 5000` is declared; the narrative body carries base language ("full book of
5,000 customers", "n=5,000"); `evidence:` points at the committed narrative; a
`population` is stated; a one-line `limitations[]` is declared. **The fixture declares
NO `claims[].supported_by` anywhere** — this keeps the case a live-miss seam and (later)
an honest MISS for the declaration-gated `DSX-CLM-034`.

### The frozen D-28-00 collision (the load-bearing clearance of DSX-CLM-033)

`_extract_claim_magnitudes` extracts exactly the claim's **percent** literals
`[27.0, 18.0]` (bare integers like "two" and the date token "2026-Q2" are not
extracted). `DSX-CLM-033` (`_check_numeric_overlap`, `dsx/checks/claims.py:343-401`)
builds its reference from the union over **all** tests of `{effect, effect×100, each CI
bound, bound×100}` and clears a literal iff it matches any reference number under
`_close_enough` = rel ≤ 5% OR abs ≤ 5e-4 (`claims.py:439-443`). Measured mapping
(from the driver's collision probe):

| Claim literal | Reconciles with (test, field, value) | Bridge | abs diff | Inside window? |
|---|---|---|---|---|
| `27` | test A `revenue_per_user` `effect` 0.27 → ×100 = 27.0 | ×100 proportion | 0.0 | yes (abs ≤ 5e-4) |
| `27` | (also) test B `activation_rate` `ci` upper 0.27 → ×100 = 27.0 | ×100 proportion | 0.0 | yes |
| `18` | test B `activation_rate` `effect` 0.18 → ×100 = 18.0 | ×100 proportion | 0.0 | yes |

Both headline literals coincide with a **real reported number of the WRONG metric**, so
`DSX-CLM-033` clears **on its full union-membership logic (not a skip)** while nothing
verifies that any test measured churn. This is the mislabelled-magnitude defect (D-28-00).

## Four-point measurement — DEFECT (collision) fixture, verbatim

Each gate point run from a fresh `tempfile.TemporaryDirectory()` as `--phase-dir`, the
entrypoint seeded into it, a plan-time decision header seeded for verify/ship — exactly
what `tests/test_known_bad_corpus.py::_gate_findings` automates. CRITICAL/HIGH only.
`claims`, `stats`, `narrative` register at **verify and ship** only
(`dsx/cli.py:121-131`); threshold is HIGH at verify/ship, CRITICAL at plan/execute
(`dsx/cli.py:135-140`).

| Gate point | Exit | CRITICAL | HIGH |
|---|---|---|---|
| `dsx validate`   | 0 | — | — |
| `dsx gate plan`    | 1 | `DSX-COH-001` | — |
| `dsx gate execute` | 0 | — | — |
| `dsx gate verify`  | 1 | `DSX-COH-001` | — |
| `dsx gate ship`    | 1 | `DSX-COH-001` | — |

**`DSX-CLM-033` is SILENT at verify and ship** — it ran fully and cleared on the merits
via the ×100 bridge above. The only blocking residual is `DSX-COH-001` (see the swap
diff below for why it is incidental).

### Existing checks that clear ON THE MERITS at ship (D-28-02 table, measured)

Verified by dumping the ship report and confirming each code is **absent** from the
findings (i.e. it ran and passed, not skipped):

`DSX-CLM-033` (numeric overlap — cleared via collision), `DSX-CLM-070` (base_n
declared), `DSX-CLM-050` (population stated, no generalisation term), `DSX-CLM-030/031`
(evidence pointer resolves to the committed narrative), `DSX-CLM-080` (n/a — descriptive
question_type does not require limitations; a limitation is declared anyway),
`DSX-NAR-020` (claim text present in the narrative), `DSX-NAR-040` (narrative body carries
base language), `DSX-STA-002/003` (each test reports an effect and a two-bound CI),
`DSX-STA-011` (non-negligible `d`; no negligible-effect flag), `DSX-STA-012`
(`effect_size_kind: d` recognised), `DSX-STA-020/021` (reporting-contract companions
clear). All fourteen clear.

## D-28-02 swap-still-fires counterfactual (applied BY LITERAL CODE)

Two variants, each rewriting **only** the claim's percent literals `27%`/`18%` (and their
echoes in the narrative body) — the tests' reported numbers (0.27, 0.18, and every CI
bound) are untouched, so each swap isolates the claim↔test numeric relationship and
nothing else.

### Variant 1 — HONEST swap: `27→15`, `18→9` (numbers that GENUINELY appear in a cited test)

15 = test A `revenue_per_user` CI lower 0.15 ×100; 9 = test B `activation_rate` CI lower
0.09 ×100. Numbers still reconcile, so `DSX-CLM-033` stays silent.

| Gate point | Exit | CRITICAL | HIGH |
|---|---|---|---|
| `dsx validate`   | 0 | — | — |
| `dsx gate plan`    | 1 | `DSX-COH-001` | — |
| `dsx gate execute` | 0 | — | — |
| `dsx gate verify`  | 1 | `DSX-COH-001` | — |
| `dsx gate ship`    | 1 | `DSX-COH-001` | — |

**Diff vs DEFECT: identical CRITICAL/HIGH set at every one of the five points — no code
toggles.** No code fires on the collision fixture that stops firing when the magnitude
is made to reconcile honestly ⇒ **no code catches the mislabelled-magnitude defect**.

### Variant 2 — BREAK swap: `27→33`, `18→44` (numbers absent from every test; collision broken)

33 and 44 appear in no test's `{effect, effect×100, CI bound, bound×100}` union.

| Gate point | Exit | CRITICAL | HIGH |
|---|---|---|---|
| `dsx validate`   | 0 | — | — |
| `dsx gate plan`    | 1 | `DSX-COH-001` | — |
| `dsx gate execute` | 0 | — | — |
| `dsx gate verify`  | 1 | `DSX-CLM-033`, `DSX-COH-001` | — |
| `dsx gate ship`    | 1 | `DSX-CLM-033`, `DSX-COH-001` | — |

**Diff vs DEFECT: `DSX-CLM-033` STARTS firing under the break swap at verify and ship.**
`DSX-CLM-033` responds only to numeric membership — it is metric-blind and `supported_by`-
blind. Its **silence on the collision fixture is caused by the numeric collision, not by
any verification that churn was computed**. That silence is the miss.

## Residual-code review

- **`DSX-CLM-033`** (CRITICAL) — the predicted catch. Measured **silent** on the collision
  fixture (cleared on the merits), and it **starts** firing only when the collision is
  broken. Under the swap-still-fires rule (a code is a catch iff it STOPS firing when the
  magnitude reconciles honestly), `DSX-CLM-033` does the opposite → **not a catch** of the
  churn-metric-binding defect; it is a numeric-membership gate the collision defeats by
  construction (D-28-00).
- **`DSX-COH-001`** (CRITICAL, `dsx/checks/coherence.py`) — fires because the claim is
  typed `association` (strength 1) while `question_type` is `descriptive` (strength 0):
  "the question framing does not license this strength of claim." It is **swap-invariant**
  (fires identically on DEFECT, HONEST and BREAK) and concerns the claim-type-vs-question
  strength ladder, a **different property** than the claim↔test metric binding — it would
  fire even if a churn test existed, and stays silent to the number-collision entirely.
  It is inherent to the frozen D-28-01 shape (an association-typed magnitude claim under a
  descriptive question) and is therefore a **documented incidental**, not a catch.

## Verdict

**LIVE MISS.** `dsx validate` and `dsx gate execute` are clean; `dsx gate plan/verify/ship`
block only on the swap-invariant, defect-orthogonal `DSX-COH-001`. After subtracting that
documented incidental, **nothing flags the uncomputed-magnitude defect**: `DSX-CLM-033`
clears on its full union-membership logic (the 27/18 collision with test A/B via the ×100
bridge) and is proven metric-blind by the break swap; no code stops firing under the honest
swap. Per D-28-02 this is the **brief §6.5 item 8 entry condition MET** — a real, documented
gap: an honest, well-formed descriptive churn spec whose headline magnitude is quoted for a
metric no test computed sails through the entire gate because its numbers happen to coincide
with the reported effects of two other metrics.

## What this unit did (and did NOT) do

Task 1 mints nothing (guardrails 2/3). The LIVE MISS opens the mint path: the phase now
proceeds to **Task 2 (RED)** and **Task 3 (GREEN)** — author `_check_supported_by_traceability`
+ `DSX-CLM-034` with its honest Wilkinson & TFSI (1999) D-05 docstring, the two additive
claims-schema keys, the unit test carrying `# D-05: DSX-CLM-034`, and the catalogue move
277 → 278 — then **Task 4 Branch B** verifies and hands off to **Plan 28-02** for fixture
promotion. `dsx/checks/dq.py` is untouched.

The measurement was run only from fresh `tempfile.TemporaryDirectory()` roots; the repo
root has no new `DECISIONS.jsonl` (`git status --porcelain DECISIONS.jsonl` prints nothing).
