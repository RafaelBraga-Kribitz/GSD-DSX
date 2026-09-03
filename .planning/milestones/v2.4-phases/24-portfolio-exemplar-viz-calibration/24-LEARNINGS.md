---
phase: 24
phase_name: "portfolio-exemplar-viz-calibration"
project: "gsd-dsx"
generated: "2026-09-03"
counts:
  decisions: 6
  lessons: 6
  patterns: 5
  surprises: 4
missing_artifacts:
  - "UAT.md"
---

# Phase 24 Learnings: portfolio-exemplar-viz-calibration

## Decisions

### Upgrade the existing exemplar in place rather than author a net-new question
The `examples/good-*` onboarding-activation exemplar was upgraded **in place** into the v2.4 capstone instead of authoring a new analytical question. The capstone reuses the proven-green statistics verbatim and adds only the v2.4 presentation delta: figures through the style layer, one honest uncertainty figure (real 95% CI 1.0-3.8pp via `DSX-VIZ-071`), a sealed manifest, a strict What/So What/Now What narrative, and a REPRO-REPORT.

**Rationale:** Architect, Statistician, and Auditor personas unanimously chose reuse: a net-new spec would re-open power, estimand, SRM, and multiplicity questions already discharged, which is gratuitous risk on a terminal phase for no integration-coverage gain. This is "the smaller, provable claim" — reuse proven statistics, add only the genuinely new presentation surface, on load-bearing content (the existing spec already carries a CI and a BH-corrected three-metric family).
**Source:** 24-CONTEXT.md

---

### Author the first bad-chart-choice fixtures on the existing known-bad convention, minimal-honest code set
Four new fixtures were added to `examples/known-bad/`, mirroring the existing `<slug>-ANALYSIS-SPEC.yaml` + `<slug>-POSTMORTEM.md` convention. The set was scoped to exactly the codes that are genuinely new or newly-routed this milestone: `gauge` and `word_cloud` as new refusal rows under existing `DSX-VIZ-001`, one pre-existing banned-type control (`radar`), and one fixture for the milestone's only net-new code, `DSX-VIZ-071`.

**Rationale:** "Minimal-honest set" — cover exactly what REQ-P24-02 ("per new code") requires and no more, so the fixture set reflects genuine new coverage rather than padding the corpus with defects unrelated to what v2.4 actually changed.
**Source:** 24-CONTEXT.md

---

### Treat REQ-P24-03 as verify-not-build
REQ-P24-03 ("catalogue current, snapshots unmutated, doc/code agreement on both selection surfaces") was scoped as **confirming** that `test_doc_code_agreement.py` and `test_selection_heuristic_docs.py` are green on the final tree, not rebuilding them. Any gap closure was authorized only if research found a genuine one, and then only that narrow gap — no speculative new selection-surface test.

**Rationale:** Both doc/code agreement tests already exist and were green at their originating phases' close; treating the requirement as an audit rather than a build avoids scope creep on a phase whose entire purpose is proving nothing drifted.
**Source:** 24-CONTEXT.md

---

### Mint zero new finding codes this phase (D-06)
Phase 24 was explicitly scoped to mint **zero** new finding codes. All fixtures, the exemplar's new visual, and the audit-prerequisite work route only to existing codes. Target: set-identity 276 -> 276, re-measured live at plan time rather than assumed from a prior count.

**Rationale:** Phase 24 is calibration and integration, not new machinery — a mint here would mean the phase quietly expanded scope beyond its stated purpose. Recorded loudly with a standard silence-equals-accept veto window rather than escalated, since D-06 numeric assignments are ordinary persona-round decisions.
**Source:** 24-CONTEXT.md

---

### Report the MEDIUM catch rate beside the headline, never fold it in
`DSX-VIZ-071` fires at MEDIUM severity, and `viz`/`figures` checks run only at verify/ship, which block at HIGH by default — so a MEDIUM-only fixture exits 0 everywhere and cannot register in the existing CRITICAL or HIGH catch-rate strata. Rather than change the code's severity or mislabel it as an ABSENT "miss," a new `_MEDIUM_TARGET_DEFECT_CODES` stratum was added, gated with `--block-on MEDIUM`, and its `medium_catch_rate` is reported as a **fourth** readout beside the (miss-rate, FPR) headline, with an explicit assertion that the headline is byte-identical before and after the MEDIUM stratum runs.

**Rationale:** Folding an easy MEDIUM catch into the headline would inflate the corpus's apparent coverage; keeping it a separate, explicitly-invariant readout preserves the catch-rate/FPR instrument's honesty (mirrors the existing HIGH stratum's own D-06-style invariance).
**Source:** 24-RESEARCH.md (Risk P1); 24-02-PLAN.md Task 3

---

### Close the chart-selection live-dict binding gap
`test_selection_heuristic_docs.py` bound the chart-selection relationship vocabulary only to a hardcoded `_RELATIONSHIPS` tuple, one-directional, never importing the live `RELATIONSHIP_CHARTS` dict — the only guard against drift was a *transitive* len==11 pin in a different test. The plan-checker's final call (flagged as RECOMMENDED, not mandatory, in the plan) was to close this gap with one both-directions assertion.

**Rationale:** On the terminal viz-integrity phase, a direct both-directions binding is exactly the drift-guard that belongs in the doc/code agreement surface itself; the close is non-speculative — one assertion, honoring "close exactly that gap and no more." `test_doc_code_agreement.py`'s own deliberate one-directionality was explicitly left untouched (documented-by-design, not a gap).
**Source:** 24-03-SUMMARY.md; 24-RESEARCH.md Q3

---

## Lessons

### The REPRO-REPORT path resolves differently from every other spec path field
Unlike every other path field in the spec (e.g. `narrative.path`, which resolves via `resolve_root`), `reproducibility.reproduce_report` is resolved by `dsx/cli.py`/`repro.py` against the raw `phase_dir` (CWD-relative fallback when `phase_dir` is `None`), not `resolve_root`. Writing the path spec-dir-relative (matching the narrative field's convention) caused `DSX-REP-060` HIGH to fire when the good-fixture-gating tests ran from repo-root CWD, flipping 16 tests red. This was caught only because the corpus test suite was run and trusted over a single ship-gate exit 0.

**Context:** Fixed within the same plan by writing the path repo-root-relative (`examples/good-REPRO-REPORT.md`), which resolves correctly both under the CLI invocation and the test harness. The underlying `phase_dir`-vs-`resolve_root` asymmetry in `dsx/cli.py`/`repro.py` is a real latent inconsistency but was correctly ruled out of the exemplar-only scope rather than "fixed" opportunistically.
**Source:** 24-01-SUMMARY.md

---

### Committed SVGs need an explicit binary git-attribute or the seal doesn't survive checkout
Sealed SVG bytes (matplotlib's Windows CRLF output) can be normalized by git's `autocrlf` on checkout, changing the committed blob and breaking the `dsx seal` hash it was supposed to match — silently and only on some platforms/checkouts, not the authoring machine.

**Context:** Fixed with a `.gitattributes` rule marking `examples/figures/*.svg binary`, added in a separate follow-up commit after the initial seal. Verified afterward that the committed index blobs seal to exactly the recorded `spec.visuals[].svg_sha256` values. Without this, a fresh or cross-platform checkout would fire `DSX-FIG-010` CRITICAL even though the local working tree looked fine.
**Source:** 24-01-SUMMARY.md

---

### The exemplar's ship-gate acceptance test is trail-sensitive; a bare run is not the real acceptance criterion
The correct way to reproduce the exemplar's "passes every gate" claim is the full sequence `dsx gate plan -> execute -> verify -> ship`, all sharing one swept `examples/DECISIONS.jsonl` on a clean, isolated trail — not a bare `dsx gate ship` call, and not a run interleaved with the rest of the test suite.

**Context:** A bare `dsx gate ship` on an empty trail legitimately exits 2 (no recorded plan-time frame lock to reconcile against); a run interleaved with the full suite picks up a stray `DECISIONS.jsonl` with a mismatched frame digest and false-fails on `DSX-PRE-020`/`DSX-PRE-041`. Neither is a defect in the shipped tree — both are procedure mistakes. Carried forward as a recommendation for the S5 milestone audit: always sweep every `DECISIONS.jsonl` and gate the exemplar as a fresh plan-to-ship sequence.
**Source:** 24-REVIEW.md

---

### A new corpus fixture touches three tree-wide registries beyond the plan's named files
The plan for 24-02 named only `tests/test_known_bad_corpus.py` as modified, but three *other* tests each iterate every committed spec and require a per-fixture entry for any new one: `test_dsx.py`'s hardcoded estimand-declaration count pin (19 -> 23), `test_frame_val.py::_EXPECTED_VAL_CODES` (4 new `set()` entries), and `test_causal_verb_golden.py::_GOLDEN_SHIP_FINDINGS` (4 new golden entries).

**Context:** Each value was measured against the fixture as actually committed (not guessed) before being written in. This is a structural property of any corpus that includes "every committed spec" registries — adding a fixture is not confined to the file that seems to own it.
**Source:** 24-02-SUMMARY.md

---

### matplotlib color arguments and .mplstyle prop-cycle hexes are not parsed the same way
Direct color keyword arguments passed to matplotlib calls (e.g. `axhline(color=...)`) require a `#` prefix on hex color strings, while the `.mplstyle` file's `axes.prop_cycle` hex values are written bare because the `cycler` machinery parses them differently.

**Context:** Discovered as an authoring bug while writing `examples/analysis/charts.py`'s direct color args (`#5c5859`, `#222222`) against the `dsx-urban.mplstyle` house style.
**Source:** 24-01-SUMMARY.md

---

### A MEDIUM-severity finding can be invisible to catch-rate instrumentation that only measures CRITICAL and HIGH strata
`DSX-VIZ-071` fires MEDIUM, and `viz`/`figures` checks are registered only at verify/ship, which block at HIGH by default. A fixture whose only finding is that MEDIUM code therefore exits 0 at every default gate point, so it cannot register as a catch in either the CRITICAL stratum (viz isn't even registered at plan/execute) or the HIGH stratum (which requires the code to fire as a blocking HIGH finding).

**Context:** This was the phase's principal design landmine, identified during research before any fixture was authored, and is what motivated adding the dedicated MEDIUM stratum with `--block-on MEDIUM` rather than trying to force the finding through existing machinery.
**Source:** 24-RESEARCH.md (Risk P1)

---

## Patterns

### Measure fixture findings through the real corpus harness, before and after authoring
Before authoring each bad-chart fixture, the chosen base spec was run through the real corpus harness (`_gate_findings`: fresh tempdir + seeded entrypoint + plan header) to confirm it produces zero findings; after authoring, each fixture was re-measured through the same harness rather than predicted from reading the checker source.

**When to use:** Any time a fixture or test case is meant to trip an exact, minimal set of findings — measuring through the actual enforcement path catches incidental findings (e.g. a stray MEDIUM from an omitted field) that source-reading alone would miss, and keeps registry entries (target-defect maps, POSTMORTEMs) honest rather than guessed.
**Source:** 24-02-SUMMARY.md

---

### Report a new severity stratum beside the headline, with an explicit invariance assertion
When a new class of finding can't be captured by an existing catch-rate/FPR stratum (e.g. a different blocking threshold), add a dedicated stratum and report its rate as an additional, clearly-separate readout, plus an assertion proving the pre-existing headline metric is unchanged by the new stratum's addition.

**When to use:** Any calibration or coverage instrument where a reviewer needs to trust that adding new "easy" test cases didn't quietly inflate an existing headline number. Precedented at Phase 12/20 and reused as-is for the MEDIUM stratum here.
**Source:** 24-02-PLAN.md Task 3; 24-REVIEW.md Risk 4

---

### Re-seal every affected artifact after any re-render, not just the changed ones
When re-rendering figures through a new style layer changes their bytes, every `svg_sha256` seal that depended on the old bytes goes stale and must be regenerated via the single hashing authority (`dsx seal`) — including figures whose *content* didn't conceptually change, only their rendering pipeline.

**When to use:** Any time a rendering pipeline, style, or generator is swapped underneath already-sealed artifacts. Missing even one stale seal produces a CRITICAL hash-mismatch finding at the next gate run.
**Source:** 24-01-PLAN.md Task 2 (Risk P2); 24-01-SUMMARY.md

---

### Prove determinism by running the generator twice and diffing sealed hashes
Deterministic re-render was proven operationally, not asserted: running the figure generator twice in a row and confirming `dsx seal` returns byte-identical digests both times, matching the sealed `spec.visuals[].svg_sha256`, rather than relying on the style layer's documented determinism guarantees alone.

**When to use:** Whenever a reproducibility claim ("this figure/pipeline is deterministic") needs to be load-bearing for a gate or audit — a live double-render-and-diff is stronger evidence than trusting the mechanism (fixed hashsalt, path-baked glyphs, suppressed timestamp) in isolation.
**Source:** 24-01-SUMMARY.md

---

### Base a corpus fixture on a clean, proven-passing spec plus exactly one injected defect
Each bad-chart fixture was created by copying a spec from `examples/good-corpus/` (already proven to pass `dsx validate` and exit 0 at plan/execute) and changing exactly one `visuals[]` field to the intended defect, deliberately omitting adjacent fields (`relationship`, `artifact_path`, `data_input_type`) that would otherwise trip a second, unintended finding.

**When to use:** Authoring any negative/adversarial test fixture where the goal is to isolate exactly one target defect for a coverage or catch-rate assertion — starting from a known-clean base and injecting a single minimal change keeps the fixture's "only finding" claim actually true.
**Source:** 24-RESEARCH.md Fixture recipe; 24-02-PLAN.md Task 1

---

## Surprises

### The exemplar's ship gate is trail-sensitive in ways a single test run won't reveal
A bare `dsx gate ship` on an empty trail exits 2, not 0 — it legitimately requires a prior recorded plan-time frame lock from `dsx gate plan` to reconcile against. Separately, running the ship gate interleaved with the full test suite picks up a stray `examples/DECISIONS.jsonl` carrying a *different* frame digest (from test fixtures gating the same spec_id), causing a false failure on `DSX-PRE-020` CRITICAL + `DSX-PRE-041` HIGH.

**Impact:** Neither behavior is a code defect, but both make the exemplar's "passes every gate" claim easy to mis-verify. The correct acceptance procedure (fresh plan->execute->verify->ship on a swept trail) had to be established and is now carried forward as an explicit methodology note for the S5 milestone audit.
**Source:** 24-REVIEW.md; 24-VERIFICATION.md

---

### git's autocrlf can silently break a sealed SVG's committed hash
On this authoring machine, autocrlf round-tripped harmlessly, but the mechanism was confirmed to normalize matplotlib's Windows-CRLF SVG output on checkout in general, meaning the git-stored blob would not equal the exact bytes that were sealed — with no local symptom to catch it.

**Impact:** Without the `.gitattributes` binary rule added as a follow-up fix, a fresh clone or a cross-platform checkout would fire `DSX-FIG-010` CRITICAL at the next gate run, even though the phase's own gate evidence showed a clean pass. This is a class of failure that only manifests on a checkout the author didn't test.
**Source:** 24-01-SUMMARY.md

---

### The initial fix for the repro-path regression was a workaround that masked a real bug
The first attempt to fix the `DSX-REP-060` regression used a `--phase-dir` flag to make the CLI invocation resolve the report path — which worked for that one invocation but did not fix the underlying inconsistency (that `reproduce_report` resolves against `phase_dir`/CWD while other path fields resolve against `resolve_root`), and would not have generalized to the test harness's own invocation pattern.

**Impact:** The eventual real fix (writing the path repo-root-relative) removed the need for the `--phase-dir` workaround entirely and restored the full suite to green. The underlying `phase_dir`-vs-`resolve_root` asymmetry in `dsx/cli.py`/`repro.py` remains a real latent inconsistency in the codebase, explicitly documented as out of this phase's exemplar-only scope rather than silently left unmentioned.
**Source:** 24-01-SUMMARY.md; 24-REVIEW.md

---

### A "doc/code agreement" test can bind only to a hardcoded mirror and never touch the live code
`test_selection_heuristic_docs.py` — nominally the test that guards the chart-selection documentation against the live code — turned out to check the documentation against a hardcoded `_RELATIONSHIPS` tuple maintained by hand inside the test file itself, never importing `RELATIONSHIP_CHARTS` from `dsx/checks/viz.py` at all. The only thing actually catching drift between the doc and the live dict was a size-only pin (`len == 11`) in a completely different test module.

**Impact:** A genuine gap that a superficial "is this test green" check would never have surfaced, since the test does pass reliably — it just isn't testing what its name implies. Closed with one additional both-directions assertion rather than left in place, per the plan-checker's ruling.
**Source:** 24-RESEARCH.md Q3

---
