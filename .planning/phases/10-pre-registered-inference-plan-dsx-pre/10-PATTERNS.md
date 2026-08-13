# Phase 10: Pre-registered inference plan (`DSX-PRE-*`) - Pattern Map

**Mapped:** 2026-08-13
**Files analyzed:** 8 (3 created source-adjacent, 1 test, 1 fixture pair, 3 modified registries)
**Analogs found:** 8 / 8

> RESEARCH.md's Target 8 already covers the `dsx/frame/` module idiom in general (check signature,
> `Report`, `DecisionRecord` emission, D-05 docstring placement, `# D-05: <CODE>` test marker), Target 4
> covers `root` threading, and Target 7 covers `tests/test_known_bad_corpus.py`'s two maps. This file
> does not repeat those — it gives the concrete file-by-file analog assignment and copy-from excerpts.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `dsx/frame/prereg.py` | check module (frame-layer) | transform + request-response (spec+root in, `Report` out) | `dsx/frame/interference.py` (module shape) **+** `dsx/suppressions.py` (`CheckError`/`root` traits) | role-match, composite |
| `tests/test_frame_prereg.py` | test | request-response (unit) | `tests/test_frame_interference.py` | exact |
| `examples/known-bad/<slug>-ANALYSIS-SPEC.yaml` | fixture | file-I/O (YAML read by gate) | `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` | role-match (closest verify-only precedent) |
| `examples/known-bad/<slug>-POSTMORTEM.md` | fixture doc | file-I/O (prose, asserted-against by test) | `examples/known-bad/weak-identification-mmm-POSTMORTEM.md` | role-match |
| `dsx/cli.py` (`GATE_PROFILES`) | config (dict literal) | CRUD (registration table) | `interference` entry within the same table | exact (same file, sibling entry) |
| `dsx/cli.py` (`run_checks` `elif`) | dispatch/service | request-response | `dq`/`code` `elif` branches (single extra positional `root` arg, no kwarg) | exact |
| `dsx/frame/paradigm.py` (`_NOT_SHIPPED`/`_PARADIGM_INDEPENDENT`) | config (dict/tuple literal) | CRUD | the `DSX-PAR-` flip that shipped in Phase 9 (same two structures) | exact |
| `scripts/gen-finding-catalogue.py` (`PREFIX_GROUPS`, `_D05_ALLOWLIST_PREFIXES`) | config | CRUD | the `DSX-INT`/`"DSX-INT-"` entries added in Phase 8 | exact |
| `tests/test_known_bad_corpus.py` (new fixture registration + dedicated test) | test | request-response | `weak-identification-mmm`'s entries + `test_weak_identification_mmm_fixture_blocks_verify_and_ship_naming_int_030` | exact |

## Pattern Assignments

### `dsx/frame/prereg.py` (check module, transform + request-response)

**Primary analog for the module shape:** `dsx/frame/interference.py`
**Secondary analog for the two traits `prereg.py` alone needs (`root` argument, `CheckError`-raising):**
`dsx/suppressions.py` for the `CheckError` route; `dsx/cli.py::run_checks`'s `dq`/`code` branches for the
`root` argument shape (see RESEARCH.md Target 4 — not re-derived here).

**Module docstring + imports pattern** (`dsx/frame/interference.py:1-40`):
```python
"""DSX-INT-* — interference, triggering and stability (Phase 8).

This module adjudicates ``validity_frame.interference``: is a declared
interference/SUTVA risk actually addressed. ...
"""

from __future__ import annotations

from ..decisions import DecisionRecord
from ..findings import Report
from ..spec import (
    INTERFERENCE_MITIGATIONS,
    INTERFERENCE_RISKS,
    METRIC_TYPES,
    get,
    is_blank,
    is_placeholder_or_refusal,
    items,
    ...
)
```
`prereg.py` copies this shape exactly: `from __future__ import annotations`, then
`from ..decisions import DecisionRecord` **plus** `from ..decisions import decisions_path, read_all`
(legal under D-03a — `dsx/frame/__init__.py:16-31` names `dsx.decisions` as a permitted import), then
`from ..findings import CheckError, Report` (interference.py imports only `Report`; `prereg.py` also
needs `CheckError`, which is exactly what `dsx/suppressions.py:16` imports alongside `Report`:
`from .findings import CheckError, Finding, Report, Severity`), then `from ..spec import (...)` for
`get`, `normalize`, and the new `_PREREG_FACTS`/`DECLARATION_POINTS`.

**Core `check()` dispatcher pattern** (`dsx/frame/interference.py:675-711`):
```python
def check(spec: dict) -> Report:
    """Emit the interference-family findings (``DSX-INT-*``).

    Reads ``validity_frame:`` and degrades to an empty report — never a
    traceback — when the block is absent or is not a dictionary ...

    Structural criterion: dispatches to one private helper per adjudicated
    concept; no numeric threshold, effect size or statistic is computed
    anywhere in this module. Guards against a non-dict ``spec`` itself ...
    """
    report = Report(check="interference")

    if not isinstance(spec, dict):
        return report

    frame = section(spec, "validity_frame")
    if not frame:
        return report
    if not needs_causal_block(spec):
        return report

    _check_interference_unaddressed(frame, report)
    _check_interference_mitigation_admissibility(frame, report)
    _check_triggering_dilution(spec, frame, report)
    _check_stability_assessment(frame, report)

    return report
```
`prereg.check(spec: dict, root: "str | None") -> Report` deviates from this in exactly one structural
way — the extra `root` positional argument (confirmed: **neither** `val.check(spec)` at `dsx/frame/val.py:200`
**nor** `interference.check(spec)` at `dsx/frame/interference.py:675` takes anything but `spec`).
Everything else — the `Report(check="prereg")` construction, the non-dict guard, the "degrade to an
empty report, never a traceback" habit, the one-private-helper-per-concept dispatch — copies verbatim.

**`CheckError`-raising pattern (the trait `interference.py`/`val.py` do NOT have)** — analog is
`dsx/suppressions.py:174-181` (the working, currently-only precedent for exit 2 from inside a check body):
```python
# dsx/suppressions.py:174-181
if code and code not in known:
    raise CheckError(f"spec.suppressions[{index}].code {code!r} is not a known DSX finding code")
```
`prereg.py` needs this shape twice: once for an unparseable `fallback_rule` condition (D-02), and once
for "no recorded plan-time header" (D-09) — both are a guard-then-`raise CheckError(f"...")` with a
literal, informative f-string, no try/except wrapping (`dsx/suppressions.py`'s own `apply_suppressions`
is called unguarded at the tail of `run_checks`, confirmed at `dsx/cli.py:184` — `return
apply_suppressions(spec, merged)`, so a raise there propagates identically to how a raise inside
`prereg.check` will propagate).

**`DecisionRecord` emission pattern** (`dsx/frame/interference.py:641-672`):
```python
report.context.setdefault("decisions", []).append(
    DecisionRecord(
        id="",
        invocation_id="",
        layer="deterministic",
        choice=f"DSX-INT-040 {'fired' if fired else 'clear'}: ...",
        inputs=["validity_frame.stability.novelty_primacy_assessed", "validity_frame.stability.evidence"],
        rule="DSX-INT-040 fires when ...",
        citation="Sadeghi et al. (2021), ..., arXiv:2102.12893v1, Eq. (13)/(9)",
        counterfactual="Declaring ... would have cleared DSX-INT-040." if fired else "... would have fired DSX-INT-040.",
    ).to_dict()
)
```
Copy verbatim per code (`id`/`invocation_id` always `""` at emission time — filled later by
`_write_decision_trail`, `dsx/cli.py:277-320`, confirmed at `:314-318`).

**`root` threading — `dq`/`code` shape to copy** (`dsx/cli.py:158-159`, `:170-171`):
```python
elif name == "dq":
    reports.append(dq.check(spec, root))
...
elif name == "code":
    reports.append(code.check(spec, root))
```
New branch for `prereg` (RESEARCH.md Target 4's recommendation, restated here as the concrete diff):
```python
elif name == "prereg":
    reports.append(prereg.check(spec, root))
```
placed among the other `elif` branches, before the generic `elif name in CHECKS:` fallback
(`dsx/cli.py:176-177`).

---

### `tests/test_frame_prereg.py` (test, request-response)

**Analog:** `tests/test_frame_interference.py` — named as the precedent in CONTEXT and confirmed as the
closest by direct read.

**Imports pattern** (`tests/test_frame_interference.py:1-27`):
```python
"""Test suite for dsx/frame/interference.py — DSX-INT-010 (...) and DSX-INT-011 (...).
Stdlib unittest — no pytest dependency.

Run:  python3 -m unittest tests.test_frame_interference -v
"""

from __future__ import annotations

import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dsx import cli  # noqa: E402
from dsx.findings import Report, Severity  # noqa: E402
from dsx.frame import interference  # noqa: E402
from dsx.loader import load  # noqa: E402
from dsx.spec import INTERFERENCE_MITIGATIONS, INTERFERENCE_RISKS, needs_causal_block  # noqa: E402
from dsx.suppressions import known_codes  # noqa: E402
```
`test_frame_prereg.py` copies this block, swapping `interference` for `prereg`; `tempfile`/`shutil` are
kept (prereg's tests need a real temp directory to write a `DECISIONS.jsonl` plan header into before
calling `prereg.check(spec, root)` — see RESEARCH.md Pitfall 1, same root cause this test file must
avoid); add `from dsx.findings import CheckError` for the exit-2 assertions and `from dsx.decisions
import append, ...` (or call `dsx gate plan` via `cli.main`) to seed a prior plan header.

**Registration + reachability test pair — copy verbatim, adjust the point tuple**
(`tests/test_frame_interference.py:180-196`):
```python
class TestGateRegistration(unittest.TestCase):
    def test_interference_registered_in_plan_verify_ship_absent_from_execute(self):
        from dsx.cli import CHECKS, GATE_PROFILES

        self.assertIs(CHECKS["interference"], interference.check)
        for point in ("plan", "verify", "ship"):
            with self.subTest(point=point):
                self.assertIn("interference", GATE_PROFILES[point])
        self.assertNotIn("interference", GATE_PROFILES["execute"])

    def test_every_dsx_int_code_reachable_from_a_gate_profile(self):
        from dsx.cli import GATE_PROFILES

        int_codes = [c for c in known_codes() if c.startswith("DSX-INT-")]
        self.assertTrue(int_codes, "expected at least DSX-INT-010 and DSX-INT-011 to be known")
        reachable_checks: "set[str]" = set().union(*GATE_PROFILES.values())
        self.assertIn("interference", reachable_checks)
```
`prereg`'s version inverts which points are asserted present vs. absent (D-11: present at `verify` and
`ship` **only**):
```python
class TestGateRegistration(unittest.TestCase):
    def test_prereg_registered_in_verify_ship_absent_from_plan_and_execute(self):
        from dsx.cli import CHECKS, GATE_PROFILES

        self.assertIs(CHECKS["prereg"], prereg.check)
        for point in ("verify", "ship"):
            with self.subTest(point=point):
                self.assertIn("prereg", GATE_PROFILES[point])
        for point in ("plan", "execute"):
            with self.subTest(point=point):
                self.assertNotIn("prereg", GATE_PROFILES[point])

    def test_every_dsx_pre_code_reachable_from_a_gate_profile(self):
        from dsx.cli import GATE_PROFILES

        pre_codes = [c for c in known_codes() if c.startswith("DSX-PRE-")]
        self.assertTrue(pre_codes, "expected at least DSX-PRE-010 to be known")
        reachable_checks: "set[str]" = set().union(*GATE_PROFILES.values())
        self.assertIn("prereg", reachable_checks)
```

**Malformed-shape degrade-gracefully idiom** (`tests/test_frame_interference.py:199-204`, class
`TestMalformedShapesDegradeGracefully`) — same loop-over-bad-values shape applies to a malformed
`inference:` block or a non-string `fallback_rule`; copy the `for bad_frame in ("s", [], None, 3):` /
`with self.subTest(...)` structure.

---

### `examples/known-bad/<slug>-ANALYSIS-SPEC.yaml` + `-POSTMORTEM.md` (fixture pair, file-I/O)

**Closest structural analog (confirmed by RESEARCH.md Target 7 and independently re-read here):**
`examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` — the only existing fixture that uses
the point-scoped `_TARGET_DEFECT_CODES` shape with a **non-`plan`** key (`{"plan": "DSX-VAL-040",
"verify": "DSX-INT-030"}`). It is a structural analog only (test-scaffolding shape), not a content
analog — copy its **header-comment shape**, not its identification-strength content.

**Header-comment shape to copy** (`examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml:1-31`):
```yaml
# A known-bad ANALYSIS-SPEC (REQ-P7-05, ROADMAP Success Criterion 1, D-15). Opposite
# polarity from its three siblings in this directory: this file is EXPECTED to exit
# non-zero at `dsx gate plan`, naming DSX-VAL-040 among its CRITICAL findings, because
# ...
#
# The encoded defect: validity_frame.identification.strength is declared `weak` with
# constraint_source `none` — ...
#
# It also blocks `dsx gate ship` (and `dsx gate verify`) on corpus-completeness gaps
# unrelated to the encoded defect — DSX-CLM-031 (...), DSX-COH-031 (...), ... — the
# same measured incidental-gap pattern the sibling fixtures carry; see
# tests/test_known_bad_corpus.py's _INCIDENTAL_GAP_CODES. See the paired POSTMORTEM.md.
#
#   dsx validate --spec examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml
#   dsx gate plan --spec examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml
```
The new fixture's header must state the analogous facts for a **verify-only** target: it clears `plan`
and `execute` (prereg is not registered there — D-11), blocks only `verify`/`ship` naming
`DSX-PRE-030`, and — critically, a trait `weak-identification-mmm` does not need but the new fixture
does — **must carry a prior `plan`-gate-point header in its own committed `DECISIONS.jsonl`-equivalent
setup**, or the fixture-driving test must run `dsx gate plan` against it first in the same temp
directory (RESEARCH.md Pitfall 1's fix, applied per-fixture). Document this explicitly in the header
comment since it is a new precondition class no existing fixture comment states.

**The `inference:` block fields this fixture must set** (`examples/good-ANALYSIS-SPEC.yaml:357-362`):
```yaml
  paradigm: frequentist            # frequentist | bayesian
  ...
  declared_at: pre_data            # pre_data | post_data
  primary_procedure: two_proportion_z
  ...
  fallback_rule: >
```
The new fixture sets `fallback_rule` to a mini-language rule whose condition is true against the
fixture's own `results:` facts (so it resolves to a real substitute branch), sets `analysis.test` to a
**different** procedure name than the resolved branch (the post-hoc-switch defect), and sets
`declared_at: pre_data` (so the fixture proves REQ-P10-03/04, not `DSX-PRE-020`).

**Post-mortem structure to copy** (`examples/known-bad/weak-identification-mmm-POSTMORTEM.md:1-20`):
```markdown
# Post-mortem: weak identification in a marketing-mix model

Paired spec: `weak-identification-mmm-ANALYSIS-SPEC.yaml`

## What was concluded

A marketing-analytics team fit a national weekly regression ... [narrative of what
was concluded, in plain domain language]

## Why it was wrong

The model's only source of identifying variation was ... [named failure(s), each
grounded in a cited source — "Chan & Perry (2017), section 4.1.2, ..."]
```
The new post-mortem's "What was concluded" section narrates an operator declaring a fallback rule,
seeing the data, and switching to a different (even strictly more conservative) procedure than the rule
selects; "Why it was wrong" cites Gelman & Loken (2014) page 463 (the φ vs. φ(y) sentence, per D-14) and
Simmons et al. (2011) page 1365 (substitution as its own researcher degree of freedom) — matching this
fixture pair to the two citations D-14 already locked, not inventing new ones. Must also satisfy the
post-mortem/catch-attribution invariant tests at `tests/test_known_bad_corpus.py` (see next section).

---

### `dsx/cli.py` — `GATE_PROFILES` edit (config, CRUD)

**Analog: the existing `interference` entries in the same dict literal** (`dsx/cli.py:90-103`, already
quoted above under `run_checks`). `interference` appears in the `"plan"`, `"verify"` and `"ship"` tuples
but not `"execute"` — the closest existing shape to `prereg`'s verify/ship-only registration, differing
only in that `prereg` additionally drops `"plan"`:
```python
GATE_PROFILES: dict[str, tuple[str, ...]] = {
    "plan": (..., "paradigm", "val", "interference"),                 # prereg: NOT added here
    "execute": (..., "paradigm"),                                     # prereg: NOT added here
    "verify": (..., "paradigm", "val", "interference"),                # prereg: appended here
    "ship": (..., "paradigm", "val", "interference"),                  # prereg: appended here
}
```
Concretely: append `"prereg"` to the end of the `"verify"` and `"ship"` tuples only.

---

### `dsx/frame/paradigm.py` — `_NOT_SHIPPED`/`_PARADIGM_INDEPENDENT` edit (config, CRUD)

**Analog:** the matched-pair flip performed when Phase 9 shipped `DSX-PAR-*` (same two structures, same
file). `_PARADIGM_INDEPENDENT` (`dsx/frame/paradigm.py:43-49`) already lists `"DSX-PRE-"` — no edit
needed there; `_NOT_SHIPPED` (`:65-68`) still lists `"DSX-PRE-"` and must have that entry **deleted** in
the landing commit (mirrors how the `DSX-PAR-` entry was removed from `_NOT_SHIPPED` in Phase 9, while
`_PARADIGM_INDEPENDENT`'s pre-existing `"DSX-PAR-002"` entry needed no change). Guard tests:
`test_applied_prefixes_have_codes_and_not_shipped_prefixes_have_none`
(`tests/test_dsx.py:2811-2858`, marked `# D-05: DSX-PAR-001` at `:2810`) — assertion for
`_PARADIGM_INDEPENDENT` at `:2838-2842`, assertion for `_NOT_SHIPPED` at `:2857-2858` (RESEARCH.md's
corrected line numbers, not CONTEXT's).

---

### `scripts/gen-finding-catalogue.py` — `PREFIX_GROUPS` / `_D05_ALLOWLIST_PREFIXES` edit (config, CRUD)

**Analog:** the `DSX-INT` heading and `"DSX-INT-"` allow-list entry added when Phase 8 shipped
`DSX-INT-*` — same two structures, same file, same shape of edit. `PREFIX_GROUPS`
(`scripts/gen-finding-catalogue.py:25-52`) gains a `DSX-PRE` heading following the existing `DSX-INT`
entry's shape; `_D05_ALLOWLIST_PREFIXES` (`:65`, currently `("DSX-PAR-", "DSX-VAL-", "DSX-INT-")`) gains
`"DSX-PRE-"` as a fourth tuple member — **this is the inclusion list that starts enforcement**, not an
exemption list (RESEARCH.md Target 6, point 4 — the easiest edit to forget). Guard tests:
`tests/test_gen_finding_catalogue.py:174-181` (missing prefix group) and `:227` (pinned covered-code
set) — both already exist and just need the new codes reflected.

---

### `tests/test_known_bad_corpus.py` — new fixture registration + dedicated positive test (test, CRUD)

**Analog:** `weak-identification-mmm`'s entries plus its dedicated positive test — the only existing
precedent for a non-`plan` `_TARGET_DEFECT_CODES` key, confirmed in RESEARCH.md Target 7 and by this
mapper's own read.

**`_TARGET_DEFECT_CODES` entry pattern** (`tests/test_known_bad_corpus.py:134-138`):
```python
_TARGET_DEFECT_CODES: "dict[str, dict[str, str]]" = {
    ...,
    "weak-identification-mmm": {"plan": "DSX-VAL-040", "verify": "DSX-INT-030"},
    ...,
}
```
New fixture's entry (verify/ship-only family, per-gate-point shape, D-16):
```python
"<new-slug>": {"verify": "DSX-PRE-030"},
```

**`_EXPECTED_CAUGHT_DEFECTS` entry** (`tests/test_known_bad_corpus.py:278-284`, RESEARCH.md-corrected
line numbers) — every fixture needs a key here even if empty, and `prereg` never runs at
`plan`/`execute` so this key must be an empty frozenset:
```python
"<new-slug>": frozenset(),
```

**Dedicated positive test to copy** (`test_weak_identification_mmm_fixture_blocks_verify_and_ship_naming_int_030`,
`tests/test_known_bad_corpus.py:446-466`) — required because the generic
`test_every_spec_blocks_only_on_its_target_defect_at_critical_threshold_points` (`:411-444`) only ever
calls `_gate_findings` for `point in _CRITICAL_THRESHOLD_POINTS` (`"plan"`, `"execute"`), so a
verify/ship-only code is **never exercised generically** — the new test asserts `exit_code == 1` and
`"DSX-PRE-030"` present among CRITICAL findings for both `"verify"` and `"ship"`, following this
method's exact shape (name it e.g. `test_<new-slug>_fixture_blocks_verify_and_ship_naming_pre_030`).

**Do not add `"DSX-PRE-*"` to `_INCIDENTAL_GAP_CODES`** — `test_incidental_allowlist_names_no_slugs_own_target_code`
(`:511-529`) forbids exactly this shortcut (already covered in CONTEXT/RESEARCH; restated here because
it is the one guard a planner copying `weak-identification-mmm`'s incidental-gap list verbatim could
trip by accident).

**The harness fix this phase's registration forces (not a new-file pattern, but blocks every other
pattern above from passing):** `_gate_findings()` (`tests/test_known_bad_corpus.py:332-353`) must run
`dsx gate plan` in the same temp directory before any `verify`/`ship` call, once `prereg` is registered —
see RESEARCH.md Pitfall 1 for the full evidence; no analog exists for this fix since it is the first
time any check reads prior gate-run state, but the concrete change is additive to the existing
`with tempfile.TemporaryDirectory() as tmp:` block already in that method.

## Shared Patterns

### `CheckError` for exit 2 (D-02/D-09)
**Source:** `dsx/suppressions.py:174-181`
**Apply to:** `dsx/frame/prereg.py` (both the unparseable-rule path and the no-plan-header path)
```python
if code and code not in known:
    raise CheckError(f"spec.suppressions[{index}].code {code!r} is not a known DSX finding code")
```
No `try/except` anywhere in the call chain catches this before `main()` (`dsx/cli.py:758-770`); a raise
inside `prereg.check` propagates identically to this existing raise inside `apply_suppressions`, which
is itself called unguarded at the tail of `run_checks` (`dsx/cli.py:184`).

### `root` threading via a named `elif` in `run_checks`
**Source:** `dsx/cli.py:158-159` (`dq`), `:170-171` (`code`)
**Apply to:** the new `elif name == "prereg": reports.append(prereg.check(spec, root))` branch.

### `Report`/`DecisionRecord` emission idiom
**Source:** `dsx/frame/interference.py:641-711`
**Apply to:** every `DSX-PRE-*` finding site in `prereg.py`; already covered in depth by RESEARCH.md
Target 8 — this file adds only the concrete excerpt above for convenience.

### Registration + reachability test pair
**Source:** `tests/test_frame_interference.py:180-196`
**Apply to:** `tests/test_frame_prereg.py`'s `TestGateRegistration` class (verbatim excerpt above, with
the present/absent point sets inverted for D-11's verify/ship-only scope).

## No Analog Found

None. Every file this phase touches has at least a role-match analog already shipped in Phases 6-9.

## Metadata

**Analog search scope:** `dsx/frame/`, `dsx/suppressions.py`, `dsx/cli.py`, `tests/test_frame_interference.py`,
`tests/test_known_bad_corpus.py`, `examples/known-bad/*`, `dsx/frame/paradigm.py`,
`scripts/gen-finding-catalogue.py`.
**Files scanned (read directly this session):** `dsx/frame/interference.py` (imports block +
`check()`/`DecisionRecord` sections), `dsx/suppressions.py` (imports + `CheckError` raise),
`dsx/cli.py:85-184` (`GATE_PROFILES`, `GATE_THRESHOLDS`, `run_checks`), `tests/test_frame_interference.py`
(imports + `TestGateRegistration`), `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml`
(header comment), `examples/known-bad/weak-identification-mmm-POSTMORTEM.md` (structure),
`examples/good-ANALYSIS-SPEC.yaml:357-362` (`inference:` block).
**Pattern extraction date:** 2026-08-13
