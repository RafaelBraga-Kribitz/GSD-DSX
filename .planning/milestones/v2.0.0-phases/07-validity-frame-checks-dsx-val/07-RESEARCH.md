# Phase 7: Validity frame checks (`DSX-VAL-*`) - Research

**Researched:** 2026-08-12
**Domain:** A Python gate-check module (`dsx/frame/val.py`) that reads a YAML analysis
contract and blocks or warns on nine kinds of invalid study design, using only
declarations already present in the spec — no statistics are computed.
**Confidence:** HIGH

## Summary (read this first)

1. `dsx/frame/val.py` should copy `dsx/frame/paradigm.py`'s shape exactly, but import
   `Report`/`Finding` from `dsx.findings`, not `dsx.checks` — `07-CONTEXT.md` names the wrong
   source module for that import, and the actual boundary test would fail if you imported
   from `dsx.checks`.
2. I read all six fixtures against the nine planned trigger rules and built the check-by-check
   table below. Two things `07-CONTEXT.md` predicted are confirmed exactly (the interference
   fixture's `DSX-VAL-020` trip, the bayesian fixture's `DSX-VAL-041` trip). One thing is new:
   `mechanism: not_assessed` + `method_implied: complete_case` appears in **all three** existing
   known-bad fixtures, so `DSX-VAL-060`'s design must not fire on that pairing or three fixtures
   need new allow-list entries nobody has flagged yet.
3. **A real test conflict, not yet named anywhere in the plan inputs:** the new
   `weak-identification-mmm` fixture (D-15) is required by `ROADMAP.md:212-213` to **block**
   `dsx gate plan`, but the existing `test_every_spec_passes_the_critical_threshold_gate_points`
   asserts **every** fixture found by globbing `examples/known-bad/*-ANALYSIS-SPEC.yaml` clears
   `plan` and `execute`. Placing the new fixture in that directory breaks that test as written.
   The planner must resolve this explicitly — see the dedicated section below.
4. D-05's docstring/test-marker enforcement is per-function, not per-module: whichever Python
   function's body contains a given `report.add("DSX-VAL-0NN", ...)` call is the function whose
   docstring is checked for `Citation:`/`Reference value:`/`Structural criterion:` lines. If
   `val.py` is split into nine helper functions (near-certain, given nine unrelated checks),
   **each helper needs its own citation block**, not one shared block on `check()`.
5. The `_NOT_SHIPPED` edit in `dsx/frame/paradigm.py` and the first `report.add("DSX-VAL-...")`
   call anywhere in the codebase are atomic — they must land in the same commit, not adjacent
   waves, or an existing invariant test fails in one direction or the other. Full mechanics below.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Locked upstream — do NOT re-litigate**

- `brief.md` §4 (D-01…D-14) and §5 (contract shape) are binding. In particular: D-01 stdlib only
  on the gate path; D-02 no statistic computed on the gate path; D-03a `dsx/frame/` imports only
  `Report`/`Finding` from `dsx/checks/`; D-05 citation + reference value + linked test per check;
  D-06 finding codes are never renumbered; **D-11 no frame-layer check reads `inference.paradigm`**.
- `PROJECT.md` Key Decisions M-01…M-09 are binding. M-09 in particular: `method_family_required`
  reuses `VARIANCE_ADJUSTMENTS` and defines no parallel vocabulary.
- `06-CONTEXT.md` D-01…D-23 are locked. Load-bearing here: severity **is** the gate point
  (CRITICAL blocks from plan, HIGH blocks at verify/ship only — `dsx/cli.py:105-110`); findings
  carry `detail`/`remedy`/`where` and actionability predicts fix rate; check for name collisions
  before coining a term; D-05 enforcement is mechanical via `scripts/gen-finding-catalogue.py`
  and `dsx/frame/*` is **not** on its exemption allow-list.
- D-08: `examples/good-ANALYSIS-SPEC.yaml` must keep passing every gate at every threshold and
  `examples/bad-ANALYSIS-SPEC.yaml` must keep being blocked by every gate; both are **extended,
  not replaced**, and the two existing exit-code tests stay unchanged.

> **Research correction to the paragraph above:** `Report` and `Finding` do not live in
> `dsx/checks/` at all — they live in `dsx/findings.py`, a sibling top-level module. See
> "1. The exact shape of a `dsx/frame/*` module" below for the verified import line and why
> importing from `dsx.checks` would actually trip the D-03a boundary scanner.

**Module layout, registration and code numbering**

- **D-01: One module, `dsx/frame/val.py`, with a single `check(spec) -> Report` entry point**,
  mirroring `dsx/frame/paradigm.py:60`. Registered as `CHECKS["val"]` in `dsx/cli.py` and added
  to the `plan`, `verify` and `ship` gate profiles — **not `execute`**. `execute` is scoped to
  environment/leakage/data-quality/code concerns and does not carry `design` either; a frame
  check there would be adjudicating a pre-data declaration at a post-data gate point.

- **D-02: Codes are assigned one decade per concept, with gaps.** *(User decision.)*

  | Code | Concept | Trigger |
  |---|---|---|
  | `DSX-VAL-010` | Estimand completeness | a required estimand sub-field is blank |
  | `DSX-VAL-011` | Estimand falsifiability | falsifier present but non-discriminating |
  | `DSX-VAL-020` | Unit triad | `units.observation` finer than `units.assignment` with no method family (**fixed by REQ-P7-02**) |
  | `DSX-VAL-021` | Unit drift | `validity_frame.units` disagrees with `design.*` unit fields |
  | `DSX-VAL-030` | Dependence | structure declared, no admissible method family |
  | `DSX-VAL-040` | Weak identification | `strength: weak` with `constraint_source: none` (**fixed by REQ-P7-05**) |
  | `DSX-VAL-041` | Strong identification carrying a constraint | `strength: strong` with a parameter-scale-informative constraint (**fixed by REQ-P7-05**) |
  | `DSX-VAL-050` | Sampling frame | frame cannot be judged against the claim population |
  | `DSX-VAL-060` | Missingness | mechanism incompatible with implied method |
  | `DSX-VAL-070` | Measurement | construct declared with no operationalisation |

  Rejected: `DSX-VAL-001` (which `research/ARCHITECTURE.md:219-227` proposed for estimand).
  In this catalogue's own convention `-001` denotes structural absence of a whole block
  (`DSX-SPEC-001`, `DSX-NAR-001`), which is Phase 6's `DSX-SPEC-080/081` territory. Also rejected:
  strictly sequential `001`–`009`, which leaves Phase 11's VAL-adjacent codes nowhere coherent to
  land. **D-06 makes this irreversible — assign exactly as tabled.**

- **D-03: Severity.** CRITICAL on `010`, `020`, `030` and `040` — each is the absence of something
  structurally required, and the project's core value is that these block *before the data is
  touched*. HIGH on `011`, `021`, `041`, `050`, `060` and `070`. `041` at HIGH is mandated
  verbatim by `ROADMAP.md:214-216` ("printed but non-blocking at plan, blocking at verify/ship").
  Note `research/PITFALLS.md:223-227` sets ~30% CRITICAL as an interrogation threshold and this
  set is 40%; the four are defended individually above rather than trimmed to hit a ratio.

**Dependence: `method_family_required` shape (Open Item 1, now resolved)**

- **D-04: The field stays single-valued and atomic against `VARIANCE_ADJUSTMENTS`
  (`dsx/spec.py:96`). The structure→admissible-methods map lives in `dsx/spec.py` as a module
  constant beside the vocabulary it references, excluded from `_VOCABULARIES` exactly as
  `CAUSAL_VERBS` (`dsx/spec.py:53`) already is.** *(User decision.)*

  The brief's `cluster_robust_or_mixed` is a mini-language, not a vocabulary member, and it fails
  the naming rule `06-CONTEXT.md:337-341` records: an operator reads a `dsx vocab` dump under time
  pressure. The map from `research/ARCHITECTURE.md:298-324`: `clustered` is satisfied by
  `{cluster_robust, bootstrap_cluster, mixed_effects}`; `repeated_measures` by
  `{mixed_effects, cluster_robust}`. The planner completes the remaining structures
  (`temporal`, `spatial`, `hierarchical`) and cites each.

  **Why `dsx/spec.py` and not `dsx/frame/val.py`:** Phase 11 keys `references/families.yaml` on
  this same taxonomy (`ROADMAP.md:195-196`). Homing the map in shared infrastructure lets Phase 11
  import it without depending on a check module or restating it as a second source of truth.

  Rejected: a list-valued field. `dsx/spec.py:816-835` calls `normalize(value)` on a scalar, so a
  list would stringify to `"['cluster_robust', 'mixed_effects']"` and trip `DSX-SPEC-082` — meaning
  edits to shipped Phase 6 code, the template, all four fixtures and the round-trip tests.

**Making free-text fields decidable under D-01 and D-02**

- **D-05: `estimand.falsifier` is adjudicated by a word-list test.** *(User decision.)*
  Two parts: (1) blank, a `<...>`-shaped placeholder, or a member of a refusal list
  (`n/a`, `tbd`, `none`, `unknown`) → `DSX-VAL-011`; (2) present but containing **no** token from a
  closed discriminating-predicate lexicon (`includes zero`, `crosses`, `below`, `above`, `exceeds`,
  `fails to`, `<`, `>`) **and** no numeric/`pp`/`%` token → `DSX-VAL-011`.

  The lexicon lives in `dsx/spec.py` beside `CAUSAL_VERBS`, because D-03a forbids `dsx/frame/`
  importing the existing lexicon precedents in `dsx/checks/narrative.py:17-21` and
  `dsx/checks/claims.py:107-113`.

  **Verified against the committed corpus:** all four non-blank falsifiers pass
  (`examples/good-ANALYSIS-SPEC.yaml:302`, `examples/known-bad/*:110/111/123` — each contains
  "includes zero"/"crosses" plus a numeric token); the blank one at
  `examples/bad-ANALYSIS-SPEC.yaml:211` and the placeholder at `templates/ANALYSIS-SPEC.yaml:288`
  both fail.

  **Known risk, accepted:** a false positive lands at the earliest, highest-friction gate on an
  honestly worded falsifier. The lexicon is designed to be loosened the first time that happens.
  Rejected: a blank-and-placeholder-only rule (makes REQ-P7-01's second clause decorative) and a
  structured `metric`/`operator`/`threshold` falsifier (reopens the Phase 6 contract that shipped
  as a breaking release ten days ago).

- **D-06: `DSX-VAL-050` (sampling frame) and `DSX-VAL-070` (measurement) adjudicate presence and
  internal consistency only — no text comparison between `source` and `claim_population`, and none
  between `measurement.construct` and the claim population.** Concretely: `claim_population` blank;
  or `selection_risk` blank/placeholder while `known_exclusions` is non-empty; or
  `operationalisation` blank while `construct` is declared.

  Forced by D-08: `examples/good-ANALYSIS-SPEC.yaml:339-342` declares
  `source: "warehouse.fct_signups, no region filter"` against
  `claim_population: "all new signups, 2026-06-01 to 2026-06-14"` with
  `selection_risk: "none identified"`. Any text-comparison rule strong enough to catch the brief's
  DACH-filter example (`brief.md:172-175`) would fail the good fixture, which must pass at every
  threshold. D-02 forbids anything heavier on the gate path.

  **Cronbach & Meehl (1955) makes D-06 the right answer for `070` rather than a compromise** — the
  necessary condition is that a construct "occur in a nomological net, at least *some* of whose
  laws involve observables". A presence test on `operationalisation` is exactly that condition.

- **D-07: `DSX-VAL-060` implements the missingness × method validity pairing as a lookup, with
  complete-case analysis under missing-at-random (MAR) data at HIGH, not CRITICAL.** Missing-not-at-
  random (MNAR) with no mechanism model stays CRITICAL. White & Carlin (2010) document a real
  sub-case where complete-case analysis is unbiased under MAR — when missingness is independent of
  the outcome given the covariates — so a CRITICAL here would produce false positives on
  legitimate specs.

  **Do not describe the rule as "the Rubin validity table".** Research confirmed no such printed
  table exists in Little & Rubin 3rd ed.; the pairing is assembled from §3.2's stated conditions
  plus White & Carlin. `REQUIREMENTS.md:102`'s phrase "the Rubin MCAR/MAR/MNAR validity table"
  describes the concept, not a citable artifact.

- **D-08: `DSX-VAL-020` decides "finer than" as string inequality** —
  `normalize(units.observation) != normalize(units.assignment)` — because
  `templates/ANALYSIS-SPEC.yaml:291` defines `observation` as "the finest-grained row in the source
  data", and `units.*` has no closed vocabulary in `_VALIDITY_FRAME_MEMBERSHIP`
  (`dsx/spec.py:719-728`), so `impression` vs `user` cannot be ordered without inventing an
  ordering that has no primary source to cite under D-05.

  **Known risk, accepted:** a spec naming the same unit two ways (`user` vs `user_id`) fires at
  CRITICAL on a naming inconsistency. If the planner judges this too sharp, the narrower trigger is
  `observation != assignment` **and** `dependence.structure` is `none`/absent **and**
  `method_family_required` is blank — at the cost of leaning entirely on `DSX-VAL-030` for the case
  where a structure is declared but the method family is not.

- **D-09: REQ-P7-03 disjointness is achieved by axis split, not by suppression logic.**
  `DSX-VAL-020` owns `observation` vs `assignment`. `DSX-EXP-021` (`dsx/checks/design.py:293-307`)
  keeps `analysis` vs `randomization` **unchanged**. `DSX-VAL-021` does pure string-equality drift
  detection across the two blocks. This resolves the wording tension between
  `REQUIREMENTS.md:97` ("analysis unit finer than the assignment unit") and `:98` /
  `ROADMAP.md:220` (`units.observation`) — the roadmap's success criterion is the binding one.

**The design-effect number — a correction to the plan**

- **D-10: The design effect (DEFF) reference value is 1.576, not 3.45.** Research established that
  `ICC = 0.05, m = 50 → 3.45` — the value `research/FEATURES.md:50-52` carries — **is not published
  anywhere**. The arithmetic is right but it is a computed illustration, and asserting it in a test
  is precisely the laundering D-05 exists to prevent.

  Use the Cochrane Handbook's worked value: intraclass correlation coefficient (ICC) 0.02, average
  cluster size 29.8, giving `1 + (29.8 - 1) × 0.02 = 1.576`. Formula and value appear in the same
  freely accessible, versioned subsection. (A second published value exists — UN handbook Ch. VI
  ¶72, ICC 0.05, cluster size 17 → 1.80 — if a second test case is wanted.)

- **D-11: `design_effect(m, icc)` ships as a pure function in `dsx/mathx.py`**, the established home
  for a reference-value-tested helper (`inflation_from_peeking()` is the precedent), and a peer
  module the D-03a boundary test permits (`tests/test_frame_boundary.py:35` denies only
  `dsx.checks`). It produces a **fixed illustrative constant** in the `DSX-VAL-020` finding text —
  **not a spec-derived number**. No `m` or `ICC` field exists anywhere in the contract
  (`brief.md:131-134`, `dsx/spec.py:712-728`), so the gate has no inputs to compute from, and D-02
  forbids it computing anyway.

**Fixtures, template and build plumbing**

- **D-12: `templates/ANALYSIS-SPEC.yaml` placeholder *values* are amended so `dsx init` output
  still clears `dsx gate plan`.** *(User decision.)* The `<...>` free-text placeholders stay; the
  values that would trip the new checks change — `identification.strength` to `strong`, consistent
  `units` placeholders, `missingness.mechanism` to `MCAR`, and one concrete example falsifier.
  Add a comment stating the values are examples to replace.

  Necessary because `dsx/cli.py:558-567` copies the template verbatim and
  `tests/test_dsx.py:1390-1393` asserts the copy passes `dsx gate plan`, while the template
  currently declares `strength: weak` with `constraint_source: none` (`:296-298`) — the literal
  `DSX-VAL-040` trigger — plus `mechanism: not_assessed` (`:331`), a placeholder falsifier (`:288`)
  and mismatched unit placeholders (`:291-292`). Phase 6 D-12 predicted this collision; it is
  resolved in favour of the new-user experience.

  **Check `tests/test_dsx.py:1239-1244`** (`test_template_validates_structurally_as_a_scaffold`,
  which asserts the template *fails* at ship) still proves what it claims after this edit.

- **D-13: `examples/good-ANALYSIS-SPEC.yaml:347` changes `method_implied` from `complete_case` to
  `multiple_imputation`.** The fixture declares `mechanism: MAR` with `rate: 0.0`, which
  `DSX-VAL-060` would flag. Multiple imputation is valid under MAR, so this is the honest fix.
  **Rejected: a "rate is zero" exemption in the check** — that makes `rate: 0` the cheapest way past
  the missingness check, the reflexive-`none` escape hatch `research/PITFALLS.md:643` warns about.

- **D-14: The known-bad corpus fixtures change; `tests/test_known_bad_corpus.py` does not.**
  `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml:113-126` declares
  `observation: impression`, `assignment: user`, `dependence.structure: none`,
  `method_family_required: ""` — the literal `DSX-VAL-020` trigger — and all three corpus fixtures
  declare `mechanism: not_assessed` with `method_implied: complete_case`. The corpus's stated
  guarantee (`tests/test_known_bad_corpus.py:41-45`) is that a fixture blocks **only** on its own
  encoded defect, so a shared-budget interference fixture blocking on pseudo-replication is a
  fixture bug. Fix by declaring `method_family_required: cluster_robust`.

  `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml:131-133`
  (`strength: strong`, `constraint_source: informative_priors`) will additionally trip
  `DSX-VAL-041` at HIGH — either edit the fixture or add an `_INCIDENTAL_GAP_CODES` entry, which is
  a deliberate call for the planner.

- **D-15: `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` is created in this
  phase.** `ROADMAP.md:212-213` names it by filename in Success Criterion 1. **Verified absent** —
  `examples/known-bad/` holds only the three Phase 6 fixtures. It needs a sourced post-mortem like
  its three siblings.

- **D-16: Three build-script edits ship in this phase or the family is invisible and uncited.**
  (a) Add `("DSX-VAL", "Validity frame", ...)` to `PREFIX_GROUPS`
  (`scripts/gen-finding-catalogue.py:26-44`) — `:179-181` silently drops any code whose prefix has
  no entry, with green CI. (b) Add `"DSX-VAL-"` to `_D05_ALLOWLIST_PREFIXES` (`:59`) — it is an
  *include* list (`:251-254`), so omitting it means D-05 enforcement never runs on the family this
  milestone most needs it for. (c) Remove `"DSX-VAL-"` from `_NOT_SHIPPED` in
  `dsx/frame/paradigm.py:50` — two invariant tests assert every `_NOT_SHIPPED` prefix resolves to
  no shipped code and will fail the moment `DSX-VAL-010` exists.

  Docstring regexes are exact and three-digit: `^\s*Citation:\s*\S`,
  `^\s*(?:Reference value|Structural criterion):\s*\S`, `#\s*D-05:\s*(DSX-[A-Z]+-\d{3})`
  (`scripts/gen-finding-catalogue.py:75-79`).

- **D-17: `brief.md` §7 (`brief.md:434-451`) is extended with the six new sources before Phase 7
  code lands**, and the two already listed get their editions pinned. §7 states "Anchor D-05
  citations here rather than sprawling", and threat T-6-07 requires it. Missing: ICH E9(R1),
  Kish (1965), the Cochrane Handbook, Hernán & Robins (2016), Popper, Cronbach & Meehl.
  Unpinned: Lohr and Little & Rubin — section numbers differ across editions.

**The D-05 citation ledger — use these verbatim**

Researched against primary documents 2026-08-10. Each is written to drop into the existing
`dsx/spec.py:738-753` docstring shape unchanged.

| Code | Citation | Evidence line |
|---|---|---|
| `010` | ICH (2019), E9(R1) Addendum, EMA/CHMP/ICH/436221/2017, Step 5, §A.3.3 ("Estimand attributes") and §A.3.2; Hernán & Robins (2016), *Am J Epidemiol* 183(8):758-764, Table 1; Hernán & Robins (2020), *Causal Inference: What If*, Ch. 1 §1.2 ("Average causal effects") | `Structural criterion:` presence of five named sub-fields |
| `011` | Popper (1959/2002), *The Logic of Scientific Discovery*, Part I, Ch. 1, §6 ("Falsifiability as a Criterion of Demarcation"), pp. 17-18 | `Structural criterion:` falsifier must name ≥1 observable outcome under which the claim is withdrawn |
| `020` | Kish (1965), *Survey Sampling*, §8.2 p. 258 (Deff definition) and pp. 161-162 (ICC); Higgins, Eldridge & Li (2024), *Cochrane Handbook* v6.5, §23.1.4 and §23.1.4.1 | `Reference value:` ICC 0.02, M 29.8 → `1 + (29.8-1)*0.02 = 1.576` |
| `030` | *Planner assigns per dependence structure* — cite the source for each structure→method pairing | `Structural criterion:` membership of declared method in the admissible set |
| `040`/`041` | Gelman, Simpson & Betancourt (2017), *Entropy* 19(10), 555, §3.3 ("For complex models, certain aspects of the prior will always be relevant") and §1.2 ("Existing methods for setting priors already depend on the likelihood") | `Structural criterion:` membership test against a **project-defined** partition |
| `050` | Lohr (2021), *Sampling: Design and Analysis*, **3rd ed.**, Ch. 1 §1.2, §1.3, §1.3.4 ("Undercoverage"); Ch. 16 §16.1 ("Coverage Error") | `Structural criterion:` presence and internal consistency |
| `060` | Little & Rubin (2019), *Statistical Analysis with Missing Data*, 3rd ed., Ch. 3 ("Complete-Case and Available-Case Analysis, Including Weighting Methods") §3.2; White & Carlin (2010), *Stat Med* 29(28):2920-2931, DOI 10.1002/sim.3944 | `Structural criterion:` (mechanism, method) pairing membership |
| `070` | Cronbach & Meehl (1955), "Construct Validity in Psychological Tests", *Psychological Bulletin* 52(4):281-302, "The Logic of Construct Validation" → "The Nomological Net", principle 3, p. 290 | `Structural criterion:` a construct with no operationalisation naming an observable is rejected |

**Two honesty disclosures the docstrings must carry — these are D-05's whole point:**

1. **`040`/`041`: no published source partitions `CONSTRAINT_SOURCES` into
   carries/does-not-carry parameter-scale information.** Gelman, Simpson & Betancourt supports the
   *premise* (§3.3) and gives a prior taxonomy (§1.2: structural priors → `hierarchical_pooling`;
   regularizing priors → `penalisation`), but publishes no such partition, and `design_restriction`
   has no counterpart in it at all. The docstring must say the partition is project-defined.
2. **The five-field estimand decomposition is project-defined.** ICH E9(R1) and Hernán & Robins
   (2016) each cover four of the five; `falsifier` appears in neither, and no source treats a
   falsifier as an estimand attribute. `time_window` is an ICH sub-specification, not an attribute.

**Two locators that are UNVERIFIED — flag, do not invent** (Phase 6 set this precedent at
`dsx/frame/paradigm.py:66-72`): a *section* number in Kish for the DEFF formula itself (page
numbers only were confirmed), and whether the typeset MDPI version of Gelman, Simpson & Betancourt
uses the same section numbers as the arXiv final version — cite by number **and** title so the
locator survives either. Do not cite Mayo (2018) with a section number; only its Tour structure
was confirmable.

### Claude's Discretion

The planner and researcher may settle these without returning to discuss:

- **Plan slicing across the 9 requirements.** No internal ordering constraints
  (`ROADMAP.md:201-203`), so waves are free apart from build plumbing (D-16) landing before or
  with the first check.
- **The remaining structure→method pairings** for `temporal`, `spatial` and `hierarchical` in
  D-04's map, and their citations.
- **The exact discriminating-predicate lexicon membership** in D-05, beyond the tokens named.
- **Which published weak-identification case** the D-15 marketing-mix-model fixture encodes.
  Vendor blogs and Medium posts are inadmissible in either direction.
- **Whether the `DSX-VAL-041` collision on the Bayesian corpus fixture** is resolved by editing the
  fixture or by an `_INCIDENTAL_GAP_CODES` entry (D-14).
- **Whether `DSX-VAL-020` uses the narrower three-condition trigger** named in D-08 if the plain
  string inequality proves too sharp against the fixtures.

### Deferred Ideas (OUT OF SCOPE)

- **Text-level comparison of sampling frame against claim population** (catching the brief's
  DACH-filter example mechanically). D-06 defers it because no rule strong enough to catch it
  passes the good fixture under D-08. Revisit when the Phase 12 calibration corpus can measure the
  false-positive rate — that is the entry condition, per D-13's "a trigger tied to a measured catch
  rate is falsifiable".
- **A `UNIT_GRANULARITY` ordered vocabulary** (impression < session < user/account < geo) making
  "finer than" literal rather than string inequality. Rejected for this phase: it forces every
  fixture's unit strings into a closed set and the ordering has no primary source to cite under
  D-05.
- **A structured `metric`/`operator`/`threshold` falsifier.** Fully decidable and directly reusable
  by Phase 10's fallback-rule mini-language. Deferred because it reopens the Phase 6 contract that
  shipped ten days ago as a breaking release. Natural entry point: a future major version, or
  Phase 10 if its DSL work makes the case overwhelming.
- **Retroactive D-05 sourcing for the 206 legacy finding codes.** Carried from Phase 6, unchanged.

Folded todos: none — `todo.match-phase 7` returned zero matches. Reviewed todos not folded: none.

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-P7-01 | An estimand missing any of `quantity`, `population`, `contrast`, `time_window` or `falsifier` is blocked, and a falsifier that cannot discriminate any outcome is blocked | Section 1 (module shape) + Section 4 (verified: `falsifier` routes through the word-list test to `DSX-VAL-011`, the other four route through a plain blank check to `DSX-VAL-010` — these are two different code paths, see the note under "Section 4" heading) |
| REQ-P7-02 | An analysis unit finer than the assignment unit is blocked, with the design-effect consequence quantified via `DEFF = 1 + (m-1)·ICC` and a test asserting the published worked value | Section 5 (EXP-020/021 boundary, confirms structural field disjointness) + Section 7 (`mathx.py` conventions, `design_effect()` placement) |
| REQ-P7-03 | `DSX-VAL-020` and `DSX-EXP-021` do not both fire on the same defect; EXP-021 unchanged | Section 5 — **verified from the actual code, not just the plan**: `DSX-EXP-021` reads `design.randomization_unit`/`design.analysis_unit`/`design.variance_adjustment`; `DSX-VAL-020` reads `validity_frame.units.observation`/`.assignment`/`dependence.method_family_required`. Disjointness is structural (different spec paths), not just conventional. |
| REQ-P7-04 | A declared dependence structure without a matching method family is blocked, using `VARIANCE_ADJUSTMENTS` | Section 8a (structure→method map recommendations for `temporal`/`spatial`/`hierarchical`) |
| REQ-P7-05 | `DSX-VAL-040`/`DSX-VAL-041` both cite Gelman, Simpson & Betancourt (2017) | Section 8b (recommended `CONSTRAINT_SOURCES` partition) |
| REQ-P7-06 | A sampling frame that cannot represent the claim population is blocked | Section 4 (fixture matrix verifies D-06's presence-only rule against the actual `is_blank()` helper) |
| REQ-P7-07 | A missingness mechanism inconsistent with the implied method is blocked | Section 8c (verified: all three existing known-bad fixtures use `not_assessed`+`complete_case` — a real constraint on the lookup table's design) |
| REQ-P7-08 | A measurement construct with no operationalisation is blocked | Section 4 (verified template/fixture behaviour) |
| REQ-P7-09 | No `DSX-VAL-*` check reads `inference.paradigm`, asserted by test | Section 6 (test-suite conventions — the existing AST boundary scanner cannot directly serve this; a new, narrower test is needed) |

</phase_requirements>

## Architectural Responsibility Map

This phase has one tier: a deterministic, stdlib-only Python library that reads an in-memory
dict (the parsed YAML spec) and returns a `Report` of findings. There is no browser, server,
CDN or database tier — `dsx` is a CLI/library invoked by GSD's gate machinery, not a web app.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Estimand/unit/dependence/identification/sampling/missingness/measurement adjudication | Gate-check library (`dsx/frame/val.py`) | — | Pure function over an in-memory dict; no I/O, no network, no persistence (D-01, D-02) |
| Shared vocabulary and structure→method mapping | Contract module (`dsx/spec.py`) | Gate-check library | Shared infrastructure Phase 11 also needs (D-04); `dsx/frame/*` imports it, never the reverse |
| Numeric reference-value helpers (`design_effect`) | Math kernel (`dsx/mathx.py`) | Gate-check library | Peer module to `dsx/frame/`, not owned by it — same pattern as `inflation_from_peeking()` |
| CLI registration and gate-profile membership | CLI entry point (`dsx/cli.py`) | — | Wires the check into `plan`/`verify`/`ship`; no logic of its own |
| Decision-trail emission | Decision-record schema (`dsx/decisions.py`) | Gate-check library | `val.py` constructs `DecisionRecord`s but the schema/writer live centrally |

## 1. The exact shape of a `dsx/frame/*` module

Read in full: `dsx/frame/paradigm.py` (163 lines).

**Signature and Report construction** (`dsx/frame/paradigm.py:60,78`):
```python
def check(spec: dict) -> Report:
    ...
    report = Report(check="paradigm")
```
`val.py` should mirror this exactly: `def check(spec: dict) -> Report: report = Report(check="val")`.

**Imports** (`dsx/frame/paradigm.py:18-20`):
```python
from ..decisions import DecisionRecord
from ..findings import Report
from ..spec import PARADIGMS, get, is_blank, normalize
```

**Correction to `07-CONTEXT.md`'s D-03a summary:** the text says `dsx/frame/*` "may import only
`Report` and `Finding` from `dsx/checks/`". I read `dsx/findings.py` (228 lines) and
`dsx/checks/__init__.py` (52 lines) directly: `Finding` and `Report` are both defined in
`dsx/findings.py` (`dsx/findings.py:52` `class Finding`, `:91` `class Report`).
`dsx/checks/__init__.py` re-exports only the fourteen check *modules* (`claims`, `code`,
`coherence`, ... `viz`) — it does not re-export `Report` or `Finding` at all, and there is no
other path by which either name is reachable through `dsx.checks`. The actual boundary
enforcement (`tests/test_frame_boundary.py:35,71`) flags **any** import of `dsx.checks` or a
submodule of it, with no exception for specific names — so `from ..checks import Report` would
both (a) raise `ImportError` because `Report` isn't there, and (b) if it somehow were, trip the
AST scanner. The correct, verified import for `val.py` is exactly `paradigm.py`'s:
`from ..findings import Report` (add `Finding` too only if a type hint needs it directly).

**`report.add(...)` call shape** (`dsx/frame/paradigm.py:117-126`):
```python
report.add(
    "DSX-PAR-001",
    "INFO",
    f"paradigm manifest — inference.paradigm: {paradigm or 'undeclared'}",
    detail=detail,
    remedy=remedy,
    where="spec.inference.paradigm",
    applied=applied,
    not_applied=not_applied,
)
```
`Report.add`'s real signature (`dsx/findings.py:101-109`) is
`add(code, severity, title, detail="", remedy="", where="", **data)` — first three positional
args must be literal strings (or an f-string whose static parts the AST extractor can read; see
Section 3), and any additional keyword arguments land in `Finding.data`, not in the rendered
text. `paradigm.py` uses this for `applied`/`not_applied` so its own tests can assert against
`finding.data.get("applied", [])` (`tests/test_dsx.py:2596`) — `val.py`'s checks can do the same
for anything a later phase might want to introspect (e.g. which specific vocabulary members
mismatched).

**Docstring layout that satisfies `gen-finding-catalogue.py --check`** (mirrors
`dsx/frame/paradigm.py:61-77`): the function docstring needs a `Citation:` line and either a
`Reference value:` or `Structural criterion:` line, each matching the three-digit-code regexes
in Section 3 verbatim. `paradigm.py`'s docstring is one continuous prose block with those two
labelled lines embedded — not a separate `Args:`/`Returns:` docstring style.

**`DecisionRecord` emission pattern** (`dsx/frame/paradigm.py:146-161`):
```python
report.context.setdefault("decisions", []).append(
    DecisionRecord(
        id="",
        invocation_id="",
        layer="deterministic",
        choice=choice,
        inputs=["inference.paradigm"],
        rule=(...),
        citation="...",
        counterfactual=counterfactual,
    ).to_dict()
)
```
`id` and `invocation_id` are always emitted as empty strings by the check itself — the CLI layer
(`dsx/cli.py::_write_decision_trail`, lines 300-316) fills both in when it flattens
`report.context` via `collect_from_report()` and writes to `DECISIONS.jsonl`. `val.py` should
follow this exactly for each of its nine judgment points (or fewer, if some codes share one
judgment — e.g. `040`/`041` are two outcomes of one `identification` evaluation and could share
one `DecisionRecord`).

**A subtlety not visible from `paradigm.py` alone, verified by reading `dsx/spec.py:731-786`
and `:868-914`:** `dsx/spec.py`'s own validity-frame/inference validators emit `DecisionRecord`s
too, using a **deferred, function-local** import (`from .decisions import DecisionRecord` inside
the function body, not at module top) to avoid a circular import at module load time — `spec.py`
is imported by nearly everything, including `decisions.py` indirectly. `paradigm.py` imports it
at module top instead (line 18), which works because `dsx/frame/` sits below `dsx/spec.py` and
`dsx/decisions.py` in the dependency graph, not above them. `val.py` is in the same position as
`paradigm.py` (a leaf consumer of `spec.py`/`decisions.py`), so the top-level import form is
safe and is the pattern to copy — no need for the deferred-import workaround `spec.py` itself
needs.

## 2. Registration mechanics

Read in full: `dsx/cli.py` (773 lines).

**`CHECKS` dict** (`dsx/cli.py:63-79`):
```python
CHECKS: dict[str, Callable] = {
    "spec": validate_structure,
    "design": design.check,
    ...
    "decision": decision.check,
    "paradigm": paradigm.check,
}
```
Add `"val": val.check,` as a new entry. This requires extending the existing import
(`dsx/cli.py:50`) from `from .frame import paradigm` to `from .frame import paradigm, val`.

**`GATE_PROFILES` dict** (`dsx/cli.py:88-101`):
```python
GATE_PROFILES: dict[str, tuple[str, ...]] = {
    "plan": ("spec", "design", "metrics", "coherence", "paradigm"),
    "execute": ("spec", "ml", "repro", "dq", "code", "paradigm"),
    "verify": (
        "spec", "design", "stats", "ml", "metrics", "claims", "viz", "repro",
        "dq", "coherence", "smells", "figures", "narrative", "code", "decision",
        "paradigm",
    ),
    "ship": (
        "spec", "design", "stats", "ml", "metrics", "claims", "viz", "repro",
        "dq", "coherence", "smells", "figures", "narrative", "code", "decision",
        "paradigm",
    ),
}
```
Add `"val"` to the `plan`, `verify` and `ship` tuples — **not** `execute`, per D-01. There is no
ordering requirement within a tuple (the code just does `for name in names`), so appending at
the end (next to `"paradigm"`, matching how `paradigm` itself was added in Phase 6) is
consistent with the existing style.

**`GATE_THRESHOLDS`** (`dsx/cli.py:105-110`) needs **no change** — `plan`/`execute` block at
CRITICAL, `verify`/`ship` block at HIGH, which already matches D-03's intended severity split
exactly (CRITICAL codes block from plan; HIGH codes only from verify/ship).

**Dispatch mechanics** (`dsx/cli.py::run_checks`, lines 135-182): most checks need special-case
branches in this function because their `check()` signature carries extra parameters (`root`,
`strict`, `gate_point`, `phase_dir`). `val.check(spec)` takes only `spec`, exactly like
`paradigm.check(spec)` — and `"paradigm"` has **no** special case in `run_checks`; it falls
through to the generic branch at `dsx/cli.py:174-175`:
```python
elif name in CHECKS:
    reports.append(CHECKS[name](spec))
```
So `val` needs **zero** changes to `run_checks()` beyond the `CHECKS` dict entry itself — this
is the one piece of registration mechanics that is *not* boilerplate to write.

**Help text** (`dsx/cli.py:667`) — `p_check.add_argument("checks", ..., help="subset to run: " +
", ".join(sorted(CHECKS)) + ", repro")` — derives its list from `CHECKS` at parser-build time,
so it picks up `"val"` automatically; no separate edit needed.

## 3. The D-05 build check's exact contract

Read in full: `scripts/gen-finding-catalogue.py` (316 lines).

**The three regexes** (`scripts/gen-finding-catalogue.py:70-74`):
```python
_CITATION_RE = re.compile(r"^\s*Citation:\s*\S", re.MULTILINE)
_REFVALUE_RE = re.compile(
    r"^\s*(?:Reference value|Structural criterion):\s*\S", re.MULTILINE
)
_TEST_MARKER_RE = re.compile(r"#\s*D-05:\s*(DSX-[A-Z]+-\d{3})")
```
`_CITATION_RE`/`_REFVALUE_RE` match a docstring line (any leading whitespace, `re.MULTILINE` so
`^`/`$` are per-line — this repo checks out CRLF on Windows per `.claude/CLAUDE.md`; Python's
`re.MULTILINE` treats `\r\n` correctly here because `^` matches after `\n`, and the regex has no
`$` anchor at all, so CRLF is not a hazard for this particular pattern). `_TEST_MARKER_RE`
requires the code to be **exactly three digits** — `DSX-VAL-10` or `DSX-VAL-1` would not match;
all nine D-02 codes (`010`...`070`) are already three digits, so this is a non-issue as tabled,
but worth stating explicitly since a typo here fails silently (the marker just wouldn't count).

**`PREFIX_GROUPS`** (`scripts/gen-finding-catalogue.py:25-45`) is a `list[tuple[str, str, str]]`
of `(prefix, heading, blurb)`, e.g.:
```python
("DSX-PAR", "Paradigm and monitoring discipline",
 "The declared inferential paradigm manifest and its symmetric peeking-monitoring pair."),
```
A `DSX-VAL` entry needs the same three-tuple shape, e.g.
`("DSX-VAL", "Validity frame", "Estimand, unit, dependence, identification, sampling, missingness and measurement adjudication.")`.
**If this entry is missing, `render()` (`:180-189`) silently drops every `DSX-VAL-*` row from
`references/finding-codes.md` with a green CI run** — the `--check` mode only diffs rendered
text against the checked-in file, and a code that renders as "dropped, consistently, on both
sides of the diff" produces no diff. This is the failure mode D-16(a) exists to prevent, and it
is a genuinely silent one — worth flagging with more force than the CONTEXT.md prose does,
because there is no test anywhere that asserts "every code in `collect()` appears in some
`PREFIX_GROUPS` entry" — I searched and found none.

**`_D05_ALLOWLIST_PREFIXES`** (`scripts/gen-finding-catalogue.py:58`) — **verified: this is an
include-list, not an exclude-list**, confirmed by reading `check_d05()` directly
(`:250-280`):
```python
covered = [
    row for row in rows
    if row[0].startswith(_D05_ALLOWLIST_PREFIXES) or row[0] in _D05_ALLOWLIST_CODES
]
if not covered:
    return []
```
Only codes matching this tuple (or the individually-named `_D05_ALLOWLIST_CODES`) are ever
checked for a citation, reference value or test marker. Every other one of the 206 pre-existing
legacy codes is silently exempt. **Omitting `"DSX-VAL-"` from this tuple means the nine new
checks can ship with zero citations and zero tests and `--check` will still report success** —
this is the mechanism D-16(b) refers to, and I confirm it reads exactly as CONTEXT.md states.

**How the script walks from a `report.add(...)` call site up to a docstring**
(`_resolve_docstrings()`, `scripts/gen-finding-catalogue.py:193-232`): it builds a full
child→parent AST map for a file, then for each `report.add(...)` call whose first argument is a
`DSX-`-prefixed string literal, walks upward through parents until it hits the nearest enclosing
`FunctionDef`/`AsyncFunctionDef` and takes **that function's own docstring**, falling back to
the *module* docstring only if no enclosing function exists at all.

**This is the single most consequential mechanical detail for planning `val.py`'s internal
structure.** `paradigm.py` has exactly one function (`check`), so its one docstring trivially
covers its one `report.add` call. `val.py` has nine independent, unrelated judgment points; if
they are implemented as nine private helper functions (`_check_estimand`, `_check_units`,
`_check_dependence`, ...) called from `check()` — the natural decomposition, and the one
`dsx/checks/design.py` itself uses for `_check_units`/`_check_duration`/etc. — then **each
helper function needs its own `Citation:`/`Reference value:` (or `Structural criterion:`)
docstring**, because the extractor takes the *immediately enclosing* function's docstring, not
`check()`'s. A single shared citation block on `check()`'s docstring would only satisfy D-05 for
whichever `report.add(...)` calls are *textually inside* `check()` itself (unlikely to be more
than a dispatcher). The planner should design each helper's docstring from the start, not treat
docstrings as an afterthought pass.

**Test markers** (`_collect_test_markers()`, `:235-247`): a raw-text regex scan (not AST) over
every file under `tests/`, collecting the code named by every `# D-05: <CODE>` comment anywhere
in the tree. Location within a test file doesn't matter — it's a flat text scan — but the
existing convention (verified against `tests/test_dsx.py:391,415,460,514,531,1456,2584`) places
the comment either as a standalone line immediately above the `def test_...` it documents, or
inline on the same line as an assertion inside the test body.

**Minimum a new check must do to pass `gen-finding-catalogue.py --check`:**
1. Add a `("DSX-VAL", ...)` entry to `PREFIX_GROUPS`.
2. Add `"DSX-VAL-"` to `_D05_ALLOWLIST_PREFIXES`.
3. Give the function that contains each `report.add("DSX-VAL-0NN", ...)` call its own docstring
   with a `Citation:` line and a `Reference value:`/`Structural criterion:` line.
4. Place a `# D-05: DSX-VAL-0NN` comment somewhere under `tests/` for each of the nine codes.
5. Run `python3 scripts/gen-finding-catalogue.py --write` and commit the regenerated
   `references/finding-codes.md` (`--check` will otherwise report the catalogue as stale).

## 4. Fixture × check matrix

I read the `validity_frame:` block of all six spec fixtures directly and traced each of the
nine planned trigger rules against the actual field values (not against CONTEXT.md's summary of
them). "✗ (no data)" means the relevant sub-block is entirely absent — under the Phase Boundary
note in `07-CONTEXT.md`, a `DSX-VAL-*` check must **not** fire in that case (Phase 6's
`DSX-SPEC-081` already owns "sub-block absent"), so these cells are correctly "would not fire"
by design, not an oversight.

| Fixture | `010` completeness | `011` falsifiability | `020` unit triad | `021` unit drift | `030` dependence | `040` weak-ID | `041` strong-ID+constraint | `050` sampling | `060` missingness | `070` measurement |
|---|---|---|---|---|---|---|---|---|---|---|
| `good-ANALYSIS-SPEC.yaml` | no fire (all 4 present) | no fire (`"includes zero"` + `+1.0pp`) | **no fire** (`session`≠`user` but `method_family_required: cluster_robust` present) | no fire (units match `design.*`) | no fire (`clustered` + `cluster_robust` ∈ admissible set) | no fire (`strength: strong`) | no fire (`constraint_source: none`) | no fire (`claim_population` present, `selection_risk` non-blank) | **would fire HIGH today** — `mechanism: MAR` + `method_implied: complete_case` (line 347) is the literal HIGH trigger under D-07; **D-13's edit to `multiple_imputation` has not yet been applied to the file I read** | no fire (`construct`+`operationalisation` present) |
| `bad-ANALYSIS-SPEC.yaml` | no fire (4 fields present) | **fires** — `falsifier: ""` (line 211) | no fire (`account`==`account`, no mismatch) | no fire (no design.* mismatch beyond what EXP-021 already owns) | ✗ (no data — `dependence` block entirely absent) | ✗ (`strength: extremely_strong` is not a `IDENTIFICATION_STRENGTHS` member — matches neither `weak` nor `strong`; `DSX-SPEC-082` already flags the vocabulary violation) | ✗ (same reason) | ✗ (no data — block absent) | ✗ (no data — block absent) | ✗ (no data — block absent) |
| `templates/ANALYSIS-SPEC.yaml` (before D-12 edit) | no fire (all 4 present, as placeholders — `is_blank()` treats non-empty placeholder text as present) | **fires** — `falsifier: "<the observation that would prove this wrong>"` is a `<...>`-shaped placeholder | **fires CRITICAL today** — `observation`/`assignment` are two *different* placeholder strings (lines 291-292) and `method_family_required: null` | no fire (`dependence` absent from design.* comparison path; no design unit fields set at all in this file) | no fire — `structure: none` (line 302) is the "independent, nothing to validate" case, skip | **fires CRITICAL today** — `strength: weak` + `constraint_source: none` (lines 296, 298) | no fire (`constraint_source: none` — not a parameter-scale-informative member) | no fire — `claim_population` is a `<...>` placeholder, **not literally blank**; see note below | no fire — `mechanism: not_assessed` (line 331) is outside D-07's stated MAR/MNAR pairing | no fire — `construct`/`operationalisation` are placeholders, non-blank |
| `known-bad/interference-shared-budget-...yaml` | no fire | no fire (`"includes zero"` + `+0.5pp`) | **fires CRITICAL today** — `observation: impression` ≠ `assignment: user` (lines 113-114) **and** `method_family_required: ""` (line 126) — the exact defect D-14 names; needs the D-14 fix (`method_family_required: cluster_robust`) | no fire (units match `design.*`: `assignment: user`==`randomization_unit: user`) | no fire — `structure: none` (line 124), skip | no fire (`strength: strong`) | no fire (`constraint_source: none`) | no fire | no fire (`not_assessed`+`complete_case`, see Section 8c) | no fire |
| `known-bad/bayesian-continuous-monitoring-...yaml` | no fire | no fire | no fire (`session`==`session`==`session`) | no fire | no fire — `structure: none`, skip | no fire (`strength: strong`) | **fires HIGH today** — `strength: strong` + `constraint_source: informative_priors` (lines 131,133), matching D-14's prediction exactly | no fire | no fire (`not_assessed`+`complete_case`) | no fire |
| `known-bad/frequentist-uncontrolled-continuous-...yaml` | no fire | no fire | no fire (`session`==`session`==`session`) | no fire | no fire — `structure: none`, skip | no fire (`strength: strong`) | no fire (`constraint_source: none`) | no fire | no fire (`not_assessed`+`complete_case`) | no fire |

**Important disambiguation confirmed by reading D-05 and D-02 together, not obvious from either
alone:** `DSX-VAL-010`'s "a required estimand sub-field is blank" does **not** include
`falsifier` in practice — D-05's word-list rule explicitly routes a blank falsifier to
`DSX-VAL-011`, not `DSX-VAL-010`. So the correct implementation is: `DSX-VAL-010` checks
`quantity`/`population`/`contrast`/`time_window` (four fields, plain `is_blank()`), and
`DSX-VAL-011` owns `falsifier` entirely (blank, placeholder, refusal-word, or
non-discriminating) via the separate word-list test. A `bad-ANALYSIS-SPEC.yaml`-style spec with
a blank falsifier fires exactly one code (`DSX-VAL-011`), not two.

**`is_blank()` vs. placeholder detection — a load-bearing asymmetry to implement correctly:**
`dsx/spec.py:326-333`'s `is_blank()` (already imported everywhere) treats any non-empty string
as "present", including `"<a placeholder>"`. D-05's falsifier rule is the *only* one of the nine
checks that needs a dedicated placeholder-and-refusal-word detector layered on top of
`is_blank()` — I verified this against the template: `templates/ANALYSIS-SPEC.yaml`'s
`sampling_frame.claim_population` (line 326) and `measurement.construct`/`operationalisation`
(lines 336-337) are **all** still `<...>`-shaped placeholders in the current file, and D-12's
plan for editing the template does **not** touch any of them — only `identification.strength`,
`units.*`, `missingness.mechanism` and the falsifier get value edits. If `DSX-VAL-050`/`070`
treated placeholders as blank the same way `DSX-VAL-011` does, the template would still trip
those two checks and D-12's edit list would be incomplete — it isn't, which confirms `050`/`070`
must use plain `is_blank()` semantics (placeholder text counts as "present"), while `011` alone
needs the specialised detector. Implement these as two genuinely different helper functions in
`dsx/spec.py`, not one shared "looks blank" utility.

## 5. The `DSX-EXP-020/021` boundary

Read: `dsx/checks/design.py:250-339` (the `_check_srm`/`_check_units`/`_check_duration`
functions).

```python
def _check_units(design: dict, report: Report) -> None:
    randomization = normalize(design.get("randomization_unit", ""))
    analysis = normalize(design.get("analysis_unit", ""))
    if not randomization or not analysis:
        report.add("DSX-EXP-020", "HIGH", ...)                    # design.py:274
        return
    if randomization == analysis:
        report.ok(...)
        return
    adjustment = design.get("variance_adjustment")
    if is_blank(adjustment):
        report.add("DSX-EXP-021", "CRITICAL", ...)                # design.py:293-307
    else:
        report.ok(...)
```
(`dsx/checks/design.py:269-309`.)

**Verified, not just repeated from CONTEXT.md:** `DSX-EXP-020` fires when either
`design.randomization_unit` or `design.analysis_unit` is blank (HIGH). `DSX-EXP-021` fires when
both are present, differ (string inequality after `normalize()`), and
`design.variance_adjustment` is blank (CRITICAL). **These three field paths —
`design.randomization_unit`, `design.analysis_unit`, `design.variance_adjustment` — are entirely
different spec locations from what `DSX-VAL-020` reads: `validity_frame.units.observation`,
`validity_frame.units.assignment`, `validity_frame.dependence.method_family_required`.**
`_check_units()` never touches `validity_frame` at all — I read the whole function and confirmed
it. This means D-09's disjointness claim is **stronger** than "the plan currently keeps them
separate" — it is a structural property of the two checks reading disjoint fields, and no
`validity_frame` edit can ever cause `DSX-EXP-021` to fire, nor can any `design.*` edit ever
cause `DSX-VAL-020` to fire. `DSX-VAL-021` (unit drift) is the only one of the nine that
deliberately bridges the two blocks, and it does so with pure string-equality comparison, never
duplicating `DSX-EXP-021`'s judgment (it doesn't assess whether a mismatch is *handled* — that's
`DSX-EXP-021`'s job for the `design.*` pair — only whether the two blocks *agree* with each
other).

**Confirmed against the actual fixtures:** `bad-ANALYSIS-SPEC.yaml` has
`design.randomization_unit: account` / `design.analysis_unit: session` (mismatch, no
`variance_adjustment` — this is the file's `DSX-EXP-021` trigger) alongside
`validity_frame.units.observation: account` / `.assignment: account` (equal — no `DSX-VAL-020`
trigger). Both checks evaluate the same fixture and reach opposite conclusions on their own
fields, simultaneously, with no interaction — direct proof the split works as designed.

## 6. Test-suite conventions

Read: `tests/test_dsx.py` (selected sections), `tests/test_frame_boundary.py` (126 lines, in
full), `tests/test_known_bad_corpus.py` (331 lines, in full).

**Gate-level (CLI, exit-code) tests** use a small per-class helper repeated verbatim across
three different `TestCase` classes (`tests/test_dsx.py:1186-1190,1698-1702,2056-2060`):
```python
def _run(self, argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = cli.main(argv)
    return code, out.getvalue(), err.getvalue()
```
then e.g. `code, _, err = self._run(["gate", "plan", "--spec", str(fixture)])` and
`self.assertEqual(code, 0, f"...:\n{err}")`.

**Check-level (unit) tests** call the check function directly against a dict literal and
inspect `report.findings`, following the pattern at `tests/test_dsx.py:390-474` exactly
(`validate_structure(spec)` there; `val.check(spec)` for this phase) — asserting on
`f.code`/`f.severity`/`f.where`/`f.detail` membership, using the module-level helper
`codes(report) -> set[str]` (`tests/test_dsx.py:26-27`, `{f.code for f in report.findings}`).

**AST boundary scanner** (`tests/test_frame_boundary.py`, read in full): it only detects
`import`/`from ... import` statements resolving to `dsx.checks` or a submodule — it has no
mechanism at all for detecting an *attribute read* like `get(spec, "inference.paradigm")`.
**REQ-P7-09 cannot literally "extend the existing AST machinery"** the way `07-CONTEXT.md`
suggests, because the existing machinery is purpose-built for import statements, not string
literals or dotted-path reads. Verified from the codebase's own idiom
(`dsx/frame/paradigm.py:80`: `get(spec, "inference.paradigm")`) that the access pattern to guard
against is a string literal `"inference.paradigm"` passed as an argument, not an import. Two
approaches, in order of robustness:
1. **AST-based** (more precise, matches the project's stated "two proofs, not one" ethos at
   `tests/test_frame_boundary.py:11`): parse `dsx/frame/val.py`, walk every `ast.Call` node
   whose `func` resolves to `get` (or any function), and flag any call where a positional
   string-literal argument equals `"inference.paradigm"` or starts with `"inference."`.
2. **Text-level fallback** (simpler, and the project already has a precedent for staying
   text-level where AST is unnecessary — `scripts/gen-finding-catalogue.py:240-241`'s comment
   citing `dsx/suppressions.py::known_codes()`'s rationale): assert the literal substring
   `"inference.paradigm"` does not appear anywhere in `dsx/frame/val.py`'s source text.

I recommend **both**, layered — a text-level substring check catches any access style (direct
dict indexing, a different helper function, a typo'd variant), and an AST-based `get(...)`-call
check catches the idiomatic path precisely and gives a better failure message. Either alone is
defensible; I would not spend a whole plan task on the AST version if time is short, since the
substring check alone already satisfies "asserted by test" and every existing frame check reads
`inference.paradigm` (if at all) exclusively through `get(spec, "inference.paradigm")` calls.

**`_INCIDENTAL_GAP_CODES`** (`tests/test_known_bad_corpus.py:49-59`): a `set[str]` of finding
codes documented as "corpus-completeness gaps" — defects the fixtures happen to also have that
are unrelated to what each fixture exists to demonstrate. Two tests police it:
`test_ship_gate_findings_are_all_documented_incidental_corpus_gaps` (lines 202-229) asserts every
CRITICAL/HIGH finding `dsx gate ship` produces against any corpus fixture is either in this set
or belongs to `_TARGET_CODE_FAMILIES` (currently `("DSX-INT-", "DSX-PAR-01")` — `DSX-VAL-` is
**not** a target family for the three *existing* fixtures, since none of them was built to
encode a validity-frame defect); `test_incidental_allowlist_names_no_target_family_code`
(lines 231-245) asserts the reverse — no entry in the allow-list may belong to a target family
(this would make a fixture permanently unable to block on the defect it exists to demonstrate,
once that code ships). **Practical consequence, verified by my own fixture audit above:** if
`DSX-VAL-041` fires HIGH on the bayesian fixture (it will, per the matrix above) and the fixture
is not edited, `"DSX-VAL-041"` must be added to `_INCIDENTAL_GAP_CODES` — this is safe, since
`DSX-VAL-` is not in `_TARGET_CODE_FAMILIES`. The same applies to `DSX-VAL-060` for all three
fixtures **only if** the planner's `not_assessed` policy (Section 8c) ends up firing on it —
recommended design avoids this entirely (see Section 8c).

## Critical planning risk: a real conflict in the known-bad corpus test, not previously named

`07-CONTEXT.md` D-15 states the new `weak-identification-mmm-ANALYSIS-SPEC.yaml` fixture is
created "in this phase" and named by `ROADMAP.md:212-213`. I read that roadmap text directly:

> "`examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` exits `1` at `dsx gate plan`
> naming `DSX-VAL-040`..." (`ROADMAP.md:212-213`)

I also read `tests/test_known_bad_corpus.py::test_every_spec_passes_the_critical_threshold_gate_points`
(lines 187-200) in full:
```python
def test_every_spec_passes_the_critical_threshold_gate_points(self):
    """The corpus's positive gate guarantee: every fixture clears both
    CRITICAL-threshold gate points, `plan` and `execute`, today."""
    specs = self._spec_paths()
    ...
    for path in specs:
        for point in _CRITICAL_THRESHOLD_POINTS:  # ("plan", "execute")
            code, findings = self._gate_findings(path, point)
            ...
            self.assertEqual(code, 0, f"{path.name} failed dsx gate {point} ...")
```
`self._spec_paths()` is `sorted(CORPUS_DIR.glob(f"*{SPEC_SUFFIX}"))` — a directory glob over
`examples/known-bad/*-ANALYSIS-SPEC.yaml`, discovered structurally, not a hardcoded filename
list (`tests/test_known_bad_corpus.py:102-103`).

**These two requirements are in direct conflict.** If
`weak-identification-mmm-ANALYSIS-SPEC.yaml` is placed in `examples/known-bad/` (as its own
filename and D-15 both require), the glob in `_spec_paths()` will pick it up automatically, and
`test_every_spec_passes_the_critical_threshold_gate_points` will assert it clears `dsx gate plan`
with exit code 0 — but the roadmap's own Success Criterion 1 requires that exact file to **exit
1** at that exact gate point, naming `DSX-VAL-040` (a CRITICAL-severity code, correctly blocking
a `plan`-threshold gate by design). This is not a hypothetical: `DSX-VAL-040` is a code this very
phase ships, unlike `DSX-INT-010`/`DSX-PAR-010`/`DSX-PAR-011`, which are why the *existing* three
fixtures can honestly claim to clear `plan`/`execute` today — their target codes don't exist yet.
The new fixture is structurally different: it demonstrates a defect whose catching code ships in
the same phase as the fixture.

**Nothing in `07-CONTEXT.md`'s Decisions or Discretion sections names this conflict** — the
existing "Claude's Discretion" list covers *which* published case to encode and whether the
`041` collision needs a fixture edit or an allow-list entry, but not this test-level
contradiction. I recommend the planner treat this as a required decision point, with a plan task
that explicitly resolves it — plausible resolutions, none of which I am picking on your behalf:
- **(a)** Narrow `test_every_spec_passes_the_critical_threshold_gate_points` (and/or
  `test_ship_gate_findings_are_all_documented_incidental_corpus_gaps`, which iterates the same
  glob) to exclude `weak-identification-mmm`, e.g. via a small "expected-to-already-block" set
  the test consults, keeping the glob-discovery property for everything else.
- **(b)** Add a companion assertion that specifically expects `weak-identification-mmm` to block
  at `plan` with `DSX-VAL-040`, and adjust the blanket assertion's iteration to skip it by name
  or by a lightweight marker (e.g. a sibling `.blocks-at-plan` sentinel file, or a slug pattern).
- **(c)** Reconsider whether this fixture belongs in `examples/known-bad/` at all versus a
  different location that still satisfies `ROADMAP.md:212-213`'s literal path — this option
  conflicts with D-15's explicit verbatim path and is probably not viable, but is listed for
  completeness.

Whichever the planner picks, it must land in the same wave as the fixture and the `DSX-VAL-040`
check itself, since the test conflict cannot be observed until both exist.

## 7. `dsx/mathx.py` conventions

Read: `dsx/mathx.py` (475 lines, in full).

**`inflation_from_peeking()`'s docstring shape** (`dsx/mathx.py:411-417`):
```python
def inflation_from_peeking(total_looks: int, alpha: float = 0.05) -> float:
    """Approximate true type-I error when a fixed-horizon test is peeked ``n`` times.

    Armitage's classic result: repeated naive testing at alpha=0.05 reaches roughly
    0.08 at 2 looks, 0.11 at 3, 0.14 at 5, 0.19 at 10. Interpolated linearly in
    log-looks between the tabulated anchors, then scaled by alpha/0.05.
    """
```
**Note this docstring has no `Citation:` or `Reference value:` line matching the D-05 regexes**
— confirmed by inspection, and independently confirmed by `.planning/STATE.md`'s own open item:
"whether the existing `inflation_from_peeking()` docstring is upgraded to a full D-05 citation
(currently 'Armitage's classic result', no year or paper)... Pre-existing docstring held to a
lower bar than the new checks it will support." This is not a bug to fix in this phase — it is
explicitly named as a Phase 9 open item, not a Phase 7 one — but it means **`inflation_from_peeking()`
is not a template to copy for docstring shape**; `dsx/frame/paradigm.py:61-77` is the template
that actually satisfies D-05's regexes, as established in Section 1.

**How the reference value is asserted in tests** (`tests/test_dsx.py:34-70`, `TestMath` class):
plain `self.assertAlmostEqual(mathx.some_fn(...), expected, places=N)` calls, one per reference
value, grouped in a dedicated `TestMath` class near the top of `test_dsx.py`. No special
machinery — direct function calls against literal expected numbers.

**Recommended `design_effect(m, icc)` shape**, following `inflation_from_peeking()`'s
structure but with a D-05-compliant docstring (unlike its neighbour):
```python
def design_effect(m: float, icc: float) -> float:
    """Design effect (DEFF) for cluster-correlated data — the variance inflation
    factor an analysis at the observation level must account for when the true
    randomization/dependence unit is coarser.

    Citation: Kish, L. (1965), Survey Sampling, p. 258 (Deff definition), pp.
    161-162 (ICC); Higgins, Eldridge & Li (2024), Cochrane Handbook v6.5, §23.1.4
    and §23.1.4.1.
    Reference value: ICC 0.02, average cluster size (m) 29.8 gives
    DEFF = 1 + (29.8 - 1) * 0.02 = 1.576 (the Cochrane Handbook's own worked example).
    """
    if m < 1:
        raise ValueError("m must be >= 1")
    if not 0.0 <= icc <= 1.0:
        raise ValueError("icc must be in [0, 1]")
    return 1.0 + (m - 1.0) * icc
```
and a test: `self.assertAlmostEqual(mathx.design_effect(29.8, 0.02), 1.576, places=3)` with a
`# D-05: DSX-VAL-020` marker nearby (per Section 3, exact placement within `tests/` is flexible
— the scan is a flat text search over the whole tree).

**Important scope note verified against `scripts/gen-finding-catalogue.py`:** `design_effect()`
itself never calls `report.add(...)` — it's a pure math helper, not a check. `check_d05()`'s
enforcement is keyed off `report.add(...)` call sites (Section 3), so `design_effect()`'s own
docstring is **not** mechanically checked by `--check`. The Citation/Reference-value block that
*is* mechanically required lives on whichever `val.py` function contains the actual
`report.add("DSX-VAL-020", ...)` call — that function's docstring should also carry (or
reference) the same citation, since it's the one D-05 gates on. Giving `design_effect()` its own
citation-shaped docstring anyway is good practice for discoverability, but does not substitute
for the check function's docstring.

## 8. Open modelling questions

### 8a. Dependence structure → admissible method family (`temporal`/`spatial`/`hierarchical`)

`DEPENDENCE_STRUCTURES` (`dsx/spec.py:186-193`) has six members; D-04 supplies citations for two
(`clustered`, `repeated_measures`) from `research/ARCHITECTURE.md:298-324`. `VARIANCE_ADJUSTMENTS`
(`dsx/spec.py:96`) has exactly four members: `cluster_robust`, `delta_method`, `bootstrap_cluster`,
`mixed_effects`. My recommendation for the remaining three, with citations checked against live
sources (see Sources section — tagged `[CITED]`, not `[VERIFIED]`, since I did not open the
primary texts myself, only confirmed the citations are real, correctly attributed publications):

| Structure | Recommended admissible set | Rationale | Citation |
|---|---|---|---|
| `temporal` | `{cluster_robust, bootstrap_cluster, mixed_effects}` | Serial correlation within a time-ordered series is the textbook case for clustering standard errors on time blocks, block-bootstrapping over time, or fitting an explicit autocorrelation structure via a mixed/random-effects model. `delta_method` addresses transformed-parameter variance, not serial dependence, so it does not belong here. | Cameron, A.C. & Miller, D.L. (2015), "A Practitioner's Guide to Cluster-Robust Inference", *Journal of Human Resources* 50(2):317-372 — covers both cross-sectional and serial-dependence clustering |
| `spatial` | `{cluster_robust, bootstrap_cluster, mixed_effects}` | Same admissible set as `temporal` for the same structural reason (nearby-observation correlation, not independent-unit correlation): geographic clustering of standard errors, spatial block bootstrap, or an explicit spatial random-effects term. | Cameron & Miller (2015), as above, plus Conley, T.G. (1999), "GMM Estimation with Cross Sectional Dependence", *Journal of Econometrics* 92(1):1-45 (spatial-HAC estimators — establishes the premise that ordinary standard errors are invalid under spatial dependence, motivating why *some* adjustment is required) |
| `hierarchical` | `{mixed_effects, cluster_robust}` | Multiple nested levels of grouping (e.g. respondents within stores within regions) is the canonical multilevel-model case; `mixed_effects` is the primary tool, `cluster_robust` (clustering at the top level) the common simplification — the same admissible pair D-04 already assigns to `repeated_measures`. | Gelman, A. & Hill, J. (2007), *Data Analysis Using Regression and Multilevel/Hierarchical Models*, Cambridge University Press — the standard reference for multilevel/hierarchical modelling (exact chapter locator not verified this session; the book's Part 2A is the multilevel-modelling section per its published table of contents) |

`[CITED]` — I confirmed via web search that both Cameron & Miller (2015) and Gelman & Hill
(2007) are real, correctly-attributed publications (multiple independent sources agree on
author/year/title/journal/publisher), but I have not opened either primary text to confirm exact
page/chapter locators the way the existing D-05 ledger did for the other eight codes. The
planner should treat these citations as a strong starting point, not a final, page-verified
locator — following the project's own "flag, do not invent" precedent
(`dsx/frame/paradigm.py:66-72`), a `design_restriction`-style honest disclosure that the exact
section number is unverified would be appropriate if the planner ships these without further
verification.

### 8b. Recommended `CONSTRAINT_SOURCES` partition for `DSX-VAL-041`

`CONSTRAINT_SOURCES` (`dsx/spec.py:171-184`) has five members. `07-CONTEXT.md` confirms no
published source settles the carries/does-not-carry-parameter-scale-information partition and
the docstring must say so. Reading each member's own description text in `dsx/spec.py` directly
(not inferring from the name alone) gives an internally consistent, definitionally-grounded
partition:

| Member | Own description (`dsx/spec.py:172-184`) | Carries parameter-scale info? |
|---|---|---|
| `none` | "No external constraint informs the estimate beyond the observed data." | **No** — its own definition is the negation |
| `informative_priors` | "A prior distribution encodes external information about the parameter." | **Yes** — "about the parameter" is explicit |
| `penalisation` | "A penalty term ... shrinks the estimate toward a null or reference value." | **Yes** — shrinkage target is a parameter-scale value |
| `design_restriction` | "The study design itself restricts the parameter space (e.g. a capped effect by construction)." | **Yes** — "restricts the parameter space" is explicit |
| `hierarchical_pooling` | "Partial pooling across groups in a hierarchical model constrains group-level estimates." | **Yes** — "constrains group-level estimates" is explicit |

**Recommendation:** `{informative_priors, penalisation, design_restriction, hierarchical_pooling}`
carry parameter-scale information; `{none}` alone does not. This is the simplest partition
consistent with each member's own vocabulary text, requires inventing no new distinctions, and
matches both verified fixture outcomes in Section 4 (`good`: `constraint_source: none` +
`strength: strong` → no fire; `bayesian-continuous-monitoring`: `constraint_source:
informative_priors` + `strength: strong` → fires, matching D-14's prediction). The docstring
must still carry the honest disclosure D-05 requires: this four-versus-one split is
project-defined, not published, even though each individual classification follows directly
from the vocabulary's own stated definitions.

### 8c. Missingness `(mechanism, implied method)` pairs for `DSX-VAL-060`

D-07 explicitly resolves two cells: MAR + complete-case → HIGH (White & Carlin's real
unbiased-under-MAR sub-case); MNAR + no mechanism model → CRITICAL. `MISSINGNESS_MECHANISMS`
(`dsx/spec.py:222-230`) has exactly four members: `MCAR`, `MAR`, `MNAR`, `not_assessed`
(deliberately no `none` member — R-02, "missingness is never absent, only unassessed").

**`missingness.method_implied` genuinely has no closed vocabulary** — verified by reading
`dsx/spec.py`'s `_VALIDITY_FRAME_MEMBERSHIP` tuple (`:719-728`) in full: it lists eight
`(sub_block, sub_field, vocab)` triples for membership checking, and `missingness.method_implied`
is not among them (only `missingness.mechanism` is checked against `MISSINGNESS_MECHANISMS`).
Free text like `"complete_case"`, `"multiple_imputation"` or a placeholder can appear in this
field with no structural validation today. This means `DSX-VAL-060`'s lookup table needs its own
small closed set of recognised method-implied strings (e.g. `complete_case`,
`multiple_imputation`, `inverse_probability_weighting`, `full_information_maximum_likelihood`,
`modelled` / `mechanism_explicitly_modelled`) to key its pairing lookup against — an unrecognised
value should presumably be treated conservatively (flag, or at minimum "cannot verify"), which is
itself a decision the planner should make explicit and document, since it's new ground D-07
doesn't cover.

**`not_assessed` — direct evidence from my own fixture audit, not previously flagged anywhere in
the plan inputs:** all three existing known-bad fixtures declare `mechanism: not_assessed` with
`method_implied: complete_case` (`interference-shared-budget:159-161`,
`bayesian-continuous-monitoring:166-168`, `frequentist-uncontrolled-continuous:154-156`). D-14's
prose lists this fact but assigns it no required fix, and neither corpus test
(`test_every_spec_passes_the_critical_threshold_gate_points`,
`test_ship_gate_findings_are_all_documented_incidental_corpus_gaps`) has any allowance for a
`DSX-VAL-060` finding on these three files today. **Recommendation:** design the lookup table to
treat `not_assessed` as a skip condition (no finding), structurally parallel to how `DSX-VAL-030`
should skip `dependence.structure: none` (Section 4) — an honestly-declared "not evaluated" is a
different epistemic state from a wrong pairing, and there is no known-good/known-bad pairing to
test `not_assessed` against in the first place (the check would be asserting a judgment about a
value the spec author explicitly declared as unknown). This keeps all three existing fixtures
passing without any new fixture edits or `_INCIDENTAL_GAP_CODES` entries — the simplest outcome,
and the one most consistent with the corpus's silence on this combination. If the planner instead
wants `not_assessed` to be treated as CRITICAL (arguably the more conservative, arguably more
correct statistical position — an unassessed mechanism genuinely cannot license any method), that
is a legitimate alternative, but it must come with three new `_INCIDENTAL_GAP_CODES` entries (one
per existing fixture) added deliberately, not discovered by a failing test after the fact.

## 9. Plan slicing recommendation

`ROADMAP.md:201-203` confirms no ordering constraint among the nine requirements themselves.
Reading the actual code surfaces four *mechanical* ordering constraints CONTEXT.md names only in
prose (D-16); I give the precise reasons below so the planner can sequence waves with confidence
rather than caution:

1. **`dsx/spec.py` additions (the structure→method map, the falsifier lexicon/refusal-word
   list, any new helper like the placeholder detector from Section 4) must land before
   `dsx/frame/val.py` can import them.** Natural Wave 0 — no dependency the other direction.

2. **`dsx/mathx.py::design_effect()` must land before or with the `DSX-VAL-020` check**, since
   the finding text needs to call it. Independent of everything else — can be Wave 0 alongside
   the `spec.py` additions, or its own micro-wave; either is fine since nothing else in the phase
   depends on `mathx.py`.

3. **The `scripts/gen-finding-catalogue.py` edits (`PREFIX_GROUPS`, `_D05_ALLOWLIST_PREFIXES`)
   and the `dsx/frame/paradigm.py::_NOT_SHIPPED` edit must land atomically with — not merely
   "before or with" in a loose sense, but in the exact same commit as — the first
   `report.add("DSX-VAL-0NN", ...)` call anywhere in the codebase.** I verified this precisely
   against `tests/test_dsx.py::test_applied_prefixes_have_codes_and_not_shipped_prefixes_have_none`
   (lines 2585-2607): it asserts, for `paradigm.py`'s computed `applied` set, that every prefix
   in it has ≥1 known code, **and separately** that every prefix literally present in
   `_NOT_SHIPPED` has **zero** known codes. Before any `DSX-VAL-*` code exists, `"DSX-VAL-"` must
   remain in `_NOT_SHIPPED` (else the first assertion fails — an "applied" prefix with no code
   yet). The moment even one `DSX-VAL-*` code exists, `"DSX-VAL-"` must already be removed from
   `_NOT_SHIPPED` (else the second assertion fails — a `_NOT_SHIPPED` prefix that does have a
   code). There is no commit ordering that satisfies both sides except landing the removal in the
   same commit as the first check that emits a `DSX-VAL-*` code. If the plan splits the nine
   checks across multiple waves (reasonable, given they're independent), the `_NOT_SHIPPED`
   removal belongs with the **first** wave that ships any `DSX-VAL-*` code, not a separate
   "plumbing" wave before it and not a "cleanup" wave after it.

4. **`brief.md` §7 citation extension (D-17) should land with or before the first check that
   cites one of the newly-added sources**, per its own text ("before Phase 7 code lands") — in
   practice this means Wave 0 or folded into whichever wave ships the first citing check.

5. **Fixture edits (D-12 template, D-13 good fixture, D-14 known-bad fixtures, D-15 new
   known-bad fixture) should land after the checks whose behaviour they're meant to exercise
   exist**, since verifying "the good fixture now passes `DSX-VAL-060`" requires `DSX-VAL-060` to
   exist. In practice this makes fixture/test-conflict resolution (see the dedicated section
   above) a late wave, after the check-implementation waves.

6. **`research/FEATURES.md`'s 3.45 correction (D-10) is fully independent** — no code dependency
   either direction — and can happen in any wave, including a first, tiny "documentation
   correction" wave that also carries the `brief.md` §7 extension, since both are prose-only
   edits with no test dependency.

**Recommended wave shape** (not prescriptive on wave *count* — the planner may merge or split
further):
- **Wave 0 — shared infrastructure:** `dsx/spec.py` additions (structure→method map, falsifier
  lexicon, placeholder detector), `dsx/mathx.py::design_effect()` + its test, `brief.md` §7
  extension, `research/FEATURES.md` correction.
- **Wave 1 — first checks + atomic build-plumbing landing:** implement whichever subset of the
  nine checks ships first, **together with** the `gen-finding-catalogue.py` edits and the
  `paradigm.py::_NOT_SHIPPED` removal in the same commit (constraint 3 above), plus
  `dsx/cli.py` registration (`CHECKS["val"]`, `GATE_PROFILES` entries).
- **Wave 2..N — remaining checks:** the rest of the nine, however split; no further plumbing
  needed once Wave 1 has landed the registration and build-script edits.
- **Late wave — fixtures, template, and the corpus-test conflict:** D-12/D-13/D-14 edits, the new
  D-15 fixture + post-mortem, and the required resolution of the
  `test_every_spec_passes_the_critical_threshold_gate_points` conflict described above. This
  wave necessarily comes after all nine checks exist, since it's exercising their combined
  behaviour against real specs.
- **REQ-P7-09 test** (no `DSX-VAL-*` path reads `inference.paradigm`) can land any time after
  `val.py` exists in any form — recommend landing it with Wave 1 so it starts proving the
  invariant from the first check onward rather than being bolted on at the end.

## Package Legitimacy Audit

Not applicable — this phase adds zero new external dependencies. D-01 requires standard-library-only
code on the gate path, and every file this phase touches or creates (`dsx/frame/val.py`,
`dsx/spec.py`, `dsx/mathx.py`, `dsx/cli.py`, `scripts/gen-finding-catalogue.py`, YAML fixtures,
markdown docs, test files) uses only Python's standard library, confirmed by reading every
source file in this research pass — none contains a `pip install`-able import beyond what the
repository already depends on (and the repository's existing dependency set is unchanged by this
phase). No `npm view`/`pip index versions`/`cargo search` check applies.

## Environment Availability

Skipped — this phase is pure Python standard-library code and Markdown/YAML documentation, with
no external tool, service, runtime or package-manager dependency beyond the Python interpreter
already required to run any part of this repository. `python3 -m unittest discover -s tests -v`
is the only execution dependency, and it is already relied on by every prior phase.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Python standard-library `unittest` (no pytest, no config file — confirmed: no `pytest.ini`/`tox.ini`/`Makefile` found in the repository root) |
| Config file | none |
| Quick run command | `python3 -m unittest tests.test_dsx -v` (or the specific new test module, once created) |
| Full suite command | `python3 -m unittest discover -s tests -v` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| REQ-P7-01 | Estimand blank field / non-discriminating falsifier blocks | unit (`val.check(spec)` dict literal) | `python3 -m unittest tests.test_dsx -v -k estimand` (new tests) | ❌ Wave 1 — new test module/class needed |
| REQ-P7-02 | Unit-triad mismatch blocks with DEFF quantified, published value asserted | unit (`mathx.design_effect` + `val.check`) | `python3 -m unittest tests.test_dsx -v -k design_effect` | ❌ Wave 0/1 |
| REQ-P7-03 | VAL-020/EXP-021 never both fire | gate-level (`self._run([...])`) against both existing v1.5.0 EXP-020/021 fixtures and new VAL fixtures | `python3 -m unittest tests.test_dsx -v -k units` | ❌ Wave 1, reusing existing EXP-020/021 fixtures as regression proof |
| REQ-P7-04 | Dependence without method family blocks | unit | new test class | ❌ Wave 1/2 |
| REQ-P7-05 | Weak/strong-ID checks cite Gelman, Simpson & Betancourt | unit + docstring/citation via `gen-finding-catalogue.py --check` | `python3 scripts/gen-finding-catalogue.py --check` | ❌ Wave 1/2 for the check; `--check` command already exists |
| REQ-P7-06 | Sampling frame vs claim population | unit | new test class | ❌ Wave 1/2 |
| REQ-P7-07 | Missingness mechanism vs implied method | unit | new test class | ❌ Wave 1/2 |
| REQ-P7-08 | Measurement construct/operationalisation | unit | new test class | ❌ Wave 1/2 |
| REQ-P7-09 | No `DSX-VAL-*` path reads `inference.paradigm` | new boundary-style test (AST or text-level, see Section 6) | `python3 -m unittest tests.test_frame_boundary -v` (extended) or a new sibling test module | ❌ Wave 1 |

### Sampling Rate

- **Per task commit:** targeted `python3 -m unittest tests.test_dsx -v -k <relevant>` plus
  `python3 scripts/gen-finding-catalogue.py --check` once any `report.add("DSX-VAL-...")` exists.
- **Per wave merge:** `python3 -m unittest discover -s tests -v` (full suite — this repo has no
  slow/integration split, everything runs fast enough to always run in full).
- **Phase gate:** full suite green, `gen-finding-catalogue.py --check` green, and the corpus
  conflict resolution (see dedicated section) explicitly landed, before `/gsd-verify-work`.

### Wave 0 Gaps

- [ ] A new test class/module for `dsx/frame/val.py` unit tests (mirroring the shape of the
      `DSX-SPEC-080/081/082` tests at `tests/test_dsx.py:390-474`) — does not exist yet.
- [ ] `mathx.design_effect()` reference-value test in the existing `TestMath` class
      (`tests/test_dsx.py:33`) — function and test both new.
- [ ] The REQ-P7-09 no-paradigm-read test — either a new method on
      `tests/test_frame_boundary.py::TestFrameImportBoundary` or a new sibling test class; neither
      exists yet.
- [ ] Resolution of the known-bad corpus test conflict (dedicated section above) — this is a
      **test-suite design gap**, not just a fixture gap; the plan needs an explicit task for it.

## Security Domain

`security_enforcement: true`, `security_asvs_level: 1` in `.planning/config.json`. This phase's
threat surface is narrow and I traced it against the actual code, not assumed from the domain
label: the module reads an already-parsed, already-loaded Python `dict` (the YAML spec is loaded
and validated for structure well before `val.check(spec)` runs — see `dsx/cli.py::run_checks`),
performs string comparisons and dict lookups against closed vocabularies, and writes only
`Finding`/`DecisionRecord` objects — no network call, no file write beyond the existing
`DECISIONS.jsonl` append path (already covered by Phase 6's security review), no subprocess, no
dynamic code execution, no external package.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | No auth surface — a local CLI reading a local file |
| V3 Session Management | No | No session concept |
| V4 Access Control | No | No access-control surface |
| V5 Input Validation | Yes (narrow) | The spec dict is already structurally validated by `validate_structure()` before any frame check runs; `val.py` must still not crash on missing/malformed sub-fields — the existing pattern (`is_blank()`, `.get()` with defaults, `section()`/`items()` helpers in `dsx/spec.py`) already handles this defensively and `val.py` should reuse it rather than assuming presence |
| V6 Cryptography | No | No cryptographic operation in this phase (the existing `sha256` frame-digest and decision-trail machinery is Phase 6's, untouched here) |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| A malformed `validity_frame` sub-block (wrong type — a string or list where a dict is expected) crashes a check instead of degrading to a finding | Denial of Service (of the gate itself) | Mirror `dsx/spec.py:788` (`if not isinstance(frame, dict) or not frame:`) — every sub-block access in `val.py` must type-check before attribute access, exactly as the existing `_validate_validity_frame_shape()` already does for the top-level block; `tests/test_dsx.py:476-483`'s `test_malformed_validity_frame_shapes_degrade_to_dsx_spec_080_not_a_crash` is the existing precedent test shape to copy for each new sub-block `val.py` reads |
| A finding's `detail`/`remedy` text echoes attacker-controlled spec content (e.g. a YAML `title` or `estimand.quantity` value) into a rendered report with no escaping | Information disclosure (low severity — this is a local CLI report, not a web response) | Already the existing pattern for every check in this repo (`f"Metric {name!r} has no definition"` etc. — Python's `!r` repr already neutralizes most injection-flavoured concerns for a text-only, local-only report); no new control needed since `val.py` follows the same idiom |

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `temporal`/`spatial` dependence structures should admit `{cluster_robust, bootstrap_cluster, mixed_effects}`; `hierarchical` should admit `{mixed_effects, cluster_robust}` | 8a | If wrong, `DSX-VAL-030` either over-blocks legitimate temporal/spatial/hierarchical designs or under-blocks invalid ones; low risk since the check is additive to two already-cited structures and easy to adjust before ship |
| A2 | Exact chapter/section locators for Cameron & Miller (2015) and Gelman & Hill (2007) are not verified against the primary text this session — only author/year/title/venue are confirmed via web search | 8a | D-05 requires a locator precise enough to be checkable; shipping an unverified locator as if verified would repeat the exact failure mode D-05 exists to prevent — must be flagged in the docstring per the project's own "flag, do not invent" precedent, or verified before ship |
| A3 | `DSX-VAL-060` should skip (not fire on) `mechanism: not_assessed` regardless of `method_implied` value | 8c | If wrong (the planner decides `not_assessed` should be CRITICAL), all three existing known-bad fixtures need edits and/or three new `_INCIDENTAL_GAP_CODES` entries not currently anticipated by any plan input |
| A4 | `missingness.method_implied` needs its own small closed set for `DSX-VAL-060`'s lookup table, since it has no existing vocabulary membership check | 8c | If the planner instead treats it as unconstrained free text with substring matching (mirroring the falsifier lexicon approach), the lookup table design changes shape entirely — worth deciding explicitly rather than discovering mid-implementation |
| A5 | The recommended `CONSTRAINT_SOURCES` partition (`none` alone does not carry parameter-scale information; the other four do) is the correct project-defined split | 8b | Low risk — directly derived from each vocabulary member's own description text already in `dsx/spec.py`, and matches both fixture outcomes I traced by hand; a different partition would need to explain why a specific member's own stated definition doesn't imply what it says |

## Open Questions

1. **Which published weak-identification case the D-15 marketing-mix-model fixture should
   encode.**
   - What we know: it must trip `DSX-VAL-040` (`strength: weak`, `constraint_source: none`) and
     needs a sourced post-mortem like its three siblings; vendor blogs/Medium posts are
     inadmissible (per CONTEXT.md's Discretion list).
   - What's unclear: no specific published marketing-mix-model case was identified in this
     research pass — this needs a dedicated literature search the planner or a later research
     pass should do, since it's load-bearing for D-15/Success Criterion 1 and I did not find one
     with sufficient confidence to name here.
   - Recommendation: treat as a Wave-0-or-later research spike within the plan itself, or a
     `checkpoint:human-verify` if the plan wants a human to pick the specific published case.

2. **Whether `not_assessed`+`complete_case` should be a skip (my recommendation, 8c) or a
   flagged case requiring `_INCIDENTAL_GAP_CODES` additions.**
   - What we know: the corpus is silent on it today; my recommendation keeps the three existing
     fixtures untouched.
   - What's unclear: whether "unassessed missingness" is a defect worth catching on its own
     merits (arguably yes, from a pure statistics standpoint) versus this phase's stated boundary
     (adjudicate the declared mechanism against the declared method, not adjudicate the *absence*
     of an assessment — which arguably belongs to a different, not-yet-specified check).
   - Recommendation: make this an explicit planner decision, not an implicit default.

## Environment Availability

(See above — section included and marked skipped, per the template's own instruction to state
this explicitly rather than omit it silently.)

## Sources

### Primary (HIGH confidence — read directly this session)

- `dsx/frame/paradigm.py` (163 lines, read in full) — the module-shape template
- `dsx/cli.py` (773 lines, read in full) — registration mechanics
- `scripts/gen-finding-catalogue.py` (316 lines, read in full) — D-05 build-check contract
- `dsx/spec.py` (958 lines, read in full) — vocabularies, structural validators, `_VALIDITY_FRAME_MEMBERSHIP`
- `dsx/mathx.py` (475 lines, read in full) — numeric helper conventions
- `dsx/findings.py` (228 lines, read in full) — `Report`/`Finding` actual location
- `dsx/decisions.py` (213 lines, read in full) — `DecisionRecord` schema
- `dsx/checks/__init__.py` (52 lines, read in full) — confirms `Report`/`Finding` are not re-exported here
- `dsx/checks/design.py:250-339` — `DSX-EXP-020/021` exact trigger logic
- `dsx/frame/__init__.py` (27 lines, read in full) — package-level D-03a boundary statement
- `tests/test_frame_boundary.py` (126 lines, read in full) — AST boundary scanner mechanics
- `tests/test_known_bad_corpus.py` (331 lines, read in full) — corpus invariants, `_INCIDENTAL_GAP_CODES`
- `tests/test_dsx.py` (selected sections: 1-70, 370-540, 1186-1260, 1380-1500, 1440-1500, 2570-2610) — test conventions
- `examples/good-ANALYSIS-SPEC.yaml`, `examples/bad-ANALYSIS-SPEC.yaml`, `templates/ANALYSIS-SPEC.yaml`, all three `examples/known-bad/*.yaml` (read in full) — the fixture matrix in Section 4
- `.planning/config.json` — workflow toggles (`nyquist_validation: true`, `security_enforcement: true`, `security_asvs_level: 1`)
- `.planning/REQUIREMENTS.md:94-104`, `.planning/ROADMAP.md:186-236`, `.planning/STATE.md` (read in full)

### Secondary (MEDIUM confidence — WebSearch corroborated against multiple independent sources)

- Cameron, A.C. & Miller, D.L. (2015), "A Practitioner's Guide to Cluster-Robust Inference", *Journal of Human Resources* 50(2):317-372 — confirmed via web search (JHR publisher page, UC Davis author page, multiple citation aggregators agree); exact section locator not verified this session
- Gelman, A. & Hill, J. (2007), *Data Analysis Using Regression and Multilevel/Hierarchical Models*, Cambridge University Press — confirmed via web search (Cambridge publisher page, author's own book site); exact chapter locator not verified this session

### Tertiary (LOW confidence — `[ASSUMED]`, not verified this session)

- Conley, T.G. (1999), "GMM Estimation with Cross Sectional Dependence", *Journal of Econometrics* — cited from training knowledge for the `spatial` structure recommendation, not independently web-verified this session; the planner should verify before treating it as a locked D-05 citation

## Metadata

**Confidence breakdown:**
- Module shape, registration mechanics, D-05 build-check contract: HIGH — every claim traced to
  a specific file and line, read in full this session, with the CONTEXT.md import-source error
  caught and corrected by direct inspection.
- Fixture × check matrix: HIGH for the six fixtures' current-state behaviour (every value quoted
  is from the actual file); MEDIUM for the inferred check-implementation logic itself, since
  `val.py` doesn't exist yet — the matrix is my derivation of what D-02/D-03/D-05/D-06/D-07/D-08/D-09
  imply the checks would do, not an observation of running code.
- The known-bad corpus test conflict: HIGH — verified by reading both the roadmap text and the
  test source directly; this is a structural fact about two documents disagreeing, not an
  interpretation.
- Structure→method citations for `temporal`/`spatial`/`hierarchical` (8a): MEDIUM — publications
  confirmed real and correctly attributed, locators not page-verified.
- `not_assessed` missingness recommendation (8c): MEDIUM — strong circumstantial evidence from
  the corpus's silence, but not a directly-stated rule anywhere in the plan inputs.

**Research date:** 2026-08-12
**Valid until:** This research is tied to the exact state of the repository at commit
`3cebf50` (per the session's git status) — valid until the next commit touches any of the Primary
sources listed above, at which point line numbers in particular should be re-verified before
reuse.
