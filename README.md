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

### The entrypoint leak scan now parses your code

Phase 11.1.1 changed how `DSX-CODE-001` and `DSX-CODE-021` (fit-before-split
and fit-after-split-on-the-wrong-frame) decide what a line of your entrypoint
means. The scan used to read the file as plain text, matching patterns
against each physical line's characters in turn. It now reads the file as
Python — using the standard library's abstract syntax tree (AST), the same
structure a compiler builds before running your code — and looks directly at
which function calls exist and what they are called on. When a file cannot
be parsed as Python, the scan falls back to the old text-matching approach,
and it says so on every finding it produces from that fallback.

**Some files that are blocked today will start passing — read this part
first, because nobody files a bug about a gate that stopped complaining.**
A module, class or function docstring that merely mentions a fit call —
for example a comment reading "we never call `scaler.fit(X)` on the full
frame" — used to block at CRITICAL severity, because the old scan matched
the text of the sentence, not the code. It no longer does, because a
docstring holds no function call for the new scan to find. The same is true
of a Jupyter notebook markdown cell that describes a leakage rule in prose.
Both were false alarms, and both are now fixed. In the same breath: code
assembled as a string and run with Python's `exec` or `eval` functions used
to be blocked — the old text scan could see the fit call written inside the
string — and it is **not** blocked after this change, because a string is
just data to a real Python parser, not a function call. This is a genuine
leak the new scan cannot see, and it belongs here rather than buried in the
limits section below.

This phase closes three more false alarms of the same shape, for three
different checks — read this part first too, for the same reason as above.
A module, class or function docstring, a bare string statement, or the
interior lines of a multi-line string — writing that merely *describes* a
full-frame cleaning idiom rather than performing one, for example a
sentence saying the file deliberately avoids filling missing values with a
column's average before splitting — used to block at CRITICAL severity
under `DSX-CODE-020`. It no longer does, for the same reason as the
docstring case above: the sentence describes the operation, and the
executable code never actually calls it. The same is true of `DSX-CODE-030`
(CRITICAL) and `DSX-CODE-031` (HIGH) when the prose mentions a
statistical-test call on the column your model targets. A second, related
shape closes alongside these three: `DSX-CODE-030` and `DSX-CODE-031`
decide whether a statistical-test call is about your target column by
checking whether that call's own line, or one of the three lines
immediately above it, mentions the target column's name. A mention of the
target column that appears only inside a docstring or a bare string
statement in that three-line window no longer counts — so a real
statistical-test call sitting a few lines below an explanatory sentence
stops being blocked on the strength of that sentence alone. Say this
plainly, for all four of these: in every case the executable code never
performed the operation the prose sentence described, so removing the
block is a corrected false alarm, not a weakened check. A file blocked
yesterday for any of these reasons can pass today.

**Some files that pass today will start failing, and every one of those new
findings is a true positive** — the leak was always in the file, and the old
scan could not see it. The shapes a reader can match against their own code:
a space or a tab before the opening parenthesis (`model.fit (df)`); a fit
call split across two lines by a trailing backslash or by an open
parenthesis; a fit call written with a keyword argument, such as
`model.fit(X=data, y=target)`; a second fit call on a line that also has a
safe first one, joined by a semicolon; a fit call whose argument is itself
another function call (`model.fit(loader.get_full_frame())`); and
`model.partial_fit(data)` written after the split, which used to draw
nothing there even though the same call before the split already blocked.

One more true positive belongs in this list, narrower than the rest because
it applies only on the FALLBACK path — the weaker text scan that runs when
a file cannot be parsed as Python at all. A fit call whose recognised
training-frame keyword arrives after another keyword — `model.fit(y=y_train,
X=full_frame)`, or the same call with several unrelated keywords in front of
the frame keyword — used to draw nothing there, even though the identical
call already blocked on the path that reads the file as real Python. It
blocks on the fallback now too. This is a true positive, not a new rule: the
leak was always in the file, and the parser-based path already caught it —
only the weaker fallback scan changed to agree with it. This matters only
for the files that reach the fallback in the first place — files that
cannot be parsed as Python at all, for example a genuine syntax error or an
unrepaired notebook command — so a file that parses cleanly is unaffected by
this particular fix.

There is also a substitution worth naming plainly, rather than filing it
under "stricter": a train/test split marker that appears only as a string
literal, or is reached only through an alias or a helper function imported
from elsewhere, no longer counts as a declared split. A file built that way
may now draw `DSX-CODE-001` or `DSX-CODE-010` where it used to draw
`DSX-CODE-021` instead. Where that happens, `DSX-CODE-010`'s own wording —
"entrypoint has no declared split marker" — can be false for a file that
plainly contains one; this document says so here because a finding's own
text is not the place to discover a contradiction.

The reported line number follows one rule: it is the physical line on which
the fit call's expression *begins*. For a call spread across several
physical lines, the reported line can move earlier than a per-line scan
would have reported it, and never later. No finding that fired before this
change stops firing because of that rule.

Two smaller, cosmetic changes. First, when a `DSX-CODE-021` finding quotes
the argument you fitted on, a token written with double quotes is now
rendered with single quotes (`data[["Age"]]` becomes `data[['Age']]`); the
verdict is unaffected, only the punctuation in the quoted text. Second,
every report now carries one extra line naming which scan path ran — even
the project's own clean example gains this line, which is a visible,
intended change to that fixture's output, not an accident.

One more change belongs here, stated plainly rather than as a footnote,
because it changes what a caller sees rather than what the scan catches. A
Jupyter notebook file can be valid JSON and still not be a notebook — for
example, the two characters `[]`, or a document whose list of cells
contains something that is not itself an object. Before this phase, a file
shaped like that crashed the whole run: a raw Python error and exit code 1
— the same number the gate uses to mean "this file was scanned and
blocked." A caller reading only the exit code could not tell a genuine
leak apart from a notebook the tool never managed to read at all. It is now
reported as NOT scanned, the same outcome the tool already gives a file it
cannot open at all, so the exit code and the report both say what actually
happened.

When a file cannot be parsed as Python at all — a syntax error, an
unsupported construct, or a file that is not really Python — the weaker,
older text scan runs in its place, and every finding it produces says so in
its own detail text, in the report's summary of what passed, and in the
recorded decision for that run. A clean result from the fallback scan is
weaker evidence than a clean result from the parser, and the tool now tells
you which one you got, rather than leaving you to guess.

If a new finding appears in your file, the fix has not changed: split the
data first, then fit only on the training fold — the same remedy the
finding itself already prints.

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

### What the entrypoint scan does not catch

A clean run of the entrypoint leak scan (`DSX-CODE-001`, `DSX-CODE-021` and
their siblings) is evidence that these particular shapes were not found in
your file. It is not evidence that the file does not leak, and no sentence
anywhere in this project should be read the other way — including the fact
that the scan now uses a real Python parser. Parsing your code means the
scan resolves the *structure* of a function call correctly; it does not mean
the scan understands what your code does at runtime, and the forms below are
real leaks, or real blind spots, that this change does not close.

The scan works by reading the one file you declared as your entrypoint,
looking for calls it recognises by name, and reasoning about which of those
calls happen before or after a declared train/test split. Every limit below
follows from one of three narrower facts: a function call whose target it
cannot resolve to a name, an argument shape it does not read, or a file it
never opens.

**A call the scan cannot resolve to a name.** Python lets you call a
function through a level of indirection the scan does not follow. Dynamic
dispatch — calling `getattr(model, "fit")(data)`, or looking a function up
in a dictionary with `handlers["fit"](data)` — draws nothing, because
neither shape is a direct call to something named `fit`. A bound method held
in a variable is the same problem in a different shape: `f = model.fit`
followed later by `f(data)` draws nothing either, because by the time `f` is
called, the scan has already lost the connection to `model.fit`. A fit call
performed inside a helper function or a module the entrypoint imports is
invisible for the same underlying reason — only the one declared entrypoint
file is read. And a train/test split performed through an alias or through
an imported helper function, rather than a direct call the scan recognises
by name, is read as if the file never split at all; the fit calls after it
can then be misclassified as fit-before-split.

**An argument shape the scan does not read.** `DSX-CODE-021` looks for a
recognised training-frame name — one that starts with something like
`X_train` or `train_df`, kept in the `TRAINING_FRAME_NAMES` list — as the
first argument to a fit call made at or after the split. A keyword whose
name is outside the small set the scan recognises, such as
`model.fit(training_frame=data)`, draws nothing: this is a deliberate trade,
accepting one kind of miss in exchange for never mistaking an unrelated
keyword's value for the frame you fitted on. A starred first argument —
`model.fit(*args)` — is skipped rather than resolved, for the same reason. A
full, unsplit frame renamed to something that merely *looks* like a training
frame — `X_train_like = data` followed by `model.fit(X_train_like)` — passes,
because the check matches the variable's name against the recognised list
and never follows the assignment back to what the name actually refers to;
this is a laundered name, and it is a real leak the scan cannot see.

**A file the scan never opens.** Only your declared entrypoint is read.
Anything that exists only while your code is running — source assembled as
a string and executed with `exec` or `eval`, code generated at runtime, or a
data frame mutated between the split and the fit — cannot be seen by a tool
that reads a file rather than running one. This is worth restating plainly
because it changed direction in this phase: `exec`-assembled fit-shaped
source used to be blocked by the old text scan (which could see the fit
call's text sitting inside the string literal) and is not blocked now — see
the announcement above.

**What the fallback text scan additionally misses, and when it runs.** When
a file cannot be parsed as Python — a syntax error, an unrepaired notebook
magic command, or genuinely non-Python content — the scan falls back to the
older, per-physical-line text match, and every finding produced that way
says so. The fallback cannot see a fit call split across a backslash-
continued line; it cannot resolve an argument that is itself a function
call; and every text guard in this module checks only for a comment that
*starts* a line, so a trailing comment on an otherwise real line of code
still reaches the pattern match. Concretely: `z = 1  # scaler.fit(data)` on
the fallback path still blocks at CRITICAL, even though the fit call lives
entirely inside a comment — a persisting false positive on that one path
that this phase did not close, named here rather than left for a user to
discover on their own.

The fallback's keyword-order fix, announced above, has its own stated edge.
It resolves a recognised training-frame keyword arriving after up to eight
other, non-recognised keyword arguments in the same call. A call whose
recognised keyword arrives after more than eight others still draws nothing
on the fallback, even though the path that reads the file as real Python
still catches it — a bound, not an oversight, and pinned by this project's
own tests so a future change cannot silently narrow or widen it without
someone noticing.

The docstring and prose fixes announced above, for `DSX-CODE-020`,
`DSX-CODE-030` and `DSX-CODE-031`, apply only on the path that reads the
file as real Python. The fallback has no parsed structure to build that
mask from, so on the fallback the mask is empty, and a docstring or a bare
string statement describing a cleaning idiom, or mentioning a
statistical-test call on the target column, still blocks `DSX-CODE-020`,
`DSX-CODE-030` and `DSX-CODE-031` there — the same false alarm this phase
just closed on the other path, still open on this one. This is the honest
residue of that fix, not a separate limit.

The prose mask that closes those three false alarms has a boundary worth
stating on its own, because it becomes visible for `DSX-CODE-020` for the
first time here. The mask covers a whole bare string statement and the
strictly interior lines of a multi-line string, but it deliberately spares
the opening line and the closing line of a multi-line string, because
either one can carry real code alongside the quotation marks. A full-frame
cleaning idiom written on the same physical line as a multi-line string's
opening quote — or its closing quote — therefore still fires
`DSX-CODE-020`. The sparing is deliberate, and it buys one specific
guarantee: the mask never hides a line that also carries executable code.

Two related limits stay open on the primary (non-fallback) text checks
that never moved to the parser and were never given the prose mask at all:
`DSX-CODE-002` (scaler fitted on the full frame) and `DSX-CODE-003` (a
resampler such as SMOTE named before the split) still match a comment that
merely *mentions* the pattern they look for — `# StandardScaler().fit_transform(X)`
still blocks `DSX-CODE-002`, and `# never use SMOTE before the split` still
blocks `DSX-CODE-003`. This is a different defect from the mask described
above, not a smaller version of it: `DSX-CODE-002` and `DSX-CODE-003` have
no leading-comment guard in their text loops at all, so even a single
leading `#` does not spare them, while `DSX-CODE-020`, `DSX-CODE-030` and
`DSX-CODE-031` do have the mask now on the path that reads the file as real
Python, and lose it only on the fallback described above. Closing the
`DSX-CODE-002` / `DSX-CODE-003` gap was outside this remediation's scope,
and it stays open. Notebooks reach the fallback more often than plain
Python files do, because an introspection line such as `df.head?` does not
parse and is not repaired.

**The notebook line-number convention is a standing limit, not a fix.** For
a Jupyter notebook, the "Line N" a finding reports counts lines in the
reconstructed concatenation of the notebook's code cells — with each
markdown cell replaced by a matching number of blank lines so that code-cell
line numbers do not shift — not the line of the raw `.ipynb` file on disk,
which a reader could not usefully open at that offset in either case. This
change preserves that numbering exactly; it does not attempt to fix it.

**The interpreter you run the scan with is now part of the answer.** The
scan accepts whatever version of the Python language grammar the running
interpreter accepts. A file using newer syntax can take the parser path on
one machine and the weaker fallback path on another, for byte-identical
input. This is disclosed in the tool's recorded decisions rather than left
for someone to discover by getting two different answers on two machines.

**Where these numbers come from, and why two of them are never compared
directly.** This phase's own before-and-after count of leaky-call variants
is a committed, runnable test — not a number asserted in prose — and is the
figure this document stands behind. A second, earlier count exists in
[`11.1.1-RESEARCH.md`](.planning/phases/11.1.1-detection-code-hardening-inserted/11.1.1-RESEARCH.md):
thirteen variants, six caught and seven missed, measured on 2026-08-21
against only the `DSX-CODE-021` argument-extraction path — a narrower
instrument than the end-to-end count above, and cited here as the
before-figure for that one path, not as a second reading of the same thing.
An older, uncommitted figure circulated during an earlier verification
session and has no committed enumeration behind it anywhere in this
repository; it is not repeated here, and is not printed alongside either of
the two figures above.

None of this makes `DSX-CODE-001`, `DSX-CODE-021`, or any other
`DSX-CODE-*` check sound, complete or exhaustive. Treat a clean scan as
one input to your own judgement, not as a verdict.

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
