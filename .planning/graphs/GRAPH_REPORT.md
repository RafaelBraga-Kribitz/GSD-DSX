# Graph Report - dsx  (2026-08-27)

> **This is a copy**, placed here to satisfy the global CLAUDE.md primer path
> (`.planning/graphs/GRAPH_REPORT.md`). The tool's real working directory is
> `dsx/graphify-out/` (gitignored) — that is where `graph.json`, `graph.html`,
> the cache, and manifest actually live, and where `graphify update dsx` looks.
> To refresh: `cd` to the repo root, run `graphify update dsx`, then re-copy
> `dsx/graphify-out/GRAPH_REPORT.md` and `graph.json` here.
>
> **Scope:** `dsx/` only (35 Python files) — pure AST extraction, zero LLM
> cost. `tests/`, `references/`, `docs/` and the top-level `.md` files were
> deliberately left out of this first pass; `.planning/` was excluded
> entirely (volatile ceremony bookkeeping, not codebase structure). Community
> labels below read "Community N" rather than plain-language names — the
> standalone CLI tried an OpenAI backend for labeling that isn't installed
> here; the graph structure and God Nodes/Surprising Connections below are
> unaffected, only the labels are generic.

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 615 nodes · 1858 edges · 18 communities (17 shown, 1 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 40 edges (avg confidence: 0.67)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c8b0bff1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Report
- cli.py
- mathx.py
- prereg.py
- code.py
- admissibility.py
- claims.py
- loader.py
- is_blank
- normalize
- input_types.py
- get
- DecisionRecord
- profiler.py
- paradigm.py
- decision.py
- _check_spec_identity
- frame/__init__.py

## God Nodes (most connected - your core abstractions)
1. `Report` - 175 edges
2. `normalize()` - 91 edges
3. `is_blank()` - 90 edges
4. `get()` - 71 edges
5. `as_number()` - 50 edges
6. `items()` - 46 edges
7. `section()` - 41 edges
8. `DecisionRecord` - 34 edges
9. `run_checks()` - 24 edges
10. `check()` - 22 edges

## Surprising Connections (you probably didn't know these)
- `main()` --indirect_call--> `SpecParseError`  [INFERRED]
  cli.py → loader.py
- `check()` --references--> `Report`  [EXTRACTED]
  checks/chart_review.py → findings.py
- `run_checks()` --calls--> `check()`  [EXTRACTED]
  cli.py → checks/chart_review.py
- `_check_schema_tag()` --references--> `Report`  [EXTRACTED]
  checks/chart_review.py → findings.py
- `_check_forbidden_scale()` --references--> `Report`  [EXTRACTED]
  checks/chart_review.py → findings.py

## Import Cycles
- None detected.

## Communities (18 total, 1 thin omitted)

### Community 0 - "Report"
Cohesion: 0.05
Nodes (94): check(), _check_assumptions(), _check_claim_ceiling(), _check_decision_language(), _check_experiment_decision(), _check_revisit_completeness(), Question ↔ claim ↔ decision coherence. Codes DSX-COH-*.  The analytical questi, Emit DSX-COH-040 when a prescriptive question or an experiment design has     n (+86 more)

### Community 1 - "cli.py"
Cohesion: 0.05
Nodes (73): ArgumentParser, check(), _check_manifest(), file_sha256(), _find_file(), Path, Figure artifact seals. Codes DSX-FIG-*.  Hermetic proof that a declared chart ma, Audit figure artifacts.      ``strict=True`` (verify/ship) requires ``svg_sha256 (+65 more)

### Community 2 - "mathx.py"
Cohesion: 0.06
Nodes (63): check(), _check_allocation(), _check_duration(), _check_experiment_power(), _check_guardrails(), _check_identification(), _check_peeking(), _check_units() (+55 more)

### Community 3 - "prereg.py"
Cohesion: 0.07
Nodes (42): Append this gate run's invocation header and decision records to     ``DECISION, _write_decision_trail(), AmendmentRecord, append(), collect_from_report(), decisions_path(), frame_digest(), InvocationHeader (+34 more)

### Community 4 - "code.py"
Cohesion: 0.07
Nodes (42): BaseException, _call_sites(), _CallSite, check(), _first_argument(), _first_fit_leak_line(), _first_full_frame_cleaning_line(), _first_line_matching() (+34 more)

### Community 5 - "admissibility.py"
Cohesion: 0.08
Nodes (39): admissible_families(), alias_index(), candidate_families(), check(), _check_declared_procedure_ranking(), _check_no_admissible_procedure(), _coerce_family(), _coerce_rule() (+31 more)

### Community 6 - "claims.py"
Cohesion: 0.10
Nodes (35): _anchor_present(), check(), _check_causal_language(), _check_causal_support(), _check_evidence_pointer(), _check_generalisation(), _check_limitations_required(), _check_numeric_overlap() (+27 more)

### Community 7 - "loader.py"
Cohesion: 0.12
Nodes (34): check(), _check_finding_tokens(), _check_forbidden_scale(), _check_schema_tag(), _check_terminal_sentinel(), _find_chart_review(), Path, CHART-REVIEW.md structural conformance. Codes DSX-CRV-*.  Validates the adversar (+26 more)

### Community 8 - "is_blank"
Cohesion: 0.12
Nodes (31): check(), _check_dependence(), _check_estimand_completeness(), _check_estimand_falsifiability(), _check_exclusions(), _check_identification(), _check_measurement(), _check_missingness() (+23 more)

### Community 9 - "normalize"
Cohesion: 0.17
Nodes (23): check(), _check_baseline(), _check_calibration(), _check_cleaning(), _check_features(), _check_metric_choice(), _check_overfit(), _check_prediction_time_definition() (+15 more)

### Community 10 - "input_types.py"
Cohesion: 0.18
Nodes (19): _by_id(), canonical_id(), family_of(), get(), input_types(), known_shapes(), _load(), permitted() (+11 more)

### Community 11 - "get"
Cohesion: 0.21
Nodes (19): get(), needs_causal_block(), The ANALYSIS-SPEC contract — closed vocabularies and structural validation.  T, The single condition deciding whether the causal ``validity_frame`` sub-blocks, Requiredness, aggregation and membership shape of the ``validity_frame:`` block., Shape validation of the optional ``inference:`` block.      Codes DSX-SPEC-085, Read a dotted path out of a nested mapping. Never raises on a missing key., Shape and vocabulary validation. Semantic coherence lives in checks/.      Cod (+11 more)

### Community 12 - "DecisionRecord"
Cohesion: 0.18
Nodes (15): DecisionRecord, One decision-trail entry — brief section 5.5's schema.      ``counterfactual``, check(), _check_interference_mitigation_admissibility(), _check_interference_unaddressed(), _check_stability_assessment(), _check_triggering_dilution(), DSX-INT-* — interference, triggering and stability (Phase 8).  This module adj (+7 more)

### Community 13 - "profiler.py"
Cohesion: 0.24
Nodes (15): date, _dump(), dump_profile_yaml(), file_sha256(), _infer_dtype(), _is_null(), _parse_date(), profile_csv() (+7 more)

### Community 14 - "paradigm.py"
Cohesion: 0.21
Nodes (11): applies_to_frequentist_admissibility(), _blank_clearing_declarations(), check(), _check_monitoring_discipline(), _check_paradigm_justification(), DSX-PAR-001 — the informational paradigm manifest — and DSX-PAR-010/011 — the s, Return the subset of ``fields`` that are blank under ``inference``.      The m, Emit DSX-PAR-010 (frequentist) and DSX-PAR-011 (bayesian) — the atomic,     sym (+3 more)

### Community 15 - "decision.py"
Cohesion: 0.67
Nodes (3): check(), _evaluate_replay(), Decision replay against results.tests. Codes DSX-DEC-*.  Structured thresholds i

### Community 16 - "_check_spec_identity"
Cohesion: 0.50
Nodes (4): _check_spec_identity(), True when ``spec`` is one of the two kinds D-08 requires a top-level     ``spec, Emit ``DSX-PRE-040`` when a prescriptive or experiment spec declares no     top, _spec_id_required()

## Knowledge Gaps
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Report` connect `Report` to `cli.py`, `mathx.py`, `prereg.py`, `code.py`, `admissibility.py`, `claims.py`, `loader.py`, `is_blank`, `normalize`, `get`, `DecisionRecord`, `paradigm.py`, `decision.py`, `_check_spec_identity`?**
  _High betweenness centrality (0.311) - this node is a cross-community bridge._
- **Why does `is_blank()` connect `is_blank` to `Report`, `cli.py`, `mathx.py`, `prereg.py`, `code.py`, `admissibility.py`, `claims.py`, `normalize`, `get`, `DecisionRecord`, `paradigm.py`, `decision.py`, `_check_spec_identity`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `normalize()` connect `normalize` to `Report`, `cli.py`, `mathx.py`, `prereg.py`, `admissibility.py`, `claims.py`, `is_blank`, `get`, `DecisionRecord`, `paradigm.py`, `decision.py`, `_check_spec_identity`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Should `Report` be split into smaller, more focused modules?**
  _Cohesion score 0.051831501831501835 - nodes in this community are weakly interconnected._
- **Should `cli.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05118601747815231 - nodes in this community are weakly interconnected._
- **Should `mathx.py` be split into smaller, more focused modules?**
  _Cohesion score 0.061057692307692306 - nodes in this community are weakly interconnected._
- **Should `prereg.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07246376811594203 - nodes in this community are weakly interconnected._