---
gsd_state_version: 1.0
milestone: v2.0.0
milestone_name: DSX Validity Frame
current_phase: 07
current_phase_name: validity-frame-checks-dsx-val
status: executing
stopped_at: Phase 9 context gathered (assumptions mode)
last_updated: "2026-08-12T15:32:43.578Z"
last_activity: 2026-08-12
last_activity_desc: Phase 07 execution started
progress:
  total_phases: 4
  completed_phases: 1
  total_plans: 31
  completed_plans: 18
  percent: 25
---

# Project state

**Status:** Ready to execute
**Progress:** [██████░░░░] 58% (1/7 phases — Phase 6 complete, 13/13 plans)  
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
- Phase 6 (M1, v2.0.0) — Contract extension, decision record, paradigm manifest. 13/13 plans, UAT 4/4, verification passed, security verified (35 threats, 0 open). Completed 2026-08-10.

## Next

- Phases 7/8/9 (M2a/M2b/M2c) — no hard ordering among themselves; listed order is catastrophe-prevention value per unit of work. Phase 7 is next up.
- Then Phase 10 (M3, soft-depends on 7), Phase 11 (M4, hard-depends on 7), Phase 12 (M5, terminal).
- Deferred, unchanged: Parquet profiler, live Glyph MCP, NLP decision_rule — out of scope for core gates.

## Accumulated Context

**Hard ordering constraints carried into planning:**

- Phase 6 blocks Phases 7–12. **Resolved** — Phase 6 complete 2026-08-10, so Phases 7–12 are unblocked.
- Phase 9's `DSX-PAR-010` and `DSX-PAR-011` are atomic (D-12): both ship or neither; the phase cannot close half-delivered. Note: 06-08 already committed both halves.
- Phase 7 precedes Phase 11 — admissibility is keyed on the dependence taxonomy.
- Phase 12 is necessarily last.

**Open items to resolve at phase discuss (do not decide silently):**

- Phase 7: `method_family_required` cannot express a disjunction under M-09's single-member reuse of `VARIANCE_ADJUSTMENTS`.
- Phases 7, 8, 11: final numeric code assignments beyond those the brief fixes (D-06 makes numbering irreversible).
- ~~Phase 9: whether the pre-existing `inflation_from_peeking()` docstring is upgraded to a full D-05 citation.~~ **Resolved 2026-08-12 at discuss** — yes, with an explicit unverified-locator flag (09-CONTEXT D-13). D-05 does not mechanically reach the function (no `report.add` call site), so this is elective; it is done because leaving it uncited puts a seam where a v2.0.0 check depends on a v1.5.0 computation. Anchor values verified by independent quadrature + Monte Carlo; the 1969 paper itself remains inaccessible, so **no table or page may be cited**.
- Phase 9: the "prior-averaged Ville bound" name is retired. **Corrected further 2026-08-12** — Deng Theorem 1 does **not** state `1/(K+1)`; it states an optional-stopping equality. The bound is unnumbered prose, §3.2 in its operational form. Verified against the arXiv LaTeX source (09-CONTEXT D-10). Ville's `1/k` remains a separate result, and Ville is never cited in Deng et al. at all (D-12). **REQ-P9-02/03 and ROADMAP Phase 9 SC 2/SC 3 still carry the old attribution and must be amended during planning.** The three regression guards in `tests/test_known_bad_corpus.py` hold the Deng-vs-Ville line and should be re-read, not assumed stale (UAT gap G-01).
- Phase 9: **new, surfaced at discuss** — omitting `inference.paradigm` (or the whole `inference:` block) produces no finding today (`dsx/spec.py:886-888`, `:917-919`), which becomes the cheapest escape from both halves of the pair the moment it ships. Mechanism preferred in 09-CONTEXT D-07; the severity question it raises is explicitly left for planning.

**Standing per-phase deliverables:**

- D-05 bar: primary-source citation naming the exact formulation + a test against a published reference value (or a named structural criterion).
- D-08: extend both canonical fixtures; the two exit-code tests stay unchanged.
- Register new modules in `GATE_PROFILES`; assert every new code is reachable from at least one profile.
- Emit decision records at each family's key judgment points (D-04).

## Current Position

Phase: 07 (validity-frame-checks-dsx-val) — EXECUTING
Plan: 1 of 7
Status: Ready to execute
Last activity: 2026-08-12 — Phase 07 execution started

## Project Reference

See: .planning/PROJECT.md (updated 2026-08-10)

**Core value:** Gate analytical work on validity before the data is touched.
**Current focus:** Phase 07 — validity-frame-checks-dsx-val

## Session

**Last session:** 2026-08-12T13:27:45.455Z
**Stopped at:** Phase 9 context gathered (assumptions mode)
**Resume file:** .planning/phases/09-monitoring-discipline-symmetric-dsx-par/09-CONTEXT.md

Note: a Phase 8 discuss ran concurrently on 2026-08-12 and produced
`.planning/phases/08-interference-triggering-stability-dsx-int/08-CONTEXT.md`. Phase 8 is
contexted but unplanned; Phase 7 is the active phase.

## Performance Metrics

| Plan | Duration | Tasks | Files |
|------|----------|-------|-------|
| Phase 06 P01 | 25min | 2 tasks | 3 files |
| Phase 06 P02 | 6min | 2 tasks | 2 files |
| Phase 06 P03 | 20min | 2 tasks | 3 files |
| Phase 06 P04 | 15min | 2 tasks | 3 files |
| Phase 06 P05 | 20min | 3 tasks | 4 files |
| Phase 06 P06 | 20min | 3 tasks | 3 files |
| Phase 06 P07 | 10min | 3 tasks | 6 files |
| Phase 06 P08 | 30min | 3 tasks | 7 files |
| Phase 06 P09 | ~10min | 3 tasks | 3 files |

## Decisions

- [Phase ?]: PEEKING_POLICIES.uncontrolled_continuous ships in Phase 6 (D-01); describe_vocabulary() now emits ALL dict-backed vocabularies as full key-sorted description dicts, not just peeking_policies
- [Phase ?]: dependence.method_family_required defines no parallel vocabulary; reuses VARIANCE_ADJUSTMENTS verbatim (M-09)
- [Phase ?]: invocation_id chosen over run_id (D-15); frame_digest lives on InvocationHeader only, not on every DecisionRecord
- [Phase ?]: check_d05() wired into gen-finding-catalogue.py --check; collect() module-label derivation fixed pre-emptively for dsx/frame/*.py (REQ-P6-11)
- [Phase ?]: PROJECT.md's version-rationale amendment is not a D-14 reversal — the sentence sits outside brief.md section 4's D-table and PROJECT.md's M-table, per 06-CONTEXT.md's explicit note
- [Phase ?]: Known limit and D-05 evidentiary-tiers content split into two README headings (## Known limits / ### Two tiers of evidentiary rigour) as distinct claims
- [Phase ?]: 06-05: good fixture uses cluster_robust and constraint_source:none (not brief's illegal literals) — M-09/CONSTRAINT_SOURCES compliance
- [Phase ?]: 06-05: bad fixture's validity_frame omits 6 of 10 sub-blocks and carries out-of-vocab defects on both new axes, no peeking-axis change (D-07)
- [Phase ?]: 06-05: Rule 1 fix — template claims[0].type retyped association->descriptive; DSX-COH-001 blocked gate plan on the unedited scaffold independent of validity_frame/inference
- [Phase ?]: 06-06: validity_frame/inference structural shape validators land, gated at CRITICAL from plan; membership comparison normalizes both value and vocab keys so MISSINGNESS_MECHANISMS' case-sensitive MCAR/MAR/MNAR match without a per-field special case (Rule 1 fix)
- [Phase ?]: 06-06: DecisionRecord emission is live for the first time — both new validators append layer=deterministic records onto report.context['decisions'], first real caller of dsx/decisions.py
- [Phase ?]: 06-06: Deng, Lu & Chen (2016) citation's exact section/theorem locator flagged unverified (escalated per D-05, not fabricated); author/title/venue/year confirmed against brief.md
- [Phase ?]: 06-07: DSX-PAR-001 paradigm manifest computes applied/not-applied check-family sets from a data-driven map (_PARADIGM_INDEPENDENT, _PARADIGM_CONDITIONAL keyed by every PARADIGMS member, _NOT_SHIPPED) rather than a paradigm branch — never blocks (INFO=10 < every default GATE_THRESHOLDS)
- [Phase ?]: 06-07: dsx/frame/ package created with D-03a import boundary enforced by an AST scanner proven against three deliberately violating sources; two Rule-1 fixes needed for gen-finding-catalogue.py compatibility (literal f-string title at call site, D-05 citation on check()'s own docstring)
- [Phase ?]: 06-08: known-bad corpus fixtures are full-shape clones of the good fixture (all validity_frame/inference blocks) rather than minimal specs, guaranteeing zero CRITICAL findings without per-field auditing
- [Phase ?]: 06-08: dsx validate (CRITICAL-only) confirmed as the acceptance bar for known-bad fixtures, not dsx gate ship — fixtures need no visuals/reproducibility/narrative sections
- [Phase ?]: 06-08: both halves of Phase 9's atomic DSX-PAR-010/DSX-PAR-011 pair committed (D-06); frequentist reference value 0.142 at 5 looks matches dsx.mathx.inflation_from_peeking exactly; Bayesian post-mortem states the prior-averaged Ville bound (K=19, ~0.05) against the point-null formulation it is not
- [Phase ?]: 06-08: Kohavi, Tang & Xu (2020) chapter locator for shared-budget interference flagged unverified, escalated for human confirmation rather than invented (T-6-16)
- [Phase ?]: 06-09: `explain` carries no `--block-on` at all (argparse exits 2) rather than accepting-and-ignoring it — a block flag on a command that always passes is a lie in the help text (D-04)
- [Phase ?]: 06-09: `add_common` gains keyword-only `include_block_on=True`, making "all four existing call sites unchanged" a property of the signature rather than a per-site re-verification
- [Phase ?]: 06-09: gate-path trail write is a side channel — an unwritable trail directory leaves every gate exit code untouched; a trail that cannot be written is a missing trail, not a failed gate (D-16/D-18)
