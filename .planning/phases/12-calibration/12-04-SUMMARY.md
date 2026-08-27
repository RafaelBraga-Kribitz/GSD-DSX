---
phase: 12-calibration
plan: 04
subsystem: test-fixtures / calibration
status: complete
requirements: [REQ-P12-03]
tags: [good-corpus, fpr-denominator, control-specs, golden-file, D-04, D-18]
dependency_graph:
  requires:
    - "tests/test_causal_verb_golden.py::_ship_findings (fresh-tempdir measurement helper)"
    - "examples/good-ANALYSIS-SPEC.yaml (n=1 clean-spec baseline for shape)"
  provides:
    - "examples/good-corpus/ — 12 clean control specs (the FPR denominator, D-04)"
    - "per-spec noise-handling decision + measured golden set (consumed by plan 12-05)"
  affects:
    - "plan 12-05 (stratified rate / FPR harness — globs examples/good-corpus/)"
tech_stack:
  added: []
  patterns:
    - "minimal-reference route: reference only committed, cwd-resolvable artifacts so a fresh-tempdir ship run fires no artifact-stripping noise codes"
    - "cwd-fallback resolution: claim evidence + narrative.path + entrypoint resolve via Path.cwd() (repo root), so no tempdir sibling-seeding is needed by plan 12-05"
key_files:
  created:
    - "examples/good-corpus/_control_readout.py (shared reproducibility entrypoint)"
    - "examples/good-corpus/*-ANALYSIS-SPEC.yaml (12 clean control specs)"
    - "examples/good-corpus/*-NARRATIVE.md (12 per-spec deliverables, double as claim evidence)"
  modified:
    - "tests/test_causal_verb_golden.py (12 new _GOLDEN_SHIP_FINDINGS entries, all frozenset())"
metrics:
  specs_added: 12
  paradigms: 2
  outcome_shapes: 3
  finding_codes_minted: 0
  completed: 2026-08-27
---

# Phase 12 Plan 04: Good-side FPR Control Corpus Summary

A multi-spec good-side control corpus of **12 genuinely clean ANALYSIS-SPECs** under
`examples/good-corpus/`, spanning both paradigms (6 frequentist, 6 Bayesian) and all three
outcome shapes (binary/proportion ×4, continuous ×4, count/ratio ×4), so REQ-P12-03's
false-positive rate is a rate with resolution (a denominator of 12, not 1) rather than 0/1
(D-04). Each spec is a genuinely clean analysis that passes `dsx validate` with no CRITICAL
on its own merits and whose measured fresh-tempdir ship-time CRITICAL/HIGH finding set is
`frozenset()`; each has a matching `_GOLDEN_SHIP_FINDINGS` entry, and zero finding codes were
minted (D-18).

## What was built

- **`examples/good-corpus/` — 12 clean control specs**, glob-discovered by the standard
  `-ANALYSIS-SPEC.yaml` suffix (no hardcoded list).
- **12 per-spec `<slug>-NARRATIVE.md` deliverables**, each doubling as the claim's evidence
  pointer (a claim is mandatory — DSX-CLM-001 fires unconditionally when `claims` is absent —
  and a mandatory claim forces a resolvable narrative via DSX-NAR-001 and resolvable evidence
  via DSX-CLM-031).
- **One shared `_control_readout.py` entrypoint**, referenced by repo-root-relative path so the
  reproducibility code-pointer check (DSX-REP-030/031) resolves.
- **12 `_GOLDEN_SHIP_FINDINGS` entries** in `tests/test_causal_verb_golden.py`, one per spec,
  each measured `frozenset()`.

## Design decision: minimal-reference via cwd-resolvable committed artifacts

The plan's preferred **minimal-reference route** cannot be taken literally to mean "reference
no artifacts at all," because three ship-gate checks make content mandatory for a clean shipped
analysis: `claims` is required (DSX-CLM-001, unconditional), a present claim forces a resolvable
`narrative.path` (DSX-NAR-001 at ship) whose body must contain the claim text (DSX-NAR-020) and
a resolvable `evidence` pointer (DSX-CLM-031), and `reproducibility.entrypoint` is required
(DSX-REP-030) and must resolve (DSX-REP-031).

The route taken removes the noise **at the source** exactly as the plan intends: every
referenced artifact is **committed and resolves from `cwd` (the repo root)** — claim evidence
and `narrative.path` resolve via the `[phase_dir, cwd]` root list, and the entrypoint resolves
via its repo-relative path. Data assertions / `profile_path`, `visuals[].artifact_path`, and
DATA-PROFILE references are simply **omitted**, so DSX-DQ-001, DSX-FIG-001 never have anything
to fail against. The net effect is the plan's stated goal: every spec's measured golden set is
`frozenset()`, and — because resolution is via `cwd`, not via `--phase-dir` — **plan 12-05 needs
no tempdir sibling-seeding**; the FPR count is honestly zero for all 12.

This is deliberately **not** the "seed route" the plan describes (committing siblings so 12-05
seeds them into the tempdir): nothing here depends on tempdir seeding. It is a third, cleaner
outcome — committed-and-cwd-resolvable references — recorded here for plan 12-05 to consume.

## Per-spec record (paradigm · outcome shape · noise decision · measured golden set)

All twelve measured via the golden test's own fresh-tempdir `_ship_findings` helper on
2026-08-27 — never guessed. Every measured set is `frozenset()` (empty).

| Spec slug | Paradigm | Outcome shape | Noise-handling decision | Measured golden set |
|-----------|----------|---------------|-------------------------|---------------------|
| freq-proportion-checkout | frequentist | binary/proportion | minimal-reference (cwd-resolvable narrative+evidence+entrypoint; no profile/figure refs) | `frozenset()` |
| freq-proportion-email-open | frequentist | binary/proportion | minimal-reference (as above) | `frozenset()` |
| freq-continuous-aov | frequentist | continuous | minimal-reference (as above) | `frozenset()` |
| freq-continuous-timeontask | frequentist | continuous | minimal-reference (as above) | `frozenset()` |
| freq-count-referrals | frequentist | count/ratio | minimal-reference (ratio_of_means + delta_method; no cell-count test) | `frozenset()` |
| freq-count-installs | frequentist | count/ratio | minimal-reference (ratio_of_means + delta_method) | `frozenset()` |
| bayes-proportion-signup | bayesian | binary/proportion | minimal-reference (no analysis.test; random_seed declared) | `frozenset()` |
| bayes-proportion-adoption | bayesian | binary/proportion | minimal-reference (as above) | `frozenset()` |
| bayes-continuous-revenue | bayesian | continuous | minimal-reference (as above) | `frozenset()` |
| bayes-continuous-nps | bayesian | continuous | minimal-reference (as above) | `frozenset()` |
| bayes-count-tickets | bayesian | count/ratio | minimal-reference (ratio_of_means; no analysis.test) | `frozenset()` |
| bayes-count-sessions | bayesian | count/ratio | minimal-reference (ratio_of_means; no analysis.test) | `frozenset()` |

Coverage: paradigms {frequentist ×6, bayesian ×6}; outcome shapes {proportion ×4, continuous ×4,
count/ratio ×4}. Denominator = 12 (was 1).

## Notes on shape-specific clean-spec construction (for plan 12-05 / future authors)

- **Frequentist count/ratio**: the frequentist admissibility ontology (`references/families.yaml`)
  has no Poisson/count family, so a per-unit rate is modelled as a `ratio_of_means` estimand with
  `inference.primary_procedure: delta_method` (recognised family, dependence `none`). `analysis.test`
  is omitted so the frequentist cell-count test-selection contract (DSX-STA-041) does not apply.
- **Bayesian (all shapes)**: `analysis.test` is omitted (the frequentist test taxonomy does not
  apply; `inference.primary_procedure` names the posterior); `inference.paradigm_justification`
  uses a closed-vocabulary value (DSX-SPEC-085); `reproducibility.random_seed` is declared (a
  Bayesian posterior is a stochastic method, DSX-REP-001); `validity_frame.identification.constraint_source`
  is `none` so the design-identifies-vs-priors tension (DSX-VAL-041) does not fire; claim text uses
  "credible interval" without a leading "95%" token so the confidence-level figure is not read as an
  unmatched claim magnitude (DSX-CLM-033).
- **Continuous frequentist**: `welch_t` (`difference_in_means`); the experiment is powered on a
  responder proportion (`design.baseline_rate`, which the power check always models as a proportion),
  with the primary analysis outcome continuous.

## Verification (verbatim)

### Task 1 gate — `python -c "import glob,sys; n=len(glob.glob('examples/good-corpus/*-ANALYSIS-SPEC.yaml')); print(str(n)+' good-corpus specs discovered'); sys.exit(0 if n>=10 else 1)"`

```
12 good-corpus specs discovered
EXIT=0
```

### Per-spec `dsx validate` (no CRITICAL on own merits)

Every spec reports `spec: PASS (blocking at CRITICAL) — CRITICAL=0 HIGH=0 MEDIUM=0 LOW=0 INFO=0`.
Representative:

```
freq-proportion-checkout-ANALYSIS-SPEC.yaml: spec: PASS (blocking at CRITICAL) — CRITICAL=0 HIGH=0 MEDIUM=0 LOW=0 INFO=0
bayes-count-sessions-ANALYSIS-SPEC.yaml: spec: PASS (blocking at CRITICAL) — CRITICAL=0 HIGH=0 MEDIUM=0 LOW=0 INFO=0
```

(All 12 identical; measured across the full glob.)

### Task 2 gate — `python -m unittest tests.test_causal_verb_golden -v`

```
----------------------------------------------------------------------
Ran 6 tests in 2.362s

OK
```

Both lockstep tests pass: `test_golden_keys_match_the_examples_tree_on_disk` (green — every new
spec has a golden entry, every golden key names a real fixture) and
`test_every_fixture_ship_finding_set_equals_its_golden_baseline` (green — each measured set equals
its committed baseline).

## Boundary compliance

- **Touched only** `examples/good-corpus/` (new spec + narrative + entrypoint files) and
  `tests/test_causal_verb_golden.py` (12 golden entries). `git diff --stat` for the two commits
  lists exactly these paths (26 files, +2614).
- **No change to** `dsx/` (any file), `references/finding-codes.md`, `GATE_PROFILES`/`CHECKS`,
  `dsx/checks/`, or `scripts/gen-finding-catalogue.py`. Verified: `git status --short dsx/
  references/finding-codes.md scripts/gen-finding-catalogue.py` is empty. **Zero finding codes
  minted (D-18)**; the catalogue is unchanged at 256.
- **No shared tracking file edited**: `.planning/STATE.md`, `.planning/ROADMAP.md`,
  `.planning/LOOP-LEDGER.md`, `.planning/HUMAN-QUEUE.md` were not staged or modified by this plan.
  The normal execute-plan STATE/ROADMAP advance step was intentionally **skipped** — the
  orchestrator writes those serially after the wave merges.
- **Not pushed** — the orchestrator re-gates the whole wave and pushes.

## Deviations from Plan

- **Corpus size 12, not the ≥10 floor** — authored two extra specs (a fourth of each outcome
  shape) for margin and cleaner 6/6 paradigm balance. Within the plan's "exact size is a planning
  choice" discretion.
- **Route framed as "minimal-reference via cwd-resolvable committed artifacts," a refinement of
  the plan's two named routes.** The plan's minimal-reference route (reference no siblings) is not
  literally reachable because a clean shipped analysis must declare a resolvable claim, narrative,
  and entrypoint (DSX-CLM-001/NAR-001/CLM-031/REP-030). The route taken achieves the plan's
  intended outcome — every measured golden set `frozenset()`, no tempdir seeding needed by 12-05 —
  by committing per-spec narratives (doubling as evidence) and one shared entrypoint that resolve
  from `cwd`. Recorded above for plan 12-05.

## Self-Check: PASSED

- All 12 `examples/good-corpus/*-ANALYSIS-SPEC.yaml` and their `-NARRATIVE.md` siblings plus
  `_control_readout.py` exist on disk (glob count = 12).
- Both commits exist: `f5fdf1e` (data — specs) and `c8b0bff` (test — golden entries).
- `git diff --stat` for the two commits touches only `examples/good-corpus/` and
  `tests/test_causal_verb_golden.py`.
- Golden suite green; Task 1 glob gate exits 0 at n=12.
