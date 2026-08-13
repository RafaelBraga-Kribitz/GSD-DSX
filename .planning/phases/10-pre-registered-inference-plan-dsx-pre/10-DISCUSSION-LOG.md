# Phase 10: Pre-registered inference plan (`DSX-PRE-*`) - Discussion Log (Assumptions Mode)

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions captured in `10-CONTEXT.md` — this log preserves the analysis.

**Date:** 2026-08-13
**Phase:** 10-pre-registered-inference-plan-dsx-pre
**Mode:** assumptions (text mode — questions presented as plain-text numbered lists per
`workflow.text_mode: true`)
**Areas analysed:** the fallback-rule mini-language and its failure mode; declared-versus-executed
reconciliation; the content lock and `declared_at` provenance; module, registration, severity,
numbering and the enforcement surfaces that go red.

## Assumptions Presented

### The fallback-rule mini-language, its facts, and the exit-2 mechanism

| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| The mini-language is opt-in, discriminated by the literal `->` arrow; a `fallback_rule` without it is free prose and out of scope | Confident | All eight committed `fallback_rule` values are English prose with zero `->` occurrences: `examples/good-ANALYSIS-SPEC.yaml:362-364`, `templates/ANALYSIS-SPEC.yaml:358`, `examples/bad-ANALYSIS-SPEC.yaml:242`, and the five `examples/known-bad/*` fixtures. Six of eight begin with "If", so an `if`-prefix trigger over-matches everything. `brief.md:204-205` uses the arrow |
| Exit `2` is produced only by raising `CheckError` from inside a check — no finding-based route exists | Confident | `dsx/findings.py:181-182` (`exit_code()` returns only 1 or 0); `dsx/findings.py:23` (`EXIT_ERROR = 2`); `dsx/cli.py:765`, `:768` (the only two returns, both in `main()`'s exception handlers). `apply_suppressions` is the working precedent |
| `clusters`, the brief's own example fact, does not exist anywhere in the contract | Likely | Zero matches for `clusters` across every `.yaml` in the repo. `validity_frame.dependence` holds `structure`, `cluster_var`, `method_family_required` and no count. `REQUIRED_TOP_LEVEL` is `("spec_version","title","question_type","decision")` — there is no `results:` shape validator at all |

### The declared-versus-executed reconciliation surface

| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| Declared side is `inference.primary_procedure`; executed side is `analysis.test`; `normalize()` is the brittleness fix | Likely | `dsx/spec.py:990-994` (`_INFERENCE_MEMBERSHIP` vocabulary-checks only three fields, so `primary_procedure` is free text); `examples/good-ANALYSIS-SPEC.yaml:231-255` (`results.tests[]` carries no procedure name); `dsx/spec.py:409-410` (`normalize()` maps `wild cluster bootstrap` → `wild_cluster_bootstrap`) |
| No importable procedure vocabulary exists, and building one is out of scope | Confident | `dsx/checks/stats.py:40-127` holds the only lexicon; `dsx/frame/__init__.py:16-31` and `tests/test_frame_boundary.py` forbid importing `dsx.checks`. `references/families.yaml` belongs to Phase 11 (`ROADMAP.md:478-482`, brief §6.6) |
| REQ-P10-03 and REQ-P10-04 are one code with two fixtures, not two codes | Likely | The check cannot rank conservatism without procedure ranking, which brief D-02 bars from the gate path and `ROADMAP.md:472-483` assigns to Phase 11. House habit of one stable fact per code: `09-CONTEXT.md:169-172`, `dsx/frame/interference.py:1-9` |

### The content lock and `declared_at` provenance

| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| The plan-time content lock already exists and already ships — Phase 10 reads it, does not build it | Confident | `dsx/decisions.py:181-190` (`frame_digest()`, sha256 over `validity_frame:`+`inference:`, key-order invariant); `dsx/decisions.py:91-108` (`InvocationHeader`); `dsx/cli.py:302-313` (written on every gate point); `examples/DECISIONS.jsonl` line 1 (the committed artifact). Matches `PITFALLS.md:88-92` and `:721` |
| Reading it promotes `DECISIONS.jsonl` from side channel to gate input — the phase's biggest architectural decision | Likely | `dsx/cli.py:288-290` states the invariant unconditionally: the write "can never change `point`'s exit code". Signature change needed: `dsx/cli.py:176-177` passes `spec` alone to frame modules; `dq`/`code`/`figures`/`narrative` are the `root`-threading precedent at `:156-175`. `dsx/frame/__init__.py:17-18` permits importing `dsx.decisions` |
| The `declared_at` documentation half of REQ-P10-02 is already half written | Confident | `dsx/spec.py:279-285` already describes `post_data` as "an unverifiable operator self-declaration (Phase 10 REQ-P10-02 documents this limit)". `README.md:309-323` and `:338` are the anchors for SC 4's README half |

### Module, registration, severity, numbering, enforcement surfaces

| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| New `dsx/frame/prereg.py`, registered at `verify` and `ship` only, at CRITICAL; registration and severity are complementary | Confident | `dsx/cli.py:90-103` (`GATE_PROFILES` — no `prereg` entry today; `verify`/`ship` tuples identical); `:107-112` (`GATE_THRESHOLDS` CRITICAL at plan/execute, HIGH at verify/ship); `ARCHITECTURE.md:231`. CRITICAL is not optional: `tests/test_known_bad_corpus.py:176` filters on `severity == "CRITICAL"`. Pattern to copy: `tests/test_frame_interference.py:169-185` |
| Five specific guards go red in the landing commit, each a designed forcing edit | Confident | (1) `dsx/frame/paradigm.py:66` + `tests/test_dsx.py:2849-2850`; (2) `dsx/frame/paradigm.py:47` + `tests/test_dsx.py:2830-2834`; (3) `scripts/gen-finding-catalogue.py:25-52` + `:184-190` + `tests/test_gen_finding_catalogue.py:174-181`; (4) `scripts/gen-finding-catalogue.py:65` — `_D05_ALLOWLIST_PREFIXES` is an inclusion list, not an exemption list; (5) `tests/test_gen_finding_catalogue.py:227` |
| Three codes: `DSX-PRE-010`, `-020`, `-030`, following the one-decade-per-concept convention with `-001` reserved | Likely | `07-CONTEXT.md:69-88` set the convention as a user decision. Shipped families confirm it: `DSX-VAL-010/011/020/021/030/040/041/050/060/070`, `DSX-INT-010/011/030/040`, `DSX-PAR-001/002/010/011`. Irreversible under brief D-06 |
| One new known-bad fixture registered in `_TARGET_DEFECT_CODES` (per-gate-point shape), with the more-conservative case as a unit-suite synthetic | Likely | `tests/test_known_bad_corpus.py:134-138` and `:259-265` are both live, with `:243-253` stating "neither shape subsumes the other". `weak-identification-mmm` uses the per-gate-point shape. `test_incidental_allowlist_names_no_slugs_own_target_code` forbids the allow-list shortcut. Post-mortem invariants at `:270-326` |

## Orchestrator Verification

Before presenting, the orchestrator independently re-read the load-bearing claims rather than
relying on the analyser's report. Confirmed by direct read: `EXIT_ERROR` occurrences and
`Report.exit_code()`; `frame_digest()`; `_write_decision_trail`'s swallow and its docstring
invariant; `clusters` returning zero matches across every `.yaml`; `_NOT_SHIPPED` and
`_PARADIGM_INDEPENDENT` both naming `"DSX-PRE-"`; `_D05_ALLOWLIST_PREFIXES` not covering it;
`GATE_PROFILES` having no `prereg` entry. All eight matched the analyser's report.

## Corrections Made

No corrections — the user selected "Yes, proceed" and all assumptions were written as locked
decisions, including the five open items with their proposed resolutions.

## Open Items Resolved At This Discuss

| Open item | Resolution | Recorded as |
|---|---|---|
| Final `DSX-PRE-0xx` numeric assignments | Three codes — `-010`, `-020`, `-030`. A rule referencing an undeclared fact folds into `-010`; `-011` is deliberately unspent. **Correction: this was never a recorded open item for Phase 10** — `STATE.md:57` names Phases 7, 8 and 11, and ROADMAP's Phase 10 entry has no "Open items" line (both verified). Settled here anyway, because brief D-06 makes the numbering irreversible regardless | 10-CONTEXT D-12 |
| Does Phase 10 coin a contract field for the mini-language's facts? | No. The fact namespace is a closed registry over fields that already exist. The brief's `clusters` example is illustrative, not binding | 10-CONTEXT D-04 |
| Does `DECISIONS.jsonl` stop being a side channel? | Yes. The docstring invariant is narrowed to the write path with the reason stated. A `verify` with no recorded plan-time header exits `2`, and the message must name `suppressions[]` so the M-07 grandfather path stays walkable | 10-CONTEXT D-09 |
| What does `declared_at: post_data` alone do? | Nothing. It stays legal and silent — blocking honest post-hoc declaration would make honesty more expensive than dishonesty, the brief-D-10 distortion | 10-CONTEXT D-10 |
| Is aborting the whole `verify` run on an unparseable rule acceptable? | Yes, accepted deliberately, matching the suppressions precedent. Recorded as a decision rather than left to be discovered | 10-CONTEXT D-03 |

## External Research

Spawned because the codebase analysis flagged two gaps: `brief.md` §7 — the section whose stated job
is to anchor D-05 citations — **names no pre-registration source at all**, making Phase 10 the first
v2.0.0 family that had to find its own; and it was unclear whether ROADMAP SC 5's "published
reference value" was satisfiable here at all.

- **Anchor selected: Gelman, A. & Loken, E. (2014)**, "The Statistical Crisis in Science",
  *American Scientist* 102(6):460-465. Full text read from two independent free copies
  (`sites.stat.columbia.edu/gelman/research/published/ForkingPaths.pdf` and
  `psychology.mcmaster.ca/bennett/psy710/readings/gelman-loken-2014.pdf`); page numbers taken from
  printed running footers and mapped page by page. Chosen because it is the only candidate whose
  stated claim is isomorphic to what the check mechanically does — p. 460's four-class enumeration
  distinguishes a prechosen test `T(y;φ)` with preregistered φ from `T(y;φ(y))` computed in an
  environment where a different test would have been performed. The declared fallback rule is φ; the
  executed procedure is φ(y). P. 463 supplies the unconditional claim: "For a p-value to be
  interpreted as evidence, it requires a strong claim that the same analysis would have been
  performed had the data been different."
- **Three live locator flags, raised rather than smoothed over.** The article has no numbered
  sections, tables or theorems, so naming one would be a fabricated locator. The symbol φ is
  garbled by optical character recognition in both available scans and is taken from the authors'
  2013 Columbia working paper, cited as a notation source only — that paper is unpublished with no
  DOI, venue or pagination. Nosek et al. (2018) was read at section-heading granularity only;
  per-sentence page numbers are unverified.
- **Secondary for REQ-P10-04 and SC 3's fixture: Simmons, Nelson & Simonsohn (2011)**,
  *Psychological Science* 22(11):1359-1366, DOI 10.1177/0956797611417632, p. 1365, "General
  Discussion" → "Nonsolutions" → "Correcting alpha levels." — a published rejection of the
  more-conservative-substitute defence: the substitution is itself a new degree of freedom.
- **Secondary for REQ-P10-02's remedy wording only: Nosek et al. (2018)**, *PNAS*
  115(11):2600-2606, via PMC5856500 — "Deviations … do not necessarily rule out testing predictions
  effectively." Explicitly the wrong anchor for REQ-P10-03/04.
- **Considered and not selected: Wagenmakers et al. (2012)**, *Perspectives on Psychological Science*
  7(6):632-638 — strong on the validity precondition ("the data may be used only once", p. 632) but
  its remedy is labelling, not machine-checkable reconciliation.
- **Conclusion on SC 5: take the `Structural criterion:` branch, not `Reference value:`.** Three
  grounded reasons — brief D-02 leaves no computed quantity to pin; four shipped precedents carry
  `Structural criterion:` alone (`dsx/frame/paradigm.py:350`, `:442`; `dsx/spec.py:868`, `:1015`) and
  `scripts/gen-finding-catalogue.py:78-80` accepts it; and the one available number is off-target.
- **Numbers verified but deliberately not asserted.** Simmons Table 1, p. 1361: 60.7% at p<.05 for
  all four degrees of freedom combined, over 15,000 simulated samples (the paper's prose rounds this
  to 61%). Claesen et al. (2021), *Royal Society Open Science* 8(10):211037, §3.3: 89% of studies had
  at least one undisclosed discrepancy. Goldacre et al. (2019), *Trials* 20:118: 87% of trials had
  discrepancies requiring a correction letter. The first measures four named researcher choices, not
  branch substitution; the latter two are prevalence rates in a literature, not properties of this
  code — asserting either would be the citation laundering brief D-05 exists to prevent. Chan et al.
  (2004), *JAMA* 291(20):2457-2465 was reached at abstract level only; no internal locator verified.
- **Follow-on action recorded in the context file:** `brief.md` §7 gains the Gelman & Loken record.
  This is a citation addition where none existed, not a brief-D-14 reversal.
