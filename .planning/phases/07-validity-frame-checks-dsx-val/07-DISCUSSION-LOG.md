# Phase 7: Validity frame checks (`DSX-VAL-*`) - Discussion Log (Assumptions Mode)

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions captured in `07-CONTEXT.md` — this log preserves the analysis.

**Date:** 2026-08-10
**Phase:** 07-validity-frame-checks-dsx-val
**Mode:** assumptions
**Areas analyzed:** module layout and code assignment; dependence method-family shape; free-text
decidability; fixtures, template and build plumbing; D-05 citation sourcing

## Assumptions Presented

### Module layout, code assignment and severity

| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| One `dsx/frame/val.py`, single `check(spec)`, registered in plan/verify/ship but not execute | Confident | `dsx/frame/paradigm.py:60`; `dsx/cli.py:88-104`; `research/ARCHITECTURE.md:160-162`, `:235-238` |
| Decade-per-concept code numbering with gaps; reject `DSX-VAL-001` | Likely | `REQUIREMENTS.md:97-100` fixes 020/040/041; `references/finding-codes.md` has zero `DSX-VAL` codes; `06-CONTEXT.md:222-224` |
| CRITICAL on 010/020/030/040, HIGH on the rest | Likely | `dsx/cli.py:105-110`; `ROADMAP.md:212-220` forces CRITICAL on 020/040 and HIGH on 041; `research/PITFALLS.md:200-227` |

### Dependence method-family shape (named open item 1)

| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| Field stays single-valued; structure→methods map lives in code, not the vocabulary | Likely | `research/ARCHITECTURE.md:298-324`; M-09 and `dsx/spec.py:717-718`; `dsx/spec.py:816-835` scalar `normalize()`; `06-CONTEXT.md:340-343` naming rule |

### Free-text decidability under D-01/D-02

| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| Falsifier adjudicated by placeholder list + discriminating-predicate lexicon | **Unclear** | `dsx/checks/narrative.py:17-21`, `dsx/checks/claims.py:107-113`, `:350-370` as precedent; all four committed falsifiers pass, `bad-ANALYSIS-SPEC.yaml:211` and `templates/ANALYSIS-SPEC.yaml:288` fail; `research/PITFALLS.md:213-214` |
| Sampling frame and measurement checked for presence and internal consistency only | Likely | `examples/good-ANALYSIS-SPEC.yaml:339-342` would fail any text-comparison rule strong enough for `brief.md:172-175`; D-08 forbids that; `research/PITFALLS.md:643` |
| Missingness as a lookup with MAR+complete-case at HIGH; DEFF as a fixed illustrative constant | Likely | `examples/good-ANALYSIS-SPEC.yaml:344-347`; `research/FEATURES.md:287`, `:301-305`, `:68-74`; no `m`/`ICC` field exists in the contract |
| `DSX-VAL-020` decides "finer than" as string inequality | Likely | `units.*` absent from `_VALIDITY_FRAME_MEMBERSHIP` (`dsx/spec.py:719-728`); `templates/ANALYSIS-SPEC.yaml:291` field semantics; resolves the `REQUIREMENTS.md:97` vs `:98`/`ROADMAP.md:220` wording tension |

### Fixtures, template and build plumbing

| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| Template must be amended or a shipped test deleted | **Unclear** | `dsx/cli.py:558-567`; `tests/test_dsx.py:1390-1393`; `templates/ANALYSIS-SPEC.yaml:288`, `:291-292`, `:296-298`, `:331`; `06-CONTEXT.md:119-126` |
| Known-bad corpus fixtures change, tests do not | Confident | `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml:113-126`; `tests/test_known_bad_corpus.py:41-45`, `:193-200` |
| Three build-script edits plus `_NOT_SHIPPED` removal or the family is invisible | Confident | `scripts/gen-finding-catalogue.py:179-181`, `:59`, `:251-254`, `:75-79`; `dsx/frame/paradigm.py:45-50` |
| `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` does not exist and must be created | Confident | Directory listing of `examples/known-bad/`; `ROADMAP.md:212-213` names it |

## Corrections Made

No assumptions were overturned. The user was asked four questions covering the two named open
items and the two Unclear assumptions, and selected the recommended option in each case.

### Falsifier discrimination test
- **Options presented:** word-list test / blank-and-placeholder only / structured falsifier field
- **User selected:** word-list test (recommended)
- **Reason given by the recommendation:** blank-only makes REQ-P7-01's second clause decorative;
  a structured field reopens the Phase 6 contract that shipped as a breaking release; the word
  list is cheap to loosen on the first false positive.

### `dependence.method_family_required` shape (open item 1)
- **Options presented:** single value with the map in `dsx/spec.py` / single value with the map in
  `dsx/frame/val.py` / list-valued field
- **User selected:** single value, map in `dsx/spec.py` (recommended)
- **Reason:** Phase 11 keys `references/families.yaml` on the same taxonomy and can import from
  shared infrastructure rather than from a check module; a list-valued field would require editing
  shipped Phase 6 membership code, the template, all four fixtures and the round-trip tests.

### `DSX-VAL-*` numeric code assignment (open item 2)
- **Options presented:** decade per concept with gaps / sequential 001-009
- **User selected:** decade per concept with gaps (recommended)
- **Reason:** both are expensive to undo under D-06; only one leaves room for Phase 11's
  VAL-adjacent codes.

### Template behaviour at the plan gate
- **Options presented:** amend template placeholder values so `dsx init` still passes / let it
  block and replace the test
- **User selected:** amend template values (recommended)
- **Reason:** a first-run failure teaches new users the gate is an obstacle, which is the adoption
  cliff Phase 6 deliberately engineered against.

### Decided without asking
- **Good-fixture missingness.** `examples/good-ANALYSIS-SPEC.yaml:347` changes `method_implied`
  from `complete_case` to `multiple_imputation` rather than adding a "rate is zero" exemption to
  `DSX-VAL-060`. An exemption would make `rate: 0` the cheapest way past the check
  (`research/PITFALLS.md:643`). One field value; cheap to undo. Stated in the presentation.

## External Research

Seven topics researched against primary documents on 2026-08-10, because the analyzer flagged that
the repository cannot supply D-05-compliant sources for three of the nine requirements and cannot
supply exact locators for two more.

- **Estimand decomposition (REQ-P7-01):** ICH E9(R1) §A.3.3 "Estimand attributes" confirmed
  verbatim, plus §A.3.2 for intercurrent events. Maps to **four** of the project's five fields —
  `falsifier` has no counterpart, and `time_window` is an ICH sub-specification, not an attribute.
  Hernán & Robins (2016) Table 1 and *Causal Inference: What If* §1.2 confirmed as better fits for
  `time_window`. **The five-field set is project-defined.**
  (Source: EMA Step 5 PDF; PMC4832051; miguelhernan.org)
- **Falsifiability (REQ-P7-01):** Popper (1959/2002) Part I, Ch. 1, §6 "Falsifiability as a
  Criterion of Demarcation", pp. 17-18, confirmed verbatim from full text. Supplies the demarcation
  principle, **not** an operational discrimination test. Mayo (2018) returned **UNVERIFIED** — Tour
  structure confirmed, no numbered sections available. (Source: archive.org full text; Cambridge TOC)
- **Design effect (REQ-P7-02):** **The planned 3.45 worked value is not published anywhere.**
  Kish (1965) §8.2 p. 258 confirmed for the Deff definition and pp. 161-162 for the ICC, but no
  *section* number for the formula — flagged UNVERIFIED. Two published worked values found:
  Cochrane Handbook §23.1.4.1 (ICC 0.02, M 29.8 → 1.576) and UN handbook Ch. VI ¶72 (ICC 0.05,
  b 17 → 1.80). Cochrane recommended.
  (Source: Park & Lee 2001 and Chromy 2014, ASA SRMS Proceedings; Cochrane Handbook v6.5 ch. 23;
  UN Studies in Methods Series F No. 96)
- **Gelman, Simpson & Betancourt (REQ-P7-05):** §3.3 confirmed for the weak-identification thesis,
  §1.2 for the prior taxonomy; journal title wording matches the project's (the arXiv preprint says
  "generally", the journal says "often"). **No published source partitions `CONSTRAINT_SOURCES` by
  parameter-scale information** — `design_restriction` has no counterpart in the paper at all. The
  partition is project-defined and the docstring must say so. Section numbers verified from the
  arXiv final version only; MDPI blocks automated fetch. (Source: arXiv 1708.07487; Crossref)
- **Missingness (REQ-P7-07):** Little & Rubin 3rd ed. Ch. 3 title confirmed; §3.2 "Complete-Case
  Analysis" is high-confidence from a publisher-licensed table of contents but was not directly
  read. **No printed MCAR/MAR/MNAR × method validity table exists** — do not describe it as one.
  White & Carlin (2010) confirmed the MAR characterisation and its exception, which is why the
  check ships at HIGH rather than CRITICAL. (Source: Wiley DOI 10.1002/9781119482260.ch3;
  Vink 2022 *Psychometrika* review; PMID 20842622)
- **Sampling frame (REQ-P7-06):** Lohr 3rd ed. (2021) Ch. 1 §1.2/§1.3/§1.3.4 and Ch. 16 §16.1
  confirmed from the author's official table of contents. **Edition must be pinned** — section
  numbers differ between 2nd and 3rd. (Source: sharonlohr.com TOC; PMC11610318)
- **Measurement (REQ-P7-08):** Cronbach & Meehl (1955), "The Nomological Net", principle 3, p. 290,
  confirmed verbatim with original *Psychological Bulletin* pagination — states the criterion almost
  word for word. Went from the phase's completely unsourced requirement to its best-sourced.
  (Source: psychclassics.yorku.ca, scholarly reproduction preserving original pagination)

### Follow-on actions the research generated

1. `brief.md` §7 (`:434-451`) needs six sources added (ICH E9(R1), Kish, Cochrane Handbook,
   Hernán & Robins 2016, Popper, Cronbach & Meehl) and two editions pinned (Lohr, Little & Rubin).
2. `.planning/research/FEATURES.md:50-52` carries the unsourced 3.45 value and should be corrected,
   or the next agent to read it reintroduces the number.
