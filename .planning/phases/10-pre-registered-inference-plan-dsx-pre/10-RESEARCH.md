# Phase 10: Pre-registered inference plan (`DSX-PRE-*`) - Research

**Researched:** 2026-08-13
**Domain:** A hand-written mini-language parser plus a decision-trail reconciliation check, added to an
existing Python gate-check package (`dsx/frame/`). Not an analysis phase — no dataset, model or chart.
**Confidence:** HIGH for everything grounded in direct code reads (all nine research targets below);
MEDIUM for the two open design questions (mini-language grammar shape, multiple-plan-header rule) where
I am recommending rather than reporting a locked fact.

## Summary

Phase 10 adds one new module, `dsx/frame/prereg.py`, carrying three finding codes
(`DSX-PRE-010/020/030`) registered only at the `verify` and `ship` gate points. Two of the phase's four
hardest pieces are already built and just need to be *read*, not written: the content lock
(`frame_digest()`) and the free-string comparison fix (`normalize()`) both shipped in Phase 6. The
third piece — a fallback-rule mini-language — is genuinely new; no parser of any kind exists in this
codebase today. The fourth piece — threading the project root into a frame check so it can read
`DECISIONS.jsonl` — has four direct precedents (`dq`, `claims`, `figures`, `narrative`) in
`dsx/cli.py::run_checks`.

The single highest-value finding from this research is **not** in the four requirements themselves: it
is that the existing test harness will break the moment `prereg` is registered at `verify`/`ship`.
`tests/test_known_bad_corpus.py::_gate_findings()` creates a brand-new, empty temporary directory for
every single gate call, so a `verify` or `ship` call made through that helper never has a prior `plan`
call in the same directory — meaning `prereg.check()` will raise `CheckError` (exit 2) against *every*
known-bad fixture the first time this test suite runs after `prereg` ships, not just against a
newly-added fixture. I traced this by reading the helper and then reproduced the underlying failure
mode empirically (below): a raised `CheckError` prints plain text to stderr, bypassing the JSON emitter
entirely, so the test helper's `json.loads(raw)` call will itself throw `json.JSONDecodeError` rather
than a clean assertion failure. This must be fixed in the same commit that registers `prereg`, or
several pre-existing tests (not just the new prereg tests) go red for a reason that has nothing to do
with the fixture the failure is nominally about.

Separately, I found and corrected several line-number citations in `10-CONTEXT.md` that point to the
wrong test, or to comment prose rather than the code/dict they describe (see **Corrections to
10-CONTEXT.md** below) — none of these change any locked decision, but the planner will cite these
lines directly and the actual lines differ from what is written there.

**Primary recommendation:** build the mini-language as a single-condition, no-`else`, stdlib-`re`
parser where the RHS of `->` is truncated at the first comma to get the branch label, and treat
`inference.primary_procedure` as the implicit "else" branch — this satisfies all four requirements
without inventing `else` syntax the brief never asked for. Fix `_gate_findings()`'s missing-plan-header
gap in the same landing commit as the `GATE_PROFILES` edit, before writing any new prereg-specific test.

## User Constraints (from CONTEXT.md)

### Locked Decisions

Sixteen phase-local decisions (D-01 through D-16) are locked in `10-CONTEXT.md` and are **not**
re-litigated here. Load-bearing ones this research directly touches, verified against the running code
during this session:

- **D-01**: the mini-language triggers only on the literal `->` substring in `fallback_rule`. No
  `if`-prefix trigger (would over-match six of the eight existing prose values).
- **D-02**: exit 2 is produced only by raising `CheckError` from inside the check. No finding-based
  route exists — `Report.exit_code()` returns only `EXIT_BLOCK`/`EXIT_PASS`
  (`dsx/findings.py:181-182`, verified).
- **D-03**: `CheckError` aborts the whole gate run and prints no findings — accepted, not a defect to
  route around.
- **D-04**: the mini-language coins no new contract field. Its fact namespace is a closed, tested
  registry of fields that already exist. Candidates: `results.observed_n`, `results.interim_looks`,
  `results.comparisons_looked_at`, `design.alpha` — **verified below**, membership narrowed.
- **D-05**: declared side is `inference.primary_procedure`; executed side is `analysis.test`; both
  free strings compared via the shipped `normalize()` (`dsx/spec.py:409-410`).
- **D-06**: no importable procedure vocabulary; `dsx/frame/` may not import `dsx.checks`
  (`dsx/frame/__init__.py:16-31`, D-03a boundary, mechanically enforced by
  `tests/test_frame_boundary.py`).
- **D-07**: REQ-P10-03 and REQ-P10-04 are one code (`DSX-PRE-030`) with two fixtures, not two codes.
- **D-08**: the plan-time content lock (`frame_digest()`, `dsx/decisions.py:181-190`) already ships;
  Phase 10 reads it, does not build it. **Correction below**: the claim that this reaches a *committed*
  artifact is wrong — see Corrections section.
- **D-09**: `prereg.check` needs a `root` argument via a new `elif` branch in `run_checks`
  (precedent: `dq`, `code`, `figures`, `narrative`). A `verify` run with no recorded `plan` header exits
  `2`. This collides with the M-07 grandfather path; the exit-2 message must name `suppressions[]`.
- **D-10**: `declared_at: post_data` stays legal and silent; documented, not blocked.
- **D-11**: new `dsx/frame/prereg.py`, registered as `CHECKS["prereg"]` and in `GATE_PROFILES["verify"]`
  / `GATE_PROFILES["ship"]` only, at `CRITICAL`.
- **D-12**: three codes, `DSX-PRE-010/020/030`, `-011` deliberately unspent.
- **D-13**: five guards go red in the landing commit (`_NOT_SHIPPED`, `_PARADIGM_INDEPENDENT`,
  `PREFIX_GROUPS`, `_D05_ALLOWLIST_PREFIXES`, the pinned code-set test) — **all five verified below,
  two with corrected line numbers**.
- **D-14**: citation anchor is Gelman & Loken (2014), `Structural criterion:` not `Reference value:`.
  Three live, unverified locators (φ's OCR garbling, no numbered sections, Nosek's per-sentence pages)
  must stay flagged, never smoothed into confident citations.
- **D-15**: no published number is asserted for `DSX-PRE-*`.
- **D-16**: one new known-bad fixture, per-gate-point map shape (`{"verify": "DSX-PRE-030"}`), plus an
  empty-frozenset entry in `_EXPECTED_CAUGHT_DEFECTS`.

### Claude's Discretion

Per `10-CONTEXT.md`, these are open for the researcher/planner to settle without returning to discuss:

- Plan slicing across the four requirements (no atomicity constraint).
- The exact grammar of the mini-language beyond the `->` trigger (comparison operators, multiple
  conditions, `else` branch expressibility).
- The final membership of D-04's fact registry.
- Where the fact registry is surfaced to an operator (`dsx vocab`, README, or both).
- Whether `DSX-PRE-020` compares against the most recent or the earliest `plan` header.
- The exact `elif` shape for threading `root` into `prereg.check`.
- Whether the paradigm-independence test is source-level or behavioural.

I address every one of these below with a concrete recommendation and the evidence behind it.

### Deferred Ideas (OUT OF SCOPE)

- Coining `results.clusters` or a `results:` shape validator.
- `DSX-PRE-011` for "rule references an unknown fact" as a distinct code.
- Procedure ranking, admissibility, conservatism ordering (Phase 11's `DSX-ADM-*`).
- Asserting a published number for `DSX-PRE-*`.
- Obtaining Chan et al. (2004) full text, or a natively-typeset Gelman & Loken copy.
- Making `analysis.test` structurally post-data.

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-P10-01 | Fallback rule in the mini-DSL parses to a decidable branch; unparseable rule exits `2` | Target 1 (grammar), Target 3 (exit-2 mechanics) below |
| REQ-P10-02 | `declared_at` provenance recorded and its limits documented — not presented as a guarantee | Target 4 (root threading), README anchor confirmed at `README.md:309`/`:338` |
| REQ-P10-03 | Executed procedure differs from selected branch → blocked, both branches named | Target 1 (grammar), Target 2 (fact registry), module idiom (Target 8) |
| REQ-P10-04 | Post-hoc switch blocks even when the substitute is individually defensible (fixture-only proof) | Target 7 (fixture/corpus structure) |

## Project Constraints (from CLAUDE.md)

- **Shell**: Windows/PowerShell. All commands in this research were run through the Bash tool's
  Git-Bash POSIX layer; the planner's task actions should assume PowerShell unless a script file is
  written.
- **Line endings**: repo checks out CRLF. Any new regex or text scan the planner specifies for
  `prereg.py` or its tests must tolerate `\r\n`, matching the existing house rule
  (`tests/test_known_bad_corpus.py` already normalizes whitespace before substring checks, e.g. lines
  570-584).
- **Verification before claiming**: every line-number citation in this document was read directly this
  session (tool calls shown in the corrections section below); nothing is carried over from
  `10-CONTEXT.md` without an independent re-read.
- **Tool version grounding**: N/A — this phase adds no new external tool config.

---

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Fallback-rule parsing (mini-language) | API / Backend (gate-check layer) | — | Pure text parsing against a closed fact registry; no I/O, no network, runs inside `dsx/frame/prereg.py` |
| Fact resolution against declared observed values | API / Backend | Database / Storage (reads `spec` dict already loaded from YAML) | The registry reads already-parsed spec fields; no new persistence |
| Content-lock reconciliation (`DSX-PRE-020`) | API / Backend | Database / Storage (`DECISIONS.jsonl` on disk) | `frame_digest()` and `DECISIONS.jsonl` already exist; this check is a read-and-compare, not a new store |
| Declared-vs-executed procedure reconciliation (`DSX-PRE-030`) | API / Backend | — | Compares two already-loaded string fields; no external call |
| Exit-code contract (`0`/`1`/`2`) | API / Backend (CLI process exit code) | — | Consumed by GSD's `command-exit-zero` gate convention, external to this phase |
| Operator-facing fact-registry discovery | CLI / Static (dsx vocab JSON dump, README prose) | — | Read-only discovery surfaces, no runtime component |

This is a single-tier phase: everything lives inside the `dsx` Python package's gate-check layer. There
is no browser, no server-rendering, no CDN concern. The only "storage" touched is a local, per-project
JSON-Lines file (`DECISIONS.jsonl`) that already exists and is already written; Phase 10 is the first
phase to *read* it as a gate input rather than treating it as a write-only side channel.

---

## Corrections to 10-CONTEXT.md

The evidence-discipline instructions require flagging any citation that turns out wrong rather than
carrying it forward silently. I re-read every code citation touched by the nine research targets. Two
categories of correction follow.

### 1. `examples/DECISIONS.jsonl` is not committed (corrects D-08's provenance claim)

D-08 states: *"the committed `examples/DECISIONS.jsonl` proves it in the artifact."* I checked this
directly:

```
git check-ignore -v examples/DECISIONS.jsonl
  .gitignore:7:DECISIONS.jsonl	examples/DECISIONS.jsonl
git ls-files examples/DECISIONS.jsonl        -> (empty, not tracked)
git log --all --oneline -- examples/DECISIONS.jsonl -> (empty, no history ever)
```

`.gitignore` line 7 is the bare pattern `DECISIONS.jsonl`, which matches this file everywhere including
under `examples/`. The file on disk right now has **8,487 lines / 1,033 invocation headers** — it is a
purely local accumulation from repeated `python -m unittest`/`./bin/dsx gate` runs that omit
`--phase-dir` (several do — see the harness-blast-radius finding below), not a committed fixture. This
does not undermine D-08's core claim (`frame_digest()` genuinely is written on every gate run, and I
independently reproduced that — see Target 5 below), but the specific evidentiary claim about a
*committed* artifact is false, and the planner should not cite `examples/DECISIONS.jsonl` as a stable,
version-controlled fixture. It is gitignored working-directory noise that happens to prove the
mechanism works, not a checked-in proof artifact.

### 2. Three test line-number citations point to the wrong location

| CONTEXT citation | Claim | What is actually there | Correct location |
|---|---|---|---|
| `tests/test_dsx.py:1390-1393` | "the template still passes `dsx gate plan`" | `test_good_fixture_passes_every_gate` — iterates gate points for `examples/good-ANALYSIS-SPEC.yaml`, not the template | `test_template_validity_frame_and_inference_pass_gate_plan`, **lines 1586-1589** |
| `tests/test_dsx.py:2830-2834` | the `_PARADIGM_INDEPENDENT` "applied prefix resolves to a known code" assertion | loop *setup* (`from dsx.suppressions import known_codes` / `known = known_codes()` / `for declared in ...`), not the assertion itself | The assertion is at **lines 2838-2842**; the whole test method (`test_applied_prefixes_have_codes_and_not_shipped_prefixes_have_none`) runs **lines 2811-2858**, with a `# D-05: DSX-PAR-001` marker comment at **line 2810** |
| `tests/test_dsx.py:2849-2850` | the `_NOT_SHIPPED` invariant (`for prefix in paradigm._NOT_SHIPPED: assertFalse(...)`) | line 2849 falls inside an unrelated f-string inside the *previous* loop | The actual `_NOT_SHIPPED` loop is **lines 2857-2858** |
| `tests/test_frame_interference.py:169-185` | "the registration + reachability test pair" | lines 169-177 are inside `TestNeedsCausalBlock`, an unrelated class; only 180-185 overlaps the real target | `test_interference_registered_in_plan_verify_ship_absent_from_execute` is **lines 181-188**; `test_every_dsx_int_code_reachable_from_a_gate_profile` is **lines 190-196** |
| `tests/test_known_bad_corpus.py:243-253` | comment stating "neither shape subsumes the other" | that exact phrase does not appear in lines 243-253 | The phrase is at **line 271**, inside the comment block spanning lines 246-277 |
| `tests/test_known_bad_corpus.py:259-265` | `_EXPECTED_CAUGHT_DEFECTS` dict definition | lines 259-265 are still comment prose | The dict itself is defined at **lines 278-284** |
| `tests/test_known_bad_corpus.py:270-326` | "post-mortem invariants" | lines 270-326 are actually `_EXPECTED_CAUGHT_DEFECTS` plus `_effective_target_map()`/`_own_target_codes()` helpers | The post-mortem/catch-attribution invariant tests are `test_every_postmortem_names_a_catch_attribution_finding_code` (**lines 400-409**), `test_ship_gate_findings_are_all_documented_incidental_corpus_gaps` (**lines 468-509**), `test_incidental_allowlist_names_no_slugs_own_target_code` (**lines 511-529**) |

Everything else CONTEXT cites in the guard list (`dsx/frame/paradigm.py:47` and `:66`,
`scripts/gen-finding-catalogue.py:25-52`/`:65`, `tests/test_gen_finding_catalogue.py:174-181`/`:227`,
`templates/ANALYSIS-SPEC.yaml:355`/`:358`, `dsx/cli.py:90-103`/`:107-112`/`:156-177`/`:288-290`,
`dsx/findings.py:23`/`:181-182`, `dsx/cli.py:763`/`:766` [CONTEXT's "765"/"768" name the `return
EXIT_ERROR` lines one line below the `except` clauses — both resolve to the same two statements]) was
independently re-read this session and is **accurate**.

### 3. New finding not in CONTEXT: the corpus test harness will break at ship/verify

Neither of the two locked line-citation corrections above changes a decision. This one is a genuine gap
CONTEXT does not name, and it needs to land in the same commit as the `GATE_PROFILES` edit — see
**Common Pitfalls, Pitfall 1** below for the full evidence and the fix.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python stdlib `re` | 3.x (bundled) | Parses the `fallback_rule` mini-language | Brief D-01 forbids any third-party dependency on the gate path; `re` plus `operator` is the entire toolkit needed |
| Python stdlib `operator` | 3.x (bundled) | Maps `<`, `<=`, `>`, `>=`, `==`, `!=` tokens to comparison callables | Avoids a hand-rolled if/elif chain for six operators |

No new library is installed by this phase. `dsx/decisions.py` (the content lock and the reader) and
`dsx/spec.py` (`normalize()`, `get()`, `as_number()`) are both already-shipped, stdlib-only modules this
phase imports and does not modify except to add the new fact-registry constant (see Target 2 below).

### Supporting

None. This phase's "supporting" layer is entirely house code already shipped in Phase 6/7/8/9.

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Hand-written `re`-based parser | A grammar library (`pyparsing`, `lark`) | Forbidden outright by brief D-01 (stdlib only on the gate path); would also be substantial overkill for a single-condition if/then |
| `_FACT_REGISTRY` as a Python dict in `spec.py` | A registry co-located in `prereg.py`, merged into `dsx vocab`'s output at the CLI layer | Both are viable (see Target 2); I recommend the `spec.py` placement because it matches the existing `_INFERENCE_FIELDS`/`inference_fields` precedent exactly and avoids adding new special-case logic to `cmd_vocab` |

**Installation:** none required.

**Version verification:** not applicable — no external package is added.

## Package Legitimacy Audit

Not applicable. This phase installs no external packages (brief D-01, stdlib only, verified against
`dsx/decisions.py`'s own docstring: *"Stdlib only (D-01): a decision trail is worthless if the gate that
would emit it can't run because a dependency is missing"*). No `npm view`/`pip index`/`cargo search`
check is meaningful here.

**Packages removed due to SLOP verdict:** none — no packages proposed.
**Packages flagged as suspicious (SUS):** none.

---

## Architecture Patterns

### System Architecture Diagram

```
ANALYSIS-SPEC.yaml (operator-authored)
        |
        v
  dsx.loader.load()  ->  spec: dict
        |
        v
  dsx gate verify | dsx gate ship
        |
        v
  run_checks(spec, GATE_PROFILES[point], ..., gate_point=point, resolve_root=root)
        |
        |-- elif name == "prereg":  prereg.check(spec, root)   <-- NEW branch (D-09)
        |         |
        |         |-- 1. read DECISIONS.jsonl via decisions.read_all(decisions_path(root))
        |         |      -> find prior "plan"-gate_point InvocationHeader(s)
        |         |      -> no header at all?  raise CheckError -> exit 2 (D-09)
        |         |
        |         |-- 2. parse inference.fallback_rule (if it contains "->")
        |         |      -> grammar-invalid?      raise CheckError -> exit 2 (D-02)
        |         |      -> fact not in registry? DSX-PRE-010 finding (not exit 2, D-04)
        |         |      -> resolves cleanly?     branch label determined
        |         |
        |         |-- 3. DSX-PRE-020: recorded plan-time frame_digest(spec)
        |         |      vs current frame_digest(spec) bytes, only when
        |         |      declared_at: pre_data is asserted
        |         |
        |         |-- 4. DSX-PRE-030: normalize(resolved_branch) vs
        |         |      normalize(analysis.test) -- names both labels in `detail`
        |         |
        |         `-- returns Report with 0-3 findings + DecisionRecord entries
        |
        v
  merge(...) -> apply_suppressions(spec, merged)   <-- unrelated CheckError route (unknown suppression code)
        |
        v
  report.exit_code(threshold)  ->  0 | 1
        |                          (2 only ever comes from a CheckError caught in main(), never from here)
        v
  _write_decision_trail(report, spec, root, point, verbose)   <-- appends THIS run's own "verify"/"ship"
        |                                                          header AFTER prereg already read the
        |                                                          prior "plan" header -- no race (see
        |                                                          Target 5 evidence)
        v
  emit(report, threshold, json, verbose)  ->  process exit code
```

### Recommended Project Structure

No new directories. One new file:

```
dsx/
├── frame/
│   ├── prereg.py        # NEW — DSX-PRE-010/020/030, this phase's only new module
│   ├── val.py            # unmodified — module idiom to copy
│   ├── interference.py   # unmodified — module idiom to copy
│   └── paradigm.py       # _NOT_SHIPPED and _PARADIGM_INDEPENDENT edited (D-13)
├── cli.py                 # GATE_PROFILES, CHECKS, run_checks edited (D-09, D-11)
└── spec.py                 # _FACT_REGISTRY constant added (Target 2 recommendation);
                             # describe_vocabulary() gains a third special case
```

---

## Research Target 1 — The mini-language grammar and parser

**No mini-language parser precedent exists anywhere in this codebase.** I grepped `dsx/spec.py`,
`dsx/decisions.py` and every `dsx/frame/*.py` module for `def parse` and `re.compile` — the only
existing regexes are `_PLACEHOLDER_RE` (angle-bracket placeholder detection) and `_FALSIFIER_NUMBER_RE`
(detects a bare number in falsifier text), neither of which is a condition/branch parser. `prereg.py`'s
parser is genuinely new code, not an adaptation of an existing pattern.

**The worked example that must parse** (`brief.md:204-205`, quoted in ROADMAP SC 1):
`if clusters < 30 -> wild cluster bootstrap, 9999 reps, seed 42`

Three structural observations from this one example, each of which shapes the grammar:

1. The condition is `<fact> <operator> <number>`, optionally prefixed with the word `if`. Since D-01
   already established that only the literal `->` triggers mini-language mode (not an `if`-prefix), the
   `if` token inside the condition can be treated as optional cosmetic sugar, stripped if present, never
   required.
2. The right-hand side is **not** a bare branch label — it is `wild cluster bootstrap, 9999 reps, seed
   42`, a label followed by comma-separated free-text annotation (reps, seed) that has no home in the
   contract and is not meant to be compared against anything. `normalize()`
   (`dsx/spec.py:409-410`, `str().strip().lower().replace("-","_").replace(" ","_")`) does not strip
   commas or digits, so naively normalizing the whole RHS would produce
   `wild_cluster_bootstrap,_9999_reps,_seed_42`, which would never match a clean
   `primary_procedure: wild_cluster_bootstrap` value. **Recommendation: split the RHS on the first
   comma; the branch label is everything before it, trimmed.** This is the smallest rule that makes the
   worked example resolve to a comparable label without inventing new structured fields for the
   annotation.
3. Nothing in the four requirements needs multiple conditions or an explicit `else`. I traced this
   through D-04/D-05 directly: **`inference.primary_procedure` can serve as the implicit "else"
   branch.** When `fallback_rule` contains `->` and its condition evaluates false against the declared
   facts, the "resolved branch" for `DSX-PRE-030`'s comparison purposes is simply
   `primary_procedure` — the same value the check already uses when no arrow-form rule exists at all
   (per D-05: *"the declared side is `inference.primary_procedure`"*). This gives "resolves to exactly
   one branch" real content without a second `->` clause: the branch is the fallback label when the
   condition holds, and `primary_procedure` when it does not. "Resolves to zero branches" is then
   reserved for exactly the case D-04 already names — the fact referenced is outside the closed
   registry. I did not find any way for a single-condition grammar to resolve to *more than one* branch,
   which is consistent with the brief's own single worked example never showing one.

**Recommended smallest grammar (stdlib-only, matching brief D-01):**

```python
import re
import operator as _operator

_ARROW = "->"
_CONDITION_RE = re.compile(
    r"^\s*(?:if\s+)?(?P<fact>[A-Za-z_][A-Za-z0-9_]*)\s*"
    r"(?P<op><=|>=|==|!=|<|>)\s*"
    r"(?P<value>-?\d+(?:\.\d+)?)\s*$"
)
_OPS = {
    "<": _operator.lt, "<=": _operator.le,
    ">": _operator.gt, ">=": _operator.ge,
    "==": _operator.eq, "!=": _operator.ne,
}

def _parse_fallback_rule(text: str):
    """Returns None if `text` is not a mini-language rule at all (D-01: no
    `->`, so no finding, no error). Raises CheckError if `->` is present but
    the left-hand side does not match the condition grammar (D-02: exit 2).
    Returns (fact_name, op_symbol, threshold, branch_label) on success."""
    if _ARROW not in text:
        return None
    lhs, _, rhs = text.partition(_ARROW)
    match = _CONDITION_RE.match(lhs)
    if not match:
        raise CheckError(
            f"unparseable fallback_rule condition: {lhs.strip()!r} "
            f"(expected '<fact> <op> <number> -> <branch>')"
        )
    branch = rhs.split(",", 1)[0].strip()
    if not branch:
        raise CheckError("fallback_rule has an arrow but no branch label after it")
    return match["fact"], match["op"], float(match["value"]), branch
```

This is a sketch, not a locked artifact — I have not written `prereg.py`, since it does not exist yet.
The planner should treat the RHS-comma-split rule and the implicit-`primary_procedure`-else rule as my
strongest recommendation (grounded directly in D-04/D-05's stated field semantics), and the exact
regex/operator table as illustrative of "the smallest thing that satisfies all four requirements," not
as a locked interface.

## Research Target 2 — The fact registry (D-04)

I verified each of CONTEXT's four candidate fields against the actual fixture that reaches `verify`
(`examples/good-ANALYSIS-SPEC.yaml`), the template, and every known-bad fixture:

```
grep -n "observed_n|interim_looks|comparisons_looked_at|^\s*alpha:" \
  examples/good-ANALYSIS-SPEC.yaml templates/ANALYSIS-SPEC.yaml examples/known-bad/*.yaml examples/bad-ANALYSIS-SPEC.yaml
```

| Candidate | Dotted path | Type | Populated in `good-ANALYSIS-SPEC.yaml`? | Recommendation |
|---|---|---|---|---|
| `alpha` | `design.alpha` | scalar float | Yes — `0.05` (line 135) | **Include.** Read via `design.py:452` today (`design.get("alpha")`), confirming it is a real, consumed field, not dead contract surface. |
| `interim_looks` | `results.interim_looks` | scalar int | Yes — `1` (line 220) | **Include.** Already consumed by `design.py:446` (`_check_peeking`). |
| `comparisons_looked_at` | `results.comparisons_looked_at` | scalar int | Yes — `3` (line 221) | **Include.** Already consumed by `design.py:407` (`_check_exploratory_looks`). |
| `observed_n` | `results.observed_n` | **list**, not scalar (per-arm counts, e.g. `[9206, 9181]`) | Yes, but as a list | **Exclude, or define a derived scalar explicitly.** A bare `clusters < 30`-style comparison has no obvious meaning against a list. Including it as-is would force the mini-language to invent list semantics (`min()`? `sum()`? first element?) that none of the four requirements need and that the brief's own `clusters` example (itself unbound to any real field — see D-04) does not clarify. |

`templates/ANALYSIS-SPEC.yaml` scaffolds all four with either a real default (`alpha: 0.05`) or an
explicit `null`/`[]` placeholder and an inline comment — none of them are silently absent from the
contract shape, matching D-04's framing that the registry draws from fields that "already exist," not
from the brief's illustrative `clusters` name.

**Recommendation: a three-member registry — `alpha`, `interim_looks`, `comparisons_looked_at` — all
scalar, all confirmed populated in the fixture that reaches `verify`.** Excluding `observed_n` is a
scope-discipline call: nothing in REQ-P10-01 through REQ-P10-04 requires it, and forcing a list into
scalar semantics is exactly the kind of speculative structure `references/families.yaml`'s exclusion
(brief §6.6) warns against for this phase.

**Where the registry lives (open in CONTEXT, my recommendation):** define it as a plain Python dict in
`dsx/spec.py`, next to `DECLARATION_POINTS`:

```python
# dsx/spec.py, alongside DECLARATION_POINTS
_PREREG_FACTS: "dict[str, str]" = {
    "alpha": "design.alpha",
    "interim_looks": "results.interim_looks",
    "comparisons_looked_at": "results.comparisons_looked_at",
}
```

Then `dsx/frame/prereg.py` imports `_PREREG_FACTS` (or a renamed public constant) from `..spec`, exactly
as `paradigm.py` imports `PARADIGMS`/`PARADIGM_JUSTIFICATIONS` and `val.py` imports
`DEPENDENCE_ADMISSIBLE_METHODS`/`IDENTIFICATION_STRENGTHS`. I recommend this placement over defining the
registry inside `prereg.py` itself, for two concrete reasons:

1. It matches the *exact* existing precedent for "a closed namespace of field names, not values":
   `_INFERENCE_FIELDS` (`dsx/spec.py:984-988`) plus its `inference_fields` special case inside
   `describe_vocabulary()` (`dsx/spec.py:1077-1096`, confirmed by direct read) exists for precisely the
   same reason — *"there is no unknown-key check under `inference:`... `dsx vocab` and the template
   scaffold are the only two mechanisms by which an operator can discover or correct a misspelled field
   name."* The fact registry is the same shape of problem one layer down.
2. It avoids a circular import: `dsx/spec.py` is a low-level module loaded before `dsx/frame/`; having
   `spec.py`'s `describe_vocabulary()` import `_FACT_REGISTRY` *from* `dsx/frame/prereg.py` would create
   an import cycle the moment `prereg.py` itself imports from `dsx.spec` (which it must, for `get()` and
   `as_number()`). Defining the registry in `spec.py` and importing it *into* `prereg.py` is the only
   direction that does not cycle.

This does **not** violate D-04 ("no new contract field is coined"): a Python lookup dict mapping short
names to already-existing dotted paths is not a field a user declares in YAML — it is exactly the same
kind of internal constant `_VOCABULARIES`, `_INFERENCE_MEMBERSHIP` and `DECLARATION_POINTS` already are.

**Surfacing to the operator (my recommendation, addressing the second open discretion item):** add a
third special case to `describe_vocabulary()` (`dsx/spec.py:1077-1096`), alongside the existing
`chart_capabilities` and `inference_fields` cases:

```python
out["prereg_facts"] = dict(sorted(_PREREG_FACTS.items()))
```

`dsx vocab` (`cmd_vocab`, `dsx/cli.py:401-403`) then dumps it for free — no CLI-layer edit needed. I
also recommend a short new subsection under README's existing `## Known limits` (confirmed at
`README.md:309`) — no subsection near `### Two tiers of evidentiary rigour` (`README.md:338`) currently
mentions `fallback_rule`, `declared_at` or `primary_procedure` at all (grep returned zero matches), so
this is new prose, not an edit to existing text.

## Research Target 3 — Exit 2 mechanics

**Confirmed exactly as CONTEXT states, with corrected line pinpointing.** `Report.exit_code()`
(`dsx/findings.py:181-182`) returns only `EXIT_BLOCK` (1) or `EXIT_PASS` (0) — there is no code path
from `report.add(...)` at any severity to exit 2. `EXIT_ERROR = 2` (`dsx/findings.py:23`) is returned in
exactly two places, both inside `main()`'s exception handlers:

```python
# dsx/cli.py:758-770
def main(argv=None):
    ...
    try:
        return int(args.func(args))
    except (CheckError, SpecParseError) as exc:   # line 763
        print(f"dsx: {exc}", file=sys.stderr)
        return EXIT_ERROR                          # line 765
    except ValueError as exc:                      # line 766
        print(f"dsx: invalid input — {exc}", file=sys.stderr)
        return EXIT_ERROR                           # line 768
```

`require(condition, message)` (`dsx/findings.py:210-213`) is a thin, already-shipped convenience wrapper
around `raise CheckError(message)`. **It is not currently used anywhere in the codebase** — I grepped
for `require(` across `dsx/` and found only its own definition. `apply_suppressions`
(`dsx/suppressions.py:160-221`) is the one working precedent, and it raises `CheckError` directly rather
than via `require()`:

```python
# dsx/suppressions.py:174-181
if code and code not in known:
    raise CheckError(f"spec.suppressions[{index}].code {code!r} is not a known DSX finding code")
```

`run_checks` (`dsx/cli.py:137-184`) has **no try/except around any individual check call** — an
exception raised inside `prereg.check()` (or any `elif` branch) propagates straight up through
`run_checks` -> `cmd_gate` -> `main()`'s handler, unmodified. I confirmed this is also true of
`apply_suppressions`, which is called at the very end of `run_checks` (`return
apply_suppressions(spec, merged)`) — a raise there propagates identically. **Nothing in the call chain
catches `CheckError` before `main()`.**

**What the operator actually sees (empirically reproduced this session, not just read):**

```
$ dsx gate ship --spec ANALYSIS-SPEC.yaml --phase-dir . --json
dsx: spec.suppressions[0].code 'DSX-NOT-A-REAL-CODE' is not a known DSX finding code
exit code: 2
```

Two things worth flagging precisely because they matter for how `_gate_findings()`-style test helpers
must be written (see Pitfall 1): the `--json` flag is **silently ignored** on the exit-2 path — the
message is plain text, not a JSON report — because the exception is caught in `main()`, entirely outside
`emit()`'s JSON-serialization branch. A caller that assumes "every `dsx gate --json` output is valid
JSON" will crash on this path, not just get a wrong exit code.

## Research Target 4 — Threading `root` into a frame check (D-09)

`run_checks` (`dsx/cli.py:137-184`) already threads `root` into six named checks via `elif` branches
before falling through to a bare `CHECKS[name](spec)` call for `spec`-only modules:

```python
# dsx/cli.py:152-177 (paraphrased structure, exact lines verified)
root = resolve_root or phase_dir
for name in names:
    if name == "repro":       reports.append(repro.check(spec, phase_dir, strict=strict))
    elif name == "dq":        reports.append(dq.check(spec, root))
    elif name == "claims":    reports.append(claims.check(spec, root, strict=strict))
    elif name == "coherence": reports.append(coherence.check(spec, strict=strict))
    elif name == "figures":   reports.append(figures.check(spec, root, strict=strict))
    elif name == "smells":    reports.append(smells.check(spec))
    elif name == "narrative": reports.append(narrative.check(spec, root, gate_point=gate_point))
    elif name == "code":      reports.append(code.check(spec, root))
    elif name == "design":    reports.append(design.check(spec, strict=strict))
    elif name == "decision":  reports.append(decision.check(spec, gate_point=gate_point))
    elif name in CHECKS:      reports.append(CHECKS[name](spec))
    else: raise CheckError(...)
```

**Recommended new branch, following the `dq`/`code` shape (single extra positional argument, no
keyword):**

```python
elif name == "prereg":
    reports.append(prereg.check(spec, root))
```

`prereg` should also be added to `CHECKS` unconditionally (`dsx/cli.py:63-81`), matching `paradigm`,
`val` and `interference` — **not** because `CHECKS` membership scopes which gate points run it (it does
not; `GATE_PROFILES` does that), but because `dsx check`/`dsx audit` (`cmd_check`, `dsx/cli.py:203-214`;
`cmd_audit`, `:217-235`) both iterate `tuple(CHECKS)` directly, bypassing `GATE_PROFILES` entirely. One
concrete consequence worth flagging to the planner: **`dsx check` (run with no `--checks` filter) will
run `prereg` unconditionally**, even though D-11 restricts it to `verify`/`ship` via `GATE_PROFILES`.
Since `dsx check`'s ad hoc invocation has no natural "gate point," and prereg's missing-plan-header
exit-2 rule (D-09) is not conditioned on gate point in CONTEXT's wording, this is consistent
behavior — a spec that has never seen `dsx gate plan` will also error out of a bare `dsx check` once
`prereg` ships. I did not find this called out in CONTEXT; it is a natural consequence, not a design
gap, but the planner should decide explicitly whether this is acceptable or whether `prereg.check`
needs a way to no-op outside a real gate point (I recommend accepting it as-is: `dsx check` already
runs every registered check regardless of "which gate point normally uses it," so this is consistent
with existing behavior, not a new inconsistency).

**`decisions_path()` and `read_all()`** (`dsx/decisions.py:193-197`, `:122-155`, both directly read this
session):

```python
def decisions_path(root: "str | Path") -> Path:
    return Path(root) / "DECISIONS.jsonl"

def read_all(path: "str | Path") -> "list[dict]":
    # Never raises. Missing path -> []. Unreadable path -> []. Undecodable
    # bytes -> replaced, then either parses or is skipped. Unparseable line
    # -> skipped, not fatal.
```

`prereg.check(spec, root)` should call `decisions.read_all(decisions.decisions_path(root))` and filter
for `record_type == "invocation"` and `gate_point == "plan"`. **This import is legal under D-03a**:
`dsx/frame/__init__.py:16-31`'s module docstring explicitly names `dsx.decisions` among the five
permitted imports (`dsx.findings`, `dsx.spec`, `dsx.loader`, `dsx.decisions`, `dsx.mathx`), and
`tests/test_frame_boundary.py` only scans for the *forbidden* direction (`dsx.checks`), so
`dsx.decisions` is unconditionally clear.

**The record shape as it actually appears** (I ran `dsx gate plan` twice against a fresh temp fixture
this session, then inspected the file):

```json
{"dsx_version": "...", "frame_digest": "58f93bf0c8056dd45342a1abc6a8f648b21c5546eb3779ecaa647d0771764da6", "gate_point": "plan", "invocation_id": "INV-0001", "record_type": "invocation"}
```

(Keys are alphabetically sorted, matching `frame_digest()`'s and `append()`'s `sort_keys=True`
contract.) A `DecisionRecord` row carries `id`, `invocation_id`, `layer`, `choice`, `inputs`, `rule`,
`citation`, `counterfactual`, `alternatives_rejected`, `confidence`, `escalate`, `record_type` —
confirmed against the dataclass definition at `dsx/decisions.py:64-88`.

**Ordering is safe, not racy, within one gate invocation:** `cmd_gate` (`dsx/cli.py:237-269`) calls
`run_checks(...)` — which is where `prereg.check` reads existing headers — **before**
`_write_decision_trail(report, spec, root, point, args.verbose)` appends *this* run's own header
(`dsx/cli.py:269`). So a `verify` run's `prereg.check` never sees its own not-yet-written header; it
only ever sees headers from strictly prior invocations. I confirmed this reading and then confirmed it
behaviorally (Target 5 below).

## Research Target 5 — The multiple-plan-headers question

**Empirically confirmed: re-running `dsx gate plan` does append a second header.** I ran this directly:

```
$ dsx gate plan --spec ANALYSIS-SPEC.yaml --phase-dir <fresh-tmp>
$ dsx gate plan --spec ANALYSIS-SPEC.yaml --phase-dir <same-tmp>   # run again, unmodified spec
$ cat DECISIONS.jsonl | ... # print record_type, gate_point, invocation_id
invocation plan INV-0001 58f93bf0c8...
invocation plan INV-0002 58f93bf0c8...
```

Two `plan`-gate_point invocation headers, same `frame_digest` (spec unchanged between runs). Nothing in
`cmd_gate` or `next_invocation_id()` prevents this, and **nothing enforces that `plan` must run before
`execute`/`verify`/`ship` chronologically** — I checked `cmd_gate` for any ordering guard and found
none; the four-stage sequence is a CLI/CI convention, not a state machine the code enforces.

This directly informs the open "most recent vs. earliest" question, and I want to surface a real tension
I found rather than a clean answer:

**Case for "earliest":** an operator who runs `dsx gate plan`, sees execution results, edits
`inference.primary_procedure`/`fallback_rule` to match what they now want, and re-runs `dsx gate plan`
before `dsx gate verify` would — under a "most recent" rule — get a *fresh* header whose `frame_digest`
matches their post-hoc edit, completely defeating the reconciliation this phase exists to build. Nothing
stops this sequence; I verified `cmd_gate` enforces no ordering. "Earliest" closes this gap by construction.

**Case for "most recent" (and why I recommend it anyway):** I found that `examples/DECISIONS.jsonl` — a
real, if uncommitted, artifact on this exact machine — already holds **1,033 invocation headers**
accumulated purely from repeated local test runs that omit `--phase-dir` (see the Corrections section
and Pitfall 1). Under an "earliest" rule, the very first historical `plan` header ever written against
that shared file — potentially from a much older revision of `good-ANALYSIS-SPEC.yaml`, written before
any of today's content existed — would permanently pin `DSX-PRE-020`'s comparison target, making the
check fail forever in that directory regardless of how many correct, up-to-date `plan` runs follow. This
is not a hypothetical: it is the exact state of this repository's own `examples/` directory right now.
"Most recent" is what makes `test_good_fixture_passes_every_gate` (`tests/test_dsx.py:1388-1392`, which
runs `plan`/`execute`/`verify`/`ship` in that literal order against the same real directory with no
`--phase-dir`) keep working.

**Recommendation: use the most recent `plan`-gate_point header.** Document the gaming vulnerability
explicitly as a known limit — the same treatment this project already gives `declared_at: post_data`
(D-10) and `analysis.test`'s plan-time nature (D-05's "honest caveat"). This is consistent with the
project's established pattern: where a limit cannot be closed without also blocking legitimate
iterative refinement (an operator adjusting their plan before `execute` ever runs is not misconduct),
document it rather than pretend to block it. State plainly in the `DSX-PRE-020` finding's remedy text
and in README that the lock is only as strong as the operator's discipline in not re-running `gate plan`
after seeing results — the same honesty this phase already owes `declared_at`.

I present this as a recommendation, not a re-litigated decision — it is squarely inside CONTEXT's
"Claude's Discretion" list, and the tension above is real enough that the planner (or the user, if it
returns to discuss) may reasonably weigh it differently.

## Research Target 6 — The five enforcement guards (D-13)

All five checked directly this session:

1. **`_NOT_SHIPPED` names `"DSX-PRE-"`**: confirmed at `dsx/frame/paradigm.py:66` exactly
   (`"DSX-PRE-": "Phase 10 ships DSX-PRE-* (pre-registered inference plan)."`). Guard test: confirmed at
   `tests/test_dsx.py:2857-2858` (**corrected from CONTEXT's `:2849-2850`** — see Corrections). The
   entry must be deleted in the landing commit.
2. **`_PARADIGM_INDEPENDENT` already lists `"DSX-PRE-"`**: confirmed at `dsx/frame/paradigm.py:47`
   exactly, inside the tuple `("DSX-SPEC-08", "DSX-VAL-", "DSX-INT-", "DSX-PRE-", "DSX-PAR-002")`. Guard
   test assertion: confirmed at `tests/test_dsx.py:2838-2842` (**corrected from CONTEXT's
   `:2830-2834`**, which points to loop setup rather than the assertion). Whole test method:
   `test_applied_prefixes_have_codes_and_not_shipped_prefixes_have_none`, lines 2811-2858, marked with
   `# D-05: DSX-PAR-001` at line 2810.
3. **`PREFIX_GROUPS` has no `DSX-PRE` entry**: confirmed — the list runs
   `scripts/gen-finding-catalogue.py:25-52` and its final entry is `DSX-INT`. `render()`'s silent-skip
   behavior confirmed at `:187-190` (`if not group: continue`). Guard test:
   `test_every_collected_code_resolves_to_a_prefix_group`, confirmed exactly at
   `tests/test_gen_finding_catalogue.py:174-181`.
4. **`_D05_ALLOWLIST_PREFIXES` does not cover `DSX-PRE-`**: confirmed exactly —
   `scripts/gen-finding-catalogue.py:65` is `_D05_ALLOWLIST_PREFIXES = ("DSX-PAR-", "DSX-VAL-",
   "DSX-INT-")`. This is genuinely the easiest edit to forget: `check_d05()` (`:257-287`) only inspects
   codes matching this tuple (or the separate `_D05_ALLOWLIST_CODES` frozenset for legacy
   single-code exemptions), so a `DSX-PRE-*` code with no citation and no test marker would pass
   `--check` silently until this line is edited.
5. **The pinned code-set test**: confirmed at `tests/test_gen_finding_catalogue.py:227`
   (`test_d05_covered_code_set_on_the_real_tree_is_exactly_the_documented_set`) exactly as CONTEXT
   states.

**The docstring shape `check_d05()` actually enforces** (read directly from
`scripts/gen-finding-catalogue.py:257-287` and `_resolve_docstrings()` at `:200-239`): for every code
matching an allow-listed prefix, `check_d05` walks up from the `report.add(code, ...)` call site to the
nearest enclosing `FunctionDef`/`AsyncFunctionDef` and requires **that function's own docstring** to
carry a `Citation:` line (regex `^\s*Citation:\s*\S`) and either a `Reference value:` or `Structural
criterion:` line (regex `^\s*(?:Reference value|Structural criterion):\s*\S`), plus a `# D-05: <CODE>`
comment somewhere under `tests/`. Two codes sharing one `report.add()`-calling function share one
docstring (this is legal — several shipped codes do this); codes in different functions need separate
docstrings. **Open question for the planner:** given D-07 folds `DSX-PRE-030` into one code for both
REQ-P10-03 and REQ-P10-04, it needs exactly one docstring. Whether `DSX-PRE-010` and `DSX-PRE-020` also
land in the same helper function as each other (sharing one docstring) or in separate helpers (needing
separate `Citation:`/`Structural criterion:` pairs) is an implementation choice the planner should make
explicitly — I did not find CONTEXT settling it, and it materially affects whether one or three Gelman &
Loken citation blocks are needed.

## Research Target 7 — The fixture and corpus structure (D-16)

Read `tests/test_known_bad_corpus.py` in full (806 lines). Key structures, all line numbers re-verified
this session:

- **`_TARGET_DEFECT_CODES`** (`:134-138`, confirmed exact): `dict[str, dict[str, str]]`, keyed by
  fixture slug then gate point, one code per point. This is the shape a verify/ship-only family needs —
  `weak-identification-mmm` already uses it for a two-gate-point case
  (`{"plan": "DSX-VAL-040", "verify": "DSX-INT-030"}`).
- **`_EXPECTED_CAUGHT_DEFECTS`** (`:278-284`, **corrected from CONTEXT's `:259-265`**): `dict[str,
  frozenset[str]]`, keyed by slug, whose codes are expected at **every** point in
  `_CRITICAL_THRESHOLD_POINTS = ("plan", "execute")` (`:53`) — the both-CRITICAL-points shape. **Every
  fixture on disk must have a key here** (`test_expected_caught_defects_keys_match_the_corpus_on_disk`,
  `:531-543`), even if the value is an empty `frozenset()`.
- Since `prereg` is registered at `verify`/`ship` only (never `plan`/`execute`), a new fixture's
  `DSX-PRE-030` code belongs **only** in `_TARGET_DEFECT_CODES["<new-slug>"] = {"verify":
  "DSX-PRE-030"}`, and its `_EXPECTED_CAUGHT_DEFECTS["<new-slug>"]` entry **must be an empty
  `frozenset()`** — putting `DSX-PRE-030` there would incorrectly assert it fires at `plan`/`execute`
  too (it structurally cannot, since `prereg` never runs there), and
  `test_every_spec_blocks_only_on_its_target_defect_at_critical_threshold_points` would then expect a
  code from a check that never runs at those points.

- **Critical, load-bearing gap I found while tracing this**: the generic test
  (`test_every_spec_blocks_only_on_its_target_defect_at_critical_threshold_points`, `:411-444`) only
  ever calls `self._gate_findings(path, point)` for `point in _CRITICAL_THRESHOLD_POINTS`, i.e. only
  `plan` and `execute`. **The "verify" key in `_TARGET_DEFECT_CODES` is never consulted by that generic
  test** — this is exactly why `weak-identification-mmm`'s `"verify": "DSX-INT-030"` entry required its
  own dedicated, hand-written positive test,
  `test_weak_identification_mmm_fixture_blocks_verify_and_ship_naming_int_030` (`:446-466`), rather than
  being covered generically. **The planner must write an equivalent dedicated test for the new prereg
  fixture** — e.g. `test_<new-slug>_fixture_blocks_verify_and_ship_naming_pre_030` — following that exact
  pattern (assert `code == 1` and `"DSX-PRE-030"` is among the CRITICAL findings, for both `verify` and
  `ship`). The generic multi-fixture test will silently not exercise this at all.

- **`test_ship_gate_findings_are_all_documented_incidental_corpus_gaps`** (`:468-509`) does check
  `ship`-point findings against `_own_target_codes(slug)` (which unions both maps' values regardless of
  which key they're stored under), so `DSX-PRE-030` in `_TARGET_DEFECT_CODES["<slug>"]["verify"]` is
  correctly recognized there without needing to also appear in `_INCIDENTAL_GAP_CODES`.

- **`test_incidental_allowlist_names_no_slugs_own_target_code`** (`:511-529`) is the guard that
  "explicitly forbids" adding `DSX-PRE-*` to `_INCIDENTAL_GAP_CODES` — confirmed exactly.

- **Closest existing fixture to copy**: `weak-identification-mmm-ANALYSIS-SPEC.yaml` is the closest
  structural analogue — it is the only existing fixture using the point-scoped `_TARGET_DEFECT_CODES`
  shape with a non-`plan` key (`"verify": "DSX-INT-030"`), and it has its own dedicated positive
  verify/ship test to copy the shape of. It is **not** a content analogue (it is about weak
  identification, not procedure substitution), so copy its *test scaffolding*, not its YAML content.

**New pitfall this research surfaced, not present in CONTEXT**: `self._gate_findings()`
(`:332-353`) constructs `with tempfile.TemporaryDirectory() as tmp:` **inside the method, fresh on every
call**. See Common Pitfalls, Pitfall 1 below — this is the single highest-impact finding of this
research and applies to every existing fixture's `ship`/`verify` calls, not only the new one.

## Research Target 8 — Module idiom for `dsx/frame/prereg.py`

Read `dsx/frame/val.py` and `dsx/frame/interference.py` in full. The house shape, confirmed by direct
read of both:

**`check(spec)` dispatcher pattern** (`interference.py:675-710`, `val.py:200-229`, both re-read this
session):

```python
def check(spec: dict) -> Report:
    """Emit the <family>-family findings (`DSX-XXX-*`).

    Reads `<top-level-block>:` and degrades to an empty report — never a
    traceback — when the block is absent or malformed (an absent block is
    already <upstream shape check>'s territory, so this function does not
    re-report it).

    Structural criterion: dispatches to one private helper per adjudicated
    concept; no numeric threshold, effect size or statistic is computed
    anywhere in this module (D-02).
    """
    report = Report(check="<name>")
    if not isinstance(spec, dict):
        return report
    <extract the relevant sub-block(s)>
    _check_one_thing(..., report)
    _check_another_thing(..., report)
    return report
```

For `prereg.check(spec, root)`, the extra `root` argument (per D-09) is the only structural deviation
from this pattern among the two modules I read (both `val.check(spec)` and `interference.check(spec)`
take `spec` alone — confirmed at `val.py:200` and `interference.py:675`).

**Finding emission — titles must be literal at the call site.** Confirmed: `PREFIX_GROUPS`'s catalogue
extractor (`_literal()`, `scripts/gen-finding-catalogue.py:84-95`) handles f-strings by collapsing any
non-constant segment to `<…>`, so a dynamic title still extracts, but the code/severity arguments (args 0
and 1 of `report.add(...)`) must be **literal string constants**, never built from a variable — this is
what `extract()` (`:98-114`) actually parses via `ast.walk`.

**`Citation:`/`Structural criterion:` docstring placement — confirmed via direct grep with context,
five live examples in `interference.py`** (lines 160, 171, 271, 291, 378, 390, 555, 566, 686 — all
re-read this session): these lines live on the **enclosing private helper function's** docstring, not
the module docstring and not always on `check()` itself. `check()`'s own docstring in both modules
carries only a generic `Structural criterion:` line with no `Citation:` (a house-keeping-only line,
consistent with `check()` never itself calling `report.add()` directly — it only dispatches).

**`DecisionRecord` emission idiom** (`interference.py:641-672`, re-read in full):

```python
report.context.setdefault("decisions", []).append(
    DecisionRecord(
        id="", invocation_id="",   # filled in later at CLI write time (_write_decision_trail)
        layer="deterministic",
        choice=f"DSX-XXX-NNN {'fired' if fired else 'clear'}: <state summary>",
        inputs=["spec.dotted.path.one", "spec.dotted.path.two"],
        rule="<one-sentence statement of the exact firing condition>",
        citation="<Author, Year, Title, locator>",
        counterfactual="<what would have made this go the other way>",
    ).to_dict()
)
```

`id=""` and `invocation_id=""` are always blank at emission time — `_write_decision_trail`
(`dsx/cli.py:277-320`) fills `id` (`f"DEC-{n:03d}"`) and `invocation_id` when it appends the record to
disk, confirmed at `:314-318`.

**The `# D-05: <CODE>` test marker idiom** (confirmed via direct read, `tests/test_dsx.py:2810-2811`):

```python
    # D-05: DSX-PAR-001
    def test_applied_prefixes_have_codes_and_not_shipped_prefixes_have_none(self):
```

A plain comment line immediately above the test method, naming exactly one code. `_collect_test_markers`
(`scripts/gen-finding-catalogue.py:242-254`) is a raw-text regex pass (`_TEST_MARKER_RE = re.compile(r"#\s*D-05:\s*(DSX-[A-Z]+-\d{3})")`), not an AST walk — it will find the marker anywhere in a
`tests/*.py` file's text, but placing it directly above the specific test that proves the code is the
established convention.

## Research Target 9 — Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Python stdlib `unittest` (no third-party test runner found — grepped for `pytest.ini`, `conftest.py`, `pyproject.toml`'s `[tool.pytest]`; none exist) |
| Config file | none — `scripts/check.sh:7` runs `python3 -m unittest discover -s tests -q` |
| Quick run command | `python -m unittest tests.test_frame_prereg -v` (new file, following `tests/test_frame_interference.py`'s per-family precedent) |
| Full suite command | `python -m unittest discover -s tests -q`, or `scripts/check.sh` (also regenerates/checks the finding catalogue and re-runs the gate-contract loop) |

### Phase Requirements -> Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| REQ-P10-01 | Mini-DSL rule resolves to exactly one branch; unparseable rule exits 2, never 0 | unit | `python -m unittest tests.test_frame_prereg.TestFallbackRuleParsing -v` | ❌ Wave 0 — new file |
| REQ-P10-02 | `declared_at` recorded and documented as unverifiable; digest comparison uses recorded bytes | unit + doc-content assertion (README substring check, matching `test_bayesian_postmortem_states_the_deng_bound_and_its_value`'s positive-assertion pattern) | `python -m unittest tests.test_frame_prereg.TestContentLockReconciliation -v` | ❌ Wave 0 — new file |
| REQ-P10-03 | Executed procedure differs from selected branch -> blocks, both branches named in `detail` | unit + integration (real `dsx gate verify` against the new known-bad fixture) | `python -m unittest tests.test_frame_prereg -v` and `python -m unittest tests.test_known_bad_corpus -v` | ❌ Wave 0 for the unit half; `tests/test_known_bad_corpus.py` exists and needs a new dedicated positive test (see Target 7) |
| REQ-P10-04 | Post-hoc switch to a strictly-more-conservative substitute still blocks (fixture-only, D-07) | unit, synthetic spec (not a committed corpus pair — D-16) | `python -m unittest tests.test_frame_prereg.TestNoMeritConsultation -v` | ❌ Wave 0 — new file |
| D-11 registration | `prereg` registered at verify/ship only, absent from plan/execute; every `DSX-PRE-*` code reachable from a `GATE_PROFILES` entry | unit, mirrors `tests/test_frame_interference.py:181-196` exactly | `python -m unittest tests.test_frame_prereg.TestGateRegistration -v` | ❌ Wave 0 |
| D-13 guards | `_NOT_SHIPPED`/`_PARADIGM_INDEPENDENT` flip together; `PREFIX_GROUPS`/`_D05_ALLOWLIST_PREFIXES` updated | existing tests, already present | `python -m unittest tests.test_dsx -v` (paradigm invariants), `python -m unittest tests.test_gen_finding_catalogue -v` | ✅ Tests exist; only the source constants need editing |
| Harness blast radius (this research's own finding) | Existing known-bad corpus verify/ship calls must not regress to exit 2 | integration, existing test file needs a fix | `python -m unittest tests.test_known_bad_corpus -v` | ✅ Exists, **needs modification** — see Pitfall 1 |

### Sampling Rate

- **Per task commit:** `python -m unittest tests.test_frame_prereg -v` (fast — new module only)
- **Per wave merge:** `python -m unittest discover -s tests -q` (full suite — catches the harness blast
  radius against `test_known_bad_corpus.py` and `test_dsx.py`)
- **Phase gate:** `scripts/check.sh` green before `/gsd-verify-work` — this also re-runs the
  good/bad-fixture gate-contract loop, which is exactly where the DECISIONS.jsonl-ordering assumption
  gets exercised for real.

### Wave 0 Gaps

- [ ] `tests/test_frame_prereg.py` — new file, covers REQ-P10-01 through REQ-P10-04 and D-11's
      registration/reachability pair, modeled directly on `tests/test_frame_interference.py`'s
      structure and imports.
- [ ] `examples/known-bad/<new-slug>-ANALYSIS-SPEC.yaml` + matching `-POSTMORTEM.md` (D-16) — the
      procedure-post-hoc-switch fixture, with `_TARGET_DEFECT_CODES["<new-slug>"] = {"verify":
      "DSX-PRE-030"}` and `_EXPECTED_CAUGHT_DEFECTS["<new-slug>"] = frozenset()`.
- [ ] A dedicated positive test in `tests/test_known_bad_corpus.py`, modeled on
      `test_weak_identification_mmm_fixture_blocks_verify_and_ship_naming_int_030` (lines 446-466), for
      the new fixture's `verify`/`ship` behavior — the generic corpus test does not cover
      non-`plan`/`execute` points (Target 7 finding).
- [ ] A fix to `tests/test_known_bad_corpus.py::_gate_findings()` (or a documented, deliberate
      alternative) so `verify`/`ship` calls do not spuriously exit 2 for every existing fixture once
      `prereg` is registered — see Pitfall 1. This is not optional; without it, the full suite goes red
      for reasons unrelated to any new fixture's own defect.
- [ ] Framework install: none — stdlib `unittest` is already the house framework.

## Security Domain

`security_enforcement` is enabled in `.planning/config.json` (absent-defaults-true is moot here — it is
explicitly `true`), so this section is included per instructions, scoped honestly to what actually
applies to a local, single-operator, no-network CLI static-analysis tool.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | No auth surface — `dsx` is a local CLI reading a local YAML file |
| V3 Session Management | No | No sessions |
| V4 Access Control | No | No multi-user access model |
| V5 Input Validation | Yes | The mini-language's `re`-based parser reads operator-authored `fallback_rule` text. It must degrade to a `CheckError` (an intentional, controlled exit 2) on malformed input, never an uncaught traceback — matching the existing house pattern of `val.check`/`interference.check` guarding against a non-dict `spec` before any `.get()` call (`interference.py:686-692`, confirmed). The recommended condition regex is anchored (`^...$`) and has no nested-quantifier structure, so it carries no catastrophic-backtracking (ReDoS) risk of the kind that matters for untrusted, unbounded-length input — `fallback_rule` values in this contract are short, single-line YAML scalars. |
| V6 Cryptography | No new surface | `frame_digest()` (sha256) is already shipped and is explicitly documented as change-detection, not a security control (`dsx/decisions.py:181-190`'s own docstring: *"Change-detection, not a security control"*) — Phase 10 reads this value, does not add new cryptographic surface. |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| A malformed or adversarially crafted `fallback_rule` string crashes the gate with an uncaught traceback instead of a clean exit 2 | Denial of Service (of the gate itself) | `CheckError` raised from a guarded parse function, matching D-02; never a bare `re.match(...).group()` that can raise `AttributeError` on no-match |
| An operator names a `results:`/`design:` field that does not exist and expects the mini-language to silently accept it | Tampering (of the pre-registration guarantee's honesty) | D-04's closed fact registry — `DSX-PRE-010` fires rather than the rule silently resolving to nothing |
| An operator re-runs `dsx gate plan` after seeing results, to reset the content lock | Repudiation (of what was actually pre-registered) | Documented as a known limit (Target 5 recommendation), same honesty treatment as `declared_at: post_data` — not block-able without also blocking legitimate iterative refinement before real execution |

---

## Common Pitfalls

### Pitfall 1: The known-bad corpus test harness will exit 2 for every existing fixture, not just the new one

**What goes wrong:** the moment `prereg` is added to `GATE_PROFILES["verify"]`/`["ship"]`, every call to
`tests/test_known_bad_corpus.py::_gate_findings(spec_path, "verify" | "ship")` — for **every** fixture
already in the corpus, not only the new one — will trip `prereg`'s "no recorded plan-time header" rule
(D-09) and raise `CheckError`, because `_gate_findings()` (`:332-353`) creates a brand-new empty
`tempfile.TemporaryDirectory()` on every single call, with no prior `dsx gate plan` run against that same
directory.

**Why it happens:** `_gate_findings()` was written under the correct assumption (true until this phase)
that each gate point is independently testable in isolation — no prior state was ever a precondition for
any check. Phase 10 is the first phase to make `DECISIONS.jsonl` a genuine, stateful gate *input*
(D-09's own framing: *"reading that lock promotes `DECISIONS.jsonl` from side channel to gate input"*).

**How I confirmed this is real, not theoretical:** I reproduced the exact downstream failure mode this
session against a live fixture, using `apply_suppressions`'s existing `CheckError` route as a stand-in
(since `prereg.py` does not exist yet to trigger its own):

```
$ dsx gate ship --spec <fixture-with-a-bad-suppression> --phase-dir <fresh-tmp> --json
dsx: spec.suppressions[0].code 'DSX-NOT-A-REAL-CODE' is not a known DSX finding code
exit code: 2
```

The `--json` flag is silently ignored on this path — the message is plain text on stderr, not JSON —
because `main()`'s exception handler (`dsx/cli.py:763-765`) prints and returns before `emit()`'s JSON
branch is ever reached. `_gate_findings()`'s own code is:

```python
raw = err.getvalue() or out.getvalue()
report = json.loads(raw)   # <-- json.JSONDecodeError on "dsx: <message>\n"
```

So the failure mode is not "the test assertion fails with a clear message" — it is `_gate_findings()`
itself throwing an unrelated `json.JSONDecodeError` deep inside the helper, for every fixture, the first
time any of the affected tests run. The affected tests I identified by tracing every call site of
`_gate_findings` with a `verify`/`ship` point argument:
`test_ship_gate_findings_are_all_documented_incidental_corpus_gaps` (:468-509) and
`test_weak_identification_mmm_fixture_blocks_verify_and_ship_naming_int_030` (:446-466).

**How to avoid:** fix `_gate_findings()` (or add a variant used by verify/ship call sites) to run `dsx
gate plan` in the same temporary directory before the point under test, when that point is `verify` or
`ship`. This must land in the **same commit** that adds `prereg` to `GATE_PROFILES`, not as a follow-up —
otherwise the corpus test suite goes red for a reason that has nothing to do with the fixture the
failure message will nominally point at, which is exactly the kind of debugging trap this project's
"verification before claiming" discipline exists to prevent.

**Warning signs:** if the planner runs `python -m unittest tests.test_known_bad_corpus -v` after landing
`prereg`'s `GATE_PROFILES` registration but before fixing the harness, expect `json.JSONDecodeError`
tracebacks (not clean `AssertionError`s) from multiple pre-existing tests that have nothing to do with
the new fixture.

### Pitfall 2: `test_good_fixture_passes_every_gate` and `scripts/check.sh` rely on a real, growing, uncommitted `DECISIONS.jsonl`

**What goes wrong:** unlike the corpus test's fresh-tempdir pattern, `tests/test_dsx.py`'s
`test_good_fixture_passes_every_gate` (lines 1388-1392) and `scripts/check.sh`'s gate-contract loop
(lines 15-23) both invoke `dsx gate <point>` **without `--phase-dir`**, so `root` resolves to
`str(path.parent)` — i.e. the real `examples/` directory — and `DECISIONS.jsonl` accumulates there
across every local test run, forever (it is gitignored, never reset).

**Why it happens:** `root = args.phase_dir or str(path.parent)` (`dsx/cli.py:259`) has always defaulted
to the fixture's own directory when no explicit phase dir is given; this was harmless before Phase 10
because nothing ever *read* `DECISIONS.jsonl` as a gate input.

**How to avoid:** because both call sites run `plan` before `verify`/`ship` in the same test/script
invocation (confirmed: `test_good_fixture_passes_every_gate` iterates `("plan", "execute", "verify",
"ship")` in that literal order; `check.sh`'s `for point in plan execute verify ship` loop does too), the
`plan` header they need will already exist by the time `verify`/`ship` runs, **provided the "most
recent header" rule from Target 5 is adopted** — an "earliest header" rule would instead pin to
whatever historical `plan` header happens to already be sitting in `examples/DECISIONS.jsonl` from a
prior, unrelated test run (there are currently 1,033 of them, from a version of the fixture that may no
longer match). This is the strongest concrete argument for the "most recent" recommendation in Target 5.

**Warning signs:** a `DSX-PRE-020` finding against `good-ANALYSIS-SPEC.yaml` that fires only
intermittently, or only on a machine with a long-lived local `examples/DECISIONS.jsonl`, is the
signature of an "earliest header" implementation colliding with this accumulation.

### Pitfall 3: `--json` does not mean "always valid JSON on this exit path"

**What goes wrong:** any new code the planner writes to consume `dsx gate ... --json` output — inside
`prereg.py`'s own tests, or in any future tooling — must not assume the output is JSON whenever the
process exits nonzero. Exit 1 (blocked) output *is* JSON (`emit()` runs normally). Exit 2
(`CheckError`) output is plain text, unconditionally, regardless of `--json`.

**Why it happens:** `main()`'s exception handler runs entirely outside `emit()`; the `--json` flag is
never consulted on that path (`dsx/cli.py:761-768`, confirmed by direct read and empirical reproduction
above).

**How to avoid:** any test helper that wraps `dsx gate` and expects to `json.loads()` its output must
either check the exit code first and skip JSON parsing on 2, or (preferably, matching
`_gate_findings()`'s existing degrade-gracefully spirit) catch `json.JSONDecodeError` and treat it as
"the check could not run," surfacing the raw stderr text in the assertion failure message.

**Warning signs:** a `json.JSONDecodeError` traceback instead of a clean test failure message, exactly
as reproduced in Pitfall 1.

---

## Code Examples

### The full `_write_decision_trail` -> `run_checks` ordering (confirmed, not inferred)

```python
# dsx/cli.py:258-269 (paraphrased for clarity, exact structure verified)
spec = load(path)
root = args.phase_dir or str(path.parent)
report = run_checks(
    spec, GATE_PROFILES[point], args.phase_dir,
    gate_point=point, resolve_root=root,
)                                          # prereg.check(spec, root) reads DECISIONS.jsonl HERE
report.check = f"gate:{point}"
report.context["spec_path"] = str(path)
_write_decision_trail(report, spec, root, point, args.verbose)   # THIS run's header is appended HERE, after
```

### `describe_vocabulary()`'s existing flat-namespace special case (the pattern to copy for the fact registry)

```python
# dsx/spec.py:1077-1096, verified by direct read
def describe_vocabulary() -> "dict[str, Any]":
    out: "dict[str, Any]" = {}
    for name, obj in _VOCABULARIES:
        out[name] = {k: obj[k] for k in sorted(obj)} if isinstance(obj, dict) else sorted(obj)
    out["chart_capabilities"] = {...}       # first special case
    out["inference_fields"] = sorted(_INFERENCE_FIELDS)   # second special case — copy this shape
    return out
```

### Registration + reachability test pair to copy exactly (D-11's stated template)

```python
# tests/test_frame_interference.py:181-196, verified by direct read
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
        reachable_checks = set().union(*GATE_PROFILES.values())
        self.assertIn("interference", reachable_checks)
```

For `prereg`, the first test's point loop must name `("verify", "ship")` present and assert
`"plan"`/`"execute"` **both** absent (matching D-11's tighter scope — `interference` is present at
`plan`/`verify`/`ship`, absent only from `execute`; `prereg` is present at `verify`/`ship` only).

## State of the Art

Not applicable in the usual sense — this is not a "what changed in the ecosystem" research question.
The one relevant internal precedent shift: Phase 9's corpus rewrite (plan 09-01) moved from a
single-shape expectation map to the current two-map (`_TARGET_DEFECT_CODES` + `_EXPECTED_CAUGHT_DEFECTS`)
structure specifically because a family-prefix string could express at most one code per family, and
Phase 8 shipped four codes in one family (`DSX-INT-*`). Phase 10 inherits that structure rather than
needing a third shape — its own `DSX-PRE-*` family has only three codes, and only one
(`DSX-PRE-030`) ever needs corpus representation (the other two are exit-2/documentation-only
concerns, not gate-blocking findings the corpus proves are caught).

**Deprecated/outdated:** none — nothing in this phase replaces a previously-shipped mechanism; it is
purely additive.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The RHS of `->` should be truncated at the first comma to derive the branch label | Target 1 | If wrong, the worked example (`wild cluster bootstrap, 9999 reps, seed 42`) would not normalize to a value comparable against `primary_procedure`/`analysis.test`, and REQ-P10-01's "resolves to exactly one branch" would need a different mechanism |
| A2 | `inference.primary_procedure` should serve as the implicit "else" branch when a mini-language condition evaluates false | Target 1 | If wrong, the grammar needs an explicit `else` clause or a different rule for what "the declared branch" means when the condition is false, changing REQ-P10-03's comparison target |
| A3 | The three-member fact registry (`alpha`, `interim_looks`, `comparisons_looked_at`) is sufficient and `observed_n` should be excluded | Target 2 | If wrong (e.g. a future requirement needs cluster-count-style comparisons against a list field), the registry needs a fourth member with explicit list-to-scalar semantics defined |
| A4 | "Most recent plan header" is the right rule for `DSX-PRE-020`'s comparison target | Target 5 | If wrong, an operator can defeat the reconciliation entirely by re-running `dsx gate plan` after seeing results and before `dsx gate verify` — this is a real, not hypothetical, gaming vector I found no code-level barrier against |
| A5 | `DSX-PRE-010` and `DSX-PRE-020` may share one enclosing helper function (and thus one `Citation:`/`Structural criterion:` docstring pair) rather than needing separate ones | Target 6 | If wrong, `check_d05()` will fail `--check` for whichever code's docstring is missing its own `Citation:`/`Structural criterion:` lines |

## Open Questions

1. **Does `DSX-PRE-010`'s citation need to be the same Gelman & Loken anchor as `DSX-PRE-030`, or does
   it need its own?**
   - What we know: ROADMAP SC 5 requires *every* `DSX-PRE-*` code to carry a primary-source citation.
     `check_d05()` enforces this per enclosing-function docstring, not per module.
   - What's unclear: whether the mini-language's own parse/resolution failure (`DSX-PRE-010`) is
     conceptually the same claim as the φ-vs-φ(y) branch-identity claim `DSX-PRE-030` embodies, or
     whether it needs a distinct locator.
   - Recommendation: the planner should decide this explicitly when drafting the docstring, and record
     the reasoning inline — I did not find CONTEXT settling it, and getting it wrong fails
     `scripts/gen-finding-catalogue.py --check` mechanically, so it will surface immediately during
     execution regardless.

2. **Should `DSX-PRE-020`'s "no recorded plan header" precondition apply identically under `dsx check`
   (which bypasses `GATE_PROFILES` and runs `prereg` unconditionally) as it does under `dsx gate
   verify`/`dsx gate ship`?**
   - What we know: `cmd_check`/`cmd_audit` both iterate `tuple(CHECKS)` directly, so once `prereg` is
     added to `CHECKS`, it runs under `dsx check` regardless of gate point.
   - What's unclear: whether this is desired (I recommend accepting it, since it matches existing
     behavior for every other check) or whether `prereg.check` needs a `gate_point` parameter to
     distinguish.
   - Recommendation: accept as-is unless the planner finds a concrete reason `dsx check` needs different
     behavior — adding a `gate_point` parameter purely to special-case this would be new complexity with
     no requirement demanding it.

## Environment Availability

Not applicable — this phase adds no external tool, service, or runtime dependency. Everything it needs
(`re`, `operator`, `hashlib`, `json`) is Python stdlib, already imported by sibling modules in this
package.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no external dependency, stdlib-only, directly confirmed against brief D-01 and
  `dsx/decisions.py`'s own docstring.
- Architecture (module idiom, root threading, exit-2 mechanics): HIGH — every claim traced to a direct
  code read this session, several empirically reproduced (multi-plan-header behavior, CheckError's
  plain-text output on `--json`).
- Mini-language grammar: MEDIUM — no existing precedent to verify against; my recommendation is
  internally consistent with D-04/D-05/D-07 but is a design proposal, not a fact I read off disk.
- Fact registry membership: HIGH — every candidate field's presence and type verified directly against
  `examples/good-ANALYSIS-SPEC.yaml`, `templates/ANALYSIS-SPEC.yaml`, and every known-bad fixture.
- Pitfalls (harness blast radius): HIGH — reproduced empirically, not just reasoned from source.

**Research date:** 2026-08-13
**Valid until:** stable — nothing here depends on an external ecosystem that moves; re-verify only if
`dsx/cli.py::run_checks`, `dsx/decisions.py`, or `tests/test_known_bad_corpus.py` change before planning
begins.
