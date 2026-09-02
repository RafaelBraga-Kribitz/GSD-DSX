---
phase: 17
phase_name: "Foundation — repairs and spec vocabulary"
project: "gsd-dsx"
generated: "2026-09-02"
counts:
  decisions: 9
  lessons: 5
  patterns: 6
  surprises: 4
missing_artifacts:
  - "UAT.md"
---

# Phase 17 Learnings: Foundation — repairs and spec vocabulary

## Decisions

### Add a 6th `estimand_kind` member, `nominal_association`, beyond REQ-P17-02's stated minimum five
The closed `estimand_kind` vocabulary on the `analysis:` block ships with six members instead of the
five the requirement names as a minimum: `linear_association`, `monotone_association`,
`nominal_association`, `agreement`, `method_comparison`, `ordered_trend`. `nominal_association` routes
phi (2×2) and Cramér's V (r×c) checks.

**Rationale:** The Statistician's carve is load-bearing — Cramér's V / phi on an unordered r×c table is
an **unsigned**, chi-square-based departure-from-independence measure with no slope and no direction, so
folding it into `linear_association` (a signed, slope-like Pearson quantity) would mis-carve the
estimand space and let the Phase-18 correlation scale/kind gate wave through a nominal×nominal
"correlation." REQ-P17-02 says "covering **at least**" the five, so the addition sits inside the
requirement's own grant — additive, not a scope escalation. Both personas (Architect, Statistician)
converged unanimously.
**Source:** 17-CONTEXT.md

---

### Keep the field name `estimand_kind` rather than renaming to `relationship_kind`
The Architect proposed renaming off the "estimand" stem to `relationship_kind` on the rigour ground
that `estimand_type`/`estimand_kind` are near-synonyms authors will mis-slot against
`validity_frame.estimand.type`. The orchestrator rejected the rename as drafted and kept `estimand_kind`.

**Rationale:** Two reasons: (1) `relationship_kind` is itself a misnomer — `agreement` and
`method_comparison` are precisely **not** relationships/associations, and that distinction is the whole
point of the Phase-18 gate that blocks correlation-for-an-agreement-estimand; (2) the name is inherited
scope — REQ-P17-02, the Phase 18/19 requirements, and both D-05 packs (HQ-16/HQ-17) all already say
`estimand_kind`, so a rename is cross-file churn for a worse label. The mis-slot concern is answered
**structurally**, not by a rotting note: the two axes live on different blocks
(`analysis.estimand_kind` vs `validity_frame.estimand.type`), are read at different sites
(`recommend_test` vs the admissibility adjudicator), and both ship closed-vocab membership guards with
disjoint member sets, so a swapped value fails membership loudly, never silently.
**Source:** 17-CONTEXT.md

---

### D-12a paradigm-disposition table classifies all nine Phase 18/19 gates before any of them are built
Every gate planned for Phases 18-19 (REQ-P18-03, REQ-P18-04, REQ-P19-01, REQ-P19-02, REQ-P19-04,
REQ-P19-05, REQ-P19-06a, REQ-P19-06b, REQ-P19-07) is classified paradigm-neutral, self-scoping, or
paradigm-specific, and ships accordingly. Eight ship "as-is." The ninth — the observed/post-hoc power
ban (REQ-P19-06b) — ships paradigm-neutral/self-scoping with its Bayesian sibling (a post-hoc Bayes
factor, or a posterior-based "probability of replication," presented as power) explicitly named and
**D-13-deferred**, with a falsifiable entry condition: the sibling gate enters when the catalog gains a
Bayesian post-hoc reporting surface for it to attach to.

**Rationale:** This is not the asymmetric ban D-12 forbids, because there is no live Bayesian
post-hoc-adequacy reporting surface in the catalog today to leave un-banned — naming the sibling with a
concrete trigger, rather than omitting it, avoids a silent asymmetry. The sanctioned substitute (MDE /
sensitivity power analysis, Lakens 2022) is paradigm-neutral and ships as a positive catalog row
instead.
**Source:** 17-CONTEXT.md

---

### D-06 code-range pre-allocation: one DSX-STA decade per thematic category, 050-129, reserving 130-139
Nine themed decades are pre-allocated ahead of Phases 18-19 needing them: 050-059 correlation
scale/kind match, 060-069 agreement declaration completeness, 070-079 RM sphericity / two-stage block,
080-089 trend declared-field gates, 090-099 resampling declaration quadruple, 100-109 post-hoc↔omnibus-
family match, 110-119 negative gates (variance-as-precondition; observed-power), 120-129
proportion/count extras, 130-139 reserved for Phase-20 calibration/overflow. Phase 17 itself assigns
**zero** codes from this range (REQ-P17-05).

**Rationale:** Address space is not scarce; predictability and parity with the existing tens sub-blocks
(000s reporting-contract, 010s practical-sig, 020s null-acceptance, 030s multiplicity, 040s
declared-test-match) outweigh tight packing. The densest foreseen block (110-119: variance-precondition
+ observed-power + the named-but-deferred Bayesian sibling) is ≈3-4 codes, comfortably ≤10. Both
personas ACCEPT. Blocks are keyed to theme rather than the mutable REQ-ID, since codes are permanent
under D-06 while requirement IDs churn.
**Source:** 17-CONTEXT.md

---

### Boschloo reconciliation direction: fix the code to match the already-correct doc
The live divergence — doc (`references/test-selection.md:10` + footnote `[^1]`, citing
Lydersen-Fagerland-Laake 2009) names Boschloo's exact test for the small-expected-cell two-proportion
case, but code (`dsx/checks/stats.py:65` pre-fix) emitted `fisher_exact` and `boschloo_exact` was
absent from `NONPARAMETRIC_TESTS` (`stats.py:23-26` pre-fix) — is closed by changing the **code**, not
the doc.

**Rationale:** The doc side carries the cited authority (Lydersen-Fagerland-Laake 2009 §9: Boschloo
dominates Fisher on power while holding size), and Boschloo is the more powerful exact test. A pinned
regression test locks doc and code together as the Boschloo-specific "down payment" on REQ-P20-04's
general doc/code agreement mechanism. Adds no new finding code — `boschloo_exact` is a test-name
routing string, not a `DSX-STA-*` code.
**Source:** 17-CONTEXT.md

---

### `ESTIMAND_KINDS` must be declared in `dsx/spec.py`, never in `dsx/checks/stats.py`
Even though `estimand_kind` looks like a natural sibling of `OUTCOME_TYPES` (both are routing
vocabularies `recommend_test` reads, and `OUTCOME_TYPES` lives in `stats.py`), the new constant is
declared in `dsx/spec.py` beside the pre-existing `ESTIMAND_TYPES`, and `dsx/checks/stats.py` imports it
from `..spec`.

**Rationale:** `dsx vocab`'s `cmd_vocab` calls only `describe_vocabulary()` in `dsx/spec.py`, which
iterates a fixed `_VOCABULARIES` list also defined in `dsx/spec.py` — a vocabulary living only in
`stats.py` would never surface in `dsx vocab` output unless `spec.py` imported `checks`, which the
D-03a architectural boundary forbids (enforced by an AST-based import test; PROJECT.md decision M-04:
"`dsx.spec` must never import `dsx.checks`"). Constant placement is therefore forced by the existing
registry + import-direction constraints, not a style choice.
**Source:** 17-RESEARCH.md (Anti-Patterns to Avoid); executed per 17-03-PLAN.md, confirmed in
17-03-SUMMARY.md.

---

### Widen the existing `DSX-STA-040` check into a membership loop instead of minting a new finding code
The `estimand_kind` membership guard reuses `DSX-STA-040` (previously scoped to `analysis.outcome_type`
alone) by turning it into a single-call-site loop over a tuple of `(field_name, vocabulary)` pairs —
`(outcome_type, OUTCOME_TYPES)` and `(estimand_kind, ESTIMAND_KINDS)` — mirroring the existing
multi-field-one-code idiom `dsx/spec.py` already uses for `DSX-SPEC-082`/`DSX-SPEC-085`
(`_VALIDITY_FRAME_MEMBERSHIP`, `_INFERENCE_MEMBERSHIP`).

**Rationale:** REQ-P17-05 forbids minting a new code this phase, and the catalogue generator
(`scripts/gen-finding-catalogue.py`) extracts codes by AST-walking `report.add(...)` call sites — it
counts a call site once regardless of how many times a runtime loop invokes it, so widening the loop's
tuple is the only code-neutral path to giving `estimand_kind` the same "loud, not silent" membership
guarantee `outcome_type` already has.
**Source:** 17-RESEARCH.md (Pattern 1, "One finding code, many checked fields")

---

### Register `ESTIMAND_KINDS` under the singular dump key `estimand_kind`, deviating from plural naming
The constant itself is named `ESTIMAND_KINDS` (plural, matching the sibling `ESTIMAND_TYPES`), but it
is registered in `_VOCABULARIES` under the **singular** dump key `estimand_kind`, not the plural
`estimand_kinds` a naming-convention-only reading would suggest.

**Rationale:** The singular key matches both the analysis-block FIELD name (`analysis.estimand_kind`)
and the binding 17-VALIDATION.md oracle `describe_vocabulary()["estimand_kind"]`; the field name and
the validation contract win over strict constant/key-name parity. Surfaced explicitly in the plan as a
deliberate choice, not left as a silent inconsistency.
**Source:** 17-03-PLAN.md ("Planner note on the dump key")

---

### The membership loop runs independently of `_check_declared_test`'s early return, tightening `outcome_type`'s existing behaviour
`_check_declared_test` previously opened with `if not declared or not outcome_type: return`, meaning a
spec declaring only `analysis.outcome_type: nonsense` with no `test:` field produced **no**
`DSX-STA-040` finding at all. Rather than give `estimand_kind` its own differently-gated check, the
plan moves the whole membership loop above that early return, so **both** `outcome_type` and
`estimand_kind` now fire independently of whether a test is declared.

**Rationale:** Nesting the new `estimand_kind` check inside the existing early return would make it a
silent no-op whenever no test is declared — directly contradicting D-01's "never a silent no-op"
language. The alternative (keep `outcome_type` gated as before, give `estimand_kind` its own ungated
check reusing the same code from a second call site) was rejected because a second static call site
with different literal title text would trigger the catalogue generator's "declared twice with
different text" warning; using an identical f-string shape at one call site avoids it. This is a
deliberate, tested behavioural tightening of `outcome_type`'s pre-existing check, not an accidental one
— confirmed safe by grepping `examples/` for a fixture that relied on the old silent exemption (none
found) and by the full suite staying green.
**Source:** 17-RESEARCH.md (Pitfall 2); executed per 17-03-PLAN.md Task 2, confirmed in 17-REVIEW.md.

---

## Lessons

### A Wave-1 plan that runs only its own targeted tests can miss a cross-file regression until the next wave's full-suite gate
The 17-01 (Boschloo) firing changed the two-proportion alternative from `fisher_exact` to
`boschloo_exact` and ran only `test_boschloo_reconciliation` plus `test_finding_catalogue_invariant`
after committing, per its own plan's verify block — it did not run the full suite. This let
`tests/test_dsx.py`'s REQ-P11-05 pinned golden snapshot `_BASELINE_TWO_PROPORTION_NO_SPEC` (which still
asserted `fisher_exact (any expected cell < 5)`, with a now-false provenance comment claiming "stats.py
byte-identical to v1.4.0 / recommend_test never changed") go undetected until the Wave-2 (17-03) merge
gate ran `python -m unittest discover -s tests -q` from a clean tree.

**Context:** Fixed as a 17-01 commit (`06d4cf6`) rather than folded into 17-03 — updating the snapshot
value, the false comment, and the docstring to the reconciled reality
(`test-selection.md:10` and `stats.py:75` both name Boschloo; `git log v1.4.0..HEAD -- dsx/checks/stats.py`
confirms `stats.py` did change). This is REQ-P17-01's intended effect surfacing late, not a new defect,
but it shows plan-scoped targeted-test verification is not sufficient on its own for changes that ripple
into another file's pinned golden values.
**Source:** 17-03-SUMMARY.md

---

### Genericizing a finding's message text changes the catalogue's rendered row even when the finding CODE does not change
Widening `DSX-STA-040`'s message from a hardcoded literal
(`f"analysis.outcome_type {outcome_type!r} is not recognised"`) to a templated form
(`f"analysis.{field_name} {value!r} is not recognised"`) changes what `scripts/gen-finding-catalogue.py`'s
AST walker extracts as the row's Finding-column text — literal segments render verbatim, interpolated
segments render as `<...>` placeholders — so `references/finding-codes.md` goes stale relative to the
code even though the code SET is unchanged.

**Context:** Anticipated in 17-RESEARCH.md (Pitfall 1) and confirmed in execution: Task 3 of 17-03
regenerated the catalogue via `scripts/gen-finding-catalogue.py --write` (never hand-edited) and
verified `--check` exits 0 afterward, while `tests/fixtures/finding-codes-phase12.md` (compared only by
code set, not text) stayed byte-frozen and unaffected.
**Source:** 17-RESEARCH.md (Pitfall 1); 17-03-PLAN.md Task 3; 17-03-SUMMARY.md

---

### `from __future__ import annotations` makes a missing typing import invisible to the entire test suite
`dsx/checks/stats.py` annotated `_MEMBERSHIP_FIELDS: "tuple[tuple[str, Any], ...]"` without importing
`Any` (unlike the sibling `_VOCABULARIES` pattern in `dsx/spec.py`, which does import it). Because the
module uses `from __future__ import annotations`, the annotation is a quoted string never evaluated at
runtime, so this produced zero test failures anywhere in a 1323-test suite.

**Context:** Found only by code review (17-REVIEW.md F1), not by any automated oracle — a latent defect
for any type-checker or a `typing.get_type_hints(stats)` call, and an inconsistency with the module it
mirrors. Fixed same-firing by adding `from typing import Any`; re-gated green.
**Source:** 17-REVIEW.md

---

### Removing an existing check's implicit early-return gating is a real behavioural change that needs explicit safety verification, not just a "loud not silent" design goal
Moving the `outcome_type`/`estimand_kind` membership loop above `_check_declared_test`'s
`if not declared or not outcome_type: return` guard makes `outcome_type` membership fire in cases where
it previously did not (a spec with `outcome_type` but no declared `test:`). CONTEXT.md's D-01 mandated
"never a silent no-op" for the *new* `estimand_kind` field but did not explicitly authorise changing
`outcome_type`'s pre-existing behaviour at that granularity.

**Context:** Treated as a deliberate in-scope tightening rather than an accidental regression, but only
after two concrete checks: grepping `examples/` for any fixture that declared `outcome_type` without a
`test:` and relied on the old silent exemption (none found), and confirming the full suite stayed green
after the change (no golden/snapshot test expected the previously-silent path).
**Source:** 17-RESEARCH.md (Pitfall 2); 17-REVIEW.md

---

### The automated `/gsd-execute-phase` branching path can compute a branch name that silently diverges from the actual ceremony branch
The framework's `handle_branching`/subagent-wave path computes `branch_name: gsd/v2.3-test-catalog`
(missing the `.0`), which mismatches the real ceremony branch `gsd/v2.3.0-test-catalog`. Using it would
fork work off `main` instead of the correct branch, orphaning everything already committed to Phase 17.

**Context:** Documented as a standing anti-pattern in `.continue-here.md`, binding for every remaining
execute step in the milestone (S2-3/S3-3/S4-3): execute inline as orchestrator instead, and assert
`git rev-parse --abbrev-ref HEAD` equals `gsd/v2.3.0-test-catalog` both before and after each firing.
**Source:** .continue-here.md

---

## Patterns

### One finding code, many checked fields (multi-field membership loop)
A single `report.add(CODE, ...)` call site sits inside a `for field_name, vocab in TUPLE:` loop; whichever
field fails membership, the SAME code fires with a field-name-interpolated message. Because the
catalogue generator (`scripts/gen-finding-catalogue.py`) finds a `report.add(...)` call site once by AST
walk regardless of how many times a runtime loop invokes it, adding a new field to the loop's tuple never
mints a new catalogue row. Pre-existing in `dsx/spec.py` for `DSX-SPEC-082`/`DSX-SPEC-085`
(`_VALIDITY_FRAME_MEMBERSHIP`, `_INFERENCE_MEMBERSHIP`); reused this phase in `dsx/checks/stats.py` for
`DSX-STA-040` over `(outcome_type, OUTCOME_TYPES)` and `(estimand_kind, ESTIMAND_KINDS)`.

**When to use:** Whenever a new field needs the same "loud, not silent" closed-vocabulary membership
behaviour an existing field already has, but the change budget forbids minting a new finding code.
**Source:** 17-RESEARCH.md (Pattern 1); 17-03-SUMMARY.md

---

### Doc↔code regression pin
A test reads a reference markdown doc via `pathlib`, whitespace-collapses it (never a line-anchored
regex, per the repo's CRLF rule), and asserts it still names what the routing table in code emits —
binding a human-readable doc to the machine-enforced behaviour without generating the doc from the code.
Used to pin `references/test-selection.md`'s Boschloo name against `recommend_test`'s emitted
`boschloo_exact` alternative.

**When to use:** Any place a documentation file makes a claim (a citation, a named test, a routing
statement) that the code is expected to match, but no automated generator produces the doc from the
code yet — the pin closes the drift risk cheaply until such a generator exists.
**Source:** 17-01-SUMMARY.md (tech-stack.patterns); 17-CONTEXT.md D-04

---

### Structural / source-scan regression pin
`inspect.getsource(fn)` plus a negative, whitespace-tolerant, quote-agnostic regex asserts that a
routing property (e.g. "reaches `log_rank` only by unconditional fallthrough") holds by the *absence* of
a specific guard in the function's source — not just by the function's current output. A future
contributor who adds the forbidden guard turns the test red, forcing a deliberate, reviewed contract
change instead of a silent reroute.

**When to use:** Pinning a "correct by fallthrough, not by explicit branch" contract before later work
adds new branches to the same dispatch function that could otherwise silently change routing for an
existing case.
**Source:** 17-02-SUMMARY.md (tech-stack.patterns); 17-RESEARCH.md ("The exact `time_to_event`
fallthrough target")

---

### Dual behavioural + structural test idiom, one module, two legs
A single `unittest.TestCase` module pairs a behavioural leg (assert the function's actual output over a
representative input matrix) with a structural leg (assert something about the function's own source via
`inspect.getsource`). Modelled explicitly on the pre-existing `tests/test_no_shapiro_autoswitch.py`
template and reused for both `test_boschloo_reconciliation.py` and `test_time_to_event_fallthrough.py`.

**When to use:** Any regression pin where "the output is currently correct" and "the source has no
shortcut/guard that could make it wrong later" are both worth asserting — the structural leg is the part
that gives the pin teeth against future edits, not just against present behaviour.
**Source:** 17-RESEARCH.md; 17-02-PLAN.md

---

### Reconcile-then-pin: lock a divergence class the moment it is fixed
The instant a doc/code (or two-artifact) divergence is reconciled, a regression test is added in the
same change that binds the two sides together, so the same class of divergence cannot recur silently
later. Explicitly framed as a narrow "down payment" on a more general mechanism (REQ-P20-04's future
doc/code agreement test) rather than a one-off fix.

**When to use:** Whenever fixing a specific instance of a drift bug (doc says X, code does Y) — pair the
fix with a pin in the same commit rather than trusting code review or documentation discipline to prevent
recurrence.
**Source:** 17-01-SUMMARY.md (patterns-established)

---

### Zero-new-code widening via AST call-site dedup
Because the catalogue generator identifies a finding code by its `report.add(...)` **call site** (found
once via AST walk) rather than by runtime invocation count, a finding code's scope can be widened to
cover additional fields/checks from a single call site without minting a new code — provided every
invocation uses an identical literal message shape (a second call site with *different* literal text
triggers the generator's non-fatal "declared twice with different text" warning).

**When to use:** Any zero-new-code budget (like REQ-P17-05) where an existing check's coverage needs to
grow — widen the loop feeding the existing call site rather than adding a new call site or a new code.
**Source:** 17-RESEARCH.md (Pattern 1, Pitfall 2)

---

## Surprises

### A two-phase-old golden snapshot's "byte-identical" provenance comment was falsified by this phase's own deliberate change
`tests/test_dsx.py`'s REQ-P11-05 pinned baseline `_BASELINE_TWO_PROPORTION_NO_SPEC` carried a comment
and docstring literally asserting `stats.py` was "byte-identical to v1.4.0" and that `recommend_test`
"never changed" — a claim that was true right up until Phase 17's own REQ-P17-01 reconciliation
(commit `99622fe`) deliberately changed the two-proportion alternative from `fisher_exact` to
`boschloo_exact`. Nothing caught the now-false claim until the Wave-2 full-suite merge gate.

**Impact:** Confirms that "byte-identical to a prior version" provenance comments in golden snapshots
are landmines for the first legitimate change to the file they describe — and that per-plan targeted-test
verification (as opposed to a full-suite run) is not sufficient to catch that class of cross-file
regression before the next wave's merge gate.
**Source:** 17-03-SUMMARY.md

---

### A missing `typing.Any` import produced zero test failures anywhere in a 1323-test suite
`dsx/checks/stats.py` used `Any` in a quoted type annotation without importing it. Because the module
carries `from __future__ import annotations`, the annotation string is never evaluated at runtime, so
every one of the phase's automated oracles (unit tests, the catalogue invariant, the full suite,
`scripts/check.sh`) passed green with the import gap present.

**Impact:** The gap was invisible to every deterministic gate this phase relies on and was found only by
a human/agent code-review pass reading the diff line-by-line (17-REVIEW.md F1) — a concrete demonstration
that this codebase's test-suite-as-oracle discipline has a structural blind spot around annotation-only
symbols under `from __future__ import annotations`.
**Source:** 17-REVIEW.md

---

### Widening `DSX-STA-040` to cover two fields did not trigger the catalogue generator's "declared twice" warning — exactly as research predicted
`scripts/gen-finding-catalogue.py` maintains a pre-existing, non-fatal warning set for codes whose
`report.add(...)` text differs across call sites (VAL-060, CLM-020/021, COH-030, PAR-002, SPEC-070,
VAL-021). Despite `DSX-STA-040` now firing for both `outcome_type` and `estimand_kind` from a widened
loop, it does not appear in that warning set.

**Impact:** Empirically validates 17-RESEARCH.md's Pitfall-2 recommendation (use an identical f-string
shape at the single call site) played out exactly as designed, with the generator's own warning mechanism
serving as an independent confirmation rather than something that had to be manually verified against the
generator's internals.
**Source:** 17-REVIEW.md; 17-RESEARCH.md (Pitfall 2)

---

### The full pre-existing suite grew to 1323 tests and stayed entirely green through the whole zero-mint phase
Baseline was 1312 tests green before any Phase 17 edit (recorded in 17-01-SUMMARY.md); after all three
plans landed, `python -m unittest discover -s tests -q` reported 1323 tests OK from a clean tree
(17-03-SUMMARY.md), and `scripts/check.sh` reported all checks passed — catalogue current at 260 codes
by set identity, capability conformant, gate contract (good passes / bad blocks / missing exits 2), and
determinism identical.

**Impact:** Empirically confirms the phase's core design goal — reconcile a divergence, add a vocabulary,
pin two regression contracts, all while minting zero new finding codes — produced no collateral
regression anywhere else in a thousand-plus-test suite, even though DSX-STA-040's behaviour was
deliberately tightened (Pitfall-2 resolution) along the way.
**Source:** 17-01-SUMMARY.md; 17-03-SUMMARY.md; 17-VERIFICATION.md
