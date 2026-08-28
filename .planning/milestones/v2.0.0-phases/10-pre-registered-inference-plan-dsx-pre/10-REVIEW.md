---
phase: 10-pre-registered-inference-plan-dsx-pre
reviewed: 2026-08-20T02:07:28Z
depth: deep
files_reviewed: 14
files_reviewed_list:
  - dsx/cli.py
  - dsx/frame/paradigm.py
  - dsx/frame/prereg.py
  - dsx/spec.py
  - examples/known-bad/post-hoc-procedure-switch-ANALYSIS-SPEC.yaml
  - examples/known-bad/post-hoc-procedure-switch-POSTMORTEM.md
  - references/finding-codes.md
  - scripts/gen-finding-catalogue.py
  - tests/_trail_seed.py
  - tests/test_dsx.py
  - tests/test_frame_interference.py
  - tests/test_frame_prereg.py
  - tests/test_frame_val.py
  - tests/test_known_bad_corpus.py
findings:
  critical: 1
  warning: 1
  info: 2
  total: 4
status: issues_found
---

# Phase 10: Code Review Report

**Reviewed:** 2026-08-20T02:07:28Z
**Depth:** deep
**Files Reviewed:** 14
**Status:** issues_found

## Summary

Phase 10 adds `dsx/frame/prereg.py` (`DSX-PRE-010/020/030`), registers `prereg` in the
`verify`/`ship` gate profiles, wires `gate_invocation`/`reconcile_trail` through
`dsx/cli.py`, and extends `dsx/spec.py` with the closed `PREREG_FACTS` registry. The
grammar (`_parse_fallback_rule`), the branch resolver (`_resolve_branch`), and the two
"trail-independent" findings (`DSX-PRE-010`, `DSX-PRE-030`) are correct, CRLF-safe, and
match their extensive test coverage (`tests/test_frame_prereg.py`, 630 tests /
1058 subtests green, `gen-finding-catalogue.py --check` clean, D-05 citations present).
The known-bad fixture pair (`post-hoc-procedure-switch-*`) is internally consistent with
`dsx/frame/prereg.py`'s logic and its own committed postmortem.

One genuine functional defect was found and is rated Critical: the exit-2 message and
docstrings for `_check_content_lock`'s missing-plan-time-header guard claim a
`suppressions[]` "grandfather route" that does not exist in the code — declaring a
suppression never avoids this specific `CheckError`, verified empirically against a live
`dsx gate verify` run. This directly contradicts the phase's own stated design goal (the
M-07 grandfather path must "stay walkable") and shipped without detection because the
only test covering the message (`TestMissingPlanHeader::test_4`) checks for the
substring `"suppressions"`, never that a declared suppression actually works. A second,
lower-severity finding covers a case-sensitivity gap in fact-name resolution. Two info
items round out maintainability observations.

## Narrative Findings (AI reviewer)

## Critical Issues

### CR-01: The `suppressions[]` "grandfather route" named in the missing-plan-header exit-2 message does not function

**File:** `dsx/frame/prereg.py:433-505`
**Issue:**

`_check_content_lock` raises `CheckError` unconditionally whenever
`_recorded_plan_digests(root)` is empty — i.e. whenever no `dsx gate plan` invocation
has ever written a header into this root's `DECISIONS.jsonl` (lines 489-505). The
raised message's fourth clause reads:

```
"...If this specification legitimately predates the plan gate, declare a
`suppressions[]` entry citing the architecture decision record or specification
that is its authority (the ADR/SPEC authority requirement); an unknown code in
that block aborts the run at exit 2 in the same way."
```

The docstring above the function (lines 433-444) and the phase's own planning record
(`10-CONTEXT.md`, `10-03-PLAN.md` threat T-10-10) both assert this is how a pre-v2.0.0
spec that never ran `dsx gate plan` is meant to "stay walkable" through `verify`/`ship`
(the M-07 grandfather path).

This claim is false as implemented. `apply_suppressions()` (`dsx/suppressions.py`) only
ever filters findings already present in a completed `Report`, and it is called from
`run_checks()` *after* every named check — including `prereg.check()` — has returned
without raising. `_check_content_lock` raises its `CheckError` directly, before any
`DSX-PRE-*` finding is created and before `run_checks()` reaches `merge()`/
`apply_suppressions()` at all. No code anywhere in `dsx/frame/prereg.py` reads
`spec.get("suppressions")`. Confirmed empirically: a spec cloned from
`examples/good-ANALYSIS-SPEC.yaml` with an added
`suppressions: [{code: DSX-PRE-020, reason: ..., authority: ADR-999}]` entry, run against
a phase directory with no recorded plan header, still exits 2 with the exact same
message — the suppression has zero effect:

```
$ dsx gate verify --spec ... --phase-dir ...
dsx: no plan-time frame lock is recorded in the decision trail at ... — dsx gate plan
has never run against this phase directory ... declare a `suppressions[]` entry ...
exit code: 2
```

This is not limited to `declared_at: pre_data` specs — the guard fires for *any* spec
reaching `verify`/`ship` (including one with no `inference:` block at all, or an
explicit `declared_at: post_data`) whose root has never recorded a plan-time header,
since the empty-`recorded` check runs before `declared_at` is even read (line 490 vs.
508-510). That makes this the universal precondition for every spec entering `verify`
or `ship` from this phase forward, not a narrow edge case — which raises the stakes of
the message being wrong.

The gap shipped undetected because the only test exercising this message
(`tests/test_frame_prereg.py::TestMissingPlanHeader::test_4_message_names_suppressions_and_authority_and_trail_path`)
only asserts the literal word `"suppressions"` appears in the exception text; no test in
the suite ever declares an actual `suppressions[]` entry and checks whether it changes
the outcome.

An operator who genuinely has a pre-v2.0.0 spec and follows the tool's own advice
(declaring a `suppressions[]` entry with an ADR/SPEC authority, exactly as instructed)
will not be unblocked, will see the identical exit 2, and has no way to tell from the
message that the advice they just followed is inert. The only remedy that actually
works — running `dsx gate plan` against the phase directory, even retroactively (this
always writes a plan-time `InvocationHeader` regardless of whether `plan` itself passes
or blocks, since `_write_decision_trail` runs unconditionally in `dsx/cli.py::cmd_gate`)
— is presented in the message as merely "the ordinary fix," not as the only fix.

**Fix:**

Pick one of two consistent options; do not leave the current mismatch between claim and
code.

Option A — make the grandfather route real (keep D-09's "never silently pass" spirit by
still requiring an authority-backed entry, not a bare presence check):

```python
def _has_grandfather_suppression(spec: dict) -> bool:
    rows = spec.get("suppressions")
    if not isinstance(rows, list):
        return False
    return any(
        isinstance(row, dict)
        and row.get("code") == "DSX-PRE-020"
        and not is_blank(row.get("authority"))
        for row in rows
    )

...
    if not recorded:
        if _has_grandfather_suppression(spec):
            return  # or: still emit DSX-PRE-020-shaped context, but do not raise
        trail_display = ...
        raise CheckError(...)
```

Option B (simpler, and consistent with T-10-10's own "not mitigated by letting the
missing header pass" note) — stop claiming a functional bypass exists. Rewrite the
message and the function/module docstrings to state plainly that the only remedy is
running `dsx gate plan` against this phase directory (retroactively is sufficient — it
writes a header even when `plan` itself blocks), and drop the `suppressions[]` sentence
entirely, or reword it to something that is true, e.g. "there is currently no
suppression-based bypass for a missing plan-time header; run `dsx gate plan` first."
Update `10-03-PLAN.md`'s T-10-10 disposition and `_check_content_lock`'s docstring to
match, and extend `TestMissingPlanHeader` with a test that declares a real
`suppressions[]` entry and asserts the actual (non-)effect on the exit code, so this
class of claim/behavior drift cannot ship silently again.

## Warnings

### WR-01: Fact-name lookup in the fallback-rule mini-language is case-sensitive, unlike the rest of the contract's vocabulary matching

**File:** `dsx/frame/prereg.py:173` (`_resolve_branch`), regex at `dsx/frame/prereg.py:35-39`
**Issue:**

`_CONDITION_RE`'s `fact` group (`[A-Za-z_][A-Za-z0-9_]*`) accepts mixed-case identifiers,
but the registry lookup immediately after, `PREREG_FACTS.get(parsed.fact)`, is a
case-sensitive dict lookup against `PREREG_FACTS`'s all-lowercase keys
(`alpha`, `comparisons_looked_at`, `interim_looks`). Every other closed-vocabulary
comparison in this codebase goes through `dsx.spec.normalize()` (lower-cases and
underscores) before membership is tested — this is the one comparison in the
`fallback_rule` mini-language that does not.

Confirmed: a rule such as `"Alpha <= 0.05 -> two_proportion_z"` (capitalized only) fires
`DSX-PRE-010` at CRITICAL — "fallback_rule references fact 'Alpha', which is outside the
closed prereg fact registry; accepted names are: alpha, ..." — even though `alpha` is a
registered fact and the only difference is capitalization:

```
DSX-PRE-010 CRITICAL fallback_rule references fact 'Alpha', which is outside the
closed prereg fact registry; accepted names are: alpha, comparisons_looked_at,
interim_looks
```

This is a plausible authoring slip (a fact name copied from a report heading, or typed
with a leading capital out of habit) that produces a CRITICAL, gate-blocking finding at
`verify`/`ship` for a spec whose fallback rule is semantically correct — inconsistent
with how forgiving the rest of the contract's vocabulary matching is, and undocumented:
neither the remedy text nor `references/finding-codes.md` mentions that fact names are
case-sensitive.

**Fix:** Normalize `parsed.fact` before the registry lookup, e.g.:

```python
_PREREG_FACTS_NORMALIZED = {normalize(k): v for k, v in PREREG_FACTS.items()}
...
path = _PREREG_FACTS_NORMALIZED.get(normalize(parsed.fact))
```

(building the normalized map once at module scope, mirroring how `_UNKNOWN_FACT`'s
accepted-names list is already built from `sorted(PREREG_FACTS)` at import time).

## Info

### IN-01: `_check_rule_resolves` re-parses the fallback rule a second time

**File:** `dsx/frame/prereg.py:228-235`
**Issue:** `_resolve_branch` already calls `_parse_fallback_rule` once to compute
`resolution`. `_check_rule_resolves` calls it a second time, purely to recover `path`
for the decision record's `inputs` list, when `fired` is true. Both calls are on the
same deterministic input and cannot disagree today, so this is not a live bug, but it is
duplicated logic that a future refactor (e.g. caching, or `_parse_fallback_rule`
gaining any non-pure behavior) could silently desynchronize.
**Fix:** Have `_resolve_branch` return the parsed `path` (or the full `_ParsedRule`)
alongside `_Resolution`, so `_check_rule_resolves` consumes it rather than re-deriving
it.

### IN-02: Tests seed `DECISIONS.jsonl` into permanent repository directories, not a temp dir

**File:** `tests/test_dsx.py:1404-1410, 1447-1454, 1584-1587, 3427-3433`; `tests/test_frame_interference.py:631-634`
**Issue:** Several of the new `seed_plan_header(...)` call sites write into
`examples/DECISIONS.jsonl` and `templates/DECISIONS.jsonl` — real paths inside the
working tree, not a `TemporaryDirectory`. The file is gitignored, so there is no commit
risk, but every local test run appends another `InvocationHeader` line, and nothing ever
truncates or rotates the file, so it grows unboundedly across repeated local runs (this
pattern already existed pre-Phase-10 via `dsx gate plan`/`ship` calls against the same
paths, so Phase 10 extends rather than introduces it).
**Fix:** Where practical, prefer seeding into a scratch copy of `examples/`/`templates/`
(as `tests/test_frame_interference.py`'s existing `shutil.copytree`-based tests already
do elsewhere in the same file) rather than the tracked directories themselves, or add a
`tearDown`/fixture step that truncates the seeded trail file after the test class runs.

---

_Reviewed: 2026-08-20T02:07:28Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep_
