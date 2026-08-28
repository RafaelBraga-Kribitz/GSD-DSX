# Phase 12: Calibration - Context

**Gathered:** 2026-08-27 (assumptions mode; headless ceremony — AskUserQuestion gates replaced by a Statistician-led 3-persona round per LOOP-BRIEF §4)
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 12 is the **terminal, measurement-only** phase of milestone v2.0.0 (DSX Validity Frame).
Its product is *a number*: a measured **catch rate** and **false-positive rate** over a
full-size known-bad corpus, a **paradigm split** across the operator's own frame history, and
a re-evaluation of every §6.5 gated-backlog entry condition against that measured evidence.

Scope anchor (ROADMAP.md §"Phase 12: Calibration", REQ-P12-01..05):

- REQ-P12-01 — extend the known-bad corpus to full size (retracted papers with published
  post-mortems, documented p-hacking cases, the operator's own prior work whose answer is now
  known; each a spec+postmortem pair).
- REQ-P12-02 — corpus cases carry structured, machine-readable **catch-attribution** tags so
  §6.5 entry conditions are machine-*countable* (D-13); the harness also reports a per-family
  **friction** column (non-target blocking findings per fixture) computed from the LIVE corpus —
  the hand-maintained attribution ledger is stale and MUST NOT be lifted.
- REQ-P12-03 — a harness reports catch rate and false-positive rate as reproducible numbers,
  per-case pass/block, attributable to specific codes.
- REQ-P12-04 — `dsx stats --paradigm` reports the frequentist/Bayesian split across the
  operator's own frame history.
- REQ-P12-05 — each §6.5 item is re-evaluated against its stated entry condition using the
  measured corpus; items whose condition cannot be evaluated are removed rather than carried
  (D-14 reversal record where a removal reverses a prior decision).

**This phase mints ZERO new `DSX-*` finding codes and adds nothing to `GATE_PROFILES`** — it is
measurement, reporting and backlog hygiene, not detection. The catalogue stays at 256 (D-18).

**Not in scope:** any new detection check; writing the unwritten frequentist mirrors that
would promote §6.5 prior/convergence items; a `dsx quiz` fading mode; enforcing `SELF-001`
as a subcommand (brief §6.6 item 3). These are named in Deferred Ideas.
</domain>

<decisions>
## Implementation Decisions

Every decision below was settled by a **Statistician-led 3-persona round** (Statistician
`dsx-statistician` = lead; Architect `dsx-analysis-architect`; Auditor `dsx-ml-integrity-auditor`;
all opus, concurrent), tie-break **rigour > reliability > flexibility**. They are loud and
**vetoable via the daily summary** (LOOP-BRIEF §4); none is a HUMAN-QUEUE escalation because
none mints a D-06 finding code, changes a numbered requirement, or is destructive. The one
irreversible artifact minted here — the D-14 reversal record **REV-002** (D-16/D-17) — is a
backlog reclassification chartered by REQ-P12-05, not a milestone re-scope.

### Corpus composition and sizing

- **D-01:** "Full size" is an **evidence/coverage-driven target, not a fixed N.** Keep the
  glob-based discovery (`tests/test_known_bad_corpus.py:544-550`) and the existing `≥3` pair
  floor (`:627-632`); add **per-class coverage predicates** (≥1 retracted-paper+postmortem
  case, ≥1 documented p-hacking case, ≥1 operator-known-answer case), modelled on the existing
  `test_corpus_includes_an_interference_case_and_a_bayesian_continuous_case` predicate (`:634`).
  No hardcoded slug lists. "Full" is falsifiable by *class present*, not by an arbitrary count.
- **D-02:** **Source-before-count (anti-padding).** Cases are sourced from the real known-bad
  population and tagged as they are added; §6.5 counts are read off whatever falls out — a
  fixture is **never** reverse-engineered to trip a §6.5 threshold (that is the optional-stopping
  pathology the corpus exists to catch). If only two cases naturally show "absence permitted a
  false pass," §6.5 item 1 stays deferred — a valid *measured* outcome, not a failure.
- **D-03:** **Case contract = four files, glob-discovered on `<slug>`:**
  `<slug>-ANALYSIS-SPEC.yaml` (required), `<slug>-POSTMORTEM.md` (required, pairing already
  enforced at `:618`), `<slug>-entrypoint.py` (optional; code-scan cases only, per
  `full-frame-cleaning`), and the new `<slug>-ATTRIBUTION.yaml` (D-06; required for
  miss/backlog-promotion cases, absent for pure-catch cases).
- **D-04:** **Add a good-side control corpus for a real FPR denominator.** REQ-P12-03's
  false-positive *rate* is currently defined over a single clean spec
  (`examples/good-ANALYSIS-SPEC.yaml`, n=1 → 0/1 or k/1, no resolution). Add a multi-spec clean
  control set (target ≈ ≥10 clean specs spanning paradigms and outcome shapes) so FPR is a rate
  with resolution. This *delivers* REQ-P12-03 (an honest number), it is not new capability.
  Exact size is a planning choice. **(Statistician "concerns" flag — must be closed for "there
  is a number" to mean a valid number.)**

### Catch-attribution (miss-attribution) tags

- **D-05:** **Polarity — the tag names the currently-ABSENT code** that *would* have caught a
  **miss**, plus which §6.5 item it promotes (D-13 machine-countability). This is the *opposite*
  polarity to the two existing maps, which name **present** codes that *do* fire
  (`_TARGET_DEFECT_CODES` `:172-248`, `_EXPECTED_CAUGHT_DEFECTS` `:388-421`). Do not overload
  those maps.
- **D-06:** **Carrier = a per-fixture SIDECAR file** `examples/known-bad/<slug>-ATTRIBUTION.yaml`,
  glob-discovered on the slug. Rejected alternatives, on contract grounds: a **top-level spec
  key** (leaks a known-bad-fixture concept — "the code that would have caught me" — into the
  shipped product spec contract that real analysts write); a **postmortem-prose block** (couples
  machine-countable data to CRLF-sensitive prose parsing); a **harness-side map** (the exact
  stale hand-maintained-ledger anti-pattern REQ-P12-02 bans). The sidecar is machine-countable
  (glob + YAML load), **frame_digest-safe** (it is not in the spec at all, so it cannot perturb
  `frame_digest`/trip `DSX-PRE-020` — the hazard 11.3 D-08 handled by keeping such fields out of
  the `validity_frame`/`inference` subtree, `dsx/decisions.py:241-250`), and instrumented **as
  each case is added**, not retrofitted.
- **D-07:** **Sidecar schema** `{ absent_code (required), promotes_backlog_item (required),
  rationale? (optional, one line), kind? (optional, default "miss") }`. `absent_code` is
  validated against the **union** of the 256 shipped catalogue codes and the named §6.5 backlog
  codes (e.g. `DSX-PAR-022`) — *referencing* an unbuilt backlog code is the point and is **not**
  minting (D-18). `promotes_backlog_item` is a real §6.5 item id — this is the field that makes
  the D-13 entry conditions countable ("≥3 cases where absence permitted a false pass" = count of
  sidecars naming that item). A sibling-integrity test (mirroring `:618`) asserts every sidecar
  names a real slug, a code in the validated union, and a real §6.5 item id.
- **D-08:** **Tag falsifiability (anti-laundering).** The harness **verifies** each tag against
  a live `_gate_findings` run (`:555-616`): for a **miss** tag, assert the named absent code does
  **not** fire at **any** gate point (union of plan/execute/verify/ship — not merely the one point
  where it happens to be silent); for a **caught** case, the named code **does** fire CRITICAL
  (keep the existing positive-test shape). A named code that is **hypothetical/unshipped** is
  inherently unfalsifiable ⇒ it counts as a **miss**, never toward catch rate ("we'd catch it
  with a code we haven't written" inflates nothing). Count **distinct live-confirmed cases only**.

### Catch-rate / FPR / friction harness

- **D-09:** **Every reported number is computed LIVE** via `_gate_findings` (fresh
  `tempfile.TemporaryDirectory`, `:555-616`) and `_classify_target_defect` (`:251-306`), never
  lifted from the stale hand-maintained ledgers `_INCIDENTAL_GAP_CODES` (`:64-88`, stamped
  "measured 2026-08-08") or `_GOLDEN_SHIP_FINDINGS`
  (`tests/test_causal_verb_golden.py:82-142`, stamped "Measured 2026-08-26") — those are the
  snapshots REQ-P12-02 forbids lifting because they silently rot the moment a new check ships.
- **D-10:** **Stratify catch rate by target-code PRESENT vs ABSENT**, each with its own
  denominator, per-case and attributable. **Headline = (miss-rate, FPR)**, *not* catch-rate
  alone: every current fixture carries a present-and-firing code, so a single headline rate is a
  regression-pin dressed as detection and adding already-caught cases drives it to ~100% for
  free. **Floor the ABSENT/miss partition** so a 100%-present corpus cannot pass as a
  calibration. Adding easy catches must be mathematically incapable of moving the headline.
- **D-11:** **Friction column = `live(ship-blocking findings) − live(own-target-codes)`, per
  family, reported RAW and NET.** Net-only is a laundering hole (a fixture over-blocking on 5
  unrelated codes looks clean if 2 are "its own", and codes can be relabelled incidental→own to
  shrink it); raw exposes total over-blocking, net attributes the intended share. Express as a
  per-family **rate** over non-target in-profile (fixture × gate-point) cells, not a bare count.
  Three guards: (a) a **synthetic arithmetic proof** (net = raw − own on a fabricated finding
  dict, filesystem-independent); (b) a **live-source proof** (friction consumes the *same*
  `_gate_findings` set as the golden test, so a lifted/hardcoded number breaks); (c) close the
  **incidental→own relabel path** — every `_TARGET_DEFECT_CODES` entry must be positively verified
  firing CRITICAL *and* named in that fixture's postmortem/attribution, so a code cannot be
  demoted out of friction without publicly declaring it the intended defect.

### `dsx stats --paradigm`

- **D-12:** **Wiring — a new `stats` argparse subparser** (the name is free; `dsx stats` today
  is only a *check* label at `dsx/cli.py:67`, not a subcommand) + `cmd_stats` modelled on
  `cmd_explain` (`:563-637`): a **pure reader that always `return 0` by construction**, with
  `--json`, and **no `--block-on`**. It is not a check and is **not** added to `GATE_PROFILES`.
- **D-13:** **Source = real operator `.planning/` decision trails ONLY.** Hard-**exclude**
  `examples/known-bad/DECISIONS.jsonl` — a polluted test floor (measured: ~1,151 invocation
  records but only 15 distinct `frame_digest` / 2 `spec_id`, ~45.8% raw-Bayesian), which counted
  raw would trip the §6.5 item-4 "Bayesian > 15%" gate roughly four-fold on fixture re-runs. The
  harness carries a **negative assertion** that the command never sources the known-bad floor.
- **D-14:** **Dedup unit = distinct `frame_digest`** — the deterministic per-frame content hash
  (`dsx/decisions.py:241-250`); re-running the same spec collapses to one frame, so re-runs
  cannot inflate the split. `spec_id` is used only as a human label / secondary diagnostic (it is
  frequently unset/`None` in the trail, so it is the wrong primary key). Paradigm is read per
  frame from its `choice="paradigm=…"` decision record (`dsx/frame/paradigm.py:616,626`); one
  paradigm per distinct frame (paradigm lives inside the `inference` block, so it is captured by
  the digest). **Denominator for the split = count of distinct operator `frame_digest`s**; the
  raw invocation count is reported only as a secondary diagnostic so the 15% predicate has one
  unambiguous denominator. **Guard:** a synthetic-trail test — N distinct frequentist frames each
  repeated many times as invocation records + 1 distinct Bayesian frame ⇒ the reported share is
  over *distinct frames* (e.g. 1/(N+1)), not the raw-record proportion.

### §6.5 backlog re-evaluation and reversals

- **D-15:** **Disposition of the nine §6.5 items (`brief.md:369-379`): carry 8, remove 1.**
  Items **4** (Bayesian admissibility — "M4 ships AND `dsx stats --paradigm` shows Bayesian
  > 15%") and **5** (`dsx quiz` fading — "M5 ships") are **CARRIED as prerequisite-pending** —
  their conditions are *evaluable-and-unmet*, not unevaluable — and item 4 must **not** be
  auto-promoted by the polluted-floor artifact (the honest operator-scoped split under D-13/D-14
  is expected < 15%; that non-promotion is the point of the number, brief `:360-362`). Items
  **1, 3** carry (their frequentist mirrors are unwritten under D-12a; a corpus count cannot
  promote them). Item **2** (prior predictive `DSX-PAR-022`) is already promoted (REV-001). Items
  **7, 8, 9** carry, **measurement-decided**: promote *only* if the measured corpus + attribution
  tags actually yield the naming case (≥1 miss attributable *only* via feature origin for 7; a
  case passing all claims checks while asserting an uncomputed magnitude for 8 — likely none,
  since paper instances already fire `DSX-CLM-070`; an admissible D-05 source *and* a corpus case
  for 9). **Never manufacture the case** (D-02).
- **D-16:** **Item 6 (Deng & Hu 2015 ratio-metric dilution) is REMOVED as structurally
  unevaluable** — not merely unmet. Its entry condition ("a source of per-unit trigger and
  outcome data reaching the gate") requires a computation the **D-01/D-02 determinism doctrine
  forbids on the gate path**, and that constraint does not lift with time. Mechanism: **relocate
  the row (do not delete it)** into a "Removed / permanently out of scope (D-14)" subsection of
  §6.5, **preserving the substrings pinned by** `tests/test_known_bad_corpus.py:1043-1069`
  ("Ratio-metric dilution for trigger analysis", "Formula (3)", "per-unit trigger and outcome
  data reaching the gate") — or update that pin test in lockstep. File **REV-002** (next id; only
  REV-001 exists in `.planning/REVERSALS.md`).
- **D-17:** **REV-002 must survive the SELF-001 self-consistency check.** The reversal is
  *deferred → permanently out of scope*. The determinism doctrine is **not** new evidence (it
  pre-dates the deferral, and the §6.5 row *already* records both it and "access was never the
  blocker" / "no closed-form scalar multiplier"), so REV-002's "New evidence" field must **not**
  launder the doctrine as novelty — that trips `SELF-001` (`.planning/REVERSALS.md:40-56`).
  Frame it honestly as a **reclassification under Phase-12's systematic §6.5 re-evaluation
  (REQ-P12-05)** that recognizes the entry condition as structurally unreachable: *what would
  have made the original deferral correct* = a declaration-evaluable scalar (Formula (3) has
  none); *what did not change* = D-01/D-02, the additive `DSX-INT-030` case stays shipped, items 4
  & 5 stay carried. **General rule locked:** "unevaluable ⇒ remove" applies *only* to structural
  unreachability, never to a merely-unmet condition; each such removal needs a D-14 REV **and**
  retention of the pinned corrected row.

### Finding-code footprint

- **D-18:** **Phase 12 mints ZERO `DSX-*` finding codes; the catalogue stays 256, unchanged.**
  `dsx stats --paradigm` is a reader; the friction column is arithmetic over existing findings;
  attribution tags *reference* existing-or-hypothetical codes; the §6.5 reshuffle instantiates no
  code. `SELF-001` is a `.planning/REVERSALS.md` convention, not a catalogue code. Add a
  **catalogue-invariant test** asserting the code count remains 256 after Phase 12. Nothing is
  registered in `GATE_PROFILES` (`dsx/cli.py:115-131`).

### Claude's Discretion

- The exact net-new corpus size and the good-side control-set size (D-01, D-04) are planning
  choices bounded by "every §6.5 count decidable" and "FPR denominator with resolution (≈≥10)".
- Precise sidecar field names and the harness report layout (columns/ordering) are the planner's
  to finalize, provided the D-07 schema fields and the D-08/D-10/D-11 guards are present.

### Folded Todos

None — `todo.match-phase 12` returned 0 matches.
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents (researcher, planner) MUST read these before planning or implementing.**

- `brief.md` — §"M5: Calibration" (lines ~354-362); §6.5 "Gated backlog (D-13)" nine-item table
  and REV-001 (lines ~364-397); D-13/D-14 (lines ~108-110); §6.6 open items (lines ~421-434);
  the determinism doctrine D-01/D-02 (§4).
- `.planning/ROADMAP.md` — "Phase 12: Calibration" (goal, 5 success criteria, ordering
  constraint that REQ-P12-02 tags are instrumented as each case is added, lines ~993-1028).
- `.planning/REQUIREMENTS.md` — REQ-P12-01..05 (lines ~175-181).
- `.planning/REVERSALS.md` — D-14 reversal template (lines ~18-38), REV-001 precedent
  (lines ~60-81), and the SELF-001 self-consistency finding (lines ~40-56) that REV-002 must
  survive.
- `tests/test_known_bad_corpus.py` — the corpus harness: `_INCIDENTAL_GAP_CODES` (`:64-88`, the
  stale ledger), `_TARGET_DEFECT_CODES` (`:172-248`), `_EXPECTED_CAUGHT_DEFECTS` (`:388-421`),
  `_gate_findings` (`:555-616`), `_classify_target_defect` (`:251-306`), the `≥3` size floor and
  coverage predicate (`:627-634`), and the Deng & Hu falsifiable-blocker pin (`:1043-1069`).
- `tests/test_causal_verb_golden.py` — `_GOLDEN_SHIP_FINDINGS` (`:82-142`, the second stale
  ledger) and the fresh-tempdir reproducibility discipline (`:18-20`).
- `dsx/cli.py` — `CHECKS` registry (`:64-85`, `stats` is a check label at `:67`),
  `GATE_PROFILES` (`:115-131`), the `cmd_explain` reader template (`:563-637`), subparser
  registration (`:810-925`), `_write_decision_trail` (`:334-393`).
- `dsx/frame/paradigm.py` — paradigm recorded as `choice="paradigm=…"` (`:616,626`).
- `dsx/decisions.py` — `frame_digest` (`:241-250`), `decisions_path`/`read_all` (`:182-257`),
  `InvocationHeader`/`spec_id` grouping (`:110-121`).
- `references/finding-codes.md` — the 256-code catalogue (Total at `:16`); the invariant D-18
  pins.
- `examples/known-bad/` — the 8 current spec+postmortem pairs + shared `DECISIONS.jsonl`;
  `examples/good-ANALYSIS-SPEC.yaml` — the current (n=1) FPR baseline.
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **The whole live-gate measurement substrate already exists** and is the intended base for
  REQ-P12-02/03: `_gate_findings` runs a real `dsx gate <point>` in a fresh tempdir and returns
  `(exit_code, findings)`; `_classify_target_defect` records per `(slug, point)` whether the
  target code is among CRITICAL findings. Catch rate, FPR and friction are computations over
  these, not new machinery.
- **Glob-based corpus discovery** (`_slugs`, `CORPUS_DIR.glob`) means new cases and new sidecars
  are picked up without editing the harness — preserve this; never hardcode a slug list.
- **`cmd_explain`** is the exact template for `cmd_stats`: a pure reader that never imports the
  block-contract primitives and returns 0 by construction.
- **The paradigm signal is already persisted** in every gate run's decision trail as
  `choice="paradigm=frequentist|bayesian|undeclared"` via the `DSX-PAR-001` manifest record —
  `dsx stats --paradigm` reads it, it does not compute it.

### Established Patterns
- **Placement discipline (11.3 D-08):** anything that must not perturb the content lock lives
  *outside* the `validity_frame`/`inference` subtree that `frame_digest` hashes (top-level
  `spec_id` is the precedent). The attribution tag honors this by living in a **sidecar**, not in
  the spec at all.
- **Anti-laundering guards are the house style** (e.g. `_INCIDENTAL_GAP_CODES`' allowlist guard
  asserting it names no slug's own target code). D-08/D-11 extend this pattern to the new
  attribution tags and the friction column.
- **Reproducibility via fresh-tempdir-per-run** keeps the shared `DECISIONS.jsonl` out of
  `examples/` (RESEARCH "landmine f"); every new measurement must follow it.
- **D-14 reversals are relocations, not deletions** when a test pins the row's text — REV-002
  must preserve the pinned Deng & Hu substrings.

### Integration Points
- **`dsx/cli.py`** — one new `stats` subparser + `cmd_stats`; **no** change to `CHECKS` or
  `GATE_PROFILES`.
- **`tests/test_known_bad_corpus.py`** — extended with the coverage predicates (D-01), the
  sidecar sibling-integrity + falsifiability tests (D-07/D-08), the stratified rate and the
  live-computed friction column (D-10/D-11), and the catalogue-invariant test (D-18).
- **`examples/known-bad/`** — new `<slug>-*` case files + `<slug>-ATTRIBUTION.yaml` sidecars.
- **`brief.md` §6.5 + `.planning/REVERSALS.md`** — the REQ-P12-05 dispositions + REV-002.
- **A new operator good-side control set** (D-04) — location a planning choice (e.g.
  `examples/good/` or a control directory the FPR harness globs).
</code_context>

<specifics>
## Specific Ideas

- The §6.5 item-4 "Bayesian frames > 15%" number is the milestone's self-audit instrument: the
  brief explicitly wants it to come back *low* if the operator's real work is frequentist, and a
  polluted-floor "45.8%" would silently invert that instrument. D-13/D-14 exist to protect it.
- REV-002 is the delicate artifact of this phase: it must be the honest kind of reversal (a
  reclassification recognizing structural unreachability), not the laundered kind (determinism
  restated as "new evidence"), or it fails its own SELF-001 convention.
</specifics>

<deferred>
## Deferred Ideas

- **Writing the unwritten frequentist mirrors** (specification-sensitivity for §6.5 item 1;
  estimation-convergence for item 3) that would let those items promote — separate future work
  under D-12a, not Phase 12.
- **`dsx quiz` fading mode** (§6.5 item 5) — future product mode, not a check, gated on M5 ship.
- **`SELF-001` enforcement as a `dsx` subcommand** (brief §6.6 item 3) — currently a
  `REVERSALS.md` convention; making it a checked subcommand is out of Phase-12 scope.
- **Bayesian admissibility ontology** (§6.5 item 4, `DSX-ADM-*` second axis) — gated on M4 ship
  *and* a genuine >15% Bayesian operator history; Phase 12 supplies only the measured split.

### Reviewed Todos (not folded)
None — `todo.match-phase 12` returned 0 matches.

### D-05 pre-registration note
New corpus cases added under REQ-P12-01 (retracted papers, documented p-hacking cases) will each
need a **D-05 primary-source citation read** (verbatim quote at locator — the project's human
bar), owed at the Phase-12 UAT/ship round and assembled the way HQ-1/HQ-4/HQ-5 packs were. The
cases are not sourced yet, so no HUMAN-QUEUE item is opened now; the round is pre-registered.
</deferred>
