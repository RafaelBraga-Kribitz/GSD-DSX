# Quick Task 260821-d6h: Deepen dsx-explore-data into an insight-driving EDA protocol - Context

**Gathered:** 2026-08-21
**Status:** Ready for planning

<domain>
## Task Boundary

Deepen `skills/dsx-explore-data/SKILL.md` from a data-trust checklist into a reusable
protocol that drives analytical insight, add `templates/EDA.md`, and wire one read line
into `capabilities/dsx/fragments/executor.md`. Agent protocol only — no gate changes.

Design source: a 10-agent research workflow (6 dimension researchers → synthesis →
3 adversarial critics), catalog E-01..E-33, all critic corrections adjudicated by the
orchestrator against the live repo before writing.

</domain>

<decisions>
## Implementation Decisions

### Constraint envelope (locked, from brief.md D-01/D-02 and EDA_enhancement_BRIEF.md)
- Gate path stays stdlib-only; gates adjudicate declarations and never compute statistics.
- No changes to `dsx/`, `dsx/checks/`, `dsx/profiler.py`, fixtures, or DATA-PROFILE schema.
- No new `DSX-*` finding codes. No gate reads `EDA.md` in this pass.
- The EDA agent may use pandas/scipy in its own environment; `dsx/` may not.
- Division of labour: **EDA computes evidence, the spec declares it, gates adjudicate the
  declaration.** Every insight step lands its output in a field that already exists in
  `templates/ANALYSIS-SPEC.yaml`.

### What ships (25 catalog items, critic-corrected)
- Trust core (current steps 1–4) kept, deepened with sub-steps: grain/dependence, joins,
  time integrity, robust summaries, concentration, outlier taxonomy, pathology sweep,
  base rate.
- Six question-type branches (descriptive, diagnostic, experiment, causal-observational,
  predictive, prescriptive), each ending in a `meets | falls_short | re-scope` verdict.
- Segments rewritten with a computed split ranking and a candidate handshake.
- Second-order look: attack the headline with a closed six-mechanism artifact menu.
- Spec reconciliation: `confirms | fills | contradicts` table — the deterministic firing
  condition for stop-and-re-scope.
- Three registers: findings ledger (closed severities with mandatory consequences),
  comparisons ledger (makes `results.comparisons_looked_at` a measurement), and
  searched-not-found (evidence of absence).
- Rerun contract, lifecycle/re-entry rules, single spec-write moment + `dsx validate`.

### Critic corrections applied (verified against repo before acceptance)
- `DSX-VAL-020`'s real clearing condition is `dependence.method_family_required`
  (`dsx/frame/val.py:270+`), so the grain step names it — verified by reading the check.
- `results.comparisons_looked_at` / `interim_looks` are adjudicated in
  `dsx/checks/design.py:407+` / `:446+`, so the comparisons ledger counts at first
  computation — a rerun must not double-count and spuriously fire multiplicity.
- ANALYSIS-SPEC has **no** "pre-declared cuts" field; promotion of a segment candidate is a
  spec amendment adding the test to `design.multiplicity.family`.
- `dsx power` is two-proportion arithmetic only — ICC and outcome_sd are recorded for
  agent-side design arithmetic, not claimed as CLI inputs.
- `validity_frame.measurement.known_gaps` is construct-shaped; outages reconcile through
  `data[].known_gaps`.
- Range-shaped data errors have no assertion type in the closed vocabulary and the profiler
  records no numeric min/max — recorded as known_gaps, never a new assertion key.
- Effect-size statistics (novelty ratio) are readout-stage, not EDA — EDA records the
  inputs (run-window coverage, weekly amplitude) instead of spending an interim look.
- EDA never authors design decisions it cannot measure (e.g. `prediction_time_definition`).
- Every judgement fork closed: artifact mechanisms all computed, decomposition dimension
  chosen by rule, outlier categorical search bounded and ordered.

### Claude's Discretion
Wording, ordering within sections, and table column names — kept in the existing terse
imperative style of the skill, with named outputs and a skip condition per step.

</decisions>

<specifics>
## Specific Ideas

- Column-scoping rule added so the protocol stays completable on wide tables (the
  binding constraint is bookkeeping, not rows).
- Differential attrition (per-arm outcome completeness) added to the experiment branch —
  named by the completeness critic as the largest uncovered validity threat for a
  ~60%-experiment workload.
- Deferred with seeds, not dropped: downstream per-skill read contracts (E-26), the
  shape pack for panel/event/series/nested data (E-27), re-expression ladder (E-28),
  two-way residuals (E-29), null lineup (E-30), expectation register (E-31).

</specifics>

<canonical_refs>
## Canonical References

- `EDA_enhancement_BRIEF.md` — the evaluation and the locked decisions this task honours
- `brief.md` — D-01 (stdlib-only gate path), D-02 (gates adjudicate declarations)
- `templates/ANALYSIS-SPEC.yaml` — every spec field the protocol writes into
- `references/question-taxonomy.md` — the five question types and licensed verbs
- `.planning/seeds/SEED-001-deepen-dsx-explore-data-eda-protocol.md` — carries the deferred set

</canonical_refs>
