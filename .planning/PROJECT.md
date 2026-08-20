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
- **v2.0.0 in progress** — Phase 6 (M1) complete 2026-08-10. Phase 9 (M2c, monitoring
  discipline) complete 2026-08-13. Phase 8 (M2b, interference/triggering/stability)
  complete 2026-08-14. Phase 7 (M2a, validity frame checks `DSX-VAL-*`) complete
  2026-08-20 — re-verification passed 5/5 success criteria, UAT 38/38, 0 open threats;
  the M2 group (7, 8, 9) is closed. Phase 10 (M3, pre-registered inference plan
  `DSX-PRE-*`) complete 2026-08-20 — 6 plans, re-verification passed 5/5, 640 tests
  green; the declared fallback branch is now reconciled against the executed procedure
  at verify and ship, blocking on branch identity alone. Package version is 2.0.0.
  Phases 11–12 remain.

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

## Requirements

### Validated

- ✓ DQ assertions vs `DATA-PROFILE.yaml`, evidence resolution, question↔claim↔decision coherence — v1.1.0
- ✓ Chart-type matrix, figure seals, viz smells, takeaway heuristics, Gate A–D verifier protocol — v1.2.0
- ✓ Narrative discipline, forbidden-claim SSOT, SQL anti-patterns, entrypoint smell scan — v1.3.0
- ✓ Assumption checkoffs/waivers, TOST/CI/MDE, multiplicity family, repro_lock, decision replay — v1.4.0
- ✓ ANALYSIS-SPEC `suppressions[]` with authority, scored CHART-REVIEW.md — v1.5.0
- ✓ `validity_frame:`/`inference:` contract blocks, decision records + `dsx explain`, `DSX-PAR-001` paradigm manifest, `dsx/frame/` package with enforced D-03a boundary, mechanical D-05 citation enforcement, known-bad corpus — Phase 6 (REQ-P6-01 … REQ-P6-16)
- ✓ Symmetric monitoring pair `DSX-PAR-010`/`DSX-PAR-011` plus membership-free `DSX-PAR-002` (requiredness; `DSX-SPEC-085` owns vocabulary membership) — Phase 9 (REQ-P9-01 … REQ-P9-07)
- ✓ Interference adjudication `DSX-INT-010`/`-011` (unaddressed risk; channel-inadmissible mitigation, disjoint on the mitigation dimension alone), triggered-versus-eligible dilution `DSX-INT-030` (additive metrics only, ratio metrics explicitly out of scope), novelty/primacy `DSX-INT-040`, and the no-paradigm-read invariant — Phase 8 (REQ-P8-01 … REQ-P8-06)

### Active

See `.planning/REQUIREMENTS.md` for the v2.0.0 requirement set (REQ-P7-* … REQ-P12-*). REQ-P6-* are complete.

### Out of Scope

- Computing test statistics or posteriors inside the gate path — breaks D-01/D-02
- Bayesian procedure recommendation and admissibility — gated backlog, entry condition in brief §6.5
- Prior justification, prior sensitivity, convergence declarations — deferred under D-12a; their frequentist mirrors are not written
- Causal identification *strategy* checking — `DSX-CAU-*` owns this
- Survival, time-series and spatial estimation *methods* — temporal/spatial dependence are declared types; the methods are out
- Reading a data warehouse from a gate — breaks the determinism doctrine
- A catalogue of every named statistical test — families, not tests

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
  - `dsx explain` and `dsx stats` do not exist yet — new subcommands.
  - No `dsx/frame/` package; `references/families.yaml` absent (correct until M4).

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
| D-03a Keep an extractable boundary: `dsx/frame/` imports only `Report`/`Finding` from `dsx/checks/` | If in six months there are no upward imports, extraction is a `git filter-repo` | Delivered Phase 6 — `dsx/frame/` exists; `tests/test_frame_boundary.py` fails the suite on any upward import |
| D-04 Never block to teach — gates emit a decision record, `dsx explain` renders it | A gate that stops to explain is disabled on a deadline, losing guardrail and lesson both | Delivered Phase 6 — `dsx/decisions.py` emits, `dsx explain` renders, always exit 0; the gate-path write is a guarded side channel |
| D-05 Citation + published reference value per check | Prevents laundering model statistics knowledge into a blocking gate | Delivered Phase 6 — `check_d05` in `gen-finding-catalogue.py --check` fails the build on a missing `Citation:` line |
| D-10 An unsupported paradigm is never blocking on its own | Blocking on `paradigm: bayesian` makes typing `frequentist` the cheapest way past the gate | Delivered Phase 6 — `DSX-PAR-001` is INFO (10); every default `GATE_THRESHOLDS` value is 40 or 50 |
| D-11 Frame-layer checks never read `paradigm` | A prior does not save you from pseudo-replication; if a frame check branches on paradigm it is in the wrong layer | — Pending |
| D-12/D-12a Paradigm-specific checks ship in symmetric pairs, and symmetry is the scoping rule | Asymmetric enforcement is how a tool silently steers method choice | Delivered Phase 9 for the monitoring pair (`DSX-PAR-010`/`-011` at identical CRITICAL; `is_blank_text` as the single clearing predicate; committed symmetry audit). D-12a deferred codes (`DSX-PAR-020`/`-021`/`-030`) remain out of scope |
| D-13 Deferred checks carry an entry condition, not a wish | A trigger tied to a measured catch rate is falsifiable; a priority is not | — Pending |
| D-14 Reversing a D-table decision requires a reversal record; evidence-free reversal logs as `SELF-001` | "Here is what would change my mind" is stronger than "here is what I chose" | — Pending |
| **M-01** `DSX-PAR-010` ships as a distinct code, `DSX-EXP-060` untouched | Triggers are disjoint — undeclared looks under a fixed horizon vs a declared continuous design with no sequential method. Widening EXP-060 would silently broaden existing suppressions, against the spirit of D-06 | Delivered Phase 9 — pair ships in `dsx/frame/paradigm.py`; `dsx/checks/design.py` untouched |
| **M-02** No `inference.stopping_rule` field; `DSX-PAR-010/011` read the existing `design.peeking_policy` | One concept, one field. Avoids a permanent consistency check between two vocabularies for the same thing. Deviates from brief §5.2, which specified a new field | Delivered Phase 9 — both codes trigger on `peeking_policy: uncontrolled_continuous` |
| **Phase 9 D-08** `DSX-PAR-002` is presence/requiredness only; `DSX-SPEC-085` owns closed-vocabulary membership | Two codes for one defect would violate one-stable-fact-per-code. UAT 2026-08-13 accepted the split; ROADMAP SC 4 / REQ-P9-04 amended to name both codes | Delivered Phase 9 |
| **M-03** `PEEKING_POLICIES` gains a value for uncontrolled continuous monitoring | Consequence of M-02: the existing vocabulary has `always_valid` (disciplined) but no value for "peeking continuously with no correction" — precisely what `DSX-PAR-010` must fire on | Delivered Phase 6 — `uncontrolled_continuous` added (`dsx/spec.py:71`) |
| **M-04** Automated import test enforces the D-03a boundary from M1 | Enforces the boundary without scaffolding an empty `families.yaml`, which brief §6.6 warns accumulates speculative structure | Delivered Phase 6 — AST scanner proven against three deliberately violating sources |
| **M-05** `SELF-001` stays a convention for v2.0.0; `REVERSALS.md` template seeded in M1 | Enforcement is a planning-process concern, not a gate concern; a subcommand adjudicating planning docs is outside the gate path | Delivered Phase 6 — `REVERSALS.md` seeded with the four-field D-14 template; SELF-001 trigger stated. Human-validated (UAT 1) |
| **M-06** `validity_frame` sub-block requiredness is gated by `question_type` from M1 | Requiring the whole block for descriptive/BI work forces reflexive `none` answers — the exact incentive distortion D-10 exists to prevent. Far cheaper decided in M1 than retrofitted after M2a/M2b are written against the wrong requiredness | Delivered Phase 6 — REQ-P6-03 |
| **M-07** Existing `suppressions[]` with its authority requirement is the grandfather path for pre-v2.0.0 specs | Zero new code, and the ADR/SPEC authority requirement makes grandfathering deliberate and attributable rather than silent | Delivered Phase 6 — README states authority as a requirement (DSX-SPEC-070) and the "a frame that lies passes" known limit. Human-validated (UAT 2) |
| **M-08** D-05 citation enforcement is automated in M1 via `scripts/gen-finding-catalogue.py` | D-05 says "if velocity pressure arrives, cut checks, never this" — an unenforced constraint is the first thing velocity pressure removes. It was the only major constraint nothing checked | Delivered Phase 6 — see D-05 |
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
*Last updated: 2026-08-20 after Phase 10*
