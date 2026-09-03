# Milestones

## v2.4 Visual Excellence (Shipped: 2026-09-03)

**Phases completed:** 4 phases (21–24), 11 plans

**Delivered:** a chart-and-style visual-excellence layer on top of v2.3's test
catalogue. Phase 21 reconciled the inherited chart-type vocabulary — every mark
now has a capability home, `BANNED_TYPES` refusal entries enriched in place to
full `{reason, code, citation}` records. Phase 22 built a merged catalog spine
(81 rows spanning five named taxonomies), a Wilke-sourced 10-mark uncertainty
vocabulary family, and a 5-layer chart-selection heuristic (mints `DSX-VIZ-071`).
Phase 23 shipped a license-audited analyst-side style layer (four `.mplstyle`
files, one vendored OFL font) with a proven SVG-determinism recipe (off-gate-path
double-render hash-equality test) and a snippet catalog that routes to existing
codes rather than restating thresholds — zero new codes minted. Phase 24 proved
the whole stack end-to-end: the existing onboarding-activation exemplar upgraded
in place with a real 95%-CI uncertainty figure, a sealed manifest, and the
project's first bad-chart-choice fixtures.

Milestone audit `passed` (16/16 requirements, 4/4 phases, 5/5 integration seams,
0 critical gaps); finding catalogue grows 275 → 276 codes, additively; full
suite green throughout (1471 → 1508 tests). Independent primary-source
verification (mirroring v2.3's discipline) caught two classes of defect before
ship: a citation round (HQ-27, 5 parallel research agents) found 7 of 13
proposed citations needed correction, including a perceptual-ranking claim with
no support in either cited paper — Cleveland & McGill (1984) publish 6 ranks
with ties, not the proposed 7-item strict order; and a license-audit round
(HQ-33) found the house-default style's palette was mislabeled — claimed
Apache-2.0/Urban Institute, actually GPL-3.0-disputed with 3 of 6 colors being
unattributed ColorBrewer stops.

---

## v2.3 Test Catalog (Shipped: 2026-09-02)

**Phases completed:** 4 phases (17–20), 11 plans

**Delivered:** the statistical-test decision surface expanded from ~15 to ~75 rows
across 11 categories (correlation/association, agreement/reliability, repeated
measures, trend, categorical, resampling, variance/scale, proportions, counts,
post-hoc, power conventions), backed by 15 new declaration-only gate checks under
full D-05 citation discipline — every citation independently re-verified against
primary sources in an interactive session before shipping (27 citations checked,
7 corrected, including one real defect: a proposed Krippendorff-alpha fixture value
that didn't actually appear anywhere in its cited paper). Milestone audit `passed`
(22/22 requirements, 0 unsatisfied/orphaned); finding catalogue grows 260 → 275
codes, additively, with the frozen Phase-12 snapshot unmutated.

**Key accomplishments:**

- Reconciled a live Boschloo doc/code divergence (the reference doc already prescribed the correct small-cell fallback; `recommend_test` still emitted the wrong one) by fixing the routing table to match, pinned by a new regression test. No new finding codes.
- Pinned the `time_to_event` → log-rank unconditional fallthrough with a behavioural + source-scan regression test, so future outcome-type rows cannot silently change routing.
- Added the `estimand_kind` closed spec vocabulary (6 members, including the D-06/D-12a-disposed `nominal_association`) and a shared `DSX-STA-040` declaration-completeness guard, with the D-05 allowlist and doc mirror landing in the same commit.
- Correlation/association routing (`recommend_association`) plus a five-code declaration-only gate (`DSX-STA-050/051/060/061/062`, all HIGH) covering scale/kind mismatches, agreement-vs-correlation routing, and ICC/kappa declaration completeness — catalogue to 265.
- Report-only correlation/agreement effect-size bands (kappa, ICC, Kendall's W, Krippendorff) added to `dsx/mathx.py` as labeled conventions — the blocking `EFFECT_SIZE_KINDS` domain stays frozen at `{d, h, r}`; bands wire only into the ungated APA template.
- Eight closed Phase-19 declared sub-vocabularies, `POSTHOC_FAMILY_MAP`, and seven dataless `recommend_*` routing functions (repeated measures, trend, resampling, post-hoc, variance role, power, proportion CI) — all keyed on declared context only, extending the anti-two-stage doctrine to six new families.
- Ten HIGH declaration-only gate codes (`DSX-STA-070/080/081/090/100/110/111/120/121/122`) covering two-stage sphericity, undeclared dose scores/autocorrelation handling, incomplete resampling quadruples, post-hoc/omnibus family mismatches, variance-test-as-precondition, observed-power-in-a-readout, Wald-for-proportion, and undeclared exposure offsets — each with its own attributable citation docstring (no shared-block citation laundering). Catalogue to 275.
- Five dedicated known-bad fixtures and three good-corpus negative controls for the Phase-18 codes (which fired nowhere in `examples/` before), making the false-positive rate a real negative control rather than a vacuous pass.
- The single calibration harness (`test_stratified_catch_rate_and_fpr_report`) extended with a live HIGH verify/ship stratum — computed from real gate findings, never from the golden-ship reference set (D-09 no-self-reference) — since the 15 new HIGH milestone codes are otherwise a provable no-op on the existing CRITICAL/plan-execute-only stratum.
- The no-autoswitch structural guard made category-complete across every new routing family, plus a fallthrough-position regression test.
- A read-only doc/code agreement cross-check (`test_doc_code_agreement.py`) binding `references/test-selection.md`'s decision-table rows to the live `recommend_test`/`recommend_*` engines by strict cell equality — the exact structural gap the Boschloo divergence exploited, now closed permanently rather than just repaired once.

---

## v2.2 Analytic Surface (Shipped: 2026-08-29)

**Phases completed:** 4 phases (13–16), 20 plans

**Delivered:** the operator-surface gap closed without turning DSX into a prompt pack —
four new router skills (`dsx-cohort`, `dsx-funnel`, `dsx-root-cause`, `dsx-segment`)
that point marketing cohort/funnel/diagnostic work at existing gates instead of
restating them; a compounding-learnings search step and a portable data dictionary
for onboarding; CUPED as a declared, gated variance adjustment with a post-treatment-
covariate check (`DSX-EXP-070`, CRITICAL) and a changing-denominator BI check
(`DSX-MET-021`, HIGH), both under full D-05 primary-source citation discipline; and
off-gate-path re-run verification via the new `dsx-reproduce` skill (`DSX-REP-060`/
`061`, both HIGH). Milestone audit `passed` (23/23 requirements, 0 unsatisfied/orphaned);
finding catalogue grows 256 → 260 codes, additively, with the frozen Phase-12 snapshot
unmutated.

**Closeout:** verified_closeout — all 4 phases technically verified (`threats_open: 0`
per phase) and human-signed-off (HUMAN-QUEUE HQ-9/10/12/14); 0 real gaps. REQ-P15-04
is satisfied **as worded**, via its own stated escape clause: the survivorship-bias
citation (Brown, Goetzmann, Ibbotson & Ross 1992) was read directly and found not to
transfer to a declaration-checkable rule, so only the changing-denominator half ships
— a documented, loud partial, not a silent scope cut (see HQ-8). 2 dormant seeds
(SEED-001, SEED-002) carried forward again, unchanged from v2.0.0's close.

**Key accomplishments:**

- Two new router `SKILL.md` files (`dsx-cohort`, `dsx-funnel`) that point marketing cohort/funnel work at the existing metric, chart-matrix, and coherence gates instead of restating them, plus a four-name append to `capability.json` registering all four Phase 13 playbooks.
- Two more router playbooks — `dsx-root-cause` routes diagnostic decomposition to `DSX-MET-030/031` and the causal-honesty guard; `dsx-segment` routes multi-cut segmentation to the multiplicity gate (`DSX-SPEC-043`, `DSX-EXP-050..053`) — both citing existing gates with zero authored thresholds.
- `dsx-explore-data` gains a hypothesis register mapping untested beliefs to `assumptions[]` and promoted beliefs to `results.tests[]`; `dsx-narrate` gains an explicit What / So What / Now What shape. Neither mints a code or a schema field.
- `dsx-scope-analysis` routes lookup/ad-hoc/full-pipeline work to GSD tiers 0/1/2, advisory-only (prints the tier command, mutates nothing); the executor fragment now prefers a `scripts/*.py` entrypoint over a notebook, framed as ordering fidelity (`DSX-REP-040`), not a leakage claim.
- Wave-2 certification that Phase 13 mints zero new `DSX-*` codes — a set-identity diff (D-07), not just a count, closing the mint-one/drop-one swap hole a count alone leaves open.
- Compounding loop: `dsx-explore-data` now searches dated learnings under `docs/dsx/learnings/` before framing a new analysis (REQ-P14-01).
- A portable `DATA-DICTIONARY.md` template sits next to `DATA-PROFILE.yaml` so later sessions do not re-guess grain and join keys (REQ-P14-02).
- Research-domain AI-assistance disclosure: when `dsx.domain == research`, `dsx-narrate` offers an optional, opt-in disclosure block; the marketing-domain default is unchanged (REQ-P14-03).
- CSV-first slash-command aliases across the DSX skills, plus a documented, honest skip of the file-drop hook — no GSD Core overlay hooks exist to wire it to (REQ-P14-04/P14-05).
- Zero-mint proof for Phase 14 by catalogue diff, plus a gate-path hermeticity guard keeping the check surface stdlib-pure and profiler-free (REQ-P14-06).
- CUPED lands in `dsx/spec.py`'s closed vocabulary — `design.variance_adjustment: cuped` no longer draws a stray `DSX-SPEC-044` — as the phase's trap-12 keystone. No mint.
- `DSX-MET-021` (HIGH): a metric pooled across cohort-comparison buckets sampled at different rates with no reweighting declared — the changing-denominator half of REQ-P15-04.
- An optional APA-style research results table (`templates/APA-TABLE-research.md`) plus a test proving the gate never silently auto-switches statistical tests on normality grounds.
- `DSX-EXP-070` (CRITICAL): CUPED declared with a covariate that is not pre-experiment now blocks at the gate, backed by θ = Cov/Var and ρ² variance-reduction helpers citing Deng, Xu, Kohavi & Walker (2013) WSDM by DOI, computed off the gate path.
- The good-fixture example spec extended to declare CUPED correctly and well-behaved cohort comparisons, proven silent at every threshold Phase 15 adds. No mint.
- Finding catalogue regenerated to 260 codes — `DSX-EXP-070` and `DSX-MET-021` added to the D-05 citation allowlist as exact strings; the invariant test rebaselined additively (258→260) without touching the frozen Phase-12 snapshot at 256.
- `DSX-REP-060`/`DSX-REP-061` (both HIGH) — a declared `reproduce_report` with a missing `REPRO-REPORT.md`, or one present whose re-run numbers don't overlap `results.tests`, now blocks at the gate. Phase 16's only catalogue mint.
- The `dsx-reproduce` skill and its `REPRO-REPORT.md` contract template, registered as the capability's 14th skill.
- `protocol_adherence` sidecars added to the three known-bad `ATTRIBUTION.yaml` fixtures, plus an additive test proving the new field changes no existing verdict.
- A static AST no-entrypoint-execution guard — the execution-detecting complement to the existing gate-path-hermeticity test, flagging the full subprocess/`os.system`/exec/spawn family anywhere in the check surface.

---

## v2.0.0 DSX Validity Frame (Shipped: 2026-08-28)

**Phases completed:** 11 phases, 89 plans, 208 tasks

**Delivered:** the full DSX validity-frame gate — estimand/unit/dependence/identification/sampling/missingness/measurement (`DSX-VAL-*`), interference and dilution (`DSX-INT-*`), the symmetric paradigm monitoring pair (`DSX-PAR-*`), the pre-registered inference plan with declared-vs-executed branch reconciliation (`DSX-PRE-*`), frequentist procedure admissibility over 14 cited families (`DSX-ADM-*`), the prescriptive-claim layer, reporting-completeness / missing-data discipline, and a calibration corpus with a measured catch rate and false-positive rate. Milestone audit `passed`; 256-code finding catalogue.

**Closeout:** override_closeout — 2 dormant seeds deferred (SEED-001, SEED-002; see STATE.md Deferred Items). All 75 requirements accounted, 0 unsatisfied.

**Key accomplishments:**

- `dsx/loader.py` `_NULL` stops swallowing the literal `none`; `dsx/spec.py` gains ten new closed vocabularies, an `uncontrolled_continuous` peeking policy, and a registry-driven `describe_vocabulary()` that stops discarding descriptions
- Stdlib-only `dsx/decisions.py` — the first write path in a read-only codebase: crash-safe JSONL append via flush()+os.fsync(), a tolerant line-by-line reader, and deterministic invocation/frame-digest identity, with no caller wired yet.
- `scripts/gen-finding-catalogue.py --check` now fails the build when a check covered by a finite, visible D-05 allow-list lacks a `Citation:` line, a `Reference value:`/`Structural criterion:` line, or a linked test — proven against a committed violating fixture, with zero new failures across the 206 pre-existing finding codes.
- Created `.planning/REVERSALS.md` with the D-14 reversal template and SELF-001 convention, documented the `suppressions[]` migration path and the known limit in README.md, and corrected PROJECT.md's version rationale to match D-10's CRITICAL/plan gate point — three files, zero code.
- `examples/good-ANALYSIS-SPEC.yaml` and `examples/bad-ANALYSIS-SPEC.yaml` gain the full `validity_frame:`/`inference:` contract surface (extended, not replaced) and `templates/ANALYSIS-SPEC.yaml` scaffolds both blocks in full — all three still pass their pre-existing gate contracts, and nothing reads the new fields yet
- `_validate_validity_frame_shape()` and `_validate_inference_shape()` land in `dsx/spec.py`, making `validity_frame:` requiredness and both blocks' closed vocabularies enforceable at `dsx gate plan` — the contract becomes a gate, not documentation, and both validators emit the project's first real `dsx/decisions.py` decision records.
- `dsx/frame/` lands with an AST-enforced import boundary and `DSX-PAR-001`, the informational paradigm manifest, registered at all four gate points — the first frame check, and the first code to compute check-family applicability from data keyed by every declared analysis paradigm rather than a frequentist-default branch.
- `examples/known-bad/` ships three real-failure spec+post-mortem pairs — shared-budget interference, uncontrolled-continuous-monitoring frequentist, and the same under Bayesian paradigm — plus `tests/test_known_bad_corpus.py`, giving Phase 8 and both halves of Phase 9's atomic pair a committed target before either phase is written.
- `dsx gate` writes a sequentially-id'd decision trail and `dsx explain` renders it, with the write wired as a side channel that no failure mode can turn into a gate verdict
- Package version 2.0.0 across all four declaration sites and both committed repro_lock fixtures, finding catalogue confirmed current (211 codes, all new DSX-SPEC-08x/DSX-PAR-001 rendered), and the six-invocation closing phase gate re-run together for the first time — 270 tests, all gate/validate/explain/vocab checks pass
- `dsx/decisions.py::read_all()` cannot raise for any on-disk state of `DECISIONS.jsonl`, and both `dsx/cli.py` call sites contain every exception below `BaseException`, closing the Phase 6 verification BLOCKER (verified truth 3b) with 9 committed regression tests observed failing before the fix
- Rewrote a false, committed claim that today's `dsx validate`/`gate` checks pass all three `examples/known-bad/` fixtures at every gate and severity threshold, and pinned the corrected claim with four new gate-driving tests measured directly against the real CLI.
- Closed WR-03/WR-01/IN-01 from 06-REVIEW.md: the D-05 allow-list is now hyphen-safe with an exact-code set, `dsx/spec.py`'s inference-field comment states only what the code enforces, and a test helper's dead branch was collapsed to one expression — zero behavior change, zero new finding codes, catalogue byte-unchanged.
- Dependence-to-method-family map, falsifier placeholder/refusal lexicon, and a Cochrane-cited design-effect helper — the three pieces `dsx/frame/val.py`'s nine checks will import, landed with 18 new tests before any check exists to read them.
- Extended brief.md section 7 with six new D-05 citation sources and two pinned editions, and replaced the unpublished 3.45 design-effect worked example in .planning/research/FEATURES.md with the Cochrane Handbook's own 1.576 value.
- `dsx/frame/val.py` ships as the family's first module — estimand completeness (`DSX-VAL-010`, CRITICAL) and estimand falsifiability (`DSX-VAL-011`, HIGH), registered in the plan/verify/ship gate profiles, with the not-shipped-map removal, catalogue prefix-group entry, D-05 allow-list prefix, and the D-11 paradigm-read boundary test all landing in the same two commits the invariant tests force.
- `dsx/frame/val.py` gains the unit triad (`DSX-VAL-020`, CRITICAL — pseudo-replication with no method family, quantified via `dsx.mathx.design_effect`'s Cochrane worked value 1.576) and unit drift (`DSX-VAL-021`, HIGH — validity-frame vs design-block unit disagreement), landing in the same commits as repairs to the template and the interference known-bad fixture that the new check would otherwise have broken, plus a structural proof that `DSX-VAL-020` and `DSX-EXP-021` can never both fire on one defect.
- `dsx/frame/val.py` gains the dependence check (`DSX-VAL-030`, CRITICAL — a declared dependence structure with no admissible method family, naming the full admissible set at the point of failure) and the identification pair (`DSX-VAL-040` CRITICAL for weak identification with no constraint, `DSX-VAL-041` HIGH for strong identification also carrying a project-defined parameter-scale constraint), landing in the same commits as repairs to the template and the bayesian corpus fixture's documentation that the new checks would otherwise have broken, plus a gate-level proof that the roadmap's severity-split wording — `DSX-VAL-041` printed but non-blocking at plan, blocking at verify/ship — actually holds through the real CLI.
- 1. [Rule 1 - Bug] `report.add()`'s severity argument for DSX-VAL-060 had to be a literal, not the `severity` variable from the pairing table
- 1. [Rule 1 - Bug] Corrected the plan's own acceptance-criteria import path
- Reconciled dsx/frame/val.py, dsx/mathx.py and brief.md onto one Kish (1965) locator set (section 8.2, page 258, pages 161-162), narrowed the honesty disclosure to name only the design-effect formula's section number as unverified, and added an AST-derived cross-file invariant test that would have caught the original contradiction.
- `dsx.mathx.diluted_effect` lands Deng & Hu (2015) Formula (1) as a pure additive-metric function, range-validated and proven against the paper's own additive-vs-ratio counterexample, never wired into any gate path.
- Rewrote the known-bad corpus's family-prefix guarantee into a per-fixture target-defect map, fixed four fixtures' dishonest stability declarations, and committed the triggering-dilution fixture pair DSX-INT-030 will be measured against.
- Task 1 — the module, in one commit.
- Shipped `DSX-INT-030` — an additive metric (count/sum/average) analysed on the eligible population with no declared dilution adjustment, cited to Deng & Hu (2015) Formula (1) and scoped away from ratio/rate metrics by a partition over `dsx.spec.METRIC_TYPES` — and rewrote `brief.md` section 6.5's ratio-metric dilution row to name the real per-user-data blocker instead of the access premise research proved false.
- Shipped `DSX-INT-040` — the interference family's fourth and only non-CRITICAL code, firing HIGH on an unassessed or unevidenced novelty/primacy declaration and blocking `verify`/`ship` by severity alone — with its disjointness statement against `DSX-EXP-030`, then hardened the finished four-code module against every malformed sub-block shape it can be handed, finding and fixing one genuine pre-existing crash along the way.
- Reworded ROADMAP.md Phase 8 success criteria 3 and 4, and REQUIREMENTS.md's REQ-P8-04, so both documents state a Phase 8 bar that is achievable and matches what the Deng & Hu (2015) paper actually says and what the code actually does — and, discovering the same disproven premise repeated a second time in REQUIREMENTS.md's Out of Scope table, corrected that too.
- Closed the DSX-INT-010/DSX-INT-011 out-of-vocabulary-mitigation gate bypass (08-REVIEW.md CR-01) with a RED-then-GREEN commit pair, plus three warning-level test/audit-completeness fixes (WR-01, WR-02, WR-03, WR-04, IN-02) and IN-01 recorded as deferred.
- Closed the second instance of the 08-REVIEW.md CR-01 gate-bypass class — an out-of-vocabulary `interference.risk` string (e.g. `shared_buget`) no longer clears `dsx gate plan` for a declared, unmitigated interference risk — with a RED-then-GREEN commit pair mirroring plan 08-07's fix on the adjacent `mitigation` field.
- Closed 08-VERIFICATION.md's second failed truth — an out-of-vocabulary `triggering.analysis_population` string (e.g. `eligable`) no longer bypasses `DSX-INT-030` — with a RED-then-GREEN commit pair mirroring plans 08-07/08-08's fix shape, then tightened the one remaining weak-assertion warning (08-REVIEW.md WR-01) with a mutation-proven structured-findings rewrite.
- Dropped the vocabulary-membership clause from `_check_interference_mitigation_admissibility`'s risk guard so a misspelled `interference.risk` paired with a real, recognised, channel-inadmissible mitigation fires DSX-INT-011 instead of clearing the gate silently; corrected the three prose sites that described the old routing; added a unit-level and a gate-level disjointness grid as permanent regression guards.
- Committed the pre-code `DSX-PAR-010`/`DSX-PAR-011` symmetry audit, extended `_INFERENCE_FIELDS` to nine members with `dsx vocab` discovery, and seeded an empty per-fixture expected-caught-defect map in the known-bad corpus suite — no new finding codes ship yet.
- `inflation_from_peeking()` now carries a full Armitage, McPherson & Rowe (1969) citation with an honest unverified-locator flag, and a new stdlib-only seeded unittest module proves DSX-PAR-010's point-null trend and DSX-PAR-011's prior-averaged 1/(K+1) ceiling are genuinely different results.
- Shipped `DSX-PAR-010` (frequentist) and `DSX-PAR-011` (bayesian) — both CRITICAL, both from one data-driven `_MONITORING_DISCIPLINE` map evaluated by one shared clearing predicate — closing the paradigm-retype and undeclared-paradigm escapes without spending a new finding code.
- Rewrote the two monitoring fixtures' spec headers and post-mortems to state what `DSX-PAR-010`/`DSX-PAR-011` now catch instead of claiming the defect is still unadjudicated, corrected the Bayesian post-mortem's Theorem-1-vs-§3.2 citation attribution (D-10), and added a positive-content test that derives its required substrings from `dsx.frame.paradigm._MONITORING_DISCIPLINE` at runtime so a clearing declaration added to the code without being added to `references/paradigm-symmetry.md` fails the suite.
- Shipped `DSX-PAR-002` (HIGH) as a membership-free presence check over `inference.paradigm_justification` and `inference.paradigm` — closing the last `_NOT_SHIPPED` entry with a mechanical, fourteen-case cross-product proof that no reason and no paradigm has its own code path.
- `dsx.spec.is_blank_text` replaces `is_blank` as the clearing predicate for DSX-PAR-010/DSX-PAR-011, so a bare `0`, `0.0` or `False` no longer clears the CRITICAL pair with zero declared content, and `references/paradigm-symmetry.md` now states that fact instead of an audit claim the code contradicted.
- The two shipped, operator-facing artifacts that paired `1/(K+1)` directly with "Theorem 1" — the `DSX-PAR-011` `detail=` string and the known-bad Bayesian fixture's own Formulation note — now attribute the bound the same way the module's own docstring, `references/paradigm-symmetry.md` and the paired POSTMORTEM.md already do: Theorem 1 licenses the bound under optional stopping; the number itself is unnumbered prose at Section 3.2.
- Arrow-triggered `fallback_rule` mini-language parses to a `_ParsedRule`, resolves against a closed three-fact registry to exactly one branch or a named reason, and raises `CheckError` (exit 2) on anything it cannot parse — all pure logic, no finding emission, no gate registration.
- `DSX-PRE-010`/`DSX-PRE-030` ship at CRITICAL with citations the catalogue actually enforces — declared-rule resolution and executed-vs-declared branch reconciliation that reads no procedure-merit ordering — and all five D-13 forcing guards flip green in the same commits that land their codes.
- `_check_content_lock` reads the plan-time frame_digest lock out of `DECISIONS.jsonl` — a missing plan-gate-point header now aborts the run at exit 2 with the M-07 grandfather route named, and a `declared_at: pre_data` claim never registered at plan blocks at CRITICAL under `DSX-PRE-020`, by set membership over every recorded plan digest, never most-recent-or-earliest.
- `prereg` is live in `GATE_PROFILES["verify"]`/`["ship"]` with the project root threaded through a named `run_checks` branch, gated on a `gate_invocation` discriminator that scopes trail reconciliation to real `dsx gate` runs alone — and every one of the six pre-existing call sites this registration would otherwise break (found by direct read plus one more found only by running the suite) now seeds a plan-time header instead of depending on test order.
- A new committed known-bad fixture whose executed procedure (`fishers_exact`) is strictly more conservative than the branch its pre-registered fallback rule selects (`two_proportion_z`) still blocks `dsx gate verify`/`ship` naming `DSX-PRE-030` — the first fixture in this corpus to prove REQ-P10-04's no-merit-consultation claim against a real gate run rather than a synthetic report, with a dedicated test covering the verify/ship-only points the generic corpus test cannot reach.
- Amended REQ-P11-01/ROADMAP SC1 from 25-35 to 14 families (D-02), replaced test-selection.md's Fisher's-exact fallback with Boschloo's exact test cited to Lydersen et al. 2009 (D-27), and folded two resolved locators (Kohavi Ch. 22; Cameron & Miller Section VI) into brief.md section 7 (D-29)
- Added the closed `ESTIMAND_TYPES` vocabulary and optional `validity_frame.estimand.type` field the admissibility adjudicator will key on, and populated it on all nine committed specs with zero gate-result drift.
- Mirror-image AST scanner closing the `dsx/checks/` → `dsx/frame/` import direction, plus `applies_to_frequentist_admissibility(spec)` — the one predicate allowed to read the declared paradigm on the adjudicator's behalf.
- Shipped `references/families.yaml` — 14 cited frequentist family entries, a 19-token cited assumption vocabulary, and 4 cited pairwise ranking rules — parsed only by `dsx.loader.load()` and proven to round-trip identically on both its PyYAML and bundled-fallback paths, with `tests/test_families_yaml.py` (28 tests) written first and left unmodified once the data made it pass.
- `dsx/frame/admissibility.py` -- a refuse-not-degrade ontology loader over `references/families.yaml` plus an exact-match, pair-scoped alias resolver with four distinguishable outcomes, built test-first across two RED/GREEN cycles with zero finding codes emitted.
- `rank_admissible()`/`dominating_rules()`/`admissible_families()`/`check()` in `dsx/frame/admissibility.py` — a rule-table ranking (never a numeric score) plus `DSX-ADM-010` (HIGH, cited-rule domination) and `DSX-ADM-020` (CRITICAL, three collapsed underdetermination causes), both reaching exit 1 through the ordinary emit path with `DecisionRecord.escalate`/`alternatives_rejected` shipping for the first time.
- `CHECKS["admissibility"]` and `GATE_PROFILES["plan"/"verify"/"ship"]` now reach `dsx/frame/admissibility.py::check()`, routed by a scoping boolean `run_checks` computes from `dsx/frame/paradigm.py` and never by the adjudicator itself; `dsx recommend-test` gained an additive `admissibility` key behind an explicit `--spec`/`--phase-dir` flag, with v1.5.0's no-flag output proven byte-identical across working directories by subprocess diff.
- `check_families_citations()` fails `--check` on any uncited `references/families.yaml` entry with a `D-24:` line naming it, and `"DSX-ADM-"` in `_D05_ALLOWLIST_PREFIXES` switches on the D-05 citation/structural-criterion/test-marker gate that plan 11-06's docstrings and markers already satisfy — the two halves of REQ-P11-06's enforcement (build time here, run time in `load_ontology()`) now both exist.
- Widened `dsx/checks/code.py`'s entrypoint scan with two new CRITICAL codes — full-frame fillna/std/quantile cleaning before the split (DSX-CODE-020) and a post-split fit call not fitted on a recognised training frame (DSX-CODE-021) — closing the exact two idioms the 2026-08-20 paper reproduction used to slip past the gate with zero findings.
- Documented the ensemble-plus-large-roster failure and the discretisation-on-a-full-frame-test failure in `references/leakage-taxonomy.md` (type 3 sub-case, cross-referencing type 7; plus a discretisation note) and mirrored both as new numbered signals 7 and 8 in `agents/dsx-ml-integrity-auditor.md`'s leakage-heuristics block, citing `The AI Data Scientist` §2.3/§2.5 directly rather than the research file's paraphrase, with no finding code named and no new numbered leakage type.
- Added a statistical-test marker family and a target-reference co-occurrence scan to `dsx/checks/code.py`, closing the blind spot where the reproduction's hypothesis stage never calls `.fit()` at all — it cross-tabulates a candidate feature against the target column and runs a chi-square test, then folds the accepted hypotheses back into the dataset.
- Moved the prediction-time-definition check (DSX-ML-033) out from behind `_check_features`'s early return so it fires whenever a model is declared, and added DSX-ML-043 (HIGH) so an undeclared or unparseable positive rate under an imbalance-unsafe primary metric produces a finding instead of silence.
- Added an optional `data[].cleaning[].fit_on` declaration so a specification can state where each cleaning step's statistics were fitted; a step fitted outside training rows draws DSX-ML-023 at CRITICAL, and a declaration that contradicts an already-honest whole-pipeline boundary of training rows only additionally draws DSX-ML-024 at HIGH — with one shared `TRAIN_ONLY_FIT_VALUES` constant so the two boundary checks (whole-pipeline and per-step) can never disagree about what counts as training rows only.
- Added two optional `results` fields — `model_score_source` and `fold_scores` — so a baseline comparison can state where its reported score came from and how much its own folds vary; a blank, disqualifying (best-fold/unknown) or unrecognised source draws DSX-ML-052 at HIGH, and a margin over baseline strictly smaller than the model's own fold spread draws DSX-ML-053 at MEDIUM naming both numbers, both gated on the model already beating its baseline.
- Added an optional `model.selection_ledger` field — `{candidates_evaluated, configurations_tried, selected_on}` — owed once `model.algorithm` is declared; an incomplete ledger draws `DSX-ML-090` at HIGH naming each missing field, a complete ledger selected on the test set draws `DSX-ML-091` at CRITICAL, and a complete ledger selected on the same folds as the reported score draws `DSX-ML-092` at HIGH, with an unrecognised selection basis (including a misspelling) folded into the missing-field case rather than buying silence.
- Committed the tenth known-bad corpus fixture — a reproduction of "The AI Data Scientist" (arXiv:2508.18113v1) whose full-frame cleaning, hypothesis test and post-split scaler above an honestly-declared training-only preprocessing boundary passed the gate with zero findings before this phase — extended the corpus harness so any fixture's declared entrypoint can now be resolved from a fresh temporary phase directory, and recorded the catch attribution (DSX-CODE-020/021/030 CRITICAL, DSX-ML-090 HIGH, all at `dsx gate execute`) with every ship-point CRITICAL/HIGH finding accounted for.
- Replaced DSX-CODE-001's line-ordered regex scan with a single `ast.parse` + `ast.walk` over the entrypoint (text-scan fallback retained), closing the whitespace/tab/backslash/multi-line detection gap and two measured prose false positives, while making a degraded or skipped scan impossible to mistake for a clean one.
- Moved DSX-CODE-021's first-argument extraction off the line-ordered regex scan onto `ast.Call` node resolution (keyword arguments, chained calls, multi-line calls, `partial_fit`, semicolon-joined second calls all now fire), widened the fallback to agree instead of contradict, and closed a BOM-notebook read gap the same class of fix plan 01 already applied to `.py`.
- Re-derived and pinned what the AST-based entrypoint scanner still cannot see (18 forms, two discovered to be persisting false positives rather than missed leaks), proved five non-regression properties the mechanism change put at risk, measured every retained pattern on both interpreters, announced the behaviour change in both directions in README.md, and committed the phase's headline number as an executable 18-row end-to-end table -- while surfacing, not silently absorbing, three genuine gaps between AST-DESIGN's promise and what plans 01/02 actually shipped.
- 1. [Rule 1 - Bug] `_first_argument` did not exclude a resolved `ast.Compare` node
- Four more malformed-`.ipynb`-JSON shapes (non-list `cells`, non-string-list `source`, non-string/non-list `source`, and recursion-limit-deep JSON) now route to a controlled "NOT scanned" pass instead of an uncaught crash that exits with the same code as a real block — a fifth, non-UTF-8 bytes, was found by a pre-execution security audit to already be handled correctly outside this branch and was deliberately left untouched.
- README.md's malformed-notebook paragraph now enumerates the six shapes plan 06 actually routes to NOT scanned instead of a false two-example generalisation, and a new fourth disclosure group in the limits section names all four residual degradations of the hardened notebook read — including the non-UTF-8 asymmetry's genuinely different, blocking exit-2 outcome — each pinned by an extended `required_substrings` tuple so a later silent deletion fails a committed test.
- Added `prescriptive` as the fifth claim type and its rank-4 coherence-ladder row, closing the silent-pass gap where a `type: prescriptive` claim tripped a HIGH "unrecognised type" warning and was then silently skipped by the CRITICAL strength-ceiling check.
- 1. Gerund-no-hedge test case was not genuinely RED at Task 1.
- DSX-PRE-040/041: a fail-closed top-level spec_id requirement and an amendment-ledger HIGH finding (identity-scoped plus an un-renameable identity-free floor) added to the decision trail, gated at verify/ship only.
- Quarantined the reader-less decision.reversible/decision.deadline template fields behind an explicit "NOT gate-read" label, added gate-read revisit_when + spec_id examples with a deadline-distinction comment, repointed the storyteller/narrate docs at enforced fields, and pinned it all with an AST+text invariant test.
- 1. [Rule 3 - Blocking] Divergent-code pin update in tests/test_gen_finding_catalogue.py
- A new sibling predicate (`revisit_when_is_discriminating`) requires a named-metric-plus-threshold-plus-time-anchor re-visit trigger for any prescriptive question or experiment, firing new CRITICAL code `DSX-COH-040` without ever mutating the shared `falsifier_is_discriminating()`.
- Committed the flagship "offer bundled incentives to reduce churn" fixture that blocks a prescriptive claim smuggled under a descriptive question, pinned every fixture's finding set against the causal-verb widening with a golden-file equality test, proved the noun negative case, recorded the verbless-recommendation and amendment-counter limits, and closed the phase with a fully green corpus, catalogue, suite and check.sh.
- DSX-STA-012 MEDIUM turns a silent effect-size skip into a visible finding, fired from a membership guard that precedes interpret_effect and reads a single-sourced EFFECT_SIZE_KINDS frozenset shared with mathx.py.
- missingness.method_implied is now a closed 7-member vocabulary (unknown → DSX-SPEC-082 HIGH via the reused membership loop), and single imputation treated as if observed under MAR fires DSX-VAL-060 CRITICAL with its own Rubin (1987) §3.1 citation — minting no code and leaving the catalogue untouched.
- DSX-VAL-080 HIGH holds a declared row-exclusion rule to account (it must carry a justification) and DSX-SPEC-083 HIGH rejects any key outside the closed {rule, action, applied_before_split, justification} set, so a data-dependent row count cannot be smuggled into a content-locked frame; applied_before_split is record-only and the existing DSX-PRE-020 lock catches a moved cutoff with zero new machinery.
- 1. [Process — mid-unit death recovered by a later firing, no scope change] Task 3 was left uncommitted by an earlier firing.
- The terminal plan of Phase 11.3 proves the phase closed cleanly: the finding catalogue is confirmed current at 256 codes (regeneration produces zero diff, `--check` exits 0), every D-15 fixture obligation is present on disk or exercised by a named unit test, and the full corpus gate (`scripts/check.sh`) runs green against the fully-merged tree — all eight net-new codes reachable, no code changed and no expected-defect map edited.
- 1. [Rule 3 - Blocking issue] Registered new fixtures in every whole-examples-tree glob harness
- Live per-family friction column (raw + net over-block as a rate over non-target in-profile cells) guarded three ways — synthetic arithmetic, same-live-source-as-golden, and incidental→own relabel closure — plus a D-18 test pinning the finding-code catalogue at exactly 256.

---
