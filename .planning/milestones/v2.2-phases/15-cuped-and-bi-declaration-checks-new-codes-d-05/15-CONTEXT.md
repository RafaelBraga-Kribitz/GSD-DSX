# Phase 15: CUPED and BI declaration checks (new codes, D-05) — Context

**Milestone v2.2 Analytic Surface · S4-1 discuss · 2026-08-29.** The last phase of
the milestone and — with Phase 16 — one of only two that extend the gate catalogue.
It is the phase carrying the D-05 primary-source reads and the D-06 irreversible
finding-code numbering. Requirements: REQ-P15-01 … REQ-P15-07 (7).

## Phase Boundary

Two new **declaration-only** gate checks plus vocabulary, template and
negative-assertion work. Nothing here computes on data or touches the gate path with
pandas/scipy/numpy (D-01/D-02). Exactly **two** finding codes are minted; the
catalogue moves **258 → 260 additively** over the byte-frozen Phase-12 snapshot (256);
the survivorship-bias code is **not** minted (its citation does not transfer — HQ-8).

## Persona round (LOOP-BRIEF §4)

Architect (`dsx-analysis-architect`) + Statistician (`dsx-statistician`), both
opus/high, concurrent — the two relevant personas for a statistical, code-minting
spec-shape phase. Tie-break **rigour > reliability > flexibility**. The round
converged on mint-count, both citations, the CUPED code, family placement of the
changing-denominator code (MET, not INT), and the survivorship non-promotion. It
**split on one call — the changing-denominator severity** — resolved by the
orchestrator below.

### The decision, stated plainly

- **CUPED covariate check → `DSX-EXP-070`, CRITICAL**, in `dsx/checks/design.py`.
- **Changing-denominator check → `DSX-MET-021`, HIGH**, in `dsx/checks/metrics.py`.
- **Survivorship-bias check → NOT SHIPPED** — stays in `brief.md` §6.5 with a
  falsifiable D-13 entry condition (operator's answered HQ-8: Brown et al. 1992 does
  not transfer to a declared-field criterion).
- Catalogue **258 → 260** additive; frozen Phase-12 snapshot (256) untouched.

## Decisions (loud, vetoable — LOOP-BRIEF §4)

**D-01 — Mint count: exactly two codes.** `DSX-EXP-070` (CRITICAL) + `DSX-MET-021`
(HIGH). Survivorship not minted. Both personas unanimous. REQ-P15-01/03/05/06/07 mint
nothing (below). 258 → 260. Orchestrator re-verified the baseline (brief §5):
`gen-finding-catalogue.py --check` exit 0, total 258; `DSX-EXP-070` and `DSX-MET-021`
both absent from `references/finding-codes.md` (grep count 0) — genuinely free.

**D-02 — CUPED post-treatment-covariate code (D-06 numbering, irreversible).**
`DSX-EXP-070`, **CRITICAL**, new `_check_cuped` in `dsx/checks/design.py` dispatched by
the always-run `design.check()` (NOT the causal-gated frame), keyed on
`normalize(variance_adjustment) == "cuped"` so it fires even when the
`looks_like_experiment` marker is not tripped.
- Finding text (fixed plain literal — AST-extractable): `"CUPED declared with a
  covariate that is not pre-experiment"`. `where = "spec.design.cuped.covariate_timing"`.
- New thin declaration surface: `design.cuped.{covariate, covariate_timing,
  covariate_source}`; `covariate_timing` is a closed two-member vocab
  `CUPED_COVARIATE_TIMINGS = {"pre_experiment", "post_treatment"}`.
- Firing rule (declaration-only, computes nothing): `pre_experiment` → `report.ok`;
  `post_treatment` **or any unrecognised/absent value** → fire CRITICAL. A correctness
  field at a CRITICAL gate must not let a typo or omission be cheaper than declaring
  `post_treatment` honestly (INT-010/INT-030 doctrine). Keep the vocab strictly
  two-valued — no fuzzy third state — so a valid covariate is never false-flagged.
- **Severity = CRITICAL is forced by REQ-P15-02**: "exits 1 at `dsx gate plan`", and
  `plan`/`execute` block only at CRITICAL (`verify`/`ship` at HIGH). Mirrors EXP-060 /
  INT-030 CRITICAL — no `GATE_THRESHOLDS`/`GATE_PROFILES` edit.
- Family: EXP is design-correctness (peeking, units, duration, multiplicity). The
  *vocabulary* question is already owned by `DSX-SPEC-044` (which now accepts `cuped`);
  the *semantic* pre-experiment question is an EXP concern. `070` is the next free EXP
  band (existing: 000/020/021/030/050-053/060).
- **Citation (D-05, confirmed via HQ-8):** Deng, Xu, Kohavi & Walker (2013),
  *Improving the Sensitivity of Online Controlled Experiments by Utilizing
  Pre-Experiment Data*, WSDM '13, pp.123-132, DOI 10.1145/2433396.2433413 —
  `Ŷ_cv = Ȳ − θ(X̄ − E[X])`, `θ = Cov(Y,X)/Var(X)`, `Var(Ŷ_cv) = Var(Ȳ)(1 − ρ²)`,
  pre-experiment independence requirement. **NOT** the Unified Framework playbook
  snippet (REQ-P15-02's explicit exclusion).

**D-03 — Changing-denominator code (D-06 numbering, irreversible).** `DSX-MET-021`,
**HIGH**, new `_check_cohort_denominator_shift` in `dsx/checks/metrics.py`, runs
**unconditionally**.
- Finding text (fixed plain literal): `"metric pooled across buckets sampled at
  different rates with no reweighting declared"`. `where = "spec.results.cohort_comparisons"`.
- Reads the NEW `results.cohort_comparisons` surface (never `results.period_comparisons`).
  Fires when a `cohort_comparisons[]` entry declares buckets whose `sampling_rate`
  (or `treatment_share`) differ by more than the declared / `0.10`-default tolerance
  **AND** `reweighted` is not the literal boolean `True`. Reads declared allocation
  shares only — never sums per-unit data.
- **Family = MET, not INT (rigour tie-break).** DSX-INT lives in the causal-gated
  `dsx/frame/interference.py`, which returns an empty report unless
  `needs_causal_block(spec)` (True only for `question_type ∈ {causal, prescriptive}`
  or `design.kind == experiment`, `spec.py:1168-1175`). The REQ-P15-03 target — a
  descriptive/diagnostic cohort/funnel BI spec — would **silently skip** an INT code.
  Kohavi's Pitfall 4 explicitly covers the non-experimental "subpopulations sampled at
  different rates" case, so the check must run for non-causal specs. MET (`metrics.py`)
  runs unconditionally. `021` is the free slot adjacent to its closest semantic sibling
  `DSX-MET-020` in the 02x "denominator" band.
- **Severity = HIGH, not CRITICAL (rigour tie-break — the round's one split).** The
  Statistician leaned CRITICAL (sibling to the CRITICAL Simpson code MET-030); the
  Architect leaned HIGH. Orchestrator adopts **HIGH**:
  1. A declaration-only check can only evidence that the bucket allocation/base
     *shifted*; it cannot prove the pooled result's sign *reversed* (full Simpson).
     Claiming CRITICAL ("the result is invalid") overstates what the declaration
     proves — rigour forbids that. HIGH ("materially overstated / partly composition")
     is exactly the framing of the sibling denominator code `DSX-MET-020` (HIGH), and
     is catalogue-consistent. MET-030 is CRITICAL because it detects the *realised*
     reversal from declared segment effects; MET-021 detects only the precondition.
  2. The Statistician's CRITICAL argument partly relied on "exit 1 at `dsx gate plan`"
     — but that plan-block clause is **REQ-P15-02 (CUPED)**, not REQ-P15-04. REQ-P15-04
     requires only that the defect "block its own bad fixture", which a HIGH code does
     at verify/ship. The premise was a REQ-P15-02↔P15-04 conflation.
  3. Reliability also favours HIGH (less over-blocking of legitimate cohort
     comparisons, which routinely differ in denominator *size* but not *definition*).
- **Citation (D-05, confirmed via HQ-8):** Crook, Frasca, Kohavi & Longbotham (2009),
  *Seven Pitfalls to Avoid when Running Controlled Experiments on the Web*, KDD '09,
  pp.1105-1114, DOI 10.1145/1557019.1557139, Section 6 "Pitfall 4" (Table 1 Simpson's
  paradox). Distinct from ratio-metric dilution (Deng & Hu 2015 Formula (3),
  permanently out of scope `brief.md:450`) and from INT-030 additive triggered-vs-
  eligible dilution.

**D-04 — REQ-P15-03 thin fields (optional/additive; good fixture stays silent, D-08).**
`metrics[].cohort_grain` (label, documentation only); `results.cohort_comparisons[]`
(the surface MET-021 reads — good fixture keeps it silent with equal `sampling_rate`
or `reweighted: true`); `results.funnel_steps[]` (ordered documentation — a natural
monotone drop-off never fires MET-021). All new keys stay **top-level under
`results`/`metrics`, never inside `validity_frame.exclusions`** (the one strict-key
block, `spec.py:1184`), so `frame_digest` is unchanged and the extended good fixture
draws zero findings at plan/execute/verify/ship.

**D-05 — REQ-P15-04 partial satisfaction (loud, not silent).** The requirement as
worded expects both survivorship and changing-denominator to ship. Per the operator's
**answered HQ-8** ("cite2 does not transfer — leave unshipped"), Phase 15 ships the
**changing-denominator half only**; survivorship stays a documented `brief.md` §6.5
non-promotion. This is compliant with REQ-P15-04's own escape clause ("a code without
a citation does not ship and stays in §6.5"), not a violation — but the checkbox
cannot be marked plainly complete. Disposition:
- Record the partial satisfaction loudly here and in the S4-5 validation
  (REQ-P15-04 status = "PARTIAL — changing-denominator shipped; survivorship deferred
  to §6.5 per HQ-8", never a bare check).
- **D-13 entry condition for the §6.5 survivorship item (falsifiable, not a wish):**
  promote only when (a) an admissible D-05 source gives an operationalisable
  *declared-field* criterion for cohort/funnel survivor-conditioning — explicitly NOT
  Brown et al. 1992, whose persistence-statistic mechanism is a computed-quantity
  defect — AND (b) an M5-corpus case where survivor-conditioning on a declared
  population, mismatched to the claim's declared estimand scope, was the documented
  failure and is not already caught by `DSX-VAL-050` generalisation.
- The `REQUIREMENTS.md` REQ-P15-04 wording change is **queued to S4-4 close-out**
  (orchestrator single-writer; not reworded mid-discuss). Operator consent already on
  record via HQ-8; noted in HQ-13 for the veto window.

**D-06 — CUPED worked value (test/docstring constant only).** Pin the analytic
identity `variance reduction = ρ²` at `ρ = 0.5 → 25 %` (variance ratio 0.75) — it is
the paper's own derived result. Do **not** assert the ~50 % Bing headline as the
worked value (it is empirical, ρ ≈ 0.707, not a derived identity) — keep it as
docstring context. The `θ`/`1 − ρ²` reference arithmetic lives only in
`dsx/mathx.py` (`cuped_theta` / `cuped_variance_reduction`) with a `# D-05:` test
marker, tested against the WSDM value, and is **never imported by the gate path** —
the `dsx.mathx.diluted_effect`↔INT-030 precedent.

**D-07 — REQ-P15-06 Shapiro–Wilk negative assertion (mints nothing).** Assert against
`references/test-selection.md` that (1) the assumption order is fixed
**independence → equal variance → normality** (lines 54-63); (2) the continuous
2-group recommendation is **Welch unconditionally** — no branch on a computed variance
test; (3) normality enters only as a **declared** shape+n property, never as the
output of a normality test the tool ran; and (4) grep the gate + skill decision
surface for `shapiro`/`normaltest`/`anderson`/`kstest`/`scipy.stats.*normal*` — none
on any test-selection decision path (belt-and-suspenders over the anti-feature at
`brief.md:463-464`).

**D-08 — Additive rebaseline (D-08 discipline).** At S4-3: bump
`tests/test_finding_catalogue_invariant.py` `_EXPECTED_TOTAL` 258 → 260; add
`DSX-EXP-070` and `DSX-MET-021` to `_MINTED_CODES` (making the expected set
`snapshot ∪ {REP-060, REP-061, EXP-070, MET-021}`); update the `258→260` prose. Keep
`_SNAPSHOT_TOTAL = 256`. The byte-frozen `tests/fixtures/finding-codes-phase12.md`
(256) is **never mutated** — same separate-snapshot-leg pattern Phase 16 used for
256→258.

**D-09 — D-05 allow-listing by exact code, not prefix.** Add `"DSX-EXP-070"` and
`"DSX-MET-021"` individually to `_D05_ALLOWLIST_CODES` in
`scripts/gen-finding-catalogue.py`. Do **not** add the `DSX-EXP-`/`DSX-MET-` prefixes
— those are legacy families with pre-existing uncited members; a prefix add would drag
them into D-05 enforcement and fail the build red. Precedent: `DSX-SPEC-080..086`,
`DSX-ML-043`.

## Escalations & queue

- **D-06 numbering veto window → HQ-13 filed** (non-blocking; drains at S5-2). Mirrors
  Phase 16's HQ-11. Silence = accept; operator may veto/amend `DSX-EXP-070`/
  `DSX-MET-021` (numbers, families, or the MET-021 HIGH-vs-CRITICAL severity) via the
  daily summary or at the S5-2 drain.
- **No new D-05 human read owed at discuss.** Both shipping citations were read and
  confirmed by the operator at their locators in **answered HQ-8** (CUPED confirmed;
  changing-denominator confirmed; survivorship does-not-transfer). D-06 numbering is
  decided by the loop, not escalated (brief §4).
- **REQ-P15-04 reword** queued to S4-4 (operator-consented via HQ-8; not a new scope
  escalation).

## Traps the plan (S4-2) must not paper over

1. **MET-021 must be provably disjoint from the pre-existing `DSX-MET-020`.** MET-020
   (`_check_denominator_drift`, HIGH) reads `results.period_comparisons` and fires on a
   count-magnitude drift between *periods*. MET-021 reads `results.cohort_comparisons`
   and fires on a *definition/allocation-share* mismatch between *cohorts/buckets*. A
   disjointness test must assert: a period-drift spec fires ONLY MET-020; a cohort
   mix-shift spec fires ONLY MET-021 — no double report. This is THE key trap.
2. **Extended good fixture silent at every threshold (D-08).** New cohort/funnel fields
   + any CUPED block (`pre_experiment`) must draw ZERO findings at plan/execute/verify/
   ship. New checks `report.ok`/return — never `.add` — on good-fixture values.
3. **Frozen snapshot not mutated; rebaseline in the invariant test only** (D-08).
4. **Both titles are AST-extractable plain literals** (or the catalogue row silently
   drops via `gen-finding-catalogue.py::_literal`). Each code also needs a `Citation:`
   line + a `Reference value:`/`Structural criterion:` line in its enclosing docstring
   + a `# D-05: <CODE>` test marker.
5. **CUPED check computes nothing on the gate path** (no θ/ρ/variance) — reference impl
   in `dsx/mathx.py`, never imported by the check (D-01/D-02).
6. **Changing-denominator check re-implements neither ratio-metric dilution
   (§6.5:450) nor INT-030** — reads declared allocation shares only.
7. **Home the changing-denominator check OUTSIDE the causal-gated
   `dsx/frame/interference.py`** — else descriptive/diagnostic BI specs escape it.
8. **No `GATE_THRESHOLDS`/`GATE_PROFILES` edit** — EXP-070 CRITICAL / MET-021 HIGH
   block by severity alone.
9. **New spec keys stay out of `validity_frame.exclusions`** so `frame_digest` is
   unchanged (D-08).
10. **Regenerate, don't hand-edit, the catalogue** — `gen-finding-catalogue.py
    --write` (→ 260), then `--check` exit 0 (REQ-P15-07).
11. **CUPED missing/unrecognised timing** fires a *distinct* finding, never a
    mislabelled affirmative post-treatment accusation; and the check does not run
    unless `variance_adjustment == cuped`.
12. **REQ-P15-01 lands before REQ-P15-02** — until `cuped ∈ VARIANCE_ADJUSTMENTS`
    (`spec.py:264`), a `variance_adjustment: cuped` spec draws a stray DSX-SPEC-044
    (MEDIUM) and the pre-experiment PASS fixture is not clean.

## Deferred / out of scope (named so nothing is silently pulled in)

- **Survivorship-bias code** — not shipped (D-05, §6.5, D-13 entry condition above).
- **Ratio-metric dilution** (Deng & Hu 2015 Formula (3)) — permanently out of scope
  for a declaration-only gate (`brief.md:450`); MET-021 must not re-mint it.
- **Two CUPED failure modes a declaration cannot see** (documented as named
  limitations, not silently claimed): a pre-timestamped covariate mechanically derived
  from a post-treatment quantity; and per-arm (vs pooled) θ estimation. Both are
  computation-time defects outside a declaration check's reach.

## What "done" means for Phase 15 (goal-backward, for S4-4 / S4-5)

- **REQ-P15-01** — `cuped ∈ VARIANCE_ADJUSTMENTS`; `dsx vocab` dumps it; the four
  existing members round-trip; D-08 fixtures extended not replaced. No mint.
- **REQ-P15-02** — post-treatment-covariate CUPED spec exits 1 at `dsx gate plan`
  (`DSX-EXP-070` CRITICAL); pre-experiment passes; docstring cites Deng et al. 2013
  WSDM naming the formulation; test pins the ρ²=25 % worked value (not the playbook).
- **REQ-P15-03** — `ANALYSIS-SPEC.yaml` accepts thin cohort-grain + funnel-step
  fields; extended good fixture passes every gate at every threshold (D-08).
- **REQ-P15-04** — **PARTIAL, loud:** changing-denominator (`DSX-MET-021` HIGH, cited
  Crook 2009) blocks its bad fixture; survivorship deferred to §6.5 per HQ-8 with a
  D-13 entry condition. REQUIREMENTS.md reword at S4-4.
- **REQ-P15-05** — research-domain APA table template exists; marketing-domain ship
  still requires narrative + sealed figure + claim evidence (existing NAR/FIG/CLM
  codes, unchanged). No mint.
- **REQ-P15-06** — negative assertion vs `test-selection.md` order; no Shapiro–Wilk
  auto-switch on any decision path. No mint.
- **REQ-P15-07** — `gen-finding-catalogue.py --check` exit 0 at 260; both canonical
  fixtures still satisfy D-08.
