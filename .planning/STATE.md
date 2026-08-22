---
gsd_state_version: 1.0
milestone: v2.0.0
milestone_name: DSX Validity Frame
current_phase: 11.1.1
current_phase_name: detection-code-hardening-inserted
status: executing
stopped_at: Phase 11.1.1 re-scoped to an AST primary path (Option B) — 3 plans rewritten, design amended after a 4-blocker adversarial pass, execution not yet resumed
last_updated: "2026-08-22T01:43:26.499Z"
last_activity: 2026-08-21
last_activity_desc: Phase 11.1.1 execution resumed (wave continue)
progress:
  total_phases: 10
  completed_phases: 6
  total_plans: 63
  completed_plans: 56
  percent: 60
---

# Project state

**Status:** Ready to execute
**Progress:** [██████████████████░░] 56/63 plans (89%)  
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
- Phase 9 (M2c, v2.0.0) — Monitoring discipline, symmetric (`DSX-PAR-010`/`-011` plus membership-free `DSX-PAR-002`). 7/7 plans, UAT 1/1 (split accepted), verification passed, security verified (24 threats, 0 open). Completed 2026-08-13.
- Phase 7 (M2a, v2.0.0) — Validity frame checks (`DSX-VAL-*`), ten codes: estimand completeness/falsifiability, unit triad, dependence method family, identification strength, sampling frame, missingness, measurement. 8/8 plans, UAT 38/38, re-verification passed 5/5 success criteria, security verified (0 open threats). Completed 2026-08-20.
- Phase 8 (M2b, v2.0.0) — Interference, triggering, stability (`DSX-INT-010`/`-011`/`-030`/`-040`). 10/10 plans, verification passed 6/6 must-haves. The out-of-vocabulary `interference.risk` bypass is closed (08-10): the risk-vocabulary clause is gone from `_check_interference_mitigation_admissibility`'s guard, so a misspelled risk with a channel-inadmissible mitigation now fires `DSX-INT-011` at CRITICAL instead of clearing the gate. Security not yet run. Completed 2026-08-14.

## Next

- Phase 7 (M2a) — **complete 2026-08-20**. Re-verification passed: 5/5 roadmap success criteria, 8/9 requirements MET, REQ-P7-08 PARTIAL by the deliberate D-06 scope decision (not a gap). Both prior `human_needed` items (Chan & Perry 2017 citation admissibility; the two D-05 honesty disclosures) were closed by recorded human verdicts in `07-UAT.md` (38/38 pass, 0 gaps). Security verified, 0 open threats. Outstanding, non-blocking: 07-REVIEW.md CR-01 (an out-of-vocabulary `inference.paradigm` made the `DSX-PAR-001` manifest contradict `DSX-PAR-010`/`-011` and silenced `DSX-PAR-002`) is **fixed 2026-08-20** in `dsx/frame/paradigm.py` — both readers now fold an unrecognised value into the undeclared case, matching `_check_monitoring_discipline`; suite 549 OK. Still open: WR-01 (`val.py::check()` hand-duplicates each `_check_*` blocking predicate with no drift test).
- Phase 8 (M2b) — **complete 2026-08-14**, verification passed 6/6. Outstanding, non-blocking: `/gsd-secure-phase 08` has not been run (security enforcement is active), and 08-REVIEW.md carries two WARNING findings (WR-01 self-contradictory DSX-INT-011 remedy text for an out-of-vocabulary risk; WR-02 `design.alpha: 0` silently defaulted in `dsx/frame/paradigm.py`).
- Then Phase 10 (M3, context re-verified 2026-08-14, 6 unexecuted plans already on disk, soft-depends on 7), Phase 11 (M4, hard-depends on 7), Phase 12 (M5, terminal).
- Inserted 2026-08-20 (paper-evaluation integration, Option A): Phases 11.1 (generated-pipeline reality), 11.2 (prescriptive claim layer), 11.3 (reporting completeness / missing-data discipline) run after Phase 11 and before Phase 12 — the catch rate Phase 12 measures must cover their checks and the full-frame-cleaning corpus case (REQ-P11.1-07).
- Deferred, unchanged: Parquet profiler, live Glyph MCP, NLP decision_rule — out of scope for core gates.

## Accumulated Context

**Hard ordering constraints carried into planning:**

- Phase 6 blocks Phases 7–12. **Resolved** — Phase 6 complete 2026-08-10, so Phases 7–12 are unblocked.
- Phase 9's `DSX-PAR-010` and `DSX-PAR-011` are atomic (D-12): both ship or neither. **Resolved** — both shipped in 09-03 at CRITICAL; phase closed 2026-08-13.
- Phase 7 precedes Phase 11 — admissibility is keyed on the dependence taxonomy.
- Phase 12 is necessarily last.
- Phases 11.1–11.3 (inserted 2026-08-20) precede Phase 12 — the corpus case REQ-P11.1-07 and the checks that catch it must exist before the catch rate is measured.

**Open items to resolve at phase discuss (do not decide silently):**

- Phase 7: `method_family_required` cannot express a disjunction under M-09's single-member reuse of `VARIANCE_ADJUSTMENTS`.
- Phases 7, 8, 11: final numeric code assignments beyond those the brief fixes (D-06 makes numbering irreversible).
- Phases 11.1–11.3: final numeric code assignments (D-06).
- Phase 11 (discuss): per-spec vs per-hypothesis adjudication — the one-row-per-hypothesis container from the 2026-08-20 paper evaluation is UNVERIFIED; run a verification spike before writing any requirement on it.
- Phase 11.3 (discuss): missingness-rate reconciliation against the profile — the naive version fires on the good fixture; redesign with tolerance + re-baseline, or defer with an entry condition.
- ~~Phase 9: whether the pre-existing `inflation_from_peeking()` docstring is upgraded to a full D-05 citation.~~ **Resolved 2026-08-12 at discuss** — yes, with an explicit unverified-locator flag (09-CONTEXT D-13). D-05 does not mechanically reach the function (no `report.add` call site), so this is elective; it is done because leaving it uncited puts a seam where a v2.0.0 check depends on a v1.5.0 computation. Anchor values verified by independent quadrature + Monte Carlo; the 1969 paper itself remains inaccessible, so **no table or page may be cited**.
- Phase 9: the "prior-averaged Ville bound" name is retired. **Corrected further 2026-08-12** — Deng Theorem 1 does **not** state `1/(K+1)`; it states an optional-stopping equality. The bound is unnumbered prose, §3.2 in its operational form. Verified against the arXiv LaTeX source (09-CONTEXT D-10). Ville's `1/k` remains a separate result, and Ville is never cited in Deng et al. at all (D-12). **REQ-P9-02/03 and ROADMAP Phase 9 SC 2/SC 3 still carry the old attribution and must be amended during planning.** The three regression guards in `tests/test_known_bad_corpus.py` hold the Deng-vs-Ville line and should be re-read, not assumed stale (UAT gap G-01).
- ~~Phase 9: omitting `inference.paradigm` produces no finding.~~ **Resolved in 09-03** — undeclared paradigm selects every `_MONITORING_DISCIPLINE` row, so both CRITICAL codes fire at `plan`.
- Phase 9 D-08 (`DSX-PAR-002` membership-free; `DSX-SPEC-085` owns vocabulary): **accepted at UAT 2026-08-13**. ROADMAP SC 4 and REQ-P9-04 now name both codes.
- Phase 10: numeric code assignments **resolved 2026-08-13 at discuss** — `DSX-PRE-010` (rule does not resolve to exactly one branch), `-020` (recorded plan-time `frame_digest` differs from verify-time bytes while `declared_at: pre_data` is claimed), `-030` (executed procedure differs from the selected branch, both labels named). `-011` deliberately unspent; the unparseable-rule case carries no code at all and is exit 2 (10-CONTEXT D-12, D-02). Note this phase was not named in the numbering open item above — it is recorded here because brief D-06 makes numbering irreversible. **Shipped 2026-08-20** — all three ship at CRITICAL: `DSX-PRE-010` owns the fallback rule not resolving to a branch (10-02), `DSX-PRE-020` owns the recorded plan-time `frame_digest` differing from verify-time bytes while `declared_at: pre_data` is claimed (10-03), `DSX-PRE-030` owns the executed procedure differing from the declared branch with both labels named (10-02).
- Phase 10: **new, surfaced at discuss** — reading the plan-time content lock promotes `DECISIONS.jsonl` from side channel to gate input, narrowing the unconditional invariant at `dsx/cli.py:285-289` to the write path. A `verify` with no recorded `plan` header exits `2`, which collides with the M-07 grandfather path; the exit-2 message must name `suppressions[]` so that path stays walkable (10-CONTEXT D-09). **Do not solve this by making the missing header pass.** Locked 2026-08-14: compare by set membership over all recorded plan-time digests; missing-header exit 2 is `gate_invocation`-only (`dsx check` / `dsx audit` stay silent); `_gate_findings` must be repaired in the same commit as `GATE_PROFILES`.
- Phase 10: fact registry locked 2026-08-14 as D-04a — exactly three scalars (`alpha`, `interim_looks`, `comparisons_looked_at`). Discretion items from the 2026-08-13 discuss are now locked in `10-CONTEXT.md`; do not re-open them at execute.
- Phase 10: `_D05_ALLOWLIST_PREFIXES` (`scripts/gen-finding-catalogue.py:65`) is an **inclusion** list, not an exemption list, and does not cover `DSX-PRE-`. Without that edit the brief-D-05 citation gate is silently disabled for this family and `--check` still passes (10-CONTEXT D-13 item 4).
- Phase 10: `brief.md` §7 names no pre-registration source and gains the Gelman & Loken (2014) anchor — a citation addition where none existed, not a brief-D-14 reversal (10-CONTEXT D-14). **Resolved 2026-08-20** — `brief.md` §7 now carries the Gelman & Loken (2014) anchor, both locator warnings intact, plus the Simmons, Nelson & Simonsohn (2011) and Nosek, Ebersole, DeHaven & Mellor (2018) secondary sources, each with its own scope note (10-06).
- Phase 10: two decisions left to the planner's discretion, settled at execute 2026-08-20 (10-06) — the content-lock comparison is set membership over every recorded plan-time digest rather than a most-recent or earliest pick, because `InvocationHeader` records no specification identity and any ordering rule produces cross-specification false positives in a shared trail directory; and trail reconciliation is scoped to a real `dsx gate` invocation only, because the read-only inspection commands (`dsx check`/`dsx audit`) never write a trail and could therefore never satisfy the precondition.

### Phase 11.1.1 re-scope (2026-08-21)

Mechanism changed from hand-patching the regular-expression text scanner to an `ast.parse`
primary path with the text scan retained as a visible fallback (owner decision, Option B).
Driver: the shipped scanner scored 3/12 on a session-time variant probe against 12/12 for a
stdlib proof of concept, and two of the misses were **false positives** — a module docstring
or a notebook markdown cell that merely describes leakage blocks byte-identical code. Phase 12
publishes a false-positive rate, so those would have been measured.

Three adversarial lenses returned `design-needs-amendment` with four blockers (notebook line
geometry, undecodable-entrypoint silent pass, `splitlines()` vs tokenizer line axis, prose
mask eating a closing line). All four are discharged in the rewritten plans;
`11.1.1-AST-DESIGN.md` carries an amendment banner naming each and its owning plan. Original
plans preserved under `superseded/`. ROADMAP success criteria amended to six (false-positive
parity and visible-fallback criteria added).

**Execution not yet resumed** — stopping at re-planned was the explicit instruction.

### Roadmap Evolution

- Phase 11.1 inserted after Phase 11 (2026-08-20): Generated-pipeline reality — closes the live gate bypass reproduced in the paper evaluation (URGENT)
- Phase 11.2 inserted after Phase 11.1 (2026-08-20): Prescriptive claim layer — recommendations become checkable
- Phase 11.3 inserted after Phase 11.2 (2026-08-20): Reporting completeness and missing-data discipline

**Standing per-phase deliverables:**

- D-05 bar: primary-source citation naming the exact formulation + a test against a published reference value (or a named structural criterion).
- D-08: extend both canonical fixtures; the two exit-code tests stay unchanged.
- Register new modules in `GATE_PROFILES`; assert every new code is reachable from at least one profile.
- Emit decision records at each family's key judgment points (D-04).

### Quick Tasks Completed

| # | Description | Date | Commit | Status | Directory |
|---|-------------|------|--------|--------|-----------|
| 260821-d6h | Deepen dsx-explore-data into an insight-driving EDA protocol (branches, ledgers, spec reconciliation, EDA.md template) | 2026-08-21 | 40e015d | Verified | [260821-d6h-deepen-dsx-explore-data-into-an-insight-](./quick/260821-d6h-deepen-dsx-explore-data-into-an-insight-/) |

## Current Position

Phase: 11.1.1 (detection-code-hardening-inserted) — EXECUTING
Plan: 1 of 3
Status: Ready to execute
Last activity: 2026-08-21 — Phase 11.1.1 execution resumed (wave continue)

## Project Reference

See: .planning/PROJECT.md (updated 2026-08-13)

**Core value:** Gate analytical work on validity before the data is touched.
**Current focus:** Phase 11.1.1 — detection-code-hardening-inserted

## Session

**Last session:** 2026-08-20T16:17:45.031Z
**Stopped at:** Phase 11 planning complete — 8 plans, checker passed, ready to execute
**Resume file:** .planning/phases/11-frequentist-admissibility-adjudicator-dsx-adm/11-01-PLAN.md

Phase 10 context was re-verified 2026-08-14 (assumptions mode). Six unexecuted plans (`10-01` … `10-06`) already exist; this refresh did not rewrite them. Phase 8's blocking gap is in `08-VERIFICATION.md` (out-of-vocabulary `interference.risk` bypass).

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

## Session Continuity

Last session: 2026-08-21T20:32:49.273Z
Stopped at: Session resumed via /gsd-resume-work — context restored from the Phase 11.1.1 handoff; awaiting selection of next action (primary: execute Phase 11.1.1).
Resume file: .planning/phases/11.1.1-detection-code-hardening-inserted/.continue-here.md
