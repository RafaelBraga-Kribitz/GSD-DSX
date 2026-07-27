<dsx_plan_review>
This is an analytical phase. Beyond the standard plan review, verify:

- **`ANALYSIS-SPEC.yaml` exists and is complete.** Run
  `dsx gate plan --phase-dir <phase> --verbose`. A non-zero exit is a blocking
  finding — quote the finding codes in your review.
- **The decision rule was written before results.** If it references an observed
  number, it was written afterwards. That is HARKing, and it invalidates the
  inferential claim regardless of how the analysis is done.
- **Power arithmetic is present and satisfied** for any experiment. Not "we'll
  run it for two weeks" — a planned per-arm sample that meets what the declared
  MDE requires.
- **The identification strategy matches the claim strength.** A causal claim
  from observational data needs a named strategy and its assumptions declared.
- **Tasks are checkable.** Each analytical task should end in an artefact a later
  claim can point at.
</dsx_plan_review>
