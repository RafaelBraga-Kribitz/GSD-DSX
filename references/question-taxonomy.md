# Question taxonomy

The classification is not cosmetic. It determines which gates apply, what
evidence is required, and — most importantly — which verbs the deliverable is
allowed to use.

| Type | Answers | Minimum evidence | Licensed verbs |
|---|---|---|---|
| `descriptive` | What happened? | Clean definitions, complete data, stated period | was, were, showed, recorded |
| `diagnostic` | Why, within the observed data? | Decomposition that accounts for the whole change | accounted for, contributed, coincided with |
| `predictive` | What will happen? | Out-of-sample score, beaten baseline | predicts, forecasts, is associated with |
| `causal` | What is the effect of X on Y? | A named identification strategy with its assumptions | causes, increases, drives, results in |
| `prescriptive` | What should we do? | A causal estimate plus a decision rule and cost model | we should, the expected value of |

## The classification error that matters

**Labelling a causal question as diagnostic to avoid the burden of
identification.** It is easy to do and it feels conservative — you avoid saying
"causes". But if the stakeholder will act as though the relationship is causal,
it is a causal question regardless of the label, and a diagnostic analysis has
given them no basis to act.

The honest test: *if we changed X, would they expect Y to change?* If yes, the
question is causal. Then either meet the burden, or tell them explicitly what
the data cannot establish and what study would.

## Escalation

Each type subsumes the requirements of the ones above it. A prescriptive answer
needs a causal estimate, which needs a design, which needs clean descriptive
foundations. Skipping a level does not save time; it moves the failure later.

## Downgrading is a legitimate outcome

"We cannot answer whether onboarding causes activation with this data, but here
is what changed and when, and here is the experiment that would answer it" is a
better deliverable than a confident regression coefficient. Deliver the downgrade
explicitly rather than silently.

## Selection heuristic — Layer 1 (question → task)

This table is also Layer 1 of the five-layer chart-selection heuristic: the
question type fixes the analytical **task** before any chart is chosen. Read the
task off Munzner's task taxonomy (2014, ch.3 — Actions × Targets): descriptive
and diagnostic questions *present* and *discover* within observed data;
predictive and causal questions *derive* a new quantity and *compare*
alternatives; prescriptive questions *decide* between actions. Once the task is
named, route onward — `references/chart-selection.md` carries Layers 2–5
(relationship → mark → encoding → uncertainty) and `references/chart-catalog.md`
carries the marks themselves. This reuses the table above; it does not restate
it or add a parallel decision tree.
