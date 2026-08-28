# Phase 9: Monitoring discipline, symmetric (`DSX-PAR-*`) - Pattern Map

**Mapped:** 2026-08-12
**Files analyzed:** 9 (3 modified core files, 4 fixture/reference files, 2 new test files)
**Analogs found:** 9 / 9 (every file has a same-repo analog; nothing routes to RESEARCH.md-only guidance)

Note (CLAUDE.md line-ending rule): none of the analogs below are regex/parser code that
matches line starts/ends (`^`/`$`) against file content, so the `\r?\n` caution does not
apply to any excerpt quoted here. If the planner adds a regex-based drift guard over
markdown/YAML content (e.g. for `references/paradigm-symmetry.md`'s positive-content
test, D-15), it must use `\r?\n`, not `\n`, per CLAUDE.md — this repo checks out CRLF on
Windows and `tests/test_known_bad_corpus.py`'s existing guards already sidestep the
issue by normalizing whitespace (`" ".join(text.split())`) rather than matching lines.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|--------------------|------|-----------|-----------------|----------------|
| `dsx/frame/paradigm.py` (add 3 `_check_*` fns) | frame check / controller-equivalent | request-response (spec in, `Report` out) | same file, existing `check()` (`DSX-PAR-001`) + `dsx/checks/design.py::_check_peeking` (`DSX-EXP-060`) | exact (same module for shape; sibling module for the `_check_*` decomposition idiom) |
| `dsx/spec.py` (`_INFERENCE_FIELDS` +3, no new membership vocab required) | model / schema (contract layer) | CRUD (schema drift-guard) | `dsx/spec.py::_INFERENCE_FIELDS` + `_INFERENCE_MEMBERSHIP` (same file, lines 946-955) | exact |
| `dsx/mathx.py::inflation_from_peeking()` (docstring-only upgrade, D-13) | utility / pure function | transform | same function; sibling `z_score_for_looks`-style table above it (lines ~400-408) for the "tabulated anchors + interpolation" idiom | exact (no new function — same function edited) |
| `templates/ANALYSIS-SPEC.yaml` (`inference:` scaffold +3 commented fields) | config / scaffold | transform (documentation-as-schema) | same file's existing `inference:` block (lines 343-352) | exact |
| `references/paradigm-symmetry.md` (new, D-15) | doc / evidence artifact | batch (static, generated-by-hand not by code) | `references/finding-codes.md` (sibling committed doc) — no closer analog exists; nearest structural neighbour, not a true match | no-analog (see below) |
| `tests/test_dsx.py` (extend `TestParadigm`-equivalent class, `_INFERENCE_FIELDS` drift guard, retype tests) | test | request-response (unit, spec-construction style) | `tests/test_dsx.py::test_applied_prefixes_have_codes_and_not_shipped_prefixes_have_none` (lines 2711-2733) and the `codes()` helper (line 26) | exact |
| `tests/test_known_bad_corpus.py` (restructure D-03: per-fixture expected-caught-defect set) | test | request-response (CLI subprocess-equivalent via `cli.main`) | same file's `_gate_findings` helper (lines 108-127) + `test_every_spec_passes_the_critical_threshold_gate_points` (lines ~186-199) | exact |
| `tests/test_par_monitoring_simulation.py` (new, D-14) | test / simulation | batch (seeded Monte Carlo, stdlib-only) | `scripts/check.sh`'s "identical input, identical output" determinism idiom (referenced at RESEARCH.md line 477); no existing seeded-simulation test file exists in-repo to copy structurally — nearest analog is the `unittest.TestCase` + `random.Random(seed)` convention implied by the repo's stdlib-only constraint, not a concrete file | partial (no existing seeded-simulation test file; see below) |
| `examples/known-bad/frequentist-uncontrolled-continuous-*` and `bayesian-continuous-monitoring-*` (header/post-mortem prose update only) | fixture / documentation | file-I/O (static YAML + MD read by tests) | same files, current "nothing adjudicates it today" prose (frequentist spec header lines 162-170; bayesian post-mortem, D-10-corrected prose already in place) | exact (editing existing files, not creating new ones) |

## Pattern Assignments

### `dsx/frame/paradigm.py` — three new `_check_*` functions

**Analog 1 (structure/shape to copy exactly):** `dsx/checks/design.py:444-471` — `_check_peeking` / `DSX-EXP-060`

```python
# Source: dsx/checks/design.py:444-471 (verified this session)
def _check_peeking(design: dict, spec: dict, report: Report) -> None:
    policy = normalize(design.get("peeking_policy", "")) if design else ""
    looks = as_number(get(spec, "results.interim_looks"))
    if looks is None:
        return
    looks = int(looks)

    if policy in ("", "fixed_horizon") and looks > 1:
        inflated = inflation_from_peeking(looks, as_number(design.get("alpha")) or 0.05)
        report.add(
            "DSX-EXP-060",
            "CRITICAL",
            f"{looks} interim looks were taken under a fixed-horizon design",
            detail=(
                f"Repeatedly testing the same accumulating data inflates the true type-I error "
                f"from {as_number(design.get('alpha')) or 0.05:.2f} to roughly {inflated:.2f}. "
                "Any 'significant' reading here is not significant at the stated level."
            ),
            remedy=(
                "Either report only the final pre-declared analysis, or switch the design to "
                "sequential_obf / always_valid and re-evaluate against the corrected boundary."
            ),
            where="spec.results.interim_looks",
            interim_looks=looks,
            inflated_alpha=round(inflated, 4),
        )
    elif looks > 1:
        report.ok(f"{looks} interim looks under policy '{policy}'")
```

This is the `_check_*(design_or_spec, report) -> None` shape the three new functions
should follow: a private module-level function, one early return for the non-applicable
case, one `report.add(CODE, SEVERITY, f"...", detail=..., remedy=..., where=..., **data)`
call for the finding case, called from the module's `check()` before `return report`.
**Do not** call `inflation_from_peeking()` a second time from a new helper table —
`DSX-PAR-010` must import and call this exact function (`from ..mathx import
inflation_from_peeking`), the same import idiom `dsx/checks/design.py:11-18` already
shows (`from ..mathx import (inflation_from_peeking, mde_two_proportions, ...)`).

**Analog 2 (docstring citation placement, registration idiom, decision-record emission):**
`dsx/frame/paradigm.py:60-163` — the existing `DSX-PAR-001` `check()` (already quoted in
full above under Existing Code Insights; reproduced here for the load-bearing citation
shape):

```python
# Source: dsx/frame/paradigm.py:60-77 (verified this session)
def check(spec: dict) -> Report:
    """Emit DSX-PAR-001 — the informational paradigm manifest.

    Citation: Deng, A., Lu, J. & Chen, S. (2016), "Continuous Monitoring of
    A/B Tests without Pain: Optional Stopping in Bayesian Testing", IEEE
    DSAA 2016 — the primary source establishing that a decision procedure's
    realised error rate is paradigm-dependent, which is what makes an
    undeclared paradigm a real gap rather than a formality. The exact
    section/theorem locator within this paper is unverified at time of
    writing (same citation, same flag as
    ``dsx/spec.py::_validate_inference_shape``, escalated in the 06-06 plan
    summary rather than invented); author/year/title/venue match brief.md
    section 7.
    Structural criterion: a set-membership computation over a data-driven
    applicability map (...), keyed by every member of ``PARADIGMS`` plus the
    undeclared case — no numeric threshold or statistic is computed here.
    """
```

**Critical mechanical point (Pitfall 2, verified against
`scripts/gen-finding-catalogue.py:193-232`):** `check_d05()`'s docstring resolver walks
up from each `report.add(...)` call site to the **nearest enclosing function**, and only
falls back to the module docstring if no enclosing function exists. Because the three new
checks will be separate `_check_*` functions (not inline in `check()`), **each one needs
its own docstring** carrying `Citation:` and (for `DSX-PAR-010`/`DSX-PAR-011`, which have
numeric anchors) a `Reference value:` line — putting the citation only on `check()`'s
docstring, or only on the module docstring, will make `scripts/gen-finding-catalogue.py
--check` fail with a missing-citation error even though a citation is visibly present
somewhere in the file. `_D05_ALLOWLIST_PREFIXES` already covers `DSX-PAR-`
(`scripts/gen-finding-catalogue.py:58`), so no script edit is needed — only correct
placement.

**Registration idiom to extend, not replace (D-06's structural-not-branching requirement):**

```python
# Source: dsx/frame/paradigm.py:38-41 (verified this session)
_PARADIGM_CONDITIONAL: "dict[str, tuple[str, ...]]" = {
    "frequentist": ("DSX-PAR-010", "DSX-ADM-"),
    "bayesian": ("DSX-PAR-011",),
}
```
This dict already names `DSX-PAR-010`/`DSX-PAR-011` as the applicable codes per paradigm
— no edit needed to this dict itself for the pair to register in the manifest; the edit
needed is removing the three matching keys from `_NOT_SHIPPED` (below) in the same commit
each code ships, and adding the three new `_check_*(spec, report)` calls inside `check()`.

**`_NOT_SHIPPED` entries that must be removed (verified, `dsx/frame/paradigm.py:49-57`):**
```python
_NOT_SHIPPED: "dict[str, str]" = {
    ...
    "DSX-PAR-002": "Phase 9 ships DSX-PAR-002 alongside the symmetric monitoring pair.",
    "DSX-PAR-010": "Phase 9 ships DSX-PAR-010 (frequentist monitoring discipline).",
    "DSX-PAR-011": "Phase 9 ships DSX-PAR-011 (bayesian monitoring discipline).",
    ...
}
```
`tests/test_dsx.py:2732` (`test_applied_prefixes_have_codes_and_not_shipped_prefixes_have_none`)
asserts every remaining `_NOT_SHIPPED` prefix resolves to zero known codes — each entry
above must be deleted in the same commit that lands its code, or this test goes red.

**Decision-record emission pattern (brief D-04), to copy per new check:**

```python
# Source: dsx/frame/paradigm.py:146-161 (verified this session)
report.context.setdefault("decisions", []).append(
    DecisionRecord(
        id="",
        invocation_id="",
        layer="deterministic",
        choice=choice,
        inputs=["inference.paradigm"],
        rule=(...),
        citation="Deng, Lu & Chen (2016), Continuous Monitoring of A/B Tests without Pain",
        counterfactual=counterfactual,
    ).to_dict()
)
```

**Title-literal pitfall (Pitfall 3):** `report.add`'s third positional arg (the title)
must be a `Constant`/`JoinedStr` literal built inline at the call site — see the comment
at `dsx/frame/paradigm.py:112-116` explaining why (`scripts/gen-finding-catalogue.py`'s
AST extractor requires it; a pre-assigned variable collapses to `<…>` in the generated
catalogue).

---

### The `DSX-PAR-010`/`DSX-PAR-011` citation + severity template — `DSX-PAR-001` and existing `DSX-SPEC-085`

**How citation enforcement finds a code (mechanism, not just idiom):**
`scripts/gen-finding-catalogue.py:193-232` (`_resolve_docstrings`) walks from each
`report.add("DSX-PAR-0xx", ...)` call site up the AST to the nearest enclosing
`FunctionDef`, reads that function's docstring, and requires a `Citation:` line (and,
per the catalogue's D-05 rule, a `# D-05: <CODE>` marker present somewhere under `tests/`
— the test file the planner adds must carry this marker comment next to its
`DSX-PAR-010`/`DSX-PAR-011` assertions, mirroring how existing `# D-05: <CODE>` markers
appear elsewhere in `tests/`).

**Severity + citation declaration together, existing sibling with a numeric anchor
(closest existing "code + severity + citation" triple outside `paradigm.py` itself):**

```python
# Source: dsx/spec.py:962-995 (verified this session, _validate_inference_shape)
def _validate_inference_shape(spec: dict, report: Report) -> None:
    """Shape validation of the optional ``inference:`` block.

    Codes DSX-SPEC-085 (sub-field outside its closed vocabulary) and DSX-SPEC-086 (the
    field M-02 removed is declared).

    Citation: Deng, A., Lu, J. & Chen, S. (2016), "Continuous Monitoring of A/B Tests
    without Pain: Optional Stopping in Bayesian Testing", IEEE DSAA 2016 — ...
    Structural criterion: presence-and-membership test on three closed-vocabulary
    sub-fields, plus a fourth check for the presence of a removed field name. No
    numeric threshold is computed here.
    """
    ...
    report.add(
        "DSX-SPEC-085",
        "HIGH",
        f"inference.{field_name} {value!r} is not recognised",
        detail="Allowed: " + ", ".join(sorted(vocab)),
        remedy=f"Set inference.{field_name} to one of the allowed values.",
        where=f"spec.inference.{field_name}",
    )
```
`DSX-PAR-002` (HIGH, per D-02) is this pattern's direct sibling in severity and shape —
requiredness/absence rather than membership, symmetric across `PARADIGMS`, HIGH not
CRITICAL. `DSX-PAR-010`/`DSX-PAR-011` (CRITICAL, per D-02) should instead mirror
`DSX-EXP-060`'s severity and `detail=`/`remedy=`/numeric-`where=` shape (quoted above) —
`DSX-EXP-060` is explicitly named in CONTEXT.md as "the template for what a peeking
finding's detail should read like — and the one `DSX-PAR-010` must be distinguishable
from at a glance."

For the `Reference value:` docstring line specifically (D-11/D-12's numeric anchor),
there is no existing exact analog carrying that literal heading in this codebase — the
nearest structural neighbour is `_validate_validity_frame_shape`'s multi-citation
docstring (`dsx/spec.py:825-849`, quoted below) which stacks several `Citation:` lines
under one `Structural criterion:` line; the planner should follow that same
one-heading-per-line convention, adding `Reference value: 1/(K+1) = 0.05 at K=19 (p=0.95)`
as its own line rather than folding it into `Citation:` prose.

```python
# Source: dsx/spec.py:825-849 (verified this session) — multi-citation docstring shape
def _validate_validity_frame_shape(spec: dict, report: Report) -> None:
    """Requiredness, aggregation and membership shape of the ``validity_frame:`` block.

    Codes DSX-SPEC-080 (block absent), DSX-SPEC-081 (required sub-block missing, one
    finding per sub-block per D-11) and DSX-SPEC-082 (sub-field outside its closed
    vocabulary).

    Citation: Hernan, M.A. & Robins, J.M. (2020), *Causal Inference: What If*, Chapter 1
    ("A Definition of Causal Effect") and Chapter 3 ("Observational Studies") — ...
    Citation: Little, R.J.A. & Rubin, D.B. (2019), *Statistical Analysis with Missing
    Data*, 3rd ed., Chapter 1 ("Introduction") — ...
    Citation: Imbens, G.W. & Rubin, D.B. (2015), *Causal Inference for Statistics,
    Social, and Biomedical Sciences*, Chapter 1, Section 1.6 ("The Stable Unit Treatment
    Value Assumption") — ...
    Structural criterion: presence-and-membership test, not a numeric one. ...
    """
```

---

### `dsx/mathx.py::inflation_from_peeking()` — D-13's docstring-only citation upgrade

**Current signature and docstring (verified, `dsx/mathx.py:411-432`):**
```python
def inflation_from_peeking(total_looks: int, alpha: float = 0.05) -> float:
    """Approximate true type-I error when a fixed-horizon test is peeked ``n`` times.

    Armitage's classic result: repeated naive testing at alpha=0.05 reaches roughly
    0.08 at 2 looks, 0.11 at 3, 0.14 at 5, 0.19 at 10. Interpolated linearly in
    log-looks between the tabulated anchors, then scaled by alpha/0.05.
    """
    if total_looks < 1:
        raise ValueError("total_looks must be >= 1")
    anchors = {1: 0.05, 2: 0.083, 3: 0.107, 4: 0.126, 5: 0.142, 10: 0.193, 20: 0.248}
    if total_looks in anchors:
        value = anchors[total_looks]
    else:
        keys = sorted(anchors)
        if total_looks > keys[-1]:
            value = anchors[keys[-1]]
        else:
            lo = max(k for k in keys if k < total_looks)
            hi = min(k for k in keys if k > total_looks)
            weight = (math.log(total_looks) - math.log(lo)) / (math.log(hi) - math.log(lo))
            value = anchors[lo] + weight * (anchors[hi] - anchors[lo])
    return min(1.0, value * alpha / 0.05)
```

**Existing caller — `DSX-EXP-060` — is the exact call-site idiom `DSX-PAR-010` must
reuse verbatim (do not disturb this call, M-01):**
```python
# Source: dsx/checks/design.py:452 (verified this session)
inflated = inflation_from_peeking(looks, as_number(design.get("alpha")) or 0.05)
```
`DSX-PAR-010` calls this same function the same way: `inflation_from_peeking(<looks
derived from the declared design, not results.interim_looks per D-04>, <declared alpha,
default 0.05>)`. **D-13 requires the docstring upgrade to be elective and additive only**
— it must remain purely a docstring edit; no `report.add` call may be introduced into
`dsx/mathx.py` (there is none today, and none should be added — D-13 explicitly notes
`check_d05()` never reaches this function mechanically because it contains no
`report.add`, and that must stay true).

---

### `DSX-PAR-001` and `DSX-PAR-002` — shipped-family template for symmetry

**`DSX-PAR-001`** is fully quoted above (module docstring + `check()` body,
`dsx/frame/paradigm.py:1-163`). Its structural pattern — data-driven applicability via
`_PARADIGM_CONDITIONAL`, no per-paradigm `if`/`elif` — is exactly what D-06/D-09 require
the new pair's *trigger* logic and `DSX-PAR-002`'s *membership-independence* to inherit.

**`DSX-PAR-002` does not exist yet** — CONTEXT.md D-08 states this explicitly: the
vocabulary it validates against (`PARADIGM_JUSTIFICATIONS`) already exists at
`dsx/spec.py:251-265`, but the code itself is new. Its nearest same-repo analog for
"requiredness on an absent value that a sibling code already handles for membership" is
`dsx/spec.py`'s own `is_blank(value): continue` skip inside `_validate_inference_shape`'s
membership loop (quoted above, `dsx/spec.py:1010-1014`) — that `continue` is precisely
the gap `DSX-PAR-002` must fill, by checking presence/requiredness of
`inference.paradigm_justification` (and, per D-07, arguably `inference.paradigm` itself)
where `_validate_inference_shape` currently says nothing.

```python
# Source: dsx/spec.py:251-265 (verified this session) — PARADIGM_JUSTIFICATIONS,
# the closed vocabulary DSX-PAR-002 must NOT re-check membership against
# (DSX-SPEC-085 already owns membership; re-checking double-fires — D-08)
# No description ranks one reason above another (D-12 symmetry).
PARADIGM_JUSTIFICATIONS = {
    "prior_information_available": "Credible external information exists to form an informative prior.",
    "sequential_monitoring_required": (
        "The analysis requires continuous or repeated looks at accumulating data."
    ),
    "decision_theoretic_loss_specified": (
        "A decision rule with an explicit loss function drives the analysis."
    ),
    ...  # 7 members total, per CONTEXT.md D-08
}
```

---

### Known-bad fixture + test pairing idiom (D-03)

**The fixture (verified, `examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml:162-170`):**
```yaml
# ── Inference plan (REQ-P6-04) ───────────────────────────────────────────────
# The defect: design.peeking_policy is uncontrolled_continuous (five interim
# looks, no sequential correction, no anytime-valid method) yet the analysis
# uses an ordinary fixed-horizon test statistic (two_proportion_z). At a
# nominal alpha of 0.05 with 5 interim looks, the true type-I error is
# approximately 0.142 (dsx.mathx.inflation_from_peeking(5) == 0.142; Armitage,
# McPherson & Rowe 1969). No sequential method is named in primary_procedure —
# that absence is itself part of the defect.
inference:
  paradigm: frequentist            # frequentist | bayesian
  paradigm_justification: team_convention
  declared_at: pre_data            # pre_data | post_data
  primary_procedure: two_proportion_z
  alpha_spending: null
  fallback_rule: ""
```
This fixture already declares `design.peeking_policy: uncontrolled_continuous` (verified
via header comment) and needs **no field changes** to trigger `DSX-PAR-010` once it
ships — only its header prose ("nothing adjudicates it today") becomes false and must be
updated, per CONTEXT.md's canonical_refs.

**The test asserting exit `1` naming a specific code (`_gate_findings` helper, the exact
idiom D-03's restructured per-fixture assertions must reuse):**
```python
# Source: tests/test_known_bad_corpus.py:108-127 (verified this session)
def _gate_findings(self, spec_path: Path, point: str) -> tuple[int, list[dict]]:
    """Run one real ``dsx gate <point>`` against one fixture and return
    ``(exit_code, findings)``. ..."""
    with tempfile.TemporaryDirectory() as tmp:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(
                ["gate", point, "--spec", str(spec_path), "--phase-dir", tmp, "--json"]
            )
        raw = err.getvalue() or out.getvalue()
        report = json.loads(raw)
    return code, report["findings"]
```
And the assertion shape it currently backs (verified, `tests/test_known_bad_corpus.py`
around lines 186-199 — the exact test D-03 must split into a per-fixture
expected-caught-defect version):
```python
def test_every_spec_passes_the_critical_threshold_gate_points(self):
    """The corpus's positive gate guarantee: every fixture clears both
    CRITICAL-threshold gate points, `plan` and `execute`, today."""
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
**D-03's required shape:** for the two monitoring fixtures specifically, this assertion
flips from `assertEqual(code, 0, ...)` to asserting `code == 1` **and** that the specific
target code (`DSX-PAR-010` for the frequentist fixture, `DSX-PAR-011` for the Bayesian
one) is present in `[f["code"] for f in findings if f["severity"] == "CRITICAL"]` — while
every other fixture (e.g. `interference-shared-budget-*`, whose target family
`DSX-INT-010` has not shipped) keeps the current `assertEqual(code, 0, ...)` form. This
is a per-fixture dict/set of expected-caught-defect codes, not a single blanket assertion
— exactly the "per-fixture expected-caught-defect set" CONTEXT.md D-03 specifies.

**The allow-list guard that must not be weakened (verified,
`tests/test_known_bad_corpus.py:80-93`):**
```python
_TARGET_CODE_FAMILIES = ("DSX-INT-", "DSX-PAR-01")

_INCIDENTAL_GAP_CODES = {
    "DSX-CLM-031", "DSX-COH-031", "DSX-EXP-007", "DSX-MET-040",
    "DSX-NAR-001", "DSX-REP-001", "DSX-REP-030", "DSX-STA-041",
}

def test_incidental_allowlist_names_no_target_family_code(self):
    """... the fixtures block only on completeness gaps, never on the semantic defect
    they exist to encode ..."""
    for code in sorted(_INCIDENTAL_GAP_CODES):
        for family in _TARGET_CODE_FAMILIES:
            with self.subTest(code=code, family=family):
                self.assertFalse(
                    code.startswith(family),
                    f"{code} is in the incidental-gap allow-list but belongs to target "
                    f"family {family!r} — a fixture would then never block on the "
                    "defect it exists to encode even after that code ships",
                )
```
`_TARGET_CODE_FAMILIES` **already contains `"DSX-PAR-01"`** — this guard is
pre-positioned for Phase 9 and forbids adding `DSX-PAR-010`/`DSX-PAR-011` to
`_INCIDENTAL_GAP_CODES` as a shortcut. Do not touch this constant or this test.

---

### D-10 regression-guard idiom (Deng/Ville misattribution retirement) — reusable for any new prose

```python
# Source: tests/test_known_bad_corpus.py:81-94 (verified this session)
_RETIRED_BOUND_MISATTRIBUTIONS = (
    "prior-averaged Ville bound",
    "martingale (Ville's inequality) argument",
    "commonly rounded and reported as",
)

_BOUND_CLAIM_DOCUMENTS = (
    ROOT / "brief.md",
    ROOT / ".planning" / "REQUIREMENTS.md",
    ROOT / ".planning" / "ROADMAP.md",
)
```
Matched against whitespace-normalized text (`" ".join(text.split())`) — this is the
existing repo idiom for line-ending-tolerant substring guards, and it already sidesteps
the CRLF-vs-LF concern CLAUDE.md flags for any new regex the planner might add, by never
matching on line boundaries at all.

---

### Seeded/reproducible test pattern (REQ-P9-07 simulation, D-14) — no exact analog exists

**Explicit statement, per CLAUDE.md's "Verification Before Claiming":** a repo-wide
search finds **no existing `tests/test_*simulation*.py` file, and no existing
`random.Random(seed)` usage anywhere under `tests/`** (verified via grep this session —
zero matches for `random.Random` under `tests/`). The nearest structural neighbours are:

1. **The determinism idiom named in RESEARCH.md** (`scripts/check.sh:27-31`) — "identical
   input, identical output" — which the planner should mirror at the assertion level (run
   the same seed twice, assert identical summary statistics), but this is a shell-script
   check comparing two `dsx audit` invocations, not a Python unittest pattern to copy
   structurally.
2. **`tests/test_known_bad_corpus.py`'s `unittest.TestCase` + `tempfile` + stdlib-only
   idiom** (the whole file, already quoted above) — the closest available example of a
   stdlib-only, no-external-dependency test class in this repo's own style (imports,
   `ROOT = Path(__file__).resolve().parent.parent`, `sys.path.insert`), even though its
   subject matter (fixture gating, not Monte Carlo) differs.

The planner should treat REQ-P9-07's simulation as new structural territory: a
`unittest.TestCase` under `tests/`, using only `random.Random(seed)` and `math`/`statistics`
from stdlib, asserting (a) a monotone-trend property under the point-null formulation and
(b) a fixed `1/(K+1)` ceiling under the prior-averaged formulation (D-14) — following the
repo's general test-file conventions (module docstring naming the `unittest` run command,
`ROOT`/`sys.path` boilerplate matching `tests/test_known_bad_corpus.py:1-24`) rather than
copying any single existing test's body.

---

### Decision-record API (referenced throughout CONTEXT.md)

```python
# Source: dsx/decisions.py:64-88 (verified this session)
@dataclass(frozen=True)
class DecisionRecord:
    """One decision-trail entry — brief section 5.5's schema.

    ``counterfactual`` is the field that teaches: what would have made this
    choice go the other way. Mirrors ``dsx.findings.Finding``'s frozen-dataclass
    idiom.
    """

    id: str
    invocation_id: str
    layer: str
    choice: str
    inputs: "list[str]" = field(default_factory=list)
    rule: str = ""
    citation: str = ""
    counterfactual: str = ""
    alternatives_rejected: "list[str]" = field(default_factory=list)
    confidence: "str | None" = None
    escalate: bool = False

    def to_dict(self) -> "dict[str, Any]":
        out = asdict(self)
        out["record_type"] = "decision"
        return out
```
Two existing call sites show the emission idiom to copy for each new check:
`dsx/frame/paradigm.py:146-161` (quoted above, `DSX-PAR-001`'s own emission) and
`dsx/spec.py:890-914`/`962-1008` (`_validate_inference_shape`'s emission, quoted above,
using `layer="deterministic"`, `id=""`, `invocation_id=""` — both left for the CLI layer
to fill in per brief D-04's "checks stay pure, only the CLI writes the trail file" rule).

## Shared Patterns

### Citation-bearing docstring, per enclosing function
**Source:** `dsx/frame/paradigm.py:60-77` and `dsx/spec.py:825-849, 973-1000`
**Apply to:** all three new `_check_*` functions in `dsx/frame/paradigm.py`
**Rule:** `Citation:` (and `Reference value:` for the two numeric-anchor codes) must sit
on the **enclosing function's own docstring**, never the module docstring — verified
mechanically load-bearing via `scripts/gen-finding-catalogue.py:193-232`.

### `report.add(CODE, SEVERITY, f"<inline literal title>", detail=, remedy=, where=, **data)`
**Source:** `dsx/checks/design.py:452-469`, `dsx/frame/paradigm.py:117-126`, `dsx/spec.py:1015-1022`
**Apply to:** all three new checks. Title must be a literal `f"..."` built inline at the
call site (Pitfall 3) — never a pre-assigned variable.

### Data-driven applicability map, never `if`/`elif` on a closed vocabulary
**Source:** `dsx/frame/paradigm.py:38-41` (`_PARADIGM_CONDITIONAL`)
**Apply to:** any per-paradigm branching inside the new checks (D-06, D-09) — extend the
existing dict/test-set-equality idiom, do not write `if paradigm == "frequentist": ...`.

### `DecisionRecord` emission via `report.context.setdefault("decisions", [])`
**Source:** `dsx/decisions.py:64-88`, used at `dsx/frame/paradigm.py:146-161` and
`dsx/spec.py:890-914`
**Apply to:** each new check's key judgement point (brief D-04 — never block to teach).

### `_gate_findings` + `cli.main([...])` subprocess-equivalent test idiom
**Source:** `tests/test_known_bad_corpus.py:108-127`
**Apply to:** the D-03 per-fixture restructuring and any new REQ-P9-05 bidirectional
retype test in `tests/test_dsx.py`.

### Whitespace-normalized substring guard (line-ending tolerant)
**Source:** `tests/test_known_bad_corpus.py` (`" ".join(text.split())` pattern, used
throughout the D-10 regression guards)
**Apply to:** any new positive-content test over `references/paradigm-symmetry.md`
(D-15) or docstring-content assertions (REQ-P9-03) — avoids the CRLF/`\r?\n` line-start
matching pitfall CLAUDE.md flags, by never matching on line boundaries.

## No Analog Found

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| `references/paradigm-symmetry.md` | doc / evidence artifact | batch | No committed audit-style markdown file with this shape exists yet in `references/`; nearest neighbour is `references/finding-codes.md` (a generated catalogue, not a hand-written audit) and `tests/test_known_bad_corpus.py:270-326`'s positive-content-test idiom (for the test that checks it, not the doc itself). Verified via `Glob("references/**/*.md")` — only `finding-codes.md` exists there today. |
| `tests/test_par_monitoring_simulation.py` (or equivalent) | test / simulation | batch (seeded Monte Carlo) | Verified via repo-wide grep: zero existing uses of `random.Random` under `tests/`, no existing simulation-style test file. This is new structural territory within the repo's general stdlib-only `unittest.TestCase` conventions (see above), not a file with a direct same-shape analog. |

## Metadata

**Analog search scope:** `dsx/frame/`, `dsx/checks/`, `dsx/spec.py`, `dsx/mathx.py`,
`dsx/decisions.py`, `dsx/findings.py`, `tests/test_dsx.py`, `tests/test_known_bad_corpus.py`,
`tests/test_frame_boundary.py`, `examples/known-bad/`, `references/`, `templates/`,
`scripts/gen-finding-catalogue.py`.
**Files scanned:** 14 read directly this session (targeted ranges, non-overlapping),
plus repo-wide greps for `random.Random`, `_INFERENCE_FIELDS`, `_NOT_SHIPPED`,
`_gate_findings`/`codes(`.
**Pattern extraction date:** 2026-08-12
