---
phase: 16
phase_name: "Re-run verification off the gate path"
project: "gsd-dsx"
generated: "2026-08-29"
counts:
  decisions: 10
  lessons: 3
  patterns: 5
  surprises: 3
missing_artifacts:
  - "UAT.md"
---

# Phase 16 Learnings: Re-run verification off the gate path

## Decisions
### Mint DSX-REP-060/061 in Phase 16 rather than deferring or reusing (Option A)
The persona round (Architect + Auditor, both opus/high) weighed three options for REQ-P16-02's
enforcement: (A) mint in Phase 16, (B) move the gate check to Phase 15 (the designated catalogue
phase), or (C) don't mint / reuse an existing code / make it advisory. Both personas voted Option A
unanimously — the tie-break axis (rigour > reliability > flexibility) was not needed.

**Rationale:** Option B fragments produce (P16-01) from enforce (P16-02) across a phase boundary,
contaminates Phase 15's D-05 statistical-citation regime with a code that has none, and inverts the
documented dependency (P16 depends only on P12, not P15). Option C is worse: no existing code names
these defects, so reuse emits false finding text; the catalogue generator dedupes by code, so a reused
code with new text leaves the count green and the corruption invisible to both invariants; and a
sub-HIGH/advisory code cannot exit 1 at verify/ship, silently defeating REQ-P16-02.
**Source:** 16-CONTEXT.md

---

### Two new codes, not one, both severity HIGH (D-05)
`DSX-REP-060` (report declared but missing) and `DSX-REP-061` (report present but numbers don't
overlap) are split rather than folded into a single code, and both are HIGH rather than MEDIUM.

**Rationale:** The catalogue's own style already splits "declaration absent" from "declaration points
at nothing" (030/031) and repro_lock states (050-053); the two defects have different remedies (run
the skill vs investigate why the fresh run disagrees) and different meaning (a process gap vs the
analysis genuinely does not reproduce). Both must be HIGH because verify/ship's block threshold is
HIGH (`cli.py:138-139`) — a MEDIUM code cannot flip exit 1, silently failing REQ-P16-02.
**Source:** 16-CONTEXT.md

---

### Gate-path purity is inviolable — only the skill may execute the entrypoint (D-01)
REQ-P16-02's check is declaration-only: `Path.exists()` plus `re`/`str`/`set`/`math.isclose` over
report text. It must never import pandas/scipy/numpy/csv and never call
`subprocess`/`runpy`/`os.system`/`exec`. The skill (REQ-P16-01) is the only sanctioned place the
entrypoint runs.

**Rationale:** Inherits D-01/D-02 from prior phases. The Auditor's threat model named the specific risk
this forecloses (T1-T4, T7): a report-parser reaching pandas, a dotted import bypassing the hermetic
test, shelling/runpy-ing the entrypoint "just to check it runs," trusting a skill verdict line, or
probing the interpreter to infer "in use."
**Source:** 16-CONTEXT.md

---

### "Skill is in use" is a new explicit opt-in field, never entrypoint-presence (D-02)
The trigger for the gate check is a new field `reproducibility.reproduce_report` (a path string), not
the pre-existing `entrypoint` field.

**Rationale:** `entrypoint` already exists in the good fixture and most real specs; keying on it would
retroactively demand `REPRO-REPORT.md` from every spec that ever declared one — a false-positive
explosion and a backward-incompatible gate change that breaks the good fixture. Absent → gate silent;
present → gate checks. This also makes "a missing interpreter is not a gate exit 1" true by
construction, since the gate never inspects interpreters, only the declared artifact.
**Source:** 16-CONTEXT.md

---

### Catalogue rebaseline is additive; the Phase-12 snapshot anchor is never mutated (D-08)
The invariant's set-identity test compares the current catalogue set against an explicit
`phase12_set ∪ {DSX-REP-060, DSX-REP-061}`, with `_EXPECTED_TOTAL` bumped 256→258. The byte-frozen
`finding-codes-phase12.md` snapshot file itself stays untouched at 256.

**Rationale:** That snapshot is the historical anchor Phases 13/14's git-frozen zero-mint claims
reference; corrupting it would retroactively falsify them. Three pinned artifacts (regenerated
catalogue, bumped `_EXPECTED_TOTAL`, extended expected-set) must move in lockstep so the mint cannot
be silent, and any code beyond the sanctioned delta still trips the test.
**Source:** 16-CONTEXT.md

---

### ROADMAP's "only Phase 15 extends the catalogue" prose is amended, not treated as binding (D-07)
The orchestrator recorded that both Phase 15 and Phase 16 extend the finding catalogue, correcting a
ROADMAP.md line-119 prose assertion.

**Rationale:** That line was a planning-time prose assertion, not a load-bearing invariant — the 256
snapshot was always meant to be rebaselined by a check-shipping phase, and REQ-P16-01/02 already
implied an enforcing code. Explicitly not a §4-cat-3 scope change: no requirement is dropped or
reworded, it is a factual reconciliation of prose the requirements already contradicted.
**Source:** 16-CONTEXT.md

---

### REQ-P16-04's test must be a distinct, non-vacuous static AST execution scan (D-09)
The no-entrypoint-execution guard is explicitly designed as orthogonal to the existing import-based
hermetic test, not a variant of it: it AST-walks `dsx/checks/` and `dsx/frame/` and denylists the
execution-primitive family (`subprocess.*`, `os.system`/`exec*`/`spawn*`, `runpy.run_path`/
`run_module`, bare `exec`/`eval`, dynamic `compile`/`__import__`), with anti-vacuity anchors (a
named non-empty scan set including `code.py` and `repro.py`) and a positive control (a synthetic
`subprocess.run`/`runpy.run_path` call asserted to be flagged).

**Rationale:** `subprocess`/`runpy`/`os.system` are stdlib, so they sail through an import-closure
check silently (Auditor T3) — only a call-site scan catches actual execution. Must not confuse
`ast.parse`/`ast.walk`/`ast.unparse` or a bare substring grep (code.py's own docstring contains the
strings `exec`/`!pip`) with genuine execution.
**Source:** 16-CONTEXT.md

---

### The missing-interpreter SKIPPED status must short-circuit DSX-REP-061 (D-11)
A legitimately skipped reproduce run (interpreter absent) that still writes a report has no fresh
numbers; a naive check would fire 061 on empty overlap and produce the exit-1 the ROADMAP forbids. The
report must carry an explicit SKIPPED/UNABLE status that 061 honours before attempting overlap.

**Rationale:** Named as "the subtlest trap" in the phase context — an honest opt-out analogous to
`DSX-REP-051`'s null repro_lock. Without this, REQ-P16-02's own stated guarantee ("a missing
interpreter on a reproduce skill run is not a gate exit 1") would be violated by construction.
**Source:** 16-CONTEXT.md

---

### "Numbers overlap" is verdict-agnostic set-membership, never a trusted PASS/FAIL line (D-04)
The gate reads a machine-readable YAML block for the lead metric and independently checks
`math.isclose` overlap against the spec's `results.tests` value. It never reads or trusts a
skill-authored verdict/status line as proof of reproduction.

**Rationale:** Directly closes Auditor threat T4 — a report whose verdict says PASS but whose numbers
disagree must still fail the gate. "Overlap" is deliberately weaker than equality (rounding-level
difference passes; a gross disagreement such as a 10x error does not), matching the ROADMAP's own word
choice.
**Source:** 16-CONTEXT.md

---

### `protocol_adherence` lives on ATTRIBUTION sidecars, never on ANALYSIS-SPEC.yaml (D-10)
The new REQ-P16-03 field is placed only on the existing `*-ATTRIBUTION.yaml` sidecars, with pins that
it never enters the catch-rate/FPR denominators or `_headline`'s arguments.

**Rationale:** A spec key could change gate findings or trip an unknown-key schema check; a sidecar key
cannot perturb `frame_digest` or any gate finding by construction. This extends REQ-P12-02 without
replacing catch rate or false-positive rate as the calibration numbers.
**Source:** 16-CONTEXT.md

---

## Lessons
### The catalogue generator requires `--write`, not a bare invocation, to rewrite the file
The 16-01 plan's Task 3 instructed running `python scripts/gen-finding-catalogue.py` with no flags to
rewrite `references/finding-codes.md`. The installed generator instead writes the file only when given
`--write`; a bare invocation prints to stdout without touching the file.

**Context:** Caught during execution as a plan-vs-tool grounding deviation; the executor used the
grounded `--write` invocation and verified the result via `--check` exit 0. This mirrors the project's
general "verify the installed tool's flags before writing config/commands against it" discipline.
**Source:** 16-01-SUMMARY.md

---

### Finding messages must be fixed plain-string literals, never f-strings, for the catalogue to render correctly
`scripts/gen-finding-catalogue.py` extracts the catalogue row's Finding-column text verbatim from the
3rd positional argument to `report.add`. Any dynamic interpolation there renders as a literal `<...>`
placeholder in the shipped catalogue rather than real text.

**Context:** Both DSX-REP-060 and DSX-REP-061 were implemented with fixed plain-string messages; every
dynamic value (metric name, declared vs. report number, tolerance) was routed through `detail=`
instead, keeping the generated catalogue row text exact.
**Source:** 16-01-SUMMARY.md

---

### A deterministic gate can only test the declared-artifact contract, not the skill's actual off-gate execution
The phase's own verification explicitly scoped out testing whether `dsx-reproduce` actually re-runs the
entrypoint correctly — that is prose/agent behavior, not something a deterministic gate test can
assert. Only the gate side (what it does with an already-produced report) was fully tested.

**Context:** Recorded as a "not verified here (correctly deferred)" item rather than a gap, clarifying
the boundary between what CI-style tests can prove and what remains agent-runtime behavior.
**Source:** VERIFICATION.md

---

## Patterns
### Verdict-agnostic honest-skip check
A gate check reads exactly two things from a producer-authored report: a `status` field used only to
short-circuit on an honest opt-out (SKIPPED/UNABLE), and a machine-readable numeric block used for an
independently-computed comparison — never a PASS/FAIL/verdict line as proof. The check recomputes
nothing; it recomputes only the *comparison*, from data the producer already had to include truthfully.

**When to use:** Any gate that must validate a claim made by an upstream process (skill, script,
human) it does not fully trust, especially where that process may legitimately be unable to complete
(e.g. missing interpreter) and needs an honest way to say so without either fabricating a result or
tripping a false failure.
**Source:** 16-01-SUMMARY.md

---

### AST scan for execution primitives, distinct from an import-closure hermetic test
Two orthogonal static tests are needed to guarantee "this code path never runs untrusted work": one
walks the import closure to forbid a forbidden *module* from being reachable (catches third-party
libraries); a second AST-walks call sites to forbid the stdlib execution-primitive family
(`subprocess.*`, `os.system`/`exec*`, `runpy.run_path`/`run_module`, bare `exec`/`eval`, dynamic
`compile`/`__import__`) because stdlib modules pass the import-based test silently. Anti-vacuity
requires (a) asserting the scanned set is named and non-empty, and (b) a positive control proving a
known-bad synthetic snippet is actually flagged, plus a negative control proving legitimate
metaprogramming (`ast.parse`, `re.compile`) is not confused with execution.

**When to use:** Any codebase with a "no code here shells out / executes arbitrary input" invariant
that today happens to hold — the AST+controls pattern is what turns "currently true" into "provably
enforced," since a grep or import-only check both have blind spots.
**Source:** 16-04-SUMMARY.md

---

### Additive calibration corpus tag on a sidecar, proven ignored via signature introspection
A new descriptive field is added to fixture sidecar files (not the primary spec files the calibration
math reads), and its "does not move the numbers" claim is proven mechanically: assert the field is not
in the target function's `__code__.co_varnames`, and re-pin the exact expected calibration output
value alongside the new assertion — rather than relying on human review to notice a wired-in field.

**When to use:** Extending a fixture corpus with new provenance/bookkeeping metadata that must be
countable but must never influence an existing calibrated metric (catch rate, false-positive rate,
or similar pinned headline numbers).
**Source:** 16-03-SUMMARY.md

---

### Additive catalogue rebaseline with a byte-frozen historical anchor plus an explicit delta set
When a new phase mints finding codes against a codebase whose finding catalogue is pinned by both a
total count and a set-identity snapshot test, the snapshot file itself is never edited; instead the
test is changed to assert `current_set == snapshot_set | {new_codes}` with the snapshot's own length
anchored to a *separate* literal that does not move. This keeps historical zero-mint claims from prior
phases falsifiable-if-untrue forever, while still gating the new mint non-silently.

**When to use:** Any append-only registry (finding codes, feature flags, migration versions) where
prior phases' "we minted nothing" claims are referenced elsewhere and must remain independently
checkable after a later phase legitimately does mint something.
**Source:** 16-01-SUMMARY.md

---

### Skill executes, gate declares — a hard purity split enforced by directory and import boundary
The "produce" half (executing an entrypoint, capturing fresh numbers) lives entirely in an agent-runtime
skill using Bash; the "enforce" half (checking an artifact exists and its numbers overlap) lives in a
gate module restricted to `pathlib`/`re`/`math`. The two communicate only through a filesystem artifact
and one opt-in spec field — the gate never inspects the skill's process, only what it wrote.

**When to use:** Any verification feature that legitimately needs to run untrusted or heavy work
(re-running analysis code, hitting a network resource, installing packages) but must not put that work
on a deterministic CI/gate path.
**Source:** 16-02-SUMMARY.md

---

## Surprises
### The "no gate module executes anything" invariant was already true — but had zero test coverage
Before Phase 16 began, a grep across `dsx/` for `subprocess|runpy|exec(|import_module|__import__|
os.system|popen|check_output|.run(` returned zero matches — REQ-P16-04's assertion held by accident,
not by design, with nothing in the test suite that would have caught a future regression.

**Impact:** Confirmed the phase's REQ-P16-04 was not busywork: a currently-true-but-untested invariant
is one incautious future change away from silently breaking, which is exactly what the D-09 AST scan
with positive controls now forecloses.
**Source:** 16-CONTEXT.md

---

### Verifying Phase 16 surfaced a stale hard-coded count from Phase 14, two phases prior
`tests/test_phase14_onboarding.py` hard-coded an expectation of 13 DSX skills. Phase 16's legitimate
addition of the 14th skill (`dsx-reproduce`) made that unrelated, already-shipped Phase 14 test stale,
and it was caught and fixed only during Phase 16's own verification pass rather than by anything in
Phase 14 or 15.

**Impact:** A one-line anchor bump (13→14) was folded into Phase 16's review to keep REQ-P14-04's
Triggers invariant holding across all 14 skills — a reminder that "additive" changes in one phase can
still break brittle cardinality assertions written in a much earlier phase.
**Source:** VERIFICATION.md

---

### The full pre-existing gate suite (1254 tests) stayed green through the entire mint
`sh scripts/check.sh` reported all checks passed with 1254 tests OK after all four Phase-16 plans
landed, with determinism identical and the gate contract (good passes / bad blocks / missing errors)
unchanged — despite the catalogue growing by two codes and a new skill being registered.

**Impact:** Empirically confirms the additive-rebaseline and purity-boundary decisions (D-08, D-01)
achieved their goal: a two-code mint plus a new skill registration produced zero regression anywhere
else in a thousand-plus-test suite.
**Source:** VERIFICATION.md
