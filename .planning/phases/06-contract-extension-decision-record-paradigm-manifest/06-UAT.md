---
status: diagnosed
phase: 06-contract-extension-decision-record-paradigm-manifest
source: [06-VERIFICATION.md]
started: 2026-08-08T12:00:00Z
updated: 2026-08-10T00:00:00Z
---

## Current Test

number: 4
name: Bayesian post-mortem states the Ville's-inequality formulation without conflation
expected: |
  The Deng, Lu & Chen (2016) citation is real and Theorem 1 supports the stated bound at
  K=19; the post-mortem's own text is internally consistent and does not slide into a
  different formulation.
awaiting: gap closure

## Tests

### 1. REVERSALS.md D-14 template is copyable and SELF-001 is defined, not merely named
expected: Template contains all four D-14 fields with self-explanatory prompts; SELF-001 states the exact triggering condition rather than just naming the convention.
result: pass
notes: Human validation confirmed all D-14 fields present with usable prompts. SELF-001 states the exact trigger (an empty or reasoning-restating New evidence field). Copyable without consulting brief.md.

### 2. README.md suppressions[] migration and known-limit prose reads as intended
expected: The authority requirement reads as a requirement, not a suggestion; the known limit is stated plainly, not softened or buried; both D-05 rigor tiers legible without brief.md.
result: pass
notes: Human validation confirmed the migration path states authority as a requirement (DSX-SPEC-070, "not a way to make the finding go away"). The known limit is the lead sentence of `## Known limits`. Both D-05 tiers are self-explanatory.

### 3. Interference post-mortem cites a real, verifiable failure pattern
expected: The cited source is real, the locator accurate, and the failure pattern genuine rather than invented to fit the fixture.
result: pass
notes: |
  Human validation confirmed. The UAT item was drafted expecting Hernan & Robins; the
  post-mortem actually cites Kohavi, Tang & Xu (2020) and Imbens & Rubin (2015)
  Chapter 1 Section 1.6. Both are real and on-point. Imbens Section 1.6 is SUTVA
  (the stable unit treatment value assumption) — locator confirmed.

  Optional upgrade available: the post-mortem currently records at line 39 that the
  Kohavi chapter number "could not be verified". Human validation confirmed the
  matching chapter is Chapter 22, "Leakage and Interference between Variants"
  (table of contents confirmed). The post-mortem correctly refused to invent a
  chapter number; that caveat can now be replaced with the verified locator.

### 4. Bayesian post-mortem states the Ville's-inequality formulation without conflation
expected: The Deng, Lu & Chen (2016) citation is real and Theorem 1 supports the stated bound; the post-mortem does not conflate formulations.
result: fail
notes: |
  Partial pass: the formulation split (prior-averaged versus point-null /
  law-of-iterated-logarithm) is stated clearly and correctly. Deng, Lu & Chen (2016)
  is a real paper. The frequentist fixture's Armitage (1969) reference and its
  approximately 0.142 figure at five looks are real.

  The failure is the locator claim. See Gap G-01 below.

## Summary

total: 4
passed: 3
issues: 1
pending: 0
skipped: 0
blocked: 0

## Gaps

### G-01: Deng Theorem 1 locator misattributed in the Bayesian post-mortem
status: failed
severity: high
source_test: 4
files:
  - examples/known-bad/bayesian-continuous-monitoring-POSTMORTEM.md
  - examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml

what_is_claimed: |
  `examples/known-bad/bayesian-continuous-monitoring-POSTMORTEM.md` line 45 states the
  bound is `1/19 ~ 0.0526`, "commonly rounded and reported as 0.05". Lines 63-64
  attribute this to Deng, Lu & Chen (2016) Theorem 1, characterised as "the martingale
  (Ville's inequality) argument".

what_is_true: |
  Deng, Lu & Chen (2016) Theorem 1 states that observing posterior odds K gives a
  false-discovery risk of `1/(K+1)`. At K=19 that is `1/20 = 0.05` exactly — not
  `1/19 ~ 0.0526`. The paper's proof is a likelihood-ratio / Bayesian-promise argument
  and does not invoke Ville by name.

  Ville's inequality separately and genuinely gives `1/k` for a nonnegative martingale
  starting at 1 crossing threshold k. Both statements are individually true; the defect
  is pinning the classic Ville `1/k` form onto Deng Theorem 1, then papering over the
  resulting `0.0526` versus `0.05` gap with the word "rounded". Those are two different
  bounds from two different theorems, not one bound rounded.

internal_contradiction: |
  The repository already contains the correct form in its binding Phase 9 text:
  `.planning/REQUIREMENTS.md` line 118 (REQ-P9-02) and `.planning/ROADMAP.md` line 314
  both assert the bound `1/(K+1)` — at K=19, `0.05` — citing Deng Theorem 1. Phase 9 is
  scheduled to ship a test asserting that value. Left uncorrected, this fixture's
  post-mortem and Phase 9's test would cite the same theorem for different numbers.

drift_sites: |
  The same `1/k` drift appears in three further places that feed future work:
  - `brief.md` lines 408-409, section 6.5: "caps the probability ... at roughly 1/k"
  - `.planning/phases/06-.../06-08-PLAN.md` lines 256, 261: the drafting guidance the
    executor followed
  - `06-08-PLAN.md` line 275: a verification assertion that requires both the strings
    "19" and "0.05" to appear in the post-mortem, which encoded the confusion into the
    plan's own acceptance check

  Separately, `REQUIREMENTS.md` line 118 and `ROADMAP.md` line 314 have the correct
  arithmetic but still name the bound "the prior-averaged Ville bound", carrying the
  attribution half of the drift into Phase 9.

blocked_by_tests: none
notes: |
  No committed test asserts the disputed value. `tests/test_known_bad_corpus.py` guards
  only the two retired gate-overclaim strings (line 71), so correcting this prose breaks
  no test. Verified by grep across `tests/` — the `0.05` matches in `tests/test_dsx.py`
  are unrelated significance levels.
