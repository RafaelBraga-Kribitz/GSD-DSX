---
phase: 30
artifact: calibration-readout-statistician-review
reviewer: dsx-statistician (adversarial), opus, high effort
reviewed: 2026-09-10
target: .planning/phases/30-calibration-rebaseline/30-READOUT.md
reproducing_gate: python -m unittest tests.test_known_bad_corpus.TestKnownBadCorpus.test_stratified_catch_rate_and_fpr_report
verdict: RECORD-WITH-AMENDMENTS
findings: F1 reword (miscount) · F2 add-caveat (F2-distinction carry-forward) · F3 hold-sound · F4 hold-sound · F5 hold-sound · F6 hold-sound · F7 optional add-caveat
numbers_changed: 0 (no BLOCK; every measured value reproduced live)
---

# Phase 30 — Calibration re-baseline — Statistician adversarial review (§6 source)

Reviewer: `dsx-statistician` persona, opus, high effort. This review fills the §6
placeholder of `30-READOUT.md`. Per the 12-READOUT precedent (GA-1), the review
sharpens **framing and honesty only** — it changes **no measured number**. Where I
believe a number is wrong that is a BLOCK finding; I raise **none** (all reproduced).
The orchestrator composes §6 from these findings after independently re-verifying each.

## Verdict: RECORD-WITH-AMENDMENTS

- **Not BLOCK.** Every headline and subtotal reproduces live on the real interpreter
  (see "Claims independently confirmed" below). The reproducing gate passes (7.6 s).
- **Not RECORD-AS-IS.** One internal enumeration in §4 miscounts a family (F1), and
  §2c has dropped the explicit Phase-12 F2 distinction that a careful reader is owed
  now that two of the new-in-v2.6 misses are of exactly the *fixture-shape-contingent*
  type that distinction governs (F2). Both are framing fixes; neither touches a number.

## Findings

### F1 — §4 enumeration miscounts the reliability family ("four" → "three"). Reword.

**Locator.** §4, closing paragraph of the `<details>` block (30-READOUT.md ~L199–203):
"18 fixtures block exactly their own target code (raw 1, net 0 — the 12 chart-family …,
**the four ICC/kappa/weighted-kappa** and two correlation single-code catches, and
`subgroup-harm-without-disposition` …)."

**Fact (reproduced).** The live corpus contains exactly **three** reliability-family
single-code fixtures — `icc-incomplete-triple`, `kappa-missing-companions`,
`weighted-kappa-missing-weights` — each raw 1 / net 0 (confirmed against the friction
JSON and an `examples/known-bad/` glob). The stated decomposition therefore sums to
12 + **4** + 2 + 1 = **19**, one more than the "18 own-target-only fixtures" it is
meant to itemise. The correct split is 12 + **3** + 2 + 1 = 18.

**Assessment.** This is a prose miscount, **not** a wrong headline. The load-bearing
subtotals all reconcile and reproduce: 18 own-target-only fixtures (raw 18, net 0),
11 clean-at-ship (raw 0), 29 "others" (raw 18 / net 0), 13 net-over-block families
(raw 83 / net 69), corpus raw 101 / net 69 over 74 cells. Only the parenthetical
word "four" is wrong.

**Action.** Reword §4: "four ICC/kappa/weighted-kappa" → "**three** ICC/kappa/
weighted-kappa". No number changes. (Not a BLOCK — the 18/83/69/101/74 subtotals hold.)

### F2 — §2c dropped the Phase-12 F2 distinction; the two new misses are fixture-shape-contingent, not uncatchable-regardless. Add caveat.

**Locator.** §2c (30-READOUT.md L124–136), and the new-miss prose in §2b (L114–122).

**Fact (reproduced / catalogue-grounded).** `DSX-ML-034` ships as CRITICAL — "Feature
'<…>' is declared available only after the prediction moment" — i.e. it fires on a
*declared* post-prediction feature. `DSX-CLM-034` ships as HIGH — "Claim magnitude does
not trace to its cited test" — i.e. it fires on a claim that *has* a cited `supported_by`
test whose magnitude does not trace. `feature-origin-only-leak` declares no
`feature_provenance` and `magnitude-without-computed-effect` declares no `supported_by`,
so both codes are silent (measured `fires_at_any_severity: false`). Each **would** fire
on its declared-and-bad instantiation.

**Assessment (opinion).** Phase-12's F2 (Applied) forced §2c to distinguish *only*
`retracted-fabricated` as uncatchable regardless of authoring, from the
fixture-shape-contingent cases the shipped codes DO catch in their declared form. The
Phase-30 §2c keeps the high-level, F2-consistent phrase "the undeclared / misdeclared /
fabricated shape a declaration gate cannot see," but **drops the explicit sub-distinction**.
That matters more now, not less: two of the five misses are new, and both
(`feature-origin-only-leak`/DSX-ML-034, `magnitude-without-computed-effect`/DSX-CLM-034)
join `garden-of-forking-paths`/DSX-EXP-051 and `operator-known-answer`/DSX-VAL-080 in the
**fixture-shape-contingent** bucket — leaving `retracted-fabricated`/DSX-REP-020 as the
lone uncatchable-regardless case. Without the distinction a reader can wrongly infer these
defect *classes* are uncatchable, when four of five are only uncatchable in their
*undisclosed* shape. §2b's per-case prose ("no `feature_provenance` declaration to fire on";
"declares no `supported_by`") implies it, but §2c should state it.

**Action.** Add to §2c the Phase-12 F2 sentence, updated for n=5: four of five misses are
fixture-shape-contingent (the shipped code fires on the declared-and-bad form), and only
`retracted-fabricated` is uncatchable regardless of authoring. "Attribution, not detection"
(§2b) is honest and stays; this restores the sharper ceiling. No number changes.

### F3 — Miss-rate 1.0 = 5/5 as a construction invariant is correct and complete. Hold sound.

**Locator.** §1 (L47–58).

**Assessment.** The framing carries Phase-12 F3 forward correctly. The ABSENT partition
is curated to misses (`kind: miss`, each confirmed silent before inclusion), so 1.0 is
true **by construction of the partition** and carries no sampling information about a miss
propensity. Growing 3 → 5 changes nothing about *how* 1.0 is read; it only adds **two more
independent per-case `fires_at_any_severity: false` confirmations** (now five), which
strengthens the evidential base without converting it into an estimated rate. Withholding a
confidence interval is the correct move — an interval on a construction invariant is
meaningless, and the readout says exactly that. "Comfortably at 5 ≥ 3" is mild but fair,
since the floor is a representation minimum, not a power threshold.

**Action.** Hold sound. (No CI to add; the readout already forbids one, correctly.)

### F4 — FPR 0/15 bound arithmetic and the "~1-in-5" claim are honest. Hold sound.

**Locator.** §3 (L146–150); §5 first bullet (L209–215).

**Fact (re-derived independently).** Clopper-Pearson one-sided 95% upper bound on 0/15 =
1 − 0.05^(1/15) = **0.18104** (readout: ≈ 0.181 ✓). Rule-of-three ≈ 3/15 = **0.20** ✓.
For comparison the Phase-12 0/12 bound was 1 − 0.05^(1/12) = 0.22092 (≈ 0.22 ✓), so the
12 → 15 move **tightened** the bound from ~0.221 to ~0.181, as claimed ("improving the rate
resolution").

**Assessment.** "A true false-positive rate as high as roughly 1-in-5 … is fully consistent
with observing 0/15" is honest: the rule-of-three upper bound is exactly 0.20 = 1/5, and the
Clopper-Pearson bound (0.181) is quoted alongside it, so the reader sees both. The readout
insists this is a **bound, not a point estimate** — correct. The denominator move is
characterised correctly ("three good-control specs added since").

**Action.** Hold sound.

### F5 — Friction RAW/NET anti-laundering is honest; the fall is denominator growth, not a shrinking over-block. Hold sound (commend), subject to F1.

**Locator.** §4 (L152–203), esp. the totals table (L158–164) and the causal claim (L166–172).

**Fact (reproduced).** Corpus raw **101** / net **69** over **74** non-target in-profile cells
→ raw **1.36**/cell, net **0.93**/cell (101/74 = 1.3649, 69/74 = 0.9324 ✓). Phase-12 was
raw 78 / net 64 over 13 cells → 6.0 / 4.92. The **absolute** over-block **grew** (raw 78→101,
net 64→69); the per-cell rate fell **only** because cells grew 13 → 74. Subtotals reconcile:
13 families raw 83 / net 69; 29 others raw 18 / net 0; sum raw 101 / net 69.

**Assessment.** This is the correct anti-laundering framing and the readout resists the
tempting-but-false headline ("friction fell from 6.0 to 1.36"). It states plainly that the
over-block did **not** shrink — the denominator grew, mostly with low-blocking chart fixtures
— and keeps the over-block visible via RAW. The dominant incidental codes (`DSX-CLM-031`,
`DSX-MET-040`, `DSX-NAR-001`, `DSX-REP-030`) are named. This is more honest than most
readouts would be.

**Action.** Hold sound. The **only** edit here is F1's "four → three" inside the same section.

### F6 — PRESENT 10/10 and the DSX-COH-041 counting choice are non-inflating. Hold sound.

**Locator.** §2a (L62–95), incl. the target-profile table (L90–95).

**Fact (reproduced).** PRESENT = 10/10. `subgroup-harm-without-disposition` is counted
**once**, at its `plan` cell, within the `(plan, execute)` CRITICAL-threshold axis; coherence
is not registered at `execute`. Its full profile — CRITICAL at plan/verify/ship, silent at
execute — is reported separately in the `out["target"]` block and does **not** enter the
PRESENT denominator (confirmed: the present-cases list contains the plan cell only).

**Assessment.** The "a single catch-rate headline would be a regression-pin dressed as
detection" caveat is honest: every present fixture is authored to carry a firing code, so
catching it is near-tautological, and the readout says so. Counting COH-041 only at `plan` is
the **non-inflating** choice — folding its verify/ship catches into the headline would pad the
denominator. Worth noting in COH-041's favour: the catch/miss axes are deliberately
asymmetric in the conservative direction — misses are verified silent across **all four**
points (a stronger miss claim), while catches are counted only on the **declared** axis (a
weaker catch claim). The asymmetry cuts against inflation, not toward it. The "real DETECTED
catch minted from the paper's own §6 idea" language is provenance, not an over-claim, and sits
inside the same regression-pin caveat as the other nine present catches.

**Action.** Hold sound.

### F7 — §5 clean-by-construction caveat is honest but dropped the Phase-12 mechanism clause. Optional add-caveat.

**Locator.** §5, third bullet (L219–221).

**Assessment (opinion).** §5 as written is honest — "0.0 FPR is a clean-by-construction result
on 15 specs … it bounds false positives on minimal, self-contained well-formed input, narrower
than 'well-formed input in the wild'. It bounds, it does not estimate." I would **not** call
this wrong. Phase-12 §7 carried one extra mechanism clause the Phase-30 §5 drops: the good
corpus "references no sibling artifacts, so it also avoids the fresh-tempdir conditions under
which dsx's incidental codes fire." Restoring it would connect the 0/15 FPR to the very
incidental-code phenomenon that dominates §4 friction (`DSX-MET-040`/`DSX-NAR-001`/`DSX-REP-030`
are **not** in `_FPR_TEMPDIR_NOISE_CODES`, so a good spec that triggered them *would* count as a
false positive — the good specs get 0 partly by dodging those conditions). This is an
enhancement, not a correction.

**Action.** Optional: restore the Phase-12 mechanism clause to §5's third bullet. Not a defect;
skip without loss of correctness.

## Alternative explanations I tested and could not turn into a defect

- **"1.0 miss-rate is a detection regression."** Ruled out: it is a construction invariant of a
  curated `kind: miss` partition; the evidential content is five per-case silences, each
  attributed to a specific §6.5 backlog item. Not a rate.
- **"The friction fall is over-block improvement being laundered."** Ruled out: absolute net
  over-block *rose* (64→69); the readout says so and reports RAW to keep it visible.
- **"COH-041's verify/ship catches inflate the catch headline."** Ruled out: counted once at
  `plan`; full profile is a non-denominator supplement.
- **"0/15 is being read as ~0 FPR."** Ruled out: the readout quotes the one-sided upper bound
  (~0.181 / rule-of-three 0.20) and insists it is a bound.
- **"The catch/miss point-axes are cherry-picked to flatter catches."** Ruled out: the asymmetry
  is conservative (misses checked at all four points; catches only on the declared axis).

## Claims independently confirmed to reproduce (live, `Python312\python.exe`)

Ran the reproducer (`test_stratified_catch_rate_and_fpr_report`, OK, 7.6 s) and the read-only
companion `_measure_readout.py`. Confirmed against live JSON:

- Headline pair: miss-rate **1.0 = 5/5**, FPR **0.0 = 0/15**; ABSENT floor 3, met at 5. ✓
- PRESENT **10/10**, exact cases match §2a incl. the new `subgroup-harm-without-disposition ×
  plan → DSX-COH-041`. ✓
- ABSENT **5/5**, all `fires_at_any_severity: false`, incl. the two new misses DSX-ML-034 /
  DSX-CLM-034, with the promoted §6.5 items 7 and 8. ✓
- Friction raw **101** / net **69** / cells **74** → **1.36** / **0.93** per cell; Phase-12
  6.0 / 4.92 over 13 cells; subtotals 83/69 (13 families), 18/0 (29 others). ✓
- FPR CI re-derived: CP 0.18104 ≈ 0.181; rule-of-three 0.20. Phase-12 0.221 for contrast. ✓
- DSX-COH-041 profile: CRITICAL plan/verify/ship, silent execute. ✓
- DSX-ML-034, DSX-CLM-034, DSX-COH-041 present in `references/finding-codes.md`; both new codes
  are declaration-contingent (grounds F2). ✓
- **Discrepancy found:** §4 says "four ICC/kappa/weighted-kappa"; the live corpus has **three**
  (F1). Prose only — no measured number affected.
