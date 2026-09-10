---
phase: 30
artifact: calibration-readout
requirement: REQ-P30-01 (terminal calibration re-baseline), REQ-P30-03 (zero-mint context)
status: recorded-pending-review
measured: 2026-09-10
reproducing_gate: python -m unittest tests.test_known_bad_corpus.TestKnownBadCorpus.test_stratified_catch_rate_and_fpr_report
statistician_review: pending — adversarial dsx-statistician review lands at S6-3/S6-4 (GA-1), against these measured numbers
---

# Phase 30 — Calibration re-baseline (terminal) — readout

**Status: RECORDED (numbers measured LIVE 2026-09-10); adversarial Statistician review PENDING.**
Per GA-1 (`30-CONTEXT.md §1`, the Phase-24 / 12-READOUT precedent), the heavy adversarial
Statistician review is part of *this readout*, deferred to the readout recording (S6-3/S6-4,
RECORD-WITH-AMENDMENTS gate) where it can bite on measured output — not the pre-measurement
discuss. §6 below is a marked placeholder.

Every number in this readout is computed **LIVE** over the grown corpus (**42 known-bad +
15 good-control** ANALYSIS-SPECs) by the harness in `tests/test_known_bad_corpus.py` via
`_gate_findings` (a real `dsx gate <point>` in a fresh tempdir) and `_classify_target_defect`
— never estimated. The numbers were extracted read-only, **off the gate path**, by
`.planning/phases/30-calibration-rebaseline/_measure_readout.py` (a read-only companion copied
forward from the Phase-12 template). The **durable reproducer of record** is the frontmatter
unittest `test_stratified_catch_rate_and_fpr_report`, not the companion; it asserts exactly
these partitions and the ABSENT floor and passed live this firing (8.3s).

This is the **terminal** re-baseline. It replaces the Phase-12 baseline (miss-rate 1.0 = 3/3,
FPR 0/12, three misses) with the post-v2.6 corpus (five misses, FPR /15) after Phases 27/28/29
wired the three v2.6 evidence cases. **Zero codes minted** — the measurement routes entirely
to existing codes.

## 1. Headline — the pair (miss-rate, false-positive-rate)

| Quantity | Value |
|---|---|
| **Miss-rate** (ABSENT partition) | **1.0** = 5 / 5 |
| **False-positive rate** (good-control corpus) | **0.0** = 0 / 15 |

The headline is deliberately the **pair (miss-rate, FPR)**, never catch-rate alone (D-10). Every
target-**present** fixture carries a present-and-firing code, so a single catch-rate headline
would be a regression-pin dressed as detection — adding already-caught cases drives it toward
100% for free. The ABSENT/miss partition is **floored at 3** (`_ABSENT_PARTITION_FLOOR`; now met
comfortably at 5 ≥ 3, up from exactly 3 in Phase 12), and an **invariance proof** in the gate
confirms that injecting a synthetic target-present case leaves the headline byte-identical.

**On reading the miss-rate as a "rate" (12-READOUT F3, carried forward).** The ABSENT partition
is *curated* to be misses — each sidecar is `kind: miss` and each case was confirmed to miss
before inclusion — so within any passing run the miss-rate is 1.0 **by construction of the
partition**; it carries **no** sampling information about a miss *propensity*. The evidential
content is not the aggregate 1.0 but the **five independent per-case `fires_at_any_severity:
false` confirmations** in §2b — that each named shipped code is genuinely silent everywhere, at
every severity across all four gate points, not merely below the CRITICAL threshold. This
milestone adds **two** such misses: **DSX-ML-034** on `feature-origin-only-leak` (item 7) and
**DSX-CLM-034** on `magnitude-without-computed-effect` (item 8), each measured silent at every
severity — mirroring the Phase-27/28 measurements. Read 1.0 as "all five curated misses
reproduce as misses," not as an estimated population rate. **No confidence interval is quoted on
the miss-rate** (it is a construction invariant, not a sample).

## 2. Catch rate — stratified PRESENT vs ABSENT (D-10)

### 2a. PRESENT partition — 10 / 10 caught (100%)

Every (fixture × gate-point) cell the effective target map expects to fire a code, live-verified
as firing that code CRITICAL at the point:

| Fixture | Point | Expected code(s) | Result |
|---|---|---|---|
| bayesian-continuous-monitoring | plan | DSX-PAR-011 | CAUGHT |
| bayesian-continuous-monitoring | execute | DSX-PAR-011 | CAUGHT |
| frequentist-uncontrolled-continuous | plan | DSX-PAR-010 | CAUGHT |
| frequentist-uncontrolled-continuous | execute | DSX-PAR-010 | CAUGHT |
| full-frame-cleaning | execute | DSX-CODE-020, DSX-CODE-021, DSX-CODE-030 | CAUGHT |
| interference-shared-budget | plan | DSX-INT-010 | CAUGHT |
| prescriptive-churn-recommendation | plan | DSX-COH-001, DSX-COH-010 | CAUGHT |
| **subgroup-harm-without-disposition** | **plan** | **DSX-COH-041** | **CAUGHT** |
| triggering-dilution | plan | DSX-INT-030 | CAUGHT |
| weak-identification-mmm | plan | DSX-VAL-040 | CAUGHT |

**PRESENT catch rate = 10/10 = 100%.** The new cell this milestone is
`subgroup-harm-without-disposition` × plan → **DSX-COH-041** (Phase 29, the corpus's first
`kind: target`). On the cells it claims, dsx catches everything, at CRITICAL, reproducibly.

**The full DSX-COH-041 catch profile (`out["target"]`, the honest inverse of the two new misses).**
The stratified partition counts DSX-COH-041 only at its `plan` cell (the PRESENT axis is
`_CRITICAL_THRESHOLD_POINTS = ("plan", "execute")`, and `coherence` is absent from the `execute`
gate profile). Measured across all four gate points, DSX-COH-041 fires **CRITICAL at plan, verify
and ship**, and is **silent at execute** (coherence not registered there):

| Code | plan | execute | verify | ship |
|---|---|---|---|---|
| DSX-COH-041 (subgroup-harm-without-disposition) | CRITICAL | — | CRITICAL | CRITICAL |

Where the two new misses cite `fires_at_any_severity: false`, the one new target cites this full
plan/verify/ship CRITICAL profile — a real DETECTED catch minted from the paper's own §6 idea.

### 2b. ABSENT partition — 5 / 5 missed (100% miss-rate)

The five miss cases: each carries a `<slug>-ATTRIBUTION.yaml` sidecar (`kind: miss`). Its
`absent_code` field names the **nearest shipped catalogue code** that stays silent on this
fixture (no code is minted in a sidecar). What is *absent* is not the code but the **capability**
to catch the defect in its undeclared / misdeclared / fabricated instantiation — the §6.5 backlog
item each sidecar promotes. The harness confirms each named code is silent at **every** severity
across all four gate points:

| Fixture | Nearest silent code (shipped) | Promotes §6.5 item | Missed at CRITICAL | **Fires at ANY severity, anywhere** |
|---|---|---|---|---|
| **feature-origin-only-leak** *(new v2.6)* | DSX-ML-034 | item 7 (feature provenance) | yes | **no** |
| garden-of-forking-paths-p-hacking | DSX-EXP-051 | item 1 (specification sensitivity) | yes | **no** |
| **magnitude-without-computed-effect** *(new v2.6)* | DSX-CLM-034 | item 8 (magnitude without computed effect) | yes | **no** |
| operator-known-answer-selective-exclusion | DSX-VAL-080 | item 1 (specification sensitivity) | yes | **no** |
| retracted-fabricated-field-experiment | DSX-REP-020 | item 7 (feature provenance) | yes | **no** |

**The two additions this milestone are genuine, measured misses.** `feature-origin-only-leak`
(item 7): the innocuous joined feature carries no `feature_provenance` declaration to fire on, so
**DSX-ML-034** — the minted provenance check — is silent (the honest attribution, Phase 27,
measured LIVE MISS in `27-MEASUREMENT.md`). `magnitude-without-computed-effect` (item 8): the
claim's reported numbers are the REAL numbers of *other* metrics, so `DSX-CLM-033` clears on full
logic while no test computed the claimed metric, and **DSX-CLM-034** — the minted
claim→cited-test traceability check — is silent because the fixture declares no `supported_by`
(Phase 28, measured LIVE MISS). Both are attribution, not detection: a declaration-integrity gate
cannot see a defect the operator never declared.

### 2c. Why a 100% miss-rate on the ABSENT partition is the intended, honest result

The ABSENT partition is the set of defects instantiated in the **undeclared / misdeclared /
fabricated shape a declaration gate cannot see**. dsx is a *declaration-integrity* gate, not a
data-forensics or replication engine. A 100% miss-rate here is **not** a detection regression — it
measures the **known ceiling on undisclosed / fabricated instantiations**, each attributed to the
specific §6.5 capability that would move it. The two numbers together — **PRESENT 10/10 caught,
ABSENT 5/5 missed** — say: *dsx catches everything it claims, and the corpus documents,
attributably, exactly the undisclosed / fabricated shapes it does not claim to catch.* The two new
v2.6 misses extend that documented ceiling honestly (feature provenance without a provenance
declaration; a magnitude claim with no computed effect behind it), and the one new v2.6 target
(DSX-COH-041) extends the demonstrated catch set with a real closed catch minted from the paper's
own subgroup-harm idea.

## 3. False-positive rate — good-control corpus (D-04)

**FPR = 0 / 15 = 0.0.** Fifteen genuinely clean ANALYSIS-SPECs under `examples/good-corpus/` gated
at ship; **none** produced a real false-positive blocking finding after excluding the documented
tempdir-noise codes (`_FPR_TEMPDIR_NOISE_CODES` — file-path `where`, not statistical-validity
concepts, D-04). **The denominator moved from 12 (Phase 12) to 15** — three good-control specs
added since — improving the rate resolution.

**0/15 is not evidence of a ~0 false-positive rate — it is a bounded observation.** The one-sided
95% upper confidence bound on 0/15 is ≈ **0.181** (Clopper-Pearson `1 − 0.05^(1/15) ≈ 0.181`;
rule-of-three ≈ 3/15 = 0.20). A true false-positive rate as high as roughly **1-in-5** on
well-formed input is fully consistent with observing 0/15. This is an upper *bound*, not a point
estimate.

## 4. Friction — per-family over-blocking (D-11)

Friction is the over-blocking BEYOND each fixture's intended catch, reported **RAW and NET**
(net-only is a laundering hole), as a per-cell rate over the non-target in-profile
(fixture × gate-point) cells.

| Corpus total | Value |
|---|---|
| Raw ship-blocking findings | 101 |
| Net (raw − own-target) | 69 |
| Non-target in-profile cells | 74 |
| **Raw friction rate** | **≈ 1.36** per cell (101 / 74) |
| **Net friction rate** | **≈ 0.93** per cell (69 / 74) |

The per-cell rates fell sharply from Phase 12 (raw 6.0, net 4.92 per cell) **not** because the
over-block shrank but because the denominator of non-target in-profile cells grew from 13 to 74
(the corpus grew to 42 known-bad fixtures, most of them low-blocking chart fixtures added since
Phase 12). The over-block is still dominated by the same handful of incidental codes that
fire on almost every analytical fixture in a fresh tempdir — `DSX-CLM-031`, `DSX-MET-040`,
`DSX-NAR-001`, `DSX-REP-030`. The friction column exists to keep this over-block **visible**
(RAW), not to hide it (NET).

**All 69 net over-block comes from 13 analytical families** (raw 83, net 69); the other 29
fixtures each block only their own target code or nothing (raw 18, net 0 — 18 own-target-only
fixtures at raw 1 each, plus 11 clean-at-ship fixtures at raw 0). The two new v2.6 misses show
`own = []` (miss cases, so raw == net): `feature-origin-only-leak` 4/4,
`magnitude-without-computed-effect` 1/1.

<details><summary>Per-family raw/net — the 13 families with net over-block (accounts for all 69 net)</summary>

| Fixture | Raw | Net | Own-target codes |
|---|---|---|---|
| bayesian-continuous-monitoring | 9 | 8 | DSX-PAR-011 |
| feature-origin-only-leak *(new v2.6 miss)* | 4 | 4 | — |
| frequentist-uncontrolled-continuous | 7 | 6 | DSX-PAR-010 |
| full-frame-cleaning | 9 | 5 | DSX-CODE-020, DSX-CODE-021, DSX-CODE-030, DSX-ML-090 |
| garden-of-forking-paths-p-hacking | 7 | 7 | — |
| interference-shared-budget | 6 | 5 | DSX-INT-010 |
| magnitude-without-computed-effect *(new v2.6 miss)* | 1 | 1 | — |
| operator-known-answer-selective-exclusion | 5 | 5 | — |
| post-hoc-procedure-switch | 8 | 7 | DSX-PRE-030 |
| prescriptive-churn-recommendation | 7 | 4 | DSX-CLM-020, DSX-COH-001, DSX-COH-010 |
| retracted-fabricated-field-experiment | 7 | 7 | — |
| triggering-dilution | 6 | 5 | DSX-INT-030 |
| weak-identification-mmm | 7 | 5 | DSX-INT-030, DSX-VAL-040 |
| **Subtotal (13 families)** | **83** | **69** | |

The remaining **29** fixtures contribute **raw 18 / net 0**: 18 fixtures block exactly their own
target code (raw 1, net 0 — the 12 chart-family CRITICAL/HIGH catches, the four ICC/kappa/weighted-kappa
and two correlation single-code catches, and `subgroup-harm-without-disposition` firing its own
DSX-COH-041), and 11 chart fixtures block nothing at ship (raw 0, net 0). Corpus total: raw
**101**, net **69**, over 42 known-bad fixtures.

</details>

## 5. Limits and honest caveats

- **Small denominators, with explicit bounds.** The ABSENT partition is n=5 and the FPR
  denominator is n=15. For the FPR, 0/15 is **not** evidence of a ~0 false-positive rate: the
  one-sided 95% upper confidence bound is ≈ **0.181** (§3). Do **not** quote a confidence interval
  on the 5/5 miss-rate: per §1 it is a construction invariant of a curated partition, not a
  sample, so an interval on it is meaningless. The point estimates are *floors of representation
  and attribution*, not precise population rates; the corpus is calibrated to be **falsifiable and
  attributable**, not statistically powered.
- **The corpus is not a random sample** of analyses; it is a curated set of known-bad archetypes
  plus a curated clean control set. The rates describe behaviour on these archetypes, not a base
  rate.
- **0.0 FPR is a clean-by-construction result** on 15 specs the harness itself certifies as clean;
  it bounds false positives on **minimal, self-contained** well-formed input, narrower than
  "well-formed input in the wild." It bounds, it does not estimate.
- **Zero mint (REQ-P30-03).** This readout records the terminal re-baseline against the existing
  catalogue; the authoritative set-identity gate (279 → 279, added={} removed={}) runs in plan
  30-02. No finding code was minted, and no frozen surface (`dsx/`, `examples/`, `references/`)
  changed during measurement — the companion is read-only and off the gate path (verified: `git
  status --porcelain` clean on those trees after the run).

---

## 6. Statistician adversarial review

**PENDING — to be completed at S6-3/S6-4 (RECORD-WITH-AMENDMENTS gate).** Per GA-1, the adversarial
`dsx-statistician` review lands here, against the measured numbers above (the 12-READOUT precedent:
the review sharpens framing/honesty, and no measured number changes). This section is a marked
placeholder until that review runs.
