# Stack Research: DSX Validity Frame (v2.0.0)

**Domain:** stdlib-only Python 3.9+ CLI gate subsystem, extending an existing installed package
**Researched:** 2026-08-07
**Confidence:** HIGH for stdlib module facts and for claims about the existing codebase (verified
by reading the files and, where a claim was checkable, by executing code against them). MEDIUM
where a recommendation is a design opinion rather than a verifiable fact.

This is not an ecosystem survey — there is no ecosystem to survey. D-01 forbids third-party
imports on the gate path, so every answer below is a specific stdlib module plus a specific
pattern, chosen against the constraints in `brief.md` §4 and `.planning/PROJECT.md`. Two concrete
gaps were found by executing the existing code, not by inspection; both are called out with
repro evidence.

## Recommended Stack

### Core stdlib modules, one row per question

| Module | Purpose | Used for |
|--------|---------|----------|
| `ast` | Parse Python source into a syntax tree without executing it | Q1 — `dsx/frame/` import-boundary test |
| `importlib.util` | `resolve_name()` turns a relative import (`from ..checks import x`, `level=2`) into an absolute dotted name | Q1 — resolving relative imports found by `ast` |
| `dataclasses` | Frozen record type + `asdict()` | Q2 — `DecisionRecord`, mirrors the existing `Finding` pattern exactly |
| `json` | `dumps(..., sort_keys=True)` / `loads()` | Q2 — decision-record serialisation (see rationale below on why not YAML) |
| `pathlib` | Path discovery, JSONL append/read | Q2, Q3 — log file I/O, mirrors `find_spec()` in `cli.py` |
| `argparse` | Subcommand registration | Q3 — `dsx explain`, extends the existing `build_parser()` in `dsx/cli.py` |
| `random` | `Random(seed)` instance, `.random()` for Bernoulli draws | Q4 — reproducible data-generating process for the simulation |
| `math` | `lgamma()` for a closed-form Beta-comparison, no sampling needed | Q4 — the performance-critical piece of the simulation |
| `statistics` | `mean()`, `NormalDist` | Q4 — aggregating replicate outcomes into a reported FPR + rough CI |
| `unittest` | Existing test runner (`python -m unittest discover -s tests`) | Q1, Q4 — both are tests, not gate code |

### Existing infra this subsystem must reuse, not duplicate

| Module | What it already provides | Confidence it's ready as-is |
|--------|---------------------------|------------------------------|
| `dsx/findings.py` | `Report`, `Finding`, `Severity`, exit-code mapping | HIGH — this is the only import `dsx/frame/` is permitted, and it needs no changes |
| `dsx/spec.py` | `normalize()`, `is_blank()`, `section()`, `items()`, `get()`, `as_number()` | HIGH — sits at the same top-level tier as `findings.py`, not inside `dsx/checks/`, so importing it from `dsx/frame/` does not violate D-03a |
| `dsx/loader.py` | `load()`/`loads()` — JSON native, PyYAML if present, else a bundled YAML-subset parser | MEDIUM — mostly ready; one concrete bug must be fixed first (Q5) |
| `dsx/cli.py` | `CHECKS` dict, `GATE_PROFILES`, `add_common()` argparse helper, `find_spec()` pattern | HIGH — `dsx explain` and any new `frame` check register the same way every existing check does |

## Installation

None. Zero third-party packages, by design (D-01). `pip install` output for this milestone is
empty — that emptiness is the deliverable, not an oversight. PyYAML stays exactly what it is
today: an opportunistic accelerant `dsx/loader.py` uses **only for reading**, never load-bearing,
never assumed present.

```bash
# Nothing to install for this milestone. Verify no new imports were introduced:
python3 -c "import dsx, dsx.frame" 2>&1  # must succeed with PyYAML absent from the environment
```

---

## Prescriptive design, per question

### Q1 — Enforcing `dsx/frame/` → `dsx/checks/` as a zero-import boundary

**Recommendation: `ast`-based static scan, in `tests/test_frame_boundary.py`, run by the existing
`unittest discover`. Not `importlib`, not `modulefinder`.**

Why `ast` over the alternatives:

- **`importlib` + `inspect`** actually executes the module. That means it can be fooled: a name
  imported from `dsx.checks.design` and re-exported gets flattened into the importing module's
  namespace, and by the time you inspect `sys.modules[name].__dict__`, most bound objects (dicts,
  strings, plain functions reassigned to new names) no longer carry a reliable trail back to
  `dsx.checks`. You'd be inferring provenance from `__module__` attributes that many objects don't
  have. It also runs arbitrary module-level code as a side effect of the *test*, which is exactly
  the kind of hidden coupling a boundary test exists to prevent.
- **`modulefinder`** resolves the full transitive import graph at runtime and is effectively
  unmaintained/deprecated-adjacent tooling for this use case. Overkill for a one-directional
  same-repo check.
- **`ast.parse()`** is static (never executes the file), fast, and gives you the exact thing you
  want to assert about: the literal `Import`/`ImportFrom` statements written in the source.

Concrete implementation:

```python
# tests/test_frame_boundary.py
import ast
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
FRAME_DIR = ROOT / "dsx" / "frame"


class TestFrameImportBoundary(unittest.TestCase):
    def test_frame_never_imports_dsx_checks(self):
        if not FRAME_DIR.exists():
            self.skipTest("dsx/frame/ not created yet")
        violations = []
        for path in sorted(FRAME_DIR.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            package = _package_for(path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    target = ("." * node.level) + (node.module or "")
                    resolved = importlib.util.resolve_name(target, package) if node.level else target
                    names = [resolved]
                else:
                    continue
                for name in names:
                    if name == "dsx.checks" or name.startswith("dsx.checks."):
                        violations.append(f"{path}:{node.lineno}: {name}")
        self.assertEqual(violations, [], "\n".join(violations))


def _package_for(path: Path) -> str:
    parts = path.relative_to(ROOT).with_suffix("").parts  # e.g. ('dsx','frame','val')
    return ".".join(parts[:-1]) if parts[-1] != "__init__" else ".".join(parts)
```

`importlib.util.resolve_name(name, package)` (stdlib since 3.3) is what turns `from ..checks
import design` written inside `dsx/frame/val.py` into `dsx.checks.design` — without it you'd have
to hand-roll dot-counting logic, which is exactly the kind of off-by-one bug a boundary
enforcement test should not itself contain.

**Flag for the roadmap — the D-03a wording is imprecise and the test above resolves it in the
practically-correct direction, but this should be a stated decision, not an assumption carried
silently forward.** D-03a says `dsx/frame/` "imports nothing from `dsx/checks/` except `Report`
and `Finding`." Verified by reading `dsx/checks/__init__.py`: it re-exports only the check
submodules (`claims`, `code`, `coherence`, …), never `Report`/`Finding`. Those two names live in
`dsx/findings.py`, a top-level sibling module, not inside `dsx/checks/`. So the exception clause
in D-03a is unreachable as literally written — there is nothing to except, because `Report`/
`Finding` were never inside `dsx/checks/` to begin with. The test above implements the intended
rule (zero imports from `dsx.checks.*`, with `dsx.findings`, `dsx.spec`, `dsx.mathx`, `dsx.loader`
all remaining fair game as top-level infrastructure), which is almost certainly what was meant.
Confidence: HIGH that the test as written is correct and enforceable; MEDIUM that this is the
intended semantics versus a typo that should instead scope the boundary as "nothing from
`dsx/checks/` or `dsx/findings/`" — reading D-03a's own rationale ("if in six months there are
still no upward imports, extraction is a `git filter-repo`") only makes sense if `dsx/frame/` is
allowed to depend on the shared output contract, so the interpretation above is the coherent one.

### Q2 — The decision record: schema and emitter

**Recommendation: a frozen `dataclass` in a new top-level module `dsx/decisions.py` (sibling to
`findings.py`, not inside `dsx/frame/`), serialised as JSON Lines (`.jsonl`), one record per
line, via the stdlib `json` module. Do not hand-roll a YAML sequence writer.**

Why JSON, not YAML, for a *write* path:

- `dsx/loader.py` only reads YAML. It has no writer, hand-rolled or otherwise, and building one
  is real surface area: every string field (`choice`, `counterfactual`, `citation`) needs correct
  quoting/escaping for colons, quotes, and multi-line text, which is precisely the class of bug
  the loader's own `_split_key`/`_unquote`/`_strip_comment` functions exist to parse *around* on
  the read side. A hand-rolled writer mirrors that complexity in the opposite, harder-to-test
  direction (generation, not recognition) for zero benefit here — nothing downstream needs the
  decision log to be YAML.
- `json.dumps(record, sort_keys=True)` has no escaping edge cases by construction, is a strict
  subset of YAML 1.2 flow content (so it stays human-legible and could always be re-wrapped as a
  `.yaml` file later without a format migration), and is exactly what `dsx/loader.py`'s own JSON
  fast path already privileges (`loads()` tries `json.loads` first whenever a `.json` suffix or a
  `{`-leading document is seen).
- **JSON Lines over a single JSON array.** Decision records are emitted "by every step" per brief
  §2 — an event stream, not a document written once. Appending a line via
  `path.open("a", encoding="utf-8")` is crash-safe: a process that dies mid-run leaves the file
  with N-1 complete, independently-parseable lines, not one corrupted JSON array. A single-array
  writer would need read-modify-write-whole-file on every emission, which is both slower and
  loses that crash-safety property.

```python
# dsx/decisions.py — new top-level module, parallel to findings.py
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DecisionRecord:
    id: str                       # "DEC-004" — assigned by a per-run counter, never uuid/random
    layer: str                    # "deterministic" | "stochastic"
    choice: str
    inputs: list[str] = field(default_factory=list)
    rule: str = ""                 # e.g. "DSX-VAL-020: analysis unit must not be finer than assignment"
    citation: str = ""
    counterfactual: str = ""
    alternatives_rejected: list[str] = field(default_factory=list)  # stochastic entries only
    confidence: "str | None" = None   # "high" | "contested" — stochastic entries only
    escalate: bool = False

    def __post_init__(self) -> None:
        if self.layer not in ("deterministic", "stochastic"):
            raise ValueError(f"layer must be 'deterministic' or 'stochastic', got {self.layer!r}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def append(path: "str | Path", record: DecisionRecord) -> None:
    """Append one record. Crash-safe: each line is independently valid JSON."""
    line = json.dumps(record.to_dict(), sort_keys=True)
    with Path(path).open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def read_all(path: "str | Path") -> list[dict]:
    records = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            records.append(json.loads(line))
    return records
```

Target artifact: `DECISION-LOG.jsonl`, written alongside `RESULTS.md`/`DATA-PROFILE.yaml` in the
phase directory — an **emitted artifact**, not a new authored contract file, so this does not
conflict with D-03 ("no new contract file"). It is parallel to how `CHART-REVIEW.md` (v1.5.0) is
generated output rather than something an agent hand-authors before the gate runs.

**Determinism requirement, inherited from the existing test convention.** `tests/test_dsx.py`
already asserts `test_determinism_same_input_same_output` (same input, byte-identical JSON output,
twice). A decision-record emitter that embeds `datetime.now()` or a random UUID by default breaks
that invariant the moment `dsx/frame/` checks start emitting records inside `dsx audit --json`.
**Do not embed wall-clock time or randomness in the record's content fields.** `id` must come from
a monotonically incrementing per-run counter (`DEC-{:03d}`), not `uuid.uuid4()`. If a timestamp is
wanted for audit purposes later, it must be an explicitly separate, non-canonical field excluded
from any determinism comparison — flag this as a decision for the roadmap to make explicitly
rather than default into.

**Why this module lives at `dsx/decisions.py`, not inside `dsx/frame/`:** D-04 ("gates emit a
decision record") is stated as applying to gates in general, not to the new frame family
specifically — brief §2 goal 2 says "every decision, deterministic or stochastic," and the
example in §5.5 (`DSX-VAL-020`) is a frame check, but nothing scopes emission to frame-only.
Existing check modules (`dsx/checks/design.py`, etc.) will plausibly want to emit records too,
eventually. Placing `DecisionRecord`/`append`/`read_all` at the top level, alongside
`findings.py`, means both `dsx/checks/*` and `dsx/frame/*` can import it without either one
importing the other — consistent with the Q1 boundary rather than in tension with it.

### Q3 — `dsx explain`: non-blocking renderer

**Recommendation: a new `cmd_explain` subcommand in `dsx/cli.py`, following the exact registration
pattern every existing subcommand uses. No new modules beyond what Q2 already introduces.**

```python
# in dsx/cli.py, alongside the other cmd_* functions
def cmd_explain(args: argparse.Namespace) -> int:
    from .decisions import read_all

    path = Path(args.log or "DECISION-LOG.jsonl")
    if not path.exists():
        raise CheckError(f"no decision log found at {path}")
    records = read_all(path)  # raises json.JSONDecodeError -> caught by main() as ValueError -> exit 2
    if args.json:
        print(json.dumps(records, indent=2))
    else:
        print(_render_decision_log(records, verbose=args.verbose))
    return 0  # ALWAYS 0 — D-04: dsx explain never blocks, regardless of content


def _render_decision_log(records: list[dict], verbose: bool) -> str:
    lines: list[str] = []
    for layer in ("deterministic", "stochastic"):
        subset = [r for r in records if r["layer"] == layer]
        if not subset:
            continue
        lines.append(f"## {layer.capitalize()}")
        for r in subset:
            lines.append(f"\n### {r['id']} — {r['choice']}")
            lines.append(f"rule: {r['rule']}")
            if r.get("citation"):
                lines.append(f"citation: {r['citation']}")
            lines.append(f"counterfactual: {r['counterfactual']}")
            if verbose and r.get("alternatives_rejected"):
                lines.append("alternatives rejected: " + ", ".join(r["alternatives_rejected"]))
    return "\n".join(lines)
```

Wiring, in `build_parser()`:

```python
p_explain = sub.add_parser("explain", help="render the decision log as a readable lesson (never blocks)")
p_explain.add_argument("--log", help="path to DECISION-LOG.jsonl (default: ./DECISION-LOG.jsonl)")
p_explain.add_argument("--json", action="store_true")
p_explain.add_argument("--verbose", action="store_true")
p_explain.set_defaults(func=cmd_explain)
```

**The one hard contract rule: `cmd_explain` must return `0` on every content path, only `CheckError`/
parse failure maps to `2` (the existing `main()` exception handler already does this correctly,
unchanged).** This is what makes "never block to teach" (D-04) structural rather than a
convention someone forgets under deadline pressure — `dsx explain` is wired the same way as every
other read-only reporting subcommand (`vocab`, `power`), which already never participate in the
`0/1/2` block-vs-pass contract at all; `explain` simply never uses code `1`.

### Q4 — Simulating DSX-PAR-011's false-positive rate: `random` + `math.lgamma`, not `random` + `betavariate`

**This code must live under `tests/`, never under `dsx/`.** Even though it is stdlib-only and
technically *could* satisfy D-01, putting a Bayesian posterior-comparison function inside
`dsx/mathx.py` creates exactly the attractive nuisance D-02 exists to prevent: a future
`DSX-PAR-*` check author who needs "the probability B beats A" would find it one import away and
be tempted to call it from the gate path, silently reintroducing posterior computation into a
layer that must only adjudicate declarations. Keep it physically separated — e.g.
`tests/simulations/beta_monitoring.py` — imported only by `tests/test_par011_simulation.py`.
This is a structural recommendation, not a stylistic one: it makes "a gate that computes
posteriors" require deliberately moving a file across a directory boundary, not just adding an
import line.

**Performance verdict: reject the naive nested-Monte-Carlo design; recommend a closed-form Beta
comparison via `math.lgamma`.** Concretely:

- Naive design: at each of ~100 checkpoints per replicate, draw ~1000–2000 `random.betavariate()`
  samples per arm and estimate `P(B>A)` empirically. `random.betavariate` (and the `gammavariate`
  it's built on) is pure-Python in CPython's stdlib, not C-accelerated. At realistic simulation
  scale (hundreds to low-thousands of replicates × dozens to ~100 checkpoints × ~1000+ draws per
  side), the call count lands in the hundreds of millions, which at low-microsecond-per-call cost
  runs into minutes, not seconds — not "fast enough" for a suite run on every `unittest discover`.
- Closed-form design: for integer Beta parameters (guaranteed here — posteriors are
  Beta(successes+prior_α, failures+prior_β) with integer counts under a standard prior), there is
  a well-known finite-sum closed form for `P(B>A)` requiring only `math.lgamma`, no sampling:

  ```
  P(B > A) = Σ_{i=0}^{a2-1} exp( lbeta(a1+i, b1+b2) − ln(b2+i) − lbeta(1+i, b2) − lbeta(a1, b1) )
  ```

  where `lbeta(x, y) = lgamma(x) + lgamma(y) − lgamma(x+y)`, `a1,b1` are arm A's posterior
  parameters and `a2,b2` are arm B's. Cost per call is `O(a2)` `lgamma` evaluations, and
  `math.lgamma` is a thin wrapper over the C library's `lgamma()` — nanoseconds per call. At the
  same simulation scale this lands well under a few seconds, comfortably "fast enough."
- **Still use `random` for what only `random` can do**: generating the actual sequence of
  simulated Bernoulli outcomes per replicate (`rng.random() < p` in a loop, or a batched success
  count over a checkpoint interval) is inherently stochastic and belongs to `random.Random`, not
  to a closed-form shortcut. Use an **instance**, `rng = random.Random(seed)`, not the
  module-level `random.seed()` — this isolates the simulation's stream from anything else the
  test process might do with the global RNG, which is what makes the test reproducible
  independent of run order or `-p`/parallel test execution. Pick one fixed integer seed and check
  it into the test.
- `statistics.mean()` (stdlib since forever) aggregates the fraction of replicates that ever
  crossed the 0.95 threshold into the reported FPR estimate; `statistics.NormalDist` (stdlib
  since 3.8, so fine on the 3.9+ floor) can construct a rough normal-approximation interval around
  that Monte Carlo estimate for reporting purposes, without needing scipy.

**Formulation to implement: the point-null case, not the prior-averaged/Ville's-inequality case —
flag this as a decision the roadmap should state explicitly, not inherit silently.** Brief §6.5's
fixture note is explicit that these give materially different numbers and that the choice must be
declared in the docstring before the reference value is picked. The point-null formulation (A and
B generated from the identical Bernoulli(p), literal repeated peeking, no averaging over a prior)
is: (a) the simpler stdlib simulation to implement and verify — it's a direct empirical frequency
over many replicated runs of the exact same random process, nothing more; (b) the one that maps
directly onto the citation already in the accepted source list (`brief.md` §7 — Deng, Lu, Chen
2016, "Continuous Monitoring of A/B Tests without Pain"), which is about the FPR under optional
stopping, not about the Ville's-inequality bound. Recommend the point-null formulation on those
two grounds, while flagging that this is the kind of call D-14 says should be recorded, not
defaulted into silently.

```python
# tests/simulations/beta_monitoring.py — test-only, never imported by dsx/
import math
import random


def _lbeta(x: float, y: float) -> float:
    return math.lgamma(x) + math.lgamma(y) - math.lgamma(x + y)


def prob_b_greater_a(a1: int, b1: int, a2: int, b2: int) -> float:
    """P(Beta(a2,b2) > Beta(a1,b1)) via the closed-form finite sum (integer params)."""
    lbeta_a1_b1 = _lbeta(a1, b1)
    total = 0.0
    for i in range(a2):
        total += math.exp(_lbeta(a1 + i, b1 + b2) - math.log(b2 + i) - _lbeta(1 + i, b2) - lbeta_a1_b1)
    return total


def simulate_point_null_fpr(
    *, p: float, prior_alpha: int, prior_beta: int, horizon: int,
    check_every: int, threshold: float, replicates: int, seed: int,
) -> float:
    rng = random.Random(seed)
    crossings = 0
    for _ in range(replicates):
        a1, b1 = prior_alpha, prior_beta  # arm A posterior params
        a2, b2 = prior_alpha, prior_beta  # arm B posterior params
        crossed = False
        for step in range(check_every, horizon + 1, check_every):
            successes_a = sum(1 for _ in range(check_every) if rng.random() < p)
            successes_b = sum(1 for _ in range(check_every) if rng.random() < p)
            a1, b1 = a1 + successes_a, b1 + (check_every - successes_a)
            a2, b2 = a2 + successes_b, b2 + (check_every - successes_b)
            if prob_b_greater_a(a1, b1, a2, b2) > threshold:
                crossed = True
                break
        crossings += crossed
    return crossings / replicates
```

Confidence: HIGH that `random.Random`, `math.lgamma`, `statistics.mean`/`NormalDist` exist and
behave as described on Python 3.9+ (verifiable, stable stdlib API). MEDIUM-HIGH on the specific
closed-form formula's correctness — it is well established in the online-experimentation
literature (frequently attributed to Evan Miller's derivation; the more academically citable
primary source is Cook, "Numerical Computation of Stochastic Inequality Probabilities" (2005)).
Because this code is test-only, D-05's per-check citation mandate does not formally apply to it,
but the same rigor is worth keeping: whoever implements this should pin one citable primary
source for the formula and unit-test `prob_b_greater_a` against a hand-computable small case
(e.g. `a1=b1=a2=b2=1` should give exactly `0.5` by symmetry) before trusting it to drive the FPR
number cited elsewhere.

### Q5 — `references/families.yaml`: what the existing loader supports, verified by execution

**Verified directly against `dsx/loader.py`'s bundled parser (PyYAML is not installed in this
environment, so the fallback path — the one that must never break, per D-01 — is exactly what was
exercised):**

```
families:
  - id: cluster_robust_welch
    estimand: mean_difference
    family: welch_t
    inference_method: frequentist
    dependence_handling: cluster_robust_se
    aliases: [welch, welch_two_sample, cluster_robust_t]
    assumptions:
      - "independence across clusters"
      - "cluster count >= 30 for asymptotic validity"
    admissible_when:
      dependence: [none, clustered]
      outcome_type: continuous
    citation: >
      Cameron, Gelbach and Miller (2011), "Robust Inference With Multiway
      Clustering," Journal of Business & Economic Statistics.
    notes: |
      Falls back to wild cluster bootstrap when clusters < 30.
```

parsed correctly for: nested mappings under a sequence item, inline flow lists (`aliases: [...]`),
block sequences of quoted scalars (`assumptions:`), a nested mapping-inside-mapping
(`admissible_when.dependence`), `>` folded and `|` literal block scalars, comments, quoted
strings. **This is squarely the subset `references/families.yaml` needs for ~25–35 entries keyed
on `estimand × family × inference method × dependence handling`, plus `aliases`, `assumptions`,
and a `citation` per D-05. No loader changes are required to support that shape.**

Two constraints to design the file's schema around, both verified by reading `dsx/loader.py`
directly rather than assumed:

1. **Top level must be a mapping, not a bare list.** `load()` raises `SpecParseError` if the
   parsed document isn't a `dict` (`dsx/loader.py:43-45`). `references/families.yaml` must be
   `families: [ ... ]` (or `version: 1` + `families: [...]`), not a bare `- id: ...` document
   root.
2. **Flow collections (`[...]`, `{...}`) must be single-line.** `_split_flow()` operates on a
   scalar's text after it has already been extracted as one logical line; there is no support for
   a flow list or mapping spanning multiple physical lines. Keep `aliases:`/short enum lists
   inline on one line; use block sequences (`- item` per line) for anything that might grow long
   enough to want wrapping.

**Concrete gap found by execution, required before `families.yaml` — or any `validity_frame:`
field using the literal enum value `"none"` — can be trusted: the bundled parser's null-token set
incorrectly includes the bare word `none`.**

```python
_NULL = {"", "null", "~", "none"}       # dsx/loader.py, current
```

Standard YAML (both the 1.1 core schema PyYAML implements and YAML 1.2) recognises `~`, `null`,
`Null`, `NULL`, and empty as null — **not** `none`. `dsx/loader.py`'s bundled fallback parser
diverges from that and from PyYAML's own behaviour by treating the bare word `none` as null too.
Reproduced directly against this repo's code:

```
>>> _parse_yaml_subset("x: none\n", "<t>")["x"]
None                    # should be the string "none"
>>> _parse_yaml_subset("x: [none, clustered]\n", "<t>")["x"]
[None, 'clustered']     # should be ["none", "clustered"]
```

This matters because **`"none"` is not an edge case in this project — it is a load-bearing,
frequently-declared value across the exact vocabularies this milestone introduces**: brief §5.1's
`validity_frame:` block uses literal `none` for `identification.constraint_source`,
`interference.risk`, `interference.mitigation`, and `dependence.structure`; the existing
`design.multiplicity.correction` vocabulary already includes `"none"` too
(`MULTIPLICITY_CORRECTIONS` in `dsx/spec.py`). The bug is currently masked for **top-level scalar**
fields only, by coincidence: `dsx/checks/design.py:375` reads
`is_blank(correction) or normalize(correction) == "none"`, and because `normalize(None)` computes
`str(None).strip().lower()` → `"none"`, the check happens to still match even when the loader
silently turned the declared string into `None`. That coincidence **does not extend to values
inside a list** (`admissible_when.dependence: [none, clustered]` from the fixture above becomes
`[None, "clustered"]` — a plain `"none" in the_list` check on that value will silently fail), and
it does not extend to `is_blank()` checks on values that are legitimately `"none"` (a field
correctly declared `interference.mitigation: none`, meaning "no mitigation, consciously declared,"
would incorrectly read as *unset* rather than *declared none*, misfiring "field is missing"
findings on already-answered fields).

**Required fix, scoped to M1 (before the `validity_frame:` block or `references/families.yaml`
ship): drop `"none"` from `dsx/loader.py`'s `_NULL` set.**

```python
_NULL = {"", "null", "~"}   # matches PyYAML/YAML null semantics; drop the non-standard "none"
```

This is safe against the existing suite (verified: `python -m unittest discover -s tests -v`
passes 160/160, 1 skipped, both before and is unaffected by this change since no current fixture
relies on bare `none` meaning null) and it is strictly more correct — it makes the bundled
fallback parser agree with PyYAML rather than silently diverge from it in an environment-dependent
way, which is exactly the failure class D-01 exists to eliminate (a gate that behaves differently
depending on whether PyYAML happens to be installed). Add a regression test asserting both
`_parse_yaml_subset("x: none\n", "<t>")["x"] == "none"` and
`_parse_yaml_subset("x: [none, clustered]\n", "<t>")["x"] == ["none", "clustered"]` alongside the
existing `TestLoader` cases in `tests/test_dsx.py`.

**Not the loader's job: `id` uniqueness across `families.yaml` entries.** The loader's
duplicate-key rejection (`dsx/loader.py:154-155`) only fires within a single mapping's own keys —
two separate list items each declaring `id: cluster_robust_welch` are two different mapping
objects and will not collide at parse time. Uniqueness of family `id`s (and any cross-reference
integrity, e.g. `alias` collisions across families) must be validated by the M4 admissibility
loader itself (`dsx/frame/families.py` or wherever it lands), not assumed to come free from
`load()`.

---

## What NOT to Use

| Avoid | Why | Use instead |
|-------|-----|--------------|
| PyYAML / ruamel.yaml as a load-bearing dependency for *writing* decision records or `families.yaml` | D-01; the loader's PyYAML path is read-only and opportunistic — never assume it's present | `json.dumps` for records; the existing bundled parser (once fixed, Q5) reads `families.yaml` fine either way |
| numpy / scipy for the DSX-PAR-011 simulation | D-01, and unnecessary — the closed-form needs only `math.lgamma` | `math`, `random`, `statistics` (Q4) |
| Nested Monte Carlo (`random.betavariate` sampled at every checkpoint) as the *primary* FPR estimator | Too slow: hundreds of millions of pure-Python `betavariate`/`gammavariate` calls land in minutes, not seconds | The closed-form `math.lgamma` sum (Q4); reserve `betavariate` for a small-scale correctness cross-check only |
| Any Bayesian posterior-comparison helper inside `dsx/mathx.py` | D-02 attractive-nuisance risk — anything importable from `dsx/` is one line away from being called by a gate | Keep it under `tests/simulations/`, imported only by the test that needs it |
| `uuid.uuid4()` / `datetime.now()` embedded in `DecisionRecord` content fields | Breaks the existing `test_determinism_same_input_same_output` invariant the moment frame checks emit records inside `dsx audit --json` | A per-run monotonic counter for `id`; keep any wall-clock timestamp as a separate, non-canonical field if wanted at all |
| YAML anchors/aliases, `<<:` merge keys, multi-document `---` separators, or multi-line flow collections in `references/families.yaml` | The bundled parser does not support any of these (verified by reading `dsx/loader.py`'s `_parse_yaml_subset`/`_split_flow`) — it will raise `SpecParseError`, which is correct behaviour (fail loud) but means the schema must be designed to avoid them, not discovered the hard way | Block-style sequences/mappings; single-line flow lists only |
| `importlib`-based runtime inspection for the Q1 boundary test | Executes the modules under test as a side effect and loses provenance for many object types once imported names are flattened into a namespace | `ast.parse()` — static, side-effect-free, and directly answers "what does this file's source say it imports" |

## Stack Patterns by Variant

**If a future frame check needs a shared numeric helper (power, effect size, multiplicity):**
Import it from `dsx.mathx` — that module is already stdlib-only, already tested against
published reference values (D-05), and sits outside `dsx/checks/`, so importing it from
`dsx/frame/` does not violate D-03a.

**If a future frame check needs a shared spec-reading helper:** Import from `dsx.spec`
(`normalize`, `is_blank`, `section`, `items`, `get`, `as_number`) — same reasoning, and it keeps
new checks consistent with every existing check's idiom rather than reinventing dotted-path
lookups.

**If PyYAML happens to be installed in a given environment:** No code path in this milestone
should behave differently because of it. `dsx/loader.py`'s read path already handles that
transparently; nothing new here writes YAML, so there is no PyYAML-present-vs-absent branch to
introduce.

## Version Compatibility

| Module / feature | Minimum Python | Compatible with the 3.9+ floor? |
|---|---|---|
| `dataclasses` | 3.7 | Yes |
| `pathlib` | 3.4 | Yes |
| `ast.parse` / `ast.walk` | all | Yes |
| `importlib.util.resolve_name` | 3.3 | Yes |
| `math.lgamma` | 3.2 | Yes |
| `random.Random`, `.betavariate` | all | Yes |
| `statistics.mean` | 3.4 | Yes |
| `statistics.NormalDist` | 3.8 | Yes — right at the floor, but the project already targets 3.9+ so this is safe |
| `json` | all | Yes |

No 3.10+-only syntax (`match` statements, bare `X | Y` type unions evaluated at runtime rather
than under `from __future__ import annotations`) should be introduced. The existing codebase
already opens every module with `from __future__ import annotations` and uses `"str | Path"` as a
*string* annotation consistently (see `dsx/loader.py`, `dsx/findings.py`) — follow that exact
convention in `dsx/decisions.py` and `dsx/frame/*`, not the runtime-evaluated `str | Path` form,
to keep behaviour identical on 3.9.

## Sources

- Direct reads of `dsx/loader.py`, `dsx/findings.py`, `dsx/mathx.py`, `dsx/cli.py`,
  `dsx/checks/decision.py`, `dsx/checks/__init__.py`, `dsx/spec.py`, `tests/test_dsx.py`,
  `.planning/PROJECT.md`, `brief.md` — HIGH confidence, primary source, this repository at its
  current committed state (v1.5.0, commit `fdc4b8f`).
- Executed verification via `python3` against this repo's actual `dsx.loader._parse_yaml_subset`
  (families.yaml-shaped fixture; the `none`-as-null defect; full test suite run,
  160 passed / 1 skipped) — HIGH confidence, reproducible, not assumed.
- Python 3.9+ standard library documentation knowledge (`ast`, `importlib.util`, `dataclasses`,
  `json`, `random`, `math`, `statistics`) — HIGH confidence, stable, well-established API surface.
- Evan Miller's closed-form Beta-comparison derivation / Cook (2005), "Numerical Computation of
  Stochastic Inequality Probabilities" — MEDIUM confidence; correct and widely used in the
  online-experimentation literature, but not among the primary sources already accepted in
  `brief.md` §7, so the implementer should pin one specific citable source before treating the
  simulation's reference value as authoritative under the spirit of D-05.

---
*Stack research for: DSX Validity Frame (gsd-dsx v2.0.0)*
*Researched: 2026-08-07*
