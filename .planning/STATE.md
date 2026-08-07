---
gsd_state_version: 1.0
milestone: v2.0.0
milestone_name: DSX Validity Frame
current_phase: 06
current_phase_name: contract-extension-decision-record-paradigm-manifest
status: executing
stopped_at: Completed 06-01-PLAN.md
last_updated: "2026-08-07T21:57:13.086Z"
last_activity: 2026-08-07
last_activity_desc: Phase 06 execution started
progress:
  total_phases: 1
  completed_phases: 0
  total_plans: 10
  completed_plans: 1
  percent: 0
---

# Project state

**Status:** Ready to execute
**Progress:** [█░░░░░░░░░] 10% (0/7 phases)  
**Locked decisions:** DQ = profile runner + hermetic gates; Glyph = hermetic svg_sha256 only (no MCP dep); forbidden claims = universal pack + optional phase YAML; repro_lock = ARS-style honest-null (not byte-replay); decision replay = structured thresholds only; suppressions = ADR/SPEC authority required (unknown codes → exit 2)  
**v2.0.0 locked decisions:** DSX-PAR-010 is a distinct code, DSX-EXP-060 untouched (M-01); no `inference.stopping_rule` — PAR-010/011 read the existing `design.peeking_policy` (M-02); PEEKING_POLICIES gains an uncontrolled-continuous-monitoring value (M-03); automated import test enforces the D-03a boundary from M1 (M-04); SELF-001 stays a convention, REVERSALS.md template seeded in M1 (M-05); `validity_frame` sub-block requiredness gated by `question_type` (M-06); existing `suppressions[]` is the pre-v2.0.0 grandfather path (M-07); D-05 citation enforcement automated via `gen-finding-catalogue.py` (M-08); `dependence.method_family_required` reuses `VARIANCE_ADJUSTMENTS` (M-09)

## Done

- v1.0.0 overlay
- Phase 1 (v1.1.0): DQ, evidence, coherence
- Phase 2 (v1.2.0): data_input_type matrix, figure seals, smells B/G/I/J/K/M, takeaway heuristics, Gate A–D verifier protocol
- Phase 3 (v1.3.0): narrative gates, CLM-070/080, NAR-*, CODE-* fit-before-split, SQL-007–014, MET-040 warehouse⇒sql
- Phase 4 (v1.4.0): assumption checkoffs/waivers, STA-020/021 TOST/CI/MDE, EXP-051/052, DEC-*, REP-050–053, recon classes
- Phase 5 (v1.5.0): ANALYSIS-SPEC `suppressions[]`, scored CHART-REVIEW.md (`dsx-chart-review-v1`), skill `dsx-chart-audit`, viz-critic writes CHART-REVIEW
- v2.0.0 requirements defined (53 requirements, REQ-P6-* … REQ-P12-*)
- v2.0.0 roadmap written — Phases 6–12, 53/53 requirements mapped, traceability populated

## Next

- Phase 6 (M1) — Contract extension, decision record, paradigm manifest. Blocks every other v2.0.0 phase.
- Then Phases 7/8/9 (M2a/M2b/M2c) — no hard ordering among themselves; listed order is catastrophe-prevention value per unit of work.
- Then Phase 10 (M3, soft-depends on 7), Phase 11 (M4, hard-depends on 7), Phase 12 (M5, terminal).
- Deferred, unchanged: Parquet profiler, live Glyph MCP, NLP decision_rule — out of scope for core gates.

## Accumulated Context

**Hard ordering constraints carried into planning:**

- Phase 6 blocks Phases 7–12.
- Within Phase 6: the loader `_NULL` fix (REQ-P6-01) lands before the `validity_frame:` schema (REQ-P6-02) — four frame fields declare `none` as a legitimate value.
- `DSX-PAR-001` (REQ-P6-09) ships in Phase 6, not Phase 9 — no window where `paradigm` exists without defined behaviour.
- Phase 9's `DSX-PAR-010` and `DSX-PAR-011` are atomic (D-12): both ship or neither; the phase cannot close half-delivered.
- Phase 7 precedes Phase 11 — admissibility is keyed on the dependence taxonomy.
- Phase 12 is necessarily last.

**Open items to resolve at phase discuss (do not decide silently):**

- Phase 7: `method_family_required` cannot express a disjunction under M-09's single-member reuse of `VARIANCE_ADJUSTMENTS`.
- Phases 7, 8, 11: final numeric code assignments beyond those the brief fixes (D-06 makes numbering irreversible).
- Phase 9: whether the pre-existing `inflation_from_peeking()` docstring is upgraded to a full D-05 citation.
- Phase 6: research (ARCHITECTURE §4.3) recommends shipping the `PEEKING_POLICIES` addition with its consumer in Phase 9; REQ-P6-05 places it in Phase 6. Reconcile at Phase 6 discuss.

**Standing per-phase deliverables:**

- D-05 bar: primary-source citation naming the exact formulation + a test against a published reference value (or a named structural criterion).
- D-08: extend both canonical fixtures; the two exit-code tests stay unchanged.
- Register new modules in `GATE_PROFILES`; assert every new code is reachable from at least one profile.
- Emit decision records at each family's key judgment points (D-04).

## Current Position

Phase: 06 (contract-extension-decision-record-paradigm-manifest) — EXECUTING
Plan: 2 of 10
Status: Ready to execute
Last activity: 2026-08-07 — Phase 06 execution started

## Session

**Last session:** 2026-08-07T21:57:13.077Z
**Stopped at:** Completed 06-01-PLAN.md
**Resume file:** None

## Performance Metrics

| Plan | Duration | Tasks | Files |
|------|----------|-------|-------|
| Phase 06 P01 | 25min | 2 tasks | 3 files |

## Decisions

- [Phase ?]: PEEKING_POLICIES.uncontrolled_continuous ships in Phase 6 (D-01); describe_vocabulary() now emits ALL dict-backed vocabularies as full key-sorted description dicts, not just peeking_policies
- [Phase ?]: dependence.method_family_required defines no parallel vocabulary; reuses VARIANCE_ADJUSTMENTS verbatim (M-09)
