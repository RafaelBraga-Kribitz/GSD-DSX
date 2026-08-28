# Retrospective: gsd-dsx

A living retrospective, appended at each milestone close.

## Milestone: v2.0.0 — DSX Validity Frame

**Shipped:** 2026-08-28
**Phases:** 11 (6, 7, 8, 9, 10, 11, 11.1, 11.1.1, 11.2, 11.3, 12) | **Plans:** 89 | **Tasks:** 208

### What Was Built

The validity layer beneath every prior DSX check. `ANALYSIS-SPEC.yaml` gained a
`validity_frame:` block and a paradigm-aware `inference:` block, both enforced from
the `plan` gate point. New finding families shipped: `DSX-VAL-*` (estimand, unit
triad, dependence, identification strength, sampling frame, missingness, measurement),
`DSX-INT-*` (interference/SUTVA, triggered-vs-eligible dilution, novelty/primacy),
`DSX-PAR-*` (paradigm manifest + the symmetric monitoring pair), `DSX-PRE-*`
(pre-registered inference plan, declared-vs-executed branch reconciliation blocking
on branch identity alone), `DSX-ADM-*` (frequentist procedure admissibility over
`references/families.yaml`, 14 cited families), the prescriptive-claim layer
(`DSX-CLM-*` / `DSX-COH-040`), and reporting-completeness / missing-data discipline.
A stdlib-only decision-record side channel (`dsx/decisions.py` + `dsx explain`) and a
calibration corpus with a measured catch rate and false-positive rate (`dsx stats
--paradigm`) closed the milestone. Finding catalogue: 256 codes.

### What Worked

- **Contract-then-check sequencing.** Phase 6 landed the contract surface, decision
  record, and D-05 citation enforcement before any `DSX-VAL/INT/PAR` check read the
  new fields — every later check had a stable target.
- **Symmetric pairs as a scoping rule (D-12).** Paradigm-specific checks shipped in
  frequentist/Bayesian pairs at identical severity, which structurally prevents the
  tool from steering method choice.
- **Determinism doctrine held (D-01/D-02).** Gates never read live data; they check
  declarations and hermetic artifacts, so every gate stayed reproducible.
- **D-05 automated at M1.** `gen-finding-catalogue.py --check` fails the build on a
  missing citation/reference-value/linked-test — the one constraint velocity pressure
  would have removed was made unremovable.

### What Was Inefficient

- **Documentation lag against reality.** Traceability rows, VERIFICATION frontmatter,
  and ROADMAP checkboxes repeatedly trailed the code; the S0 hygiene stage and the S4
  audit both had to reconcile "ledger claim vs repo fact." Single-writer tracking and
  earlier reconciliation would have cut this.
- **Inserted phases (11.1, 11.1.1, 11.2, 11.3).** Paper-evaluation integration and
  detection-code hardening arrived outside the original brief §6 milestone map,
  stretching the phase count from 7 to 11.

### Patterns Established

- **Reversal records (D-14).** `REVERSALS.md` with a four-field template; REV-001 and
  REV-002 exercised it. Evidence-free reversals log as `SELF-001`.
- **Entry conditions, not wishes (D-13).** Deferred checks carry a falsifiable trigger
  tied to a measured catch rate; the §6.5 gated backlog was re-evaluated against real
  calibration numbers at Phase 12 (carry 8, remove 1).
- **Extractable boundary (D-03a).** `dsx/frame/` imports only `Report`/`Finding` from
  `dsx/checks/`, AST-enforced by a test.

### Key Lessons

- Land the contract and its enforcement before the checks that depend on it.
- A finding code is a permanent public interface (D-06); reuse an existing code before
  minting a new one, and record every mint loudly.
- The gate checks declarations against declarations — **a frame that lies still
  passes.** The insurance is still a domain human reading the frame before the data is
  touched; the milestone's value is making that review cheap, structured, and routine.

### Process Observations

- Delivered by a scheduled headless completion ceremony: one fresh process per work
  unit, state persisted only in `.planning/` files, GSD's own per-phase state files as
  the resumable memory. Model routing per the ceremony brief (haiku for mechanical doc
  fixes, sonnet-class for execution, opus/fable for planning, verification, adversarial
  statistical review, and the milestone audit).

## Cross-Milestone Trends

| Milestone | Phases | Plans | Shipped |
|-----------|--------|-------|---------|
| v1.1.0–v1.5.0 | 5 | — | (incremental) |
| v2.0.0 DSX Validity Frame | 11 | 89 | 2026-08-28 |
