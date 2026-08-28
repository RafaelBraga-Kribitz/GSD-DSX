<dsx_execution_discipline>
Analytical phase. The spec is the contract; the code must match it.

**Rules that hold for every task:**

- **Profile before you compute.** Prefer
  `dsx profile <extract.csv> --out DATA-PROFILE.yaml --pk … --time …`. Record
  `profile_path` and `assertions` on the matching `data[]` entry. Never invent
  profile numbers — use the runner or a measured export.
- **Read `EDA.md` front-matter first when it exists** in the phase directory: it
  carries the measured grain, missingness mechanisms, leakage suspects, base-rate
  verdict and segment candidates this phase already established, and its
  `comparisons_looked_at` seeds `results.comparisons_looked_at` (add confirmatory
  looks to that count; never reset it). `stop_triggered: true` means the data
  contradicted the spec — resolve the listed `contradictions` before computing.
  No `EDA.md` → record `eda_artifact: none` and source those facts from
  `DATA-PROFILE.yaml` or declare them with `computed_by` honesty.
- **Assert, don't assume.** After every join, assert the row count matches the
  expected grain. After every filter, record how many rows it removed. Cheap
  assertions in the pipeline replace expensive debugging in the review.
- **Fit every transform inside the training fold.** Scalers, imputers, encoders,
  feature selectors, resamplers. Fitting on the full dataset leaks test
  statistics into training and never raises an error. `dsx check code` scans the
  entrypoint for fit-before-split (`DSX-CODE-*`) at execute.
- **Set the seed everywhere.** The language RNG, numpy, and the framework each
  have their own. An unseeded result cannot be confirmed or refuted.
- **Fill `results:` in ANALYSIS-SPEC.yaml as you go** — observed sample sizes,
  effect estimates, intervals, train and test scores, how many times the test set
  was touched, how many interim looks were taken. The verify gate reads this
  block. Recording an inconvenient number is the point; omitting it is how a
  guardrail gets silently disabled.
- **Report the effect and its interval, never a bare p-value.** The p-value is
  the least informative number in the output.
- **Warehouse metrics need SQL.** A `source` of `warehouse.*` / `dbt.*` /
  `catalog.schema.table` without `sql:` fails `DSX-MET-040`.
- **Prefer a `scripts/*.py` entrypoint over a notebook** for
  `reproducibility.entrypoint`. A notebook entrypoint fires `DSX-REP-040` HIGH
  unless it is confirmed to run clean top-to-bottom, whose own remedy is to move
  the logic into a module the notebook imports; and the `DSX-CODE` fit-order scan
  reads `.py` source directly, where a saved `.ipynb` offers only reconstructed
  cell offsets a reader cannot usefully open. The benefit is ordering fidelity — a
  linear `.py` makes `reproducibility.entrypoint` a faithful record of execution
  order, not an out-of-order cell counter. This is NOT a leakage claim: the
  deterministic `dsx check code` gate stays suffix-neutral, reading `.py` and
  `.ipynb` identically and blocking no notebook.

**Stop and escalate rather than working around:**

- Sample ratio mismatch. Do not read the results — find the assignment defect.
- A metric that will not reconcile across sources. Reconcile first; publishing
  two versions of one number costs more than the delay.
- A model that does not beat its baseline. That is a finding to report, not a
  problem to hide behind more feature engineering.
- Fit-before-split in the entrypoint. Fix the order before arguing with the
  ML auditor.

Run `dsx gate execute --phase-dir <phase>` before declaring the phase complete.
</dsx_execution_discipline>
