---
phase: 30
phase_name: "Calibration re-baseline"
project: "gsd-dsx"
generated: "2026-09-10"
counts:
  decisions: 4
  lessons: 4
  patterns: 4
  surprises: 3
missing_artifacts:
  - "UAT.md"
---

# Phase 30 Learnings: Calibration re-baseline

## Decisions

### GA-1 — Run the persona round inline, defer the adversarial review to the readout
Ran the S6-1 persona round inline (Architect + Statistician), matching the Phase-24 calibration precedent, rather than spawning two parallel opus personas (the pattern the v2.6 evidence phases 25–29 used). The heavy adversarial Statistician review was explicitly deferred to the readout recording (S6-3/S6-4) rather than run pre-measurement, mirroring the 12-READOUT precedent where the review folded into the readout and changed no measured number.

**Rationale:** Phase 30 measures an already-built corpus; it does not design. The classification of every case is already fixed by harness maps the evidence phases committed, so spawning personas to re-derive facts a reproducing unittest already asserts would add wall-clock and mid-unit-compaction risk for no design decision they would actually make. The load-bearing judgement in a calibration readout is framing, not arithmetic — that judgement belongs in an adversarial review against real measured output, not a pre-measurement discuss with nothing yet to review.
**Source:** 30-CONTEXT.md

### GA-2 — Classification of the three v2.6 evidence cases is CONFIRMED live, not re-decided
The corpus-case classification (feature-origin-only-leak and magnitude-without-computed-effect as ABSENT/miss; subgroup-harm-without-disposition as PRESENT/target) was treated as FORCED by the committed harness wiring from Phases 27/28/29. Phase 30's job was to confirm it live, not re-decode it.

**Rationale:** Re-decoding a frozen corpus at the terminal phase would be a D-13 violation (reshaping to a preferred outcome). The consequences (miss partition = 5 ≥ floor 3; headline miss-rate as a construction invariant; PRESENT partition gains one target cell) were to be confirmed at measurement, not argued in advance.
**Source:** 30-CONTEXT.md

### GA-4 — REQ-P30-02 is verify-not-build; close exactly one genuine gap, no more
REQ-P30-02 was treated as a verification requirement, not a build. A plan-time search confirmed no existing test asserted the literature record's corpus counts track the live corpus glob (test_doc_code_agreement covers decision-table/membership only; other candidate tests were unrelated). The gap was closed with exactly one lightweight agreement test (`tests/test_literature_corpus_count_agreement.py`) asserting doc-vs-live agreement, never a hardcoded number, and pinning nothing beyond the row-15 counts.

**Rationale:** Authoring anything beyond the one genuine gap would be speculative test-writing outside the phase's measurement mandate. The test had to assert AGREEMENT rather than a fixed literal because a hardcoded number is exactly what let the doc drift stale (39 vs. live 42) in the first place.
**Source:** 30-CONTEXT.md, 30-02-PLAN.md, 30-02-SUMMARY.md

### FPR and miss-rate must be reported as bounded observations, never point estimates
The readout explicitly reports FPR = 0/15 as a one-sided 95% upper confidence bound (Clopper-Pearson 1 − 0.05^(1/15) ≈ 0.181; rule-of-three ≈ 3/15 = 0.20) rather than as evidence of a near-zero false-positive rate, and explicitly withholds any confidence interval on the 5/5 miss-rate because the ABSENT partition is a curated construction invariant, not a random sample.

**Rationale:** A true false-positive rate as high as roughly 1-in-5 on well-formed input is fully consistent with observing 0/15; reporting a bare "0.0" without the bound would overstate calibration to a sceptical reader. An interval on a construction-invariant rate would be meaningless since the partition is curated to be misses by design (12-READOUT F3 precedent carried forward).
**Source:** 30-READOUT.md, 30-STATS-REVIEW.md

---

## Lessons

### A prose enumeration can silently miscount even when all load-bearing numbers reconcile
The adversarial Statistician review (F1) caught that §4 of the readout said "the four ICC/kappa/weighted-kappa" fixtures when the live corpus has exactly three, making the stated decomposition sum to 19 against a claimed 18. All the actual subtotals (18/83/69/101/74) were correct — only the descriptive word "four" was wrong, caught by re-running a live corpus glob rather than trusting the prose.

**Context:** Found during the S6-4 adversarial review of 30-READOUT.md; confirmed independently by the orchestrator via a live glob before being applied. Demonstrates that even a rigorously measured record needs adversarial re-derivation of its descriptive enumerations, not just its headline numbers.
**Source:** 30-STATS-REVIEW.md, 30-READOUT.md §6

### Dropping a shape-contingent distinction across phases quietly weakens a ceiling claim
The Statistician review (F2) found that §2c of the readout kept the high-level "undeclared / misdeclared / fabricated shape a declaration gate cannot see" framing but dropped the explicit Phase-12 F2 sub-distinction: four of the five misses are catchable in their declared form (fixture-shape-contingent) and only one (retracted-fabricated-field-experiment) is uncatchable regardless of authoring. Without restating it, a reader could wrongly infer all five miss classes are intrinsically undetectable.

**Context:** This mattered more at Phase 30 than at Phase 12 because two of the five misses are new (DSX-ML-034, DSX-CLM-034), both joining the fixture-shape-contingent bucket — so the distinction needed explicit restatement, not just implicit carry-forward via per-case prose.
**Source:** 30-STATS-REVIEW.md, 30-READOUT.md §6

### A per-cell friction rate falling can mask an absolute over-block that rose
Friction fell from 6.0/4.92 (raw/net per cell, Phase 12) to 1.36/0.93 (Phase 30) — but the Statistician review confirmed (F5) this fall happened only because the denominator of non-target in-profile cells grew from 13 to 74 as the corpus grew; the absolute net over-block actually rose (64 → 69). The readout was held sound specifically because it reported RAW alongside NET and stated the fall was denominator growth, not over-block shrinkage.

**Context:** This is the D-11 anti-laundering discipline in action — reporting only the improved-looking net-per-cell rate without the raw absolute count would have been a misleading headline.
**Source:** 30-STATS-REVIEW.md, 30-READOUT.md §4

### Conservative asymmetry between catch-axis and miss-axis counting is a defensible, non-inflating choice
The PRESENT partition counts DSX-COH-041 only once, at its `plan` cell (the declared axis), while the ABSENT partition verifies each miss is silent across all four gate points. The Statistician review (F6) noted this asymmetry cuts against inflation, not toward it — misses get a stronger (harder-to-satisfy) silence claim while catches get a weaker (easier-to-satisfy, non-padded) catch claim.

**Context:** Confirms that deliberately asymmetric axis choices between catch and miss counting, when the asymmetry favors the more conservative claim, survive adversarial review rather than needing correction.
**Source:** 30-STATS-REVIEW.md, 30-READOUT.md §2a

---

## Patterns

### Measure-first via a read-only companion script, off the gate path
`_measure_readout.py` was copied forward from the Phase-12 template, adapted only to resolve ROOT correctly from its new location (`parents[3]`, verified live via an assertion rather than assumed) and to add one supplementary read-only block for the new `kind: target` case. It imports the live harness functions from `tests/test_known_bad_corpus.py` and shells `dsx gate <point>` in a fresh tempdir per call — it computes nothing on the gate path and never perturbs the PRESENT/ABSENT partitions (the target block runs in its own loop, after `out["present"]` is finalized, and never touches the `pd`/`pc`/`am`/`ad` partition variables).

**When to use:** Whenever a phase needs to extract and record numbers from an existing, gate-verified measurement harness without adding new gate-path computation or risking corruption of frozen partitions. The companion is explicitly NOT the reproducer of record — the existing unittest remains the durable, independently-asserting gate.
**Source:** 30-01-PLAN.md, 30-01-SUMMARY.md, 30-REVIEW.md

### Agreement tests over hardcoded literals for doc-vs-corpus pinning
`test_literature_corpus_count_agreement` asserts the literature doc's row-15 corpus counts equal `len(glob(...))` against the live corpus directories — never a hardcoded expected number. This is the exact pattern needed to close the REQ-P30-02 gap, because a hardcoded literal is precisely what let the doc drift stale (39 vs. live 42) in the first place.

**When to use:** Whenever a documentation record asserts a fact that is also derivable live from the codebase (a count, a set, a status) — pin the doc to a live derivation, not to a value typed in at authoring time, so future drift fails a gate instead of silently persisting.
**Source:** 30-02-PLAN.md, 30-02-SUMMARY.md, 30-REVIEW.md

### D-13-honest doc rewrites: promote only with code + fixture + measured evidence named
Both doc rewrites (brief.md §6.5 and the literature record) promoted backlog items out of "deferred" status only by naming the specific catalogue code, the fixture, and the measured evidence (LIVE-MISS or TARGET) for each — never on an estimate. The literature doc additionally retitled its "What is deferred" section to "What was deferred, and how it was promoted (D-13)" because a stale present-tense "deferred" header over now-satisfied content would mislead a reader, even though this retitling wasn't explicitly pre-specified.

**When to use:** Whenever a phase promotes a backlog/deferred item to satisfied status based on measured evidence — cite the exact code, fixture, and measurement, and audit surrounding prose (like section headers) for consistency with the new disposition, not just the specific promoted lines.
**Source:** 30-CONTEXT.md, 30-02-SUMMARY.md, 30-REVIEW.md

### Frozen-surface byte-freeze verified via whole-phase git diff, not per-task
The invariant that `dsx/`, `examples/`, and `references/finding-codes.md` stayed byte-identical for the entire phase was verified with a single whole-phase diff (`git diff --stat 03de340^..HEAD -- dsx/ examples/ references/finding-codes.md` / `git diff 03de340^..0c924bb -- ...`) confirmed empty at multiple gates (code review, security, verification) rather than only checked once per task.

**When to use:** When a phase constrains itself to touching zero of a named set of frozen files across multiple tasks/waves, re-verify the invariant with a single cumulative diff at each downstream gate (review, security, verification) rather than trusting an earlier task's local check.
**Source:** 30-REVIEW.md, 30-SECURITY.md, 30-VERIFICATION.md

---

## Surprises

### Zero measured numbers changed despite a RECORD-WITH-AMENDMENTS verdict
The adversarial Statistician review returned RECORD-WITH-AMENDMENTS with seven findings (F1–F7), two of which were applied (F1 reword, F2 add-caveat) — yet neither amendment altered a single measured number. Both were prose/framing fixes: a miscounted enumeration ("four" → "three") and a restored shape-contingent distinction.

**Impact:** Confirms the GA-1 design bet that deferring the adversarial review to the readout (rather than running it pre-measurement) preserves rigor without risking the measured baseline — the review's teeth were entirely in framing/honesty, exactly as the 12-READOUT precedent predicted.
**Source:** 30-STATS-REVIEW.md, 30-READOUT.md §6

### The headline miss-rate is explicitly framed as carrying zero sampling information
The readout states outright that reading 1.0 = 5/5 as a "rate" would be a misreading: because the ABSENT partition is curated so every sidecar is `kind: miss` and each case was confirmed to miss before inclusion, the 1.0 is true by construction and carries no information about a population miss propensity. The evidential content is instead the five independent per-case `fires_at_any_severity: false` confirmations, and no confidence interval is ever quoted on the miss-rate.

**Impact:** This framing choice — treating a would-be headline statistic as explicitly non-statistical — is unusual rigor for a calibration record and is what let the review find zero BLOCK-level defects in a report whose top-line number is, on its face, a suspiciously perfect 100%.
**Source:** 30-READOUT.md §1, 30-CONTEXT.md

### The set-identity zero-mint invariant held exactly 279 → 279 across a phase that promoted three backlog items
Despite promoting three backlog items (7, 8, 9) from deferred to satisfied and rewriting two calibration records, the finding catalogue set-identity stayed exactly 279 → 279 (added={}, removed={}) for the entire phase — the promotions cited only pre-existing codes (DSX-ML-034, DSX-CLM-034, DSX-COH-041) that were minted in the earlier evidence phases (27/28/29), not in Phase 30 itself.

**Impact:** Validates the phase's "measures, does not design" framing operationally: a phase can move three items from deferred to satisfied status in the durable record while minting zero new catalogue surface, because the detection capability was already shipped and Phase 30's job was purely to measure and document it.
**Source:** 30-CONTEXT.md, 30-02-SUMMARY.md, 30-SECURITY.md
