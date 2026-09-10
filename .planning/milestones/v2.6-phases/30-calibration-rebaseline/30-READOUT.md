---
phase: 30
artifact: calibration-readout
requirement: REQ-P30-01 (terminal calibration re-baseline), REQ-P30-03 (zero-mint context)
status: recorded
measured: 2026-09-10
reproducing_gate: python -m unittest tests.test_known_bad_corpus.TestKnownBadCorpus.test_stratified_catch_rate_and_fpr_report
statistician_review: complete (S6-4, 2026-09-10) — RECORD-WITH-AMENDMENTS, F1/F2 applied, F3–F7 held; no measured number changed. See §6.
---

# Phase 30 — Calibration re-baseline (terminal) — readout

**Status: RECORDED (numbers measured LIVE 2026-09-10); adversarial Statistician review COMPLETE — see §6.**
Per GA-1 (`30-CONTEXT.md §1`, the Phase-24 / 12-READOUT precedent), the heavy adversarial
Statistician review is part of *this readout*, deferred to the readout recording (S6-4,
RECORD-WITH-AMENDMENTS gate) where it can bite on measured output — not the pre-measurement
discuss. It ran at S6-4 (verdict RECORD-WITH-AMENDMENTS, F1/F2 applied below, F3–F7 held); §6
records it. No amendment changed a measured number.

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
specific §6.5 capability that would move it. **This ceiling is about instantiation *shape*, not
capability-in-principle (Statistician §6, F2).** Four of the five misses are caught by their nearest
shipped code in the *declared* form of the defect and miss only in the undisclosed / misdeclared
shape: `DSX-ML-034` fires on a *declared* post-prediction feature, `DSX-CLM-034` on a claim whose
cited test does not trace, `DSX-EXP-051` on a declared forking path, `DSX-VAL-080` on a declared
exclusion. Only `retracted-fabricated-field-experiment` (`DSX-REP-020`) is uncatchable **regardless
of authoring** — a declaration-integrity gate cannot detect fabricated source data. So 5/5 is a
ceiling on *undisclosed* instantiations, not a claim that these defects are intrinsically
undetectable. The two numbers together — **PRESENT 10/10 caught,
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
target code (raw 1, net 0 — the 12 chart-family CRITICAL/HIGH catches, the three ICC/kappa/weighted-kappa
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

Reviewer: `dsx-statistician` persona, opus, high effort (LOOP-BRIEF §3/§4), run at S6-4 against the
measured numbers above. Verdict: **RECORD-WITH-AMENDMENTS** (seven findings F1–F7). The orchestrator
independently re-verified every load-bearing claim against the live tree before folding these in
(brief §5): **F1 and F2 were applied; F3–F6 were held sound as the reviewer found them; F7 was held
sound with a note and NOT applied.** No amendment changed a measured number — each sharpened framing
or honesty. The reproducing gate `test_stratified_catch_rate_and_fpr_report` is green (7.6s), and
every headline/subtotal was re-derived live by both the reviewer and the orchestrator. The full
review is `.planning/phases/30-calibration-rebaseline/30-STATS-REVIEW.md`.

### 6.1 Reviewer findings (summary)

Verdict **RECORD-WITH-AMENDMENTS** — not BLOCK (arithmetic reproduces, the reproducing gate passes,
the load-bearing miss-vs-catch polarity is correct) and not RECORD-AS-IS (two characterisations would
otherwise mislead the durable record).

- **F1 — §4 miscounted the reliability family.** The §4 enumeration of the 18 own-target-only fixtures
  read "the **four** ICC/kappa/weighted-kappa … and two correlation single-code catches", which sums
  12 + 4 + 2 + 1 = **19**, contradicting the stated 18. The reliability family has **three** fixtures.
  → reword "four" → "three". Prose only; 18/83/69/101/74 all still reconcile. **Applied (§4).**
- **F2 — §2c dropped the shape-contingent distinction (Phase-12 F2).** The two new v2.6 misses are
  silent because nothing is *declared*, not because they are uncatchable regardless of authoring; four
  of the five misses are caught in their declared form and only `retracted-fabricated` is uncatchable
  regardless. → add the distinction to §2c so 5/5 is not read as intrinsic undetectability.
  **Applied (§2c).**
- **F3 — miss-rate 1.0 = 5/5 is a construction invariant**, not a sampled rate; growing the partition
  3 → 5 only adds two per-case silence confirmations and quotes no CI. → **Held sound** (framing in §1
  correct and complete).
- **F4 — FPR 0/15 upper bound** re-derived: Clopper-Pearson `1 − 0.05^(1/15) = 0.18104 ≈ 0.181`,
  rule-of-three `3/15 = 0.20`; "a true rate as high as ~1-in-5 is consistent with 0/15" is honest; the
  12 → 15 denominator move tightened the bound 0.221 → 0.181. → **Held sound** (§3, §5).
- **F5 — friction RAW/NET is honest**: the per-cell rate fell 6.0 → 1.36 only because non-target
  in-profile cells grew 13 → 74; absolute net over-block actually *rose* (≈64 → 69). RAW-and-NET
  disclosure is the right anti-laundering guard; subtotals reconcile. → **Held sound** (§4, subject to
  the F1 reword).
- **F6 — PRESENT 10/10** with DSX-COH-041 counted once (at its `plan` cell — the PRESENT axis is
  `("plan","execute")` and coherence is absent from `execute`) is a conservative, non-inflating
  choice; the full plan/verify/ship profile is a non-denominator supplement. → **Held sound** (§2a).
- **F7 — §5 clean-by-construction caveat** omits the Phase-12 "no sibling artifacts → avoids
  fresh-tempdir incidental codes" mechanism clause. → optional add-caveat, **not a defect**.

### 6.2 Orchestrator adjudication (brief §5 — persona claims independently re-verified)

- **F1 CONFIRMED and applied.** A live glob of `examples/known-bad/*-ANALYSIS-SPEC.yaml` shows exactly
  **three** reliability fixtures (`icc-incomplete-triple`, `kappa-missing-companions`,
  `weighted-kappa-missing-weights`) and **two** correlation-agreement fixtures
  (`correlation-for-agreement-estimand`, `correlation-pearson-ordinal-scale`;
  `chart-correlation-drawn-as-line` is a chart fixture, not counted here). The enumeration
  12 chart + 3 reliability + 2 correlation + 1 subgroup-harm = **18** now equals the stated 18
  own-target-only fixtures, and 12 chart own-target + 11 chart clean-at-ship = 23 total chart fixtures
  also reconciles. §4 reworded; no measured number changed.
- **F2 CONFIRMED and applied.** Re-checked against the shipped designs: `DSX-ML-034`
  (`feature-origin-only-leak`) and `DSX-CLM-034` (`magnitude-without-computed-effect`) are silent only
  for want of a `feature_provenance` / `supported_by` declaration (Phases 27/28, attribution-not-
  detection by design), and the Phase-12 F2 precedent already established that
  `garden-of-forking-paths` (`DSX-EXP-051`) and `operator-known-answer` (`DSX-VAL-080`) miss only in
  their undisclosed shape while `retracted-fabricated` (`DSX-REP-020`) is uncatchable regardless. The
  §2c sentence is grounded, not a softening.
- **F3–F6 CONFIRMED and held.** F4's bound re-computed independently (`1 − 0.05^(1/15) = 0.18104`;
  `3/15 = 0.20`); the friction subtotals reconciled (13 families raw 83 / net 69; 29 others raw 18 /
  net 0; corpus raw 101 / net 69 over 74 non-target in-profile cells → 1.36 / 0.93); F5's absolute-rose
  observation is consistent with the §4 framing, which already states the rate fell because the
  denominator grew, "not because the over-block shrank".
- **F7 held sound, NOT applied (loud §5 note, not a silent drop).** The Phase-12 mechanism clause is
  already carried by §5's "bounds false positives on **minimal, self-contained** well-formed input";
  adding a second clause buys no honesty the reader lacks, and the brief prefers the smaller provable
  claim. Recorded here rather than applied.

**Outcome: readout RECORDED.** Reproducing gate `test_stratified_catch_rate_and_fpr_report` green;
every number re-computed live this firing; framing amended per F1–F2, F3–F7 held. No measured number
changed.
