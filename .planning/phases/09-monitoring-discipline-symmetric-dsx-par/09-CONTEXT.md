# Phase 9: Monitoring discipline, symmetric (`DSX-PAR-*`) - Context

**Gathered:** 2026-08-12 (assumptions mode)
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 9 delivers the **symmetric monitoring-discipline family** — three finding codes that make
uncontrolled continuous monitoring block under *both* declared paradigms, at identical severity,
with no cheaper dishonest escape on either side.

It ships:

- `DSX-PAR-010` — a frequentist design declaring `design.peeking_policy: uncontrolled_continuous`
  with no alpha-spending and no sequential method, reusing the existing `inflation_from_peeking()`
  table (REQ-P9-01).
- `DSX-PAR-011` — a Bayesian design declaring the same policy with neither threshold calibration
  nor a justified informative prior, asserting the `1/(K+1)` risk figure (REQ-P9-02, REQ-P9-03).
- `DSX-PAR-002` — requiredness and symmetry for `inference.paradigm_justification` (REQ-P9-04).
- Closure of the paradigm-retype escape in both directions, and of the *undeclared*-paradigm
  escape (REQ-P9-05).
- A committed symmetry audit of the cheapest dishonest satisfaction path per half (REQ-P9-06).
- A seeded, reproducible simulation under `tests/`, never on the gate path (REQ-P9-07).

**`DSX-PAR-010` and `DSX-PAR-011` are atomic (brief D-12).** Both ship or neither ships, at
identical severity. This phase cannot be marked complete with one half delivered — a half-shipped
pair is precisely the silent paradigm-steering the family exists to prevent.

**Out of this phase's boundary:** `DSX-VAL-*` (Phase 7), `DSX-INT-*` (Phase 8), `DSX-PRE-*`
(Phase 10), `DSX-ADM-*` (Phase 11). No Bayesian *procedure recommendation* or admissibility —
that is the gated backlog (brief §6.5). No prior justification quality judgement, no prior
sensitivity, no convergence declarations — deferred under brief D-12a, and their frequentist
mirrors are not written.

Requirements: REQ-P9-01 … REQ-P9-07 (7 requirements, see `.planning/REQUIREMENTS.md`).

</domain>

<decisions>
## Implementation Decisions

> **Numbering note.** `D-nn` below are **phase-local** decision ids for Phase 9, following the
> precedent set by `06-CONTEXT.md`. The project-wide decision table in `brief.md` §4 is referenced
> throughout as **brief D-nn**, and `PROJECT.md`'s milestone table as **M-nn**. They are different
> namespaces; do not conflate `D-05` (this file, the simulation) with brief D-05 (the citation rule).

### Locked upstream — do NOT re-litigate

- `brief.md` §4 (brief D-01…D-14) and §5 (contract shape) are binding inputs (`PROJECT.md` §Context).
- **M-01**: `DSX-PAR-010` is a distinct code; `DSX-EXP-060` is untouched.
- **M-02**: there is no `inference.stopping_rule` field; the pair reads the existing
  `design.peeking_policy`. `DSX-SPEC-086` already redirects anyone who declares the removed field
  (`dsx/spec.py:930-941`).
- **M-03**: `PEEKING_POLICIES` already carries `uncontrolled_continuous` (shipped Phase 6).
- **brief D-02**: no test statistic or posterior is computed on the gate path.
- **brief D-04**: never block to teach — emit decision records; `dsx explain` renders them.
- **brief D-06**: finding codes are never renumbered.
- **brief D-10**: an unsupported paradigm is never blocking *on its own*.
- **brief D-11 does not constrain this family.** Frame-layer checks never read `paradigm` — but
  `DSX-PAR-*` exists precisely to branch on it (`06-CONTEXT.md` §Integration Points).
- **brief D-12**: the pair ships symmetrically; symmetry is the scoping rule.
- The name "prior-averaged **Ville** bound" is **retired**. Deng, Lu & Chen (2016) and Ville's
  inequality are different results (see D-08 below).

### Module layout, severity, gate registration

- **D-01:** All three codes ship inside the existing `dsx/frame/paradigm.py`. No new module, and
  no `GATE_PROFILES` edit ships in Phase 9. `paradigm.py` is 163 lines — nowhere near needing a
  split. `"paradigm"` is already registered at all four gate points (`dsx/cli.py:88-101`,
  **verified**), which is exactly the footprint the pair needs; `"design"` is absent from the
  `execute` profile, so a new module would need four separate profile edits to match. `_NOT_SHIPPED`
  (`dsx/frame/paradigm.py:49-57`, **verified** — it names `DSX-PAR-002`, `DSX-PAR-010` and
  `DSX-PAR-011` explicitly) must be edited wherever the checks live.
  - **Consequence the planner must honour:** `tests/test_dsx.py:2585-2607` asserts every
    `_NOT_SHIPPED` prefix resolves to zero known codes. Each of the three entries must be removed
    in the same commit that lands its code, or the suite goes red.

- **D-02: `DSX-PAR-010` and `DSX-PAR-011` both ship at `CRITICAL`. `DSX-PAR-002` ships at `HIGH`.**
  Severity *is* the gate point here — `GATE_THRESHOLDS` is CRITICAL at plan/execute and HIGH at
  verify/ship (`dsx/cli.py:105-110`, **verified**), so only CRITICAL makes ROADMAP SC 1's "exits `1`
  at `dsx gate plan`" true. brief D-12 forces the two halves to be identical; an asymmetric
  CRITICAL/HIGH split would itself be the D-12 violation. `HIGH` for `DSX-PAR-002` matches its
  nearest sibling `DSX-SPEC-085` (`dsx/spec.py:921-928`) and keeps a missing *justification* from
  blocking plan the way a genuinely uncontrolled *design* does.

- **D-03:** `tests/test_known_bad_corpus.py` is restructured in this phase — three tests going red is
  the designed forcing edit, not a defect. `test_every_spec_passes_the_critical_threshold_gate_points`
  (lines 187-200) asserts *every* known-bad fixture exits `0` at plan and execute; both monitoring
  fixtures declare `peeking_policy: uncontrolled_continuous`. `test_ship_gate_findings_are_all_documented_incidental_corpus_gaps`
  (202-229) fails on any new blocking code, and `test_incidental_allowlist_names_no_target_family_code`
  (231-245) explicitly **forbids** the obvious fix of adding `DSX-PAR-01x` to `_INCIDENTAL_GAP_CODES`.
  - **Required shape of the fix:** a per-fixture *expected-caught-defect* set. A fixture that its
    target check now catches must assert exit `1` **naming that code**; fixtures whose target family
    has not yet shipped keep the current exit-`0` assertion. The allow-list stays for genuinely
    incidental gaps only. Do not weaken the guard at 231-245 — it is the thing preventing the pair
    from being neutralised by allow-list.

### Triggers, disjointness, and both escapes

- **D-04:** Both halves trigger on `design.peeking_policy == "uncontrolled_continuous"` alone. Neither
  reads `results.interim_looks`. No change to `dsx/checks/design.py`. `_check_peeking` returns
  early when `results.interim_looks` is absent (`dsx/checks/design.py:446-449`, **verified**) and
  only fires for `policy in ("", "fixed_horizon")` (`:451`) — structurally unreachable on either
  monitoring fixture. Decisively: **at `dsx gate plan` there is no `results:` block at all**, so a
  trigger depending on `interim_looks` would silently become verify/ship-only and break ROADMAP SC 1.
  Disjointness from `DSX-EXP-060` is therefore by construction, and the Phase 6 parametrised test
  (`tests/test_dsx.py:678-690`) is inherited as the guard against double-firing.

- **D-05:** Phase 9 coins three new `inference:` fields — `threshold_calibration`,
  `prior_justification`, `decision_threshold` — and extends `_INFERENCE_FIELDS`, its drift-guard
  test, `templates/ANALYSIS-SPEC.yaml` and `dsx vocab`. Repo-wide grep finds these names only in
  `brief.md:209-213` (commented out) and the research files — never in `dsx/spec.py`, the template,
  or any fixture. Without them **`DSX-PAR-011` has no satisfaction path at all**: its only possible
  trigger would be "paradigm is bayesian and policy is uncontrolled_continuous", which is
  unsatisfiable and makes REQ-P9-06's "disjunctive `prior_justification` route" meaningless.
  - `_INFERENCE_FIELDS` holds exactly six names (`dsx/spec.py:852-855`, **verified**) and
    `tests/test_dsx.py:504-511` asserts that tuple literally — it must be extended in the same commit.
  - **There is no unknown-key check under `inference:`** — `dsx/spec.py:843-848` says so in prose.
    New keys would therefore be read silently while the template never scaffolds them and `dsx vocab`
    never shows them. Extending the template and the vocabulary dump is not optional polish; it is
    what makes the fields discoverable by an operator.
  - **Apply the collision habit before coining** (see `<specifics>`): grep `dsx/`, `tests/`,
    `examples/`, `references/`, `templates/` for each of the three names first.

- **D-06:** The paradigm-retype escape is closed structurally, by exhaustive `PARADIGMS` coverage —
  not by two hand-written `if` branches. `PARADIGMS` has exactly two members
  (`dsx/spec.py:245-248`, **verified**), and `_PARADIGM_CONDITIONAL` (`dsx/frame/paradigm.py:38-41`)
  already establishes the house idiom: a dict keyed by every member with a set-equality test. The
  property to make provable is *"for every member of `PARADIGMS`, an uncontrolled-continuous design
  resolves to some blocking code."* REQ-P9-05's both-directions test then falls out of the structure
  rather than being two bespoke assertions.

- **D-07:** The *undeclared*-paradigm escape is real, currently open, and must be closed in this phase
  — but the planner verifies the mechanism before writing it.
  **Verified during discuss:** `_validate_inference_shape` returns early when `inference:` is absent
  or empty (`dsx/spec.py:886-888`), and skips blank values inside the membership loop
  (`dsx/spec.py:917-919`). So **today, omitting `inference.paradigm` — or the whole `inference:`
  block — produces no finding whatsoever.** The moment the pair ships, that becomes the cheapest
  escape from *both* halves: the exact brief-D-10 distortion, arriving through a door brief D-10 was
  not written to guard.
  - **Preferred mechanism: `DSX-PAR-002` carries the requiredness** — a declared
    `peeking_policy: uncontrolled_continuous` with no `inference.paradigm` is a `DSX-PAR-002`
    finding. This coins **no new irreversible code number** (brief D-06) and keeps the whole escape
    story inside one family, so REQ-P9-06's audit can enumerate every escape path in one place.
  - Rejected alternative: a new `DSX-SPEC-08x` requiring `inference.paradigm` conditionally. It
    matches the `question_type`-gated requiredness pattern (M-06), but spends a permanent code number
    and splits the escape story across two families.
  - **This does not violate brief D-10.** D-10 forbids blocking *because a paradigm is unsupported*.
    Requiring a declaration that is load-bearing for a check that is about to fire is requiredness,
    not a judgement about the paradigm's value.
  - **Severity consequence to settle in planning:** under D-02, `DSX-PAR-002` is HIGH, which does
    not block at `plan` — so if requiredness rides on `DSX-PAR-002` the escape is closed at
    verify/ship but not at plan. The planner must either accept that asymmetry with a stated reason,
    or split requiredness onto its own CRITICAL code. **Do not settle this silently.**

### `DSX-PAR-002` scope

- **D-08:** `PARADIGM_JUSTIFICATIONS` already exists — Phase 9 coins no vocabulary. `DSX-PAR-002` owns
  *requiredness and symmetry*; `DSX-SPEC-085` keeps *membership*. The vocabulary is at
  `dsx/spec.py:251-265` (**verified**) with all seven brief §5.2 members and the comment "No
  description ranks one reason above another (D-12 symmetry)" at `:250`. It is in `_VOCABULARIES`
  (`:296`) so `dsx vocab` already dumps it, and `_INFERENCE_MEMBERSHIP` (`:857-861`) already
  validates it, with `examples/bad-ANALYSIS-SPEC.yaml:238` carrying
  `paradigm_justification: gut_feeling # → DSX-SPEC-085` and a test asserting exactly three
  `DSX-SPEC-085` findings.
  - **Absence is what is silent today** (`is_blank(value): continue`, `dsx/spec.py:918-919`) — that
    gap is `DSX-PAR-002`'s content.
  - A `DSX-PAR-002` that re-checked membership would double-fire with `DSX-SPEC-085` on
    `examples/bad-ANALYSIS-SPEC.yaml` — two codes, one defect, in a repo whose premise is one stable
    fact per code. Removing the row from `_INFERENCE_MEMBERSHIP` to avoid that would turn
    `tests/test_dsx.py:527` red and silently narrow a shipped code. **Do neither.**

- **D-09:** "No reason ranked above another" is enforced mechanically — one membership path, no
  per-member branching and no per-paradigm branching, proven by a 7×2 parametrised test.
  `dsx/spec.py:250` states the property as a comment with nothing enforcing it. The failure mode
  brief D-12 names is that `team_convention` or `vendor_constraint` quietly acquires a "weaker
  reason" code path later and nothing catches it. `PITFALLS.md:421-467` is the argument that D-12
  compliance must be checked on *cost of satisfaction*, not on code existence.

### Citations — external research applied, and a requirement correction

- **D-10:** REQ-P9-02 and REQ-P9-03 misattribute the bound, and their wording is corrected here.
  Deng et al.'s Theorem 1 does NOT state `1/(K+1)`.
  Verified against the arXiv LaTeX source (`arxiv.org/e-print/1602.05549`, `KDD2015-Submission.tex`),
  read directly because ar5iv **garbles Table 1** for this paper (it transposes the Type-I and
  Early-Stop-Rate rows). The paper contains exactly **one** numbered theorem and **no** corollary,
  lemma or proposition.
  - **Theorem 1** (§1, Introduction) states an optional-stopping *equality*:
    `P(H₁|PostOdds_τ)/P(H₀|PostOdds_τ) = PostOdds_τ`, for any proper stopping time, **with known
    prior odds**.
  - **`1/(K+1)` is unnumbered prose** — §1 (immediately after Theorem 1) and, in its operational
    *bound* form, **§3.2**: "rejecting H₀ when observing a posterior odds no less than K exposes us
    to a risk of false discovery at most `1/(1+K)`".
  - **Cite §3.2 for the bound, Theorem 1 for what licenses it under optional stopping.** Do not
    quote §1's two sentences: they say "rejecting **H₁**" where the quantity given is `P(H₀|Data)` —
    the paper's own slip. §3.2 is the coherent reading.
  - Equality vs bound: conditioning on posterior odds *exactly* K it is an equality; it becomes
    "at most" only under a *stop when odds ≥ K* rule, because of overshoot. The paper's Table 1
    shows the overshoot cost — designed FDR 0.10, realised 0.09.
  - **This is not a brief-D-14 reversal.** REQ-P9-02/03 are requirements in `REQUIREMENTS.md`, which
    sits outside both `brief.md` §4's D-table and `PROJECT.md`'s M-table — the same reasoning
    `06-CONTEXT.md` applied to PROJECT.md's version-rationale amendment. It is a factual correction
    to a citation and must be **written into `REQUIREMENTS.md` REQ-P9-02/03 and ROADMAP Phase 9
    SC 2/SC 3**, not just noted here.

- **D-11:** `K` is the posterior odds. `K = p/(1-p)` is a legitimate derivation, but the docstring must
  state that `1/(K+1) = 1-p` identically — otherwise the check reads as circular.
  The paper says "posterior odds K" in both prose occurrences and in §3.2's rule. Posterior odds
  equals the Bayes factor **only when prior odds are 1:1**, which the paper states at §3.1 and §5.1 —
  that is why its Table 1 simulation can call K=9 a Bayes-factor threshold. At p=0.95: K=19 and
  `1/20 = 0.05` — **but 0.05 is just `1-p`.** The non-trivial content Theorem 1 supplies is that this
  identity *survives evaluation at a random stopping time*. That sentence is what makes
  `DSX-PAR-011` meaningful rather than a tautology, and it belongs in the docstring.
  - **The condition that binds:** Theorem 1 requires *known prior odds*, and the paper's conclusion
    (§7) warns that evaluating conditional on "null is true or alternative is true" is the common
    mistake. So `K = p/(1-p)` is legitimate **only if the declared `p` is a real posterior
    probability computed with the operator's actual prior odds.** A tool reporting `P(B>A) = 0.95`
    off a flat prior, where §6.2 puts real prior odds "less than 20%" for most metrics, is not
    reporting the operator's false-discovery risk. Worth a `remedy` line; **not** something the gate
    can adjudicate (brief D-02).

- **D-12:** The Ville distinction is confirmed and is stronger than the repo assumed — Ville is never
  cited in Deng et al. at all (zero occurrences in the full source). Their proof (§5) is the
  **likelihood-ratio identity / change of measure**, an equality, not a maximal inequality. Ville
  gives `P(sup_t M_t ≥ k) ≤ 1/k` for a test martingale — `1/19 ≈ 0.0526` at k=19.
  - **The five-minute readable distinction, in the paper's own words (§6.2):** Type-I error is "the
    chance of false rejection when H₀ is true"; FDR is "the chance of false rejection when decided to
    reject H₀"; and "there is no simple relationship between the two." **Different conditioning
    event, hence the different denominator — `1/(K+1)` vs `1/k` is the signature of which one you are
    looking at.** REQ-P9-03's docstring requirement is satisfied by carrying that sentence.
  - Table 1 demonstrates both at once: type-I error rose 0.018 → 0.060 under continuous monitoring
    **while** FDR held at its designed ceiling. The bound holding and the type-I error inflating are
    not in tension; they are different quantities.
  - The point-null / law-of-iterated-logarithm formulation is confirmed a genuine **third** result
    (§1 and §6.1), under which type-I error tends to 1 as the horizon grows. It has **no ceiling**,
    so it cannot be encoded as a fixed reference value — which is exactly why REQ-P9-03 demands the
    docstring say the check asserts the prior-averaged formulation and not this one.
  - **Existing "unverified locator" flags can now be removed** — `dsx/frame/paradigm.py:66-72` and
    `dsx/spec.py:878-881` (**verified present**) — but only if replaced with a locator that does not
    claim Theorem 1 states `1/(K+1)`.

- **D-13:** `inflation_from_peeking()`'s docstring IS upgraded to a full brief-D-05 citation, carrying
  an explicit unverified-locator flag. This resolves the STATE.md open item.
  - **Mechanically, brief D-05 does not reach this function.** `check_d05()` resolves citations per
    finding code by walking up from each `report.add(...)` call site
    (`scripts/gen-finding-catalogue.py:193-232, 250-280`), and `dsx/mathx.py:411-432` contains no
    `report.add`. It is never in `rows`. **The upgrade is elective, and it is worth doing anyway:**
    leaving the function that produces `DSX-PAR-010`'s numbers citing "Armitage's classic result"
    with no year or paper, while the check citing it carries a full reference, puts a visible seam in
    the two-tier evidentiary story at the one place a v2.0.0 check depends on a v1.5.0 computation.
  - **It is docstring-only, in a module with no `report.add` calls** — it cannot alter any finding,
    any catalogue row, or `DSX-EXP-060`'s output (M-01). The risk is bounded.
  - **The values are verified; the locator is not.** Independent computation — exact numerical
    quadrature (recursive convolution over the continuation region) cross-checked by seeded Monte
    Carlo (4×10⁶ paths) — reproduces the whole anchor table: 2 looks 0.08314, 3 looks 0.10728,
    4 looks 0.12620, 5 looks 0.14171, 10 looks 0.19338, 20 looks 0.24793, against the repo's
    0.083 / 0.107 / 0.126 / 0.142 / 0.193 / 0.248. **The repo's 0.248 at 20 looks is right and the
    widely-circulated 0.246 is wrong** — the two methods agree at 0.2479, more than 5 Monte Carlo
    standard errors away. Record that, so a reviewer arriving with 0.246 and a secondary source is
    answered from the file.
  - **No table or page in Armitage et al. (1969) may be cited.** The paper is subscriber-only at OUP,
    Wiley and JSTOR; Jennison & Turnbull was equally unobtainable. Naming "Jennison & Turnbull
    Table 1.1" would be the fabricated locator brief D-05 exists to prevent. The paper also tabulates
    **three** distributional cases (binomial, normal, exponential), so the citation must name the
    normal, known-variance, equal-group-size case at two-sided nominal α=0.05, and say plainly that
    the values are verified **by computation, not by citation**.
  - **`_D05_ALLOWLIST_PREFIXES` already covers `DSX-PAR-`** (`scripts/gen-finding-catalogue.py:58`),
    so **no script edit is needed** for the three new codes. The `Citation:` and `Reference value:`
    lines must sit on the **enclosing function's** docstring — this exact trap already bit plan 06-07.

### Evidence artifacts

- **D-14:** The REQ-P9-07 simulation is a stdlib-only, `random.Random(seed)` unittest under `tests/`,
  asserting two different things about two different formulations. A **monotone-trend** assertion
  under the point null (formulation (a) — no ceiling exists, so a fixed number cannot be asserted),
  and a **fixed `1/(K+1)` ceiling** assertion under the prior-averaged setup (formulation (b)).
  Swapping them produces a test that passes at one horizon and fails at another — the "implementation
  bug for a day" brief §6.5 warns about, now inside the suite.
  - Stdlib only: there is no `pyproject.toml`, `requirements.txt` or `setup.py` anywhere in the repo,
    and `scripts/check.sh:6-7` runs `python3 -m unittest discover -s tests -q` with nothing installed.
    `tests/` is not formally bound by brief D-01, but numpy would be the repo's **first** external
    dependency, in a project whose stated argument is that a gate which breaks on a missing
    dependency is a gate that gets turned off.
  - It must run **by default** in `scripts/check.sh` discovery. A simulation gated behind an env var
    or excluded from discovery stops running, and then it rots. Budget it sub-second (a few thousand
    trials); resolution is not the point, reproducibility is.

- **D-15:** The REQ-P9-06 symmetry audit ships as `references/paradigm-symmetry.md` — with the tool,
  not only in `.planning/`. ROADMAP SC 5 requires a *committed* audit of the cheapest dishonest
  satisfaction path per half. `.planning/` is filtered out of PR branches by the `gsd-pr-branch`
  workflow, so a `.planning/phases/09-*/` location would hide the brief-D-12 symmetry argument from
  every external reader of the shipped tool. `references/` already holds check-reference material and
  the generated `finding-codes.md` — it is where a reader looks after reading the catalogue, and the
  README's existing "Two tiers of evidentiary rigour" section is the natural link point.
  - **It needs a positive-content test, in the existing idiom.** `tests/test_known_bad_corpus.py:270-326`
    already pairs negative drift guards with an assertion that a post-mortem still *states* its key
    values. Reuse that shape: assert the audit still enumerates both halves' satisfaction paths, and
    assert those enumerated paths match the code's actual clearing conditions. Prose asserting
    symmetry with nothing underneath it is what brief D-12 fails to survive.
  - Write it **at plan time, before the checks are built** (`PITFALLS.md:456-467`). An audit written
    afterwards documents what was built; written first, it constrains what gets built.

### Claude's Discretion

The planner and researcher may settle these without returning to discuss:

- **Plan slicing across the seven requirements**, subject to the atomicity constraint: no plan may
  land `DSX-PAR-010` without `DSX-PAR-011` reaching the same commit range at the same severity.
- **The exact member names and shapes of the three new `inference:` fields** (D-05), subject to the
  collision check and the operator-readability naming rule in `<specifics>`.
- **Whether `threshold_calibration` is a scalar or a sub-dict** (e.g. `{method:, fpr:}`), and whether
  `DSX-PAR-011` performs the `1/(K+1)` numeric comparison on the gate path or asserts only presence
  and defers the number to the docstring and the simulation. Both satisfy REQ-P9-02; the numeric
  comparison is the stronger check and is pure arithmetic on declared values, so it does not breach
  brief D-02 — but confirm that reading before relying on it.
- **The precise restructuring of `tests/test_known_bad_corpus.py`** (D-03), provided the guard at
  lines 231-245 is not weakened.
- **Whether the three regression guards protecting the Deng/Ville attribution need rewording** given
  D-10. Read them first: a guard asserting the post-mortem mentions "Theorem 1" stays correct; one
  asserting Theorem 1 *states* `1/(K+1)` does not.

### Folded Todos

None — `todo.match-phase 9` returned zero matches.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Binding inputs — not re-litigable

- `brief.md` §4 — decisions brief D-01…D-14; D-02, D-04, D-05, D-06, D-10, D-12 are directly
  load-bearing here.
- `brief.md` §5.2 (`inference:` block — note M-02 removed `stopping_rule`), §5.3 (the symmetric
  monitoring pair), §6.5 (gated backlog and the prior-averaged vs point-null formulation trap),
  §7 (reference sources).
- `.planning/PROJECT.md` — Key Decisions M-01…M-09, Constraints, Out of Scope, Known limits.
- `.planning/REQUIREMENTS.md` lines 115-124 — REQ-P9-01…REQ-P9-07. **REQ-P9-02 and REQ-P9-03 require
  the D-10 citation correction.**
- `.planning/ROADMAP.md` lines 285-335 — Phase 9 goal, the atomicity constraint, and the five success
  criteria. **SC 2 and SC 3 require the D-10 citation correction.** Lines 78-82 state the
  milestone-wide brief-D-05 bar.
- `.planning/STATE.md` — hard ordering constraints, standing per-phase deliverables, and the two
  open items this file resolves (D-13 and D-01/D-07 code assignments).
- `.planning/phases/06-.../06-CONTEXT.md` — the naming rule, the collision habit, and the
  `DSX-PAR-011` docstring requirement seeded there.

### Source files this phase modifies or must not disturb

- `dsx/frame/paradigm.py` — the module all three codes land in; `_NOT_SHIPPED` (`:49-57`) and
  `_PARADIGM_CONDITIONAL` (`:38-41`); the unverified-locator flag at `:66-72` (D-12).
- `dsx/spec.py:245-248` `PARADIGMS`; `:250-265` `PARADIGM_JUSTIFICATIONS`; `:272-297` `_VOCABULARIES`;
  `:838-855` `_INFERENCE_FIELDS` and its prose on the missing unknown-key check; `:857-861`
  `_INFERENCE_MEMBERSHIP`; `:868-941` `_validate_inference_shape`, including the early return at
  `:886-888` and the blank-skip at `:917-919` that together leave the D-07 escape open, and the
  unverified-locator flag at `:878-881`.
- `dsx/checks/design.py:444-471` — `_check_peeking` / `DSX-EXP-060`. **Must not change** (M-01). The
  early return at `:446-449` is why `DSX-PAR-010` cannot depend on `results.interim_looks`.
- `dsx/mathx.py:411-432` — `inflation_from_peeking()`, the table REQ-P9-01 mandates reusing and D-13
  upgrades. `dsx/checks/design.py:11-18` shows the import idiom a frame module copies.
- `dsx/cli.py:88-101` `GATE_PROFILES` (`paradigm` in all four; `design` absent from `execute`);
  `:105-110` `GATE_THRESHOLDS`.
- `dsx/decisions.py:64-88` — `DecisionRecord`; the brief-D-04 emission API.
- `dsx/findings.py` — `Severity`; `:202-207` `merge()` and how `report.context` nests per check name.
- `tests/test_known_bad_corpus.py:49-59, 187-245` — the three tests D-03 restructures and the
  allow-list guard that must not be weakened; `:270-326` — the checkable-markdown idiom D-15 reuses.
- `tests/test_dsx.py:504-511` `_INFERENCE_FIELDS` drift guard; `:513-528` the three-`DSX-SPEC-085`
  assertion D-08 must not disturb; `:678-690` the D-08 disjointness test inherited as the
  double-firing guard; `:1390-1393` the template-passes-`gate plan` assertion; `:2585-2607` the
  `_NOT_SHIPPED` invariant.
- `tests/test_frame_boundary.py:35, 58-89` — the D-03a AST scanner. It forbids only `dsx.checks`;
  importing `..mathx` is permitted, but `dsx/frame/__init__.py:16-18`'s allow-list prose should be
  amended to say so.
- `scripts/gen-finding-catalogue.py:43-44` `PREFIX_GROUPS` (the `DSX-PAR` heading already exists);
  `:58` `_D05_ALLOWLIST_PREFIXES` (already covers `DSX-PAR-`); `:70-73` the marker regexes;
  `:193-247` the per-code citation resolution and the `# D-05: <CODE>` test-marker requirement.
- `templates/ANALYSIS-SPEC.yaml:343-352` — the `inference:` scaffold D-05 extends.
- `examples/known-bad/frequentist-uncontrolled-continuous-*` and `bayesian-continuous-monitoring-*` —
  the two target fixtures and their post-mortems. **Both spec headers and the Bayesian post-mortem
  currently state that "nothing in this repository adjudicates it today"; all become false when this
  phase ships and must be updated.**
- `references/finding-codes.md` — regenerate via `scripts/gen-finding-catalogue.py --write`.
- `scripts/check.sh:6-7, 15-23` — the suite entrypoint and the `good-ANALYSIS-SPEC.yaml`
  exits-0-everywhere assertion that will surface any accidental widening.

### Research — advisory, superseded where this file says so

- `.planning/research/FEATURES.md:126-238` — the formulation (a)/(b) split and the warning against a
  second inflation table both stand. **Three corrections, all recorded in D-10/D-11/D-12:** its
  claim that Theorem 1 *states* `1/(K+1)` is wrong; its "Ville's-inequality-type bound" label at
  `:145` is the exact conflation the docstring must prevent; and at `:157-166` it compares the
  paper's **Type-I** figure (0.060) against the **FDR** ceiling (0.10) and calls it "well under" —
  different quantities, and the realised FDR was 0.09, at its ceiling. Its Table 1 *numbers* are
  right; its stated method ("verified via ar5iv") is not reliable for this paper.
- `.planning/research/PITFALLS.md:421-478` — Pitfall 7, the direct source for REQ-P9-06 and D-15.
- `.planning/research/ARCHITECTURE.md:218, 349-368` — module layout and the all-four-gate-points
  recommendation; consistent with D-01 and D-02.

### Primary sources verified during discuss

- **arXiv:1602.05549 LaTeX source** (`arxiv.org/e-print/1602.05549`) — Deng, Lu & Chen (2016). Read
  directly; ar5iv garbles this paper's Table 1. Theorem 1 at §1; `1/(1+K)` bound at §3.2; prior-odds
  1:1 equivalence at §3.1 and §5.1; the FDR-vs-Type-I sentence at §6.2; LIL at §1 and §6.1; proof
  mechanism at §5.
- **Ramdas, Grünwald, Vovk & Shafer (2023)**, "Game-Theoretic Statistics and Safe Anytime-Valid
  Inference", *Statistical Science* 38(4), arXiv:2210.01948 §2.5 eq. (1) — Ville's inequality,
  `P(sup_t M_t ≥ α) ≤ 1/α`. Used for the D-12 contrast only.
- **Armitage, McPherson & Rowe (1969)**, JRSS-A 132(2): 235-244, DOI 10.2307/2343787 — bibliographic
  record and abstract confirmed; **full text not accessible, no table or page verified** (D-13).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- **`dsx.mathx.inflation_from_peeking()`** (`dsx/mathx.py:411-432`) — shipped, tested, and now
  independently value-verified. `DSX-PAR-010` reuses it directly; it is importable from `dsx/frame/`
  without tripping the D-03a boundary scanner, which forbids only `dsx.checks`.
- **`_PARADIGM_CONDITIONAL`-style data-driven applicability** (`dsx/frame/paradigm.py:38-41`) — a
  dict keyed by every `PARADIGMS` member with a set-equality test. The existing house pattern for
  turning a symmetry claim into a structural property; D-06 and D-09 both build on it.
- **`PARADIGM_JUSTIFICATIONS`** (`dsx/spec.py:251-265`) — complete, already in `_VOCABULARIES`,
  already dumped by `dsx vocab`, already carrying the D-12 symmetry comment. Phase 9 coins nothing.
- **`DecisionRecord` + `report.context.setdefault("decisions", [])`** (`dsx/decisions.py:64-88`, used
  at `dsx/frame/paradigm.py:146-161`) — the brief-D-04 emission API. Checks stay pure; the CLI does
  the only file write.
- **The checkable-markdown test idiom** (`tests/test_known_bad_corpus.py:270-326`) — negative drift
  guards plus a positive content assertion. Directly reusable for D-15's audit.
- **`suppressions[]` with its ADR/SPEC authority requirement** — the migration path for any
  pre-v2.0.0 spec caught by the new pair (M-07). Zero new code.

### Established Patterns

- **Severity, not profile membership, selects the gate point.** `GATE_PROFILES` and
  `GATE_THRESHOLDS` are independent knobs (`dsx/cli.py:88-110`). Because `"paradigm"` is already in
  all four profiles, keeping the codes in `paradigm.py` means zero profile edits (D-01).
- **Titles passed to `report.add` must be `Constant`/`JoinedStr` literals at the call site** — the
  catalogue's AST extractor requires it, and a dynamic segment collapses to `<…>`
  (`scripts/gen-finding-catalogue.py:77-88`).
- **Citations resolve per finding code, walking up from the `report.add(...)` call site to the
  enclosing function's docstring**, with a `# D-05: <CODE>` marker required somewhere under `tests/`.
  Put `Citation:` and `Reference value:` on the *enclosing function*, not the module.
- **Findings carry `detail` / `remedy` / `where`, with the numbers in `detail`.** `DSX-EXP-060`
  (`dsx/checks/design.py:453-469`) is the template for what a peeking finding's detail should read
  like — and the one `DSX-PAR-010` must be distinguishable from at a glance.
- **Check for name collisions before coining a term** (`06-CONTEXT.md` `<specifics>`) — applies to
  `threshold_calibration`, `prior_justification` and `decision_threshold` (D-05).

### Integration Points

- `dsx/frame/paradigm.py` — the three checks, and the three `_NOT_SHIPPED` entries that must be
  removed as each code lands (`tests/test_dsx.py:2585-2607` enforces it).
- `dsx/spec.py` — three new `inference:` fields, `_INFERENCE_FIELDS`, `_VOCABULARIES` if any new
  vocabulary is coined, and the D-12 locator replacement at `:878-881`.
- `templates/ANALYSIS-SPEC.yaml:343-352` — the `inference:` scaffold; `tests/test_dsx.py:1390-1393`
  asserts the template still passes `dsx gate plan` afterwards.
- `tests/test_known_bad_corpus.py` — three tests restructured (D-03); the two monitoring fixtures
  flip from "exits 0" to "exits 1 naming its code".
- `references/finding-codes.md` (regenerate) and `references/paradigm-symmetry.md` (new, D-15).
- `README.md` — the "Two tiers of evidentiary rigour" section is the link point for D-15's audit.
- Both known-bad spec headers and the Bayesian post-mortem — their "nothing adjudicates it today"
  statements become false.

</code_context>

<specifics>
## Specific Ideas

- **The naming rule, carried forward from Phase 6 and binding on D-05's three new fields:** *"A
  vocabulary member in a `dsx vocab` dump is read by an operator choosing a value under time
  pressure, not by someone holding §5.3 in their head. The name has to carry the distinction on its
  own."*
- **Check for name collisions before coining a term.** This habit caught the `run_id` collision in
  Phase 6 unprompted. Apply it to `threshold_calibration`, `prior_justification` and
  `decision_threshold` across `dsx/`, `tests/`, `examples/`, `references/` and `templates/`.
- **Traceability to the brief's own wording is worth little where the brief was already wrong.**
  §5's *structure* binds; its phrasing does not bind at the token level. D-10 is this phase's
  instance: REQUIREMENTS.md inherited a citation error from the brief's framing, and the primary
  source wins.
- **When a locator cannot be verified, flag it — never invent it.** Phase 6 escalated two unverified
  locators rather than fabricating them, and that discipline is why D-10 was catchable at all. D-13
  carries the same flag forward for Armitage et al. (1969), and the researcher explicitly declined
  to name a Jennison & Turnbull table it could not open.
- **`1/(K+1)` vs `1/k` is the signature of the conditioning event**, not a rounding difference.
  Whoever writes the `DSX-PAR-011` docstring should make that legible in one sentence — the whole
  point of REQ-P9-03 is that a mismatch reads as a formulation question in five minutes rather than
  an implementation bug for a day.

</specifics>

<deferred>
## Deferred Ideas

- **Adjudicating whether a declared posterior probability was computed with honest prior odds**
  (raised by D-11). The gate cannot check it — that is the known limit ("a frame that lies passes")
  in its purest form. It belongs in the `remedy` text and the human frame review, not in code.
- **Bayesian procedure recommendation and admissibility** — gated backlog, entry condition in
  brief §6.5. Explicitly not this phase.
- **Prior justification *quality*, prior sensitivity, convergence declarations** — deferred under
  brief D-12a; their frequentist mirrors are not written, so shipping them would be the asymmetry
  brief D-12 forbids.
- **Ratio-metric dilution** — Phase 8's REQ-P8-04 already records it as out of scope for v2.0.0 with
  a brief-D-13 entry condition.
- **Retroactive brief-D-05 sourcing for the legacy finding codes.** D-13 upgrades exactly one
  function because a new check depends on it; the allow-list shrinking generally remains a separate
  effort.
- **Obtaining Armitage et al. (1969) and Jennison & Turnbull to replace D-13's unverified-locator
  flag.** A library or institutional copy would close it. Worth doing whenever access appears; not
  worth blocking this phase.

### Reviewed Todos (not folded)

None — `todo.match-phase 9` returned zero matches.

</deferred>

---

*Phase: 09-monitoring-discipline-symmetric-dsx-par*
*Context gathered: 2026-08-12 (assumptions mode)*
