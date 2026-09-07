---
phase: 27-evidence-case-feature-origin-only-leak
plan: 01
subsystem: dsx/checks/ml + finding-catalogue
tags: [mint, DSX-ML-034, feature-provenance, D-05, catalogue, tdd]
requires: [27-CONTEXT.md §S3-1-CLOSE (Kaufman confirmed), 27-MEASUREMENT.md (LIVE MISS)]
provides: [DSX-ML-034, _check_feature_provenance, catalogue@277]
affects: [dsx/checks/ml.py, references/finding-codes.md, gen-finding-catalogue.py]
tech-stack:
  added: []
  patterns: [declaration-only check, closed-vocabulary membership test, two-severity one-code dedupe]
key-files:
  created:
    - tests/test_ml_feature_provenance.py
  modified:
    - dsx/checks/ml.py
    - scripts/gen-finding-catalogue.py
    - references/finding-codes.md
    - tests/test_finding_catalogue_invariant.py
    - tests/test_phase20_zero_mint_close.py
    - tests/test_p19_categorical_rows.py
    - tests/test_gen_finding_catalogue.py
decisions:
  - "DSX-ML-034 emitted at two literal severities (CRITICAL after_prediction, HIGH unknown-no-waiver); source order arranged so the deduped catalogue row renders CRITICAL."
  - "Kaufman (2012) cited as secondary-corroborated, primary PDF paywalled — no first-hand read claim, no invented locator (§S3-1-CLOSE binding)."
metrics:
  duration: ~15m
  completed: 2026-09-07
  tasks: 3
  files: 7
status: complete
---

# Phase 27 Plan 01: Mint DSX-ML-034 (feature-provenance leak) Summary

Minted DSX-ML-034 — a declaration-only feature-provenance check in `dsx/checks/ml.py`
that reads an optional `model.feature_provenance[]` block and fires CRITICAL when a
feature is declared `available_at: after_prediction` and HIGH when `available_at: unknown`
without a waiver — then wired it into the finding catalogue (276 → 277). TDD: RED test
first, GREEN implementation, then deterministic catalogue regeneration and count-pin moves.

## What shipped

- **`_check_feature_provenance(model, report)`** in `dsx/checks/ml.py`, dispatched from
  `check()`'s model-present block alongside `_check_features`. Returns early when
  `model.get("feature_provenance")` is falsy (additive/optional — every existing spec still
  validates silently). `normalize()`s each entry's `available_at`; membership test on the
  closed vocabulary `before_prediction | at_prediction | after_prediction | unknown`.
  Attribution not detection — a spec that omits or lies in the block still passes.
- **Kaufman D-05 docstring:** `Citation:` line (Kaufman, Rosset, Perlich & Stitelman 2012,
  ACM TKDD 6(4) Article 15, DOI 10.1145/2382577.2382579) described as
  **secondary-corroborated, primary PDF paywalled** (no first-hand ACM read, no locator);
  `Structural criterion:` line describing the closed-vocabulary membership test and the
  attribution-not-detection limit.
- **`tests/test_ml_feature_provenance.py`** — six behaviour tests + the `# D-05: DSX-ML-034`
  marker carrying the honesty phrase.
- **Catalogue @ 277** — DSX-ML-034 added to `_D05_ALLOWLIST_CODES` (exact code), catalogue
  regenerated via `--write` (one CRITICAL row between DSX-ML-033 and DSX-ML-040), byte
  deterministic across regenerations.

## TDD gate compliance

- RED: `python -m unittest tests.test_ml_feature_provenance` exited **1** (3 presence
  assertions failed; absence assertions passed) — committed as `test(27-01): ...` (336560d).
- GREEN: same command exits **0** (6 tests OK) after the implementation — committed as
  `feat(27-01): implement ...` (3d63c09).
- No refactor commit needed.

## Verification (all green)

- `python -m unittest tests.test_ml_feature_provenance` → 6 tests OK.
- `python scripts/gen-finding-catalogue.py --check` → exit 0 ("finding catalogue is current"),
  D-05 gate passes (Citation + Structural criterion + `# D-05: DSX-ML-034` marker resolve).
- Rendered row: `| \`DSX-ML-034\` | CRITICAL | Feature '<…>' is declared available only after the prediction moment |`.
- Total line: `**Total: 277 codes.**`.
- Catalogue byte-deterministic (identical git hash-object across two `--write` runs).
- Full suite: `python -m unittest discover -s tests -q` → **1596 tests OK**.
- `git diff --stat -- dsx/checks/dq.py` → empty (byte-freeze held across all three commits).

## Count pins moved to 277

| Pin | File:line | In PLAN files_modified? |
|-----|-----------|--------------------------|
| catalogue Total | references/finding-codes.md:16 | yes (regenerated) |
| `_EXPECTED_TOTAL` (+ `_MINTED_CODES`, method name/docstring) | tests/test_finding_catalogue_invariant.py:40 | yes |
| phase-20 close assert | tests/test_phase20_zero_mint_close.py:100 | yes |
| Phase-19 categorical-rows live-total pin | tests/test_p19_categorical_rows.py:38 | **no — deviation (Rule 3)** |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Third live-total pin not named in the plan (test_p19_categorical_rows.py)**
- **Found during:** Task 3 (full-suite run).
- **Issue:** The plan's research (§E) enumerated only two count pins beyond the catalogue
  itself (`_EXPECTED_TOTAL`, the phase-20 assert). A third `_EXPECTED_TOTAL = 276` lives in
  `tests/test_p19_categorical_rows.py:38`, self-documented as "kept in lockstep with
  tests/test_finding_catalogue_invariant.py::_EXPECTED_TOTAL". It failed at 277 != 276.
- **Fix:** Moved it to 277 with the same lockstep-honesty comment/message update. This is the
  minimal correct change; the pin's own comment mandates lockstep.
- **Files modified:** tests/test_p19_categorical_rows.py
- **Commit:** df766dd

**2. [Rule 3 - Blocking] Two-severity code trips the divergent-declaration pin (test_gen_finding_catalogue.py)**
- **Found during:** Task 2 (full-suite run).
- **Issue:** DSX-ML-034 fires at two literal severities by design (§S3-1-CLOSE severity map).
  `test_divergent_code_set_is_exactly_the_pinned_five` pins the exact set of codes emitted
  with divergent (severity, title). The plan's RISK 3 anticipated the one-code/two-severity
  collision but its research stated "I found no test asserting zero generator warnings" — it
  missed this `_CANONICAL_DECLARATIONS` pin.
- **Fix:** Added DSX-ML-034's two pinned declarations to `_CANONICAL_DECLARATIONS` with a
  rationale comment — exactly the remedy the test instructs ("add it to
  _CANONICAL_DECLARATIONS deliberately"). Also added `DSX-ML-034` to `_MINTED_CODES` in
  test_finding_catalogue_invariant.py (required by the set-identity test; same file was
  already in files_modified).
- **Files modified:** tests/test_gen_finding_catalogue.py, tests/test_finding_catalogue_invariant.py
- **Commit:** df766dd

Both deviations are Rule 3 blocking fixes directly caused by this plan's mandated two-severity
design and the catalogue count move; neither touches case shape (D-27-01) or the pass/fail rule
(D-27-02) — guardrail 1 intact. No architectural (Rule 4) changes.

## Invariants held

- Only `dsx/checks/ml.py` edited under `dsx/`; `dsx/checks/dq.py` byte-frozen (empty diff).
- `.planning/REQUIREMENTS.md`, `STATE.md`, `ROADMAP.md` NOT touched (single-writer /
  orchestrator serial-write after wave merge).
- No branches created/switched; all three commits on `gsd/v2.6.0-exploration-depth`.
- No packages installed; `node install.mjs` NOT run (Wave 2's job).
- DSX-ML-034 added to `_D05_ALLOWLIST_CODES` as an exact code, never a `DSX-ML-` prefix.

## Not done (out of this plan's scope)

- Plan 27-02 fixture files (`examples/known-bad/feature-origin-only-leak-*`), the corpus
  harness maps, the ATTRIBUTION sidecar, the spec-count pin (42→43), and `node install.mjs`.
- STATE/ROADMAP/REQUIREMENTS updates (orchestrator-owned).

## Self-Check: PASSED
- FOUND: tests/test_ml_feature_provenance.py
- FOUND: dsx/checks/ml.py::_check_feature_provenance
- FOUND: references/finding-codes.md DSX-ML-034 row (CRITICAL) + Total 277
- FOUND commit 336560d (RED), 3d63c09 (GREEN), df766dd (catalogue)
