# Phase 17: Foundation — repairs and spec vocabulary - Research

**Researched:** 2026-08-29
**Domain:** Repair of an existing Python code-and-documentation contract (no new
statistics, no new package, no network/security surface). The task is: fix a
known doc/code mismatch, add one closed vocabulary, pin two behaviours with
regression tests, and prove no finding code moved.
**Confidence:** HIGH — every claim below was checked directly against the files
in this repository during this research session, not recalled from training
data. Nothing in this phase depends on an external library, so there was no
web research to do; the phase note in the task briefing said not to pad this
document with generic web research, and I have not.

## Summary

Phase 17 touches four files that already exist and one new small test file (or
three small new test files, house style allows either — see the open question
in "Where the new tests should live"). Nothing here computes a number: every
change is either a string constant, a membership check against a fixed list,
or a paragraph in a markdown reference file.

The Boschloo repair (REQ-P17-01) is the simplest item: two edits in
`dsx/checks/stats.py`, both already at the exact tree state the CONTEXT.md
decision assumed. The `estimand_kind` vocabulary (REQ-P17-02) is the item that
needs a genuine design decision the CONTEXT.md does not spell out at
implementation granularity: because `dsx vocab` is driven by exactly one
registry (`dsx/spec.py`'s `_VOCABULARIES` list), and because
`dsx/spec.py` is forbidden from importing `dsx/checks/*` (an enforced
architectural boundary, confirmed by a passing test in this tree), the new
6-member vocabulary constant has to live in `dsx/spec.py`, not next to
`OUTCOME_TYPES` in `dsx/checks/stats.py` where a first instinct might put it.
The membership guard that makes a mis-slotted value "loud, not a silent no-op"
then has to decide which of two existing patterns to extend — and because
REQ-P17-05 forbids minting a new finding code, the only code-neutral path is
to widen the *existing* `DSX-STA-040` check (currently scoped to
`analysis.outcome_type` alone) into a small membership loop that also covers
`analysis.estimand_kind`, mirroring the multi-field-one-code pattern
`dsx/spec.py` already uses for `DSX-SPEC-082` and `DSX-SPEC-085`. This is
spelled out in full below because it is the one piece of this phase that is
genuinely a design choice, not a lookup.

The `time_to_event` fallthrough guard (REQ-P17-04) and the catalogue
set-identity diff (REQ-P17-05) are both narrow, mechanical, and in the second
case almost certainly already implemented: `tests/test_finding_catalogue_invariant.py`
already asserts the live catalogue's code *set* equals a frozen Phase-12
snapshot plus a named list of sanctioned additive mints. Phase 17 adds no
mint, so that existing test is very likely the REQ-P17-05 gate already, and
the planner's job is to run it and confirm it still passes, not to write a new
one from scratch.

**Primary recommendation:** implement the `estimand_kind` membership guard by
widening `DSX-STA-040`'s existing check in `dsx/checks/stats.py` into a
`(field_name, vocabulary)` loop — the same shape `dsx/spec.py`'s
`_VALIDITY_FRAME_MEMBERSHIP` and `_INFERENCE_MEMBERSHIP` already use — so one
existing code covers both `analysis.outcome_type` and `analysis.estimand_kind`
and REQ-P17-05's zero-new-codes requirement is met by construction, not by
special-casing.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Boschloo test-name reconciliation | Backend / gate library (`dsx/checks/stats.py`) | Reference docs (`references/test-selection.md`) | The routing table lives in Python; the doc is the human-readable mirror the code must match. Neither is a service — this is a single-process CLI/library. |
| `estimand_kind` vocabulary declaration + dump | Backend / spec contract (`dsx/spec.py`) | CLI (`dsx/cli.py::cmd_vocab`) | `dsx/spec.py` is the sole source every closed vocabulary is declared in and the sole object `dsx vocab` serialises; `dsx/cli.py` only prints what `describe_vocabulary()` returns. |
| `estimand_kind` membership enforcement | Backend / gate library (`dsx/checks/stats.py`) | — | `analysis:` block content-checking already lives in `stats.py::_check_declared_test`; there is no separate `analysis:` shape validator in `dsx/spec.py` the way there is for `model:`/`design:`. |
| `time_to_event` fallthrough pin | Test suite (`tests/`) | — | A regression test, not a gate check — it protects the *shape* of `recommend_test`'s source, not a spec being validated. |
| D-12a disposition table | Planning document (`17-CONTEXT.md`) | — | Already recorded; no code artifact. |
| D-06 range pre-allocation | Planning document (`17-CONTEXT.md`) | Code comment (optional) | Already textually committed (see "D-06 note" below); a short reservation comment near `dsx/checks/stats.py`'s `DSX-STA-*` constants is a low-risk reinforcement, not a requirement. |
| Catalogue set-identity diff | Test suite (`tests/test_finding_catalogue_invariant.py`) | Build script (`scripts/gen-finding-catalogue.py`) | The test reads the generated `references/finding-codes.md`; the script regenerates it from the real `report.add(...)` call sites. |

## User Constraints

<user_constraints>

### Locked Decisions (17-CONTEXT.md `## Decisions`, verbatim intent — see full text for exact wording)

- **D-01** — `estimand_kind` stays that exact field name (not renamed to
  `relationship_kind`). Closed 6-member vocabulary:
  `linear_association`, `monotone_association`, `nominal_association`,
  `agreement`, `method_comparison`, `ordered_trend`. Lives on the `analysis:`
  block. Absence is never blocking (D-10 style). A mis-slotted value must fail
  loudly (a "DSX-SPEC-082-style decidable error" — CONTEXT.md's own phrase,
  meaning the *behaviour*, not necessarily literally that code number). Ships
  with an orthogonality note (code comment + `dsx vocab` description) stating:
  `estimand_kind` (on `analysis:`) drives test routing;
  `validity_frame.estimand.type` (a pre-existing, different vocabulary, see
  `ESTIMAND_TYPES` in `dsx/spec.py`) drives causal-admissibility adjudication.
  The two never share a read site.
- **D-02** — D-12a paradigm-disposition table for all nine Phase 18/19 gate
  checks: recorded in full in `17-CONTEXT.md`. No code to write this phase;
  the table itself is the deliverable, already committed.
- **D-03** — D-06 code-range pre-allocation: DSX-STA 050–129 in decades, one
  decade per Phase 18/19 theme, 130–139 reserved. Phase 17 assigns **zero**
  codes from this range. The `time_to_event` fallthrough guard is bound here
  too (not a code, a regression test).
- **D-04** — Boschloo reconciliation direction: fix the **code** to match the
  **doc** (doc already correctly cites Lydersen-Fagerland-Laake 2009 §9 for
  Boschloo dominating Fisher's exact on power). Adds no new finding code —
  `boschloo_exact` is a test-name string in a routing table, not a `DSX-STA-*`
  code.

### Claude's Discretion

CONTEXT.md does not delegate open-ended discretion to Phase 17 execute beyond
implementation mechanics (which module a constant lives in, which existing
code a membership guard reuses, test file layout). Those mechanics are exactly
what this research resolves below, because getting them wrong would either
violate REQ-P17-05 (mint a code) or violate the D-03a import-direction rule
(`dsx.spec` must never import `dsx.checks`).

### Deferred Ideas (OUT OF SCOPE for Phase 17)

- Wiring `estimand_kind` into `recommend_test`'s actual dispatch logic for
  correlation/agreement routing — that is Phase 18's job (REQ-P18-01/02/03),
  not Phase 17's. Phase 17 only needs the vocabulary to exist, be dumped, and
  be membership-guarded.
- The observed-power ban's Bayesian sibling (D-02) — named and D-13-deferred,
  no code this phase.
- The general doc/code agreement test (REQ-P20-04) — Phase 17's Boschloo
  regression test is explicitly its "down payment," not the general mechanism.
- Renaming `estimand_kind` — resolved, rejected, do not revisit.

</user_constraints>

<phase_requirements>

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-P17-01 | Boschloo reconciliation: `recommend_test`'s small-expected-cell fallback emits `boschloo_exact`; `boschloo_exact` joins `NONPARAMETRIC_TESTS`; pinned regression test | Exact two edits identified at `dsx/checks/stats.py:65` and `:23-26`; doc side (`references/test-selection.md:10`+footnote) confirmed already correct, needs no edit; regression-test shape specified below |
| REQ-P17-02 | `estimand_kind` closed 6-member vocabulary, additive to `ANALYSIS-SPEC.yaml`, absence non-blocking, both canonical fixtures extended, `dsx vocab` dumps it | Full placement analysis below: constant must live in `dsx/spec.py` (D-03a layering + `_VOCABULARIES` registry requirement); membership guard design options with a concrete recommendation; canonical fixtures identified precisely as `examples/good-ANALYSIS-SPEC.yaml` + `examples/bad-ANALYSIS-SPEC.yaml` |
| REQ-P17-03 | D-12a disposition table recorded | Already fully recorded in `17-CONTEXT.md` `## Decisions` D-02 — no further research or code needed; planner should treat this as complete on merge of CONTEXT.md, which is already committed (`2a6b7c8`) |
| REQ-P17-04 | D-06 range pre-allocation note + `time_to_event` fallthrough regression test | Range table already committed in `17-CONTEXT.md` D-03 (textually discharged); fallthrough guard target confirmed at `dsx/checks/stats.py:128-129`; test shape specified below |
| REQ-P17-05 | Zero new codes, asserted by set-identity diff | `tests/test_finding_catalogue_invariant.py` already implements exactly this mechanism against a frozen Phase-12 snapshot plus a named mint list; very likely already sufficient — verify it still passes unchanged after this phase's edits, see "Validation Architecture" |

</phase_requirements>

## Standard Stack

Not applicable in the conventional sense — this phase installs no package and
uses no library beyond the Python 3 standard library, matching the project's
own D-01/D-02 gate-path constraint ("Nothing here computes on data or touches
the gate path with pandas/scipy/numpy"). Confirmed: `python3 --version` on
this machine reports `3.14.6`; the test suite runs on stdlib `unittest`
(`python3 -m unittest discover -s tests -q`, confirmed working by running
`tests/test_no_shapiro_autoswitch.py` directly during this research session —
4 tests, all passed). No `pytest` is installed in this environment
(`No module named pytest`) — do not write `pytest`-only syntax (fixtures,
`@pytest.mark`, `assert` outside `unittest.TestCase`) into any new test file;
follow the `unittest.TestCase` convention every existing test file in
`tests/` uses.

## Package Legitimacy Audit

Not applicable. This phase installs zero external packages (Python standard
library only, on a stdlib-only gate path by standing project rule). No
`npm view` / `pip index versions` / registry check is needed.

## Architecture Patterns

### System Architecture Diagram

```
ANALYSIS-SPEC.yaml (analyst-authored, or a fixture)
        │
        ▼
dsx/loader.py::load()  ──────────────────────────────► parsed dict (spec)
        │
        ▼
dsx/spec.py::validate_structure(spec)
        │  - shape + closed-vocabulary checks (DSX-SPEC-*)
        │  - describe_vocabulary() is a SEPARATE read path, called by
        │    dsx/cli.py::cmd_vocab, not part of this validate call
        ▼
dsx/checks/stats.py::check(spec)
        │  - section(spec, "analysis") ──► _check_declared_test(analysis, spec, report)
        │        │
        │        ├─ analysis.outcome_type membership  (DSX-STA-040, existing)
        │        ├─ analysis.estimand_kind membership (DSX-STA-040, WIDENED — this phase)
        │        │
        │        └─ recommend_test(outcome_type, n_groups, paired, ...)  [pure function]
        │                 │
        │                 ├─ outcome == "proportion", n_groups <= 2
        │                 │     → _rec("two_proportion_z", ..., alternatives=[
        │                 │           "boschloo_exact (any expected cell < 5)",  ← THIS PHASE
        │                 │           "chi_square", "bootstrap"], ...)
        │                 │
        │                 └─ outcome == "time_to_event"  (unconditional final branch)
        │                       → _rec("log_rank", ...)   ← pinned by regression test, this phase
        │
        │  - declared test vs recommended test compared (DSX-STA-041, existing, untouched)
        ▼
Report (findings list)  ──────────────────────────────► dsx gate / dsx audit / dsx validate CLI output

references/test-selection.md  ── documentation mirror of the same routing table,
                                   read by humans, NOT parsed by any code path.
                                   Kept in sync by a regression TEST, not by
                                   generation, until REQ-P20-04 ships the
                                   general doc/code agreement mechanism.
```

### Recommended Project Structure

No new directories. Files touched or added:

```
dsx/
├── spec.py                    # add ESTIMAND_KINDS dict; register in _VOCABULARIES
├── checks/
│   └── stats.py                # NONPARAMETRIC_TESTS += boschloo_exact; alternatives
│                                # string fix; widen DSX-STA-040 into a membership loop
references/
└── test-selection.md          # no edit needed — already correct (S0-2 confirmed)
examples/
├── good-ANALYSIS-SPEC.yaml    # add one `estimand_kind:` line to the analysis: block
└── bad-ANALYSIS-SPEC.yaml     # add one `estimand_kind:` line to the analysis: block
templates/
└── ANALYSIS-SPEC.yaml         # add estimand_kind to the analysis: block scaffold, with
                                 # its allowed-values comment, matching outcome_type's style
tests/
├── test_boschloo_reconciliation.py   # NEW — pins REQ-P17-01 (naming per house style, see below)
├── test_estimand_kind_vocab.py       # NEW — pins REQ-P17-02, modelled on test_cuped_vocab.py
├── test_time_to_event_fallthrough.py # NEW — pins REQ-P17-04's fallthrough guard
└── test_finding_catalogue_invariant.py  # UNCHANGED — verify it still passes (REQ-P17-05)
```

### Pattern 1: One finding code, many checked fields (the multi-field membership loop)

**What:** `dsx/spec.py` already has this pattern twice. A single
`report.add("DSX-SPEC-082", ...)` call site sits inside a `for` loop over a
tuple of `(block_name, field_name, vocabulary)` triples; whichever field fails
membership, the SAME code fires with a field-name-interpolated message. The
catalogue generator (`scripts/gen-finding-catalogue.py`) extracts codes by
walking the AST for `report.add(...)` call sites — it finds this call site
**once**, regardless of how many times the loop invokes it at runtime, so
adding a new field to the loop's tuple never mints a new catalogue row.

**When to use:** Exactly the situation REQ-P17-02 creates — a new field
needs the same "loud, not silent" membership behaviour an existing field
already has, and REQ-P17-05 forbids a new code.

**Example (existing code, `dsx/spec.py:1165-1176` and `:1279-1298`):**
```python
# Source: dsx/spec.py (this repository, read during this research session)
_VALIDITY_FRAME_MEMBERSHIP: "tuple[tuple[str, str, Any], ...]" = (
    ("estimand", "type", ESTIMAND_TYPES),
    ("identification", "strength", IDENTIFICATION_STRENGTHS),
    # ... eight more triples ...
)

for block_name, field_name, vocab in _VALIDITY_FRAME_MEMBERSHIP:
    block = frame.get(block_name)
    if not isinstance(block, dict):
        continue
    value = block.get(field_name)
    if is_blank(value):
        continue                      # <-- absence is never blocking (matches D-10/D-01)
    if normalize(value) not in {normalize(k) for k in vocab}:
        report.add(
            "DSX-SPEC-082",
            "HIGH",
            f"validity_frame.{block_name}.{field_name} {value!r} is not recognised",
            detail="Allowed: " + ", ".join(sorted(vocab)),
            remedy=f"Set validity_frame.{block_name}.{field_name} to one of the allowed values.",
            where=f"spec.validity_frame.{block_name}.{field_name}",
        )
```

**Recommended widening of `DSX-STA-040` for `estimand_kind` (this phase's
implementation, sketched — not yet written):**
```python
# Sketch only — dsx/checks/stats.py, generalising the existing
# DSX-STA-040 check (currently lines 440-447) into the same loop shape.
_ANALYSIS_MEMBERSHIP = (
    ("outcome_type", OUTCOME_TYPES),
    ("estimand_kind", ESTIMAND_KINDS),   # imported from dsx.spec — see D-03a note below
)

def _check_analysis_membership(analysis: dict, report: Report) -> bool:
    """Returns False if outcome_type failed membership (existing callers need
    this to short-circuit recommend_test the same way they do today)."""
    outcome_ok = True
    for field_name, vocab in _ANALYSIS_MEMBERSHIP:
        value = analysis.get(field_name)
        if is_blank(value):
            continue
        if normalize(value) not in {normalize(k) for k in vocab}:
            report.add(
                "DSX-STA-040",
                "MEDIUM",
                f"analysis.{field_name} {value!r} is not recognised",
                detail="Allowed: " + ", ".join(sorted(vocab)),
                remedy=f"Declare analysis.{field_name} as one of the allowed values.",
                where=f"spec.analysis.{field_name}",
            )
            if field_name == "outcome_type":
                outcome_ok = False
    return outcome_ok
```

### Anti-Patterns to Avoid

- **Defining `ESTIMAND_KINDS` in `dsx/checks/stats.py` next to `OUTCOME_TYPES`.**
  This looks natural (both are routing vocabularies `recommend_test` will read)
  but it breaks REQ-P17-02's `dsx vocab` requirement: `describe_vocabulary()`
  in `dsx/spec.py` is the **only** function `cmd_vocab` calls, and it iterates
  a fixed `_VOCABULARIES` list defined in `dsx/spec.py`. A vocabulary living
  only in `dsx/checks/stats.py` would never appear in `dsx vocab` output
  unless `dsx/spec.py` imported it — which the codebase's own D-03a rule
  forbids (`dsx.spec` must never import `dsx.checks`; there is an AST-based
  test enforcing this boundary, referenced in `PROJECT.md`'s decision log as
  "M-04 Automated import test enforces the D-03a boundary"). The constant must
  be born in `dsx/spec.py`; `dsx/checks/stats.py` imports it from there, the
  same way it already imports `as_number`, `get`, `is_blank`, `items`,
  `normalize`, `section` from `..spec`.
- **Minting a new `DSX-SPEC-09x` or `DSX-STA-04x` code for the guard.** Adding
  a brand-new code is the obvious way to build a membership guard and is
  exactly what REQ-P17-05 forbids. The catalogue's zero-new-codes gate
  (`tests/test_finding_catalogue_invariant.py`) compares the live code **set**
  against a frozen snapshot plus a named, closed list of sanctioned mints —
  any new literal `report.add("DSX-STA-0xx", ...)` call site anywhere under
  `dsx/` fails that test immediately.
- **Checking `estimand_kind` only inside the existing early-return gate.**
  `_check_declared_test` (the function `DSX-STA-040` currently lives inside)
  opens with `if not declared or not outcome_type: return` — i.e. it does
  nothing at all unless `analysis.test` is ALSO declared. If the new
  `estimand_kind` membership check is nested inside that same early return, a
  spec that declares `analysis: {estimand_kind: bogus_value}` with no
  `test:`/`outcome_type:` field would get **no finding at all** — a silent
  no-op, which directly contradicts D-01's "never a silent no-op" language.
  The membership loop must run before, or independently of, that gate. See
  "Open Questions" below for the one behavioural risk this creates for the
  pre-existing `outcome_type` check.
- **Editing `references/test-selection.md`.** S0-2 already confirmed the doc
  side is correct (it names Boschloo, cites Lydersen-Fagerland-Laake 2009 §9,
  and the footnote is intact). D-04's direction is "reconcile to the doc" —
  the code changes, the doc does not.
- **Removing `fisher_exact` from `NONPARAMETRIC_TESTS`.** It is still the
  correct alternative for the 3+-group sparse-cell case
  (`dsx/checks/stats.py:69`, unrelated to this fix). Only the two-proportion
  small-cell alternative string (line 65) changes from `fisher_exact` to
  `boschloo_exact`; `boschloo_exact` is *added* to `NONPARAMETRIC_TESTS`,
  `fisher_exact` stays.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Detecting whether the finding-code catalogue gained or lost a code | A new bespoke diff script | `scripts/gen-finding-catalogue.py --check` + `tests/test_finding_catalogue_invariant.py`'s existing set-identity test | Both already exist, are already wired into `scripts/check.sh`, and already do exactly what REQ-P17-05 asks for (set-identity, not just count, comparison against a frozen snapshot) |
| Verifying nothing under `dsx/` calls a normality test on the decision surface | Ad hoc grep in the plan | `tests/test_no_shapiro_autoswitch.py`'s `DecisionSurfaceScanTest` pattern | Already-proven token-scan idiom scoped to `dsx/` and `skills/`, CRLF-safe; if the planner wants a similar "no silent no-op" structural scan for `estimand_kind`, this file is the template to copy, not reinvent |
| Regenerating `references/finding-codes.md` by hand after any `report.add` edit | Hand-editing the markdown table | `python3 scripts/gen-finding-catalogue.py --write` | The file's own header says "Do not edit by hand"; the AST-driven generator is the single source of truth and `--check` is a CI gate against drift |

**Key insight:** every mechanism this phase needs (vocabulary registry, code
dedup, doc/code pinning idiom, corpus discovery) already exists in this
codebase, proven by a passing test. The work is composition, not invention —
which is also why the phase mints zero new finding codes.

## Common Pitfalls

### Pitfall 1: Genericizing `DSX-STA-040`'s message text breaks nothing today, but verify it does not silently change `references/finding-codes.md`'s committed row text without regenerating it
**What goes wrong:** The current `DSX-STA-040` message is a hardcoded literal,
`f"analysis.outcome_type {outcome_type!r} is not recognised"`. Widening it to
`f"analysis.{field_name} {value!r} is not recognised"` changes the extracted
title text the catalogue generator captures (from a literal chunk to a
templated one), even though the **code** stays the same.
**Why it happens:** `scripts/gen-finding-catalogue.py`'s AST walker keeps
interpolated f-string segments as `<…>` placeholders and literal segments
verbatim — changing which parts are literal changes the rendered row text in
`references/finding-codes.md`, even with zero change to the code string.
**How to avoid:** After the edit, run `python3 scripts/gen-finding-catalogue.py --write`
and commit the regenerated `references/finding-codes.md`. Do **not** hand-edit
that file. Do **not** touch `tests/fixtures/finding-codes-phase12.md` — it is
explicitly "byte-frozen... never mutated" and is compared only by code **set**,
not text, so it is unaffected by a title-text change.
**Warning signs:** `scripts/gen-finding-catalogue.py --check` exits 1 with
"finding catalogue is stale" after the code edit but before regenerating.

### Pitfall 2: The `_check_declared_test` early-return gate silently exempts `outcome_type` from its own membership check today — decide deliberately whether `estimand_kind` inherits that gate
**What goes wrong:** `_check_declared_test(analysis, spec, report)` returns
immediately if `analysis.test` (or `analysis.outcome_type`) is blank — meaning
today, a spec that declares only `analysis: {outcome_type: nonsense}` with no
`test:` field produces **no** `DSX-STA-040` finding. This is pre-existing,
unrelated-to-this-phase behaviour (confirmed: no test in `tests/` pins
`DSX-STA-040` specifically, so this exact gap has no committed regression
protecting it either way).
**Why it happens:** the function was written to serve one purpose — compare a
declared test against `recommend_test`'s output — and the outcome_type
membership check was added inline as a guard clause for that purpose, not as
an independent contract check.
**How to avoid:** if the planner widens the check into a standalone loop that
runs before the early return (the recommended approach, since `estimand_kind`
must not be silently exempted), `outcome_type`'s behaviour changes too — it
will now fire even when `test` is absent. This is very likely a **desirable**
side effect (a stricter, more consistent contract) but it is a behavioural
change to existing, working code, not something CONTEXT.md explicitly
authorised. The planner should either (a) accept this as in-scope tightening
and add a test proving `outcome_type` now fires independently of `test`, or
(b) keep `outcome_type`'s check gated exactly as today and give
`estimand_kind` its own ungated check reusing the same `DSX-STA-040` code from
a second call — but a second static call site with a **different** literal
title text triggers `gen-finding-catalogue.py`'s "declared twice with
different text" warning (non-fatal, printed to stderr, but avoidable by using
identical f-string shape at both sites). Option (a) is cleaner and is this
research's recommendation.
**Warning signs:** a fixture in `examples/good-corpus/` or
`examples/known-bad/` that declares `analysis.outcome_type` without
`analysis.test` and currently expects zero `DSX-STA-040` findings — none was
found in this session's search, but the planner should grep
`analysis:` blocks across `examples/` before committing to option (a).

### Pitfall 3: `n_groups` default in `_check_declared_test` masks a possible mismatch when only `estimand_kind` is declared
**What goes wrong:** `_check_declared_test` reads
`n_groups = int(as_number(analysis.get("n_groups")) or 2)` — if a spec
declares `analysis: {estimand_kind: agreement}` with no `outcome_type`, no
`n_groups`, no `test`, the function still returns early (per Pitfall 2) before
this line is reached, so this is currently inert. It only becomes relevant if
the planner's chosen implementation moves the membership loop above the early
return; even then it does not affect the `estimand_kind` membership check
itself (a pure string-membership test, no dependency on `n_groups`).
**Why it happens:** `n_groups`'s default exists for the test-recommendation
path, not the membership-guard path.
**How to avoid:** keep the `estimand_kind` membership check a pure
`is_blank` / `normalize`-in-`vocab` test with no dependency on any other
`analysis:` field, exactly like every existing membership check in this
codebase (`_VALIDITY_FRAME_MEMBERSHIP`, `_INFERENCE_MEMBERSHIP`). Do not let
it read `n_groups` or `paired`.
**Warning signs:** none observed in the live tree; flagged because it is the
kind of coupling that is easy to introduce by accident when two checks share
a function.

## Code Examples

### The exact Boschloo edit sites (verified this session, `dsx/checks/stats.py`)

```python
# Source: dsx/checks/stats.py:23-26 — CURRENT state, confirmed by direct read
NONPARAMETRIC_TESTS = {
    "mann_whitney", "wilcoxon_signed_rank", "kruskal_wallis", "spearman_correlation",
    "fisher_exact", "mcnemar", "chi_square", "permutation_test", "bootstrap",
}
# CHANGE: add "boschloo_exact" to this set literal (keep fisher_exact — it is
# still the correct 3+-group sparse-cell alternative at line 69).
```

```python
# Source: dsx/checks/stats.py:62-67 — CURRENT state, confirmed by direct read
if n_groups <= 2:
    return _rec(
        "two_proportion_z",
        "Two independent proportions with adequate expected cell counts.",
        ["fisher_exact (any expected cell < 5)", "chi_square", "bootstrap"],
        "risk_difference + cohens_h",
    )
# CHANGE: replace "fisher_exact (any expected cell < 5)" with
# "boschloo_exact (any expected cell < 5)". This is the ONLY string that needs
# to change for REQ-P17-01's primary fix; recommend_test's PRIMARY returned
# test for n_groups<=2 stays "two_proportion_z" (matches the doc's "two-
# proportion z (Boschloo's exact test if any expected cell < 5)" row).
```

```python
# Source: dsx/checks/stats.py:463-465 — CURRENT state, confirmed by direct read.
# No change needed here — shown to prove the acceptable-alternatives check
# will correctly accept a declared "boschloo_exact" test once the string above
# changes, with zero further edits:
acceptable = {recommended} | {
    normalize(alt.split(" ")[0]) for alt in recommendation["alternatives"]
}
# alt.split(" ")[0] on "boschloo_exact (any expected cell < 5)" => "boschloo_exact"
```

### The exact `time_to_event` fallthrough target (verified this session)

```python
# Source: dsx/checks/stats.py:128-129 — CURRENT state, confirmed by direct read.
# This is the LAST statement in recommend_test(); every other outcome_type
# branch returns earlier. No `if outcome == "time_to_event":` guard exists —
# reaching this line is a fallthrough, not a match.
    return _rec("log_rank", "Time-to-event outcome with censoring.",
                ["cox_proportional_hazards", "restricted_mean_survival_time"], "hazard_ratio")
```

**Recommended regression test shape (modelled on
`tests/test_no_shapiro_autoswitch.py`'s dual behavioural + structural-scan
pattern):**
```python
# Sketch — tests/test_time_to_event_fallthrough.py
import re
import unittest
from dsx.checks import stats

class TimeToEventFallthroughTest(unittest.TestCase):
    def test_time_to_event_routes_to_log_rank(self):
        for n_groups in (1, 2, 3):
            for paired in (True, False):
                rec = stats.recommend_test("time_to_event", n_groups, paired=paired)
                self.assertEqual(rec["test"], "log_rank")

    def test_recommend_test_has_no_conditional_guard_on_time_to_event(self):
        # Structural pin: catches a future contributor adding a branch that
        # would silently change routing for some outcome/n_groups combination
        # without anyone updating this test.
        import inspect
        source = inspect.getsource(stats.recommend_test)
        self.assertNotRegex(
            source, r'outcome\s*==\s*["\']time_to_event["\']',
            "recommend_test must reach log_rank by unconditional fallthrough, "
            "not by an explicit time_to_event guard (REQ-P17-04)",
        )
```

### The exact `estimand_kind` vocab test shape (modelled on `tests/test_cuped_vocab.py`)

```python
# Sketch — tests/test_estimand_kind_vocab.py
import unittest
from dsx.spec import ESTIMAND_KINDS, describe_vocabulary

_MEMBERS = {
    "linear_association", "monotone_association", "nominal_association",
    "agreement", "method_comparison", "ordered_trend",
}

class EstimandKindVocabularyTest(unittest.TestCase):
    def test_estimand_kinds_is_exactly_six_members(self):
        self.assertEqual(set(ESTIMAND_KINDS), _MEMBERS)

    def test_vocab_dump_lists_estimand_kind(self):
        dumped = describe_vocabulary()["estimand_kind"]
        self.assertEqual(set(dumped), _MEMBERS)

    def test_absence_is_non_blocking(self):
        from dsx.checks import stats
        report = stats.check({"results": {}, "analysis": {}})
        self.assertFalse([f for f in report.findings if "estimand_kind" in f.message])

    def test_out_of_vocabulary_value_reports_loudly(self):
        # D-05-style marker if this check ends up sharing DSX-STA-040:
        # D-05: DSX-STA-040
        from dsx.checks import stats
        spec = {"analysis": {"outcome_type": "proportion", "estimand_kind": "not_a_real_kind"}}
        report = stats.check(spec)
        found = [f for f in report.findings if f.code == "DSX-STA-040"
                 and "estimand_kind" in f.message]
        self.assertEqual(len(found), 1)
```

## State of the Art

Not applicable — this phase repairs an internal defect and adds an internal
vocabulary; there is no external ecosystem or library version to track.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Widening `DSX-STA-040` into a membership loop (rather than some other zero-new-code mechanism) is the intended implementation of the "DSX-SPEC-082-style decidable error" language in `17-CONTEXT.md` D-01 | Architecture Patterns / Pattern 1, Summary | If the planner picks a different mechanism, no functional harm — but this document's concrete recommendation (and the sketch code) would need adaptation; re-verify the AST/catalogue mechanics hold for whatever mechanism is actually chosen |
| A2 | Moving the `estimand_kind`/`outcome_type` membership check above `_check_declared_test`'s early-return gate is safe (no existing fixture currently relies on `outcome_type` membership being silently skipped when `test` is absent) | Common Pitfalls / Pitfall 2 | Low — no test currently pins the exempted behaviour, but the planner should still grep `examples/` for an `analysis:` block with `outcome_type` and no `test` before committing, since this research's grep pass may have missed a fixture added between S0-2 and now |
| A3 | `examples/good-ANALYSIS-SPEC.yaml` and `examples/bad-ANALYSIS-SPEC.yaml` are "both canonical fixtures" referenced by REQ-P17-02/D-08, as opposed to some pair inside `examples/good-corpus/` or `examples/known-bad/` | Standard Stack / Architecture / throughout | Medium if wrong — confirmed by REQ-P20-02's singular "the good fixture" language and by these two files' outsized reuse across `tests/test_dsx.py`, `tests/test_frame_val.py`, `tests/test_causal_verb_golden.py` and `scripts/check.sh`'s own gate smoke test, but the exact phrase "both canonical fixtures" is not defined verbatim anywhere in `.planning/`; if wrong, the fixture-extension task targets the wrong two files |

**If this table is empty:** N/A — see above; both entries are implementation-mechanism inferences, not factual claims about the live tree (everything else in this document was read directly from the repository during this session).

## Open Questions

1. **Where should the three new regression tests live — one file each, or folded into `tests/test_dsx.py`?**
   - What we know: this codebase has both patterns. `tests/test_dsx.py` is a
     large multi-topic file that already hosts the existing `DSX-STA-041`/`043`
     tests. But every recently-added, single-topic vocabulary or invariant
     test in this tree (`test_cuped_vocab.py`, `test_no_shapiro_autoswitch.py`,
     `test_effect_size_kind.py`, `test_finding_catalogue_invariant.py`) is its
     own small file.
   - What's unclear: whether the project has an unstated rule for which
     pattern applies when.
   - Recommendation: three small, single-purpose files (as sketched above) —
     it matches the majority of recent additions, keeps each regression
     traceable to its requirement in the file name, and avoids growing an
     already-large `test_dsx.py` further. Non-blocking either way; the planner
     can choose freely.

2. **Should the D-06 range pre-allocation get a reinforcing code comment in `dsx/checks/stats.py`, given `17-CONTEXT.md` is already committed?**
   - What we know: `17-CONTEXT.md` (containing the full D-03 range table) is
     already committed to this branch (commit `2a6b7c8`, confirmed in the
     provided git log). REQ-P17-04 says the note must be "committed" — that
     bar looks already cleared.
   - What's unclear: whether "committed note" was meant to require a
     machine-discoverable pointer closer to the code the ranges will be drawn
     from (so a Phase 18/19 author does not have to know to look in an old
     phase's CONTEXT.md).
   - Recommendation: add a short comment block near
     `dsx/checks/stats.py`'s `PARAMETRIC_TESTS`/`NONPARAMETRIC_TESTS`
     constants pointing at `.planning/phases/17-.../17-CONTEXT.md` D-03 for the
     reserved `DSX-STA-050`–`139` range. Low-cost, not required by any test,
     purely a discoverability improvement — planner's discretion.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3 | Everything | Yes | 3.14.6 | — |
| `unittest` (stdlib) | Test execution | Yes | stdlib, ships with Python | — |
| `pytest` | Not used by this project | No | — | N/A — project uses stdlib `unittest` exclusively; do not introduce `pytest` syntax |
| Git Bash / POSIX sh | `scripts/check.sh` | Yes (confirmed — this research session ran shell commands successfully) | — | On native PowerShell, run the two commands inside `check.sh` individually rather than the `.sh` script itself |

No missing dependencies block this phase.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Python stdlib `unittest` (no `pytest` installed or used anywhere in this repo) |
| Config file | none — tests are discovered by `unittest discover -s tests` |
| Quick run command | `python3 -m unittest tests.<module_name> -v` (e.g. `python3 -m unittest tests.test_time_to_event_fallthrough -v`) |
| Full suite command | `python3 -m unittest discover -s tests -q` (this is exactly what `scripts/check.sh` runs first) |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| REQ-P17-01 | `recommend_test("proportion", 2)`'s alternatives name `boschloo_exact`; `boschloo_exact` is a member of `NONPARAMETRIC_TESTS`; `references/test-selection.md` still names Boschloo (doc↔code pin) | unit | `python3 -m unittest tests.test_boschloo_reconciliation -v` | ❌ Wave 0 — new file |
| REQ-P17-02 (vocab exists, dumped) | `ESTIMAND_KINDS` has exactly 6 named members; `describe_vocabulary()["estimand_kind"]` returns the same 6 | unit | `python3 -m unittest tests.test_estimand_kind_vocab -v` | ❌ Wave 0 — new file |
| REQ-P17-02 (absence non-blocking) | `analysis: {}` (no `estimand_kind`) produces zero `estimand_kind`-related findings | unit | same file as above | ❌ Wave 0 — new file |
| REQ-P17-02 (membership guard fires) | `analysis: {estimand_kind: "not_a_real_kind"}` produces exactly one loud finding naming `analysis.estimand_kind` | unit | same file as above | ❌ Wave 0 — new file |
| REQ-P17-02 (fixtures extended) | `examples/good-ANALYSIS-SPEC.yaml` still passes every gate threshold with the new `estimand_kind:` line present | integration | `python3 -m unittest tests.test_good_fixture_phase15 -v` (existing file, no change needed — just re-run after the fixture edit) | ✅ pre-existing |
| REQ-P17-03 | D-12a table recorded | manual-only (documentation review) | N/A — `17-CONTEXT.md` review, already committed | ✅ complete |
| REQ-P17-04 (fallthrough pin) | `recommend_test("time_to_event", ...)` always returns `log_rank`, and no `if outcome == "time_to_event"` guard exists in source | unit | `python3 -m unittest tests.test_time_to_event_fallthrough -v` | ❌ Wave 0 — new file |
| REQ-P17-04 (range note) | D-03 table present in committed `17-CONTEXT.md` | manual-only | N/A — already committed (`2a6b7c8`) | ✅ complete |
| REQ-P17-05 | Live catalogue code set equals frozen Phase-12 snapshot plus the same sanctioned-mint list as before (no addition, no removal) | unit | `python3 -m unittest tests.test_finding_catalogue_invariant -v` | ✅ pre-existing — verify it still passes unchanged after this phase's edits |
| REQ-P17-05 (build gate) | `references/finding-codes.md` is not stale relative to the AST-extracted code set | build script | `python3 scripts/gen-finding-catalogue.py --check` | ✅ pre-existing |

### Sampling Rate
- **Per task commit:** run the single new test module touched by that task
  (e.g. `python3 -m unittest tests.test_boschloo_reconciliation -v` right
  after the Boschloo edit), plus
  `python3 -m unittest tests.test_finding_catalogue_invariant -v` on any task
  that touches a `report.add(...)` call site, since that is the cheapest early
  signal for an accidental code mint.
- **Per wave merge:** `python3 -m unittest discover -s tests -q`.
- **Phase gate:** `scripts/check.sh` in full (or its four steps run
  individually on native PowerShell) before `/gsd-verify-work` — this also
  exercises the good/bad fixture gate smoke test at all four gate points
  (`plan`, `execute`, `verify`, `ship`), which is the strongest available
  proof that the extended fixtures did not regress.

### Wave 0 Gaps
- [ ] `tests/test_boschloo_reconciliation.py` — covers REQ-P17-01
- [ ] `tests/test_estimand_kind_vocab.py` — covers REQ-P17-02
- [ ] `tests/test_time_to_event_fallthrough.py` — covers REQ-P17-04's fallthrough half
- [ ] No framework install needed — stdlib `unittest` is already the whole
      house convention, confirmed working this session.

## Security Domain

`security_enforcement` is `true` in `.planning/config.json` (`security_asvs_level: 1`,
`security_block_on: "high"`), so this section is required even though this
phase has no obvious security surface.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | This phase touches no authentication code; `dsx` is a local CLI/library with no auth surface anywhere in the tree |
| V3 Session Management | No | No session concept exists in this codebase |
| V4 Access Control | No | No access-control surface; file-based CLI |
| V5 Input Validation | Yes, but unchanged | `estimand_kind`'s membership guard IS an input-validation control — it is being *added*, not weakened, and follows the exact closed-set/normalize/membership pattern every other spec field already uses (never a regex against free text, never a fuzzy match — `dsx/frame/admissibility.py`'s own docstring calls this out as a deliberate anti-pattern-avoidance: "no distance, containment, prefix or any other approximate match") |
| V6 Cryptography | No | No cryptographic operation anywhere in this phase |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| A closed-vocabulary check implemented as substring/fuzzy match instead of exact-after-normalize equality, letting a malformed or adjacent value silently pass | Tampering (of the validation contract itself, not of external input) | Exact `normalize(value) not in {normalize(k) for k in vocab}` equality check only — this is the pattern every existing vocabulary guard in `dsx/spec.py` already uses; do not introduce `in`/substring/`startswith` matching for `estimand_kind` |
| A membership guard silently skipped when a sibling field is absent, converting an intended "loud" error into a silent no-op | Repudiation (the tool "silently" accepts a bad value with no record) | The explicit design point in Pitfall 2 above — decide deliberately whether the guard runs unconditionally or is gated, and add a test either way, rather than let the early-return's existing shape decide by accident |
| Regenerated `references/finding-codes.md` committed out of sync with the real `report.add(...)` call sites | Tampering (documentation drifting from enforced behaviour) | `scripts/gen-finding-catalogue.py --check` as a build gate — already wired into `scripts/check.sh`; run it after every `report.add` edit |

This phase introduces no new attack surface (no network call, no
deserialization of untrusted input beyond the existing YAML spec loader it
already uses unchanged, no new file write path, no new subprocess, no new
credential or secret).

## Sources

### Primary (HIGH confidence — read directly from the live tree during this session)
- `dsx/checks/stats.py` — full file read; Boschloo, `NONPARAMETRIC_TESTS`,
  `recommend_test`, `_check_declared_test`, `DSX-STA-040/041/042/043` all
  confirmed at the line numbers cited above
- `dsx/spec.py` — full file read (two passes, ~1486 lines); `QUESTION_TYPES`,
  `ESTIMAND_TYPES`, `_VOCABULARIES`, `_VALIDITY_FRAME_MEMBERSHIP`,
  `_INFERENCE_MEMBERSHIP`, `describe_vocabulary()`, the D-03a import-boundary
  comment, all confirmed
- `dsx/frame/admissibility.py` — full file read; confirms
  `validity_frame.estimand.type` is read at a wholly separate site/block from
  where `analysis.estimand_kind` will be read, supporting D-01's orthogonality
  claim
- `dsx/cli.py` — grepped for `vocab`; confirms `cmd_vocab` calls
  `describe_vocabulary()` and nothing else
- `references/test-selection.md` — full file read; Boschloo table row and
  footnote `[^1]` confirmed intact and correct
- `references/finding-codes.md` and `scripts/gen-finding-catalogue.py` — full
  files read; catalogue generation, dedup-by-code, and the 260-code total
  mechanism confirmed
- `examples/good-ANALYSIS-SPEC.yaml` and `examples/bad-ANALYSIS-SPEC.yaml` —
  both read; `analysis:` block shape confirmed in each
- `tests/test_no_shapiro_autoswitch.py`, `tests/test_cuped_vocab.py`,
  `tests/test_known_bad_corpus.py`, `tests/test_finding_catalogue_invariant.py`,
  `tests/test_gen_finding_catalogue.py`, `tests/test_good_fixture_phase15.py` —
  all read to establish house test-style conventions
- `scripts/check.sh` — full file read; confirms the phase-gate command
  sequence and the good/bad fixture smoke test at all four gate points
- `.planning/phases/17-foundation-repairs-and-spec-vocabulary/17-CONTEXT.md`,
  `.planning/REQUIREMENTS.md`, `.planning/STATE.md`,
  `.planning/v2.3-SCOPE-RECHECK.md`, `.planning/config.json` — all read in full
- Live shell checks this session: `python3 --version` (3.14.6),
  `python3 -m unittest tests.test_no_shapiro_autoswitch -v` (4/4 passed,
  proving the stdlib-`unittest` runner works from repo root), confirming
  `pytest` is not installed

### Secondary (MEDIUM confidence)
- None used — no web research was performed for this phase per the task's
  own instruction not to pad with generic external research on a pure
  internal-repair phase.

### Tertiary (LOW confidence)
- None.

## Metadata

**Confidence breakdown:**
- Boschloo reconciliation (REQ-P17-01): HIGH — every locator directly read
  and cross-checked against the pre-existing S0-2 scope-recheck document,
  which itself re-verified the same locators independently
- `estimand_kind` vocabulary placement and membership-guard mechanism
  (REQ-P17-02): HIGH on the placement constraint (D-03a layering is an
  enforced, tested boundary — not a matter of opinion); MEDIUM on the exact
  membership-guard implementation choice, because CONTEXT.md specifies the
  *outcome* ("loud, DSX-SPEC-082-style") but not the *mechanism*, and this
  research's recommended mechanism (widen `DSX-STA-040`) is the most
  code-consistent option found, not the only conceivable one — flagged as A1
  in the Assumptions Log
- D-12a table and D-06 range note (REQ-P17-03/04's documentation halves):
  HIGH — both already committed, directly confirmed via git log and file read
- `time_to_event` fallthrough and set-identity diff (REQ-P17-04/05's test
  halves): HIGH — exact target lines confirmed by direct read;
  `test_finding_catalogue_invariant.py`'s existing mechanism confirmed by
  direct read to already implement the REQ-P17-05 requirement verbatim

**Research date:** 2026-08-29
**Valid until:** This phase is a point-in-time repair of a specific, already
S0-2-verified tree state. The research is valid as long as no other work
lands on `gsd/v2.3.0-test-catalog` between this research and Phase 17
execute that touches `dsx/checks/stats.py`, `dsx/spec.py`, or
`references/finding-codes.md`. Re-verify the exact line numbers cited above
immediately before executing if any such change has landed.
