---
phase: 12
artifact: calibration-readout
requirement: REQ-P12-03 (catch rate + false-positive rate), REQ-P12-04 (paradigm split), REQ-P12-02 (friction)
status: recorded
measured: 2026-08-27
reproducing_gate: python -m unittest tests.test_known_bad_corpus.TestKnownBadCorpus.test_stratified_catch_rate_and_fpr_report
statistician_review: complete — RECORD-WITH-AMENDMENTS (dsx-statistician, opus/high, 2026-08-27); F1–F3/F5/F6 applied, F4 corrected on independent re-check (see §8.2)
---

# Phase 12 — Calibration readout (catch rate, false-positive rate, paradigm split, friction)

**Status: RECORDED — Statistician adversarial review complete (LOOP-BRIEF §S3 / §3 high effort); see §8.**
Amendments from that review (F1–F3, F5, F6) are folded into the sections below; F4 was independently
re-checked and corrected (§8.2). No measured number changed — the review sharpened framing and honesty,
not arithmetic.
Every number below is computed **LIVE** by the S3-3 harness (`tests/test_known_bad_corpus.py`)
via `_gate_findings` (a real `dsx gate <point>` in a fresh tempdir) and `_classify_target_defect`
— never lifted from the stale `_INCIDENTAL_GAP_CODES` / `_GOLDEN_SHIP_FINDINGS` ledgers (D-09).
The reproducing gate is the frontmatter test; it asserts exactly these partitions and floors.
Measurement extracted by re-running the harness functions read-only over the live corpus via
`.planning/phases/12-calibration/_measure_readout.py` (a read-only companion committed alongside this
readout; the unittest `test_stratified_catch_rate_and_fpr_report` remains the durable reproducer of
record).

## 1. Headline — the pair (miss-rate, false-positive-rate)

| Quantity | Value |
|---|---|
| **Miss-rate** (ABSENT partition) | **1.0** = 3 / 3 |
| **False-positive rate** (good-control corpus) | **0.0** = 0 / 12 |

The headline is deliberately the **pair (miss-rate, FPR)**, not catch-rate alone (D-10). Every
target-**present** fixture carries a present-and-firing code, so a single catch-rate headline would
be a regression-pin dressed as detection — adding already-caught cases drives it toward 100% for
free. The ABSENT/miss partition is **floored at 3** (`_ABSENT_PARTITION_FLOOR`, met exactly: 3 ≥ 3),
and an **invariance proof** in the gate confirms that injecting a synthetic target-present case
leaves the headline byte-identical.

**On reading the miss-rate as a "rate" (Statistician §8, F3).** The ABSENT partition is *curated* to be
misses — each sidecar is `kind: miss` and each case was confirmed to miss before inclusion — so within
any passing run the miss-rate is 1.0 by construction of the partition; it carries no sampling
information about a miss *propensity*. The evidential content is not the aggregate 1.0 but the **three
independent per-case `fires_at_any_severity: false` confirmations** in §2b: that each named shipped code
is genuinely silent everywhere, not merely below the CRITICAL threshold. Read 1.0 as "all three curated
misses reproduce as misses," not as an estimated population rate.

## 2. Catch rate — stratified PRESENT vs ABSENT (D-10)

### 2a. PRESENT partition — 9 / 9 caught (100%)

Every (fixture × gate-point) cell the effective target map expects to fire a code, live-verified as
firing that code CRITICAL:

| Fixture | Point | Expected code(s) | Result |
|---|---|---|---|
| bayesian-continuous-monitoring | plan | DSX-PAR-011 | CAUGHT |
| bayesian-continuous-monitoring | execute | DSX-PAR-011 | CAUGHT |
| frequentist-uncontrolled-continuous | plan | DSX-PAR-010 | CAUGHT |
| frequentist-uncontrolled-continuous | execute | DSX-PAR-010 | CAUGHT |
| full-frame-cleaning | execute | DSX-CODE-020, DSX-CODE-021, DSX-CODE-030 | CAUGHT |
| interference-shared-budget | plan | DSX-INT-010 | CAUGHT |
| prescriptive-churn-recommendation | plan | DSX-COH-001, DSX-COH-010 | CAUGHT |
| triggering-dilution | plan | DSX-INT-030 | CAUGHT |
| weak-identification-mmm | plan | DSX-VAL-040 | CAUGHT |

**PRESENT catch rate = 9/9 = 100%.** This is what dsx *claims* to catch; on the cells it claims,
it catches everything, at CRITICAL, reproducibly.

### 2b. ABSENT partition — 3 / 3 missed (100% miss-rate)

The three Phase-12 miss cases: each carries a `<slug>-ATTRIBUTION.yaml` sidecar. Its `absent_code` field
names the **nearest shipped catalogue code** that stays silent on this fixture — the sidecar comments
say so explicitly ("absent_code REFERENCES an existing shipped catalogue code", D-18: no code is minted
here). What is *absent* is not the code but the **capability** to catch the defect in its undeclared /
misdeclared / fabricated instantiation — the §6.5 backlog item each sidecar promotes (Statistician §8,
F1). The harness confirms each named code is silent at CRITICAL across all four gate points.

| Fixture | Nearest silent code (shipped) | Promotes §6.5 item | Missed at CRITICAL | **Fires at ANY severity, anywhere** |
|---|---|---|---|---|
| garden-of-forking-paths-p-hacking | DSX-EXP-051 | item 1 (specification sensitivity) | yes | **no** |
| operator-known-answer-selective-exclusion | DSX-VAL-080 | item 1 (specification sensitivity) | yes | **no** |
| retracted-fabricated-field-experiment | DSX-REP-020 | item 7 (feature provenance) | yes | **no** |

**These are genuine misses, not lens artifacts.** The S3-3 Wave-3 log flagged the open question for
this readout: *DSX-VAL-080 now exists (minted in Phase 11.3) — is `operator-known-answer` a genuine
miss, or a HIGH-severity catch that the corpus's CRITICAL-only miss-lens is hiding?* This firing
measured each absent code at **every** severity (not only CRITICAL) across all four gate points:
**none of the three fires at any severity, anywhere** (`fires_at_any_severity: false` for all three).
DSX-VAL-080 does not fire even at HIGH — because the fixture's exclusion is **undeclared**, and
DSX-VAL-080 fires on a *declared* exclusion lacking justification, so it has no declared exclusion to
fire on. The miss is structural (a declaration-only gate cannot catch an undeclared choice), not a
severity-threshold hidden catch. **The S3-3 flag is resolved: the 1.0 miss-rate is honest.**

### 2c. Why a 100% miss-rate on the ABSENT partition is the intended, honest result

The ABSENT partition is the set of defects instantiated in the **undeclared / misdeclared / fabricated
shape a declaration gate cannot see**: p-hacking reported as a single comparison, an *undeclared*
selective exclusion, and fabricated data behind a plausible declaration. dsx is a
*declaration-integrity* gate, not a data-forensics or replication engine.

An honest distinction the Statistician review forced into this section (§8, F2): **only
retracted-fabricated is uncatchable regardless of how it is authored** — no declaration gate can detect
fabricated data behind a valid declaration. The other two are **fixture-shape-contingent**: the shipped
codes DO catch their *declared* forms (a declared exclusion lacking justification fires DSX-VAL-080; a
disclosed `comparisons_looked_at` exceeding the reported test count fires DSX-EXP-051). They miss here
because these fixtures author the defect in its *undisclosed* form — which is the realistic archetype
(p-hacking and operator selective-exclusion are hidden by nature) and which a declaration gate genuinely
cannot catch, but the ceiling is precisely "undisclosed / fabricated instantiation," not "this class of
defect entirely." A 100% miss-rate here is therefore not a detection regression — it measures the
**known ceiling on undisclosed / fabricated instantiations**, each attributed to the specific §6.5
capability that would move it. The two numbers together — PRESENT 9/9 caught, ABSENT 3/3 missed — say:
*dsx catches everything it claims, and the corpus documents, attributably, exactly the undisclosed /
fabricated shapes it does not claim to catch.*

## 3. False-positive rate — good-control corpus (D-04)

**FPR = 0 / 12 = 0.0.** Twelve genuinely clean ANALYSIS-SPECs under `examples/good-corpus/`
(6 frequentist / 6 Bayesian, spanning proportion / continuous / count outcomes) gated at ship;
**none** produced a real false-positive blocking finding after excluding the documented tempdir-noise
codes (`_FPR_TEMPDIR_NOISE_CODES` — file-path `where`, not statistical-validity concepts, D-04).
The denominator (12) gives the rate resolution; the prior n=1 baseline could only report 0/1 or 1/1.

## 4. Friction — per-family over-blocking (REQ-P12-02, D-11)

Friction is the over-blocking BEYOND each fixture's intended catch, reported **RAW and NET** (net-only
is a laundering hole), as a per-cell rate over the non-target in-profile (fixture × gate-point) cells.

| Corpus total | Value |
|---|---|
| Raw ship-blocking findings | 78 |
| Net (raw − own-target) | 64 |
| Non-target in-profile cells | 13 |
| **Raw friction rate** | **6.0** per cell |
| **Net friction rate** | **4.92** per cell |

The over-block is dominated by four incidental codes that fire on almost every fixture in a fresh
tempdir — `DSX-CLM-031` (evidence sibling absent), `DSX-MET-040`, `DSX-NAR-001` (narrative artifact
absent), `DSX-REP-030` — the documented incidental corpus gaps (`_INCIDENTAL_GAP_CODES`). The friction
column exists to keep this over-block **visible** (RAW), not to hide it (NET). The three new miss
fixtures show `own = []` (they are miss cases, so raw == net): garden-of-forking-paths 7/7,
operator-known-answer 5/5, retracted-fabricated 7/7.

**Cross-check against the FPR exclusion (Statistician §8, F4 — independently re-checked and corrected).**
The review argued the friction-dominant codes are "the same tempdir artifacts §3 excludes from FPR,"
implying the ~6/cell rate is inflated ~3× by codes the FPR drops. On independent re-check of the two
code sets this is **not** so: `_FPR_TEMPDIR_NOISE_CODES` = {DSX-DQ-001, DSX-CLM-031, DSX-FIG-001,
DSX-NAR-010}; the four friction-dominant codes = {DSX-CLM-031, DSX-MET-040, DSX-NAR-001, DSX-REP-030}.
Exactly **one** code (DSX-CLM-031) is in both. The other three friction-dominant codes are documented
*incidental corpus gaps* (`_INCIDENTAL_GAP_CODES`), not the file-path tempdir-noise the FPR excludes —
and this section already discloses that the over-block is dominated by incidental codes. So the RAW/NET
disclosure stands as-is and the reviewer's proposed "~2 semantic over-blocks/cell" figure is withdrawn
(it rested on an overstated overlap). The honest statement remains: friction is ~5–6 blocking findings
per non-target cell, dominated by incidental (not statistical-over-reach) codes, shown RAW so it stays
visible.

<details><summary>Per-family raw/net</summary>

| Fixture | Raw | Net | Own-target codes |
|---|---|---|---|
| bayesian-continuous-monitoring | 9 | 8 | DSX-PAR-011 |
| frequentist-uncontrolled-continuous | 7 | 6 | DSX-PAR-010 |
| full-frame-cleaning | 9 | 5 | DSX-CODE-020/021/030, DSX-ML-090 |
| garden-of-forking-paths-p-hacking | 7 | 7 | — |
| interference-shared-budget | 6 | 5 | DSX-INT-010 |
| operator-known-answer-selective-exclusion | 5 | 5 | — |
| post-hoc-procedure-switch | 8 | 7 | DSX-PRE-030 |
| prescriptive-churn-recommendation | 7 | 4 | DSX-CLM-020, DSX-COH-001, DSX-COH-010 |
| retracted-fabricated-field-experiment | 7 | 7 | — |
| triggering-dilution | 6 | 5 | DSX-INT-030 |
| weak-identification-mmm | 7 | 5 | DSX-INT-030, DSX-VAL-040 |

</details>

## 5. Paradigm split — `dsx stats --paradigm` (REQ-P12-04, D-13/D-14)

```
$ dsx stats --paradigm --root .planning
dsx: no operator history yet — no operator decision trails found under
'.planning' (examples/ and templates/ excluded).
(exit 0)
```

The operator's real `.planning/` decision trails hold **no persisted `frame_digest` frames** (this is
the milestone-ceremony repository, not an analytical project on which `dsx gate` has been run against
real work). The polluted `examples/known-bad/DECISIONS.jsonl` floor (~45.8% raw-Bayesian) is
hard-excluded by path (D-13), so it cannot invert the instrument. **§6.5 item 4** (Bayesian > 15%
→ promote Bayesian admissibility) is therefore **NOT promoted** — but the honest reason (Statistician
§8, F5) is that the split is **0/0, undefined**: with zero frames there is no denominator, so item 4's
">15%" condition is **untestable here**, not measured-below-threshold. Item 4 is carried as
prerequisite-pending. Absence of operator Bayesian history is not evidence of a sub-15% Bayesian share;
the number says only that the instrument has nothing to promote on when the operator has run no gated
work, as CONTEXT D-15 anticipated.

## 6. §6.5 linkage (measured evidence for REQ-P12-05, already applied in 12-07)

- The two `item 1` miss cases (DSX-EXP-051, DSX-VAL-080 absent) are the measured "absence permitted a
  false pass" evidence for §6.5 item 1 — but item 1's frequentist specification-sensitivity mirror is
  unwritten (D-12a), so a corpus count cannot promote it: **carried**.
- The `item 7` miss case (retracted-fabricated) is the honestly-flagged least-bad fit for feature
  provenance: **carried**.
- Item 4 (Bayesian > 15%): empty split → **not promoted / carried** (this readout, §5).
- These dispositions were already recorded in `12-07-SUMMARY.md` / `brief.md` §6.5; this readout
  supplies the measured numbers behind them.

## 7. Limits and honest caveats (for Statistician review)

- **Small denominators, with explicit bounds (Statistician §8, F6).** The ABSENT partition is n=3 and
  the FPR denominator is n=12. For the FPR, 0/12 is **not** evidence of a ~0 false-positive rate: the
  one-sided 95% upper confidence bound is ≈**0.22** (Clopper-Pearson `1 − 0.05^(1/12)` ≈ 0.221;
  rule-of-three ≈ 3/12 = 0.25) — a true false-positive rate as high as ~1-in-4 on well-formed input is
  fully consistent with observing 0/12. Do **not** quote a confidence interval on the 3/3 miss-rate:
  per §1/§8-F3 it is a construction invariant of a curated partition, not a sample, so an interval on
  it is meaningless. The point estimates are *floors of representation and attribution*, not precise
  population rates; the corpus is calibrated to be **falsifiable and attributable**, not statistically
  powered.
- **The corpus is not a random sample** of analyses; it is a curated set of known-bad archetypes plus
  a curated clean control set. The rates describe behaviour on these archetypes, not a base rate.
- **0.0 FPR is a clean-by-construction result** on 12 specs the harness itself certifies as clean; it
  bounds false positives on **minimal, self-contained** well-formed input (the good corpus is authored
  to reference no sibling artifacts, so it also avoids the fresh-tempdir conditions under which dsx's
  incidental codes fire), narrower than "well-formed input in the wild." It bounds, it does not estimate.

---

## 8. Statistician adversarial review

Reviewer: `dsx-statistician` persona, opus, high effort (LOOP-BRIEF §3/§4). Verdict:
**RECORD-WITH-AMENDMENTS** (six findings F1–F6). The orchestrator independently re-verified every
load-bearing claim against the live tree before folding these in (brief §5); F1–F3, F5, F6 were applied
as the reviewer specified, F4 was corrected (§8.2). No amendment changed a measured number — each
sharpened framing or honesty.

### 8.1 Reviewer findings (summary)

**Verdict RECORD-WITH-AMENDMENTS** — not BLOCK (arithmetic reproduces, reproducing gate passes, and the
load-bearing S3-3 flag — "are these genuine misses, or HIGH catches the CRITICAL lens hid?" — is
correctly resolved); not RECORD-AS-IS (four characterisations would mislead the durable record).

- **F1 — the three "absent" codes are shipped, not absent.** DSX-EXP-051 (HIGH, emitter
  `dsx/checks/design.py:466`, catalogue `finding-codes.md:84`), DSX-VAL-080 (HIGH, `dsx/frame/val.py:1358`,
  `:390`), DSX-REP-020 (MEDIUM, `dsx/checks/repro.py:127`, `:300`) all exist. The sidecar `absent_code`
  field references a shipped code that is *silent on this fixture*; what is absent is the *capability*.
  → retitle the §2b column and fix the prose. **Applied.**
- **F2 — "structural ceiling" is overstated for two of three.** Only retracted-fabricated is uncatchable
  regardless of authoring; garden-of-forking-paths and operator-known-answer are caught in their
  *declared* forms by the shipped codes and miss only in the undisclosed shape. → qualify §2c. **Applied.**
- **F3 — miss-rate 1.0 is a construction invariant**, not a sampled rate; the evidence is the three
  per-case `fires_at_any_severity=false` confirmations. → caveat in §1. **Applied.**
- **F4 — the FPR excludes the same codes friction counts** (claimed ~3× inflation). → §4 reconciliation.
  **Corrected, not applied as stated — see §8.2.**
- **F5 — the empty paradigm split is 0/0 undefined, not "<15% by definition."** Item 4 is untestable
  here, not measured-below-threshold. → rewrite §5. **Applied.**
- **F6 — report intervals.** One-sided 95% upper bound on 0/12 FPR ≈ 0.22; no CI on the 3/3 miss-rate.
  → §7. **Applied.**

**Held sound by the reviewer (stands):** the S3-3 flag resolution (DSX-VAL-080 genuinely silent at every
severity on operator-known-answer — the exclusion is undeclared, so a declared-exclusion check has
nothing to bite); the headline-as-pair design with floored ABSENT partition + invariance proof (D-10);
RAW-and-NET friction and the D-13 known-bad exclusion as the right anti-laundering guards; the §7 limits
as far as they went.

### 8.2 Orchestrator adjudication (brief §5 — persona claims independently re-verified)

- **F1 CONFIRMED and applied.** `grep` over `references/finding-codes.md` and `dsx/` confirms all three
  codes are catalogued and emitted at the lines above; each `-ATTRIBUTION.yaml` header comment already
  states "absent_code REFERENCES an existing shipped catalogue code (D-18)." The defect was purely the
  readout's over-literal rendering of the field name — now fixed. No code or fixture changed.
- **F2, F3, F5, F6 CONFIRMED and applied** as specified. F3's mechanism was re-derived precisely (the
  partition is curated to misses via `kind: miss`, so 1.0 reflects curation) rather than copied, and
  F6's 0.22 bound re-computed (`1 − 0.05^(1/12) ≈ 0.221`).
- **F4 CORRECTED — the persona overstated the overlap.** The reviewer claimed ~4 of the ~6 friction
  codes are the tempdir artifacts the FPR excludes. The live code sets show only **one** overlap
  (DSX-CLM-031): `_FPR_TEMPDIR_NOISE_CODES` = {DSX-DQ-001, DSX-CLM-031, DSX-FIG-001, DSX-NAR-010};
  friction-dominant = {DSX-CLM-031, DSX-MET-040, DSX-NAR-001, DSX-REP-030}. The other three dominant
  codes are incidental corpus gaps, not FPR-excluded path-noise, so the proposed "~2 semantic
  over-blocks/cell" figure is withdrawn. §4 now records the true one-code overlap and keeps the RAW/NET
  disclosure the reviewer itself called sound. This is a loud §4 orchestrator override of a persona
  claim, recorded per brief §5.

**Outcome: readout RECORDED.** Reproducing gate `test_stratified_catch_rate_and_fpr_report` green
(2.2s); every number re-computed live this firing; framing amended per F1–F3/F5/F6, F4 corrected.
