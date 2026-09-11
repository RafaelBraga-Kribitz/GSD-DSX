---
phase: 30
plan: 30-02
type: execute
status: complete
executed: 2026-09-10
executor: orchestrator-direct (opus/high) — measurement-transcription + audit battery, no design decision (S6-3 Wave-1 routing precedent)
requirements-completed: [REQ-P30-01, REQ-P30-02, REQ-P30-03]
---

# Plan 30-02 — Doc re-baseline + REQ-P30-02 audit battery + zero-mint — SUMMARY

S6-3 Wave 2. Refreshed the two stale calibration records to the Phase-30 measured
re-baseline (numbers transcribed from `30-READOUT.md`, plan 30-01 — none estimated),
closed the one genuine REQ-P30-02 gap with a single lightweight agreement test, and ran
the full milestone-audit verification battery on the final tree. **Zero codes minted.**

## Task 1 — brief.md §6.5 refreshed to the Phase-30 re-baseline

- **Item-7/8/9 entry rows (`brief.md:376-378`) VERIFIED, not rewritten** — already
  consistent with the re-baseline: item 7 = `DSX-ML-034` miss on `feature-origin-only-leak`;
  item 8 = `DSX-CLM-034` miss on `magnitude-without-computed-effect`; item 9 = `DSX-COH-041`
  PRESENT/DETECTED catch on `subgroup-harm-without-disposition`. Left byte-identical.
- **Added a dated `### Phase 30 re-evaluation of the gated backlog (terminal re-baseline,
  2026-09-10)` section** immediately after the Phase-12 (2026-08-27) section, which is
  preserved verbatim as history. The new backdrop reads the measured numbers: the pair
  **(miss-rate 1.0, FPR 0.0)** (D-10, never catch-rate alone); FPR **0/15** over the
  fifteen-spec good-control corpus as a bounded observation (one-sided 95% upper bound
  ≈ 0.181, not a point estimate — D-04); a **five-case** ABSENT/miss partition (floor 3,
  met at 5 ≥ 3); per F3 the 5/5 miss-rate framed as a construction invariant (no CI); names
  the two new misses `DSX-ML-034` + `DSX-CLM-034` and the one new target `DSX-COH-041`.
- Stale Phase-12 calibration tokens (`twelve-spec`, `0/12`, `3/3 miss`) remain ONLY inside
  the dated 2026-08-27 block; the current-state backdrop is the new dated Phase-30 note.
- Task-1 automated verify: **PASS**.

## Task 2 — docs/literature/the-ai-data-scientist.md updated

- Applied via a byte-precise CRLF-preserving script (file is CRLF; each replacement
  asserted to occur exactly once — no partial edit on mismatch; the one-shot helper was
  removed after use).
- **Mapping-table row 15**: `39 known-bad specs` → **`42 known-bad specs`**, `15
  good-control specs` unchanged, dated to the Phase-30 re-baseline.
- **Mapping-table status cells flipped**: row 7 provenance `deferred` → satisfied
  (attributed miss via `DSX-ML-034`); row 10 magnitude residual `deferred` → satisfied
  (`DSX-CLM-034`); row 12 subgroup gate `deferred` → present (catch via `DSX-COH-041`).
- **"What is deferred" section**: retitled to **"What was deferred, and how it was
  promoted (D-13)"** (a stale "deferred" header over satisfied content would mislead a
  sceptical reader — an honesty consistency edit, in the spirit of Task 2); the "none is
  met" line updated to "all three met at the Phase-30 re-baseline"; the three-row deferred
  table rewritten to a **Satisfied** disposition, one line each, code + fixture + measured
  evidence named. The SECOND `39 known-bad specs` occurrence (item-7 cell, W1 from the
  plan-checker) is cleared — **no `39 known-bad specs` string survives anywhere**.
- Task-2 automated verify: **PASS** (`42 known-bad specs` present; DSX-ML-034/CLM-034/COH-041
  present; `39 known-bad specs` gone).

## Task 3 — REQ-P30-02 gap closed with ONE agreement test

- `tests/test_literature_corpus_count_agreement.py` (new, the only new file this phase):
  a `unittest.TestCase` resolving ROOT from the test-file location, reading the literature
  doc as UTF-8, extracting the row-15 known-bad and good-control count integers with
  CRLF-tolerant regexes, and asserting each **equals** the live
  `examples/{known-bad,good-corpus}/*-ANALYSIS-SPEC.yaml` glob count.
- Asserts **doc == live agreement, never a hardcoded number** (cannot under-pin to a stale
  literal, cannot over-fire on formatting); an anti-false-pass `assert m is not None` fails
  loudly if the row-15 phrasing is renamed/absent. Pins nothing beyond row-15 (GA-4 "close
  exactly this gap and no more"). Mints no code; off the gate path.
- Verify: **2 tests OK** on real 3.12.10.

## Task 4 — REQ-P30-02 audit battery + REQ-P30-03 zero-mint (final tree, real 3.12.10)

All green, in order (stray root `DECISIONS.jsonl` cleaned first):
1. **Catalogue set-identity 279 → 279** — `gen-finding-catalogue.py --check` EXIT 0
   ("finding catalogue is current"); **live count re-measured 279** (`finding-codes.md:16`
   "Total: 279 codes." + 279 rows), all three v2.6 codes present. The "declared twice"
   warnings are the by-design two-severity dedup (DSX-COH-041/ML-034/CLM-034 etc.),
   non-failing. **Zero mint (REQ-P30-03).**
2. **Frozen count-pins / snapshots green** — `test_finding_catalogue_invariant`,
   `test_phase20_zero_mint_close`, `test_p19_categorical_rows`, example-profile digests.
3. **Doc/code agreement green** — `test_doc_code_agreement`, `test_selection_heuristic_docs`,
   and the new `test_literature_corpus_count_agreement` (30 tests OK combined).
4. **`node install.mjs --check` passed** — 6/6 agents, 14/14 skills, 5 gates, self-test
   passed (read-only; installer trees untouched — brief.md/docs/ are not under skills/,
   agents/, templates/, references/).
5. **`scripts/check.sh` green** — "all checks passed" (catalogue current, manifest valid,
   gate contract, determinism).
6. **Full unittest suite 1629 OK** (67.7s) on the real interpreter, no skips; the plotstyle
   determinism test RAN (0.729s, not skipped under the python3 stub).

## Frozen surfaces + tracking (clean)

- `git status --porcelain dsx/ examples/ references/finding-codes.md` **EMPTY** — no
  frozen-surface diff. `git status` shows only `brief.md`, `docs/literature/the-ai-data-scientist.md`
  (tracked, modified) and the new test file (untracked), plus operator-local untracked.
- **No REQUIREMENTS.md / STATE.md / ROADMAP.md edit by this plan** (single-writer honored).
- No installer re-generation run (INSTALLER SCOPE: `--check` read-only only).

## Not done here (deferred to S6-4, per GA-1)

The readout's **§6 adversarial `dsx-statistician` review remains a marked PLACEHOLDER**.
Per GA-1 (`30-CONTEXT.md §1`, the 12-READOUT precedent) it lands at S6-3/S6-4 against the
measured numbers; plan 30-02 (S6-3's gated plan) does not schedule it. It is carried into
S6-4 (code review + verification) as that unit's load-bearing sub-task — a heavy
opus/high (or fable) spawn, not started here to respect the pacing cap. Per the precedent
the review sharpens framing/honesty and changes no measured number.
