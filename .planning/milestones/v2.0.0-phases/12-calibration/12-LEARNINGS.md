---
phase: 12
phase_name: "Calibration"
project: "gsd-dsx"
generated: "2026-08-27"
counts:
  decisions: 7
  lessons: 7
  patterns: 7
  surprises: 6
missing_artifacts:
  - "UAT.md"
---

# Phase 12 Learnings: Calibration

## Decisions

### Attribution-tag carrier = per-fixture sidecar file, not a spec key or a harness map
The catch-attribution tag (which currently-absent code would have caught a miss, plus which §6.5
item it promotes) lives only in `examples/known-bad/<slug>-ATTRIBUTION.yaml`, glob-discovered by
slug. Three alternatives were explicitly rejected: a top-level ANALYSIS-SPEC key (leaks a
known-bad-fixture concept into the shipped spec contract real analysts write), a postmortem-prose
block (couples machine-countable data to CRLF-sensitive prose parsing), and a harness-side map
(the exact stale hand-maintained-ledger anti-pattern the phase's REQ-P12-02 bans).

**Rationale:** The sidecar is machine-countable (glob + YAML load) and frame_digest-safe — living
entirely outside the `validity_frame`/`inference` subtree means it cannot perturb `frame_digest`
or trip `DSX-PRE-020`, and it is authored in the same change that adds the case rather than
retrofitted.
**Source:** .planning/phases/12-calibration/12-CONTEXT.md (D-06)

---

### Headline is the pair (miss-rate, FPR), never a single catch-rate number
Catch rate is stratified into a PRESENT partition (fixtures carrying a firing target code) and an
ABSENT partition (curated miss cases), each with its own denominator. The reported headline is
`(miss-rate, FPR)`, and the ABSENT partition is floored at 3 with a synthetic + live invariance
proof showing that injecting an extra target-PRESENT case leaves the headline byte-identical.

**Rationale:** Every fixture at the start of the phase already carried a present-and-firing code,
so a single catch-rate headline would be a regression-pin dressed as detection — adding
already-caught cases drives it toward 100% for free. Stratifying and flooring makes that gaming
mathematically impossible.
**Source:** .planning/phases/12-calibration/12-CONTEXT.md (D-10); .planning/phases/12-calibration/12-READOUT.md §1-2

---

### `dsx stats --paradigm` hard-excludes the known-bad fixture floor, hardened to an absolute boundary
The command sources only real operator `.planning/` decision trails; `examples/known-bad/DECISIONS.jsonl`
(and any `examples/**` or `templates/**` trail) is hard-excluded. A code-review finding (CR-01)
showed the original relative-path exclusion could be defeated by pointing `--root` at or inside
the excluded tree (`relative_to(root)` strips the very component being matched), so the fix moved
the match to the trail's **resolved, case-folded absolute path components** — a boundary that
fails safe (over-excludes) rather than leaking.

**Rationale:** The known-bad floor measures ~45.8% raw-Bayesian across ~1,151 invocation records
but only 15 distinct `frame_digest`s; counted raw it would falsely trip the §6.5 item-4
"Bayesian > 15%" promotion gate roughly four-fold. A boundary this load-bearing must hold under
any documented invocation of the CLI flag that controls it, not just the default.
**Source:** .planning/phases/12-calibration/12-CONTEXT.md (D-13); .planning/phases/12-calibration/12-REVIEW.md (CR-01, fix commit 4e8d1ff)

---

### §6.5 item 6 (ratio-metric dilution) removed as structurally unevaluable, via relocate-not-delete + REV-002
Item 6's entry condition needs a per-unit trigger/outcome computation the D-01/D-02 determinism
doctrine forbids on the gate path — a constraint that does not lift with time. The row was moved
verbatim (not deleted, not softened) into a new "Removed / permanently out of scope (D-14)"
subsection of `brief.md` §6.5, preserving the exact substrings a pre-existing pin test asserts, and
`REV-002` was filed in `.planning/REVERSALS.md`.

**Rationale:** "Unevaluable ⇒ remove" is reserved for structural unreachability, never a
merely-unmet condition (items 4 and 5 stay carried as prerequisite-pending, not removed). REV-002's
"New evidence" field had to name the systematic Phase-12 re-evaluation event, not the D-01/D-02
determinism doctrine itself, because that doctrine pre-dates the deferral and restating it as novel
would trip the project's own SELF-001 self-consistency convention.
**Source:** .planning/phases/12-calibration/12-CONTEXT.md (D-16, D-17); .planning/phases/12-calibration/12-07-SUMMARY.md

---

### Phase 12 mints zero new finding codes; the 256-code catalogue is pinned with a dedicated invariant test
No `DSX-*` code is created and nothing is added to `GATE_PROFILES`. Attribution sidecars only
*reference* existing-or-backlog codes; `dsx stats --paradigm` is a pure reader; the friction column
is arithmetic over existing findings. A new `tests/test_finding_catalogue_invariant.py` asserts the
catalogue Total line AND the enumerated `DSX-*` rows both equal 256.

**Rationale:** Phase 12 is measurement, reporting, and backlog hygiene — not detection — so the
catalogue must stay provably frozen; a silent mint would break the phase's own zero-mint contract
(D-18) and undermine the calibration story being told.
**Source:** .planning/phases/12-calibration/12-CONTEXT.md (D-18); .planning/phases/12-calibration/12-06-SUMMARY.md

---

### Friction is reported RAW and NET, never net-only, with the incidental→own relabel path closed
The per-family over-blocking column subtracts each fixture's own declared target codes from its
total ship-blocking findings, but both the raw total and the net (raw − own) are surfaced. A
dedicated guard requires every `_TARGET_DEFECT_CODES` entry to be positively verified firing
blocking-live at its mapped point AND named in that fixture's postmortem/attribution before it can
count as "own" rather than incidental over-blocking.

**Rationale:** Net-only reporting is a laundering hole — a fixture over-blocking on 5 unrelated
codes looks clean if 2 of them are silently relabelled "its own." Requiring public naming closes
that path without banning legitimate own-target codes.
**Source:** .planning/phases/12-calibration/12-CONTEXT.md (D-11); .planning/phases/12-calibration/12-06-SUMMARY.md

---

### Good-corpus FPR denominator built via cwd-resolvable committed artifacts, a third route beyond the plan's two named options
The plan offered "seed siblings into the tempdir" or "keep the spec minimal enough to reference
nothing." Neither was literally viable because a clean shipped analysis must declare a resolvable
claim, narrative, and entrypoint. The route taken commits per-spec narratives (doubling as claim
evidence) and one shared entrypoint that all resolve from the repo root (`cwd`), so every one of
the 12 control specs' measured ship-time finding set is `frozenset()` with no tempdir seeding
needed downstream.

**Rationale:** This achieves the plan's actual goal — an honest zero false-positive count on 12
specs — without the complexity of sibling-artifact seeding in the FPR harness that consumes the
corpus.
**Source:** .planning/phases/12-calibration/12-04-SUMMARY.md

---

## Lessons

### The `--root` flag could defeat the D-13 exclusion by stripping its own match target
Code review found that `_discover_operator_trails` matched `"examples"`/`"templates"` against a
trail's path **relative to `--root`**. When `--root` was pointed at or inside the excluded tree
(e.g. `--root examples/known-bad`), `relative_to()` had already stripped the matched component, so
the guard silently never fired — live-reproduced as a false 20% Bayesian share, exactly the
false-promotion scenario the exclusion exists to prevent.

**Context:** This was not caught by the original guard test, because that test only ever placed
the known-bad floor *under* a synthetic root, never pointed `--root` *at* the excluded directory
itself — a green test masking a live defect. The fix matches against the trail's resolved,
case-folded absolute path instead.
**Source:** .planning/phases/12-calibration/12-REVIEW.md (CR-01, WR-01)

---

### Continuous-outcome specs have no clean path in the current schema
Early drafts of the retracted-fabricated and operator-known-answer fixtures, when framed as
continuous-outcome experiments, fired accidental spec-quality findings (invalid `baseline_rate`,
unit mismatch, additive dilution) because the schema's checks assume a proportion baseline_rate and
there is no continuous sibling.

**Context:** Both fixtures were reframed — one to a proportion outcome ("share who durably
warmed"), one to a descriptive group-mean contrast — purely to make each fire only its intended
defect, not the schema gap. Anyone authoring a continuous-outcome fixture in this corpus should
expect the same friction.
**Source:** .planning/phases/12-calibration/12-01-SUMMARY.md

---

### A new corpus fixture requires lockstep registration in five separate whole-tree test harnesses, not just the golden test
Adding glob-discovered fixtures under `examples/known-bad/` hard-failed not only
`tests/test_causal_verb_golden.py` but also `_INCIDENTAL_GAP_CODES`, `_EXPECTED_CAUGHT_DEFECTS`,
`tests/test_frame_val.py::_EXPECTED_VAL_CODES`, `tests/test_frame_interference.py::_NON_CAUSAL_KNOWN_BAD`,
and `tests/test_dsx.py`'s committed-spec count.

**Context:** The RESEARCH artifact's "Pitfall 2" only named the golden test explicitly; execution
found the pattern generalizes to every whole-examples-tree harness with per-fixture registration,
requiring four additional files touched beyond the plan's declared scope (mechanically required,
no logic change).
**Source:** .planning/phases/12-calibration/12-01-SUMMARY.md

---

### The empty operator paradigm split is 0/0 undefined, not evidence of "below 15%"
The initial readout draft characterized the empty `dsx stats --paradigm` result as satisfying
§6.5 item 4's "Bayesian > 15%" condition being unmet ("expected below 15%"). The Statistician
adversarial review (finding F5) corrected this: with zero distinct frames there is no denominator,
so the ">15%" predicate is untestable here, not measured-and-failing.

**Context:** Absence of operator Bayesian history is not statistical evidence of a sub-15%
Bayesian share — it means the instrument has nothing to promote on because the operator has run
no gated work yet, exactly as a prior context decision (D-15) anticipated in the abstract but the
readout initially mis-stated in the concrete.
**Source:** .planning/phases/12-calibration/12-READOUT.md §5, §8.1 (F5)

---

### The frequentist admissibility ontology has no count/Poisson family
Authoring frequentist count/ratio control specs for the good-corpus hit a schema gap: there is no
Poisson family in `references/families.yaml`. Per-unit rates had to be modelled as a
`ratio_of_means` estimand with `inference.primary_procedure: delta_method` instead.

**Context:** This is a durable schema limitation future fixture/spec authors need to know before
attempting a genuine count-outcome frequentist spec — the workaround (ratio_of_means +
delta_method, omitting `analysis.test` so the frequentist cell-count test-selection contract
doesn't apply) is the only clean path today.
**Source:** .planning/phases/12-calibration/12-04-SUMMARY.md

---

### A "clean, minimal-reference" spec still cannot omit claims, narrative, or entrypoint
The plan's literal minimal-reference route ("reference no sibling artifacts at all") turned out to
be unreachable: `claims` is unconditionally required (DSX-CLM-001), a present claim forces a
resolvable `narrative.path` and evidence pointer (DSX-NAR-001, DSX-CLM-031), and
`reproducibility.entrypoint` is required and must resolve (DSX-REP-030/031).

**Context:** The actual minimal route is "reference only committed, cwd-resolvable artifacts,"
not "reference nothing" — a distinction that matters for anyone trying to construct a genuinely
zero-sibling clean spec in this schema.
**Source:** .planning/phases/12-calibration/12-04-SUMMARY.md

---

### `_TARGET_DEFECT_CODES` naming allows a documented cross-fixture fallback, not just "that slug's own docs"
Guard (c) (every own-target code must be named in its fixture's postmortem/attribution) initially
assumed strict per-slug naming, but `weak-identification-mmm`'s secondary code `DSX-INT-030` is
actually `triggering-dilution`'s primary declared code — named in triggering-dilution's postmortem,
not weak-identification-mmm's own, and weak-identification-mmm has no ATTRIBUTION.yaml.

**Context:** The guard was relaxed to accept a code named in **any** corpus postmortem/attribution
as a documented fallback, since the threat being closed (silent incidental→own relabeling) is still
prevented as long as the code is publicly declared an intended defect *somewhere* in the corpus.
**Source:** .planning/phases/12-calibration/12-06-SUMMARY.md

---

## Patterns

### Source-before-count (anti-padding)
Corpus cases are sourced from the real known-bad population and tagged as they are added; §6.5
counts are read off whatever falls out. A fixture is never reverse-engineered to trip a threshold —
if only two cases naturally demonstrate a condition, the related backlog item stays deferred as a
valid measured outcome, not a failure to fix.

**When to use:** Any time a corpus, fixture set, or sample is being built specifically to produce a
measured statistic that will gate a decision — the optional-stopping pathology this pattern
prevents is exactly the kind of bias the resulting number would otherwise exist to catch.
**Source:** .planning/phases/12-calibration/12-CONTEXT.md (D-02)

---

### Stratify a detection rate by target-PRESENT vs target-ABSENT with independent floors and an invariance proof
Rather than one catch-rate number, report two partitions with independent denominators, floor the
ABSENT/miss partition at a minimum representation, and add a synthetic + live proof that adding
target-PRESENT cases cannot move the headline.

**When to use:** Any calibration of a detector/gate where the corpus composition itself could
otherwise be gamed (deliberately or by drift) to inflate a single aggregate rate — floor + stratify
+ invariance-prove makes that gaming structurally impossible rather than merely discouraged.
**Source:** .planning/phases/12-calibration/12-CONTEXT.md (D-10); .planning/phases/12-calibration/12-05-SUMMARY.md

---

### Two-proofs discipline: filesystem-independent synthetic arithmetic proof beside a live-source integration proof
Pure helper functions (e.g. `_headline`, `_friction`) are exercised both by a fabricated,
filesystem-independent unit test that carries a real RED/GREEN signal, and by a live integration
test tying the same helper to the actual `_gate_findings` output.

**When to use:** Whenever the "real" corpus a live test runs against is clean-by-construction (so
a naive/broken helper would still pass), a synthetic proof over deliberately non-degenerate inputs
is needed to carry the non-trivial failure signal that the live test cannot provide by itself.
**Source:** .planning/phases/12-calibration/12-05-SUMMARY.md; .planning/phases/12-calibration/12-06-SUMMARY.md

---

### All numbers computed LIVE via the shared gate-invocation helper, never lifted from a stale ledger
Every reported number (catch rate, FPR, friction, attribution falsifiability) is computed by
calling `_gate_findings` (a real `dsx gate <point>` in a fresh tempdir) at report time, and existing
hand-maintained snapshots (`_INCIDENTAL_GAP_CODES`, `_GOLDEN_SHIP_FINDINGS`) are explicitly
forbidden as a source of truth for these numbers even though they exist for other purposes.

**When to use:** Any report or gate deriving from check/finding output where new checks might ship
later — a stamped-date snapshot silently rots the moment detection logic changes, while a live call
stays honest by construction.
**Source:** .planning/phases/12-calibration/12-CONTEXT.md (D-09); .planning/phases/12-calibration/12-READOUT.md (frontmatter)

---

### Commit a read-only companion measurement script alongside a data-derived readout
`.planning/phases/12-calibration/_measure_readout.py` was committed alongside `12-READOUT.md`
specifically so the readout's numbers can be independently re-derived read-only, while the
unittest `test_stratified_catch_rate_and_fpr_report` remains the durable reproducer of record.

**When to use:** Any narrative readout whose numbers come from a test/harness — pairing the prose
with a lightweight, read-only reproduction script (distinct from the pass/fail gate test) makes the
claim independently checkable without re-running the whole suite.
**Source:** .planning/phases/12-calibration/12-READOUT.md (frontmatter)

---

### Allowlist-with-inline-reason for any "codes excluded from X" set
New documented exclusion/reference sets this phase (`_SECTION_65_BACKLOG_CODES`,
`_FPR_TEMPDIR_NOISE_CODES`) each carry one code per line with an inline comment explaining why,
mirroring the pre-existing `_INCIDENTAL_GAP_CODES` house style, and are kept as fresh, separate
constants rather than reused/extended from an existing stale ledger.

**When to use:** Any time a test needs to special-case a small, named set of codes (noise, backlog
references, known gaps) — the inline-reason-per-entry convention keeps the exclusion set itself
auditable rather than an opaque allowlist.
**Source:** .planning/phases/12-calibration/12-03-SUMMARY.md; .planning/phases/12-calibration/12-05-SUMMARY.md

---

### Fail-safe over fail-open when hardening a security boundary under ambiguity
When code review found two plausible fixes for the `--root`-defeats-D-13 boundary (fail-safe:
resolve+case-fold, over-excluding under edge-case checkout paths; vs. fail-open-friendlier: a
minimal as-given correction), the persona round resolved on the rigour tie-break toward the fix
that **over-excludes** (fails safe, an empty readout) rather than one that could still leak under
an unanticipated alias.

**When to use:** Any time a "never leak / never source X" invariant has a fix-choice between a form
that risks under-exclusion (leak) and one that risks over-exclusion (false negative on legitimate
input) — prefer over-exclusion for boundaries whose entire purpose is preventing pollution of a
downstream number.
**Source:** .planning/phases/12-calibration/12-REVIEW.md (CR-01 resolution)

---

## Surprises

### The Statistician review's own overlap claim (F4) was overstated and got corrected on independent re-check
The adversarial Statistician review argued the friction-dominant codes were "the same tempdir
artifacts §3 excludes from FPR" (implying ~3x inflation of the reported friction rate) and proposed
a "~2 semantic over-blocks/cell" corrected figure. An independent orchestrator re-check of the
actual code sets found only **one** code (`DSX-CLM-031`) overlaps between the FPR-exclusion set and
the friction-dominant set — the other three friction-dominant codes are documented incidental
corpus gaps, not FPR-excluded noise. The reviewer's proposed figure was withdrawn.

**Impact:** Demonstrates the phase's own "independently re-verify every load-bearing claim, even
the adversarial reviewer's" discipline catching a reviewer error, not just an executor error — the
original RAW/NET disclosure stood unchanged.
**Source:** .planning/phases/12-calibration/12-READOUT.md §4, §8.2 (F4)

---

### The three "absent" catch-attribution codes are actually shipped, catalogued codes
The readout's framing initially implied the `absent_code` sidecar field names a code that doesn't
exist. Review (F1) confirmed all three named codes — DSX-EXP-051, DSX-VAL-080, DSX-REP-020 — are
fully shipped, catalogued, and emitted by real code paths; what is genuinely absent is the
*capability* to catch the defect in its undisclosed/fabricated instantiation, not the code itself.

**Impact:** Required retitling the readout's §2b column and rewriting the surrounding prose — a
purely framing-level fix with no change to any fixture, code, or measured number.
**Source:** .planning/phases/12-calibration/12-READOUT.md §2b, §8.1 (F1)

---

### Miss-rate 1.0 is a construction invariant, not a sampled detection rate
Because the ABSENT partition is curated (`kind: miss`, each case confirmed to miss before
inclusion), the 3/3 = 1.0 miss-rate is guaranteed by the partition's construction within any passing
run — it carries no information about a population-level miss propensity, and a confidence interval
on it would be meaningless.

**Impact:** The evidential content of the ABSENT partition is not the aggregate 1.0 but the three
independent `fires_at_any_severity: false` per-case confirmations; the readout was rewritten to make
this distinction explicit rather than implying 1.0 estimates anything.
**Source:** .planning/phases/12-calibration/12-READOUT.md §1, §8.1 (F3)

---

### DSX-VAL-080 (minted only in Phase 11.3) genuinely fires nowhere, even at HIGH, resolving an open cross-phase flag
An open question flagged in an earlier wave asked whether `operator-known-answer-selective-exclusion`
was a genuine miss or a HIGH-severity catch hidden by the corpus's CRITICAL-only miss lens, since
DSX-VAL-080 now exists. Measuring at every severity (not just CRITICAL) across all four gate points
found it fires nowhere at all — because the fixture's exclusion is *undeclared*, while DSX-VAL-080
fires on a *declared* exclusion lacking justification, so it has no declared exclusion to catch.

**Impact:** Resolved the flag definitively: the miss is structural (a declaration-only gate cannot
see an undeclared choice), not an artifact of the CRITICAL-only measurement lens.
**Source:** .planning/phases/12-calibration/12-READOUT.md §2b

---

### A documented, first-class CLI flag could silently defeat the phase's central integrity boundary
`--root` is a normal, help-documented flag with no special warning, yet pointing it at or inside
the excluded fixture tree silently flipped the reported Bayesian share to 20% — precisely the false
§6.5 item-4 auto-promotion scenario D-13 exists to prevent — while the command still returned exit
0 and the existing guard test stayed green throughout, having never exercised that exact vector.

**Impact:** The single highest-severity finding of the phase's code review (CR-01); required a
fix hardening the exclusion to resolved absolute path matching plus a new guard test
(`test_root_pointed_at_the_floor_still_excludes_it`) pinning the exact vector that had been missed.
**Source:** .planning/phases/12-calibration/12-REVIEW.md (CR-01, WR-01)

---

### Twenty-one test count grew, zero finding codes grew
Across the phase the full suite grew from ~1200 to 1221 tests and multiple new harness helpers,
sidecars, and a new CLI subcommand were added — yet the finding-code catalogue stayed pinned at
exactly 256 throughout, confirmed by a dedicated invariant test at the end of every plan. The
entirety of the phase's surface growth was measurement and test infrastructure, never detection
capability.

**Impact:** Concretely demonstrates the phase's stated framing ("this phase mints ZERO new
DSX-* finding codes") held in practice across seven plans and a code-review remediation cycle, not
just in the phase's stated intent.
**Source:** .planning/phases/12-calibration/12-VERIFICATION.md; .planning/phases/12-calibration/12-06-SUMMARY.md; .planning/phases/12-calibration/12-07-SUMMARY.md
