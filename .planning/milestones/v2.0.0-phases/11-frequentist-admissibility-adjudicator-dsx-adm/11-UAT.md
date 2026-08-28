---
status: complete
phase: 11-frequentist-admissibility-adjudicator-dsx-adm
source: [11-VERIFICATION.md]
started: 2026-08-22T19:08:21Z
updated: 2026-08-28T00:02:00Z
---

## Current Test

number: 1
name: Read each of families.yaml's 14 family entries' citation string against its real source (T-11-13/T-11-14)
expected: |
  The cited work exists, actually supports the named estimator family, and locator_status
  (verified/unverified) matches whether the specific locator (chapter/section/page) was
  actually confirmed.
awaiting: none — all four checks resolved; ⚠Z fixed 2026-08-27 (S4-1b, see test 1 result)

## Tests

### 1. Citation authenticity for all 14 families.yaml entries (T-11-13/T-11-14)
expected: |
  The cited work exists, actually supports the named estimator family, and locator_status
  (verified/unverified) matches whether the specific locator (chapter/section/page) was
  actually confirmed.
why_human: No parser can confirm a citation string names a real, correctly-quoted source that
  supports the claim attached to it. Explicitly still-open per 11-04-SUMMARY.md ("has not yet
  been performed") and 11-VALIDATION.md's Manual-Only Verifications table.
result: [pass]
human_verdict: |
  2026-08-26 — Operator review (HQ-1). Thirteen of fourteen family citations accepted at
  article level. ⚠Z (HIGH): Zimmerman (2004) *Journal of General Psychology* 131(2):142-160
  for `no_variance_pretesting` could not be located in that volume/issue; flagged for manual
  research before the `verified` status on families #6/#7/#8 and `ranking_rules` can stand.
  Likely candidate: Zimmerman (2004), *British Journal of Mathematical and Statistical
  Psychology* 57(1):173-181, DOI 10.1348/000711004849222 — operator has not confirmed.
  ⚠L accepted as noted (Lydersen §9 pointer loose for domination half; substance real in §5.4/§6.4).
  2026-08-27 — ⚠Z RESOLVED (S4-1b). Operator confirmed Zimmerman (2004), *British Journal of Mathematical and Statistical Psychology* 57(1):173-181, DOI 10.1348/000711004849222 (HUMAN-QUEUE ⚠Z; verified via Wiley, PubMed, Semantic Scholar) — no article exists at the former *Journal of General Psychology* 131(2):142-160 locator. references/families.yaml corrected at all five Zimmerman sites; gen-finding-catalogue.py --check exit 0 and the full suite (1221 tests) green. Check 1 passes and REQ-P11-01 is satisfied. The no_variance_pretesting token (Zimmerman-only) is now truly locator_status: verified; families #6/#7/#8 and ranking_rules carry the corrected locator but stay locator_status: unverified for their other caveated co-citations (Delacre superseded tables, Ruxton unconfirmed, Cameron D-29 numbering).

### 2. DSX-ADM-010 finding wording does not overstate ranking strength
expected: |
  Uniform-domination language (Boschloo-over-Fisher) is used only where the source states a
  uniform result; hedged/default-preference orderings (Welch-over-Student, CV3-over-CV1,
  interacted-over-unadjusted) are worded as preferences, not dominations.
why_human: Only a reader can tell a uniform domination from a hedged reliability ordering apart
  in prose -- a test can assert the strength field is a valid enum value, not that the rendered
  sentence honestly reflects the source at that strength.
result: [pass]
human_verdict: |
  2026-08-26 — Operator review (HQ-1). Accept as noted. DSX-ADM-010 prints the ontology
  `strength` token verbatim and never renders "dominates"; cannot overstate beyond the field.

### 3. references/test-selection.md's corrected Fisher/Boschloo row and Lydersen footnote read correctly
expected: |
  The row no longer prescribes Fisher's exact as the small-cell fallback and the citation reads
  as an accurate, non-overstated summary.
why_human: 11-01-PLAN.md Task 2's own human-check requires this read; 11-01-SUMMARY.md records
  human_judgment true without recording that the read was performed.
result: [pass]
human_verdict: |
  2026-08-26 — Operator review (HQ-1). Accept as noted. Row correctly prescribes Boschloo over
  Fisher for small cells (D-27 fix confirmed). ⚠L accepted: domination claim is in Lydersen
  §5.4/§6.4 (analytic, credited to Boschloo 1970), not §9; §9 carries the "never use Fisher"
  recommendation only.

### 4. brief.md's two D-29 locators (Kohavi Tang Xu; Cameron Miller) read at the strength the evidence supports
expected: |
  The Kohavi locator reads as verified; the Cameron and Miller locator reads as
  manuscript-verified with the numbering caveat intact and unambiguous.
why_human: 11-01-PLAN.md Task 3's own human-check requires this read; 11-01-SUMMARY.md records
  human_judgment true without recording that the read was performed.
result: [pass]
human_verdict: |
  2026-08-26 — Operator review (HQ-1). Accept as noted. Kohavi Ch.22 identity confirmed (page
  range 226-234 second-hand only). Cameron & Miller VIII→XI numbering jump confirmed by direct
  manuscript read. ⚠LR accepted: `missing_at_random_given_covariates` Ch.3 §3.2 locator is
  wrong (taxonomy in Ch.1); adjacent to this check, follow-up fix unit. ⚠J informational only
  (Johari et al. arXiv byline author count — no action).

## Summary

total: 4
passed: 4
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

- **⚠Z — Zimmerman (2004) citation (Check 1, HIGH) — RESOLVED 2026-08-27 (S4-1b):** `references/families.yaml`
  formerly cited a non-existent *Journal of General Psychology* 131(2):142-160 entry for
  `no_variance_pretesting` (marked `verified`). Operator confirmed the real source and the loop
  corrected the locator at all five Zimmerman sites to *British Journal of Mathematical and
  Statistical Psychology* 57(1):173-181 (DOI 10.1348/000711004849222); catalogue gate + full
  suite green. Check 1 now passes and REQ-P11-01 is satisfied — the last open item from Phase
  11's original UAT round.
- **⚠LR — Little & Rubin Ch.3 locator (adjacent Check 4, MEDIUM, accepted as noted):**
  `missing_at_random_given_covariates` cites Ch.3 §3.2; taxonomy is in Ch.1. Follow-up fix
  unit (also affects `brief.md` §7 / DSX-VAL-060).
