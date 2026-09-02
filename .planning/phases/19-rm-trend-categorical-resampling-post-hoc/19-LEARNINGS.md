---
phase: 19
phase_name: "RM, trend, categorical, resampling, post-hoc"
project: "gsd-dsx"
generated: "2026-09-02"
counts:
  decisions: 10
  lessons: 6
  patterns: 7
  surprises: 5
missing_artifacts:
  - "UAT.md"
---

# Phase 19 Learnings: RM, trend, categorical, resampling, post-hoc

## Decisions

### D-01: Ten new HIGH codes across six pre-allocated decades, split not merged
`DSX-STA-070/080/081/090/100/110/111/120/121/122` are all HIGH — the "recognised-but-contradictory
/ incomplete declaration" class, the same class as the HIGH `DSX-STA-041/050/051/060/061/062`. One
code per explicit "Gate:/blocks" clause in the requirements, split (not merged) because each
failure mode has a distinct remedy, distinct citation, and distinct declared-field predicate under
permanent D-06 numbering. Catalogue moves 265 → 275.

**Rationale:** REQ language "blocks / must / mandatory" pins HIGH; splitting rather than merging keeps each code's citation and remedy independently auditable and independently allowlist-able.
**Source:** 19-CONTEXT.md D-01

---

### D-02: Routing integration shape extends the Phase-18 hybrid pattern verbatim
Thin dataless `recommend_*` functions per family (returning the acceptable-test/interval SET per
declared context) plus `_check_declared_*` gates sitting beside the untouched `recommend_test`,
wired into `check()` at both call sites. New rows (incl. DEPRECATED + pointer) land in
`references/test-selection.md` as the doc mirror, in lockstep with the code in the same commit;
`references/finding-codes.md` regen happens in the gate commit; new codes join
`_D05_ALLOWLIST_CODES` by exact name.

**Rationale:** the dataless signatures are the mechanical anti-two-stage proof (no data, no n, no distribution flag) — the no-autoswitch test guards exactly those signatures, extending REQ-P18-06 doctrine to the six new families.
**Source:** 19-CONTEXT.md D-02

---

### D-03: Declared-field shapes fixed at persona-round time; reuse-before-add discipline
Reuse an existing declared field where one plausibly exists; otherwise add an additive,
membership-guarded sub-vocab in `dsx/spec.py` `_VOCABULARIES` so a mis-slotted value fires the
existing `DSX-STA-040` for free (the Phase-18 mechanism). Absence of a trigger field is
non-blocking (D-10). The exact field NAMES (as opposed to their shapes) were explicitly delegated
to plan-time (19-A-PLAN.md `field_bindings`, resolving 19-RESEARCH.md Open Questions OQ-1..OQ-8).

**Rationale:** fixing shapes at persona-round time while deferring exact names to the planner lets the round converge on the load-bearing semantics (what a field means) without stalling on naming bikeshedding.
**Source:** 19-CONTEXT.md D-03

---

### D-04: DEPRECATED routing-off rows are structurally distinct from pointer rows
Yates (P19-03), SNK + unprotected-LSD-at-k>3 (P19-05), and Vuong-for-zero-inflation (P19-07) ship
as doc-only rows in `references/test-selection.md` flagged `status: deprecated` — minting no code,
adding no blocking behaviour, and never selected by any `recommend_*` function as a default. A
**pointer row** (mixed-model/GEE, log-linear, ZIP/hurdle) is routing-neutral and points OUTWARD to
an out-of-detailed-scope method ("this route exists"); a **DEPRECATED row** is routing-off and
points at an IN-scope method that should not be used, carrying a "use X instead" redirect plus the
why-citation (Yates→N-1 chi-square Campbell 2007; SNK/LSD-k>3→protected post-hoc Hayter 1986 JASA
81(396):1000-1004; Vuong→misuse-finding only, Wilson 2015, no replacement endorsed). Active
deprecation enforcement ("declared-deprecated-method blocks") is a named D-13 deferral, not shipped.

**Rationale:** the structural distinction (routing-neutral vs routing-off) lets the catalogue retire a bad-but-in-scope method without the heavier decision of actively blocking every analyst who still declares it.
**Source:** 19-CONTEXT.md D-04

---

### D-05: Zimmerman 2004 scoped to two-group with an explicit principled-extension flag on the k-group span
Zimmerman 2004 (BJMSP 57(1):173–181) tested Levene-then-t in the two-group case only, but the
`DSX-STA-110` gate spans k-group ANOVA (Brown-Forsythe/Bartlett/Fligner-Killeen are k-group scale
tests). Resolution: scope the *cited empirical result* to two-group and attach an explicit
principled-extension flag to the k-group span — `principled-extension: two-group→k-group; mechanism
= a location test conditioned on a data-dependent variance pretest distorts Type I error; mechanism
is invariant to group count; empirical k-group magnitude UNVERIFIED`. Bancroft 1944 (the candidate
general k-group pretest-bias authority) ships not-in-hand/backlog, never pinned unverified.

**Rationale:** citing Zimmerman alone for a k-group gate is the citation-overreach this portfolio forbids above all; the gate's predicate ("variance test declared as a location-choice pretest → block") does not actually need Zimmerman's magnitude, only the mechanism, so rigour favours honest scoping plus a flag over an unread citation.
**Source:** 19-CONTEXT.md D-05

---

### D-06: Over-block guards on the predicate rulings for 070/110/111/122
Two-stage sphericity (070) keys on the DECLARED "Mauchly-then-correct-if-significant" procedure,
never on the mere presence of repeated measures — else it false-blocks the legitimate
mixed-model/GEE route, which never invokes a sphericity step. Variance-precondition (110) reads the
DECLARED **role**: pretest/precondition → block (Zimmerman); scale/dispersion-is-the-estimand →
allow (the scale test is the correct primary analysis); role undeclared → block for
declaration-incompleteness — keyed on the declared role, never on Levene/BF/Bartlett/Fligner
presence. Observed power (111) fires narrowly on `{observed, post_hoc}` only; broadening to all
post-hoc power uses is a named D-13 deferral pending Hoenig-Heisey source confirmation. NNT (122)
is a GATE on the internal completeness doctrine — a bare point NNT is active false precision (its
sampling distribution is discontinuous when the ARR CI crosses zero), the same self-scoping class
as the resampling quadruple and Phase-18's `DSX-STA-050`.

**Rationale:** each over-block guard exists to prevent the gate from false-blocking a legitimate declaration that merely resembles the defect on the surface — the recurring "point-biserial-whitelist" lesson from Phase 18.
**Source:** 19-CONTEXT.md D-06

---

### D-06 (adjudication): CMH-with-declared-stratification ships as a row, not a gate, this phase
The persona round split on exactly one call: the Statistician's Simpson's-paradox reading
(declaring CMH while pooling across un-named strata is a real error) is statistically correct, but
REQ-P19-03 is the *only* requirement with no "Gate:" clause and no pre-allocated decade — and the
same requirement family wrote an explicit gate clause for the exposure/offset case (REQ-P19-07),
so the author deliberately did not for CMH. The orchestrator adjudicated: CMH ships as a
non-blocking row surfacing a declared-stratification field; the stratifier concern is a named D-13
deferral, not a silent drop.

**Rationale:** minting a CMH gate would need a code from outside the theme-decade scheme, breaking committed D-06 numbering discipline, and adds unrequested scope; the tie-break favoured the smaller provable claim plus an honest named deferral over an unrequested gate.
**Source:** 19-CONTEXT.md D-06

---

### D-07: D-05 dispositions are almost entirely catalog-only, because the gates check presence, not computed statistics
Pins are confirmed bibliographic locators, algebraic identities (Campbell's χ²₍N−1₎ identity,
Hoenig-Heisey's observed-power-as-monotone-f(p) identity), and the Newcombe A/B disambiguation
(Paper B = Stat Med 17(8):873–890 = RD; Paper A = 857–872 = single-proportion — the highest-value
pin in the set). Everything doctrinal/chapter-level/house-convention ships catalog-only. The
load-bearing DO-NOT-HARD-CODE flags: Greenhouse-Geisser epsilon (computed from data, never a
fixture; NOT the reversed 1958 Annals paper), the Hamed-Rao autocorrelation-significance lag
threshold, Davidson-MacKinnon's 19/99-vs-399/1499 (never conflated, B's value never checked),
Efron's "BCa" acronym (Efron-Tibshirani 1993, not the 1987 JASA text), Hayter's numeric inflated-α,
Brown-Cai-DasGupta's n≤40 cutoff, and McCullagh-Nelder's §6.2 page.

**Rationale:** a declaration-only gate needs no computed value, so pinning a numeric detail the gate never checks would be false authority — the discipline scopes citation obligations to exactly what the mechanism uses.
**Source:** 19-CONTEXT.md D-07

---

### D-08: Two sequential waves, rows-then-gates, with the conditional 19-B dropped before planning
Wave 1 (19-A) writes every `recommend_*` function, sub-vocabulary, and doc row while the catalogue
provably stays unchanged at 265; Wave 2 (19-C, `depends_on: [19-A]`) reads those frozen names to
write the ten gates, wire them into `check()`, extend `_D05_ALLOWLIST_CODES`, and extend the bad
fixture, taking the catalogue to 275. Every shared file (`stats.py`, `spec.py`,
`test-selection.md`, `finding-codes.md`) has exactly one writer per wave, so `stats.py` is never
concurrently written. The conditional 19-B (`dsx/mathx.py` band growth) was researched and dropped
before planning: no REQ-P19 requirement text names an effect-size band, and Kendall's W — the only
RM/Friedman candidate — is already catalog-only from Phase 18.

**Rationale:** rows-then-gates is preferred over a merged one-wave shape because it freezes the declared-field names before the fixtures written against them exist, and it gives an intermediate 265-checkpoint that catches a premature or accidental mint.
**Source:** 19-CONTEXT.md D-08, 19-RESEARCH.md "The 19-B Verdict"

---

### SHAPE-override: dedicated `analysis.trend_test` / `analysis.variance_test` fields instead of the single-valued `analysis.test`
19-A-PLAN.md's `field_bindings` block deliberately deviates from 19-RESEARCH.md's sketch, which had
proposed reading the trend/variance gate triggers off the single-valued `analysis.test`. The plan
instead binds gates 080/081 to a dedicated `analysis.trend_test` field (a string OR a list of
strings — a defective spec may declare more than one trend analysis) and gate 110 to a dedicated
`analysis.variance_test` field.

**Rationale:** three-fold — (1) `analysis.test` is single-valued but 080 (`cochran_armitage`), 081 (`mann_kendall`/`sens_slope`), and 110 (a variance test) are three mutually-exclusive triggers, so keying all three on `analysis.test` would make the D-08 merge gate "the bad fixture fires all ten in one audit" unsatisfiable; (2) it dodges 19-RESEARCH.md Pitfall 1, where a trend/variance token placed in `analysis.test` would trip a spurious `DSX-STA-041` from the untouched `_check_declared_test`; (3) it is semantically precise for 110 — the pretest scenario has the LOCATION test as `analysis.test` and the variance test as a declared companion, so reading the variance test off `analysis.test` would misread the scale-estimand case.
**Source:** 19-A-PLAN.md `field_bindings` ("TREND / VARIANCE FIELD DECISION")

---

## Lessons

### A disposition token can accidentally re-name the forbidden concept it exists to reject
The first GREEN implementation of `recommend_variance_role` used the disposition token
`drop_the_pretest_use_welch_unconditionally`, which contains the substring "pretest" that the
no-autoswitch proof asserts must be absent (the precondition disposition must not itself name a
pretest gate). It was renamed to `use_welch_unconditionally` mid-task, and the proof then held.

**Context:** caught inside the same RED→GREEN cycle (19-A Task 2), not at a later review — the plan's intent (the precondition role never endorses a variance pretest as a location gate) was preserved exactly by the rename.
**Source:** 19-A-SUMMARY.md Deviations from Plan

---

### Distinguishing "a concept" from "a printed number" requires care even when both derive from the same citation
19-A-PLAN.md's Task 3 action text asked for a prose note distinguishing "19/99 (an exactness
floor)" from "399/1499 (a recommended minimum)" for Davidson-MacKinnon 2000's resampling `B`, while
the phase's own hard constraint forbids hard-coding either pair as a numeric statistic. Resolved by
writing the conceptual distinction — an exactness floor is not the same thing as a
recommended-minimum `B`, both confirm-at-source, neither printed — without ever printing the
specific numeric floors.

**Context:** the gate never checks `B`'s value regardless of this distinction, so the constraint bites the doc-only sentence rather than the gate predicate itself.
**Source:** 19-A-SUMMARY.md Deviations from Plan

---

### A phase's own instructed catalogue bump can invalidate its own earlier wave's test pins
Wave 2 (19-C) bumping the catalogue 265→275 per its own Task 2 instructions broke two Wave-1 (19-A)
test pins that had frozen the pre-bump reality: `tests/test_p19_categorical_rows.py`'s
`_EXPECTED_TOTAL` (a REQ-P19-03 no-mint proof kept in lockstep with
`test_finding_catalogue_invariant.py`) and `tests/test_causal_verb_golden.py`'s golden CRITICAL/HIGH
set for `bad-ANALYSIS-SPEC.yaml` (predating the Task-3 fixture extension). Both were rebaselined in
the same wave (commit `bab4132`) as a blocking auto-fix, not treated as scope creep.

**Context:** full-suite verification after the bad-fixture extension and the catalogue regen caught this — neither task's own narrower verification would have — echoing the same cross-plan lockstep-gap class that a prior milestone's byte-anchor lesson (v2.2 Phase 15) also surfaced.
**Source:** 19-C-SUMMARY.md Deviations from Plan

---

### `is_blank` treats legitimate falsy declarations as present, so numeric/enum zero-values don't false-fire
`is_blank(0)` and `is_blank(0.0)` both evaluate `False` — only `None`, the empty string, and an
empty container are blank. So a declared `resampling.seed: 0`, a declared `dose_scores: 0`, or an
explicit `autocorrelation_handling: none` are all non-blank and SATISFY their respective gates;
`DSX-STA-081`/`DSX-STA-090` do not false-fire on these legitimate explicit declarations.

**Context:** adversarially probed during code review and confirmed against the trend and resampling gate test modules — a value that looks "empty" on a casual read (0, or the literal string "none") is not the same thing as an absent field.
**Source:** 19-REVIEW.md "Adversarially probed, cleared with no finding"

---

### `normalize()`'s `str(value)` coercion turns a wrong-typed declaration into a loud recognition failure, never a crash
Because `normalize()` calls `str(value)` before comparison, a non-string `sphericity_correction` /
`omnibus` / etc. yields a token that is simply out-of-vocab (recognised loudly via `DSX-STA-040`)
rather than raising an `AttributeError`. `_check_declared_resampling` additionally guards
`isinstance(resampling, dict)`, and `_check_declared_trend` handles str-or-list-or-other, so a
dict/other `trend_test` yields a harmless non-matching token rather than a crash.

**Context:** confirmed during adversarial code-review probing of crash-safety on wrong-typed declarations — no crash path was found across any of the ten new gates.
**Source:** 19-REVIEW.md "Adversarially probed, cleared with no finding"

---

### A measured golden-set delta is the sanctioned way to rebaseline a pinned fixture; absorbing unexpected drift is not
When `test_causal_verb_golden.py`'s golden CRITICAL/HIGH set for `bad-ANALYSIS-SPEC.yaml` needed
updating after the Task-3 fixture extension, the delta added was exactly the ten measured
`DSX-STA-*` codes the extension was designed to trigger — nothing more, nothing dropped. This is
the sanctioned "fixture built to demonstrate the new catch" case, distinct from editing a golden
set to silently absorb an unexpected drift.

**Context:** the distinction mattered because a golden-set edit is exactly the kind of change that could mask a regression if applied carelessly; the fix explicitly named which case applied (measured, not absorbed) as part of its own justification.
**Source:** 19-C-SUMMARY.md Deviations from Plan

---

## Patterns

### Per-family `_check_declared_*` helpers, each with an attributable `Citation:` docstring, to defeat citation-laundering
`scripts/gen-finding-catalogue.py`'s `_resolve_docstrings` (:303–342) maps every `report.add(...)`
call site to the docstring of its NEAREST enclosing `FunctionDef`. A single dispatcher body
emitting all ten Phase-19 codes would satisfy the D-05 build gate with one shared, generic
docstring — laundering seven genuinely distinct citation obligations (Greenhouse-Geisser;
Cochran-Armitage/Hamed-Rao; Davidson-MacKinnon/Efron; Hayter/Games-Howell; Zimmerman;
Hoenig-Heisey/Lakens; Brown-Cai-DasGupta/McCullagh-Nelder/internal-completeness) into one pass.
Phase 19 splits into seven per-family helpers (`_check_declared_rm_sphericity`, `_trend`,
`_resampling`, `_posthoc`, `_variance_role`, `_power_reporting`, `_proportion_count`, at
`stats.py:1078–1308`), each carrying its own `Citation:` + `Structural criterion:` docstring line,
dispatched from a thin `_check_declared_advanced_stats`.

**When to use:** whenever one gate function would otherwise emit multiple codes drawing on genuinely different citations, in any repo whose D-05-style build gate resolves citations per-function rather than per-code.
**Source:** 19-RESEARCH.md Pattern 1, 19-C-PLAN.md, 19-SECURITY.md T-19-C-02

---

### Wire a new declaration-only dispatcher at BOTH of `check()`'s existing call sites
`dsx/checks/stats.py::check()` calls its declaration gates from two places: the `if not tests:`
early-return branch and the post-loop return. A pure declaration-only spec (an RM/trend/resampling
plan with no computed `results.tests` yet) hits only the early-return branch, so
`_check_declared_advanced_stats(analysis, spec, report)` had to be added at both sites
(`stats.py:485` and `:501`) or a declaration-only spec would silently skip every Phase-19 gate.

**When to use:** any time a gate-dispatch function has more than one call site keyed on different control-flow branches of the same `check()` — verify the new dispatcher is wired at every site, not just the "obvious" one, and prove it with an inline `getsource(...).count(...)>=2` assertion.
**Source:** 19-RESEARCH.md Pattern 2, 19-C-PLAN.md Task 1 verify

---

### DEPRECATED vs pointer rows as a doc-only, code-parsing-free routing-off mechanism
`references/test-selection.md` is parsed by no code path (only `dsx/frame/prereg.py` names the
*concept* "test-selection function" in prose, never reading the file). A `status: deprecated` row
(Yates, SNK, unprotected-LSD-k>3, Vuong) mints no code and adds no behaviour, but is structurally
distinct from a `status: pointer` row (mixed-model/GEE, log-linear, ZIP/hurdle): a pointer row is
routing-neutral and points OUTWARD to an out-of-detailed-scope method ("this route exists"); a
DEPRECATED row is routing-off and points at an IN-scope method that should not be used, carrying a
"use X instead" redirect plus the why-citation.

**When to use:** whenever a catalog needs to retire a method without minting an enforcement code (active deprecation enforcement is a separate, heavier decision) — a doc-only status column, combined with `recommend_*` functions that never select the deprecated row as a default, ships the retirement safely at zero code cost.
**Source:** 19-RESEARCH.md Pattern 3, 19-CONTEXT.md D-04

---

### Rows-then-gates two-wave split freezes declared-field names before the fixtures that exercise them are written
Wave 1 (19-A) writes every `recommend_*` function, sub-vocabulary, and doc row while the catalogue
provably stays unchanged (265); Wave 2 (19-C, `depends_on: [19-A]`) reads those frozen names to
write the ten gates and extend the bad fixture, taking the catalogue to 275. The import seam in
`stats.py` is deliberately frozen at the end of Wave 1 — including one constant unused that wave,
`DOSE_SCORE_SCHEMES` — so Wave 2's gate helpers never re-touch the single-writer import block.

**When to use:** any phase that mints multiple codes reading multiple new declared-field names, where the plan wants an intermediate merge-gate checkpoint (catalogue count unchanged) before the higher-risk gate-wiring work begins.
**Source:** 19-CONTEXT.md D-08, 19-A-PLAN.md, 19-A-SUMMARY.md "Notes for 19-C"

---

### Scalar closed-vocab fields join the flat `_MEMBERSHIP_FIELDS` loop for free recognition; nested/list-valued fields are validated inside their own gate helper
The six scalar fields (`sphericity_correction`, `autocorrelation_handling`, `variance_test`,
`variance_test_role`, `power_reporting_type`, `proportion_ci_method`) are registered as
`(field_name, vocabulary)` tuples in `_MEMBERSHIP_FIELDS` (`stats.py:40-44`) so a mis-slotted value
fires the existing `DSX-STA-040` for free — zero new code for the recognition half. The nested
`analysis.resampling.method` and the str-OR-list `analysis.trend_test` are deliberately excluded
from that flat loop and validated inside their own Wave-2 gate helper instead, because the flat
loop only handles single scalar values.

**When to use:** adding a new closed-vocabulary declared field to a `dsx`-style declaration gate library — default to the flat membership loop for scalars; fall back to a bespoke in-helper check only when the field is structurally nested or multi-valued.
**Source:** 19-A-PLAN.md Task 2, 19-RESEARCH.md "Don't Hand-Roll"

---

### Exact-name D-05 allowlisting, never a family-prefix add, to scope new citation obligations
`_D05_ALLOWLIST_PREFIXES` does not contain `"DSX-STA-"` — a ~40-code legacy family carrying no
citation. All ten Phase-19 codes are appended to `_D05_ALLOWLIST_CODES`
(`scripts/gen-finding-catalogue.py:168-178`) by exact code string, with a dated Phase-19 comment
block after the Phase-18 precedent block, so `--check` enforces the citation discipline on exactly
the ten new codes without dragging the ~40 uncited legacy siblings into the build gate.

**When to use:** adding a citation obligation to a subset of codes within an existing, partially-uncited code family — allowlist by exact name, never by the family's prefix.
**Source:** 19-RESEARCH.md Pitfall 3 / Anti-Patterns, 19-C-PLAN.md Task 2, 19-C-SUMMARY.md key-decisions

---

### Extend-not-replace fixture discipline, with every new bad-fixture trigger field kept in-vocabulary
`examples/bad-ANALYSIS-SPEC.yaml`'s `analysis:` block is extended (never replaced) with ten
dedicated fields — one per code — each drawn from a valid vocabulary member, so the extension fires
exactly the ten intended gates in one `stats.check` pass with no spurious `DSX-STA-040` noise.
`examples/good-ANALYSIS-SPEC.yaml` is verified silent on all ten and left unedited rather than
touched defensively.

**When to use:** any phase extending the canonical bad/good fixture pair to exercise new gates — choose in-vocabulary trigger values deliberately (an out-of-vocab value would fire the unrelated recognition code instead of, or in addition to, the intended gate) and confirm the good fixture's silence empirically rather than assuming it.
**Source:** 19-C-PLAN.md Task 3, 19-REVIEW.md files-reviewed table, 19-VERIFICATION.md fixture-discipline

---

## Surprises

### Phase 19 is the first phase in the v2.3 milestone to carry HIGH-severity threats
19-SECURITY.md notes explicitly: "Unlike Phases 17–18 (all-low registers), Phase 19 carries two
HIGH threats" — T-19-C-01 (a new code shipping uncited because `DSX-STA-` is not an allowlisted
D-05 prefix) and T-19-C-02 (a monolithic gate laundering seven citation obligations under one
shared docstring) — despite the phase's own persona round deciding NOT to engage the Auditor lens
because the work is "declaration-only string/structure comparisons with no data path, no leakage
surface and no security surface."

**Impact:** the declaration-only framing that exempted Phases 17–19 from Auditor-lens review did not exempt Phase 19 from carrying its highest-severity threats to date; both were pre-empted by design (the seven-helper split, exact-name allowlisting) rather than discovered as defects, and both were re-run green from a clean tree before the register closed.
**Source:** 19-SECURITY.md

---

### 19-CONTEXT.md's own D-08 single-writer table misplaced the `_D05_ALLOWLIST_CODES` location
19-CONTEXT.md's D-08 states `_D05_ALLOWLIST_CODES` lives in `dsx/spec.py`; both 19-A-PLAN.md and
19-C-PLAN.md carry an explicit "CORRECTION to 19-CONTEXT.md D-08's single-writer table" surfacing
that it actually lives in `scripts/gen-finding-catalogue.py:168-178`. Under the corrected
allocation, `dsx/spec.py` is a Wave-1-only write and `scripts/gen-finding-catalogue.py` is a
Wave-2-only write — the single-writer-per-wave invariant still holds, but only because the planner
caught and fixed the CONTEXT document's own locator error before any file was written.

**Impact:** shows the plan-checking discipline catching an error in the upstream persona-round decision document itself, not just in downstream code — a CONTEXT.md decision record is not infallible ground truth and was independently re-verified against the live tree before being trusted.
**Source:** 19-A-PLAN.md single_writer_proof, 19-C-PLAN.md single_writer_proof

---

### 8 of the 10 gate-code doc entries were already present before Wave 2 started
19-A (Wave 1) wrote "Wave 2" forward-reference doc entries for eight of the ten gate codes while
authoring the six `test-selection.md` sections, so when 19-C (Wave 2) reached its own doc-lockstep
task, only the DSX-STA-110/111 variance/power section remained to be added — the other eight
needed no edit at all.

**Impact:** avoided duplicate or conflicting doc rows for the same code across two waves; recorded explicitly as an "Observation (no edit owed)" in 19-C-SUMMARY.md rather than silently skipped, so the doc-lockstep claim in the plan's `must_haves` stays auditable.
**Source:** 19-C-SUMMARY.md "Observation (no edit owed)"

---

### Dead imports passed every automated gate because this repo's check pipeline runs no linter
`dsx/checks/stats.py` imported `DOSE_SCORE_SCHEMES` and `RESAMPLING_METHODS` from `dsx.spec` but
referenced neither in executable code — `DOSE_SCORE_SCHEMES` appeared on exactly one line (the
import) and `RESAMPLING_METHODS` only in a comment and a docstring, never as an evaluated binding.
`scripts/check.sh` runs unittest + catalogue `--check` + gate-contract + determinism only, with no
linter, so Python's own silence on unused imports meant the S3-3 gate passed regardless; only the
S3-4 adversarial code review caught it.

**Impact:** confirms that unused-but-harmless imports are structurally invisible to this repo's entire automated verification chain and rely entirely on human/adversarial code review to catch — a class of finding no oracle in the Nyquist validation map would have surfaced.
**Source:** 19-REVIEW.md LOW-1

---

### DSX-STA-100 also fires on an omnibus the catalogue does not recognise at all, not only on a mismatched post-hoc pair
Because `POSTHOC_FAMILY_MAP.get(omnibus_family, frozenset())` defaults to an empty set for an
unrecognised omnibus, any declared post-hoc paired with an out-of-map omnibus is reported as "not
matched" — broader firing than "post-hoc family ≠ omnibus family" might suggest at first read.
`omnibus` is intentionally NOT registered in `_MEMBERSHIP_FIELDS`, so only the four covered
families (`welch_anova`/`anova`/`kruskal_wallis`/`friedman`) are recognised; anything else blocks
under the declaration-completeness doctrine ("an omnibus+post-hoc pair the catalogue cannot
recognise cannot be validated as matched, and blocking is the safe direction").

**Impact:** recorded as a "scoping observation, not a defect" in code review — the good fixture does not false-fire, so there is no regression, but broadening `POSTHOC_FAMILY_MAP`'s recognised-omnibus set is left as a future-phase decision rather than something this phase's requirement text made obvious.
**Source:** 19-REVIEW.md "Scoping observation (not a defect — recorded, no fix)"
