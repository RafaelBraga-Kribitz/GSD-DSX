---
phase: 09-monitoring-discipline-symmetric-dsx-par
reviewed: 2026-08-13T00:00:00Z
depth: deep
files_reviewed: 13
files_reviewed_list:
  - dsx/frame/__init__.py
  - dsx/frame/paradigm.py
  - dsx/mathx.py
  - dsx/spec.py
  - examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml
  - examples/known-bad/bayesian-continuous-monitoring-POSTMORTEM.md
  - examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml
  - examples/known-bad/frequentist-uncontrolled-continuous-POSTMORTEM.md
  - references/finding-codes.md
  - references/paradigm-symmetry.md
  - templates/ANALYSIS-SPEC.yaml
  - tests/test_dsx.py
  - tests/test_known_bad_corpus.py
  - tests/test_par_monitoring_simulation.py
findings:
  critical: 2
  warning: 3
  info: 1
  total: 6
status: issues_found
---

# Phase 9: Code Review Report

**Reviewed:** 2026-08-13T00:00:00Z
**Depth:** deep
**Files Reviewed:** 13
**Status:** issues_found

## Summary

The `DSX-PAR-010`/`DSX-PAR-011` pair itself is genuinely symmetric: one dict
(`_MONITORING_DISCIPLINE`), one shared clearing predicate
(`_blank_clearing_declarations`), one code path for both severities and both
retype directions — the tests that pin this (`TestPhase9MonitoringDiscipline`
in `tests/test_dsx.py`, the `_retype_and_gate` tests, and the known-bad
corpus's per-fixture contract in `tests/test_known_bad_corpus.py`) hold up
under tracing. `DSX-PAR-002`'s presence/membership split with `DSX-SPEC-085`
also holds on every path I traced: a bogus `paradigm_justification` value is
always caught by one code or the other, never neither. `tests/test_par_monitoring_simulation.py`
stays off the gate path, proven by its own AST-walking test and confirmed by
reading `dsx/frame/paradigm.py` end to end (no import of `tests`).

Two problems survive that tracing. First, the shared clearing predicate
(`is_blank()` in `dsx/spec.py`, reused unmodified by `_blank_clearing_declarations`)
does not treat numeric `0`, `0.0`, or `False` as blank — so `alpha_spending: 0`,
`prior_justification: false`, or the shared `threshold_calibration: 0` clears
the CRITICAL-severity pair with a value that carries zero declared content,
on both paradigms equally (confirmed by direct execution, not just reading).
Second, the finding text `DSX-PAR-011` actually emits at gate time attributes
the `1/(K+1)` bound to "Theorem 1" — the exact locator error the same
function's own docstring, three sentences earlier, and
`references/paradigm-symmetry.md` both explicitly warn against (the bound is
unnumbered prose at Section 3.2, not something Theorem 1 states directly).
Both are concrete, reproducible defects, not stylistic quibbles.

## Critical Issues

### CR-01: `alpha_spending`/`prior_justification`/`threshold_calibration` can be cleared with a bare `0` or `false`, defeating the CRITICAL gate on both paradigms

**File:** `dsx/spec.py:369-376` (`is_blank()`), reused by `dsx/frame/paradigm.py:94-104` (`_blank_clearing_declarations`)

**Issue:** `_blank_clearing_declarations()` is the sole predicate deciding
whether `DSX-PAR-010`/`DSX-PAR-011` fire — the module's docstring calls this
"the mechanical proof of cost symmetry." It delegates entirely to
`dsx.spec.is_blank()`:

```python
def is_blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) == 0
    return False
```

`is_blank()` has no branch for `int`, `float`, or `bool` — any such value
falls through to `return False`, i.e. "not blank." Because the three
clearing declarations (`alpha_spending`, `prior_justification`,
`threshold_calibration`) are documented as "free-text scalar" fields with no
type check enforcing that, declaring any of them as a bare number or boolean
satisfies the clearing condition with literally zero declared justification.
Verified by direct execution against the shipped code:

```
>>> is_blank(0), is_blank(False), is_blank(0.0)
(False, False, False)

>>> spec = {"design": {"peeking_policy": "uncontrolled_continuous"},
...         "inference": {"threshold_calibration": 0}}
>>> {f.code for f in paradigm.check(spec).findings}
{'DSX-PAR-001', 'DSX-PAR-002'}   # neither DSX-PAR-010 nor DSX-PAR-011 fires
```

This does **not** break the pair's symmetry — both halves use the same
predicate, so the escape is identically cheap on both sides, preserving
brief D-12's equal-cost requirement. But it undermines the requirement
itself: `references/paradigm-symmetry.md` describes the cheapest dishonest
fix as "type any non-blank string" — typing a bare `0` is cheaper still, and
arguably not even a considered act of dishonesty, just an operator filling
in a placeholder-looking value. The codebase already knows this class of
pitfall exists — `dsx.spec.as_number()` explicitly special-cases `bool`
before the general numeric branch to avoid a related `True`/`False`
coercion bug — but that same discipline was not applied to `is_blank()`.

**Fix:** Require the three clearing declarations to be non-blank *strings*
specifically, not just "not `is_blank()`" over any type — either a local
check in `_blank_clearing_declarations()`:

```python
def _blank_clearing_declarations(inference: dict, fields: tuple[str, ...]) -> list[str]:
    return [
        name for name in fields
        if not isinstance(inference.get(name), str) or is_blank(inference.get(name))
    ]
```

or a small, generically-named helper in `dsx/spec.py` (e.g.
`is_blank_text(value)`) that both this call site and any future free-text
clearing field can share, so the fix does not live only in `dsx/frame/paradigm.py`.

### CR-02: `DSX-PAR-011`'s emitted finding text attributes the `1/(K+1)` bound to "Theorem 1" — the locator error the module's own docstring warns against

**File:** `dsx/frame/paradigm.py:244-253`

**Issue:** The `detail=` text actually shipped in the `DSX-PAR-011` finding
(verified by executing `paradigm.check()` directly) reads:

> "Under the prior-averaged formulation (Deng, Lu & Chen 2016, Theorem 1),
> the risk of false discovery at a P(B>A) > 0.95 decision threshold is
> bounded by 1/(K+1) = 1/20 = 0.05 at K = 19 — a fixed reference anchor..."

This ties the specific numeric bound `1/(K+1)` directly to "Theorem 1" in
one clause. But the same function's docstring, three sentences above this
code (`dsx/frame/paradigm.py:149-155`), states explicitly:

> "Theorem 1 states the optional-stopping equality that licenses this figure
> under known prior odds; the bound itself... is unnumbered prose
> immediately following Theorem 1 and again in the paper's Section 3.2, so
> citing Theorem 1 alone for the number 1/(K+1) would be a locator error."

`references/paradigm-symmetry.md` makes the identical distinction ("Theorem
1 itself states an optional-stopping equality, not the bound directly — the
bound is unnumbered prose... and citing Theorem 1 alone for the number
1/(K+1) would be a locator error"). The bayesian post-mortem gets this
right too. Only the actual, user-facing `report.add(detail=...)` text — the
thing an operator reads when `dsx gate plan` blocks — commits the exact
error the rest of this phase was built to prevent (brief D-05: "naming one
would be the fabricated locator brief D-05 exists to prevent," applied
elsewhere in this same file to the Armitage citation). This is not a
documentation nit: it is the shipped, user-visible output of a CRITICAL
check misattributing a citation, inside the one file that most carefully
argues against doing exactly that.

**Fix:** Rephrase the `detail=` string so the number is attributed the same
way the docstring and the audit document already attribute it, e.g.:

```python
detail=(
    "design.peeking_policy is uncontrolled_continuous: interim "
    "looks continue with no sequential correction and no "
    "anytime-valid method. Under the prior-averaged formulation "
    "(Deng, Lu & Chen 2016), the risk of false discovery at a "
    "P(B>A) > 0.95 decision threshold is bounded by 1/(K+1) = "
    "1/20 = 0.05 at K = 19 (Theorem 1 licenses this bound under "
    "optional stopping; the bound itself is stated in unnumbered "
    "prose following Theorem 1 and again in Section 3.2) — a fixed "
    "reference anchor, never a computation over any "
    "operator-declared value."
),
```

## Warnings

### WR-01: `design.alpha: 0` is silently replaced by the 0.05 default via Python's falsy-`or` idiom

**File:** `dsx/frame/paradigm.py:206`

**Issue:**

```python
alpha = as_number(get(spec, "design.alpha")) or 0.05
```

`as_number(0)` returns `0.0`, and `0.0 or 0.05` evaluates to `0.05` because
`0.0` is falsy in Python — the fallback fires even though the operator
explicitly declared a real (if statistically odd) `alpha` value. Verified:

```
>>> paradigm.check({"design": {"peeking_policy": "uncontrolled_continuous",
...                            "alpha": 0},
...                  "inference": {"paradigm": "frequentist"}})
# DSX-PAR-010 detail text reads "at a nominal alpha of 0.05" — not 0.00
```

`alpha=0` is a degenerate edge case in practice, so the blast radius is
small, but the pattern is the classic "falsy default" pitfall — `is None`
is the correct guard here, not `or`, and using `or` for a *numeric* default
is exactly the kind of bug `as_number`'s own explicit `bool` special-case
elsewhere in `dsx/spec.py` shows this codebase already knows to avoid.

**Fix:**

```python
alpha_value = as_number(get(spec, "design.alpha"))
alpha = 0.05 if alpha_value is None else alpha_value
```

### WR-02: `references/finding-codes.md` silently drops one of `DSX-PAR-002`'s two distinct trigger messages

**File:** `references/finding-codes.md:354`, generated from `dsx/frame/paradigm.py:344-389`

**Issue:** `_check_paradigm_justification` has two mutually-exclusive
`report.add("DSX-PAR-002", ...)` call sites with two different title
strings — "inference.paradigm (<…>) is declared with no
paradigm_justification" and "inference.paradigm is not declared under an
uncontrolled continuous design." `scripts/gen-finding-catalogue.py::collect()`
extracts both (confirmed by reading its AST-walk logic), but then
deduplicates by code with last-write-wins:

```python
seen: dict[str, tuple[str, str, str, str]] = {}
for row in rows:
    if row[0] in seen and seen[row[0]][1:] != row[1:]:
        print(f"warning: {row[0]} declared twice with different text", file=sys.stderr)
    seen[row[0]] = row
```

so only the second message survives into `references/finding-codes.md` —
the "declared with no justification" case (arguably the more common,
higher-signal trigger of the two) never appears in the generated catalogue
at all. The generator does print a warning, but nothing in
`tests/test_gen_finding_catalogue.py` asserts on that warning or on stderr
being empty, so this silently regressed the catalogue's completeness with
no test failure. A reader relying on `references/finding-codes.md` — which
opens with "**Total: 224 codes**," implying a complete enumeration — gets an
incomplete picture of what `DSX-PAR-002` actually covers.

**Fix:** Either render both titles for one code (e.g. join with `" / "` in
`render()`), or make `check_d05`/the test suite fail when `collect()` would
print a "declared twice with different text" warning, so a future
multi-message code fails the build instead of silently losing a message.

### WR-03: The `DSX-PAR-001` counterfactual for a declared paradigm hard-codes "the other paradigm" as a single value

**File:** `dsx/frame/paradigm.py:493-503`

**Issue:**

```python
other_paradigms = [p for p in PARADIGMS if p != paradigm]
if paradigm:
    ...
    other = other_paradigms[0] if other_paradigms else None
```

This works correctly today because `PARADIGMS` has exactly two members, so
`other_paradigms` never has more than one element. But the module's own
comments elsewhere are emphatic about `PARADIGMS`-keyed structures being
"data, not an if/else," specifically so "a future `PARADIGMS` addition...
fails loudly instead of silently under-reporting." This one spot does not
have that property: adding a third paradigm would make `other_paradigms[0]`
silently describe only one of the two real alternatives in the
counterfactual text, with no test failure to flag it (unlike
`_MONITORING_DISCIPLINE` and `_PARADIGM_CONDITIONAL`, which do have
set-equality tests against `PARADIGMS`).

**Fix:** Either loop over all of `other_paradigms` in the counterfactual
text, or add a test asserting `len(PARADIGMS) == 2` (documenting the
assumption this code silently relies on) so a third paradigm addition
surfaces this spot for a required edit.

## Info

### IN-01: `is_blank()`'s numeric/boolean gap is a pre-existing helper, not new to this phase — worth a wider audit

**File:** `dsx/spec.py:369-376`

**Issue:** `is_blank()` is used across many other `DSX-SPEC-*` checks (e.g.
`decision.decision_rule`, `metric.definition`), where a `0` or `False` value
is plausibly meaningful data rather than a dodge, so this gap is not unique
to Phase 9. Phase 9 is where it first becomes load-bearing for a
CRITICAL-severity, presence-only, "the frame that lies passes" gate whose
entire design intent is a symmetric, free-text clearing declaration (per
`references/paradigm-symmetry.md`) — which is why CR-01 above is scoped to
this phase's usage rather than proposing a blanket change to `is_blank()`'s
general semantics (which would need its own audit across every caller).

**Fix:** No action beyond CR-01's fix; noting this so a future audit of
`is_blank()` callers elsewhere in the checks does not treat CR-01 as the
only instance of this class of gap.

---

_Reviewed: 2026-08-13T00:00:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep_
