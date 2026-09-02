# Phase 18: Correlation, association and agreement - Research

**Researched:** 2026-09-01
**Domain:** Extension of an existing declaration-only Python gate library (no new
statistics computed, no new package, no data path). The task is: add one dataless
routing function, one new gate function emitting five new HIGH codes from two
pre-allocated code decades, three new closed sub-vocabularies, and a report-only
effect-size convention registry that must NOT widen the existing blocking band
domain.
**Confidence:** HIGH on every claim tagged `[VERIFIED: live tree]` below — every
locator, line number, and mechanism cited was read directly from the live
repository during this session (not recalled from training data, not copied
from a stale prior-phase document). MEDIUM/flagged-`[ASSUMED]` on the handful of
field-shape decisions 18-CONTEXT.md D-03/D-05 explicitly deferred to "a plan-time
binding for S2-2" — those are called out individually in Open Questions and are
NOT yet resolved anywhere in the committed tree.

## Summary

Phase 18 touches four files that already exist (`dsx/checks/stats.py`,
`dsx/spec.py`, `dsx/mathx.py`, `references/test-selection.md`), one generated
file that must be regenerated not hand-edited (`references/finding-codes.md`),
one build script that needs a small addition most of 18-CONTEXT.md's own
locator list omits (`scripts/gen-finding-catalogue.py`), one invariant test that
must move its pinned numbers (`tests/test_finding_catalogue_invariant.py`), one
ungated template (`templates/APA-TABLE-research.md`), and several new test
files. Nothing here computes a number from data: every new check compares
DECLARED strings/structures in `ANALYSIS-SPEC.yaml` against closed vocabularies
or acceptable-coefficient sets, exactly the same idiom Phase 17 already
established and this session re-verified is still live and unchanged.

Three things this research found that the phase's own scoping documents
(18-CONTEXT.md, the additional-context locator list) do not spell out at
implementation granularity, and that materially change how Plan 18-A should be
written:

1. **The five new codes are invisible to the D-05 citation build gate unless
   explicitly added to an allowlist.** `scripts/gen-finding-catalogue.py`'s
   `check_d05()` only enforces the "Citation: / Reference value: / # D-05: CODE
   test marker" discipline on codes matching `_D05_ALLOWLIST_PREFIXES` (six
   hyphen-terminated family prefixes, none of which is `"DSX-STA-"`) or named
   individually in `_D05_ALLOWLIST_CODES`. `DSX-STA-*` is a large pre-existing
   family with ~40 legacy codes carrying no citation; adding the prefix would
   retroactively fail the build on all of them. The correct mechanism — already
   established four times in this exact file (`DSX-EXP-070`, `DSX-MET-021`,
   `DSX-COH-040`, and the `DSX-SPEC-08x`/`DSX-ML-0xx` set) — is to add the five
   new codes **by exact name** to `_D05_ALLOWLIST_CODES`. Without this edit the
   `--check` build gate stays green even if the five new codes ship with no
   citation at all, silently defeating REQ-P18-03/04's own "D-05 citation +
   published reference value" requirement.
2. **`check_d05`'s docstring resolution is per nearest-enclosing-function, not
   per-code.** If all five `report.add(...)` call sites for DSX-STA-050/051/
   060/061/062 live inside one monolithic `_check_declared_association`
   function, the build gate is satisfied by a single shared `Citation:` /
   `Structural criterion:` line covering all five — which would let an honest
   but generic docstring quietly launder five different citation obligations
   (Pearson/Spearman/Kendall/point-biserial/phi family for 050/051;
   Shrout-Fleiss + McGraw-Wong for 060; a weighted-kappa weighting citation for
   061; Feinstein-Cicchetti Parts I+II for 062) into one pass. Splitting into
   two private helpers — one for the two correlation codes, one for the three
   agreement codes — gives each its own attributable docstring and matches
   D-02's own framing ("two correlation + three agreement" as distinct
   predicate groups).
3. **Neither canonical fixture needs editing to stay silent.** Both
   `examples/good-ANALYSIS-SPEC.yaml` and `examples/bad-ANALYSIS-SPEC.yaml`
   were read in full this session. Their `analysis:` blocks declare
   `test: two_proportion_z` / `test: welch_t` with `estimand_kind:
   linear_association` — neither is a correlation coefficient, neither
   `estimand_kind` is `agreement`/`method_comparison`, and neither declares any
   ICC/kappa sub-fields. None of the five new predicates can fire against
   either file as it stands today. D-08's "extend, not replace" is a safety
   rail for IF the planner chooses to add illustrative rows, not a requirement
   that they must be touched — confirm silence empirically with `dsx audit
   --spec` rather than assuming an edit is owed.

**Primary recommendation:** implement `recommend_association` and
`_check_declared_association` in `dsx/checks/stats.py` exactly as D-01
specifies, but split the gate body into two private helpers by predicate
group (`_check_correlation_scale_kind` for 050/051, `_check_agreement_
completeness` for 060/061/062) so each carries its own D-05 docstring; add all
five codes by exact name to `scripts/gen-finding-catalogue.py`'s
`_D05_ALLOWLIST_CODES`; and treat the three field-shape questions D-03/D-05
left open (declared operand scale; ICC triple nesting; kappa weights/companion
nesting) as this session's concrete, reasoned recommendations — not as already
decided — per Open Questions below.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| `recommend_association` routing lookup | Backend / gate library (`dsx/checks/stats.py`) | Docs (`references/test-selection.md`) | Dataless pure function; the doc section is the human-readable mirror, kept in lockstep by convention (no generator yet, per Phase 17's own open item — REQ-P20-04 is the future general mechanism). |
| `_check_declared_association` (DSX-STA-050/051/060/061/062) | Backend / gate library (`dsx/checks/stats.py`) | — | Declaration-only string/structure comparison against `ANALYSIS-SPEC.yaml`'s `analysis:` block; same tier as the existing `_check_declared_test`. |
| ICC triple / kappa companion / coefficient closed vocabularies | Backend / spec contract (`dsx/spec.py`) | CLI (`dsx/cli.py::cmd_vocab`, if registered) | Mirrors `ESTIMAND_KINDS`'s placement rationale: `dsx.spec` is the sole `_VOCABULARIES` registry; `dsx.checks.stats` must import from it, never the reverse (enforced import-direction boundary). |
| D-05 citation/reference-value build gate | Build script (`scripts/gen-finding-catalogue.py`) | Test suite (`tests/test_finding_catalogue_invariant.py`) | The allowlist-and-docstring-resolution mechanism lives in the generator; the invariant test only re-reads its output. |
| Effect-size convention bands (Kendall's W, kappa, ICC) | Backend / stats kernel (`dsx/mathx.py`) | Ungated template (`templates/APA-TABLE-research.md`) | `mathx.py` is the sole source of numeric bands (mirrors `EFFECT_SIZE_KINDS`/`interpret_effect`'s existing placement); the template is the one and only wiring point that mints no finding code (D-06). |
| Report-only effect-size KIND recognition (DSX-STA-012 branch) | Backend / gate library (`dsx/checks/stats.py`) | Backend / stats kernel (`dsx/mathx.py`, the new registry) | The blocking guard stays in `stats.py`; the registry it consults is imported from `mathx.py`, the same coupling pattern `EFFECT_SIZE_KINDS` already uses today. |

## User Constraints

<user_constraints>

### Locked Decisions (18-CONTEXT.md `## Decisions` D-01…D-08, verbatim intent — see 18-CONTEXT.md for exact wording)

- **D-01** — Hybrid routing shape: a new dataless pure function
  `recommend_association(estimand_kind: str) -> {tests, effect_size, citation}`
  returning the acceptable-coefficient SET per `estimand_kind`
  (`linear_association` -> {pearson_correlation, point_biserial};
  `monotone_association` -> {spearman_correlation, kendall_tau_b};
  `nominal_association` -> {phi, cramers_v}), plus a new gate function
  `_check_declared_association(analysis, spec, report)` sitting beside
  `_check_declared_test`. `recommend_test` is left untouched. A new
  "Association / agreement" section is added to `references/test-selection.md`.
  The gate membership-checks a SET, not one coefficient (a legitimate
  Kendall-vs-Spearman choice must not be over-blocked).
- **D-02** — Five new HIGH codes, from the Phase-17 pre-allocated ranges:
  `DSX-STA-050` (Pearson declared against declared-ordinal, >2 levels),
  `DSX-STA-051` (correlation coefficient declared for an `agreement`/
  `method_comparison` estimand), `DSX-STA-060` (ICC without full declared
  (model, type, definition) triple), `DSX-STA-061` (weighted kappa without
  declared weights), `DSX-STA-062` (kappa without declared p_pos/p_neg
  companions). 050/051 mutually exclusive by `estimand_kind`; 052-059 and
  063-069 stay free for later codes.
- **D-03** — DSX-STA-050 whitelist: fires ONLY when declared operand scale is
  `ordinal` with MORE than two levels; declared `point_biserial` and any
  declared-dichotomous (2-level) operand are whitelisted and never fire 050.
  The operand scale must be a DECLARED field, never inferred from data;
  absence non-blocking; **the exact field shape is a plan-time binding for
  S2-2** — reuse an existing declared measurement-scale field if
  `ANALYSIS-SPEC.yaml` already carries one, else add an additive,
  membership-guarded one.
- **D-04** — DSX-STA-062 companions are `p_pos` AND `p_neg` specifically (not
  "raw agreement + prevalence" as REQUIREMENTS.md's own parenthetical says) —
  the HQ-16-corrected reading of Feinstein & Cicchetti 1990. Cites BOTH Part I
  (43(6):543-549, the paradoxes) and Part II (43(6):551-558, the p_pos/p_neg
  recommendation). REQUIREMENTS.md is not edited this firing (HQ-20
  non-blocking veto window covers the one-word alignment).
- **D-05** — ICC triple = presence + membership completeness only (not
  combination-coherence, which is deferred as candidate `DSX-STA-063`).
  Admissible values: `model` in {`one_way_random`, `two_way_random`,
  `two_way_mixed`}; `type` in {`single`, `average`}; `definition` in
  {`consistency`, `absolute_agreement`} (Shrout & Fleiss 1979; McGraw & Wong
  1996 corrected edition).
- **D-06** — Effect-size KIND handling is a report-only registry; the blocking
  band domain STAYS `{d, h, r}` — never widen `mathx.EFFECT_SIZE_KINDS`.
  DSX-STA-012's remedy branches for report-only kinds ("magnitude is a labeled
  convention, not a gated band"). Bands live in `mathx.py` report-only tables,
  wired only into the ungated `templates/APA-TABLE-research.md` (mints no
  finding code).
- **D-07** — Pin vs catalog-only: Krippendorff alpha = 0.7598 @ ordinal level
  (MUST carry `level: ordinal`) and Landis-Koch kappa bands PIN values, label
  convention. ICC (Koo-Li) bands, Kendall's W bands, dCor, partial correlation,
  Cronbach->omega, and the P18-03 doctrinal scale citation ALL ship
  catalog-only / not-in-hand — no fabricated locator, no invented boundary
  value.
- **D-08** — Two file-disjoint plans: **Plan 18-A** (routing + gates + doc/
  catalogue lockstep) writes `dsx/checks/stats.py`, `dsx/spec.py`,
  `references/test-selection.md`, `references/finding-codes.md` (regenerated),
  gate fixtures, gate tests (050/051/060/061/062), the P18-06 no-autoswitch
  test. **Plan 18-B** (effect-size convention vocabulary) writes
  `dsx/mathx.py`, `templates/APA-TABLE-research.md`, extends the existing
  011/012 tests. Semantic coupling only: 18-A imports `EFFECT_SIZE_KINDS` from
  18-B's `mathx.py`.

### Claude's Discretion

18-CONTEXT.md does not carry a separate "Claude's Discretion" heading — the
phase is fully bound by D-01...D-08. The residual implementation mechanics
D-03 and D-05 explicitly defer ("a plan-time binding for S2-2") are exactly
what this research resolves with concrete, reasoned recommendations rather
than treating them as pre-decided — see Open Questions. Additionally
undecided by 18-CONTEXT.md, confirmed this session, and left to the planner:
whether to add a `dsx recommend-association` CLI subcommand mirroring `dsx
recommend-test` (not required by any REQ-P18 item — recommendation: defer,
non-blocking), and whether to register the new ICC/kappa/coefficient
sub-vocabularies in `dsx/spec.py`'s `_VOCABULARIES` list so `dsx vocab` dumps
them (not required by any REQ-P18 item, unlike REQ-P17-02's explicit `dsx
vocab` requirement for `estimand_kind` — recommendation: register anyway, for
consistency with house style, low cost).

### Deferred Ideas (OUT OF SCOPE for Phase 18)

- **HQ-20 veto window (non-blocking):** the D-02 code numbering and the D-04
  requirement-parenthetical alignment ("prevalence" -> "p_pos/p_neg"). Silence
  = accept; do not action unless HQ-20 resolves with an objection.
- **Coefficient-typo guard** (e.g. a typo'd `"pearsons"` matching no family and
  escaping all five new gates) — named, deferred, candidate for the 130s
  reserve. Do not build a test-name closed-vocab guard this phase.
- **ICC combination-coherence** (`one_way_random` requiring `absolute_
  agreement`) — deferred as candidate `DSX-STA-063`, falsifiable D-13 entry
  condition: a fixture demonstrating a complete-but-incoherent triple passing
  DSX-STA-060.
- **D-05 not-in-hand:** ICC (Koo-Li) band VALUES, Kendall's W bands (no
  citation exists anywhere in the repo or HQ-16), the P18-03 external
  doctrinal scale citation — all ship catalog-only / definition-backed. Do not
  invent a locator or a numeric boundary for any of these this phase.
- Renaming or restructuring `estimand_kind` — resolved by Phase 17, do not
  revisit.

</user_constraints>

<phase_requirements>

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-P18-01 | Decision-table rows (doc + `recommend_test`... actually `recommend_association`, kept in lockstep): Pearson, Spearman, Kendall tau-b, point-biserial, phi keyed on DECLARED `estimand_kind`; dCor/partial ship catalog-only | D-01's exact acceptable-set mapping confirmed against live `ESTIMAND_KINDS` docstrings in `dsx/spec.py:398-423` (already names which coefficients each kind routes to, consistent with D-01); `recommend_association` sketch and `test-selection.md` Association-section sketch below |
| REQ-P18-02 | Agreement/reliability rows: Cohen's/weighted/Fleiss kappa, Krippendorff alpha, ICC (model,type,definition) triple, Bland-Altman for `method_comparison`; Cronbach->McDonald-omega pointer row | Row content and D-07 pin/catalog-only disposition table reproduced verbatim above; `test-selection.md` Association-section sketch below covers all named rows |
| REQ-P18-03 | Gate: correlation scale/kind match (DSX-STA-050/051) | Exact predicates, exact whitelist reasoning, and the field-shape gap (operand scale) all resolved below with a concrete recommendation; D-05 build-gate allowlist requirement identified (not previously called out) |
| REQ-P18-04 | Gate: agreement declaration completeness (DSX-STA-060/061/062) | Exact predicates reproduced; the weighted-kappa `weights` field's heterogeneous type (string enum OR explicit matrix) identified as a deviation from the pure-string-membership idiom every other guard in this codebase uses — flagged as Pitfall 5 |
| REQ-P18-05 | Effect-size vocabulary growth in `dsx/mathx.py`, report-only, wired into `templates/APA-TABLE-research.md` | `EFFECT_SIZE_KINDS`/`interpret_effect` locators confirmed at `dsx/mathx.py:296,299-319`; DSX-STA-011/012 locators confirmed at `dsx/checks/stats.py:297-326`; the ambiguous "remedy branches" language in D-06 resolved into a concrete recommendation (see Pitfall 6) |
| REQ-P18-06 | No-autoswitch invariant extends to this category, asserted by test | `recommend_association`'s dataless signature (no `n`, no `data`, no distribution flag) is itself the structural proof; test sketch below modelled on `tests/test_no_shapiro_autoswitch.py` and Phase 17's `test_time_to_event_fallthrough.py` |

</phase_requirements>

## Standard Stack

Not applicable in the conventional sense — this phase installs no package and
uses no library beyond the Python 3 standard library, matching D-01/D-02's
gate-path constraint. `[VERIFIED: live tree]` `python3 --version` on this
machine reports `3.14.6`; `python3 -m unittest tests.test_finding_catalogue_
invariant -v` runs clean (2/2 tests pass) from repo root this session,
confirming the stdlib `unittest` runner and the pre-Phase-18 baseline (260
codes) are both live and unchanged. No `pytest` is installed or used anywhere
in this repo — do not write `pytest`-only syntax into any new test file.

## Package Legitimacy Audit

Not applicable. This phase installs zero external packages. No `npm view` /
`pip index versions` / registry check is needed.

## Architecture Patterns

### System Architecture Diagram

```
ANALYSIS-SPEC.yaml (analyst-authored, or a fixture)
        |
        v
dsx/checks/stats.py::check(spec)
        |
        |-- section(spec, "analysis")
        |         |
        |         |-- _check_declared_test(analysis, spec, report)      [UNTOUCHED, D-01]
        |         |       |-- membership loop (outcome_type, estimand_kind)  -> DSX-STA-040
        |         |       `-- recommend_test(outcome_type, n_groups, ...)    -> DSX-STA-041/042/043
        |         |
        |         `-- _check_declared_association(analysis, spec, report)   [NEW, beside the above]
        |                 |
        |                 |-- _check_correlation_scale_kind(analysis, report)   [recommended split]
        |                 |       |-- declared test == pearson_correlation AND
        |                 |       |   declared operand_scale == ordinal (>2 levels, D-03 whitelist)
        |                 |       |       -> DSX-STA-050
        |                 |       `-- declared test in CORRELATION_FAMILY AND
        |                 |           declared estimand_kind in {agreement, method_comparison}
        |                 |               -> DSX-STA-051
        |                 |
        |                 `-- _check_agreement_completeness(analysis, report) [recommended split]
        |                         |-- declared ICC row: model/type/definition
        |                         |       incomplete or out-of-vocabulary -> DSX-STA-060
        |                         |-- declared weighted_kappa: weights
        |                         |       blank/unrecognised               -> DSX-STA-061
        |                         `-- declared kappa family: p_pos/p_neg
        |                                 missing                          -> DSX-STA-062
        |
        `-- recommend_association(estimand_kind)  [pure, dataless, called by the gate above]
                    reads dsx.spec.ESTIMAND_KINDS' six-member vocabulary,
                    returns the acceptable coefficient SET per kind

dsx/mathx.py
        |-- EFFECT_SIZE_KINDS = frozenset({"d","h","r"})   [UNCHANGED, D-06]
        |-- interpret_effect(kind, value)                  [UNCHANGED, D-06]
        `-- NEW: report-only convention-band tables + a report-only kind
             registry, consumed by DSX-STA-012's remedy branch in stats.py
             and wired only into templates/APA-TABLE-research.md (ungated)

references/test-selection.md   -- NEW "Association / agreement" section,
                                    the doc mirror of recommend_association,
                                    read by humans, not parsed by any code path

references/finding-codes.md    -- REGENERATED (never hand-edited) via
                                    scripts/gen-finding-catalogue.py --write;
                                    260 -> 265 rows

scripts/gen-finding-catalogue.py -- _D05_ALLOWLIST_CODES gains the five new
                                      codes by exact name (NOT a prefix add —
                                      DSX-STA-* has ~40 uncited legacy codes)
```

### Recommended Project Structure

```
dsx/
├── spec.py                    # ICC_MODELS / ICC_TYPES / ICC_DEFINITIONS,
│                               # KAPPA_WEIGHTS (or equivalent) dicts; optional
│                               # registration in _VOCABULARIES (discretionary)
├── checks/
│   └── stats.py                # recommend_association(); _check_declared_
│                                # association() dispatching to
│                                # _check_correlation_scale_kind() and
│                                # _check_agreement_completeness(); wired at
│                                # BOTH call sites inside check() (lines 162
│                                # and 177, see Code Examples)
├── mathx.py                    # report-only convention-band tables + a
│                                # report-only kind registry (Plan 18-B)
references/
├── test-selection.md          # new "## Association / agreement" section
└── finding-codes.md           # regenerated, 260 -> 265
scripts/
└── gen-finding-catalogue.py   # _D05_ALLOWLIST_CODES += the five new codes
templates/
└── APA-TABLE-research.md      # new convention-band note (Plan 18-B)
examples/
├── good-ANALYSIS-SPEC.yaml    # verified: no edit required to stay silent
└── bad-ANALYSIS-SPEC.yaml     # verified: no edit required to stay silent
tests/
├── test_declared_association_routing.py   # NEW — REQ-P18-01/06
├── test_correlation_scale_kind_gate.py    # NEW — REQ-P18-03
├── test_agreement_completeness_gate.py    # NEW — REQ-P18-04
├── test_finding_catalogue_invariant.py    # EXTENDED — bump 260 -> 265
└── test_effect_size_kind.py               # EXTENDED — report-only-kind cases
```

### Pattern 1: Split the gate body by predicate group so D-05's per-function docstring resolution stays honest

**What:** `scripts/gen-finding-catalogue.py::_resolve_docstrings` maps each
`report.add(...)` call site to the docstring of its NEAREST enclosing
`FunctionDef`, walking upward through a synthesized parent map (there is no
native parent pointer in `ast`). If DSX-STA-050 through DSX-STA-062 all sit in
one function, they all share that one function's docstring for D-05 purposes.

**When to use:** Any time a single gate function is being asked to emit
findings that draw on genuinely different citations (here: a
correlation-coefficient family citation for 050/051, versus Shrout-Fleiss /
McGraw-Wong for 060, a weighting citation for 061, and the two-part
Feinstein-Cicchetti citation for 062).

**Recommended shape (sketch, not yet written):**
```python
# Source: dsx/checks/stats.py (this repository), sketch for this phase.
# Sits beside _check_declared_test, called from check() at both existing
# call sites (see Code Examples below).

CORRELATION_FAMILY = {
    "pearson_correlation", "spearman_correlation", "kendall_tau_b",
    "point_biserial", "phi", "cramers_v",
}

_ASSOCIATION_ROUTES: "dict[str, tuple[frozenset[str], str, str]]" = {
    "linear_association": (frozenset({"pearson_correlation", "point_biserial"}),
                            "fisher_z", "Pearson (Fisher-z CI)"),
    "monotone_association": (frozenset({"spearman_correlation", "kendall_tau_b"}),
                              "rho_or_tau", "Spearman rho / Kendall tau-b"),
    "nominal_association": (frozenset({"phi", "cramers_v"}), "phi_or_v",
                             "phi (2x2) / Cramer's V (r x c)"),
}


def recommend_association(estimand_kind: str) -> dict[str, object]:
    """Dataless string->set lookup — the anti-two-stage proof (REQ-P18-06).

    Takes no data, no n, no distribution flag. Raises ValueError on a kind
    with no association routing (agreement/method_comparison/ordered_trend
    route elsewhere or are out of this function's scope).
    """
    kind = normalize(estimand_kind)
    if kind not in _ASSOCIATION_ROUTES:
        raise ValueError(f"no association routing for estimand_kind {estimand_kind!r}")
    tests, effect_size, citation = _ASSOCIATION_ROUTES[kind]
    return {"tests": tests, "effect_size": effect_size, "citation": citation}


def _check_declared_association(analysis: dict, spec: dict, report: Report) -> None:
    if not analysis:
        return
    _check_correlation_scale_kind(analysis, report)
    _check_agreement_completeness(analysis, report)


def _check_correlation_scale_kind(analysis: dict, report: Report) -> None:
    """DSX-STA-050/051: declared correlation coefficient vs declared scale/kind.

    Citation: Fisher, R.A. (1915) for the Pearson/ordinal mismatch rationale;
    [row-bibliography pass confirms the exact locator before printing, per
    18-CONTEXT.md D-07's "external citation not-in-hand" disposition].
    Structural criterion: declaration-only string comparison against
    ANALYSIS-SPEC.yaml's analysis: block; never reads results.tests or any
    computed statistic.
    """
    declared_test = normalize(analysis.get("test", ""))
    estimand_kind = normalize(analysis.get("estimand_kind", ""))
    operand_scale = normalize(analysis.get("operand_scale", ""))  # see Open Questions

    if declared_test == "pearson_correlation" and operand_scale == "ordinal":
        report.add(
            "DSX-STA-050", "HIGH",
            "Pearson correlation declared against a declared-ordinal operand",
            detail="Pearson assumes linear, interval-or-better scale; an ordinal "
                   "operand with more than two levels calls for a monotone measure.",
            remedy="Redeclare estimand_kind as monotone_association and use "
                   "spearman_correlation or kendall_tau_b.",
            where="spec.analysis.test",
        )
        # D-05: DSX-STA-050

    if declared_test in CORRELATION_FAMILY and estimand_kind in ("agreement", "method_comparison"):
        report.add(
            "DSX-STA-051", "HIGH",
            f"Correlation coefficient '{declared_test}' declared for a "
            f"{estimand_kind} estimand",
            detail="A correlation coefficient measures association, not "
                   "chance-corrected agreement or method bias.",
            remedy="Route to kappa/ICC (agreement) or Bland-Altman (method_comparison).",
            where="spec.analysis.test",
        )
        # D-05: DSX-STA-051


def _check_agreement_completeness(analysis: dict, report: Report) -> None:
    """DSX-STA-060/061/062: agreement declarations, presence + membership only.

    Citation: Shrout, P.E. and Fleiss, J.L. (1979), Psychological Bulletin,
    86(2):420-428; McGraw, K.O. and Wong, S.P. (1996, corrected), Psychological
    Methods, 1(1):30-46 [ICC]; Feinstein, A.R. and Cicchetti, D.V. (1990) /
    Cicchetti, D.V. and Feinstein, A.R. (1990), J. Clin. Epidemiol. 43(6),
    Parts I (543-549) and II (551-558) [kappa companions].
    Structural criterion: presence + closed-vocabulary membership over
    declared sub-fields; never a coherence or numeric-agreement judgment.
    """
    icc = analysis.get("icc") if isinstance(analysis.get("icc"), dict) else None
    if icc is not None or normalize(analysis.get("test", "")) == "icc":
        icc = icc or {}
        for field_name, vocab in (("model", ICC_MODELS), ("type", ICC_TYPES),
                                   ("definition", ICC_DEFINITIONS)):
            value = icc.get(field_name)
            if is_blank(value) or normalize(value) not in vocab:
                report.add(
                    "DSX-STA-060", "HIGH",
                    f"ICC declared without a complete (model, type, definition) triple",
                    detail=f"Missing or unrecognised: analysis.icc.{field_name}",
                    remedy="Declare all three: model, type and definition.",
                    where=f"spec.analysis.icc.{field_name}",
                )
                # D-05: DSX-STA-060
                break

    if normalize(analysis.get("test", "")) == "weighted_kappa":
        weights = analysis.get("weights")
        ok = isinstance(weights, str) and normalize(weights) in ("linear", "quadratic")
        ok = ok or isinstance(weights, (list, tuple)) and len(weights) > 0
        if not ok:
            report.add(
                "DSX-STA-061", "HIGH",
                "Weighted kappa declared without declared weights",
                remedy="Declare weights as 'linear', 'quadratic', or an explicit matrix.",
                where="spec.analysis.weights",
            )
            # D-05: DSX-STA-061

    if normalize(analysis.get("test", "")) in ("cohens_kappa", "weighted_kappa", "fleiss_kappa"):
        if is_blank(analysis.get("p_pos")) or is_blank(analysis.get("p_neg")):
            report.add(
                "DSX-STA-062", "HIGH",
                "Kappa declared without its p_pos/p_neg companions",
                detail="Feinstein-Cicchetti 1990 Part I documents two paradoxes an "
                       "omnibus kappa can hide; Part II recommends reporting "
                       "p_pos and p_neg alongside it.",
                remedy="Declare analysis.p_pos and analysis.p_neg.",
                where="spec.analysis",
            )
            # D-05: DSX-STA-062
```
This sketch is illustrative, not final — field names (`analysis.icc.*`,
`analysis.weights`, `analysis.p_pos`/`p_neg`, `analysis.operand_scale`) are
this session's recommendation, not a committed contract. See Open Questions.

### Pattern 2: Wire the new gate at BOTH of `check()`'s existing `_check_declared_test` call sites

**What:** `[VERIFIED: live tree]` `dsx/checks/stats.py::check()` calls
`_check_declared_test(analysis, spec, report)` from two different places
depending on whether `results.tests` is populated:

```python
# Source: dsx/checks/stats.py:151-178 — CURRENT state, confirmed by direct read.
def check(spec: dict) -> Report:
    report = Report(check="stats")
    ...
    if not tests:
        analysis = section(spec, "analysis")
        if analysis:
            _check_declared_test(analysis, spec, report)   # <- call site 1, line 162
        return report

    ... # loop over tests, accumulate pvalues
    _check_correction_applied(spec, pvalues, alpha, report)
    _check_declared_test(section(spec, "analysis"), spec, report)  # <- call site 2, line 177
    return report
```

**How to use:** `_check_declared_association(analysis, spec, report)` must be
added immediately beside `_check_declared_test` at BOTH call sites (lines 162
and 177), not just one — a spec with no `results.tests` block (the
`not tests` early-return branch) is exactly the shape a pure declaration-only
correlation/agreement spec will usually have (no computed p-values to report
yet), so call site 1 is not an edge case to skip.

### Anti-Patterns to Avoid

- **Widening `EFFECT_SIZE_KINDS` to admit kappa/ICC/Kendall's W/phi/Cramer's
  V/tau-b/rho.** This is D-06's explicit prohibition. `interpret_effect` uses a
  flat `abs(value)` band; Cramer's V thresholds are df-dependent (Cohen's
  0.1/0.3/0.5 hold only at df=1) and phi/W are unsigned with a different null —
  a single flat band would be statistically wrong for these kinds, independent
  of the "conventions never block" doctrine.
- **Adding `"DSX-STA-"` to `_D05_ALLOWLIST_PREFIXES`.** `[VERIFIED: live tree]`
  confirmed at `scripts/gen-finding-catalogue.py:87-89` — this family has ~40
  legacy codes with no `Citation:`/`Structural criterion:` docstring line and
  no `# D-05:` test marker; a prefix add fails the build red on every one of
  them. Use the exact-code path (`_D05_ALLOWLIST_CODES`) instead, exactly as
  `DSX-EXP-070`/`DSX-MET-021`/`DSX-COH-040` already do for the same reason.
- **Hand-editing `references/finding-codes.md`.** The file's own header says
  "Do not edit by hand." Run `python3 scripts/gen-finding-catalogue.py --write`
  after the code lands and commit the regenerated file in the same commit as
  the `report.add` calls (D-08's own instruction).
- **Conflating `_EXPECTED_TOTAL` and `_SNAPSHOT_TOTAL` in `tests/test_finding_
  catalogue_invariant.py`.** `[VERIFIED: live tree]` at lines 35 and 41: only
  `_EXPECTED_TOTAL` (260 -> 265) and `_MINTED_CODES` (add the five new codes)
  change. `_SNAPSHOT_TOTAL` (256) and `tests/fixtures/finding-codes-phase12.md`
  are byte-frozen and NEVER mutated — this exact trap is even named in the
  test file's own comment ("D-08 trap #3").
- **Using pure-string `normalize(...) not in vocab` membership for the
  weighted-kappa `weights` field.** Unlike every other closed-vocabulary check
  in this codebase, `weights` may legitimately be an explicit matrix (a
  list/nested structure), not a string — `normalize()` calls `str(value)` on
  its input, which would silently stringify a matrix into meaningless text
  rather than validating it. This field needs an explicit type branch (see
  Pitfall 5), a deliberate, documented deviation from the house idiom, not an
  oversight.
- **Editing `examples/good-ANALYSIS-SPEC.yaml` or `examples/bad-ANALYSIS-SPEC.
  yaml` reflexively because D-08 says "extend, not replace."** Verified this
  session: neither file's current `analysis:` block trips any of the five new
  predicates. Extend them only if the planner wants an illustrative
  correlation/agreement row; do not treat an edit as mandatory.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Detecting whether the catalogue gained/lost a code | A new bespoke diff | `scripts/gen-finding-catalogue.py --check` + `tests/test_finding_catalogue_invariant.py`'s existing set-identity test, EXTENDED with the five new codes | Already exists, already wired into the phase-gate sequence, already does set-identity (not just count) comparison |
| Enforcing that a new finding code carries a citation | A new review checklist item | `scripts/gen-finding-catalogue.py`'s `check_d05()` + the `_D05_ALLOWLIST_CODES` mechanism | Already exists as a build-time gate; the only missing step is naming the five new codes in the allowlist |
| A "no autoswitch" structural proof for the new category | A prose review note | `inspect.signature(recommend_association)` structural assertion, modelled on `tests/test_time_to_event_fallthrough.py`'s `inspect.getsource` scan | The dataless signature IS the proof; a test that inspects the live signature (not a docstring claim) cannot silently rot |
| A convention-vs-threshold distinction for effect-size bands | A comment saying "this is just a convention" | A separate report-only registry + a labeling function distinct from `interpret_effect`, never fed into DSX-STA-011 | Discipline alone (a comment) does not survive a future contributor adding a branch; the structural separation D-06 mandates does |

**Key insight:** every mechanism this phase needs (membership-guard idiom,
code-dedup, D-05 citation enforcement, catalogue set-identity, doc/code
lockstep-by-test) already exists in this codebase. The work is composition
plus three genuinely new field-shape decisions (Open Questions below) — not
invention of new machinery.

## Common Pitfalls

### Pitfall 1: The untouched `_check_declared_test` can fire a false DSX-STA-041 against a new gate-test fixture
**What goes wrong:** `_check_declared_test` runs unconditionally whenever both
`analysis.test` and `analysis.outcome_type` are declared and non-blank
(`[VERIFIED: live tree]` `dsx/checks/stats.py:473-476`), and it has no
awareness of `estimand_kind`. A hand-written gate-test fixture that declares
`analysis: {outcome_type: continuous, estimand_kind: linear_association, test:
pearson_correlation}` to exercise the NEW correlation gate will ALSO trip the
OLD gate: `recommend_test("continuous", 2, ...)` derives something like
`welch_t`/`mann_whitney`, `pearson_correlation` is not in that recommendation's
acceptable set, and `_check_declared_test` fires an unrelated DSX-STA-041.
**Why it happens:** `recommend_test`/`_check_declared_test` and
`recommend_association`/`_check_declared_association` are deliberately
independent (D-01's "hybrid, not fold-in"), so nothing suppresses one when the
other is the intended target of a test.
**How to avoid:** new gate unit tests for DSX-STA-050/051/060/061/062 should
either (a) omit `analysis.outcome_type` entirely in their fixture dict (the
early-return in `_check_declared_test` then skips the test-recommendation
comparison, though the membership loop for `estimand_kind` still runs — this
is fine and intended), or (b) call `_check_declared_association` directly as a
unit rather than routing through the full `stats.check(spec)` entry point, or
(c) if going through `stats.check(spec)` end-to-end, choose an
`outcome_type`/`n_groups`/`test` combination that `recommend_test` would
actually accept alongside the correlation declaration. Whichever the planner
picks, name it explicitly in the test's docstring so a future reader does not
mistake the omission/choice for an oversight.
**Warning signs:** a new gate test asserts `DSX-STA-050 in codes` but the
assertion also silently allows `DSX-STA-041` to appear in the same findings
list without the test noticing — check `codes` exhaustively, not just
membership of the code under test.

### Pitfall 2: D-05's docstring resolution is per enclosing function, not per code — see Pattern 1 above for the recommended split
Restated here as a pitfall because it is easy to miss: a single
`_check_declared_association` monolith emitting all five codes would still
pass `check_d05()` with one shared, generic docstring — the build stays green
while the actual per-code citation obligation (Shrout-Fleiss for 060 is not
the same citation as Feinstein-Cicchetti for 062) goes unmet in substance even
though the mechanical gate is satisfied. Split by predicate group.

### Pitfall 3: The five new codes are silently uncovered by the D-05 build gate unless named in `_D05_ALLOWLIST_CODES`
**What goes wrong:** `[VERIFIED: live tree]` `scripts/gen-finding-catalogue.py:
87-89` (`_D05_ALLOWLIST_PREFIXES`) does not include `"DSX-STA-"`. Unless the
five new codes are added by exact name to `_D05_ALLOWLIST_CODES` (lines
156-165), `check_d05()` never inspects them — `--check` passes even if the new
`report.add` call sites carry no `Citation:` line and no `# D-05: <CODE>` test
marker, silently defeating REQ-P18-03/04's own citation requirement.
**Why it happens:** `DSX-STA-*` is a pre-existing family with ~40 legacy codes
that carry no citation; the allowlist is deliberately scoped to avoid dragging
those in.
**How to avoid:** add all five codes — `DSX-STA-050`, `DSX-STA-051`,
`DSX-STA-060`, `DSX-STA-061`, `DSX-STA-062` — to `_D05_ALLOWLIST_CODES`, with a
dated comment following the file's own precedent style (see the `DSX-EXP-070`/
`DSX-MET-021`/`DSX-COH-040` comment blocks immediately above the set literal).
**Warning signs:** `scripts/gen-finding-catalogue.py --check` exits 0 even
though a new `report.add("DSX-STA-050", ...)` call site has no `Citation:`
docstring line — this is the silent-pass signature of a missing allowlist
entry, not proof the citation requirement is met.

### Pitfall 4: `_EXPECTED_TOTAL`/`_MINTED_CODES`/`_SNAPSHOT_TOTAL` triple in the invariant test
**What goes wrong:** bumping only `_EXPECTED_TOTAL` to 265 without adding the
five codes to `_MINTED_CODES` (or vice versa) makes the set-identity test fail
even though the count test might pass, or leaves a cardinality-preserving swap
undetected.
**Why it happens:** `[VERIFIED: live tree]` the two tests
(`test_finding_catalogue_stays_at_260_codes` and
`test_code_set_is_phase12_snapshot_plus_the_phase15_and_phase16_mints`) are
deliberately independent checks over the same file — the count alone cannot
catch a mint-one/drop-one swap.
**How to avoid:** update all three together: `_EXPECTED_TOTAL = 265`,
`_MINTED_CODES` gains the five Phase-18 codes (union with the existing four),
`_SNAPSHOT_TOTAL` and `tests/fixtures/finding-codes-phase12.md` stay
byte-frozen at 256, unchanged.
**Warning signs:** `test_code_set_is_phase12_snapshot_plus_the_phase15_and_
phase16_mints` fails with a non-empty `added=` or `removed=` list in its
assertion message — read that list, it names exactly what drifted.

### Pitfall 5: The weighted-kappa `weights` field cannot use the pure-string membership idiom
**What goes wrong:** every existing closed-vocabulary guard in this codebase
(`_MEMBERSHIP_FIELDS`, `_VALIDITY_FRAME_MEMBERSHIP`, `_INFERENCE_MEMBERSHIP`)
assumes the declared value is a scalar string and calls
`normalize(value) not in vocab`. D-02's own predicate for DSX-STA-061 admits
THREE shapes: `"linear"`, `"quadratic"`, or "explicit matrix" — the third is
structurally a list/nested sequence, not a string. Calling `normalize()` on a
list stringifies it (`str([[1,0],[0,1]])`) into something that will never
match any vocabulary member, but also never crash — a silent false-positive
061 firing on a perfectly valid explicit-matrix declaration.
**Why it happens:** the house idiom was designed for closed enum fields; this
is the phase's first field whose valid values span both an enum AND a
structural type.
**How to avoid:** branch on `isinstance` before normalizing: a string is
checked against `{"linear", "quadratic"}`; a non-empty list/tuple/nested
sequence is accepted as a declared explicit matrix without further validation
(this phase does not audit matrix VALIDITY, only presence); anything else
(blank, a bare number, a dict) fires DSX-STA-061.
**Warning signs:** a fixture declaring `weights: [[1, 0.5], [0.5, 1]]` fires
DSX-STA-061 when it should not — the tell-tale sign the guard used
`normalize()` on a non-string value.

### Pitfall 6: D-06's "DSX-STA-012's remedy text branches" language is ambiguous about whether 012 still fires for report-only kinds
**What goes wrong:** read literally, "recognised... no nonsensical nag" implies
DSX-STA-012 should NOT fire at all for a report-only kind (e.g.
`effect_size_kind: kappa`); but "remedy text branches" implies the finding
still fires, just with different wording. Implementing the wrong one either
reintroduces the nag D-06 explicitly forbids, or silently drops test coverage
Plan 18-B's own validation list expects.
**Why it happens:** 18-CONTEXT.md's D-06 prose describes the OUTCOME (no nag,
never banded) without pinning the exact control-flow shape.
**How to avoid — this session's recommendation:** extend the membership test
that gates DSX-STA-012 to `kind not in EFFECT_SIZE_KINDS and kind not in
REPORT_ONLY_EFFECT_KINDS` before firing; when `kind` IS in the report-only
registry, call `report.ok(...)` with a message naming the convention (e.g.
"'{label}' declares effect_size_kind={kind}; magnitude is a labeled
convention, not a gated band") instead of `report.add("DSX-STA-012", ...)`.
DSX-STA-012 then fires ONLY for a kind in neither set — genuinely unrecognised.
This is a recommendation, not a locked decision; the planner should confirm
this reading matches the persona round's intent before implementing, since it
changes DSX-STA-012's control flow, not just its text.
**Warning signs:** a test asserting `effect_size_kind: kappa` produces ZERO
DSX-STA-011/012 findings AND a `report.ok(...)` entry mentioning "convention"
— if the planner instead keeps 012 firing (at MEDIUM, say) with only the
remedy text changed, that is a different, equally defensible reading; either
way, write the test first (TDD, `tdd_mode: true` in config) so the behavior is
pinned before the ambiguity can drift.

### Pitfall 7: `dsx/checks/stats.py`'s `PARAMETRIC_TESTS`/`NONPARAMETRIC_TESTS` sets are orthogonal to the new gate and do not need touching
**What goes wrong:** a contributor might reflexively add `kendall_tau_b`,
`point_biserial`, `phi`, `cramers_v` to `PARAMETRIC_TESTS`/
`NONPARAMETRIC_TESTS` "for completeness."
**Why it happens:** `pearson_correlation` and `spearman_correlation` are
already members (`[VERIFIED: live tree]` lines 30-38), so it looks like an
oversight that the others are absent.
**How to avoid:** these two sets exist ONLY to gate DSX-STA-042/043
(parametric-assumption-unassessed / independence-violated checks inside
`_check_declared_test`), a mechanism entirely orthogonal to the new
association gate. Adding the new coefficient names to either set would make a
correlation declaration trip DSX-STA-042 ("unassessed normality_ok/equal_
variance/independence_ok") — assumptions that do not obviously apply the same
way to a rank correlation. Leave both sets unchanged unless the planner makes
an explicit, separately-justified decision to extend them; note the decision
either way so it is not mistaken for an oversight later.

## Code Examples

### The exact two `_check_declared_test` call sites (verified this session, `dsx/checks/stats.py`)
```python
# Source: dsx/checks/stats.py:159-178 — CURRENT state, confirmed by direct read.
if not tests:
    analysis = section(spec, "analysis")
    if analysis:
        _check_declared_test(analysis, spec, report)
    return report

pvalues: list[float] = []
for index, test in enumerate(tests):
    ...
_check_correction_applied(spec, pvalues, alpha, report)
_check_declared_test(section(spec, "analysis"), spec, report)
return report
```
`_check_declared_association(analysis, spec, report)` must be added at both
`_check_declared_test(...)` call sites above.

### The exact `estimand_kind`/`ESTIMAND_KINDS` state the new gate reads (verified this session, `dsx/spec.py`)
```python
# Source: dsx/spec.py:398-423 — CURRENT state, confirmed by direct read.
ESTIMAND_KINDS = {
    "linear_association": (
        "Signed, slope-like linear dependence - Pearson r, including point-biserial "
        "(Pearson r on {0,1}-coded vs continuous data). Routes Pearson and point-biserial."
    ),
    "monotone_association": (
        "Signed, rank-monotone dependence with no linearity assumption. "
        "Routes Spearman's rho and Kendall's tau-b."
    ),
    "nominal_association": (
        "Unsigned, chi-square-based departure from independence on an unordered r x c "
        "table - no slope and no direction. Routes phi (2x2) and Cramer's V (r x c)."
    ),
    "agreement": (
        "Dimensionless, chance-corrected agreement between raters or methods. Routes "
        "Cohen's / weighted / Fleiss' kappa, Krippendorff's alpha, and the ICC."
    ),
    "method_comparison": (
        "Bias plus limits of agreement between two measurement methods, in the "
        "measurement units. Routes Bland-Altman."
    ),
    "ordered_trend": (
        "A monotone trend across an ordered factor or dose. Routes Cochran-Armitage, "
        "Jonckheere-Terpstra, and Mann-Kendall with Sen's slope."
    ),
}
```
This dict's own descriptions already name which coefficients each kind
routes to — confirming D-01's acceptable-set mapping is not a new invention,
it is making explicit what Phase 17's docstrings already asserted in prose.

### The exact `EFFECT_SIZE_KINDS`/`interpret_effect` state Plan 18-B must not widen (verified this session, `dsx/mathx.py`)
```python
# Source: dsx/mathx.py:292-319 — CURRENT state, confirmed by direct read.
EFFECT_SIZE_KINDS = frozenset({"d", "h", "r"})

def interpret_effect(kind: str, value: float) -> str:
    v = abs(value)
    table = {
        "d": ((0.2, "negligible"), (0.5, "small"), (0.8, "medium")),
        "h": ((0.2, "negligible"), (0.5, "small"), (0.8, "medium")),
        "r": ((0.1, "negligible"), (0.3, "small"), (0.5, "medium")),
    }
    if kind not in EFFECT_SIZE_KINDS:
        raise ValueError(f"unknown effect kind {kind!r}; expected one of {sorted(EFFECT_SIZE_KINDS)}")
    bands = table[kind]
    for threshold, label in bands:
        if v < threshold:
            return label
    return "large"
```
Plan 18-B adds a SEPARATE registry and a SEPARATE labeling function (e.g.
`REPORT_ONLY_EFFECT_KINDS = frozenset({"kappa", "icc", "kendalls_w", "phi",
"cramers_v", "tau_b", "rho"})` and `label_convention_band(kind, value) -> str`)
— never adding to `EFFECT_SIZE_KINDS` or branching inside `interpret_effect`.

### The exact DSX-STA-011/012 site Plan 18-B's remedy branch must extend (verified this session, `dsx/checks/stats.py`)
```python
# Source: dsx/checks/stats.py:297-326 — CURRENT state, confirmed by direct read.
if p < alpha and standardized is not None:
    kind = normalize(test.get("effect_size_kind", "d"))
    if kind in EFFECT_SIZE_KINDS:
        magnitude = interpret_effect(kind, standardized)
        if magnitude == "negligible":
            report.add("DSX-STA-011", "MEDIUM", ...)
    else:
        report.add("DSX-STA-012", "MEDIUM", ...)
```
Recommended extension (Pitfall 6): change the `else` branch's condition to
also exclude `REPORT_ONLY_EFFECT_KINDS`, and add a third branch calling
`report.ok(...)` for the report-only case.

### D-05 citation-allowlist precedent to follow exactly (verified this session, `scripts/gen-finding-catalogue.py`)
```python
# Source: scripts/gen-finding-catalogue.py:147-165 — CURRENT state, confirmed by direct read.
# Phase 15 (REQ-P15-02, REQ-P15-04) adds DSX-EXP-070 and DSX-MET-021 here, by
# exact code and NOT via _D05_ALLOWLIST_PREFIXES: each lives inside a
# pre-existing family (DSX-EXP-*, DSX-MET-*) whose legacy siblings carry no
# Citation:/Structural criterion: docstring line and no # D-05: marker...
_D05_ALLOWLIST_CODES = frozenset(
    {
        "DSX-SPEC-080", "DSX-SPEC-081", "DSX-SPEC-082", "DSX-SPEC-085", "DSX-SPEC-086",
        "DSX-CODE-020", "DSX-CODE-021", "DSX-CODE-030", "DSX-CODE-031",
        "DSX-ML-023", "DSX-ML-024", "DSX-ML-043", "DSX-ML-052", "DSX-ML-053",
        "DSX-ML-090", "DSX-ML-091", "DSX-ML-092",
        "DSX-COH-040",
        "DSX-EXP-070", "DSX-MET-021",
        # Phase 18 (REQ-P18-03/04) adds the five correlation/agreement codes here,
        # for the same reason: DSX-STA-* is a pre-existing family (v1.0.0) with
        # ~40 legacy codes carrying no citation; a prefix add would fail the
        # build on all of them.
        "DSX-STA-050", "DSX-STA-051", "DSX-STA-060", "DSX-STA-061", "DSX-STA-062",
    }
)
```

### The exact invariant-test locators to bump (verified this session, `tests/test_finding_catalogue_invariant.py`)
```python
# Source: tests/test_finding_catalogue_invariant.py:34-42 — CURRENT state.
_EXPECTED_TOTAL = 260   # -> 265
_SNAPSHOT_TOTAL = 256   # UNCHANGED — never mutate the byte-frozen snapshot
_MINTED_CODES = {"DSX-REP-060", "DSX-REP-061", "DSX-EXP-070", "DSX-MET-021"}
# -> add "DSX-STA-050", "DSX-STA-051", "DSX-STA-060", "DSX-STA-061", "DSX-STA-062"
```

### The no-autoswitch structural proof for REQ-P18-06 (sketch, modelled on Phase 17's fallthrough test)
```python
# Sketch — tests/test_declared_association_routing.py
import inspect
import unittest
from dsx.checks import stats

class RecommendAssociationSignatureTest(unittest.TestCase):
    def test_recommend_association_is_dataless(self):  # REQ-P18-06
        sig = inspect.signature(stats.recommend_association)
        self.assertEqual(
            list(sig.parameters), ["estimand_kind"],
            "recommend_association must take no n, no data, no distribution "
            "flag — its dataless signature is the anti-two-stage proof",
        )

    def test_linear_association_routes_to_pearson_and_point_biserial(self):
        rec = stats.recommend_association("linear_association")
        self.assertEqual(set(rec["tests"]), {"pearson_correlation", "point_biserial"})

    def test_monotone_association_routes_to_spearman_and_kendall(self):
        rec = stats.recommend_association("monotone_association")
        self.assertEqual(set(rec["tests"]), {"spearman_correlation", "kendall_tau_b"})

    def test_nominal_association_routes_to_phi_and_cramers_v(self):
        rec = stats.recommend_association("nominal_association")
        self.assertEqual(set(rec["tests"]), {"phi", "cramers_v"})

    def test_agreement_kind_has_no_association_route(self):
        with self.assertRaises(ValueError):
            stats.recommend_association("agreement")
```

## State of the Art

Not applicable — this phase extends an internal declaration-only contract; the
statistical definitions themselves (Pearson/Spearman/Kendall/kappa/ICC/
Krippendorff/Bland-Altman) are decades-old and stable. No external ecosystem
version to track. The one genuinely current-state item is the McGraw & Wong
1996 ICC paper's own ERRATUM (noted in 18-CONTEXT.md D-05 and the HQ-16 read):
any pinned ICC formula reference must be checked against the CORRECTED
edition, not the original — this affects citation text only, not the
completeness gate itself (which is formula-independent).

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `analysis.operand_scale` (new field, vocab `{continuous, ordinal, dichotomous, nominal}`) is the correct field-shape recommendation for D-03's "declared operand scale" | Open Questions OQ-1 | Medium — confirmed no existing field serves this purpose (exhaustive grep for scale/ordinal/operand/measurement across all `.yaml` fixtures and `dsx/`), but the exact name/vocab is this session's design proposal, not a committed contract; if the planner picks a different name the sketch code above needs renaming only, not re-architecting |
| A2 | Nested blocks `analysis.icc: {model, type, definition}` and flat `analysis.weights`/`analysis.p_pos`/`analysis.p_neg` (rather than, e.g., a nested `analysis.kappa: {...}` block) are the recommended field shapes for D-05's ICC triple and D-02's kappa companions | Open Questions OQ-2/OQ-3 | Medium — `design.cuped: {covariate, covariate_timing, covariate_source}` is a real precedent for a nested sub-block under a top-level section, supporting the ICC nesting choice; the kappa fields are recommended flat only because `weights` must already carry a non-string (matrix) type and nesting adds no membership-guard benefit there — reasonable but not the only defensible shape |
| A3 | Splitting `_check_declared_association` into `_check_correlation_scale_kind` + `_check_agreement_completeness` (two functions, two docstrings) rather than one monolith is required to make `check_d05()`'s docstring-per-function resolution attribute the right citation to the right code | Architecture Patterns Pattern 1, Pitfall 2 | Low if wrong on style (the build gate still passes with one shared docstring covering all five codes' citations) but Medium on substance — a shared generic docstring makes it easy to under-cite one of the five distinct citation obligations without the build noticing |
| A4 | DSX-STA-012 should STOP firing (replaced by a `report.ok(...)`) for a report-only effect-size kind, rather than continuing to fire with only its remedy text changed | Pitfall 6 | Medium — both readings satisfy D-06's prose taken loosely; picking wrong changes the 011/012 test extension's expected assertions and possibly the finding-codes.md row text (a MEDIUM-severity "unrecognised kind" firing on a legitimately-declared convention kind would itself be the "nonsensical nag" D-06 forbids, which is why this session recommends the report.ok reading) |

## Open Questions

1. **What is the exact declared-field shape for D-03's "operand scale" the
   DSX-STA-050 whitelist reads?**
   - What we know: `[VERIFIED: live tree]` no field resembling a declared
     measurement scale for a correlation operand exists anywhere in
     `ANALYSIS-SPEC.yaml`, `templates/ANALYSIS-SPEC.yaml`, or any file under
     `examples/` (exhaustive grep this session for `scale`/`ordinal`/
     `operand`/`measurement` across every `.yaml` in the repo — the only
     hits are `validity_frame.measurement` (a free-text construct/
     operationalisation block, unrelated) and unrelated files). D-03 itself
     says "the exact field shape is a plan-time binding for S2-2" — this is
     explicitly NOT decided anywhere yet.
   - What's unclear: whether a single new field is sufficient (this session's
     recommendation) or whether the two-operand nature of a correlation
     (both variables could independently be ordinal/continuous/dichotomous)
     eventually needs two fields.
   - Recommendation: add `analysis.operand_scale` with a closed vocabulary
     `{"continuous", "ordinal", "dichotomous", "nominal"}`, registered in the
     existing `_MEMBERSHIP_FIELDS` loop (reusing DSX-STA-040 for vocabulary
     recognition, zero new code for that half) so a mis-slotted value is
     loud by the same mechanism `outcome_type`/`estimand_kind` already use;
     DSX-STA-050 then reads this field's value directly. The `"ordinal"` vs
     `"dichotomous"` split is deliberately what encodes D-03's ">2 levels"
     requirement, so no separate level-count field is needed. **This is a
     planner decision, not resolved by 18-CONTEXT.md — confirm before
     writing PLAN.md's task list.** — **UPDATE (S2-2): RESOLVED in 18-A-PLAN.md** — the planner adopted `analysis.operand_scale` with vocab `{continuous, ordinal, dichotomous, nominal}`, registered in `_MEMBERSHIP_FIELDS` (DSX-STA-040 reuse); the ordinal-vs-dichotomous split encodes D-03's ">2 levels" whitelist (18-A objective + Tasks 1/2).

2. **What is the exact declared-field shape for the ICC (model, type,
   definition) triple?**
   - What we know: D-05 names the three sub-fields and their closed vocab
     members but not their nesting/parent-field name.
   - What's unclear: whether they nest under a new `analysis.icc: {...}`
     block (mirroring `design.cuped`'s existing nested-block precedent) or
     live as three flat fields (`analysis.icc_model`, `analysis.icc_type`,
     `analysis.icc_definition`).
   - Recommendation: nest under `analysis.icc: {model, type, definition}` —
     matches the one existing precedent for a multi-field declared unit
     living under a top-level section (`design.cuped`), and gives
     DSX-STA-060 a clean, single presence check ("is `analysis.icc` a
     non-blank dict, or is `analysis.test == 'icc'`?") before it walks the
     three sub-fields. **RESOLVED in 18-A-PLAN.md** — `analysis.icc: {model, type, definition}` nesting adopted (18-A objective, OQ-2 resolution).

3. **What is the exact declared-field shape for `weights`, `p_pos`, `p_neg`?**
   - What we know: D-02/D-04 name these as declared fields on the kappa
     declaration; not otherwise specified.
   - What's unclear: whether they nest under an `analysis.kappa: {...}`
     block (parallel to the ICC recommendation above) or live flat on
     `analysis:` directly.
   - Recommendation: flat (`analysis.weights`, `analysis.p_pos`,
     `analysis.p_neg`) — unlike the ICC triple, these three fields don't
     always co-occur (weights only applies to `weighted_kappa`; p_pos/p_neg
     applies to the whole kappa family), so a shared parent block buys no
     completeness-check simplification the way `analysis.icc` does, and flat
     fields keep `analysis.weights`'s heterogeneous string-or-matrix type
     (Pitfall 5) from needing an extra nesting level. **RESOLVED in 18-A-PLAN.md** — flat `analysis.weights` / `analysis.p_pos` / `analysis.p_neg` adopted (18-A objective, OQ-3 resolution).

4. **HQ-20 (veto window, non-blocking) — RESOLVED per 18-CONTEXT.md as a
   silence-accepts item.** The D-02 code numbering (050/051/060/061/062) and
   the D-04 requirement-parenthetical alignment are both already recorded as
   accepted absent an objection; no action needed unless HQ-20 resolves
   otherwise before execute.

5. **Coefficient-typo guard — RESOLVED (deferred) per 18-CONTEXT.md.** Not
   built this phase; named as a candidate for the 130s reserve. No planner
   action beyond not accidentally scope-creeping into it.

6. **ICC combination-coherence — RESOLVED (deferred, D-13-conditioned) per
   18-CONTEXT.md D-05.** Candidate `DSX-STA-063`; enters only when a fixture
   demonstrates a complete-but-incoherent triple passing DSX-STA-060. No
   planner action this phase beyond not building it prematurely.

7. **D-05 not-in-hand items (ICC/Koo-Li band values, Kendall's W bands, the
   P18-03 doctrinal scale citation) — RESOLVED (catalog-only / not-in-hand)
   per 18-CONTEXT.md D-07.** These ship as named, presence-only rows with no
   numeric fixture and no invented locator. Validated by presence-in-doc
   assertions only (see Validation Architecture below), never a numeric
   assertion.

8. **Should `dsx recommend-association` exist as a CLI subcommand mirroring
   `dsx recommend-test`? — Not resolved by 18-CONTEXT.md, not required by any
   REQ-P18 item.** `[VERIFIED: live tree]` `dsx/cli.py:1032-1047` shows the
   `recommend-test` subcommand pattern (`cmd_recommend`, `p_rec.set_defaults
   (func=cmd_recommend)`). Recommendation: defer — REQ-P18-06's no-autoswitch
   proof is satisfied by the function's signature directly (tested via
   `inspect.signature`), not via CLI exposure; adding a CLI command is a
   nice-to-have consistency improvement, not a phase requirement. **Planner's
   discretion, non-blocking either way.**

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3 | Everything | Yes | 3.14.6 `[VERIFIED: live tree]` | — |
| `unittest` (stdlib) | Test execution | Yes | stdlib, ships with Python | — |
| `pytest` | Not used by this project | No | — | N/A — project uses stdlib `unittest` exclusively |
| `scripts/gen-finding-catalogue.py` | Catalogue regen + D-05 build gate | Yes, ran this session (`--check` passes at 260, pre-Phase-18 baseline) | — | — |

No missing dependencies block this phase.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Python stdlib `unittest` |
| Config file | none — discovered via `unittest discover -s tests` |
| Quick run command | `python3 -m unittest tests.<module_name> -v` |
| Full suite command | `python3 -m unittest discover -s tests -q` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| REQ-P18-01 | `recommend_association(kind)` returns the correct acceptable-coefficient SET per kind; catalog-only rows (dCor, partial correlation) named in `test-selection.md` | unit + doc-presence | `python3 -m unittest tests.test_declared_association_routing -v` | Wave 0 — new file |
| REQ-P18-02 | Agreement/reliability rows present in `test-selection.md`; catalog-only rows (Cronbach->omega) named with deprecation citation | doc-presence | a small assertion reading `references/test-selection.md` for the new section headers/row text (can live in the same new test file) | Wave 0 — new assertions |
| REQ-P18-03 | DSX-STA-050 fires on `pearson_correlation` + declared-ordinal (>2 levels); does NOT fire on `point_biserial` or a declared-dichotomous operand; DSX-STA-051 fires on any correlation-family test declared against `agreement`/`method_comparison` | unit | `python3 -m unittest tests.test_correlation_scale_kind_gate -v` | Wave 0 — new file |
| REQ-P18-04 | DSX-STA-060 fires on missing/out-of-vocab ICC sub-field, silent on a complete valid triple; DSX-STA-061 fires on missing/unrecognised `weights` for `weighted_kappa`, accepts an explicit matrix; DSX-STA-062 fires when either `p_pos` or `p_neg` is missing for any kappa-family test | unit | `python3 -m unittest tests.test_agreement_completeness_gate -v` | Wave 0 — new file |
| REQ-P18-05 (pinned: Krippendorff alpha, Landis-Koch kappa bands) | `mathx`'s report-only Krippendorff reference value = 0.7598 at `level=ordinal`; Landis-Koch band boundaries match the cited paper's published thresholds | unit, numeric fixture assertion | extend `tests/test_effect_size_kind.py` or a new `tests/test_agreement_convention_bands.py` | Wave 0 — new assertions |
| REQ-P18-05 (catalog-only: ICC/Koo-Li bands, Kendall's W bands, dCor, partial, Cronbach->omega) | Each is present as a named, cited pointer row in `test-selection.md` and/or `templates/APA-TABLE-research.md`, with NO numeric boundary asserted | doc-presence only | `self.assertIn("Kendall's W", text)`-style substring assertions, never a numeric equality assertion | Wave 0 — new assertions |
| REQ-P18-05 (report-only kind recognition) | `effect_size_kind: kappa` (or any report-only kind) on a significant result fires neither DSX-STA-011 nor DSX-STA-012; a `report.ok(...)` entry names the convention (Pitfall 6) | unit | extend `tests/test_effect_size_kind.py` | Wave 0 — new assertions in existing file |
| REQ-P18-06 | `recommend_association`'s signature carries exactly one parameter (`estimand_kind`), no data/n/distribution flag | unit, structural (`inspect.signature`) | `python3 -m unittest tests.test_declared_association_routing -v` | Wave 0 — same new file as REQ-P18-01 |
| Catalogue mint proof (all REQ-P18-03/04) | Live catalogue = frozen Phase-12 snapshot plus the four pre-existing mints plus exactly the five new Phase-18 codes; declared total = 265 | unit | `python3 -m unittest tests.test_finding_catalogue_invariant -v` | Extended — pre-existing file, bump pinned numbers |
| D-05 citation build gate (all five codes) | Each of the five codes has a `Citation:` line, a `Reference value:`/`Structural criterion:` line, and a `# D-05: <CODE>` test marker under `tests/` | build script | `python3 scripts/gen-finding-catalogue.py --check` | Extended — `_D05_ALLOWLIST_CODES` addition required (Pitfall 3) |
| D-08 fixture silence (both canonical fixtures) | `examples/good-ANALYSIS-SPEC.yaml` and `examples/bad-ANALYSIS-SPEC.yaml` fire none of the five new codes | integration | `dsx audit --spec examples/good-ANALYSIS-SPEC.yaml --verbose` / same for bad; or re-run `tests/test_good_fixture_phase15.py` and `tests/test_known_bad_corpus.py` | Pre-existing — verify unchanged after Phase 18 lands |

### Sampling Rate
- **Per task commit:** the single new test module the task touched (e.g.
  `python3 -m unittest tests.test_correlation_scale_kind_gate -v` right after
  writing DSX-STA-050/051), plus `python3 -m unittest tests.test_finding_
  catalogue_invariant -v` on any task that adds a `report.add(...)` call site.
- **Per wave merge:** `python3 -m unittest discover -s tests -q`.
- **Phase gate:** `scripts/check.sh` in full (or its steps run individually on
  native PowerShell) before `/gsd-verify-work` — exercises
  `scripts/gen-finding-catalogue.py --check` (catches a missing
  `_D05_ALLOWLIST_CODES` entry AND a stale `finding-codes.md`) and the
  good/bad fixture gate smoke test at all four gate points.

### Wave 0 Gaps
- [ ] `tests/test_declared_association_routing.py` — covers REQ-P18-01, REQ-P18-06
- [ ] `tests/test_correlation_scale_kind_gate.py` — covers REQ-P18-03
- [ ] `tests/test_agreement_completeness_gate.py` — covers REQ-P18-04
- [ ] `tests/test_finding_catalogue_invariant.py` extension — no new file, pinned numbers move
- [ ] `tests/test_effect_size_kind.py` extension — covers REQ-P18-05's report-only-kind branch
- [ ] `scripts/gen-finding-catalogue.py` `_D05_ALLOWLIST_CODES` addition — build-gate prerequisite for the D-05 citation checks in the new test files to mean anything
- [ ] No framework install needed — stdlib `unittest` confirmed working this session.

## Security Domain

`security_enforcement` is `true` in `.planning/config.json`
(`security_asvs_level: 1`, `security_block_on: "high"`), so this section is
required even though this phase has a thin threat surface, matching Phase
17's own assessment and the 18-CONTEXT.md persona round's decision not to
engage the Auditor lens (declaration-only, no data path).

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | No auth surface anywhere in this local CLI/library |
| V3 Session Management | No | No session concept exists |
| V4 Access Control | No | File-based CLI, no access-control surface |
| V5 Input Validation | Yes, extended | Five new closed-vocabulary/structural membership guards are being ADDED, following the exact-normalize-equality idiom `dsx/spec.py`'s own admissibility module calls out as deliberate ("no distance, containment, prefix or any other approximate match") — with the one documented, deliberate exception for the `weights` field's string-or-matrix type branch (Pitfall 5), which must still reject anything that is neither a recognised string nor a non-empty sequence |
| V6 Cryptography | No | No cryptographic operation anywhere in this phase |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| A closed-vocabulary check implemented as substring/fuzzy match, letting a malformed or adjacent value silently pass | Tampering (of the validation contract itself) | Exact `normalize(value) not in vocab` equality only, for every field EXCEPT `weights` |
| A type-confused membership check on the `weights` field (calling `normalize()`/`str()` on a matrix, silently producing a value that matches nothing but also raises nothing) | Tampering / Denial of validation | Explicit `isinstance` branch before any normalize/string comparison (Pitfall 5); a non-string, non-sequence value must still fire DSX-STA-061, not pass through un-checked |
| A new gate silently exempted from D-05's citation build gate because its family prefix isn't in the allowlist (Pitfall 3) | Repudiation (a code ships with no verifiable citation and the build gate reports nothing wrong) | Add the five codes by exact name to `_D05_ALLOWLIST_CODES`, not by prefix |
| Regenerated `references/finding-codes.md` committed out of sync with the real `report.add(...)` call sites | Tampering (documentation drifting from enforced behaviour) | `scripts/gen-finding-catalogue.py --check` as a build gate, already wired into `scripts/check.sh` |
| A fabricated or approximated citation locator for one of the D-07 not-in-hand items (ICC bands, Kendall's W bands, the P18-03 doctrinal citation) | Tampering (false authority) | Ship these as named, presence-only catalog rows with explicit "not-in-hand" / "no citation exists" language, never a numeric boundary or invented page/section locator |

This phase introduces no new attack surface (no network call, no
deserialization of untrusted input beyond the existing YAML spec loader used
unchanged, no new file write path beyond the existing catalogue-regen
mechanism, no new subprocess, no new credential or secret).

## Sources

### Primary (HIGH confidence — read directly from the live tree during this session)
- `dsx/checks/stats.py` — full file read (547 lines); `OUTCOME_TYPES`,
  `_MEMBERSHIP_FIELDS`, `PARAMETRIC_TESTS`/`NONPARAMETRIC_TESTS`,
  `recommend_test`, `check()`'s two `_check_declared_test` call sites,
  `_check_practical_significance` (DSX-STA-010/011/012),
  `_check_declared_test` (DSX-STA-040/041/042/043) all confirmed at the exact
  line numbers cited above
- `dsx/spec.py` — targeted reads (ESTIMAND_TYPES/ESTIMAND_KINDS block lines
  370-618; access-helper block lines 621-690; `describe_vocabulary()` tail
  lines 1499-1521); confirmed `_VOCABULARIES` registry shape, `is_blank`/
  `normalize`/`section`/`items`/`as_number` semantics, and the exhaustive
  grep confirming no declared measurement-scale field exists anywhere
- `dsx/mathx.py` — full file read (604 lines); `EFFECT_SIZE_KINDS`,
  `interpret_effect`, and every other function confirmed unmodified since
  Phase 15/16
- `references/test-selection.md` — full file read; confirmed current decision
  table has no correlation/agreement rows yet, and the fixed-assumption-order
  section the no-autoswitch test greps
- `references/finding-codes.md` — header and DSX-STA-* rows read; confirmed
  "Total: 260 codes" and the DSX-STA-040..043 rows are the current tail of
  that family
- `scripts/gen-finding-catalogue.py` — full file read (471 lines);
  `_D05_ALLOWLIST_PREFIXES`, `_D05_ALLOWLIST_CODES`, `check_d05()`,
  `_resolve_docstrings()` (per-enclosing-function resolution confirmed by
  direct read of the parent-map walk), `collect()`/`render()` mechanics
- `tests/test_finding_catalogue_invariant.py` — full file read (142 lines);
  `_EXPECTED_TOTAL`, `_SNAPSHOT_TOTAL`, `_MINTED_CODES`, both test bodies
- `tests/test_no_shapiro_autoswitch.py` — full file read; the structural-scan
  pattern this phase's REQ-P18-06 test should mirror
- `tests/test_effect_size_kind.py` — full file read; the existing DSX-STA-012
  test shapes this phase extends
- `tests/test_known_bad_corpus.py` — partial read; confirmed the known-bad
  corpus invariants are structural/compositional, not code-specific, and that
  new gate-code fixtures are a Phase 20 (REQ-P20-01) concern, not Phase 18's
- `dsx/cli.py` — grepped for `recommend`; confirmed `cmd_recommend`/
  `recommend-test` subcommand shape at lines 435-460 and 1032-1047
- `dsx/findings.py` — `Report.add`/`Report.ok` signatures confirmed at lines
  91-129
- `templates/APA-TABLE-research.md` — full file read (34 lines); confirmed it
  is genuinely ungated ("mints no finding code") and is the correct D-06
  wiring point
- `examples/good-ANALYSIS-SPEC.yaml`, `examples/bad-ANALYSIS-SPEC.yaml` —
  both read in full; confirmed neither `analysis:` block trips any of the
  five new predicates as currently declared
- `examples/known-bad/`, `examples/good-corpus/` — directory listings read;
  confirmed no existing fixture names correlation/agreement content
- `.planning/config.json` — read; confirmed `nyquist_validation: true`,
  `security_enforcement: true`, `security_asvs_level: 1`,
  `security_block_on: "high"`, `tdd_mode: true`
- `.planning/phases/18-correlation-association-and-agreement/18-CONTEXT.md`,
  `.planning/REQUIREMENTS.md`, `.planning/STATE.md`,
  `.planning/phases/17-foundation-repairs-and-spec-vocabulary/17-RESEARCH.md`
  and its cross-referenced `17-CONTEXT.md` D-02 disposition table (grepped
  for the Phase 18 rows, confirming REQ-P18-03/04 are already dispositioned
  paradigm-neutral, ships as-is — no D-12a pairing action needed this phase)
  — all read in full or via targeted grep this session
- Live shell checks this session: `python3 --version` (3.14.6),
  `python3 -m unittest tests.test_finding_catalogue_invariant -v` (2/2
  passed, confirming the pre-Phase-18 baseline of 260 codes is live and
  unchanged)

### Secondary (MEDIUM confidence)
- None used — no web research was performed. This is an internal-repository
  extension phase; the task briefing's own instruction (mirrored from Phase
  17's research) is not to pad this document with generic external research
  when every claim can and should be checked directly against the live tree.
  The row-level bibliographic citations for the statistical methods
  themselves (Shrout-Fleiss 1979, McGraw-Wong 1996 corrected, Feinstein-
  Cicchetti 1990 Parts I/II, Landis-Koch 1977, the Krippendorff 0.7598@ordinal
  reference value) were already confirmed by the operator-answered HQ-16 pack
  referenced in 18-CONTEXT.md D-04/D-05/D-07 — this research does not
  re-verify those external citations, it verifies where and how the CODE
  consumes them.

### Tertiary (LOW confidence)
- None.

## Metadata

**Confidence breakdown:**
- Live-tree locators (file paths, line numbers, function signatures, existing
  constants): HIGH — every one read directly this session, not carried over
  from a prior document.
- D-05 build-gate mechanism and the `_D05_ALLOWLIST_CODES` gap: HIGH — the
  mechanism is fully read and its precedent (`DSX-EXP-070`/`DSX-MET-021`/
  `DSX-COH-040`) is unambiguous; this is a factual gap in the phase's own
  locator list, not a judgment call.
- Field-shape recommendations (operand scale, ICC nesting, kappa field
  nesting): MEDIUM — reasoned from the one existing nested-block precedent
  (`design.cuped`) and from D-03's own explicit "plan-time binding" framing,
  but genuinely undecided anywhere in the committed tree; flagged as Open
  Questions for the planner to confirm or override, not asserted as settled.
- The DSX-STA-012 report-only control-flow question (Pitfall 6): MEDIUM — two
  readings of D-06's prose are both defensible; this session's recommendation
  is reasoned but not verified against the persona-round transcript itself
  (not available to this research session).
- Statistical citations (Shrout-Fleiss, McGraw-Wong, Feinstein-Cicchetti,
  Landis-Koch, Krippendorff): inherited HIGH confidence from 18-CONTEXT.md's
  own citation of the operator-answered HQ-16 pack — not independently
  re-verified by this research session (out of scope; this session verifies
  code/doc mechanics, not the underlying statistical literature).

**Research date:** 2026-09-01
**Valid until:** This research is a point-in-time read of the tree as it
stood immediately after Phase 17 closed (commit history through
`8df1068`/`a266a9b`/`c45f666`/`1ab7f8a`/`2f5618e`). Re-verify the exact line
numbers cited above immediately before executing if any further commit lands
on `gsd/v2.3.0-test-catalog` touching `dsx/checks/stats.py`, `dsx/spec.py`,
`dsx/mathx.py`, or `scripts/gen-finding-catalogue.py` between this research
and Phase 18 execute.
