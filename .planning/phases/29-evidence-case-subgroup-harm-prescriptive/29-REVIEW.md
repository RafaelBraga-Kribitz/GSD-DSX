---
phase: 29-evidence-case-subgroup-harm-prescriptive
reviewed: 2026-09-08T00:00:00Z
depth: deep
files_reviewed: 17
files_reviewed_list:
  - dsx/checks/coherence.py
  - examples/known-bad/subgroup-harm-without-disposition-ANALYSIS-SPEC.yaml
  - examples/known-bad/subgroup-harm-without-disposition-entrypoint.py
  - examples/known-bad/subgroup-harm-without-disposition-POSTMORTEM.md
  - examples/known-bad/subgroup-harm-without-disposition-ATTRIBUTION.yaml
  - references/finding-codes.md
  - scripts/gen-finding-catalogue.py
  - templates/ANALYSIS-SPEC.yaml
  - tests/test_subgroup_harm_disposition.py
  - tests/test_known_bad_corpus.py
  - tests/test_frame_val.py
  - tests/test_causal_verb_golden.py
  - tests/test_dsx.py
  - tests/test_finding_catalogue_invariant.py
  - tests/test_gen_finding_catalogue.py
  - tests/test_p19_categorical_rows.py
  - tests/test_phase20_zero_mint_close.py
findings:
  blocker: 0
  high: 1
  medium: 2
  low: 1
  total: 4
status: issues_found
---

# Phase 29: Code Review Report

**Reviewed:** 2026-09-08
**Depth:** deep (cross-file: check ↔ schema ↔ catalogue ↔ corpus harness; live-run confirmation)
**Files Reviewed:** 17
**Status:** issues_found

## Summary

Phase 29 mints `DSX-COH-041` (`_check_subgroup_harm_disposition`) and promotes the corpus's
first `kind: target` fixture. The wiring is sound: I ran the touched suites live on CPython
3.12.10 — `test_subgroup_harm_disposition`, `test_known_bad_corpus`, `test_frame_val`,
`test_causal_verb_golden`, `test_dsx`, and the three catalogue-pin tests all pass (774 tests),
and `gen-finding-catalogue.py --check` exits 0. Five of the six load-bearing invariants hold
outright.

The defects are all in the **check's enforcement surface** (invariant 6). The sign+floor
trigger core is correct, but the *disposition-validation* and the *segment-count guard* are
weaker than the frozen design claims, and I confirmed three silent evasions **by live probe**
that are NOT covered by the docstring's stated bounded-catch boundary:

1. A `subgroup_harm[]` row that names the segment but carries a **missing or invalid
   disposition** silences the CRITICAL entirely — the gate's core "force disclosure" guarantee
   is defeated by a content-free declaration (HIGH). This directly contradicts D-29-03's own
   recommendation ("no valid disposition = silence → CRITICAL").
2. The borrowed `len(segments) < 2` guard silences a **lone declared opposing segment** — a
   guard whose Simpson's-paradox justification does not transfer to this check's semantics
   (MEDIUM).
3. Omitting a harmed segment's **`n`** escapes even the strictest default floor of 0,
   contradicting D-29-01's "no escape by omission / un-gameable" claim (MEDIUM).

## Invariant verdicts

| # | Invariant | Verdict |
|---|-----------|---------|
| 1 | D-05 citation honesty (Gail & Simon = motivating definition only; Obermeyer abstract+metadata) | **HOLDS** |
| 2 | Catalogue integrity (one row, four pins at 279, exact-code allowlist, out of backlog, both severities fire) | **HOLDS** |
| 3 | `dq.py` + `cli.py` byte-frozen | **HOLDS** (empty diff) |
| 4 | TARGET polarity (`_TARGET_DEFECT_CODES` plan/verify/ship, `_EXPECTED_CAUGHT_DEFECTS` empty, golden present) | **HOLDS** |
| 5 | `kind: target` vocab complete (incl. the stale `# kind == "caught"` comment — **it was fixed**) | **HOLDS** |
| 6 | `_check_subgroup_harm_disposition` correctness | **DOES NOT FULLY HOLD** — trigger core correct; disposition-validation + `len<2` guard + `n`-omission gaps below |

Invariant detail:
- **1 HOLDS.** Docstring (`coherence.py:224-250`), test marker (`test_subgroup_harm_disposition.py:10-20`),
  POSTMORTEM, ATTRIBUTION rationale, and the spec header all frame Gail & Simon as the motivating
  definition ONLY, with an explicit "runs NO such test / computes NO statistic (D-02) / not the
  enforcement mechanic" disclaimer. Obermeyer is cited at abstract+metadata grade with "paper body
  was not read." No over-claim found.
- **2 HOLDS.** The single rendered row (`references/finding-codes.md:357`) is `HIGH` via last-seen
  dedup (same pattern as DSX-COH-030 — see LW-01). Both severities fire live (unit tests
  `test_missing_row_critical` CRITICAL / `test_accept_blank_rationale_high` HIGH, both pass). Four
  pins = 279 (catalogue Total, `test_finding_catalogue_invariant._EXPECTED_TOTAL`,
  `test_phase20_zero_mint_close`, `test_p19_categorical_rows`). Exact code in `_D05_ALLOWLIST_CODES`
  (not a prefix); absent from `_SECTION_65_BACKLOG_CODES`; `--check` deterministic.
- **3 HOLDS.** `git diff 4945a62..HEAD -- dsx/checks/dq.py dsx/cli.py` is empty.
- **4 HOLDS.** `_TARGET_DEFECT_CODES["subgroup-harm-without-disposition"]` = plan/verify/ship only
  (execute correctly absent); `_EXPECTED_CAUGHT_DEFECTS[slug]` = `frozenset()`;
  `_GOLDEN_SHIP_FINDINGS[...]` = `frozenset({DSX-COH-041})`. `test_known_bad_corpus` (the
  critical-threshold test) passes — execute is not demanded.
- **5 HOLDS.** Closed vocab extended to `("miss", "caught", "target")`; falsifiability non-miss
  branch routes `target` through `assertIn`. The carried-forward nit was **fixed**:
  `test_known_bad_corpus.py` now reads `else:  # kind == "caught" or "target" (Phase 29 D-29-00): must fire`.

## High

### HG-01: Missing/invalid disposition in a `subgroup_harm[]` row silences the CRITICAL gate

**File:** `dsx/checks/coherence.py:283-323` (the row-present branch)
**Issue:** The CRITICAL fires only when `row is None` (no matching segment name). Once a row
exists for the segment, the *only* remaining emit is the HIGH branch, which requires
`disposition == "accept"` AND a blank rationale. A row with **no `disposition` key**, or an
**unrecognized disposition** (`proceed`, `noted`, a typo of `accept`), falls through both
branches and the check goes silent. The disposition vocabulary `{accept|exclude|mitigate}` is
never validated. Confirmed live:

```
row {'segment':'D'}                    -> []          (should be CRITICAL)
row {'segment':'D','disposition':'proceed'} -> []     (should be CRITICAL)
control (no row)                        -> ['CRITICAL']
```

An analyst can clear the CRITICAL on a genuinely harmed, above-floor minority segment by adding
one content-free line `- segment: D`. The gate's stated purpose ("force an undispositioned
minority harm to disclosure", template `ANALYSIS-SPEC.yaml:59-64`; REQ-P29-03 "forced to
disclosure") is defeated with zero disclosure. This is **not** one of the three evasions the
docstring's bounded-catch paragraph admits (omit the segment / lie about sign / game the floor)
— all of those hide or visibly raise something auditable; this one satisfies the obligation with
nothing. It also directly contradicts the frozen design D-29-03: "an unknown `disposition` value
or a row missing a required key → **CRITICAL** (no valid disposition = silence)".

**Fix:** Treat a matching row with a missing/unknown disposition as an unmet obligation. In the
`else` limb, before the `accept`-blank check, validate the disposition against the closed set and
emit CRITICAL otherwise:
```python
disposition = normalize(str(row.get("disposition", "")))
if disposition not in ("accept", "exclude", "mitigate"):
    report.add("DSX-COH-041", "CRITICAL",
               f"decision.subgroup_harm[] row for {name!r} has no valid disposition",
               ...)
elif disposition == "accept" and is_blank(row.get("rationale")):
    report.add("DSX-COH-041", "HIGH", ...)
```
If leaving this out is intentional (the frozen plan scoped only two severities), the bounded-catch
docstring MUST be widened to name "a matching row with a missing/invalid disposition passes" so the
honesty boundary is not silently overstated.

## Medium

### MD-01: `len(segments) < 2` guard silences a lone declared opposing segment

**File:** `dsx/checks/coherence.py:258`
**Issue:** The early return `if overall is None or len(segments) < 2: return` is copied from
`_check_simpsons_paradox` (`metrics.py:300`), where ≥2 segments are needed to *compare segments
against each other* for a reversal. This check does not compare segments to each other — it
compares each segment's sign against the declared `overall_effect`. So its semantics need only
1 segment. A prescriptive spec that declares `overall_effect` positive and a **single** opposing
segment above the floor is exactly the harm this check targets, yet it is silent. Confirmed live:
```
segments=[{'name':'D','effect':-0.06,'n':1000}], floor=500 -> []   (should be CRITICAL)
```
Evasion: drop the aligned segments A/B/C and declare only the harmed one. The guard's rationale
does not hold for this check.
**Fix:** Change the guard to `if overall is None or not segments: return` (require only a
non-empty segment list). The empty-results / non-prescriptive early returns are unaffected.

### MD-02: Omitting a harmed segment's `n` escapes even the strict default floor of 0

**File:** `dsx/checks/coherence.py:277-280`
**Issue:** `above_floor = n is not None and n >= floor`; when `n` is absent, `above_floor` is
False, and with no `ci` on today's schema the segment is skipped. D-29-01 makes the default floor
0 precisely so that "omitting the floor makes the check maximally strict ... No escape by
omission." But a declared opposing segment that simply omits `n` escapes at any floor, including
the strict default. Confirmed live:
```
segments=[A +0.05, {'name':'D','effect':-0.06}], floor absent(=0) -> []   (should be CRITICAL)
```
This undercuts the load-bearing "un-gameable default" claim (D-29-01) and is not listed in the
docstring's bounded-catch evasions.
**Fix:** Decide the intended semantics and encode it. Strictest reading of D-29-01 (default floor
0, no escape by omission): treat a missing `n` as `n = 0` for a declared opposing segment, so
`n >= floor` is True at the default floor — `n = 0.0 if n is None else n`. If a missing `n` is
meant to be un-actionable, say so in the bounded-catch docstring.

## Low

### LW-01: Catalogue row labels DSX-COH-041 `HIGH` though it fires (and blocks) at CRITICAL

**File:** `references/finding-codes.md:357`
**Issue:** The generated row reads `| DSX-COH-041 | HIGH | ...`, because the AST extractor keeps
the last-seen `report.add` (HIGH) for a two-severity code. But DSX-COH-041 fires CRITICAL on the
missing-row path and therefore blocks at `plan`/`execute` (CRITICAL threshold). A reader
consulting the human catalogue would conclude it only blocks at verify/ship. This is the
established DSX-COH-030 convention (and `test_gen_finding_catalogue.py` pins both declarations),
so it is not a regression — but for a code whose *higher* severity is the load-bearing one it is
a genuine legibility trap.
**Fix:** Consider having the catalogue render the max severity for multi-severity codes, or append
a `(also CRITICAL)` note. If the convention is deliberately last-seen, no code change is needed;
flagged for awareness.

---

## Notes on things checked and found clean

- **No vacuous tests.** All seven methods in `test_subgroup_harm_disposition.py` assert both count
  (`len(hits) == 1` / `== []`) and severity; `test_floor_boundary` exercises both below-floor
  (silent) and at-floor (`n == floor` fires); `test_sign_gate` proves same-sign silence.
- **Sign convention** is reused verbatim (`_sign(v) = (v>0)-(v<0)`) and the trigger is sign+n, NOT
  CI-based — the CI OR-arm is correctly latent (segments schema has no `ci`), avoiding the
  circularity the CONTEXT warned about.
- **Fixture arithmetic** verified: n-weighted overall = 320/10000 = +0.032; segment D (−0.06,
  n=1000) opposes above the 500 floor with no disposition row = the sole defect.
- **`_ci_excludes_zero`** logic (both bounds same non-zero sign) is correct for its latent purpose.

---

_Reviewed: 2026-09-08_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep_

---

## Orchestrator disposition (S5-4, 2026-09-08)

The orchestrator independently re-verified all four findings against the committed
code and the FROZEN design (`29-CONTEXT.md`, repo is the fact — the reviewer's claims
were not trusted) before acting.

- **HG-01 (HIGH) — FIXED.** Confirmed at `coherence.py:283-322`: once a row named the
  segment, the only remaining emit required `disposition == "accept"` + blank rationale,
  so a content-free `- segment: D` (no/invalid disposition) fell through both branches
  and silenced the CRITICAL. The plan (S5-2, `29-01-PLAN.md:26,133`) enumerated only the
  two REQ-P29-03 severities and **under-specified** — it neither carried nor explicitly
  rejected the discuss round's own D-29-03 recommendation ("an unknown `disposition`
  value or a row missing a required key → CRITICAL"). A minted check silenceable by one
  content-free line is indefensible to the sceptical-statistician bar. Fixed by validating
  the disposition against the closed vocabulary `{accept, exclude, mitigate}`; an invalid
  or missing disposition on a matching row now fires CRITICAL. This **implements D-29-03's
  own recommendation**, is a strict tightening (catches more gaming, never reshapes the
  fixture — D-13-safe), and leaves the shipped TARGET fixture unchanged (it declares no
  `subgroup_harm` row → still the `row is None` CRITICAL). Same class as the Phase-27
  WR-01 fix (broaden a minted check's over-permissive branch at code-review, applied solo
  with a loud recorded rationale). Still ONE code / TWO severities per REQ-P29-03
  (CRITICAL for missing-or-invalid, HIGH for accept-blank), per-segment mutually exclusive.
  Locked by `test_matching_row_missing_disposition_critical`,
  `test_matching_row_invalid_disposition_critical`, `test_valid_exclude_disposition_silent`;
  the `_CANONICAL_DECLARATIONS` pin gained the third declaration deliberately (comment
  records why).
- **MD-01 (MEDIUM) — FIXED.** The borrowed `len(segments) < 2` guard (`coherence.py:258`)
  contradicts the SETTLED D-29-01 per-segment semantics (each declared opposing segment is
  judged against `overall_effect` alone — the ≥2-to-compare rationale of
  `_check_simpsons_paradox` does not transfer). Changed to `not segments`. Locked by
  `test_lone_opposing_segment_critical`.
- **MD-02 (MEDIUM) — FIXED.** A declared opposing segment omitting `n` escaped even the
  strict default floor 0 (`coherence.py:277-280`), contradicting the SETTLED D-29-01 "no
  escape by omission / maximally strict". A missing `n` now reads as 0. Locked by
  `test_opposing_segment_missing_n_fires_at_default_floor` (fires at default floor 0;
  still ruled out by an affirmatively-declared floor above 0 — the floor mechanism intact).
- **LW-01 (LOW) — ACCEPTED (residual).** The catalogue renders DSX-COH-041 as `HIGH` via
  the last-seen-dedup convention, though its load-bearing severity is CRITICAL. This is the
  established repo-wide DSX-COH-030 convention (pinned in `test_gen_finding_catalogue.py`);
  changing it is a cross-cutting generator behavior change touching every two-severity code
  and risks the catalogue byte-determinism invariant — out of Phase-29 scope. Recorded as a
  known legibility residual, consistent with prior-phase accepted residuals.

MD-01/MD-02 were unambiguous bug-fixes (code diverged from the FROZEN D-29-01 contract);
the rigour>reliability tiebreak on HG-01 was unambiguous (Phase-27 WR-01 precedent) → no
persona fork. **All gates re-run by the orchestrator on real Python 3.12.10 (subagent NOT
trusted):** full suite **1627 OK** (1622+5); `gen-finding-catalogue.py --check` EXIT 0,
catalogue Total **279** (behavior-only change, mints nothing); DSX-COH-041 row unchanged
(`finding-codes.md` byte-identical to HEAD); `dq.py`+`cli.py` byte-frozen (empty diff);
S5-4 change scope = `dsx/checks/coherence.py` + `tests/test_subgroup_harm_disposition.py`
+ `tests/test_gen_finding_catalogue.py` (pin) ONLY; `node install.mjs --check` self-test
passed (6/6 agents, 14/14 skills, 5 gates). The TARGET fixture still fires DSX-COH-041 at
plan/verify/ship (`test_known_bad_corpus` green in-suite) — polarity and golden set intact.
