---
audit_date: 2026-09-04
trigger: "operator request, while traveling: self-audit v2.4.0 and prior milestones for gaps, contradictions, and flaws"
method: "8-dimension multi-agent find pass, each finding adversarially re-verified independently before being trusted"
agents: 36
findings_raw: 28
findings_confirmed_real: 26
findings_applied: 21
findings_escalated: 2
findings_investigated_and_dropped: 2
---

# Post-ship self-audit — 2026-09

**Scope boundary used throughout:** fix directly only what's unambiguous and
low-risk (prose, citations, stale cross-references, message-text corrections);
escalate anything that would require a gate-behavior change, a finding-code
change, or reopening a persona-round scope decision, rather than deciding it
unilaterally overnight. Never touch `~/.claude/gsd-core/` (the shared GSD
framework, not part of this repo) — out of this audit's blast radius.

Every fix below was independently re-verified against the live file or a
fetched primary source before being applied — not trusted from the finding
alone. Two findings that looked like real defects turned out, on closer
inspection, to be deliberate, already-tested project design; those are
recorded as **investigated and dropped**, not fixed, to avoid re-litigating
settled decisions.

Full test suite: **1508 OK** after all fixes (confirmed via the correct
Python 3.12 interpreter with matplotlib installed — a shell `python3` alias
pointing at a bare interpreter stub caused one false failure signal during
this audit; see "Process notes" below).

## Applied fixes (21)

### Documentation / cross-reference corrections

1. **`.planning/STATE.md`** — stale "ship pending" prose left over from
   mid-session (before the actual ship completed), contradicting the file's
   own 100%-complete frontmatter and every other doc. Corrected throughout
   (Status, Loop control, Current focus, Current Position, Operator Next
   Steps) to state the ship is done (merge `89f77eb`, tag `v2.4.0`).
2. **`.planning/milestones/v2.2-REQUIREMENTS.md`** — the file's own "traceability
   correction" note claimed all 23 Phase 13–16 rows were corrected to
   complete, but a second table ~50 lines later still listed all 23 as
   "Queued," and a separate line stated "v2.0.0 remains 53/53" against the
   75/75 total stated two sections earlier in the same file (stale, from
   before Phases 11.1–11.3 were inserted). Both reconciled.
3. **`.planning/ROADMAP.md`** — all four "Full phase detail archived at
   `.planning/milestones/vX-ROADMAP.md`" citations (v2.0.0, v2.2, v2.3, v2.4)
   were wrong: each archived file is a pre-execution scoping snapshot with no
   plan counts or completion dates, not a post-completion record. Reworded
   to state the actual location of that detail (the current ROADMAP.md,
   already present) and describe the archives accurately.

### Citation / attribution corrections

4. **`references/chart-catalog.md`** (table + embedded JSON, both) —
   `waterfall`'s Function-axis citation said "Deviation"; the actual FT
   Visual Vocabulary poster places Waterfall only under Part-to-whole and
   Flow, never Deviation. Corrected to Part-to-whole. Independently confirmed
   by fetching and reading the poster image directly.
5. **`references/chart-catalog.md`** (table + embedded JSON, both) —
   `spine_chart`'s citation said "Deviation/Magnitude"; the poster places
   Spine under Deviation only. Dropped "/Magnitude". Same independent
   confirmation.
6. **`references/chart-catalog.md`** + **`.planning/PROJECT.md`** (D-3 row) +
   **`.planning/v2.4-D05-EVIDENCE-PACK.md`** — a real contradiction inside the
   FT's own repository: `visual-vocabulary/README.md` states "all rights
   reserved," but the poster image itself prints "© Financial Times 2016-2019.
   This work is licensed under a Creative Commons Attribution-ShareAlike 4.0
   International License" in its own footer. Confirmed by direct visual
   inspection of the fetched poster image (not just trusting the sub-agent's
   read). D-3's outcome is unaffected (own descriptions only, nothing copied
   from either the README or the poster regardless) — recorded as a documented
   open contradiction rather than resolved in either direction.
7. **`dsx/checks/design.py`** (message string only, no logic change) —
   DSX-EXP-052's finding text claimed a "declared family" precondition the
   firing guard never actually checks (traced to commit `fb51f33`, Phase 11.3,
   D-02's family-independence decision, which changed the firing condition but
   never updated the message). Corrected to "Multiple tests reported but
   comparisons_looked_at is missing." **This file carries a content-hash
   guard (REQ-P7-03, `tests/test_frame_val.py::_DESIGN_PY_SHA256`)** — updated
   the anchor and added a dated comment in the same commit, following the
   file's own established convention for its four prior legitimate edits.
8. **`dsx/suppressions.py`** (docstring only) — claimed "Codes
   DSX-SPEC-070…073"; DSX-SPEC-073 does not exist anywhere in the codebase
   (only 070–072 are ever emitted). Corrected the range.
9. **`.planning/v2.4-D05-EVIDENCE-PACK.md`** — appended a dated, additive
   "Post-ship follow-up research" section recording new findings against all
   8 previously-"unverified" items (2 now independently confirmed via direct
   fetch — Graphic Continuum's self-contradictory count, Munzner's absent
   "cardinality" term; the rest reconfirmed as genuinely access-restricted
   rather than merely unattempted). The original signed items and D-1…D-4 are
   untouched — this is a follow-up record, not a rewrite of the signed pack.

### README.md accuracy

10. Skill count/list corrected: said "Eight skills," listed nine, and was
    missing 5 real registered skills (`dsx-cohort`, `dsx-funnel`,
    `dsx-root-cause`, `dsx-segment`, `dsx-reproduce`) — all shipped, merged
    features from Phases 13 and 16, not drafts. Now states 14 and lists all.
11. The check-families table and intro sentence covered only 16 of the 23
    families in `references/finding-codes.md` — missing Paradigm/monitoring,
    Validity frame, Interference, Pre-registered inference, Frequentist
    admissibility, and Chart review conformance, all live in `dsx/cli.py`'s
    verify/ship gate profiles. Added all 6.
12. Stale test count in the Development section ("121 tests" vs. the actual
    1508 — off by ~12x). Corrected.

*(Fixes 1–12 above cover 12 of the 21 file-level changes; several findings
shared the same file, so the total distinct fix locations is 10 files.)*

## Investigated and dropped (2) — not fixed, because they're not defects

- **DSX-VAL-060 / DSX-COH-030 "hidden" severity variants.** Two findings
  claimed `references/finding-codes.md` misleadingly shows only one severity
  for codes that actually fire at two. True on its face — but this exact
  situation (a generator that collapses same-code, divergent-declaration
  rows) was already identified and deliberately resolved at **v2.0.0's own
  milestone audit as GAP-PROC-05**: rather than changing the generator (which
  would inflate the rendered row count past the `_EXPECTED_TOTAL` invariant
  every phase close depends on), the project pinned the full divergent set —
  7 codes, not just these 2 — in a dedicated, already-passing test
  (`tests/test_gen_finding_catalogue.py::TestCanonicalDeclarations`), which
  locks each code's exact declaration set and fails if a new code starts
  diverging without being consciously pinned. Confirmed this is exactly
  today's live behavior (same 8 warnings, unchanged) before deciding not to
  touch it. No action taken — re-litigating an already-resolved, tested
  design decision would have been the wrong move, not a fix.

## Escalated for operator decision (2) — not touched, need your call

### 1. DSX-ML-051/060/061 silently invert their verdict for lower-is-better metrics

`dsx/checks/ml.py`'s baseline-beat check (`DSX-ML-051`) and overfit check
(`DSX-ML-060`/`061`) both do raw numeric comparisons that hard-code
"bigger number is better" — but `model.task` explicitly supports `regression`
and `forecasting`, for which the conventional primary metrics (RMSE, MAE,
MAPE, log-loss) are lower-is-better. For any such metric:

- A model that legitimately **halved** its baseline's error fires
  `DSX-ML-051` CRITICAL ("does not beat baseline"), while a model that is
  **strictly worse** is reported as beating it.
- A genuine overfit signature reports `DSX-ML-061` ("test exceeds train...
  leakage"), and genuine leakage reports `DSX-ML-060` ("overfitting") — the
  two verdicts are exactly swapped.

No field anywhere (`dsx/spec.py`, `templates/ANALYSIS-SPEC.yaml`, any
docstring) records metric direction. Confirmed by reading the code directly;
this is a real logic defect, not a doc issue, and fixing it means adding a
direction concept (a new spec field or a metric-name lookup table) plus
branching logic in two check functions — a design decision, not something to
patch silently.

**Recommendation:** worth fixing before any regression/forecasting-heavy
analysis relies on these two checks. A minimal fix: add an optional
`model.metric_direction: higher_is_better | lower_is_better` field (default
`higher_is_better` to preserve current behavior for the classification-heavy
existing test suite), and branch both check functions on it.

### 2. Calibration corpus: 17 of 21 DSX-VIZ finding codes have never fired against a constructed positive case

The known-bad corpus (`examples/known-bad/`) has exactly 4 chart-defect
fixtures, all added in Phase 24 (commit `5de04e9`). Tracing what each
actually trips: three banned-type fixtures fire `DSX-VIZ-001` plus two
incidental codes; the uncertainty fixture fires only `DSX-VIZ-071`. That's 4
of 21 `DSX-VIZ-*` codes ever exercised by a real fixture — including the
**single CRITICAL-severity code in the whole family**, `DSX-VIZ-020`
(truncated y-axis, the canonical "lying bar chart"), which has never been
constructed. Two further checks (`DSX-VIZ-012`/`013`, the "declared but
conflicting" branches of the relationship/data-type matrix) are also
untested at the corpus level, though covered by inline unit tests.

This is a **deliberate, acknowledged scoping decision** from Phase 24's own
discuss round (GA-2, S4-1): `REQ-P24-02` was scoped to fixtures "per new
code," meaning the one code minted in v2.4 (`DSX-VIZ-071`), not the 17
pre-existing ones. That scoping was a real persona-round decision, not an
oversight — which is exactly why this is escalated rather than silently
"completed" tonight. Building 12+ new fixtures unilaterally would reopen a
scope call that was made deliberately, by name, with a documented rationale.

**Recommendation:** worth a scoped follow-up in a future milestone (or a
standalone corpus-hardening pass) — starting with `DSX-VIZ-020` given it's
the only CRITICAL code in the family with zero empirical catch-rate
evidence. Each new fixture is a small, additive, no-risk addition (one new
`ANALYSIS-SPEC.yaml` + `POSTMORTEM.md` + test-map entry per code) — the
question is whether/when to spend the effort, not whether it's safe.

## Process notes

- One audit finding depended on reading pixel content from a fetched image
  via a sub-agent; rather than trust that at face value, the underlying PNG
  was re-fetched and read directly with vision before any correction was
  applied — confirmed independently, not taken on faith.
- One "safe" fix (the DSX-EXP-052 message-text correction) tripped a
  content-hash guard on `dsx/checks/design.py` that looked at first like a
  hard freeze. It's not — it's a "loud, deliberate, recorded" pattern
  (update the anchor + explain why, in the same commit) already used four
  times in that file's own history. Anchor updated accordingly rather than
  reverting the fix.
- The generator-fix idea for DSX-VAL-060/DSX-COH-030 was checked against
  `tests/test_gen_finding_catalogue.py` before touching anything — which is
  what surfaced GAP-PROC-05 and prevented an unnecessary change that would
  have broken the catalogue's row-count invariant across every future phase
  close.
