# Phase 11: Frequentist admissibility adjudicator (`DSX-ADM-*`) - Research

**Researched:** 2026-08-20
**Domain:** Statistical-procedure ontology as data; a gate-time adjudicator over a closed
YAML vocabulary; CLI composition; build-time citation enforcement.
**Confidence:** HIGH for schema/parser/composition/call-site findings (all verified by
executing the actual code in this repository); MEDIUM for the estimand-axis recommendation
(a design choice, not a fact, but backed by a concrete traceability failure demonstrated
against the committed corpus); MEDIUM for the exact family roster (sized and evidenced, but
final axis values are explicitly Claude's Discretion per `11-CONTEXT.md`).

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

All of `11-CONTEXT.md`'s D-01 through D-29 are locked and binding. This research does not
re-litigate any of them; it answers the questions `11-CONTEXT.md` explicitly left open. The
full decision list is reproduced in `11-CONTEXT.md` and is not duplicated here verbatim to
avoid drift between two copies — the planner MUST read `11-CONTEXT.md` directly. The load-bearing
subset this research depends on most heavily:

- D-01/D-02: `references/families.yaml` ships ~10-14 families (not 25-35); REQ-P11-01 and
  ROADMAP SC 1 are amended by this phase, with the amendment written into
  `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md`.
- D-03/D-03a: the alias table has exactly one consumer (`dsx/frame/admissibility.py`); no
  code under `dsx/frame/` imports from `dsx.checks` (no carve-out).
- D-04/D-04a: `recommend-test` is extended by composition inside `dsx/cli.py::cmd_recommend`;
  `recommend_test()` itself is not moved, wrapped, or edited; a reverse-direction boundary
  scanner should be added to `tests/test_frame_boundary.py`.
- D-05: data file resolves as `Path(__file__).resolve().parents[2] / "references" / "families.yaml"`,
  loaded once via `dsx.loader.load()`; a missing/unreadable file is `CheckError` -> exit 2.
- D-06/D-07/D-08/D-09: exact YAML shape constraints (flat mappings, no anchors/merge
  keys/block scalars/document markers), flat `inference_method:` key (never a string
  starting `inference.`), a test pinning both loader paths to agree, `locator_status:
  verified | unverified` per entry.
- D-10/D-11: ~16-19 assumption tokens with per-token citations, a mandatory `notes:` field,
  an explicit `vocabulary_is_not_exhaustive: true` header declaration; six source clusters.
- D-12 through D-18: ranking is a rule table (not a scoring function); four citable
  orderings; Manski's Law of Decreasing Credibility as the structural fallback;
  lexicographic tiebreak on family `id`, byte-stable; three causes collapse into one
  `DSX-ADM-020`; `DecisionRecord.escalate`/`alternatives_rejected` get their first user;
  an unrecognised alias escalates, never fuzzy-matches.
- D-19 through D-22: exactly two codes (`DSX-ADM-010` HIGH, `DSX-ADM-020` CRITICAL);
  registered at `plan`/`verify`/`ship`, absent from `execute`; exit 1 via the ordinary
  `emit()` path (never `CheckError`); frequentist-only scoping happens **outside**
  `dsx/frame/admissibility.py`, via a helper exported from `dsx/frame/paradigm.py`.
- D-23 through D-25: a new sibling function in `scripts/gen-finding-catalogue.py` (not an
  extension of `check_d05`); two-sided enforcement (build-time citation check, run-time
  refusal to rank an uncited family); `"DSX-ADM-"` added to `_D05_ALLOWLIST_PREFIXES`.
- D-26 through D-29: two live citation-correction hazards (Delacre 2017/2022 Correction,
  Pustejovsky & Tipton 2018/2023 Corrigendum); a live D-05 defect in
  `references/test-selection.md` that this phase must fix; NIST as the preferred
  reference-value source; two previously-unverified locators now resolved.

### Claude's Discretion

- **The estimand axis shape** — this research's primary deliverable; see
  [Estimand Axis](#the-estimand-axis-primary-research-output) below. Binding constraint
  either way: no fuzzy string match on free prose may become the primary lookup path.
- Which 10-14 families, and their exact axis values, within D-01's sourcing rule.
- Plan slicing across the six requirements, subject to `families.yaml` and its citations
  existing before the adjudicator is written against them.
- Whether the reverse-direction boundary scanner (D-04a) ships as its own plan or rides
  along with the module that creates the temptation.
- Exact membership of the 16-19 assumption tokens, beyond the clusters named in D-11.
- Which NIST Statistical Reference Dataset backs each family reducible to linear-model
  arithmetic.

### Deferred Ideas (OUT OF SCOPE)

- Growing `families.yaml` to 25-35 entries — Phase 12, alongside the corpus that justifies
  them.
- Reconciling the two procedure-name comparison mechanisms (the alias table vs.
  `dsx/checks/stats.py` / `dsx/frame/prereg.py`'s raw string compares) — needs its own
  phase with a suppression-migration story.
- Bayesian procedure admissibility (`DSX-ADM-*` second axis) — gated backlog, entry
  condition M4 shipped **and** `dsx stats --paradigm` showing Bayesian frames above 15%.
- Closing the reference-value gap for quantile, count/rate, survey-weighted and
  delta-method families — either before those families ship, or those families wait.
- Pinning the Wooldridge edition for the MLR.1-MLR.6 assumption tokens.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-P11-01 | `references/families.yaml` holds ~10-14 (amended from 25-35, D-02) estimator families as data, keyed on estimand x family x inference method x dependence handling, parsed by the existing loader | [Families.yaml Schema](#families-yaml-schema-verified-round-trip), [Which Families](#which-10-14-families) — worked, parser-verified 3-entry example; concrete 12-family roster traced to fixtures |
| REQ-P11-02 | Named tests resolve as aliases into families rather than being enumerated as a test catalogue | [Alias Resolution Algorithm](#alias-resolution-algorithm) |
| REQ-P11-03 | The admissibility function returns a ranked admissible set, naming for each entry the assumptions bought and charged | [Ranking Algorithm](#ranking-algorithm-and-decisx-adm-010-vs-020-semantics) |
| REQ-P11-04 | An underdetermined frame returns `no_admissible_procedure` and escalates rather than guessing | [Ranking Algorithm](#ranking-algorithm-and-decisx-adm-010-vs-020-semantics), D-16 |
| REQ-P11-05 | The adjudicator extends the existing `dsx recommend-test` rather than replacing it | [cmd_recommend Composition](#cmd_recommend-composition-exact-signature) |
| REQ-P11-06 | D-05 applies to `families.yaml` entries as it does to checks: each family carries a primary-source citation, enforced by the M1 catalogue check | [gen-finding-catalogue.py Changes](#gen-finding-cataloguepy-changes) |
</phase_requirements>

## Summary

Phase 11 adds one new frame module (`dsx/frame/admissibility.py`), one new data file
(`references/families.yaml`), a composition point inside an existing CLI command
(`cmd_recommend`), a new sibling function in the build-time citation gate
(`scripts/gen-finding-catalogue.py`), and a paradigm-routing call site in `run_checks`. No
new runtime dependency is introduced (D-01: stdlib only on the gate path); the file is
parsed by the existing two-parser `dsx.loader.load()`, verified in this research to
round-trip identically on both the PyYAML path and the bundled-parser path for a
representative 3-family, 3-token worked example (D-08's mechanical proof).

The single highest-value finding is that **the "estimand axis" cannot be
`analysis.outcome_type` + `n_groups` + `paired`** (the second option CONTEXT.md names) without
breaking D-01's own traceability requirement: `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml`
— the committed fixture that specifically needs the `linear_regression` family — has **no**
`analysis:` block and **no** `model:` block at all. Its only procedure signal is
`inference.primary_procedure: linear_regression`. Keying the estimand axis on `analysis.*`
fields leaves this fixture's axis permanently blank, meaning the `linear_regression` family
entry required by D-01 could never actually be exercised by the one fixture that justifies
it — self-defeating against ROADMAP SC 5 ("every family entry traces to a fixture ... that
needed it"). The recommended alternative — a new **optional** `validity_frame.estimand.type`
field backed by a new closed `ESTIMAND_TYPES` vocabulary registered in `dsx/spec.py` — reaches
every committed fixture (the `estimand:` sub-block is always-required, per
`_VALIDITY_FRAME_ALWAYS_REQUIRED`) and slots into the existing `_VALIDITY_FRAME_MEMBERSHIP`
enforcement mechanism with zero new code paths.

A second load-bearing finding, verified by reading `tests/test_known_bad_corpus.py`'s
`_TARGET_DEFECT_CODES` map directly: **`validity_frame.estimand.type` must be populated in
all nine committed specs, not only `good-ANALYSIS-SPEC.yaml`.** `post-hoc-procedure-switch`
today clears `dsx gate plan` (its target defect, `DSX-PRE-030`, only fires at
verify/ship — `prereg` is absent from `GATE_PROFILES["plan"]`). If the new axis field is left
blank on that fixture, `DSX-ADM-020` (CRITICAL, blank-axis cause) will newly fire at `plan`,
flipping that fixture's `dsx gate plan` exit code from 0 to 1 and silently corrupting the
per-fixture target-defect map's guarantee. This is not hypothetical — it is a direct,
demonstrable consequence of the axis design, verified against the actual test file.

**Primary recommendation:** add `validity_frame.estimand.type` (optional, closed vocabulary,
`ESTIMAND_TYPES` in `dsx/spec.py`) as the estimand axis; build `references/families.yaml` as a
top-level mapping with a `vocabulary_is_not_exhaustive: true` header key, a block-sequence
`assumption_vocabulary:` key, and a block-sequence `families:` key (verified round-trip on
both loader paths in this session); resolve aliases by scanning each candidate family's own
`aliases:` list after filtering by `(estimand.type, dependence.structure)`, never globally
and never fuzzily; compose `cmd_recommend`'s output as a flat dict merge (existing
`recommend_test()` keys unchanged, one new `"admissibility"` key added only when a spec is
resolvable) so v1.5.0 CLI output is byte-identical when no spec is available.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Estimator ontology (families, aliases, assumptions) | Data (`references/families.yaml`) | — | Pure declarative data, no logic; D-01 explicitly forbids computing anything from it |
| Admissibility ranking / refusal | Frame layer (`dsx/frame/admissibility.py`) | — | Adjudicates a frame's coherence — the frame layer's defined job; must not import `dsx.checks` (D-03a) |
| Frequentist-only scoping | Frame layer (`dsx/frame/paradigm.py`) | CLI (`dsx/cli.py::run_checks`) | D-22: computed by a helper outside `admissibility.py`, passed in as a bool by the CLI dispatch layer — mirrors how `run_checks` already derives `strict`/`reconcile_trail` before dispatch |
| Gate registration and severity routing | CLI (`dsx/cli.py`: `CHECKS`, `GATE_PROFILES`, `GATE_THRESHOLDS`) | — | Existing single point where every check family is wired into the four gate points |
| `dsx recommend-test` composition | CLI (`dsx/cli.py::cmd_recommend`) | Checks layer (`dsx/checks/stats.py::recommend_test`) + Frame layer (`dsx/frame/admissibility.py`) | D-04: CLI is the *only* place the two packages meet (`dsx/cli.py:23-52` already imports both) |
| Build-time citation enforcement | Build script (`scripts/gen-finding-catalogue.py`) | — | Off the gate path entirely; runs in CI/pre-commit, not at `dsx gate` |
| Decision-trail emission | Frame layer (`dsx/frame/admissibility.py`) via `report.context["decisions"]` | CLI (`dsx/cli.py::_write_decision_trail`) writes the file | Existing pattern every other frame check already follows (`val.py`, `paradigm.py`) |

## Standard Stack

No new runtime dependency. D-01 (stdlib only on the gate path) and the project's existing
architecture already provide everything this phase needs:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `dsx.loader` (in-repo) | current | Parses `references/families.yaml` — same loader every other spec/template uses | D-05 names it explicitly; verified in this session to round-trip both parser paths |
| Python stdlib (`pathlib`, `functools`, `dataclasses`) | 3.9+ (matches repo's existing `from __future__ import annotations` style) | File resolution, caching the loaded ontology, no new abstractions needed | Every existing `dsx/frame/*.py` module uses only these |
| PyYAML | 6.0.3 (installed and verified in this research session; **optional** at runtime per D-06/D-08) | One of the two loader paths `dsx.loader.load()` already supports | Confirmed present in this dev environment; the bundled fallback parser (`dsx/loader.py::_parse_yaml_subset`) must still parse the file identically when PyYAML is absent |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Reusing `dsx.loader.load()` | A dedicated small YAML-subset parser for `families.yaml` only | Explicitly forbidden by REQ-P11-01 ("parsed by the existing loader with no new parser") |
| `validity_frame.estimand.type` closed vocabulary | Free-text `validity_frame.estimand.quantity` with fuzzy/substring matching | Explicitly forbidden by CONTEXT.md's binding constraint (no fuzzy string match as primary lookup path) |
| `validity_frame.estimand.type` closed vocabulary | `analysis.outcome_type` + `n_groups` + `paired` | Demonstrated in this research to leave `weak-identification-mmm`'s axis permanently blank (no `analysis:`/`model:` block exists in that fixture) — breaks D-01/SC5 traceability |

**Installation:** None required — no new package. If PyYAML is not already installed in a
target environment, `dsx.loader.load()` already degrades gracefully to its bundled parser;
this phase does not change that contract.

## Package Legitimacy Audit

Not applicable. This phase installs no external package (D-01: stdlib only on the gate
path; the sole dependency touched, PyYAML, is a pre-existing optional dependency of
`dsx.loader`, already shipped and already conditionally imported at `dsx/loader.py:20-23`).
No `npm view` / `pip index versions` / `cargo search` check is needed and none was run.

## The Estimand Axis (primary research output)

CONTEXT.md names two candidate shapes and leaves the choice to planning, with one binding
constraint: no fuzzy string match on free prose may become the primary lookup path.

### Option B (rejected): key on `analysis.outcome_type` + `n_groups` + `paired`

This is the shape `recommend_test()` already takes (`dsx/checks/stats.py:32-45`), and reusing
it would avoid inventing a new vocabulary — an appealing property, since M-09 already set a
project-wide precedent against parallel vocabularies (`dependence.method_family_required`
reuses `VARIANCE_ADJUSTMENTS` rather than defining a new set).

**Verified, decisive problem:** `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml`
— read in full during this research — has **no `analysis:` block and no `model:` block at
all**. Confirmed by direct grep across the file: zero matches for `^analysis:` or `^model:`.
Its only fields naming a procedure are `design.identification: regression_adjustment` and
`inference.primary_procedure: linear_regression`. This fixture is the one D-01 explicitly
names as the source justifying the `linear_regression` family
("the six distinct procedure labels present across all nine committed specs ... `linear_regression`").
Under Option B, this fixture's estimand axis is unconditionally blank — the `linear_regression`
family could never be reached through it, which means ROADMAP SC 5 ("every family entry
traces to a fixture ... that needed it") could never be proven for that family. This is not
a marginal edge case; it is the single fixture the requirement's own procedure-label list
depends on.

A second, structural problem: Option B's axis lives in a block (`analysis:`) that is **not**
one of the ten `validity_frame` sub-blocks and has no requiredness gate at all
(`REQUIRED_TOP_LEVEL` in `dsx/spec.py:483` does not include it; `_validate_validity_frame_shape`
never touches it). Any causal/observational spec that reasons purely through `design:` +
`validity_frame:` (exactly the shape a regression-adjustment analysis takes) has no obligation
to declare `analysis:` at all.

### Option A (recommended): new optional `validity_frame.estimand.type` field

Add a new closed-vocabulary field `validity_frame.estimand.type`, backed by a new
`ESTIMAND_TYPES` vocabulary registered in `dsx/spec.py` alongside the project's other closed
vocabularies (`_VOCABULARIES` list, `dsx/spec.py:332-357`), and added as one more row to
`_VALIDITY_FRAME_MEMBERSHIP` (`dsx/spec.py:845-854`):

```python
# dsx/spec.py — new vocabulary, same shape as every existing one (name -> description dict)
ESTIMAND_TYPES = {
    "difference_in_proportions": "The estimand is a difference (or ratio) between two or more group proportions.",
    "difference_in_means": "The estimand is a difference between two or more group means.",
    "regression_coefficient": "The estimand is a coefficient from a fitted regression model.",
}
# ... registered in _VOCABULARIES, exactly like every other entry:
    ("estimand_types", ESTIMAND_TYPES),
# ... added to _VALIDITY_FRAME_MEMBERSHIP:
    ("estimand", "type", ESTIMAND_TYPES),
```

Because `_validate_validity_frame_shape`'s membership loop (`dsx/spec.py:948-967`) already
`continue`s on a blank value before checking vocabulary membership, this field is
**structurally optional by construction** — no `_VALIDITY_FRAME_ALWAYS_REQUIRED` change is
needed, so no existing spec (inside or outside this repository) is newly broken by its
introduction. Declaring it out-of-vocabulary produces the existing `DSX-SPEC-082` (HIGH) for
free, with zero new code in `dsx/spec.py` beyond the two additions above.

Because `validity_frame.estimand` is one of the six **always-required** sub-blocks
(`_VALIDITY_FRAME_ALWAYS_REQUIRED`, `dsx/spec.py:838-840`), this field is reachable from
**every** spec that has passed Phase 6's own shape gate — including
`weak-identification-mmm`, whose `estimand:` sub-block is fully populated (quantity,
population, contrast, time_window, falsifier all present) even though it has no
`analysis:`/`model:` block at all.

**This closes the exact gap Option B could not close**, at the cost of one new field the
plan must populate across the corpus (see next section).

### Consequence the planner must action: populate the new field on all nine committed specs

Verified by reading `tests/test_known_bad_corpus.py:96-131`'s `_TARGET_DEFECT_CODES` map
directly: `post-hoc-procedure-switch` maps to `{"verify": "DSX-PRE-030"}` only — **no
`"plan"` key** — because `prereg` is absent from `GATE_PROFILES["plan"]`
(`dsx/cli.py:100-101`). This fixture clears `dsx gate plan` today. If
`validity_frame.estimand.type` is left blank on this fixture once `admissibility` joins
`GATE_PROFILES["plan"]`, `DSX-ADM-020` (CRITICAL, "required axis blank" per D-16) will newly
fire at `plan`, flipping this fixture's plan-gate exit code from 0 to 1 and requiring
`_TARGET_DEFECT_CODES["post-hoc-procedure-switch"]` to be edited just to keep the existing
test green — a change with no relationship to the fixture's actual purpose (demonstrating
`DSX-PRE-030`).

**Action for the plan:** populate `validity_frame.estimand.type` on all nine committed specs
(`good-ANALYSIS-SPEC.yaml`, `bad-ANALYSIS-SPEC.yaml`, all six `examples/known-bad/*.yaml`
fixtures, and `templates/ANALYSIS-SPEC.yaml`) as part of the same plan that introduces the
field — not just the good fixture. This is the standing "extend both canonical fixtures"
deliverable (recorded in `.planning/STATE.md`'s Accumulated Context) generalised to the full
known-bad corpus, because unlike prior phases' fields this one is read by a check
(`admissibility`) newly registered at `plan` — a gate point every known-bad fixture is
already asserted against.

## Families.yaml Schema (verified round-trip)

D-06 requires: a top-level mapping whose one key holds a block sequence of flat mappings;
axis keys and `citation` are single-line quoted scalars; `aliases`/`buys`/`charges` are
sequences of scalars; no anchors, no merge keys, no `|`/`>` block scalars, no `---` document
markers. D-08 requires a test proving the committed file parses identically on both loader
paths.

**This research built a representative worked example (3 families, 3 assumption tokens) and
executed it through `dsx.loader.load()` twice in this session** — once with PyYAML importable
(installed for this research: `pyyaml==6.0.3`), once with `dsx.loader._pyyaml` monkeypatched
to `None` to force the bundled-parser path — and confirmed **byte-for-byte equal parsed
output** on both paths.

```yaml
# references/families.yaml — worked example, VERIFIED to round-trip identically through
# both dsx.loader.load() paths (PyYAML present and PyYAML absent) in this research session.

vocabulary_is_not_exhaustive: true

assumption_vocabulary:
  - token: "exchangeability"
    citation: "Hernan, M.A. & Robins, J.M. (2020), Causal Inference: What If, Chapter 3, sections 3.1-3.5"
    locator_status: "verified"
  - token: "no_variance_pretesting"
    citation: "Zimmerman, D.W. (2004), Journal of General Psychology 131(2):142-160"
    locator_status: "verified"
  - token: "uniform_domination_over_conditional_exact"
    citation: "Lydersen, S., Fagerland, M.W. & Laake, P. (2009), Statistics in Medicine 28(7):1159-1175, section 9"
    locator_status: "verified"

families:
  - id: "welch_t"
    estimand: "difference_in_means"
    family: "welch_t"
    inference_method: "frequentist"
    dependence: "none"
    aliases: ["welch_t", "welchs_t_test", "students_t_welch"]
    buys: ["no_variance_pretesting"]
    charges: ["exchangeability"]
    citation: "Delacre, M., Lakens, D. & Leys, C. (2017), International Review of Social Psychology 30(1):92-101, plus 2022 Correction DOI 10.5334/irsp.661"
    locator_status: "verified"
    notes: "Preferred over Student's t unconditionally per Delacre et al 2017/2022 correction and Ruxton 2006; do not pre-test variance equality (Zimmerman 2004)."

  - id: "boschloo_exact"
    estimand: "difference_in_proportions"
    family: "boschloo_unconditional"
    inference_method: "frequentist"
    dependence: "none"
    aliases: ["boschloo_exact", "unconditional_exact"]
    buys: ["uniform_domination_over_conditional_exact"]
    charges: ["exchangeability"]
    citation: "Lydersen, S., Fagerland, M.W. & Laake, P. (2009), Statistics in Medicine 28(7):1159-1175, section 9"
    locator_status: "verified"
    notes: "Uniformly dominates Fisher's exact test in power (Lydersen et al 2009 section 9) -- the only genuine uniform domination found in the ranking research (D-13)."

  - id: "cluster_robust_ols"
    estimand: "regression_coefficient"
    family: "linear_regression"
    inference_method: "frequentist"
    dependence: "clustered"
    aliases: ["cluster_robust_ols", "cluster_robust", "linear_regression_cr"]
    buys: ["exchangeability"]
    charges: ["exchangeability"]
    citation: "MacKinnon, J.G., Nielsen, M.O. & Webb, M.D. (2023), Journal of Econometrics 232(2):272-299"
    locator_status: "verified"
    notes: "CV3/wild bootstrap dominate CV1 on reliability grounds (MacKinnon Nielsen Webb 2023 section 9), hedged by the authors themselves and known to fail with few treated clusters."
```

**Key design decisions in this schema, each justified against the actual code:**

1. **Top level has three keys** (`vocabulary_is_not_exhaustive`, `assumption_vocabulary`,
   `families`), not literally one. D-06's "one key holds a block sequence of flat mappings"
   is read here as distinguishing the block-sequence-holding key from scalar keys, not as an
   assertion that the file has exactly one top-level key overall — `dsx.loader.load()`
   requires only that the top level be *a mapping* (`dsx/loader.py:43-44`), which this
   satisfies regardless of key count. **This reading is a judgment call, not a verified
   fact — flag it to the user/planner for confirmation before treating it as settled,**
   because a stricter reading (literally one top-level key) is also textually defensible and
   would require nesting `assumption_vocabulary` and the header flag under the same key as
   `families` (e.g. all three as siblings inside one `ontology:` mapping).
2. **No block scalars (`|`/`>`) anywhere**, including in `notes:` — every free-text field
   uses a single-line double-quoted scalar. This is the safest possible choice against D-08's
   named hazard (`_strip_comment`'s space-preceded-`#` truncation inside `|` blocks): avoiding
   block scalars entirely sidesteps the whole class of divergence, rather than requiring every
   future editor to remember never to write ` #` inside one.
3. **`assumption_vocabulary` and `families` are separate top-level lists.** D-10's ~16-19
   assumption tokens each need their own citation, independent of which family cites them
   (a token like `exchangeability` is charged by many families) — a single shared list avoids
   the citation for one token drifting across the families that reference it, and keeps each
   family entry's own `citation:` field scoped to the *procedure's* primary source, not the
   token's.
4. **`buys`/`charges` are plain token-name sequences** (`["exchangeability"]`), matching D-06's
   "sequences of scalars" exactly — the token's citation lives once, in
   `assumption_vocabulary`, never duplicated per family.

**Build-time invariant the plan should test for:** within any single `(estimand, dependence)`
pair, no two family entries may declare an overlapping `aliases` value — this is what keeps
alias resolution unambiguous per candidate set (see next section) without requiring global
alias uniqueness across the whole file (the same alias string, e.g. `"welch_t"`, may
legitimately appear in more than one family entry across different dependence structures if a
future family needs it, though the worked corpus below does not require this).

## Alias Resolution Algorithm

REQ-P11-02 ("named tests resolve as aliases into families rather than being enumerated as a
test catalogue") and D-18 ("an unrecognised alias escalates rather than resolving — no
nearest-match, no fuzzy string comparison") together specify an **exact-match, closed-set**
lookup. Recommended algorithm, all string comparisons via the existing
`dsx.spec.normalize()` (lower + `-`/space -> `_`, already imported by every frame module —
no new normalization scheme):

1. Build the alias table once, at load time, as a derived structure — **not** a separate
   YAML section — by iterating every family entry's `aliases:` list:
   `alias_table[normalize(alias)] = family_id` for each `(family, alias)` pair. This keeps
   the alias and its owning family's citation physically adjacent in the source file (easier
   to audit than a standalone alias->family mapping that could drift from the family
   definitions it names).
2. Read the declared procedure from `inference.primary_procedure` (**not** `analysis.test`):
   `primary_procedure` is the pre-registered, forward-looking declaration this phase's
   admissibility question is about; `analysis.test` names what was *executed*, which is
   `dsx/frame/prereg.py`'s territory (D-03 explicitly keeps prereg's own executed-vs-declared
   reconciliation untouched by this phase's alias table).
3. Filter `families.yaml` to the candidate set `C` matching
   `(validity_frame.estimand.type, validity_frame.dependence.structure)`, both read directly
   from the frame (no alias resolution involved in this step).
4. If `inference.primary_procedure` is non-blank, resolve it via `alias_table` — this can
   surface three distinct outcomes worth distinguishing in `report.context` even though they
   collapse to one finding code (D-16): (a) resolves to a family inside `C` — the ordinary
   case; (b) resolves to a family **outside** `C` — the declared procedure names a family
   whose own `(estimand, dependence)` disagrees with the frame's declared axis values,
   informative for the finding's detail text; (c) does not resolve at all — D-16's third
   named cause.

## Ranking Algorithm and DSX-ADM-010 vs -020 Semantics

Working backward from D-19's severities (`DSX-ADM-010` HIGH, `DSX-ADM-020` CRITICAL) and the
standing constraint that `examples/good-ANALYSIS-SPEC.yaml` must keep passing every gate at
every threshold (`.planning/STATE.md`'s "Standing per-phase deliverables": *"extend both
canonical fixtures; the two exit-code tests stay unchanged"*), `DSX-ADM-010` cannot fire
unconditionally whenever ranking succeeds — the good fixture declares
`inference.primary_procedure: two_proportion_z` under `dependence.structure: clustered`, and
if `DSX-ADM-010` fired on every successful ranking regardless of the declared choice's
standing, the good fixture would newly block at `ship` (HIGH threshold) — a direct regression
against that standing invariant.

**Recommended semantics**, consistent with D-12's requirement that "`DSX-ADM-010`'s message
names which rule fired and what condition it depends on":

- `DSX-ADM-020` (CRITICAL) fires when the admissible set for the candidate filter is empty
  for any of D-16's three collapsed causes (blank axis, zero matching families, unresolved
  alias). This is refusal — REQ-P11-04's `no_admissible_procedure`.
- `DSX-ADM-010` (HIGH) fires when the admissible set is non-empty **and** the declared
  procedure (resolved via step 4 above) is admissible but **not the top-ranked entry** —
  naming the specific rule (D-13's four citable orderings, or D-14's Manski fallback) that
  ranks another family above it. This is "you are using a legal but dominated choice,"
  distinct from refusal.
- When the declared procedure resolves to the top-ranked entry (or no procedure is yet
  declared — this check can run informationally before commitment, same as
  `recommend_test()` itself), neither code fires; `report.ok(...)` records the pass, matching
  every other frame check's convention.

**This means every family entry the plan adds for a fixture that is supposed to clear a gate
cleanly must be checked against that fixture's actual declared procedure and dependence
structure to confirm it resolves to the top-ranked (or sole) candidate** — otherwise
`DSX-ADM-010` will newly fire on fixtures that have no reason to carry it. This is a concrete
verification step the plan should include as a task, not leave to incidental discovery at
test time.

## Which ~10-14 Families

D-01 requires covering the six procedure labels present in the committed corpus
(`two_proportion_z`, `welch_t`, `fishers_exact`, `bayesian_ab`, `linear_regression`, and the
template's `null`) and the three committed dependence structures (`none`, `clustered`,
`temporal`) — **verified directly by grepping every committed spec** in this research
session:

| Fixture | Declared procedure | Dependence | Estimand (this phase's new axis) |
|---|---|---|---|
| `good-ANALYSIS-SPEC.yaml` | `two_proportion_z` | `clustered` | `difference_in_proportions` |
| `bad-ANALYSIS-SPEC.yaml` | `welch_t` (deliberately wrong family) | (n/a — legacy fixture, always blocks) | `difference_in_proportions` |
| `bayesian-continuous-monitoring` | `bayesian_ab` | `none` | (excluded — `paradigm: bayesian`, D-22) |
| `frequentist-uncontrolled-continuous` | `two_proportion_z` | `none` | `difference_in_proportions` |
| `interference-shared-budget` | `two_proportion_z` | `clustered` | `difference_in_proportions` |
| `post-hoc-procedure-switch` | declared `two_proportion_z`, executed `fishers_exact` | `none` | `difference_in_proportions` |
| `triggering-dilution` | `welch_t` | `clustered` | `difference_in_means` |
| `weak-identification-mmm` | `linear_regression` (via `inference.primary_procedure` only — no `analysis:`/`model:` block) | `temporal` | `regression_coefficient` |
| `templates/ANALYSIS-SPEC.yaml` | placeholder / null | `none` (default) | (placeholder) |

Since `bayesian_ab` is excluded from this phase's admissible set entirely (D-22 scopes
`DSX-ADM-*` to frequentist frames only — `paradigm: bayesian` frames never reach
`admissibility.check()`), the frequentist procedure set that actually needs coverage
collapses to five labels: `two_proportion_z`, `welch_t`, `fishers_exact`, `linear_regression`,
plus whatever alternates each of D-13's four citable orderings requires as the *other* side
of the pairing.

**Recommended 12-family roster** (within D-01's 10-14 band), each entry justified either by a
direct fixture trace or by one of D-13's four named orderings (each ordering needs both sides
of its pair present, or `DSX-ADM-010`'s "which rule fired" message has no dominated
alternative to name):

| # | Family (`id`) | Estimand | Dependence | Traceability |
|---|---|---|---|---|
| 1 | `two_proportion_z` | `difference_in_proportions` | `none` | `frequentist-uncontrolled-continuous`, `post-hoc-procedure-switch` (declared side) |
| 2 | `two_proportion_z_cluster_robust` | `difference_in_proportions` | `clustered` | `good-ANALYSIS-SPEC.yaml`, `interference-shared-budget` (matches `dependence.method_family_required: cluster_robust`) |
| 3 | `fishers_exact` | `difference_in_proportions` | `none` | `post-hoc-procedure-switch` (executed side, D-01's explicit label list) |
| 4 | `boschloo_exact` | `difference_in_proportions` | `none` | D-13 ordering #2 (Lydersen, Fagerland & Laake 2009 §9 — dominates #3) |
| 5 | `welch_t` | `difference_in_means` | `none` | D-13 ordering #1 partner (dominates #6); general two-sample continuous case |
| 6 | `students_t` | `difference_in_means` | `none` | D-13 ordering #1 (Delacre, Lakens & Leys 2017 + 2022 Correction; Ruxton 2006 — dominated by #5) |
| 7 | `welch_t_cluster_robust` | `difference_in_means` | `clustered` | `triggering-dilution` |
| 8 | `linear_regression_cv1` | `regression_coefficient` | `temporal` | D-13 ordering #3 partner (dominated by #9); `weak-identification-mmm`'s dependence axis |
| 9 | `linear_regression_cv3_wild_bootstrap` | `regression_coefficient` | `temporal` | D-13 ordering #3 (MacKinnon, Nielsen & Webb 2023 §9 — dominates #8); `weak-identification-mmm` |
| 10 | `linear_regression_unadjusted` | `regression_coefficient` | `none` | D-13 ordering #4 partner (dominated by #11) |
| 11 | `linear_regression_interacted_adjustment` | `regression_coefficient` | `none` | D-13 ordering #4 (Lin 2013 "cannot hurt"; Freedman 2008 — dominates #10) |
| 12 | `linear_regression_cluster_robust` | `regression_coefficient` | `clustered` | `weak-identification-mmm`-adjacent coverage; the general clustered-regression case (Cameron & Miller 2015) |

This roster is a **starting recommendation, not a locked list** — CONTEXT.md explicitly
reserves "which 10-14 families, and their exact axis values" for the planner's discretion.
The evidence backing it (which fixtures need which labels, which D-13 orderings need both
sides of their pair present) is what this research contributes; the final citations, exact
`buys`/`charges` tokens per family, and `locator_status` flags are plan-time work.

## cmd_recommend Composition (exact signature)

Read in full: `dsx/cli.py:396-409` (current `cmd_recommend`) and `dsx/cli.py:727-735`
(current `p_rec` parser — **has no `--spec`/`--phase-dir` flags today**, unlike almost every
other subcommand, which all call `add_common(...)`).

Current behavior: `dsx recommend-test proportion --groups 2` always prints
`json.dumps(recommendation, indent=2)` where `recommendation` is exactly
`recommend_test()`'s return dict (`{"test", "rationale", "alternatives", "effect_size"}`) —
no spec is ever read.

**D-04 requires:** `cmd_recommend` calls `recommend_test` and the new `admissibility` module
"separately and merges their output." Recommended concrete implementation, preserving
byte-identical output when no spec is available (this is what "extended, not replaced" means
operationally for a CLI tool with no prior `--spec` flag):

```python
# dsx/cli.py — p_rec gains --spec/--phase-dir (new)
p_rec.add_argument("--spec", help="path to ANALYSIS-SPEC (auto-discovered when omitted)")
p_rec.add_argument("--phase-dir", help="GSD phase directory to search and resolve paths against")

# dsx/cli.py::cmd_recommend — merge by flat dict update, not nesting
def cmd_recommend(args: argparse.Namespace) -> int:
    from .checks.stats import recommend_test
    from .frame.admissibility import admissible_families  # pure function, no Report

    recommendation = recommend_test(
        args.outcome_type, args.groups, paired=args.paired,
        normal=_tri(args.normal), equal_variance=_tri(args.equal_variance),
        n_per_group=args.n_per_group, overdispersed=_tri(args.overdispersed),
    )
    output: dict[str, object] = dict(recommendation)  # SAME top-level keys as v1.5.0

    try:
        path = find_spec(args.spec, args.phase_dir)
    except CheckError:
        path = None
    if path is not None:
        spec = load(path)
        output["admissibility"] = admissible_families(spec)  # new key, additive only

    print(json.dumps(output, indent=2))
    return 0
```

This keeps `recommendation`'s four existing keys (`test`, `rationale`, `alternatives`,
`effect_size`) at the **same top level**, not nested under a new `"recommend_test"` wrapper
key — a caller piping v1.5.0 output with no `--spec` given sees byte-identical JSON. The one
new key, `"admissibility"`, appears only when a spec is resolvable — this is the "extended,
not replaced" property ROADMAP SC 2 asks for, made concrete.

**`admissible_families(spec) -> dict` should be a pure function** (no `Report`, no findings,
no `DecisionRecord`) — mirroring the exact split already established in
`dsx/checks/stats.py` between `recommend_test()` (pure, `dsx/cli.py:396-409` calls it
directly) and `_check_declared_test()` (the `Report`-emitting wrapper,
`dsx/checks/stats.py:405-487`). `dsx/frame/admissibility.py::check(spec, applies_to_frame)`
(the `CHECKS["admissibility"]` gate entry point) then calls `admissible_families(spec)`
internally and translates its result into `DSX-ADM-010`/`DSX-ADM-020` findings plus the
`DecisionRecord`. This reuse of an existing, already-precedented split inside the same
package is the cleanest way to satisfy D-04's "separately and merges" instruction without
duplicating the ranking logic between the CLI composition point and the gate check.

## The `run_checks` Call-Site Change

Read in full: `dsx/cli.py:100-113` (`GATE_PROFILES`), `dsx/cli.py:147-202` (`run_checks`),
`dsx/cli.py:63-82` (`CHECKS`), and `dsx/frame/paradigm.py:54-57` (`_PARADIGM_CONDITIONAL`,
already lists `"DSX-ADM-"` under `"frequentist"`).

**GATE_PROFILES** — `"admissibility"` is added to `plan`, `verify` and `ship`, absent from
`execute` (D-20), following exactly the same insertion pattern `"val"`/`"interference"`
already use:

```python
GATE_PROFILES: dict[str, tuple[str, ...]] = {
    "plan": ("spec", "design", "metrics", "coherence", "paradigm", "val", "interference", "admissibility"),
    "execute": ("spec", "ml", "repro", "dq", "code", "paradigm"),  # unchanged
    "verify": (
        "spec", "design", "stats", "ml", "metrics", "claims", "viz", "repro",
        "dq", "coherence", "smells", "figures", "narrative", "code", "decision",
        "paradigm", "val", "interference", "prereg", "admissibility",
    ),
    "ship": (  # same addition as verify
        "spec", "design", "stats", "ml", "metrics", "claims", "viz", "repro",
        "dq", "coherence", "smells", "figures", "narrative", "code", "decision",
        "paradigm", "val", "interference", "prereg", "admissibility",
    ),
}
```

**CHECKS registry** — `"admissibility": admissibility.check` is added for discoverability
(`--checks` argument listing, `dsx audit`'s `tuple(CHECKS) + ("repro",)`), even though — like
`"design"` today — it is *always* intercepted by a special case in `run_checks` before the
generic `elif name in CHECKS:` branch, because it needs an extra parameter beyond `spec`.

**`run_checks` special case** — D-22's helper lives in `dsx/frame/paradigm.py` (the one file
exempt from the D-11 scanner, `tests/test_frame_boundary.py:145`), and `run_checks` calls it
and passes the plain boolean result into `admissibility.check`, exactly mirroring how
`run_checks` already computes `strict`/`reconcile_trail` before dispatch (`dsx/cli.py:168-169`):

```python
# dsx/frame/paradigm.py — new function, alongside the existing _PARADIGM_CONDITIONAL table
def applies_to_frequentist_admissibility(spec: dict) -> bool:
    """True when DSX-ADM-* should be evaluated against this frame (D-22): the declared
    inference.paradigm is 'frequentist', or no recognised paradigm is declared at all —
    undeclared/unrecognised widens to every paradigm-conditional family, matching
    _check_monitoring_discipline's and check()'s own fallback, so an honest paradigm
    declaration never costs more than silence (D-10)."""
    declared = get(spec, "inference.paradigm")
    paradigm = normalize(declared) if not is_blank(declared) else ""
    return paradigm not in PARADIGMS or paradigm == "frequentist"

# dsx/cli.py::run_checks — new elif branch, alongside the existing ones for "design"/"prereg"/etc.
elif name == "admissibility":
    reports.append(
        admissibility.check(spec, applies_to_frame=paradigm.applies_to_frequentist_admissibility(spec))
    )
```

```python
# dsx/cli.py — import line gains admissibility (alphabetical, matching the existing style)
from .frame import admissibility, interference, paradigm, prereg, val
```

**Hard constraint verified against the actual scanner code** (`tests/test_frame_boundary.py:148-201`):
`dsx/frame/admissibility.py` is **not** in `_PARADIGM_READ_EXCLUDED_FILENAMES` (only
`paradigm.py` is exempt), so its source text must never contain the literal substring
`inference.paradigm` — not in code, not in a comment, not in a docstring — and must never
pass a string literal beginning `inference.` as a call argument, and must never subscript
`spec["inference"]["paradigm"]`. The `applies_to_frame: bool` parameter name (a plain
boolean, never a paradigm string) is what keeps `admissibility.py` compliant; **the module
must not even explain D-22 in its own docstring using the word "paradigm" combined with a
literal `inference.` prefix** — describe the parameter in terms of "frequentist scoping" or
"whether this check applies," never by naming the dotted path.

## gen-finding-catalogue.py Changes

Read in full: `scripts/gen-finding-catalogue.py:1-326`.

Two **separate, complementary** mechanisms are needed (REQ-P11-06 conflates them in its
one-sentence description, but the actual script has two distinct code paths, verified by
reading `check_d05()` in full):

1. **`_D05_ALLOWLIST_PREFIXES` gains `"DSX-ADM-"`** (D-25, one-line change at
   `scripts/gen-finding-catalogue.py:68`). This activates the **existing** `check_d05()`
   mechanism (`:260-290`) for `dsx/frame/admissibility.py`'s own two `report.add(...)` call
   sites — it enforces that the docstrings enclosing `report.add("DSX-ADM-010", ...)` and
   `report.add("DSX-ADM-020", ...)` each contain a `Citation:` line, a
   `Reference value:`/`Structural criterion:` line, and that a `# D-05: DSX-ADM-010` /
   `# D-05: DSX-ADM-020` comment marker exists somewhere under `tests/`. This mechanism needs
   **no new code** — only the allowlist edit — because `check_d05()` already walks every
   `*.py` under `dsx/` via `collect()` -> `extract()` (`:101-117`, AST-based, already covers
   `dsx/frame/admissibility.py` once it exists).

2. **A new sibling function enforces citations *inside the YAML data itself*** (D-23/D-24) —
   this is what REQ-P11-06's "each family carries a primary-source citation" is actually
   about, and it is a capability `check_d05()` genuinely does not have: `check_d05()` only
   ever reads `ast.walk()`-extracted `report.add(...)` call arguments and Python docstrings
   (`:203-242`); it has no file-path parameter for a data file and never does
   `sys.path.insert(0, str(ROOT))` (confirmed: no `sys.path` manipulation exists anywhere in
   the current script), so it cannot `import dsx.loader` at all today.

```python
# scripts/gen-finding-catalogue.py — new sibling function, new sys.path line (D-23)
def check_families_citations(families_path: Path) -> list[str]:
    """D-24 build-time enforcement: every references/families.yaml family entry must carry
    a non-blank citation. Distinct from check_d05() (D-23): that function only ever reads
    ast.walk()-extracted report.add(...) call sites and Python docstrings under dsx/, has no
    file-path parameter for a data file, and the script never does
    sys.path.insert(0, str(ROOT)) — it cannot import dsx.loader today. This function is what
    gives that capability, scoped to the one data file it needs to read."""
    problems: list[str] = []
    if not families_path.exists():
        return [f"{families_path}: not found"]
    sys.path.insert(0, str(ROOT))  # enables `import dsx.loader` — the script has never done this before
    from dsx.loader import SpecParseError, load

    try:
        data = load(families_path)
    except SpecParseError as exc:
        return [f"{families_path}: {exc}"]

    families = data.get("families") if isinstance(data, dict) else None
    if not isinstance(families, list):
        return [f"{families_path}: no top-level 'families' block sequence found"]

    for entry in families:
        if not isinstance(entry, dict):
            continue
        fid = entry.get("id", "<unknown>")
        citation = entry.get("citation")
        if not citation or not str(citation).strip():
            problems.append(f"families.yaml entry {fid!r}: missing or blank citation")
    return problems
```

Wired into `main()`'s `--check` branch alongside the existing `check_d05(...)` call
(`scripts/gen-finding-catalogue.py:312-316`), reported with a `"D-24:"` prefix (distinct from
the existing `"D-05:"` prefix) to disambiguate the two mechanisms in CI output:

```python
family_problems = check_families_citations(ROOT / "references" / "families.yaml")
for problem in family_problems:
    print(f"D-24: {problem}", file=sys.stderr)
if family_problems:
    exit_code = 1
```

**The run-time half of D-24** ("the adjudicator drops uncited families at load and refuses to
rank them") is `dsx/frame/admissibility.py`'s own responsibility, not this script's — the
loader that reads `families.yaml` inside `admissibility.py` should filter out (or raise on,
per the plan's choice) any entry with a blank `citation`, independent of whether the
build-time gate above has already caught it, so a manually-edited or corrupted file cannot
silently rank an uncited family even if `--check` was skipped.

## Which Existing Tests Go Red

Verified by reading the actual test files, not inferred:

1. **`tests/test_known_bad_corpus.py`** — `_TARGET_DEFECT_CODES` (`:96-131`) currently maps
   `post-hoc-procedure-switch` to `{"verify": "DSX-PRE-030"}` only. Once `admissibility` joins
   `GATE_PROFILES["plan"]`, this fixture's `dsx gate plan` exit code depends entirely on
   whether `validity_frame.estimand.type` was populated on it (see "Consequence the planner
   must action" above). **If left unpopulated, this test's plan-gate assertion for this
   fixture goes red** and the map needs a new `"plan": "DSX-ADM-020"` entry — a change
   unrelated to the fixture's actual purpose, and the sign that the axis wasn't populated
   everywhere it needed to be.
2. **`tests/test_known_bad_corpus.py::test_good_fixture_passes_every_gate`** (`:1390-1391`)
   and the sibling `test_bad_fixture_blocks_at_plan`/`test_bad_fixture_blocks_at_ship`
   (`:1396-1402`) — both **must** stay green (this is the "two exit-code tests stay
   unchanged" standing deliverable). This is the direct verification target for the ranking
   design in this research: the good fixture's declared `two_proportion_z` under
   `dependence: clustered` must resolve to the *top-ranked* candidate in whatever family set
   the plan ships, or `DSX-ADM-010` (HIGH) will newly fire and this test breaks at the `ship`
   threshold.
3. **`tests/test_dsx.py`** — the `GATE_PROFILES`/`CHECKS` structural assertions around line
   1617-1686 (`from dsx.cli import CHECKS, GATE_PROFILES`, iterating `GATE_PROFILES.items()`,
   and `set().union(*GATE_PROFILES.values())` reachability checks) will need `"admissibility"`
   accounted for — these tests are written generically enough (iterating the live dicts) that
   most should extend automatically, but any test asserting an exact `len(GATE_PROFILES["plan"])`
   or an exact `len(CHECKS)` will need updating.
4. **`tests/test_frame_boundary.py`** — both `TestFrameImportBoundary` (D-03a) and
   `TestFrameParadigmReadBoundary` (D-11) scan `FRAME_DIR.rglob("*.py")` generically, so
   `dsx/frame/admissibility.py` is automatically swept into both scanners the moment the file
   exists — no test edit needed there, but the module's own source **must** pass both scans
   the first time (see the hard constraint on the `applies_to_frame` parameter above); a
   naive first draft that reads `inference.paradigm` directly (rather than receiving the
   pre-computed bool) will fail `TestFrameParadigmReadBoundary` immediately.
5. **`tests/test_gen_finding_catalogue.py`** — exists and presumably exercises `check_d05()`
   and the allowlist constants directly; the new `check_families_citations()` function and
   the `_D05_ALLOWLIST_PREFIXES` addition should get dedicated new test cases here (not
   inferred from existing tests — this file was not read in full in this session; the planner
   should read it before writing new tests to match its existing style).
6. **The finding catalogue itself** (`references/finding-codes.md`) goes stale the moment
   `DSX-ADM-010`/`DSX-ADM-020` exist in code — `scripts/gen-finding-catalogue.py --write` must
   be re-run as part of this phase's own deliverables (this is standard practice every prior
   phase in this milestone has followed, not new to Phase 11).

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| YAML parsing for `families.yaml` | A second parser, even a "simpler" one scoped to this one file | `dsx.loader.load()` | REQ-P11-01 explicitly forbids a new parser; the two-parser hazard (D-08) is already solved once, centrally — a second parser reopens it |
| Fuzzy/nearest-match alias resolution | Levenshtein distance, substring containment, or any "did you mean" heuristic on procedure names | Exact `normalize()` + closed alias-table lookup | D-18 explicitly forbids this; it is also the exact failure mode `DSX-VAL-020`'s own docstring names as a known, accepted risk elsewhere in this codebase (naming inconsistency looking like a defect) — importing that same ambiguity into an alias table would compound it |
| A scoring function for ranking admissible procedures | Any numeric weight/score combining "number of assumptions," "power," "citation count," etc. | The rule table (D-12: named pairwise orderings + Manski's Law structural fallback + lexicographic tiebreak) | D-12 states directly that classical testing theory rules out a total order for two-sided/composite alternatives — a scoring function would assert a false total order where none exists |
| A new estimator-assumption taxonomy from first principles | Any de novo classification of "what assumptions does test X make" | The six cited source clusters (D-11) plus the explicit `vocabulary_is_not_exhaustive: true` disclosure | Research already established, negatively, that no published taxonomy of estimator assumptions exists (STATO, OBO Foundry both checked and found lacking) — assembling one silently, without the disclosure, would misrepresent project-defined judgment as settled science, exactly the failure mode D-05 exists to prevent |

**Key insight:** every "don't hand-roll" item above already has a documented precedent
elsewhere in this codebase (`_MISSINGNESS_METHOD_VALIDITY` in `dsx/frame/val.py:187-198` is
explicitly disclosed as project-assembled, not a printed table; `_PARAMETER_SCALE_CONSTRAINT_SOURCES`
in the same file is explicitly disclosed as a project-defined partition). Phase 11's job is to
follow that established honesty convention for the admissibility ranking, not invent a new one.

## Common Pitfalls

### Pitfall 1: Populating the estimand axis on the good fixture only
**What goes wrong:** `DSX-ADM-020` (CRITICAL) newly fires at `plan` on known-bad corpus
fixtures whose target defect was never meant to block `plan` (verified concretely for
`post-hoc-procedure-switch` in this research).
**Why it happens:** `_VALIDITY_FRAME_ALWAYS_REQUIRED` doesn't cover the new optional field, so
it is easy to treat "extend the good fixture" as sufficient, following the pattern of simpler
prior-phase field additions that genuinely only touched the good fixture.
**How to avoid:** populate `validity_frame.estimand.type` on all nine committed specs in the
same plan that introduces the field, and re-run `tests/test_known_bad_corpus.py` before
considering the plan complete.
**Warning signs:** any known-bad fixture's `dsx gate plan` exit code changes from what
`_TARGET_DEFECT_CODES` currently documents.

### Pitfall 2: `DSX-ADM-010` firing unconditionally whenever ranking succeeds
**What goes wrong:** the good fixture (`two_proportion_z` under `clustered` dependence)
blocks `ship` for the first time, breaking the standing "good fixture passes every gate at
every threshold" invariant.
**Why it happens:** it is tempting to make `DSX-ADM-010` an "informational ranking report"
that always fires once a ranking is computed (mirroring `DSX-PAR-001`'s always-fires
pattern) — but `DSX-PAR-001` is INFO severity (never blocks anything, by construction);
`DSX-ADM-010` is HIGH (blocks at verify/ship) per D-19, so the same always-fires pattern
produces a different, blocking outcome.
**How to avoid:** scope `DSX-ADM-010` to "declared procedure is admissible but not
top-ranked" (see Ranking Algorithm above), and verify the good fixture's declared procedure
actually IS top-ranked for whatever family set the plan ships.
**Warning signs:** the good fixture's ship-gate exit code changes.

### Pitfall 3: Wiring the alias table into `dsx/checks/stats.py` or `dsx/frame/prereg.py`
**What goes wrong:** `DSX-STA-041`'s and `DSX-PRE-030`'s existing firing sets on the known-bad
corpus change, silently invalidating suppressions operators have already written against the
current behavior (this is D-03's own stated rationale, restated here because it is the single
easiest boundary to accidentally cross while implementing REQ-P11-02, since the natural
instinct once an alias table exists is to make everything that compares procedure names use
it).
**Why it happens:** `post-hoc-procedure-switch` is a very tempting fixture to "fix" once
aliases exist — its declared/executed mismatch (`two_proportion_z` vs `fishers_exact`) looks
like exactly the kind of thing an alias table should reconcile.
**How to avoid:** the alias table has exactly one consumer, `dsx/frame/admissibility.py`
(D-03) — do not import it from, or duplicate its logic into, `dsx/checks/stats.py` or
`dsx/frame/prereg.py` in this phase.
**Warning signs:** any diff touching `dsx/checks/stats.py` or `dsx/frame/prereg.py` in this
phase's plans.

### Pitfall 4: `#` inside a `notes:` field silently diverging between parsers
**What goes wrong:** a citation page range like `34 #1` or a note containing an inline `#`
comment-like character parses differently under PyYAML (preserves it inside a quoted or
block-scalar string) vs. the bundled parser (`_strip_comment` truncates at a
space-preceded `#` even inside what looks like a scalar, per D-08's own named hazard).
**Why it happens:** this bites hardest inside `|`/`>` block scalars specifically — but even a
single-line scalar containing ` #` unescaped could be affected if the schema ever allows
unquoted scalars for free-text fields.
**How to avoid:** every free-text field in `families.yaml` (`notes:`, `citation:`) must be a
**double-quoted** single-line scalar (verified safe in this research's worked example — the
double-quoted `"...2022 Correction DOI 10.5334/irsp.661"` and similar values round-tripped
identically on both parser paths). Never use `|`/`>` for any field in this file, per D-06.
**Warning signs:** the D-08 dual-parser test (which the plan must write) failing only on
CI/dev machines that differ in whether PyYAML is installed.

## Code Examples

### Verified parser round-trip (executed in this research session)

```python
# Verified in this session: both loader paths agree byte-for-byte on the schema above.
import sys
sys.path.insert(0, "/path/to/gsd-dsx")
from dsx import loader

data_pyyaml = loader.load("references/families.yaml")   # loader._pyyaml is not None
loader._pyyaml = None
data_bundled = loader.load("references/families.yaml")  # forces the bundled parser
assert data_pyyaml == data_bundled  # PASSED for the 3-family, 3-token worked example above
```

### Existing pure/wrapper split this phase should reuse (`dsx/checks/stats.py:32-134` / `:405-487`)

```python
# The precedent for admissible_families() (pure) vs. check() (Report-emitting):
def recommend_test(outcome_type, n_groups, paired=False, ...) -> dict[str, object]:
    """Pure and total — every input combination yields a recommendation. No Report,
    no findings, no side effects."""
    ...

def _check_declared_test(analysis: dict, spec: dict, report: Report) -> None:
    """Calls recommend_test() internally, then translates the comparison into
    report.add(...) findings. This is the ONLY function that touches Report."""
    recommendation = recommend_test(...)
    ...
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|---------------|--------|
| Fisher's exact test as the default small-cell-count fallback for two-proportion comparisons | Boschloo's unconditional exact test uniformly dominates Fisher's exact in power (Lydersen, Fagerland & Laake 2009 §9) | Documented since 2009; `references/test-selection.md` in this repository still carries the old, uncited recommendation (D-27's named live defect) | The ranking table this phase ships is the mechanism that finally corrects a documented-but-uncorrected internal defect, not merely a new feature |
| Treating CV1 (the classic cluster-robust variance estimator) as sufficient whenever clustering is declared | CV3/the restricted wild cluster bootstrap is more reliable, especially with few treated clusters (MacKinnon, Nielsen & Webb 2023 §9) | 2023, explicitly hedged by the authors themselves | This ordering (D-13's third) is a *reliability* ordering, not a strict domination — the ranking rule table (not a scoring function) is specifically designed to represent this kind of conditional, hedged preference rather than flattening it into a single number |
| Reporting an unadjusted difference-in-means from an experiment | Regression adjustment interacted with treatment ("cannot hurt," Lin 2013) is weakly preferred, provided the interaction term is included (Freedman 2008 names why the interaction is not optional) | 2013 (Lin), building on Freedman's 2008 critique | The fourth citable ordering; the ranking rule table must encode "interacted, not just adjusted" as the actual condition, not merely "adjusted vs. unadjusted" |

**Deprecated/outdated:**
- Pre-testing for equal variance before choosing between Student's and Welch's t-test:
  Zimmerman (2004) is cited in this research's worked example specifically to back the
  `no_variance_pretesting` assumption token — the practice of testing-then-choosing is a
  documented source of inflated Type-I error, not a neutral convenience.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `families.yaml`'s top level may safely have more than one key (a header scalar plus two block-sequence keys) without violating D-06's "one key holds a block sequence of flat mappings" wording | Families.yaml Schema | If the stricter single-top-level-key reading is intended, the schema needs restructuring (nesting `assumption_vocabulary` and the header flag under the same key as `families`) before the D-08 dual-parser test is written — low cost to fix if caught at plan review, since it was verified only against one candidate schema, not against every schema the wording could support |
| A2 | `inference.primary_procedure` (not `analysis.test`) is the correct field for alias resolution to read as "the declared procedure" | Alias Resolution Algorithm | If `analysis.test` is intended instead, the algorithm needs to read a different field — a low-risk assumption because it follows directly from D-03's own text distinguishing "declared" from "executed," and `inference.primary_procedure` is literally named "primary procedure" |
| A3 | `DSX-ADM-010` fires only when the declared procedure is admissible-but-not-top-ranked, not whenever ranking succeeds | Ranking Algorithm | If wrong, the good fixture's ship-gate exit code likely regresses (verified this is the failure mode to watch for); this is a design recommendation derived from the standing "good fixture always passes" invariant, not a fact read directly from CONTEXT.md |
| A4 | The recommended 12-family roster's exact `estimand`/`dependence` pairings (e.g., `two_proportion_z_cluster_robust` as a distinct family from `two_proportion_z`) are statistically coherent labels, not verified against a named external source for that specific combination | Which 10-14 Families | CONTEXT.md explicitly reserves this to planner discretion; if the planner picks different axis values, the fixture-traceability table should be re-derived against the final choices, not assumed to still hold |

## Open Questions

1. **Does `families.yaml`'s top level need to be literally one key, or is the
   three-key structure (header flag + two block sequences) verified in this research
   acceptable?**
   - What we know: both readings satisfy `dsx.loader.load()`'s bare requirement (top level is
     a mapping) and both were tested to parse cleanly; only the three-key version was actually
     executed against both parser paths in this session.
   - What's unclear: D-06's exact intended scope for "one key."
   - Recommendation: confirm with the user/planner before finalizing; if the answer is "must
     be one key," nest `assumption_vocabulary` and `vocabulary_is_not_exhaustive` under the
     same top-level key as `families` (e.g., one `ontology:` mapping containing all three as
     sub-keys) and re-run the round-trip verification against that revised shape.

2. **Should `DSX-ADM-010`'s "not top-ranked" case distinguish "admissible but dominated by a
   D-13 citable ordering" from "admissible but ranked lower only by the D-14 Manski
   fallback"?**
   - What we know: D-12 requires the message to name "which rule fired and what condition it
     depends on" — this is satisfiable either way.
   - What's unclear: whether the finding's severity or remedy text should differ between a
     hard citable domination (e.g., Boschloo over Fisher's) and the softer "fewer assumptions
     charged" structural fallback.
   - Recommendation: treat both as the same HIGH severity (D-19 fixes exactly two codes; a
     severity split would need a third code, which D-19 does not authorize) but let the
     `detail` text name which of the two mechanisms produced the ranking, since the finding's
     `data` payload is free-form beyond the fixed code/severity/title.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3 | Everything in this phase | Yes (this session ran it directly) | 3.14 (dev machine; repo targets 3.9+ per `from __future__ import annotations` usage) | n/a |
| PyYAML | One of `dsx.loader.load()`'s two parser paths | Yes — installed in this session (`pip install pyyaml`, resolved to 6.0.3) | 6.0.3 | The bundled parser (`dsx/loader.py::_parse_yaml_subset`) — already the existing fallback, unchanged by this phase |
| `python3 -m unittest discover -s tests -v` | Running the existing 549+ test suite before/after this phase's changes | Not executed in this research session (research does not modify code) | n/a | n/a |

**Missing dependencies with no fallback:** none.
**Missing dependencies with fallback:** none — PyYAML was actually installed and verified in
this session; the fallback path (bundled parser) was also directly exercised via
monkeypatching, not merely assumed.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | `unittest` (stdlib), run via `python3 -m unittest discover -s tests -v` |
| Config file | none — no `pytest.ini`/`pyproject.toml` test config found in the repository root |
| Quick run command | `python3 -m unittest tests.test_frame_boundary -v` (fast, targets the two boundary scanners this phase's new module must pass) |
| Full suite command | `python3 -m unittest discover -s tests -v` (README documents ~549 tests as of the last phase; count will grow) |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| REQ-P11-01 | `families.yaml` parses identically via both loader paths | unit | `python3 -m unittest tests.test_families_yaml -v` (new file) | ❌ Wave 0 |
| REQ-P11-01 | Every family entry traces to a fixture (SC5) | integration | new test asserting each family `id` is exercised by at least one committed spec's resolved `(estimand.type, dependence.structure)` + `inference.primary_procedure` alias | ❌ Wave 0 |
| REQ-P11-02 | Alias resolution is exact-match, never fuzzy | unit | new test asserting an unrecognised alias string does not resolve via any distance/substring heuristic | ❌ Wave 0 |
| REQ-P11-03 | Ranked admissible set names assumptions bought/charged | unit | new test on `admissible_families()`'s return shape | ❌ Wave 0 |
| REQ-P11-04 | Underdetermined frame -> `no_admissible_procedure`, exit 1 at CRITICAL | integration | new test constructing a spec with blank `estimand.type` and asserting `DSX-ADM-020` + exit 1 at `plan` | ❌ Wave 0 |
| REQ-P11-05 | `cmd_recommend` output is additive, not replacing | integration | new test: `dsx recommend-test proportion --groups 2` (no `--spec`) produces byte-identical output to v1.5.0's recorded shape | ❌ Wave 0 |
| REQ-P11-06 | Uncited family fails the build check | unit | `python3 -m unittest tests.test_gen_finding_catalogue -v` (extend existing file) | Existing file, new cases needed |
| (regression) | Good fixture passes every gate; bad fixture blocks every gate | regression | `python3 -m unittest tests.test_known_bad_corpus -v` | Existing file |
| (regression) | D-03a/D-11 boundary scanners pass against the new module | regression | `python3 -m unittest tests.test_frame_boundary -v` | Existing file |

### Sampling Rate
- **Per task commit:** `python3 -m unittest tests.test_frame_boundary -v` (cheapest, catches
  the two hardest-to-debug failure modes — a stray `dsx.checks` import or a stray
  `inference.paradigm` read — immediately)
- **Per wave merge:** `python3 -m unittest discover -s tests -v` (full suite)
- **Phase gate:** Full suite green before `/gsd-verify-work`, plus
  `python3 scripts/gen-finding-catalogue.py --check` green (both the existing D-05 mechanism
  and the new D-24 families-citation mechanism)

### Wave 0 Gaps
- [ ] `tests/test_families_yaml.py` — new file: schema round-trip (D-08), citation presence
      (D-24 run-time half), alias uniqueness within `(estimand, dependence)` pairs
- [ ] New test cases inside `tests/test_dsx.py` or a new `tests/test_frame_admissibility.py`
      — `admissible_families()` pure-function behavior, `check()`'s `DSX-ADM-010`/`-020`
      emission, `DecisionRecord.escalate` actually set to `True` on the refusal path
- [ ] `tests/test_gen_finding_catalogue.py` — extend with `check_families_citations()` cases
      (this existing file was not read in full in this session; match its established style)

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | This is a local CLI gate tool with no auth surface; not applicable |
| V3 Session Management | No | No sessions exist in this tool |
| V4 Access Control | No | No multi-user access model |
| V5 Input Validation | Yes | `references/families.yaml` is parsed via the existing `dsx.loader.load()` (already uses `yaml.safe_load`, never `yaml.load`/`yaml.unsafe_load` — confirmed at `dsx/loader.py:64`, no arbitrary object deserialization). The bundled fallback parser is a hand-written recursive-descent parser over a closed grammar subset — already reviewed and hardened in prior phases (D-08's own hazard-avoidance is itself an input-validation control) |
| V6 Cryptography | No new surface | No new cryptographic primitive is introduced; existing `frame_digest()` (SHA-256 over `validity_frame`/`inference` blocks, `dsx/decisions.py:181-190`) is unchanged by this phase and is explicitly documented as change-detection, not a security control |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Regex denial-of-service (ReDoS) via a maliciously crafted `notes:`/`citation:` free-text field matched against a future alias-normalization or search regex | Denial of Service | This codebase has an explicit, documented precedent for this exact concern: `dsx/spec.py:450`'s `_FALSIFIER_NUMBER_RE` comment names threat T-7-03 and uses "bounded, non-nested quantifiers only." Any new regex this phase introduces (there should be none needed — alias matching is exact-string, not regex) must follow the same discipline if one becomes necessary |
| A local user hand-editing `families.yaml` to add an uncited family, bypassing the build-time gate | Tampering / Repudiation | D-24's two-sided enforcement (build-time `--check` gate AND run-time refusal to rank an uncited family inside `admissibility.py` itself) is the mitigation — the run-time half specifically exists so a file that skipped `--check` (e.g., hand-edited post-build) still cannot silently rank an uncited family at gate time |
| A crafted `families.yaml` with deeply nested or pathological structure causing excessive parse time in the bundled fallback parser | Denial of Service | D-06's schema (flat mappings, no nesting beyond one level, no anchors/merge keys) is itself the mitigation — the schema recommended in this research has no recursive or self-referential structure for the bundled parser to choke on |

## Sources

### Primary (HIGH confidence — verified by executing code in this repository during this session)
- `dsx/loader.py` — read in full; both parser paths executed against a worked `families.yaml` example
- `dsx/checks/stats.py` — read in full; `recommend_test()`/`_check_declared_test()` split is the precedent for `admissible_families()`/`check()`
- `dsx/frame/paradigm.py` — read in full; `_PARADIGM_CONDITIONAL`, `_check_monitoring_discipline`'s undeclared-paradigm-widens fallback pattern
- `dsx/frame/val.py` — read in full; frame-module `check(spec) -> Report` convention, `DecisionRecord` emission pattern, project-defined-partition disclosure convention
- `dsx/spec.py` — read in full; `_VOCABULARIES`, `_VALIDITY_FRAME_MEMBERSHIP`, `_validate_validity_frame_shape`'s blank-skips-membership-check behavior
- `dsx/cli.py` — read in full; `CHECKS`, `GATE_PROFILES`, `GATE_THRESHOLDS`, `run_checks`, `cmd_recommend`, `build_parser`
- `dsx/decisions.py` — read in full; `DecisionRecord`/`InvocationHeader` schema, `escalate`/`alternatives_rejected` fields
- `dsx/findings.py` — read in full; `Report`/`Finding`/`Severity`/`emit` contract
- `scripts/gen-finding-catalogue.py` — read in full; `check_d05()`, `_D05_ALLOWLIST_PREFIXES`, `collect()`/`extract()`, confirmed no `sys.path` manipulation exists today
- `tests/test_frame_boundary.py` — read in full; both scanners' exact detection mechanisms
- `tests/test_known_bad_corpus.py` — `_INCIDENTAL_GAP_CODES` and `_TARGET_DEFECT_CODES` sections read directly, confirming `post-hoc-procedure-switch`'s plan-gate pass-through
- `examples/good-ANALYSIS-SPEC.yaml`, `examples/bad-ANALYSIS-SPEC.yaml`, all six
  `examples/known-bad/*.yaml` fixtures, `templates/ANALYSIS-SPEC.yaml` — grepped and/or read
  in full for declared procedure, dependence structure, and `analysis:`/`model:` block presence

### Secondary (MEDIUM confidence)
- `11-CONTEXT.md`'s citation spine (D-11, D-13, D-26-D-29) — taken as given per the phase's
  own binding-input status; not independently re-verified against the named papers in this
  session (that verification was already performed during `/gsd-discuss-phase` per
  `11-CONTEXT.md`'s own text)

### Tertiary (LOW confidence — flagged in the Assumptions Log above)
- The exact top-level key count reading of D-06 (A1)
- The choice of `inference.primary_procedure` over `analysis.test` for alias resolution (A2)
- The `DSX-ADM-010` "not top-ranked" semantics (A3)
- The specific 12-family roster's axis-value coherence (A4)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new dependency; the one optional dependency touched (PyYAML) was
  actually installed and both loader paths were actually executed in this session
- Architecture (call sites, composition, catalogue script): HIGH — every recommendation cites
  exact file:line locations read in full during this session, and the `run_checks`/`cmd_recommend`
  changes follow existing, already-shipped precedents in the same files
- Estimand axis: MEDIUM — the recommendation is backed by a concrete, demonstrated
  traceability failure of the alternative (not merely a preference), but it is still a design
  choice CONTEXT.md explicitly left open, not a fact
- Family roster: MEDIUM — sized and evidenced against the actual corpus, but CONTEXT.md
  explicitly reserves the final list to planner discretion

**Research date:** 2026-08-20
**Valid until:** 30 days (stable, in-repository research — the underlying code does not
change on its own; re-verify if any of Phases 6-10's shipped modules are touched by an
intervening hotfix before Phase 11 executes)
