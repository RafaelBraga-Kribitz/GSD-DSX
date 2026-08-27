# Phase 12: Calibration - Research

**Researched:** 2026-08-27
**Domain:** Measurement/reporting harness over an existing deterministic gate (no new detection code); Python stdlib test-suite engineering
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Corpus composition and sizing**
- **D-01:** "Full size" is an evidence/coverage-driven target, not a fixed N. Keep the glob-based
  discovery (`tests/test_known_bad_corpus.py:544-550`) and the existing `≥3` pair floor
  (`:627-632`); add per-class coverage predicates (≥1 retracted-paper+postmortem case, ≥1
  documented p-hacking case, ≥1 operator-known-answer case), modelled on the existing
  `test_corpus_includes_an_interference_case_and_a_bayesian_continuous_case` predicate (`:634`).
  No hardcoded slug lists.
- **D-02:** Source-before-count (anti-padding). Cases are sourced from the real known-bad
  population and tagged as they are added; §6.5 counts are read off whatever falls out — never
  reverse-engineer a fixture to trip a §6.5 threshold.
- **D-03:** Case contract = four files, glob-discovered on `<slug>`: `<slug>-ANALYSIS-SPEC.yaml`
  (required), `<slug>-POSTMORTEM.md` (required, pairing already enforced at `:618`),
  `<slug>-entrypoint.py` (optional; code-scan cases only), and the new `<slug>-ATTRIBUTION.yaml`
  (D-06; required for miss/backlog-promotion cases, absent for pure-catch cases).
- **D-04:** Add a good-side control corpus for a real FPR denominator. REQ-P12-03's FPR is
  currently defined over a single clean spec (`examples/good-ANALYSIS-SPEC.yaml`, n=1 → 0/1 or
  k/1, no resolution). Add a multi-spec clean control set (target ≈ ≥10 clean specs spanning
  paradigms and outcome shapes). Statistician "concerns" flag — must be closed for "there is a
  number" to mean a valid number.

**Catch-attribution (miss-attribution) tags**
- **D-05:** Polarity — the tag names the currently-ABSENT code that would have caught a miss,
  plus which §6.5 item it promotes. Opposite polarity to `_TARGET_DEFECT_CODES` (`:172-248`) and
  `_EXPECTED_CAUGHT_DEFECTS` (`:388-421`), which name present codes that do fire. Do not overload
  those maps.
- **D-06:** Carrier = a per-fixture sidecar file `examples/known-bad/<slug>-ATTRIBUTION.yaml`,
  glob-discovered on the slug. Rejected: top-level spec key (leaks a fixture concept into the
  real spec contract), postmortem-prose block (couples machine-countable data to CRLF-sensitive
  prose parsing), harness-side map (the stale hand-maintained-ledger anti-pattern REQ-P12-02
  bans). Frame_digest-safe: not in the spec at all, so it cannot perturb `frame_digest`/trip
  `DSX-PRE-020`. Instrumented as each case is added, not retrofitted.
- **D-07:** Sidecar schema `{ absent_code (required), promotes_backlog_item (required),
  rationale? (optional), kind? (optional, default "miss") }`. `absent_code` validated against the
  union of the 256 shipped catalogue codes and named §6.5 backlog codes (e.g. `DSX-PAR-022`) —
  referencing an unbuilt backlog code is the point, not minting. `promotes_backlog_item` is a
  real §6.5 item id. A sibling-integrity test (mirroring `:618`) asserts every sidecar names a
  real slug, a code in the validated union, and a real §6.5 item id.
- **D-08:** Tag falsifiability (anti-laundering). The harness verifies each tag against a live
  `_gate_findings` run (`:555-616`): for a miss tag, assert the named absent code does not fire
  at ANY gate point (union of plan/execute/verify/ship); for a caught case, the named code DOES
  fire CRITICAL. A hypothetical/unshipped named code is inherently unfalsifiable ⇒ counts as a
  miss, never toward catch rate. Count distinct live-confirmed cases only.

**Catch-rate / FPR / friction harness**
- **D-09:** Every reported number is computed LIVE via `_gate_findings` (fresh
  `tempfile.TemporaryDirectory`, `:555-616`) and `_classify_target_defect` (`:251-306`), never
  lifted from `_INCIDENTAL_GAP_CODES` (`:64-88`, stamped "measured 2026-08-08") or
  `_GOLDEN_SHIP_FINDINGS` (`tests/test_causal_verb_golden.py:82-142`, stamped "Measured
  2026-08-26").
- **D-10:** Stratify catch rate by target-code PRESENT vs ABSENT, each with its own denominator,
  per-case and attributable. Headline = (miss-rate, FPR), not catch-rate alone. Floor the
  ABSENT/miss partition so a 100%-present corpus cannot pass as a calibration.
- **D-11:** Friction column = `live(ship-blocking findings) − live(own-target-codes)`, per family,
  reported RAW and NET. Express as a per-family rate over non-target in-profile (fixture ×
  gate-point) cells. Three guards: (a) synthetic arithmetic proof (filesystem-independent); (b)
  live-source proof (friction consumes the same `_gate_findings` set as the golden test); (c)
  close the incidental→own relabel path — every `_TARGET_DEFECT_CODES` entry must be positively
  verified firing CRITICAL AND named in that fixture's postmortem/attribution.

**`dsx stats --paradigm`**
- **D-12:** Wiring — a new `stats` argparse subparser (`dsx stats` today is only a check LABEL at
  `dsx/cli.py:67`, not a subcommand) + `cmd_stats` modelled on `cmd_explain` (`:563-637`): a pure
  reader that always `return 0` by construction, with `--json`, no `--block-on`. Not a check, not
  added to `GATE_PROFILES`.
- **D-13:** Source = real operator `.planning/` decision trails ONLY. Hard-exclude
  `examples/known-bad/DECISIONS.jsonl` — a polluted test floor (measured: ~1,151 invocation
  records but only 15 distinct `frame_digest` / 2 `spec_id`, ~45.8% raw-Bayesian), which counted
  raw would trip the §6.5 item-4 "Bayesian > 15%" gate roughly four-fold on fixture re-runs. The
  harness carries a negative assertion that the command never sources the known-bad floor.
- **D-14:** Dedup unit = distinct `frame_digest` (`dsx/decisions.py:241-250`); re-running the same
  spec collapses to one frame. `spec_id` is a secondary diagnostic only (frequently
  unset/`None`). Paradigm read per frame from `choice="paradigm=…"` (`dsx/frame/paradigm.py
  :616,626`). Denominator = count of distinct operator `frame_digest`s; raw invocation count is a
  secondary diagnostic. Guard: a synthetic-trail test — N distinct frequentist frames each
  repeated many times + 1 distinct Bayesian frame ⇒ reported share is over distinct frames
  (e.g. 1/(N+1)), not the raw-record proportion.

**§6.5 backlog re-evaluation and reversals**
- **D-15:** Disposition of the nine §6.5 items: carry 8, remove 1. Items 4 (Bayesian
  admissibility) and 5 (`dsx quiz` fading) CARRIED as prerequisite-pending — item 4 must NOT be
  auto-promoted by the polluted-floor artifact. Items 1, 3 carry (frequentist mirrors unwritten).
  Item 2 already promoted (REV-001). Items 7, 8, 9 carry, measurement-decided — promote only if
  the measured corpus + attribution tags actually yield the naming case. Never manufacture the
  case (D-02).
- **D-16:** Item 6 (Deng & Hu 2015 ratio-metric dilution) is REMOVED as structurally
  unevaluable — its entry condition requires a computation the D-01/D-02 determinism doctrine
  forbids on the gate path, and that constraint does not lift with time. Mechanism: relocate the
  row (do not delete it) into a "Removed / permanently out of scope (D-14)" subsection of §6.5,
  preserving the substrings pinned by `tests/test_known_bad_corpus.py:1043-1069` ("Ratio-metric
  dilution for trigger analysis", "Formula (3)", "per-unit trigger and outcome data reaching the
  gate") — or update that pin test in lockstep. File REV-002 (next id; only REV-001 exists).
- **D-17:** REV-002 must survive the SELF-001 self-consistency check. The determinism doctrine is
  NOT new evidence (it pre-dates the deferral). Frame it honestly as a reclassification under
  Phase-12's systematic re-evaluation (REQ-P12-05) recognizing structural unreachability. General
  rule: "unevaluable ⇒ remove" applies only to structural unreachability, never a merely-unmet
  condition; each such removal needs a D-14 REV AND retention of the pinned corrected row.

**Finding-code footprint**
- **D-18:** Phase 12 mints ZERO `DSX-*` finding codes; catalogue stays 256, unchanged. Add a
  catalogue-invariant test asserting the code count remains 256 after Phase 12. Nothing
  registered in `GATE_PROFILES` (`dsx/cli.py:115-131`).

### Claude's Discretion

- The exact net-new corpus size and the good-side control-set size (D-01, D-04) are planning
  choices bounded by "every §6.5 count decidable" and "FPR denominator with resolution (≈≥10)".
- Precise sidecar field names and the harness report layout (columns/ordering) are the planner's
  to finalize, provided the D-07 schema fields and the D-08/D-10/D-11 guards are present.

### Deferred Ideas (OUT OF SCOPE)

- Writing the unwritten frequentist mirrors (specification-sensitivity for §6.5 item 1;
  estimation-convergence for item 3) — separate future work under D-12a, not Phase 12.
- `dsx quiz` fading mode (§6.5 item 5) — future product mode, gated on M5 ship.
- `SELF-001` enforcement as a `dsx` subcommand (brief §6.6 item 3) — out of Phase-12 scope.
- Bayesian admissibility ontology (§6.5 item 4, `DSX-ADM-*` second axis) — gated on M4 ship AND a
  genuine >15% Bayesian operator history; Phase 12 supplies only the measured split.
- New corpus cases each need a D-05 primary-source citation read (verbatim quote at locator) owed
  at the Phase-12 UAT/ship round; pre-registered, not opened as a HUMAN-QUEUE item now.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-P12-01 | Extend the known-bad corpus to full size (retracted papers with published post-mortems, documented p-hacking cases, the operator's own prior work whose answer is now known; each a spec+postmortem pair) | Corpus census below (8 pairs currently) + D-01 coverage-predicate pattern already exists as a template (`test_corpus_includes_an_interference_case_and_a_bayesian_continuous_case`); new-spec landmine (golden-file glob) documented below |
| REQ-P12-02 | Structured, machine-readable catch-attribution tags; per-family friction column computed from the LIVE corpus | Sidecar mechanics (D-06/D-07/D-08) grounded against `dsx/decisions.py::frame_digest` and the existing informal prose precedent in postmortems (`## Which absent code would have caught it`); friction arithmetic grounded against `_gate_findings`/`_TARGET_DEFECT_CODES` |
| REQ-P12-03 | Harness reports catch rate and FPR as reproducible numbers, per-case pass/block, attributable to codes | `_gate_findings`/`_classify_target_defect` reuse pattern; FPR-denominator landmine (fresh-tempdir artifact-resolution noise) documented below — this is the single most load-bearing finding for an honest FPR |
| REQ-P12-04 | `dsx stats --paradigm` reports frequentist/Bayesian split across operator's own frame history | `cmd_explain` template verified at `dsx/cli.py:563-637`; architecture gap documented — `cmd_explain`'s single-root model does not generalize to a directory-tree aggregate, and no `.planning/`-rooted `DECISIONS.jsonl` exists yet in this repo |
| REQ-P12-05 | Every §6.5 item re-evaluated against its stated entry condition; unevaluable items removed | §6.5 table enumerated below (9 rows, row-to-item-number mapping confirmed); REV-002 template and SELF-001 guard verified against `.planning/REVERSALS.md`; pin-preservation test verified at `tests/test_known_bad_corpus.py:1043-1069` |
</phase_requirements>

## Summary

Phase 12 adds no detection logic. Its work is: (1) grow `examples/known-bad/` past its current 8
spec+postmortem pairs with coverage-predicate-gated new cases; (2) add a per-fixture
`<slug>-ATTRIBUTION.yaml` sidecar naming which absent code would have caught a miss, machine-
verified against a live gate run so the tag cannot lie; (3) extend the corpus test harness to
report catch rate/FPR/friction as live-computed, stratified numbers, and add a genuine multi-spec
good-side control corpus so FPR has a real denominator; (4) add a `dsx stats --paradigm`
subcommand that aggregates `frame_digest`-deduplicated paradigm choices across the operator's own
(not the fixture corpus's) decision trails; (5) re-evaluate all nine §6.5 backlog rows against
measured evidence, removing exactly one (ratio-metric dilution) via a REV-002 reversal record
that must not launder its own reasoning as "new evidence."

Verification of every anchor cited in `12-CONTEXT.md` against the live tree found **zero
material line-number drift** — every function/constant/test the CONTEXT.md cites is exactly
where it says it is (details in Anchor Verification below). The substantive risk in this phase is
not stale anchors; it is architectural gaps and measurement-honesty traps that CONTEXT.md's
decisions correctly anticipate in outline but that only become concrete once you run the actual
harness against the actual fixtures — which this research did. Four load-bearing findings that
CONTEXT.md does not (and could not, without running code) already state precisely:

1. The corpus harness's fresh-`tempfile.TemporaryDirectory()`-per-run pattern — essential for
   keeping `DECISIONS.jsonl` out of `examples/` — silently strips away a fixture's own committed
   sibling artifacts (DATA-PROFILE, figures, narrative, evidence files). Run today,
   `examples/good-ANALYSIS-SPEC.yaml` fires **4 real findings** (`DSX-DQ-001` CRITICAL +
   `DSX-CLM-031`/`DSX-FIG-001`/`DSX-NAR-010` HIGH) under this isolation — not because the analysis
   is invalid, but because the tempdir has no profile/figure/narrative files to resolve against.
   The new D-04 good-control corpus will reproduce this noise on every new spec unless the
   harness seeds sibling artifacts (extending the existing `_seed_entrypoint` pattern) or
   explicitly excludes these codes as harness-context noise (extending the existing
   `_INCIDENTAL_GAP_CODES` pattern).
2. A second, separate test file (`tests/test_causal_verb_golden.py`) recursively globs
   `examples/**/*-ANALYSIS-SPEC.yaml` and hard-fails
   (`test_golden_keys_match_the_examples_tree_on_disk`) the moment a new spec is committed
   anywhere under `examples/` without a matching golden CRITICAL/HIGH finding-set entry. This
   applies to every new REQ-P12-01 corpus case AND every new D-04 control-corpus spec — a second
   lockstep-update obligation invisible if you only read `test_known_bad_corpus.py`.
3. `dsx stats --paradigm`'s locked source, "real operator `.planning/` decision trails," has no
   existing target: no `DECISIONS.jsonl` exists anywhere under `.planning/` in this repo today.
   `cmd_stats` needs new multi-file directory-tree-walk logic (unlike `cmd_explain`'s single-root
   read), and run for real here it will report an honestly empty history — expected, not a bug,
   but it means the synthetic-trail test (D-14) is the only test that exercises the real
   aggregation logic in CI.
4. The CONTEXT.md cites "the hazard 11.3 D-08" as the precedent for keeping the sidecar's fields
   outside `validity_frame`/`inference`. Live-checked: that precedent is actually **11.2 D-08**
   (`spec_id` placement, `dsx/decisions.py:99-121`). 11.3's own D-08 is a different, near-opposite
   decision (`validity_frame.exclusions` deliberately placed INSIDE `validity_frame` so it IS
   digest-covered, `.planning/phases/11.3-.../11.3-CONTEXT.md:200-203`). Citing 11.3 D-08 when
   writing the sidecar design rationale points at the wrong precedent.

**Primary recommendation:** Build the ATTRIBUTION.yaml sidecar and the stratified catch-rate/FPR
harness as direct extensions of the existing `_gate_findings`/`_classify_target_defect`/
`_INCIDENTAL_GAP_CODES` machinery in `tests/test_known_bad_corpus.py` — every guard pattern D-08/
D-09/D-11 asks for already has a working precedent in that file. Solve the FPR-noise problem
(finding 1 above) before writing any new control-corpus spec, or the "there is a number" headline
will include noise the corpus author knows is spurious.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Known-bad corpus growth (new spec+postmortem pairs) | Test fixtures (`examples/known-bad/`) | — | Data, not code; discovered by glob, never registered anywhere |
| Catch-attribution sidecar (`<slug>-ATTRIBUTION.yaml`) | Test fixtures (`examples/known-bad/`) | Test harness (`tests/test_known_bad_corpus.py`) | Data lives beside the fixture; the harness is what reads, validates and falsifies it |
| Good-side control corpus (D-04) | Test fixtures (new location under `examples/`) | Test harness (new or extended module) | Same pattern as known-bad, opposite polarity (clean specs, not defective ones) |
| Catch-rate / FPR / friction harness | Test harness (`tests/test_known_bad_corpus.py`, extended) | Gate engine (`dsx gate <point>` via `cli.main`) | The harness computation lives in tests/; it *calls* the real CLI/gate engine, it does not reimplement gate logic |
| `dsx stats --paradigm` | CLI / reader command (`dsx/cli.py`, new `cmd_stats`) | Decisions layer (`dsx/decisions.py`) | Pure reader over `DECISIONS.jsonl` files, modelled on `cmd_explain`; never touches the block-contract/Report machinery |
| §6.5 backlog re-evaluation + REV-002 | Planning documents (`brief.md`, `.planning/REVERSALS.md`) | Test harness (pin-preservation test) | Prose editorial work with one machine-checked invariant (the substring pin) |
| Catalogue-invariant test (D-18) | Test harness (new test, likely in `tests/test_known_bad_corpus.py` or a catalogue-focused test module) | `references/finding-codes.md` (generated artifact) | Assertion over generated output, no new detection code |

## Standard Stack

No new third-party packages. D-01 ("Gate path is stdlib-only Python, hermetic, no third-party
imports") governs the entire codebase and Phase 12 introduces no exception to it — every new
piece of work (sidecar YAML parsing, harness computation, `cmd_stats`) reuses existing in-repo
modules (`dsx.loader.load`, `dsx.decisions.read_all`, `dsx.cli.main`) or Python stdlib
(`pathlib`, `tempfile`, `json`, `hashlib`, `collections.Counter`).

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python stdlib (`pathlib`, `tempfile`, `json`, `unittest`) | 3.12.10 (confirmed installed, `[VERIFIED: python --version]`) | Harness runtime | D-01 hermeticity; already the whole codebase's substrate |
| `dsx.loader.load` (in-repo) | n/a | Parse `<slug>-ATTRIBUTION.yaml` sidecars | Same bundled-YAML-subset parser already used for every ANALYSIS-SPEC and DATA-PROFILE — no new parsing surface |
| `dsx.decisions.read_all`/`frame_digest` (in-repo) | n/a | Read/dedup decision trails for `dsx stats --paradigm` | Exact functions D-13/D-14 name; `frame_digest` verified at `dsx/decisions.py:241-250` |

### Supporting

None. PyYAML is present in the dev environment (`[VERIFIED: python -c "import yaml"]` succeeded)
and is used elsewhere in the test suite for cross-checking the bundled parser (REQ-P6-01
precedent), but nothing in Phase 12 requires it — sidecar parsing should use `dsx.loader.load`
exactly like every other spec-adjacent YAML file in this repo, for the same hermeticity reason.

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Extending `tests/test_known_bad_corpus.py` | A brand-new `tests/test_calibration.py` module | CONTEXT.md's own Integration Points section directs extension of the existing file; a new module would duplicate `_gate_findings`/`_seed_entrypoint`/`seed_plan_header` machinery already proven correct there. Recommend: extend existing file for corpus-scoped tests (D-01/D-07/D-08/D-09/D-10/D-11/D-18); a fresh module is reasonable only for `dsx stats --paradigm`'s own CLI tests (mirrors how `cmd_explain` likely has its own test module — verify at plan time) |

**Installation:** none — no new dependencies.

**Version verification:** N/A, no new packages.

## Package Legitimacy Audit

Not applicable — Phase 12 introduces zero new third-party packages (D-01 hermeticity doctrine).
No legitimacy check was run because there is nothing to check.

**Packages removed due to [SLOP] verdict:** none
**Packages flagged as suspicious [SUS]:** none

## Architecture Patterns

### System Architecture Diagram

```
                    ┌─────────────────────────────────────────────┐
                    │        examples/known-bad/<slug>-*           │
                    │  (glob-discovered: SPEC, POSTMORTEM,          │
                    │   optional entrypoint.py, optional            │
                    │   ATTRIBUTION.yaml sidecar — D-03)             │
                    └───────────────────┬───────────────────────────┘
                                         │ CORPUS_DIR.glob(*)
                                         ▼
                    ┌─────────────────────────────────────────────┐
                    │  tests/test_known_bad_corpus.py               │
                    │  ┌─────────────────────────────────────────┐ │
                    │  │ _gate_findings(spec, point)                │ │  fresh tempfile.TemporaryDirectory()
                    │  │  -> real `dsx gate <point>` via cli.main() │◄┼──── per call (never examples/DECISIONS.jsonl)
                    │  └─────────────────────┬───────────────────┘ │
                    │                         ▼                     │
                    │  ┌─────────────────────────────────────────┐ │
                    │  │ _classify_target_defect(slug, point, …)    │ │  compares live findings against
                    │  │  -> pass/fail per (slug, point)            │ │  _TARGET_DEFECT_CODES /
                    │  └─────────────────────┬───────────────────┘ │  _EXPECTED_CAUGHT_DEFECTS (existing)
                    │                         │                     │
                    │  ┌─────────────────────▼───────────────────┐ │
                    │  │ NEW: catch-rate / FPR / friction report    │ │  D-09/D-10/D-11 —
                    │  │  reads ATTRIBUTION.yaml sidecars, verifies │ │  stratified PRESENT/ABSENT,
                    │  │  falsifiability (D-08), computes RAW/NET   │ │  raw+net friction, both guarded
                    │  │  friction, floors the ABSENT partition     │ │  by synthetic + live-source proofs
                    │  └─────────────────────────────────────────┘ │
                    └─────────────────────────────────────────────┘
                                         ▲
                                         │ same fresh-tempdir _gate_findings pattern,
                                         │ extended with sibling-artifact seeding
                                         │ (NEW — see Pitfall 1)
                    ┌────────────────────┴──────────────────────────┐
                    │  examples/<good-control-dir>/*-ANALYSIS-SPEC   │  D-04 — multi-spec clean
                    │  (≥10 clean specs spanning paradigms/outcomes) │  control corpus, new location
                    └─────────────────────────────────────────────┘

    Separately, and NEVER touching the two flows above:

    ┌───────────────────────────┐        ┌────────────────────────────────────────┐
    │  operator's real .planning/│  walk  │  dsx/cli.py: cmd_stats (NEW)             │
    │  **/DECISIONS.jsonl trails │───────►│   -> aggregate InvocationHeader records   │
    │  (none exist in this repo  │  glob  │      by distinct frame_digest (D-14)      │
    │  today — see Pitfall 3)    │        │   -> read choice="paradigm=…" per frame   │
    └───────────────────────────┘        │      (dsx/frame/paradigm.py:616,626)      │
                                          │   -> negative-assert never sources        │
                                          │      examples/**/DECISIONS.jsonl or       │
                                          │      templates/DECISIONS.jsonl (D-13)     │
                                          │   -> print frequentist/bayesian/undeclared│
                                          │      split, always exit 0                 │
                                          └────────────────────────────────────────┘
```

### Recommended Project Structure

No new top-level packages. Concrete file-level changes:

```
examples/
├── known-bad/
│   ├── <existing 8 slugs>-{ANALYSIS-SPEC.yaml,POSTMORTEM.md}   # unchanged
│   ├── full-frame-cleaning-entrypoint.py                        # unchanged (only entrypoint case today)
│   ├── <new-slug>-ANALYSIS-SPEC.yaml / -POSTMORTEM.md           # REQ-P12-01 additions
│   ├── <new-or-existing-slug>-ATTRIBUTION.yaml                  # D-06 sidecar, miss/promotion cases only
│   └── DECISIONS.jsonl                                          # excluded from dsx stats (D-13); keeps growing — see Pitfall 4
├── <good-control location — planner's choice, e.g. good-corpus/>
│   └── <slug>-ANALYSIS-SPEC.yaml (≥10, D-04)                    # new; MUST get a golden entry too (Pitfall 2)
└── DECISIONS.jsonl                                              # pre-existing, unrelated to this phase, also excluded

tests/
├── test_known_bad_corpus.py     # extended: coverage predicates (D-01), sidecar sibling-integrity +
│                                  # falsifiability tests (D-07/D-08), stratified rate + friction (D-10/D-11),
│                                  # catalogue-invariant test (D-18)
├── test_causal_verb_golden.py    # MUST gain one _GOLDEN_SHIP_FINDINGS entry per new spec anywhere
│                                  # under examples/ (Pitfall 2) — both known-bad and good-control
└── test_cli_stats.py (or similar, planner's choice)  # cmd_stats: synthetic-trail guard (D-14),
                                   # negative-source assertion (D-13), always-exit-0 (D-12)

dsx/
└── cli.py    # + p_stats subparser (~ alongside p_explain, line ~848) + cmd_stats (~ alongside
              #   cmd_explain, line ~563) — no CHECKS/GATE_PROFILES change (D-12/D-18)

brief.md      # §6.5 table: 8 rows carried, 1 row relocated to a new "Removed / permanently out of
              # scope" subsection with pinned substrings intact (D-16)

.planning/REVERSALS.md   # + REV-002 record (D-16/D-17)
```

### Pattern 1: Live-gate measurement via fresh tempdir

**What:** Every reported number comes from actually invoking `dsx gate <point>` (via
`cli.main(...)`) against a spec, with `--phase-dir` pointed at a fresh
`tempfile.TemporaryDirectory()`, never a shared or reused directory.
**When to use:** Any place D-09 requires a live-computed number (catch rate, FPR, friction).
**Example:**
```python
# Source: tests/test_known_bad_corpus.py:555-616 (verified live, exact line match)
def _gate_findings(self, spec_path: Path, point: str) -> tuple[int, list[dict]]:
    with tempfile.TemporaryDirectory() as tmp:
        _seed_entrypoint(tmp, spec_path)
        if point in ("verify", "ship"):
            seed_plan_header(tmp, spec_path)
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(
                ["gate", point, "--spec", str(spec_path), "--phase-dir", tmp, "--json"]
            )
        raw = err.getvalue() or out.getvalue()
        report = json.loads(raw)
    return code, report["findings"]
```
This is the exact function D-09 names and D-11's "live-source proof" guard must reuse (call the
same function, not a parallel reimplementation).

### Pattern 2: Falsifiable attribution tags via live-verified absence/presence

**What:** A sidecar's `absent_code` claim is checked against a live `_gate_findings` union across
ALL gate points (not just the one point where it happens to be silent), and a `kind: caught`
sidecar's code must fire CRITICAL somewhere live.
**When to use:** D-08's anti-laundering guard.
**Example (sketch, no precedent to quote verbatim — new code):**
```python
def _verify_attribution_falsifiable(slug, sidecar, spec_path):
    absent_code = sidecar["absent_code"]
    kind = sidecar.get("kind", "miss")
    all_critical = set()
    for point in ("plan", "execute", "verify", "ship"):
        _, findings = self._gate_findings(spec_path, point)
        all_critical |= {f["code"] for f in findings if f["severity"] == "CRITICAL"}
    if kind == "miss":
        assert absent_code not in all_critical, (
            f"{slug!r} attribution claims {absent_code!r} is absent, but it fires CRITICAL"
        )
    elif kind == "caught":
        assert absent_code in all_critical, (
            f"{slug!r} attribution claims {absent_code!r} is caught, but it never fires CRITICAL"
        )
```
A code not present anywhere in `references/finding-codes.md`'s 256-entry catalogue AND not a
named §6.5 backlog code (D-07's validated union) fails schema validation before this check even
runs — that is what keeps a hallucinated code out.

### Pattern 3: Two-map dict-collision-avoidance for multi-point catches

**What:** When one fixture's target code fires at a gate point other than the "primary" one
recorded for the fixture's own-code recognition, a second dict key is added purely so
`_own_target_codes` (which flattens every key regardless of name) still recognizes it — the key
name itself carries no "only fires here" claim.
**When to use:** Any new corpus case whose catch spans multiple gate points with different check
families registered at each (common: `coherence`/`claims` fire at plan+verify+ship but not
execute; `code`/`ml` fire at execute+ship but not plan).
**Example:**
```python
# Source: tests/test_known_bad_corpus.py:201-204 (verified live, exact line match)
"full-frame-cleaning": {
    "execute": frozenset({"DSX-CODE-020", "DSX-CODE-021", "DSX-CODE-030"}),
    "ship": "DSX-ML-090",
},
```

### Pattern 4: `cmd_explain` as the reader-command template

**What:** A subcommand that never imports block-contract primitives (`Severity`, `GATE_THRESHOLDS`,
`Report`), returns 0 unconditionally, and degrades to an empty/informative result on any missing
or unreadable input rather than raising.
**When to use:** `cmd_stats` (D-12).
**Example:**
```python
# Source: dsx/cli.py:563-637 (verified live, exact line match) — the "always return 0" shape
def cmd_explain(args: argparse.Namespace) -> int:
    ...
    try:
        records = read_all(decisions_path(root))
        ...
        if args.json:
            print(json.dumps(selected, indent=2, sort_keys=True))
        ...
    except Exception as exc:
        print("dsx: no readable decision trail was found", file=sys.stdout)
        if args.verbose:
            print(f"dsx: {exc}", file=sys.stderr)
    return 0
```
**Divergence `cmd_stats` must introduce:** `cmd_explain` resolves exactly ONE root
(`args.phase_dir or str(path.parent)`) and reads exactly one `DECISIONS.jsonl`
(`decisions_path(root)`). `cmd_stats --paradigm` must aggregate across potentially many
`DECISIONS.jsonl` files under a search root (see Pitfall 3) — this is new logic with no direct
precedent in this codebase; model it as a directory walk (`Path(root).rglob("DECISIONS.jsonl")`)
feeding the same `read_all()` per file, filtered through the D-13 negative-source exclusion before
aggregation.

### Anti-Patterns to Avoid

- **Lifting a number from `_INCIDENTAL_GAP_CODES` or `_GOLDEN_SHIP_FINDINGS` into the catch-rate
  report:** D-09 explicitly forbids this — both are stamped-date snapshots that rot the moment a
  new check ships. Compute everything from a fresh `_gate_findings` call inside the same test run
  that reports the number.
- **Treating the recursive golden-file glob as scoped to "known-bad only":** it globs all of
  `examples/`. See Pitfall 2.
- **Running FPR measurement without seeding sibling artifacts:** produces phantom findings that
  are measurement noise, not real false positives. See Pitfall 1.
- **Citing "11.3 D-08" for the frame_digest-placement precedent:** the real precedent is 11.2
  D-08. See Pitfall 5.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Sidecar YAML parsing | A bespoke minimal YAML/JSON reader for `<slug>-ATTRIBUTION.yaml` | `dsx.loader.load(path)` | Already the bundled-parser entry point every spec-adjacent YAML file in this repo uses; keeps hermeticity (D-01) and gets the existing CRLF/`none`-literal handling for free (REQ-P6-01) |
| Live gate invocation for measurement | A new subprocess-spawning or module-reimport harness | `cli.main([...])` called in-process inside a fresh `tempfile.TemporaryDirectory()`, exactly as `_gate_findings` already does | Precedent proven correct across 1199 passing tests; a subprocess harness would be slower and would reintroduce the `DECISIONS.jsonl`-pollution problem this pattern already solves |
| Aggregating decision trails across many roots | A new decision-record database/index | Directory walk + repeated calls to the existing `dsx.decisions.read_all()` per file, aggregated in memory | `read_all()` already tolerates every malformed on-disk state (missing file, undecodable bytes, half-written crash tail) — reimplementing that tolerance elsewhere duplicates a bug surface that is already closed |
| Deduplicating repeated runs of the same analysis | A custom hash of the whole spec, or `spec_id`-based grouping | `frame_digest` (`dsx/decisions.py:241-250`), already computed and stored per invocation header | It is the existing, tested, deterministic per-frame content hash; `spec_id` is frequently `None` in real trails and is documented as the wrong primary key (D-14) |

**Key insight:** every piece of new machinery Phase 12 needs (falsifiable tag verification, live
stratified rate computation, cross-file trail aggregation) is a direct extension of a pattern that
already exists and is already exercised by 1199 passing tests. The risk in this phase is not
"we lack the building blocks" — it is "the existing building blocks have edge behaviors (tempdir
artifact-stripping, recursive golden-file globbing, empty `.planning/` history) that a plan
written from CONTEXT.md alone, without running the code, would not surface."

## Common Pitfalls

### Pitfall 1: Fresh-tempdir isolation strips sibling artifacts, manufacturing false positives

**What goes wrong:** A new D-04 good-control spec that declares `data[].assertions`,
`claims[].evidence`, `visuals[]`, or `narrative.path` will fire `DSX-DQ-001` (CRITICAL),
`DSX-CLM-031`, `DSX-FIG-001`, `DSX-NAR-010` (all HIGH) purely because the fresh
`tempfile.TemporaryDirectory()` the FPR harness runs in has none of the fixture's own committed
sibling files (`DATA-PROFILE.yaml`, figure artifacts, `NARRATIVE.md`, evidence files).
**Why it happens:** `_gate_findings`/`_ship_findings` isolate `--phase-dir` in a fresh tempdir
specifically to keep `DECISIONS.jsonl` writes out of `examples/` (the pollution problem D-13 also
guards against) — but the isolation has a side effect nobody papered over: it also isolates the
gate from every OTHER file the fixture references relative to its own directory.
**Confirmed live:** running `dsx gate ship --spec examples/good-ANALYSIS-SPEC.yaml` with a fresh
tempdir root (exactly the golden test's own method) currently fires exactly
`{DSX-CLM-031, DSX-DQ-001, DSX-FIG-001, DSX-NAR-010}` — matching the committed
`_GOLDEN_SHIP_FINDINGS` entry for that spec `[VERIFIED: live unittest run,
test_causal_verb_golden.py::test_every_fixture_ship_finding_set_equals_its_golden_baseline
passed]`. Running the SAME spec against its real, non-isolated directory (where
`good-DATA-PROFILE.yaml`, `good-FIGURE-MANIFEST.yaml`, `good-NARRATIVE.md` actually sit) makes
all four of those findings disappear entirely `[VERIFIED: manual live run against real root]` —
proving the four are artifacts of the isolation technique, not the analysis.
**How to avoid:** extend `_seed_entrypoint`'s pattern (`tests/test_known_bad_corpus.py:~505-541`)
to also copy a spec's `data[].profile_path`, `visuals[].artifact_path`, `narrative.path`, and
`claims[].evidence` targets into the tempdir before the gate run — OR explicitly document these
four codes (and any others discovered the same way) as harness-context noise excluded from the
FPR count, mirroring `_INCIDENTAL_GAP_CODES`'s existing allowlist-with-documented-reason pattern.
Either choice must be made deliberately and stated in the plan; silently inheriting the noise into
the FPR headline would make "there is a number" a dishonest number.
**Warning signs:** a new control-corpus spec blocks at ship with a finding whose `where` field
names a file path (evidence, figure, profile, narrative) rather than a statistical-validity
concept.

### Pitfall 2: A second, stricter golden-file test globs ALL of `examples/`, not just known-bad

**What goes wrong:** Committing a new `<slug>-ANALYSIS-SPEC.yaml` anywhere under `examples/`
(a new known-bad case, OR a new D-04 good-control spec) without a matching entry in
`tests/test_causal_verb_golden.py::_GOLDEN_SHIP_FINDINGS` fails
`test_golden_keys_match_the_examples_tree_on_disk` immediately, in a file most of the
CONTEXT.md's canonical references never mention.
**Why it happens:** `SPEC_GLOB = "**/*-ANALYSIS-SPEC.yaml"` against `EXAMPLES_DIR = ROOT /
"examples"` (`tests/test_causal_verb_golden.py:58-59`) is recursive over the whole `examples/`
tree, independent of `tests/test_known_bad_corpus.py`'s narrower `CORPUS_DIR =
examples/known-bad` scoping.
**How to avoid:** every plan task that adds a corpus or control-corpus spec must, in the SAME
commit, add its measured CRITICAL/HIGH finding set to `_GOLDEN_SHIP_FINDINGS`
(`tests/test_causal_verb_golden.py:82-142`) — measured via the exact same fresh-tempdir
`_ship_findings()` helper the test itself uses, not guessed.
**Warning signs:** `test_golden_keys_match_the_examples_tree_on_disk` failing with a
`golden ^ disk` diff naming the new spec path.

### Pitfall 3: `dsx stats --paradigm`'s locked source (`.planning/`) has no real data yet, and no aggregation precedent exists

**What goes wrong:** Assuming `cmd_stats` can reuse `cmd_explain`'s `decisions_path(root)` +
`read_all(path)` pattern verbatim. That pattern resolves exactly one root and reads exactly one
file. `dsx stats --paradigm` needs to aggregate across potentially many `DECISIONS.jsonl` files
scattered under a directory tree — there is no existing multi-file-aggregation code to copy.
**Confirmed live:** `find . -name DECISIONS.jsonl` in this repo returns only
`examples/DECISIONS.jsonl`, `examples/known-bad/DECISIONS.jsonl`, `templates/DECISIONS.jsonl`,
and a stray worktree copy — **none under `.planning/`** `[VERIFIED: live filesystem search]`.
Running `dsx stats --paradigm` for real in this repo today would (correctly) report zero operator
history.
**How to avoid:** design `cmd_stats` as a directory walk (e.g. `Path(root).rglob
("DECISIONS.jsonl")`) from a configurable root (default `.planning/` or cwd — planner's
discretion, per CONTEXT.md's report-layout discretion clause), feeding each discovered file
through the existing `read_all()`. Handle the zero-history case explicitly (report "no operator
history yet", never a division by zero on an empty denominator). Write the D-14 synthetic-trail
test as the PRIMARY test of the aggregation logic, since it is the only test that can exercise a
populated case in this repo's current state.
**Warning signs:** a plan task that assumes `cmd_stats` is "just `cmd_explain` with a different
flag" — it structurally cannot be, because the root-resolution model differs.

### Pitfall 4: The two existing `DECISIONS.jsonl` fixture-floor files keep growing from manual dev-time runs

**What goes wrong:** `examples/known-bad/DECISIONS.jsonl` is 13,129 lines / 1,157 invocation
records / 15 distinct `frame_digest` / 2 `spec_id` today `[VERIFIED: live dsx.decisions.read_all
count]` — closely matching but not identical to CONTEXT.md's cited "~1,151 invocation records...
15 distinct frame_digest / 2 spec_id, ~45.8% raw-Bayesian" (live raw-Bayesian share of paradigm
decision records measured at 45.9% — 1,062 of 2,314 — the ~0.1pp difference is consistent with a
handful of additional manual `dsx gate` invocations against these fixtures since the CONTEXT.md
was drafted, not a real inconsistency). The top-level `examples/DECISIONS.jsonl` is far larger:
75,379 lines. Neither file is test-managed; both grow whenever a developer runs `dsx gate ... --
spec examples/...` directly from a shell (outside the test suite's tempdir isolation) during
manual plan work.
**Why it happens:** nothing in the repo currently prevents or bounds this growth; D-13's
hard-exclude is a correctness workaround for the pollution, not a fix for the growth itself.
**How to avoid:** not a Phase 12 blocker — D-13's exclusion is sufficient for correctness — but
worth an explicit open-question note (see Open Questions) since these files will keep growing and
nothing currently caps or gitignores them.
**Additional finding-by-computation:** deduplicating `examples/known-bad/DECISIONS.jsonl`'s own
15 distinct `frame_digest`s by paradigm gives 12 frequentist / 3 Bayesian = **20% Bayesian** even
after digest-dedup `[VERIFIED: live computation]` — still above the §6.5 item-4 15% threshold,
though far less dramatically than the raw 45.8-45.9%. This number is IRRELEVANT to the real
measurement (D-13 excludes this file entirely; `dsx stats --paradigm` must never read it) but is
useful evidence that dedup alone would not have been sufficient to protect the instrument — full
exclusion (D-13) is the right call, not merely partial mitigation via D-14's dedup.

### Pitfall 5: CONTEXT.md's "11.3 D-08" citation names the wrong phase for the frame_digest-placement precedent

**What goes wrong:** A planner or implementer who opens `11.3-CONTEXT.md` looking for "the
precedent for keeping fields outside `validity_frame`/`inference`" (as `12-CONTEXT.md`'s D-06 and
canonical_refs literally direct) finds a decision that does the OPPOSITE: 11.3's own D-08
deliberately places `validity_frame.exclusions` INSIDE `validity_frame` specifically so it IS
digest-covered (`.planning/phases/11.3-reporting-completeness/11.3-CONTEXT.md:200-203`,
`[VERIFIED: live file read]`).
**Why it happens:** the correct precedent — `spec_id` living outside `validity_frame`/`inference`
so it never enters `frame_digest`'s inputs — is **11.2 D-08**
(`.planning/phases/11.2-prescriptive-claim-layer/11.2-CONTEXT.md:194-196`, `[VERIFIED: live file
read]`), and is also documented directly in the code itself
(`dsx/decisions.py:99-121`'s `InvocationHeader.spec_id` docstring, which explicitly says "(D-08)"
in that exact context). Each phase's CONTEXT.md numbers its own decisions independently starting
from D-01, so "D-08" is not a globally unique identifier — 12-CONTEXT.md's citation collided with
the wrong phase.
**How to avoid:** when writing the ATTRIBUTION.yaml sidecar's design rationale (comments,
docstrings, or a future architecture note), cite **11.2 D-08** (`spec_id` placement) as the
precedent, not 11.3 D-08.
**Warning signs:** none at test time — this is a documentation-accuracy issue only, not a
functional one, since the sidecar's actual mechanism (living entirely outside the spec file) is
correct regardless of which precedent's name is attached to it.

## Code Examples

### Reading the paradigm choice from a decision trail

```python
# Source: dsx/frame/paradigm.py:614-626 (verified live, exact line match)
other_paradigms = [p for p in PARADIGMS if p != paradigm]
if paradigm:
    choice = f"paradigm={paradigm}"
    ...
else:
    choice = "paradigm=undeclared"
    ...
report.context.setdefault("decisions", []).append(
    DecisionRecord(
        id="", invocation_id="", layer="deterministic", choice=choice, ...
    )
)
```
Note the three-way vocabulary: `frequentist`, `bayesian`, or `undeclared` (an out-of-vocabulary or
absent `inference.paradigm` folds to `undeclared`, per the corrected reader logic noted in
`STATE.md`'s Phase 7 CR-01 fix). `dsx stats --paradigm` must report all three buckets, not force a
binary split.

### Computing `frame_digest`

```python
# Source: dsx/decisions.py:241-250 (verified live, exact line match)
def frame_digest(spec: "dict[str, Any]") -> str:
    payload = json.dumps(
        {"validity_frame": spec.get("validity_frame"), "inference": spec.get("inference")},
        sort_keys=True,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
```
Deterministic, key-order-invariant, unaffected by edits outside these two blocks. This is the
D-14 dedup key.

### Reading every invocation header + its decision records for a given trail file

```python
# dsx.decisions.read_all — general shape (dsx/decisions.py:182-215, verified live)
records = read_all(path)  # tolerant: [] on missing/unreadable, skips unparseable lines
invocations = [r for r in records if r.get("record_type") == "invocation"]
decisions = [r for r in records if r.get("record_type") == "decision"]
```
For `cmd_stats`, call this once per discovered `DECISIONS.jsonl` under the search root, and
aggregate `invocations` across files before deduplicating by `frame_digest`.

## State of the Art

Not applicable in the usual sense (no external library evolution to track — this is entirely
in-repo measurement/reporting work). The one relevant "state of the art" shift is internal:
Phase 10's `prereg` family made `DECISIONS.jsonl` a **gate input** (content-lock reconciliation),
not merely an output — which is why every fresh-tempdir gate call in this codebase now must seed
a plan-time header before calling verify/ship (`seed_plan_header`), a pattern that postdates the
original corpus harness design and that any new Phase 12 harness code must inherit correctly.

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|---------------|--------|
| `DECISIONS.jsonl` as a write-only side channel | `DECISIONS.jsonl` as a gate INPUT at verify/ship (`prereg`'s content-lock) | Phase 10 | Any new tempdir-isolated gate call at verify/ship must call `seed_plan_header(tmp, spec_path)` first, or it hits exit 2 rather than a real finding set |

**Deprecated/outdated:** none specific to this phase.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The good-control corpus location is a new directory under `examples/` (planner's discretion per CONTEXT.md) rather than flat files alongside `examples/good-ANALYSIS-SPEC.yaml` | Recommended Project Structure | Low — either choice is picked up identically by the recursive golden-file glob (Pitfall 2); only affects naming/organization, not correctness |
| A2 | `cmd_stats`'s default search root should be `.planning/` (matching D-13's literal wording) rather than an operator-supplied `--root` flag with `.planning/` as one convenient default | Pitfall 3 / Architecture diagram | Medium — if the real intended source is "wherever the operator's real DECISIONS.jsonl trails live" (which may not literally be named `.planning/` in every operator's environment), a hardcoded `.planning/`-only root could under-report. Recommend the planner treat the root as configurable with `.planning/` as the default, and confirm this interpretation before implementation — this is the one place D-13's locked wording ("Source = real operator `.planning/` decision trails ONLY") could bear a narrower or broader reading than intended |
| A3 | The `<good-control>` corpus target size of "≈≥10" clean specs (CONTEXT.md's own Claude's Discretion framing) is sufficient resolution for an honest FPR rate | Standard Stack / D-04 | Low-Medium — this number is explicitly named a planning choice in CONTEXT.md itself, not asserted as verified here; the actual sizing decision should weigh the note in Pitfall 1 (each spec needs artifact-seeding or noise-documentation work, so size has an implementation-cost tradeoff, not just a statistical-resolution one) |

**If this table is empty:** N/A — see entries above. All anchor citations, code line ranges, test
pass/fail status, corpus counts, and pollution percentages elsewhere in this document were
directly verified against the live tree and tagged `[VERIFIED: ...]` at point of use, not
`[ASSUMED]`.

## Open Questions

1. **Should `examples/known-bad/DECISIONS.jsonl` and `examples/DECISIONS.jsonl`'s unbounded
   growth (13,129 and 75,379 lines respectively today) be addressed in Phase 12, or left as a
   standing known issue?**
   - What we know: D-13's hard-exclude fully protects `dsx stats --paradigm`'s correctness
     regardless of how large these files grow. Nothing currently caps, rotates, or gitignores
     them.
   - What's unclear: whether this is intended to be addressed as repo hygiene at some point, and
     if so whether Phase 12 (which is explicitly the terminal measurement phase) is the right
     place, given D-18 forbids minting any new detection code and this isn't a detection concern
     anyway.
   - Recommendation: out of scope for Phase 12's requirements (none of REQ-P12-01..05 touch this),
     but worth a one-line note in the phase's ship notes so it isn't rediscovered as a surprise
     later.

2. **Does `cmd_stats`'s search root need to be configurable, or is a hardcoded `.planning/`
   sufficient?** (See Assumption A2.) This is the one place a locked D-13 decision could bear two
   readings, and it materially affects whether `dsx stats --paradigm` is useful outside a
   `.planning/`-organized project. Recommend surfacing this explicitly at plan time rather than
   silently picking one reading.

3. **What is the exact target list of new REQ-P12-01 corpus cases (which retracted papers, which
   documented p-hacking cases, which of the operator's own prior work)?** D-02 (source-before-
   count) explicitly forbids pre-deciding this to hit a count, and the Deferred Ideas section
   pre-registers a D-05 primary-source citation obligation for each new case at ship. This
   research does not attempt to source candidate cases — that sourcing work is explicitly the
   planner/executor's task, gated by the coverage predicates (≥1 retracted-paper+postmortem, ≥1
   p-hacking, ≥1 operator-known-answer), not a fixed list this research should pre-select.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python | Entire test/harness runtime | ✓ | 3.12.10 `[VERIFIED: python --version]` | — |
| PyYAML | Cross-check tests only (not required by any Phase 12 task) | ✓ | importable `[VERIFIED: python -c "import yaml"]` | Not needed — `dsx.loader.load` is the required path (D-01) |
| Network access | None required | n/a | — | Gate path and this phase's harness are fully offline by design (D-01) |

**Missing dependencies with no fallback:** none.
**Missing dependencies with fallback:** none — nothing is missing.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | `unittest` (stdlib), invoked via `python -m unittest discover -s tests -p "test_*.py"` |
| Config file | none — no pytest.ini/config; convention-based discovery |
| Quick run command | `python -m unittest tests.test_known_bad_corpus -v` (2.5s, 30 tests today) |
| Full suite command | `python -m unittest discover -s tests -p "test_*.py"` (43s, 1199 tests today `[VERIFIED: live run, all pass]`) |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| REQ-P12-01 | New corpus cases pass structural coverage predicates (≥1 retracted-paper case, ≥1 p-hacking case, ≥1 operator-known-answer case), each a spec+postmortem pair | unit (coverage predicate) | `python -m unittest tests.test_known_bad_corpus.TestKnownBadCorpus.test_corpus_includes_full_coverage_classes -v` (new predicate, modelled on existing `test_corpus_includes_an_interference_case_and_a_bayesian_continuous_case`, `:634`) | ❌ Wave 0 — new predicate function |
| REQ-P12-02 | Sidecar sibling-integrity (every sidecar names a real slug, a code in the validated union, a real §6.5 item id) | unit (structural) | `python -m unittest tests.test_known_bad_corpus.TestKnownBadCorpus.test_attribution_sidecars_reference_valid_codes_and_items -v` (new) | ❌ Wave 0 |
| REQ-P12-02 | Sidecar falsifiability (D-08): miss tags fire nowhere live, caught tags fire CRITICAL live | unit (live gate, fresh tempdir) | `python -m unittest tests.test_known_bad_corpus.TestKnownBadCorpus.test_attribution_tags_are_falsifiable_against_live_gate -v` (new) | ❌ Wave 0 |
| REQ-P12-02 | Friction column: synthetic arithmetic proof (filesystem-independent) | unit (pure function) | `python -m unittest tests.test_known_bad_corpus.TestFrictionArithmetic -v` (new, mirrors `TestClassifyTargetDefectHelper`'s synthetic-map pattern already in the file) | ❌ Wave 0 |
| REQ-P12-02 | Friction column: live-source proof (consumes same `_gate_findings` set as golden test) | unit (live gate, cross-referenced against `_GOLDEN_SHIP_FINDINGS`) | `python -m unittest tests.test_known_bad_corpus.TestKnownBadCorpus.test_friction_uses_the_same_live_findings_as_golden -v` (new) | ❌ Wave 0 |
| REQ-P12-03 | Stratified catch rate (PRESENT/ABSENT partitions, each own denominator) + FPR over the new good-control corpus | unit (live gate, stratified aggregation) | `python -m unittest tests.test_known_bad_corpus.TestKnownBadCorpus.test_stratified_catch_rate_and_fpr_report -v` (new) | ❌ Wave 0 |
| REQ-P12-03 | Good-control corpus golden-file coverage (Pitfall 2) | unit (existing mechanism, new data) | `python -m unittest tests.test_causal_verb_golden -v` (existing test, extended `_GOLDEN_SHIP_FINDINGS` dict) | ✓ mechanism exists, ❌ new entries needed each time a spec is added |
| REQ-P12-04 | `dsx stats --paradigm` always exits 0, never in `GATE_PROFILES` | unit (CLI contract) | new test module, e.g. `python -m unittest tests.test_cli_stats.TestCmdStats.test_always_exits_zero -v` | ❌ Wave 0 |
| REQ-P12-04 | Negative-source assertion — never reads `examples/**/DECISIONS.jsonl` or `templates/DECISIONS.jsonl` | unit (negative assertion, likely via a poisoned-fixture directory containing a huge fake known-bad-shaped trail and asserting it's excluded) | `python -m unittest tests.test_cli_stats.TestCmdStats.test_never_sources_the_known_bad_floor -v` | ❌ Wave 0 |
| REQ-P12-04 | Synthetic-trail guard (D-14): N distinct frequentist frames repeated many times + 1 distinct Bayesian frame ⇒ reported share is over distinct frames | unit (synthetic fixture directory, no real `.planning/` dependency) | `python -m unittest tests.test_cli_stats.TestCmdStats.test_dedup_is_by_distinct_frame_digest -v` | ❌ Wave 0 |
| REQ-P12-05 | Every §6.5 item's disposition (carry 8, remove 1) reflected in `brief.md`; pinned Deng & Hu substrings preserved | unit (existing pin test, verify still passes after the edit) | `python -m unittest tests.test_known_bad_corpus.TestKnownBadCorpus.test_brief_states_the_ratio_metric_dilution_entry_condition_as_a_falsifiable_blocker -v` (existing, at `:1043-1069` — this test does NOT require the row to stay in its original table location, only that the three substrings remain present anywhere in `brief.md`) | ✓ exists, must keep passing |
| REQ-P12-05 | REV-002 filed, survives SELF-001 (New evidence field is not a restatement) | manual/human review (SELF-001 has no mechanical enforcement — `.planning/REVERSALS.md:49-56` confirms this is a convention, not a gate check) | N/A — human review at ship/UAT, per the pre-registered note in Deferred Ideas | N/A |
| REQ-P12-01/02/03 | Catalogue stays 256 after Phase 12 (D-18) | unit (generated-artifact assertion) | `python -m unittest tests.test_known_bad_corpus.TestKnownBadCorpus.test_finding_catalogue_stays_at_256_codes -v` (new, reads `references/finding-codes.md`'s `**Total: N codes.**` line, or invokes `scripts/gen-finding-catalogue.py`'s row-collection function directly) | ❌ Wave 0 |

### Sampling Rate

- **Per task commit:** `python -m unittest tests.test_known_bad_corpus -v` and (whenever a new
  `examples/**/*-ANALYSIS-SPEC.yaml` is touched) `python -m unittest tests.test_causal_verb_golden
  -v` — both run in under 3 seconds each.
- **Per wave merge:** `python -m unittest discover -s tests -p "test_*.py"` (full suite, currently
  1199 tests / ~43s).
- **Phase gate:** Full suite green before `/gsd-verify-work`; additionally, `scripts/gen-finding-
  catalogue.py --check` must pass (asserts the committed `references/finding-codes.md` matches
  what the generator would produce, and indirectly enforces D-18's 256 count).

### Wave 0 Gaps

- [ ] New coverage-predicate test(s) in `tests/test_known_bad_corpus.py` — covers REQ-P12-01 (D-01)
- [ ] New sidecar schema-validation test(s) — covers REQ-P12-02 (D-07)
- [ ] New sidecar falsifiability test(s) against live `_gate_findings` — covers REQ-P12-02 (D-08)
- [ ] New friction synthetic-arithmetic + live-source proof tests — covers REQ-P12-02 (D-11)
- [ ] New stratified catch-rate/FPR aggregation test(s), including the good-control corpus and its
      sibling-artifact-seeding or noise-exclusion decision (Pitfall 1) — covers REQ-P12-03 (D-04/D-10)
- [ ] Extended `_GOLDEN_SHIP_FINDINGS` entries for every new spec under `examples/` — covers REQ-P12-01/REQ-P12-03 (Pitfall 2)
- [ ] New `tests/test_cli_stats.py` (or equivalent) — covers REQ-P12-04 (D-12/D-13/D-14), including
      the always-exit-0 contract, the negative-source assertion, and the synthetic-trail dedup guard
- [ ] New catalogue-invariant test (256 codes) — covers D-18
- [ ] Existing pin test `test_brief_states_the_ratio_metric_dilution_entry_condition_as_a_falsifiable_blocker`
      must be re-run (not modified) after the §6.5 edit — covers REQ-P12-05 (D-16)

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | No auth surface — this is a local CLI/test-harness phase |
| V3 Session Management | no | N/A |
| V4 Access Control | no | N/A |
| V5 Input Validation | yes | `absent_code` and `promotes_backlog_item` in `<slug>-ATTRIBUTION.yaml` must be validated against the closed union of 256 catalogue codes + named §6.5 backlog codes and real §6.5 item ids before use (D-07's sibling-integrity test) — an unvalidated sidecar value is an injection surface into the catch-rate report's attributed-code column |
| V6 Cryptography | no | `frame_digest` (SHA-256) is change-detection, not a security control (explicitly documented, `dsx/decisions.py:241-244`'s docstring) — no cryptographic guarantee is claimed or required here |

### Known Threat Patterns for this phase's stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| A hand-authored `<slug>-ATTRIBUTION.yaml` naming a hallucinated/misspelled finding code, silently inflating a §6.5 promotion count | Tampering (data integrity, not adversarial) | D-07's validated-union check + D-08's live-falsifiability check — a code that doesn't exist in the catalogue or backlog fails schema validation before it can be "verified" at all |
| A sidecar's `absent_code` naming a code that DOES fire live, laundering a catch as a miss (or vice versa) to game a §6.5 promotion count | Repudiation / Tampering | D-08's mandatory live cross-check against `_gate_findings` union across all four gate points — this is the exact mechanism this pattern requires |
| `dsx stats --paradigm` accidentally ingesting the known-bad fixture floor (or `examples/DECISIONS.jsonl`, or `templates/DECISIONS.jsonl`) and silently inflating the measured Bayesian share past the 15% threshold, causing an unwarranted auto-promotion of §6.5 item 4 | Tampering (measurement integrity) | D-13's hard-exclude + mandatory negative-source assertion test; this is the load-bearing security-adjacent control of the whole phase — see Summary point 3 and Pitfall 3 for why the exclusion boundary needs to be drawn carefully (root-scoping, not a single hardcoded path literal) |
| Friction "incidental→own" relabeling — quietly moving a code from friction into `_TARGET_DEFECT_CODES` to shrink the reported over-blocking rate without actually fixing the over-blocking | Tampering / Repudiation | D-11(c)'s guard: every `_TARGET_DEFECT_CODES` entry must be positively verified firing CRITICAL AND named in the fixture's postmortem/attribution — closing exactly this relabel path |

## Sources

### Primary (HIGH confidence)
- `tests/test_known_bad_corpus.py` (1236 lines, read in full across multiple passes) — every cited
  anchor verified against the live file
- `tests/test_causal_verb_golden.py` (317 lines, read in full) — golden-file mechanism and its
  recursive-glob scope verified live
- `dsx/cli.py` (943 lines, relevant ranges read) — `CHECKS`, `GATE_PROFILES`, `cmd_explain`,
  `_write_decision_trail`, subparser registration all verified live
- `dsx/frame/paradigm.py` (relevant range read) — `choice="paradigm=…"` verified live at both
  cited lines
- `dsx/decisions.py` (296 lines, read in full) — `frame_digest`, `read_all`, `decisions_path`,
  `InvocationHeader`/`spec_id` all verified live
- `references/finding-codes.md` (line 16 read) — "Total: 256 codes." verified live
- `.planning/REVERSALS.md` (read in full) — REV-001 precedent and SELF-001 convention verified
  live; confirmed REV-002 is the next unused id
- `brief.md` §6.5 (lines 354-434 read) — the 9-item table, REV-001 record, D-01/D-02 determinism
  doctrine, and §6.6 open items all verified live
- `.planning/phases/11.2-prescriptive-claim-layer/11.2-CONTEXT.md` and
  `.planning/phases/11.3-reporting-completeness/11.3-CONTEXT.md` (relevant D-08 sections read) —
  used to correct the CONTEXT.md's "11.3 D-08" citation to the actual 11.2 D-08 precedent
- Live `unittest` runs: `tests.test_known_bad_corpus` (30/30 pass), `tests.test_causal_verb_golden`
  (6/6 pass), full suite discovery (1199/1199 pass)
- Live Python execution against `dsx.decisions.read_all()` over
  `examples/known-bad/DECISIONS.jsonl` — corpus pollution figures measured directly, not quoted
  from CONTEXT.md
- Live Python execution comparing `dsx gate ship` findings for `examples/good-ANALYSIS-SPEC.yaml`
  under fresh-tempdir isolation vs. its real directory root — the source of Pitfall 1

### Secondary (MEDIUM confidence)
- None used beyond the primary in-repo sources above — this phase's research question is entirely
  answerable from the codebase itself; no external documentation lookup was needed.

### Tertiary (LOW confidence)
- None.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new dependencies, D-01 doctrine unambiguous and unchanged
- Architecture: HIGH — every mechanism recommended is a direct, verified extension of existing,
  currently-passing code
- Pitfalls: HIGH — all five pitfalls were confirmed by direct code reading and/or live execution,
  not inferred from CONTEXT.md's prose alone

**Research date:** 2026-08-27
**Valid until:** Effectively unbounded for the architectural/pitfall findings (they are properties
of code that changes only when Phase 12 itself changes it); the corpus pollution figures
(invocation counts, frame_digest counts, raw-Bayesian %) will drift further every time a developer
manually runs `dsx gate` against `examples/known-bad/` outside the test suite — treat those
specific numbers as a snapshot, not a constant, and re-measure at plan/execute time if precision
matters for a specific test assertion.
