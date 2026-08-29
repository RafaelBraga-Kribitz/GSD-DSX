---
phase: 15-cuped-and-bi-declaration-checks-new-codes-d-05
plan: 03
status: complete
requirements: [REQ-P15-05, REQ-P15-06]
---

# 15-03 SUMMARY — APA research template + Shapiro negative assertion, no mint

## What shipped
- **`templates/APA-TABLE-research.md`** (new) — an optional research-domain APA-style results table
  (group/condition · n · M · SD · statistic+symbol · df · p · effect size (kind) · 95% CI columns + a
  `Note.` line), mirroring `templates/DISCLOSURE-research.md`. Header states it is optional and
  research-domain and that the marketing ship path (narrative + sealed figure + claim evidence via the
  unchanged NAR/FIG/CLM codes) is unchanged. States normality is a **declared** shape+n property, never a
  tool-run test that flips the recommended test. Mints nothing.
- **`tests/test_apa_template.py`** (new) — existence, APA column vocabulary, and domain framing.
- **`tests/test_no_shapiro_autoswitch.py`** (new, D-07) — pins `references/test-selection.md`'s fixed
  assumption order (independence → equal variance → normality), the unconditional Welch recommendation,
  and normality-as-declared-small-n; and scans the gate + skill decision surface (`dsx/` and `skills/`
  only — never `tests/`, never the untracked `references/` paper) for normality-test CALL tokens
  (`scipy.stats`/`shapiro(`/`normaltest(`/`anderson(`/`kstest(`) with an anti-vacuity named non-empty set.

## Gate evidence (all re-run by the orchestrator, brief §5)
- `python -m unittest tests.test_apa_template` → OK; template column/domain assertions pass.
- `python -m unittest tests.test_no_shapiro_autoswitch` → OK; decision-surface grep over dsx/+skills/
  finds zero normality-test calls.
- `git status --porcelain -- dsx/ references/finding-codes.md` empty for this plan (no gate edit, no mint).
