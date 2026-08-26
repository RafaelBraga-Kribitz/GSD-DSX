# gsd-dsx

**Data science, analytics and BI rigour for GSD Core.**

## Purpose

Specialise the GSD phase loop for analytical work without forking gsd-core.
Agents fill structured contracts; deterministic Python gates block the loop when
the contracts and artifacts do not hold up.

## Core Value

A statistically invalid analysis must fail at the gate, before the data is
touched — not later, in someone else's review.

## Success bar — ten quality dimensions

Every analytical phase that ships under dsx must satisfy these with code where
decidable, and with strong agent guardrails where judgement is required:

1. Analytical Question
2. Analytical Logic
3. Chart Type
4. Missing Evidence
5. Data Quality
6. Code Quality
7. Statistical Issues
8. Plot Construction
9. Visual Design
10. Communication and Data Storytelling

## Determinism doctrine

| Stochastic (agent judgement) | Deterministic (code) |
|---|---|
| Framing the question, choosing the design, writing claims and narrative | Checking the spec is coherent and that produced artifacts satisfy it |

Gates never read live warehouses. They check declarations and hermetic artifacts
(`ANALYSIS-SPEC.yaml`, `DATA-PROFILE.yaml`, evidence files). `dsx profile`
computes profiles from local CSV when available; the gate still only reads the
written profile.

## Current state

- **v1.5.0** shipped: Phases 1–5 complete. Ten quality dimensions gated where
  decidable (DQ, evidence, coherence, viz/seals/smells, narrative/code, analytical
  logic / stats extensions including decision replay and repro_lock, plus scored
  CHART-REVIEW and ADR-authorised suppressions).

## Current Milestone: v2.0.0 DSX Validity Frame

**Goal:** Check the layer beneath every existing DSX check — that the estimand,
unit triad, dependence structure, interference risk, triggering, sampling frame,
missingness mechanism, measurement and declared inferential paradigm are coherent
enough for any DSX finding to mean anything.

**Why now:** The existing families (`DSX-EXP-*`, `DSX-STA-*`, `DSX-MET-*` …) all
assume a sound foundation. Class A failures — the ones recoverable only by
collecting new data — are largely uncovered today. Test choice is recoverable by
reanalysis; a wrong estimand is not.

**Operating context:** marketing data science, roughly 60% online controlled
experiments, under both frequentist and Bayesian paradigms, often on shared
paid-media budgets. The check set is weighted accordingly.

**Target features:**

- `validity_frame:` and paradigm-aware `inference:` blocks in `ANALYSIS-SPEC.yaml`
- Decision record (`5.5` schema) emitted by every step, plus non-blocking `dsx explain`
- `DSX-VAL-*` — estimand, unit triad, dependence, identification strength, sampling
  frame, missingness, measurement
- `DSX-INT-*` — interference/SUTVA, triggering and dilution, novelty and primacy
- `DSX-PAR-*` — paradigm manifest and the symmetric monitoring pair
- `DSX-PRE-*` — pre-registered inference plan, declared branch vs executed branch
- `DSX-ADM-*` — frequentist procedure admissibility over `references/families.yaml`
- Calibration corpus with measured catch rate and false-positive rate

**Version rationale:** v2.0.0 rather than v1.6.0 because `validity_frame:` becomes
required from plan (the `plan` gate point, at CRITICAL severity), so existing
specs without it begin to block — a breaking contract change.

## Queued Milestone: v2.1 Analytic Surface

**Status:** Queued. Not started. Does not reopen Phases 7–12.

**Goal:** Close the operator-surface gaps that Claude Code data-science packs
cover with playbooks — cohort/funnel/root-cause skills, knowledge compounding,
CUPED as a declared variance adjustment, a CSV-first start, file-first scripts,
and off-gate re-run verification — without turning DSX into a prompt pack and
without computing statistics on the gate path.

**Why after v2.0.0:** Brief §3 ranks risk reduction first. The comparison packs
do not gate shared-budget interference, triggering dilution, or Bayesian
continuous monitoring. Folding their playbooks into Phases 7–12 would delay
that work. Entry condition is Phase 12 closed (`brief.md` §6.5). Skill-only
drafts may begin after Phase 6; they do not gate v2.0.0.

**Target features:** Phases 13–16 in `.planning/ROADMAP.md`. Requirements
REQ-P13-* … REQ-P16-* in `.planning/REQUIREMENTS.md` under **Queued**, outside
the 53/53 v2.0.0 map. Comparison evidence: `.planning/research/SURFACE.md`.

**Anti-features (explicitly not queued):** Docker as a required runtime; MLflow
or Great Expectations on the gate path; notebooks as the shipped artifact;
Shapiro–Wilk auto-switch; SEM/HLM/IRT; bundled education datasets; a batch
path that skips the plan gate.

## Requirements

### Validated

- ✓ DQ assertions vs `DATA-PROFILE.yaml`, evidence resolution, question↔claim↔decision coherence — v1.1.0
- ✓ Chart-type matrix, figure seals, viz smells, takeaway heuristics, Gate A–D verifier protocol — v1.2.0
- ✓ Narrative discipline, forbidden-claim SSOT, SQL anti-patterns, entrypoint smell scan — v1.3.0
- ✓ Assumption checkoffs/waivers, TOST/CI/MDE, multiplicity family, repro_lock, decision replay — v1.4.0
- ✓ ANALYSIS-SPEC `suppressions[]` with authority, scored CHART-REVIEW.md — v1.5.0

### Active

See `.planning/REQUIREMENTS.md` for the v2.0.0 requirement set (REQ-P6-* … REQ-P12-*).
Queued v2.1 requirements (REQ-P13-* … REQ-P16-*) are recorded there under
**Queued — Milestone v2.1** and are not Active until Phase 12 closes.

### Out of Scope

- Computing test statistics or posteriors inside the gate path — breaks D-01/D-02
- Bayesian procedure recommendation and admissibility — gated backlog, entry condition in brief §6.5
- Prior justification, prior sensitivity, convergence declarations — deferred under D-12a; their frequentist mirrors are not written
- Causal identification *strategy* checking — `DSX-CAU-*` owns this
- Survival, time-series and spatial estimation *methods* — temporal/spatial dependence are declared types; the methods are out
- Reading a data warehouse from a gate — breaks the determinism doctrine
- A catalogue of every named statistical test — families, not tests
- Operator-surface playbooks, CUPED, compounding, reproduce-skill — **queued as v2.1** after Phase 12, not this milestone. Not a rejection. See Queued Milestone above.

## Context

- Seed brief: `brief.md` (committed at milestone start). Sections 4 (decisions),
  5 (contract), 6 (milestones), 6.5 (gated backlog) and 7 (citations) are binding
  inputs to planning and must not be re-litigated in discuss.
- Existing integration surface verified at v1.5.0:
  - Gate profiles are check-module tuples in `dsx/cli.py` (`GATE_PROFILES`), with
    thresholds CRITICAL at plan/execute and HIGH at verify/ship. New families must
    be registered there.
  - `DSX-EXP-060` already fires on undeclared interim looks under a fixed horizon.
  - `DSX-EXP-020/021` already reconciles `randomization_unit` vs `analysis_unit`.
  - `PEEKING_POLICIES` in `dsx/spec.py` already covers the stopping-rule concept.
  - `VARIANCE_ADJUSTMENTS` overlaps the proposed `dependence.method_family_required`.
    On 2026-08-26 the set is `{cluster_robust, delta_method, bootstrap_cluster,
    mixed_effects}` — CUPED is absent; adding it is queued Phase 15, not a v2.0.0
    vocabulary change.
  - `dsx explain` and `dsx stats` do not exist yet — new subcommands.
  - No `dsx/frame/` package; `references/families.yaml` absent (correct until M4).
  - Analytic-surface comparison against five Claude Code packs: `.planning/research/SURFACE.md`
    (2026-08-26). That file does not authorise finding codes.

## Constraints

- **Tech stack**: Python 3.9+, stdlib only on the gate path — D-01. A gate that breaks on a missing dependency is a gate that gets turned off.
- **Dependencies**: GSD Core >= 1.6. Extends the existing DSX package — no fork, no second installer, no patched upstream workflows.
- **Compatibility**: Exit codes remain the contract — `0` pass, `1` block, `2` could not run.
- **Compatibility**: Finding codes are never renumbered — D-06. A suppression written today stays valid.
- **Evidence**: No check ships without a primary-source citation in its docstring and a test against a published reference value — D-05. If velocity pressure arrives, cut checks, never this.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| D-03 Extend DSX in place, one install/contract/gate/test suite/catalogue | Highest-value checks are cross-cutting; a check spanning two contracts cannot live cleanly in either of two plugins | — Pending |
| D-03a Keep an extractable boundary: `dsx/frame/` imports only `Report`/`Finding` from `dsx/checks/` | If in six months there are no upward imports, extraction is a `git filter-repo` | — Pending |
| D-04 Never block to teach — gates emit a decision record, `dsx explain` renders it | A gate that stops to explain is disabled on a deadline, losing guardrail and lesson both | — Pending |
| D-05 Citation + published reference value per check | Prevents laundering model statistics knowledge into a blocking gate | — Pending |
| D-10 An unsupported paradigm is never blocking on its own | Blocking on `paradigm: bayesian` makes typing `frequentist` the cheapest way past the gate | — Pending |
| D-11 Frame-layer checks never read `paradigm` | A prior does not save you from pseudo-replication; if a frame check branches on paradigm it is in the wrong layer | — Pending |
| D-12/D-12a Paradigm-specific checks ship in symmetric pairs, and symmetry is the scoping rule | Asymmetric enforcement is how a tool silently steers method choice | — Pending |
| D-13 Deferred checks carry an entry condition, not a wish | A trigger tied to a measured catch rate is falsifiable; a priority is not | — Pending |
| D-14 Reversing a D-table decision requires a reversal record; evidence-free reversal logs as `SELF-001` | "Here is what would change my mind" is stronger than "here is what I chose" | — Pending |
| **M-01** `DSX-PAR-010` ships as a distinct code, `DSX-EXP-060` untouched | Triggers are disjoint — undeclared looks under a fixed horizon vs a declared continuous design with no sequential method. Widening EXP-060 would silently broaden existing suppressions, against the spirit of D-06 | — Pending |
| **M-02** No `inference.stopping_rule` field; `DSX-PAR-010/011` read the existing `design.peeking_policy` | One concept, one field. Avoids a permanent consistency check between two vocabularies for the same thing. Deviates from brief §5.2, which specified a new field | — Pending |
| **M-03** `PEEKING_POLICIES` gains a value for uncontrolled continuous monitoring | Consequence of M-02: the existing vocabulary has `always_valid` (disciplined) but no value for "peeking continuously with no correction" — precisely what `DSX-PAR-010` must fire on | — Pending |
| **M-04** Automated import test enforces the D-03a boundary from M1 | Enforces the boundary without scaffolding an empty `families.yaml`, which brief §6.6 warns accumulates speculative structure | — Pending |
| **M-05** `SELF-001` stays a convention for v2.0.0; `REVERSALS.md` template seeded in M1 | Enforcement is a planning-process concern, not a gate concern; a subcommand adjudicating planning docs is outside the gate path | — Pending |
| **M-06** `validity_frame` sub-block requiredness is gated by `question_type` from M1 | Requiring the whole block for descriptive/BI work forces reflexive `none` answers — the exact incentive distortion D-10 exists to prevent. Far cheaper decided in M1 than retrofitted after M2a/M2b are written against the wrong requiredness | — Pending |
| **M-07** Existing `suppressions[]` with its authority requirement is the grandfather path for pre-v2.0.0 specs | Zero new code, and the ADR/SPEC authority requirement makes grandfathering deliberate and attributable rather than silent | — Pending |
| **M-08** D-05 citation enforcement is automated in M1 via `scripts/gen-finding-catalogue.py` | D-05 says "if velocity pressure arrives, cut checks, never this" — an unenforced constraint is the first thing velocity pressure removes. It was the only major constraint nothing checked | — Pending |
| **M-09** `dependence.method_family_required` reuses `VARIANCE_ADJUSTMENTS` | Same reasoning as M-02: one concept, one vocabulary. Consequence: the field holds a single member, so the brief's example `cluster_robust_or_mixed` is not expressible — carried as an open item for the M2a discuss rather than silently modelled as a disjunction | — Pending |

## Non-goals

- Patching gsd-core workflows
- Third-party Python deps inside the gate process
- Reading production databases from `dsx gate`

## Known limits

The gate checks declarations against declarations. **A frame that lies passes.**
The insurance against a bad question is still a human who knows the domain reading
the frame before the data is touched. What this changes is that the review becomes
cheap, structured and repeatable, so it actually happens. To be stated in the README.

## Evolution

This document evolves at phase transitions and milestone boundaries.

**Queued work is not a phase transition.** Adding v2.1 Analytic Surface to the
roadmap (2026-08-26) does not move v2.0.0 requirements, does not close Phase 6,
and does not authorise implementation of Phases 13–16 until Phase 12 closes.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-08-26 — queued milestone v2.1 Analytic Surface after v2.0.0;
current milestone remains v2.0.0 DSX Validity Frame*
