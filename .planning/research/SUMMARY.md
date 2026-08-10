# DSX Validity Frame Research Summary

**Project:** gsd-dsx v2.0.0 "DSX Validity Frame"  
**Domain:** Statistical-validity gate checks for online experiments and analytics  
**Researched:** 2026-08-07  
**Confidence:** HIGH for architecture; MEDIUM for features (some UNSOURCED items explicitly flagged)

## Executive Summary

The DSX Validity Frame is a cross-cutting gate subsystem checking whether statistical foundations (estimand, units, dependence, paradigm, identification) are coherent before any downstream check. Gates check *declarations* in ANALYSIS-SPEC.yaml against closed vocabularies and structural logic, never computing statistics (D-01/D-02 constraint).

**Recommended approach:** Ship M1 (foundation, bug fix, paradigm manifest) → M2a/M2b/M2c → M3 → M4 → M5.

**Top 3 risks:** (1) D-05 enforcement is code-review-only; families.yaml in M4 is highest-risk place for silent violation. (2) Six fields allow declaring safe values at zero cost. (3) Requiring validity_frame uniformly forces 40% of non-experimental work to fill irrelevant blocks.

## Key Findings

### Stack and Infrastructure

**No new third-party deps.** Stdlib only: ast, dataclasses, json, pathlib, argparse, random, math, statistics (Python 3.9+ compatible).

**CRITICAL BUG FIX (M1, before M2a):** dsx/loader.py _NULL set incorrectly includes "none" as null, diverging from PyYAML/YAML standards. Corrupts four validity_frame fields declaring literal "none". **Bug reproduced:** _parse_yaml_subset("x: [none, clustered]") returns [None, "clustered"] instead of ["none", "clustered"]. **Fix:** Change _NULL = {"", "null", "~", "none"} to _NULL = {"", "null", "~"}. Backwards-safe; 160 tests unaffected.

### Features and Reference Values

**Every numeric claim traced to primary source.** UNSOURCED items explicitly flagged.

**Ready now:** (1) DSX-VAL-020/021 unit triad: DEFF = 1 + (m-1)*ICC (Kish/Cornfield/Senn); (2) DSX-PAR-010: reuses inflation_from_peeking() (Armitage et al. 1969); (3) **DSX-PAR-011: CRITICAL CHOICE — asserts prior-averaged Ville's bound 1/(K+1), NOT point-null/LIL** (Deng/Lu/Chen 2016 Theorem 1; K=19 → 0.05 ceiling). Brief warns: "fixture against formulation (a), tested against (b) looks like bug"; (4) DSX-INT-030 dilution (additive): delta_diluted ≈ delta_triggered * trigger_rate (Deng & Hu 2015); (5) Missingness: MCAR/MAR/MNAR table (Rubin/Little & Rubin); (6) SUTVA: Imbens & Rubin 2015, Blake & Coey 2014; (7) Identification: Gelman/Simpson/Betancourt 2017; (8) Novelty/primacy: Sadeghi et al. 2021.

**UNSOURCED:** Ratio-metric dilution (DSX-INT-030): Deng & Hu WSDM'15 exact equation could not be extracted. Ship additive-metric only; defer ratio via phase-specific spike pending ACM DL access.

### Architecture and Integration

**D-03a boundary enforceable:** dsx/frame/ may import dsx.findings/spec/loader/decisions but never dsx.checks.*. Enforced via AST test.

**Gate registration independent knobs:** GATE_PROFILES (which checks run) and GATE_THRESHOLDS (what blocks) are separate.

**Severity.INFO exists with zero consumers today.** DSX-PAR-001 is first real user. Cannot block; visibility preserved.

**Decision records are parallel channel** to Report/Finding. Emitted for every judgment including passes.

## Critical Pitfalls (Top 10)

1. **Cheapest-lie fields:** risk: none, declared_at: pre_data, dilution_adjusted: true, analyzed units. Mitigation: basis field, content-hash lock, structural cross-check, tie to trigger.

2. **Monolithic block forces boilerplate:** Requiring validity_frame for all question_types forces ~40% non-experimental work to fill irrelevant blocks. Mitigation: gate sub-block by question_type.

3. **CRITICAL severity misallocation:** Static-analysis literature shows 35–91% non-actionable warnings train users to ignore tools. Mitigation: CRITICAL only for structural absence; HIGH for invalid combinations.

4. **D-05 enforcement automation missing:** Citation + published value is code-review-only. families.yaml in M4 is highest-risk. Mitigation: extend scripts/gen-finding-catalogue.py to require citation marker.

5. **Simulation-formulation trap generalizes:** Published numbers depend on choices titles don't pin. Mitigation: docstring names exact formulation; fixture traces to section/table/equation.

6. **Backlog entry conditions unfalsifiable:** Some require manual narrative judgment. Mitigation: instrument M5 corpus from day one with structured catch-attribution tags.

7. **Symmetric pairs unequal in satisfaction cost:** DSX-PAR-010 requires real sequential method; DSX-PAR-011 can use free-text prior_justification. Mitigation: verify neither half's dishonest path is cheaper.

8. **Pre-data/post-data fields mixed in one required block:** Contract is "filled before data" but contains post-data fields. Mitigation: split gate-profile blocking along pre-data/post-data seam.

9. **Breaking-change migration without grandfather path:** v2.0.0's validity_frame requirement causes all pre-existing specs to fail. Mitigation: document suppression-authority convention; offer dsx frame init scaffolder.

10. **Ontology creep via alias-completeness:** M4's ~25–35 families bounded; aliases unbounded. Mitigation: build from calibration corpus; use escalate branch; cap axis space (frequentist only).

## Implications for Roadmap

Seven milestones, hard and soft dependencies:

- **M1:** Foundation (decisions.py, frame scaffold, DSX-PAR-001, dsx explain, D-03a test, bug fix). Research: none.
- **M2a:** Validity checks. Research: VIF threshold, Rubin MCAR/MAR/MNAR nuance, identification.evidence shape.
- **M2b:** Interference. Research **BLOCKING:** exact Deng & Hu WSDM'15 ratio-metric formula; ship additive-only until extracted.
- **M2c:** Paradigm monitoring pair (DSX-PAR-010/011, atomic per D-12). Research: verify closed-form Beta.
- **M3:** Pre-registration. Research: DSL design, lock choice, results.tests mapping.
- **M4:** Admissibility + families.yaml. Research: corpus-driven taxonomy, admissibility conditions.
- **M5:** Calibration corpus, catch/FPR measurement, backlog gating. Research: labeling criteria, tag schema, measurement methodology.

**Hard constraints:** M1 → all; M2a before M4; DSX-PAR-010/011 atomic; M5 last.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | **HIGH** | Executed against bundled parser; bug reproduced; fix tested (160/160 pass) |
| Features | **MEDIUM** | Numeric claims traced to primary sources; 2 UNSOURCED explicitly (ratio-metric, O'Brien VIF text). Highest confidence: Kish/Cornfield DEFF (3-source), Deng/Lu/Chen Theorem 1 (direct ar5iv verification) |
| Architecture | **HIGH** | Verified against all source files; read from v1.5.0 commit fdc4b8f |
| Pitfalls | **HIGH** | All 10 grounded in D-01…D-14, project constraints, and D-05-sourced literature |

**Overall: HIGH-MEDIUM.**

---

*Research synthesis completed: 2026-08-07*
*Ready for roadmap: yes, with phase-specific research items flagged per phase*
