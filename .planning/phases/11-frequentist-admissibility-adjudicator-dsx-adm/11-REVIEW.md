---
phase: 11-frequentist-admissibility-adjudicator-dsx-adm
reviewed: 2026-08-22T00:00:00Z
depth: deep
files_reviewed: 24
files_reviewed_list:
  - brief.md
  - dsx/cli.py
  - dsx/frame/admissibility.py
  - dsx/frame/paradigm.py
  - dsx/spec.py
  - examples/bad-ANALYSIS-SPEC.yaml
  - examples/good-ANALYSIS-SPEC.yaml
  - examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml
  - examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml
  - examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
  - examples/known-bad/post-hoc-procedure-switch-ANALYSIS-SPEC.yaml
  - examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml
  - examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml
  - references/families.yaml
  - references/finding-codes.md
  - references/test-selection.md
  - scripts/gen-finding-catalogue.py
  - templates/ANALYSIS-SPEC.yaml
  - tests/test_dsx.py
  - tests/test_families_yaml.py
  - tests/test_frame_admissibility.py
  - tests/test_frame_boundary.py
  - tests/test_frame_paradigm.py
  - tests/test_gen_finding_catalogue.py
findings:
  critical: 1
  warning: 5
  info: 0
  total: 6
status: fixed
resolution:
  fixed_at: 2026-08-22T00:00:00Z
  commit: d49666c
  CR-01: "fixed — cmd_recommend now calls applies_to_frequentist_admissibility(spec) before admissible_families(), omitting the admissibility key when it doesn't apply. Regression test: test_bayesian_spec_omits_admissibility_key_rather_than_refusing."
  WR-01: "fixed — dominating_rules() now sorts matches by rule id before returning. Regression test: test_order_independent_of_ontology_file_order_when_two_rules_dominate (necessarily synthetic — unreachable with today's 4-rule ontology)."
  WR-02: "tracked as follow-up — design gap in DSX-ADM-010's counterfactual field for a two-hop domination chain, unreachable in the current ontology, needs a more invasive fix (recursive dominating_rules check or fall-through-to-top-of-rank logic). Not fixed."
  WR-03: "fixed — load_ontology() now drops uncited ranking_rules entries the same way it already drops uncited families. Regression test: test_one_uncited_ranking_rule_is_dropped_and_named. assumption_vocabulary left as-is: confirmed no consumer of ontology.tokens exists anywhere in the module, so there is no live finding-text risk to close there."
  WR-04: "tracked as follow-up — Resolution.detail/outside_axes computed but unconsumed (dead output, maintenance hazard not a correctness bug). Not fixed."
  WR-05: "not this phase's scope — DSX-PAR-002's dual title strings predate this phase (Phase 9, commit df20ef6). Not touched."
---

# Phase 11: Code Review Report

**Reviewed:** 2026-08-22T00:00:00Z
**Depth:** deep
**Files Reviewed:** 24
**Status:** issues_found

## Summary

This is the first review pass of Phase 11 (`DSX-ADM-*`, the frequentist admissibility
adjudicator). I read every listed source, reference and test file, ran the full test
suites for `tests/test_frame_admissibility.py`, `tests/test_frame_boundary.py`,
`tests/test_frame_paradigm.py`, `tests/test_families_yaml.py`,
`tests/test_gen_finding_catalogue.py` and the Phase-11 slices of `tests/test_dsx.py`
(all 186 tests pass), and additionally exercised the CLI directly against the committed
fixtures to probe behaviour the test suite does not cover.

The five specific concerns named in the review brief were checked point by point:

1. **DSX-ADM-010 fires only on a cited pairwise-domination rule.** Verified correct by
   direct code reading and by a synthetic reproduction: `dominating_rules()` only
   consults `ontology.rules` (the four cited `ranking_rules` entries), never
   `_MANSKI_RULE`/`_TIEBREAK_RULE`, so a Manski-fallback-only or tiebreak-only
   separation between two admissible families can never fire DSX-ADM-010. This is
   correctly narrower than what the module's own docstrings imply the project's
   research doc originally recommended.
2. **Two-sided D-05 citation enforcement.** `load_ontology()` drops uncited `families`
   entries at runtime and `check_families_citations()` fails the build on any blank
   citation in `families`, `assumption_vocabulary` **and** `ranking_rules`. The two
   mechanisms do not silently substitute for each other for the `families` block —
   but the runtime side only protects `families`; it does not also drop or reject
   uncited `ranking_rules`/`assumption_vocabulary` entries (WR-04 below).
3. **`dsx/frame/admissibility.py` never reads `inference.paradigm`.** Confirmed by
   direct reading and by `tests/test_frame_boundary.py`'s scanner (both the blunt text
   scan and the AST scan pass clean on this file). The frequentist-only scoping
   boolean is always computed by `dsx/frame/paradigm.py::applies_to_frequentist_admissibility`
   and passed in as a parameter to `admissibility.check()` — but see BLOCKER-01: one
   *other* caller of the ontology (`dsx/cli.py::cmd_recommend`) skips that scoping
   boolean entirely, which is a real, reproduced bug, not merely a hypothetical gap.
4. **`dsx recommend-test` composition is additive and the byte-identity test is real.**
   `test_no_spec_output_is_byte_identical_regardless_of_working_directory` genuinely
   subprocess-runs `python -m dsx.cli recommend-test` twice (different `cwd`) and diffs
   `stdout` byte-for-byte, and `test_spec_flag_is_additive_with_the_four_original_values_unchanged`
   asserts both the exact 5-key ordering and that the original four values are
   untouched. Confirmed by reading and by rerunning both tests directly.
5. **Alias-resolution design (filter by axis pair first, then resolve alias within it).**
   The candidate-then-alias ordering is correct and I could not find a case where it
   silently falls through to the wrong `Resolution` status — but I found a related,
   provable file-order dependency in a *different* part of the ranking pipeline
   (WR-01 below) that the module's own stated design principle (order-independence,
   D-15) explicitly disclaims elsewhere but does not actually enforce here.

One reproduced functional bug (BLOCKER-01) and five quality/robustness gaps are
recorded below.

## Critical Issues

### CR-01: `dsx recommend-test --spec <bayesian-spec>` bypasses the paradigm scoping and prints a false frequentist refusal

**File:** `dsx/cli.py:430-459` (`cmd_recommend`)
**Issue:**

`admissibility.check()` correctly gates itself with the caller-supplied
`applies_to_frame` boolean (`dsx/frame/paradigm.py::applies_to_frequentist_admissibility`),
and `dsx/cli.py::run_checks()` correctly computes and passes that boolean for every
gate/check/audit invocation of the `"admissibility"` name (verified: `dsx check
admissibility --spec <bayesian spec>` returns an empty finding set, as designed).

`cmd_recommend`, however, imports `admissible_families()` directly and calls it
unconditionally whenever `--spec`/`--phase-dir` is given — it never consults
`applies_to_frequentist_admissibility`:

```python
def cmd_recommend(args: argparse.Namespace) -> int:
    from .checks.stats import recommend_test
    from .frame.admissibility import admissible_families
    ...
    if args.spec is not None or args.phase_dir is not None:
        path = find_spec(args.spec, args.phase_dir)
        spec = load(path)
        out["admissibility"] = admissible_families(spec)   # no paradigm scoping at all
```

`admissible_families()` (unlike `admissibility.check()`) has no scoping parameter of
its own — it always evaluates the declared frame against the frequentist-only
ontology. For a spec that legitimately declares `inference.paradigm: bayesian`, this
produces a `"refusal": "no_admissible_procedure"` / `"refusal_cause":
"declared_procedure_unresolved"` payload naming the analyst's Bayesian procedure as an
unrecognised frequentist test — reproduced directly:

```
$ python -m dsx.cli recommend-test proportion --groups 2 \
    --spec examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml
{
  ...
  "admissibility": {
    "declared_procedure": "bayesian_ab",
    "resolution": "unresolved",
    "admissible": [ ...4 frequentist candidates ranked... ],
    "refusal": "no_admissible_procedure",
    "refusal_cause": "declared_procedure_unresolved"
  }
}
```

This directly contradicts D-10 ("An unsupported or unimplemented paradigm is never a
blocking finding on its own" — the *spirit* of which is that declaring a paradigm
honestly must never cost more than staying silent) and D-22/REQ-P11-05, which exists
specifically so the frequentist ontology is never evaluated against a Bayesian frame.
The gate path (`dsx gate`, `dsx check`, `dsx audit`) gets this right; only the
`recommend-test` composition path — added in this same phase (11-07) — does not. No
existing test exercises `cmd_recommend` against a Bayesian-paradigm spec (the only
`--spec` test uses the frequentist `good-ANALYSIS-SPEC.yaml`), which is how this
shipped unnoticed.

**Fix:**
```python
from .frame.paradigm import applies_to_frequentist_admissibility

if args.spec is not None or args.phase_dir is not None:
    path = find_spec(args.spec, args.phase_dir)
    spec = load(path)
    if applies_to_frequentist_admissibility(spec):
        out["admissibility"] = admissible_families(spec)
    # else: omit the key entirely, or emit a small { "applies": False, ... }
    # shape — mirroring admissibility.check()'s own widen-never-penalise behaviour.
```
Add a regression test that runs `recommend-test --spec` against a Bayesian-declared
spec (e.g. `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml`) and
asserts the `admissibility` key is either absent or explicitly marked not-applicable.

## Warnings

### WR-01: `dominating_rules()` picks the first dominating rule in ontology file order, not a canonical order

**File:** `dsx/frame/admissibility.py:518-540` (`dominating_rules`), `:713` (`_check_declared_procedure_ranking`, `rule = rules[0]`)
**Issue:**

Every other order-sensitive path in this module goes out of its way to be
file-order-independent: `alias_index()` raises `CheckError` rather than "last one
wins" on a same-pair alias collision (explicitly to keep the resolved outcome
independent of file order, D-15); `candidate_families()` sorts its output
lexicographically by id "so downstream consumers' ordering is a function of the
candidate set itself, never of the ontology file's own entry order"; and
`resolve_declared_procedure()` explicitly sorts `other_matches` by family id and
documents "the lexicographically first family id is taken" for exactly this reason.

`dominating_rules()` breaks that pattern: it returns rules "ordered as they appear in
`rules` (ontology order)" (its own docstring), and `_check_declared_procedure_ranking`
takes `rules[0]` — the first *matching* rule in `references/families.yaml`'s own
declaration order — with no secondary sort. Reproduced with two synthetic rules that
both dominate the same family in opposite tuple order:

```
order1 dominating rules for b: ['rule_z_last', 'rule_a_first']
order2 dominating rules for b: ['rule_a_first', 'rule_z_last']
order1[0]==order2[0]? False
```

Today this is latent: no family in the committed `references/families.yaml` is named
as `over` by two different `ranking_rules` entries, so `rules[0]` is always the only
element. But the ontology is explicitly planned to grow toward 25-35 entries (brief.md
§6, M4), and the moment two cited orderings dominate the same family, which
citation/condition text lands in the DSX-ADM-010 finding becomes a silent function of
where the two rules happen to sit in the YAML file — exactly the failure mode the rest
of this module was deliberately built to rule out.

**Fix:** Sort candidate dominating rules by a stable key before taking the first —
e.g. `sorted(candidates, key=lambda r: r.id)[0]`, or `sorted(..., key=lambda r:
r.prefers)` to match the "lexicographically first family id" convention used
elsewhere in this same file — and add a test with two synthetic rules dominating one
family to pin the chosen tie-break the same way `test_order_independent_of_family_order_in_ontology`
pins `candidate_families()`.

### WR-02: DSX-ADM-010's `counterfactual` is not verified against the preferred family itself being undominated

**File:** `dsx/frame/admissibility.py:891-907` (`check()`, the `fired_code == "DSX-ADM-010"` branch)
**Issue:**

The decision record's `counterfactual` field states unconditionally:

```python
counterfactual = (
    f"Declaring {fired_rule.prefers!r} instead of the resolved "
    "family would have cleared DSX-ADM-010."
)
```

This is true only when `fired_rule.prefers` is not itself dominated by some other
cited rule. `dominating_rules()` is only ever called against the *declared* (resolved)
family, never against the *preferred* family named in the fired rule — so in a
candidate set with a two-hop domination chain (rule 1: B preferred over A; rule 2: C
preferred over B), declaring `A` fires DSX-ADM-010 citing rule 1 and claims declaring
`B` would clear it, when in fact `B` would immediately re-fire DSX-ADM-010 under rule
2. Brief.md §5.5 singles out the `counterfactual` field as the single most
load-bearing part of the decision record ("Here is what I chose" is weak learning...
the rule is what transfers") — a counterfactual that can be proven false undermines
exactly the property that field exists to guarantee.

Not reachable in the current 4-rule, 14-family ontology (no chain currently exists),
so this is a design gap rather than a live incorrect finding today.

**Fix:** Before asserting the counterfactual, check `dominating_rules(fired_rule.prefers,
candidates, ontology.rules)` is empty; if not, either name the rule chain in the
counterfactual text or fall through to the top of the ranked set rather than the
immediate preferred family.

### WR-03: Runtime citation enforcement (D-05/D-24) only drops `families`, not `ranking_rules` or `assumption_vocabulary`

**File:** `dsx/frame/admissibility.py:138-226` (`load_ontology`)
**Issue:**

`load_ontology()`'s docstring frames itself as "the run-time half of the two-sided
citation enforcement," but the actual drop logic only applies to the `families:`
block:

```python
for entry in families_raw:
    ...
    citation = str(entry.get("citation", "")).strip()
    if not citation:
        dropped.append(str(entry.get("id", "")))
        continue
    families.append(_coerce_family(entry))

rules = tuple(
    _coerce_rule(entry) for entry in rules_raw if isinstance(entry, dict)
)   # no citation filtering at all

tokens = {
    str(entry.get("token", "")): str(entry.get("citation", ""))
    for entry in vocabulary_raw
    if isinstance(entry, dict)
}   # no citation filtering at all
```

`scripts/gen-finding-catalogue.py::check_families_citations()` *does* cover all three
blocks at build time, so the committed tree is clean today. But the build-time gate
and the runtime reader are two independent code paths by design (per this module's own
docstring: "a hand-edited file that skipped the build-time gate still cannot rank an
uncited family" — a claim that is true for `families` and false for `ranking_rules`).
A `ranking_rules` entry with a blank citation that reaches a live gate run (e.g. a
local edit never run through `--check`) would still be used by `dominating_rules()`
and would surface in a live DSX-ADM-010 finding's `citation` field as an empty string
— exactly the outcome D-05 ("no check ships without a citation... the single most
important constraint in the project") exists to prevent.

**Fix:** Apply the same non-blank-after-strip drop to `ranking_rules` (and, if
`buys`/`charges` tokens are ever surfaced with their citation text directly in a
finding, to `assumption_vocabulary` too), mirroring the existing `families` drop
logic, so the two enforcement mechanisms are actually symmetric rather than one being
a strict subset of the other.

### WR-04: `Resolution.detail` and `Resolution.outside_axes` are computed but never consumed

**File:** `dsx/frame/admissibility.py:96-105` (`Resolution`), `:313-394` (`resolve_declared_procedure`)
**Issue:**

`resolve_declared_procedure()` builds a nontrivial, branch-specific `detail` sentence
for every one of its four return paths (including the "more than one other pair
matched" disambiguation text at lines 377-381), and threads through `outside_axes` for
the `outside_candidate_set` case. Neither field is read anywhere downstream:
`admissible_families()` copies only `resolution.status` and `resolution.family_id`
into its return dict, and `_check_no_admissible_procedure()` — the one place that
builds a user-facing finding for an unresolved/outside-candidate-set procedure —
reconstructs an entirely separate detail string from scratch rather than reusing
`resolution.detail` or `resolution.outside_axes`. Confirmed via grep: no test asserts
on `Resolution.detail`'s content either (only `.status`, `.family_id`,
`.outside_axes` are asserted, and `.outside_axes` only at the `resolve_declared_procedure`
unit-test level, never at `admissible_families()`/`check()` level).

This is dead computed output, not a correctness bug, but it is a real maintenance
hazard: a future edit to `_check_no_admissible_procedure()`'s hand-written detail text
can silently drift from `resolution.detail`'s independently-maintained version of the
same information with nothing to catch the divergence.

**Fix:** Either wire `_check_no_admissible_procedure()`'s detail text to reuse
`resolution.detail`/`outside_axes` directly (removing the duplicated string-building),
or remove the two unused fields from `Resolution` if the duplication is intentional
for some reason not documented in the current docstrings.

### WR-05: `DSX-PAR-002` is declared with two different title strings, which the finding-catalogue generator silently resolves by last-write-wins

**File:** `dsx/frame/paradigm.py:382-427` (`_check_paradigm_justification`)
**Issue:**

Not introduced by this phase (present since Phase 9, commit `df20ef6`) but the file is
in this phase's review scope and the effect is visible when running the tooling this
phase also touches (`scripts/gen-finding-catalogue.py`). Two `report.add("DSX-PAR-002",
...)` call sites in the same function use different title strings:

```python
report.add("DSX-PAR-002", "HIGH",
    f"inference.paradigm ({paradigm}) is declared with no paradigm_justification", ...)
...
report.add("DSX-PAR-002", "HIGH",
    "inference.paradigm is not declared under an uncontrolled continuous design", ...)
```

Running `scripts/gen-finding-catalogue.py --check` (or any test that calls
`g.collect()`) prints `warning: DSX-PAR-002 declared twice with different text` to
stderr, and `collect()`'s `seen[row[0]] = row` means whichever call site is visited
last during the AST walk silently wins — `references/finding-codes.md` therefore
documents only one of the two real DSX-PAR-002 messages an operator can actually see.
This does not fail the build (the check is advisory, not gating) and is out of this
phase's direct authorship, but it is a live quality defect in a file this phase's
`files` list names for review, and it degrades the finding catalogue's accuracy for a
code this phase's own `_PARADIGM_CONDITIONAL["frequentist"]` entry (`"DSX-ADM-"`) sits
right next to.

**Fix:** Split into two distinct codes (costs a code number, D-06 makes that
permanent) or normalise both call sites to one shared title string parameterised by
which branch fired, so `references/finding-codes.md` documents both real messages (or
neither is lost to last-write-wins).

---

_Reviewed: 2026-08-22T00:00:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep_
