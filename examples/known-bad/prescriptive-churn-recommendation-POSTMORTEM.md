# Post-mortem: a prescriptive recommendation smuggled under a descriptive question

Paired spec: `prescriptive-churn-recommendation-ANALYSIS-SPEC.yaml`

## What was concluded

A customer-success analytics team set out to answer a descriptive question — how
quarterly churn moved across the enterprise customer segments over FY26. The
question was framed honestly as descriptive: a summary of what happened, with no
inference beyond the observed accounts. But the deliverable it produced did not
stop at description. Its headline claim was a recommendation — "offer bundled
incentives to reduce churn in the at-risk enterprise segment" — and its decision
rule committed the business to acting on that recommendation ("offer bundled
incentives to the at-risk segment to reduce churn whenever the segment's observed
quarterly churn sits above 6%"). No identification strategy was declared behind the
recommended intervention; the recommendation rested on nothing more than the
observed churn levels the descriptive analysis reported.

## Why it was wrong

A descriptive analysis establishes what happened in the sample. It does not
establish that a specific intervention will change what happens next. The jump from
"the at-risk segment churned at 6%" to "offer this segment bundled incentives to
reduce churn" is a jump across three rungs of inferential strength — from a
descriptive summary, past association, past prediction, past causation, to a
prescription — with no evidence at any intermediate rung. The observed churn rate
is consistent with the incentive working, with it doing nothing, and with it making
matters worse (the at-risk segment may be at risk for reasons an incentive does not
touch). A recommendation is an intervention, and an intervention needs
identification — a design or an argument that rules out the confounding between the
segment's churn and everything else that moves with it — not merely an association,
and certainly not merely a description.

The defect is not that the recommendation is necessarily wrong. It may even be
right. The defect is that the frame claims a strength of evidence the analysis does
not carry: a descriptive question, answered with descriptive data, cannot license a
prescriptive commitment. Framing the question as descriptive while shipping a
prescriptive claim is precisely how an analysis passes its own honesty test on the
question line while overreaching on the claim line — the frame reads as modest, and
the recommendation rides out under cover of that modesty.

## The codes that catch it

Four findings fire against this fixture, at two gate points, each attributable to
one part of the encoded defect:

- **`DSX-COH-001`** (CRITICAL, `dsx/checks/coherence.py::_check_claim_ceiling`).
  The claim is typed `prescriptive` (strength 4) while the question is typed
  `descriptive` (strength 0); a claim may not exceed its question's ceiling. Fires
  at `dsx gate plan` onward — `coherence` is in the plan, verify and ship gate
  profiles (`dsx/cli.py::GATE_PROFILES`).

- **`DSX-COH-010`** (CRITICAL, `dsx/checks/coherence.py::_check_decision_language`).
  The decision rule uses the purpose-gated causal verb `reduce` ("...to reduce
  churn") under a descriptive question. The purpose gate
  (`dsx/spec.py::causal_verb_matches`) fires `reduce` only when a purpose marker
  ("to") precedes it within a bounded window — which is exactly the recommendation
  phrasing here. Fires at `dsx gate plan` onward.

- **`DSX-CLM-011`** (CRITICAL, `dsx/checks/claims.py::_check_causal_language`).
  The claim is not typed `causal`, is not hedged, yet uses the causal verb
  `reduce`. Readers take the verb and drop the type label. Fires at `dsx gate
  verify`/`ship` — `claims` is in the verify and ship gate profiles only.

- **`DSX-CLM-020`** (CRITICAL, `dsx/checks/claims.py::_check_causal_support`).
  The claim is prescriptive and recommends an intervention, but neither the claim
  nor the design declares an identification strategy behind it (a prescriptive
  claim is held to the same identification standard as a causal one — the superset
  gate, D-03). Fires at `dsx gate verify`/`ship`.

`dsx gate execute` exits 0 on this fixture: neither `coherence` nor `claims` is
registered in the execute gate profile (`dsx/cli.py::GATE_PROFILES`), so the two
plan-time coherence catches and the two verify/ship-time claim catches all fall
outside execute. The fixture is otherwise structurally clean, so it passes `dsx
validate` (which runs only the `spec` structural check).

## What this fixture deliberately does not exercise

The fixture keeps `question_type: descriptive` and `design.kind: observational` on
purpose. Setting either `question_type: prescriptive` or `design.kind: experiment`
would pull the causal `validity_frame` sub-blocks into scope and fire `DSX-COH-040`
(missing revisit trigger) and `DSX-PRE-040` (missing `spec_id`) — findings this
fixture is not built to demonstrate. Isolating the four catches above is the whole
point: a prescriptive claim under a descriptive question, with no identification, is
the single defect on trial here.

## Known limit this fixture does NOT close (D-15)

A recommendation phrased without any causal verb — "offer bundled incentives" on its
own, with no "to reduce churn" trailing it, or "prioritise segment Y", or "the
optimal action is X" — would still be a prescriptive claim under a descriptive
question, and `DSX-COH-001` would still catch the type-ceiling breach. But
`DSX-COH-010` (decision-rule causal language) and `DSX-CLM-011` (claim causal
language) would both fall silent, because there is no causal verb to match. The
identification catch `DSX-CLM-020` depends only on the claim being typed
prescriptive with no identification, so it survives; but the verb-based catches do
not. Closing the verbless-recommendation hole — recognising an imperative
recommendation by its imperative mood rather than by a causal verb — is a named,
deferred limit (see the README "Known limits" section), not something this fixture
or this phase's checks catch.
