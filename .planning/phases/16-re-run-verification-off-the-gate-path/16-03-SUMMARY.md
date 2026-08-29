---
phase: 16-re-run-verification-off-the-gate-path
plan: 03
status: complete
requirements: [REQ-P16-03]
---

# 16-03 SUMMARY — protocol_adherence sidecars + additive accepted-but-ignored corpus test

## What shipped
- **Three `examples/known-bad/*-ATTRIBUTION.yaml` sidecars** — added a top-level
  `protocol_adherence: skipped` key (vocabulary `adhered | skipped | not_applicable`) with a
  one-line comment, and extended each file's schema comment to name `protocol_adherence?` as an
  optional additive Phase-16 field reported BESIDE catch rate / FPR, never inside them (D-10).
  `absent_code`/`promotes_backlog_item`/`kind`/`rationale` byte-unchanged; NO ANALYSIS-SPEC edited.
- **`tests/test_known_bad_corpus.py`** — added ONE test to `TestKnownBadCorpus`,
  `test_protocol_adherence_is_additive_and_ignored`: every sidecar's value is in the closed
  vocabulary; `"protocol_adherence" not in _headline.__code__.co_varnames` (accepted-but-ignored,
  like `present`); `_headline((2,5),(1,4),(3,10)) == (0.25,0.3)`; skipped count ≥ 1. The two
  standalone headline anchor tests (`TestStratifiedHeadlineHelpers`) and `_headline` are unedited.

## Gate evidence (all re-run by the orchestrator, brief §5)
- Task 1: 3 sidecars load via `dsx.loader.load`, all `protocol_adherence == "skipped"`, `absent_code` intact; `git status --porcelain examples/known-bad/*ANALYSIS-SPEC.yaml` empty.
- Task 2: `python -m unittest tests.test_known_bad_corpus` → **Ran 45 tests OK** (full live-gate corpus suite green — calibration and per-fixture gate findings unchanged at the 258 catalogue); new method present, both headline anchors present.
- Zero finding codes minted; catalogue stays 258.
