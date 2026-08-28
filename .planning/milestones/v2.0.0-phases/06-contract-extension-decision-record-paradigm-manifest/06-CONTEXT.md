# Phase 6: Contract extension, decision record, paradigm manifest - Context

**Gathered:** 2026-08-07
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 6 delivers the **v2.0.0 contract surface** — the parseable, readable foundation every
other v2.0.0 phase imports. It ships: the `dsx/loader.py` `_NULL` fix; the `validity_frame:`
and `inference:` schema with `question_type`-gated requiredness; the new closed vocabularies
and their `dsx vocab` exposure; a decision-record module and append-only emitter; `dsx explain`;
the `DSX-PAR-001` INFO paradigm manifest; the `dsx/frame/` package with its D-03a AST boundary
test; mechanical D-05 enforcement in `scripts/gen-finding-catalogue.py`; extended canonical
fixtures per D-08; the known-bad seed corpus with post-mortems; `.planning/REVERSALS.md`;
README updates; version 2.0.0 and a regenerated catalogue.

**No check-family logic ships here beyond `DSX-PAR-001`.** `DSX-VAL-*`, `DSX-INT-*`,
`DSX-PRE-*` and `DSX-ADM-*` are Phases 7–11. `references/families.yaml` and
`dsx/frame/admissibility.py` are **not created** in this phase (brief §6.6 item 2).

Requirements: REQ-P6-01 … REQ-P6-16 (16 requirements, see `.planning/REQUIREMENTS.md`).

</domain>

<decisions>
## Implementation Decisions

### Locked upstream — do NOT re-litigate

- `brief.md` §4 (D-01…D-14) and §5 (contract shape) are binding inputs (`PROJECT.md` §Context).
- `PROJECT.md` Key Decisions M-01…M-09 are binding. In particular: `DSX-PAR-010` is a distinct
  code with `DSX-EXP-060` untouched (M-01); no `inference.stopping_rule` field (M-02);
  `validity_frame` sub-block requiredness gated by `question_type` (M-06); `suppressions[]` is
  the pre-v2.0.0 grandfather path (M-07); `dependence.method_family_required` reuses
  `VARIANCE_ADJUSTMENTS` (M-09).
- `SELF-001` stays a convention for v2.0.0; `REVERSALS.md` template is seeded here (M-05).
- brief §6.6 items 1 and 3 are already resolved by M-01 and M-05 respectively.
- `DSX-PAR-011` asserts the prior-averaged Ville bound `1/(K+1)`, **not** the point-null / LIL
  formulation (brief §6.5 fixture note; SUMMARY.md).

### Vocabulary: `PEEKING_POLICIES` and the new frame vocabularies

- **D-01: The `PEEKING_POLICIES` member ships in Phase 6, as REQ-P6-05 states.** This overrides
  `research/ARCHITECTURE.md` §4.3's recommendation to defer it to Phase 9. §4.3's premise —
  "a vocabulary member with no consumer should not exist for two milestones" — is false:
  Phase 6 must commit a Bayesian continuous-monitoring known-bad fixture (REQ-P6-13) that
  passes `dsx validate` structurally (ROADMAP SC 5), and that fixture must declare uncontrolled
  continuous monitoring. Without the member it trips `DSX-SPEC-042` at HIGH
  (`dsx/spec.py:448-457`). REQ-P6-05, ROADMAP SC 1 and the Phase 9 depends-on line
  (`ROADMAP.md:238`) all stand unedited.
- **D-02: The member is named `uncontrolled_continuous`.** The deciding constraint is who reads
  the string: an operator choosing a value under time pressure from a `dsx vocab` dump, not
  someone holding brief §5.3 in their head. `optional_continuous` (brief §5.2's wording) fails
  that — "optional stopping" names the *design*, and reads as a synonym of `always_valid` to
  anyone who half-knows the literature, which is precisely the misconception `DSX-PAR-011`
  exists to catch. `continuous_uncorrected` describes the analyst's omission rather than a
  property of the procedure, reads oddly beside `sequential_obf`/`sequential_pocock` which name
  methods, and "uncorrected" misleadingly hints at multiplicity correction (a different DSX
  family). `uncontrolled_continuous` names the property that actually differs — error rate not
  controlled — and sits correctly against `always_valid`. **Verified: no `uncontrolled` prefix
  collision anywhere in `dsx/`, `tests/`, `examples/`, `references/` or `templates/`.**
- **D-03: `dsx vocab` emits `peeking_policies` as a name→description object**, not a flat list.
  `describe_vocabulary()` currently dumps `sorted(PEEKING_POLICIES)` (`dsx/spec.py:552`), which
  discards the descriptions that carry the `always_valid` vs `uncontrolled_continuous`
  distinction. Set-backed vocabularies stay flat lists. `always_valid`'s description is tightened
  to name what controls the error rate. v2.0.0 is the breaking release, so this is the window;
  a parallel `"descriptions"` key was rejected as the split-vocabulary pattern M-02 and M-09
  already argued against.
- **D-04: Every new frame vocabulary is a name→description dict. No exceptions, no split rule.**
  (An initial "dicts where subtle, sets elsewhere" answer was reversed in-discussion once it
  became clear the split would need its own stable criterion to survive Phases 7–12.) brief §5.1
  already carries much of the prose as inline comments, so this is largely transcription.
  Membership checks are unchanged — `x in DICT` tests keys.
- **D-05: `describe_vocabulary()` is built from an explicit vocabulary-name registry, with a test asserting coverage.** Removes the two-places-to-update problem (REQ-P6-06, PITFALLS:655)
  without needing an introspection deny-list for the existing non-vocabulary module constants
  (`SPEC_VERSION`, `CAUSAL_VERBS`, `REQUIRED_TOP_LEVEL`, `IMBALANCE_UNSAFE_METRICS`).

### Fixtures for the Phase 9 pair

- **D-06: Both halves of the Phase 9 atomic pair get a known-bad fixture in Phase 6.** A
  frequentist uncontrolled-continuous fixture ships alongside the REQ-P6-13-mandated Bayesian
  continuous-monitoring fixture. This is one fixture more than REQ-P6-13 requires, and it
  directly serves D-12: the pair cannot ship half-delivered, and having both targets committed
  early makes a half-shipped Phase 9 harder to fudge.
- **D-07: `examples/bad-ANALYSIS-SPEC.yaml` is NOT extended on the peeking axis.** A declared
  defect sitting in the canonical fixture with no finding against it for three phases is
  indistinguishable from a missed one.
- **D-08: A parametrised disjointness test proves M-01 mechanically.** One test over all five
  `PEEKING_POLICIES` members asserting `DSX-EXP-060` fires for `""` and `fixed_horizon` and
  nothing else. This pins the *property*, so it also fails if someone later widens
  `_check_peeking`. Phase 9 inherits it as the guard that `DSX-PAR-010` is not double-firing.
  **No `DSX-EXP-060` code change is needed** — `dsx/checks/design.py:451` already gates on
  `policy in ("", "fixed_horizon")`, so a new member falls straight through.

### Structural validation: location, codes, severity

- **D-09: `_validate_validity_frame_shape()` and `_validate_inference_shape()` live in `dsx/spec.py` under `DSX-SPEC-08x`**, mirroring `_validate_design_shape` (`dsx/spec.py:422`)
  exactly — ARCHITECTURE §4.3's recommendation. `spec` is already in all four gate profiles
  (`dsx/cli.py:72-84`), so **no `GATE_PROFILES` change ships in Phase 6**. `DSX-SPEC-0xx` is
  free from `080` (used through `073` in `dsx/suppressions.py`). This keeps `dsx/frame/` holding
  only `paradigm.py`, the cleanest possible D-03a starting point.
- **D-10: A missing required `validity_frame` sub-block is CRITICAL — uniformly.** Severity *is*
  the gate point here: thresholds are CRITICAL at plan/execute and HIGH at verify/ship
  (`dsx/cli.py:87-92`), so CRITICAL blocks from plan onward. This serves the project's core
  value literally — a frame first demanded at verify is a frame filled after the data was
  touched. M-07's `suppressions[]` path, with its ADR/SPEC authority requirement, makes the
  migration deliberate and attributable rather than silent.
  - **ACTION for the planner:** `PROJECT.md:79-80`'s version rationale currently reads
    "`validity_frame:` becomes required at verify/ship" and must be amended to "required from
    plan". This is **not** a D-14 reversal — the version rationale sits outside both the brief
    §4 D-table and the PROJECT.md M-table — but it cannot be left contradicting the gate.
- **D-11: Finding granularity is aggregate-when-absent.** Block entirely absent → **one**
  finding itemising every missing required sub-block in `detail`. Block present but a required
  sub-block missing → **one finding per sub-block**. A legacy spec is therefore grandfathered
  with a single `suppressions[]` entry carrying one ADR authority rather than six; once
  migration starts, findings get specific. Grounded in the empirical result that *actionability*,
  not warning count, predicts whether a warning gets fixed.
- **D-12: `templates/ANALYSIS-SPEC.yaml` scaffolds both blocks in full** — every sub-block
  present, with brief §5.1/§5.2 guidance comments and placeholder values, so `dsx init` output
  keeps passing `dsx validate` and `dsx gate plan` structurally. Necessary because the template
  declares `question_type: descriptive` (`templates/ANALYSIS-SPEC.yaml:25`) and
  `estimand`/`units`/`measurement` are required for *every* question type — at CRITICAL, an
  unchanged template would ship a spec that fails its own gate. Placeholders will still fail
  Phase 7 falsifiability and Phase 8 mitigation checks; that is correct — Phase 6 checks shape,
  later phases check content.

### Decision record

- **D-13: Only the new surface emits records in Phase 6** — `DSX-PAR-001` plus the new
  `DSX-SPEC-08x` structural adjudications. **The 15 existing check modules are untouched.**
  This reads STATE.md's standing deliverable ("emit decision records at each family's key
  judgment points") as *each family emitting when it ships*, which is how Phases 7–12 inherit
  the pattern. It also keeps the Phase 6 diff off the v1.5.0 surface, so D-08's two exit-code
  tests are provably unaffected.
- **D-14: One `DECISIONS.jsonl` beside the spec**, resolved the way `find_spec()` already
  resolves the spec (`phase_dir` → cwd → `.planning/`), appended across every invocation. The
  trail accumulates across plan→execute→verify→ship, which is exactly the trail D-04 wants
  rendered. A fixed `.planning/` location was rejected because dsx is installable outside a GSD
  repo — `find_spec()` already falls back to cwd for that reason.
- **D-15: The per-invocation identifier must NOT be called `run_id`.** `run_id` is already taken
  for an operator-declared *readout* id in `visuals[]` and `FIGURE-MANIFEST.yaml`, enforced by
  `DSX-SMELL-013` (`dsx/checks/smells.py:156`). Reusing the name for a gate-invocation id would
  collide two unrelated concepts in one contract.
- **D-16: An invocation-header record is emitted once per gate invocation**, carrying the
  invocation id, gate point, dsx version, and a stdlib `hashlib` digest of the `validity_frame:`
  + `inference:` blocks. Two jobs in one record: it is the grouping anchor `dsx explain` needs to
  separate one run's trail from the next, and it is the **plan-time content lock ROADMAP Phase 10
  SC 4 conditions on** ("where a content lock … is captured at plan, reconciliation compares the
  recorded bytes, not the declared string"). Capturing it here means Phase 10 ships against real
  history instead of an empty capability. The hash is a property of the invocation, not of each
  decision, so it does not go on every record.
- **D-17: Crash-safety is fsync-per-record plus a tolerant reader.** Append one JSON line,
  `flush()` then `os.fsync()`; the reader skips an unparseable tail line rather than failing the
  file. Both halves are load-bearing — fsync makes the completed line survive the crash, tolerant
  reading makes the half-written one harmless. Stdlib only (D-01). The gate is not a hot path, so
  per-record fsync is negligible at the tens-of-records scale a gate produces.
- **D-18: `dsx explain` is a trail renderer with no `--block-on`.** Signature:
  `dsx explain [--spec PATH] [--phase-dir DIR] [--invocation ID] [--json]`, defaulting to the most
  recent invocation, human-readable text by default. It borrows `--spec`/`--phase-dir`/`--json`
  from `add_common()` (`dsx/cli.py:426-431`) but deliberately **not** `--block-on` — a
  `--block-on` flag on a command that always exits `0` is a lie in the help text, and D-04 is
  precisely about `explain` staying out of the block contract. **Refactor `add_common()` to make
  the blocking flags opt-in** rather than copy-pasting three arguments into a new parser.
- **D-19: The gate emits `layer: deterministic` records only — the append contract is documented.** REQ-P6-07 mandates the `layer` field, but nothing in `dsx` makes stochastic decisions — the
  agents do. Phase 6 documents file location, line format and required fields so a dsx agent can
  begin writing `layer: stochastic` entries with no further code change, and `dsx explain` renders
  both layers correctly the moment anything writes them. Wiring the agents was rejected as beyond
  the contract surface, and because two writers on one append-only file raises a Windows
  interleaving question the single-writer gate never has.

### D-05 enforcement (REQ-P6-11, M-08)

- **D-20: The citation-marker requirement binds new v2.0.0 checks only, via an explicit allow-list.** It applies to `dsx/frame/*` and the new `DSX-SPEC-08x` checks. The **206
  pre-existing finding codes across 17 families** are exempted by an allow-list carried *inside*
  the check itself, so the exemption is finite, visible and shrinks as codes get cited — not an
  implicit "anything old is fine". D-05's own wording is "no check *ships* without", written for
  this subsystem. Blanket retroactive enforcement was rejected on two grounds: it would swamp the
  contract work this phase exists to deliver, and many existing codes are structural
  (`DSX-SPEC` shape checks, `DSX-SQL` fan-out) with no primary statistical source — forcing a
  citation there manufactures exactly the fake authority D-05 exists to prevent.
  - **README must state the two tiers of evidentiary rigour plainly** rather than let a reader
    assume uniformity.
- **D-21: The marker is a structured docstring line.** `Citation:` naming author, year, work and
  the **exact formulation** — e.g. `Citation: Deng, Lu & Chen (2016), "Continuous Monitoring of
  A/B Tests without Pain", Theorem 1`. The script greps the prefix and asserts non-empty content.
  This maps directly onto a `citation:` key when Phase 11 applies the same rule to
  `references/families.yaml` data, satisfying REQ-P11-06 with **one mechanism, not two**, and it
  matches D-05's literal wording ("in its docstring"). A decorator was rejected for diverging from
  that wording and for sitting on functions while codes are emitted per `report.add` call; a
  prose-plus-year-token rule was rejected as unvalidatable in the way that matters.
- **D-22: Enforcement is per finding code, resolved by walking up.** Every new code must resolve
  to a `Citation:` line, found by walking from its `report.add(...)` call site to the enclosing
  function's docstring, falling back to the module docstring. This matches how
  `gen-finding-catalogue.py` already thinks — in codes, not functions — and the fallback handles a
  helper emitting several related codes off one source without forcing a code split for a
  documentation rule.
- **D-23: BOTH halves of D-05 are automated, not just the citation.** Docstrings carry `Citation:`
  **and** `Reference value:` (or `Structural criterion:` where the check is structural rather than
  numeric, per the ROADMAP D-05 bar at `ROADMAP.md:78-82`), and the script additionally asserts a
  linked test exists — via a `# D-05: <CODE>` marker comment in `tests/`, AST-walked. This closes
  M-08's argument completely rather than half of it: half (b) is the one that actually stops model
  knowledge being laundered into a blocking gate, and M-08's own reasoning ("an unenforced
  constraint is the first thing velocity pressure removes") applies to it verbatim.
  `scripts/gen-finding-catalogue.py` is a **build script, not the gate path**, so D-01 does not
  constrain what it reads — walking `tests/` is stdlib-easy. The test→code linking convention
  binds Phases 7–12 from the moment it lands; state it in the README.
  - ROADMAP SC 4's "proven against a deliberately violating case in the suite" applies to both
    halves.

### Claude's Discretion

The user explicitly delegated these; the researcher and planner may settle them without
returning to discuss:

- **Which real analyses the known-bad corpus encodes.** REQ-P6-13 requires ≥3 with documented
  post-mortems; D-06 pins two of them (frequentist and Bayesian uncontrolled-continuous
  monitoring) and REQ-P6-13 requires ≥1 interference case. *Which* published retraction,
  documented p-hacking case, or prior work is used for the interference case is open. brief §6
  M5 notes the operator's own past work is admissible; brief §6.5 makes vendor blogs and Medium
  posts inadmissible under D-05 in **either** direction.
- **Exact `DSX-SPEC-08x` number assignments.** `080` onward is free. D-06 makes these
  irreversible, so assign deliberately and leave gaps between concept groups.
- **The precise name of the per-invocation identifier** (constrained only by D-15: not `run_id`).
- **Plan slicing across the 16 requirements**, subject to the ROADMAP ordering constraints
  (REQ-P6-01 before REQ-P6-02; REQ-P6-09 in this phase; REQ-P6-10/11 before Phase 7 opens
  `frame/val.py`).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Binding inputs — not re-litigable

- `brief.md` §4 — decisions D-01…D-14. The single most important is D-05.
- `brief.md` §5 — the contract: §5.1 `validity_frame:`, §5.2 `inference:` (note M-02 removes
  `stopping_rule`), §5.3 the symmetric monitoring pair, §5.4 the paradigm manifest text,
  §5.5 the decision-record schema.
- `brief.md` §6 — milestone definitions; §6.5 gated backlog and the M1 fixture note (the
  prior-averaged vs point-null formulation trap); §6.6 open items (1 and 3 now resolved);
  §7 reference sources; §8 the known limit for the README; §9 runtime constraints.
- `.planning/PROJECT.md` — Key Decisions M-01…M-09, Constraints, Out of Scope, Known limits.
  **Note the amendment required by D-10 above at lines 79-80.**
- `.planning/REQUIREMENTS.md` — REQ-P6-01…REQ-P6-16, plus the Out of Scope and Open Items tables.
- `.planning/ROADMAP.md` — Phase 6 goal, ordering constraints and the five success criteria;
  lines 78-82 state the milestone-wide D-05 bar; line 238 states Phase 9's dependency on this
  phase.
- `.planning/STATE.md` — accumulated hard ordering constraints and standing per-phase deliverables.

### Research — advisory, superseded where this CONTEXT.md says so

- `.planning/research/SUMMARY.md` — synthesis; confidence assessment per area.
- `.planning/research/ARCHITECTURE.md` §4.3 — `design.peeking_policy` as single source.
  **Its Phase 9 sequencing recommendation is overridden by D-01 above.** Its module-layout and
  D-03a boundary analysis stands.
- `.planning/research/ARCHITECTURE.md` §5 — decision-record plumbing.
- `.planning/research/PITFALLS.md` — the ten pitfalls; #3 (severity misallocation), #8
  (pre-data/post-data seam), #9 (migration without grandfather path) and line 655 (vocabulary
  sync + EXP-060 regression) are directly load-bearing for this phase.
- `.planning/research/FEATURES.md` — reference values and their primary sources; UNSOURCED items
  flagged.
- `.planning/research/STACK.md` — the `_NULL` bug reproduction and fix (REQ-P6-01).

### Source files this phase modifies or must not disturb

- `dsx/loader.py:32` — `_NULL = {"", "null", "~", "none"}`; REQ-P6-01 drops `"none"`.
- `dsx/spec.py:63-68` — `PEEKING_POLICIES`; `:89` `VARIANCE_ADJUSTMENTS`; `:422` the
  `_validate_design_shape` pattern to mirror; `:544-563` `describe_vocabulary()`.
- `dsx/cli.py:72-84` `GATE_PROFILES`; `:87-92` `GATE_THRESHOLDS`; `:332-334` `cmd_vocab`;
  `:418-431` `build_parser` / `add_common`.
- `dsx/findings.py:26-33` — `Severity.INFO = 10`, zero consumers today; `DSX-PAR-001` is the first.
- `dsx/checks/design.py:444-461` — `_check_peeking` / `DSX-EXP-060`. **Must not change** (M-01).
- `dsx/checks/smells.py:156` — `DSX-SMELL-013` `run_id` consistency; the name collision behind D-15.
- `dsx/suppressions.py` — `DSX-SPEC-070…073`, the highest `DSX-SPEC` numbers in use.
- `scripts/gen-finding-catalogue.py` — AST-walks `report.add(...)`; extended by REQ-P6-11.
- `templates/ANALYSIS-SPEC.yaml:25` — `question_type: descriptive`; `:169` `run_id`.
- `examples/good-ANALYSIS-SPEC.yaml`, `examples/bad-ANALYSIS-SPEC.yaml` — D-08 contract.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- **`_validate_design_shape()` (`dsx/spec.py:422`)** — the exact pattern to mirror for
  `_validate_validity_frame_shape()` / `_validate_inference_shape()`: read the section, normalise,
  test membership against the closed vocabulary, `report.add` with `detail`/`remedy`/`where`.
- **`dsx.loader.load()`** — generic `Path → dict`; Phase 11 reuses it verbatim for
  `families.yaml`. No new parser is needed anywhere in v2.0.0.
- **`Severity.INFO` (`dsx/findings.py:29`)** — exists with **zero consumers**. `DSX-PAR-001` is
  its first real user, and `INFO = 10` sits below every configured threshold, so D-10's
  "never blocking" is satisfied structurally rather than by special-casing.
- **`gen-finding-catalogue.py`'s `extract()`** — already AST-walks for `report.add(...)` and
  pulls `(code, severity, title)`. REQ-P6-11 extends this walk to resolve a docstring upward from
  the same call site; the traversal machinery is in place.
- **`suppressions[]` with its ADR/SPEC authority requirement (Phase 5)** — the entire migration
  story for M-07. Zero new code.
- **`find_spec()` (`dsx/cli.py:94-113`)** — the resolution order (`phase_dir` → cwd →
  `.planning/`) that `DECISIONS.jsonl` reuses per D-14.

### Established Patterns

- **Closed vocabulary + structural membership check + `dsx vocab` dump** is the contract idiom.
  All new vocabularies follow it (D-04, D-05).
- **`GATE_PROFILES` and `GATE_THRESHOLDS` are independent knobs** — which checks run vs what
  blocks. Because `spec` is already in all four profiles, severity alone selects the gate point
  for the new structural checks (D-10). **No profile edit ships in Phase 6.**
- **Findings carry `detail`, `remedy` and `where`.** The empirical literature says actionability
  predicts fix rate far better than severity label, so the aggregate finding of D-11 must itemise
  the missing sub-blocks in `detail` and name the remedy concretely.
- **`_NULL`-style module constants are hand-maintained** — hence D-05's explicit registry.

### Integration Points

- `dsx/spec.py` — new shape validators + `DSX-SPEC-08x` codes + new vocabularies + registry.
- `dsx/frame/__init__.py` + `dsx/frame/paradigm.py` — new package; `DSX-PAR-001` only.
  **Must import nothing from `dsx.checks.*` except `Report`/`Finding`** (D-03a), asserted by the
  AST boundary test (REQ-P6-10, M-04). ARCHITECTURE §4.3 additionally suggests the boundary test
  cover "no `inference.paradigm` read outside `frame/paradigm.py`" — D-11 applies to
  `DSX-VAL-*`/`DSX-INT-*`, not to `DSX-PAR-*`, which exists to branch on paradigm.
- `dsx/decisions.py` — new top-level peer module (schema, accumulator, JSONL writer), importable
  from both `checks/` and `frame/` without creating a checks↔frame edge.
- `dsx/cli.py` — `explain` subcommand; `add_common` refactor (D-18); `cmd_vocab` output shape (D-03).
- `scripts/gen-finding-catalogue.py` — D-05 enforcement (D-20…D-23) + catalogue regen (REQ-P6-16).
- `tests/test_dsx.py` (1606 lines) — the single existing test module; new tests land alongside,
  including the deliberately-violating cases ROADMAP SC 4 requires.

</code_context>

<specifics>
## Specific Ideas

- **The naming rule the user articulated, which should govern every vocabulary decision in
  Phases 7–12:** *"A vocabulary member in a `dsx vocab` dump is read by an operator choosing a
  value under time pressure, not by someone holding §5.3 in their head. The name has to carry the
  distinction on its own."* This is why `uncontrolled_continuous` beat `optional_continuous`, why
  `dsx vocab` now emits descriptions, and why all frame vocabularies are dicts.
- **Traceability to the brief's own wording is worth little where the brief was already wrong** —
  the user's words: §5.2's field "was wrong enough to be removed in the previous gate" (M-02).
  Do not treat brief §5 phrasing as binding at the token level; §4 decisions and §5 *structure*
  are what bind.
- **Check for name collisions before coining a term.** The user asked for this on
  `uncontrolled_continuous`; it then caught the `run_id` collision (D-15) unprompted. Apply it to
  the invocation-id name and to every new vocabulary member in Phases 7–12.
- The `DSX-PAR-011` docstring must state the prior-averaged formulation explicitly and the fixture
  must comment the theorem its number traces to — brief §6.5 warns a formulation mismatch "will
  look like an implementation bug for a day". Phase 6 seeds the fixture; the docstring lands in
  Phase 9.

</specifics>

<deferred>
## Deferred Ideas

- **`dsx frame init` scaffolder subcommand** for migrating pre-v2.0.0 specs (PITFALLS #9's
  suggestion). No REQ-P6-* covers it, and M-07's `suppressions[]` path already provides the
  migration story with zero new code. Would be its own scope.
- **`dsx explain --code DSX-XXX-NNN`** — a rule/citation lookup mode independent of any run.
  Serves goal #2 (operator learning) well, but needs a per-code prose source of truth that
  Phase 6 would have to invent. Revisit once the D-05 `Citation:` markers exist across a family —
  they are most of the data such a mode would need.
- **Wiring dsx agents and skills to append `layer: stochastic` records.** D-19 documents the
  append contract so this becomes a no-code-change follow-up; the work itself reaches into
  `agents/` and `skills/`, beyond this phase's contract surface.
- **Retroactive D-05 sourcing for the 206 legacy finding codes.** D-20's allow-list is designed to
  shrink; a later phase or a background effort can retire entries from it. Explicitly not this
  phase's work.

</deferred>

---

*Phase: 6-contract-extension-decision-record-paradigm-manifest*
*Context gathered: 2026-08-07*
