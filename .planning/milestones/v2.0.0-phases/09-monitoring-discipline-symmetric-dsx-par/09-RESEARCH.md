# Phase 9: Monitoring discipline, symmetric (`DSX-PAR-*`) - Research

**Researched:** 2026-08-12
**Domain:** Statistical-validity gate checks inside a self-contained Python CLI tool (`dsx`) — no external services, no database, no network I/O. Domain content is the Deng/Lu/Chen (2016) Bayesian optional-stopping result and the Armitage/McPherson/Rowe (1969) repeated-significance-test result.
**Confidence:** HIGH — every code-location claim below was read from the file at the stated line range in this session; every citation was independently cross-checked via web search against the primary/bibliographic record.

<user_constraints>
## User Constraints (from CONTEXT.md)

09-CONTEXT.md is unusually complete for a phase-context document — it already resolved 15 phase-local decisions (D-01…D-15) with verified file:line citations, including the exact statistical corrections (D-10/D-11/D-12) and the citation-upgrade decision (D-13). This research **does not re-litigate any of it**; it re-verifies the load-bearing claims against the live tree and adds what a planner needs beyond what discuss already nailed down. Read `09-CONTEXT.md` in full before planning — it is the primary planning input, not this file.

### Locked Decisions (binding, do not re-litigate)

- **D-01**: All three codes ship inside `dsx/frame/paradigm.py`. No new module, no `GATE_PROFILES` edit.
- **D-02**: `DSX-PAR-010` and `DSX-PAR-011` both ship at `CRITICAL`. `DSX-PAR-002` ships at `HIGH`.
- **D-03**: `tests/test_known_bad_corpus.py` is restructured — the two monitoring fixtures move from "exits 0" to "exits 1 naming its code"; the allow-list guard at lines 231-245 must not be weakened.
- **D-04**: Both halves trigger on `design.peeking_policy == "uncontrolled_continuous"` alone. Neither reads `results.interim_looks`. No change to `dsx/checks/design.py`.
- **D-05**: Phase 9 coins three new `inference:` fields — `threshold_calibration`, `prior_justification`, `decision_threshold` — extending `_INFERENCE_FIELDS`, its drift-guard test, `templates/ANALYSIS-SPEC.yaml`, and `dsx vocab`.
- **D-06**: The paradigm-retype escape is closed structurally via exhaustive `PARADIGMS` coverage (dict keyed by every member + set-equality test), not hand-written `if` branches.
- **D-07**: The undeclared-paradigm escape is real and open today; must close via `DSX-PAR-002` requiredness. The plan-time severity consequence (HIGH doesn't block at `plan`) must be settled explicitly, not silently.
- **D-08**: `PARADIGM_JUSTIFICATIONS` already exists — Phase 9 coins no vocabulary. `DSX-PAR-002` owns requiredness/symmetry only; `DSX-SPEC-085` keeps membership. A `DSX-PAR-002` that re-checks membership would double-fire on `examples/bad-ANALYSIS-SPEC.yaml`.
- **D-09**: "No reason ranked above another" is enforced mechanically — one membership path, no per-member/per-paradigm branching, proven by a 7×2 parametrised test.
- **D-10**: Deng et al.'s Theorem 1 does **not** state `1/(K+1)` directly — that is unnumbered prose (§1, and the operational bound form at §3.2). REQUIREMENTS.md REQ-P9-02/03 and ROADMAP.md Phase 9 SC 2/SC 3 already carry the corrected wording (verified in this session — see below).
- **D-11**: `K` is the posterior odds; `1/(K+1) = 1-p` identically at `p=0.95, K=19`. The docstring must state this so the check does not read as circular, and must state the "known prior odds" condition Theorem 1 requires.
- **D-12**: Ville is never cited in Deng et al. Deng's proof is a likelihood-ratio identity/change-of-measure (an equality), not Ville's maximal inequality. Ville gives `1/k` (`≈0.0526` at k=19), a different, larger figure from a different conditioning event (Type-I error vs. FDR).
- **D-13**: `inflation_from_peeking()`'s docstring is upgraded to a full D-05 citation, elective (no `report.add` call site, so `check_d05()` never reaches it mechanically) but done anyway. No table/page of Armitage et al. (1969) may be cited (paywalled, unverified). Values are independently verified by computation (quadrature + Monte Carlo), not by citation.
- **D-14**: The REQ-P9-07 simulation is stdlib-only (`random.Random(seed)`), asserting a monotone-trend property under the point-null formulation and a fixed `1/(K+1)` ceiling under the prior-averaged formulation — two different assertions about two different formulations. Must run by default under `scripts/check.sh` discovery.
- **D-15**: The REQ-P9-06 symmetry audit ships as `references/paradigm-symmetry.md` (not `.planning/`, which is filtered from PR branches), written **before** the checks are built, with a positive-content test in the `tests/test_known_bad_corpus.py:270-326` idiom.

### Claude's Discretion (research/planner may settle)

- Plan slicing across the seven requirements, subject to atomicity: no plan lands `DSX-PAR-010` without `DSX-PAR-011` in the same commit range at the same severity.
- Exact member names/shapes of the three new `inference:` fields (subject to the collision check and operator-readability naming rule).
- Whether `threshold_calibration` is a scalar or a sub-dict (e.g. `{method:, fpr:}`), and whether `DSX-PAR-011` performs the `1/(K+1)` numeric comparison on the gate path or asserts presence-only and defers the number to the docstring/simulation. Both satisfy REQ-P9-02.
- Precise restructuring shape of `tests/test_known_bad_corpus.py` (D-03), provided the 231-245 guard is not weakened.
- Whether the three Deng/Ville regression guards need rewording given D-10 (read them first — see Verified below, they are already correct).

### Deferred Ideas (OUT OF SCOPE)

- Adjudicating whether a declared posterior probability was computed with honest prior odds — belongs in `remedy` text and human review, not code (the gate cannot check it).
- Bayesian procedure recommendation/admissibility (`DSX-ADM-*` second axis) — gated backlog.
- Prior justification *quality*, prior sensitivity, convergence declarations (`DSX-PAR-020/021/030`) — deferred under brief D-12a; their frequentist mirrors are not written, so shipping them now would itself be a D-12 asymmetry violation.
- Ratio-metric dilution — Phase 8's scope, unrelated to Phase 9.
- Retroactive D-05 sourcing for legacy finding codes generally (D-13 upgrades exactly one function because Phase 9 depends on it).
- Obtaining Armitage et al. (1969) / Jennison & Turnbull full text to replace the unverified-locator flag.

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-P9-01 | `DSX-PAR-010` blocks a frequentist design declaring continuous/group-sequential monitoring with no alpha-spending/sequential method, reusing `inflation_from_peeking()` | Verified: `dsx/mathx.py:411-432` exists, tested, reused (not duplicated) by `dsx/checks/design.py:452` for `DSX-EXP-060`. `DSX-PAR-010` must call the same function, never a second table. Trigger is `design.peeking_policy == "uncontrolled_continuous"` (D-04) — structurally disjoint from `DSX-EXP-060`'s `results.interim_looks`-gated trigger (`dsx/checks/design.py:444-449`). |
| REQ-P9-02 | `DSX-PAR-011` blocks a Bayesian design with neither `threshold_calibration` nor a justified informative prior, asserting `1/(K+1)`, `K=19` at `P(B>A)>0.95`, bound `0.05`, citing Deng, Lu & Chen (2016) Theorem 1, not Ville | Statistical grounding independently re-verified below (Sources). REQUIREMENTS.md's live text already carries the corrected attribution (D-10 resolved, confirmed by direct read in this session). |
| REQ-P9-03 | `DSX-PAR-011` docstring states it asserts the prior-averaged formulation, not point-null/LIL; fixture traces the theorem number | The known-bad Bayesian fixture and post-mortem already carry this distinction verbatim (`examples/known-bad/bayesian-continuous-monitoring-*`, verified below) — the docstring the planner writes must match that prose, not restate it differently. |
| REQ-P9-04 | `DSX-PAR-002` validates `paradigm_justification` requiredness/symmetry against the closed vocabulary, no reason ranked above another | `PARADIGM_JUSTIFICATIONS` (`dsx/spec.py:251-265`) and its 7-member vocabulary confirmed complete; `DSX-SPEC-085` (`dsx/spec.py:921-928`) already does membership. `DSX-PAR-002`'s job is the *absence* case (`is_blank` skip at `dsx/spec.py:918-919`), verified open today. |
| REQ-P9-05 | Neither code satisfiable by retyping `paradigm`; asserted both directions | `_PARADIGM_CONDITIONAL` (`dsx/frame/paradigm.py:38-41`) is the existing house pattern for a provably-exhaustive per-paradigm map — extend it, don't branch. |
| REQ-P9-06 | Documented audit of the cheapest dishonest escape per half; disjunctive `prior_justification` route no weaker than sequential-method requirement | `references/finding-codes.md` and `references/` layout confirmed as the committed, non-`.planning` location (D-15). No such audit file exists yet — this phase creates `references/paradigm-symmetry.md`. |
| REQ-P9-07 | `DSX-PAR-011` simulation lives under `tests/`, seeded, reproducible, never on gate path | Confirmed: no `pyproject.toml`/`requirements.txt`/`setup.py` anywhere in the repo (checked this session) — stdlib-only is a hard constraint, not a style preference. `scripts/check.sh:6-7` runs `python3 -m unittest discover -s tests -q` with default `test*.py` glob; a new file under `tests/` is picked up automatically, no discovery config needed. |

</phase_requirements>

## Summary

Phase 9 is almost entirely a **synthesis exercise**, not a discovery exercise: 09-CONTEXT.md's assumptions-mode discuss session already read the live tree and the arXiv LaTeX source directly, and every claim in it was re-verified byte-for-byte in this research pass — no discrepancy found anywhere (module layout, `_INFERENCE_FIELDS`, `PARADIGM_JUSTIFICATIONS`, `_check_peeking`'s early return, `inflation_from_peeking()`'s anchor table, the three known-bad-corpus regression guards, the `# D-05` catalogue-enforcement mechanics, and both target fixtures' current shape). REQUIREMENTS.md and ROADMAP.md already carry the D-10-corrected citation wording — the "correction" work described in D-10 is already committed, not still pending.

What remains for planning is code that does not exist yet: `dsx/frame/paradigm.py`'s `check()` function today emits only `DSX-PAR-001` (the informational manifest); Phase 9 must add three new checks to the *same* function/module (D-01), each following the `_check_*` decomposition pattern already used in `dsx/checks/design.py`. Three new `inference:` fields must be coined and threaded through `_INFERENCE_FIELDS`, its drift-guard test, the template, and `dsx vocab` (D-05) — brief.md §5.2's commented-out scaffold (lines 195-213, read directly this session) is the closest thing to a canonical shape for `threshold_calibration` (a sub-dict: `{method:, sims:, fpr:}`) and `decision_threshold` (a free-text expression like `"P(uplift > 0.01) > 0.95"`), though the planner has discretion on exact shape. `prior_justification` in the brief's original design mapped to the *deferred* `DSX-PAR-020` quality-judgement code — Phase 9 reuses the field name for a presence-only disjunctive satisfaction path on `DSX-PAR-011`, which is a different semantic use of the same name and worth flagging explicitly in the docstring so a reader doesn't conflate "prior_justification is set" (Phase 9's bar) with "the prior justification is any good" (Phase 11+'s deferred bar).

**Primary recommendation:** extend `dsx/frame/paradigm.py::check()` with three new `_check_*` helper functions (mirroring `dsx/checks/design.py`'s decomposition), each calling `report.add(...)` with the enclosing function's docstring carrying `Citation:`/`Reference value:` lines per the D-05 mechanics already proven working for `DSX-PAR-001`; extend `_PARADIGM_CONDITIONAL` and remove all three `_NOT_SHIPPED` entries in the same commit; write `references/paradigm-symmetry.md` **before** writing the checks (D-15); and settle the D-07 severity question (does the undeclared-paradigm escape close at `plan`, or only at `verify`/`ship`?) explicitly in the plan rather than let it fall out of D-02 by default.

## Architectural Responsibility Map

`dsx` is a single-process CLI static-analysis tool with no browser/server/DB tiers in the conventional sense. The relevant tiers are internal module boundaries, already enforced by an AST-based import-boundary test.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Frequentist monitoring-discipline check (`DSX-PAR-010`) | `dsx/frame/` (frame layer) | `dsx/mathx.py` (computation) | Frame checks read across the whole spec and branch on `paradigm`; `mathx.py` supplies the pure-function inflation table, imported per the existing idiom, never duplicated. |
| Bayesian monitoring-discipline check (`DSX-PAR-011`) | `dsx/frame/` | — | Same tier as above; no computation helper needed if the check does presence/structural comparison only (numeric `1/(K+1)` comparison is pure arithmetic on declared values if the planner chooses the stronger form). |
| Justification requiredness/symmetry (`DSX-PAR-002`) | `dsx/frame/` | `dsx/spec.py` (vocabulary source) | Requiredness logic lives in the frame check; the vocabulary it validates against (`PARADIGM_JUSTIFICATIONS`) is owned by `spec.py` and must not be duplicated. |
| New `inference:` field schema (`threshold_calibration`, `prior_justification`, `decision_threshold`) | `dsx/spec.py` (contract/schema layer) | `templates/ANALYSIS-SPEC.yaml` (scaffold) | `spec.py` is the single source of truth for `_INFERENCE_FIELDS`; the template must scaffold the fields or they are undiscoverable (no unknown-key check exists under `inference:` today). |
| Gate dispatch / severity thresholds | `dsx/cli.py` | — | `CHECKS["paradigm"] = paradigm.check` and `GATE_PROFILES`/`GATE_THRESHOLDS` already route all four gate points through this one function; **no CLI edit is needed** for Phase 9 (D-01). |
| Decision-record emission | `dsx/frame/paradigm.py` (caller) | `dsx/decisions.py` (schema) | Each new check's key judgement point should emit a `DecisionRecord` via `report.context.setdefault("decisions", [])`, the pattern `dsx/frame/paradigm.py:146-161` and `dsx/spec.py:890-914` both already use. |
| Symmetry audit (evidence artifact) | `references/` (committed docs) | `tests/` (positive-content test) | Must ship with the tool (not `.planning/`, which PR-branch filtering strips) and be checked by a test in the `tests/test_known_bad_corpus.py:270-326` idiom, not left as unchecked prose. |
| Seeded simulation (evidence artifact) | `tests/` | — | Must never be importable from `dsx/` (D-02/D-14) — it is proof-of-property, not gate logic. Runs via `unittest discover`'s default glob, no wiring needed. |

## Standard Stack

### Core

No external libraries. This phase, like the rest of `dsx`, is **Python 3 standard library only**.

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `unittest` (stdlib) | Python 3.x bundled | Test framework for the REQ-P9-07 simulation and all new check tests | Already the repo's only test framework (`scripts/check.sh:7`); no `pyproject.toml`/`requirements.txt`/`setup.py` exists anywhere in the repo (confirmed this session) — introducing a dependency (e.g. `numpy` for the simulation) would be the repo's first external dependency, contradicting the stated argument that "a gate which breaks on a missing dependency is a gate that gets turned off" (D-14). |
| `random.Random(seed)` (stdlib) | Python 3.x bundled | Seeded, reproducible trials for the REQ-P9-07 simulation | Deterministic given a fixed seed; no cryptographic RNG needed since this is a statistical simulation, not a security control. |

### Supporting

None. `dsx/mathx.py::inflation_from_peeking()` is existing, in-repo code (not a package) and is reused, not installed.

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| stdlib `random`/hand-rolled Monte Carlo | `numpy`/`scipy.stats` for the simulation | Faster and less code, but breaks the repo's zero-dependency invariant (D-14) for a sub-second, few-thousand-trial simulation where speed is not the bottleneck — rejected. |
| Numeric `1/(K+1)` comparison inside `DSX-PAR-011` | Presence-only check (declare `threshold_calibration` or `prior_justification`, no arithmetic) | Both satisfy REQ-P9-02 per 09-CONTEXT's Claude's Discretion. The numeric form is a pure comparison of *declared* values (not a computed statistic), so it does not breach brief D-02's "no test statistic or posterior computed on the gate path" — but this reading should be confirmed, not assumed, before relying on it in the plan. |

**Installation:** None required — no new packages.

**Version verification:** N/A (no packages). Python interpreter confirmed present: `python3 --version` → `Python 3.14.6` in this environment (exact CI/production version may differ; the repo has no version pin file, so this is informational, not a constraint to encode).

## Package Legitimacy Audit

**Not applicable — this phase installs no external packages.** `dsx` has zero third-party dependencies (verified: no `pyproject.toml`, `requirements.txt`, `setup.py`, `setup.cfg`, or `Pipfile` anywhere in the repository root). D-14 makes staying stdlib-only an explicit design constraint for the new simulation code, not an oversight. The planner should not introduce any package (including `numpy`) for this phase.

**Packages removed due to [SLOP] verdict:** none.
**Packages flagged as suspicious [SUS]:** none.

## Architecture Patterns

### System Architecture Diagram

```
                    ┌─────────────────────────────┐
                    │   ANALYSIS-SPEC.yaml (input)│
                    │  design.peeking_policy       │
                    │  inference.{paradigm,         │
                    │    paradigm_justification,    │
                    │    threshold_calibration*,    │
                    │    prior_justification*,      │
                    │    decision_threshold*}       │
                    └──────────────┬───────────────┘
                                   │ dsx/loader.py::load()
                                   ▼
                    ┌─────────────────────────────┐
                    │        dsx/cli.py            │
                    │  cmd_gate(point) dispatches   │
                    │  via CHECKS["paradigm"] =     │
                    │  dsx.frame.paradigm.check     │
                    │  (GATE_PROFILES / THRESHOLDS  │
                    │   — unchanged this phase)     │
                    └──────────────┬───────────────┘
                                   │ spec: dict
                                   ▼
        ┌───────────────────────────────────────────────────┐
        │         dsx/frame/paradigm.py :: check(spec)        │
        │                                                     │
        │  DSX-PAR-001 (existing, INFO, never blocks)          │
        │       │                                             │
        │  DSX-PAR-002 (new) ── requiredness/symmetry ──►      │──reads dsx/spec.py::PARADIGM_JUSTIFICATIONS
        │       │                  of paradigm_justification    │  (membership already owned by DSX-SPEC-085)
        │       │                                             │
        │  ┌────┴─────────────────────┐                       │
        │  ▼ paradigm == frequentist   ▼ paradigm == bayesian  │
        │  DSX-PAR-010 (new, CRITICAL) DSX-PAR-011 (new,       │
        │  reuses dsx/mathx.py::         CRITICAL)             │
        │  inflation_from_peeking()     asserts 1/(K+1),       │
        │       │                       K=19 at p=0.95         │
        │       └──────────┬────────────────┘                 │
        │                  ▼                                  │
        │         report.add(...) + DecisionRecord             │
        │         (dsx/decisions.py, same pattern as            │
        │          the existing DSX-PAR-001 emission)           │
        └───────────────────────┬───────────────────────────┘
                                 │ Report (findings + context.decisions)
                                 ▼
                    ┌─────────────────────────────┐
                    │  dsx/findings.py :: emit()   │
                    │  exit 0/1/2 per severity ×    │
                    │  gate threshold (unchanged)   │
                    └─────────────────────────────┘

  * new inference: fields (D-05) — schema owned by dsx/spec.py, scaffolded
    in templates/ANALYSIS-SPEC.yaml; there is no unknown-key check under
    inference: today, so scaffolding is what makes them discoverable.

  Evidence artifacts (outside the gate path):
    references/paradigm-symmetry.md  — committed audit, D-15
    tests/test_*.py                  — seeded simulation, REQ-P9-07, D-02
```

### Recommended Project Structure

No new files/directories beyond what D-01/D-05/D-15/D-14 already specify. Everything lands in existing files, plus exactly two new artifacts:

```
dsx/
├── frame/
│   └── paradigm.py         # EXTEND: add _check_justification, _check_frequentist_monitoring,
│                            #   _check_bayesian_monitoring; extend _PARADIGM_CONDITIONAL;
│                            #   remove 3 entries from _NOT_SHIPPED
├── spec.py                 # EXTEND: _INFERENCE_FIELDS (+3), _validate_inference_shape unaffected
│                            #   (new fields have no membership vocab — see Pitfalls)
├── mathx.py                 # EXTEND (docstring only, D-13): inflation_from_peeking() citation upgrade
templates/
└── ANALYSIS-SPEC.yaml       # EXTEND: inference: scaffold gains 3 new commented fields
references/
├── finding-codes.md         # REGENERATE via scripts/gen-finding-catalogue.py --write
└── paradigm-symmetry.md     # NEW (D-15) — write before the checks, per PITFALLS.md:456-467
examples/known-bad/
├── frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml   # header prose update only (no field change needed —
│                                                              already has alpha_spending: null, no sequential method)
├── frequentist-uncontrolled-continuous-POSTMORTEM.md         # "nothing adjudicates it today" → now false
├── bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml         # header prose update only (new fields absent by default)
└── bayesian-continuous-monitoring-POSTMORTEM.md              # "nothing adjudicates it today" → now false
tests/
├── test_dsx.py              # EXTEND: _INFERENCE_FIELDS drift guard (9 members), new DSX-PAR-* tests
├── test_known_bad_corpus.py # RESTRUCTURE (D-03): per-fixture expected-caught-defect set
├── test_frame_boundary.py   # UNCHANGED — new paradigm.py code still only imports findings/spec/decisions/mathx
└── test_par_monitoring_simulation.py  # NEW (suggested name; D-14) — seeded stdlib simulation,
                              #   picked up automatically by `unittest discover -s tests` (default test*.py glob)
```

### Pattern 1: Frame check decomposition (`_check_*` helpers merged into one `Report`)

**What:** A single `check(spec) -> Report` entry point per module, internally decomposed into private `_check_*` functions that each append findings to the same shared `Report` object.

**When to use:** Any time a check module (`dsx/checks/*.py` or `dsx/frame/*.py`) must emit more than one finding code from one spec — this is the established house pattern, not a Phase 9 invention.

**Example (existing code, `dsx/checks/design.py:444-471`, verified this session):**
```python
def _check_peeking(design: dict, spec: dict, report: Report) -> None:
    policy = normalize(design.get("peeking_policy", "")) if design else ""
    looks = as_number(get(spec, "results.interim_looks"))
    if looks is None:
        return
    looks = int(looks)
    if policy in ("", "fixed_horizon") and looks > 1:
        inflated = inflation_from_peeking(looks, as_number(design.get("alpha")) or 0.05)
        report.add(
            "DSX-EXP-060", "CRITICAL",
            f"{looks} interim looks were taken under a fixed-horizon design",
            detail=(...), remedy=(...), where="spec.results.interim_looks",
            interim_looks=looks, inflated_alpha=round(inflated, 4),
        )
```
The three new Phase 9 checks should follow this exact shape: a `_check_*(spec, report)` function, called from `dsx/frame/paradigm.py::check()`, each appending to the same `report` the module-level `check()` already constructs (it currently builds one `DSX-PAR-001` finding directly in-line — Phase 9 does not need to refactor that call, just add sibling calls before `return report`).

### Pattern 2: Exhaustive per-paradigm applicability map, not `if`/`elif`

**What:** A `dict` keyed by every member of a closed vocabulary (`PARADIGMS`), with a test asserting set-equality against that vocabulary — so a future vocabulary addition fails loudly instead of silently under-covering.

**Example (existing code, `dsx/frame/paradigm.py:38-41`, verified this session):**
```python
_PARADIGM_CONDITIONAL: "dict[str, tuple[str, ...]]" = {
    "frequentist": ("DSX-PAR-010", "DSX-ADM-"),
    "bayesian": ("DSX-PAR-011",),
}
```
D-06 requires the *retype* escape be closed by this same structural property (D-09's parallel requirement: "no reason ranked above another" via one membership path, proven by a 7×2 parametrised test) — not by writing `if paradigm == "frequentist": ... elif paradigm == "bayesian": ...` inside the two new checks.

### Pattern 3: Citation-bearing docstrings on the *enclosing function*, never the module

**What:** `scripts/gen-finding-catalogue.py::_resolve_docstrings()` walks up from each `report.add(...)` call site to the nearest enclosing `FunctionDef`/`AsyncFunctionDef` and reads *that* function's docstring — falling back to the module docstring only if no enclosing function exists.

**Verified trap (already bit plan 06-07, per 09-CONTEXT.md canonical_refs, and independently confirmed by reading `scripts/gen-finding-catalogue.py:193-232`):** if the `Citation:`/`Reference value:` (or `Structural criterion:`) lines are placed on the module docstring while `report.add(...)` is called from inside a named function, `check_d05()` will not find them and `scripts/gen-finding-catalogue.py --check` fails the build.

```python
# Source: dsx/frame/paradigm.py:60-77 (existing DSX-PAR-001, the template to copy)
def check(spec: dict) -> Report:
    """Emit DSX-PAR-001 — the informational paradigm manifest.

    Citation: Deng, A., Lu, J. & Chen, S. (2016), "Continuous Monitoring of
    A/B Tests without Pain: Optional Stopping in Bayesian Testing", IEEE
    DSAA 2016 — ...
    Structural criterion: a set-membership computation over a data-driven
    applicability map ...
    """
```
Each new `_check_*` function needs its **own** docstring carrying these two lines (or the equivalent `Reference value:` form for `DSX-PAR-010`/`DSX-PAR-011`, which have numeric anchors) plus a `# D-05: <CODE>` comment marker somewhere under `tests/`.

### Anti-Patterns to Avoid

- **A second `inflation_from_peeking()`-equivalent table for `DSX-PAR-010`.** REQ-P9-01 explicitly forbids this ("reusing the existing table rather than introducing a second one"). Import it: `from ..mathx import inflation_from_peeking` — permitted by the D-03a boundary scanner (it forbids only `dsx.checks`, and `dsx/checks/design.py:11-18` already shows the identical import idiom from a sibling module).
- **Branching `DSX-PAR-011`'s trigger on `results.interim_looks`.** D-04 is explicit and verified structurally: at `dsx gate plan` there is no `results:` block at all, so a trigger reading it would silently become verify/ship-only, breaking ROADMAP SC 1's "exits 1 at `dsx gate plan`" claim.
- **Re-checking `paradigm_justification` membership inside `DSX-PAR-002`.** `DSX-SPEC-085` already owns that (`dsx/spec.py:916-928`); duplicating it double-fires on `examples/bad-ANALYSIS-SPEC.yaml`, which a committed test (`tests/test_dsx.py:513-528`) already pins at exactly 3 `DSX-SPEC-085` findings.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Type-I inflation under repeated frequentist peeking | A second lookup table or formula | `dsx.mathx.inflation_from_peeking()` (`dsx/mathx.py:411-432`) | Already tested, already independently value-verified (D-13's quadrature+Monte-Carlo cross-check), and REQ-P9-01 forbids a second one outright. |
| Closed vocabulary for paradigm justification reasons | A new `PARADIGM_JUSTIFICATIONS`-equivalent set | `dsx.spec.PARADIGM_JUSTIFICATIONS` (`dsx/spec.py:251-265`) | Already complete (7 members matching brief §5.2), already in `_VOCABULARIES`, already dumped by `dsx vocab`. |
| Exhaustive per-paradigm behaviour switch | Hand-written `if paradigm == "frequentist": ... elif ...` | The `_PARADIGM_CONDITIONAL` dict-keyed-by-`PARADIGMS` pattern (`dsx/frame/paradigm.py:38-41`) | Makes the "provable for every member" property structural rather than something a reviewer has to re-derive by reading branches. |
| Citation bookkeeping / catalogue regeneration | A parallel citation-tracking mechanism | `scripts/gen-finding-catalogue.py`'s existing `_D05_ALLOWLIST_PREFIXES` mechanism — `DSX-PAR-` is **already** in it (`scripts/gen-finding-catalogue.py:58`) | No script edit needed for the three new codes; D-05 enforcement is already wired to fire against them the moment `report.add("DSX-PAR-01x", ...)` exists. |
| Decision-trail emission | A bespoke logging/audit mechanism | `dsx.decisions.DecisionRecord` + `report.context.setdefault("decisions", [])` (`dsx/decisions.py:64-88`, used at `dsx/frame/paradigm.py:146-161`) | Established brief-D-04 API; checks stay pure, only the CLI writes the trail file. |

**Key insight:** almost nothing in this phase requires new infrastructure — the module layout, the vocabulary, the citation-enforcement mechanism, the decision-record schema, and the reusable inflation table all already exist and are already wired to the right gate points. The work is almost entirely *filling in three new `_check_*` functions and one new schema slice* inside structures that were built in Phase 6 specifically to receive them.

## Common Pitfalls

### Pitfall 1: Misattributing the `1/(K+1)` bound to Ville's inequality (or vice versa)

**What goes wrong:** Writing "Ville's inequality gives `1/(K+1)`" or reconciling `0.05` and `0.0526` with the word "rounded" — both individually-true-sounding sentences that combine into a false attribution. This exact drift already happened once in this repo (UAT gap G-01) and was corrected.

**Why it happens:** `1/(K+1)` (Deng, Theorem 1, likelihood-ratio/change-of-measure, an *equality* conditioned on hitting exactly `K`) and `1/k` (Ville, a *maximal inequality* over a whole path) are numerically close at `K=k=19` (`0.05` vs. `≈0.0526`) and answer superficially similar-sounding questions ("what's my false-discovery risk under continuous monitoring?"). They condition on different events — Deng's is FDR (`P(reject | rejected)`), Ville's bounds `P(∃t: M_t ≥ threshold)` — and Deng et al. never cite Ville at all (confirmed: zero occurrences in the arXiv source, per 09-CONTEXT D-12).

**How to avoid:** Cite Deng, Lu & Chen (2016) Theorem 1 for `DSX-PAR-011`'s docstring, cite it for the operational bound at what the paper calls §3.2 (not the two sentences immediately after Theorem 1 in §1, which contain the paper's own slip — see D-10), and mention Ville only as an explicit named contrast ("this is not Ville's inequality, which gives the different bound `1/k`"), never as an alternative derivation of the same number.

**Warning signs:** the phrase "prior-averaged Ville bound" (a name this repo has already retired — `_RETIRED_BOUND_MISATTRIBUTIONS` in `tests/test_known_bad_corpus.py:81-85` blocks it from reappearing anywhere under `examples/known-bad/`, `brief.md`, `REQUIREMENTS.md`, or `ROADMAP.md`); the word "rounded" used to explain away a bound mismatch.

### Pitfall 2: Docstring citation on the wrong scope (module vs. enclosing function)

**What goes wrong:** `scripts/gen-finding-catalogue.py --check` fails with "missing 'Citation:' line" even though a citation clearly exists somewhere in the file, because it was placed on the module docstring while the `report.add()` call lives inside a named function.

**Why it happens:** `_resolve_docstrings()` (`scripts/gen-finding-catalogue.py:193-232`, verified) only falls back to the module docstring when **no** enclosing function is found at all — any named function short-circuits that fallback.

**How to avoid:** Put `Citation:` and `Reference value:`/`Structural criterion:` on each `_check_*` function's own docstring, not on `dsx/frame/paradigm.py`'s module docstring.

**Warning signs:** `scripts/gen-finding-catalogue.py --check` exit 1 naming a code that visibly has a citation somewhere in the file.

### Pitfall 3: Titles that are not AST-literal at the call site

**What goes wrong:** `scripts/gen-finding-catalogue.py`'s AST extractor (`extract()`, `dsx/frame/paradigm.py`-style pattern) requires the third positional argument to `report.add(...)` to be a `Constant` or `JoinedStr` node *at the call site* — a pre-assigned variable collapses to `<…>` in the generated catalogue.

**How to avoid:** Follow the existing `DSX-PAR-001` idiom exactly: build the f-string inline in the `report.add(...)` call, as `dsx/frame/paradigm.py:112-120`'s comment explicitly documents ("The title is a single f-string literal at the call site (not a pre-assigned variable)").

### Pitfall 4: `_INFERENCE_FIELDS` drift-guard test going red silently

**What goes wrong:** `tests/test_dsx.py:504-511` asserts `_INFERENCE_FIELDS` equals a literal 6-tuple. Adding three new field names to `dsx/spec.py` without updating this test's literal breaks the suite — and the failure message ("expected 6-tuple, got 9-tuple") could read as a regression rather than the deliberate D-05 extension it is.

**How to avoid:** Update the test's literal tuple in the **same commit** that extends `_INFERENCE_FIELDS`.

### Pitfall 5: New `inference:` fields silently unvalidated (no unknown-key check)

**What goes wrong:** `dsx/spec.py:843-848`'s own prose states there is no unknown-key check under `inference:` — a misspelled `theshold_calibration` (typo) is accepted silently, with no `DSX-SPEC-08x` finding, unless the field also happens to appear in `templates/ANALYSIS-SPEC.yaml` where an operator can visually compare against the scaffold.

**How to avoid:** Treat the template scaffold and `dsx vocab` extension as load-bearing, not polish (D-05 already says this) — they are the *only* mechanism making the three new fields discoverable/correctable by an operator, since there is no programmatic typo guard.

### Pitfall 6: `DSX-PAR-002`'s severity leaves the D-07 escape half-closed

**What goes wrong:** If `DSX-PAR-002` (HIGH) is the *only* mechanism closing the undeclared-`inference.paradigm` escape, that escape is closed at `verify`/`ship` (HIGH threshold) but **not** at `plan`/`execute` (CRITICAL threshold) — because `GATE_THRESHOLDS` (`dsx/cli.py:105-110`, verified) is CRITICAL at plan/execute. A spec that omits `inference:` entirely would still pass `dsx gate plan` with an uncontrolled-continuous peeking policy declared but unadjudicated by either `DSX-PAR-010` or `DSX-PAR-011` (neither fires — paradigm is blank, so `_PARADIGM_CONDITIONAL` selects nothing).

**How to avoid:** This is explicitly named in 09-CONTEXT D-07 as a decision the planner must make *visibly*, not let fall out of D-02 by default: either accept the plan/verify asymmetry with a stated reason (the manifest `DSX-PAR-001` still surfaces "paradigm=undeclared" at INFO, so it's not silent, just non-blocking at plan), or give the undeclared-paradigm-with-uncontrolled-peeking combination its own CRITICAL-severity path. **Do not silently default to leaving it open at plan.**

### Pitfall 7: Conflating Phase 9's `prior_justification` (presence) with the deferred quality-judgement code

**What goes wrong:** brief.md's original commented-out scaffold (`brief.md:209`, verified this session) maps `prior_justification` to `DSX-PAR-020` — a code explicitly deferred under D-12a (out of scope for v2.0.0, per REQUIREMENTS.md's Out-of-Scope table: "Prior justification and prior sensitivity (`DSX-PAR-020/021`)"). Phase 9 reuses the *field name* `prior_justification` for a different, weaker purpose: a disjunctive presence-only satisfaction path for `DSX-PAR-011` (D-05's phrasing: "the disjunctive `prior_justification` route"). A reader who sees `prior_justification` declared might assume its *quality* has been judged — it has not; only its *presence* has.

**How to avoid:** State explicitly in the `DSX-PAR-011` docstring/remedy text that a non-blank `prior_justification` satisfies the check structurally (presence, not quality) and that prior-justification *quality* is `DSX-PAR-020`'s job, deferred to a later milestone.

## Code Examples

Verified patterns from the live repository (not external docs — this phase's code lives entirely in-repo):

### The existing `DSX-PAR-001` check — the template to extend

```python
# Source: dsx/frame/paradigm.py:60-163 (existing, verified this session)
def check(spec: dict) -> Report:
    """Emit DSX-PAR-001 — the informational paradigm manifest. ..."""
    report = Report(check="paradigm")
    declared = get(spec, "inference.paradigm")
    paradigm = normalize(declared) if not is_blank(declared) else ""
    # ... DSX-PAR-001 logic ...
    report.add("DSX-PAR-001", "INFO", f"paradigm manifest — inference.paradigm: {paradigm or 'undeclared'}",
               detail=detail, remedy=remedy, where="spec.inference.paradigm",
               applied=applied, not_applied=not_applied)
    report.context.setdefault("decisions", []).append(DecisionRecord(...).to_dict())
    return report
```
Phase 9 adds calls to new `_check_justification(spec, report)`, `_check_frequentist_monitoring(spec, report)`, `_check_bayesian_monitoring(spec, report)` before `return report`, each appending to the same `report`.

### The reusable inflation table (REQ-P9-01's required dependency)

```python
# Source: dsx/mathx.py:411-432 (existing, verified this session — do not duplicate)
def inflation_from_peeking(total_looks: int, alpha: float = 0.05) -> float:
    """Approximate true type-I error when a fixed-horizon test is peeked ``n`` times. ..."""
    anchors = {1: 0.05, 2: 0.083, 3: 0.107, 4: 0.126, 5: 0.142, 10: 0.193, 20: 0.248}
    # log-linear interpolation between anchors, scaled by alpha/0.05
```
`DSX-PAR-010` at 5 looks with a fixture declaring `alpha: 0.05` will compute `inflation_from_peeking(5) == 0.142` — this exact value is already asserted elsewhere against the frequentist known-bad fixture's inference-block comment (`examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml:167-170`, verified this session: "approximately 0.142 ... `dsx.mathx.inflation_from_peeking(5) == 0.142`").

### The brief's original (advisory, not binding) shape for the three new fields

```yaml
# Source: brief.md:195-213 (verified this session — advisory scaffold, not binding on field shape)
  # --- bayesian branch ---
  # prior: {family: beta, alpha: 1, beta: 1, scale: weakly_informative}
  # prior_justification: "..."                      # DSX-PAR-020 (deferred; Phase 9 reuses the NAME for a presence-only DSX-PAR-011 path — see Pitfall 7)
  # decision_threshold: "P(uplift > 0.01) > 0.95"
  # threshold_calibration: {method: simulation, sims: 10000, fpr: 0.048}  # DSX-PAR-011
```
This is the closest thing to a canonical shape in the project's own binding brief — `threshold_calibration` as a sub-dict (method/sims/fpr), `decision_threshold` as a free-text posterior-probability expression. 09-CONTEXT.md leaves the exact shape to the planner's discretion, but deviating from this scaffold without a stated reason would be surprising to a reader who already read brief.md §5.2.

### Known-bad fixtures already shaped to trigger both checks without further field edits

Both target fixtures (verified read in full this session) already declare `design.peeking_policy: uncontrolled_continuous`, and neither declares any of the three new `inference:` fields (they don't exist in the spec vocabulary yet) — so once the checks ship, both fixtures should trigger their target code **without any fixture field change**, only header-prose updates (the "nothing adjudicates it today" sentences becoming false). This is a strong signal the D-04 trigger design and the D-05 field additions compose correctly; if a fixture needs new fields added to trigger, that is worth treating as a signal the trigger condition drifted from what 09-CONTEXT specified.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|---------------|--------|
| `inflation_from_peeking()` docstring cites "Armitage's classic result" with no year/paper | Full D-05 citation (Armitage, McPherson & Rowe 1969, JRSS-A 132(2):235-244) with an explicit unverified-locator flag | This phase (D-13, elective upgrade) | Closes the milestone's own STATE.md open item; the function a v2.0.0 check depends on now carries the same evidentiary bar as the check itself. |
| Repo's earlier attribution of the `1/(K+1)` bound to "Ville's inequality" | Corrected to Deng, Lu & Chen (2016) Theorem 1, §3.2, with Ville named only as an explicit contrast | Already corrected before this research pass (UAT gap G-01; REQUIREMENTS.md and ROADMAP.md text confirmed already carrying the fix) | Nothing left to do here structurally — the planner should write the `DSX-PAR-011` docstring to match the already-corrected fixture/post-mortem prose, not re-derive it. |

**Deprecated/outdated:** the phrase "prior-averaged Ville bound" is retired repo-wide and mechanically guarded against reappearing (`tests/test_known_bad_corpus.py:81-94`).

## Assumptions Log

> Every claim below either came from a direct read of the live repository tree or from a web search cross-check against the bibliographic record. None are pure training-data recall presented as fact.

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|----------------|
| A1 | `threshold_calibration` should be a sub-dict `{method:, sims:, fpr:}` per brief.md's commented scaffold, rather than a scalar | Architecture Patterns / Code Examples | Low — 09-CONTEXT explicitly leaves this to planner discretion; brief.md's scaffold is advisory, not binding. If the planner picks a scalar instead, no test or existing code depends on the dict shape. |
| A2 | The undeclared-paradigm escape (D-07) should be closed via `DSX-PAR-002` rather than a new CRITICAL code | Common Pitfalls (Pitfall 6) | Medium — this is 09-CONTEXT's *preferred* mechanism, not a hard lock; the severity consequence is explicitly flagged as unsettled ("Do not settle this silently"). If the planner picks the CRITICAL-code alternative instead, a brief-D-06 permanent code number is spent, which 09-CONTEXT's own rejected-alternative note already weighs against. |
| A3 | A new test file (e.g. `tests/test_par_monitoring_simulation.py`) is the natural home for the REQ-P9-07 simulation, versus adding it to `tests/test_dsx.py` | Recommended Project Structure | Low — either location satisfies "lives under `tests/`" and is picked up by `unittest discover`'s default glob; no test asserts a specific filename. |

**If this table is empty:** N/A — see above.

## Open Questions

1. **Does `DSX-PAR-002` requiredness close the undeclared-paradigm escape at `plan`, or only at `verify`/`ship`?**
   - What we know: `GATE_THRESHOLDS` is CRITICAL at plan/execute, HIGH at verify/ship (`dsx/cli.py:105-110`, verified). `DSX-PAR-002` ships at HIGH (D-02, locked). `DSX-PAR-001` (INFO) already surfaces "paradigm=undeclared" at every gate point without blocking.
   - What's unclear: whether that asymmetry (escape closed at verify/ship, open at plan/execute) is acceptable, or whether a CRITICAL-severity companion is needed for the specific undeclared-paradigm + uncontrolled-peeking combination.
   - Recommendation: the planner should write this decision explicitly into the plan's rationale (09-CONTEXT D-07 already frames both options and their tradeoffs) rather than let severity assignment default silently. Given D-06's "codes never renumbered" pressure and D-07's own preference, defaulting to the `DSX-PAR-002`-only mechanism with an explicitly stated and tested plan/verify asymmetry is the lower-risk choice, but this is the planner's call to make visibly.

2. **Does `DSX-PAR-011` perform the numeric `1/(K+1)` comparison on the gate path, or assert presence only?**
   - What we know: both satisfy REQ-P9-02 per 09-CONTEXT's Claude's Discretion. The numeric form only requires arithmetic on *declared* values (e.g. a declared `decision_threshold` expression parsed for its probability, or a declared `threshold_calibration.fpr`), not a computed statistic or posterior — which 09-CONTEXT argues does not breach brief D-02.
   - What's unclear: whether parsing an operator-declared expression like `"P(uplift > 0.01) > 0.95"` to extract `0.95` for a numeric comparison is itself in-scope for this phase, or over-engineering relative to a simpler presence check plus a docstring-stated reference value.
   - Recommendation: presence-only is the lower-risk default for a first cut (REQ-P9-02's own wording — "asserting the prior-averaged bound 1/(K+1)" — is satisfied by the docstring/test asserting the number, not necessarily by gate-path arithmetic on every spec). If the planner wants the stronger numeric form, confirm the D-02 reading with the discuss owner before committing to it, per 09-CONTEXT's explicit caveat.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| Python 3 interpreter | All of `dsx`, all tests | ✓ | 3.14.6 (this environment) | — (no fallback needed; repo has no version pin, so any Python 3.x with `unittest`, `random`, `ast`, `re` from stdlib suffices) |
| `pyproject.toml` / `requirements.txt` / `setup.py` / `Pipfile` | N/A | ✗ (confirmed absent) | — | Intentional — repo is stdlib-only by design (D-14); this is a design invariant to preserve, not a gap to fill. |
| Git repository / working tree | Committing `references/paradigm-symmetry.md`, fixture edits | ✓ | — | — |

**Missing dependencies with no fallback:** none — nothing is missing that this phase needs.
**Missing dependencies with fallback:** none.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Python stdlib `unittest` (no version pin; bundled with the interpreter) |
| Config file | none — `scripts/check.sh:6-7` runs `python3 -m unittest discover -s tests -q` with default discovery (`test*.py` glob, no `unittest.cfg`) |
| Quick run command | `python3 -m unittest tests.test_dsx -v` (or a single test: `python3 -m unittest tests.test_dsx.<TestClass>.<test_name> -v`) |
| Full suite command | `sh scripts/check.sh` (unit tests + finding-catalogue freshness/D-05 check + capability-manifest validation + good/bad gate contract + determinism check) |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|--------------------|--------------|
| REQ-P9-01 | `DSX-PAR-010` fires on frequentist + uncontrolled_continuous + no alpha_spending/sequential method, reuses `inflation_from_peeking()` | unit + fixture (CLI exit code) | `python3 -m unittest tests.test_dsx -k paradigm_010 -v` (new test, name TBD by planner); `./bin/dsx gate plan --spec examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml --json` (exit 1, code `DSX-PAR-010`) | ❌ Wave 0 — new unit test + fixture already exists, only its expected exit code changes (D-03) |
| REQ-P9-02 | `DSX-PAR-011` fires on bayesian + uncontrolled_continuous + no threshold_calibration/prior_justification, asserts `1/(K+1)=0.05` at `K=19` | unit + fixture (CLI exit code) + seeded simulation | `./bin/dsx gate plan --spec examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml --json` (exit 1, code `DSX-PAR-011`); `python3 -m unittest tests.test_par_monitoring_simulation -v` (new file, D-14) | ❌ Wave 0 — new unit test + new simulation test file; fixture already exists |
| REQ-P9-03 | `DSX-PAR-011` docstring states prior-averaged vs. point-null/LIL distinction; fixture traces theorem number | doc/text assertion | `scripts/gen-finding-catalogue.py --check` (D-05 mechanics: Citation:/Reference value: lines) + a new positive-text test asserting the docstring contains both formulation names | ❌ Wave 0 — new test |
| REQ-P9-04 | `DSX-PAR-002` requiredness/symmetry, no reason ranked above another (7×2 parametrised) | unit (parametrised) | `python3 -m unittest tests.test_dsx -k par_002 -v` (new test) | ❌ Wave 0 — new test |
| REQ-P9-05 | Neither code satisfiable by retyping `paradigm`; both directions | unit (bidirectional, using existing fixtures retyped in-memory) | `python3 -m unittest tests.test_dsx -k retype -v` (new test — load each known-bad fixture, override `inference.paradigm` to the other value, assert exit 1 under the *other* code) | ❌ Wave 0 — new test |
| REQ-P9-06 | Documented symmetry audit of cheapest dishonest satisfaction path per half | positive-content doc test (idiom from `tests/test_known_bad_corpus.py:270-326`) | `python3 -m unittest tests.test_known_bad_corpus -k symmetry -v` (new test) checking `references/paradigm-symmetry.md` exists and states both halves' clearing conditions | ❌ Wave 0 — new file + new test |
| REQ-P9-07 | Seeded, reproducible simulation under `tests/`, never on gate path | unit (simulation, monotone-trend + fixed-ceiling assertions) | `python3 -m unittest tests.test_par_monitoring_simulation -v` | ❌ Wave 0 — new file |

### Sampling Rate

- **Per task commit:** `python3 -m unittest tests.test_dsx tests.test_known_bad_corpus tests.test_frame_boundary -v` (the three modules Phase 9 touches) plus `python3 scripts/gen-finding-catalogue.py --check` (fast; catches D-05 docstring/marker regressions immediately).
- **Per wave merge:** `sh scripts/check.sh` (full suite: unit tests, catalogue freshness, capability manifest, good/bad gate contract at all four points, determinism).
- **Phase gate:** Full suite green before `/gsd-verify-work`, plus a manual `./bin/dsx gate plan --spec <each known-bad fixture>` run to eyeball the exact finding code and message (the D-15 audit's own positive-content test should already cover the machine-checkable half of this).

### Symmetry testing (REQ-P9-05), concretely

Both directions must be asserted by test, not just by inspection:

1. **Retype the frequentist bad fixture to `bayesian`:** load `examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml`, override `inference.paradigm: bayesian` in memory (or via a copy), run `dsx gate plan`, assert exit `1` and assert `DSX-PAR-011` (not `DSX-PAR-010`) is in the finding codes.
2. **Retype the Bayesian bad fixture to `frequentist`:** same pattern in reverse — assert exit `1` naming `DSX-PAR-010`.

Both assertions belong in the same test module (`tests/test_dsx.py`, following the pattern already established by `tests/test_dsx.py:2585-2607`'s `_NOT_SHIPPED` proof, which loads fixtures programmatically rather than hardcoding expected output strings) so a future asymmetric edit to one direction is caught by running the whole file, not just half of it.

### Keeping the seeded simulation off the gate path (REQ-P9-07, D-02) while reproducible

- **Location, not a flag, is the enforcement mechanism.** The simulation lives as a `unittest.TestCase` under `tests/` and is never imported from anywhere under `dsx/` — `tests/test_frame_boundary.py`'s AST scanner only checks `dsx/frame/` imports, so there is no existing mechanical guard preventing a `dsx/` module from importing a `tests/` module; the discipline here is a code-review/plan-checker concern, not an automated one. The plan should state explicitly that no file under `dsx/` imports anything from `tests/`.
- **Reproducibility:** seed the `random.Random` instance with a literal, fixed integer (not derived from wall-clock time or `os.urandom`), and assert the exact same summary statistic (e.g. observed FDR) twice from two separately-seeded runs with the same seed, to prove determinism the way `scripts/check.sh:27-31`'s existing "identical input, identical output" pattern does for `dsx audit`.
- **Budget:** D-14 specifies "sub-second, a few thousand trials" — resolution is not the goal, the property (monotone trend under the point-null formulation; fixed `1/(K+1)` ceiling under the prior-averaged formulation) is.
- **Default execution:** because `scripts/check.sh` uses `unittest discover`'s default glob (`test*.py`), any correctly-named new file under `tests/` runs automatically — no `scripts/check.sh` edit and no CI config edit is needed to wire it in.

### Wave 0 Gaps

- [ ] New test assertions in `tests/test_dsx.py` for `DSX-PAR-002`, `DSX-PAR-010`, `DSX-PAR-011` (unit-level, spec-construction style matching existing `TestDesignChecks`/`TestParadigm` classes) — covers REQ-P9-01, REQ-P9-02, REQ-P9-04
- [ ] Bidirectional retype tests (both fixtures, both directions) — covers REQ-P9-05
- [ ] `_INFERENCE_FIELDS` drift-guard test literal update (9-tuple) — required, not new, but must not be forgotten (Pitfall 4)
- [ ] `tests/test_par_monitoring_simulation.py` (or equivalent new file) — covers REQ-P9-07, and its two-formulation assertions feed REQ-P9-03's docstring accuracy
- [ ] `tests/test_known_bad_corpus.py` restructuring (D-03) — per-fixture expected-caught-defect set, replacing the current blanket "exits 0 at plan/execute" assumption for the two monitoring fixtures
- [ ] Positive-content test for `references/paradigm-symmetry.md` (D-15) — covers REQ-P9-06
- [ ] Framework install: none — stdlib only, nothing to install

## Security Domain

`security_enforcement` is enabled in `.planning/config.json` (ASVS level 1, `security_block_on: high`). `dsx` is an offline, single-user CLI static-analysis tool with no network listener, no authentication surface, no session state, and no persisted user data beyond the trail file the operator's own filesystem already controls. Most ASVS categories (V2 Authentication, V3 Session Management, V4 Access Control, V6 Cryptography) are structurally inapplicable to this phase's change surface — Phase 9 adds no new I/O boundary, no new file format beyond extending the existing YAML `inference:` block, and no new external input beyond what `dsx/loader.py` already parses.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|----------------|---------|-------------------|
| V2 Authentication | No | No auth surface; single-user local CLI. |
| V3 Session Management | No | No sessions. |
| V4 Access Control | No | No multi-principal access model. |
| V5 Input Validation | Yes | Closed-vocabulary membership checks (`normalize()` + set-membership against `PARADIGMS`/`PARADIGM_JUSTIFICATIONS`/new field vocabularies, per the existing `_validate_inference_shape` pattern, `dsx/spec.py:868-941`) — never free-text pattern matching or `eval()`-style parsing of a declared expression like `decision_threshold`. If the numeric-comparison route from Open Question 2 is chosen, any parsing of an operator-declared string must use a narrow, explicit grammar (not `eval`), matching the existing repo-wide avoidance of dynamic code execution over spec content. |
| V6 Cryptography | No | No secrets, no crypto operations; `random.Random(seed)` in the REQ-P9-07 simulation is explicitly non-cryptographic and appropriately so (statistical reproducibility, not confidentiality). |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|-----------------------|
| A malicious/malformed `ANALYSIS-SPEC.yaml` causing unbounded recursion or resource exhaustion while parsing new `inference:` fields | Denial of Service | Reuse `dsx/loader.py`'s existing bundled YAML fallback parser and `dsx/spec.py`'s existing `get()`/`is_blank()`/`normalize()` helpers, which already handle arbitrary nested/malformed input defensively (never raise on missing keys, per `get()`'s docstring) — do not write new bespoke parsing logic for the three new fields. |
| An operator declaring a `decision_threshold` expression designed to be parsed unsafely (if the numeric-comparison route is chosen) | Tampering / Code Injection | Never use `eval()`/`exec()` on a declared spec string. If numeric extraction is needed, use a narrow regex or a small explicit grammar, matching the repo's existing avoidance of dynamic evaluation anywhere in `dsx/`. |
| Suppressing a genuine `DSX-PAR-010`/`DSX-PAR-011` finding via `suppressions[]` without a real ADR/SPEC authority | Repudiation | Already handled by the existing `suppressions[]` mechanism's authority requirement (unknown codes abort with exit 2) — no new mitigation needed, but the planner should confirm `DSX-PAR-010`/`DSX-PAR-011` are suppressible the same way every other CRITICAL code is (no special-casing). |

## Sources

### Primary (HIGH confidence — read directly from the live repository in this session)

- `dsx/frame/paradigm.py` (full file) — existing `DSX-PAR-001` check, `_PARADIGM_CONDITIONAL`, `_NOT_SHIPPED`, `_PARADIGM_INDEPENDENT`
- `dsx/spec.py:245-297, 830-942` — `PARADIGMS`, `PARADIGM_JUSTIFICATIONS`, `_VOCABULARIES`, `_INFERENCE_FIELDS`, `_INFERENCE_MEMBERSHIP`, `_validate_inference_shape`
- `dsx/spec.py:60-74` — `PEEKING_POLICIES` including `uncontrolled_continuous`
- `dsx/mathx.py:411-432` — `inflation_from_peeking()`
- `dsx/checks/design.py:1-20, 430-471` — `_check_peeking`/`DSX-EXP-060`, the import idiom
- `dsx/cli.py:80-110` — `CHECKS`, `GATE_PROFILES`, `GATE_THRESHOLDS`
- `dsx/decisions.py:55-88` — `DecisionRecord`
- `dsx/findings.py:190-218` — `Report.add`/`merge`/`CheckError`
- `dsx/suppressions.py:1-44` — `known_codes()`
- `dsx/frame/__init__.py` (full file) — D-03a boundary prose
- `tests/test_dsx.py:495-530, 670-691, 1380-1398, 2570-2611` — inference-block tests, `DSX-EXP-060` disjointness test, template-passes-gate-plan tests, `DSX-PAR-001` invariant tests, `codes()` helper
- `tests/test_known_bad_corpus.py` (full file) — corpus invariants, `_INCIDENTAL_GAP_CODES`, `_RETIRED_BOUND_MISATTRIBUTIONS`, `_BOUND_CLAIM_DOCUMENTS`, the three D-10-related regression guards
- `tests/test_frame_boundary.py` (full file) — D-03a AST scanner
- `scripts/gen-finding-catalogue.py:30-310` — `PREFIX_GROUPS`, `_D05_ALLOWLIST_PREFIXES`, `check_d05()`, `_resolve_docstrings()`
- `scripts/check.sh` (full file) — test/build entrypoint
- `templates/ANALYSIS-SPEC.yaml:335-364` — `inference:` scaffold
- `examples/good-ANALYSIS-SPEC.yaml:138-140, 353-357` — good fixture's `peeking_policy: fixed_horizon`
- `examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml` (full file), `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` (full file), `examples/known-bad/bayesian-continuous-monitoring-POSTMORTEM.md` (full file)
- `README.md:304-363` — "Two tiers of evidentiary rigour"
- `references/finding-codes.md:347-353` — confirms only `DSX-PAR-001` currently in the catalogue
- `brief.md:195-221` — original `inference:` scaffold including the three new fields' advisory shape
- `.planning/ROADMAP.md:311-340` — Phase 9 goal/success criteria (confirmed already carrying the D-10-corrected wording)
- `.planning/config.json` — `nyquist_validation: true`, `security_enforcement: true`, no search-provider flags enabled

### Secondary (MEDIUM confidence — web search, cross-checked against the primary-source read already done at discuss time)

- Deng, A., Lu, J. & Chen, S. (2016), "Continuous Monitoring of A/B Tests without Pain: Optional Stopping in Bayesian Testing", IEEE International Conference on Data Science and Advanced Analytics (DSAA) 2016, Montreal, Oct 17-19, 2016, pp. 243-252 — bibliographic details (venue, page range) confirmed via dblp/arXiv/ResearchGate this session; content (Theorem 1 proved via change-of-measure) confirmed consistent with the direct arXiv-source read already performed at discuss time.
- Armitage, P., McPherson, C. K. & Rowe, B. C. (1969), "Repeated Significance Tests on Accumulating Data", *Journal of the Royal Statistical Society, Series A (General)*, 132(2): 235-244, DOI 10.2307/2343787 — bibliographic record confirmed via Oxford Academic/Wiley this session. Full text remains inaccessible (paywalled) — no table or page independently verified in this session, consistent with D-13's unverified-locator flag; **no table/page citation should be added regardless of this confirmation.**
- Ville's inequality — `P(sup_t M_t ≥ α) ≤ 1/α` for a nonnegative test martingale, confirmed via web search this session against a 2023 restatement (Ramdas, Grünwald, Vovk & Shafer, *Statistical Science* 38(4), arXiv:2210.01948) matching 09-CONTEXT's own citation of the same source.

### Tertiary (LOW confidence)

- None used in this research — every claim above was either read directly from the repository or cross-checked via web search against a bibliographic record.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no external dependencies exist or are needed; confirmed by direct filesystem check (no manifest files).
- Architecture: HIGH — every pattern cited was read from the live file at the stated line range in this session, not inferred from 09-CONTEXT's prose alone.
- Statistical citations: HIGH — independently cross-checked via web search against bibliographic records, consistent with 09-CONTEXT's own direct-primary-source read at discuss time; no discrepancy found.
- Pitfalls: HIGH — six of seven pitfalls are drawn from verified, already-existing guard mechanisms in the codebase (tests, AST scanners, allow-lists), not speculative.
- Open questions: MEDIUM — both open questions are genuine unresolved design choices 09-CONTEXT itself flags as "do not settle silently"; this research states the tradeoffs but does not resolve them, by design.

**Research date:** 2026-08-12
**Valid until:** Effectively indefinite for the code-location claims (they will go stale only when Phase 9 itself edits those files, which is expected). The citation claims are stable primary-literature facts (no re-verification cadence needed). Treat as valid through the end of Phase 9's execution; re-verify file:line references if execution is paused for more than a few weeks and other phases (7/8) land in the interim, since they touch adjacent files (`dsx/spec.py`, `dsx/frame/`).
