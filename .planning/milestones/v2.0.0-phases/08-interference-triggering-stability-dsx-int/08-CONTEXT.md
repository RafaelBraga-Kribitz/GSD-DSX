# Phase 8: Interference, triggering, stability - Context

**Gathered:** 2026-08-12 (assumptions mode)
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 8 delivers the `DSX-INT-*` check family: interference and SUTVA risk, shared-budget
versus marketplace patterns, triggered-versus-eligible dilution, and novelty/primacy over the
declared stability window. It creates `dsx/frame/interference.py`, registers it in
`GATE_PROFILES`, ships one new known-bad fixture pair, and restructures the known-bad corpus
contract to absorb its own findings.

**Requirements:** REQ-P8-01 … REQ-P8-06 (6 requirements, `.planning/REQUIREMENTS.md:108-113`).

**Not in this phase.** No new `validity_frame:` contract fields — the `interference`,
`triggering` and `stability` sub-blocks and their vocabularies all shipped in Phase 6.
No `DSX-VAL-*` (Phase 7), no `DSX-PAR-*` beyond what Phase 6 shipped (Phase 9), no
`references/families.yaml` (Phase 11). Ratio-metric dilution is descoped by REQ-P8-04.

**Depends on:** Phase 6 only. No hard dependency on Phase 7 or Phase 9 — the sub-blocks are
disjoint. See D-13 below for the one place Phase 7 and Phase 8 collide.

</domain>

<decisions>
## Implementation Decisions

### Locked upstream — do NOT re-litigate

- `brief.md` §4 (D-01…D-14) and §5 (contract shape) are binding (`PROJECT.md` §Context).
- `PROJECT.md` Key Decisions M-01…M-09 are binding.
- Phase 6's `06-CONTEXT.md` decisions are binding where they set precedent, in particular:
  D-04 (every new vocabulary is a name→description dict), D-10 (severity *is* the gate point),
  D-11 (finding granularity: aggregate when the block is absent, per-field when present),
  D-20…D-23 (the D-05 citation, reference-value and linked-test enforcement mechanism).
- **D-11 (brief §4):** no `DSX-INT-*` check may read `inference.paradigm`. REQ-P8-06 asserts
  this by test.
- **D-06:** finding codes are never renumbered. The numbers in D-01 below are irreversible
  once committed.
- **D-03a:** `dsx/frame/` imports only `Report`/`Finding` from `dsx/checks/`, enforced by
  `tests/test_frame_boundary.py` (`_FORBIDDEN_PACKAGE = "dsx.checks"`, line 35).

### Codes, severity and gate wiring

- **D-01: Four codes, with gaps left between concept groups.**

  | Code | Fires when | Severity | Blocks from |
  |---|---|---|---|
  | `DSX-INT-010` | `interference.risk != none`, `mitigation` is `none`, and `residual_note` is blank or a placeholder | CRITICAL | plan |
  | `DSX-INT-011` | A mitigation is declared but is not admissible for the declared risk | CRITICAL | plan |
  | `DSX-INT-030` | An additive metric is analysed on the `eligible` population with `dilution_adjusted` not true | CRITICAL | plan |
  | `DSX-INT-040` | The `stability` sub-block is present and novelty/primacy is unassessed, or assessed with a blank evidence pointer | HIGH | verify |

  `DSX-INT-010` is fixed by the existing fixture header
  (`examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml:12`) and its post-mortem.
  `DSX-INT-030` is fixed verbatim by `brief.md:164`. The `010`/`011` split — absent
  declaration versus present-but-wrong declaration — follows the shipped `DSX-CAU-010`/`011`
  pattern. Groups: `01x` interference, `03x` triggering, `04x` stability.

- **D-02: Severity alone selects the gate point; no `GATE_THRESHOLDS` edit.** `dsx/cli.py:105`
  sets CRITICAL at plan and execute, HIGH at verify and ship. ROADMAP success criteria 1 and 3
  say "exits `1` at `dsx gate plan`" (CRITICAL); success criterion 5 says novelty/primacy is
  flagged "at verify/ship" (HIGH). This is Phase 6 D-10's reasoning applied unchanged.

- **D-03: `GATE_PROFILES` DOES change this phase.** Unlike Phase 6 — which needed no profile
  edit only because `spec` was already in all four profiles — `interference` is a new module
  key in no profile. Add `"interference": interference.check` to `CHECKS` (`dsx/cli.py:63`) and
  register `"interference"` in the `plan`, `verify` and `ship` profiles (`dsx/cli.py:88`),
  **not** `execute`. This mirrors the existing `design` module's absence from `execute` and
  keeps the shared-budget fixture's blast radius to one CRITICAL-threshold gate point instead
  of two. The check reads only `spec`, so `run_checks` (`dsx/cli.py:135`) needs no new dispatch
  branch.

- **D-04: Three edits to `scripts/gen-finding-catalogue.py`.** Append `"DSX-INT-"` to
  `_D05_ALLOWLIST_PREFIXES` (line 58, currently `("DSX-PAR-",)`, whose own comment says the
  list grows as each later phase adds its prefix); add a `DSX-INT` entry to `PREFIX_GROUPS`
  (line 25) or the codes ship uncatalogued and no test notices; regenerate
  `references/finding-codes.md`. No change to `_D05_ALLOWLIST_CODES`. All four codes are three
  digits, so `_TEST_MARKER_RE` (line 74) accepts them unchanged.

### The interference mitigation admissibility rule

- **D-05: The mapping is a module constant in `dsx/frame/interference.py`, not a vocabulary in `dsx/spec.py`.**
  It mirrors `_PARADIGM_CONDITIONAL` (`dsx/frame/paradigm.py:38`) exactly,
  including a test asserting its keys are set-equal to `dsx.spec.INTERFERENCE_RISKS` so a
  future vocabulary addition without a matching key fails loudly. Rationale: this is a
  capability matrix, not a vocabulary — the category `describe_vocabulary()` already
  special-cases for `CHART_CAPABILITIES`. It also carries the D-05 citation burden, so it
  belongs beside the docstring that cites it. `dsx/frame/` may import `dsx.spec` freely; only
  `dsx.checks` is forbidden.

- **D-06: The mapping ships on a STRUCTURAL CRITERION, not as a cited published table.**
  *(User decision, 2026-08-12.)* Research verified the technique names and page numbers from
  Cambridge's own published index, but Chapter 22's running text (pp. 227-234) is unreachable —
  Cambridge Core returns HTTP 429, and there is no library scan, preview or lending copy.
  Therefore:
  - **`Citation:` names Kohavi, Tang & Xu (2020), Ch. 22 "Leakage and Interference between
    Variants", pp. 230-233, for the EXISTENCE AND NAMING of the technique set** — which is
    verified from primary publisher metadata.
  - **`Structural criterion:` states the admissibility rule itself:** *a mitigation is
    admissible only where it operates on the same interference channel the risk names.*
  - The docstring must state plainly that the cell-level table is derived from that criterion
    and is **not** quoted from the book. Borrowed authority is precisely what D-05 exists to
    stop; a rule you can state and falsify is stronger than a table you cannot read.

- **D-07: All five risks are mapped, not just the two the success criteria need.** The channel
  test derives every cell the same way, so the full map costs no more reasoning than a partial
  one, and a partial map would be strict in two places and permissive in three with no visible
  reason. Proposed mapping (the planner may refine, but must justify each cell against the
  channel test and against the mitigation's own description at `dsx/spec.py:211-218`):

  | Risk | Admissible mitigations |
  |---|---|
  | `none` | check short-circuits |
  | `shared_budget` | `budget_isolation`, `time_split`, `modelled` |
  | `marketplace` | `cluster_randomisation`, `geo_split`, `time_split`, `modelled` |
  | `geo_spillover` | `geo_split`, `cluster_randomisation`, `modelled` |
  | `social_graph` | `cluster_randomisation`, `modelled` |
  | `shared_inventory` | `budget_isolation`, `time_split`, `cluster_randomisation`, `modelled` |

  **`cluster_randomisation` is the cell ROADMAP success criterion 2 depends on** — admissible
  for `marketplace`, inadmissible for `shared_budget`. It is the only such candidate among the
  six mitigation members. If the planner's channel analysis overturns this cell, success
  criterion 2 becomes unsatisfiable without extending `INTERFERENCE_MITIGATIONS`, which is
  contract surface Phase 8 is not scoped for — escalate rather than widen the vocabulary.

  **Two facts from the verified index the planner must not paper over:** `modelled` has **no**
  index entry in the book — it is not a book-named technique, so it cannot be cited to Ch. 22
  and must be justified on the structural criterion alone. And the book carries a fifth
  technique the vocabulary omits, "network egocentric randomization" (p. 233); note it, do not
  add it.

- **D-08: `residual_note` is checked with a new shared placeholder helper.** *(User decision,
  2026-08-12.)* Add `is_placeholder()` to `dsx/spec.py` beside `is_blank()` (line 326), matching
  text wrapped in angle brackets. `DSX-INT-010`'s escape hatch requires `residual_note` to be
  both non-blank and not a placeholder. Reason: `templates/ANALYSIS-SPEC.yaml:310` ships
  `residual_note: "<what remains unaddressed, if anything>"`, which is non-blank — without this,
  `dsx init` scaffolds a file that clears a blocking check unedited. The helper is written to be
  reused by Phases 7 through 11 for every prose escape hatch they introduce; do not let each
  phase invent its own. The template itself is unaffected because it declares
  `question_type: descriptive` and `design.kind: observational`, so these checks skip it
  entirely (see D-12).

### The dilution check

- **D-09: `delta_diluted = delta_triggered × trigger_rate` lives in `dsx/mathx.py` as a pure function and is NEVER called from the gate path.**
  `DSX-INT-030` adjudicates declarations
  only: is `triggering.analysis_population == "eligible"` and `dilution_adjusted` not true.
  `.planning/REQUIREMENTS.md:153` puts computing test statistics on the gate path out of scope,
  breaking D-01/D-02. `dsx/frame/` may import `dsx.mathx`.

- **D-10: The citation is exact; the reference value is the paper's own counterexample.**
  *(User decision, 2026-08-12.)* Research read the full camera-ready (free at
  `https://alexdeng.github.io/public/files/wsdm2015-dilution.pdf`; ACM DL DOI
  10.1145/2684822.2685307).
  - **`Citation:` Deng & Hu (2015), "Diluted Treatment Effect Estimation for Trigger Analysis
    in Online Controlled Experiments", WSDM '15, Formula (1) in §2.1, derived in §3.2.** The
    formula as printed is `∆overall = ∆Tr × N_Tr/N`. Its stated preconditions — additivity, no
    treatment effect for untriggered users, no effect on the trigger complement — belong in the
    docstring.
  - **`Reference value:` the paper's time-to-success counterexample (§2.1): true effect
    −26 msec, naive formula yields −18 msec.** Time-to-success is a *ratio* metric, so this
    published pair tests the additive-only scope boundary REQ-P8-04 demands, in the same test.
  - **ROADMAP success criterion 3 must be reworded** from "against the Deng & Hu (2015)
    published value" to "against the Deng & Hu (2015) published counterexample". **This is a
    factual correction, not a lowered bar:** the paper contains no additive worked example at
    all — every number in it is for a ratio metric. Record the reword so it does not read as
    quiet slippage.
  - Do **not** use the Appendix toy example (`0.271 − 0.313 = −0.042`). It is a genuine
    published number, and it was independently re-derived, but it describes the ratio path this
    check deliberately does not cover.
  - Notation note for the docstring: the paper uses `N_Tr/N` for the user trigger rate. `TR` in
    that paper means something else (a per-user denominator trigger rate, §3.3). The contract
    field is `expected_trigger_rate`; `trigger_rate` is not a field. Name the `mathx` parameter
    so the distinction is explicit.

- **D-11: Additivity is a new partition constant over the existing `METRIC_TYPES`.**
  `METRIC_TYPES` (`dsx/spec.py:98`) is a pre-Phase-6 set carrying no additive/ratio
  distinction. Add a partition in `dsx/frame/interference.py` that *references* it — do not
  coin a parallel metric vocabulary (the split-vocabulary pattern M-02 and M-09 rejected).
  Additive: `{count, sum, average}`. Explicitly out of scope: `{ratio, rate}`. Unadjudicated:
  `{percentile, index}`. `DSX-INT-030` fires only on the additive set.
  **A metric with no declared `type` causes a skip plus a decision record naming the skip and
  its reason** — not a finding. `_validate_metrics` (`dsx/spec.py:522`) treats `type` as
  optional today, so firing on an undeclared type is a new blocking condition this phase is not
  scoped for. **Known limit to state in the finding detail:** this leaves a live escape hatch —
  deleting one line dodges a CRITICAL check. The decision record makes it visible in the
  `dsx explain` trail; it does not close it.

- **D-12: REQ-P8-04's ratio-metric entry condition is REWRITTEN, because its premise is false.**
  The condition as written in REQ-P8-04 and ROADMAP success criterion 4 is that "the Deng & Hu
  (2015) ratio-metric equation is obtained from primary source". Research established that the
  paper is freely and publicly available and its exact ratio equation — Formula (3), §3.3 — is
  readable now. **The entry condition is already met as worded, so it would unblock
  immediately.** The real blocker is mathematical: Formula (3) sums over individual users
  (`∆Overall(X) = (1/N) Σ_Tr TR_i × (TrX_iT − TrX_iC)`) and has no closed-form scalar
  multiplier, so it needs per-user data a declaration-only gate never has. The `brief.md` §6.5
  row must name **that** as the entry condition — falsifiable, per D-13. Flag for the planner:
  this may be permanently out of scope for a gate rather than deferred, and the §6.5 wording
  should not promise otherwise.

### Novelty and primacy

- **D-13: `DSX-INT-040` checks the assessment declaration and its evidence pointer — not the window length, and not the file.**
  It fires when `stability` is present and
  `novelty_primacy_assessed` is not true, or it is true and `stability.evidence` is blank.
  - **Not window length:** `DSX-EXP-030`/`031` already adjudicate `design.duration_days`
    (`dsx/checks/design.py:311-338`). A second window check is the double-firing M-01 forbids.
    `DSX-INT-040`'s `detail` must state why it is not `DSX-EXP-030`, the same way M-01 required
    for `DSX-PAR-010` versus `DSX-EXP-060`. Note `DSX-EXP-030`'s detail text already uses the
    word "novelty" (`dsx/checks/design.py:322`).
  - **Not the file:** resolving the evidence pointer needs `_find_evidence_file`/`_anchor_present`
    from `dsx/checks/claims.py:249-258`, which D-03a forbids `dsx/frame/` from importing. Doing
    it properly would mean extracting them into a new stdlib-only peer module — the move Phase 6
    made for `dsx/decisions.py` — and touching a v1.5.0 surface D-08 wants stable. Out of scope
    here; note it as a candidate if a later phase needs the same thing.
  - **"Assessment method cited" (success criterion 5) is satisfied by the check's own
    docstring**, not by a new configuration field. There is no `stability.method` field in
    `brief.md:166-169` or the template, and adding one is contract surface Phase 6 froze.
  - **`where=` must be fully qualified** as `spec.validity_frame.stability.evidence`. Three
    distinct contract fields are named `evidence` — `claims[].evidence` (adjudicated by
    `DSX-CLM-030/031/032`), `validity_frame.identification.evidence`, and this one. An
    unqualified `where` reads as the claims check firing.
  - **`Citation:` for the assessment method: arXiv:2102.12893v1** (Sadeghi et al., 2021,
    "Novelty and Primacy: A Long-Term Estimator for Online Experiments"), Equation (13) in §4.2
    for the general difference-in-differences estimator, Equation (9) in §4.1 for the
    three-period case. **Attribution correction: the published p-value 0.0083 attaches to
    Equation (9), not Equation (13)** — §4.4 says so explicitly. Cite Technometrics 64(4):524-534
    (2022) alongside as the version of record, but **do not cite it for the equation numbers or
    the values**: it is paywalled, arXiv holds only v1 from Feb 2021, and the preprint was never
    synced to the accepted manuscript, so agreement between the two is unverified.

### Cross-phase and test-surface consequences

- **D-14: The D-11 paradigm-read scanner is net-new, and MUST be written parameterised over a module list.**
  No test today scans for *reads* of `inference.paradigm` — `tests/test_frame_boundary.py`
  scans imports only. Phase 7's REQ-P7-09 needs the identical scanner for `dsx/frame/val.py`,
  and the roadmap permits Phases 7 and 8 to run in parallel. **Whichever phase lands first
  writes it over a module list; the second phase adds its module and nothing else.** Two
  independently written scanners will diverge in coverage and the weaker one will permit the
  read it was written to forbid. Prove it fires against deliberately-violating source strings,
  following `tests/test_frame_boundary.py:104-121`. It must catch at least
  `get(spec, "inference.paradigm")`, `spec["inference"]["paradigm"]`, and the bare string
  literal.

- **D-15: `tests/test_known_bad_corpus.py` needs a STRUCTURAL REWRITE, not an allow-list edit.**
  This is the phase's largest under-sized item. Three tests break when `DSX-INT-010`
  starts firing on the shared-budget fixture:
  `test_every_spec_passes_the_critical_threshold_gate_points` (line 187),
  `test_ship_gate_findings_are_all_documented_incidental_corpus_gaps` (line 202), and
  `test_every_postmortem_names_a_catch_attribution_finding_code` (line 176) may follow.
  **The obvious fix is actively forbidden:** `test_incidental_allowlist_names_no_target_family_code`
  (line 231) rejects any code matching `_TARGET_CODE_FAMILIES = ("DSX-INT-", "DSX-PAR-01")`
  (line 66) entering `_INCIDENTAL_GAP_CODES` (line 49). The corpus guarantee must change from
  "every fixture clears plan and execute" to a per-fixture map of the codes each fixture is
  *expected* to be caught by. The module docstring at lines 202-214 says this failure is the
  intended signal, not a defect — it exists to force exactly this edit rather than let the
  documentation rot. The fixture header and post-mortem both assert the fixture clears
  `dsx gate plan`; both become false and must be rewritten.

- **D-16: The new checks skip unless the question is causal or the design is an experiment.**
  Reuse the same `needs_causal_block` condition `_validate_validity_frame_shape` computes
  (`dsx/spec.py:758-761`). Without it, `templates/ANALYSIS-SPEC.yaml` breaks its own gate test:
  it declares `analysis_population: eligible` (line 315), `dilution_adjusted: false` (line 317)
  and `novelty_primacy_assessed: false` (line 321), and is saved only by
  `question_type: descriptive`. Also skip entirely when a required sub-block is absent —
  `DSX-SPEC-081` owns that case (Phase 6 D-11).

- **D-17: Fixtures.** Commit one new pair, `examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml`
  plus its post-mortem, as a full-shape clone of the good fixture (Phase 6's 06-08 decision),
  declaring an additive metric, `analysis_population: eligible`, `dilution_adjusted: false`, and
  `expected_trigger_rate < 1.0`. Success criterion 1's mitigated variant and success criterion
  2's marketplace-mitigation variant are **built in temporary directories inside tests**,
  following the copy-and-mutate idiom already at `tests/test_dsx.py:1410-1447`, so committed
  fixtures are never edited.
  **Pin the gate point in every such test.** Success criterion 1's "exits `0`" holds at plan and
  execute only — the shared-budget fixture still exits `1` at verify and ship on five documented
  incidental gaps (`DSX-CLM-031`, `DSX-COH-031`, `DSX-MET-040`, `DSX-NAR-001`, `DSX-REP-030`).
  A test written against a bare "exits 0" will fail for unrelated reasons.
  `examples/good-ANALYSIS-SPEC.yaml` is safe on its own merits (`interference.risk: none`,
  `dilution_adjusted: true`, `novelty_primacy_assessed: true` with a resolvable evidence
  pointer). `examples/bad-ANALYSIS-SPEC.yaml` already declares the `DSX-INT-010` pattern and
  already exits `1`, so D-08's two exit-code tests are unaffected.

- **D-18: REQ-P8-04's deliverable is four artifacts**, not one: (1) the rewritten `brief.md` §6.5
  row per D-12; (2) `DSX-INT-030`'s docstring stating the additive-only scope; (3) a test
  asserting `DSX-INT-030` does **not** fire on a `type: ratio` metric under otherwise-firing
  conditions; (4) a documentation-content test asserting the §6.5 row exists, following the
  precedent of `test_no_planning_document_misattributes_the_prior_averaged_bound`
  (`tests/test_known_bad_corpus.py:292`), which already greps planning documents for prose
  drift. Without (4) the row can be silently softened and nothing notices.

- **D-19: REQ-P8-01's SUTVA citation is now exact.** Imbens & Rubin (2015), *Causal Inference
  for Statistics, Social, and Biomedical Sciences*, **§1.6, Assumption 1.1, p. 10**, verified
  verbatim from Cambridge's free Chapter 1 excerpt. Sub-sections: §1.6.1 "SUTVA: No
  Interference" (pp. 10-11), §1.6.2 "SUTVA: No Hidden Variations of Treatments" (pp. 11-12).
  **Wording correction:** the book says "No Hidden **Variations** of Treatments", not
  "versions". Assumption 1.1 reads: *"The potential outcomes for any unit do not vary with the
  treatments assigned to other units, and, for each unit, there are no different forms or
  versions of each treatment level, which lead to different potential outcomes."*

- **D-20: Marketplace-as-distinct-from-shared-budget has a verified citation if the planner wants one.**
  Blake & Coey (2014), "Why Marketplace Experimentation is Harder than It Seems",
  EC '14, abstract: *"Ignoring test-control interference leads to estimates of the campaign's
  effectiveness which are too large by a factor of around two."* Verified verbatim from the
  authors' own manuscript. The body (§3) says "over two" and shows the arithmetic (0.74%
  user-level versus ≈0.35% auction-level). Usable in the `DSX-INT-011` docstring or the
  marketplace fixture's post-mortem. Note the author copy carries no EC '14 proceedings
  pagination — sections are citable, pages are not.

### Claude's Discretion

The user accepted the assumption set as written; the researcher and planner may settle these
without returning to discuss:

- The exact channel-test justification prose for each of the five mapping cells in D-07,
  provided each is argued from the mitigation's own description and the `cluster_randomisation`
  cell survives.
- Plan slicing across the six requirements. No internal ordering constraints exist, but D-15's
  corpus rewrite should land in the same plan as the check that breaks it, not after.
- Which real analysis the new `triggering-dilution` fixture encodes, subject to D-05's rule that
  vendor blogs and Medium posts are inadmissible in either direction.
- The `dsx/mathx.py` parameter naming, constrained only by D-10's note that `trigger_rate` is
  not a contract field.
- Whether `test_every_postmortem_names_a_catch_attribution_finding_code` needs changing, or only
  the three tests D-15 names.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Binding inputs — not re-litigable

- `brief.md` §4 — decisions D-01…D-14; D-05 and D-11 are load-bearing here.
- `brief.md` §5.1 — the `validity_frame:` contract; lines 152-170 give the `interference`,
  `triggering` and `stability` sub-block shapes verbatim.
- `brief.md` §6 M2b (lines 307-313) — the milestone definition; §6.5 the gated backlog table
  (lines 364-375), which D-12 amends; §7 reference sources.
- `.planning/PROJECT.md` — Key Decisions M-01…M-09, Constraints, Out of Scope, Known limits.
- `.planning/REQUIREMENTS.md:108-113` — REQ-P8-01…REQ-P8-06; line 153 the gate-path
  computation exclusion; line 158 the ratio-metric Out of Scope row.
- `.planning/ROADMAP.md:238-283` — Phase 8 goal, dependencies, open items and the five success
  criteria. **Success criterion 3 is reworded by D-10 and success criterion 4 by D-12.**
- `.planning/STATE.md` — accumulated ordering constraints and standing per-phase deliverables.
- `.planning/phases/06-contract-extension-decision-record-paradigm-manifest/06-CONTEXT.md` —
  the precedent decisions this phase inherits (its D-04, D-10, D-11, D-20…D-23 in particular).

### Research — advisory, superseded where this CONTEXT.md says so

- `.planning/research/ARCHITECTURE.md` — module layout and the D-03a boundary analysis;
  lines 223-250 propose the code numbering and reserve the `interference` profile key.
- `.planning/research/FEATURES.md` — reference values and their sources. **Its grading of the
  Deng & Hu additive case as "derived" and the ratio case as "UNSOURCED" is superseded by
  D-10 and D-12: the full paper was read, the additive formula is exactly citable, and the
  ratio equation is readable — the blocker was never access.**
- `.planning/research/PITFALLS.md` — #3 severity misallocation and #9 migration are relevant.

### Primary sources verified for this phase

- Deng, A. & Hu, V. (2015), WSDM '15, pp. 349-358 — camera-ready at
  `https://alexdeng.github.io/public/files/wsdm2015-dilution.pdf`; ACM DL DOI
  10.1145/2684822.2685307. Formula (1) §2.1; derivation §3.2; ratio Formula (3) §3.3;
  time-to-success counterexample §2.1.
- Imbens, G. & Rubin, D. (2015), Cambridge UP — §1.6, Assumption 1.1, p. 10. Free Chapter 1
  excerpt at `https://assets.cambridge.org/97805218/85881/excerpt/9780521885881_excerpt.pdf`.
- Kohavi, R., Tang, D. & Xu, Y. (2020), Cambridge UP — Ch. 22, pp. 226-234; "Some Practical
  Solutions" pp. 230-234. Technique names and pages from the publisher index at
  `https://assets.cambridge.org/97811087/24265/index/9781108724265_index.pdf`.
  **Running text unread — see D-06.**
- Sadeghi, S. et al. (2021), arXiv:2102.12893v1 — Eq. (13) §4.2, Eq. (9) §4.1, p = 0.0083 in
  §4.4. Technometrics 64(4):524-534 (2022) is the version of record but is unverified.
- Blake, T. & Coey, D. (2014), EC '14 — abstract and §3, at
  `https://dominiccoey.github.io/assets/papers/marketplace_experiments.pdf`.

### Source files this phase modifies or must not disturb

- `dsx/frame/paradigm.py` — the only existing frame-check exemplar. Mirror its structure,
  citation style, decision-record emission and `_PARADIGM_CONDITIONAL` set-equality test
  (line 38).
- `dsx/frame/interference.py` — **new**; named explicitly by ROADMAP success criterion 5.
- `dsx/spec.py:98` `METRIC_TYPES`; `:195-218` `INTERFERENCE_RISKS`/`INTERFERENCE_MITIGATIONS`;
  `:326` `is_blank` (D-08 adds `is_placeholder` beside it); `:522` `_validate_metrics`;
  `:715` `_VALIDITY_FRAME_CAUSAL_REQUIRED` (note the do-not-"fix" comment at 708-714);
  `:758-761` `needs_causal_block`.
- `dsx/cli.py:63` `CHECKS`; `:88` `GATE_PROFILES`; `:105` `GATE_THRESHOLDS`; `:135` `run_checks`.
- `dsx/mathx.py` — home for the dilution function (D-09).
- `dsx/checks/design.py:311-338` `DSX-EXP-030`/`031`; `:322` the "novelty" detail text.
  **Must not change** (D-13).
- `dsx/checks/claims.py:249-258` — evidence resolution helpers; **out of reach** under D-03a.
- `scripts/gen-finding-catalogue.py:25` `PREFIX_GROUPS`; `:58` `_D05_ALLOWLIST_PREFIXES`;
  `:74` `_TEST_MARKER_RE`.
- `tests/test_known_bad_corpus.py:49` `_INCIDENTAL_GAP_CODES`; `:66` `_TARGET_CODE_FAMILIES`;
  `:176`, `:187`, `:202`, `:231` the affected tests; `:292` the documentation-grep precedent.
- `tests/test_frame_boundary.py:35` `_FORBIDDEN_PACKAGE`; `:104-121` the two-proof pattern.
- `tests/test_dsx.py:1410-1447` — the copy-to-temp-and-mutate fixture idiom.
- `templates/ANALYSIS-SPEC.yaml:310` `residual_note` placeholder; `:315-321` the triggering and
  stability defaults that make D-16 necessary.
- `examples/known-bad/interference-shared-budget-*` — header and post-mortem both need
  rewriting (D-15).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- **`dsx/frame/paradigm.py`** — the only shipped frame check. Its `_PARADIGM_CONDITIONAL`
  constant plus set-equality test (line 38 and its comment) is the exact pattern D-05 copies
  for the risk→mitigation map, so a future vocabulary addition without a matching key fails
  loudly instead of silently passing.
- **`INTERFERENCE_RISKS`, `INTERFERENCE_MITIGATIONS`, `ANALYSIS_POPULATIONS`** already exist
  with full descriptions (`dsx/spec.py:195-232`) and are already registered in `_VOCABULARIES`.
  **No contract or vocabulary change ships in Phase 8** — the sub-blocks landed in Phase 6.
- **`is_blank()` (`dsx/spec.py:326`)** — the only emptiness primitive in the codebase; there is
  no placeholder detection anywhere today, which is why D-08 adds one helper rather than
  scattering regexes.
- **`_validate_validity_frame_shape`'s `needs_causal_block`** (`dsx/spec.py:758-761`) — the
  gating condition D-16 reuses verbatim, so the new checks and the shape validator can never
  disagree about when the causal sub-blocks apply.
- **`dsx.mathx`** — the declared home for what a guardrail computes rather than asserts,
  importable from `dsx/frame/` (only `dsx.checks` is forbidden).
- **`dsx/decisions.py`** — the decision-record emitter; D-11's skip record and each check's
  key judgment point write through it (D-04 standing deliverable).
- **`tests/test_dsx.py:1410-1447`** — the copy-examples-into-a-temporary-directory-and-mutate
  idiom, already used so a good fixture is never edited in place. D-17 reuses it.

### Established Patterns

- **`GATE_PROFILES` and `GATE_THRESHOLDS` are independent knobs** — which checks run versus
  what blocks. Phase 6 needed no profile edit because `spec` was already registered; Phase 8
  does need one, because `interference` is a new key (D-03).
- **Findings carry `detail`, `remedy` and `where`.** Actionability predicts fix rate far better
  than severity label, so each finding must itemise what is missing and name the remedy
  concretely — and `where` must be fully qualified where a field name is ambiguous (D-13).
- **A new check family declares its own disjointness from any adjacent existing code.** M-01 set
  this precedent for `DSX-PAR-010` versus `DSX-EXP-060`; `DSX-INT-040` owes the same statement
  against `DSX-EXP-030` (D-13).
- **Escalate an unverified citation locator; never invent one.** Phase 6 did this twice rather
  than guess. D-06 and D-10 are this phase's two instances.

### Integration Points

- `dsx/frame/interference.py` — new module, four codes, the admissibility map, the additive
  partition. Imports `dsx.spec`, `dsx.mathx`, `dsx.decisions`; from `dsx.checks` only `Report`
  and `Finding`.
- `dsx/spec.py` — `is_placeholder()` helper only (D-08). No new vocabulary, no new field.
- `dsx/cli.py` — `CHECKS` entry plus three profile registrations (D-03).
- `dsx/mathx.py` — the dilution function, never called from the gate path (D-09).
- `scripts/gen-finding-catalogue.py` — prefix allow-list, catalogue group, regeneration (D-04).
- `brief.md` §6.5 — the rewritten ratio-metric entry condition (D-12), with a documentation
  test guarding it (D-18).
- `.planning/ROADMAP.md` — success criteria 3 and 4 reworded (D-10, D-12).
- `tests/` — the corpus restructure (D-15), the parameterised paradigm-read scanner (D-14), the
  new fixture pair and the temporary-directory variants (D-17).

</code_context>

<specifics>
## Specific Ideas

- **The user's standing evidentiary posture, reaffirmed twice in this discussion:** a rule you
  can state, argue with and falsify beats a citation you cannot read. Both D-06 and D-10 were
  decided that way — ship the structural criterion and say so plainly, rather than dress a
  derived rule in a page number nobody has checked. Apply this to every remaining v2.0.0 phase.
- **When research contradicts a planning document, the document is the claim and the source is
  the fact.** D-12 exists because a requirement's stated blocker turned out to be false on
  inspection. The planner should expect one or two more of these in Phases 9-12 and should say
  so rather than route around them.
- **Check for name collisions before coining a term** (carried forward from Phase 6). This
  discussion already caught three live confusions: `evidence` names three different contract
  fields; `trigger_rate` is a formula variable but `expected_trigger_rate` is the only field;
  and `novelty` already appears in `DSX-EXP-030`'s detail text.
- **A published counterexample can be a stronger test than a published worked example**, when
  the check's scope boundary is the thing most likely to be got wrong. D-10 chose the
  time-to-success case for exactly that reason.

</specifics>

<deferred>
## Deferred Ideas

- **Evidence-pointer resolution for `validity_frame` fields.** `DSX-INT-040` would ideally open
  `stability.evidence` and check the anchor resolves, as `DSX-CLM-030` does for claims. Blocked
  by D-03a: the helpers live in `dsx/checks/claims.py`. Doing it properly means extracting them
  into a stdlib-only peer module, the move Phase 6 made for `dsx/decisions.py`. Worth doing once
  a second frame check needs it — Phase 7's `identification.evidence` is the likely trigger.
- **`network_egocentric` as a sixth interference mitigation.** Kohavi Ch. 22 p. 233 names it and
  the vocabulary omits it. Adding a vocabulary member is contract surface, which this phase is
  not scoped for. Note it; revisit at a contract-touching phase.
- **Firing rather than skipping on an undeclared metric type.** D-11 skips, leaving a live
  escape hatch. Closing it means some pre-v2.0.0 configuration files newly block, which is a
  migration decision, not a check decision.
- **Ratio-metric dilution.** Descoped by REQ-P8-04 and re-grounded by D-12. Likely permanently
  out of scope for a declaration-only gate rather than merely deferred, because the exact
  equation needs per-user data. The §6.5 wording should not promise a delivery that the
  determinism doctrine forbids.
- **Retiring `modelled` or grounding it.** It is the one mitigation with no book-named
  counterpart, so it is admissible for every risk under the channel test almost by default —
  which makes it the cheapest way past `DSX-INT-011`. Not this phase's problem, but it is the
  next place this family will leak.

</deferred>

---

*Phase: 08-interference-triggering-stability-dsx-int*
*Context gathered: 2026-08-12*
