# HUMAN-QUEUE — items only you can answer

Milestone **v2.6 Exploration Depth and Backlog Evidence**. The loop keeps working
around these; it only blocks at the close-out stage (S7-2) if any remain.

**How to answer:** the operator is usually remote and cannot run local commands.
Answer in the session; an interactive Claude session records the verdict in the
proper GSD artifact (UAT file, SECURITY.md) and checks the item off here.

**What reaches this queue** (brief §4 — everything else the loop decides itself via
a persona round and records loudly):

1. A D-05 primary-source read — citation authenticity. The loop may prepare the
   evidence pack; it may not sign it.
2. An irreversible destructive operation (file deletion, history rewrite, force-moving
   a published tag).
3. A change to milestone scope (dropping or rewording a requirement).
4. A security sign-off (`SECURITY.md` approval line).
5. An outward-facing ship action (merge to `main`, release tag, opening a PR).

## Open

### HQ-40 — v2.6 D-05 citation evidence pack (filed 2026-09-06 by S0-3; UNSIGNED — needs a human primary-source read)

**What this is.** The loop PREPARED the evidence for every citation a v2.6 minted
check would carry. Per D-05 the loop may prepare but **must not sign** — a citation
is authentic only when a human confirms it *at its locator*. Until then each row's
primary-source claim is UNVERIFIED. **Non-blocking for Phases 25–26.** Blocks: the
Hyndman & Fan row blocks nothing gate-side (it is a definition test, not a mint) but
Phase 25's plan must pin the type; the Kaufman row blocks **S3-1** (Phase 27); the
Wilkinson/JARS row blocks **S4-1** (Phase 28); the Gail & Simon row blocks **S5-1**
(Phase 29). A row answered in isolation unblocks only its phase.

**How to answer.** For each row, read the cited locator and mark the primary-source
claim **CONFIRMED** (optionally correcting the locator/wording) or **REJECTED** (the
source does not state the claim → the phase falls back to the structural criterion
alone with the citation demoted to context, or mints nothing). An interactive Claude
session then records the verdict in the phase's docstring `# D-05:` marker and
`_D05_ALLOWLIST_CODES`, and checks this item off.

| # | Citation (as the code will render it) | Locator to read | Exact claim the code cites | Confirmed by the loop (secondary / mechanical) | UNVERIFIED — needs your read |
|---|---|---|---|---|---|
| 40a | Hyndman, R. J. & Fan, Y. (1996). *Sample Quantiles in Statistical Packages.* The American Statistician **50(4)**: 361–365. | The paper's Table 1 / the nine sample-quantile type definitions; and CPython docs for `statistics.quantiles` (Python 3.12). | `statistics.quantiles(method='exclusive')` (the stdlib default the profiler uses) computes the Hyndman & Fan **type 6** sample quantile; `method='inclusive'` computes **type 7**. Phase 25 pins whichever it uses (default = exclusive = type 6). | On Python 3.12.10, `quantiles([1..10], n=4)` = `[2.75, 5.5, 8.25]` (exclusive) and `[3.25, 5.5, 7.75]` (inclusive) — reproducible reference values; the CPython docs describe "exclusive"/"inclusive" **without naming an H&F type number**. | That "exclusive = type 6" and "inclusive = type 7" **in the Hyndman & Fan (1996) taxonomy** — the paper's own type numbering. The docs do not assert it; only the paper does. Confirm the type number the profiler's method maps to. |
| 40b | Kaufman, S., Rosset, S., Perlich, C. & Stitelman, O. (2012). *Leakage in Data Mining: Formulation, Detection, and Avoidance.* ACM TKDD **6(4)**, Article 15. | The TKDD 6(4) article 15 front matter (author list) + its *legitimacy* definition. | A feature is **legitimate** for a prediction iff its value would be available at the moment of prediction; a feature whose value depends on the outcome window is a leak regardless of its name. (Phase 27's `feature_provenance` / `available_at` check enforces exactly this as a declaration.) | `references/leakage-taxonomy.md` already states this rule in DSX's own words; `LEAKAGE_PATTERNS` (10 name patterns) demonstrably does **not** catch a pre-joined innocuously-named column — the gap the citation attaches a primary source to. | The **author list and year at the TKDD locator** (the 2011 KDD conference version and the 2012 TKDD journal version differ — the code must cite the one actually read), and that the legitimacy condition is stated as above in that source. |
| 40c | Wilkinson, L. & the Task Force on Statistical Inference (1999). *Statistical Methods in Psychology Journals: Guidelines and Explanations.* American Psychologist **54(8)**: 594–604. | The "Effect Sizes" / results-reporting guidance section. | Primary results must report an effect-size magnitude and its interval, not significance alone — the operational basis for requiring a claimed magnitude to trace to a computed test (Phase 28). | DSX already enforces the adjacent rule (`DSX-STA-012` fires on a reported test with no effect size); Phase 28's check is the text-to-declared-number overlap (`DSX-REP-061` precedent), not a recomputation. | **Which of the two candidates states the *operational* rule** the check enforces (this one **or** 40d), read at the locator. If neither states it operationally, record that and the check falls back to the structural criterion with the citation as context. |
| 40d | Appelbaum, M. et al. (2018). *Journal Article Reporting Standards for Quantitative Research in Psychology (APA JARS–Quant).* American Psychologist **73(1)**: 3–25. | The JARS–Quant reporting tables for inferential results. | Every reported inferential claim must be accompanied by the estimate, its precision (interval), and the test it derives from. | Same as 40c — the DSX mechanism is a declared cross-reference, not a computed test. | The **author list** and whether JARS–Quant, rather than 40c, is the cleaner locator for the operational rule. Pick exactly one of 40c/40d for the minted code (or neither → structural-only). |
| 40e | Gail, M. & Simon, R. (1985). *Testing for Qualitative Interactions between Treatment Effects and Patient Subsets.* Biometrics **41(2)**: 361–372. | The definition of a *qualitative* (crossover) interaction. | A **qualitative interaction** exists when a treatment's effect is of **opposite sign** across pre-declared subsets — the published definition of "this subgroup is harmed while the average benefits" (Phase 29's `subgroup_harm` declaration criterion). | `dsx/checks/metrics.py` confirms `DSX-MET-030/031` fire only when ALL / ≥HALF of segments oppose the aggregate, so a single minority segment (1-of-4) is structurally uncaught today — the real gap Phase 29 measures. The **test statistic itself is never computed on the gate path** (D-02); only the definition is enforced as a declaration. | That Gail & Simon (1985) **states the opposite-sign-across-subsets definition** at this locator, and the author list / pages. |

**Scope note.** The Phase 29 *documented public case* where an average benefit masked
subgroup harm (REQ-P29-02) is a **Phase 29 research deliverable**, not part of this
pack; if research finds a case whose authenticity needs a human read, that arrives as
a separate queue item at S5-2. "Not found" is a valid, recorded outcome.

### HQ-41 — Phase 25 end-of-phase sign-off: security + UAT (filed 2026-09-07 by S1-5; non-blocking until S7-2)

**What this is.** Phase 25 (Hermetic profile depth) passed both verify:post gates
technically; two items need the operator's sign-off at close-out (S7-2), neither
blocking any earlier work.

1. **Security sign-off (SECURITY.md approval line — brief §4.4).** The loop re-gated
   all 8 threats at their code locators → **SECURED, `threats_open: 0`, 8/8 CLOSED**
   (`25-SECURITY.md`, `status: verified` technical). The Approval line is written but
   **unsigned** — the loop verifies mitigations, it does not sign. **To answer:** read
   `25-SECURITY.md`; confirm the register + the HIGH threat T-25-07 closure; approve.
2. **UAT round.** `25-VALIDATION.md` is `nyquist_compliant: true`, 0 gaps, all 3
   requirements COVERED by named tests (phase module 51/51 green on real 3.12.10).
   Phase 25 has no user-facing runtime behaviour beyond the CLI flags already tested,
   so its acceptance test IS the automated invariant set. **To answer:** confirm UAT
   accepted (or name a manual check to run).

An interactive session records both verdicts in the proper artifacts (SECURITY.md
Approval line; a UAT note) and checks this item off. **Non-blocking until S7-2.**

## Will be added by the loop when reached

- ~~S0-3: the v2.6 D-05 citation evidence pack~~ — **FILED as HQ-40 (2026-09-06)**,
  see Open above. Non-blocking for Phases 25–26; the Kaufman/Wilkinson-or-JARS/Gail
  rows block S3-1, S4-1 and S5-1 respectively.
- Phase 25/26/27/28/29/30 end-of-phase security sign-off + UAT rounds (batched per
  phase; non-blocking until S7-2). **Phase 25 filed as HQ-41 (2026-09-07).**
- D-06 numbering veto windows for any code Phases 27–29 mint, and for any number
  reserved in `_SECTION_65_BACKLOG_CODES` for a miss sidecar (from a freshly
  re-measured live catalogue count; silence = accept).
- Phase 29's documented subgroup-harm case source, if research finds one whose
  authenticity needs a human read.
- The S7-6 ship decisions: merge to `main` and the `v2.6.0` release tag, together
  with the S7-5 interactive-complete step, after S7-4's audit PASSES.
- Any persona decision the operator vetoes from a daily summary.

## Standing framework notes (not queue items — nothing to answer, just remember)

**`/gsd-audit-uat`'s automated CLI under-reports human-verification items —
multiple documented defects.** (1) `gsd-core/bin/lib/uat.cjs::parseVerificationItems`
only recognizes a level-2 `## Human Verification` heading while the verifier
template writes level-3 `### Human Verification Required` (found v2.0.0).
(2) `uat.cjs:78` filters on `f.includes('-VERIFICATION')`, which matches this
project's `NN-VERIFICATION.md` naming but not a bare `VERIFICATION.md` — check
which convention the current milestone's phases use before trusting the CLI's
file discovery. (3) The frontmatter-status gate only emits a verification file
when `status ∈ {human_needed, gaps_found}`; a phase whose VERIFICATION.md
carries `verdict: PASSED` with no `status:` key resolves to `status:unknown`
and is silently dropped (found v2.3 S5-1). **At S7-1, never accept the CLI's
"all clear" — hand-check every phase's verification file directly.**

**`check.decision-coverage-plan` false-blocks on this project's CONTEXT.md
decision-bullet style (found v2.3 S1-2).** The plan-phase decision-coverage
gate's regexes expect `- **D-NN:** …` (colon-immediate) or an em-dash inside
the bold; this project's discuss rounds write `- **D-06 range
pre-allocation** — one …` (title inside the bold, separator after the closing
`**`), matching none of the regexes → `total:0, reason:"could-not-parse"`. This
is a parser format-mismatch, **not** an uncovered decision — the
`gsd-plan-checker`'s Dimension-7 (Context Compliance) substantively verifies the
same property. **At every phase plan gate, do NOT treat a could-not-parse/
total:0 result as a real coverage gap** — confirm via the plan-checker Dim-7
pass instead.

**`init.manager`'s `verification_status` can read "missing" for a genuinely
verified phase (found v2.3 close-out; confirmed again at v2.4's).** Same class of
naming-convention blind spot as the audit-uat issues, on a different code path. If
it happens again, read the actual verification file directly before treating it as
a real gap.

**`/gsd-pr-branch` does not survive a long ceremony branch.** Its per-commit
cherry-pick chain hit recurring modify/delete conflicts on v2.0.0's 707-commit
branch and was abandoned mid-run. Ship by direct 3-way merge.

**Ship by EXPLICIT branch name — never the framework's auto-detect.** This repo
now carries six stale `gsd/*` branches from prior milestones (`v1.1.0-milestone`,
`v2.0.0-dsx-validity-frame`, `v2.0.0-milestone`, `v2.2.0-analytic-surface`,
`v2.3.0-test-catalog`, `v2.4.0-visual-excellence`); `/gsd-complete-milestone`'s
`handle_branches` picks the alphabetically-first `gsd/*` branch, which is always
wrong here (found and bypassed at v2.2, v2.3 and v2.4 ship).
`git merge --no-ff gsd/v2.6.0-exploration-depth` by name, verified on a throwaway
branch first.

**`gsd-tools query commit` (used by GSD planner/researcher/executor subagents)
auto-creates the wrong branch mid-run — recurring, budget for it.** Confirmed
three times in v2.4: when a `gsd-*` subagent commits via `gsd-tools query commit`,
it can create + switch to a stray branch (v2.4's was `gsd/v2.4-visual-excellence`,
**no `.0`**) and land the commit there instead of the canonical branch; the
subagent's own return then confidently **misreports** the branch/push state.
**After ANY subagent that may commit, the orchestrator must reconcile against the
repo, not the report:** `git rev-parse --abbrev-ref HEAD` + `git branch -vv`; if a
stray branch holds the work, it is a linear descendant of canonical →
`git checkout` canonical → `git merge --ff-only <stray>` (no commit lost) →
`git branch -d`/`-D` the stray → push; verify tree-hash identity /
`git merge-base --is-ancestor` before deleting. This is exactly why the loop uses
plain `git commit` for orchestrator-authored files, and why the `gsd/*` count must
be re-asserted (6 stale + 1 active) every planning firing.

**Release tags: never force-move a published one.** v2.0.0 shipped as tag
`v2.1.0` for this reason; v2.2 as `v2.2.0`; v2.3 as `v2.3.0`; v2.4 as `v2.4.0`;
`v2.4.1` and `v2.5.0` were interactive releases. The next free tag for this
milestone is `v2.6.0`.

**`/gsd-complete-milestone` output needs hand-verification — recurring at every
close so far.** At v2.2's, v2.3's and v2.4's close, its generated accomplishment
bullets were truncated mid-sentence or captured YAML frontmatter instead of
prose, STATE.md's generated body contradicted its own frontmatter, and the
archived REQUIREMENTS.md carried all rows forward still unchecked despite the
passed audit — all needed hand-correction each time. Budget for this as a standing
cost, not a surprise. Also: it is NOT headless-safe (interactive prompts +
`git rm REQUIREMENTS.md`) — interactive session only.

**Run the full suite from a clean tree, on the real interpreter.** A stray root
`DECISIONS.jsonl` false-fails two `explain` tests
(`tests/test_dsx.py::test_explain_missing_spec_exits_zero_not_two`,
`tests/test_explain_self_reported.py::test_returns_zero_when_spec_cannot_be_loaded`);
if exactly these two fail: `rm -f DECISIONS.jsonl examples/DECISIONS.jsonl
examples/known-bad/DECISIONS.jsonl templates/DECISIONS.jsonl` and re-run. A bare
`python3` on this machine can resolve to a package-less stub (Python 3.14.6) that
reports the matplotlib determinism test as *skipped*; the real interpreter is
`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`.

**`node install.mjs --check` is now a real gate (fixed in v2.5.0).** Before
2026-09-06 its self-test ran `gate ship` alone and had failed on every fresh install
since Phase 10, and the installer shipped the gitignored `examples/DECISIONS.jsonl`
into the overlay; both fixed. Installed skill/agent copies had silently drifted
from the repo for two weeks. Every phase that touches `skills/`, `agents/`,
`templates/` or `references/` ends with `node install.mjs` and a passing `--check`.

**Usage-limit backoff is the wrapper's job — proven working in production.**
`scripts/run-ceremony-firing.ps1` detects limit hits, writes
`.planning/loop-logs/.backoff-until`, and re-probes every 30 minutes during a
hold with one trivial `claude -p` call to catch an early release rather than
blindly waiting the full window. Firings: log one line, stop, never retry-loop,
never touch the backoff/probe-marker files. The pause switch
`.planning/loop-logs/.paused` is the operator's; the loop never creates or removes it.

**A firing that finds uncommitted, ledger-inconsistent changes at start should
hold, not act.** Confirmed working at v2.3's close: a firing found an
interactive session's in-progress `/gsd-complete-milestone` work uncommitted in
the tree and correctly left it untouched (neither committed nor discarded),
logging the observation instead. This is the correct behavior, not a bug to fix.

## Answered

### HQ-39 — v2.6 scope: open the milestone with both halves (answered 2026-09-06 — operator direction; reverses HQ-38)

**Operator verdict: "Both: EDA depth + paper evidence."** Asked after the operator
directed that the ceremony run rather than stay paused. Three options were offered
in the decision-block shape: both halves (~6 phases), EDA depth only (~3), paper
evidence only (~4). The operator chose both. Consequences, all recorded:

- **SEED-002 promoted** (Phase 25) — this reverses **HQ-38**, answered hours earlier
  the same day, which had held the seed on its unmet D-13 entry condition. The
  reversal is by operator direction with a stated reason (the portfolio work starting
  now should consume hash-bound numbers from its first phase rather than produce the
  evidence first); the seed carries both decisions in order.
- **SEED-001 E-26 promoted** (Phase 26), its entry condition likewise overridden by
  direction; E-27 … E-31 unchanged.
- **§6.5 items 7, 8, 9 get their corpus cases built and measured** (Phases 27–29)
  under the brief's D-13 rule: a case the gate already catches closes its phase with
  no mint. Nothing is promoted by this answer; only the evidence is commissioned.
- Terminal calibration re-baseline (Phase 30). Ships as `v2.6.0`.

Recorded in `.planning/research/V2.6-SCOPE.md`, `REQUIREMENTS.md`, the seeds, and
STATE.md. The v2.4 queue (HQ-27 … HQ-38) is archived at
`.planning/milestones/v2.4-HUMAN-QUEUE.md`; numbering continues from HQ-40.
