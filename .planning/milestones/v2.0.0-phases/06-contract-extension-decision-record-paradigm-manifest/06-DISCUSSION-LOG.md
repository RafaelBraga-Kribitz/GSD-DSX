# Phase 6: Contract extension, decision record, paradigm manifest - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-08-07
**Phase:** 6-contract-extension-decision-record-paradigm-manifest
**Areas discussed:** PEEKING_POLICIES timing and vocabulary shape, Requiredness codes + severity, Decision record scope, D-05 marker scope

Gray areas offered but not selected for discussion: none — all four were selected. Two smaller
areas were parked as Claude's discretion at the outset (`dsx explain` surface, known-bad fixture
selection); the first was pulled into the decision-record area on the user's request, the second
remains at discretion.

---

## PEEKING_POLICIES timing and vocabulary shape

### Q1 — REQ-P6-05 (Phase 6) vs ARCHITECTURE §4.3 (Phase 9)

| Option | Description | Selected |
|--------|-------------|----------|
| Ship in Phase 6 (Recommended) | Phase 6's Bayesian known-bad fixture is a real consumer; without the member it trips DSX-SPEC-042 at HIGH and cannot pass `dsx validate` structurally per ROADMAP SC 5. No requirement edits. | ✓ |
| Defer to Phase 9 per §4.3 | Follow the research recommendation; amend REQ-P6-05, ROADMAP SC 1 and the Phase 9 depends-on line. | |
| Ship in 6, flag consumer-pending | Add the member but mark it as having no semantic consumer until Phase 9. | |

**User's choice:** Ship in Phase 6.
**Notes:** The deciding evidence was surfaced during the discussion, not present in the research —
`dsx/spec.py:448-457` fires `DSX-SPEC-042` at HIGH on an unrecognised `peeking_policy`, which
falsifies §4.3's "no consumer for two milestones" premise.

### Q2 — Member name

| Option | Description | Selected |
|--------|-------------|----------|
| `uncontrolled_continuous` (Rec) | ARCHITECTURE §4.3's suggestion; names the discipline failure and contrasts unambiguously with `always_valid`. | ✓ |
| `optional_continuous` | brief §5.2/§5.3's own wording; maximum traceability to the binding input. | |
| `continuous_uncorrected` | Most literal about the defect. | |

**User's choice:** `uncontrolled_continuous`.
**Notes:** The user supplied the governing principle in full — *"A vocabulary member in a `dsx
vocab` dump is read by an operator choosing a value under time pressure, not by someone holding
§5.3 in their head. The name has to carry the distinction on its own."* They rejected
`optional_continuous` because "optional stopping" names the design rather than the control, so it
reads as a synonym of `always_valid` to anyone who half-knows the literature — the exact
misconception `DSX-PAR-011` exists to catch — and noted that traceability to brief §5.2's wording
is worth little given that section's field "was wrong enough to be removed in the previous gate"
(M-02). They rejected `continuous_uncorrected` for describing the analyst's omission rather than a
property of the procedure, for reading oddly beside `sequential_obf`/`sequential_pocock` which name
methods, and because "uncorrected" hints at multiplicity correction, a different DSX family. They
requested a collision check before committing; it came back clean, and the same habit later caught
the `run_id` collision in the decision-record area.

### Q3 — Which Phase 6 fixtures declare it

| Option | Description | Selected |
|--------|-------------|----------|
| Bayesian known-bad only (Rec) | Smallest surface; Phase 9 brings its own frequentist fixture. | |
| Both halves seeded now | Ship a frequentist uncontrolled-continuous fixture too, so both halves of the Phase 9 atomic pair have committed targets. Serves D-12. | ✓ |
| Add to canonical bad fixture too | Extend `examples/bad-ANALYSIS-SPEC.yaml` as well. | |

**User's choice:** Both halves seeded now.
**Notes:** One fixture beyond REQ-P6-13's floor. Also partially resolves the parked
fixture-selection question — two of the three required known-bad cases are now pinned.

### Q4 — Proving DSX-EXP-060 unaffected (M-01, PITFALLS:655)

| Option | Description | Selected |
|--------|-------------|----------|
| Parametrised disjointness (Rec) | One test over all five members asserting EXP-060 fires for `""` and `fixed_horizon` and nothing else. Pins the property, not a snapshot. | ✓ |
| Re-run existing fixtures | Assert unchanged output on today's EXP-060 fixtures. | |
| Both | Parametrised test plus the snapshot assertion. | |

**User's choice:** Parametrised disjointness.
**Notes:** Confirmed during discussion that `dsx/checks/design.py:451` already gates on
`policy in ("", "fixed_horizon")`, so M-01 holds by construction and no EXP-060 code change is
needed. The test exists to keep it that way.

### Q5 — `dsx vocab` and descriptions

| Option | Description | Selected |
|--------|-------------|----------|
| Emit as name→description (Rec) | `peeking_policies` becomes an object; sets stay flat lists; `always_valid`'s description tightened. | ✓ |
| Separate descriptions key | Purely additive top-level `"descriptions"` object. | |
| Leave the dump alone | Carry the distinction in template comments and README. | |

**User's choice:** Emit as name→description.
**Notes:** Prompted by a finding surfaced mid-discussion — `describe_vocabulary()` at
`dsx/spec.py:552` dumps `sorted(PEEKING_POLICIES)`, so the descriptions that carry the whole
distinction never reach the operator. A parallel `descriptions` key was rejected as the
split-vocabulary pattern M-02 and M-09 already argued against.

### Q6 — Vocabulary/dump sync (REQ-P6-06)

| Option | Description | Selected |
|--------|-------------|----------|
| Introspection test (Rec) | Walk module-level constants and assert each is dumped; generalises to Phases 7–12. Needs a deny-list for existing non-vocabulary constants. | |
| Explicit registry + test | One hand-maintained tuple; `describe_vocabulary()` built from it; test asserts coverage. | ✓ |
| Assert the new ones only | Name each new vocabulary in a Phase 6 test. | |

**User's choice:** Explicit registry + test.

### Q7 — Sets or description dicts for the new frame vocabularies

| Option | Description | Selected |
|--------|-------------|----------|
| All description dicts | Every new frame vocabulary teaches itself in `dsx vocab`; brief §5.1 already carries the prose. | ✓ (on reversal) |
| Dicts where subtle, sets elsewhere | Descriptions only where the distinction is real. | (initially selected) |
| Plain sets throughout | Match the existing codebase. | |

**User's choice:** Initially "dicts where subtle, sets elsewhere"; **reversed to "dicts always, no
split rule"** after a follow-up question asked what criterion would keep "subtle" stable across
Phases 7–12. The three candidate criteria offered were a term-of-art test (recommended), a member
count threshold, and following brief §5.1's comment placement. The user's response — *"dict always,
no split rule"* — removed the need for any of them.
**Notes:** Worth recording as a pattern: the criterion question is what exposed that the split
wasn't worth its own rule.

---

## Requiredness codes + severity

Research surfaced before this area: false positives were 76% of static-analysis warnings in a
Tencent industrial study and >90% counting incomplete-context cases; 56% of SAST warnings across
30 OSS Java projects were never addressed; and *actionability*, not severity label, is what
correlates with fix rate.

### Q1 — Location and namespace

| Option | Description | Selected |
|--------|-------------|----------|
| spec.py, DSX-SPEC-08x (Rec) | Mirror `_validate_design_shape`; `spec` already in all four gate profiles so no GATE_PROFILES change; `DSX-SPEC-0xx` free from 080. | ✓ |
| Shape in spec.py, requiredness in frame/ | Separate well-formedness from requiredness. | |
| All in frame/ | Keep every v2.0.0 contract concern behind the D-03a boundary. | |

**User's choice:** spec.py, DSX-SPEC-08x.

### Q2 — Severity of a missing required sub-block

| Option | Description | Selected |
|--------|-------------|----------|
| CRITICAL uniformly (Rec) | Blocks from plan onward; serves "before the data is touched" literally; M-07 gives the migration path. Requires amending PROJECT.md:79. | ✓ |
| HIGH uniformly | Blocks at verify/ship, exactly as PROJECT.md:79 already states. | |
| Split by conditionality | CRITICAL for the always-required triad, HIGH for the question_type-conditional blocks. | |

**User's choice:** CRITICAL uniformly.
**Notes:** The conflict was put to the user directly — PROJECT.md:79-80 says "required at
verify/ship" (implying HIGH), PITFALLS #3 says "CRITICAL only for structural absence", and the core
value says "before the data is touched". Choosing CRITICAL makes PROJECT.md:79-80 an amendment
action rather than a D-14 reversal, since the version rationale sits outside both decision tables.

### Q3 — Finding granularity for a legacy spec

| Option | Description | Selected |
|--------|-------------|----------|
| Aggregate when absent (Rec) | One finding when the block is absent, itemised in `detail`; per-sub-block when partial. One suppression entry grandfathers a legacy spec. | ✓ |
| One per missing sub-block | Uniform and mechanical; three to six CRITICALs and suppression entries per legacy spec. | |
| One finding for the whole rule | Fewest irreversible codes burned; cannot target a single remaining gap with `suppressions[]`. | |

**User's choice:** Aggregate when absent.

### Q4 — Template scope

| Option | Description | Selected |
|--------|-------------|----------|
| Full blocks scaffolded (Rec) | Both blocks with brief §5.1/§5.2 guidance comments and placeholders; `dsx init` output keeps passing its own gate. | ✓ |
| Required triad only, rest commented | Smallest passing scaffold for the template's `descriptive` default. | |
| Template unchanged this phase | Document in README only. | |

**User's choice:** Full blocks scaffolded.
**Notes:** Forced by the CRITICAL decision — `templates/ANALYSIS-SPEC.yaml:25` declares
`question_type: descriptive`, and `estimand`/`units`/`measurement` are required for every question
type, so an unchanged template would ship a spec failing its own gate at plan.

---

## Decision record scope

Research surfaced before this area: the standard crash-safe append pattern is line-granular — a
crash mid-append leaves an unparseable tail line the reader skips; durability comes from
`flush()` + `os.fsync()` per record; `buffering=1` alone reaches the OS buffer, not the disk; and
readers that fail the whole file on one bad line are the common defect.

### Q1 — What emits records in Phase 6

| Option | Description | Selected |
|--------|-------------|----------|
| New surface only (Rec) | DSX-PAR-001 plus the new DSX-SPEC-08x adjudications; the 15 existing modules untouched. Matches STATE.md's per-family standing deliverable. | ✓ |
| Retrofit every check module | Satisfies brief §5.5's "emitted by every step" literally; collides with the D-05 marker work. | |
| New surface + a sample retrofit | Two representative legacy modules to prove the emitter works from both paths. | |

**User's choice:** New surface only.

### Q2 — Storage and invocation identity

| Option | Description | Selected |
|--------|-------------|----------|
| One file beside the spec (Rec) | `DECISIONS.jsonl` resolved like `find_spec()`, appended across invocations, each record tagged with an id named something other than `run_id`. | ✓ |
| One file per invocation | No interleaving; scattered cross-gate trail. | |
| Fixed `.planning/` location | Matches GSD conventions; breaks the spec-adjacent property and fails outside a GSD repo. | |

**User's choice:** One file beside the spec.
**Notes:** The `run_id` collision was surfaced before the question — `run_id` is already an
operator-declared readout id in `visuals[]` and `FIGURE-MANIFEST.yaml`, enforced by
`DSX-SMELL-013` at `dsx/checks/smells.py:156`.

### Q3 — Crash-safety mechanism

| Option | Description | Selected |
|--------|-------------|----------|
| fsync per record + tolerant read (Rec) | Both halves load-bearing; stdlib only; gate is not a hot path. | ✓ |
| Line buffering, no fsync | Survives a process crash, not a machine crash. | |
| Buffer in memory, one fsync at exit | Always well-formed; loses the entire trail on a hard crash — the run you would most want to explain. | |

**User's choice:** fsync per record + tolerant read.

### Q4 — Phase 10's plan-time content lock

| Option | Description | Selected |
|--------|-------------|----------|
| Invocation-header record (Rec) | One header per invocation carrying id, gate point, dsx version and a `hashlib` digest of the two blocks; doubles as `dsx explain`'s grouping anchor. | ✓ |
| Field on every record | Self-contained records; repeats the hash on every line and still leaves no grouping key. | |
| Defer entirely to Phase 10 | Smallest Phase 6; Phase 10 ships against zero history. | |

**User's choice:** Invocation-header record.
**Notes:** Raised because ROADMAP Phase 10 SC 4 conditions on a lock "captured at plan", and the
plan-time decision record is the only channel that exists to capture it.

### Q5 — `dsx explain` surface

| Option | Description | Selected |
|--------|-------------|----------|
| Trail renderer, no `--block-on` (Rec) | `--spec`/`--phase-dir`/`--invocation`/`--json`; refactor `add_common()` to make blocking flags opt-in. | ✓ |
| Also a `--code` lookup mode | Rule/citation lookup without a run; needs a per-code prose source of truth. | |
| Positional JSONL path | Simplest signature; diverges from `--spec`-driven discovery. | |

**User's choice:** Trail renderer, no `--block-on`.
**Notes:** This was one of the two areas originally parked as Claude's discretion; the user pulled
it into discussion. Grounded on `dsx/cli.py:426-431` — every subcommand shares `add_common()`,
which carries `--block-on`, and that flag on a command that always exits `0` is a lie in the help
text.

### Q6 — Who writes `layer: stochastic` records

| Option | Description | Selected |
|--------|-------------|----------|
| Gate emits, convention documented (Rec) | Deterministic records only; append contract documented so an agent can start writing with no code change. | ✓ |
| Wire the agents too | Goal #2 fully alive; reaches into `agents/`/`skills/`; two writers on one append-only file raises a Windows interleaving question. | |
| Gate-only, path left open | Field ships meaning nothing; first agent invents a format the reader may disagree with. | |

**User's choice:** Gate emits, convention documented.

---

## D-05 marker scope

Research surfaced before this area added little — the literature covers citing software, not
enforcing citations inside it. The one transferable point: the community converged on
machine-readable structured metadata (CITATION.cff, codemeta.json) rather than free prose, because
prose cannot be validated. Grounding established instead from the codebase: **206 unique finding
codes across 17 families**, most check functions carrying no docstring at all.

### Q1 — Retroactive scope

| Option | Description | Selected |
|--------|-------------|----------|
| New checks only, explicit list (Rec) | Binds `dsx/frame/*` and the new DSX-SPEC-08x checks; the 206 legacy codes exempted by a visible, shrinking allow-list inside the check. | ✓ |
| All 206 codes, no exemptions | Strongest reading of D-05; would swamp the phase, and structural codes have no primary statistical source, so the rule would force fake citations. | |
| All statistical checks, structural exempt | Principled rather than grandfathered; "is this statistical?" is a judgement made 206 times. | |

**User's choice:** New checks only, explicit list.

### Q2 — Marker syntax

| Option | Description | Selected |
|--------|-------------|----------|
| Structured docstring line (Rec) | `Citation:` naming author, year, work and exact formulation; maps onto a `citation:` key for `families.yaml` in Phase 11, satisfying REQ-P11-06 with one mechanism. | ✓ |
| Decorator on the check | Machine-readable without prose parsing; diverges from D-05's "in its docstring". | |
| Prose plus a source token | Lowest friction; unvalidatable in the way that matters. | |

**User's choice:** Structured docstring line.

### Q3 — Unit of enforcement

| Option | Description | Selected |
|--------|-------------|----------|
| Per code, walk up to enclosing (Rec) | Walk from the `report.add(...)` call site to the enclosing function docstring, falling back to the module docstring. Matches how the catalogue already thinks. | ✓ |
| Per function, no fallback | No silent inheritance; forces code splits for a documentation rule. | |
| Per module | One block shows a family's whole evidentiary basis; citation drifts from the logic it justifies. | |

**User's choice:** Per code, walk up to enclosing.

### Q4 — Does Phase 6 automate D-05's second half

| Option | Description | Selected |
|--------|-------------|----------|
| Automate both halves (Rec) | `Citation:` + `Reference value:` (or `Structural criterion:`), plus a `# D-05: <CODE>` test-linkage marker AST-walked from `tests/`. Closes M-08's argument completely. | ✓ |
| Citation marker only | Exactly REQ-P6-11 as written; leaves the laundering-prevention half unenforced. | |
| Both markers, no test linkage | Docstring names the value; nothing checks a test asserts it. | |

**User's choice:** Automate both halves.
**Notes:** Raised because ROADMAP:78-82 states the milestone D-05 bar as *both* halves while
REQ-P6-11 and ROADMAP SC 4 automate only the first, and M-08's own rationale ("an unenforced
constraint is the first thing velocity pressure removes") applies to the second verbatim. Noted
during the question that `scripts/gen-finding-catalogue.py` is a build script, not the gate path,
so D-01 does not constrain what it reads.

---

## Claude's Discretion

- **Which real analyses the known-bad corpus encodes.** Two of the three are now pinned by the
  fixture-seeding decision (frequentist and Bayesian uncontrolled-continuous monitoring); the
  interference case and any beyond the floor are at discretion. brief §6 admits the operator's own
  past work; brief §6.5 makes vendor blogs and Medium posts inadmissible under D-05 in either
  direction.
- **Exact `DSX-SPEC-08x` number assignments** (`080` onward free; D-06 makes them irreversible).
- **The precise name of the per-invocation identifier**, constrained only by not being `run_id`.
- **Plan slicing across the 16 requirements**, subject to the ROADMAP ordering constraints.

Offered but declined at the closing prompt: further discussion of fixture case selection,
`DSX-SPEC-08x` numbering, and how the extended good/bad fixtures satisfy D-08 under CRITICAL
requiredness.

## Deferred Ideas

- `dsx frame init` scaffolder subcommand for migrating pre-v2.0.0 specs (PITFALLS #9). No REQ-P6-*
  covers it; M-07's `suppressions[]` path already provides the migration story with zero new code.
- `dsx explain --code DSX-XXX-NNN` rule/citation lookup independent of a run. Revisit once D-05
  `Citation:` markers exist across a family — they are most of the data it would need.
- Wiring dsx agents and skills to append `layer: stochastic` records. D-19's documented append
  contract makes this a no-code-change follow-up.
- Retroactive D-05 sourcing for the 206 legacy finding codes. The allow-list is designed to shrink.
