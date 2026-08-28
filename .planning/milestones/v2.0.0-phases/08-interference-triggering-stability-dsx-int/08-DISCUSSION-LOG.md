# Phase 8: Interference, triggering, stability - Discussion Log (Assumptions Mode)

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions captured in `08-CONTEXT.md` — this log preserves the analysis.

**Date:** 2026-08-12
**Phase:** 08-interference-triggering-stability-dsx-int
**Mode:** assumptions
**Areas analyzed:** codes/severity/gate wiring; risk→mitigation admissibility and the
residual-note escape hatch; the dilution assertion and additive-metric detection;
novelty/primacy and the paradigm-read scanner; fixtures, corpus blast radius and REQ-P8-04

## Assumptions Presented

### Codes, severity and gate wiring

| Assumption | Confidence | Evidence |
|---|---|---|
| Four codes: `DSX-INT-010`/`011` CRITICAL, `030` CRITICAL, `040` HIGH, with gaps between concept groups | Likely | `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml:12`; `brief.md:164`; `dsx/cli.py:105`; `.planning/research/ARCHITECTURE.md:228-230` |
| `GATE_PROFILES` does change this phase — `interference` registered at plan/verify/ship, not execute | Confident | `dsx/cli.py:63`, `:88`; `dsx/frame/paradigm.py` precedent; `design`'s existing absence from `execute` |
| Three edits to `scripts/gen-finding-catalogue.py`: prefix allow-list, catalogue group, regeneration | Confident | `scripts/gen-finding-catalogue.py:58` (`_D05_ALLOWLIST_PREFIXES = ("DSX-PAR-",)` with its own growth comment), `:25`, `:74` |

### Admissibility mapping and the residual-note escape hatch

| Assumption | Confidence | Evidence |
|---|---|---|
| The mapping is a module constant in `dsx/frame/interference.py`, mirroring `_PARADIGM_CONDITIONAL`, not a new vocabulary | Likely | `dsx/frame/paradigm.py:38`; `describe_vocabulary()`'s existing capability-matrix special case for `CHART_CAPABILITIES` |
| `cluster_randomisation` is the only mitigation admissible for `marketplace` and inadmissible for `shared_budget` — the single cell success criterion 2 depends on | Unclear | Derived by matching `dsx/spec.py:211-218` mitigation descriptions to `:195-209` risk descriptions. **No cell sourced at cell level.** |
| `residual_note` is "explicit" iff non-blank, with no placeholder rule | Likely | `dsx/spec.py:326` `is_blank` is the only emptiness primitive; a repo-wide search found no placeholder handling anywhere in `dsx/` |

### The dilution check

| Assumption | Confidence | Evidence |
|---|---|---|
| The formula lives in `dsx/mathx.py` and is never called on the gate path; `DSX-INT-030` adjudicates declarations only | Confident | `.planning/REQUIREMENTS.md:153`; `.planning/research/FEATURES.md:120-124`; `dsx/mathx.py:1-11` |
| Additivity is a new partition over the existing `METRIC_TYPES`; undeclared type → skip plus decision record | Likely | `dsx/spec.py:98` (a set with no additive/ratio distinction), `:522` (`type` optional today); `dsx/frame/paradigm.py:43-57` `_NOT_SHIPPED` precedent |
| No published additive reference value exists — must be escalated, not invented | Confident | `.planning/research/FEATURES.md:100-112`, `:521-522`; Phase 6 escalated two comparable cases |

### Novelty/primacy and the paradigm scanner

| Assumption | Confidence | Evidence |
|---|---|---|
| `DSX-INT-040` checks the assessment boolean and evidence pointer; not window length, not file resolution | Likely | `.planning/research/FEATURES.md:404-412`; `dsx/checks/design.py:311-338` already owns window length; `dsx/checks/claims.py:249-258` is out of reach under D-03a |
| The D-11 paradigm-read scanner is net-new; Phase 7 needs the identical one | Confident | `tests/test_frame_boundary.py:35`, `:76-89` scan imports only; `06-CONTEXT.md:322-324` deferred this coverage to Phases 7 and 8 |

### Fixtures, corpus blast radius, REQ-P8-04

| Assumption | Confidence | Evidence |
|---|---|---|
| `tests/test_known_bad_corpus.py` needs a structural rewrite; the allow-list fix is actively forbidden | Confident | `:66` `_TARGET_CODE_FAMILIES = ("DSX-INT-", "DSX-PAR-01")`; `:231` the test enforcing it; `:187`, `:202` the breaking tests; module docstring `:202-214` says this is the intended signal |
| New checks skip unless causal or experiment, reusing `needs_causal_block` | Confident | `dsx/spec.py:758-761`; `templates/ANALYSIS-SPEC.yaml:310-321` would otherwise fail its own gate test |
| One new committed fixture pair; success-criteria variants built in temporary directories | Likely | `tests/test_dsx.py:1410-1447` copy-and-mutate idiom; `tests/test_known_bad_corpus.py:131` forces a sibling post-mortem |
| REQ-P8-04's deliverable is four artifacts including a documentation-content test | Likely | `tests/test_known_bad_corpus.py:292` precedent; `brief.md:364-375` §6.5 table has no ratio row today |

## External Research

Five topics researched against primary sources. Four verified from primary text; one blocked
behind a paywall. The evidentiary instruction was explicit that "could not verify" is the
correct answer where verification fails, and that no page, theorem or equation number was to
be filled in speculatively.

| Topic | Verification level | Outcome |
|---|---|---|
| Deng & Hu (2015) dilution formula and worked example | primary-text-verified (all 10 pages) | Formula (1) §2.1 verified verbatim, derived §3.2. **No additive worked example exists** — every number in the paper is for a ratio metric. Ratio Formula (3) §3.3 also readable. |
| Kohavi, Tang & Xu (2020) Ch. 22 mitigation taxonomy | (a) primary-metadata-verified; (c) **not-found** | Technique names and pages verified from the publisher's own index. Chapter running text (pp. 227-234) unreachable — Cambridge Core HTTP 429, no scan, no preview, no lending copy. Cell-level admissibility not quotable. |
| Sadeghi et al. (2021) novelty/primacy estimator | primary-text-verified (arXiv); **not-found** (journal) | Eq. (13) §4.2 and Eq. (9) §4.1 confirmed. **Correction: p = 0.0083 attaches to Eq. (9), not Eq. (13)** (§4.4 states this). arXiv holds only v1; Technometrics version paywalled and never synced. |
| Blake & Coey (2014) marketplace interference | primary-text-verified | "too large by a factor of around two" quotable verbatim from the abstract; body §3 says "over two" with the arithmetic (0.74% versus ≈0.35%). Confidence raised from medium to verified. |
| Imbens & Rubin (2015) SUTVA statement | primary-text-verified | §1.6, Assumption 1.1, p. 10, quotable verbatim. **Wording correction: the book says "No Hidden Variations of Treatments", not "versions".** |

### What research overturned

1. **ROADMAP success criterion 3 is unsatisfiable as literally written.** It requires a test
   "against the Deng & Hu (2015) published value" for the additive case. That value does not
   exist in the paper. This is a fact about the paper, not an access barrier.
2. **REQ-P8-04's ratio-metric entry condition rests on a false premise.** It defers on the
   condition that the ratio equation "is obtained from primary source". The paper is free and
   public and the equation — Formula (3), §3.3 — is readable now, so the condition is already
   met and would unblock immediately. The real blocker is that Formula (3) sums over individual
   users and needs per-user data a declaration-only gate never has.
3. **The interference admissibility mapping cannot ship as a cited published table.** Only the
   existence and naming of the technique set is verified; which technique addresses which risk
   is not. Two incidental findings: `modelled` has no index entry and is therefore not a
   book-named technique at all, and the book carries a fifth technique the vocabulary omits
   ("network egocentric randomization", p. 233).

### Sources

- https://alexdeng.github.io/public/files/wsdm2015-dilution.pdf (ACM DL DOI 10.1145/2684822.2685307)
- https://assets.cambridge.org/97811087/24265/index/9781108724265_index.pdf
- https://assets.cambridge.org/97811087/24265/frontmatter/9781108724265_frontmatter.pdf
- https://arxiv.org/abs/2102.12893
- https://dominiccoey.github.io/assets/papers/marketplace_experiments.pdf
- https://assets.cambridge.org/97805218/85881/excerpt/9780521885881_excerpt.pdf

### Escalated to a human — unresolved

- **Kohavi, Tang & Xu Ch. 22, pp. 227-234 running text.** Needs institutional Cambridge Core
  access or a physical copy. Until obtained, the mapping ships on the structural criterion
  (CONTEXT D-06). Cambridge Core returned HTTP 429 on every attempt across two tools and both
  URL forms.
- **Technometrics 64(4):524-534 version of Sadeghi et al.** Needs Taylor & Francis access to
  confirm the journal version agrees with arXiv v1 on the estimator and values. Until obtained,
  cite arXiv:2102.12893v1 for the locators (CONTEXT D-13).

## Corrections Made

Four questions were put to the user. All four recommendations were accepted.

### Dilution reference value

- **Original assumption:** no published additive reference value exists; the gap must be
  escalated. Open question: what the required test then asserts against.
- **User decision:** cite Formula (1) as the formulation and test against the paper's own
  time-to-success counterexample (true effect −26 msec versus the naive formula's −18 msec).
  Reword ROADMAP success criterion 3 from "published value" to "published counterexample".
- **Reason:** it is the only option that yields a genuinely published number *and* tests the
  additive-only scope boundary REQ-P8-04 demands, in a single test. The counterexample metric
  is a ratio, so it exercises exactly the boundary most likely to be got wrong. Rejected: a
  bare structural criterion (ships the boundary untested) and the appendix toy example (a real
  published number, but about the ratio path the check does not cover).

### Interference mitigation admissibility mapping

- **Original assumption:** a module constant mirroring `_PARADIGM_CONDITIONAL`, with the cell
  content unsourced and flagged Unclear.
- **User decision:** map all five risks. Cite Ch. 22 pp. 230-233 for the existence and naming
  of the technique set (verified). Ship the cells themselves under a structural criterion —
  *a mitigation is admissible only where it operates on the same interference channel the risk
  names* — and state in the docstring that the table is derived, not quoted.
- **Reason:** the channel test is a rule that can be stated, argued with and falsified, whereas
  a cited table nobody can read is borrowed authority — the thing D-05 exists to stop. Mapping
  all five costs no more reasoning than two, since every cell derives from the same test.
  Rejected: mapping only the two risks the success criteria need (strict in two places and
  permissive in three, with no visible reason) and holding `DSX-INT-011` until the book arrives
  (stalls the phase on an access barrier for a rule the book probably does not state as a table).

### The `residual_note` escape hatch

- **Original assumption:** non-blank is sufficient, with the hole documented as another instance
  of the known limit "a frame that lies passes".
- **User decision:** add a shared `is_placeholder()` helper to `dsx/spec.py` beside `is_blank()`,
  matching angle-bracket text, and require `residual_note` to be non-blank *and* not a
  placeholder. Phases 7 through 11 reuse it.
- **Reason:** `templates/ANALYSIS-SPEC.yaml:310` ships a non-blank placeholder, so without this
  `dsx init` scaffolds a file that clears a blocking check unedited — the scaffold becomes the
  escape hatch. One small helper closes it for the four remaining phases rather than for this
  one only. Rejected: documenting the hole (leaves it open) and requiring two non-blank fields
  (both template lines are placeholders too, so it raises the price without closing anything).

### Everything else

- **User decision:** accepted as written — code numbers and severities, the
  no-computation-on-the-gate-path rule, additive-metric detection with skip-plus-decision-record
  on an undeclared type, what the novelty/primacy check tests, the known-bad corpus rewrite, and
  the shared parameterised paradigm-read scanner.
- Two offered alternatives were declined: revisiting the four code numbers (for example folding
  the mitigation-mismatch check into `DSX-INT-010`), and firing rather than skipping on an
  undeclared metric type.

## Decided by Claude, not asked

- **REQ-P8-04's entry condition is rewritten to name the mathematical blocker** rather than the
  access blocker, because the access premise was verified false. Stated to the user as a call
  made rather than a question asked, with an invitation to push back toward permanent descoping.
  Recorded as CONTEXT D-12, with the permanent-descope possibility carried in Deferred Ideas.
- **Success criteria 3 and 4 need roadmap edits.** Recorded so the reword is attributable and
  does not read as quiet slippage.
