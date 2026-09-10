---
phase: 30-calibration-rebaseline
artifact: code-review
reviewed: 2026-09-10
depth: deep
reviewer: gsd-code-reviewer (adversarial)
scope: git diff 03de340^..0c924bb (4 tracked artifacts)
files_reviewed_list:
  - brief.md
  - docs/literature/the-ai-data-scientist.md
  - tests/test_literature_corpus_count_agreement.py
  - .planning/phases/30-calibration-rebaseline/_measure_readout.py
findings:
  blocker: 0
  high: 0
  medium: 0
  low: 2
  total: 2
status: clean
verdict: SHIP
---

# Phase 30 — Calibration re-baseline (terminal) — code review

**Verdict: SHIP.** Zero BLOCKER, zero HIGH, zero MEDIUM, 2 LOW (both latent, invariants
hold today). All four load-bearing invariants VERIFIED against live measurement, not
assumed. This is a genuinely zero-mint documentation + off-gate-path measurement phase;
no frozen surface moved and every doc number reproduces live.

## The four load-bearing invariants

### 1. Doc claims match measured reality — **HOLDS**

Ran the companion on the real interpreter and cross-checked every claim in `brief.md`
and `docs/literature/the-ai-data-scientist.md` against the live measurement and
`30-READOUT.md`. Every number and every miss/catch polarity matches:

| Claim | Doc | Live-measured | Match |
|---|---|---|---|
| Headline (miss-rate, FPR) | 1.0, 0.0 | 1.0, 0.0 | ✓ |
| ABSENT partition | 5/5, floor 3 | 5/5, floor 3 | ✓ |
| FPR denominator | 0/15 | 0/15 | ✓ |
| CB upper bound | ≈0.181 | Clopper-Pearson 1−0.05^(1/15) | ✓ |
| row-15 known-bad count | 42 | 42 (`examples/known-bad/*-ANALYSIS-SPEC.yaml`) | ✓ |
| row-15 good-control count | 15 | 15 (`examples/good-corpus/*-ANALYSIS-SPEC.yaml`) | ✓ |
| item 7 `feature-origin-only-leak` | attributed MISS, `DSX-ML-034` silent | miss, DSX-ML-034, missed_critical=True, fires_at_any=False | ✓ |
| item 8 `magnitude-without-computed-effect` | attributed MISS, `DSX-CLM-034` silent | miss, DSX-CLM-034, missed_critical=True, fires_at_any=False | ✓ |
| item 9 `subgroup-harm-without-disposition` | CATCH, `DSX-COH-041` CRITICAL plan/verify/ship | target, DSX-COH-041 plan=CRIT verify=CRIT ship=CRIT execute=[] | ✓ |

- **Polarity is honest.** Literature rows 7 (`docs/literature/the-ai-data-scientist.md:35`)
  and 10 (`:38`) call item 7/8 an "attributed miss" — never a "catch"; row 12 (`:40`) calls
  item 9 a "catch". The D-13 disposition table (`:81-85`) qualifies items 7/8 explicitly as
  "buys attribution, not a catch" and item 9 as "a real closed catch (PRESENT/DETECTED)".
  No attribution-only miss is dressed as detection, and vice-versa.
- **No stale token survives where it changes meaning.** Grepped the literature doc:
  `39 known-bad`, `As of 2026-09-06`, and any `**deferred**` status cell are all GONE. The
  only surviving "deferred" is the past-tense heading "What was deferred, and how it was
  promoted" (`:74`) — a correct historical framing, not a false present-tense claim.
- `brief.md:447-471` (the new §6.5 re-evaluation block) matches the readout: pair headline,
  0/15 with ≈0.181 bound, five-case floored-at-3 ABSENT partition, two new misses named with
  their attributing codes, one new target firing CRITICAL plan/verify/ship. No overstatement.

### 2. The new test cannot false-pass and cannot over-fire — **HOLDS**

`tests/test_literature_corpus_count_agreement.py`:
- **Asserts DOC == LIVE, never a hardcoded literal.** `assertEqual(doc_n, live_n)` where
  `live_n` is a live glob (`:35-36`). It cannot under-pin to a stale number (that is the
  exact drift it exists to catch — 39-vs-42) and cannot over-fire on formatting.
- **Fails loudly if row-15 renamed.** `assert m is not None` (`:31`) — a missing/renamed
  phrase is a loud failure, not silent agreement.
- **Regex binds the intended line uniquely.** Grep confirms exactly ONE line in the doc
  carries both `\d+ known-bad specs` and `\d+ good-control specs` (line 43), so
  `.search()` (first match) binds row-15 unambiguously. `_KNOWN_BAD_RE` captures 42,
  `_GOOD_CONTROL_RE` captures 15.
- **CRLF-tolerant.** Both phrases are intra-line and `\s+` never needs to span a line
  boundary; `read_text` universal-newline mode also normalises `\r\n`. Line endings never
  reach the match — docstring claim (`:21-22`) is accurate.
- **Correct dirs/suffix.** Globs `examples/known-bad/` and `examples/good-corpus/` for
  `*-ANALYSIS-SPEC.yaml` (`:36,47,57`) — byte-identical to the live harness's
  `CORPUS_DIR` (`test_known_bad_corpus.py:34`), `GOOD_CORPUS_DIR` (`:1001`), and
  `SPEC_SUFFIX` (`:35`).
- **Runs green live:** `python312 -m unittest tests.test_literature_corpus_count_agreement`
  → 2 OK (0.002s).

### 3. The companion resolves ROOT and does not corrupt partitions — **HOLDS**

`.planning/phases/30-calibration-rebaseline/_measure_readout.py`:
- **ROOT correct.** `parents[3]` from `.planning/phases/30-calibration-rebaseline/` = repo
  root; the self-asserting guard (`:25-27`) checks `tests/test_known_bad_corpus.py` exists,
  and the file ran successfully and reproduced every readout number — the guard is correct,
  not merely present.
- **`out["target"]` block is read-only and partition-safe.** It is a separate loop (`:135-154`)
  running AFTER `out["present"]` (`:66`) is finalised. It filters `kind != "target"`
  (`:138`), reads only `severity_by_point`, and never touches `pd`/`pc` (PRESENT) or
  `am`/`ad` (ABSENT). The ABSENT loop (`:71-100`) filters `kind != "miss"`, so the one
  `kind: target` sidecar is excluded from ABSENT (denom stays 5, not 6) — confirming the
  target axis does not inflate the miss partition.
- **No transcription bug vs the live harness.** The `fpr`/`present`/`absent`/`friction`
  loops use the same `_gate_findings`, `_false_positive_findings`, `_classify_target_defect`,
  `_headline`, `_friction`, `_non_target_in_profile_cells` functions the reproducer uses,
  and the companion's output (headline 1.0/0.0; present 10/10; absent 5/5; fpr 0/15;
  friction raw 101 / net 69 / cells 74 / 1.36 / 0.93) is byte-identical to the READOUT and
  consistent with the independent reproducer `test_stratified_catch_rate_and_fpr_report`
  (passes live, 8.2s). A transcription error would have to coincidentally reproduce a
  passing independent gate — ruled out.

### 4. No frozen surface was touched — **HOLDS**

`git diff 03de340^..0c924bb -- dsx/ examples/ references/finding-codes.md` is EMPTY.
Set-identity 279→279 preserved. Zero mint confirmed.

---

## Narrative findings (AI reviewer)

### LOW-01: `.search()` first-match binding is latently fragile (invariant holds today)

**File:** `tests/test_literature_corpus_count_agreement.py:23-24,28`
**Issue:** `_KNOWN_BAD_RE`/`_GOOD_CONTROL_RE` use `re.search` (first match). Safe today
because exactly one `\d+ known-bad specs` and one `\d+ good-control specs` phrase exist in
the doc (verified: 1 matching line). If a future edit introduces a second such phrase
EARLIER in the doc, the test would silently bind the wrong line and could pass on stale
row-15 counts. This is exactly the GA-4 "close this gap and no more" scope, so the risk is
acknowledged and accepted; no action required this phase.
**Failure scenario:** future doc adds "we grew from 39 known-bad specs to …" prose above
row 15 → test binds 39, passes against a stale row 15.
**Fix (optional, deferrable):** none needed now; if hardened later, `findall` + assert
len==1 before comparing.

### LOW-02: "satisfied" in mapping rows 7/10 is qualified, not overstated (HOLDS)

**File:** `docs/literature/the-ai-data-scientist.md:35,38`
**Issue:** Rows 7/10 say the backlog item is "now **satisfied**", which in isolation could
read as "dsx now catches this." It does not overstate because each cell immediately adds
"attributed miss via `DSX-ML-034`/`DSX-CLM-034`" and the D-13 disposition table (`:81-83`)
states "buys attribution, not a catch." "Satisfied" refers to the backlog ENTRY CONDITION
(a measured corpus case exists), not to a detection capability. No overstatement survives a
careful read; recorded for transparency only.
**Fix:** none required.

---

_Reviewed: 2026-09-10_
_Reviewer: Claude (gsd-code-reviewer), adversarial stance_
_Depth: deep (cross-file: doc ↔ live measurement ↔ harness ↔ reproducer)_
