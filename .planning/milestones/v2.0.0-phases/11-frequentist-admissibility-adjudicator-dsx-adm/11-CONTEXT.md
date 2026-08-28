# Phase 11: Frequentist admissibility adjudicator (`DSX-ADM-*`) - Context

**Gathered:** 2026-08-20 (assumptions mode)
**Status:** Ready for planning

<domain>
## Phase Boundary

Given a coherent frame, the tool names which frequentist procedures are admissible and what
each one costs in assumptions — and refuses rather than guesses when the frame is
underdetermined.

In scope: `references/families.yaml` as data; the alias table resolving named tests into
families; the admissibility function with its ranking policy and its
`no_admissible_procedure → escalate` branch; extension of `dsx recommend-test`; D-05 citation
enforcement over the ontology data.

Out of scope, and not to be widened during planning: Bayesian procedure admissibility (gated
backlog, brief §6.5 — entry condition is M4 shipping *and* `dsx stats --paradigm` showing
Bayesian frames above 15%); causal identification *strategy* checking (`DSX-CAU-*` owns it);
a catalogue of every named statistical test (families, not tests); computing any test statistic
on the gate path (brief D-02).
</domain>

<decisions>
## Implementation Decisions

### Locked upstream — do NOT re-litigate

- `brief.md` §4 (D-01…D-14), §5 (contract), §6 (M4), §6.5 (gated backlog) and §7 (citations)
  are binding inputs. Load-bearing here: **D-01** stdlib only on the gate path; **D-02** no test
  statistic or posterior computed on the gate path; **D-05** primary-source citation plus a
  published reference value; **D-06** finding codes are never renumbered; **D-11** frame-layer
  checks never read `inference.paradigm`.
- **D-03a, as actually enforced.** `brief.md`, `PROJECT.md` and `06-CONTEXT.md` all word this as
  "`dsx/frame/` imports only `Report`/`Finding` from `dsx/checks/`". That wording is wrong about
  where the classes live and wrong about the carve-out. `Report` and `Finding` are defined in
  `dsx/findings.py`, and `tests/test_frame_boundary.py:35` sets `_FORBIDDEN_PACKAGE = "dsx.checks"`
  with **no carve-out**. The operative rule is: `dsx/frame/*` imports nothing from `dsx.checks`,
  and gets `Report` via `from ..findings import Report`. This correction was established in
  `07-CONTEXT.md` and is restated here because REQ-P11-05 runs straight into it.
- `PROJECT.md` Key Decisions M-01…M-09 are binding. **M-09** in particular:
  `dependence.method_family_required` reuses `VARIANCE_ADJUSTMENTS` and defines no parallel
  vocabulary — the ontology's dependence axis keys on that shipped shape, not on a new one.
- `07-CONTEXT.md` **D-04**: `method_family_required` is single-valued and the admissible-methods
  map lives in `dsx/spec.py`.
- `10-CONTEXT.md` **D-02**: exit `2` is produced only by raising `CheckError`.
- `10-CONTEXT.md` **D-06**: Phase 10 recorded that no importable procedure vocabulary existed and
  that building one was out of scope *for Phase 10*. Phase 11 builds it. See D-03 below for the
  scope boundary that keeps this from changing Phase 10's shipped behaviour.

### Ontology size and traceability

- **D-01: `references/families.yaml` ships with roughly 10–14 families, not 25–35.** Every entry
  points at a fixture or corpus case that is **committed in the repository at the time Phase 11
  lands**. The file covers the six distinct procedure labels present across all nine committed
  specs (`two_proportion_z`, `welch_t`, `fishers_exact`, `bayesian_ab`, `linear_regression`, and
  the template's `null`), the three committed dependence structures (`none`, `clustered`,
  `temporal`), and the clusters the marketing operating context guarantees — clustered
  dependence, sequential monitoring, ratio metrics. *(User decision.)*

  **Rationale.** ROADMAP SC 1 asks for 25–35 families and ROADMAP SC 5 asks that every family
  trace to a case that needed it. Measured against the repository, those two cannot both hold:
  the corpus supplies six procedures and Phase 12 — the phase that grows the corpus — comes
  *after* this one. Sizing to the evidence keeps the stated principle ("a family is added when a
  real case needs it") literally true of the file that ships, rather than aspirationally true.

- **D-02: REQ-P11-01 and ROADMAP SC 1 are amended from "25–35" to the real number, with the
  reason recorded.** This is a requirement amendment, not a silent under-delivery. The planner
  writes the amendment into `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` as part of the
  phase, and states the delivered count. Phase 12 grows `families.yaml` alongside the corpus.

  **Accepted cost.** The citation work is split across two phases rather than done once, and the
  adjudicator returns `no_admissible_procedure` more often at first — which will read as the tool
  being unhelpful until the ontology fills in. Both were weighed and accepted.

### Scope boundary — the alias table has exactly one consumer

- **D-03: the alias table is read by `dsx/frame/admissibility.py` and by nothing else. Neither
  `dsx/checks/stats.py` nor `dsx/frame/prereg.py` is rewired in this phase.** *(User decision.)*

  **Concrete case this leaves alone.** `examples/known-bad/post-hoc-procedure-switch-ANALYSIS-SPEC.yaml:100`
  declares `test: fishers_exact` while `dsx/checks/stats.py:65` spells it `fisher_exact`. That
  mismatch currently fires `DSX-STA-041` at HIGH and is absorbed by `_INCIDENTAL_GAP_CODES` in
  `tests/test_known_bad_corpus.py`. It keeps firing exactly as it does today. Likewise
  `dsx/frame/prereg.py:327` keeps reconciling declared against executed procedure by raw
  `normalize()` string compare, so `DSX-PRE-030`'s firing set is unchanged.

  **Rationale.** ROADMAP SC 2 requires `dsx recommend-test`'s v1.5.0 behaviour on existing specs
  to be unchanged, and the same spirit protects `DSX-PRE-030`. Wiring aliases into either check
  changes a shipped firing set, which can silently invalidate suppressions operators have already
  written. Two name-comparison mechanisms coexisting is the accepted cost; reconciling them is a
  later phase's work.

### Module layout, and how `recommend-test` is extended legally

- **D-04: `recommend-test` is extended by composition inside `dsx/cli.py::cmd_recommend`
  (`cli.py:396-409`).** `recommend_test()` in `dsx/checks/stats.py:32` is **not** moved, **not**
  wrapped, and **not** edited. `cmd_recommend` calls `dsx.checks.stats.recommend_test` and the new
  `dsx.frame.admissibility` separately and merges their output.

  **Why this and not the obvious alternative.** The enforced boundary is one-directional:
  `tests/test_frame_boundary.py:93-102` scans only `FRAME_DIR.rglob("*.py")`, so nothing today
  stops `dsx/checks/stats.py` importing `dsx.frame.admissibility`. That import would ship green
  while destroying the extraction property D-03a exists to protect.
  `.planning/research/ARCHITECTURE.md:101-102` asserts the reverse direction is also forbidden and
  names `dsx/cli.py` as the only place the two packages meet — which `cli.py:23-52` already is.

- **D-04a: the planner should add the reverse-direction scanner** to `tests/test_frame_boundary.py`
  (assert no file under `dsx/checks/` imports `dsx.frame`). Today that doctrine is honour-system.
  This is the cheapest moment to close it, because Phase 11 is the first phase with a real
  incentive to violate it.

- **D-05: `dsx/frame/admissibility.py` resolves the data file as
  `Path(__file__).resolve().parents[2] / "references" / "families.yaml"`**, loads it once through
  `dsx.loader.load()`, and treats an absent or unreadable file as `CheckError` → **exit 2**, never
  as a silently empty ontology.

  **Why.** `install.mjs:39-47` copies `dsx/` and `references/` as siblings, and `cli.py:594`
  already uses this idiom for `templates/ANALYSIS-SPEC.yaml`. The counter-precedent at
  `dsx/input_types.py:32-33` returns an empty catalogue on a missing data file; that is wrong here
  because an empty ontology makes every frame look underdetermined — a blocking gate would report
  an install defect as an analyst's error.

### The data file shape, and the two-parser hazard

- **D-06: `families.yaml` is a top-level mapping whose one key holds a block sequence of flat
  mappings.** Axis keys and `citation` are single-line quoted scalars. `aliases`, `buys` and
  `charges` are sequences of scalars. **No anchors, no merge keys, no `|`/`>` block scalars, no
  `---` document markers.** `dsx.loader.load()` rejects a non-mapping top level outright
  (`loader.py:43-44`), so a bare top-level list is not available.

- **D-07: the inference-method axis key is flat — `inference_method:` — and the adjudicator never
  passes a string literal beginning `inference.` as a call argument.**
  `tests/test_frame_boundary.py:185-187` flags *any* call-argument literal that starts
  `inference.`, and the blunt text detector at `:155` flags the substring `inference.paradigm`
  anywhere in the file, comments and docstrings included. `dsx/frame/prereg.py:504` documents this
  having already bitten Phase 10. Getting this wrong late means renaming the key across every
  entry and every test asserting on them.

- **D-08: a test pins the two parsers together.** `dsx/loader.py` is two parsers — PyYAML when
  importable (`loader.py:62-66`), a bundled subset otherwise (`:68`) — and they measurably
  disagree. A `#` preceded by a space inside a `|` block scalar is silently truncated by
  `_strip_comment` (`loader.py:114`) and preserved by PyYAML; anchors and merge keys raise
  `SpecParseError` on the bundled path and resolve under PyYAML. A test must assert the committed
  `families.yaml` parses **identically on both paths**.

  **What this prevents.** A citation containing a page range written `34 #1` would otherwise ship
  with two different values depending on whether the operator's Python has PyYAML installed — so
  the same file passes the D-05 catalogue check on one machine and fails on another. That is the
  laundering D-05 exists to prevent, arriving through the parser rather than the author.

- **D-09: each entry carries `locator_status: verified | unverified`** alongside `citation:`,
  extending the honesty convention already established at `dsx/frame/paradigm.py:66-72` and
  `dsx/spec.py:216-228`. An unconfirmed chapter number is declared unverified, never silently
  omitted and never guessed.

### Assumption vocabulary — bought and charged

- **D-10: a closed vocabulary of roughly 16–19 assumption tokens, each carrying its own citation,
  plus a mandatory free-text `notes:` field per family, plus an explicit
  `vocabulary_is_not_exhaustive: true` declaration in the file header.**

  **Why the header declaration is load-bearing.** Research established, negatively, that **no
  published taxonomy of estimator assumptions exists**. The Statistical Methods Ontology (STATO)
  advertises coverage of "conditions of application" and delivers zero classes labelled
  "assumption" across 109 properties; no ontology in the OBO Foundry has one either. The
  vocabulary is *assembled* from six canonical sources with per-token citations. Its **closure is
  this project's editorial judgement, not anyone's published finding**, and the file must say so.

- **D-11: the six source clusters for the vocabulary** are — causal identification
  (exchangeability, positivity, consistency: Hernán & Robins Ch.3 §§3.1–3.5, verified);
  interference (SUTVA: Rubin 1980 JASA 75(371):591–593, plus Imbens & Rubin Ch.1 §1.6 already
  anchored); missingness (MCAR/MAR/MNAR: Rubin 1976 Biometrika 63(3):581–592, plus Little & Rubin
  Ch.3 §3.2 already anchored); linear-model and generalised-linear-model assumptions (Wooldridge's
  numbered MLR.1–MLR.6 scheme — **the edition must be pinned first**, because the graduate text
  uses an incompatible OLS.1–OLS.3 scheme); cluster and sandwich conditions (Cameron & Miller 2015
  §II and §VI; MacKinnon, Nielsen & Webb 2023 §2 and §4); distributional regularity.

### Ranking, refusal, and the escalation record

- **D-12: ranking is a rule table of narrow conditioned pairwise orderings, not a scoring
  function.** `DSX-ADM-010`'s message names **which rule fired and what condition it depends on**.
  Classical testing theory positively rules out a total order — admissibility is a partial order
  by construction, and uniformly most powerful tests do not exist for two-sided or general
  composite alternatives.

- **D-13: four orderings are citable today** — Welch over Student (Delacre, Lakens & Leys 2017,
  **plus the 2022 Correction**; Ruxton 2006; Zimmerman 2004 for the prohibition on variance
  pre-testing); Boschloo/unconditional over Fisher's exact (Lydersen, Fagerland & Laake 2009 §9,
  which supplies the only genuine **uniform** domination found anywhere in the research); CV3 and
  the restricted wild cluster bootstrap over CV1 (MacKinnon, Nielsen & Webb 2023 §9 — a
  *reliability* ordering, hedged by its own authors, and one that fails with few treated
  clusters); interacted regression adjustment over unadjusted (Lin 2013's "cannot hurt", with
  Freedman 2008 as the reason the interaction term is not optional).

- **D-14: for every other pair, ranking is by declared structural criterion — fewer assumptions
  charged ranks higher — cited to Manski's Law of Decreasing Credibility** (*Partial Identification
  of Probability Distributions*, Springer, 2003, Introduction "Partial Identification and Credible
  Inference"): "The credibility of inference decreases with the strength of the assumptions
  maintained." Cite by **named principle and section title, not by page** — the statement is
  verified from the author's pre-publication manuscript and the typeset page number is unverified.
  Cite it as a principle about credibility, **not** as a theorem about efficiency.

- **D-15: the final tiebreak is lexicographic on family `id`, and the whole order is byte-stable.**
  No `set`/`dict` traversal order may reach the ranking. Byte-stability is already an enforced
  house property — see `tests/test_dsx.py:345` and the `sorted()` discipline in
  `describe_vocabulary()` (`dsx/spec.py:1112-1118`). A non-deterministic order turns `DSX-ADM-010`
  into noise and breaks the suppression contract, which is only valid if the ordering reproduces.

- **D-16: three distinct causes collapse into the single `DSX-ADM-020` finding** — a required axis
  blank or absent in the frame; the complete key matching zero families; a declared procedure label
  resolving to no alias. All three record `DecisionRecord(escalate=True)`.

  **Why one code.** All three share one remedy — complete the frame, or name a family the ontology
  knows. Splitting them burns irreversible numbers under D-06. This follows `DSX-PRE-010`'s
  two-reasons-one-code precedent (`prereg.py:247-258`) and `10-CONTEXT.md` D-07.

- **D-17: Phase 11 is the first shipped user of `DecisionRecord.escalate` and
  `alternatives_rejected`** (`dsx/decisions.py:82-83`). Both are brief §5.5 schema fields that no
  check has ever set. `escalate=True` is the literal mechanism for REQ-P11-04; the
  ranked-but-not-top entries belong in `alternatives_rejected`. Without `escalate=True`,
  `dsx explain` renders a refusal as an ordinary deterministic choice and the operator never learns
  the tool refused rather than decided.

- **D-18: an unrecognised alias escalates rather than resolving.** No nearest-match, no fuzzy
  string comparison, no fallback to the nearest-sounding family. This branch is the phase's
  scope-bounding mechanism, which is why there is no completeness pressure on the alias list.

### Codes, severity and registration

- **D-19: exactly two codes ship — `DSX-ADM-010` at HIGH and `DSX-ADM-020` at CRITICAL** — as
  pre-assigned in `.planning/research/ARCHITECTURE.md:229-231`. `references/finding-codes.md`
  contains zero `DSX-ADM-` entries today, so nothing collides. Under D-06 these digits are
  irreversible; getting the *count* wrong is worse than getting the digits wrong
  (`10-CONTEXT.md:186-188`).

- **D-20: registered as `CHECKS["admissibility"]` at `plan`, `verify` and `ship`; absent from
  `execute`.**

- **D-21: exit `1` comes from the ordinary `emit()` path** — `DSX-ADM-020` at CRITICAL against
  `GATE_THRESHOLDS["plan"] == "CRITICAL"`. **No new exit code, no `CheckError` for an
  underdetermined frame, no change to `dsx/findings.py`.** Raising `CheckError` would produce exit
  2, which routes to the gate's error branch (`cli.py:9-11`) — reporting an operational failure
  where the analyst has a real, nameable defect.

- **D-22: the frequentist-only scoping decision is made outside `dsx/frame/admissibility.py`.**
  *(User decision.)* A helper exported from `dsx/frame/paradigm.py` — the one file exempt from the
  D-11 scanner (`test_frame_boundary.py:145`) — answers whether the adjudicator applies to this
  spec. `run_checks` (`cli.py:171-200`) calls that helper and passes the answer in as a parameter.
  The adjudicator module never mentions the paradigm. `"DSX-ADM-"` **stays** in
  `_PARADIGM_CONDITIONAL["frequentist"]` (`dsx/frame/paradigm.py:55`); no D-14 reversal record is
  needed.

  **Why not make it paradigm-independent.** That was the alternative. It would make an honest
  `paradigm: bayesian` declaration draw `DSX-ADM-020` at CRITICAL because no frequentist family
  matches — making honesty more expensive than misdeclaration, the exact inversion brief D-10
  exists to block. It would also break the invariant at `dsx/frame/paradigm.py:466-471` that a
  family can never be reported "not applied" in a report where it fired.

  **Accepted cost.** `run_checks` gains a special case, so the generic `CHECKS[name](spec)` branch
  (`cli.py:194-195`) has an exception the next paradigm-conditional check may copy rather than
  share.

### D-05 enforcement over data

- **D-23: a new sibling function in `scripts/gen-finding-catalogue.py`, not an extension of
  `check_d05`.** `check_d05` (`gen-finding-catalogue.py:260-290`) operates exclusively on rows
  extracted by `ast.walk` from `report.add(...)` calls (`:101-117`) and resolves docstrings from
  `dsx/**/*.py` (`:203-242`). It has no file-path parameter for data and no YAML awareness. The
  script also never does `sys.path.insert(0, str(ROOT))`, so it cannot currently import
  `dsx.loader` at all. REQ-P11-06's wording ("enforced by the M1 catalogue check") describes a
  capability that check does not have.

- **D-24: enforcement is two-sided.** Build-time — the new function loads `families.yaml` and
  fails on any entry with a blank or missing `citation`. Run-time — the adjudicator **drops
  uncited families at load and refuses to rank them**, rather than silently including them. Both
  are prescribed by `.planning/research/PITFALLS.md:296-302`.

- **D-25: `"DSX-ADM-"` must be added to `_D05_ALLOWLIST_PREFIXES`**
  (`gen-finding-catalogue.py:57-68`). That constant is an **inclusion** list, not an exemption list
  — forgetting the prefix means `--check` passes green while enforcing nothing on the new family.

### Citation hygiene — two live hazards and one existing defect

- **D-26: two papers the ontology will cite have published corrections that invalidate specific
  numbers.** Delacre, Lakens & Leys (2017) has a **2022 Correction** (DOI 10.5334/irsp.661) listing
  six errors including two simulation script errors; the headline recommendation survives verbatim
  but the tables do not. Pustejovsky & Tipton (2018) has a **2023 Corrigendum** (DOI
  10.1080/07350015.2023.2174123). Any reference value taken from either paper is validated against
  its correction first.

- **D-27: `references/test-selection.md` carries a live D-05 defect that Phase 11 must fix.** It
  prescribes "two-proportion z (Fisher exact if any expected cell < 5)". Lydersen, Fagerland &
  Laake (2009) §9 states directly: "The traditional Fisher's exact test should practically never be
  used." That file is uncited and the alias layer would inherit the error. Fixing the reference
  file is in scope; **changing any check's firing set is not** (see D-03).

- **D-28: published reference values come from the National Institute of Standards and Technology
  (NIST) where possible** — Handbook 151 §1.3.5.3 (verified worked two-sample t-test example) and
  the Statistical Reference Datasets, SRD 140 (58 datasets, certified values to 16 significant
  digits). Open, versioned, and purpose-built to be the number software is tested against. **NIST
  publishes no DOI for these — cite by handbook and section number with the URL, and do not invent
  a DOI.**

- **D-29: two locators the project currently carries as unverified are now resolved and should be
  folded into `brief.md` §7** — Kohavi, Tang & Xu Chapter 22, *Leakage and Interference between
  Variants*, pp. 226–234 (closes the flag in `06-08-SUMMARY.md` and `06-VERIFICATION.md`); and
  Cameron & Miller (2015) **Section VI *Few Clusters***, with Section II for the estimator and
  Section IV for the clustering dimension (partially closes the flag in `07-01-SUMMARY.md`).
  **Caveat: the accepted manuscript jumps from Section VIII to Section XI, so the typeset journal
  numbering may differ — the manuscript numbering is the verified object.**

### Claude's Discretion

- **The estimand axis shape.** `validity_frame.estimand.quantity` is free prose in every committed
  spec (`examples/good-ANALYSIS-SPEC.yaml:283`), `dsx/frame/val.py:53` only blank-checks it, and
  the one closed outcome vocabulary (`OUTCOME_TYPES`, `dsx/checks/stats.py:15`) is unreachable from
  `dsx/frame/` under D-03a. `_VALIDITY_FRAME_MEMBERSHIP` (`dsx/spec.py:845-854`) has no estimand
  row. The planner chooses between adding an `ESTIMAND_TYPES` vocabulary plus a new **optional**
  `validity_frame.estimand.type` field, or keying on `analysis.outcome_type` + `n_groups` +
  `paired` (the shape `recommend_test` already takes, which would require moving `OUTCOME_TYPES`
  into `dsx/spec.py` first). **Binding constraint either way: no fuzzy string match on free prose
  may become the primary lookup path** — that is the nearest-sounding-family fallback D-18 forbids.
  Presented to the user; they chose to leave it to planning within this constraint.
- **Which 10–14 families, and their exact axis values**, within D-01's sourcing rule.
- **Plan slicing across the six requirements**, subject to the ordering constraint that
  `families.yaml` and its citations exist before the adjudicator is written against them.
- **Whether the reverse-direction boundary scanner (D-04a) ships as its own plan or rides along**
  with the module that creates the temptation.
- **Exact membership of the 16–19 assumption tokens** in D-10, beyond the clusters named in D-11.
- **Which NIST Statistical Reference Dataset** backs each family reducible to linear-model
  arithmetic.

### Folded Todos

None — `todo.match-phase 11` returned zero matches.
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

- `brief.md` — §4 (decisions D-01…D-14), §5 (the contract, incl. §5.4 paradigm manifest and §5.5
  decision record), §6 (M4), §6.5 (gated backlog), §7 (citations). Binding; not to be re-litigated.
- `.planning/PROJECT.md` — Key Decisions M-01…M-09, Constraints, Out of Scope.
- `.planning/REQUIREMENTS.md` — REQ-P11-01 … REQ-P11-06. **Note D-02: REQ-P11-01's "25–35" is
  amended by this phase.**
- `.planning/ROADMAP.md` — Phase 11 section, Success Criteria 1–5. **Note D-02: SC 1 is amended.**
- `.planning/research/ARCHITECTURE.md` — esp. lines 99-102 (the two-directional boundary doctrine),
  145, 168, 174 (file placement), 229-251 (`DSX-ADM-*` code, severity, gate points, dispatch),
  345, 564, 610, 634 (M4-after-M2a ordering rationale).
- `.planning/research/PITFALLS.md` — esp. lines 246-302 (D-05 over `families.yaml`, the two-sided
  fix), 612-645 (premature-scaffolding and citation-deferral anti-patterns).
- `.planning/phases/07-validity-frame-checks-dsx-val/07-CONTEXT.md` — D-03a correction; D-04
  (`method_family_required` single-valued); the dependence taxonomy this ontology keys on.
- `.planning/phases/10-pre-registered-inference-plan-dsx-pre/10-CONTEXT.md` — D-02 (exit 2 only via
  `CheckError`), D-06 (procedure vocabulary deferred to this phase), D-07 and D-12
  (one-code-per-fact discipline).
- `.planning/phases/06-contract-extension-decision-record-paradigm-manifest/06-CONTEXT.md` —
  severity-is-the-gate-point; D-05 mechanical enforcement.
- `references/finding-codes.md` — the code registry; confirm no `DSX-ADM-` collision before
  assigning.
- `references/test-selection.md` — **carries the live D-05 defect named in D-27.**
- `references/paradigm-symmetry.md` — the D-12/D-12a symmetry audit.

**Code that constrains the design** (read before planning, not just before implementing):
`dsx/loader.py`, `tests/test_frame_boundary.py`, `dsx/frame/paradigm.py`,
`scripts/gen-finding-catalogue.py`, `dsx/cli.py`, `dsx/checks/stats.py`, `dsx/decisions.py`.
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- **`dsx.loader.load()`** (`dsx/loader.py`) — the parser REQ-P11-01 requires. **It is two parsers**:
  PyYAML when importable (`:62-66`), a bundled subset otherwise (`:68`). See D-06 and D-08.
- **`DecisionRecord`** (`dsx/decisions.py:82-83`) — `escalate` and `alternatives_rejected` already
  exist and have never been set by any check. Phase 11 is their first user.
- **`recommend_test()`** (`dsx/checks/stats.py:32`) and **`cmd_recommend`** (`dsx/cli.py:396-409`) —
  the v1.5.0 behaviour REQ-P11-05 extends. `cmd_recommend` is 13 lines with no spec loading, so
  composition there is purely additive.
- **`dsx/frame/paradigm.py`** — already classifies `"DSX-ADM-"` as paradigm-conditional under
  frequentist (`:55`); the sole file exempt from the D-11 scanner (`test_frame_boundary.py:145`);
  carries the `locator_status` honesty convention at `:66-72`.
- **`dsx/frame/val.py`, `prereg.py`, `interference.py`** — the established frame-module shape:
  single `check(spec) -> Report` entry point, `from ..findings import Report`.
- **`describe_vocabulary()`** (`dsx/spec.py:1112-1118`) — the byte-stability precedent D-15 follows.
- **NIST Statistical Reference Datasets (SRD 140)** and **NIST Handbook 151 §1.3.5.3** — external,
  open, certified sources of the published reference values D-05 requires.

### Established Patterns

- **Severity is the gate point.** CRITICAL blocks from `plan`; HIGH blocks at `verify`/`ship` only
  (`dsx/cli.py:105-110`).
- **Exit codes are the contract.** `0` pass, `1` block, `2` could not run. Exit 2 only via
  `CheckError`/`SpecParseError`/`ValueError` (`cli.py:796-801`).
- **Routing knobs are computed outside check modules.** `run_checks` (`cli.py:171-200`) already
  derives `strict`, `reconcile_trail` and `gate_point` before dispatch — the precedent D-22 follows.
- **Data-file path resolution.** `cli.py:594` resolves `templates/ANALYSIS-SPEC.yaml` as a package
  sibling; `install.mjs:39-47` copies `dsx/` and `references/` as siblings, so repo and installed
  layouts match.
- **Unverified locators are declared, not omitted** (`dsx/spec.py:216-228`,
  `dsx/frame/paradigm.py:66-72`).
- **One stable fact per finding code**; the count matters more than the digits.

### Integration Points

- `dsx/cli.py` — `CHECKS` registry (new `"admissibility"` entry), `GATE_PROFILES` (register at
  `plan`/`verify`/`ship`), `run_checks` (the D-22 paradigm-routing special case), `cmd_recommend`
  (the D-04 composition point).
- `scripts/gen-finding-catalogue.py` — new sibling function (D-23), `_D05_ALLOWLIST_PREFIXES`
  (D-25), and a `sys.path` edit so the script can import `dsx.loader`.
- `tests/test_frame_boundary.py` — new reverse-direction scanner (D-04a); the existing D-11 scanner
  at `:210-222` constrains D-07.
- `references/` — new `families.yaml`; correction to `test-selection.md` (D-27); new `DSX-ADM-*`
  rows in `finding-codes.md`.
- `brief.md` §7 — the two locator corrections in D-29, plus the new citation spine.
- `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` — the D-02 amendment.
</code_context>

<specifics>
## Specific Ideas

- **The citation spine established by research** — nine works beyond the seven already in
  `brief.md` §7, because the relevant clusters span three literatures and no smaller set covers
  them: Deng, Xu, Kohavi & Walker (2013) WSDM, DOI 10.1145/2433396.2433413 (CUPED — variance
  reduction, with verified equations and empirical values, openly accessible); Deng, Knoblich & Lu
  (2018) KDD, DOI 10.1145/3219819.3219919 (delta method for ratio metrics, arXiv:1803.06336);
  MacKinnon, Nielsen & Webb (2023) *Journal of Econometrics* 232(2):272-299 (cluster-robust,
  arXiv:2205.03285); Wooldridge (2010) *Econometric Analysis of Cross Section and Panel Data* 2nd
  edn; Cameron & Trivedi (2013) *Regression Analysis of Count Data* 2nd edn; Koenker (2005)
  *Quantile Regression* with Firpo (2007) *Econometrica* 75(1):259-276; Agresti (2013) *Categorical
  Data Analysis* 3rd edn; Lumley (2010) *Complex Surveys* (reproducible worked examples, better
  D-05 source than Lohr); and for sequential inference — Johari, Koomen, Pekelis & Walsh (2022)
  *Operations Research* 70(3):1806-1821 (arXiv:1512.04922), Howard, Ramdas, McAuliffe & Sekhon
  (2021) *Annals of Statistics* 49(2), and Jennison & Turnbull (2000) *Group Sequential Methods*.
  Sandwich and small-sample corrections: Liang & Zeger (1986), Bell & McCaffrey (2002) — openly
  accessible via Statistics Canada, Imbens & Kolesár (2016), Pustejovsky & Tipton (2018) with its
  Corrigendum.
- **Verified reference values available today**: Cameron & Miller §VI rejection rates
  (.063/.058/.080/.115 at G = 50/20/10/6; .068/.081/.118/.208 at G = 30/20/10/5; .183 unbalanced at
  G = 10); Deng 2013 Eq. (5) `var(Y_cv) = var(Y)(1 − ρ²)` and the 45%/52%/49% empirical reductions;
  Lydersen 2009 §7.1 epinephrine example (exact conditional p = 0.0544, mid-p = 0.0297); Delacre
  2017 Type-I rates 0.028 and 0.083 versus Welch stable at 0.05 (**validate against the 2022
  Correction first**); NIST Handbook 151 §1.3.5.3 AUTO83B.DAT (T = −12.62059, pooled sd 6.34260,
  ν = 326).
- **Four clusters have verified citations but no verified reference value** — quantile treatment
  effects, count/rate models, survey-weighted estimation, and the delta method. Close that gap
  before those families ship, or do not ship them. Do not paper over it.
- **Do not invent page numbers, chapter numbers or DOIs.** The project's stated preference is an
  admitted gap over a plausible-looking fabrication. Locators flagged unverified in the research —
  Wooldridge (2010) chapters, Cameron & Trivedi chapters, Koenker/Firpo chapters, Agresti chapters,
  Lumley chapters, White (1980) volume/issue/pages, Lehmann & Romano's admissibility section, Howard
  et al. page range — stay `locator_status: unverified` until someone opens the book.
</specifics>

<deferred>
## Deferred Ideas

- **Growing `families.yaml` to 25–35 entries** — Phase 12, alongside the corpus that justifies
  them. Consequence of D-01/D-02.
- **Reconciling the two procedure-name comparison mechanisms** — wiring the alias table into
  `dsx/checks/stats.py` and `dsx/frame/prereg.py`. Deferred by D-03 because it changes shipped
  firing sets. Needs its own phase with a suppression-migration story.
- **Bayesian procedure admissibility (`DSX-ADM-*` second axis)** — gated backlog, brief §6.5. Entry
  condition: M4 ships **and** `dsx stats --paradigm` shows Bayesian frames above 15% of the
  operator's history. Phase 11 satisfies the first half only. A test asserts no `families.yaml`
  entry declares a Bayesian inference method (ROADMAP SC 5).
- **Closing the reference-value gap for quantile, count/rate, survey-weighted and delta-method
  families** — either before those families ship, or those families wait.
- **Pinning the Wooldridge edition** for the MLR.1–MLR.6 assumption tokens (D-11). Until pinned,
  that cluster's tokens cannot be cited.

### Reviewed Todos (not folded)

None — `todo.match-phase 11` returned zero matches.
</deferred>
