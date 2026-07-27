# Narrative discipline

Gates that keep the decision-maker's document from outrunning the evidence.

## Required artefacts

| Field | Rule |
|---|---|
| `narrative.path` | Required at ship when `claims[]` is non-empty; file must exist |
| `claims[].text` ⊆ narrative | Every claim string (whitespace-normalised) must appear in the deliverable |
| `limitations[]` | Non-empty at verify/ship for causal / prescriptive / predictive questions |

## Relative percentages need a base

"Up 40%" from 5→7 is not the same story as 500→700. Readers assume the larger one.

A claim (or narrative sentence) with a relative `%` must have either:

- nearby base language (`from …`, `n=`, `of N users`, …), or
- `base_n` set, or
- both `from_value` and `to_value`.

Absolute "2.4 percentage points" with a CI is already covered by `DSX-CLM-033`.

## Forbidden wording

Universal pack (always on) plus optional `FORBIDDEN-CLAIMS.yaml` in the phase dir:

- "the data proves / shows that / demonstrates that"
- "with high confidence"
- "under virtually all scenarios"

Project-specific refuted claims belong in the phase file, not in dsx core.

## Dashboard (optional)

If `dashboard.path` is declared, the path must exist at ship. No BI skill is required.
