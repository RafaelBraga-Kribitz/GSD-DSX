# Phase 11: Frequentist admissibility adjudicator (`DSX-ADM-*`) - Discussion Log (Assumptions Mode)

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions captured in `11-CONTEXT.md` — this log preserves the analysis.

**Date:** 2026-08-20
**Phase:** 11-frequentist-admissibility-adjudicator-dsx-adm
**Mode:** assumptions
**Calibration tier:** standard (no `USER-PROFILE.md`, no `preferences.vendor_philosophy` set)
**Areas analyzed:** data-file shape vs loader capability; module layout and the D-03a boundary;
code numbering, severity and paradigm-conditional registration; ranking determinism, the refusal
branch, and D-05 over data.

## Assumptions Presented

### `families.yaml` schema shape vs the loader's real capability

| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| Top-level mapping holding a block sequence of flat mappings; single-line quoted scalars for axis keys and `citation`; no anchors, no merge keys, no block scalars, no `---` markers | Confident | `dsx/loader.py:43-44`, `:62-66`, `:68`, `:114`, `:145-174`. Both parser paths measured against a candidate schema |
| Inference-method axis key is flat (`inference_method:`); no call-argument string literal begins `inference.` | Confident | `tests/test_frame_boundary.py:155`, `:185-187`; `dsx/frame/prereg.py:504` documents this having already bitten Phase 10 |
| The estimand axis needs a new closed vocabulary in `dsx/spec.py` | Likely | `examples/good-ANALYSIS-SPEC.yaml:283`; `dsx/frame/val.py:53`; `dsx/checks/stats.py:15`; `dsx/spec.py:845-854` |

### Module layout and how `recommend-test` is extended

| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| The D-03a boundary is one-directional; `recommend-test` is extended by composition in `cmd_recommend`, leaving `recommend_test()` untouched | Confident | `tests/test_frame_boundary.py:35`, `:93-102`; `dsx/cli.py:23-52`, `:396-409`; `.planning/research/ARCHITECTURE.md:101-102` |
| `families.yaml` resolved as a package sibling; absent file raises `CheckError` → exit 2, never an empty ontology | Likely | `install.mjs:39-47`; `dsx/cli.py:594`; counter-precedent `dsx/input_types.py:32-33` |

### `DSX-ADM-*` numbering, severity, paradigm-conditional registration

| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| Exactly two codes: `DSX-ADM-010` HIGH, `DSX-ADM-020` CRITICAL; registered at `plan`/`verify`/`ship`, absent from `execute` | Confident | `.planning/research/ARCHITECTURE.md:229-251`; `dsx/cli.py:194-195`; `references/finding-codes.md` has zero `DSX-ADM-` entries; `10-CONTEXT.md:186-188` |
| Exit 1 via the ordinary `emit()` path; no new exit code, no `CheckError`, no change to `dsx/findings.py` | Confident | `dsx/findings.py:181-199`; `dsx/cli.py:796-801`; `10-CONTEXT.md` D-02 |
| The frequentist-only scoping decision is made outside `dsx/frame/admissibility.py` | **Unclear** | `dsx/frame/paradigm.py:54-57`, `:145`, `:466-471`; `tests/test_frame_boundary.py:210-222`; `brief.md` §5.4; `dsx/cli.py:171-200` |

### Ranking determinism, the refusal branch, and D-05 over data

| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| Ranking is a static total order from declared axes only, lexicographic tiebreak on family `id`, byte-stable | Likely → upgraded by research | brief D-02; `10-CONTEXT.md` D-07; `tests/test_dsx.py:345`; `dsx/spec.py:1112-1118` |
| Three causes collapse into one `DSX-ADM-020`, all recording `DecisionRecord(escalate=True)` | Likely | `dsx/decisions.py:82-83` (fields exist, never set by any check); `dsx/frame/prereg.py:247-258`; `.planning/research/PITFALLS.md:617-621` |
| D-05 over data needs a new sibling function in `scripts/gen-finding-catalogue.py`, plus a runtime drop of uncited families | Confident | `scripts/gen-finding-catalogue.py:57-68`, `:101-117`, `:203-242`, `:260-290`; `.planning/research/PITFALLS.md:246-302` |

## External Research

Three gaps were flagged by the analyzer and researched before the assumptions were presented.

**Topic 1 — a citation spine for the ontology.** No single work covers the eight relevant
estimator clusters; they span industrial online-controlled-experiment work, econometrics and
biostatistics/survey statistics. The minimum honest spine is nine works beyond the seven already in
`brief.md` §7. Two locators the project carries as unverified were resolved: Kohavi, Tang & Xu
Chapter 22 *Leakage and Interference between Variants*, pp. 226–234; and Cameron & Miller (2015)
Section VI *Few Clusters* (with the caveat that the accepted manuscript's numbering jumps VIII → XI,
so the typeset journal numbering may differ). Published reference values are best sourced from NIST
Handbook 151 §1.3.5.3 and the NIST Statistical Reference Datasets (SRD 140) rather than from
paywalled textbooks. Four clusters — quantile treatment effects, count/rate models, survey-weighted
estimation, delta method — have verified citations but **no verified reference value**.

**Topic 2 — is there a published assumption taxonomy?** No, and this was established negatively
rather than by failure to find one. The Statistical Methods Ontology (STATO) advertises coverage of
"conditions of application" and returns zero classes labelled "assumption" across 109 properties;
its closest-sounding property, `assumes values specified by`, is about variable value ranges, not
statistical assumptions. No ontology in the OBO Foundry has a class labelled "assumption". The
Ontology of Biological and Clinical Statistics contributes one assumption-adjacent term, and it is a
*process* rather than a vocabulary. A ~16–19 token vocabulary is assemblable from six canonical
sources with per-token citations; its closure is editorial judgement and the file must declare that.

**Topic 3 — can admissible procedures be ranked with citations?** Partially, and the partiality is
the answer. Four pairwise orderings are citable: Welch over Student; Boschloo/unconditional over
Fisher's exact (the only genuine *uniform* domination found); CV3 and the restricted wild cluster
bootstrap over CV1 (a reliability ordering, hedged by its own authors, failing with few treated
clusters); interacted regression adjustment over unadjusted. Classical testing theory positively
rules out a total order. Manski's Law of Decreasing Credibility supplies a citable structural
criterion for the remainder, converting "fewer assumptions charged ranks higher" from a house rule
into a sourced principle.

Two D-05 hazards surfaced: Delacre, Lakens & Leys (2017) has a 2022 Correction listing six errors
including two simulation script errors, and Pustejovsky & Tipton (2018) has a 2023 Corrigendum. Both
invalidate specific numbers in papers the ontology will otherwise want to cite.

## Corrections Made

Three decisions were put to the user as decision blocks. All three were open questions the codebase
could not settle.

### Ontology size versus traceability

- **Original assumption:** implicit in the roadmap — 25–35 families, every one traceable to a case
  that needed it.
- **What the analysis found:** the two cannot both hold. All nine committed specs together declare
  six distinct procedure labels and three dependence structures. Phase 12 — the phase that grows the
  corpus — comes *after* Phase 11.
- **Options presented:** (A) keep 25–35, let `motivating_case` name planned but uncommitted Phase 12
  cases; (B) ship ~10–14 sized to committed evidence and amend the requirement; (C) keep 25–35 and
  write ~20 new fixtures inside Phase 11.
- **User chose:** B.
- **Recorded as:** `11-CONTEXT.md` D-01, D-02.
- **Dropped option, and why:** keeping 25–35 and deleting the traceability criterion — that
  criterion is the phase's only defence against the taxonomic-completeness padding `brief.md` warns
  about twice.

### Paradigm routing for a frame-layer check that cannot read the paradigm

- **Original assumption:** the frequentist-only scoping decision is made outside the adjudicator
  module. Confidence: **Unclear** — this was the only Unclear item in the analysis.
- **What the analysis found:** `dsx/frame/paradigm.py:55` already lists `"DSX-ADM-"` as
  paradigm-conditional under frequentist and `brief.md` §5.4 shows it as "not applied" for a Bayesian
  spec, but D-11 forbids the new module from reading the paradigm, and no shipped mechanism makes a
  frame-layer check paradigm-conditional.
- **Options presented:** (A) a helper in `dsx/frame/paradigm.py` answers whether the judge applies;
  `run_checks` passes it in; (B) move `"DSX-ADM-"` to the paradigm-independent list and let the
  frequentist-only ontology do the work, with a D-14 reversal record.
- **User chose:** A.
- **Recorded as:** `11-CONTEXT.md` D-22.
- **Deciding argument:** option B makes an honest `paradigm: bayesian` declaration draw a CRITICAL
  block, so misdeclaring as frequentist becomes cheaper than telling the truth — the exact inversion
  brief D-10 exists to block. It also breaks the invariant at `dsx/frame/paradigm.py:466-471`.

### Scope of the new test-name alias table

- **Original assumption:** flagged by the analyzer as a scope-boundary question for the human rather
  than a planner's judgement call.
- **What the analysis found:** `examples/known-bad/post-hoc-procedure-switch-ANALYSIS-SPEC.yaml:100`
  declares `fishers_exact` while `dsx/checks/stats.py:65` spells it `fisher_exact`; the mismatch
  currently fires `DSX-STA-041` at HIGH and is absorbed by `_INCIDENTAL_GAP_CODES`. Phase 10's D-06
  recorded that building a procedure vocabulary was out of scope *for Phase 10*; Phase 11 builds it.
- **Options presented:** (A) the new adjudicator is the only consumer; (B) wire into both
  `dsx/checks/stats.py` and `dsx/frame/prereg.py`; (C) wire into `dsx/frame/prereg.py` only.
- **User chose:** A.
- **Recorded as:** `11-CONTEXT.md` D-03.
- **Deciding argument:** ROADMAP SC 2 requires existing specs to behave unchanged. B and C both
  change a shipped firing set, which can silently invalidate suppressions operators have already
  written.

### Remaining assumptions

Presented as a group with the estimand-axis question flagged separately, because it coins a new
optional field in `ANALYSIS-SPEC.yaml` and is therefore a contract change rather than an
implementation detail. **User chose "Yes, proceed"** — take the remaining assumptions as decisions
and leave the estimand axis to the planner within the stated constraint that no fuzzy string match
on free prose may become the primary lookup path.

## Conflicts Recorded

Eight places where the planning documents contradict the shipped code. All are carried into
`11-CONTEXT.md` rather than left in this log.

1. `brief.md` D-03a's `Report`/`Finding` carve-out describes a state that never existed —
   `tests/test_frame_boundary.py:35` has no carve-out and the classes live in `dsx/findings.py`.
2. `.planning/research/ARCHITECTURE.md:101-102` asserts a symmetric import ban that no test enforces;
   `dsx/checks/*` importing `dsx.frame.*` would ship green. → `11-CONTEXT.md` D-04a.
3. `DSX-ADM-*` is declared paradigm-conditional in code that cannot see the paradigm. → resolved by
   user decision, D-22.
4. REQ-P11-01 keys families on estimand, but no estimand vocabulary exists and the one closed
   outcome vocabulary is unreachable under D-03a. → left to planner discretion within a constraint.
5. REQ-P11-06 names the M1 catalogue check as the enforcer; that check reads only Python syntax trees
   and docstrings and cannot import `dsx.loader`. → D-23.
6. ROADMAP SC 1's "the existing loader, no new parser" conceals that `load()` is two parsers that
   measurably disagree. → D-06, D-08.
7. ROADMAP SC 1's 25–35 count and SC 5's traceability criterion are jointly unsatisfiable against the
   committed corpus. → resolved by user decision, D-01/D-02.
8. Phase 10 D-06's scope boundary is live, with a concrete casualty in the Fisher spelling mismatch.
   → resolved by user decision, D-03.

Additionally, one live defect in an existing file: `references/test-selection.md` prescribes "Fisher
exact if any expected cell < 5", directly contradicted by Lydersen, Fagerland & Laake (2009) §9. That
file is uncited. → `11-CONTEXT.md` D-27.

## Auto-Resolved

Not applicable — this was an interactive run, not `--auto`.
