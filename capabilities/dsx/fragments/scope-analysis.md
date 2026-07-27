<dsx_scope_step>
Before planning tasks, produce `ANALYSIS-SPEC.yaml` in the phase directory.

1. Decide whether this phase is analytical at all. If it produces no number,
   model or chart, skip this step — the gates pass cleanly on phases with no
   spec.
2. If it is analytical, scaffold with `dsx init --output <phase>/ANALYSIS-SPEC.yaml`
   and fill it using the `dsx-scope-analysis` skill.
3. Validate with `dsx validate --phase-dir <phase>` and fix what it reports.

The spec is not documentation written after the fact. It is the input the rest
of the phase is checked against, so every field left at its placeholder is a
decision that has not been made yet.
</dsx_scope_step>
