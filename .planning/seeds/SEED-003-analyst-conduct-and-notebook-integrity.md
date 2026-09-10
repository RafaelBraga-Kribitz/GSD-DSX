---
id: SEED-003
status: dormant
planted: 2026-09-10
planted_during: v2.6 Phase 30 (Calibration re-baseline) — operator direction, mid-milestone
trigger_when: v2.6 ships (tag `v2.6.0`) AND a new milestone opens whose scope includes analyst conduct, notebook artifacts, or claim-quantity semantics
scope: mixed — the skill/reference items are quick tasks; the gate items are D-13 evidence phases and may only be built after a measured corpus miss. Not one unit of work.
---

# SEED-003: Analyst conduct, notebook integrity, and claim-quantity semantics

Source: an operator-supplied analyst method (`analista-senior`, written in Portuguese)
describing how to conduct an interactive Jupyter analysis — one question at a time,
short cells, a written interpretation after every result, and a critical review before
any finding becomes a conclusion. The operator's instruction was to stop carrying it as
a loose skill and bind it into DSX where each part belongs.

## The rule for reading this seed

The method is **mostly already implemented, and DSX's version is stronger** — because
DSX gates declarations while the method advises an agent. Three of its five themes are
covered by shipped machinery and must not be rebuilt. What survives splits three ways:

1. **Gate candidates** — a real, currently-invisible failure mode. Subject to D-13:
   nothing here is built until a corpus case is measured a LIVE MISS first, and a case
   the gate already catches closes with **no mint**. Each needs D-05 and D-06.
2. **Skill/reference items** — genuine craft that no gate can adjudicate. Quick tasks.
3. **Rejected** — recorded below so a future reader does not re-litigate them.

## A. Gate candidates (D-13 — entry condition, not a wish)

| id | Candidate | Why it is a real gap (verified live 2026-09-10) | Entry condition |
|---|---|---|---|
| AC-01 | **Notebook execution integrity** — read the declared `.ipynb` and check `execution_count` monotonicity, code cells with `execution_count: null` (never run), and cells whose stored `outputs[]` carry `output_type: "error"` | `DSX-REP-040` (`dsx/checks/repro.py:179-200`) reads the **self-declared boolean** `runs_clean_top_to_bottom` and never opens the notebook; the `else` branch emits `report.ok(...)` on the strength of that checkbox. Its own `remedy` text names the exact hazard — "Out-of-order execution leaves results that depend on cells no longer present... The notebook then reproduces nothing" — and then trusts a promise. `dsx/checks/code.py:1222-1290` already parses the same `.ipynb`, but reads only `cells[].source`; `execution_count`/`outputs` appear nowhere in `dsx/`. The evidence is on disk and the gate is not looking at it. | A corpus case whose notebook declares `runs_clean_top_to_bottom: true` while its own `execution_count` sequence proves otherwise, measured a LIVE MISS at all four gate points |
| AC-02 | **Share vs. risk (quantity-kind mismatch)** — a claim asserting elevated *risk* ("2.3× more likely per case") supported only by a *share of a total* ("accounts for 70% of incidents"), or the reverse | `DSX-CLM-034`'s own docstring concedes it (`dsx/checks/claims.py:506-510`): "this catches only via a STRAY claim number that lies outside the cited test — never via metric-identity. A claim whose every number happens to sit inside the one cited test still passes, **even if that test measured the wrong metric**." `supported_by` constrains digits, not the kind of quantity. `METRIC_TYPES` (`dsx/spec.py:272`) is never compared to claim wording. This is the single highest-value gap in the method: it is the error that turns a big group into a dangerous one. | A corpus case whose claim asserts per-unit risk while its only cited test computes a share of a total, every existing claims/coherence/stats check clearing at default threshold |
| AC-03 | **Base (n) beyond relative percentages** | `DSX-CLM-070` is narrower than it looks: it fires only on a **relative percentage** in claim text (`dsx/checks/claims.py:663-681`) and is discharged by `base_n`, by `from_value`+`to_value`, **or merely by base-sounding words near the number** (`dsx/pct_base.py:14-18,46`) — so prose can satisfy it. Means, counts and absolute rates are uncovered, and `results.tests[]` has no `n`/`base_n` field at all (`templates/ANALYSIS-SPEC.yaml:290-301`). | A corpus case whose headline mean or absolute rate rests on a base small enough to be noise, cleared today by the prose leg of the CLM-070 predicate |
| AC-04 | **Claim or metric naming a column absent from the data** | Only `dsx/checks/dq.py` reads `DATA-PROFILE.yaml` (`:33-64`), and its one referential check is `DSX-DQ-030` on `assertions.max_null_rate` keys (`:226-233`). No metric numerator/denominator/dimension or claim reference is mapped to `profile.columns`. Note the D-02 tension: this makes a gate depend on profiler output, which is a **separate recorded decision**, not an assumption — `DSX-DQ-030` is the only precedent. | A corpus case naming a variable the profile does not contain; **and** a recorded D-02 ruling that this class of gate may read the profile |
| AC-05 | **Cross-chart colour consistency** — one category keeps one colour across every figure in an analysis | Colour rules are strictly per-chart (`DSX-VIZ-050/051/052`, `dsx/checks/viz.py:350-372`); the only set-level check is `DSX-SMELL-013` (disagreeing `run_id`). `templates/ANALYSIS-SPEC.yaml:248` carries `palette: null` and there is no category→colour map to adjudicate. | A corpus case where a category changes colour between two figures of one analysis, plus a declared encoding map for the check to read |
| AC-06 | **Small-window fragility outside experiments** | `DSX-EXP-030/031` enforce a 7-day floor on `design.duration_days` for **experiments only** (`dsx/checks/design.py:314-340`). Nothing flags a descriptive or diagnostic finding drawn from a handful of periods. Weakest item here — likely folds into existing sample-size machinery rather than earning a code. | A corpus case where a descriptive finding on a very short window survives every current check |

### D-05 citation candidates (NOT verified — operator read required)

- **AC-01** — Pimentel, Murta, Braganholo & Freire (2019), *A Large-Scale Study About
  Quality and Reproducibility of Jupyter Notebooks*, Proc. IEEE/ACM 16th Int. Conf. on
  Mining Software Repositories (MSR '19), pp. 507–517, DOI `10.1109/MSR.2019.00077`.
  **Status: bibliography confirmed** at convergent independent sources (DBLP, ACM DL,
  the MSR 2019 programme, NYU Scholars, Semantic Scholar). **Content NOT confirmed** —
  the public abstract states only "We studied 1.4 million notebooks from GitHub... a
  detailed analysis of their characteristics that impact reproducibility"; it does not
  state the execution-order or unexecuted-cell criteria at abstract level. A body read
  at the locator is required before this may be cited, per D-05.
- **AC-02** — no candidate proposed yet. The distinction is the base-rate / denominator
  problem; the epidemiological framing (proportional mortality vs. incidence rate) and
  the judgment literature (Bar-Hillel 1980) are both plausible starting points, but
  neither has been read and neither is recorded here as a citation.

## B. Skill and reference items (no gate can adjudicate these)

| id | Item | Where it belongs |
|---|---|---|
| AC-10 | The conduct cycle — one question at a time; markdown stating intent **before** the code; run it and read the real output; a written interpretation **after**; only then choose the next question. Explicitly: do not write ten cells to run later. | `skills/dsx-explore-data/SKILL.md` — but see the open question below; the skill currently prescribes the opposite medium |
| AC-11 | Cell craft — one question per cell, most cells 1–3 lines, no comment restating the code, inspectable outputs (`.head()`/`.shape`/`.value_counts()`) never whole-frame dumps, `Series.to_frame()` for display, and every transforming cell ends by showing the affected columns | new `references/notebook-conduct.md` (no incumbent; nearest neighbours are `narrative-discipline.md` and `chart-selection.md`) |
| AC-12 | Section headings are plain business questions, not technical labels ("How many orders were delivered late?" not "Univariate analysis"); no data-science jargon for a business audience; interpret the number rather than restating it | `references/narrative-discipline.md` + `skills/dsx-narrate/SKILL.md`. Verified gap: `DSX-NAR-001…050` cover artefact path, claim presence, forbidden wording and base-for-% only. The nearest analogue is chart-only (`DSX-VIZ-060/063/064` takeaway titles) |
| AC-13 | Misparse triage immediately after `read_csv`/`read_excel` — mojibake in labels → encoding; everything in one column → separator; numbers as text/NaN → decimal and thousands; junk rows at top/bottom → `skiprows`/`skipfooter`; confirm with `shape`, `dtypes`, `head()` before analysing anything | `references/notebook-conduct.md`, cross-referenced from `dsx-explore-data` step 1. **Do not gate it** — but see AC-20 |
| AC-14 | Locale pack — PT-BR currency rendering (display only, never mutating the data) and the Jupyter hazard that `$…$` in a markdown cell renders as mathematics, so money in prose must be escaped or set in inline code | a clearly-scoped locale section of `references/notebook-conduct.md`. The repo's working language stays English; this is locale knowledge, not a second language for the codebase |
| AC-15 | Notebook continuation discipline — when extending an analysis that already ends in a conclusion, insert new question/code/interpretation cells **above** the conclusion block and then update the conclusion; if the new request is a genuinely different subject, ask whether it should be a new notebook | `references/notebook-conduct.md` |

## C. Profiler-side (producer, never a gate — D-02)

| id | Item | Note |
|---|---|---|
| AC-20 | A `parse_health` block in `dsx profile` — mojibake-suspect labels, numeric-looking columns stored as text, a single column containing delimiters, all rows landing in one column | Belongs with [[grow-data-profile-hermetic-eda-artifacts]]. The profiler may compute it freely; **any gate reading it is a separate D-02/D-06 decision**, exactly as Phase 25's new keys were |

## D. Rejected — already covered, and DSX's version is stronger

Recorded so this is not re-litigated. Rebuilding any of these would duplicate shipped
machinery with a weaker, advice-shaped version:

- **Establish the business question, the audience, and ambiguous column meanings before
  touching code.** Covered by `dsx-scope-analysis` and the `decision.owner` /
  `decision_rule` / `action_if_null` / `question_type` declarations — which are *gated*,
  not merely advised.
- **Do not assert causation without a basis.** Covered by the two-tier verb lexicon
  (`dsx/spec.py:83-92`), `DSX-CLM-010/011/020` and `DSX-COH-010`. Known boundary, already
  documented: paraphrase without a listed verb ("the reason for", "X is why Y") escapes.
- **Chart choice and honesty** — type from the relationship, bars from zero, ordered by
  value, chart junk removed, direct labels over legends. Covered by v2.4 Visual
  Excellence (`references/chart-selection.md`, `DSX-VIZ-010/012/013/020/080`,
  `chart-snippets.md`, `templates/dsx_plotstyle.py`). Only cross-chart consistency
  survives, as AC-05.
- **The analysis arc** (load → know → clean → explore one variable → cross variables →
  summarise). Covered far more deeply by `dsx-explore-data`'s fourteen steps, including
  a grain ladder, a missingness mechanism, a second-order attack, a comparisons ledger
  and a rerun contract.

## SETTLED 2026-09-10 — the medium question (operator direction)

**The conflict.** The method is notebook-native; `dsx-explore-data` prescribes the
opposite medium, verbatim (`skills/dsx-explore-data/SKILL.md:25-26`): "Write EDA as a
script, not as scattered cells. It will be re-run when the data refreshes, and a script
re-runs while a notebook session does not." `DSX-REP-040`'s remedy agrees ("Better: move
the logic into a module the notebook imports").

**Decision: two media, explicit boundary (Option A).** The operator chose this on
2026-09-10, over reversing the script-first rule.

- `dsx-explore-data` **keeps script-first** for the gated EDA artifact. The
  re-runnability argument behind that rule is the same argument the reproducibility gate
  exists to enforce; it is not weakened.
- The notebook conduct rules (AC-10, AC-11, AC-15) go into the new
  `references/notebook-conduct.md`, governing **exploratory and portfolio notebooks** —
  the medium the operator actually works in for portfolio pieces.
- **Each document must state plainly when the other applies.** A reader arriving at
  either one must learn, in that document, which medium governs their situation. A
  boundary that lives only in one of the two is a boundary that will be missed.
- No reversal entry is owed under D-14: the script-first instruction stands unchanged
  within its scope.

**Cost accepted with this choice:** every future conduct rule must be filed under one
medium or the other, and the boundary statement needs re-checking whenever either
document changes. A phase implementing AC-10/11/15 should treat "both documents still
name the boundary correctly" as an explicit verification item, not an assumption.

AC-01 was already independent of this decision and remains so: `.ipynb` is a permitted
entrypoint today, so the integrity check earns its place under either medium.

## Breadcrumbs

- `skills/dsx-explore-data/SKILL.md` — the conduct home, and the medium conflict
- `references/narrative-discipline.md` — home for AC-12
- `dsx/checks/repro.py:179-200` — the self-declared notebook boolean AC-01 would falsify
- `dsx/checks/claims.py:506-510` — the bounded-catch docstring that concedes AC-02
- `dsx/pct_base.py:14-18,46` — the prose leg that weakens `DSX-CLM-070` (AC-03)
- `brief.md` §6.5 — where a promoted gate item becomes a row; note the harness pins
  `_SECTION_65_ITEM_IDS` at exactly nine members with an assertion
  (`tests/test_known_bad_corpus.py:981-991,1769-1772`), so a new row moves that pin in
  lockstep with its fixture
- [[deepen-dsx-explore-data-eda-protocol]] — SEED-001; E-27…E-31 remain deferred and
  AC-10 must be reconciled against them rather than layered on top
