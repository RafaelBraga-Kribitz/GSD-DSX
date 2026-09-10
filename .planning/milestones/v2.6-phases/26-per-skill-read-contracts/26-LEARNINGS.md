---
phase: 26
phase_name: "Per-skill read contracts"
project: "gsd-dsx"
generated: "2026-09-10"
counts:
  decisions: 7
  lessons: 6
  patterns: 6
  surprises: 6
missing_artifacts:
  - "UAT.md"
---

# Phase 26 Learnings: Per-skill read contracts

## Decisions

### D-26-01 — Visible `<inputs>` block, not hidden HTML-comment fences
The Architect persona proposed a visible `<inputs>` block with bold-labeled key lines; the Auditor persona proposed hidden `<!-- reads:eda-frontmatter -->` HTML-comment fences with one key per line for wrap-safety. The orchestrator converged on the visible block, keeping the Auditor's one-key-per-bullet wrap-safety but rejecting the hidden fence.

**Rationale:** Rigour > reliability > flexibility. A portfolio artifact read by skeptical engineers should parse the keys the reader *sees*; a hidden comment fence creates a parallel structure that can silently drift from the visible prose. One-key-per-bullet gives wrap-safety without a hidden layer — any non-conforming line fails loudly instead of letting stray prose masquerade as "zero keys."
**Source:** 26-CONTEXT.md

### D-26-02 — Grounded per-skill key mapping demotes prose-only facts out of the key lists
The scope proposal had given `dsx-define-metrics` a "joins matrix" and `dsx-build-model` a `policy_recommendation` as if they were front-matter keys. Both live only in EDA prose (§1 Joins; §4 Wide categoricals), not in the front-matter block. The settled mapping moved both to zero-backtick "Also consult" prose lines instead of key bullets, and corrected other scope errors (`contradictions[]`→`contradictions`, bare `weekly_cycle_amplitude`→`dependence.weekly_cycle_amplitude`, `grain.implied_dependence` expanded to its two real leaves).

**Rationale:** Naming a prose-only fact as a backtick key would fail REQ-P26-02's guard (the key genuinely doesn't exist in front-matter) — so the guard's own mechanism forced the mapping to be honest about what is machine-parseable versus what is narrative guidance.
**Source:** 26-CONTEXT.md

### D-26-03 — Three-tier fallback wording, per skill, mirroring the executor fragment
Each skill's `When absent:` sentence follows the same three-tier honesty ladder already stated in `capabilities/dsx/fragments/executor.md`: recorded absence (`eda_artifact: none`) → DATA-PROFILE fallback → `computed_by` declared honesty — scoped to the specific facts that skill would otherwise fake (e.g., scope-analysis never reads a missing EDA as a `stop_triggered` clear).

**Rationale:** The executor fragment already states this rule for the general analytical loop; restating it per skill (rather than inventing a new mechanism) keeps one honesty ladder as the single source of truth instead of five divergent ad hoc fallbacks.
**Source:** 26-CONTEXT.md

### D-26-04 — Guard-test contract: full dotted-path matching, negative control, uncomment pre-processor
Adopted the Auditor's guard design in full: `tests/test_skill_read_contracts.py`, off the gate path, zero imports from `dsx/`, full dotted-path set-membership (leaf-only matching explicitly rejected), an uncomment pre-processor for DATA-PROFILE.yaml's commented example keys, an in-file negative control (`grain.__orphan__`, `columns[].__orphan__`) proving the guard discriminates, and an anchor non-vacuity pin (`len(eda) >= 30`) guarding against a degenerate empty parse.

**Rationale:** Leaf-only matching would let a parent rename (`base_rate:`→`baseline:`) leave a same-named leaf (`overall`) matchable elsewhere and silently orphan the read step — exactly the failure REQ-P26-02 forbids. The negative control is the load-bearing proof that the assertion actually discriminates rather than passing vacuously.
**Source:** 26-CONTEXT.md

### Skill-only invariant — zero `dsx/` edits, zero new finding codes
The phase boundary explicitly excludes any change under `dsx/`, any template edit, and any new finding code. Proven at close: `git diff --stat -- dsx/` empty across the whole phase, and the finding catalogue held set-identity 276 → 276.

**Rationale:** This phase is skill-doc + one off-gate-path test only; a genuinely needed fact with no existing template key is a scope escalation (a template would grow), not license to invent a key.
**Source:** 26-CONTEXT.md; 26-04-SUMMARY.md

### Installer re-sync gate: `node install.mjs && node install.mjs --check`, never `--check` alone
Phase end requires re-running the installer copy step before the check step, reusing the exact command sequence Phase 25 established.

**Rationale:** `install.mjs`'s `check()` only verifies manifest-declared skill directories exist and the self-test passes — it does not diff file content. A stale installed copy with the pre-edit `SKILL.md` would still pass `--check` alone; only `node install.mjs` first actually re-copies `skills/` into the runtime overlay.
**Source:** 26-RESEARCH.md (Pitfall 3); 26-04-SUMMARY.md

### Do not `import yaml` — hand-roll a stdlib-only line-oriented parser
The new guard test deliberately avoids PyYAML even though it is installed and would parse the templates without error.

**Rationale:** Two independent reasons: (1) every per-column/flag-gated key the skills need lives behind a YAML `#` comment, and every conformant parser (PyYAML included) discards comments by design — so PyYAML alone would return `columns: null` and miss `unit`/`target` entirely; (2) PyYAML is an optional dependency in this repo's own established pattern (`dsx/loader.py` falls back to a bundled parser when absent, "a blocking gate must never fail because of a missing dependency") — importing it unconditionally in a new test would be this repo's first hard third-party test dependency.
**Source:** 26-RESEARCH.md

---

## Lessons

### `--check` alone never proves installed content is current
`install.mjs`'s `check()` verifies presence (directory exists) and a self-test, not file content — it would report success even against a stale installed copy carrying the pre-edit `SKILL.md`.

**Context:** Surfaced during research as "Pitfall 3" before execution, then applied correctly at phase close (26-04): `node install.mjs` (re-sync) run before `node install.mjs --check` (verify), never the check alone.
**Source:** 26-RESEARCH.md; 26-04-SUMMARY.md

### A naive "push every key onto the indent stack" parser mis-nests fully-commented blocks
26-RESEARCH.md traced the uncomment indentation math only for the `columns:` block, where the block header is a real, uncommented top-level key at indent 0. The `unit:` and `target:` blocks are fully commented — their headers (`# unit:`, `# target:`) sit at column 0 and uncomment to indent 2, not 0. The first GREEN implementation attempt nested them under the preceding top-level scalar `sentinels_found: []`, producing `sentinels_found.unit.rows_per_unit` instead of `unit.rows_per_unit`.

**Context:** Fixed by pushing a key onto the indent stack only when its value is empty (a potential block parent); scalars, scalar-lists, and flow-maps never become parents. This kept the fix inside the parser body as a correctness detail of D-26-04's "indent-stack + inline-flow awareness," not a design change.
**Source:** 26-03-SUMMARY.md

### The two templates the guard reads do not share one line-ending convention
`templates/EDA.md` is CRLF (206/206 lines, matching the general repo convention); `templates/DATA-PROFILE.yaml` is the outlier at 0 CRLF / 72 bare-LF.

**Context:** A `\r\n`-only split would silently find zero line breaks in `DATA-PROFILE.yaml` (a vacuous empty parse, not a crash) — exactly the failure class the anchor non-vacuity pin is designed to catch. Every line-oriented operation must use `\r?\n` (or `splitlines()`), never special-case one template's convention.
**Source:** 26-RESEARCH.md

### Leaf-only key matching is empirically, not just theoretically, unsafe for these templates
Both templates were checked and genuinely do contain leaf-name collisions across unrelated blocks: `overall` appears under both `base_rate` and (commented) `target`; `verdict` appears under `grain`, `base_rate`, `branch`, `time.tz_verdicts[]`, and (commented) `target` — five distinct `verdict` leaves.

**Context:** Confirms full dotted-path matching (D-26-04's rejection of leaf-only matching) is a necessity for this exact template pair, not a defensive over-design; a parent rename really could hide behind a same-named leaf elsewhere.
**Source:** 26-RESEARCH.md

### CONTEXT.md's own stated rationale for avoiding PyYAML was factually wrong, though its conclusion held
CONTEXT.md said "no PyYAML — the templates carry placeholders like `<int>` and `MCAR | MAR | …` that will not load." Live testing showed `yaml.safe_load()` parses both templates cleanly — the placeholders are valid YAML scalars.

**Context:** The real, stronger reason the stdlib parser is still mandatory: every per-column/flag-gated key lives behind a `#` comment, which any conformant YAML parser (PyYAML included) discards by design. The design conclusion (hand-roll a parser) was correct; the stated justification needed correcting in the new test's docstring.
**Source:** 26-RESEARCH.md

### Already-commented example lines can carry a second, semantic `#` comment
Some commented example lines in `templates/DATA-PROFILE.yaml` carry a second `#`-delimited comment after the value, e.g. `#   verdict: stable        # stable | drifting | null (...)`. Uncommenting must replace only the FIRST `#` (the one commenting out the whole line), then separately strip any remaining trailing `# …` — doing these steps in the wrong order or skipping the second corrupts the key/value split.

**Context:** Not hypothetical — it hits at least 3 live commented lines the research session touched (`verdict`, `first_period_ratio`, `last_period_ratio`).
**Source:** 26-RESEARCH.md

---

## Patterns

### Visible `<inputs>` block, one backtick-wrapped key per bullet line
A literal `<inputs>…</inputs>` block placed immediately after `</objective>` (before `<precondition>` for `dsx-narrate`'s exception), with EDA and DATA-PROFILE key regions each listing one backtick-quoted dotted-path key per bullet line, a "These set:" prose line, an optional zero-backtick "Also consult" prose line, and a "When absent:" fallback line.

**When to use:** Any agent-facing prompt/skill that needs to declare a machine-checkable read contract against a structured artifact, where the contract must be both human-legible (visible to a skeptical reader) and independently guardable (parseable by an off-gate-path test) without a parallel hidden structure that can drift.
**Source:** 26-CONTEXT.md; 26-01-SUMMARY.md; 26-02-SUMMARY.md

### Three-tier absent-artifact honesty ladder
Recorded absence (`eda_artifact: none`) → fallback source (`DATA-PROFILE.yaml`) → declared honesty (`computed_by`) rather than asserting a fact the skill cannot substantiate, mirrored verbatim in wording pattern from one canonical source (`capabilities/dsx/fragments/executor.md`) into every consumer.

**When to use:** Any skill or agent step that depends on an optional upstream artifact and must degrade gracefully without silently fabricating the missing evidence.
**Source:** 26-CONTEXT.md

### Zero-backtick "Also consult" line as a prose/key demotion mechanism
A prose-only reference to EDA narrative sections (e.g., "§1 Joins", "§4 Wide categoricals") is written as plain text with zero backtick characters, and the guard asserts the line contains no backticks — enforcing that prose references can never be mistaken for machine-parsed keys.

**When to use:** Whenever a read contract needs to point a reader at narrative guidance that has no corresponding structured field, without letting that reference masquerade as (or later drift into) an enforceable key.
**Source:** 26-CONTEXT.md; 26-REVIEW.md

### Off-gate-path repo-integrity test: stdlib-only, zero imports from the gated module tree
`tests/test_skill_read_contracts.py` imports only `re`/`unittest`/`pathlib`/`__future__`, structurally outside `test_gate_path_hermetic`'s import-closure walk (which starts only from `dsx.cli.GATE_PROFILES`-resolved files) by construction — nothing in `dsx/` ever imports from `tests/`.

**When to use:** Any structural/documentation-drift guard that validates prose or template agreement rather than runtime behavior, where the guard should never participate in (or risk tripping) the blocking gate profile.
**Source:** 26-RESEARCH.md

### In-file negative control + anchor non-vacuity pin as the anti-silent-orphan proof
A fabricated key (`grain.__orphan__`, `columns[].__orphan__`) is fed through the exact same matcher the real assertions use and must be rejected; separately, a non-vacuity pin (`len(eda) >= 30`, known real keys present) guards against the parser degenerating to an empty or over-broad set that would make every membership test pass vacuously.

**When to use:** Any guard whose entire value proposition is "a rename/removal must be caught" — without a negative control, a guard that only ever asserts positive membership cannot prove it discriminates at all.
**Source:** 26-CONTEXT.md; 26-03-SUMMARY.md

### Bidirectional membership test (skill-side and template-side renames both fail)
The membership test is asserted both ways: each skill's live `<inputs>` keys must equal the ratified D-26-02 matrix, AND each key must exist in the live template key set — so a skill-side edit that drifts from the ratified mapping fails just as loudly as a template-side rename.

**When to use:** Where a documented "expected" mapping and a "live ground truth" both exist and could each independently drift; testing only one direction leaves the other undefended.
**Source:** 26-03-SUMMARY.md

---

## Surprises

### The entire D-26-02 mapping resolved against live templates with zero orphaned keys on first check
Every key across all five skills' EDA and DATA-PROFILE regions (~30 rows) was checked by direct file read against the live templates before any code was written, and none failed to resolve — no trimming was needed for correctness.

**Impact:** The grounding work invested in CONTEXT.md and RESEARCH.md (reading both templates in full, hand-tracing every key) paid off as a genuinely clean mapping rather than one requiring plan-time correction, which is unusual enough to be worth recording as a confirmation the upfront rigor was proportionate.
**Source:** 26-RESEARCH.md

### `columns[].categorical` is an intermediate map header, not a leaf value
`categorical:` is a sub-map header one level under `columns.column_name`, not a scalar leaf — it only resolves as a named key because the guard records every intermediate dotted path, not just leaves.

**Impact:** Validates D-26-04's rejection of leaf-only matching wasn't just about collision-safety; it was also necessary for this specific key to be nameable at all. Confirmed both by trace (RESEARCH) and by byte-level re-verification during code review.
**Source:** 26-RESEARCH.md; 26-REVIEW.md

### The traced indentation math worked for one template block but not another, only discovered at GREEN
26-RESEARCH.md's hand-traced indentation math (verified against the live `columns:` block) turned out not to generalize to the fully-commented `unit:`/`target:` blocks, whose headers uncomment to indent 2 rather than 0 — this was found only when the first parser implementation actually failed a test (`unit.rows_per_unit` resolving as `sentinels_found.unit.rows_per_unit`), not by further static analysis.

**Impact:** A concrete instance of research-verified-but-incomplete: the RESEARCH grounding was accurate as far as it traced, but traced only one representative case; TDD's RED→GREEN cycle caught the gap that pure research reading did not.
**Source:** 26-03-SUMMARY.md

### An exhaustive manual rename probe during code review found zero gaps
The reviewer did not take the GREEN claim on trust: it mechanically renamed every skill-named leaf key, every parent key (`columns`, `time`, `target`, `unit`, `grain`, `implied_dependence`, `dependence`, `base_rate`), and the `column_name` placeholder token, confirming each rename left zero surviving referenced keys — i.e., the guard would have failed the suite in every one of those cases.

**Impact:** Moved REQ-P26-02's "renamed key fails loudly" claim from theoretical (tested only against two synthetic negative-control keys) to empirically exhaustive against every real key actually in use.
**Source:** 26-REVIEW.md

### All three code-review findings were accepted with zero code changes, and phase closed with zero blocking issues
The review returned 0 HIGH / 0 MEDIUM / 3 LOW, all three "latent-robustness" notes about hypothetical future template shapes (positional `#` stripping corrupting a value that legitimately embeds `#`; hyphenated key names being silently excluded from the parsed set; intermediate map-header paths being accepted as members) — none triggered by current templates or skills, all accepted as documented residuals rather than fixed.

**Impact:** The phase shipped with a security register showing 8/8 threats closed and a verification verdict of PASSED with zero fixes applied post-review — an unusually clean close for a phase that added both new prompt surface and a new parser.
**Source:** 26-REVIEW.md; 26-VERIFICATION.md; 26-SECURITY.md

### Two persona divergence rounds produced zero requirement rewording and zero human escalation
Despite the Architect/Auditor advisor round surfacing one real design divergence (visible vs. hidden `<inputs>` shape), the phase's own D-05 escalation burden was recorded as 0 — no scope change, no reworded requirement, silence-equals-accept applied cleanly.

**Impact:** Notable for a phase that minted zero finding codes and touched zero `dsx/` code: the entire design-quality bar was met through internal advisor convergence plus a deep code review, without needing to escalate any open question to the human.
**Source:** 26-CONTEXT.md
