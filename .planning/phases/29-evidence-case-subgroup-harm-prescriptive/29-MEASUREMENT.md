VERDICT: LIVE MISS

<!--
phase: 29
phase_name: Evidence case — subgroup harm under a prescriptive recommendation
milestone: v2.6
unit: S5-3 (D-13 measurement — the mint boundary)
measured: 2026-09-08
interpreter: CPython 3.12.10 (real; C:/Users/Benutzer1/AppData/Local/Programs/Python/Python312/python.exe)
verdict: LIVE MISS — brief section 6.5 item 9 entry condition MET; proceed to the RED/GREEN mint tasks (Branch B)
codes_minted: 0 (this unit mints nothing; Task 1 is the measurement only)
-->

# Phase 29 — MEASUREMENT (D-13 measured-first, S5-3)

This records the four/five-point measurement the frozen design (D-29-00..05) authorised.
The case shape (D-29-02), the segment floor (D-29-01) and the disposition ladder (D-29-03)
were **frozen in `29-CONTEXT.md` before this measurement began** (guardrail 1:
FREEZE-BEFORE-MEASURE); nothing here edits them. The measurement mints nothing
(guardrails 2/3). Reproduce with:

```
C:/Users/Benutzer1/AppData/Local/Programs/Python/Python312/python.exe \
  .planning/phases/29-evidence-case-subgroup-harm-prescriptive/spike/subgroup-harm-without-disposition-MEASURE.py
```

## Fixture (spike, NOT a committed corpus fixture)

`spike/subgroup-harm-without-disposition-ANALYSIS-SPEC.yaml` +
`spike/subgroup-harm-without-disposition-entrypoint.py` +
`spike/subgroup-harm-without-disposition-NARRATIVE.md` +
`spike/subgroup-harm-without-disposition-MEASURE.py` (the driver).

A genuinely **prescriptive** retention-rollout recommendation
(`question_type: prescriptive`, `design.kind: experiment`,
`identification: randomized_experiment`), a minimal-perturbation clone of the clean
control `examples/good-corpus/freq-proportion-checkout-ANALYSIS-SPEC.yaml` (which
already clears the full frame). The recipe applied (D-29-02):

- `question_type: causal → prescriptive`; the claim retyped to `prescriptive`
  ("Roll the retention bundle out to all at-risk accounts…"), carrying
  `identification: randomized_experiment`.
- `results.overall_effect: 0.032` (the positive **+3.2pp** n-weighted aggregate).
- `results.segments[]` = the frozen four-segment table (NOT shaved toward a trivial
  n/effect — D-13):

  | Segment | n | effect | opposes overall (+3.2pp)? |
  |---|---|---|---|
  | A (high-value) | 4000 | +5.0pp | no |
  | B (mid) | 3000 | +4.0pp | no |
  | C (established) | 2000 | +3.0pp | no |
  | **D (minority)** | **1000** | **−6.0pp** | **yes** |

- `decision.subgroup_harm_floor: 500` declared; segment D opposes at **n=1000, well
  above the floor**.
- `decision.subgroup_harm[]` **OMITTED entirely** — that omission, given D opposing
  above the floor under a prescriptive recommendation, is the **sole defect**.

The fixture otherwise clears the full frame honestly: SRM-balanced `observed_n`
[10000, 10000], a fully-reported primary test (effect + two-bound CI + p +
`effect_size_kind` + `standardized_effect` + `interpretation`), a time-anchored
`decision.revisit_when`, a checked assumption, `decision.minimum_practical_effect` +
`action_if_null`, and a structured `decision.replay` that greenlights the rollout on
the positive aggregate.

### The MET-030/031 structural seam (the miss, confirmed by arithmetic BEFORE interpreting)

`_check_simpsons_paradox` (`dsx/checks/metrics.py:296-349`) is the **only** function in
`dsx/` that reads `results.segments[]`. Its two emit gates, evaluated verbatim by the
driver against the DEFECT fixture:

```
overall_effect=+0.032 sign=+1; effects=[('A',0.05),('B',0.04),('C',0.03),('D',-0.06)]
opposing=[('D',-0.06)]  (count = 1 of 4)
DSX-MET-030 (metrics.py:316)  len(opposing)==len(effects):  1 == 4   -> False  (SILENT)
DSX-MET-031 (metrics.py:334)  len(opposing)>=len(effects)/2: 1 >= 2.0 -> False  (SILENT)
```

Both are **SILENT at 1-of-4 opposing**. Worse, the `else` branch (`metrics.py:348-349`)
emits `report.ok("segment effects are directionally consistent with the aggregate")` —
an INFO the driver observed at every gate point — i.e. the existing gate actively
*reassures* on a book that hides a −6.0pp minority harm. A `≥half` rule is definitionally
blind to a harmed **minority** under a positive average. This is the structural gap
§6.5 item 9 targets, confirmed by the arithmetic, not asserted.

## Four/five-point measurement — DEFECT (D opposing), verbatim

Each gate point run from a fresh `tempfile.TemporaryDirectory()` as `--phase-dir`, the
entrypoint seeded into it, a plan-time decision header seeded for verify/ship — exactly
what `tests/test_known_bad_corpus.py::_gate_findings` automates. Threshold is CRITICAL at
plan/execute, HIGH at verify/ship (`dsx/cli.py:135-140`).

| Gate point | Exit | CRITICAL | HIGH |
|---|---|---|---|
| `dsx validate`   | 0 | — | — |
| `dsx gate plan`    | 0 | — | — |
| `dsx gate execute` | 0 | — | — |
| `dsx gate verify`  | 0 | — | — |
| `dsx gate ship`    | 0 | — | — |

**No CRITICAL and no HIGH finding fires at any point.** `DSX-MET-030` and `DSX-MET-031`
are absent from the findings at every point (confirmed by dumping the full report:
`MET codes present: []`). The undispositioned opposing minority segment — the sole
defect — is caught by **no existing code**.

### Sub-threshold residuals (recorded for completeness; non-blocking, swap-invariant)

Dumping the full report (all severities) confirms the checks **ran and cleared on the
merits** rather than erroring:

- `plan`: 1 finding, INFO only — the Simpson's `report.ok` "directionally consistent"
  message described above.
- `ship`: 2 findings — the same INFO plus **`DSX-STA-011` at MEDIUM** (the primary test's
  Cohen's `h` standardized effect 0.066 is small, so the negligible-effect advisory
  fires). MEDIUM sits **below** the HIGH ship threshold, so it does not block (exit 0),
  and it reads the primary test's `standardized_effect` only — a field identical in both
  variants — so it is **swap-invariant**. It is not shaved away: the frozen case is
  +3.2pp on a 60% baseline, and reshaping the effect to dodge a non-blocking MEDIUM would
  manufacture the case (D-13). It concerns the aggregate effect size, a property entirely
  orthogonal to the undispositioned-subgroup-harm defect.

## D-29-02 swap-still-fires counterfactual (applied BY LITERAL CODE)

The driver's `build_swap` loads the DEFECT spec and flips **only** segment D's declared
effect from `−0.06` (opposing) to `+0.06` (aligned), leaving `overall_effect` declared at
`+0.032` and every other field byte-identical — so the swap isolates the **opposition of
D** and nothing else. Under the swap, `opposing = []` (0 of 4):

```
DSX-MET-030  0 == 4   -> False (SILENT)
DSX-MET-031  0 >= 2.0 -> False (SILENT)
```

Swap measurement:

| Gate point | Exit | CRITICAL | HIGH |
|---|---|---|---|
| `dsx validate`   | 0 | — | — |
| `dsx gate plan`    | 0 | — | — |
| `dsx gate execute` | 0 | — | — |
| `dsx gate verify`  | 0 | — | — |
| `dsx gate ship`    | 0 | — | — |

### Swap diff — codes that TOGGLE (per point)

| Point | stopped-under-swap (CATCH) | started-under-swap |
|---|---|---|
| validate | — | — |
| plan     | — | — |
| execute  | — | — |
| verify   | — | — |
| ship     | — | — |

**Nothing toggles.** No CRITICAL/HIGH code fires on the DEFECT fixture that stops firing
when segment D is made to align — because no CRITICAL/HIGH code fires on the DEFECT
fixture at all. There is therefore **no existing catch to subtract**: the swap-invariant
sub-threshold `DSX-STA-011` MEDIUM (aggregate effect size, orthogonal) fires identically
in both variants and never blocks.

## Verdict

**LIVE MISS.** `dsx validate` and all four gate points (`plan`/`execute`/`verify`/`ship`)
exit **0** on the honest, fully-framed prescriptive fixture. The sole defect — a declared
minority segment D opposing the positive aggregate at n=1000, well above the declared 500
floor, with no `decision.subgroup_harm[]` disposition row — is flagged by **no shipped
code**. `DSX-MET-030`/`031` are structurally silent at 1-of-4 (confirmed by the arithmetic
and by their absence from the findings), and the existing Simpson's check emits a
reassuring "directionally consistent" INFO. The swap-still-fires counterfactual toggles
nothing, so there is no existing catch to subtract. This is the cleanest possible live
miss: a genuinely prescriptive rollout recommendation, positive on the aggregate,
recommending rollout to **all** at-risk accounts while a −6.0pp harm on a material minority
(n=1000, 10% of the book) sails through the entire gate undisclosed.

Per D-13 / D-29-00 this is the **brief §6.5 item 9 entry condition MET** — a real,
documented gap. REQ-P29-02's documented public case is already found (Obermeyer et al.
2019, confirmed at its locator — `29-RESEARCH.md`), so the case-source condition of the
mint is also satisfied. The phase proceeds to **Branch B**.

## What this unit did (and did NOT) do

Task 1 mints nothing (guardrails 2/3). Confirmed:

- The measurement ran only from fresh `tempfile.TemporaryDirectory()` roots; the repo
  root has **no new `DECISIONS.jsonl`** (`git status --porcelain DECISIONS.jsonl` prints
  nothing). The transient swap spec written beside the entrypoint is deleted in a
  `finally` block; the spike directory holds only the four authored files.
- No `dsx/` file was touched (no check code authored — Task 1 authors none).
- No git command was run by this task; the orchestrator commits serially.

**Branch B — proceed to the mint path.** The LIVE MISS opens Task 2 (RED) / Task 3
(GREEN): author `_check_subgroup_harm_disposition` + `DSX-COH-041` with its honest
Gail & Simon (1985) D-05 docstring (motivating definition of a qualitative/crossover
interaction only — never the enforcement mechanic; bounded-catch: attribution over
honestly-declared segments, not detection of hidden harm), the two additive
decision-schema keys (`decision.subgroup_harm[]`, `decision.subgroup_harm_floor`), the
unit test carrying `# D-05: DSX-COH-041`, and the catalogue move 278 → 279 with all four
count pins in lockstep — then Task 4 Branch B verifies and hands off to Plan 29-02 for
fixture promotion. `dsx/checks/dq.py` stays byte-frozen.
