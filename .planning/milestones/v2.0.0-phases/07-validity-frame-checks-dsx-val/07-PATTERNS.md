# Phase 7: Validity frame checks (`DSX-VAL-*`) - Pattern Map

**Mapped:** 2026-08-12
**Files analyzed:** ~14 (1 new module, 2 new fixture artifacts, 4 edited fixtures, 3 build-plumbing
edits, 2 doc-only edits, plus test additions across `tests/test_dsx.py` and
`tests/test_frame_boundary.py`)
**Analogs found:** 14 / 14

**Note on scope:** `07-RESEARCH.md` already extracts, with file:line citations, the primary analog
for `dsx/frame/val.py` (→ `dsx/frame/paradigm.py`), the `dsx/cli.py` registration mechanics, the
`scripts/gen-finding-catalogue.py` D-05 contract, and `dsx/mathx.py` conventions in full. This
document does not repeat those blocks — see `07-RESEARCH.md` §§1–3, §7 for the primary module-shape
excerpts. This document adds the analogs `07-RESEARCH.md` covered only in prose: test files, YAML
fixtures/post-mortems, `dsx/spec.py` module-constant precedents, and the two documentation-only
edits.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `dsx/frame/val.py` | check module (frame layer) | request-response (dict in, `Report` out) | `dsx/frame/paradigm.py` | exact (see 07-RESEARCH.md §1) |
| `dsx/spec.py` (dependence→method map constant) | module-level constant | CRUD-adjacent lookup table | `dsx/spec.py:53` `CAUSAL_VERBS` (exclusion precedent) | exact |
| `dsx/spec.py` (falsifier lexicon + placeholder detector) | module-level constant + helper | transform (text→bool classification) | `dsx/checks/narrative.py:17-21`, `dsx/checks/claims.py:107-113` (idiom only — cannot be imported, D-03a) | role-match, re-homed |
| `dsx/mathx.py::design_effect()` | utility (pure function) | transform | `dsx/mathx.py::inflation_from_peeking()` (see 07-RESEARCH.md §7) | exact |
| `dsx/cli.py` (`CHECKS`, `GATE_PROFILES`) | config/registration | request-response | `dsx/cli.py:63-101` existing `paradigm` entries (see 07-RESEARCH.md §2) | exact |
| `scripts/gen-finding-catalogue.py` (`PREFIX_GROUPS`, `_D05_ALLOWLIST_PREFIXES`) | build/config | batch | existing `DSX-PAR` entry (see 07-RESEARCH.md §3) | exact |
| `dsx/frame/paradigm.py` (`_NOT_SHIPPED` edit) | config constant | — | itself, edited in place | exact |
| `tests/test_dsx.py` — unit tests for `val.check(spec)` | test (unit) | request-response | `tests/test_dsx.py:390-474` (`DSX-SPEC-080/081/082` tests) | exact |
| `tests/test_dsx.py` — gate-level exit-code tests | test (integration/CLI) | request-response | `tests/test_dsx.py:1183-1244` (`TestCLI`, `_run` helper) | exact |
| `tests/test_dsx.py` — `mathx.design_effect()` reference-value test | test (unit, numeric) | transform | `tests/test_dsx.py:33-70` (`TestMath`) | exact |
| `tests/test_frame_boundary.py` — REQ-P7-09 no-`inference.paradigm`-read test | test (AST/text invariant) | batch/scan | `tests/test_frame_boundary.py` (`TestFrameImportBoundary`, full file) | role-match (different invariant, same scanner idiom) |
| `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` | fixture (YAML) | file-I/O | `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml` | exact |
| `examples/known-bad/weak-identification-mmm-POSTMORTEM.md` | doc fixture | file-I/O | `examples/known-bad/interference-shared-budget-POSTMORTEM.md` | exact |
| `templates/ANALYSIS-SPEC.yaml`, `examples/good-ANALYSIS-SPEC.yaml`, `examples/known-bad/*.yaml` (D-12/13/14 edits) | fixture (YAML) | file-I/O | the same files, edited in place; boilerplate cloned from `interference-shared-budget-ANALYSIS-SPEC.yaml`'s `validity_frame:` block shape | exact |
| `brief.md` §7 | doc (reference list) | — | itself, `brief.md:434-451`, edited in place | exact |
| `.planning/research/FEATURES.md` (3.45 correction) | doc (research) | — | itself, `:44-57`, edited in place | exact |

## Pattern Assignments

### `tests/test_dsx.py` — unit tests for `val.check(spec)` (test, unit)

**Analog:** `tests/test_dsx.py:390-474` — the `DSX-SPEC-080/081/082` block-shape tests. This is the
named analog in `07-RESEARCH.md` §6; quoted here in full so a new `DSX-VAL-0NN` test class can
mirror the exact idiom (dict-literal spec, direct call to the checker, `codes()`/`f.code` assertions,
`# D-05:` marker on the line above the test).

```python
def test_causal_spec_with_no_validity_frame_key_reports_one_critical_itemising_ten(self):
    # D-05: DSX-SPEC-080
    report = validate_structure(
        {"spec_version": 1, "title": "t", "question_type": "causal", "decision": {"owner": "x"}}
    )
    found = [f for f in report.findings if f.code == "DSX-SPEC-080"]
    self.assertEqual(len(found), 1)
    detail = found[0].detail
    for name in (
        "estimand", "units", "measurement", "dependence", "sampling_frame", "missingness",
        "identification", "interference", "triggering", "stability",
    ):
        self.assertIn(name, detail)
```

```python
def test_out_of_vocabulary_sub_field_reports_high_with_allowed_members(self):
    # D-05: DSX-SPEC-082
    spec = {
        "spec_version": 1, "title": "t", "question_type": "descriptive", "decision": {"owner": "x"},
        "validity_frame": {
            **{k: {"a": 1} for k in
               ("estimand", "units", "measurement", "sampling_frame", "missingness")},
            "dependence": {"structure": "not_a_member"},
        },
    }
    report = validate_structure(spec)
    found = [f for f in report.findings if f.code == "DSX-SPEC-082"]
    self.assertEqual(len(found), 1)
    self.assertEqual(found[0].severity, Severity.HIGH)
    self.assertEqual(found[0].where, "spec.validity_frame.dependence.structure")
    self.assertIn("clustered", found[0].detail)
```

**Malformed-shape defensive-programming precedent** (V5 ASVS control, cite verbatim per
`07-RESEARCH.md`'s Security Domain section — `val.py` must not crash on a wrong-typed sub-block):

```python
def test_malformed_validity_frame_shapes_degrade_to_dsx_spec_080_not_a_crash(self):
    for bad in ("a string", [], {}, None):
        spec = {
            "spec_version": 1, "title": "t", "question_type": "causal", "decision": {"owner": "x"},
            "validity_frame": bad,
        }
        report = validate_structure(spec)  # must not raise
        self.assertIn("DSX-SPEC-080", codes(report))
```

The module-level helper every test in this style relies on (`tests/test_dsx.py:26-27`):
```python
def codes(report: Report) -> set[str]:
    return {f.code for f in report.findings}
```

New `val.py` unit tests should call `val.check(spec)` in place of `validate_structure(spec)`,
build the minimal `validity_frame.<sub_block>` dict literal needed to isolate one code, and assert
via `codes(report)` / `f.severity` / `f.where` / `f.detail`, exactly as above.

---

### `tests/test_dsx.py` — gate-level exit-code tests (test, integration/CLI)

**Analog:** `tests/test_dsx.py:1183-1244`, class `TestCLI`. The shared per-class helper
(`07-RESEARCH.md` §6 already names its existence; full body below):

```python
class TestCLI(unittest.TestCase):
    ROOT = Path(__file__).resolve().parent.parent

    def _run(self, argv: list[str]) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()
```

**Exit-code assertion shape**, three variants a `DSX-VAL-040` gate-blocking test should mirror —
positive (clears every gate), CRITICAL-blocks-at-plan, and template-must-still-fail-at-ship:

```python
def test_good_fixture_passes_every_gate(self):
    fixture = self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"
    for point in ("plan", "execute", "verify", "ship"):
        code, _, err = self._run(["gate", point, "--spec", str(fixture)])
        self.assertEqual(code, 0, f"gate {point} unexpectedly blocked:\n{err}")

def test_bad_fixture_blocks_at_plan(self):
    fixture = self.ROOT / "examples" / "bad-ANALYSIS-SPEC.yaml"
    code, _, err = self._run(["gate", "plan", "--spec", str(fixture)])
    self.assertEqual(code, 1)
    self.assertIn("DSX-", err)

def test_template_validates_structurally_as_a_scaffold(self):
    # The template ships with placeholders, so it must NOT pass — proving the
    # gate cannot be satisfied by shipping the unedited scaffold.
    template = self.ROOT / "templates" / "ANALYSIS-SPEC.yaml"
    code, _, _ = self._run(["gate", "ship", "--spec", str(template)])
    self.assertEqual(code, 1)
```

For `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml`, the new gate-level test must
assert exit code `1` at `plan` **and** `"DSX-VAL-040"` present in stderr — this is the fixture the
corpus-test conflict (07-RESEARCH.md, dedicated section) requires a resolution for; whichever
resolution is chosen, the assertion body follows `test_bad_fixture_blocks_at_plan`'s shape above.

---

### `tests/test_dsx.py` — `mathx.design_effect()` reference-value test (test, unit/numeric)

**Analog:** `tests/test_dsx.py:33-70`, class `TestMath` — plain `assertAlmostEqual` against a
published number, no special machinery:

```python
class TestMath(unittest.TestCase):
    def test_norm_ppf_reference_values(self):
        for p, expected in ((0.975, 1.959964), (0.95, 1.644854), (0.80, 0.841621),
                            (0.99, 2.326348), (0.5, 0.0)):
            self.assertAlmostEqual(mathx.norm_ppf(p), expected, places=5, msg=f"p={p}")

    def test_chi2_sf_reference_values(self):
        # Critical values at alpha=0.05
        self.assertAlmostEqual(mathx.chi2_sf(3.841459, 1), 0.05, places=5)
```

New test, same class, same shape (07-RESEARCH.md §7 already gives the exact call):
```python
def test_design_effect_matches_cochrane_worked_example(self):
    # D-05: DSX-VAL-020
    self.assertAlmostEqual(mathx.design_effect(29.8, 0.02), 1.576, places=3)
```

---

### `tests/test_frame_boundary.py` — REQ-P7-09 no-`inference.paradigm`-read test (test, invariant scan)

**Analog:** the whole file (126 lines), class `TestFrameImportBoundary`. Not a literal match for
REQ-P7-09 (this scanner only walks `import`/`from...import` AST nodes, not string-literal
arguments — 07-RESEARCH.md §6 already flags this precisely), but it is the **only** existing
precedent for "parse real `dsx/frame/*.py` source, plus a synthetic-violation control, and assert
zero violations." Quote of the scanner loop and its "real files + synthetic proof" structure to
mirror for a new, narrower scanner/substring check:

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

The project's own two-proofs rationale, stated in the module docstring (`tests/test_frame_boundary.py:11-15`),
applies directly to REQ-P7-09's new test:

> "Two proofs, not one: the real `dsx/frame/*.py` tree scans clean, AND the scanner is shown to
> actually fire against three deliberately violating source strings... A boundary test that only
> ever walks real files can never fail, which means it is not actually enforcing anything."

A REQ-P7-09 test should therefore assert (1) the real `dsx/frame/val.py` source contains no
`"inference.paradigm"` substring / no `get(spec, "inference.paradigm")`-shaped AST call, and (2) a
synthetic violating source string (e.g. `'get(spec, "inference.paradigm")\n'`) is correctly flagged
by whatever detector is written — either as a new method on `TestFrameImportBoundary` or a sibling
test class in the same file.

---

### `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` + `-POSTMORTEM.md` (fixture, file-I/O)

**Analog:** `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml` +
`examples/known-bad/interference-shared-budget-POSTMORTEM.md` — read in full; this is the fixture
D-14 already references by name for its own defect (`method_family_required` fix), and structurally
the closest of the three existing known-bad fixtures (also encodes exactly one validity-frame-shaped
defect against an otherwise-clean spec).

**Fixture header comment convention** (top of file, before `spec_version:`) — states what the
fixture *does* clear, what it *doesn't*, and points at the paired post-mortem:

```yaml
# A known-bad ANALYSIS-SPEC (REQ-P6-13, D-06). This file is structurally valid —
# it parses, and it accepts dsx validate and both CRITICAL-threshold gate points,
# dsx gate plan and dsx gate execute (both exit 0) — but it encodes a real,
# documented interference failure: a declared shared-budget interference risk with
# no mitigation and no residual note. ...
# ... none of which is the interference defect this fixture exists to encode; see
# tests/test_known_bad_corpus.py's _INCIDENTAL_GAP_CODES for the full measured
# list. ... See the paired POSTMORTEM.md.
#
#   dsx validate --spec examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
```
For the new fixture, this header must instead say the file is expected to **block** at `dsx gate
plan` with `DSX-VAL-040` (the opposite polarity from the three existing fixtures) — this is the
one place the analog's wording must NOT be copied verbatim; see the corpus-test-conflict section in
`07-RESEARCH.md`.

**Validity-frame boilerplate is a full-shape clone** — every sub-block from the good/existing
fixture's shape is present, only the identification block carries the encoded defect. Per
`07-CONTEXT.md` D-15/D-04, the new fixture's `validity_frame.identification` block should read:
```yaml
identification:
  strength: weak                 # weak — the encoded defect
  evidence: "<describe the MMM's identifying variation, or lack thereof>"
  constraint_source: none        # none — the encoded defect: weak strength, no constraint
  constraint_justification: ""
```
mirroring the shape (comments, inline vocabulary hints) of the analog's own `identification:` block
at lines 117-121, with every other `validity_frame.*` sub-block populated as non-defective
boilerplate (same field names, same `# vocab | hint` comment style as lines 112-166 of the analog).

**Post-mortem structure** (`interference-shared-budget-POSTMORTEM.md`, read in full — five
mandatory sections in this order):

```markdown
# Post-mortem: shared advertising budget interference

Paired spec: `interference-shared-budget-ANALYSIS-SPEC.yaml`

## What was concluded

[narrative: what the team believed, what action they took]

## Why it was wrong

[the mechanism, with the formal name of the failure — e.g. SUTVA violation — named explicitly]

## Source

Kohavi, R., Tang, D. & Xu, Y. (2020), *Trustworthy Online Controlled
Experiments: A Practical Guide to A/B Testing*, Cambridge University Press,
Chapter 22 (...) — the chapter documents ... and the book is named explicitly in the reference
list this project anchors D-05 citations to (brief.md section 7).

Imbens, G.W. & Rubin, D.B. (2015), ... — the formal [concept] statement this ... pattern violates.

Vendor blogs, Medium posts and tool marketing are inadmissible under D-05 in
either direction — neither cited source is one.

## Which absent code would have caught it

`DSX-INT-010` (Phase 8) — no code in this codebase adjudicates ... today ...
```

For the new fixture, "Which absent code would have caught it" inverts: `DSX-VAL-040` is **not**
absent — it ships this phase and blocks the fixture at `dsx gate plan` — so that final section
should instead read something like "Which code catches it" and name `DSX-VAL-040` at CRITICAL,
citing exactly how it fires (`strength: weak` + `constraint_source: none`). Per `07-CONTEXT.md`'s
Claude's Discretion, the specific published weak-identification MMM case cited in "Source" is not
yet chosen — vendor blogs/Medium posts remain inadmissible in either direction, per the analog's
own closing line.

---

### `dsx/spec.py` module constants (D-04 dependence map, D-05 falsifier lexicon)

**Analog for exclusion-from-`_VOCABULARIES` precedent:** `dsx/spec.py:53` `CAUSAL_VERBS`, together
with the `_VOCABULARIES` registry comment at `:267-271` that explicitly enumerates what is
deliberately left out:

```python
# Verbs that assert causation. Used to catch a causal claim mislabelled as
# association — the single most common analytical overreach.
CAUSAL_VERBS = (
    "causes", "caused", "causing", "drives", "drove", "driving", "leads to", "led to",
    "results in", "resulted in", "increases", "decreases", "improves", "improved",
    "reduces", "reduced", "boosts", "boosted", "lifts", "lifted", "impact of",
    "effect of", "because of", "due to", "thanks to", "responsible for",
    "attributable to", "uplift from", "generates", "generated",
)
```

```python
# Single registry behind describe_vocabulary() (D-05, REQ-P6-06): the object each shape
# validator imports is the exact object dumped here — one place to add a vocabulary, not two.
# Deliberately excludes SPEC_VERSION, CAUSAL_VERBS, REQUIRED_TOP_LEVEL and
# IMBALANCE_UNSAFE_METRICS — they are not vocabularies. chart_capabilities stays
# special-cased in describe_vocabulary() below, exactly as before.
_VOCABULARIES: "list[tuple[str, Any]]" = [
    ("question_types", QUESTION_TYPES),
    ...
    ("identification_strengths", IDENTIFICATION_STRENGTHS),
    ("constraint_sources", CONSTRAINT_SOURCES),
    ("dependence_structures", DEPENDENCE_STRUCTURES),
    ...
]
```

The new D-04 structure→method map and D-05 falsifier lexicon/refusal-word list/placeholder detector
must (a) sit as bare module-level constants beside `VARIANCE_ADJUSTMENTS` (`:96`) and the
`IDENTIFICATION_STRENGTHS`/`CONSTRAINT_SOURCES` block (`:162-184`) respectively, matching
`CAUSAL_VERBS`'s tuple-with-comment shape, and (b) get a one-line addition to the `_VOCABULARIES`
comment at `:269-271` naming them alongside `CAUSAL_VERBS` as deliberately excluded — they are
lookup tables and word-lists, not `dsx vocab`-dumpable enumerations.

---

### `brief.md` §7 (doc, reference list)

**Analog:** `brief.md:434-451`, itself, edited in place. Existing formatting convention — flowing
prose paragraph, one sentence per source, `*Title*` in italics, parenthetical noting which
finding-code family the source anchors:

```markdown
## 7. Reference sources

Anchor D-05 citations here rather than sprawling.

Kohavi, Tang and Xu, *Trustworthy Online Controlled Experiments* (triggering, dilution,
interference, novelty and primacy, SRM). Imbens and Rubin, *Causal Inference for Statistics,
Social, and Biomedical Sciences* (SUTVA, estimands). ... Gelman,
Simpson and Betancourt (2017), "The Prior Can Often Only Be Understood in the Context of the
Likelihood" (why prior strength is meaningless without identification, the source for
`DSX-VAL-040/041`). Deng, Lu and Chen (2016), "Continuous Monitoring of A/B Tests without
Pain" (error rates under optional stopping, the source for `DSX-PAR-011`).
```

Note `DSX-VAL-040/041`'s citation is **already present** in this list (Gelman, Simpson & Betancourt
2017) — D-17's edit adds the six missing sources (ICH E9(R1), Kish 1965, Cochrane Handbook, Hernán
& Robins 2016, Popper, Cronbach & Meehl) in the same flowing-paragraph style, each with a
parenthetical naming its `DSX-VAL-0NN` anchor exactly like the two examples above, and pins Lohr and
Little & Rubin's editions (currently unpinned in this list — "Lohr, *Sampling: Design and Analysis*"
has no edition; must become "Lohr (2021), *Sampling: Design and Analysis*, 3rd ed." per the D-05
ledger in `07-CONTEXT.md`).

---

### `.planning/research/FEATURES.md` (D-10 correction)

**Analog:** the file itself, `:44-57`, edited in place. Existing prose convention — bold lead-in
label, then the claim, with citation inline:

```markdown
**Worked published example:** ICC = 0.05, cluster size m = 50 → `DEFF = 1 + 49*0.05 = 3.45`
(commonly reproduced in cluster-RCT methods texts, e.g. Donner & Klar, *Design and Analysis of
Cluster Randomization Trials in Health Research*, 2000, and the Cochrane Handbook §16.3.4). At
that DEFF, the naive interval is `sqrt(3.45) ≈ 1.86x` too narrow. ...
```

D-10 requires this replaced with the actually-published Cochrane Handbook value (ICC 0.02, cluster
size 29.8 → `1.576`), in the same "bold lead-in, formula, citation" shape, with an explicit note
that `3.45` was an unsourced computed illustration — matching this document's own admission
elsewhere in `.planning/research/` that unsourced-but-plausible numbers are the exact failure mode
D-05 exists to catch (see `07-CONTEXT.md` `<specifics>`).

## Shared Patterns

### `Report`/`Finding` import boundary (D-03a)
**Source:** `dsx/frame/paradigm.py:18-20`
**Apply to:** `dsx/frame/val.py` only
```python
from ..decisions import DecisionRecord
from ..findings import Report
from ..spec import PARADIGMS, get, is_blank, normalize
```
`val.py` swaps in whatever `dsx.spec` names it needs (the new D-04/D-05 constants, `get`,
`is_blank`, `normalize`) but never imports from `dsx.checks` — enforced by
`tests/test_frame_boundary.py`.

### `report.add(...)` call shape and per-function D-05 docstrings
**Source:** `dsx/frame/paradigm.py:117-126`, mechanics in `scripts/gen-finding-catalogue.py:193-232`
**Apply to:** every helper function inside `val.py` that calls `report.add("DSX-VAL-0NN", ...)`
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
Because `gen-finding-catalogue.py` resolves a docstring to the *nearest enclosing function*, not
`check()`, each of `val.py`'s (near-certain) nine private helpers needs its own `Citation:` +
`Reference value:`/`Structural criterion:` docstring lines — see `07-RESEARCH.md` §3 for the exact
regexes and the D-05 citation ledger table for the text to drop in verbatim per code.

### Gate-level CLI test helper
**Source:** `tests/test_dsx.py:1186-1190` (`TestCLI._run`)
**Apply to:** all new exit-code / finding-code assertions against fixtures, including the new
`weak-identification-mmm` fixture and the four D-12/13/14-edited fixtures
```python
def _run(self, argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = cli.main(argv)
    return code, out.getvalue(), err.getvalue()
```

### `# D-05: DSX-XXX-NNN` marker convention
**Source:** `tests/test_dsx.py:391,415,460`, verified occurrences
**Apply to:** at least one test per `DSX-VAL-0NN` code, anywhere under `tests/` (flat text scan,
placement is flexible — standalone line above `def test_...` is the dominant existing style)
```python
def test_causal_spec_with_no_validity_frame_key_reports_one_critical_itemising_ten(self):
    # D-05: DSX-SPEC-080
    ...
```

## No Analog Found

None — every file this phase creates or modifies has at least a role-match analog in the existing
codebase; see table above.

## Metadata

**Analog search scope:** `dsx/frame/`, `dsx/spec.py`, `dsx/mathx.py`, `dsx/cli.py`,
`scripts/gen-finding-catalogue.py`, `tests/test_dsx.py`, `tests/test_frame_boundary.py`,
`tests/test_known_bad_corpus.py`, `examples/`, `templates/`, `brief.md`,
`.planning/research/FEATURES.md`.
**Files scanned:** ~20 (read in full or targeted-range), reusing `07-RESEARCH.md`'s already-verified
line numbers where noted rather than re-reading them.
**Pattern extraction date:** 2026-08-12
