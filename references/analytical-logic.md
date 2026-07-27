# Analytical logic

Gates that keep the decision logic honest after results exist (dims 2 and 7).

## Assumption dispositions

For causal / prescriptive questions, every `assumptions[]` entry must at ship have
either `checked: true` or a non-blank `waiver`. An unchecked assumption without a
waiver is not a plan — it is an undeclared risk (`DSX-COH-031`).

## Null is not “no effect”

Failing to reject H0 is not evidence of equivalence. A null-phrase interpretation
(`no difference`, `no effect`, …) requires one of:

1. `equivalence_bound` **and** the CI wholly inside ±bound, or
2. `tost.lower_p` and `tost.upper_p` both &lt; α, or
3. a declared `detectable_mde` (study power floor).

Bare `equivalence_bound` without CI/TOST proof no longer clears the gate.

## Exploratory cuts vs multiplicity family

`results.comparisons_looked_at` counts every cut actually examined, including
segments labelled exploratory. If it exceeds `len(design.multiplicity.family)`,
the declared correction understates the family (`DSX-EXP-051`).

## Decision replay

Do not ask the gate to parse English `decision_rule`. Declare structured
thresholds in `decision.replay` and evaluate them against `results.tests`.
The finding detail includes a compact JSON verdict for agents to quote.

## repro_lock (honest null)

When `results.tests` is non-empty:

| Value | Verdict |
|---|---|
| key omitted | `DSX-REP-050` HIGH |
| `repro_lock: null` | `DSX-REP-051` MEDIUM — honest opt-out |
| populated object | requires `schema_version` + `stochasticity_declaration` |

The lock documents configuration. It is not a byte-replay guarantee.

## Reconciliation classes

| class | default relative tolerance |
|---|---|
| financial | 0.005 |
| user | 0.02 |
| behavioral | 0.05 |
| default | 0.01 |

Per-metric `tolerance` overrides the class default.
