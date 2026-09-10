---
phase: 30-calibration-rebaseline
verified: 2026-09-10T00:00:00Z
status: passed
verdict: PASSED
score: 3/3 requirements MET (REQ-P30-01/02/03); terminal calibration re-baselined LIVE over the grown 42+15 corpus with the three v2.6 cases classified (2 misses DSX-ML-034/DSX-CLM-034 + 1 target DSX-COH-041); zero codes minted (set-identity 279->279); the two stale doc records re-baselined and pinned by a new agreement test; code review 0 BLOCKER/HIGH/MEDIUM (2 LOW accepted); adversarial dsx-statistician review RECORD-WITH-AMENDMENTS (F1/F2 applied as prose framing, F3-F7 held, no measured number changed)
behavior_unverified: 0
overrides_applied: 0
re_verification: false
gaps: []
human_verification:
  - "End-of-phase security sign-off (S6-5 /gsd-secure-phase 30) — batched to HUMAN-QUEUE, non-blocking until S7-2 per brief §6."
  - "End-of-phase UAT round (S6-5 /gsd-validate-phase 30) — batched, non-blocking until S7-2."
---

# Phase 30: Calibration re-baseline (terminal) — Verification Report

**Phase Goal:** Re-measure the stratified calibration (catch rate, FPR, every stratum,
friction) LIVE over the post-v2.6 corpus after Phases 27/28/29 wired the three evidence
cases; classify each of the three cases from the committed harness wiring (PRESENT with its
new firing code, or ABSENT with an attribution sidecar); confirm the miss-partition floor
still holds; re-baseline the two stale calibration records (the `brief.md` §6.5 backdrop and
the `docs/literature/the-ai-data-scientist.md` deferred table) with each item's measured
outcome; and confirm every milestone-audit prerequisite — all with **zero codes minted**
(set-identity 279 → 279) and every gate module and corpus fixture byte-frozen. Phase 30
**measures**; it does not design.

**Verified:** 2026-09-10 (orchestrator, all gates re-run on real Python 3.12.10 —
`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`; not trusted from a
subagent report).

**Status:** passed — 3/3 requirements MET.

## Verdict

`passed`. All three phase requirements are met. The `gsd-code-reviewer` (opus) returned
**0 BLOCKER / 0 HIGH / 0 MEDIUM / 2 LOW** (`30-REVIEW.md`, verdict SHIP) and confirmed all
four load-bearing invariants hold outright: doc claims match measured reality; the new
agreement test cannot false-pass or over-fire; the read-only measurement companion resolves
ROOT correctly and never perturbs the PRESENT/ABSENT partitions; no frozen surface was
touched. Both LOW findings are latent (the agreement regex's first-match binding is safe
today; the "satisfied" doc wording is adequately qualified in-cell) and accepted per GA-4
scope. The adversarial `dsx-statistician` (opus) — the load-bearing S6-4 sub-task deferred
from the discuss per GA-1 — returned **RECORD-WITH-AMENDMENTS** (seven findings, `30-STATS-REVIEW.md`):
one real prose defect (**F1** — §4 said "four ICC/kappa/weighted-kappa", making the
enumeration sum to 19 against the stated 18) and one honest-framing amendment (**F2** — §2c
had dropped the Phase-12 distinction that four of the five misses are catchable in their
declared form). Both were applied to `30-READOUT.md` §4/§2c after the orchestrator
independently re-verified them against the live tree (brief §5 — F1 confirmed by a corpus
glob: exactly three reliability + two correlation fixtures); F3–F6 held sound as found; F7
held sound with a loud note and not applied. **No amendment changed a measured number.** No
requirement is provisional. The D-13 "measure before you conclude" rule was satisfied at
S6-3 (`30-READOUT.md`, every number computed live off the gate path); this unit reviews and
verifies that record without re-measuring, then re-runs the audit battery.

## Requirement verdicts

### REQ-P30-01 — MET
Catch rate, FPR and every stratum were re-measured LIVE over the grown corpus (**42 known-bad
+ 15 good-control** ANALYSIS-SPECs) and recorded in `30-READOUT.md`, reproduced by the durable
gate `tests/test_known_bad_corpus.py::test_stratified_catch_rate_and_fpr_report` (re-run this
unit: **OK, 7.8s**). The headline is the pair **(miss-rate 1.0 = 5/5, FPR 0.0 = 0/15)** (D-10,
never catch-rate alone). The three v2.6 cases are classified exactly as the committed harness
wiring forces (GA-2, confirmed live, not re-decoded): **feature-origin-only-leak** → ABSENT
miss attributed to `DSX-ML-034` (item 7), and **magnitude-without-computed-effect** → ABSENT
miss attributed to `DSX-CLM-034` (item 8), each measured `fires_at_any_severity: false`;
**subgroup-harm-without-disposition** → PRESENT target `DSX-COH-041` (item 9), firing CRITICAL
at plan/verify/ship (the corpus's first `kind: target`). The miss-partition floor
`_ABSENT_PARTITION_FLOOR = 3` still holds — measured misses now 5 ≥ 3 (up from exactly 3 in
Phase 12). Both stale records were re-baselined: `brief.md` §6.5 gained a dated Phase-30
re-evaluation section reading the measured pair (the Phase-12 block preserved as history), and
`docs/literature/the-ai-data-scientist.md` flipped rows 7/10/12 from `deferred` to satisfied
with the code + fixture + measured evidence, retitled the "What was deferred, and how it was
promoted (D-13)" section, and updated the row-15 corpus counts 39 → 42.

### REQ-P30-02 — MET
Every milestone-audit prerequisite is green on the real interpreter, orchestrator-re-run this
unit: `gen-finding-catalogue.py --check` exit 0 ("finding catalogue is current"); all frozen
snapshots and doc/code agreement tests pass (`test_finding_catalogue_invariant`,
`test_phase20_zero_mint_close`, `test_p19_categorical_rows`, `test_doc_code_agreement`,
`test_selection_heuristic_docs` + the new agreement test = **30 OK**); `node install.mjs --check`
self-test passed (6/6 agents, 14/14 skills, 5 gates); `scripts/check.sh` "all checks passed"
(including the determinism check); full suite **1629 tests OK**. The one genuine gap the audit
surfaced — no existing test bound the literature record's row-15 corpus counts to the live
corpus (precisely the drift that let the doc read "39" while the corpus had grown to 42) — is
closed by the new off-gate-path `tests/test_literature_corpus_count_agreement.py` (asserts
DOC == LIVE glob agreement, never a hardcoded literal; **2 OK**), which pins nothing beyond the
row-15 counts (GA-4: "close exactly this gap and no more").

### REQ-P30-03 — MET
Zero new codes. The authoritative set-identity gate is `gen-finding-catalogue.py --check`
(exit 0, "current") over the live catalogue re-measured at **279** (`references/finding-codes.md`
"Total: 279 codes.", 279 rows) — set-identity **279 → 279, added={} removed={}**. Every frozen
surface is byte-clean across the whole phase: `git diff --stat 03de340^..HEAD -- dsx/ examples/
references/finding-codes.md` is **empty**. The phase's only tracked edits are `brief.md`, the
literature doc, and the new agreement test; the measurement companion and this readout are
`.planning` artifacts off the gate path.

## Code review disposition (`30-REVIEW.md` — 0 BLOCKER / 0 HIGH / 0 MEDIUM / 2 LOW — verdict SHIP)

- **LOW-01 (`tests/test_literature_corpus_count_agreement.py`) — ACCEPTED (latent).** The
  agreement regex's `.search()` first-match binding is safe today (exactly one `\d+ known-bad
  specs` phrase survives in the doc) but would silently bind the wrong line if a second such
  phrase were later added earlier in the doc. Accepted per GA-4 scope (close exactly the gap and
  no more); the invariant holds today.
- **LOW-02 (`docs/literature/the-ai-data-scientist.md` rows 7/10) — ACCEPTED (latent).** "satisfied"
  in the status cells is adequately qualified in-cell as "attributed miss" and by the disposition
  table's "buys attribution, not a catch." No overstatement survives; no fix owed.

All four load-bearing invariants (doc↔measurement agreement; agreement test cannot false-pass /
over-fire; companion ROOT + partition safety; frozen surfaces untouched) were independently
re-confirmed by the reviewer live (companion run, reproducer green, `git diff` empty).

## Statistician adversarial review disposition (`30-STATS-REVIEW.md` — RECORD-WITH-AMENDMENTS)

The full review and the orchestrator adjudication are recorded in `30-READOUT.md` §6. Summary:
**F1** (§4 "four" → "three" reliability fixtures) — a real internal inconsistency (enumeration
summed to 19 vs the stated 18), **applied** after a live corpus glob confirmed exactly three
reliability fixtures. **F2** (§2c catchable-in-declared-form distinction, Phase-12 F2 precedent)
— **applied** as a prose sentence so 5/5 is not misread as intrinsic undetectability. **F3–F6**
(miss-rate construction-invariant; FPR 0/15 bound ≈ 0.181 re-derived; RAW/NET friction honesty;
PRESENT 10/10 conservative counting) — **held sound**, each re-verified live. **F7** (§5 clean-by-
construction mechanism clause) — **held sound, not applied** (a loud §5 note; the mechanism is
already carried by §5's "minimal, self-contained"). No measured number changed.

## Gate evidence (orchestrator-re-run, real 3.12.10 — Python 3.12.10)

- Full suite: **1629 tests OK** (`unittest discover -s tests`, 65.7s; no skips — the plotstyle
  determinism test ran, not skipped under a python3 stub).
- Reproducer of record `test_stratified_catch_rate_and_fpr_report`: **OK** (7.8s) over the 42+15
  corpus (independent PRESENT/ABSENT denominators, 5-case ABSENT floor ≥ 3, target-present
  invariance proof).
- Catalogue: `gen-finding-catalogue.py --check` exit 0, "current"; live count re-measured **279**;
  set-identity **279 → 279** (REQ-P30-03 zero-mint). The DSX-COH-041 "declared twice" warnings are
  the by-design two-severity dedup pattern, non-failing.
- Frozen snapshots + doc/code agreement (incl. the new REQ-P30-02 test): **30 OK**.
- `node install.mjs --check`: self-test passed (6/6 agents, 14/14 skills, 5 gates).
- `scripts/check.sh`: "all checks passed" (determinism check included).
- Frozen-surface diff for the whole phase (`03de340^..HEAD -- dsx/ examples/ references/finding-codes.md`):
  **empty**. No REQUIREMENTS/STATE/ROADMAP edited by any subagent (single-writer).

## Human verification (batched, non-blocking until S7-2)

1. Security sign-off (S6-5 `/gsd-secure-phase 30`) — SECURITY.md approval line.
2. UAT round (S6-5 `/gsd-validate-phase 30`).

Both to be filed to HUMAN-QUEUE at S6-5 per brief §6; neither blocks any earlier unit.
