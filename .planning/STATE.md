# Project state

**Status:** Phase 5 complete (v1.5.0)  
**Locked decisions:** DQ = profile runner + hermetic gates; Glyph = hermetic svg_sha256 only (no MCP dep); forbidden claims = universal pack + optional phase YAML; repro_lock = ARS-style honest-null (not byte-replay); decision replay = structured thresholds only; suppressions = ADR/SPEC authority required (unknown codes → exit 2)

## Done

- v1.0.0 overlay
- Phase 1 (v1.1.0): DQ, evidence, coherence
- Phase 2 (v1.2.0): data_input_type matrix, figure seals, smells B/G/I/J/K/M, takeaway heuristics, Gate A–D verifier protocol
- Phase 3 (v1.3.0): narrative gates, CLM-070/080, NAR-*, CODE-* fit-before-split, SQL-007–014, MET-040 warehouse⇒sql
- Phase 4 (v1.4.0): assumption checkoffs/waivers, STA-020/021 TOST/CI/MDE, EXP-051/052, DEC-*, REP-050–053, recon classes
- Phase 5 (v1.5.0): ANALYSIS-SPEC `suppressions[]`, scored CHART-REVIEW.md (`dsx-chart-review-v1`), skill `dsx-chart-audit`, viz-critic writes CHART-REVIEW

## Next

- Maintenance / optional later extensions (Parquet profiler, live Glyph MCP, NLP decision_rule — explicitly out of scope for core gates)
