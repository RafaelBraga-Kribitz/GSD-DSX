---
gsd_state_version: 1.0
milestone: v2.0.0
milestone_name: DSX Validity Frame
status: planning
last_updated: "2026-08-07T12:00:57.553Z"
last_activity: 2026-08-07
progress:
  total_phases: 0
  completed_phases: 0
  total_plans: 0
  completed_plans: 0
  percent: 0
---

# Project state

**Status:** v1.5.0 shipped (Phases 1–5 complete); milestone v2.0.0 DSX Validity Frame starting  
**Locked decisions:** DQ = profile runner + hermetic gates; Glyph = hermetic svg_sha256 only (no MCP dep); forbidden claims = universal pack + optional phase YAML; repro_lock = ARS-style honest-null (not byte-replay); decision replay = structured thresholds only; suppressions = ADR/SPEC authority required (unknown codes → exit 2)  
**v2.0.0 locked decisions:** DSX-PAR-010 is a distinct code, DSX-EXP-060 untouched (M-01); no `inference.stopping_rule` — PAR-010/011 read the existing `design.peeking_policy` (M-02); PEEKING_POLICIES gains an uncontrolled-continuous-monitoring value (M-03); automated import test enforces the D-03a boundary from M1 (M-04); SELF-001 stays a convention, REVERSALS.md template seeded in M1 (M-05)

## Done

- v1.0.0 overlay
- Phase 1 (v1.1.0): DQ, evidence, coherence
- Phase 2 (v1.2.0): data_input_type matrix, figure seals, smells B/G/I/J/K/M, takeaway heuristics, Gate A–D verifier protocol
- Phase 3 (v1.3.0): narrative gates, CLM-070/080, NAR-*, CODE-* fit-before-split, SQL-007–014, MET-040 warehouse⇒sql
- Phase 4 (v1.4.0): assumption checkoffs/waivers, STA-020/021 TOST/CI/MDE, EXP-051/052, DEC-*, REP-050–053, recon classes
- Phase 5 (v1.5.0): ANALYSIS-SPEC `suppressions[]`, scored CHART-REVIEW.md (`dsx-chart-review-v1`), skill `dsx-chart-audit`, viz-critic writes CHART-REVIEW

## Next

- Milestone v2.0.0 — DSX Validity Frame. Defining requirements, then roadmap (Phases 6–12).
- Deferred, unchanged: Parquet profiler, live Glyph MCP, NLP decision_rule — out of scope for core gates.

## Current Position

Phase: Not started (defining requirements)
Plan: —
Status: Defining requirements
Last activity: 2026-08-07 — Milestone v2.0.0 started
