# Phase 7: Validity frame checks (`DSX-VAL-*`) - Context

**Gathered:** 2026-08-10 (assumptions mode)
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 7 adjudicates the **paradigm-independent content** of the `validity_frame:` block that
Phase 6 made parseable. Phase 6 checks *shape* (`DSX-SPEC-080/081/082` — block absent, required
sub-block missing, sub-field outside its closed vocabulary). Phase 7 checks *content*: a missing
or unfalsifiable estimand, a unit triad that guarantees pseudo-replication, dependence declared
with no method family, weak identification dressed as strong, a sampling frame that cannot carry
the claim population, a missingness mechanism the implied method cannot survive, and a
measurement construct with no operationalisation.

Requirements: REQ-P7-01 … REQ-P7-09 (9 requirements, see `.planning/REQUIREMENTS.md:94-104`).

**Not in this phase.** `DSX-INT-*` (interference, triggering, stability) is Phase 8;
`DSX-PAR-010/011` is Phase 9; `DSX-PRE-*` is Phase 10; `references/families.yaml` and
`dsx/frame/admissibility.py` are Phase 11. No `DSX-VAL-*` check may read `inference.paradigm`
(D-11) — that is the whole point of the layer.

**Do not duplicate Phase 6 shape checks.** If a sub-block is absent entirely, `DSX-SPEC-081`
already fires at CRITICAL. `DSX-VAL-*` fires on a sub-block that is *present and internally
incoherent*.

</domain>

<decisions>
## Implementation Decisions

### Locked upstream — do NOT re-litigate

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

### Module layout, registration and code numbering

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

### Dependence: `method_family_required` shape (Open Item 1, now resolved)

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

### Making free-text fields decidable under D-01 and D-02

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

### The design-effect number — a correction to the plan

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

### Fixtures, template and build plumbing

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

### The D-05 citation ledger — use these verbatim

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

### Folded Todos

None — `todo.match-phase 7` returned zero matches.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Binding inputs — not re-litigable

- `brief.md` §4 — decisions D-01…D-14. D-05 and D-11 govern this phase.
- `brief.md` §5.1 (`brief.md:119-186`) — the `validity_frame:` contract with every sub-field name
  and the inline `DSX-VAL-020/040/041` trigger comments. Note `06-CONTEXT.md:344-346`: brief §5
  *structure* binds, brief §5 *token-level phrasing* does not (`cluster_robust_or_mixed` is the
  case in point — see D-04).
- `brief.md` §6.5 gated backlog; §7 reference sources (**extended by D-17**); §9 runtime constraints.
- `.planning/PROJECT.md` — Key Decisions M-01…M-09, Constraints, Out of Scope, Known limits.
- `.planning/REQUIREMENTS.md:94-104` — REQ-P7-01…REQ-P7-09; `:149-163` Out of Scope;
  `:165-171` Open Items (**both Phase 7 items resolved by D-02 and D-04 above**).
- `.planning/ROADMAP.md:186-236` — Phase 7 goal, dependencies, and the five success criteria.
  `:78-82` states the milestone-wide D-05 bar.
- `.planning/STATE.md:61-66` — standing per-phase deliverables.
- `.planning/phases/06-contract-extension-decision-record-paradigm-manifest/06-CONTEXT.md` —
  D-01…D-23, especially D-10 (severity is the gate point), D-11 (finding granularity),
  D-20…D-23 (the D-05 mechanism this phase's checks must satisfy).

### Research — advisory, superseded where this CONTEXT.md says so

- `.planning/research/ARCHITECTURE.md:160-162` (module layout), `:219-227` (code grouping —
  **its `DSX-VAL-001` is overridden by D-02**), `:235-238` (gate-profile precedent),
  `:285-296` (unit drift), `:298-324` (the dependence map D-04 adopts).
- `.planning/research/PITFALLS.md:171-188` (false-positive adoption cost), `:200-227` (severity
  tiering), `:643` (escape-hatch warning).
- `.planning/research/FEATURES.md:50-52` — **contains the unpublished 3.45 design-effect value;
  superseded by D-10.** `:284-305` (missingness validity, supports D-07), `:313-332` (Gelman,
  Simpson & Betancourt thesis verification).

### Source files this phase creates, modifies or must not disturb

- **Creates:** `dsx/frame/val.py`; `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml`
  and its post-mortem.
- `dsx/frame/paradigm.py:27-33` `_PARADIGM_INDEPENDENT`, `:45-48` invariant tests, `:50`
  `_NOT_SHIPPED` (**edited**), `:60` the `check(spec)` signature to mirror, `:66-72` the
  unverified-locator precedent.
- `dsx/spec.py:53` `CAUSAL_VERBS` (the exclusion precedent), `:96` `VARIANCE_ADJUSTMENTS`,
  `:162-184` `IDENTIFICATION_STRENGTHS`/`CONSTRAINT_SOURCES`, `:186-193` `DEPENDENCE_STRUCTURES`,
  `:222-230` `MISSINGNESS_MECHANISMS`, `:272` `_VOCABULARIES`, `:712-728` the Phase 6 requiredness
  and membership tuples, `:816-835` the scalar membership loop (**why D-04 rejects a list**).
- `dsx/cli.py` `CHECKS` and `GATE_PROFILES` (**edited**), `:105-110` `GATE_THRESHOLDS`,
  `:558-567` `cmd_init`.
- `dsx/checks/design.py:293-307` — `DSX-EXP-021`. **Must not change** (REQ-P7-03).
- `dsx/mathx.py` — `inflation_from_peeking()` precedent; gains `design_effect()` (D-11).
- `dsx/decisions.py` + `dsx/spec.py:766` — the `DecisionRecord` emission pattern to follow.
- `scripts/gen-finding-catalogue.py:26-44`, `:59`, `:75-79`, `:179-181`, `:251-254` (**edited**).
- `templates/ANALYSIS-SPEC.yaml:288`, `:291-292`, `:296-298`, `:331` (**edited**, D-12).
- `examples/good-ANALYSIS-SPEC.yaml:302`, `:339-342`, `:344-347` (**edited**, D-13);
  `examples/bad-ANALYSIS-SPEC.yaml:211`.
- `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml:113-126` (**edited**, D-14);
  `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml:131-133`.
- `tests/test_frame_boundary.py:35` — the D-03a deny list.
- `tests/test_known_bad_corpus.py:41-45`, `:193-200`, `:202-229` `_INCIDENTAL_GAP_CODES`.
- `tests/test_dsx.py:1239-1244`, `:1390-1393` — the two template assertions D-12 touches.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- **`dsx/frame/paradigm.py`** — the complete template for a `dsx/frame/*` module: `check(spec)`
  signature, docstring citation shape, `DecisionRecord` emission, `report.add` call form. Phase 7
  copies its structure wholesale.
- **`dsx/mathx.py` `inflation_from_peeking()`** — the precedent for a pure numeric helper carrying a
  published reference value and a linked test. `design_effect()` follows it exactly.
- **`dsx/checks/claims.py:350-370` `_NUMBER_RE`** — numeric-token extraction with unit-aware
  exclusions, the pattern D-05's falsifier numeric test needs. **Cannot be imported** under D-03a;
  re-home the pattern in `dsx/spec.py`.
- **`dsx/checks/narrative.py:17-21` and `dsx/checks/claims.py:107-113`** — proof that lexicon-based
  free-text adjudication is an established idiom here, not an invention. Same import restriction.
- **`scripts/gen-finding-catalogue.py` `extract()`** — already resolves a docstring upward from a
  `report.add(...)` call site; D-16 only adds prefix entries, no new machinery.
- **`tests/test_known_bad_corpus.py` `_INCIDENTAL_GAP_CODES`** — the existing mechanism for a
  fixture tripping a code that is not its encoded defect (ship-level only; the plan/execute
  assertion at `:193-200` has no escape hatch).

### Established Patterns

- **Severity selects the gate point, not registration.** `spec` and `frame.paradigm` are already in
  every profile; CRITICAL blocks from plan, HIGH from verify. D-03 assigns severity accordingly and
  registers `val` in three of four profiles for scope, not for blocking behaviour.
- **Findings carry `detail`, `remedy` and `where`, and actionability predicts fix rate.** The
  `DSX-VAL-020` finding must quantify the design-effect consequence in `detail` (REQ-P7-02).
- **A check that branches on `inference.paradigm` is in the wrong layer** (D-11). REQ-P7-09 requires
  a test asserting no `dsx/frame/val.py` path reads it — extend the existing AST machinery in
  `tests/test_frame_boundary.py` rather than writing a second scanner.
- **Flag an unverified citation locator; never invent one.** `dsx/frame/paradigm.py:66-72` and the
  Phase 6 decision log both set this precedent.
- **Check for name collisions before coining a term** (`06-CONTEXT.md:346-348`) — applies to the
  new module constant names in D-04 and D-05.

### Integration Points

- `dsx/frame/val.py` — new module, all nine codes. Imports only `Report`/`Finding` from
  `dsx/checks/`; may import `dsx/spec.py`, `dsx/mathx.py` and `dsx/decisions.py` freely.
- `dsx/spec.py` — the structure→method map (D-04) and the falsifier lexicon (D-05), both excluded
  from `_VOCABULARIES`.
- `dsx/cli.py` — `CHECKS["val"]` plus three profile entries.
- `dsx/mathx.py` — `design_effect(m, icc)`.
- `scripts/gen-finding-catalogue.py` — two edits, then catalogue regeneration.
- `tests/` — new tests plus `# D-05: DSX-VAL-0NN` markers; edits to
  `tests/test_known_bad_corpus.py` fixtures (not assertions) and the two template tests.

</code_context>

<specifics>
## Specific Ideas

- **The 3.45 design-effect value in `research/FEATURES.md:50-52` is unsourced and must not ship.**
  This is a live instance of exactly what D-05 exists to catch: a plausible number, correct
  arithmetic, attributed to "commonly reproduced in cluster-RCT methods texts", printed in none of
  them. It survived research synthesis and roadmap authoring unchallenged. **Correct
  `research/FEATURES.md` too, or the next agent to read it reintroduces the value.**
- **Cronbach & Meehl (1955) states REQ-P7-08's criterion almost verbatim** — "A necessary condition
  for a construct to be scientifically admissible is that it occur in a nomological net, at least
  *some* of whose laws involve observables" (p. 290). This requirement went from the phase's
  weakest-sourced to its best-sourced. Use the sentence in the finding's `remedy` text.
- **Two of this phase's checks rest on project-defined partitions, and both must say so out loud**
  (the `CONSTRAINT_SOURCES` split and the five-field estimand). A gate that presents a project
  convention as a published finding is the failure mode D-05 names.
- **`brief.md` §5.1's `constraint_source: informative_priors_from_lift_tests` (`brief.md:141`) is
  not a member of the shipped `CONSTRAINT_SOURCES` vocabulary** (`dsx/spec.py:171-184`). Another
  case of brief §5 phrasing not binding at token level — the same trap `06-CONTEXT.md:344-346`
  recorded.

</specifics>

<deferred>
## Deferred Ideas

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

### Reviewed Todos (not folded)

None — no pending todos matched Phase 7.

</deferred>

---

*Phase: 07-validity-frame-checks-dsx-val*
*Context gathered: 2026-08-10*
