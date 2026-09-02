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

## Milestone: v2.3 — Test Catalog

**Shipped:** 2026-09-02
**Phases:** 4 (17, 18, 19, 20) | **Plans:** 11

### What Was Built

The analyst-facing test-selection surface, expanded as close to exhaustion as
stayed manageable and citable: the `recommend_test` decision table grew from
~15 to ~75 rows across 11 categories (correlation/association, agreement/
reliability, repeated measures, trend, categorical, resampling, variance/scale,
proportions, counts, post-hoc, power conventions), backed by 15 new
declaration-only gate checks (`DSX-STA-050`…`122`, all HIGH) under full D-05
citation discipline. Every check reads declared fields only — the anti-two-stage
doctrine already proven for Shapiro-Wilk was extended structurally to six new
families, including two new NEGATIVE gates (a variance test declared as a
precondition to a location-test choice blocks; observed/post-hoc power declared
in a readout blocks). Finding catalogue: 260 → 275 codes, additive, both frozen
snapshots (Phase-12 at 256, v2.2's set) unmutated.

### What Worked

- **Front-loading the repairs.** Phase 17 fixed the inherited Boschloo doc/code
  divergence and added the missing `estimand_kind` spec vocabulary *before* any
  new gate check was written, so nothing later inherited a known defect.
- **Filing both D-05 evidence packs at bootstrap (S0-3/S0-4), before Phase 17
  even planned.** The two packs (HQ-16, HQ-17 — 27 citations combined) were the
  milestone's long pole; filing them at open let the operator read
  asynchronously while Phase 17 built, exactly the pattern that worked for
  v2.2's HQ-8.
- **Citation granularity as an explicit, load-bearing ruling.** One human D-05
  read per new gate CODE, one bibliographic citation per catalog ENTRY — stated
  and held to. Without it, a ~75-row table would have demanded ~90 human reads
  instead of the 27 actually needed, stalling the ceremony's one human-gated
  step for a milestone of this size.
- **Independent re-verification of every citation before shipping, not after.**
  An interactive session re-derived all 27 citations against primary sources
  (7 parallel research agents) rather than trusting the loop's bibliographic
  corroboration alone. This caught a real defect: a proposed Krippendorff's-
  alpha fixture value (0.743, with a claimed "0.734 textbook typo") that does
  not appear anywhere in the cited 2007 paper — its own worked example gives
  0.7598. Six smaller corrections followed the same pattern (a citation
  attributing a broader claim than its source supports; a locator pinned more
  precisely than the original guess; a claimed replacement-test recommendation
  the source doesn't actually make).
- **Real independent security re-gates, not trusted reports.** All four phases'
  sign-offs (54 threats total, 7 of them HIGH in Phases 19-20) were backed by
  the orchestrator re-running every non-accepted mitigation from a clean tree —
  including confirming citation-laundering and self-reference threats were
  structurally closed (per-family docstrings, not shared blocks; HIGH catch
  computed live, never from the golden reference set) — before the operator
  ever saw the sign-off request.

### What Was Inefficient

- **A weekly usage-limit hit exposed a real gap in the backoff design.**
  Anthropic released the account's weekly limit early; the wrapper's
  dead-reckoning wait (park until the computed deadline) had no way to notice,
  and needed a manual clear plus a same-day fix (a periodic re-probe every 30
  minutes during any hold) before the loop could self-correct on future early
  releases. Caught only because the operator was watching the clock, not
  because the system noticed on its own.
- **`init.manager`'s `verification_status` read "missing" for all four phases**
  despite every one having a real, PASSED `NN-VERIFICATION.md` — the same class
  of framework-CLI naming-convention blind spot as v2.0.0's/v2.2's audit-uat
  issues, just manifesting on a different code path. Required direct evidence
  (reading the actual verification files) to safely override at close-out.
- **The milestone-complete CLI's accomplishment extraction was still unreliable**
  a second time (v2.2 had the same defect) — several bullets truncated
  mid-sentence or captured YAML frontmatter instead of prose. Hand-corrected
  again from the real `SUMMARY.md` files rather than fixing the extractor
  itself, which remains a standing, accepted cost of milestone close.

### Patterns Established

- **Deprecated methods ship as first-class routing-off catalog rows**, not
  silent omissions — Yates' correction, unprotected LSD at k>3, Vuong-for-zero-
  inflation, observed power all get a named row stating why they're wrong and
  what replaces them, mirroring the honesty already shipped for Fisher-vs-
  Boschloo in the original 15-row table.
- **Negative gates for doctrine, not just positive gates for coverage.** Where
  the anti-two-stage rule needed active enforcement rather than passive
  avoidance, the milestone shipped gates that block the wrong pattern directly
  (variance-test-as-precondition; observed-power-in-a-readout) instead of only
  documenting the right one.
- **A permanent doc/code agreement cross-check**, not just a one-time repair —
  `test_doc_code_agreement.py` binds `references/test-selection.md`'s decision
  rows to the live routing engines by strict cell equality, closing the
  structural gap the Boschloo divergence exploited so that class of bug cannot
  recur silently again.

### Key Lessons

- A citation pack that has already self-flagged its own uncertain spots (locator
  traps, edition ambiguities, disputed values) is a *better* pack, not a weaker
  one — it is exactly what let the independent re-verification focus effort
  where it mattered and confirm the rest quickly.
- An automated backoff/retry mechanism needs to periodically re-test its own
  precondition, not just wait out a computed deadline — any dead-reckoned
  estimate of an external system's state can be wrong in either direction.
- The same class of defect (generated milestone-close output needing hand
  verification) recurring at a second consecutive milestone close means it is
  now a standing operating cost to budget for, not a one-off surprise.

### Process Observations

- Delivered by the same headless completion ceremony as v2.0.0/v2.2, with the
  operator traveling and reachable only intermittently for this milestone's
  close-out — all seven remaining human-gated items (four security sign-offs,
  three D-06/methodology veto windows) and the ship decision were reviewed and
  approved in a single batched interactive session on the operator's explicit
  go-ahead, rather than split across several round-trips.

## Cross-Milestone Trends

| Milestone | Phases | Plans | Shipped |
|-----------|--------|-------|---------|
| v1.1.0–v1.5.0 | 5 | — | (incremental) |
| v2.0.0 DSX Validity Frame | 11 | 89 | 2026-08-28 |
| v2.2 Analytic Surface | 4 | 20 | 2026-08-29 |
| v2.3 Test Catalog | 4 | 11 | 2026-09-02 |
