# Phase 8: Interference, triggering, stability (`DSX-INT-*`) - Research

**Researched:** 2026-08-12
**Domain:** A Python gate-check module (`dsx/frame/interference.py`) that reads an already-parsed
YAML analysis contract and blocks or flags four kinds of declared-but-unmitigated causal-inference
risk (interference/SUTVA, dilution, novelty/primacy) using only declarations already present in the
spec — no statistics are computed on the gate path.
**Confidence:** HIGH

## Summary

This is an implementation-research pass, not a literature pass — the five citations (Deng & Hu,
Kohavi/Tang/Xu, Sadeghi et al., Imbens & Rubin, Blake & Coey) are already verified and locked in
`08-CONTEXT.md`. What this document adds is what the codebase actually looks like *right now*,
verified by reading it directly rather than by trusting the line numbers `08-CONTEXT.md` cites (most
have drifted, because `08-CONTEXT.md` and `07-CONTEXT.md` were gathered concurrently and Phase 7's
plan 07-01 has already landed on `main`, adding ~90 lines to `dsx/spec.py` before this file's line
numbers were recorded).

**Primary recommendation:** build `dsx/frame/interference.py` as a structural clone of
`dsx/frame/paradigm.py`, exactly as Phase 7 built `dsx/frame/val.py`. Two of Phase 7's
already-landed additions are directly reusable and must not be re-implemented: `is_placeholder_or_refusal()`
(`dsx/spec.py:421`) satisfies D-08's placeholder-detection need without a new helper, and
`design_effect()`'s sibling in `dsx/mathx.py` establishes the exact pure-function shape for D-09's
dilution formula. One collision is real and unavoidable — the known-bad corpus's
`interference-shared-budget` fixture will, once `DSX-INT-040` ships, block on a **second**,
previously undocumented code (`DSX-INT-040`, novelty/primacy) in addition to its intended
`DSX-INT-010`, because the fixture already declares `stability.novelty_primacy_assessed: false`
(line 149) — a fact neither `07-RESEARCH.md` nor `08-CONTEXT.md` names. Section 1 below gives the
concrete fix.

**Five things this document establishes that `08-CONTEXT.md` could not, because they require reading
code that either didn't exist yet at context-gathering time or has since changed:**

1. Phase 7 has **not been executed** — only its planning documents and two infrastructure-only
   plans (07-01, 07-02) have landed. `dsx/frame/val.py` does not exist on disk;
   `dsx/frame/` contains only `paradigm.py`. `dsx/cli.py` registers no `val` check. This is the
   answer to phase-specific question 2(d): if Phase 8 executes before Phase 7's plan 07-03, the
   paradigm-read scanner (`TestFrameParadigmReadBoundary`) does not exist and Phase 8's plan must
   write it, not assume it.
2. The paradigm-read scanner Phase 7 designed (07-03-PLAN.md Task 2) is **not** "parameterised over
   a module list" the way D-14 predicted — it is a directory glob over every `*.py` file under
   `dsx/frame/`, with `paradigm.py` excluded by name. This is strictly better than a list: once
   either phase writes it, `dsx/frame/interference.py` is covered automatically, with **zero**
   further edits, the moment the file exists in that directory. See Section 2.
3. `dsx/spec.py` already has a placeholder-detection helper — `is_placeholder_or_refusal()`
   (line 421), shipped by Phase 7's already-landed 07-01 — that is a near-exact match for what
   D-08 asks Phase 8 to build from scratch. Building a second, narrower `is_placeholder()` would be
   the "two phases add near-identical helpers" collision D-08 itself warns about. See Section 4.
4. `METRIC_TYPES` (`dsx/spec.py:110`, a plain `set`) and `_validate_metrics`
   (`dsx/spec.py:561`) confirm `type` is optional today with no requiredness finding — exactly the
   escape hatch D-11 already names. `DEPENDENCE_ADMISSIBLE_METHODS` at `dsx/spec.py:229` is the
   live precedent for a *non*-vocabulary constant excluded from `_VOCABULARIES`'s coverage test,
   which is the shape Phase 8's additive/ratio partition should also take. See Section 5.
5. Every citation to `dsx/cli.py:63/88/105` in `08-CONTEXT.md` is currently accurate (Phase 7 has
   not touched this file yet) — but that will stop being true the moment Phase 7's 07-03 lands, so
   the plan should locate these by name (`CHECKS`, `GATE_PROFILES`, `GATE_THRESHOLDS`), not by line
   number, in its own action text.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-P8-01 | Declared interference risk with no mitigation and no residual note is blocked, citing Imbens & Rubin (2015) SUTVA | Section 3 (accessor idioms for `interference.risk`/`.mitigation`/`.residual_note`) + Section 4 (`is_placeholder_or_refusal()` for the residual-note escape-hatch test) |
| REQ-P8-02 | Shared-budget and marketplace interference are distinct risks with distinct admissible mitigations | Section 3 (`INTERFERENCE_RISKS`/`INTERFERENCE_MITIGATIONS` already shipped, `dsx/spec.py:237-260`) — D-05/D-07's admissibility map is `08-CONTEXT.md`'s own territory, not re-derived here |
| REQ-P8-03 | `DSX-INT-030` blocks eligible-population analysis of an additive metric with no dilution adjustment, asserting `delta_diluted = delta_triggered × trigger_rate` | Section 5 (metric-type partition, `_validate_metrics` optionality) + Section 7 (`dsx/mathx.py::design_effect()` as the exact pure-function precedent for the new dilution function) |
| REQ-P8-04 | Ratio-metric dilution is out of scope, backlog entry rewritten per D-12 | Section 6 (decision-record emission points) — confirmed `brief.md` §6.5 currently carries **no row at all** about ratio-metric dilution, so this is a new row, not an edit |
| REQ-P8-05 | Unassessed novelty/primacy over the stability window is flagged with assessment method cited | Section 3 (`stability.*` accessors) + Section 1 (the `interference-shared-budget` fixture collision this requirement's own check creates) |
| REQ-P8-06 | No `DSX-INT-*` check reads `inference.paradigm`, asserted by test | Section 2 (the paradigm-read scanner's actual, verified mechanics) |
</phase_requirements>

## Architectural Responsibility Map

Same single tier as Phase 7 (`07-RESEARCH.md`'s own map, unchanged): a deterministic, stdlib-only
Python library reading an in-memory dict and returning a `Report`. No browser, server, CDN or
database tier.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Interference/SUTVA, triggering-dilution, stability adjudication | Gate-check library (`dsx/frame/interference.py`) | — | Pure function over an in-memory dict; no I/O, no network, no persistence |
| Risk→mitigation admissibility map, additive/ratio metric partition | `dsx/frame/interference.py` module constants | Contract module (`dsx/spec.py`) for the vocabularies referenced | D-05: this is a capability matrix, not a vocabulary — it stays local to the check, unlike Phase 7's structure→method map, which Phase 11 also needs and therefore lives in `dsx/spec.py` |
| Dilution arithmetic (`delta_diluted = delta_triggered × trigger_rate`) | Math kernel (`dsx/mathx.py`) | Gate-check library | Peer module, same pattern as `design_effect()`/`inflation_from_peeking()`; never called from the gate path (D-09) |
| Shared vocabulary (`INTERFERENCE_RISKS`, `INTERFERENCE_MITIGATIONS`, `ANALYSIS_POPULATIONS`, `METRIC_TYPES`) | Contract module (`dsx/spec.py`) | Gate-check library | Already shipped by Phase 6; Phase 8 adds zero new vocabulary members |
| CLI registration and gate-profile membership | CLI entry point (`dsx/cli.py`) | — | Wires `interference` into `plan`/`verify`/`ship`, not `execute` |
| Decision-trail emission | Decision-record schema (`dsx/decisions.py`) | Gate-check library | `interference.py` constructs `DecisionRecord`s; the schema/writer are central and unchanged |
| Paradigm-read invariant | Test-only scanner (`tests/test_frame_boundary.py`) | — | Enforces D-11 across the whole `dsx/frame/` package by directory glob, not a module list |

## Package Legitimacy Audit

Not applicable. This phase is zero new external dependencies — D-01 (stdlib only on the gate path,
inherited from `brief.md`) applies unchanged, and every file this phase touches or creates
(`dsx/frame/interference.py`, `dsx/spec.py`, `dsx/mathx.py`, `dsx/cli.py`,
`scripts/gen-finding-catalogue.py`, YAML fixtures, Markdown docs, test files) is Python
standard-library code, verified by reading the equivalent Phase 7 files directly (Section headers
below cite the actual, current source). No `npm view`/`pip index versions`/`cargo search` check
applies.

## Environment Availability

Skipped — pure Python standard-library code and Markdown/YAML documentation, identical reasoning to
`07-RESEARCH.md`'s own skip. `python3 -m unittest discover -s tests -v` (Python 3.14.6, confirmed by
`07-03-PLAN.md`'s `<shell_note>`) is the only execution dependency.

---

## 1. The known-bad corpus rewrite — Phase 7's proposed resolution, a second collision it missed, and the concrete new shape

**Phase 7's research already named this exact conflict** (`07-RESEARCH.md`, "Critical planning
risk" section, and its own D-15) for its own new fixture,
`weak-identification-mmm-ANALYSIS-SPEC.yaml`, which must **block** `dsx gate plan` under
`DSX-VAL-040` while `test_every_spec_passes_the_critical_threshold_gate_points` currently asserts
every fixture found by globbing `examples/known-bad/*-ANALYSIS-SPEC.yaml` clears `plan`/`execute`
with exit code 0. Phase 7's research offered three resolutions (narrow the blanket test with an
exclusion set; add a companion assertion plus a skip marker; relocate the fixture — rejected as
non-viable). **As of this research pass, none of the three has been chosen or implemented** —
Phase 7's plan 07-03 (which creates the first blocking `DSX-VAL-*` code) has not executed, so the
conflict is still purely theoretical on Phase 7's side too. There is no rewritten
`tests/test_known_bad_corpus.py` on disk anywhere to build on. **Whichever phase's plan executes
first performs this rewrite; the second phase extends the resulting data structure, not a second
parallel one.** Given the roadmap's own "no hard dependency" framing and that both phases' plans are
independently drafted, the Phase 8 plan should write the rewrite defensively: check whether the
per-fixture map already exists (Phase 7 landed first) and extend it, or create it (Phase 8 landed
first) in the shape below.

### The current structure, read directly (`tests/test_known_bad_corpus.py`, 331 lines, read in full)

```python
_CRITICAL_THRESHOLD_POINTS = ("plan", "execute")          # line 41
_INCIDENTAL_GAP_CODES = { ... 8 entries ... }              # line 49-59
_TARGET_CODE_FAMILIES = ("DSX-INT-", "DSX-PAR-01")         # line 66
```

Three tests read these:
- `test_every_spec_passes_the_critical_threshold_gate_points` (line 187) — every fixture must exit
  `0` at `plan` and `execute`, no exceptions, no per-fixture allowance.
- `test_ship_gate_findings_are_all_documented_incidental_corpus_gaps` (line 202) — every
  CRITICAL/HIGH finding at `ship` must be in `_INCIDENTAL_GAP_CODES`.
- `test_incidental_allowlist_names_no_target_family_code` (line 231) — no entry in
  `_INCIDENTAL_GAP_CODES` may start with a `_TARGET_CODE_FAMILIES` prefix.

`_TARGET_CODE_FAMILIES` **already contains `"DSX-INT-"`** — it was written when Phase 6 authored the
`interference-shared-budget` fixture's post-mortem naming `DSX-INT-010` as the code that will catch
it, before Phase 7 or Phase 8 existed as separate phases. This means the family-level exclusion in
`test_incidental_allowlist_names_no_target_family_code` is not a hypothetical Phase 8 will trigger —
**it already exists and already targets Phase 8's whole code family**, not just `DSX-INT-010`.

### The second collision, not previously named anywhere: `DSX-INT-040` on the same fixture

I read `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml:147-150` directly:

```yaml
stability:
  window: "14 days"
  novelty_primacy_assessed: false
  evidence: ""
```

Under `08-CONTEXT.md` D-01, `DSX-INT-040` fires HIGH when `stability` is present and
`novelty_primacy_assessed` is not `true` — which this fixture satisfies independently of its
intended defect (`DSX-INT-010`, interference). **This fixture will block `dsx gate ship` on two
`DSX-INT-*` codes, not one, the moment both land**, and `DSX-INT-040`'s block is not the defect the
fixture's header or post-mortem documents. Because `DSX-INT-040` starts with `"DSX-INT-"`, it
**cannot** be added to `_INCIDENTAL_GAP_CODES` under the current family-blanket exclusion — the
exact failure mode that makes a coarse family-prefix exclusion insufficient once a family ships more
than one code. This is concrete, present-tense evidence for why D-15's "per-fixture map" framing is
right and a finer-grained family exclusion would not be: the corpus needs to distinguish "the code
this fixture exists to demonstrate" from "an incidental code from the same family this fixture
happens to also trip," and no set of family-prefix strings can express that distinction once a
family has more than one member.

**Recommendation (not a re-litigation of D-15, an execution of it):** fix this by declaring the
fixture's `stability` block honestly — `novelty_primacy_assessed: true` with a real `evidence`
pointer — rather than adding a second undocumented incidental gap. The fixture's own defect is
interference, not stability; there is no reason for it to also carry an unassessed novelty/primacy
declaration, and the corpus's stated guarantee (module docstring, "a fixture blocks only on its own
encoded defect") is best served by removing the second defect rather than documenting around it.
This mirrors Phase 7's own D-14 resolution for `interference-shared-budget`'s pre-existing
`method_family_required: ""` problem — edit the fixture's *unrelated* field rather than grow the
allow-list. If the planner instead prefers to document it, `DSX-INT-040` must be treated as a
target-family code inside the new per-fixture structure (below), not squeezed into the old
blanket list.

### The concrete new shape

Replace the flat `_INCIDENTAL_GAP_CODES`/`_TARGET_CODE_FAMILIES` pair with a per-fixture map naming,
for each slug, the code(s) it exists to demonstrate and at which gate point(s) they are expected to
block:

```python
# Per-fixture: the finding code(s) each corpus fixture exists to demonstrate, and the gate
# point(s) at which that code is expected to block. A fixture whose target code has not shipped
# yet is absent from this map — it defaults to "clears every gate point cleanly", which is
# today's behaviour for every fixture, preserved exactly for fixtures with no target code yet.
_TARGET_DEFECT_CODES: dict[str, dict[str, str]] = {
    # slug: {gate_point: code}
    "interference-shared-budget": {"plan": "DSX-INT-010"},
    "triggering-dilution": {"plan": "DSX-INT-030"},
    # Phase 9 adds two more slugs here (DSX-PAR-010/011, currently _TARGET_CODE_FAMILIES's
    # other member) when its own plan lands; Phase 7 adds weak-identification-mmm the same way.
}
```

And rewrite the three affected tests against it:

1. **`test_every_spec_passes_the_critical_threshold_gate_points`** →
   `test_every_spec_blocks_only_on_its_target_defect_at_critical_threshold_points`: for each
   fixture and each of `("plan", "execute")`, look up `_TARGET_DEFECT_CODES.get(slug, {}).get(point)`.
   If absent, assert exit code `0` exactly as today. If present, assert exit code `1` **and** that
   the target code is among the CRITICAL findings — this is the fixture's positive proof, not just
   the absence of a negative one.
2. **`test_ship_gate_findings_are_all_documented_incidental_corpus_gaps`** → keep
   `_INCIDENTAL_GAP_CODES` as the residual allow-list for genuinely incidental defects, but subtract
   each fixture's own `_TARGET_DEFECT_CODES` entries from `blocking` before checking membership, so
   a fixture's intended defect is never mistaken for an incidental gap.
3. **`test_incidental_allowlist_names_no_target_family_code`** → becomes
   `test_incidental_allowlist_names_no_slugs_own_target_code`: for each fixture, assert none of its
   own `_TARGET_DEFECT_CODES` values are also present in `_INCIDENTAL_GAP_CODES` (a fixture's target
   defect must never be laundered into "incidental"). This is strictly more precise than the old
   family-prefix check and does not block a genuinely incidental code from a *different* family
   member on the *same* fixture — the exact case `DSX-INT-040`-on-the-interference-fixture would
   have needed, had the planner chosen to document rather than fix it.

`test_every_postmortem_names_a_catch_attribution_finding_code` (line 176) needs **no change** —
verified by reading it: it only asserts the post-mortem text matches `_FINDING_CODE_RE`
(`\bDSX-[A-Z]+-\d+\b`) anywhere, regardless of whether that code currently blocks. The interference
fixture's post-mortem already names `DSX-INT-010` (predates this phase), so this test already
passes and stays green through the rewrite untouched — resolving `08-CONTEXT.md`'s Discretion item
on this question.

## 2. The paradigm-read detector — not a module list, a directory glob; ordering dependency stated plainly

I read `07-03-PLAN.md` Task 2 in full (`.planning/phases/07-validity-frame-checks-dsx-val/07-03-PLAN.md:318-396`)
and `tests/test_frame_boundary.py` (126 lines, read in full, current state — Phase 7's Task 2 has
**not executed**, so today the file contains only `TestFrameImportBoundary`, no paradigm-read class
at all).

**(a) Not parameterised over a module list.** Task 2's action text says explicitly: *"Scan every
Python file under the frame package, not only the new module, so a future frame module inherits the
invariant without anyone remembering to extend the test... The paradigm module itself is the one
legitimate reader of that field and must be excluded by name."* This is a directory glob
(`FRAME_DIR.rglob("*.py")`, matching the existing import-boundary scanner's own
`test_real_frame_modules_import_nothing_from_checks` at `tests/test_frame_boundary.py:93-102`, which
already globs the whole `dsx/frame/` tree this exact way) with one hardcoded exclusion
(`paradigm.py`), not a list the planner edits per phase.

**(b) What Phase 8 needs to change:** nothing, if Phase 7's 07-03 lands first. `dsx/frame/interference.py`
is a new file under `dsx/frame/`; the glob picks it up automatically the moment it exists, with no
edit to the scanner. If Phase 8 lands first, its own plan must write this scanner (mirroring 07-03
Task 2's action text exactly), because it does not exist yet — see (d) below.

**(c) Coverage of the three required read forms, verified against the actual planned detector
design (two layered detectors, per Task 2's action text):**

| Form | Detector | Verified |
|---|---|---|
| `get(spec, "inference.paradigm")` | AST: "reports a violation when any positional argument is a string constant equal to that dotted path" | Yes — `"inference.paradigm"` is a string-literal positional arg to `get` |
| `spec["inference"]["paradigm"]` | AST: "It should also report a violation for a subscript chain that reads the inference key and then the paradigm key" | Yes — Task 2's action text names this exact subscript form explicitly |
| Bare string literal `"inference.paradigm"` anywhere | Text-level: "reports a violation when the source contains the dotted path... anywhere at all — in code, in a comment or inside a message string" | Yes — a plain substring scan, deliberately blunt |

All three forms D-14 requires are covered by the design as planned. The text-level detector alone
would **not** catch `spec["inference"]["paradigm"]` (that source text never contains the contiguous
substring `"inference.paradigm"`), which is exactly why Task 2 specifies the second, AST-based
detector as a separate layer rather than relying on the text scan alone — read this as confirmation
the two-detector design is load-bearing, not decorative.

**(d) Ordering, stated plainly.** As of this research pass: `dsx/frame/val.py` does not exist,
`tests/test_frame_boundary.py` has one test class, and `dsx/cli.py` registers no `val` check.
**Phase 8's plan cannot assume the scanner exists.** Two honest options for the Phase 8 plan:

- Write the scanner itself (full duplicate of 07-03 Task 2's design), accepting that if Phase 7
  lands second, its own Task 2 either becomes a no-op requiring only the addition of an
  explanatory comment, or the two plans need light de-duplication at merge time (a `git` conflict
  in `tests/test_frame_boundary.py`, resolved by keeping the union of both phases' synthetic-violation
  test cases — no logic conflict, since both would specify the identical directory-glob-plus-exclude
  design).
- Have the Phase 8 plan's task check, at execution time, whether `TestFrameParadigmReadBoundary`
  already exists in `tests/test_frame_boundary.py` (i.e. whether Phase 7 landed first) and, if so,
  skip creating it and instead add only a regression assertion that `dsx/frame/interference.py`
  specifically scans clean under it — the substantive coverage is already guaranteed by the glob,
  so this reduces to a documentation/traceability step, not new detection logic.

Either is defensible; the second is cheaper and matches the "second phase adds its module and
nothing else" framing D-14 itself uses, updated for the fact that "adding its module" now means
literally nothing beyond creating the file in the right directory.

## 3. The interference/triggering/stability sub-block accessor idiom, with real code

Read `dsx/spec.py:346-367` (access helpers, unchanged since Phase 6, current line numbers verified)
and `dsx/spec.py:806-921` (`_validate_validity_frame_shape`, Phase 6's own shape validator, the
existing reference implementation of exactly this reading pattern):

```python
# dsx/spec.py:346-358
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
```

`get(spec, "validity_frame.interference.risk")` is the dotted-path idiom `dsx/frame/paradigm.py:80`
already uses for `inference.paradigm`; `section(frame, "interference")` (or the equivalent
`frame.get("interference")` with an `isinstance` guard, the pattern `_validate_validity_frame_shape`
itself uses at line 911-913) is the idiom for pulling out a sub-block before reading its fields. The
correct field paths for this phase, verified against `_VALIDITY_FRAME_MEMBERSHIP`
(`dsx/spec.py:813-822`) and the template (`templates/ANALYSIS-SPEC.yaml:306-322`):

```
validity_frame.interference.risk            validity_frame.triggering.analysis_population
validity_frame.interference.mechanism       validity_frame.triggering.expected_trigger_rate
validity_frame.interference.mitigation      validity_frame.triggering.dilution_adjusted
validity_frame.interference.residual_note   validity_frame.stability.window
                                             validity_frame.stability.novelty_primacy_assessed
                                             validity_frame.stability.evidence
```

`risk`, `mitigation` and `analysis_population` have closed-vocabulary membership already checked by
`DSX-SPEC-082` (`_VALIDITY_FRAME_MEMBERSHIP` lines 813-822, matching against `INTERFERENCE_RISKS`,
`INTERFERENCE_MITIGATIONS`, `ANALYSIS_POPULATIONS`) — Phase 8's checks read these fields but do not
need to re-validate membership, exactly as Phase 7 does not re-validate `identification.strength`'s
membership. `mechanism`, `residual_note`, `window` and `evidence` are free text with **no** vocabulary
membership check anywhere — `is_blank()`/`is_placeholder_or_refusal()` are the only guards available
for them, same as Phase 7's `falsifier`.

**The `_NULL` / missing-vs-blank-vs-false distinction (D-08/D-13's turning point):** `get()`
(above) returns `default` (typically `None`) both when a key is genuinely absent from the dict *and*
when the stored value is Python `None` — the two are indistinguishable through `get()` alone. This
matters concretely for `stability.novelty_primacy_assessed`: the template declares it `false`
(`templates/ANALYSIS-SPEC.yaml:321`, a real boolean, not absent), and `is_blank(False)` returns
`False` (`dsx/spec.py:369-376`'s `is_blank` only treats `None`, an empty string, or an empty
collection as blank — a boolean `False` is none of those). **A check written as
`if is_blank(get(frame, "stability.novelty_primacy_assessed")): fire` would never fire on the
literal `false` value D-01's trigger requires** — it must instead do
`if get(frame, "stability.novelty_primacy_assessed") is not True: fire` (or equivalently, compare
against the boolean directly), because "declared false" and "declared absent" must both count as
"not assessed" under D-01's wording ("novelty/primacy is unassessed... or assessed with a blank
evidence pointer") but `is_blank()` alone conflates neither correctly with a boolean field. This is
the load-bearing reason D-01's four codes cannot be written as a single generic "is_blank check"
helper reused four times — three of the four (`risk`+`mitigation`+`residual_note`,
`analysis_population`+`dilution_adjusted`, `novelty_primacy_assessed`+`evidence`) each combine a
string-blankness test with a boolean-identity test, and the exact combination differs per code.

## 4. `is_placeholder()` — the collision is real, and the collision is with an already-shipped helper

**Direct read of `dsx/spec.py:369-446`, current state, confirms Phase 7's 07-01 plan has already
landed `is_placeholder_or_refusal()`:**

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

    Layered beside ``is_blank()``, never a replacement for it — ``is_blank()`` stays
    unchanged because placeholder text still counts as present for the sampling-frame
    and measurement checks (plan 07-06), which must treat placeholder text as present
    so the template does not trip them.
    """
    if is_blank(value):
        return True
    if isinstance(value, str) and _PLACEHOLDER_RE.match(value.strip()):
        return True
    return normalize(value) in _FALSIFIER_REFUSALS
```

`08-CONTEXT.md` D-08 asks Phase 8 to "Add `is_placeholder()` to `dsx/spec.py` beside `is_blank()`
(line 326)... matching text wrapped in angle brackets," citing `residual_note`'s escape hatch
requiring the field to be "both non-blank and not a placeholder." **This is functionally what
`is_placeholder_or_refusal()` already computes**, plus a refusal-token check D-08's prose doesn't
mention but doesn't rule out either (a `residual_note` of literal `"n/a"` should not clear the gate
any more than a blank one should — the refusal-token layer is strictly more correct for this use
case, not a mismatch). `is_placeholder_or_refusal(value)` returning `True` means exactly "this is
not a real answer" — blank, an angle-bracket placeholder, or a refusal word — which is precisely
what D-08's escape-hatch test needs to reject.

**Recommendation: reuse `is_placeholder_or_refusal()` directly. Do not add a second, narrower
helper.** This is the exact "check for name collisions before coining a term" precedent
`06-CONTEXT.md` and `07-CONTEXT.md` both invoke, applied to Phase 8's own D-08. Two supporting
reasons beyond avoiding duplication:

1. `is_blank()` itself has moved from `dsx/spec.py:326` (as cited in `08-CONTEXT.md`, stale) to
   `dsx/spec.py:369` — any Phase 8 action text that locates the new helper "beside `is_blank()` at
   line 326" is citing a line that currently holds unrelated code (`normalize()`'s neighbourhood
   has shifted). The plan should locate helpers by name, not line number, exactly as this
   document's own summary recommends generally.
2. `_PLACEHOLDER_RE` (`^<[^>]*>$`) already matches the template's exact placeholder shape
   (`templates/ANALYSIS-SPEC.yaml:310`: `residual_note: "<what remains unaddressed, if anything>"`)
   — this is the literal case D-08's own rationale names ("`dsx init` scaffolds a file that clears
   a blocking check unedited"). A second regex would either duplicate this pattern exactly (pure
   waste) or diverge from it slightly (a real bug: two placeholder detectors disagreeing on which
   shapes count).

**One naming caveat for the plan to resolve explicitly:** `is_placeholder_or_refusal()`'s own
docstring says it is "layered beside `is_blank()`," written for the falsifier use case, and Phase 8
would be its second caller. If the planner wants the name to read cleanly for a general-purpose
helper rather than one that reads as falsifier-specific, an alias or a docstring update (not a
reimplementation) is the lightest fix — e.g. broadening the docstring's language from
"the falsifier" to "any free-text escape hatch," which D-08 itself anticipates ("the helper is
written to be reused by Phases 7 through 11 for every prose escape hatch they introduce"). This is
squarely Claude's Discretion, not a re-litigated decision — D-08's *substance* (residual_note needs
non-blank-and-non-placeholder) is unchanged; only the vehicle (reuse vs. new function) is corrected.

## 5. The metric-type partition and how a plan's metrics are enumerated

Read `dsx/spec.py:110` and `dsx/spec.py:561-624` (`_validate_metrics`, in full) directly.

```python
# dsx/spec.py:110
METRIC_TYPES = {"ratio", "count", "sum", "average", "rate", "percentile", "index"}
```

Confirmed: `METRIC_TYPES` is a plain `set`, 7 members, no additive/ratio distinction — exactly as
`08-CONTEXT.md` D-11 states (its cited line 98 is stale; current location is 110).

```python
# dsx/spec.py:615-624 — the only place `type` is read against METRIC_TYPES
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

**Confirmed: `type` is optional today.** The guard is `if mtype and mtype not in METRIC_TYPES` — an
absent or blank `type` short-circuits the whole check silently. This is exactly D-11's "live escape
hatch": a metric with no declared `type` cannot be classified additive or ratio, so `DSX-INT-030`
cannot adjudicate it, and deleting a `type: count` line is the cheapest way past the check. D-11's
prescribed handling (skip plus a decision record, not a finding) is the right response given this
confirmed behaviour — firing on an undeclared type would be a *new* requiredness rule
`_validate_metrics` doesn't currently express, which `08-CONTEXT.md` correctly scopes out.

**How a check walks a plan's metrics**, the existing idiom (`items()`, `dsx/spec.py:361-367`, used
by `_validate_metrics` itself at line 562):

```python
def items(spec: dict, name: str) -> list[dict]:
    """Return a list section, keeping only mapping entries."""
    value = spec.get(name)
    if not isinstance(value, list):
        return []
    return [v for v in value if isinstance(v, dict)]
```

`DSX-INT-030`'s helper should do `metrics = items(spec, "metrics")` (top-level, not under
`validity_frame` — metrics live at `spec.metrics`, confirmed by `good-ANALYSIS-SPEC.yaml:28`), then
for each metric read `normalize(metric.get("type", ""))` the same way `_validate_metrics` does, and
partition against the new additive/ratio constant.

**The `_VOCABULARIES` exclusion precedent, verified directly** (`dsx/spec.py:309-340`, the actual
comment and list):

```python
# dsx/spec.py:309-314
# Single registry behind describe_vocabulary() (D-05, REQ-P6-06): the object each shape
# validator imports is the exact object dumped here — one place to add a vocabulary, not two.
# Deliberately excludes SPEC_VERSION, CAUSAL_VERBS, REQUIRED_TOP_LEVEL,
# IMBALANCE_UNSAFE_METRICS, DEPENDENCE_ADMISSIBLE_METHODS and FALSIFIER_DISCRIMINATORS —
# they are not vocabularies. chart_capabilities stays special-cased in
# describe_vocabulary() below, exactly as before.
_VOCABULARIES: "list[tuple[str, Any]]" = [ ... ]   # METRIC_TYPES is registered here as "metric_types"
```

`DEPENDENCE_ADMISSIBLE_METHODS` (`dsx/spec.py:229`, Phase 7's structure→admissible-method map) is
the **live, already-shipped precedent** for exactly the shape Phase 8's additive/ratio partition
needs: a constant that *references* an existing vocabulary member set (here, `METRIC_TYPES`) without
being registered in `_VOCABULARIES` itself. Following this precedent exactly — adding the new
partition's name to the same exclusion comment, alongside `DEPENDENCE_ADMISSIBLE_METHODS` — is what
keeps it out of `_VOCABULARIES`'s registry coverage test (the same test D-05's rationale in
`08-CONTEXT.md` correctly anticipates would otherwise trip). Concretely:

```python
# Additive vs. ratio partition over METRIC_TYPES (D-11, REQ-P8-03/04) — not a vocabulary,
# excluded from _VOCABULARIES for the same reason DEPENDENCE_ADMISSIBLE_METHODS is: it
# references an existing vocabulary's members rather than defining new ones.
_ADDITIVE_METRIC_TYPES = frozenset({"count", "sum", "average"})
_RATIO_METRIC_TYPES = frozenset({"ratio", "rate"})          # explicitly out of scope, REQ-P8-04
# {"percentile", "index"} are neither — unadjudicated by DSX-INT-030, per D-11.

assert _ADDITIVE_METRIC_TYPES | _RATIO_METRIC_TYPES <= METRIC_TYPES  # the set-equality-style
# invariant D-05 asks every capability matrix to carry, mirroring _PARADIGM_CONDITIONAL's own
# test at dsx/frame/paradigm.py — a future METRIC_TYPES addition without a matching bucket here
# should fail loudly rather than silently landing in neither partition.
```

This constant belongs in `dsx/frame/interference.py` itself (D-05's own instruction: "Add a
partition in `dsx/frame/interference.py` that *references* it — do not coin a parallel metric
vocabulary"), **not** in `dsx/spec.py` — unlike Phase 7's structure→method map, which Phase 11 also
needs and therefore lives centrally. Nothing downstream of Phase 8 is known to need this partition,
so there is no reuse argument for centralising it.

## 6. Decision-record emission points

`dsx/decisions.py` (213 lines, read in full) is unchanged since Phase 6/7; the schema, `append()`,
`read_all()` and `collect_from_report()` mechanics are identical to what `07-RESEARCH.md` Section 1
already documents for Phase 7. The concrete emission pattern, verified against both
`dsx/frame/paradigm.py:146-161` and `dsx/spec.py:860-880` (`_validate_validity_frame_shape`'s own
`DecisionRecord`, the R-01 requiredness rule):

```python
report.context.setdefault("decisions", []).append(
    DecisionRecord(
        id="", invocation_id="",              # CLI layer fills both in
        layer="deterministic",
        choice="<what was concluded>",
        inputs=["validity_frame.interference.risk", "validity_frame.interference.mitigation"],
        rule="<the structural rule applied, in one sentence>",
        citation="<the D-05 citation for this judgment>",
        counterfactual="<what a different declaration would have produced>",
    ).to_dict()
)
```

**Four emission points for Phase 8's four codes**, one per `report.add(...)` call site (matching
Section 3's finding that each code combines a distinct field-pair test, so each needs its own
docstring under the D-05 build check anyway — see `07-RESEARCH.md` Section 3 for the exact
mechanism, which transfers unchanged: the extractor resolves a docstring from the nearest enclosing
function, so `DSX-INT-010`/`011`/`030`/`040` each need their own `Citation:`/
`Structural criterion:`/`Reference value:` block if implemented as four private helpers, which is
the natural decomposition and the one `dsx/checks/design.py` and Phase 7's plan both use).

**D-11's skip-on-undeclared-metric-type record** (Section 5 above) is a fifth, distinct emission
point — not a finding, a decision record only, following `_validate_validity_frame_shape`'s own
pattern of emitting a `DecisionRecord` even on the path that produces no `report.add(...)` call
(compare `dsx/spec.py:852-880`: the R-01 decision record is appended unconditionally, before the
function branches into the missing-block/present-block paths). Concretely: for each metric with no
declared `type`, append a `DecisionRecord` with `choice="skip: metric type undeclared"`,
`inputs=["metrics[].type"]`, and a `rule` naming the escape hatch explicitly ("a metric with no
`type` cannot be classified additive or ratio and is not adjudicated by `DSX-INT-030`") — this is
what makes the known limit visible in the `dsx explain` trail, per D-11's own text.

**`brief.md` §6.5, read directly (`brief.md:364-390`):** the gated-backlog table currently has
**zero rows about ratio-metric dilution or Deng & Hu's ratio equation.** D-12's rewrite is therefore
a **new row**, not an edit to an existing one — confirming REQ-P8-04's fourth deliverable (D-18: "a
documentation-content test asserting the §6.5 row exists") tests for presence, not for a changed
wording, which simplifies that test's design.

## 7. Fixture mechanics

**The copy-and-mutate idiom, current location** (`08-CONTEXT.md` cites `tests/test_dsx.py:1410-1447`,
which today is a *different*, broader idiom — a multi-file phase-directory setup for cross-check
gate testing, not a single-field mutation). The precise single-field copy-and-mutate idiom D-17
describes is `_bayesian_variant_spec_path` at `tests/test_dsx.py:1535-1555`, read in full:

```python
def _bayesian_variant_spec_path(self, tmp: str) -> Path:
    """Copy examples/ into tmp and flip inference.paradigm to bayesian on
    the good fixture, in place — no second committed fixture, and the
    good fixture's own paradigm is never edited. ...
    """
    import json, shutil
    from dsx.loader import load

    target = Path(tmp) / "examples"
    shutil.copytree(self.ROOT / "examples", target)
    spec_path = target / "good-ANALYSIS-SPEC.yaml"
    spec = load(spec_path)
    spec.setdefault("inference", {})["paradigm"] = "bayesian"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    return spec_path
```

This is the exact shape for success criterion 1's mitigated variant and success criterion 2's
marketplace-mitigation variant (D-17): `shutil.copytree(examples/, tmp)`, `load()` the target spec,
mutate the one field under test with plain dict assignment, write back as JSON (the loader accepts
JSON regardless of the `.yaml` suffix — confirmed by the docstring's own note, which is accurate:
`dsx.loader.loads()` tries JSON first whenever stripped text starts with `{`).

**What a full-shape known-bad fixture needs to clear `dsx validate` structurally** (Phase 6's 06-08
decision, unchanged): `test_every_spec_passes_dsx_validate` (`tests/test_known_bad_corpus.py:166`)
runs `dsx validate` (structural/vocabulary checks only — `DSX-SPEC-*`, not the frame checks) and
requires exit `0`. This means the new `triggering-dilution` fixture must declare **every** required
`validity_frame` sub-block (all ten, since `question_type: causal` or `design.kind: experiment`
triggers `needs_causal_block`, confirmed at `dsx/spec.py:852-855`) with values inside their closed
vocabularies — the "full-shape clone of the good fixture" instruction in D-17 is not optional
polish, it is what makes `dsx validate` pass at all.

**What `tests/test_known_bad_corpus.py:131` requires of a sibling post-mortem**, verified directly
(line 131, `test_every_spec_has_a_sibling_postmortem_and_vice_versa`): the file must be named
`<slug>-POSTMORTEM.md` where `<slug>` matches the spec's own `<slug>-ANALYSIS-SPEC.yaml` filename
exactly — a set-symmetric-difference check, no content requirement beyond what
`test_every_postmortem_names_a_catch_attribution_finding_code` (line 176, Section 1 above) adds: the
text must contain at least one `DSX-<LETTERS>-<digits>` code. So
`examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml` needs a sibling
`examples/known-bad/triggering-dilution-POSTMORTEM.md` naming `DSX-INT-030` somewhere in its text —
the existing three post-mortems' structure (a "which absent code would have caught it" section) is
the idiom to copy, not a hard requirement of the test itself.

## 8. `GATE_PROFILES` registration

Read `dsx/cli.py:63-110` directly — **unchanged from `08-CONTEXT.md`'s citations**, because Phase
7's val-check registration (which would touch these same lines) has not landed yet:

```python
# dsx/cli.py:63-79
CHECKS: dict[str, Callable] = {
    "spec": validate_structure, "design": design.check, "stats": stats.check,
    "ml": ml.check, "metrics": metrics.check, "claims": claims.check, "viz": viz.check,
    "coherence": coherence.check, "dq": dq.check, "smells": smells.check,
    "figures": figures.check, "narrative": narrative.check, "code": code.check,
    "decision": decision.check, "paradigm": paradigm.check,
}

# dsx/cli.py:88-101
GATE_PROFILES: dict[str, tuple[str, ...]] = {
    "plan": ("spec", "design", "metrics", "coherence", "paradigm"),
    "execute": ("spec", "ml", "repro", "dq", "code", "paradigm"),
    "verify": ("spec", "design", "stats", "ml", "metrics", "claims", "viz", "repro",
               "dq", "coherence", "smells", "figures", "narrative", "code", "decision", "paradigm"),
    "ship": ("spec", "design", "stats", "ml", "metrics", "claims", "viz", "repro",
             "dq", "coherence", "smells", "figures", "narrative", "code", "decision", "paradigm"),
}

# dsx/cli.py:105-110
GATE_THRESHOLDS: dict[str, str] = {
    "plan": "CRITICAL", "execute": "CRITICAL", "verify": "HIGH", "ship": "HIGH",
}
```

Add `"interference": interference.check` to `CHECKS`, add `"interference"` to the `plan`, `verify`
and `ship` tuples (not `execute`, per D-03) — no change to `GATE_THRESHOLDS` needed, since the
existing CRITICAL/HIGH split at plan/verify already matches D-02's severity assignment.
`run_checks` (`dsx/cli.py:174-175`) needs no dispatch branch: `interference.check(spec)` takes only
`spec`, exactly like `paradigm.check(spec)`, and falls through the same generic branch
`CHECKS[name](spec)` Phase 7's research already verified requires zero special-casing.

**Reachability test — expressible and precedented, verified by reading the existing analogue**
(`tests/test_dsx.py:1583-1590`, `test_every_dsx_par_code_reachable_from_a_gate_profile`):

```python
def test_every_dsx_par_code_reachable_from_a_gate_profile(self):
    from dsx.cli import GATE_PROFILES
    from dsx.suppressions import known_codes

    par_codes = [c for c in known_codes() if c.startswith("DSX-PAR-")]
    self.assertTrue(par_codes, "expected at least DSX-PAR-001 to be known")
    reachable_checks = set().union(*GATE_PROFILES.values())
    self.assertIn("paradigm", reachable_checks)
```

`known_codes()` (`dsx/suppressions.py:24-40`, read in full) is an AST scanner over every `*.py` file
under `dsx/`, collecting the first argument of every `report.add(...)` call — it needs **no**
registration step of its own; any `DSX-INT-*` code Phase 8 emits is automatically discovered the
moment the `report.add("DSX-INT-0NN", ...)` call exists in source, regardless of gate-profile
wiring. The reachability test therefore only needs to assert `"interference"` is a member of *some*
`GATE_PROFILES` tuple, mirroring the PAR analogue exactly:

```python
def test_every_dsx_int_code_reachable_from_a_gate_profile(self):
    from dsx.cli import GATE_PROFILES
    from dsx.suppressions import known_codes

    int_codes = [c for c in known_codes() if c.startswith("DSX-INT-")]
    self.assertTrue(int_codes, "expected at least DSX-INT-010 to be known")
    reachable_checks = set().union(*GATE_PROFILES.values())
    self.assertIn("interference", reachable_checks)
```

This satisfies STATE.md's standing per-phase deliverable ("assert every new code is reachable from
at least one profile") with a direct, already-proven-pattern test, not new machinery.

**`_NOT_SHIPPED` atomicity, confirmed already primed for this phase:** `dsx/frame/paradigm.py:49-57`
(`_NOT_SHIPPED`, read in full) already contains
`"DSX-INT-": "Phase 8 ships DSX-INT-* (interference/SUTVA, triggering, dilution)."` — this entry
must be removed in the **same commit** as the first `report.add("DSX-INT-0NN", ...)` call, for the
identical mechanical reason Phase 7's research proved for `DSX-VAL-`
(`tests/test_dsx.py::test_applied_prefixes_have_codes_and_not_shipped_prefixes_have_none`, an
existing invariant test with no ordering that satisfies both its halves except a single atomic
commit). `_PARADIGM_INDEPENDENT` (`dsx/frame/paradigm.py:27-33`) **already lists `"DSX-INT-"`** too
— no edit needed there, confirming D-11's framing (Phase 8's checks are paradigm-independent) is
already encoded upstream and needs no new declaration.

---

## Architecture Patterns

### Recommended module shape

`dsx/frame/interference.py` mirrors `dsx/frame/paradigm.py` exactly, the same template Phase 7's
`dsx/frame/val.py` (planned, not yet built) follows:

```python
from __future__ import annotations

from ..decisions import DecisionRecord
from ..findings import Report
from ..mathx import <dilution function name>
from ..spec import (
    ANALYSIS_POPULATIONS, INTERFERENCE_MITIGATIONS, INTERFERENCE_RISKS, METRIC_TYPES,
    get, is_blank, is_placeholder_or_refusal, items, normalize, section,
)

_RISK_MITIGATION_MAP: "dict[str, frozenset[str]]" = { ... }   # D-05/D-07, this module's own
_ADDITIVE_METRIC_TYPES = frozenset({"count", "sum", "average"})
_RATIO_METRIC_TYPES = frozenset({"ratio", "rate"})


def check(spec: dict) -> Report:
    report = Report(check="interference")
    frame = section(spec, "validity_frame")
    if not frame:
        return report
    _check_interference_declared(frame, report)      # DSX-INT-010, DSX-INT-011
    _check_triggering_dilution(spec, frame, report)   # DSX-INT-030
    _check_stability_assessed(frame, report)          # DSX-INT-040
    return report
```

### System Architecture Diagram

```
ANALYSIS-SPEC.yaml (author-declared)
        │
        ▼
  dsx.loader.load()  ──► in-memory dict (already structurally validated by
        │                 dsx.spec.validate_structure() before any frame
        │                 check runs)
        ▼
  dsx gate <point>  ──► run_checks(spec, point)
        │                 (dsx/cli.py:135-182, dispatch by GATE_PROFILES[point])
        ▼
  interference.check(spec)
        │
        ├─► section(spec, "validity_frame") ──► absent/non-dict? return empty Report
        │
        ├─► _check_interference_declared(frame, report)
        │     reads .interference.{risk,mitigation,residual_note}
        │     risk != none AND mitigation == none AND residual_note blank/placeholder
        │       ──► DSX-INT-010 (CRITICAL, blocks plan)
        │     mitigation declared but not in _RISK_MITIGATION_MAP[risk]
        │       ──► DSX-INT-011 (CRITICAL, blocks plan)
        │
        ├─► _check_triggering_dilution(spec, frame, report)
        │     needs_causal_block gate (reused from dsx.spec, D-16)
        │     reads .triggering.{analysis_population,dilution_adjusted}
        │     + spec.metrics[].type (additive partition, D-11)
        │     eligible AND not dilution_adjusted AND any additive metric
        │       ──► DSX-INT-030 (CRITICAL, blocks plan)
        │     metric with undeclared type ──► skip + DecisionRecord (no finding)
        │
        └─► _check_stability_assessed(frame, report)
              reads .stability.{novelty_primacy_assessed,evidence}
              present AND (not True OR evidence blank)
                ──► DSX-INT-040 (HIGH, blocks verify/ship only)
        │
        ▼
  Report(findings=[...], context={"decisions": [...]})
        │
        ▼
  dsx/cli.py — merge with sibling checks' Reports, apply GATE_THRESHOLDS[point],
               write DecisionRecords to DECISIONS.jsonl, exit 0 or 1
```

A reader can trace the primary use case (a shared-budget interference declaration blocking `dsx
gate plan`) start to finish: spec file → loader → `run_checks` → `interference.check` →
`_check_interference_declared` → `DSX-INT-010` finding → `GATE_THRESHOLDS["plan"] == "CRITICAL"` →
non-zero exit.

### Anti-Patterns to Avoid

- **A second, near-duplicate placeholder helper.** Section 4 above — reuse
  `is_placeholder_or_refusal()`.
- **A second paradigm-read scanner parameterised by a hand-maintained module list.** Section 2 —
  the existing design is a directory glob; do not narrow it to a list "for clarity."
- **`is_blank()` alone for a boolean field.** Section 3 — `is_blank(False)` is `False`; boolean
  fields need an explicit `is not True` comparison, not the blankness helper.
- **A family-level string-prefix exclusion in the known-bad corpus once a family ships more than
  one code.** Section 1 — this is the concrete failure `DSX-INT-040` on the interference fixture
  demonstrates; the fix is the per-fixture map, not a finer prefix.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Placeholder/refusal-token detection for a free-text field | A second `is_placeholder()` regex | `dsx.spec.is_placeholder_or_refusal()` (already shipped, Section 4) | Two placeholder detectors in the same file will diverge on edge cases; one already exists and matches the template's exact placeholder shape |
| Dotted-path spec reading | Manual nested `.get()` chains | `dsx.spec.get(spec, "validity_frame.interference.risk")` | Already handles missing intermediate keys without raising, matching every other check in the codebase |
| Sub-block presence guard | A bespoke `isinstance` check per field | `dsx.spec.section(spec, name)` | One-line, already the idiom `_validate_validity_frame_shape` itself uses |
| Metrics enumeration | A custom loop over `spec.get("metrics", [])` with ad hoc type-filtering | `dsx.spec.items(spec, "metrics")` | Already filters non-mapping entries, matching `_validate_metrics`'s own enumeration |
| Decision-trail persistence | A bespoke JSON writer | `dsx.decisions.DecisionRecord` + `report.context.setdefault("decisions", [])` | The CLI layer's `collect_from_report()`/`_write_decision_trail` already own file I/O and ID assignment; a check must never write the file itself |

**Key insight:** every primitive Phase 8 needs to read a declaration and adjudicate it against a
closed set already exists in `dsx/spec.py`, most of it shipped before this phase's context was even
gathered. The actual net-new code this phase writes is the four check functions, one module
constant (the risk→mitigation map), one partition constant, one `mathx.py` function, and the
known-bad corpus's structural rewrite — not new infrastructure.

## Common Pitfalls

### Pitfall 1: Citing a stale line number from `08-CONTEXT.md`
**What goes wrong:** `08-CONTEXT.md` was gathered concurrently with Phase 7's plan 07-01 landing;
several of its `dsx/spec.py` line citations (e.g. `is_blank` "line 326", `_validate_metrics` "line
522", `_VALIDITY_FRAME_CAUSAL_REQUIRED`/`needs_causal_block` "lines 758-761") are now off by roughly
90 lines.
**Why it happens:** Phase 7's 07-01 plan inserted ~90 lines of falsifier-lexicon and structure→method
constants ahead of these locations.
**How to avoid:** this document's own citations were re-verified against the current file state
(Section headers above give the current, correct line numbers). The plan should locate helpers by
name in its action text, not by line number, so it survives whichever of Phase 7's remaining plans
(07-04 through 07-07) land before Phase 8 executes.
**Warning signs:** a `read_first` instruction pointing at a line range that, when read, contains
unrelated code.

### Pitfall 2: Treating `stability.novelty_primacy_assessed: false` as equivalent to "absent"
**What goes wrong:** a check written with `is_blank()` alone never fires on a real, present `false`
value — the exact value the template and the `interference-shared-budget` fixture both currently
declare (Section 3).
**Why it happens:** `is_blank()`'s contract (None/empty-string/empty-collection) doesn't cover
booleans by design — it wasn't written for boolean fields.
**How to avoid:** use `value is not True` for boolean-shaped declaration fields
(`novelty_primacy_assessed`, `dilution_adjusted`), not `is_blank(value)`.
**Warning signs:** a test asserting the good fixture's `novelty_primacy_assessed: true` doesn't fire
but the template's/known-bad fixtures' `false` also silently doesn't fire — a sign the check is
checking blankness, not truth.

### Pitfall 3: Growing `_INCIDENTAL_GAP_CODES` instead of fixing the fixture
**What goes wrong:** once `DSX-INT-040` exists, the family-prefix exclusion in
`test_incidental_allowlist_names_no_target_family_code` makes it *impossible* to add `DSX-INT-040`
to the old flat allow-list (Section 1) — a plan that tries will produce a red test with no legal fix
under the old structure, discovered only at execution time.
**Why it happens:** the corpus was designed around one code per family shipping at a time; Phase 8
is the first family to ship four codes in one phase, exposing the coarse-grained exclusion.
**How to avoid:** do the per-fixture rewrite (Section 1) before writing the fixture-firing tests, and
prefer fixing the `interference-shared-budget` fixture's stability declaration over documenting a
second incidental gap.
**Warning signs:** a red `test_incidental_allowlist_names_no_target_family_code` with no code change
that satisfies it under the current data structure.

### Pitfall 4: Assuming Phase 7's paradigm-read scanner exists
**What goes wrong:** a Phase 8 plan task that says "extend the existing
`TestFrameParadigmReadBoundary` class" will fail at execution time if Phase 7's 07-03 hasn't landed
yet — the class doesn't exist (Section 2).
**Why it happens:** both phases' context/research were gathered assuming a shared, symmetric
dependency, but only one phase's plan can land first, and as of this research pass neither has.
**How to avoid:** the plan task should check for the class's existence and branch (Section 2(d)),
not assume either ordering.
**Warning signs:** `python3 -m unittest tests.test_frame_boundary -v` failing with
`AttributeError`/`ImportError` rather than a assertion failure.

## Code Examples

### The `is not True` pattern for a boolean declaration field
```python
# Source: verified against templates/ANALYSIS-SPEC.yaml:321 and
# examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml:149, both real `false` values
assessed = get(frame, "stability.novelty_primacy_assessed")
if assessed is not True:
    # fires on False, None (absent), or any non-boolean garbage value alike
    ...
```

### The four-code dispatch shape, mirroring `dsx/frame/paradigm.py:60,78`
```python
# Source: dsx/frame/paradigm.py:60-78 (structure), adapted for this phase's four codes
def check(spec: dict) -> Report:
    report = Report(check="interference")
    frame = section(spec, "validity_frame")
    if not frame:
        return report
    _check_interference_declared(frame, report)
    _check_triggering_dilution(spec, frame, report)
    _check_stability_assessed(frame, report)
    return report
```

### The `DEPENDENCE_ADMISSIBLE_METHODS`-precedent shape for the additive/ratio partition
```python
# Source: dsx/spec.py:229 DEPENDENCE_ADMISSIBLE_METHODS (Phase 7, already shipped) — the
# structural precedent for a non-vocabulary constant referencing an existing vocabulary
_ADDITIVE_METRIC_TYPES = frozenset({"count", "sum", "average"})
_RATIO_METRIC_TYPES = frozenset({"ratio", "rate"})
assert _ADDITIVE_METRIC_TYPES | _RATIO_METRIC_TYPES <= METRIC_TYPES
```

## State of the Art

Not applicable in the usual sense — there is no prior implementation of this check family to
compare against; `dsx/frame/paradigm.py` (Phase 6) is the only shipped precedent and this document
already treats it as the template throughout.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The `interference-shared-budget` fixture should be edited (novelty_primacy_assessed: true + real evidence) rather than documented as a second incidental gap | 1 | If the planner prefers documentation instead, the per-fixture rewrite's allow-list structure needs a slightly different shape (per-fixture *set* of incidental codes, not just a target-code map) — a larger but still mechanical change |
| A2 | Whichever of Phase 7/8 lands first writes the paradigm-read scanner in full; the second phase adds no code, only a regression assertion | 2(d) | If both phases' plans independently write the full scanner, a merge produces a duplicate-class conflict requiring manual resolution — annoying but not silently wrong, since both designs are identical by construction |
| A3 | `is_placeholder_or_refusal()` should be reused as-is for `residual_note`, with only a docstring broadening, not a new function | 4 | If the planner disagrees and ships a second helper anyway, the two will very likely diverge in behaviour over time on refusal-token handling specifically, since only one of the two would carry it |
| A4 | The additive/ratio metric partition belongs in `dsx/frame/interference.py`, not `dsx/spec.py`, because (unlike Phase 7's structure→method map) no later phase is known to need it centrally | 5 | Low risk — moving a two-line constant later, if a future phase does need it, is a one-file edit with no data-shape change |

## Open Questions

1. **Whether `DSX-INT-040`'s collision on `interference-shared-budget` should be fixed by editing
   the fixture or documented per-fixture (A1 above).**
   - What we know: the fixture currently declares `stability.novelty_primacy_assessed: false` with
     a blank `evidence`, which will block `dsx gate ship` under `DSX-INT-040` once it ships,
     independent of the fixture's intended `DSX-INT-010` defect.
   - What's unclear: whether the corpus's stated single-defect guarantee should be read strictly
     (fix the fixture) or loosely (document the second gap, now that the per-fixture map can
     express it precisely).
   - Recommendation: fix the fixture (Section 1's recommendation) — it is the smaller edit, and it
     keeps the fixture's own post-mortem honest about what it demonstrates.

2. **Whether Phase 7 or Phase 8 lands first, and how the paradigm-read scanner is de-duplicated.**
   - What we know: neither has landed as of this research pass; both plans, if independently
     written, would specify an identical directory-glob design.
   - What's unclear: the exact git-merge mechanics if both phases' plans execute concurrently in
     separate worktrees, as `.claude/CLAUDE.md`'s parallel-subagent rules permit.
   - Recommendation: the Phase 8 plan should write its task defensively (check-then-branch, Section
     2(d)) rather than assume an ordering.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Python standard-library `unittest` (no pytest, no config file — confirmed, same finding as `07-RESEARCH.md`) |
| Config file | none |
| Quick run command | `python3 -m unittest tests.test_frame_interference -v` (new module, once created) |
| Full suite command | `python3 -m unittest discover -s tests -v` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| REQ-P8-01 | Declared risk with no mitigation and no residual note blocks; mitigated or residual-noted variant passes | unit (`interference.check(spec)` dict literal) + gate-level (copy-mutate temp fixture) | `python3 -m unittest tests.test_frame_interference -v -k risk` | ❌ new module needed |
| REQ-P8-02 | Shared-budget vs. marketplace distinct admissible mitigations; cross-applied mitigation still blocks | unit, table-driven over `_RISK_MITIGATION_MAP` | `python3 -m unittest tests.test_frame_interference -v -k mitigation` | ❌ new |
| REQ-P8-03 | Additive metric on eligible population with no dilution adjustment blocks; published counterexample asserted in `mathx` | unit (`mathx` function) + unit (`interference.check`) | `python3 -m unittest tests.test_dsx -v -k dilution` (mathx) + `tests.test_frame_interference -v -k triggering` | ❌ new (both) |
| REQ-P8-04 | `DSX-INT-030` does not fire on `type: ratio`; §6.5 row exists (doc-content test) | unit + documentation-content test (grep-style, precedent `test_no_planning_document_misattributes_the_prior_averaged_bound`, `tests/test_known_bad_corpus.py:292`) | `python3 -m unittest tests.test_frame_interference -v -k ratio_scope` + a new corpus-module doc test | ❌ new |
| REQ-P8-05 | Unassessed novelty/primacy flags at verify/ship, not plan; assessment method cited in docstring | unit + gate-level (threshold pinning, HIGH not CRITICAL) | `python3 -m unittest tests.test_frame_interference -v -k stability` | ❌ new |
| REQ-P8-06 | No `DSX-INT-*` path reads `inference.paradigm` | boundary scanner (Section 2) | `python3 -m unittest tests.test_frame_boundary -v` | ❌ Section 2 — may or may not exist depending on Phase 7 ordering |

### Sampling Rate

- **Per task commit:** targeted `python3 -m unittest tests.test_frame_interference -v -k <relevant>`
  plus `python3 scripts/gen-finding-catalogue.py --check` once any `report.add("DSX-INT-...")` exists.
- **Per wave merge:** `python3 -m unittest discover -s tests -v` (full suite, no slow/integration
  split in this repo — identical finding to `07-RESEARCH.md`).
- **Phase gate:** full suite green, `gen-finding-catalogue.py --check` green, the known-bad corpus
  rewrite (Section 1) landed, and the `interference-shared-budget` fixture's second-code collision
  resolved, before `/gsd-verify-work`.

### Wave 0 Gaps

- [ ] A new test module `tests/test_frame_interference.py`, mirroring `tests/test_frame_val.py`'s
      planned shape (07-03-PLAN.md) — does not exist yet.
- [ ] A `mathx.py` dilution function + its reference-value test (Deng & Hu counterexample) in the
      existing `TestMath` class — function and test both new.
- [ ] The per-fixture known-bad corpus rewrite (Section 1) — a **test-suite design gap**, shared
      with Phase 7, not merely a fixture gap; needs an explicit plan task.
- [ ] The paradigm-read scanner (Section 2) — may already exist depending on execution order; the
      plan needs a check-then-branch task, not an assumption either way.
- [ ] The `examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml` fixture + post-mortem — does
      not exist yet (confirmed: `examples/known-bad/` currently holds three pairs, none named
      `triggering-dilution`).

## Security Domain

`security_enforcement: true`, `security_asvs_level: 1` (`.planning/config.json:47-48`, confirmed
directly). Identical threat surface reasoning to `07-RESEARCH.md`'s own Security Domain section:
this module reads an already-validated in-memory dict, does string/dict comparisons against closed
sets, and writes only `Finding`/`DecisionRecord` objects. No network call, no subprocess, no dynamic
code execution, no external package.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | No auth surface — local CLI reading a local file |
| V3 Session Management | No | No session concept |
| V4 Access Control | No | No access-control surface |
| V5 Input Validation | Yes (narrow) | The spec dict is already structurally validated before any frame check runs; `interference.py` must still not crash on a malformed sub-block — reuse `section()`/`.get()`-with-default idioms rather than assuming presence, mirroring `dsx/spec.py:882` (`if not isinstance(frame, dict) or not frame`) |
| V6 Cryptography | No | No cryptographic operation in this phase |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| A malformed `interference`/`triggering`/`stability` sub-block (wrong type) crashes a check instead of degrading to a finding | Denial of Service (of the gate itself) | Type-check before attribute access on every sub-block read, mirroring `dsx/spec.py:882` and Phase 7's precedent test `test_malformed_validity_frame_shapes_degrade_to_dsx_spec_080_not_a_crash` — copy the shape for `interference`/`triggering`/`stability` specifically |
| A finding's `detail`/`remedy` text echoes attacker-controlled spec content with no escaping | Information disclosure (low severity — local CLI report) | Already the existing repo-wide idiom (`!r` repr); no new control needed |
| The dilution `mathx` function silently returning a plausible-but-wrong number if fed a `None`/out-of-range `trigger_rate` (it is never called from the gate path per D-09, but its own unit tests must still bound it) | Tampering (data integrity of a published-value test) | Explicit range validation in the function (mirroring `design_effect()`'s `if m < 1: raise ValueError`, `dsx/mathx.py:445-448`), so a malformed input raises rather than silently producing a number that looks like the Deng & Hu counterexample but isn't |

## Sources

### Primary (HIGH confidence — read directly this session)

- `dsx/spec.py` (958 lines total; read in full and by section — vocabularies, access helpers,
  falsifier/placeholder helpers, `_validate_metrics`, `_validate_validity_frame_shape`,
  `_VOCABULARIES`, `DEPENDENCE_ADMISSIBLE_METHODS`)
- `dsx/frame/paradigm.py` (163 lines, read in full) — module-shape template, `_NOT_SHIPPED`,
  `_PARADIGM_INDEPENDENT`
- `dsx/frame/__init__.py` (27 lines, read in full) — package docstring, no hardcoded module list
- `dsx/decisions.py` (213 lines, read in full) — `DecisionRecord`/`InvocationHeader` schema,
  `collect_from_report()`
- `dsx/cli.py:60-110` — `CHECKS`, `GATE_PROFILES`, `GATE_THRESHOLDS`, current (Phase 7 has not
  touched this file yet)
- `dsx/mathx.py:411-458` — `inflation_from_peeking()`, `design_effect()` (already shipped by Phase
  7's 07-01), the pure-function precedent
- `dsx/suppressions.py:1-40` — `known_codes()`, the AST-based `report.add` scanner
- `tests/test_frame_boundary.py` (126 lines, read in full) — current state, one test class only
- `tests/test_known_bad_corpus.py` (full structure read: lines 1-260) — `_INCIDENTAL_GAP_CODES`,
  `_TARGET_CODE_FAMILIES`, and the three affected tests, read directly
- `tests/test_dsx.py` (selected: 24-30, 1385-1450, 1520-1600) — `codes()` helper, copy-mutate idiom,
  `test_every_dsx_par_code_reachable_from_a_gate_profile`
- `templates/ANALYSIS-SPEC.yaml:280-338` — the full `validity_frame:` block including
  `interference`/`triggering`/`stability`
- `examples/good-ANALYSIS-SPEC.yaml`, `examples/bad-ANALYSIS-SPEC.yaml`,
  `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml` (relevant sections read
  directly, including the `stability` block that surfaces the `DSX-INT-040` collision)
- `scripts/gen-finding-catalogue.py:25-79` — `PREFIX_GROUPS`, `_D05_ALLOWLIST_PREFIXES`, the three
  regexes, current (unedited by any Phase 7 plan yet)
- `brief.md:364-390` — §6.5 gated backlog, confirmed to carry no existing ratio-dilution row
- `.planning/phases/07-validity-frame-checks-dsx-val/07-RESEARCH.md` (1238 lines, read in full) —
  the sibling phase's research; cited, not re-derived, per this document's instructions
- `.planning/phases/07-validity-frame-checks-dsx-val/07-CONTEXT.md` (read in full)
- `.planning/phases/07-validity-frame-checks-dsx-val/07-03-PLAN.md` (488 lines, read in full) —
  the exact planned shape of the paradigm-read scanner and the first `DSX-VAL-*` checks
- `.planning/phases/06-contract-extension-decision-record-paradigm-manifest/06-CONTEXT.md`
  (referenced via Phase 7's own citations; not separately re-read this session beyond what
  `07-RESEARCH.md`/`07-CONTEXT.md` already quote verbatim)
- `.planning/REQUIREMENTS.md:95-113`, `.planning/STATE.md` (read in full), `.planning/config.json`
  (workflow toggles) — read directly
- `git log`/`git status` on the working tree — confirmed Phase 7's actual execution state (07-01,
  07-02 landed; 07-03 through 07-07 not executed; `dsx/frame/val.py` absent)

### Secondary / Tertiary

None — every claim in this document is either read directly from the current repository state
(`[VERIFIED]`) or is this document's own reasoning about that state. No web search was performed:
the five external citations for this phase are locked and pre-verified per
`08-CONTEXT.md`'s `<already_researched_do_not_repeat>` instruction, and every other claim here is
implementation research grounded in the actual codebase, not literature.

## Metadata

**Confidence breakdown:**
- Codebase state (module shape, registration mechanics, current line numbers, Phase 7's actual
  execution progress): HIGH — every claim traced to a specific file read directly this session,
  cross-checked against `git log`/`git status` for execution state, not assumed from planning
  documents.
- The `DSX-INT-040`/`interference-shared-budget` fixture collision: HIGH — read directly from the
  fixture file; the arithmetic (declared `false` value → D-01's trigger condition as written) is
  mechanical, not inferred.
- The paradigm-read scanner's actual design (directory glob, not module list): HIGH — read directly
  from `07-03-PLAN.md`'s action text, which is unambiguous on this point.
- The known-bad corpus rewrite's proposed concrete shape (Section 1): MEDIUM — the *problem* is
  HIGH confidence (read directly), the *proposed data structure* is this document's own design,
  consistent with but not dictated by Phase 7's research, and the planner should treat it as a
  strong starting point rather than a locked shape.
- `is_placeholder_or_refusal()` reuse recommendation: HIGH for the collision (the function exists
  and does what D-08 asks); MEDIUM for whether reuse-with-docstring-broadening is preferable to a
  differently-named wrapper, which is genuinely Claude's Discretion.

**Research date:** 2026-08-12
**Valid until:** Tied to the exact state of the repository at the time of this research (Phase 7:
07-01 and 07-02 landed, 07-03 through 07-07 not executed; `dsx/frame/` contains only `paradigm.py`).
Re-verify every line-number citation in this document if any further Phase 7 plan lands before
Phase 8 executes — several sections above already had to correct `08-CONTEXT.md`'s own citations
for exactly this reason.
