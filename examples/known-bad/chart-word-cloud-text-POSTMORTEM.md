# Post-mortem: category counts shown as a word cloud

Paired spec: `chart-word-cloud-text-ANALYSIS-SPEC.yaml`

One of the first **bad-chart-choice** fixtures (Phase 24, GA-2): a clean analysis
carrying exactly one bad visual. The underlying spec is a copy of the clean
`examples/good-corpus/freq-count-referrals` control and clears the two
CRITICAL-threshold gate points exactly like its base.

## What was concluded

A growth team presented "which sources drive referrals" as a word cloud — each
referral source rendered as text sized by the number of referrals it produced,
laid out to fill a rectangle.

## Why it was wrong

A word cloud sizes words by a raw count and lays them out for packing, not for
comparison. Area is a weak perceptual channel to begin with, and word length
confounds it further: a long low-count source can occupy more space than a short
high-count one, so the reader cannot reliably rank the sources or read the gap
between them — the very quantities the chart exists to show. It strips context and
carries no baseline. A sorted horizontal bar chart shows the same counts on a
position/length encoding the reader can actually decode.

## Source

Jacob Harris, "Word clouds considered harmful", Nieman Journalism Lab,
2011-10-13 (HQ-27, signed 2026-09-03) — the editorial rationale recorded in
`dsx/checks/viz.py` `BANNED_TYPES["word_cloud"]`. The objection here is
editorial/analytical, not a single perceptual constant.

## Which code catches it

`DSX-VIZ-001` (HIGH) — `word_cloud` is a live member of `BANNED_TYPES`, so
`_check_banned` refuses it at `dsx gate verify` and `dsx gate ship`. It routes to
the **existing** `DSX-VIZ-001` shared by every banned mark — no new code minted.
The incidental MEDIUM findings (`DSX-VIZ-010`, `DSX-VIZ-014`) are below the HIGH
block threshold and are not the encoded defect.
