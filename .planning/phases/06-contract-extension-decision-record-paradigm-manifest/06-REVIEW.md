---
phase: 06-contract-extension-decision-record-paradigm-manifest
reviewed: 2026-08-08T00:00:00Z
depth: deep
files_reviewed: 22
files_reviewed_list:
  - dsx/cli.py
  - dsx/decisions.py
  - dsx/frame/__init__.py
  - dsx/frame/paradigm.py
  - dsx/loader.py
  - dsx/spec.py
  - examples/bad-ANALYSIS-SPEC.yaml
  - examples/good-ANALYSIS-SPEC.yaml
  - examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml
  - examples/known-bad/bayesian-continuous-monitoring-POSTMORTEM.md
  - examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml
  - examples/known-bad/frequentist-uncontrolled-continuous-POSTMORTEM.md
  - examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
  - examples/known-bad/interference-shared-budget-POSTMORTEM.md
  - references/finding-codes.md
  - scripts/gen-finding-catalogue.py
  - templates/ANALYSIS-SPEC.yaml
  - tests/fixtures/d05/bad_check.py
  - tests/test_decisions.py
  - tests/test_dsx.py
  - tests/test_frame_boundary.py
  - tests/test_gen_finding_catalogue.py
  - tests/test_known_bad_corpus.py
findings:
  critical: 2
  warning: 3
  info: 1
  total: 6
status: issues_found
---

# Phase 6: Code Review Report

**Reviewed:** 2026-08-08
**Depth:** deep
**Files Reviewed:** 22
**Status:** issues_found

## Summary

Reviewed the full Phase 6 body of work: the `validity_frame:`/`inference:` spec
contract (`dsx/spec.py`), the append-only decision-record substrate
(`dsx/decisions.py`), the `dsx/frame/` import-boundary package and its
`DSX-PAR-001` paradigm manifest, the `dsx explain` subcommand and gate-path
trail write (`dsx/cli.py`), D-05 mechanical enforcement
(`scripts/gen-finding-catalogue.py`), and the known-bad seed corpus. The 270
existing unit tests all pass, and the design of the shape validators, the
honesty invariants around the paradigm manifest, and the append/fsync +
tolerant-reader durability model are all sound in the cases the test suite
exercises.

Two BLOCKER-level defects were found and independently reproduced by running
the actual CLI (not just reading code): (1) `dsx explain` and the gate-path
trail writer both violate their own documented "never blocks / can never
change the exit code" contracts when `DECISIONS.jsonl` contains bytes that
are not valid UTF-8 — the reader's tolerant-line-skip only tolerates
JSON-level truncation, not encoding-level corruption, and the one call site
that is supposed to be exception-proof (`cmd_explain`) has no exception
handling around the read at all; and (2) all three `examples/known-bad/*`
fixtures, and their paired POSTMORTEM.md files, assert a specific, testable
claim ("passes every gate at every severity threshold" / "today's dsx
validate/gate checks pass it") that is false — every one of the three
fixtures blocks `dsx gate verify` and `dsx gate ship` today, for reasons
unrelated to the documented target defect, and the test suite only exercises
`dsx validate` (structural-only) against this corpus, never `dsx gate`, so
the false claim was never caught.

Three WARNING-level and one INFO-level maintainability issues are also
recorded below.

## Critical Issues

### CR-01: `dsx explain` and the gate-path trail writer crash instead of degrading gracefully on a non-UTF-8 `DECISIONS.jsonl`

**File:** `dsx/decisions.py:117` (root cause), consumed by `dsx/cli.py:413` (`cmd_explain`) and `dsx/cli.py:275-308` (`_write_decision_trail`)

**Issue:** `read_all()` does:

```python
for line in p.read_text(encoding="utf-8").splitlines():
```

`Path.read_text(encoding="utf-8")` raises `UnicodeDecodeError` (a `ValueError`
subclass) if the file contains any byte sequence that is not valid UTF-8.
`read_all()`'s only exception handling is `except json.JSONDecodeError`
around the per-line `json.loads()` call (line 123) — it does **not** guard
the `read_text()` call itself, so a decode error propagates out of
`read_all()` and out of `next_invocation_id()` (which calls `read_all()`).

This breaks two explicitly documented invariants:

1. **`dsx explain`** (`dsx/cli.py:393-406`) is documented as "a pure reader …
   never blocks, always returns 0". `cmd_explain` calls
   `read_all(decisions_path(root))` at line 413 with **no** try/except around
   it at all. A corrupted trail file makes `dsx explain` exit 2 instead of 0.
2. **`_write_decision_trail`** (`dsx/cli.py:275-308`), the function that
   writes the gate-path trail, is documented as: "the write is a side
   channel, never part of the block contract, so it can never change
   `point`'s exit code." Its `try/except OSError` (line 289-308) does not
   catch `UnicodeDecodeError`, so a corrupted trail file turns a spec that
   would otherwise pass or fail cleanly into an exit-2 operational error —
   exactly the outcome the docstring says can never happen.

Reproduced end-to-end against the real CLI:

```
$ python3 -c "
import tempfile, sys
from pathlib import Path
sys.path.insert(0, '.')
from dsx import cli
from dsx.decisions import append, InvocationHeader

with tempfile.TemporaryDirectory() as tmp:
    trail = Path(tmp) / 'DECISIONS.jsonl'
    append(trail, InvocationHeader(invocation_id='INV-0001', gate_point='plan',
                                    dsx_version='x', frame_digest='y'))
    with open(trail, 'ab') as fh:
        fh.write('café'.encode('utf-8')[:-1])   # truncated multi-byte tail
    print('explain exit:', cli.main(['explain', '--phase-dir', tmp]))
"
dsx: invalid input — 'utf-8' codec can't decode byte 0xc3 in position 126: unexpected end of data
explain exit: 2
```

The same corrupted-file setup makes `dsx gate plan --spec <a spec that would
otherwise pass>` exit 2 instead of 0 (verified directly against
`examples/good-ANALYSIS-SPEC.yaml`).

Note on real-world likelihood: `append()` writes via
`json.dumps(record.to_dict(), sort_keys=True)`, and `json.dumps` defaults to
`ensure_ascii=True`, so every byte `dsx` itself ever writes to
`DECISIONS.jsonl` is plain ASCII — a crash strictly *during `dsx`'s own
`append()` call* cannot by itself produce this exact failure mode (an ASCII
prefix truncated anywhere is still valid UTF-8, so it degrades to the
already-handled `JSONDecodeError` path). The gap is real regardless, though:
it fires on any other source of invalid bytes in the file — hand-editing,
disk/filesystem corruption of a byte that was already written (the scenario
the module's own docstring explicitly claims to guard against: "an
unparseable trailing line … is skipped, not fatal, so one crash never
invalidates every record written before it"), or any future change that sets
`ensure_ascii=False` or otherwise writes non-ASCII content. Given `dsx
explain`'s contract has zero carve-outs ("always returns 0"), this is a
genuine, provable contract violation today, not merely theoretical.

**Fix:** Make `read_all()` itself tolerant of encoding errors, matching its
existing "tolerant reader" design for JSON-level corruption — the minimal
fix is a one-line change:

```python
def read_all(path: "str | Path") -> "list[dict]":
    p = Path(path)
    if not p.exists():
        return []
    records: "list[dict]" = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        ...
```

`errors="replace"` guarantees `read_text()` never raises; any line whose
content was corrupted enough to need replacement characters will then
harmlessly fail `json.loads()` and be skipped by the existing
`except json.JSONDecodeError` path, preserving every intact record before
and after it. As defense in depth, also widen
`_write_decision_trail`'s `except OSError` (`dsx/cli.py:306`) — the
docstring's invariant ("can never change `point`'s exit code") is broader
than `OSError` alone covers (e.g. a future decisions-dict shape drift would
raise `TypeError` from `DecisionRecord(**fields)` at line 305, which is
likewise uncaught today).

### CR-02: `examples/known-bad/*` fixtures and their POSTMORTEM.md files assert a false, falsifiable claim about gate behavior

**File:** `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml:4`, `examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml:4`, `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml:2`, `examples/known-bad/interference-shared-budget-POSTMORTEM.md:59` (test coverage gap: `tests/test_known_bad_corpus.py:82-90`)

**Issue:** All three known-bad spec files carry a header comment of the form:

> "The file is structurally valid — it parses, and today's dsx validate/gate
> checks pass it — but it …"

and the interference postmortem states the claim explicitly and
unambiguously:

> "which is exactly why this fixture passes every gate at every severity
> threshold as of this phase."

This is false today. Running the actual CLI against all three committed
fixtures:

```
bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml       plan     exit=0
bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml       execute  exit=0
bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml       verify   exit=1   <-- BLOCK
bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml       ship     exit=1   <-- BLOCK
frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml  plan     exit=0
frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml  execute  exit=0
frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml  verify   exit=1   <-- BLOCK
frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml  ship     exit=1   <-- BLOCK
interference-shared-budget-ANALYSIS-SPEC.yaml           plan     exit=0
interference-shared-budget-ANALYSIS-SPEC.yaml           execute  exit=0
interference-shared-budget-ANALYSIS-SPEC.yaml           verify   exit=1   <-- BLOCK
interference-shared-budget-ANALYSIS-SPEC.yaml           ship     exit=1   <-- BLOCK
```

(`examples/good-ANALYSIS-SPEC.yaml`, run the same way, is `exit=0` at all
four gate points, confirming the harness itself is not at fault.)

Each fixture blocks at `verify`/`ship` on several HIGH findings that are
**unrelated to the documented target defect**, e.g. for
`interference-shared-budget-ANALYSIS-SPEC.yaml`:

```
[HIGH] DSX-CLM-031  Evidence pointer does not resolve to an existing file
[HIGH] DSX-COH-031  Assumption[0] is neither checked nor waived
[HIGH] DSX-MET-040  Warehouse-like source has no sql definition
[HIGH] DSX-NAR-001  Claims declared but narrative.path is missing
[HIGH] DSX-REP-030  No analysis entrypoint declared
```

None of these five is `DSX-INT-010` (the Phase 8 code the fixture exists to
motivate) — they're incidental gaps (no `narrative.path`, no
`reproducibility.entrypoint`, an unwaived assumption, a missing evidence
file, a warehouse metric with no `sql:`) that have nothing to do with the
interference/SUTVA defect the corpus is documented to encode. The same
pattern holds for the other two fixtures (missing entrypoint, missing
narrative path, an unassessed-assumptions parametric test, etc.).

`tests/test_known_bad_corpus.py::test_every_spec_passes_dsx_validate` (lines
82-90) only runs `dsx validate` (the structural-only `spec` check via
`cmd_validate`) against the corpus — it never runs `dsx gate` or `dsx audit`,
so this false claim was never caught by CI. This matters beyond prose
accuracy: the postmortems' own "which absent code would have caught it"
sections invite Phase 7/8/9/11 authors to treat "passes every gate today,
blocks once the new code ships" as the corpus's baseline contract for their
own future regression tests — a reasonable assumption to build on, and one
that is false as committed.

**Fix:** Either (a) correct the header comments and postmortem prose to
state precisely what is true today — "passes `dsx validate` and blocks at
`plan`/`execute` (which threshold at CRITICAL); it also currently blocks at
`verify`/`ship` on unrelated incidental gaps (missing narrative/entrypoint/
evidence), which is a corpus completeness gap, not the documented defect" —
or (b) fill in the incidental gaps in each fixture (add
`reproducibility.entrypoint`, `narrative.path` + a matching narrative file,
resolve/replace the evidence pointer, waive or check the assumption, add
`metrics[].sql`) so the fixtures genuinely pass `verify`/`ship` today and
only the documented target defect remains uncaught, matching the claim as
written. Either way, extend
`tests/test_known_bad_corpus.py` to assert the actual guarantee (e.g. that
`dsx gate ship` on each fixture blocks with *zero* CRITICAL/HIGH findings
other than a documented allow-list, or that it exits 0) so this claim is
enforced going forward instead of only asserted in prose.

## Warnings

### WR-01: `dsx/spec.py::_INFERENCE_FIELDS` is dead code that overstates what is actually validated

**File:** `dsx/spec.py:830-833`

**Issue:** `_INFERENCE_FIELDS` is a 6-tuple of every field name under
`inference:`. Its own comment claims "the machine-readable statement plan
06-05's round-trip test and the catalogue can both read" it, but a
repository-wide search shows it is referenced nowhere except by
`tests/test_dsx.py::test_inference_fields_constant_matches_req_p6_04`, which
only asserts the constant equals a hard-coded literal — a test of the
constant against itself, not against behavior. `_validate_inference_shape`
(the function that actually validates the `inference:` block) does not
consult `_INFERENCE_FIELDS` at all; it uses the separate
`_INFERENCE_MEMBERSHIP` tuple (3 of the 6 fields) plus the single hard-coded
`_INFERENCE_REMOVED_FIELD` check for `stopping_rule`. There is no check that
flags an unknown/misspelled field under `inference:` in general (e.g.
`inference: {paradgim: bayesian}` is silently accepted — only the specific
string `"stopping_rule"` is special-cased). `_INFERENCE_FIELDS` therefore
creates the false impression that the six names form an enforced closed set
when only three are membership-checked and only one non-member is rejected.

**Fix:** Either wire `_INFERENCE_FIELDS` into a real check (e.g. a new
low-severity finding for any key under `inference:` outside this set, mirror
of the existing `stopping_rule` redirect), or remove the constant and its
now-misleading comment, and correct the comment on the field-name check
inside `_validate_inference_shape` to state plainly that only `paradigm`,
`paradigm_justification` and `declared_at` are vocabulary-checked today.

### WR-02: `next_invocation_id()` + `append()` is a non-atomic read-then-write — concurrent gate runs can collide on invocation IDs

**File:** `dsx/decisions.py:128-135` (`next_invocation_id`), consumed by `dsx/cli.py:291` (`_write_decision_trail`)

**Issue:** `next_invocation_id()` derives the next ID purely by re-reading
and counting existing `"invocation"` records in `DECISIONS.jsonl`, then the
caller separately calls `append()` to write the new header. There is no
locking between the read and the write. Two `dsx gate` processes racing
against the same `DECISIONS.jsonl` (e.g. a GSD pipeline that runs multiple
gate points in parallel against the same phase directory, or two terminals)
can both compute the same `next_invocation_id()` (e.g. both compute
`INV-0004`), then both append a header with that same ID, followed by their
own `DEC-001, DEC-002, …` decision records under it. `dsx explain`'s
"render the last invocation" and `--invocation <id>` selection logic both
key purely on `invocation_id` equality (`dsx/cli.py:416-427`), so the two
runs' decision records would be interleaved and indistinguishable under one
invocation header — silently corrupting the very grouping guarantee
`InvocationHeader`'s docstring describes ("the grouping anchor for one gate
run's trail").

**Fix:** At minimum, document that concurrent `dsx gate` invocations against
the same root are unsupported. A more complete fix would take an OS-level
advisory lock (e.g. `msvcrt.locking`/`fcntl.flock`, platform-guarded) around
the read-count-then-append sequence, or derive the invocation ID from a
monotonic source that doesn't require a read (e.g. a UUID plus a separate,
lock-protected sequence file) if concurrent gate runs are expected to be
supported.

### WR-03: `scripts/gen-finding-catalogue.py`'s D-05 allow-list prefix `"DSX-SPEC-08"` is a bare numeric-string prefix, not a hyphen-delimited one

**File:** `scripts/gen-finding-catalogue.py:51`

**Issue:** `_D05_ALLOWLIST_PREFIXES = ("DSX-PAR-", "DSX-SPEC-08")` mixes two
different prefix shapes: `"DSX-PAR-"` is hyphen-terminated (matches exactly
the `DSX-PAR-*` family), but `"DSX-SPEC-08"` is not — it matches any code
whose numeric suffix *starts with* `08`, which today happens to be exactly
`DSX-SPEC-080/081/082/085/086` (the intended set) but would just as
happily match a hypothetical future `DSX-SPEC-0800` or `DSX-SPEC-089x`-style
code without a human noticing the allow-list needs updating, since
`str.startswith()` performs no boundary check after the shared digits. This
is consistent with the D-20 "grows only as each later milestone phase adds
its own new prefix" design note, but the asymmetry between the two entries'
shapes is easy to copy forward incorrectly (a future contributor adding
`"DSX-VAL-1"` intending to scope one sub-family could accidentally also
match `DSX-VAL-10`, `DSX-VAL-100`, etc.).

**Fix:** Either use a fully-qualified boundary-safe prefix (e.g. match
against a compiled regex `^DSX-SPEC-08[0-9]-` or enumerate the exact code
list) or add a comment at the declaration site making the "no boundary
check" behavior explicit so a future edit doesn't assume hyphen-delimited
semantics uniformly.

## Info

### IN-01: `tests/test_frame_boundary.py::_package_for` has a dead, misleading if/else

**File:** `tests/test_frame_boundary.py:38-54`

**Issue:** The docstring explains that an `__init__.py`'s package is its own
directory, while a plain module's package is its *containing* directory
(the module name is not part of the package). The implementation, however,
computes the identical result in both branches:

```python
if parts and parts[-1] == "__init__":
    parts = parts[:-1]
else:
    parts = parts[:-1]
```

Both arms execute `parts[:-1]` — dropping the last path segment always
yields the correct package name whether that segment is `__init__` or an
ordinary module name, so the `if`/`else` split is a no-op that only exists
to narrate the two cases from the docstring. This isn't a correctness bug
(both cases resolve correctly today), but the branching invites a future
edit to "fix" one arm under the belief the two paths currently differ, when
they don't.

**Fix:** Collapse to `parts = parts[:-1]` unconditionally, with a one-line
comment noting that dropping the last path segment is correct for both an
`__init__.py` (whose own directory is `parts[:-1]`) and a plain module
(whose containing directory is also `parts[:-1]`) — the same operation
serves both cases by construction.

---

_Reviewed: 2026-08-08_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep_
