# Post-mortem: shared advertising budget interference

Paired spec: `interference-shared-budget-ANALYSIS-SPEC.yaml`

## What was concluded

A growth-marketing team ran a randomized experiment raising bid caps for a
high-intent audience segment (treatment) against the existing bid caps
(control), split at the user level. The team concluded the raised bid caps
increased the 24-hour signup rate by 0.6 percentage points and rolled the
change out to 100% of the audience.

## Why it was wrong

Both arms drew ad impressions from one shared, capacity-limited daily
advertising budget managed by the ad platform's auction. Treatment's higher
bid caps won a larger share of that shared budget's auctions, which reduced
the volume of impressions the platform served to control on the same days.
Control's measured signup rate fell in part because control users were
simply shown fewer ads — not because they behaved differently in response to
the bid-cap change. The two arms were not independent of one another: this
is a textbook Stable Unit Treatment Value Assumption (SUTVA) violation via a
shared, finite resource, the same failure mode documented for shared paid
media budgets, shared inventory pools, and other capacity-limited resources
split between test and control. The observed 0.6pp lift conflates a real
behavioral effect with a budget-reallocation artifact; the two cannot be
disentangled from the data as collected, because no mitigation (geo split,
cluster randomization, time split or budget isolation) was applied and no
residual interference note was recorded.

## Source

Kohavi, R., Tang, D. & Xu, Y. (2020), *Trustworthy Online Controlled
Experiments: A Practical Guide to A/B Testing*, Cambridge University Press,
Chapter 22 ("Leakage and Interference between Variants") — the chapter
documents shared-resource interference (including shared
advertising/marketing budgets) as a recurring, catastrophic threat to
experiment trustworthiness, and the book is named explicitly in the reference
list this project anchors D-05 citations to (brief.md section 7). The chapter
locator was confirmed against the published table of contents during Phase 6
human verification; the authoring pass correctly declined to invent it rather
than guessing.

Imbens, G.W. & Rubin, D.B. (2015), *Causal Inference for Statistics, Social,
and Biomedical Sciences*, Cambridge University Press, Chapter 1, Section 1.6
("The Stable Unit Treatment Value Assumption") — the formal SUTVA statement
this interference pattern violates: one unit's assigned treatment must not
affect another unit's potential outcomes. A shared, capacity-limited budget
is exactly the channel through which treatment "leaks" from one arm into the
other's observed outcome.

Vendor blogs, Medium posts and tool marketing are inadmissible under D-05 in
either direction — neither cited source is one.

## Which absent code would have caught it

`DSX-INT-010` (Phase 8) — no code in this codebase adjudicates
`validity_frame.interference` today; Phase 6 only checks that the block is
present and its fields are legal vocabulary members (`dsx/spec.py`'s
`_validate_validity_frame_shape`), so nothing in this repository names the
shared-budget interference defect today: the fixture clears `dsx validate`
and both CRITICAL-threshold gate points, `dsx gate plan` and `dsx gate
execute`, with no finding attributable to that defect. The fixture does
block at `dsx gate verify` and `dsx gate ship` (both exit 1), on the
corpus-completeness gaps named in the paired ANALYSIS-SPEC.yaml header —
tracked as a corpus completeness gap, not as the documented interference
defect. Phase 8 is scoped to block a declared `interference.risk` other than
`none` when `interference.mitigation` is `none` and `residual_note` is
blank — precisely the combination this fixture declares.
