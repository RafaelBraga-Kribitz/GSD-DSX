# gsd-dsx

**Data science, analytics and BI rigour for [GSD Core](https://github.com/open-gsd/gsd-core).**

A capability overlay that specialises the GSD phase loop for analytical work. It
installs alongside `gsd-core` — no fork, no patched workflows — and survives every
upstream release.

---

## The idea

GSD solves context rot by running heavy work in fresh subagents against structured
artifacts. That machinery is domain-agnostic. What it does not know is that a
random train/test split on time-ordered data invalidates the model, that three
metrics tested at α = 0.05 carry a 14% family-wise error rate, or that a bar chart
starting at 40 exaggerates whatever it shows.

`gsd-dsx` supplies that knowledge — and, critically, supplies it as **code that
runs in blocking gates** rather than as advice in a prompt.

### Where the determinism goes

The split is deliberate and it is the whole design:

| | Stochastic (agent judgement) | Deterministic (code) |
|---|---|---|
| **What** | Filling `ANALYSIS-SPEC.yaml` — framing the question, choosing the design, defining the metric, writing the claim | Checking the spec is coherent and that the produced artifacts satisfy it |
| **Why** | These need context, domain knowledge and conversation with a human | These are decidable, and a decidable check should never be delegated to a model |

An agent decides that this is a causal question needing a difference-in-differences
design. Code then verifies that parallel-trends evidence was declared, that the
claim's verb matches the design's strength, that the sample meets the power the
declared MDE requires, and that no feature in the model is populated after the
outcome. The agent stays flexible; the output stops being a matter of opinion.

**Finding codes** across check families (contract, experiment, causal, stats, ML,
metrics/SQL, claims, narrative, code, decision, data quality, coherence,
visualization, reproducibility), each with a stable identifier, a severity,
evidence in numbers, and a concrete fix.

---

## Install

```bash
git clone https://github.com/RafaelBraga-Kribitz/GSD-DSX.git
cd gsd-dsx
node install.mjs                 # --runtime cursor|codex|opencode|... , --local
```

Requires GSD Core ≥ 1.6 and Python 3.9+. **No third-party Python packages** — the
statistics kernel is stdlib-only, because a gate that breaks on a missing
dependency is a gate that gets turned off.

The installer runs a self-test: it asserts the known-good fixture passes every
gate and the known-bad fixture is blocked by every gate. If either fails, the
install aborts.

```bash
node install.mjs --check         # verify an existing install
node install.mjs --uninstall
```

---

## What it adds to the loop

```
  discuss ──▶ plan ──────▶ execute ──────▶ verify ──────▶ ship
               │             │               │              │
        ┌──────┴──────┐      │        ┌──────┴──────┐       │
        │ ANALYSIS-   │      │        │ STATS-      │       │
        │ SPEC.yaml   │      │        │ REVIEW.md   │       │
        └──────┬──────┘      │        └──────┬──────┘       │
               ▼             ▼               ▼              ▼
         ✋ gate plan   ✋ gate execute  ✋ gate verify  ✋ gate ship
         blocks at        blocks at       blocks at      blocks at
         CRITICAL         CRITICAL        HIGH           HIGH
```

Each gate is a GSD `command-exit-zero` predicate running `dsx gate <point>`:
exit 0 passes, exit 1 blocks the loop with the findings in the gate message,
exit 2 routes to the gate's `onError`. A spec we judged bad stops the loop; a
spec we could not read is an operational error — the distinction matters, and
the exit codes preserve it.

**Phases with no `ANALYSIS-SPEC.yaml` pass through untouched**, so this is safe
to enable in a mixed repository. Set `dsx.require_spec true` in a pure analytics
project to make the spec mandatory.

---

## The contract

`ANALYSIS-SPEC.yaml` is the deterministic input everything else is checked
against. It is written **before the data is touched** — that is not process
theatre, it is the only thing that distinguishes a decision rule from a
rationalisation.

```yaml
question_type: causal

decision:
  owner: "VP Growth"
  decision_rule: >
    Roll out if the 95% CI lower bound on uplift exceeds +1.0pp and no
    guardrail degrades beyond its tolerance.
  action_if_null: "Keep current onboarding; close the initiative."
  minimum_practical_effect: 0.02

design:
  kind: experiment
  randomization_unit: user
  analysis_unit: user
  baseline_rate: 0.31
  mde: 0.02
  alpha: 0.05
  power: 0.80
  planned_n_per_arm: 9000       # dsx computes what this MUST be
  peeking_policy: fixed_horizon
  multiplicity:
    family: [activation_rate, retention_d7, revenue_per_user]
    correction: benjamini_hochberg

claims:
  - text: "The checklist increases 7-day activation by 2.4pp (95% CI 1.0–3.8)"
    type: causal                # the verb must match the design's strength
    evidence: "RESULTS.md#uplift"
    population: "New non-bot signups, 2026-06-01 to 2026-06-14"
```

Run `dsx init` to scaffold it, `dsx vocab` to see every closed vocabulary.

### Migrating a pre-v2.0.0 spec

From v2.0.0, `validity_frame:` is required starting at the `plan` gate, at
CRITICAL severity — so a spec written against v1.x begins blocking the moment
you upgrade. The supported path is to fill the frame: `estimand`, `units`,
`identification`, `dependence`, `interference`, `triggering`, `stability`,
`sampling_frame`, `missingness`, `measurement`.

The supported *interim* path is the existing `suppressions[]` mechanism (see
[Finding suppressions](#finding-suppressions) below): declare the missing-frame
findings there with a `reason` and an `authority` naming a real ADR or SPEC
file. Suppressions apply after checks and before the blocking threshold, and
an unknown code aborts the run with exit 2.

Say this plainly: a suppression is an attributable, dated decision with a
named authority, not a way to make the finding go away. A suppression with no
resolvable `authority` reference already produces `DSX-SPEC-070` — the
grandfather path is deliberate, not silent.

---

## What the gates actually catch

Real output, not a description of it:

```
$ dsx audit --spec examples/bad-ANALYSIS-SPEC.yaml

[CRITICAL] DSX-EXP-006  Experiment is underpowered: 1,200 per arm vs 47,528 required
    where:  spec.design.planned_n_per_arm
    detail: At baseline=0.08, MDE=0.005, alpha=0.05, the target power of 0.80
            needs 47,528 per arm. The plan is 97% short, delivering only 0.06
            power. The smallest effect actually detectable at 1,200 per arm is
            0.03382, which is 6.8x the declared MDE.
    fix:    Raise planned_n_per_arm to 47,528, raise the MDE to 0.03382, or
            extend the run until the sample is reached. Do not proceed and
            reinterpret a null as evidence of no effect.
```

That number is computed, not asserted. The same is true of the SRM chi-square,
the peeking-inflated α, the Benjamini-Hochberg adjustment, and the reconciliation
gap.

### The check families

| Family | Codes | Catches |
|---|---|---|
| **Contract** | `DSX-SPEC-*` | Missing decision rule, undefined denominators, duplicate metric names, unclassified claims |
| **Experiment** | `DSX-EXP-*` | Underpowering (computed), sample ratio mismatch (χ² tested), randomization/analysis unit mismatch, uncorrected multiplicity, peeking under a fixed-horizon design, sub-week duration, missing guardrails |
| **Causal** | `DSX-CAU-*` | Causal question with no identification strategy, strategies missing their required assumptions, weak strategies presented as strong |
| **Statistics** | `DSX-STA-*` | Test that does not match the outcome's shape, p-value with no effect size or interval, interval and p-value disagreeing, null accepted without an equivalence test, results that die under correction, significant-but-trivial effects |
| **ML integrity** | `DSX-ML-*` | Random split on temporal data, overlapping train/test periods, leaky feature names, preprocessing fitted before the split, resampling before the split, accuracy or ROC-AUC on an imbalanced target, no baseline, model losing to its baseline, train/test gap, test-set reuse, threshold tuned on test |
| **Metrics & SQL** | `DSX-MET-*` `DSX-SQL-*` | Undefined metrics in use, cross-source reconciliation beyond class/tolerance, denominator drift, Simpson's paradox, warehouse source without `sql`, join fan-out, `NOT IN` NULL traps, average-of-ratios, division without `NULLIF`, `= NULL`, `SELECT *`, `JOIN` without `ON`, `SUM(a/b)`, `BETWEEN` on timestamps |
| **Claims** | `DSX-CLM-*` | Causal verbs on an association claim, causal claims with no strategy, unhedged conclusions from weak identification, missing or unresolvable evidence pointers, claim numbers that do not overlap `results.tests`, relative `%` without a base, empty limitations on causal/prescriptive/predictive, overbroad generalisation, false precision against the interval |
| **Narrative** | `DSX-NAR-*` | Missing `narrative.path` at ship, claim text absent from deliverable, forbidden wording (`data proves`, …), relative `%` in narrative without base, missing `dashboard.path` |
| **Code reality** | `DSX-CODE-*` | Fit/transform before split, full-frame `StandardScaler().fit_transform`, SMOTE before split, model block with no split marker in entrypoint |
| **Decision replay** | `DSX-DEC-*` | Missing structured `decision.replay` at ship, metric missing from tests, replay FAIL, pass with non-significant primary p |
| **Data quality** | `DSX-DQ-*` | Assertions vs `DATA-PROFILE.yaml`: row count, PK uniqueness, null caps, time gaps, banned sentinels, manual profiles without gap notes |
| **Coherence** | `DSX-COH-*` | Claim type exceeding question type, causal decision language on descriptive questions, experiments missing MPE/`action_if_null`, empty assumptions, unchecked/unwaived assumptions |
| **Figure seals** | `DSX-FIG-*` | Missing artifacts, `svg_sha256` mismatch, unsealed paths at ship, glyph without seal, duplicate `chart_id`, FIGURE-MANIFEST coverage |
| **Plot smells** | `DSX-SMELL-*` | Dead series, density on atoms, stacked scenarios, category dropouts, self-correlation, disagreeing `run_id` |
| **Visualization** | `DSX-VIZ-*` | Truncated baselines on length-encoded charts, dual axes, chart type wrong for the relationship or data_input_type, takeaway = name, >5 pie slices, 3D, red/green as sole distinction, rainbow scales, estimates with no uncertainty, missing units |
| **Reproducibility** | `DSX-REP-*` | No seed on stochastic methods, unpinned environment, unidentifiable data extracts, missing entrypoint, notebooks not confirmed clean top-to-bottom, missing/`null`/incomplete `repro_lock` |

Full catalogue: [`references/finding-codes.md`](references/finding-codes.md) —
generated from the source, so it cannot drift from what the code emits.

---

## Agents and skills

Six specialists, each with a narrow adversarial brief:

| Agent | Role |
|---|---|
| `dsx-analysis-architect` | Turns a vague question into a checkable spec, before any data is touched |
| `dsx-statistician` | Adversarial review: magnitude, generalisation, alternative explanations |
| `dsx-ml-integrity-auditor` | Reads the pipeline code to verify it matches the spec's leakage claims |
| `dsx-metric-steward` | Definitions, reconciliation, SQL correctness |
| `dsx-viz-critic` | Encoding correctness and proportional geometry |
| `dsx-data-storyteller` | The decision-ready narrative, without outrunning the evidence |

Eight skills covering the workflow end to end: `dsx-scope-analysis`,
`dsx-explore-data`, `dsx-design-experiment`, `dsx-define-metrics`,
`dsx-build-model`, `dsx-visualize`, `dsx-chart-audit`, `dsx-narrate`,
`dsx-review-analysis`.

`dsx-chart-audit` is the standalone retroactive path: run `dsx check viz smells
figures`, spawn `dsx-viz-critic`, write scored `CHART-REVIEW.md`
(`schema: dsx-chart-review-v1`). Use when you need a figure audit without a full
experiment/ML readout.

### Finding suppressions

When a SPEC or ADR forbids the preferred fix (e.g. a mandated dual axis), declare:

```yaml
suppressions:
  - code: DSX-VIZ-030
    chart_id: a3_realized_vol
    reason: "AN-301 requires twin axes; change needs ADR"
    authority: "docs/SPEC-04_analytics.md"
```

Suppressions apply after checks and before the blocking threshold. Unknown codes
abort the run (exit 2). Missing `reason` / `authority` → `DSX-SPEC-070`.

---

## Standalone CLI

`dsx` is useful outside GSD:

```bash
dsx init                                          # scaffold a spec
dsx validate                                      # structure only
dsx audit --verbose --report DATA-REVIEW.md       # everything
dsx check ml metrics                              # a subset
dsx profile extract.csv --out DATA-PROFILE.yaml --pk user_id --time signup_at
dsx seal figures/chart.svg                            # sha256:… for visuals[].svg_sha256
dsx power --baseline 0.31 --mde 0.02              # sample size, achieved power, detectable MDE
dsx recommend-test continuous --groups 3 --normal false
dsx vocab                                         # every closed vocabulary
```

Add `--json` anywhere for machine-readable output. Exit codes are the contract:
`0` pass, `1` block, `2` could not run.

---

## Configuration

```bash
gsd config set dsx.enforce true            # master switch (default: true)
gsd config set dsx.require_spec true       # mandatory spec (default: false)
gsd config set dsx.domain experimentation  # bias agent and reference loading
```

| Key | Default | Effect |
|---|---|---|
| `dsx.enforce` | `true` | Master switch for all gates |
| `dsx.require_spec` | `false` | Fail the plan gate when a phase has no spec |
| `dsx.viz_audit` | `true` | Audit chart specs before shipping |
| `dsx.causal_guard` | `true` | Block causal wording the design does not support |
| `dsx.reproducibility_gate` | `true` | Require seed, environment, data identity, entrypoint |
| `dsx.dq_gate` | `true` | Compare `data[].assertions` to `DATA-PROFILE.yaml` |
| `dsx.figure_seal` | `true` | Require `svg_sha256` when `artifact_path` is set |
| `dsx.domain` | `auto` | `experimentation` · `machine_learning` · `business_intelligence` · `marketing_science` · `research` |
| `dsx.python` | `python3` | Interpreter for the CLI |

---

## Development

```bash
./scripts/check.sh                           # the full gate: everything below
python3 -m unittest discover -s tests -v     # 121 tests
python3 scripts/validate-capability.py       # manifest conformance
python3 scripts/gen-finding-catalogue.py --write
```

**Adding a check.** Write it in the relevant `dsx/checks/*.py` module returning
`Report` findings with a new code in that module's prefix. Add a test that proves
it fires *and* a test that proves it does not fire on the good fixture. Regenerate
the catalogue. Codes are never renumbered — a suppression written today stays
valid.

**The two fixtures are the contract.** `examples/good-ANALYSIS-SPEC.yaml` must
pass every gate at every threshold; `examples/bad-ANALYSIS-SPEC.yaml` must be
blocked by every gate. If a new check breaks the good fixture, either the check is
wrong or the fixture has a real defect. Both are worth finding out.

---

## Known limits

The gate checks declarations against declarations — **a frame that lies passes.**
The insurance against a bad question is still a human who knows the domain
reading the frame before the data is touched. What this changes is that the
review becomes cheap, structured and repeatable, so it actually happens.

This is a different failure from the one `dsx-ml-integrity-auditor` covers
(see [Design notes](#design-notes) below): that audit catches a pipeline
whose *code* misdeclares what it does. This is about a `validity_frame:`
block that is internally coherent — every sub-field filled, every closed
vocabulary respected, every cross-field check satisfied — and still false,
because nothing in the frame's shape can verify that "difference in 7-day
activation rate" was the right question to ask in the first place.

### Concurrent `dsx gate` invocations are not supported

Run `dsx gate` points against one analysis directory sequentially, not in
parallel. The per-invocation identifier in `DECISIONS.jsonl` is derived by
reading and counting existing invocation headers, and nothing locks that
read against a second process's write. Two concurrent `dsx gate` runs
against the same directory can both derive the same invocation identifier
and both append a header carrying it, merging their decision trails under
one invocation in `dsx explain`'s output. This does not affect any gate's
exit code — the trail stays a side channel — but it does corrupt the
grouping guarantee the trail is supposed to provide for that one invocation.
Serialising `dsx gate` runs against a given analysis directory is the
operator's responsibility today.

### What the declared-versus-executed reconciliation cannot see

The pre-registered inference plan check (`DSX-PRE-*`) reconciles a declared
inference plan against what actually ran. Four things about that
reconciliation are worth stating plainly, because correct code alone does
not make them obvious from the outside.

First, `declared_at`. This field records whether the operator says the
inference plan was declared before the data was observed (`pre_data`) or
after it (`post_data`). It is an operator self-declaration that the tool
cannot verify — nothing in the gate can tell a true `pre_data` claim from a
false one. Declaring `post_data` honestly is legal and produces no finding.
This is deliberate: if an honest post-hoc declaration were blocked, staying
silent about the truth would be cheaper than declaring it, and that is
exactly the incentive this project exists to avoid.

Second, the executed side. The reconciliation reads the procedure it treats
as "executed" from `analysis.test`. That field is scaffolded into the
specification at plan time, by the same template that scaffolds everything
else — so "executed" is a convention imposed by the gate point at which this
check runs, not a property the field itself carries. It is the same class of
limit as `declared_at`.

Third, the content lock. Where `dsx gate plan` has run, the reconciliation
compares a hash computed over the `validity_frame:` and `inference:` blocks
as they were recorded at that point against the same hash computed now — it
compares recorded bytes, not a declared string. The limit: nothing in the
code enforces an ordering between the four gate points (`plan`, `execute`,
`verify`, `ship`). An operator who re-runs `dsx gate plan` after seeing
results registers the edited frame and clears the check. The lock is only as
strong as the operator's discipline in not doing that. The hash also covers
only those two blocks, so an edit anywhere else in the specification does
not move it — this is change detection, not a security control.

Fourth, the missing-lock case. A `dsx gate verify` or `dsx gate ship` run
that finds no plan-time header recorded anywhere in the decision trail stops
at exit 2 — could not run — rather than passing. A specification that
legitimately predates the plan gate takes the existing `suppressions[]`
route, which requires citing the architecture decision record (ADR) or
specification that authorises it.

The declared fallback rule (`inference.fallback_rule`) may only reference a
closed set of three facts: `alpha` (read from `design.alpha`),
`comparisons_looked_at` (read from `results.comparisons_looked_at`), and
`interim_looks` (read from `results.interim_looks`). A rule naming anything
outside that set produces a finding rather than being silently ignored. The
arrow (`->`) is what makes a `fallback_rule` value a rule at all — a value
with no arrow is read as ordinary prose and left alone. `dsx vocab` emits the
same three names under `prereg_facts`, so that command is the
machine-readable source for this set rather than this paragraph.

### Two tiers of evidentiary rigour

Not every finding code in the catalogue carries the same evidentiary bar.

**Tier one — codes introduced in v2.0.0.** Every new finding code carries, in
its docstring, a `Citation:` line naming author, year, work and the exact
formulation, plus a `Reference value:` line (or `Structural criterion:` where
the check is structural rather than numeric), plus a `# D-05: <CODE>` marker
comment in `tests/` linking the code to the test that proves it fires. All
three are enforced mechanically:

```bash
python3 scripts/gen-finding-catalogue.py --check
```

**Tier two — pre-existing codes.** The finding codes that predate this rule
are carried on a finite allow-list inside `gen-finding-catalogue.py`. Many
are structural (contract shape, SQL fan-out) with no primary statistical
source to cite — forcing a citation there would manufacture exactly the fake
authority the rule exists to prevent. The allow-list is designed to shrink:
as an old code earns a citation, it comes off the list.

The `# D-05: <CODE>` test-linkage convention isn't cosmetic bookkeeping — it
is how every check family from here forward proves its citation is actually
exercised by a test, not just quoted in a comment. It binds every later
milestone phase from the moment it lands.

The `DSX-PAR-*` family's own symmetry argument — why neither the frequentist
nor the Bayesian half of its monitoring-discipline pair is cheaper to satisfy
dishonestly than the other — is committed separately at
[`references/paradigm-symmetry.md`](references/paradigm-symmetry.md).

---

## Design notes

**Why the exit codes are split three ways.** GSD maps a non-zero check-command
exit to the gate's `onError` route, and a `block: true` result to a halt. Keeping
"I judged this bad" (1) separate from "I could not run" (2) means a missing
interpreter never masquerades as a statistical verdict.

**Why the statistics are reimplemented rather than imported.** `norm_ppf`,
`chi2_sf`, the power functions and the multiplicity corrections are ~400 lines of
stdlib Python, unit-tested against published reference values. Depending on SciPy
inside a blocking gate trades a small amount of code for a large amount of
environment fragility, and the failure mode — a disabled gate — defeats the point.

**Why the spec is YAML with a bundled parser.** PyYAML is used when present;
otherwise a bundled parser covers the template's subset and is tested for parity
against PyYAML. Same reasoning as above.

**What this deliberately does not do.** It does not read your warehouse from a
gate. Data-quality checks compare declarations to a hermetic `DATA-PROFILE.yaml`
(preferably produced by `dsx profile` on a local CSV). Every other check runs
against declarations and reported results, which means gates are fast, hermetic
and safe to run anywhere — but also that a spec can lie. That is what
`dsx-ml-integrity-auditor` is for: it reads the pipeline code and verifies the
declarations match. Deterministic checks catch the errors; the audit catches the
misdeclarations.

---

MIT. Built on [GSD Core](https://github.com/open-gsd/gsd-core) by open-gsd.
