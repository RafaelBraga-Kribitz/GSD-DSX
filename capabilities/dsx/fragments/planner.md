<dsx_planner_contract>
**This phase is analytical work.** Plan it as an argument to be defended, not a
pipeline to be built.

**Before any task exists, `ANALYSIS-SPEC.yaml` must be filled.** It is the
deterministic input every gate reads. A plan whose spec is incomplete will be
blocked at `plan:post` by `dsx gate plan` — so treat spec completion as task
zero, not documentation.

**Decompose backwards from the decision.** The order is fixed because each step
is only checkable once the previous one is fixed:

1. **Decision** — who acts, on what rule, and what happens under the null.
   Written before results exist. This is the defence against reading the answer
   out of the data afterwards.
2. **Metric** — one name, one definition, an explicit denominator and a grain.
3. **Design** — how confounding is ruled out. For an experiment: the
   randomization unit, the analysis unit, and the power arithmetic.
4. **Data** — sources, period, row counts, known gaps.
5. **Analysis** — the test derived from the outcome's shape, not from habit.
6. **Communication** — the claim, typed and scoped to what the design licenses.

**Task-shape rules for analytical phases:**

- The first task always produces or completes `ANALYSIS-SPEC.yaml`.
- Data-quality profiling is its own task, before any modelling task. Discovering
  a broken join after the model is trained wastes the model.
- Never plan "run the analysis" as one task. Split acquisition, validation,
  analysis and readout — each has a different failure mode and a different fix.
- A modelling task must be preceded by a baseline task. A model that never got
  compared to `majority_class` or `last_value` has not been evaluated.
- Every task producing a number must name the artefact that number lands in, so
  a claim can point at it.

**Refuse to plan these:**

- A causal question with observational data and no identification strategy. Send
  it back: either the strategy is named, or the question is re-scoped as
  diagnostic and every claim is reworded as association.
- An experiment whose planned sample is below what its own MDE requires. The
  arithmetic is not negotiable — run `dsx power --baseline <p> --mde <d>` and
  plan the real number, or plan a larger MDE.
- A dashboard task with no declared metric definitions. It will produce numbers
  that disagree with another dashboard within a quarter.

**Verify before finishing:** run `dsx gate plan --phase-dir <phase>` yourself. If
it blocks, fix the spec now — the gate will block the loop otherwise, and it
reports exactly which field and why.
</dsx_planner_contract>
