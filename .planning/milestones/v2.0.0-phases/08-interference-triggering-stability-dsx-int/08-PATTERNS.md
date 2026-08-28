# Phase 8: Interference, triggering, stability - Pattern Map

**Mapped:** 2026-08-12
**Files analyzed:** 11
**Analogs found:** 11 / 11

**Note on line numbers:** `08-RESEARCH.md` already flagged that `08-CONTEXT.md`'s own line
citations for `dsx/spec.py` are stale (Phase 7's 07-01 inserted ~90 lines ahead of them). Every
line number below was re-verified directly against the current working tree at the time this
document was written. Locate helpers by **name** in plan action text, not by line number, in case
a further Phase 7 plan lands before Phase 8 executes.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `dsx/frame/interference.py` | check module (gate-check library) | request-response (pure function over in-memory dict → Report) | `dsx/frame/paradigm.py` | exact (only existing `dsx/frame/*` check) |
| `dsx/spec.py` (no new helper; reuse `is_placeholder_or_refusal`) | contract/vocabulary module | transform (dict → validated dict / findings) | itself — `is_blank()` (line 369) and `is_placeholder_or_refusal()` (line 421) | exact — reuse, not new code |
| `dsx/mathx.py` (add dilution function) | utility (pure math kernel) | transform (pure function, no I/O) | `design_effect()` (line 435) | exact |
| `dsx/cli.py` (CHECKS + GATE_PROFILES edits) | config/route registration | request-response (CLI dispatch table) | the `paradigm` entry already in `CHECKS` (line 78) / `GATE_PROFILES` (lines 89-100) | exact — same file, same shape, one more row |
| `scripts/gen-finding-catalogue.py` (`_D05_ALLOWLIST_PREFIXES`, `PREFIX_GROUPS`) | build/config script | batch (AST-scan → regenerate doc) | the existing `"DSX-PAR-",` entry (line 58) and `DSX-PAR` `PREFIX_GROUPS` row (lines 43-44) | exact |
| `tests/test_frame_interference.py` (new) | test | request-response (unit + table-driven) | `tests/test_frame_boundary.py` shape + `dsx/frame/paradigm.py`'s own test coverage pattern in `tests/test_dsx.py` | role-match (no sibling test file exists yet for `paradigm.py` beyond `test_dsx.py`; `test_frame_boundary.py` is closest same-package precedent) |
| `tests/test_known_bad_corpus.py` (structural rewrite) | test (corpus/contract test) | batch (glob fixtures → per-fixture assertions) | its own current structure, lines 41-66, 176-245 | exact — modify in place |
| `tests/test_frame_boundary.py` (paradigm-read scanner, D-14) | test (boundary scanner) | batch (AST/text scan over `dsx/frame/*.py`) | its own existing two-proof pattern, lines 92-122 | exact — extend in place (or confirm no-op if Phase 7 landed first) |
| `examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml` + `-POSTMORTEM.md` | fixture pair (YAML + Markdown) | file-I/O (static fixture, loaded by tests/CLI) | `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml` + its `-POSTMORTEM.md` | exact |
| `brief.md` §6.5 | documentation | file-I/O (static prose table) | the five existing rows in that table | role-match |
| `.planning/ROADMAP.md` (success criteria 3, 4 reword) | documentation | file-I/O | its own existing wording | role-match |

## Pattern Assignments

### `dsx/frame/interference.py` (check module, request-response)

**Analog:** `dsx/frame/paradigm.py` (163 lines, read in full)

**Imports pattern** (paradigm.py lines 16-20 — D-03a boundary: only `dsx.checks`-free imports):
```python
from __future__ import annotations

from ..decisions import DecisionRecord
from ..findings import Report
from ..spec import PARADIGMS, get, is_blank, normalize
```
For `interference.py`, per D-05/D-09/D-11, the equivalent import block is:
```python
from __future__ import annotations

from ..decisions import DecisionRecord
from ..findings import Report
from ..mathx import <dilution_function_name>          # D-09
from ..spec import (
    INTERFERENCE_RISKS, METRIC_TYPES,                  # membership already enforced by DSX-SPEC-082;
    get, is_placeholder_or_refusal, items, normalize, section,   # read here, not re-validated
)
```
`dsx.checks` is never imported — enforced by `tests/test_frame_boundary.py::TestFrameImportBoundary`.

**Module-constant + set-equality-test pattern** (paradigm.py lines 35-41, the exact template D-05
copies for the risk→mitigation admissibility map):
```python
# Keyed by every member of PARADIGMS (D-12 symmetry) — a test asserts set
# equality with dsx.spec.PARADIGMS, so a future PARADIGMS addition without a
# matching key here fails loudly instead of silently under-reporting.
_PARADIGM_CONDITIONAL: "dict[str, tuple[str, ...]]" = {
    "frequentist": ("DSX-PAR-010", "DSX-ADM-"),
    "bayesian": ("DSX-PAR-011",),
}
```
The corresponding test (not shown in paradigm.py itself — lives in `tests/test_dsx.py`, look for
`self.assertEqual(set(_PARADIGM_CONDITIONAL), set(PARADIGMS))`-shaped assertions) is the pattern
`dsx/frame/interference.py`'s own test module must replicate for `_RISK_MITIGATION_MAP` against
`dsx.spec.INTERFERENCE_RISKS` (D-05's explicit instruction).

**`_NOT_SHIPPED` bookkeeping already primed for this phase** (paradigm.py lines 49-57):
```python
_NOT_SHIPPED: "dict[str, str]" = {
    ...
    "DSX-INT-": "Phase 8 ships DSX-INT-* (interference/SUTVA, triggering, dilution).",
    ...
}
```
This entry (`dsx/frame/paradigm.py:51`) **must be removed in the same commit** as the first
`report.add("DSX-INT-0NN", ...)` call — verified test precedent:
`tests/test_dsx.py::test_applied_prefixes_have_codes_and_not_shipped_prefixes_have_none` (exact
name confirmed by research Section 8). `_PARADIGM_INDEPENDENT` (paradigm.py lines 27-33) **already
lists `"DSX-INT-"`** — no edit needed there.

**Core dispatch/check pattern** (paradigm.py lines 60-78, adapted per `08-RESEARCH.md`'s own
recommended shape):
```python
def check(spec: dict) -> Report:
    report = Report(check="interference")
    frame = section(spec, "validity_frame")
    if not frame:
        return report
    _check_interference_declared(frame, report)       # DSX-INT-010, DSX-INT-011
    _check_triggering_dilution(spec, frame, report)    # DSX-INT-030
    _check_stability_assessed(frame, report)           # DSX-INT-040
    return report
```

**Citation/Structural-criterion docstring convention** (paradigm.py lines 60-77 verbatim shape —
`Citation:` then `Structural criterion:` as separate labelled paragraphs inside the function
docstring; this is what `scripts/gen-finding-catalogue.py`'s `_CITATION_RE`/`_REFVALUE_RE` greps
for):
```python
def check(spec: dict) -> Report:
    """Emit DSX-PAR-001 — the informational paradigm manifest.

    Citation: Deng, A., Lu, J. & Chen, S. (2016), "Continuous Monitoring of
    A/B Tests without Pain: Optional Stopping in Bayesian Testing", IEEE
    DSAA 2016 — ...
    Structural criterion: a set-membership computation over a data-driven
    applicability map ...
    """
```
Each of `DSX-INT-010`/`011`/`030`/`040` needs its own `Citation:`/`Structural criterion:` (or
`Reference value:`) block under its own private helper function, per D-06/D-10/D-19's per-code
citation requirements — this is the natural decomposition (four private functions), matching how
`dsx/checks/design.py` structures multi-code modules.

**`report.add(...)` call shape** (paradigm.py lines 117-126 — title is a single f-string literal
at the call site, never a pre-assigned variable, because `gen-finding-catalogue.py`'s AST extractor
requires a `Constant`/`JoinedStr` literal in that argument position):
```python
report.add(
    "DSX-PAR-001",
    "INFO",
    f"paradigm manifest — inference.paradigm: {paradigm or 'undeclared'}",
    detail=detail,
    remedy=remedy,
    where="spec.inference.paradigm",
    applied=applied,
    not_applied=not_applied,
)
```

**Decision-record emission pattern** (paradigm.py lines 146-161 — the `DecisionRecord` fields and
`report.context.setdefault("decisions", []).append(...)` idiom, unchanged since Phase 6/7):
```python
report.context.setdefault("decisions", []).append(
    DecisionRecord(
        id="",
        invocation_id="",
        layer="deterministic",
        choice=choice,
        inputs=["inference.paradigm"],
        rule="...",
        citation="Deng, Lu & Chen (2016), Continuous Monitoring of A/B Tests without Pain",
        counterfactual=counterfactual,
    ).to_dict()
)
```
D-11's undeclared-metric-type skip needs a **fifth**, distinct emission point — a `DecisionRecord`
only, no `report.add(...)` call — matching `dsx/spec.py:860-880`'s `_validate_validity_frame_shape`,
which appends a `DecisionRecord` unconditionally before branching (see excerpt below).

**Error handling / malformed-input degrade pattern** — `dsx/spec.py` line ~882 area guards a
non-dict `frame` before attribute access:
```python
frame = spec.get("validity_frame")
```
followed by an `isinstance` guard before use (Phase 7's precedent test name, per research:
`test_malformed_validity_frame_shapes_degrade_to_dsx_spec_080_not_a_crash`). `interference.py`'s
`section(spec, "validity_frame")` (below) already returns `{}` for a non-dict value, so this guard
is structural, not a new `try`/`except` — there is **no try/except pattern anywhere in
`dsx/frame/paradigm.py`**; the whole module is written to degrade via type checks (`section()`,
`get()` with defaults), never to raise. Copy that, not exception handling.

---

### `dsx/spec.py` — reuse, do not add a duplicate helper

**Analog for the escape-hatch idiom:** `is_placeholder_or_refusal()` (lines 421-433, current,
shipped by Phase 7's already-landed 07-01 — supersedes `08-CONTEXT.md` D-08's instruction to add a
new `is_placeholder()`):
```python
# dsx/spec.py:411
_PLACEHOLDER_RE = re.compile(r"^<[^>]*>$")

# dsx/spec.py:403-405
_FALSIFIER_REFUSALS = frozenset(
    {"n/a", "na", "tbd", "tba", "none", "unknown", "not assessed", "to be determined"}
)

# dsx/spec.py:421-433
def is_placeholder_or_refusal(value: Any) -> bool:
    """True when ``value`` is blank, an angle-bracket placeholder, or a refusal token.
    ...
    """
    if is_blank(value):
        return True
    if isinstance(value, str) and _PLACEHOLDER_RE.match(value.strip()):
        return True
    return normalize(value) in _FALSIFIER_REFUSALS
```
**Use this directly for `residual_note`.** Do not write a second, narrower helper — see
`08-RESEARCH.md` Section 4 for the full collision analysis. If the docstring reads too
falsifier-specific, broaden its wording (Claude's Discretion, not a re-litigation).

**`is_blank()`'s null-handling idiom** (lines 369-376 — the emptiness primitive it is layered
beside):
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
**Critical gotcha (D-08/D-13's turning point, verified in `08-RESEARCH.md` Section 3 and Pitfall
2):** `is_blank(False)` is `False` — a boolean `False` value is none of `None`/empty-string/empty-
collection. For `stability.novelty_primacy_assessed` and `triggering.dilution_adjusted` (both real
booleans in the template and in `interference-shared-budget-ANALYSIS-SPEC.yaml:149`), the correct
guard is:
```python
assessed = get(frame, "stability.novelty_primacy_assessed")
if assessed is not True:
    # fires on False, None (absent), or any non-boolean value alike
    ...
```
never `if is_blank(assessed):`.

**Accessor idioms** (lines 346-367, unchanged since Phase 6):
```python
def get(spec: Any, path: str, default: Any = None) -> Any:
    """Read a dotted path out of a nested mapping. Never raises on a missing key."""
    node: Any = spec
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node if node is not None else default


def section(spec: dict, name: str) -> dict:
    value = spec.get(name)
    return value if isinstance(value, dict) else {}


def items(spec: dict, name: str) -> list[dict]:
    """Return a list section, keeping only mapping entries."""
    value = spec.get(name)
    if not isinstance(value, list):
        return []
    return [v for v in value if isinstance(v, dict)]
```
Field paths for this phase (verified against `_VALIDITY_FRAME_MEMBERSHIP`, lines 813-822, and
`templates/ANALYSIS-SPEC.yaml:306-322`):
```
validity_frame.interference.risk            validity_frame.triggering.analysis_population
validity_frame.interference.mechanism        validity_frame.triggering.expected_trigger_rate
validity_frame.interference.mitigation       validity_frame.triggering.dilution_adjusted
validity_frame.interference.residual_note    validity_frame.stability.window
                                              validity_frame.stability.novelty_primacy_assessed
                                              validity_frame.stability.evidence
```

**`needs_causal_block` — the exact skip condition D-16 reuses verbatim** (`dsx/spec.py:852-855`,
inside `_validate_validity_frame_shape`):
```python
needs_causal_block = (
    normalize(spec.get("question_type", "")) in ("causal", "prescriptive")
    or normalize(get(spec, "design.kind", "")) == "experiment"
)
```
`interference.py` must import and call this same condition (or recompute it identically inline —
research recommends reuse, not reimplementation) so the frame checks and the shape validator never
disagree about when the causal sub-blocks apply.

**Metric-type enumeration and the optional-`type` escape hatch** — `_validate_metrics` (lines
561-624, in full; the only place `type` is read against `METRIC_TYPES`):
```python
# dsx/spec.py:110
METRIC_TYPES = {"ratio", "count", "sum", "average", "rate", "percentile", "index"}

# inside _validate_metrics, the only read-and-check of a metric's type
mtype = normalize(metric.get("type", ""))
if mtype and mtype not in METRIC_TYPES:
    report.add(
        "DSX-SPEC-025", "MEDIUM",
        f"Metric {name!r} has unrecognised type {metric.get('type')!r}",
        detail="Allowed: " + ", ".join(sorted(METRIC_TYPES)),
        remedy="Use a listed type so downstream checks know how to treat it.",
        where=where,
    )
```
Confirmed: `if mtype and mtype not in METRIC_TYPES` — an absent/blank `type` short-circuits
silently. `DSX-INT-030`'s helper walks `metrics = items(spec, "metrics")` (top-level `spec.metrics`,
not under `validity_frame`) and reads `normalize(metric.get("type", ""))` the same way, then
partitions against the new additive/ratio constant — skip + `DecisionRecord` (no finding) when
`type` is undeclared, per D-11.

**The `DEPENDENCE_ADMISSIBLE_METHODS`-precedent shape for a non-vocabulary constant** — this is the
research's own recommended closer analog than `_PARADIGM_CONDITIONAL` for *some* aspects (a
constant that references an existing vocabulary's members without being registered in
`_VOCABULARIES`), though the risk→mitigation map itself should still follow `_PARADIGM_CONDITIONAL`'s
set-equality-test discipline per D-05's explicit instruction. Read directly (`dsx/spec.py:229-235`,
plus the exclusion comment at `309-314`):
```python
DEPENDENCE_ADMISSIBLE_METHODS: "dict[str, frozenset[str]]" = {
    "clustered": frozenset({"cluster_robust", "bootstrap_cluster", "mixed_effects"}),
    "repeated_measures": frozenset({"mixed_effects", "cluster_robust"}),
    "temporal": frozenset({"cluster_robust", "bootstrap_cluster", "mixed_effects"}),
    "spatial": frozenset({"cluster_robust", "bootstrap_cluster", "mixed_effects"}),
    "hierarchical": frozenset({"mixed_effects", "cluster_robust"}),
}

# dsx/spec.py:309-314
# Single registry behind describe_vocabulary() (D-05, REQ-P6-06): the object each shape
# validator imports is the exact object dumped here — one place to add a vocabulary, not two.
# Deliberately excludes SPEC_VERSION, CAUSAL_VERBS, REQUIRED_TOP_LEVEL,
# IMBALANCE_UNSAFE_METRICS, DEPENDENCE_ADMISSIBLE_METHODS and FALSIFIER_DISCRIMINATORS —
# they are not vocabularies.
```
**Which analog the planner should copy, and why:** copy `_PARADIGM_CONDITIONAL`'s **set-equality
test discipline** for `_RISK_MITIGATION_MAP` (D-05 requires this explicitly, and
`INTERFERENCE_RISKS` is a closed vocabulary the map must stay in lock-step with). Copy
`DEPENDENCE_ADMISSIBLE_METHODS`'s **placement discipline** (a capability-matrix constant excluded
from `_VOCABULARIES`, living beside the code that uses it — though `interference.py`'s own
additive/ratio partition lives in `dsx/frame/interference.py` per D-05's instruction, not in
`dsx/spec.py`, unlike `DEPENDENCE_ADMISSIBLE_METHODS` which is central because Phase 11 also needs
it). The two analogs are complementary, not competing: shape from `DEPENDENCE_ADMISSIBLE_METHODS`,
invariant-test rigor from `_PARADIGM_CONDITIONAL`.

**Vocabulary constants already shipped, read verbatim** (`dsx/spec.py:237-277`):
```python
INTERFERENCE_RISKS = {
    "none": "Treatment of one unit does not plausibly affect another unit's outcome.",
    "shared_budget": "Units compete for a shared, capacity-limited resource (e.g. a paid-media budget).",
    "marketplace": "Units interact through a two-sided market where one side's treatment shifts the other side's outcomes.",
    "geo_spillover": "Treatment effects in one geography leak into a nearby untreated geography.",
    "social_graph": "Units are connected by a social or referral graph through which treatment can propagate.",
    "shared_inventory": "Units draw from a shared, finite inventory of a physical or virtual good.",
}

INTERFERENCE_MITIGATIONS = {
    "none": "No mitigation is applied; interference risk, if any, is unaddressed.",
    "geo_split": "Randomization is performed at the geography level to contain spillover.",
    "cluster_randomisation": "Randomization is performed at the cluster level rather than the individual level.",
    "time_split": "Treatment and control are separated in time rather than concurrently.",
    "budget_isolation": "Each arm draws from a separate, non-competing budget.",
    "modelled": "Interference is estimated and adjusted for statistically rather than designed away.",
}

ANALYSIS_POPULATIONS = {
    "eligible": "The population that met eligibility criteria, regardless of subsequent engagement.",
    "triggered": "The subset of the eligible population that actually triggered the analyzed event.",
}
```
No edits needed to any of these — Phase 8 ships zero new vocabulary members.

---

### `dsx/mathx.py` — new dilution function (utility, transform, pure)

**Analog:** `design_effect()` (lines 435-453, in full):
```python
def design_effect(m: float, icc: float) -> float:
    """The factor by which the variance of an estimate is inflated when observations
    inside a cluster are correlated and the analysis is run at a level finer than the
    true dependence unit.

    Citation: Kish, L. (1965), Survey Sampling, page 258 (design-effect definition)
    and pages 161-162 (intraclass correlation); Higgins, J.P.T., Eldridge, S. and Li,
    T. (2024), Cochrane Handbook for Systematic Reviews of Interventions version 6.5,
    sections 23.1.4 and 23.1.4.1.
    The section number inside Kish for the formula itself is UNVERIFIED — the page
    numbers above were confirmed, the section number was not. Do not invent one.
    Reference value: an intraclass correlation of 0.02 and an average cluster size of
    29.8 yield 1.576 — the Cochrane Handbook's own published worked example.
    """
    if m < 1:
        raise ValueError(f"m (average cluster size) must be >= 1, got {m!r}")
    if not 0.0 <= icc <= 1.0:
        raise ValueError(f"icc (intraclass correlation) must be in [0, 1], got {icc!r}")
    return 1.0 + (m - 1.0) * icc
```
**Range-validation idiom to copy exactly:** raise `ValueError` with an f-string that echoes the
offending value via `!r`, one `if` per parameter, before the return statement. For D-09's dilution
function (`delta_diluted = delta_triggered × trigger_rate`), the parameter that needs range
validation is the trigger rate (bounded `[0, 1]`, matching `icc`'s `0.0 <= icc <= 1.0` pattern
above) — name it per D-10's notation note (`expected_trigger_rate` is the contract field;
`trigger_rate`/`TR` are formula variables with different meanings in the source paper, so the
`mathx` parameter name must make the distinction explicit, e.g. `user_trigger_rate` or
`n_tr_over_n`).

**Docstring convention** — `Citation:` then `Reference value:` (not `Structural criterion:` — that
label is for check modules; `mathx.py` functions use `Reference value:` for a published worked
example/counterexample), exactly as `design_effect()` demonstrates above. For D-09/D-10, the
`Reference value:` is the Deng & Hu (2015) time-to-success counterexample (true effect −26 msec,
naive formula yields −18 msec) — see `08-CONTEXT.md` D-10 for the exact wording obligations.

**Where the unit test lives** — the `TestMath` class in `tests/test_dsx.py` (existing tests for
`design_effect()`/`inflation_from_peeking()` live there; grep `class TestMath` in that file). The
new dilution function's reference-value test belongs in the same class, following whatever
assertion-style (`assertAlmostEqual`, given floating-point results) the existing `design_effect()`
tests use.

**D-09's constraint, restated as a pattern:** this function is imported by
`dsx/frame/interference.py` but **never called from `check()`** — `DSX-INT-030` adjudicates the
*declaration* (`analysis_population == "eligible" and dilution_adjusted is not True`), not a
computed statistic. If a plan task ends up calling this function from inside `check()`, that is a
D-01/D-02 violation — flag it.

---

### `dsx/cli.py` — `CHECKS` and `GATE_PROFILES` registration

**Analog:** the existing `paradigm` entry, registered in `CHECKS` and in **every** profile (because
it's INFO-severity and structurally cannot block); `interference` instead follows the narrower
`design` pattern (present in `plan`/`verify`/`ship`, absent from `execute`) per D-03.

**Current state, read directly** (`dsx/cli.py:23-38` imports, `63-79` `CHECKS`, `88-101`
`GATE_PROFILES`, `105-110` `GATE_THRESHOLDS`):
```python
from .frame import paradigm
...
CHECKS: dict[str, Callable] = {
    "spec": validate_structure,
    "design": design.check,
    ...
    "paradigm": paradigm.check,
}

GATE_PROFILES: dict[str, tuple[str, ...]] = {
    "plan": ("spec", "design", "metrics", "coherence", "paradigm"),
    "execute": ("spec", "ml", "repro", "dq", "code", "paradigm"),
    "verify": (
        "spec", "design", "stats", "ml", "metrics", "claims", "viz", "repro",
        "dq", "coherence", "smells", "figures", "narrative", "code", "decision",
        "paradigm",
    ),
    "ship": (
        "spec", "design", "stats", "ml", "metrics", "claims", "viz", "repro",
        "dq", "coherence", "smells", "figures", "narrative", "code", "decision",
        "paradigm",
    ),
}

GATE_THRESHOLDS: dict[str, str] = {
    "plan": "CRITICAL", "execute": "CRITICAL", "verify": "HIGH", "ship": "HIGH",
}
```
**Required edits (D-03):**
1. `from .frame import interference` added beside `from .frame import paradigm` (line 50).
2. `"interference": interference.check,` added to `CHECKS` (after `"paradigm"`, matching
   dict-literal insertion order convention already used).
3. `"interference"` appended to the `plan`, `verify` and `ship` tuples — **not** `execute`.
4. No `GATE_THRESHOLDS` edit — CRITICAL at plan already matches D-02, HIGH at verify/ship already
   matches D-02 for `DSX-INT-040`.
5. No `run_checks` dispatch-branch edit — `interference.check(spec)` takes only `spec`, exactly
   like `paradigm.check(spec)`, and falls through the same generic `CHECKS[name](spec)` branch.

**Reachability test analog** (`tests/test_dsx.py:1583-1590`,
`test_every_dsx_par_code_reachable_from_a_gate_profile`, in full):
```python
def test_every_dsx_par_code_reachable_from_a_gate_profile(self):
    from dsx.cli import GATE_PROFILES
    from dsx.suppressions import known_codes

    par_codes = [c for c in known_codes() if c.startswith("DSX-PAR-")]
    self.assertTrue(par_codes, "expected at least DSX-PAR-001 to be known")
    reachable_checks = set().union(*GATE_PROFILES.values())
    self.assertIn("paradigm", reachable_checks)
```
Copy verbatim with `"DSX-INT-"` / `"interference"` substituted.

**Registration test analog** (`tests/test_dsx.py:1526-1533`,
`test_paradigm_check_registered_in_every_gate_profile` — note this one asserts membership in
*every* profile, which is specific to `paradigm`'s all-profile registration; `interference`'s test
must instead assert membership in `plan`/`verify`/`ship` and **absence** from `execute`):
```python
def test_paradigm_check_registered_in_every_gate_profile(self):
    from dsx.cli import CHECKS, GATE_PROFILES
    from dsx.frame import paradigm

    self.assertIs(CHECKS["paradigm"], paradigm.check)
    for point, checks in GATE_PROFILES.items():
        with self.subTest(point=point):
            self.assertIn("paradigm", checks)
```

---

### `scripts/gen-finding-catalogue.py` — three edits (D-04)

**Analog:** the existing `DSX-PAR-` entries, added by Phase 6 for exactly this reason. Read directly
(`scripts/gen-finding-catalogue.py:25-58`):
```python
PREFIX_GROUPS = [
    ...
    ("DSX-PAR", "Paradigm and monitoring discipline",
     "The declared inferential paradigm manifest and its symmetric peeking-monitoring pair."),
]

# D-20: the finite, visible exemption boundary for D-05 citation/reference-value
# enforcement. This list grows only as each later v2.0.0 phase adds its own
# new-in-this-milestone prefix (DSX-VAL-*, DSX-INT-*, ...) — never to exempt a
# code this milestone introduces from its citation and reference-value obligations.
_D05_ALLOWLIST_PREFIXES = ("DSX-PAR-",)
```
**Required edits:**
1. Append a `("DSX-INT", "Interference, triggering, stability", "<one-line summary>")` tuple to
   `PREFIX_GROUPS` (line 25 area) — or the codes ship uncatalogued and no test notices.
2. Append `"DSX-INT-"` to `_D05_ALLOWLIST_PREFIXES` (line 58) — the comment there already says the
   tuple grows exactly this way.

   **Correction to CONTEXT.md's framing:** re-read the comment directly — `_D05_ALLOWLIST_PREFIXES`
   is described as "the finite, visible exemption boundary for D-05 citation/reference-value
   **enforcement**", i.e. codes in this allow-list are **exempted from** the citation/reference-
   value requirement, not required to carry it. Since D-01/D-06/D-10/D-19 all require Phase 8's
   codes to carry real citations, the planner must resolve whether `DSX-INT-` belongs in this
   allow-list at all, or whether `08-CONTEXT.md` D-04's instruction to add it is describing catalog
   membership (`PREFIX_GROUPS`) rather than citation exemption. **Escalate this discrepancy rather
   than silently adding to the wrong list** — flag it for the planner as an open question rather
   than resolving it here, since it affects whether Phase 8's four codes are checked for citations
   at all by the build script.
3. No change to `_D05_ALLOWLIST_CODES` (line 66) or `_TEST_MARKER_RE` (line 74, `\bDSX-[A-Z]+-\d{3}`
   already accepts three-digit codes unchanged).
4. Regenerate `references/finding-codes.md` via `python3 scripts/gen-finding-catalogue.py --write`.

---

### `tests/test_frame_interference.py` (new test module)

**Analog:** `tests/test_frame_boundary.py`'s module-docstring/shape conventions (imports,
`ROOT`/`sys.path.insert` bootstrap, `unittest.TestCase` subclasses per concern) plus the general
`tests/test_dsx.py` conventions for CLI-level gate assertions (`self._run([...])`,
`redirect_stdout`/`redirect_stderr`, `tempfile.TemporaryDirectory()`). No sibling test file exists
yet for `dsx/frame/paradigm.py` as a standalone module — its tests live inline in
`tests/test_dsx.py` — so this is a **new pattern** for the repo (Phase 7's planned, not-yet-landed
`tests/test_frame_val.py`, per `07-03-PLAN.md`, is the nearest sibling in intent). Table-driven
tests over `_RISK_MITIGATION_MAP` (REQ-P8-02) should follow the `with self.subTest(...)` idiom used
throughout `tests/test_known_bad_corpus.py` (e.g. line 193-200) and `tests/test_frame_boundary.py`
(line 111, 120).

---

### `tests/test_known_bad_corpus.py` — structural rewrite (D-15, the phase's largest under-sized item)

**Current structure, read directly (331 lines total; this excerpt covers every location cited by
`08-CONTEXT.md`/`08-RESEARCH.md`):**

```python
# line 41
_CRITICAL_THRESHOLD_POINTS = ("plan", "execute")

# lines 49-59
_INCIDENTAL_GAP_CODES = {
    "DSX-CLM-031",  # claims[].evidence points at "RESULTS.md#..." — a file this corpus never commits
    "DSX-COH-031",  # assumptions[0] is declared but neither checked: true nor waived
    "DSX-EXP-007",  # frequentist fixture: design.mde (0.02) exceeds decision.minimum_practical_effect (0.01)
    "DSX-MET-040",  # metrics[0].source is warehouse.* with no metrics[0].sql definition
    "DSX-NAR-001",  # claims declared but narrative.path missing (ship-only check)
    "DSX-REP-001",  # bayesian fixture: bayesian_ab is a stochastic method with no reproducibility.random_seed
    "DSX-REP-030",  # reproducibility.entrypoint is not declared
    "DSX-STA-041",  # bayesian fixture: declared analysis.test (bayesian_ab) is outside the stats
                    # recommendation engine's acceptable set for this outcome shape
}

# line 66
_TARGET_CODE_FAMILIES = ("DSX-INT-", "DSX-PAR-01")
```

**The four affected tests, read directly:**
- `test_every_postmortem_names_a_catch_attribution_finding_code` (line 176) — regex-only, **needs
  no change** (verified: `_FINDING_CODE_RE` matches any `DSX-<LETTERS>-<digits>` anywhere,
  regardless of blocking status; the interference fixture's post-mortem already names
  `DSX-INT-010`).
- `test_every_spec_passes_the_critical_threshold_gate_points` (line 187):
  ```python
  def test_every_spec_passes_the_critical_threshold_gate_points(self):
      specs = self._spec_paths()
      self.assertTrue(specs, "no known-bad specs found to gate")
      for path in specs:
          for point in _CRITICAL_THRESHOLD_POINTS:
              with self.subTest(spec=path.name, point=point):
                  code, findings = self._gate_findings(path, point)
                  critical = [f["code"] for f in findings if f["severity"] == "CRITICAL"]
                  self.assertEqual(
                      code, 0,
                      f"{path.name} failed dsx gate {point} (CRITICAL threshold): {critical}",
                  )
  ```
- `test_ship_gate_findings_are_all_documented_incidental_corpus_gaps` (line 202):
  ```python
  def test_ship_gate_findings_are_all_documented_incidental_corpus_gaps(self):
      specs = self._spec_paths()
      self.assertTrue(specs, "no known-bad specs found to gate")
      for path in specs:
          with self.subTest(spec=path.name):
              _code, findings = self._gate_findings(path, "ship")
              blocking = {
                  f["code"] for f in findings if f["severity"] in ("CRITICAL", "HIGH")
              }
              undocumented = blocking - _INCIDENTAL_GAP_CODES
              self.assertEqual(undocumented, set(), ...)
  ```
- `test_incidental_allowlist_names_no_target_family_code` (line 231):
  ```python
  def test_incidental_allowlist_names_no_target_family_code(self):
      for code in sorted(_INCIDENTAL_GAP_CODES):
          for family in _TARGET_CODE_FAMILIES:
              with self.subTest(code=code, family=family):
                  self.assertFalse(code.startswith(family), ...)
  ```
  This is **the test that actively forbids the obvious fix** — `_TARGET_CODE_FAMILIES` already
  contains `"DSX-INT-"`, so any attempt to add `DSX-INT-040` to `_INCIDENTAL_GAP_CODES` fails this
  test by construction.

**The second, previously-undocumented collision** (verified directly,
`examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml:147-150`):
```yaml
stability:
  window: "14 days"
  novelty_primacy_assessed: false
  evidence: ""
```
This fires `DSX-INT-040` independently of the fixture's intended `DSX-INT-010` defect, the moment
both codes ship. **Recommended fix (not a re-litigation of D-15):** edit this fixture's `stability`
block to `novelty_primacy_assessed: true` with a real, resolvable `evidence` pointer — the
fixture's own defect is interference, not stability, and this mirrors Phase 7's own precedent of
editing a fixture's unrelated field rather than growing the allow-list.

**The concrete new shape** (per-fixture target-defect map, replacing the flat
`_INCIDENTAL_GAP_CODES`/`_TARGET_CODE_FAMILIES` pair):
```python
_TARGET_DEFECT_CODES: dict[str, dict[str, str]] = {
    # slug: {gate_point: code}
    "interference-shared-budget": {"plan": "DSX-INT-010"},
    "triggering-dilution": {"plan": "DSX-INT-030"},
}
```
Rewrite the three affected tests against it — see `08-RESEARCH.md` Section 1 for the exact
per-test rewrite spec (three renamed tests:
`test_every_spec_blocks_only_on_its_target_defect_at_critical_threshold_points`,
`test_ship_gate_findings_are_all_documented_incidental_corpus_gaps` (kept, but subtracts each
fixture's `_TARGET_DEFECT_CODES` before the allow-list check), and
`test_incidental_allowlist_names_no_slugs_own_target_code` (replacing the family-prefix check with
a fixture-scoped one)). Treat `08-RESEARCH.md` Section 1 as the load-bearing specification for this
rewrite; this PATTERNS.md file only reproduces the current structure it replaces.

---

### `tests/test_frame_boundary.py` — the paradigm-read scanner (D-14) and its two-proof pattern

**Current state, read in full (126 lines):** only `TestFrameImportBoundary` exists (D-03a's
`dsx.checks` import scanner). **No paradigm-read scanner exists yet** — `08-CONTEXT.md`'s D-14
assumed both Phase 7 and Phase 8 might land it; as of this pass, Phase 7's plan 07-03 has not
executed either. **The plan must write this scanner defensively** (check whether
`TestFrameParadigmReadBoundary` already exists — Phase 7 landed first — and skip creation if so, per
`08-RESEARCH.md` Section 2(d)).

**The two-proof pattern to mirror** (`tests/test_frame_boundary.py:92-122`, in full — this is the
exact structure D-14's new scanner class must replicate: one test scanning the real tree, a second
test proving the scanner actually fires against synthetic violating/permitted sources):
```python
class TestFrameImportBoundary(unittest.TestCase):
    def test_real_frame_modules_import_nothing_from_checks(self):
        violations: list[str] = []
        files = sorted(FRAME_DIR.rglob("*.py"))
        self.assertTrue(files, "dsx/frame/ has no *.py files to scan")
        for path in files:
            text = path.read_text(encoding="utf-8")
            package = _package_for(path)
            for problem in _scan_source_for_checks_imports(text, package):
                violations.append(f"{path.relative_to(ROOT)}: {problem}")
        self.assertEqual(violations, [], "\n".join(violations))

    def test_scanner_fires_on_violating_sources_and_permits_allowed_ones(self):
        violating_sources = [
            "from dsx.checks import design\n",
            "from ..checks import design\n",
            "import dsx.checks.design\n",
        ]
        for source in violating_sources:
            with self.subTest(source=source):
                result = _scan_source_for_checks_imports(source, "dsx.frame")
                self.assertTrue(result, f"expected a violation for: {source!r}")

        permitted_sources = [
            "from ..findings import Report\n",
            "from dsx.checksum import x\n",
        ]
        for source in permitted_sources:
            with self.subTest(source=source):
                self.assertEqual(_scan_source_for_checks_imports(source, "dsx.frame"), [])
```
The new scanner, per `08-RESEARCH.md` Section 2, must be a **directory glob** (`FRAME_DIR.rglob(
"*.py")`, matching `test_real_frame_modules_import_nothing_from_checks`'s own glob at line 95) with
`paradigm.py` hardcoded-excluded by name, plus two layered detectors: an AST detector (catching
`get(spec, "inference.paradigm")` string-literal args and `spec["inference"]["paradigm"]`
subscript chains) and a text-level substring scan (catching the bare string literal anywhere,
including comments). It must catch at least the three forms D-14 lists, verified against
deliberately-violating source strings the same way `test_scanner_fires_on_violating_sources_and_
permits_allowed_ones` does.

---

### `examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml` + `-POSTMORTEM.md` (new fixture pair)

**Analog:** the three existing pairs in `examples/known-bad/`, especially
`interference-shared-budget-ANALYSIS-SPEC.yaml` / `-POSTMORTEM.md` (same directory, same corpus
contract, same "full-shape clone of the good fixture" instruction from Phase 6's 06-08 decision).

**What structurally must be true** (verified against `tests/test_known_bad_corpus.py`):
1. `test_every_spec_has_a_sibling_postmortem_and_vice_versa` (line 131) — filename must be
   `triggering-dilution-ANALYSIS-SPEC.yaml` with sibling `triggering-dilution-POSTMORTEM.md`
   (exact slug match, set-symmetric-difference check, no content requirement beyond code-naming).
2. `test_every_spec_passes_dsx_validate` (line 166) — must declare **every** required
   `validity_frame` sub-block (all ten, since `needs_causal_block` will be true) with values inside
   their closed vocabularies — this is what makes `dsx validate` (structural-only) pass.
3. `test_every_postmortem_names_a_catch_attribution_finding_code` (line 176) — post-mortem text
   must contain `DSX-INT-030` (or another `DSX-<LETTERS>-<digits>` code) somewhere.
4. Per D-17: declare an additive metric (`type: count`/`sum`/`average`), `analysis_population:
   eligible`, `dilution_adjusted: false`, and `expected_trigger_rate < 1.0`.
5. Register in the new `_TARGET_DEFECT_CODES` map (above) as `{"plan": "DSX-INT-030"}`.

---

### `brief.md` §6.5 and `.planning/ROADMAP.md` — documentation edits

**Analog:** the five existing rows in the §6.5 gated-backlog table (`brief.md:364-390`, confirmed
by research to currently carry **zero** rows about ratio-metric dilution — D-12's rewrite is a
**new row**, not an edit). Follow the existing rows' column shape exactly (condition / status /
what would unblock it) when adding the ratio-metric-dilution row, per D-12's rewritten entry
condition (the mathematical blocker — Formula (3) needs per-user data, not an access blocker).

**Documentation-content test precedent** (D-18's fourth deliverable) —
`tests/test_known_bad_corpus.py:292` area,
`test_no_planning_document_misattributes_the_prior_averaged_bound` (greps planning documents for
prose drift against `_RETIRED_BOUND_MISATTRIBUTIONS`/`_BOUND_CLAIM_DOCUMENTS`, lines 74-94). Copy
this precedent's shape (a tuple of documents to scan, a tuple of forbidden/required substrings, a
test asserting presence or absence) for a new test asserting the §6.5 ratio-dilution row exists.

**ROADMAP success criteria 3 and 4** — reworded per D-10 ("against the Deng & Hu (2015) published
value" → "...published counterexample") and D-12 (the entry condition's true blocker restated as
the per-user-data limitation, not the access blocker). No code analog; this is a prose-only edit
guarded by the same documentation-content test mechanism above, since `.planning/ROADMAP.md` is one
of `_BOUND_CLAIM_DOCUMENTS`'s siblings in spirit.

## Shared Patterns

### Citation/Structural-criterion docstring discipline (D-05/D-06/D-19)
**Source:** `dsx/frame/paradigm.py:60-77` (check-function docstrings),
`dsx/mathx.py:435-448` (`design_effect()`, module-function docstrings)
**Apply to:** every `report.add(...)`-emitting helper in `dsx/frame/interference.py`, and the new
`dsx/mathx.py` dilution function. `Citation:` and `Structural criterion:` (checks) or `Citation:`
and `Reference value:` (math functions) are separate labelled paragraphs, greppable by
`scripts/gen-finding-catalogue.py`'s `_CITATION_RE`/`_REFVALUE_RE` regexes (lines 70-73):
```python
_CITATION_RE = re.compile(r"^\s*Citation:\s*\S", re.MULTILINE)
_REFVALUE_RE = re.compile(
    r"^\s*(?:Reference value|Structural criterion):\s*\S", re.MULTILINE
)
```
**CRLF caveat:** these regexes use `^`/`re.MULTILINE`, which Python's `re` module already treats as
matching after `\n` regardless of a preceding `\r` — `^` anchors are CRLF-safe in Python `re`
(unlike some other regex engines/languages). No change needed here, but flag any **new** regex a
plan writes for line-start/end matching (e.g. inside the new corpus-doc test or the paradigm-read
text scanner) to use `\r?\n` if it does its own line-splitting rather than relying on `re.MULTILINE`.

### Boolean-field declaration guard (`is not True`, not `is_blank`)
**Source:** `dsx/spec.py:369-376` (`is_blank`), contrasted with the correct idiom in
`08-RESEARCH.md` Section 3/Pitfall 2
**Apply to:** `_check_triggering_dilution` (`dilution_adjusted`) and `_check_stability_assessed`
(`novelty_primacy_assessed`) — both must use `value is not True`, never `is_blank(value)`.

### Free-text escape-hatch detection
**Source:** `dsx/spec.py:421-433` (`is_placeholder_or_refusal`)
**Apply to:** `residual_note` in `_check_interference_declared`. Reuse directly; do not add a
second helper (D-08 vs. research Section 4 — this is the one place `08-CONTEXT.md`'s decision is
superseded by already-landed Phase 7 code).

### `needs_causal_block` skip gate
**Source:** `dsx/spec.py:852-855`
**Apply to:** `_check_triggering_dilution` — and arguably `_check_interference_declared`/
`_check_stability_assessed` too, since all three sub-blocks are members of
`_VALIDITY_FRAME_CAUSAL_REQUIRED` and are absent from the spec entirely (not merely empty) when
`needs_causal_block` is false. In practice `section(spec, "validity_frame")` returning `{}` and each
sub-`section()` call returning `{}` for an absent sub-block already causes each check to no-op
naturally — but D-16 requires this be an explicit, testable condition, not an accidental one falling
out of empty-dict defaults.

### `dsx.checks` import boundary (D-03a)
**Source:** `tests/test_frame_boundary.py:35` (`_FORBIDDEN_PACKAGE = "dsx.checks"`)
**Apply to:** `dsx/frame/interference.py` — verified automatically by the existing
`TestFrameImportBoundary.test_real_frame_modules_import_nothing_from_checks` glob (no test edit
needed, the glob picks up the new file automatically).

## No Analog Found

None. Every file this phase touches or creates has a concrete, current, directly-read analog in the
codebase — this is a mature, template-driven repo where Phase 6/7 already established every shape
Phase 8 needs.

## Metadata

**Analog search scope:** `dsx/frame/`, `dsx/spec.py`, `dsx/mathx.py`, `dsx/cli.py`,
`scripts/gen-finding-catalogue.py`, `tests/test_frame_boundary.py`,
`tests/test_known_bad_corpus.py`, `tests/test_dsx.py` (selected ranges), `examples/known-bad/`,
`dsx/checks/design.py` (novelty-text disjointness check only).
**Files scanned:** 11 source/test files read directly (several in full), plus both upstream
planning documents (08-CONTEXT.md, 08-RESEARCH.md) in full.
**Pattern extraction date:** 2026-08-12
