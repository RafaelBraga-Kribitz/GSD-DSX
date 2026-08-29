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

## Milestone: v2.2 — Analytic Surface

**Shipped:** 2026-08-29
**Phases:** 4 (13, 14, 15, 16) | **Plans:** 20

### What Was Built

The operator-surface layer that sits alongside the validity frame rather than
inside it: four router skills (`dsx-cohort`, `dsx-funnel`, `dsx-root-cause`,
`dsx-segment`) that fill `ANALYSIS-SPEC.yaml` fields against existing gates
instead of restating them; a compounding-learnings search step and a portable
`DATA-DICTIONARY.md` onboarding artifact; CUPED as a declared, gated variance
adjustment with a post-treatment-covariate check (`DSX-EXP-070`, CRITICAL) and
a changing-denominator BI check (`DSX-MET-021`, HIGH), both cited to their
primary sources under full D-05 discipline; and off-gate-path re-run
verification via the new `dsx-reproduce` skill (`DSX-REP-060`/`061`, both
HIGH). Finding catalogue: 256 → 260 codes, additive, frozen Phase-12 snapshot
unmutated.

### What Worked

- **Deliberate phase ordering (13 → 14 → 16 → 15, not numeric).** Phase 15 —
  the only phase minting codes with a D-05 human-read gate — ran last, so its
  citation evidence pack (HQ-8) could be filed early and answered
  asynchronously while the other three phases built without waiting on it.
- **Direct primary-source reads over bibliographic corroboration.** For HQ-8,
  the interactive session downloaded and read all three candidate citations
  directly rather than stopping at a corroboration pack. This caught a
  web-search summary that misattributed CUPED's authors, and correctly
  determined the survivorship-bias source does not transfer to the needed
  rule — an honest non-promotion instead of a stretched citation.
- **Set-identity diffs, not counts, for zero-mint proof (D-07).** Phase 13's
  and 14's "no new codes" claims were asserted by comparing the distinct code
  *set* against the Phase 12 snapshot, closing the mint-one/drop-one swap hole
  a count invariant alone leaves open.
- **Persona rounds for D-06 numbering, human veto window for the record.**
  Architect/Statistician/Auditor rounds decided severities and numbering
  (`DSX-MET-021` HIGH not CRITICAL; `DSX-REP-060/061` banded in a fresh `06x`
  block) with full rationale recorded before the operator's veto window
  opened — no numbering decision waited idle for a human who had nothing to
  add.

### What Was Inefficient

- **Framework-CLI blind spots kept recurring.** Three distinct, unrelated GSD
  Core CLI quirks were caught and had to be hand-verified around this
  milestone: `/gsd-audit-uat`'s heading-level mismatch (carried from v2.0.0),
  a stray gitignored `DECISIONS.jsonl` false-failing two `explain` tests from
  an un-isolated CWD, and `init.manager`'s `verification_status` reading
  `missing` for every phase because this repo names its file `NN-VALIDATION.md`
  rather than the framework's generic `VERIFICATION.md`. None were real gaps;
  all needed a direct, by-hand cross-check against the actual phase artifacts
  before being safely dismissed.
- **`/gsd-complete-milestone`'s branch auto-detection is unsafe on this repo.**
  Its `handle_branches` step picks "the milestone branch" as the alphabetically
  first `gsd/*` branch — with four stale `gsd/*` branches left over from prior
  milestones, that would have silently merged the wrong one. Caught before
  running it; shipped by an explicit, named `git merge --no-ff`, verified on a
  throwaway branch first.
- **Generated MILESTONES.md/traceability content needed hand correction.**
  `gsd-tools.cjs`'s accomplishment extraction truncated several one-liners
  mid-sentence, and the archived `v2.2-REQUIREMENTS.md` carried all 23 rows
  forward still reading `[ ]`/"(queued)" despite the milestone actually
  shipping — both are copy/archival artifacts, not content defects, but both
  needed a human pass before the record was portfolio-accurate.

### Patterns Established

- **Loop-prepared evidence is never a substitute for the human D-05 read.**
  HQ-8 stayed explicitly unsigned by the loop even after it corroborated every
  citation across independent sources — the operator's own read at the
  locator is what binds.
- **Batch end-of-phase human items, don't drip them.** Each phase's security
  sign-off + UAT confirmation was filed as one HUMAN-QUEUE item (HQ-9/10/12/14)
  rather than as separate security and UAT items, halving the operator's
  round-trips without losing which artifact each verdict landed in.
- **A loop firing can file the ship-approval item itself.** Once the queue
  drained, an autonomous firing recognized the close-out stage was reached and
  filed HQ-15 (merge/tag/archival approval) with a fully-reasoned recommended
  path — the operator's decision was a single "ship it," not a design session.

### Key Lessons

- A framework default (branch auto-detection, a generic CLI query) is scoped
  to the common case; a repo with real history (stale branches, a
  project-specific file-naming convention) needs its own explicit override,
  verified against actual repo state before trusting the default.
- Reading the primary source yourself is not optional even when a
  corroboration pack already looks solid — the CUPED author misattribution
  would have shipped as a citation error if the interactive session had
  stopped at the corroboration step.
- An honest "this doesn't transfer" is worth more than a citation that merely
  looks close enough — REQ-P15-04 shipped as a documented partial rather than
  a stretched full satisfaction.

### Process Observations

- Delivered by the same scheduled headless completion ceremony as v2.0.0, with
  two additions: a knowledge-graph primer (`graphify`, code-only, zero LLM
  cost) to cut blind codebase exploration, and a tighter ~15-minute poll /
  ~12-minute per-firing pacing cap after v2.0.0 measured a 9% duty cycle under
  the original 4-hour poll interval.
- The final close-out steps (HUMAN-QUEUE drain, `/gsd-complete-milestone`,
  merge + tag) were run in an interactive session rather than a headless
  firing — `/gsd-complete-milestone` has genuine interactive prompts (readiness
  confirm, incomplete-requirements proceed/abort, branch-merge choice) that a
  headless firing correctly refused to self-approve.

## Cross-Milestone Trends

| Milestone | Phases | Plans | Shipped |
|-----------|--------|-------|---------|
| v1.1.0–v1.5.0 | 5 | — | (incremental) |
| v2.0.0 DSX Validity Frame | 11 | 89 | 2026-08-28 |
| v2.2 Analytic Surface | 4 | 20 | 2026-08-29 |
