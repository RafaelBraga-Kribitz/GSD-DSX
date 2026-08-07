# Architecture Research: DSX Validity Frame Integration

**Domain:** Extending an existing deterministic gate package (`gsd-dsx`) with a new
cross-cutting check subsystem
**Researched:** 2026-08-07
**Confidence:** HIGH — every claim below was checked against the current source
(`dsx/cli.py`, `dsx/checks/__init__.py`, `dsx/findings.py`, `dsx/spec.py`,
`dsx/checks/design.py`, `dsx/suppressions.py`, `dsx/loader.py`,
`examples/good-ANALYSIS-SPEC.yaml`, `examples/bad-ANALYSIS-SPEC.yaml`,
`tests/test_dsx.py`, `capabilities/dsx/capability.json`), not assumed from the brief.

---

## 1. Verified facts about the existing architecture

These are read from code, not restated from the brief, because everything downstream
depends on them being right:

- `dsx/checks/` is a flat package of modules, each exposing `check(spec, **kwargs) -> Report`
  and owning one or more code prefixes (`dsx/checks/__init__.py` docstring is the
  authoritative map — e.g. `design.py` owns `DSX-EXP-*` **and** `DSX-CAU-*`).
- The **only** shared primitives every check module imports are from two peer modules,
  neither of which is `dsx/checks/`: `dsx/findings.py` (`Report`, `Finding`, `Severity`)
  and `dsx/spec.py` (`get`, `section`, `items`, `is_blank`, `as_number`, `normalize`,
  plus the closed-vocabulary constants). `dsx/checks/design.py` imports
  `IDENTIFICATION_STRATEGIES` straight out of `dsx/spec.py`, for example.
- `dsx/spec.py` owns two things: every closed vocabulary (`PEEKING_POLICIES`,
  `VARIANCE_ADJUSTMENTS`, `IDENTIFICATION_STRATEGIES`, …) and `validate_structure()`,
  which does **shape/vocabulary** validation under `DSX-SPEC-*`. Semantic,
  cross-field, sometimes-computed validation lives in `dsx/checks/*.py` under each
  family's own prefix. `design.py`'s `_check_units`/`_check_identification` is the
  worked example of this split: `spec.py` checks that `design.identification` is a
  member of `IDENTIFICATION_STRATEGIES` (`DSX-SPEC-041`); `design.py` checks whether
  the *right* strategy was declared for the question type (`DSX-CAU-010/011`).
- `dsx/cli.py` is the only place that wires check modules to loop points. Two
  dictionaries do all the work: `CHECKS` (name → `check` callable, consumed by
  `dsx check`/`dsx audit`) and `GATE_PROFILES` (loop point → tuple of `CHECKS` keys,
  consumed by `dsx gate`). `run_checks()` has an explicit dispatch table for check
  functions that need extra keyword arguments (`strict`, `gate_point`, `root`); any
  check function with only `check(spec)` falls through to the generic
  `CHECKS[name](spec)` branch.
- `GATE_THRESHOLDS = {"plan": CRITICAL, "execute": CRITICAL, "verify": HIGH, "ship": HIGH}`.
  Crucially, `GATE_PROFILES` controls **which checks run**; `GATE_THRESHOLDS` controls
  **which findings block the exit code**, independently. A HIGH finding from a check
  that runs at `plan` is fully computed and printed at `plan`, it simply cannot flip
  the exit code to 1 there (`Report.blocks()` only counts findings `>= threshold`).
  This is the mechanism the whole severity design in §3 below leans on.
- `Severity.INFO` (value 10) exists in the ladder today but **no check in the
  repository currently emits it** (verified by grep — the only two hits for `INFO`
  in `dsx/` are the enum member itself and a label list in `Report.render()`).
  `DSX-PAR-001` will be the first real consumer.
- `Report.context` is already a free-form `dict[str, Any]` used as a side channel
  for non-finding data (`report.context["srm"]`, `report.context["suppressions_applied"]`).
  `merge()` folds each sub-report's context under `merged.context[sub.check]`, i.e.
  contexts nest by check name rather than flattening.
- `apply_suppressions()` / `known_codes()` discover valid `DSX-*` codes by
  AST-walking every `.py` file under `dsx/` for `<report>.add("DSX-...", ...)` calls
  (plus a regex pass over `metrics.py`'s SQL rule tuples). **Any new package under
  `dsx/` is automatically covered** — no registration step is needed for
  suppressions to recognise new codes, provided findings are still emitted via
  `report.add(...)`.
- D-08's regression fixtures are enforced by exactly two tests today
  (`tests/test_dsx.py::TestCLI.test_good_fixture_passes_every_gate` and
  `test_bad_fixture_blocks_at_plan` / `test_bad_fixture_blocks_at_ship`), each
  running `dsx gate <point> --spec <fixture>` through the real CLI and asserting the
  exit code. They do not enumerate which checks ran — the invariant is exit-code
  level, which is exactly why it stays testable as new families are added: the two
  tests never need to change, only the fixture *content* grows.

---

## 2. Module boundary (D-03a) and file layout

### The apparent tension, resolved

D-03a reads as if it forbids `dsx/frame/` from reading anything outside its own
block. It does not — it forbids **calling into `dsx/checks/*.py` implementation
code**. Every existing check already free-reads *any* top-level spec section it
needs (`design.py` reads `spec['results']` and `spec['decision']`, not just
`spec['design']`), because a check's contract is `check(spec) -> Report`, not
`check(spec['design']) -> Report`. The two "cross-cutting" examples in the prompt
are not actually cross-package dependencies:

- **Procedure admissibility** (`DSX-ADM-*`) needs `validity_frame` (dependence
  structure, identification strength) and `inference` (`primary_procedure`,
  `paradigm`). Both are top-level keys on the same `spec` dict, filled in the same
  `ANALYSIS-SPEC.yaml` at the same planning step. `dsx/frame/admissibility.py`
  reads `section(spec, "validity_frame")` and `section(spec, "inference")` directly
  — zero import from `dsx/checks/`.
- **Unit reconciliation** (`DSX-VAL-020`) needs `validity_frame.units` and, for the
  cross-block consistency variant (§4.1), `design.randomization_unit`. Again, both
  are top-level `spec` keys. `dsx/frame/val.py` reads `section(spec, "design")`
  directly — it does not call `dsx.checks.design.check()` or import any function
  from that module.

So the rule that keeps the boundary real is simpler than "never read outside your
block": **`dsx/frame/*.py` may read any part of the raw `spec` dict and may import
`dsx/findings.py`, `dsx/spec.py`, and `dsx/loader.py` (all peer infrastructure, not
`dsx/checks/`) and, once it exists, `references/families.yaml` as data. It must
never `import` a name out of `dsx.checks.*`.** `dsx/checks/*.py` is symmetrically
never allowed to import `dsx.frame.*` either — the only place the two packages meet
is `dsx/cli.py`, which imports both and wires them into `CHECKS`/`GATE_PROFILES`.
That keeps the dependency graph a strict DAG with `cli.py` at the top:

```
dsx/cli.py
   │  imports both, wires CHECKS / GATE_PROFILES
   ├──> dsx/checks/*.py  ──┐
   └──> dsx/frame/*.py  ───┤
                            ├──> dsx/findings.py   (Report, Finding, Severity)
                            ├──> dsx/spec.py       (vocab constants, get/section/items/…)
                            ├──> dsx/loader.py     (load() — generic YAML-subset loader)
                            └──> dsx/decisions.py  (NEW — DecisionRecord, see §5)
```

No arrow points from `dsx/findings.py`, `dsx/spec.py`, `dsx/loader.py`, or
`dsx/decisions.py` back up to either `checks/` or `frame/`. If in six months there
are genuinely zero `frame → checks` imports (there is no code reason there ever
should be one), `dsx/frame/` extracts cleanly with `git filter-repo`, exactly as
D-03a's rationale requires.

### Concrete file layout

```
dsx/
  cli.py                  # EXTENDED: CHECKS dict + GATE_PROFILES gain new keys (§3);
                           #   new `explain` subcommand (§5); GATE_THRESHOLDS unchanged.
  findings.py              # UNCHANGED. Severity.INFO already exists; DSX-PAR-001 is
                           #   its first real user (§6). No dataclass changes needed.
  spec.py                  # EXTENDED: new closed vocabularies for validity_frame/
                           #   inference fields (dependence.structure, interference.risk,
                           #   interference.mitigation, missingness.mechanism,
                           #   identification.strength/constraint_source, paradigm,
                           #   paradigm_justification); PEEKING_POLICIES gains one member
                           #   (§4.3); new _validate_validity_frame_shape() /
                           #   _validate_inference_shape() under DSX-SPEC-08x, following
                           #   the exact pattern _validate_design_shape() already uses.
  decisions.py              # NEW peer module (M1). DecisionRecord dataclass + accumulator
                           #   + JSONL writer. Peer to findings.py/spec.py — importable
                           #   from both checks/ and frame/ without creating a
                           #   checks<->frame edge. See §5.
  loader.py, mathx.py, profiler.py, suppressions.py, __init__.py, __main__.py
                           # UNCHANGED. loader.load() is generic (`Path -> dict`), so
                           #   dsx/frame/admissibility.py reuses it verbatim to read
                           #   references/families.yaml — no new loader needed.
  checks/                  # UNCHANGED package boundary; existing modules untouched
                           #   except where §4 calls out a specific reconciliation edit.
    __init__.py
    design.py              # DSX-EXP-*, DSX-CAU-* — DSX-EXP-020/021 logic untouched (§4.1)
    metrics.py, stats.py, ml.py, claims.py, viz.py, coherence.py, dq.py, smells.py,
    figures.py, narrative.py, code.py, decision.py   # unchanged
  frame/                   # NEW package. D-03a boundary lives here.
    __init__.py             # M1. Mirrors dsx/checks/__init__.py: docstring mapping
                           #   family -> prefix -> milestone, imports the modules that
                           #   exist so far, __all__. Grows one entry per milestone;
                           #   never pre-imports a module before its milestone ships.
    paradigm.py             # M1: DSX-PAR-001 (manifest, INFO, §6).
                           # M2c: DSX-PAR-002 (paradigm_justification vocab),
                           #      DSX-PAR-010/011 (symmetric monitoring pair, §4.3).
    val.py                  # M2a: DSX-VAL-* — estimand, unit triad, dependence vs
                           #   method family, identification vs constraint (040/041),
                           #   sampling frame vs claims, missingness, measurement.
    interference.py          # M2b: DSX-INT-* — SUTVA/interference, triggering/dilution,
                           #   novelty/primacy stability.
    prereg.py               # M3: DSX-PRE-* — fallback-rule DSL, declared_at
                           #   provenance, declared-branch-vs-executed-branch
                           #   reconciliation against results.tests.
    admissibility.py         # M4: DSX-ADM-* — reads references/families.yaml (data,
                           #   loaded via dsx.loader.load(), never hand-parsed here),
                           #   admissibility function, ranking, no_admissible_procedure
                           #   -> escalate branch. Extends `dsx recommend-test`.
references/
  finding-codes.md          # EXTENDED every milestone, as today (generated catalogue).
  families.yaml             # Created in M4 ONLY (brief §6.6 item 2 — do not scaffold
                           #   early; an empty ontology sitting unused for three
                           #   milestones accumulates speculative structure). By the
                           #   same logic, dsx/frame/admissibility.py is not created
                           #   before M4 either — there is nothing for it to do without
                           #   the data file, and an empty check module is the code
                           #   analogue of the empty-ontology anti-pattern.
```

**Trace of the two named cross-cutting checks against this layout**, confirming
neither needs an upward import:

| Check | Fields it reads | Where each field lives | Import needed from `dsx/checks/`? |
|---|---|---|---|
| `DSX-ADM-*` admissibility | `validity_frame.dependence.structure`, `validity_frame.estimand`, `inference.primary_procedure`, `inference.paradigm`, `design.kind` | All top-level `spec` keys, read via `section()`/`get()` | No — same pattern `design.py` already uses to read `spec['decision']` |
| `DSX-VAL-020` unit triad | `validity_frame.units.*`, (cross-check variant) `design.randomization_unit`/`design.analysis_unit` | Top-level `spec` keys | No — `frame/val.py` reads `section(spec, "design")` directly, same as any other check reading a foreign section |

---

## 3. Gate profile registration — loop points, severity, rationale

### The threshold mechanic this table exploits

Because `GATE_PROFILES` (which checks run) and `GATE_THRESHOLDS` (what blocks) are
independent, a check can — and for this subsystem, mostly should — **run at every
loop point where its inputs exist**, while its **severity**, not its registration,
decides whether it actually stops the loop at `plan`/`execute` (CRITICAL only) versus
`verify`/`ship` (HIGH or above). This mirrors the existing precedent exactly:
`design.py` (which owns both `DSX-CAU-010` CRITICAL and `DSX-CAU-011` HIGH) is
registered at `plan` for both, and only `DSX-CAU-010` actually blocks planning.

The one real constraint on **registration** (as opposed to severity) is data
availability: a check cannot meaningfully run at a loop point before the field(s)
it reads are expected to be filled in. That is what separates `DSX-PRE-*` (needs an
*executed* branch — cannot exist before results do) from everything else in this
subsystem, which is entirely declaration-based per D-02 and is therefore knowable
the moment `validity_frame:`/`inference:` are written, i.e. at `plan`.

### Registration and severity table

| Family | Codes (examples) | Gate loop points | Severity | Rationale |
|---|---|---|---|---|
| `DSX-PAR-*` manifest | `DSX-PAR-001` | plan, execute, verify, ship | **INFO** | Purely informational (D-10); must exist the moment `paradigm` exists (M1), and is cheap enough to run everywhere. INFO can never block regardless of threshold — see §6. |
| `DSX-PAR-*` justification | `DSX-PAR-002` | plan, execute, verify, ship | HIGH | Closed-vocabulary declaration check, same shape as `DSX-SPEC-04x`; not Class-A on its own, but should eventually block if never fixed. Non-blocking at plan/execute (threshold CRITICAL), blocking at verify/ship. |
| `DSX-PAR-*` monitoring pair | `DSX-PAR-010`, `DSX-PAR-011` | plan, execute, verify, ship | **CRITICAL, symmetric** | Both read `design.peeking_policy` + `inference.paradigm` (§4.3) — pure declarations, known before data is touched, so they belong at plan like `DSX-EXP-001`/`DSX-CAU-010`. CRITICAL because uncontrolled continuous monitoring is Class A (unrecoverable without new data) and, per D-12, the two codes must carry **identical** severity — an asymmetric CRITICAL/HIGH split would itself be the kind of silent paradigm-steering D-12 exists to prevent. |
| `DSX-VAL-*` estimand | `DSX-VAL-001` (missing/non-falsifiable estimand) | plan, verify, ship | **CRITICAL** | "No estimand" is the #1 Class-A row in the brief and is fully declaration-checkable at plan. |
| `DSX-VAL-*` unit triad | `DSX-VAL-020` (observation finer than assignment, no dependence handling) | plan, verify, ship | **CRITICAL** | New defect class EXP-021 cannot see (no `observation` concept exists in `design:`); pseudo-replication is Class A; purely declarative. |
| `DSX-VAL-*` cross-block consistency | `DSX-VAL-021` (units disagree with `design.randomization_unit`/`analysis_unit`) | plan, verify, ship | HIGH | Spec-hygiene / drift-between-blocks defect, not itself a statistical catastrophe — see §4.1. |
| `DSX-VAL-*` dependence | `DSX-VAL-030` (structure declared, no method family) | plan, verify, ship | **CRITICAL** | "Dependence ignored" Class-A row; purely declarative given `validity_frame.dependence`. |
| `DSX-VAL-*` identification vs constraint | `DSX-VAL-040` (weak + no constraint) | plan, verify, ship | **CRITICAL** | Explicitly bolded Class-A row ("weak identification treated as strong"); declarative. |
| | `DSX-VAL-041` (strong + constraint carrying parameter-scale info) | plan, verify, ship | HIGH | Brief's own language is a softer signal ("the constraint *may* be doing the work") — worth surfacing, not worth stopping planning over. |
| `DSX-VAL-*` sampling frame | `DSX-VAL-05x` (claim population vs `sampling_frame.claim_population`) | verify, ship only | HIGH | Needs `claims[]`, which is typically not finalized until verify/ship — cannot be checked meaningfully at plan. |
| `DSX-VAL-*` missingness | `DSX-VAL-06x` (MNAR/not_assessed + complete-case, no sensitivity) | plan, verify, ship | **CRITICAL** | Explicit Class-A row; fully declared in `validity_frame.missingness` at plan. |
| `DSX-VAL-*` measurement | `DSX-VAL-07x` (construct/operationalisation gap) | verify, ship only | HIGH | Reinforces existing `DSX-MET-*` (already "Partial" per the brief); not new Class-A ground. |
| `DSX-INT-*` interference/SUTVA | `DSX-INT-010` (risk declared, mitigation=none, no residual_note) | plan, verify, ship | **CRITICAL** | Bolded Class-A row; fully declared in `validity_frame.interference` at plan. |
| `DSX-INT-*` triggering/dilution | `DSX-INT-030` (analysing eligible without `dilution_adjusted`) — code taken verbatim from the brief's own YAML comment, preserved per D-06 | plan, verify, ship | **CRITICAL** | Bolded Class-A row; fully declared in `validity_frame.triggering` at plan. |
| `DSX-INT-*` novelty/primacy | `DSX-INT-04x` (stability not assessed) | verify, ship only | HIGH | Needs comparison evidence (week-over-week) that only exists once results do. |
| `DSX-PRE-*` declared vs executed | `DSX-PRE-*` | **verify, ship only** | **CRITICAL** | Cannot run at plan/execute — there is no executed branch yet to reconcile against. Once results exist, a mismatch is post-hoc specification, a named Class-A row, hence CRITICAL like the existing `DSX-EXP-060` peeking precedent. |
| `DSX-ADM-*` admissibility | `DSX-ADM-020` (`no_admissible_procedure` → escalate) | plan, verify, ship | **CRITICAL** | Structurally identical to `DSX-CAU-010` (identification strategy missing) — an underdetermined frame is the general form of "weak identification treated as strong"; fully declarative once `references/families.yaml` (M4) exists. |
| | `DSX-ADM-010` (procedure admissible but not the top-ranked one) | plan, verify, ship | HIGH | Advisory-strength signal, mirrors `DSX-CAU-011`/`012`. |

None of the new families are registered at `execute` except `DSX-PAR-*`, matching
the existing precedent that `design.py` itself (source of the closest analogous
checks, `DSX-EXP-*`/`DSX-CAU-*`) is absent from the `execute` profile — `execute`
is scoped to environment/leakage/dq/code concerns, not design or frame validity.
`DSX-PAR-*` is the one exception, and only because it is cheap, fully declarative,
and (for `DSX-PAR-001`) can never block regardless of where it runs.

`CHECKS` (in `dsx/cli.py`) gains five new keys — `"val"`, `"interference"`,
`"paradigm"`, `"prereg"`, `"admissibility"` — each added in the milestone that ships
the corresponding module, mapped to that module's `check` function. `run_checks()`'s
explicit dispatch table needs one new branch for `"prereg"` if it takes `gate_point`
(recommended, mirroring `decision.py`'s existing `gate_point` parameter, so a future
milestone can differentiate verify vs ship behaviour without a signature change);
`"val"`, `"interference"`, `"paradigm"` and `"admissibility"` can take `spec` only
and fall through to the generic `CHECKS[name](spec)` branch already in
`run_checks()`.

---

## 4. Existing-check overlap — concrete resolutions

### 4.1 `DSX-EXP-020/021` vs the new `units:` triad (`DSX-VAL-020`)

**Verified:** `design.py::_check_units` fires `DSX-EXP-020` (HIGH) when
`design.randomization_unit`/`design.analysis_unit` aren't both declared, and
`DSX-EXP-021` (CRITICAL) when they're declared, differ, and no
`design.variance_adjustment` is set. This logic is untouched by this milestone.

The brief's own `validity_frame.units` block (§5.1) already coexists with
`design.randomization_unit`/`analysis_unit` in the worked example — both blocks are
kept, per D-03's "extend, don't replace" posture and the fact that `design:` is
existing, shipped contract surface (D-06-adjacent: changing its meaning would be a
breaking change to every spec already using it). Two fields that could encode the
"same" fact (`validity_frame.units.assignment` and `design.randomization_unit`) is a
real risk of silent drift, so the resolution has to do two things: keep the checks
disjoint, and add one narrow check for the drift itself.

Resolution, applying the same "disjoint triggers" principle already established for
**M-01** (`DSX-PAR-010` vs `DSX-EXP-060`):

1. **`DSX-EXP-020`/`DSX-EXP-021` keep their exact existing trigger** — mismatch
   between `design.randomization_unit` and `design.analysis_unit` — untouched.
2. **`DSX-VAL-020` (new, CRITICAL) fires on a defect `DSX-EXP-021` structurally
   cannot see**: `validity_frame.units.observation` finer than
   `validity_frame.units.assignment`, with `validity_frame.dependence.structure`
   absent/`none` or `validity_frame.dependence.method_family_required` blank. There
   is no `observation` concept anywhere in `design:`, so this is not a re-check of
   EXP-021's territory — it is the *new* third rung of the triad the brief
   introduces (observation vs assignment), which the old two-field check has no way
   to express.
3. **`DSX-VAL-021` (new, HIGH) is the drift check**: pure string-equality between
   `validity_frame.units.assignment` and `design.randomization_unit` (and
   `.analysis` vs `.analysis_unit`) when both blocks declare a value. This is not a
   re-implementation of EXP-021's "variance-adjustment missing" judgment — it is a
   data-entry consistency check, catching the case where one block was edited and
   the other wasn't. Severity HIGH (spec hygiene, not itself a Class-A statistical
   failure, though it can mask one) — blocks at verify/ship, not plan.

No finding can double-fire: EXP-021 only ever compares two `design:` fields;
VAL-020 only ever compares two `validity_frame:` fields; VAL-021 is the only check
that crosses the block boundary, and it does pure equality, never re-deriving
EXP-021's "is a correction declared" judgment.

### 4.2 `VARIANCE_ADJUSTMENTS` vs `dependence.method_family_required`

**Recommendation (not yet a recorded decision — flag for an M-06-style entry
alongside M-01…M-05 during planning):** reuse `VARIANCE_ADJUSTMENTS` — do **not**
introduce a second, parallel vocabulary. This generalises the same principle
**M-02** already applied to `stopping_rule` ("one concept, one field... avoids a
permanent consistency check between two vocabularies for the same thing"): here the
concept is "family of variance-correction methods," and it should have one
vocabulary regardless of whether the field is recording what *was applied*
(`design.variance_adjustment`) or what *is required* by a declared dependence
structure (`validity_frame.dependence.method_family_required`).

Concretely: the brief's own worked example uses a composite value,
`method_family_required: cluster_robust_or_mixed`, which is **not** a member of
`VARIANCE_ADJUSTMENTS` (a disjunction, not an atomic value) — inventing composite
strings would mean inventing a second mini-language just for this one field, which
the project's own `D-05`-driven discipline argues against (every new piece of
domain logic needs a citation and a reference test; a composite-string DSL is scope
creep with no citation to anchor it). The cleaner resolution: keep
`method_family_required` typed against the **same atomic** `VARIANCE_ADJUSTMENTS`
set, and let `DSX-VAL-030`'s check *logic* — not the vocabulary — encode which
`dependence.structure` values accept which subset of adjustments (e.g.
`structure: clustered` is satisfied by any of `{cluster_robust, bootstrap_cluster,
mixed_effects}`, `structure: repeated_measures` by `{mixed_effects,
cluster_robust}`, etc.). This keeps `dsx vocab` honest (one list of variance
methods, not two overlapping ones) and keeps the "or" logic where it belongs — in
code with a citation, not in a spec value.

### 4.3 M-02/M-03: `design.peeking_policy` as the single source, `PEEKING_POLICIES` gains a value

**Verified against `dsx/spec.py`:** `PEEKING_POLICIES` currently has four members
(`fixed_horizon`, `sequential_obf`, `sequential_pocock`, `always_valid`), validated
structurally by `_validate_design_shape` as `DSX-SPEC-042`, and read semantically by
`design.py::_check_peeking` for the existing `DSX-EXP-060`.

Per **M-02** (no new `inference.stopping_rule` field) and **M-03** (new
`PEEKING_POLICIES` value for uncontrolled continuous monitoring):

- Add one member to `PEEKING_POLICIES` in `dsx/spec.py`, e.g.
  `"uncontrolled_continuous": "Interim looks continue indefinitely with no
  error-rate correction — the discipline failure DSX-PAR-010/011 exist to catch."`
  This is a vocabulary-member addition, not a finding-code change, so **D-06 does
  not apply** — it is safe by construction. `_validate_design_shape`'s existing
  `DSX-SPEC-042` check needs no code change; it already validates membership
  generically against whatever `PEEKING_POLICIES` contains.
- **Where this addition should ship**: not M1. Following the same
  don't-scaffold-unused-structure reasoning the brief applies to
  `references/families.yaml` (§6.6 item 2), a vocabulary member with no consumer
  should not exist for two milestones before anything reads it. Recommend shipping
  the `PEEKING_POLICIES` addition in **M2c**, atomically with `DSX-PAR-010/011` —
  the milestone that actually gives it meaning.
- **Where `DSX-PAR-010`/`DSX-PAR-011` read from**: both read `design.peeking_policy`
  (via `section(spec, "design").get("peeking_policy")`, same accessor pattern
  `design.py` already uses) and `inference.paradigm` (via
  `section(spec, "inference")`) to select which half of the pair applies.
  `DSX-PAR-010` additionally reads `inference.alpha_spending`; `DSX-PAR-011`
  additionally reads `inference.threshold_calibration` and `inference.prior` (+
  its justification). This is the one place in the new subsystem where reading
  `paradigm` is not just permitted but is the entire point — **D-11 ("frame-layer
  checks never read paradigm") applies to `DSX-VAL-*`/`DSX-INT-*`, not to
  `DSX-PAR-*`**, which exists precisely to branch on it. Keeping this distinction
  explicit in the module boundary (`frame/paradigm.py` is the only frame module
  permitted to import `inference.paradigm` for branching purposes; `frame/val.py`
  and `frame/interference.py` must not) is a good candidate for the D-03a-style
  automated boundary test mentioned in §7 (M1, per **M-04**) — it can be a static
  check ("no `spec.get('paradigm')` / `inference.paradigm` read outside
  `frame/paradigm.py`"), not just an import-graph check.
- **Spec-schema change surface, summarised**: `PEEKING_POLICIES` dict (`dsx/spec.py`,
  M2c) gains one member; no new top-level field anywhere; `_validate_design_shape`
  is unchanged; `frame/paradigm.py` (new, M2c logic added to the M1-created module)
  is the only new code that reads the value semantically.

---

## 5. Decision record plumbing

**Recommendation: a parallel channel, not a `Report`/`Finding` change.** A decision
record is emitted for *every* judgment a check resolves, including ones that pass
cleanly with no `Finding` at all (the brief's own §5.5 example — "analysis_unit =
account, not session" — logs the *rule that was applied*, not a defect). Forcing
that through `Report.findings` would mean minting a phantom `INFO`-severity finding
for every non-defect decision, which pollutes `apply_suppressions()`'s
`known_codes()` AST scan (it would start finding "codes" that are not really
findable/suppressible in the D-06 sense) and `Report.counts()`. Keeping it separate
avoids both problems and requires **zero changes to the `Report`/`Finding`
dataclasses**.

- **New module `dsx/decisions.py`** (peer to `findings.py`/`spec.py`, M1). Defines
  `DecisionRecord` (a frozen dataclass mirroring §5.5's schema exactly: `id`,
  `layer`, `choice`, `inputs`, `rule`, `citation`, `counterfactual`,
  `alternatives_rejected`, `confidence`, `escalate`) plus `to_dict()`, and a small
  helper `record(report: Report, **fields) -> DecisionRecord` that both constructs
  the record and appends it to `report.context.setdefault("decisions", [])` — reusing
  `Report.context`, the extensibility point that already exists and is already used
  for exactly this kind of side-channel data (`report.context["srm"]`).
- **Accumulation across a gate run**: because `merge()` nests each sub-report's
  context under `merged.context[sub.check]`, decisions from `frame/val.py`'s
  sub-report land at `context["val"]["decisions"]`, from `frame/paradigm.py` at
  `context["paradigm"]["decisions"]`, etc. `cmd_gate` (after computing the merged
  report) flattens every `*.decisions` list it finds and **appends** each record as
  one JSON line to `{phase_dir or spec.parent}/DECISIONS.jsonl`, tagged with
  `gate_point` and a timestamp. Append-only means the file accumulates the full
  plan→execute→verify→ship trail for a phase without any cross-process
  coordination — each `dsx gate <point>` invocation just adds its lines. This
  mirrors the existing visible-artifact convention (`DATA-REVIEW.md`,
  `FIGURE-MANIFEST.yaml`) rather than hiding state in a dotfile.
- **`dsx explain` (new, non-blocking subcommand)**: reads `DECISIONS.jsonl` next to
  the resolved spec (same path-resolution convention as every other subcommand —
  `--spec`/`--phase-dir`), parses each line, and renders it grouped by `id`/`layer`
  with `citation` and `counterfactual` foregrounded (per D-04, the counterfactual
  is "what does the teaching"). **Always returns 0** — it never calls
  `Severity.parse`/`emit()`/`GATE_THRESHOLDS` at all, so there is no threshold to
  misconfigure into blocking. This is purely additive to `dsx/cli.py`: one new
  `cmd_explain()` and one new `sub.add_parser("explain", ...)`; nothing in the
  existing `emit()`/`Report`/gate machinery is touched.
- **Scope for v1**: wire `decisions.record()` into the new frame families
  (`DSX-VAL-*`, `DSX-INT-*`, `DSX-PAR-*`, `DSX-PRE-*`, `DSX-ADM-*`) at the specific
  judgment points each milestone's plan identifies (not every single `Finding` —
  most structural "field X is blank" findings are not "decisions" in the §5.5
  sense). Retrofitting the ten pre-existing quality dimensions to also emit
  decision records is out of scope for this milestone; it is a reasonable D-03-style
  "extend in place, don't retrofit everything" scope boundary, worth flagging
  explicitly in the roadmap rather than silently deciding it.

---

## 6. INFO-severity manifest flow through `emit()` — verified end to end

Traced against the real `Severity`/`Report`/`emit()` code, not assumed:

1. `frame/paradigm.py` calls `report.add("DSX-PAR-001", "INFO", "…", where=...,
   applied=[...], not_applied=[...])`. `Report.add()` calls `Severity.parse("INFO")`
   → `Severity.INFO` (value `10`), constructs a `Finding`, appends it. No different
   from any other `report.add(...)` call in the codebase.
2. `Report.blocks(threshold)` = `bool(self.at_or_above(threshold))`, and
   `at_or_above` keeps only findings with `severity >= threshold`. Every configured
   `GATE_THRESHOLDS` value (`CRITICAL`=50 at plan/execute, `HIGH`=40 at verify/ship)
   is far above `INFO`=10, and `LOW`=20 and `MEDIUM`=30 both are too. An `INFO`
   finding can only ever contribute to a block if a caller explicitly passes
   `--block-on INFO` on the CLI — a deliberate manual override of every documented
   default, not something a gate config produces by accident.
3. `emit()` computes `code = report.exit_code(threshold)` purely from `blocks()`; an
   `INFO`-only addition to an otherwise-passing report leaves `code == EXIT_PASS`
   (0), unchanged.
4. **Visibility is not lost on a pass.** `emit()` routes output to `stdout` when
   `code == EXIT_PASS`, but `report.render()` (the function that produces that
   text) iterates **all** `self.findings` sorted by severity, with no threshold
   filter — `render()`'s only use of `threshold` is the final PASS/BLOCK summary
   line. So the `DSX-PAR-001` manifest text is printed on every passing gate run
   where `paradigm` is declared, on stdout, exactly like every other finding; it is
   simply guaranteed never to be the reason the run blocks.
5. `Report.counts()` already initializes an `"INFO"` bucket
   (`{s.label: 0 for s in Severity}` iterates the full enum, `INFO` included) and
   `_markdown_report()`/`render()` already print an `INFO=` count in the summary
   line — no changes needed anywhere in `findings.py` or the report renderers.
   `Severity.INFO` is fully first-class infrastructure today; it has simply never
   been exercised until this subsystem.

Net: `DSX-PAR-001` requires **zero changes to `dsx/findings.py`**. It is a pure
consumer of existing, already-correct machinery.

---

## 7. Fixture strategy (D-08)

### The two canonical fixtures

`examples/good-ANALYSIS-SPEC.yaml` and `examples/bad-ANALYSIS-SPEC.yaml` are
extended, never replaced, and the D-08 invariant is enforced by exactly two
exit-code-level tests (`test_good_fixture_passes_every_gate`,
`test_bad_fixture_blocks_at_plan`/`test_bad_fixture_blocks_at_ship`) that never need
to change as new families are added — they assert on `dsx gate <point>`'s exit
code, not on which checks ran. This is the load-bearing property that keeps D-08
mechanically cheap to maintain: **each milestone only has to grow fixture content**,
never touch the test that enforces the invariant.

- **`good-ANALYSIS-SPEC.yaml`**: each milestone that adds a check family extends
  this fixture's `validity_frame:`/`inference:` blocks with values that are not
  merely vocabulary-valid but semantically clean against *that milestone's* new
  checks specifically (e.g. M2a must confirm the `identification.strength` /
  `constraint_source` pairing it adds doesn't trip `DSX-VAL-040`, and that
  `dependence.structure` and `method_family_required` are mutually consistent per
  §4.2's subset logic). The existing `design:` block (`randomization_unit: user`,
  `analysis_unit: user`, `peeking_policy: fixed_horizon`) is already compatible
  with the new fields and needs no change — `validity_frame.units.*` should be set
  to `user` throughout to stay consistent (no finer `observation` unit than
  `assignment`), and the M2c-added `PEEKING_POLICIES` member has no effect on this
  fixture since it already declares `fixed_horizon`.
- **`bad-ANALYSIS-SPEC.yaml`**: each milestone injects at least one concrete new
  defect so the fixture keeps its own stated purpose ("see the whole finding
  catalogue at once"). Recommended concrete injections: `validity_frame.units`
  with an unhandled finer observation unit (`DSX-VAL-020`), `dependence.structure:
  clustered` with no `method_family_required` (`DSX-VAL-030`), weak identification
  with `constraint_source: none` (`DSX-VAL-040`), `interference.risk: shared_budget`
  with `mitigation: none` and no `residual_note` (`DSX-INT-010`), triggered
  analysis without `dilution_adjusted` (`DSX-INT-030`). Since a single spec
  declares one `paradigm`, this fixture (already `question_type: causal`) should
  stay `paradigm: frequentist` and carry the `DSX-PAR-010` trip
  (`peeking_policy: uncontrolled_continuous`, no `alpha_spending`) — the
  `DSX-PAR-011` (Bayesian) side is covered separately, below, exactly as the brief
  requires ("one a Bayesian continuous-monitoring case" among the pulled-forward
  M1 fixtures).

### The 3–4 pulled-forward real-known-bad fixtures (M1)

Organise these **separately** from the two canonical fixtures, in
`examples/known-bad/`, one `<slug>-ANALYSIS-SPEC.yaml` + `<slug>-POSTMORTEM.md`
pair per case (mirroring the existing convention of a header comment explaining
provenance, but promoted to a full file since these need a documented real
post-mortem, not a one-line comment). This keeps them additive and narrowly scoped
— each fixture demonstrates *one* family's defect against a real remembered
failure, rather than growing into a second "everything wrong" fixture that would
compete with `bad-ANALYSIS-SPEC.yaml`'s existing role.

Recommended M1 set (minimum satisfying the brief's "at least one interference case
and one Bayesian continuous-monitoring case"):

1. `known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml` — trips `DSX-INT-010`.
2. `known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` — trips
   `DSX-PAR-011`. This is the one fixture the brief gives explicit numerical
   guidance for (§ "Fixture note for M1"): decide up front whether the reference
   simulation is against a **point null** (unbounded inflation via the law of the
   iterated logarithm) or **averaged over the prior** (Ville's-inequality bound,
   roughly `1/k`), state the choice in the check's docstring per D-05, and pick
   the reference value to match — building the fixture against one formulation and
   testing against the other "will look like an implementation bug for a day."
3. `known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` — trips `DSX-VAL-040`,
   modelled on the brief's own MMM/collinear-channel-spend example.
4. `known-bad/triggering-dilution-ANALYSIS-SPEC.yaml` — trips `DSX-INT-030`.

**Sequencing caveat, made explicit because it resolves a real gap in a literal
reading of the brief's M1 done-when clause:** these fixtures are *committed* in
M1 with their post-mortems, but the checks that would fire on them
(`DSX-VAL-*`/`DSX-INT-*`/`DSX-PAR-*` semantic logic) do not exist until
M2a/M2b/M2c. M1's own test coverage for them is therefore necessarily narrower —
confirm the fixture parses and validates *structurally* (shape/vocabulary, i.e.
`dsx validate` passes even though `dsx gate` doesn't yet know to block it) and that
the post-mortem file exists. The **code-specific regression test** ("this fixture
blocks with `DSX-INT-010`") is added in the milestone that ships that code, not in
M1. This is consistent with — not a violation of — the brief's M1 done-when
wording ("the real-case fixtures are committed with their documented
post-mortems"), which stops short of claiming they already block anything.

### Keeping D-08 testable going forward

Each milestone's plan should include, as a standing checklist item (not a new test
harness — the harness already exists and is sufficient):

1. Extend `good-ANALYSIS-SPEC.yaml` / `bad-ANALYSIS-SPEC.yaml` with that
   milestone's new fields; re-run the two existing canonical tests unchanged —
   they should still pass/fail exactly as before, now exercising the larger spec.
2. Add exactly one new unittest per newly-activated `known-bad/*` fixture, asserting
   the specific code fires (`assertIn("DSX-VAL-040", err)`-style, matching the
   existing `test_bad_fixture_blocks_at_plan` pattern).

---

## 8. Build order across M1, M2a, M2b, M2c, M3, M4, M5

### Hard ordering constraints (technical, not preference)

| Constraint | Why it is hard, not a preference |
|---|---|
| **M1 before everything else** | `validity_frame:`/`inference:` field existence, the new closed vocabularies, `dsx/frame/` package existence, and `dsx/decisions.py` are read/imported by every later family. No later milestone's checks have anything to read without M1. |
| **`DSX-PAR-001` ships inside M1, atomically with the `paradigm` field** | Stated directly in the brief and reconfirmed by tracing D-10: the instant `inference.paradigm` is a legal field, an operator can set it to `bayesian`, and per D-10 the only sane response to an unsupported/unimplemented paradigm is the INFO manifest — not silently passing (worse than blocking) and not blocking (the exact failure D-10 forbids). There is no milestone in which "paradigm exists, manifest doesn't" is a safe state to leave the tool in, so the two cannot ship in different milestones. |
| **`DSX-PAR-010` and `DSX-PAR-011` ship together, within M2c** | D-12/D-12a: shipping one half of a symmetric pair without the other is exactly the paradigm-steering the family exists to prevent. This is an atomicity constraint *inside* M2c, not an inter-milestone one. |
| **M4 (`DSX-ADM-*`) after M2a (`DSX-VAL-*`)** | `references/families.yaml` is explicitly keyed in part on "dependence handling" (brief §6, M4) — i.e. on the `validity_frame.dependence` taxonomy M2a establishes. Building the family ontology before that taxonomy is stable risks keying it on a shape that changes under it. `references/families.yaml` must also not be created before M4 (brief §6.6 item 2, explicit) — and by the same reasoning, `dsx/frame/admissibility.py` itself should not be created before M4 either; there is no code to write against a data file that does not exist yet, and an empty module is the code-level version of the anti-pattern the brief calls out for the data file. |
| **M5 last** | M5's own scope ("extend the M1 corpus to full size," `dsx stats --paradigm`) presupposes M1's corpus mechanism and M2c's paradigm data already exist. The gated-backlog entry condition for the second `DSX-ADM-*` axis explicitly requires "M4 ships, **and** `dsx stats --paradigm` shows Bayesian frames above 15%" — a condition that cannot even be evaluated before M5 ships. M5 is a hard terminal milestone by construction, not by convenience. |
| **The D-03a boundary test (M-04) is an M1 deliverable** | It has to exist before M2a+ start adding the first real cross-cutting logic (`frame/val.py`, `frame/interference.py`), or there is a window where a violation could land undetected. It can run against the near-empty M1 `dsx/frame/` (just `__init__.py` + `paradigm.py`) and continues to gate every subsequent milestone unchanged — an AST/import scan asserting no `dsx/frame/*.py` imports `dsx.checks.*`, extended per §4.3 to also assert `inference.paradigm` is read only from `frame/paradigm.py`. |
| **`REVERSALS.md` template (M-05) is an M1 deliverable** | Tangential to the check architecture but stated as an M1 output in PROJECT.md; noted here only because it belongs in the same milestone as the decision-record infrastructure it is conceptually adjacent to. |

### Preferences (the brief's stated order is value-driven, not dependency-driven)

- **M2a vs M2b have no technical dependency on each other.** Both need only M1's
  `validity_frame:` contract shape; `DSX-VAL-*` reads `estimand`/`units`/
  `dependence`/`identification`/`sampling_frame`/`missingness`/`measurement`,
  `DSX-INT-*` reads `interference`/`triggering`/`stability` — disjoint sub-blocks.
  The brief's ordering ("catastrophe-prevention value per unit of work") is a
  prioritisation choice, and a legitimate one (M2b is called out as "the largest
  single risk reduction for a 60%-A/B-test workload"), but a roadmap could
  technically parallelise or reorder M2a/M2b without breaking anything downstream.
- **M3 (`DSX-PRE-*`) does not hard-depend on M2a/M2b/M2c**, only on M1's
  `inference.fallback_rule`/`declared_at` fields and on `results.tests` existing —
  both M1-era surface. It is, however, a **soft** dependency worth sequencing after
  M2a specifically: the brief's own fallback-rule example ("if clusters < 30 ->
  wild cluster bootstrap") references a concept (`clusters`) that only has a
  stable, checked meaning once `validity_frame.dependence.structure` (M2a) exists
  and is enforced — writing M3 before M2a risks the DSL referencing a field whose
  semantics haven't settled yet. Recommend sequencing M3 after M2a; not a hard
  blocker if schedule pressure argues otherwise.
- **Per-milestone decision-record wiring is a recommendation, not a requirement
  imposed by any dependency.** Each new check family *could* ship without emitting
  `DecisionRecord`s and have that retrofitted in a later pass; doing so would
  undercut D-04's framing of decision records as the mechanism that makes "never
  block to teach" true from day one, so this document recommends treating "the new
  checks in this milestone emit decision records for their key judgment calls" as
  a standing per-milestone deliverable rather than a deferred retrofit milestone —
  but nothing in the code makes this mandatory the way, say, the `DSX-PAR-010`/`011`
  atomicity constraint is.

### Resulting order

```
M1 ──> M2a ──┬──> M3 ──┐
      (pref) │         │
             M2b        ├──> M4 ──> M5
             M2c ───────┘
```

`M1` is the only true single point every other node depends on. `M2a`/`M2b`/`M2c`
are mutually independent in principle (drawn in the brief's stated priority order
above); `M3` is best sequenced after `M2a` (soft); `M4` hard-depends on `M2a`
(dependence taxonomy) and, separately, on `references/families.yaml` not existing
before it; `M5` hard-depends on everything before it and is necessarily last.

---

## Sources

All findings above are grounded in direct reads of this repository at the current
commit, not external research (this is an internal-integration architecture
question, not an ecosystem survey):

- `brief.md` (sections 1, 4, 5, 6, 6.5, 6.6 — binding per `.planning/PROJECT.md`)
- `.planning/PROJECT.md` (M-01…M-05 decisions, integration-surface notes)
- `dsx/cli.py` (`CHECKS`, `GATE_PROFILES`, `GATE_THRESHOLDS`, `run_checks`, `cmd_gate`)
- `dsx/checks/__init__.py` (family/prefix map, import pattern)
- `dsx/findings.py` (`Severity`, `Finding`, `Report`, `emit`, `merge`)
- `dsx/spec.py` (closed vocabularies, `validate_structure`, `_validate_design_shape`)
- `dsx/checks/design.py` (`DSX-EXP-020/021` unit reconciliation, `DSX-EXP-060` peeking,
  `_check_identification`)
- `dsx/checks/decision.py` (structured-threshold pattern used as the `gate_point`
  parameter precedent for `frame/prereg.py`)
- `dsx/suppressions.py` (`known_codes()` AST scan — confirms new packages need no
  separate registration to be suppressible)
- `dsx/loader.py` (`load()` is a generic `Path -> dict` loader, reusable for
  `references/families.yaml`)
- `examples/good-ANALYSIS-SPEC.yaml`, `examples/bad-ANALYSIS-SPEC.yaml`
- `tests/test_dsx.py` (`TestCLI` — the exact tests enforcing D-08 today)
- `capabilities/dsx/capability.json` (gate wiring into the GSD phase loop, confirms
  gates shell out to `dsx gate <point>` and interpret exit codes per the CLI docstring)

---
*Architecture research for: DSX Validity Frame subsystem integration (gsd-dsx v2.0.0)*
*Researched: 2026-08-07*
