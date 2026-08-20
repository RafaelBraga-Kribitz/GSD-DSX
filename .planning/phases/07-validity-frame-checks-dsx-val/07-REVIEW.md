---
phase: 07-validity-frame-checks-dsx-val
reviewed: 2026-08-20T00:04:46Z
depth: deep
files_reviewed: 16
files_reviewed_list:
  - dsx/cli.py
  - dsx/frame/paradigm.py
  - dsx/frame/val.py
  - dsx/mathx.py
  - dsx/spec.py
  - examples/good-ANALYSIS-SPEC.yaml
  - examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
  - examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml
  - examples/known-bad/weak-identification-mmm-POSTMORTEM.md
  - references/finding-codes.md
  - scripts/check_brief_refs.py
  - scripts/gen-finding-catalogue.py
  - templates/ANALYSIS-SPEC.yaml
  - tests/test_dsx.py
  - tests/test_frame_boundary.py
  - tests/test_frame_val.py
  - tests/test_known_bad_corpus.py
findings:
  critical: 1
  warning: 4
  info: 1
  total: 6
resolved:
  - id: CR-01
    commits: [e523a70, 2160cde]
    date: 2026-08-20
status: issues_found
---

# Phase 07: Code Review Report

**Reviewed:** 2026-08-20T00:04:46Z
**Depth:** deep
**Files Reviewed:** 16 (plus cross-referenced `tests/test_dsx.py` sections, `dsx/frame/interference.py` name-checks, `dsx/suppressions.py::known_codes()`)
**Status:** issues_found

## Summary

Phase 07 adds `dsx/frame/val.py` (the ten `DSX-VAL-*` validity-frame content
checks) and the supporting `dsx/frame/paradigm.py` monitoring-discipline pair
(`DSX-PAR-010`/`DSX-PAR-011`), plus the closed vocabularies and structural
shape checks in `dsx/spec.py` that back them. The module is unusually well
tested (the `tests/test_frame_val.py` fixture-matrix, citation-obligation,
and D-11 import/paradigm-read boundary tests are genuinely load-bearing), and
the great majority of the conditional logic in `val.py` traces correctly
against both the good fixture and the three `known-bad` fixtures.

Adversarial tracing through edge cases not covered by the existing test
suite — an out-of-vocabulary `inference.paradigm` value, a negative
`design.alpha`, and the finding-catalogue generator's handling of a code
declared with two different severities — surfaced one reproducible logic bug
in `dsx/frame/paradigm.py` (the DSX-PAR-001 manifest can assert a check
"was not selected" while that very check fired as CRITICAL in the same
report) and several lower-severity correctness/quality gaps. None of the
issues found flip a gate's exit code incorrectly — the CRITICAL/HIGH
blocking behaviour of `DSX-VAL-*`/`DSX-PAR-*` is intact — but the manifest
honesty defect directly contradicts the design goal (`D-10`) that module's
own docstring states as its reason to exist.

## Critical Issues

### CR-01: DSX-PAR-001's applied/not-applied manifest is factually wrong for an out-of-vocabulary `inference.paradigm` value, while DSX-PAR-002 silently stops firing for the same input

**File:** `dsx/frame/paradigm.py:458-469` (`check()`) and `dsx/frame/paradigm.py:363,386` (`_check_paradigm_justification`)

**Issue:** `check()`'s selection logic only special-cases two states of `paradigm`:

```python
selected: "set[str]" = set(_PARADIGM_INDEPENDENT)
if paradigm in _PARADIGM_CONDITIONAL:
    selected.update(_PARADIGM_CONDITIONAL[paradigm])
elif not paradigm:
    for prefixes in _PARADIGM_CONDITIONAL.values():
        selected.update(prefixes)
```

A third state is reachable and untested: `paradigm` is a non-blank string
that is *not* a member of `PARADIGMS` (a typo such as `"bayesain"`, or any
other free text — `inference.paradigm` has no enum enforcement blocking
`plan`, only `DSX-SPEC-085` at HIGH, which does not block `plan`'s CRITICAL
threshold). For that state neither branch above fires, so `selected` stays
just `_PARADIGM_INDEPENDENT` — meaning `DSX-PAR-010`, `DSX-PAR-011` and
`DSX-ADM-` are all reported as **"not applied"**, each with the message
`"not selected for the declared paradigm"`.

`_check_monitoring_discipline` (the function that actually decides whether
`DSX-PAR-010`/`DSX-PAR-011` fire) handles the same third state differently
and correctly:

```python
if paradigm in _MONITORING_DISCIPLINE:
    rows = {paradigm: _MONITORING_DISCIPLINE[paradigm]}
else:
    rows = dict(_MONITORING_DISCIPLINE)   # both rows — same as "undeclared"
```

So for an out-of-vocabulary paradigm, `_check_monitoring_discipline` treats
it exactly like an undeclared paradigm and evaluates (and can fire) *both*
`DSX-PAR-010` and `DSX-PAR-011`, while `check()`'s manifest claims neither is
applicable. Reproduced directly:

```
$ python -c "
from dsx.frame import paradigm
spec = {'inference': {'paradigm': 'bayesain'},
        'design': {'peeking_policy': 'uncontrolled_continuous'}}
report = paradigm.check(spec)
print([f.code for f in report.findings])
f = [x for x in report.findings if x.code == 'DSX-PAR-001'][0]
print(f.data['not_applied'])
"
['DSX-PAR-001', 'DSX-PAR-010', 'DSX-PAR-011']
{'DSX-ADM-': 'Phase 11 ships DSX-ADM-* ...',
 'DSX-PAR-010': 'not selected for the declared paradigm',
 'DSX-PAR-011': 'not selected for the declared paradigm', ...}
```

`DSX-PAR-010` and `DSX-PAR-011` are both listed as CRITICAL findings in the
same `report.findings`, while the DSX-PAR-001 finding in that identical
report states they were "not selected." The manifest's whole reason to
exist, per this file's own module docstring, is "for every gate run, names
which check families applied given the declared `inference.paradigm`... and
which did not — and why," specifically so that "an operator's honest
`bayesian` never costs more than a dishonest ... declaration" (D-10). A
manifest that asserts the opposite of what the same run actually evaluated
is a correctness defect in exactly the property this file exists to
guarantee, not a cosmetic one.

The same missing third branch causes a second, related symptom:
`_check_paradigm_justification`'s two mutually exclusive branches —
`paradigm in PARADIGMS` and `not paradigm` — both evaluate false for an
out-of-vocabulary paradigm, so `DSX-PAR-002` (HIGH, the requiredness check
for `paradigm_justification`/paradigm declaration under an uncontrolled
design) silently never fires for this input, even though the design is
uncontrolled and no valid paradigm was actually declared:

```
$ python -c "
from dsx.frame import paradigm
spec = {'inference': {'paradigm': 'bayesain'},
        'design': {'peeking_policy': 'uncontrolled_continuous'}}
print([f.code for f in paradigm.check(spec).findings])
"
['DSX-PAR-001', 'DSX-PAR-010', 'DSX-PAR-011']   # no DSX-PAR-002
```

No test in `tests/test_dsx.py`'s `TestPhase6ParadigmManifest` or the
Phase 9 monitoring-pair test class exercises an out-of-vocabulary
`inference.paradigm` value — every test uses either a valid `PARADIGMS`
member or a blank/absent one — so this gap is not caught by the existing
(otherwise thorough) suite.

**Fix:** Treat "non-blank and not a `PARADIGMS` member" identically to
"undeclared" in both places, the same way `_check_monitoring_discipline`
already does — e.g. in `check()`:

```python
selected: "set[str]" = set(_PARADIGM_INDEPENDENT)
if paradigm in _PARADIGM_CONDITIONAL:
    selected.update(_PARADIGM_CONDITIONAL[paradigm])
else:
    # blank OR out-of-vocabulary: every paradigm-conditional family applies,
    # matching _check_monitoring_discipline's own fallback branch.
    for prefixes in _PARADIGM_CONDITIONAL.values():
        selected.update(prefixes)
```

and in `_check_paradigm_justification`, change `elif not paradigm and
policy == _UNCONTROLLED_POLICY:` to `elif paradigm not in PARADIGMS and
policy == _UNCONTROLLED_POLICY:` (adjusting the message to distinguish
"undeclared" from "unrecognised" if desired). Add a regression test with
`inference.paradigm` set to a non-blank, out-of-vocabulary string under
`design.peeking_policy: uncontrolled_continuous`, asserting the manifest's
`not_applied` never contradicts findings that actually fired in the same
report, and that `DSX-PAR-002` still fires.

**Resolved 2026-08-20** — `test(07)` e523a70 pinned the defect (12 subtest
failures across the manifest honesty invariant, the applied-set fallback and
the `DSX-PAR-002` requiredness half, on four out-of-vocabulary values);
`fix(07)` 2160cde folded the unrecognised case into the undeclared one in both
`check()` and `_check_paradigm_justification`, keying on `PARADIGMS` membership
after `normalize()` — the same fallback `_check_monitoring_discipline` already
used. `DSX-PAR-001`'s detail gained a third branch naming the unrecognised
case. Membership *reporting* stays `DSX-SPEC-085`'s (D-08): T-9-14 passes
unchanged. Full suite 549 tests OK; `gen-finding-catalogue.py --check` exit 0.

## Warnings

### WR-01: `dsx/frame/val.py::check()` hand-duplicates every sub-check's blocking predicate to build decision records, risking silent drift

**File:** `dsx/frame/val.py:231-556`

**Issue:** After dispatching to the nine private `_check_*` helper
functions (each of which independently computes its own blocking
condition and calls `report.add(...)`), `check()` recomputes the *same*
blocking condition a second time, by hand, for every sub-block, purely to
build a `DecisionRecord`'s `choice` string (e.g. `triad_blocked`,
`drift_blocked`, `dependence_blocked`, `weak_blocked`/`strong_flagged`,
`sampling_frame_blocked`, `missingness_blocked`, `measurement_blocked`).
Today these ~9 duplicated predicates all agree with their corresponding
`_check_*` function (verified by tracing each one), but they are two
independent code paths that must be kept in sync by hand forever — exactly
the failure mode this codebase goes out of its way to avoid elsewhere (see
`paradigm.py`'s `_blank_clearing_declarations`, whose docstring calls out
"no per-paradigm and no per-field code path exists anywhere in the pair" as
the mechanical proof of D-12 symmetry). A future edit to one of `val.py`'s
`_check_*` functions (e.g. adding a new clearing condition to
`_check_dependence`) that is not mirrored in `check()`'s duplicate block
would silently produce a `DecisionRecord` that disagrees with the actual
finding — undermining the decision-trail (`dsx explain`) the whole
`DecisionRecord` mechanism exists to keep trustworthy.

**Fix:** Have each `_check_*` function return (or the dispatcher derive) the
blocking boolean and use it both to decide whether to `report.add(...)` and
to build the `DecisionRecord`, rather than re-deriving the condition from
scratch in `check()`. At minimum, add a comment at each duplicated block
noting which `_check_*` function it must be kept identical to, and a test
that fails if they diverge (mirroring the spirit of
`test_editing_only_validity_frame_never_changes_which_design_codes_fire` in
`tests/test_frame_val.py`).

### WR-02: `scripts/gen-finding-catalogue.py` silently drops one of two title/severity variants when a code is emitted from more than one call site — affects `DSX-VAL-021` and `DSX-VAL-060` from this phase

**File:** `scripts/gen-finding-catalogue.py:159-164` (`collect()`); observable in `references/finding-codes.md`

**Issue:** `collect()`'s dedup only prints a non-failing warning to stderr
when the same code is declared with different severity/title text, then
silently keeps whichever call site was visited last:

```python
for row in rows:
    if row[0] in seen and seen[row[0]][1:] != row[1:]:
        print(f"warning: {row[0]} declared twice with different text", file=sys.stderr)
    seen[row[0]] = row
```

Running `python scripts/gen-finding-catalogue.py --check` today prints:

```
warning: DSX-VAL-021 declared twice with different text
warning: DSX-VAL-060 declared twice with different text
finding catalogue is current
```

— confirmed by direct execution. `dsx/frame/val.py::_check_unit_drift`
emits `DSX-VAL-021` with two different titles ("validity frame *assignment*
unit disagrees with design randomization unit" vs "validity frame
*analysis* unit disagrees with design analysis unit"); the catalogue
(`references/finding-codes.md`) documents only the second. Likewise
`_check_missingness` emits `DSX-VAL-060` at `HIGH` for the MAR/deny case and
at `CRITICAL` for the MNAR/allow case; the catalogue documents only
`CRITICAL`. An analyst reading `references/finding-codes.md` — the
project's own stated single source of truth for "every check emits findings
with a stable code" — has no way to discover that `DSX-VAL-060` can also
fire at HIGH, or that `DSX-VAL-021` covers two distinct disagreements. This
pattern predates Phase 07 (`DSX-COH-030`, `DSX-PAR-002`, `DSX-SPEC-070` show
the same warning), so it is a pre-existing generator limitation rather than
a wholly new defect, but this phase added two more instances of it and
`--check` treats it as non-fatal, so it will keep silently recurring.

**Fix:** Either (a) make `collect()` fail (non-zero exit under `--check`)
when a code's severity/title text disagrees across call sites, forcing an
explicit per-variant naming convention (e.g. `DSX-VAL-060` documented as
"HIGH or CRITICAL depending on mechanism"), or (b) extend the row shape to
carry every distinct (severity, title) pair per code and render them as
multiple rows/one row with a combined severity cell.

### WR-03: `inflation_from_peeking()` has no bounds check on `alpha`, letting an out-of-range `design.alpha` produce a nonsensical negative "type-I error" figure inside a CRITICAL finding's evidentiary text

**File:** `dsx/mathx.py:411-453` (`inflation_from_peeking`); consumed at `dsx/frame/paradigm.py:219-221`

**Issue:** Unlike its sibling functions in the same module
(`sample_size_two_proportions`, `power_two_proportions`, `z_two_sided`, all
of which call `_check_prob(alpha, "alpha")`), `inflation_from_peeking` never
validates that `alpha` is in `(0, 1]`. It only clamps the upper bound:
`return min(1.0, value * alpha / 0.05)`. `_check_monitoring_discipline`
computes `alpha = as_number(get(spec, "design.alpha")) or 0.05` with no
range check either, so a spec declaring an invalid `design.alpha` (e.g. a
typo like `-1`, or any negative value) flows straight through into the
CRITICAL `DSX-PAR-010` finding's `detail` text as a fabricated negative
probability. Reproduced directly:

```
$ python -c "
from dsx.frame import paradigm
spec = {'inference': {}, 'design': {'peeking_policy': 'uncontrolled_continuous', 'alpha': -1}}
print([f.detail for f in paradigm.check(spec).findings if f.code == 'DSX-PAR-010'][0])
"
...at a nominal alpha of -1.00, the true type-I error is approximately
-2.840 at five interim looks and -4.960 at twenty...
```

`DSX-PAR-010` still correctly fires (the gate still blocks), and
`DSX-EXP-003` ("alpha is outside a sane range") independently flags the bad
`design.alpha` value elsewhere in the report — but this specific finding's
own citation-grade evidentiary text (the module goes to considerable
lengths elsewhere to keep every reference value honest and independently
verified, per its own D-05 citation discipline) prints a self-evidently
impossible negative "type-I error," which undermines exactly the honesty
guarantee the rest of the module is built around.

**Fix:** Either have `inflation_from_peeking` validate `0 < alpha <= 1` (raising, matching its siblings), or have `_check_monitoring_discipline` clamp/validate `alpha` before use and fall back to the documented 0.05 nominal value when the declared `design.alpha` is out of range, rather than passing a raw unchecked number through to a citation-quality finding.

### WR-04: `as_number(...) or 0.05` collapses a legitimately-declared `design.alpha: 0` into the 0.05 default

**File:** `dsx/frame/paradigm.py:219`

**Issue:**

```python
alpha = as_number(get(spec, "design.alpha")) or 0.05
```

`as_number(0)` returns `0.0`, which is falsy in Python, so `0.0 or 0.05`
evaluates to `0.05` — an explicitly declared `design.alpha: 0` is silently
replaced by the 0.05 default rather than being used (or rejected) as
declared. The correct pattern is an explicit `None` check:
`raw = as_number(...); alpha = raw if raw is not None else 0.05`. This
exact anti-pattern is already present at four other call sites in the
codebase (`dsx/checks/stats.py:143`, `dsx/checks/design.py:452,459`,
`dsx/checks/decision.py:106`), so it is a systemic, pre-existing convention
rather than something newly introduced by this phase — flagged here because
it is present in a file under review and because `alpha: 0` (while a
degenerate value no honest design would declare) is exactly the kind of
falsy-but-declared numeric value `is_blank()`'s own docstring elsewhere in
this codebase is explicit about needing to treat as "meaningful data," not
absence.

**Fix:** Replace the `or` idiom with an explicit `is not None` check at
this call site, and consider a shared helper (`as_number_or(value, default)`)
in `dsx/spec.py` so the other four call sites can be fixed the same way
without four separate edits.

## Info

### IN-01: `dsx/frame/val.py`'s module docstring miscounts the family as "nine planned codes" when ten codes ship

**File:** `dsx/frame/val.py:13-26`

**Issue:** The module docstring states: "Two of the family's nine planned
codes shipped in plan 07-03 ... two more shipped in plan 07-04 ... Plan
07-05 added three more ... This plan (07-06) adds the last three ... All
nine planned codes now exist behind the same `check()` dispatcher." Counting
the codes actually named across those four sentences (`DSX-VAL-010`,
`-011`, `-020`, `-021`, `-030`, `-040`, `-041`, `-050`, `-060`, `-070`)
gives ten, matching both `references/finding-codes.md`'s ten-row `DSX-VAL-*`
table and the ten codes `dsx/frame/val.py` itself emits. "Nine" is stale —
likely left over from an earlier plan revision before the identification
pair (`DSX-VAL-040`/`DSX-VAL-041`) was split into two codes.

**Fix:** Change "nine planned codes" / "All nine planned codes" to "ten"
in the module docstring.

---

_Reviewed: 2026-08-20T00:04:46Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep_
