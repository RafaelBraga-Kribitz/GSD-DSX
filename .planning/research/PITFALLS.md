# Pitfalls Research: DSX Validity Frame (v2.0.0)

**Domain:** Declaration-adjudicating statistical-validity gates added to an existing,
installed check tool (gsd-dsx). Operating context: marketing data science, ~60%
online controlled experiments, frequentist and Bayesian paradigms, shared paid-media
budgets.
**Researched:** 2026-08-07
**Confidence:** HIGH (grounded directly in `brief.md`, `.planning/PROJECT.md`,
`references/finding-codes.md`, `dsx/suppressions.py`, `dsx/findings.py`,
`dsx/cli.py`, `dsx/spec.py`, `references/experiment-pitfalls.md` — primary-source
tier per this project's own D-05 standard; external grounding is MEDIUM tier,
cited separately)

Every pitfall below is stated against **this** codebase's actual mechanisms, not
generic gate/linter advice. Where a claim depends on a number, the number was
counted from `references/finding-codes.md` directly (205 codes: CRITICAL 41 / 20%,
HIGH 110 / 54%, MEDIUM 45 / 22%, LOW 9 / 4%; `GATE_THRESHOLDS` in `dsx/cli.py`
blocks `plan`/`execute` at CRITICAL and `verify`/`ship` at HIGH, so verify/ship
already blocks on 151/205 = 74% of the existing catalogue before a single new
family ships).

---

## Critical Pitfalls

### Pitfall 1: The frame lies through the cheapest field, not the obvious one

**What goes wrong:**
D-10 exists because blocking on `paradigm: bayesian` makes `frequentist` the
cheapest lie. The same shape recurs at least four more times in the proposed
contract, and none of the other four have D-10's informational-manifest
mitigation:

- `interference.risk: none` — declaring no interference is strictly cheaper than
  declaring `shared_budget` and then having to fill `mechanism`, `mitigation`,
  and `residual_note`. Unlike `paradigm`, there is no manifest naming "risk was
  declared none, here is what that means for coverage" — a false `none` is
  simply invisible.
- `missingness.mechanism: not_assessed` — this value exists precisely so an
  honest "I haven't checked" is representable (good, see Pitfall 2), but nothing
  distinguishes "haven't checked, will find out" from "checked, don't want to
  deal with MNAR" — both render identically and both pass. `not_assessed` is a
  full substitute for doing the assessment, at zero cost.
- `validity_frame.units.analysis` — DSX-VAL-020 checks that the *declared*
  analysis unit is no finer than the *declared* assignment unit. It has no way
  to see whether the analysis in the entrypoint actually ran at that grain
  (unlike `DSX-CODE-*`, which does read the entrypoint file for fit/split
  order). Retyping `analysis: account` in YAML is cheaper than re-aggregating a
  session-level pipeline to account level, and the gate cannot tell the
  difference.
- `triggering.dilution_adjusted: true` — a bare boolean with an `evidence`
  pointer elsewhere in the frame, not tied to `DSX-INT-030`'s actual trigger.
  Flipping it to `true` is cheaper than building the adjustment.
- `inference.declared_at: pre_data` (§5.2) — self-reported provenance with no
  clock. Nothing in the contract or in `dsx/findings.py`/`dsx/spec.py` ties this
  string to a timestamp, a commit hash, or a lock file. An analyst who wrote the
  "pre-registered" branch after seeing the results can still type `pre_data`,
  which defeats the entire purpose of `DSX-PRE-*` (M3): the reconciliation gate
  in M3 checks the *executed* branch against the *declared* branch, but nothing
  checks that the declared branch was declared *before* the data, which is the
  actual claim `DSX-PRE-*` exists to make credible.

**Why it happens:**
D-02 ("gates adjudicate declarations, they do not compute statistics") is the
right call for D-01 (stdlib-only, hermetic), but it means every field without a
computable cross-check inherits D-10's exact incentive problem by default. D-10
was fixed because `paradigm` was the one field someone thought to interrogate
adversarially (D-09). The others were not yet subjected to the same audit.

**How to avoid:**
- For `interference.risk`: add an M2b finding (new code, HIGH) equivalent in
  spirit to D-10's manifest — not blocking on `risk: none`, but requiring a
  `basis` field (e.g., "no shared channel, no marketplace, no social feature in
  path") so a bare `none` with no basis is itself flagged, the same way a bare
  `suppression` with no `reason` is flagged today (`DSX-SPEC-070` pattern in
  `dsx/suppressions.py`).
- For `missingness.mechanism: not_assessed`: make it legal at `plan`, but raise
  its severity at `verify`/`ship` the same way `DSX-COH-031` already treats an
  unresolved assumption checkoff (neither checked nor waived) as blocking by
  ship. "Not assessed" is fine mid-phase; it is not fine in a shipped analysis.
- For `DSX-VAL-020` / `dilution_adjusted`: this cannot be closed with a
  declaration-only check under D-02. Document the limit explicitly (ties to
  Pitfall 6 / D-05) and, where possible, add a cheap structural cross-check the
  way `DSX-CODE-*` already scans the entrypoint file — e.g., grep the
  entrypoint for a groupby/aggregation step at the declared assignment-unit
  column before the primary test runs. Partial coverage beats none, and this
  matches the existing `DSX-CODE-*` precedent of a hermetic-but-real check.
- For `declared_at`: lock the `validity_frame` + `inference` blocks with a
  content hash captured at the `plan` gate (mirrors `repro_lock`'s
  `schema_version`/`dsx_version` pattern in `DSX-REP-050`–`053`), and have
  `DSX-PRE-*`'s reconciliation check fail if the hash at `verify` differs from
  the hash recorded at `plan` — not the declared string, the actual bytes.

**Warning signs:**
A fixture where every "risky" field is set to its safest value and the fixture
still passes cleanly with no findings at all is not a clean fixture — it is
untested. If the M1 "pull forward from M5" fixtures (an interference case, a
Bayesian continuous-monitoring case) don't include at least one case that lies
about `interference.risk` or `declared_at` and gets caught by something other
than a human reading it, this pitfall shipped.

**Milestone to address:** M1 (declared_at lock, fixture design), M2a (VAL-020
structural cross-check), M2b (interference basis requirement), M3
(reconciliation must check the lock, not the string).

---

### Pitfall 2: "None" and "not applicable" are conflated for question_types that don't need the block at all

**What goes wrong:**
`validity_frame:` becomes required at verify/ship for every `ANALYSIS-SPEC.yaml`,
regardless of `question_type`. But `identification`, `triggering`, and
`stability` are only meaningful for causal/experimental work; `interference` is
only meaningful when there is a shared resource or population overlap. A
descriptive report ("what % of users did X last month") has no honest content
for `triggering.eligible_population` or `stability.novelty_primacy_assessed` —
there is no "eligible population" or "novelty window" concept in a one-shot pull.
Forced to fill a required field with no honest empty state, an analyst will
type `all users` / `n/a` / `true` reflexively, and every one of those five
sub-blocks becomes noise for the 40% of work that is not an online controlled
experiment.

**Why it happens:**
The contract in §5.1 is written as one block, and D-03 ("one contract file")
correctly resists a second file — but "one contract file" does not require "one
undifferentiated required block for every question type." The existing tool
already has the pattern for this exact problem: `DSX-COH-001`
("Claim type exceeds question_type") and the `question_type`-gated requirements
in `DSX-CLM-080` (limitations list required only for
causal/prescriptive/predictive) both scale requirement strength by declared
question type. `validity_frame:` was drafted before that pattern was applied to it.

**How to avoid:**
Gate sub-block *requiredness* by `question_type`, reusing the existing
`DSX-COH-*` mechanism rather than inventing a new one:
- `estimand`, `units`, `dependence`, `sampling_frame`, `measurement` — required
  for every question type (paradigm-independent per D-11, and every analysis has
  a unit of observation and a claimed population).
- `identification`, `triggering`, `stability` — required only when
  `question_type` is causal or the design declares an experiment
  (`design.kind` present), mirroring how `DSX-CAU-001` already gates on
  `question_type`. For descriptive/diagnostic work, these blocks should be
  *absent-and-fine*, not *present-and-empty*.
- `interference` — required whenever `design.kind` implies shared assignment
  infrastructure (experiments, geo tests); optional with a one-line
  justification otherwise, consistent with Pitfall 1's `basis` field.

This is the same fix twice: Pitfall 1's problem (a free `none` with no basis) and
Pitfall 2's problem (a forced answer with no honest content) both resolve to
"scale requiredness and evidentiary weight by what the declared question type
actually needs," which is exactly what `DSX-COH-*` and `DSX-CLM-080` already do
elsewhere in this codebase.

**Warning signs:**
If the M1/M2a good fixture (`examples/good-ANALYSIS-SPEC.yaml`) is descriptive
or diagnostic and still has fully populated `identification`/`triggering`/
`stability` blocks with real-looking content, that content is very likely
decorative — nobody's descriptive dashboard pull has a genuine "triggered
population" story. Check what the fixture actually is before trusting that it
demonstrates real coverage.

**Milestone to address:** M1 (schema + required-ness gating designed alongside
the contract extension, since retrofitting required-ness after M2a/M2b ship
means re-touching every check's precondition), enforced incrementally as each
family's checks land in M2a/M2b.

---

### Pitfall 3: New CRITICAL findings on self-reported fields recreate exactly the alert-fatigue failure mode the literature documents for static analysis tools

**What goes wrong:**
Research on static-analysis-tool adoption is consistent: non-actionable warning
rates of 35–91% train developers to ignore a tool wholesale, and the reasons
cited (warnings not actionable, false positives, low trust in results) map
directly onto declaration-adjudication checks, which are *by construction*
higher false-positive risk than a check that reads real code — a check on
`interference.risk` cannot distinguish "the analyst is wrong" from "the analyst
lied" from "the check's own heuristic is too aggressive." This project already
runs a disciplined severity ladder (20% CRITICAL, 54% HIGH, 22% MEDIUM, 4% LOW
across 205 codes) with CRITICAL reserved almost entirely for structural absence
(`DSX-SPEC-001`, `DSX-SPEC-010`, `DSX-SPEC-020`) or computed, hard-evidence
violations (`DSX-EXP-006` underpowering, `DSX-EXP-011` SRM, `DSX-EXP-060` interim
looks, `DSX-ML-021`/`022`/`031`/`051`/`071`/`072` leakage). If the five new
families lean on the brief's own "Class A failure" framing (§2) and mark most
new codes CRITICAL because the underlying *failure mode* is unrecoverable, that
conflates "the failure mode is catastrophic" with "the check that detects it is
reliable" — and blocks `plan`/`execute` (the earliest, highest-friction gate
points) on findings that are frequently just a badly worded free-text field.

**Why it happens:**
The brief's Class A table is genuinely persuasive about how bad these failures
are, and it is tempting to let severity track failure-mode severity rather than
check-reliability. But `DSX-STA-043` ("Independence assumption is declared
violated") is CRITICAL precisely because it fires on a *declared* fact, not an
inference — a useful existing precedent for when CRITICAL is earned on a
declaration-only check: only when the declaration is unambiguous and the
consequence is definitionally fatal (e.g., `dependence.structure: clustered`
with no `method_family_required` set at all — absence, not a judgment call).

**How to avoid:**
Apply the same three-tier split the existing catalogue already uses:
- CRITICAL: structural absence only (a required field or sub-block missing
  entirely, mirroring `DSX-SPEC-001`/`DSX-SPEC-020`) — e.g., no `estimand`
  block, no `units` block when `design.kind` is set.
- HIGH: a declared combination that is definitionally invalid regardless of
  free-text content (`DSX-VAL-020` unit finer than assignment, `DSX-PAR-010`/
  `011` monitoring pair, `DSX-INT-030` triggered-vs-eligible mismatch) — this
  should be the majority tier, matching the existing 54% HIGH share.
  Threshold placement matters here specifically: HIGH blocks at verify/ship,
  not plan/execute, giving the analyst room to fill the frame progressively
  during a phase rather than being blocked at `plan` before data exists (see
  Pitfall 8 on the pre-data/post-data split).
  it exists but is weak/underspecified (`sampling_frame.selection_risk` present
  but vague, `estimand.falsifier` present but not actually falsifiable).

Do not let `plan`/`execute` (CRITICAL-only) grow much past structural-absence
checks for the new families — those two gate points fire earliest and most
often, and D-05's own citation-and-published-value bar is hardest to meet for a
check aggressive enough to be CRITICAL, which raises the temptation to cut D-05
corners under time pressure (Pitfall 6) precisely on the checks least equipped
to bear that shortcut.

**Warning signs:**
Count the new codes by severity once M2a/M2b land and compare the ratio to the
existing 20/54/22/4 split. A new-family ratio meaningfully skewed toward
CRITICAL (say, above ~30%) is the number to interrogate before shipping, not
after operators start suppressing wholesale.

**Milestone to address:** M2a and M2b (severity assignment at the point each
check is written), reviewed as a ratio check before M2c ships (three more
codes) and again before M4 (an unknown-sized addition from the ontology).

---

### Pitfall 4: D-05's citation-and-test requirement has no enforcement mechanism, and the ontology in M4 is the most likely place it gets skipped without anyone noticing

**What goes wrong:**
`scripts/gen-finding-catalogue.py` regenerates `references/finding-codes.md`
from `report.add(...)` calls via `ast.walk` — it extracts code, severity, and
title, and nothing else. There is no script anywhere in `scripts/` (confirmed:
only `validate-capability.py` and `gen-finding-catalogue.py` exist) that checks
a docstring contains a citation, or that a test file references a published
value. D-05 ("no check ships without (a) a citation... and (b) a test against a
published reference value") is enforced entirely by code review discipline
today, for a project whose own stated single most important constraint is this
exact rule.

The place this is most likely to be quietly violated is not one of the checks —
it's **the M4 ontology itself**, `references/families.yaml`. D-05 as literally
worded binds "checks" (things that call `report.add`); the ontology is *data*
that checks read, not a check. Twenty-five to thirty-five estimator-family
definitions, keyed on four axes with named-test aliases, is exactly the kind of
content an LLM can produce fluently and plausibly from training data with no
primary source per entry — which is precisely what D-05 exists to prevent
("Prevents laundering a language model's statistics knowledge into code carrying
the authority of a blocking gate"), just one layer removed from the check code
where the rule is textually anchored.

A second likely violation point: many `DSX-VAL-*`/`DSX-INT-*` checks are
structural (declaration-presence, combination-validity) rather than numeric, so
there often is no real "published reference value" to test against — only
`DSX-PAR-011` (Deng, Lu & Chen 2016) and a handful of others have an actual
number. Under velocity pressure, the path of least resistance for a structural
check is to write a test asserting the finding fires, then retrofit a citation
next to it that supports the *rule* but was never checked against a *number* —
technically present, substantively decorative.

**Why it happens:**
D-05 is a review-time norm, not a gate-time check, and this project otherwise
insists everything decidable be code (D-02, D-04, the whole determinism
doctrine in README.md). D-05 is the one load-bearing rule in this milestone
that is currently *not* code.

**How to avoid:**
- Extend `scripts/gen-finding-catalogue.py` (or a sibling script run in the same
  CI step) to require a citation marker — a `# Source:` comment or a docstring
  line matching a simple pattern — within N lines of every new-family
  `report.add` call, and fail `--check` if absent, exactly mirroring how the
  script already fails `--check` when the catalogue itself drifts.
- Require each check's docstring to explicitly state whether D-05(b) is
  satisfied by a *numeric* reference value (name it: "Deng et al. 2016, Table
  2, k=20 threshold") or by a *structural* criterion from the citation
  ("Senn 2021 ch.8: analysis unit must not be finer than assignment") — make
  the distinction itself part of the required docstring shape, so "decorative
  citation with no real test" becomes visible in review rather than implicit.
- Extend D-05 explicitly to `references/families.yaml` before M4 starts: each
  family entry needs its own citation field (paper/section, not just "common
  knowledge"), and the M4 admissibility function should refuse to rank a family
  with no citation rather than silently including it. This closes the exact
  loophole above — D-05 binds "no check ships without," and the ontology feeds
  a check (the admissibility function itself), so require the same discipline
  one level down.

**Warning signs:**
Any check whose only citation is a vendor blog, a Medium post, or "general
knowledge" — the brief's own fixture note (§6.5) already flags this class of
source as inadmissible under D-05 "in either direction." A `references/
families.yaml` entry with no citation column at all, once M4 starts, is the
single highest-value thing to look for.

**Milestone to address:** M1 (add the enforcement script alongside the contract
extension, before any new family exists to violate it), M4 (extend the rule to
the ontology data file explicitly, before the first 25–35 entries are written).

---

### Pitfall 5: The simulation trap generalizes to every check with a numeric published reference value, not just DSX-PAR-011

**What goes wrong:**
The brief's own fixture note is explicit: a `DSX-PAR-011` fixture built against
a point-null formulation (unbounded inflation via the law of the iterated
logarithm) but checked against a prior-averaged, Ville's-inequality-bounded
reference value will look like an implementation bug for a day, because both
are correct statements about *different quantities* that happen to share a
citation. This is a general trap, not a one-off: **any time a published number
depends on a choice the citation's title doesn't pin down (which null, which
averaging, which horizon, which boundary family, which convergence threshold
convention), a test written against the wrong choice produces a plausible-looking
off-by-some-factor discrepancy that reads exactly like an arithmetic bug in the
implementation.** Concrete places this can recur in this milestone beyond
`DSX-PAR-011`:
- Sequential-boundary critical values differ by boundary family
  (O'Brien-Fleming vs Pocock, both in `PEEKING_POLICIES`) at the same look
  count — testing a Pocock implementation against an O'Brien-Fleming table
  value looks like a bug.
- VIF thresholds for weak identification (`DSX-VAL-040`) vary by source (some
  cite >5, some >10); the good fixture in §5.1 uses ">12" — if the docstring's
  citation and the fixture's threshold come from different sources, a review
  years later cannot tell whether "12" is defensible or an arbitrary choice
  dressed as a citation.
- Convergence diagnostics (`DSX-PAR-030`, gated backlog) risk mixing the
  Vehtari et al. (2021) rank-normalized R-hat threshold (1.01) with the older
  Gelman-Rubin convention (1.1/1.2) — both are "R-hat," only one matches the
  cited paper.

**Why it happens:**
A citation names a paper; it does not, by itself, name the exact conditioning,
parameterization, or convention the check's test uses. The gap between "cited"
and "operationalized identically to the citation" is invisible until a test
fails and someone spends a day assuming the code is wrong before discovering the
test's assumed formulation was wrong instead.

**How to avoid:**
Generalize the brief's own instruction for `DSX-PAR-011` ("decide which one it
is asserting before writing the fixture, state it in the docstring, and choose
the reference value to match") into a standing rule for every D-05 check with a
numeric reference value: the docstring must name not just the paper but the
*specific formulation* (null hypothesis, conditioning, boundary family,
convention) the test value comes from, and the test/fixture file must comment
which section/table/equation the number traces to. This turns a future "looks
like a bug" day into a five-minute docstring read.

**Warning signs:**
A failing test on a `DSX-PAR-*`, `DSX-VAL-040`/`041`, or (eventually)
`DSX-PAR-030` check where the observed value is close to but not exactly the
expected one, and the implementation logic looks correct on inspection — before
debugging the code, re-read the docstring's stated formulation against the
test's actual simulation/threshold setup. Add this as an explicit first step in
whatever debugging runbook covers this family, so the "day lost" the brief
warns about happens at most once.

**Milestone to address:** M1 (establish the docstring convention when the first
citations are written), M2a/M2c (apply it to `DSX-VAL-040`/`041` and
`DSX-PAR-011` specifically, since these are the two checks in v1 with a genuine
numeric reference value), M4/backlog (apply to convergence diagnostics if/when
`DSX-PAR-030` is promoted).

---

### Pitfall 6: Backlog entry conditions in §6.5 are falsifiable in wording but unenforceable in practice, because nothing computes them

**What goes wrong:**
D-13 requires every deferred item to carry an entry condition tied to measured
evidence rather than a priority — a real improvement over "we'll get to it."
But one of the four entry conditions in §6.5 is already mechanically
computable ("`dsx stats --paradigm` shows Bayesian frames above 15%"), while
two others are not: "the M5 corpus contains at least three cases where absence
of either permitted a false pass" requires someone to (a) look at a false-pass
case in the calibration corpus, (b) determine counterfactually that *this
specific* missing check — not general looseness — would have caught it, and
(c) tally that against a threshold nobody has instrumented. PROJECT.md's own
M-05 decision confirms the adjacent `SELF-001` reversal-tracking mechanism
"stays a convention for v2.0.0... a subcommand adjudicating planning docs is
outside the gate path" — meaning the tooling discipline this project already
applies to itself (measure, don't judge) has an explicit, acknowledged gap
right where backlog promotion needs it most. An entry condition that requires
manual narrative judgment to evaluate decays exactly like a priority does: it
just takes longer and has more ceremony on the way down.

**Why it happens:**
"The M5 corpus contains ≥3 cases" reads as falsifiable prose, but falsifiable
prose still needs someone to run the falsification. Without a structured field
on each corpus case naming which currently-absent check would have caught it,
"3 cases" is not a count, it's a debate.

**How to avoid:**
Extend the M5 calibration harness so every corpus case carries a structured,
machine-readable tag for "which currently-absent DSX-PAR-02x/03x code would
have caught this, if any" at the time the case is added to the corpus — not
reconstructed later from memory. Then `dsx stats` (already planned to report
`--paradigm` split) can report backlog-promotion counts the same mechanical way
it reports the paradigm split, and every entry condition in §6.5 becomes as
computable as the one that already is. Piggyback the actual *review* of these
counts onto the existing milestone-boundary ritual PROJECT.md already commits
to ("After each milestone... Full review of all sections"), rather than
inventing a new recurring process this project's own D-13/M-05 discipline says
to avoid.

**Warning signs:**
At any milestone-boundary review, if nobody can point to a specific corpus
case ID when asked "has this entry condition been met," the condition is
decaying the same way an un-triaged backlog item would, just wearing D-13's
paperwork.

**Milestone to address:** M5 (instrument the corpus with structured
catch-attribution tags as it is built, not retrofitted after "full size" is
declared reached).

---

### Pitfall 7: A symmetric pair can exist on both sides of D-12 and still steer method choice, if one half's satisfaction path is a free-text field and the other's is a closed vocabulary

**What goes wrong:**
`DSX-PAR-010` (frequentist) has exactly one way to be satisfied: declare a real
sequential method from `PEEKING_POLICIES` (a closed, enumerable vocabulary).
`DSX-PAR-011` (Bayesian), as specified in §5.3, has two disjunctive ways to be
satisfied: a `threshold_calibration` block backed by a simulation (numeric,
hard to fake convincingly) **or** an informative `prior` with a `prior_
justification` (free text, self-declared, no numeric proof that the prior is
actually informative enough to bound the false-positive rate the way the cited
Ville's-inequality result requires). Both codes exist, both fixtures fire, D-12
looks satisfied on the catalogue — but if the second `DSX-PAR-011` path can be
cleared with a plausible-sounding paragraph while the frequentist analyst must
adopt a real, behavior-changing correction, the pair is asymmetric in the
dimension D-12 actually cares about (cost of honest satisfaction), not in the
dimension that's easy to check (do both codes exist). This is D-12's own
warning ("Asymmetric enforcement is how a tool silently steers method choice")
recurring *inside* a nominally compliant pair rather than in an obviously
missing counterpart.

The same risk applies to the M2c-adjacent prior-predictive pair (`DSX-PAR-022`
and its frequentist "simulated-data check on the prior-free specification"
mirror, per REV-001): D-02 makes `DSX-PAR-022` a check on three self-reported
fields (`run: true`, an evidence pointer, `outcome_scale_sane: true`), while its
frequentist mirror is described as an actual simulated-data check — if the
mirror requires the check to genuinely execute a simulation-shaped comparison
(even hermetically, against a stored artifact) while the Bayesian side accepts
three booleans, the pair is unequal in verification rigor even though it is
equal in code-existence.

**Why it happens:**
D-12/D-12a police whether a counterpart *exists*. Nothing in the decision table
polices whether the two halves are equally *hard to satisfy honestly*, which is
a harder, more qualitative property to check than "is there a code."

**How to avoid:**
For every symmetric pair, write down at plan time (not after the checks are
built) the answer to: "what is the cheapest way to satisfy each half
dishonestly, and are the two costs comparable?" Where one half accepts free text
as an alternative to a numeric requirement (as `DSX-PAR-011`'s prior path does),
either require the free-text path to carry the same kind of hard evidence the
numeric path does (e.g., `prior_justification` must reference a stored prior
object with a stated scale, checkable against `constraint_source` in
`DSX-VAL-040`/`041`'s vocabulary, not a bare sentence) or drop the disjunction
and require the numeric path only. Treat this as a required line item in the
M2c "done when" criteria alongside "both carry citations per D-05" — add "and
neither half's satisfaction path is cheaper than the other's" explicitly.

**Warning signs:**
If the bad fixture for `DSX-PAR-011` can be flipped to passing by adding one
sentence of `prior_justification` with no change to the actual monitoring
behavior, while the bad fixture for `DSX-PAR-010` requires actually adopting a
named sequential method, the pair is asymmetric regardless of what the
catalogue says.

**Milestone to address:** M2c (design the disjunction's evidentiary bar before
shipping, not after), revisited at the M2c-adjacent prior-predictive pair once
its frequentist mirror is drafted.

---

### Pitfall 8: The validity_frame block mixes pre-data and post-data facts inside one gate that is supposed to be filled "before the data is touched"

**What goes wrong:**
§5 states the contract is "written before the data is touched," and D-09's
adversarial framing questions and `declared_at: pre_data` both assume the frame
is a pre-registration artifact. But the example block itself contains fields
that cannot honestly be known before the data is touched: `missingness.rate:
0.04` (a computed statistic), `stability.evidence: "RESULTS.md#week1-vs-week2"`
(a post-hoc pointer to results that don't exist yet at plan time), and
`identification.evidence: "VIF > 12..."` (a diagnostic computed from data). If
the whole block is required and blocking at `plan` (CRITICAL per
`GATE_THRESHOLDS`), analysts are forced to either delay filling the frame past
the point the contract claims it was written, or fabricate placeholder values
for fields they cannot yet know — which is Pitfall 1/2's boilerplate problem
recurring for a structural reason (timing) rather than an applicability reason
(question type).

**Why it happens:**
The frame conflates two different commitments: "the estimand, units,
dependence structure, and identification strategy are fixed before data" (a
pre-registration claim, genuinely checkable at `plan`) and "here is what the
data turned out to look like" (a post-data report, only checkable once data
exists). Both live under one `validity_frame:` key.

**How to avoid:**
Split blocking by gate point along the pre-data/post-data seam that already
exists in `GATE_PROFILES` (`plan` vs `execute`/`verify`): require
`estimand`, `units`, `dependence.structure`, `identification.strength` (a
design property, known before data), `interference.risk`/`mitigation`, and
`triggering` (a design property) at `plan`; require `missingness.rate`,
`identification.evidence`, and `stability.evidence` (necessarily post-data) no
earlier than `execute`/`verify`. This is a straightforward extension of the
gate-profile pattern that already exists in `dsx/cli.py` — new families need
registering there anyway (per PROJECT.md's noted integration surface), so this
costs a design decision, not new infrastructure.

**Warning signs:**
If the M1 fixture round-trips the block as static at `plan` with real-looking
`rate`/`evidence` values already filled in, check whether that fixture is
honestly representing when those values would be known in a real analysis —
if the fixture was authored end-to-end after the fact (a real risk, since
fixtures are usually written once the whole example is understood), it will
not surface this problem even though a live analyst would hit it immediately.

**Milestone to address:** M1 (this is a schema/gate-profile design decision,
cheapest to make before M2a/M2b build checks against the block).

---

### Pitfall 9: `validity_frame:` becoming required at verify/ship is a breaking change with no grandfather path, and this tool already has the mechanism to build one

**What goes wrong:**
The moment v2.0.0 ships, every pre-existing `ANALYSIS-SPEC.yaml` in the wild
(none of which has a `validity_frame:` block, per PROJECT.md's own integration-
surface note) starts failing the new structural-absence findings at
`verify`/`ship`. This is exactly the kind of rollout that causes gate/linter
tools to get disabled wholesale rather than adopted — the tool's own
`references/experiment-pitfalls.md` and the alert-fatigue research above both
describe the same mechanism from opposite ends: a sudden wall of new,
unaddressable findings is the single fastest way to get a gate turned off
entirely, taking the *existing* nine milestones of coverage down with it.

**Why it happens:**
D-08 requires both fixtures to demonstrate every gate at every threshold, which
correctly proves the *new* checks work — but proves nothing about the
*migration* experience for specs that predate the new contract, because the
fixtures are written fresh, not carried forward from a real pre-v2.0.0 spec.

**How to avoid:**
This project already has the exact mechanism needed: `dsx/suppressions.py`'s
`suppressions[]` block, which requires a `reason` and an `authority` pointer and
aborts (exit 2) on an unknown code. Two concrete, low-effort moves:
1. Document, in the v2.0.0 CHANGELOG/README, the sanctioned migration path:
   add a scoped `suppressions[]` entry (e.g.,
   `authority: "v2.0.0 migration, backfill by <date>"`) for the new
   structural-absence codes on specs not yet updated, rather than leaving teams
   to discover this ad hoc under deadline pressure.
2. A best-effort `dsx frame init` (or equivalent) helper that scaffolds
   `validity_frame:` from fields the spec already has — `units:` from the
   existing `randomization_unit`/`analysis_unit` pair `DSX-EXP-020`/`021`
   already reconciles, `inference.stopping_rule`-equivalent from the existing
   `design.peeking_policy` (already the plan per PROJECT.md's M-02 decision) —
   so migration starts from a partially-filled block instead of a blank
   12-field one. This also directly reduces Pitfall 2's boilerplate risk, since
   a scaffolded block only asks for what genuinely isn't inferable.

Both moves are cheap specifically *because* this codebase already has the
suppression-authority mechanism and the field-reuse decisions (M-02) built in;
a tool without either would need to invent a grandfather mechanism from
scratch.

**Warning signs:**
If the only tested migration path by the time v2.0.0 ships is "the fixtures
pass," and no one has run an actual pre-v2.0.0 spec (not the golden fixture)
through `dsx gate ship`, this pitfall has not been checked, only assumed away.

**Milestone to address:** M1 (this is where the breaking change is introduced,
the version bump to v2.0.0 already anticipates it per PROJECT.md, and the
suppression mechanism/field-reuse decisions it depends on are already in
place).

---

### Pitfall 10: The estimator-family ontology (M4) creeps via alias-completeness, not via the four-axis taxonomy itself

**What goes wrong:**
"Roughly 25 to 35 families" is a bounded target for the *families* axis, but
the brief also requires "named tests as aliases resolving into families" — and
the space of named statistical tests is unbounded in a way the family count is
not. The realistic overrun in M4 is not "the ontology grew a 36th family," it's
"M4's time went into chasing alias-list completeness" (adding every synonym and
regional naming convention for tests that already resolve into an existing
family) while family *definitions* and the admissibility/ranking logic — the
part that actually does the work `DSX-ADM-*` exists for — got less attention
than the brief intended. This is the same shape as the explicitly named
non-goal "a catalogue of every named statistical test" reappearing inside a
milestone that is allowed to have named-test aliases at all.

**Why it happens:**
Alias completeness is easy, visible progress (each entry is a five-minute
lookup) compared to admissibility logic, which is genuinely hard design work.
Under any velocity pressure, the easy, visible work crowds out the hard,
load-bearing work — the inverse of D-05's warning ("if velocity pressure
arrives, cut checks, never this") applied to a milestone rather than a check.

**How to avoid:**
- Build the ontology from the calibration corpus, not from taxonomic
  completeness: only add a family (and its aliases) when a real fixture — one
  of the M1 pulled-forward fixtures, or the operator's own frame history — 
  actually needs it, exactly as brief §6.6 already warns against scaffolding
  `references/families.yaml` early "to satisfy the boundary rule."
- Rely on the explicit `no_admissible_procedure -> escalate` branch as the
  scope-bounding mechanism it's designed to be: since "escalate, I don't know"
  is an acceptable, even desired, outcome, there is no completeness pressure
  requiring every possible test name to resolve to something. An unrecognized
  alias should escalate, not silently default into the nearest-sounding family.
- Cap the axis space explicitly to v1's actual scope: frequentist only (per
  D-12a, Bayesian ADM stays gated-backlog), which halves the inference-method
  axis before work starts.
- Use the M-04 automated import-boundary test (already decided in PROJECT.md:
  enforces `dsx/frame/` never imports upward from `dsx/checks/`) as a forcing
  function to keep the ontology pure data with no creeping business logic —
  scope creep in a pure-data file is at least legible in a diff in a way
  creeping logic isn't.

**Warning signs:**
If M4's commit history shows many small commits adding aliases and few commits
touching the admissibility/ranking function itself, the milestone is creeping
in the direction this pitfall predicts. A `families.yaml` where the alias list
is several times longer than the family list is worth a specific look at
whether every alias earned its place from a real fixture.

**Milestone to address:** M4 (design the corpus-driven, escalate-permitted
scoping rule before the ontology file is opened, not after it starts growing).

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|-----------------|------------------|
| Free-text `evidence`/`justification` fields left unvalidated (no length, no structure) | Ships faster — no parser to write | Becomes the "type `none`/`n/a` reflexively" escape hatch (Pitfalls 1, 2) | Only for fields with no honest failure mode already gated by `question_type` (e.g., `measurement.known_gaps` on a descriptive spec) |
| Citing a paper without stating the exact formulation the test value comes from | Satisfies D-05's letter immediately | Sets up the simulation-formulation trap (Pitfall 5); wastes a debugging day later | Never — this is the one shortcut the brief itself says never to take |
| Deferring `families.yaml` citation requirements until "the ontology stabilizes" | M4 ships sooner | Exactly the D-05 loophole (Pitfall 4) the project exists to close | Never |
| Shipping `validity_frame:` required-ness uniformly across `question_type` rather than gating it (Pitfall 2) | One code path, simpler M1 | Boilerplate noise for ~40% of non-experimental work, erodes trust in the whole family | Only as a temporary M1 placeholder if the `DSX-COH-*`-style gating is explicitly planned for immediately after, not indefinitely |
| Treating `dsx stats --paradigm` and the M5 harness as "good enough" evidence without structured per-case catch-attribution (Pitfall 6) | M5 ships without extra instrumentation | Backlog entry conditions become unfalsifiable in practice (Pitfall 6) | Never, if D-13 is meant to mean anything beyond the paradigm-split item |

## Integration Gotchas

| Integration point | Common Mistake | Correct Approach |
|---|---|---|
| `GATE_PROFILES` in `dsx/cli.py` | Forgetting to register the new `frame`/`interference`/`paradigm`/`preregistration`/`admissibility` check modules at the right gate points, silently leaving new families unenforced at some or all of `plan`/`execute`/`verify`/`ship` | Register each new module explicitly per milestone, and add a test asserting every `DSX-VAL-*`/`DSX-INT-*`/`DSX-PRE-*`/`DSX-PAR-*`/`DSX-ADM-*` code is reachable from at least one `GATE_PROFILES` entry, mirroring how `known_codes()` in `dsx/suppressions.py` already asserts every code is real |
| `suppressions[]` matching (`_matches` in `dsx/suppressions.py`) | Assuming frame-level findings need `chart_id`-style scoping like `DSX-VIZ-*`/`DSX-SMELL-*` findings do | Not a real gotcha here — `_matches` already degrades gracefully to code-only matching when `chart_id` is absent, which is exactly what a spec-wide (not chart-scoped) finding needs. Confirmed correct as-is; no change needed, but worth a test asserting it explicitly for the new families |
| `PEEKING_POLICIES` vocabulary (`dsx/spec.py`) | Adding the new "uncontrolled continuous monitoring" value (M-03) without checking whether `dsx vocab`'s output (already referenced in M1's scope) and any downstream consumer of the enum stay in sync | Extend the vocabulary and `dsx vocab` output in the same commit, and re-run `DSX-EXP-060`'s existing fixtures to confirm the new value doesn't change that check's behavior — M-01 explicitly requires `DSX-EXP-060` stay untouched |

## Performance Traps

Not a significant risk area for this milestone — the gate path is hermetic,
stdlib-only, and reads no live data (D-01/D-02), so the new families add at
most a bounded amount of YAML parsing and dict lookups. The one item worth a
glance: `known_codes()` in `dsx/suppressions.py` walks every `.py` file under
`dsx/` with `ast.parse` on every run (cached in-process via `_KNOWN`, but not
across runs). Five new check modules plus a 25–35-entry `families.yaml` do not
meaningfully change this; not worth engineering around.

## Security Mistakes

| Mistake | Risk | Prevention |
|---|---|---|
| Treating `authority` on a migration-era `suppressions[]` entry (Pitfall 9) as a rubber stamp rather than a real pointer | A vague `authority: "v2.0.0 migration"` string with no ticket/date could be reused indefinitely to suppress structural-absence findings on every legacy spec, permanently, defeating the whole point of the new contract | Require the migration-authority convention to include a concrete backfill deadline or ticket reference, and treat suppressions whose `authority` string matches a generic migration pattern as a distinct, reviewable category (a `dsx stats`-style count of "how many specs are still on the migration suppression" is cheap and valuable) |

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---|---|---|
| D-04 splits the guardrail (blocking finding) from the lesson (`dsx explain`, non-blocking) into two separate invocations, with nothing in the blocking output pointing to the second | An operator blocked by a new `DSX-VAL-*`/`DSX-PAR-*` finding sees the `remedy` text and fixes the YAML to pass, without ever running `dsx explain` — Goal 2 ("operator learning") silently fails even though Goal 1 ("risk reduction") works, because the two are architecturally connected but not discoverably connected | Every new-family finding's `remedy` field should explicitly name `dsx explain <code>` (or equivalent) as the next step, the same way `DSX-SPEC-072`'s `remedy` today points at `references/finding-codes.md`. Make this a required convention in the M1 check-writing pattern, not an afterthought once `dsx explain` exists |

## "Looks Done But Isn't" Checklist

- [ ] **`DSX-VAL-020` / unit-triad checks:** Often verified only against the
  *declared* strings in `validity_frame.units` — verify there is at least a
  partial structural cross-check against the entrypoint (mirroring
  `DSX-CODE-*`'s real file scan), not pure declaration-vs-declaration.
- [ ] **A symmetric pair (`DSX-PAR-010`/`011`, and later the prior-predictive
  pair):** Often verified only by "both codes exist and both bad-fixtures
  fire" — verify the *cheapest honest-looking dishonest satisfaction path* is
  comparably costly on both sides (Pitfall 7), not just that both sides have
  code.
- [ ] **A D-05 citation:** Often verified only by "a paper name appears in the
  docstring" — verify the docstring states the *specific formulation* the test
  value comes from, and the test/fixture comments trace the number to a
  section/table/equation (Pitfall 5).
- [ ] **A §6.5 backlog entry:** Often verified only by "the row exists in the
  table with a stated condition" — verify the condition is mechanically
  computable from `dsx stats`/the M5 harness, not narrative judgment
  (Pitfall 6).
- [ ] **Migration readiness at ship:** Often verified only by "both fixtures
  pass every gate" (D-08) — verify an actual pre-v2.0.0 spec, not the golden
  fixture, has been run through `dsx gate ship` and the migration path
  (suppression convention or `dsx frame init`) has actually been exercised
  once (Pitfall 9).
- [ ] **`references/families.yaml` (M4):** Often verified only by "resolves the
  test names in the calibration corpus" — verify every family entry carries
  its own citation and that the alias list isn't growing faster than the
  admissibility logic it feeds (Pitfall 10).

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---|---|---|
| Citation-formulation mismatch discovered post-ship (Pitfall 5) | MEDIUM | Fix the docstring to name the exact formulation, regenerate the fixture's reference value to match; the code itself (D-06) is never renumbered, so this is a content fix, not a breaking change |
| Monolithic required block causing reflexive boilerplate across specs (Pitfall 2) | HIGH | Retrofit `question_type`-gated required-ness onto the existing checks (reusing the `DSX-COH-*` pattern), regenerate the catalogue, and expect a version bump since required-ness behavior changes for existing specs — cheaper the earlier it's done, ideally before M2a ships rather than after |
| Backlog entry condition found unfalsifiable in practice (Pitfall 6) | LOW | Reword the §6.5 table row to name a structured, computable field; per D-14 this reversal needs a reversal record (evidence: "the condition as worded required manual judgment with no owner"), but no code changes |
| Breaking-change migration pain discovered after v2.0.0 ships without a grandfather path (Pitfall 9) | HIGH | Retroactively document the suppression-authority convention and ship a best-effort `dsx frame init`; costs real user trust in the interim, since the failure is visible to every team on upgrade day, not caught internally |

## Pitfall-to-Milestone Mapping

| Pitfall | Milestone | Verification |
|---|---|---|
| 1. Cheapest-lie fields beyond `paradigm` | M1 (lock mechanism), M2a (VAL-020 cross-check), M2b (interference basis), M3 (reconciliation checks the lock) | Bad fixtures include a case that lies about `interference.risk`/`declared_at` and gets caught by something other than a human reading it |
| 2. Monolithic block forces boilerplate for non-experimental `question_type` | M1 (schema design), M2a/M2b (enforcement) | Descriptive/diagnostic good fixture has genuinely absent, not decoratively-filled, `identification`/`triggering`/`stability` blocks |
| 3. Alert fatigue from severity misallocation | M2a, M2b (assignment), reviewed before M2c/M4 | New-family CRITICAL share stays near the existing ~20% baseline, not skewed toward it |
| 4. D-05 unenforced, ontology is the likely gap | M1 (enforcement script), M4 (extend to `families.yaml`) | `gen-finding-catalogue.py --check`-equivalent fails on a missing citation marker; every M4 family entry has a citation column |
| 5. Simulation-formulation trap generalizes | M1 (docstring convention), M2a/M2c (apply to VAL-040/041, PAR-011) | Docstrings name the exact formulation; fixtures comment which section/table the number traces to |
| 6. Backlog entry conditions unfalsifiable in practice | M5 | Corpus cases carry structured catch-attribution tags; `dsx stats` can report a backlog-promotion count the same way it reports the paradigm split |
| 7. Symmetric pair unequal in satisfaction cost | M2c | "Done when" criteria explicitly include "neither half's satisfaction path is cheaper than the other's," not just "both carry citations" |
| 8. Pre-data/post-data fields mixed in one required block | M1 | Gate-profile registration splits blocking by field, not just by family |
| 9. Breaking-change migration with no grandfather path | M1 | An actual pre-v2.0.0 spec passes `dsx gate ship` via the documented suppression convention or a scaffolding helper, not by hand-authoring all 12 fields |
| 10. Ontology scope creep via alias-completeness | M4 | Family count stays near 25–35 with corpus-driven justification per entry; `escalate` branch used, not stretched-family assignment |

## Sources

Primary (this project, HIGH confidence per this project's own D-05 standard):
- `brief.md` — full document, especially §2 (Class A failure table), §4
  (D-01–D-14), §5 (contract), §6/6.5/6.6 (milestones, gated backlog, open
  items), §7 (citations), §8 (known limits)
- `.planning/PROJECT.md` — M-01–M-05 decisions, integration surface, out of
  scope
- `references/finding-codes.md` — 205-code catalogue, severity distribution
  counted directly (CRITICAL 41, HIGH 110, MEDIUM 45, LOW 9)
- `dsx/suppressions.py`, `dsx/findings.py`, `dsx/cli.py` (`GATE_PROFILES`,
  `GATE_THRESHOLDS`), `dsx/spec.py` (`PEEKING_POLICIES`, `VARIANCE_ADJUSTMENTS`)
- `references/experiment-pitfalls.md` — existing project pitfall catalogue
- `scripts/gen-finding-catalogue.py`, `scripts/validate-capability.py` —
  confirmed absence of any D-05 enforcement mechanism

External (MEDIUM confidence, general grounding for Pitfall 3 only):
- [Lessons from Building Static Analysis Tools at Google — CACM](https://cacm.acm.org/research/lessons-from-building-static-analysis-tools-at-google/)
- [Challenges with Responding to Static Analysis Tool Alerts (ResearchGate)](https://www.researchgate.net/publication/331792299_Challenges_with_Responding_to_Static_Analysis_Tool_Alerts)
- [A Large-Scale Collection Of (Non-)Actionable Static Code Analysis Reports — Scientific Data](https://www.nature.com/articles/s41597-025-06154-7)
- [Mitigating False Positive Static Analysis Warnings — ResearchGate](https://www.researchgate.net/publication/375259352_Mitigating_false_positive_static_analysis_warnings_Progress_challenges_and_opportunities)
- [What is Goodhart's Law? — Splunk](https://www.splunk.com/en_us/blog/learn/goodharts-law.html)

---
*Pitfalls research for: DSX Validity Frame v2.0.0 (gsd-dsx)*
*Researched: 2026-08-07*
