---
phase: 18
phase_name: "Correlation, association and agreement"
project: "gsd-dsx"
generated: "2026-09-02"
counts:
  decisions: 9
  lessons: 5
  patterns: 6
  surprises: 4
missing_artifacts:
  - "UAT.md"
---

# Phase 18 Learnings: Correlation, association and agreement

## Decisions

### Hybrid routing shape: a dataless `recommend_association` beside the untouched `recommend_test`
D-01: rather than folding correlation/agreement into `recommend_test` or building a
gate-only check with no programmatic mirror, Phase 18 adds a thin dataless pure function
`recommend_association(estimand_kind: str) -> {tests, effect_size, citation}` returning
the acceptable-coefficient SET per kind (`linear_association` → {pearson_correlation,
point_biserial}; `monotone_association` → {spearman_correlation, kendall_tau_b};
`nominal_association` → {phi, cramers_v}), plus a new gate function
`_check_declared_association(analysis, spec, report)` sitting beside
`_check_declared_test`. `recommend_test` is left completely untouched, and a new
"Association / agreement" section is added to `references/test-selection.md` as the doc
mirror. The gate membership-checks a SET, not one coefficient, so a legitimate
Kendall-vs-Spearman choice is never over-blocked.

**Rationale:** `recommend_test`'s signature already carries data-shape flags (`normal=`,
`n_per_group=`, `overdispersed=`) and raises on an unknown `outcome_type`; correlation/
agreement have no `outcome_type`, so folding them in would either pollute the closed
`OUTCOME_TYPES` vocab or bolt a branch onto a switch keyed on a field they don't have.
Gate-only was rejected because it abandons the module's "derived, not chosen" doctrine
and leaves the new doc section with no programmatic mirror.
**Source:** 18-CONTEXT.md

---

### Five new HIGH codes from the Phase-17 pre-allocated decades, numbered and split by remedy
D-02: `DSX-STA-050`/`DSX-STA-051` (correlation/kind mismatch) and `DSX-STA-060`/
`DSX-STA-061`/`DSX-STA-062` (agreement completeness) are all severity HIGH — the
"recognised-but-contradictory declaration" class (same class as existing HIGH
`DSX-STA-041`, not the MEDIUM `DSX-STA-040` "unrecognised vocabulary" class), matching
REQ-P18-04's "blocks at verify/ship" language. They are split rather than merged because
each failure mode has a distinct remedy, distinct citation, and distinct declared-field
predicate, and a merged code would emit the wrong remedy for half its firings under
permanent D-06 numbering. 050/051 are mutually exclusive by `estimand_kind` context (no
double-fire); 052–059 and 063–069 stay free for later codes (dCor/partial promotion,
Fleiss category-count, Krippendorff level-of-measurement, ICC combination-coherence).

**Rationale:** Numeric code assignments from pre-allocated ranges are persona-round
decisions recorded loudly with a veto window (HQ-20), not a scope escalation; splitting
by predicate group keeps each code's D-05 citation obligation attributable.
**Source:** 18-CONTEXT.md

---

### DSX-STA-050 whitelists point-biserial and dichotomous operands (the ">2 levels" rule)
D-03: a naive `test == pearson AND scale ∈ {ordinal, dichotomous}` predicate would
false-block every legitimate point-biserial declaration, since point-biserial *is*
Pearson r on a {0,1} dichotomy and lives in `linear_association` by Phase-17 D-01. So
`DSX-STA-050` fires only when the declared operand scale is `ordinal` with more than two
levels; declared `point_biserial` and any declared-dichotomous (2-level) operand are
whitelisted and never fire it. The operand scale must be a declared field — never
inferred from data — and its absence is non-blocking.

**Rationale:** Both personas treated this as a non-negotiable rider: the ordinal-vs-
dichotomous split *is* the mechanism that encodes ">2 levels" without an extra
level-count field, and it prevents a correct, common declaration from tripping a HIGH
finding.
**Source:** 18-CONTEXT.md

---

### DSX-STA-062 requires p_pos AND p_neg specifically, not "raw agreement + prevalence"
D-04: REQUIREMENTS.md's own parenthetical paraphrased the kappa companions as "raw
agreement + prevalence, per Feinstein & Cicchetti 1990." The operator-answered HQ-16
correction established that the actual reporting recommendation — "the omnibus κ should
always be accompanied by separate individual values of p_pos and p_neg" — lives in the
companion Part II (Cicchetti & Feinstein 1990, *J. Clin. Epidemiol.* 43(6):551–558),
while Part I (43(6):543–549) states the two paradoxes. `DSX-STA-062` therefore requires
the declared companions to be `p_pos` AND `p_neg` specifically, and cites both parts.
REQUIREMENTS.md is not edited unilaterally this firing; the one-word alignment
("prevalence" → "p_pos/p_neg") is offered non-blocking in HQ-20 instead.

**Rationale:** Shipping the stale paraphrase would encode a weaker, mis-attributed gate —
a citation-integrity defect the portfolio's standard forbids above all else; this
implements the requirement's intent with the operator's own corrected specifics rather
than the loop rewording a requirement on its own authority.
**Source:** 18-CONTEXT.md

---

### ICC completeness (DSX-STA-060) is presence + membership only; coherence deferred as candidate DSX-STA-063
D-05: `DSX-STA-060` fires on missing-or-out-of-vocabulary `model`/`type`/`definition`
sub-fields only (admissible values per Shrout & Fleiss 1979; McGraw & Wong 1996 corrected
edition). The Statistician recommended an additional coherence rider (`one_way_random`
⇒ `definition` must be `absolute_agreement`, since one-way-random has no rater effect to
partial out for a consistency ICC) — statistically correct but a different gate
(coherence, not completeness) with its own citation burden and its own permanent code.
This is deferred to a falsifiable D-13 entry condition: the coherence gate (candidate
`DSX-STA-063`, in the 060–069 reserve) enters only when a fixture demonstrates a
complete-but-incoherent triple passing `DSX-STA-060`.

**Rationale:** REQ-P18-04 asks for declaration completeness, which is provably
presence + membership; coherence is additive scope, so the tie-break (prefer the smaller
provable claim) applies, and the deferral is recorded as a named, triggered decision
rather than a silent omission.
**Source:** 18-CONTEXT.md

---

### Effect-size KIND growth stays report-only; the blocking band domain never widens past {d, h, r}
D-06: the existing magnitude guard (`DSX-STA-011`/`DSX-STA-012` in `stats.py`) bands
`effect_size_kind` via `mathx.interpret_effect`, whose domain is
`EFFECT_SIZE_KINDS = frozenset({"d","h","r"})`. Kappa, ICC, Kendall's W, phi, Cramér's V,
tau-b and rho are deliberately NOT added to that frozenset. Instead, a separate
report-only registry is consulted so a spec declaring `effect_size_kind: kappa` on a
significant result is recognised (no nonsensical "declare d/h/r" nag) but is never
banded by a blocking code; the bands themselves live in `mathx.py` report-only tables,
wired only into the ungated `templates/APA-TABLE-research.md`.

**Rationale:** Widening `EFFECT_SIZE_KINDS` would make `DSX-STA-011` adjudicate a
convention as a band boundary (violating REQ-P18-05), and `interpret_effect`'s flat
`abs(value)` band is statistically wrong for these kinds anyway — Cramér's V thresholds
are df-dependent (Cohen's 0.1/0.3/0.5 hold only at df=1) and phi/W are unsigned with a
different null. "Conventions never block" is implemented structurally, not by
discipline.
**Source:** 18-CONTEXT.md

---

### D-07 pin-vs-catalog-only dispositions: only confirmed-at-source values are pinned
D-07: Krippendorff α = 0.7598 is pinned specifically at the ordinal level (the same data
yields 0.4765/0.7574/0.6621 at nominal/interval/ratio, so the value must always carry its
level), and the Landis & Koch (1977) kappa bands are pinned with edge-tie handling
labeled a convention choice, not the paper's exact wording. ICC (Koo & Li 2016) bands,
Kendall's W bands, dCor, partial correlation, and Cronbach→McDonald ω all ship
catalog-only/pointer-only with no numeric boundary and no fabricated locator, because
either the exact boundary values are unconfirmed at source (ICC) or no band citation
exists anywhere in the repo or the HQ-16 pack at all (Kendall's W).

**Rationale:** A value is pinned only if confirmed at source; otherwise catalog-only —
this is the phase's operationalization of the portfolio-wide "no fabricated locator"
standard applied per-item rather than per-phase.
**Source:** 18-CONTEXT.md

---

### File-disjoint single-writer wave split: Plan 18-A (routing+gates+catalogue) ∥ Plan 18-B (effect-size conventions)
D-08: two parallelizable plans, serialized only at the orchestrator's tracking-file
merge. Plan 18-A writes `dsx/checks/stats.py`, `dsx/spec.py`,
`references/test-selection.md`, `references/finding-codes.md` (regenerated), gate
fixtures and gate tests. Plan 18-B writes `dsx/mathx.py`,
`templates/APA-TABLE-research.md`, and extends the existing effect-size tests, minting no
finding code so it never touches `finding-codes.md`. The one coupling is semantic: 18-A's
`stats.py` imports `EFFECT_SIZE_KINDS`/`REPORT_ONLY_EFFECT_KINDS` from 18-B's `mathx.py`.

**Rationale:** Disjoint file sets let both plans run concurrently in Wave 1 with no
catalogue-regen contention; the single semantic seam is resolved defensively (see the
`getattr` pattern below) so each plan stays green in isolation regardless of merge order.
**Source:** 18-CONTEXT.md

---

### Field-shape decisions for D-03/D-05's deferred bindings: `operand_scale`, nested `icc`, flat kappa companions
18-CONTEXT.md explicitly deferred three field shapes to "a plan-time binding for S2-2";
18-A-PLAN.md resolved all three by accepting 18-RESEARCH.md's recommendations: (1) the
declared operand scale is a new field `analysis.operand_scale` with closed vocabulary
`{continuous, ordinal, dichotomous, nominal}`, registered in the existing
`_MEMBERSHIP_FIELDS` loop (DSX-STA-040 reuse — zero new code for recognition); (2) the
ICC triple nests under `analysis.icc: {model, type, definition}`, mirroring the existing
`design.cuped` nested-block precedent; (3) the kappa companions are flat:
`analysis.weights`, `analysis.p_pos`, `analysis.p_neg` (not nested, because `weights`
only applies to `weighted_kappa` while `p_pos`/`p_neg` apply to the whole kappa family,
so a shared parent block buys no completeness-check simplification).

**Rationale:** The ordinal-vs-dichotomous split in `operand_scale` is what encodes D-03's
">2 levels" whitelist without a separate level-count field; the ICC nesting gives
`DSX-STA-060` a single clean presence check before walking three sub-fields; flat kappa
fields avoid an extra nesting level for `weights`'s heterogeneous string-or-matrix type.
**Source:** 18-A-PLAN.md, 18-RESEARCH.md

---

## Lessons

### D-05's citation build gate resolves docstrings per nearest-enclosing-function, not per code
`scripts/gen-finding-catalogue.py`'s `check_d05()` maps each `report.add(...)` call site
to the docstring of its nearest enclosing `FunctionDef`. If all five report.add sites for
DSX-STA-050/051/060/061/062 lived inside one monolithic `_check_declared_association`,
the build gate would be satisfied by a single shared, generic docstring covering all
five — silently laundering five genuinely different citation obligations (Pearson/
Spearman/Kendall/point-biserial/phi family for 050/051; Shrout-Fleiss + McGraw-Wong for
060; a weighting citation for 061; Feinstein-Cicchetti Parts I+II for 062) into one pass.
The gate body was split into `_check_correlation_scale_kind` and
`_check_agreement_completeness` specifically so each carries its own attributable
docstring.

**Context:** Discovered by reading `_resolve_docstrings`'s parent-map walk directly
during research, before any plan was written — the mechanical build gate staying green
does not by itself prove the substantive citation obligation was met per code.
**Source:** 18-RESEARCH.md

---

### The five new codes are invisible to the D-05 citation gate unless named in the allowlist by exact code
`_D05_ALLOWLIST_PREFIXES` in `scripts/gen-finding-catalogue.py` does not include
`"DSX-STA-"` — that family carries ~40 legacy codes with no citation, so adding the
prefix would retroactively fail the build on all of them. Without adding
`DSX-STA-050`/`051`/`060`/`061`/`062` individually to `_D05_ALLOWLIST_CODES`, `--check`
would stay green even if the new `report.add` call sites shipped with no `Citation:` line
at all, silently defeating REQ-P18-03/04's own citation requirement.

**Context:** This was not spelled out at implementation granularity anywhere in
18-CONTEXT.md's own locator list; it was surfaced only by reading the live
`gen-finding-catalogue.py` file and following the `DSX-EXP-070`/`DSX-MET-021`/
`DSX-COH-040` exact-name precedent already established in that file.
**Source:** 18-RESEARCH.md

---

### A "cannot drift" comment does not enforce equality between two independently-declared literals
`dsx/checks/stats.py` defined `CORRELATION_FAMILY` (the set DSX-STA-051 keys on) as a
standalone literal, and separately defined `_ASSOCIATION_ROUTES` whose three
acceptable-coefficient sets union to the same six coefficients. A module comment claimed
the two "cannot drift," but nothing actually enforced the equality — a future contributor
could add a coefficient to one without the other, silently diverging DSX-STA-051's firing
set from `recommend_association`'s routing table under permanent D-06 numbering. Code
review verified the two sets were currently equal, then added
`CorrelationFamilyInvariantTest.test_family_equals_union_of_route_coefficient_sets` to
lock the claim with a checkable oracle.

**Context:** Caught at S2-4 code review (LOW-1), not during planning or execution — a
reminder that documentation-only invariants between independently-maintained constants
are exactly the kind of drift a structural test, not a comment, is needed to prevent.
**Source:** 18-REVIEW.md

---

### Verification-honesty requires updating prose that states a stale number, not just the pinned assertion values
When bumping `tests/test_finding_catalogue_invariant.py`'s `_EXPECTED_TOTAL` from 260 to
265 and extending `_MINTED_CODES`, the plan named only those two symbols — but two test
method names and their assertion failure messages literally said "260," which would have
contradicted the assertions they guarded. These were updated to "265" as a self-initiated
honesty-driven adjustment, while `_SNAPSHOT_TOTAL` (256) and the byte-frozen
`tests/fixtures/finding-codes-phase12.md` were correctly left untouched.

**Context:** A repo-wide verification-honesty norm (never let a claim/prose contradict
what the code actually asserts) applied even inside a test file whose pinned numeric
constants were the plan's only explicitly named targets.
**Source:** 18-A-SUMMARY.md

---

### Existing declaration-only primitives already handle edge cases the new gates implicitly depend on
Adversarial review confirmed two pre-existing helper behaviors the new gates rely on
without re-testing them explicitly: `is_blank` (spec.py) returns `False` for any numeric
value including `0.0`, so a legitimate `p_pos: 0.0`/`p_neg: 0.0` is treated as present and
does not false-fire DSX-STA-062; and `normalize` (spec.py) calls `str(value)` first, so a
non-string ICC sub-field like `icc.model: 123` becomes `"123"` (correctly out-of-vocab,
firing DSX-STA-060) rather than raising an `AttributeError`.

**Context:** Neither behavior was newly built for Phase 18 — both were confirmed, not
assumed, by deliberately probing the new gates with adversarial fixture values at code
review, rather than trusting that reusing existing `is_blank`/`normalize` was automatically
safe for the new field shapes.
**Source:** 18-REVIEW.md

---

## Patterns

### Dataless string-to-set routing lookup, with `inspect.signature` as the anti-two-stage proof
`recommend_association(estimand_kind: str)` takes no data, no `n`, no distribution flag —
its signature is asserted by `inspect.signature(...)` to equal exactly `["estimand_kind"]`
in `test_declared_association_routing.py`. This is a stronger anti-two-stage guarantee
than a branch bolted onto a function that already accepts data-shape arguments (like
`recommend_test`), because a future contributor adding any data/n/flag parameter turns
the structural test red immediately, rather than relying on a docstring claim or a code
review catching a semantic violation.

**When to use:** Any routing/recommendation function whose entire value proposition is
"decides from declared metadata alone, never from computed data" — assert the parameter
list structurally, not just behaviorally, so the anti-two-stage invariant cannot silently
rot as the function evolves.
**Source:** 18-A-SUMMARY.md, 18-RESEARCH.md

---

### Split a gate body by predicate group so per-function D-05 docstring resolution stays honest
`_check_declared_association` dispatches to two private helpers —
`_check_correlation_scale_kind` (DSX-STA-050/051) and `_check_agreement_completeness`
(DSX-STA-060/061/062) — each carrying its own `Citation:`/`Structural criterion:`
docstring, rather than one monolithic function with a single shared docstring.

**When to use:** Any gate function about to emit findings that draw on genuinely
different citations or remedy logic — split along predicate/citation boundaries before
`check_d05()`'s nearest-enclosing-function resolution turns a shared docstring into an
unintentional citation-laundering surface.
**Source:** 18-RESEARCH.md, 18-A-SUMMARY.md

---

### isinstance-before-normalize for a declared field spanning both an enum and a structural type
The weighted-kappa `weights` field admits three legitimate shapes — `"linear"`,
`"quadratic"`, or an explicit matrix (a list/nested sequence) — unlike every other
closed-vocabulary field in the codebase, which is a scalar string checked via
`normalize(value) not in vocab`. Calling `normalize()` (which does `str(value)` first) on
a matrix would silently stringify it into text that matches nothing, producing a false
DSX-STA-061 firing on a perfectly valid declaration without ever raising. The guard
instead branches on `isinstance` first: a string is checked against
`{"linear", "quadratic"}`; a non-empty list/tuple is accepted as an explicit matrix
without further validation; anything else fires DSX-STA-061.

**When to use:** Any declared field whose valid values legitimately span both a closed
string vocabulary and a non-string structural type — branch on `isinstance` before any
`normalize`/`str()` call, and add a fixture proving the structural-type branch does NOT
false-fire.
**Source:** 18-RESEARCH.md (Pitfall 5), 18-A-SUMMARY.md

---

### Defensive `getattr(module, attr, default)` for a cross-plan seam that is inert until the other plan merges
The DSX-STA-012 branch in `dsx/checks/stats.py` (Plan 18-A) reads
`getattr(mathx, "REPORT_ONLY_EFFECT_KINDS", frozenset())` rather than a direct name
import, so the branch is a harmless no-op (falls through to the pre-existing DSX-STA-012
firing) when Plan 18-B's `mathx.py` registry has not yet merged, and activates
automatically the moment it does — without either plan needing to know the other's merge
order or timing.

**When to use:** Any file-disjoint parallel-plan split (D-08-style) with exactly one
semantic (not file-level) coupling point — prefer a defensive attribute lookup with an
inert default on the consuming side over a hard name import, so each plan's own isolated
test run stays green regardless of merge order.
**Source:** 18-A-PLAN.md, 18-A-SUMMARY.md

---

### Guarded cross-plan seam oracle via `unittest.skipUnless` on a live-seam probe
Plan 18-B's `tests/test_effect_size_kind.py` adds
`test_report_only_kappa_fires_neither_011_nor_012_and_reports_ok`, guarded by
`unittest.skipUnless(_report_only_seam_is_live(), ...)` — a small helper that probes
whether `stats.check` currently produces the report-only behavior for a `kappa` kind. The
assertion SKIPS (not fails) when Plan 18-A's consuming branch is absent, and RUNS and
enforces once both plans are merged — confirmed by 18-VERIFICATION.md and the
S2-4 review re-run, where the oracle ran (not skipped) and passed.

**When to use:** Any test that pins behavior spanning two independently-mergeable units
of work — skip on absence of the dependency (never fail red on a legitimate in-progress
state), and enforce automatically once the dependency lands, rather than hard-coding an
assumed merge order into the test.
**Source:** 18-B-PLAN.md, 18-B-SUMMARY.md, 18-VERIFICATION.md

---

### A pinned numeric reference value must always carry its level of measurement
`KRIPPENDORFF_REFERENCE` in `mathx.py` is level-keyed (`ordinal → 0.7598`,
`nominal → 0.4765`, `interval → 0.7574`, `ratio → 0.6621`) rather than a single bare
number, because the same underlying data yields a materially different, equally "correct"
α depending on the declared level of measurement — a level-free pin would be simply
wrong, not just imprecise. A lookup with no level (or a level-free pin) is explicitly
asserted to be rejected.

**When to use:** Any citation-backed numeric constant whose value is a function of a
categorical parameter (level of measurement, model assumption, edge-tie convention,
etc.) — key the pin by that parameter structurally, and test that omitting the parameter
does not silently return a value for the wrong context.
**Source:** 18-B-SUMMARY.md, 18-CONTEXT.md (D-07)

---

## Surprises

### The requirement's own citation paraphrase was wrong, and had to be corrected without editing REQUIREMENTS.md
REQ-P18-04's parenthetical described the kappa companions as "raw agreement + prevalence,
per Feinstein & Cicchetti 1990" — but the operator-answered HQ-16 correction established
the actual recommendation (p_pos AND p_neg specifically) lives in the companion Part II,
not the paraphrase's framing. Rather than treating the requirement's wording as
authoritative or silently rewriting REQUIREMENTS.md, the phase implemented the
HQ-16-corrected intent and filed the one-word requirement alignment as a non-blocking
HQ-20 item for the operator to accept by silence.

**Impact:** Shows a requirement document itself can carry a citation defect that
execution must catch and correct against primary sources, while still respecting that
rewording a requirement is an escalation the loop does not perform on its own authority.
**Source:** 18-CONTEXT.md (D-04)

---

### A "cannot drift" invariant between two hand-written literals was unverified until code review found it
`CORRELATION_FAMILY` and the union of `_ASSOCIATION_ROUTES`'s three coefficient sets were
documented in a comment as unable to drift apart, but no test actually enforced their
equality anywhere in Plan 18-A's TDD cycle — the gap survived RED/GREEN/REFACTOR and was
only caught adversarially at the separate S2-4 code review pass, which verified the two
were currently equal and then added a dedicated invariant test.

**Impact:** Confirms that a phase's own TDD loop, scoped to the behavior each task is
actively building, does not automatically catch cross-constant consistency invariants
that a later, differently-framed adversarial read is needed to surface.
**Source:** 18-REVIEW.md

---

### Both canonical fixtures needed zero edits to stay silent — verified empirically, not assumed from D-08's wording
D-08's "extend, not replace" instruction for the canonical fixtures could easily have
been read as "an edit is owed." Research read both `examples/good-ANALYSIS-SPEC.yaml` and
`examples/bad-ANALYSIS-SPEC.yaml` in full and confirmed neither `analysis:` block trips
any of the five new predicates as declared today (neither declares a correlation
coefficient, neither `estimand_kind` is `agreement`/`method_comparison`, neither declares
ICC/kappa sub-fields) — so no fixture edit was required, and Plan 18-A's Task 3 explicitly
recorded that fact rather than adding an illustrative row reflexively.

**Impact:** Avoided an unnecessary fixture edit and its associated regression-surface
increase; demonstrates that a "safety rail" instruction (extend, not replace) is not the
same as a mandate to always extend.
**Source:** 18-RESEARCH.md, 18-A-SUMMARY.md

---

### D-06's own prose was ambiguous about whether DSX-STA-012 should keep firing for report-only kinds
Read literally, D-06's "recognised... no nonsensical nag" could mean DSX-STA-012 should
simply stop firing for a report-only kind like `kappa`; but "remedy text branches"
suggested the finding still fires, just reworded. Both readings are defensible from the
persona-round prose alone. Research flagged this explicitly as Pitfall 6 / Assumption A4
and committed to a specific reading (report.ok, firing neither 011 nor 012) before
planning could proceed, rather than leaving the ambiguity for the planner to resolve
independently — and the Wave-1 merge gate and S2-4 verification later confirmed that
reading was in fact the one the persona round intended.

**Impact:** Shows a single ambiguous sentence in a locked decision document can require an
explicit, separately-recorded interpretive commitment before implementation — and that
getting it wrong would have either reintroduced the nag D-06 forbade or silently dropped
expected test coverage.
**Source:** 18-RESEARCH.md (Pitfall 6, Assumption A4)

---
