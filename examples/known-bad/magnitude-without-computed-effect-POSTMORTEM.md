# Post-mortem: a headline magnitude quoted for a metric no test computed

Paired spec: `magnitude-without-computed-effect-ANALYSIS-SPEC.yaml`
Paired entrypoint: `magnitude-without-computed-effect-entrypoint.py`

## What was concluded

A retention-analytics team published a descriptive quarterly readout of customer
churn. The headline claim states, verbatim:

> Customers holding fewer than two products churn at 27% against 18% for the rest
> of the book, over the 2026-Q2 window.

The specification is honest in every declaration a gate can read: `question_type`
is `descriptive`, `design.kind` is `observational` (so no causal-identification or
`decision.replay` obligation attaches), `base_n` is declared, a `population` is
stated, a one-line `limitations[]` is present, the `evidence:` pointer resolves to
a committed narrative, and the narrative body carries the base language. Two
`results.tests[]` entries are computed and each clears the statistics reporting
contract on its merits.

## Why it was wrong

The two computed tests are on metrics **other than churn**: test **A** is on
`revenue_per_user` (`effect: 0.27`, `ci: [0.15, 0.39]`) and test **B** is on
`activation_rate` (`effect: 0.18`, `ci: [0.09, 0.27]`). **No test computes
churn** — the metric the headline magnitude is quoted for. The claim's literals
`27` and `18` are real reported numbers, but of the *wrong metrics*: `0.27`×100 =
27 is test A's `revenue_per_user` effect (and also test B's `activation_rate` CI
upper bound), and `0.18`×100 = 18 is test B's `activation_rate` effect. This is a
copy-from-the-wrong-row error — the single commonest real-world magnitude defect.

`DSX-CLM-033` (`_check_numeric_overlap`, `dsx/checks/claims.py:343-401`) builds its
reference from the **union over all tests** of `{effect, effect×100, each CI bound,
bound×100}` and clears a claim literal iff it matches any reference number under
`_close_enough` (rel ≤ 5% OR abs ≤ 5e-4). Both `27` and `18` are present in that
union via the ×100 proportion bridge, so `DSX-CLM-033` clears **on its full
union-membership logic — not by a skip** — while nothing verifies that any test
measured the claimed metric. `DSX-CLM-033` is metric-blind and reads no
claim-to-cited-test pointer; its silence is caused by the numeric collision, not
by any verification that churn was computed. That silence is the miss.

The defect is attributable **only** through the missing claim→test metric binding
— the exact brief §6.5 item 8 entry condition. The fixture omits the optional
claim-to-cited-test traceability pointer, so the declaration-gated `DSX-CLM-034`
(minted in plan 28-01, HIGH) finds nothing to read and correctly stays silent:
`DSX-CLM-034` buys **attribution, not detection**.

## Four-point measurement (the D-28-02 entry-condition test)

Measured on the real interpreter (CPython 3.12.10) from a fresh
`tempfile.TemporaryDirectory()` as `--phase-dir` per gate point, the entrypoint
seeded into it and a plan-time decision header seeded for verify/ship — exactly
what `tests/test_known_bad_corpus.py::_gate_findings` automates. CRITICAL/HIGH
only. This reproduces the four-point table recorded verbatim in
`28-MEASUREMENT.md` and is the D-28-02 entry-condition test for a live miss.

| Gate point | Exit | CRITICAL findings | HIGH findings |
|---|---|---|---|
| `dsx validate`   | 0 | — | — |
| `dsx gate plan`    | 1 | `DSX-COH-001` | — |
| `dsx gate execute` | 0 | — | — |
| `dsx gate verify`  | 1 | `DSX-COH-001` | — |
| `dsx gate ship`    | 1 | `DSX-COH-001` | — |

`DSX-CLM-033` is **silent at verify and ship** — it ran fully and cleared on the
merits via the ×100 bridge above. The only blocking residual is `DSX-COH-001`.

## The swap-still-fires counterfactual (applied by literal code)

Two variants rewrite **only** the claim's percent literals (and their echoes in the
narrative body); the tests' reported numbers are untouched, so each swap isolates
the claim↔test numeric relationship and nothing else.

### Variant 1 — HONEST swap: `27→15`, `18→9` (numbers that genuinely appear in a cited test)

15 = test A `revenue_per_user` CI lower 0.15 ×100; 9 = test B `activation_rate` CI
lower 0.09 ×100. The numbers still reconcile, so `DSX-CLM-033` stays silent.

| Gate point | Exit | CRITICAL findings | HIGH findings |
|---|---|---|---|
| `dsx validate`   | 0 | — | — |
| `dsx gate plan`    | 1 | `DSX-COH-001` | — |
| `dsx gate execute` | 0 | — | — |
| `dsx gate verify`  | 1 | `DSX-COH-001` | — |
| `dsx gate ship`    | 1 | `DSX-COH-001` | — |

**Diff vs DEFECT: identical CRITICAL/HIGH set at every point — no code toggles.**
No code fires on the collision fixture that stops firing when the magnitude is made
to reconcile honestly ⇒ **no code catches the mislabelled-magnitude defect**.

### Variant 2 — BREAK swap: `27→33`, `18→44` (numbers absent from every test; collision broken)

33 and 44 appear in no test's `{effect, effect×100, CI bound, bound×100}` union.

| Gate point | Exit | CRITICAL findings | HIGH findings |
|---|---|---|---|
| `dsx validate`   | 0 | — | — |
| `dsx gate plan`    | 1 | `DSX-COH-001` | — |
| `dsx gate execute` | 0 | — | — |
| `dsx gate verify`  | 1 | `DSX-CLM-033`, `DSX-COH-001` | — |
| `dsx gate ship`    | 1 | `DSX-CLM-033`, `DSX-COH-001` | — |

**Diff vs DEFECT: `DSX-CLM-033` starts firing under the break swap at verify and
ship.** It responds only to numeric membership — it is metric-blind and reads no
claim-to-cited-test pointer. Its silence on the collision fixture is caused by the
numeric collision, not by any verification that churn was computed.

## The residual is a documented incidental, not a catch

`DSX-COH-001` (CRITICAL, `dsx/checks/coherence.py::_check_claim_ceiling`) fires
because the one claim is typed `association` (strength 1) while `question_type` is
`descriptive` (strength 0): "the question framing does not license this strength of
claim." `_check_claim_ceiling` reads **only** `claims[].type` and `question_type`
and no numeric literal, so its swap-invariance is a **structural theorem**, not
merely the measured swap tables above — it fires identically on the DEFECT, HONEST
and BREAK variants, and would fire even if a churn test existed. It concerns the
claim-type-vs-question strength ladder, a **different property** than the claim↔test
metric binding this fixture exists to demonstrate. It is therefore a swap-invariant,
defect-orthogonal **documented incidental corpus-gap code**, none about claim→test
traceability — encoded per D-28-06 in
`tests/test_known_bad_corpus.py::_PER_FIXTURE_INCIDENTAL_CODES` (point-scoped to
plan/verify/ship), never credited as this fixture's catch. It is also
`prescriptive-churn-recommendation`'s own declared target, which is exactly why it
cannot be laundered into the global `_INCIDENTAL_GAP_CODES`.

## The code that now attributes the miss

`DSX-CLM-034` (HIGH, `dsx/checks/claims.py::_check_supported_by_traceability`,
minted in plan 28-01 under D-05 with a Wilkinson & TFSI (1999) motivating-principle
docstring) is the code that **attributes** this miss. It reads a declared
claim-to-cited-test pointer and checks the headline magnitude traces to the
specific cited test; this honest spec declares no such pointer, so the check
correctly stays silent — attribution of the gap, not detection of it. A separate
positive-firing unit test proves `DSX-CLM-034` bites when the pointer *is* declared
but does not cover the number. The machine-countable absent-code tag lives in the
paired `magnitude-without-computed-effect-ATTRIBUTION.yaml` sidecar
(`absent_code: DSX-CLM-034`, `kind: miss`).
