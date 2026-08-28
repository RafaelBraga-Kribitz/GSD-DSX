# Phase 9: Monitoring discipline, symmetric (`DSX-PAR-*`) - Discussion Log (Assumptions Mode)

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions captured in `09-CONTEXT.md` — this log preserves the analysis.

**Date:** 2026-08-12
**Phase:** 09-monitoring-discipline-symmetric-dsx-par
**Mode:** assumptions
**Calibration:** standard (no `USER-PROFILE.md`, no `preferences.vendor_philosophy` in config)
**Areas analyzed:** module layout / severity / gate registration; triggers, disjointness and the two
escapes; `DSX-PAR-002` scope vs the shipped `DSX-SPEC-085`; evidence artifacts (citations,
simulation, symmetry audit)

## Assumptions Presented

### Area A — Module layout, severity, gate registration

| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| All three codes ship inside the existing `dsx/frame/paradigm.py`; no new module, no `GATE_PROFILES` edit | Likely | `dsx/cli.py:88-101` (`paradigm` in all four profiles, `design` absent from `execute`); `dsx/frame/paradigm.py:49-57` `_NOT_SHIPPED` names all three codes; `ARCHITECTURE.md:359-368` |
| `DSX-PAR-010` and `DSX-PAR-011` both CRITICAL; `DSX-PAR-002` HIGH | Confident (pair) / Likely (PAR-002) | `dsx/cli.py:105-110` `GATE_THRESHOLDS`; brief D-12; ROADMAP SC 1; `dsx/spec.py:921-928` for the HIGH sibling |
| `tests/test_known_bad_corpus.py` must be restructured — three tests go red by design | Confident | `tests/test_known_bad_corpus.py:187-200`, `:202-229`, `:231-245`, `:49-59`; both fixtures declare `peeking_policy: uncontrolled_continuous` |

### Area B — Triggers, disjointness, the escapes

| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| Both halves trigger on `design.peeking_policy` alone, never `results.interim_looks`; disjoint from `DSX-EXP-060` by construction, no `design.py` change | Confident | `dsx/checks/design.py:446-449` early return, `:451` policy gate; no `results:` block exists at `dsx gate plan`; `tests/test_dsx.py:678-690` |
| Phase 9 coins `inference.threshold_calibration`, `prior_justification`, `decision_threshold`; extends `_INFERENCE_FIELDS` + drift test | Likely | Repo-wide grep: names appear only in `brief.md:209-213` (commented) and research files; `dsx/spec.py:852-855`; `tests/test_dsx.py:504-511`; no unknown-key check under `inference:` (`dsx/spec.py:843-848`) |
| Retype-escape closed structurally by exhaustive `PARADIGMS` coverage | Likely | `dsx/spec.py:245-248` (two members); `dsx/frame/paradigm.py:38-41` keyed-by-every-member idiom with set-equality test |
| Undeclared-paradigm fires neither half (brief D-10) and needs a separate door-closer | Likely | brief D-10; `Severity.INFO = 10` below every threshold |

### Area C — `DSX-PAR-002` scope

| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| `PARADIGM_JUSTIFICATIONS` already exists; `DSX-PAR-002` owns requiredness + symmetry, not membership | Likely | `dsx/spec.py:251-265` (seven members, D-12 symmetry comment at `:250`); `_INFERENCE_MEMBERSHIP` `:857-861`; `examples/bad-ANALYSIS-SPEC.yaml:238`; `tests/test_dsx.py:513-528`; absence silent via `is_blank(value): continue` `:918-919` |
| "No reason ranked above another" enforced mechanically by a 7×2 parametrised test | Confident | `dsx/spec.py:250` states it as an unenforced comment; `PITFALLS.md:421-467` |

### Area D — Evidence artifacts

| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| REQ-P9-02/03 misattribute the bound; Theorem 1 does not state `1/(K+1)` | Confident (after research) | arXiv:1602.05549 LaTeX source, read directly |
| `K` is posterior odds; `K = p/(1-p)` legitimate; `1/(K+1) = 1-p` identically | Confident (after research) | Paper §1, §3.1, §3.2, §5.1, §7 |
| Ville distinction correct and stronger — Ville never cited in Deng et al. | Confident (after research) | Paper §5, §6.2; Ramdas et al. (2023) §2.5 |
| `inflation_from_peeking()` values right, 1969 locator not verifiable | Confident (after research) | Independent quadrature + Monte Carlo; OUP/Wiley/JSTOR paywalls |
| Simulation is a stdlib-only seeded unittest under `tests/`, running by default | Likely | No `pyproject.toml`/`requirements.txt`/`setup.py` in repo; `scripts/check.sh:6-7`; `FEATURES.md:168-191` |
| Location of the REQ-P9-06 symmetry audit | **Unclear** | Phase 6 artifact precedent (`.planning/phases/06-*/`) vs `references/` + PR-branch filtering |

## Verification Performed by the Orchestrator

The analyzer's load-bearing citations were spot-checked directly before being written into
`09-CONTEXT.md` as canonical, per the project's verification-before-claiming agreement. All checked
references were confirmed accurate:

- `dsx/frame/paradigm.py:49-57` — `_NOT_SHIPPED` contains all three Phase 9 codes. Confirmed.
- `dsx/cli.py:88-101` / `:105-110` — `paradigm` in all four profiles; `design` absent from `execute`;
  thresholds CRITICAL/CRITICAL/HIGH/HIGH. Confirmed.
- `dsx/spec.py:852-855` — `_INFERENCE_FIELDS` holds exactly six names; the surrounding comment
  independently confirms there is no unknown-key check for the block. Confirmed.
- `dsx/spec.py:245-265` — `PARADIGMS` (2 members), `PARADIGM_JUSTIFICATIONS` (7 members), the D-12
  symmetry comment. Confirmed.
- `dsx/checks/design.py:444-451` — early return on missing `results.interim_looks`, policy gate on
  `("", "fixed_horizon")`. Confirmed.

**One item was escalated beyond the analyzer's finding.** The analyzer rated the undeclared-paradigm
escape `Likely`. Reading `_validate_inference_shape` directly (`dsx/spec.py:868-941`) upgraded it to
a verified open hole: the function returns early when `inference:` is absent or empty (`:886-888`)
**and** skips blank values inside the membership loop (`:917-919`). Omitting `inference.paradigm`, or
the whole block, produces no finding at all today. This became decision D-07 with a preferred
mechanism and an explicitly unresolved severity question flagged for planning rather than settled
silently.

## Corrections Made

No corrections — the user reviewed all four areas and selected "Yes, proceed", accepting the
recommended option on each open item:

- **D-15 (symmetry audit location, rated Unclear):** recommended option taken —
  `references/paradigm-symmetry.md` rather than `.planning/phases/09-*/`, because `.planning/` is
  filtered out of PR branches and ROADMAP SC 5 requires a committed audit an external reader can see.
- **D-13 (`inflation_from_peeking()` docstring upgrade, a STATE.md open item):** recommended option
  taken — perform the upgrade with an explicit unverified-locator flag, on the grounds that it is
  docstring-only in a module with no `report.add` calls and therefore cannot alter any finding,
  catalogue row, or `DSX-EXP-060` output.
- **D-05 (three new `inference:` fields):** recommended option taken — coin all three rather than
  only `threshold_calibration`, because the narrower option leaves `DSX-PAR-011` with no satisfaction
  path.
- **D-10 (citation correction):** recorded as a decision that amends REQ-P9-02/03 and ROADMAP SC 2/3.

## External Research

Spawned because the codebase analysis flagged three gaps it could not close, one of which was a
direct contradiction between an in-code "unverified locator" flag and a research file's claim of
verification.

**Method note:** the researcher bypassed the paywall/rendering problem by downloading the arXiv
LaTeX source (`arxiv.org/e-print/1602.05549` → `KDD2015-Submission.tex`) and reading the theorem
environment directly. This matters — its own ar5iv fetch of this paper **garbled Table 1**,
transposing the Type-I row with the Early Stop Rate row. `FEATURES.md`'s stated provenance ("verified
via ar5iv") happened to read correctly but is not a reliable method for this paper.

### Deng, Lu & Chen (2016) Theorem 1 — VERIFIED against primary source

The paper contains exactly one numbered theorem (`\begin{thm}\label{mainthm}`, §1) and **no**
corollary, lemma or proposition. Theorem 1 states an optional-stopping *equality*:
`P(H₁|PostOdds_τ)/P(H₀|PostOdds_τ) = PostOdds_τ`, for any proper stopping time, with known prior odds.

`1/(K+1)` appears in three unnumbered prose locations: §1 before the theorem (fixed-horizon
interpretation), §1 after the theorem (optional-stopping version), and §3.2 as the operational bound
— "rejecting H₀ when observing a posterior odds no less than K exposes us to a risk of false
discovery at most `1/(1+K)`". §1's two sentences say "rejecting **H₁**" where the quantity given is
`P(H₀|Data)`; §3.2 is the coherent reading and is the one to quote.

**Impact:** REQ-P9-02 and REQ-P9-03 misattribute the bound. The in-code unverified-locator flags at
`dsx/frame/paradigm.py:66-72` and `dsx/spec.py:878-881` can be removed, but only if the replacement
does not claim Theorem 1 states `1/(K+1)`. → decision D-10.

*Residual:* the IEEE DSAA 2016 published version was not accessible, so renumbering there cannot be
ruled out — though with a single theorem in the paper, "Theorem 1" is not at risk.

### `K` is posterior odds, not Bayes factor — VERIFIED against primary source

Both prose occurrences and §3.2's rule say "posterior odds K". Posterior odds equals the Bayes factor
only when prior odds are 1:1, which the paper states at §3.1 and §5.1 — which is why its Table 1
simulation can call K=9 a Bayes-factor threshold.

`K = p/(1-p)` is a legitimate derivation, but `1/(K+1) = 1-p` identically: at p=0.95, K=19 and
`1/20 = 0.05` is a restatement of the declared threshold. Theorem 1's contribution is that the
identity survives evaluation at a random stopping time. Theorem 1 requires *known prior odds*, and §7
warns that conditioning on "null is true or alternative is true" is the common mistake — so the
derivation holds only if the declared `p` is a real posterior computed with the operator's actual
prior odds (§6.2 puts those "less than 20%" for most metrics).

**Impact:** → decisions D-11 and the D-11-derived deferred idea. Two errors identified in
`FEATURES.md:157-166`.

### Ville's inequality is a different result — VERIFIED against primary sources

The word "Ville" does not appear in Deng et al. at all. Their proof (§5) is the likelihood-ratio
identity / change of measure — an equality, not a maximal inequality. Ville gives
`P(sup_t M_t ≥ α) ≤ 1/α` (Ramdas, Grünwald, Vovk & Shafer, *Statistical Science* 38(4), 2023,
arXiv:2210.01948 §2.5).

The distinction, in the paper's own words (§6.2): Type-I error is "the chance of false rejection when
H₀ is true", FDR is "the chance of false rejection when decided to reject H₀", and "there is no
simple relationship between the two". Different conditioning event, hence the different denominator.
Table 1 shows both at once — type-I error rose 0.018 → 0.060 while FDR held at its designed ceiling.

The point-null / law-of-iterated-logarithm formulation is confirmed a distinct third result (§1 and
§6.1) with no ceiling.

**Impact:** confirms and strengthens the repo's existing guard; `FEATURES.md:145`'s
"Ville's-inequality-type bound" label is the exact conflation the docstring must prevent.
→ decision D-12.

*Caveat:* Ville's inequality was verified from Ramdas et al. (peer-reviewed, the standard modern
reference) rather than from Ville (1939) itself.

### Armitage, McPherson & Rowe (1969) provenance — PARTIALLY VERIFIED

**Values verified by independent computation, not by citation.** Exact numerical quadrature
(recursive convolution of the sub-density over the continuation region, FFT, grid-refined to
convergence) cross-checked by seeded Monte Carlo (4×10⁶ paths). Setup: iid N(0,1) increments, equal
group sizes, K equally spaced analyses, reject the first time |Z_k| > 1.959964 (two-sided nominal
α=0.05).

| looks | repo anchor | quadrature | Monte Carlo (±95%) |
|---|---|---|---|
| 2 | 0.083 | 0.08314 | 0.08295 ±0.00027 |
| 3 | 0.107 | 0.10728 | 0.10704 ±0.00030 |
| 4 | 0.126 | 0.12620 | 0.12590 ±0.00033 |
| 5 | 0.142 | 0.14171 | 0.14151 ±0.00034 |
| 10 | 0.193 | 0.19338 | 0.19317 ±0.00039 |
| 20 | 0.248 | 0.24793 | 0.24781 ±0.00042 |

Notable: **the repo's 0.248 at 20 looks is correct and the widely-circulated 0.246 is not** — both
methods agree at 0.2479, more than 5 Monte Carlo standard errors away. Before this pass the 20-look
value had no cross-check of any kind (`FEATURES.md:212-218` covers only 5 and 10 looks, against
Lakens, a secondary source).

**Provenance NOT verified.** The 1969 paper is paywalled at OUP, Wiley and JSTOR; only the
bibliographic record and abstract were confirmed. Jennison & Turnbull was equally unobtainable and
the researcher explicitly declined to invent a table number. The abstract shows the paper covers
three distributional cases (binomial, normal, exponential), so any citation must name the normal,
known-variance, equal-group-size case.

**Impact:** → decision D-13. The docstring upgrade proceeds, citing Armitage et al. (1969) as the
origin of the *result*, stating the numerals as computed values with their exact setup, and carrying
an explicit unverified-locator flag. No table or page may be named.
