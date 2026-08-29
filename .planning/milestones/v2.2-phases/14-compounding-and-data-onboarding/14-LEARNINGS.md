---
phase: 14
phase_name: "Compounding and data onboarding"
project: "gsd-dsx"
generated: "2026-08-29"
counts:
  decisions: 7
  lessons: 3
  patterns: 5
  surprises: 2
missing_artifacts:
  - "UAT.md"
---

# Phase 14 Learnings: Compounding and data onboarding

## Decisions

### D-01 — Skill/doc/template-only packaging, zero `dsx/**/*.py` edits
Phase 14's entire artifact set is exhaustively enumerated: a new `docs/dsx/learnings/`
directory + dated files, `templates/DATA-DICTIONARY.md`, `templates/DISCLOSURE-research.md`,
a plan:pre learnings-search instruction, edits to `dsx-explore-data`/`dsx-narrate`, an alias
table + hook-skip subsection in the operating guide, and optional command shims. Zero edits
to any `dsx/**/*.py` file are required.

**Rationale:** The catalogue generator walks only `dsx/**/*.py` for `report.add(...)`
first-args, so every one of these artifacts is structurally incapable of minting a finding
code — REQ-P14-06 holds by construction, not by discipline.
**Source:** 14-CONTEXT.md

---

### D-02 — Compounding-loop search lives in the framing owner as prompt guidance, not a CLI
The "search dated learnings before framing" behaviour was added as plan:pre prompt guidance
to `dsx-scope-analysis` (the loop-wired plan:pre step that produces `ANALYSIS-SPEC.yaml`),
with a one-line pointer in `fragments/researcher.md`. Learnings live at
`docs/dsx/learnings/YYYY-MM-DD-<slug>.md` with a fixed frontmatter key set (`date, title,
domain, question_type, tags, metrics, phase, source_spec, outcome, supersedes?`).

**Rationale:** `dsx-scope-analysis` already grants Read/Grep/Glob/Bash, so the search needs
no new tool grant and no CLI. A markdown-only `dsx learnings search` subcommand would mint
nothing but adds `dsx/` surface and portability cost for no rigour gain — declined under
rigour > flexibility.
**Source:** 14-CONTEXT.md

---

### D-03 — DATA-DICTIONARY.md is authored by `dsx-explore-data`, roster copied verbatim, written+ungated
`templates/DATA-DICTIONARY.md` mirrors the `templates/EDA.md` pattern. The column roster
(name/dtype/null_rate/unique_count) is copied verbatim from `DATA-PROFILE.yaml`; the
semantics the CSV cannot carry (grain, join keys, per-column meaning, PII) are authored.

**Rationale:** The gate does NOT check the dictionary — even an existence check would add a
`report.add` and mint a code (see D-07). It is an analyst artifact like DATA-PROFILE:
written, ungated, reusing the skill's existing "never invent profile numbers" discipline.
**Source:** 14-CONTEXT.md

---

### D-04 — Research-domain disclosure is additive, opt-in, and gated on the literal `research` value
`dsx-narrate` offers an optional AI-assistance disclosure block only when `dsx.domain ==
research`, read via the documented `gsd-tools.cjs config-get dsx.domain` reader. The default
`auto` never infers it; `marketing_science` and every other value take today's code path with
no new section, no reordering.

**Rationale:** Because `dsx-narrate` is a prompt skill, "marketing default byte-unchanged" is
a structural fact, not a promise — the trigger is the literal value only, so the block can
never become a gate. `templates/DISCLOSURE-research.md` is GUIDE-LLM-derived but explicitly
not a third-party dependency.
**Source:** 14-CONTEXT.md

---

### D-05 — Documented alias convention is primary; host command shims are optional non-load-bearing sugar
CSV-first routing is delivered as a canonical alias table in `docs/operating-guide.md` plus
CSV-first trigger phrases added to each DSX skill's frontmatter `description`. Host-native
`.claude/commands/*.md` shims are permitted only as additive sugar, never the sole path. A
`capability.json` `aliases` key was rejected outright.

**Rationale:** The alias table is portable and `supported:["*"]`-compatible; a
`capability.json aliases` key is not grounded in the installed GSD Core schema, and the
repo's Tool Version Grounding rule forbids writing a key that may silently no-op. Aliases
take the CSV path as an argument, which also makes them the portable substitute for the
D-06 skipped hook.
**Source:** 14-CONTEXT.md

---

### D-06 — REQ-P14-05 resolved as the documented-skip branch (file-drop hook vetoed)
The conditional requirement ("either a file-drop hook runs `dsx profile`, or the operating
guide documents that GSD Core exposes no overlay hooks and the skip is the accepted
satisfaction") was resolved to the documented-skip branch, decided against evidence read
directly from the installed GSD Core, not by preference.

**Rationale:** The portable hook floor (`hook-bus.cjs:28`) has no "a file appeared" event.
`FileChanged` exists but is Claude-Code-family-only and, decisively, the capability's own
`hooks[]` validation does not check `event` against the runtime's hook surface — so a
declared `FileChanged` hook would be written for every runtime and silently no-op on every
non-Claude-Code runtime with nothing in the pipeline catching it, breaching the DSX
capability's `runtimeCompat.supported: ["*"]` contract. Secondary reasons: unverified host
behaviour on a new arbitrary CSV, and collision with REQ-P14-04's rejection of a watched
special folder. The skip weakens no control because `DSX-DQ-001` CRITICAL already forces
profile production on a missing/unreadable `profile_path`. The operating guide states all
four honesty claims verifiably rather than silently narrowing scope, and records a reversal
condition for a future milestone.
**Source:** 14-CONTEXT.md

---

### D-07 — Zero-mint proof reuses Phase-13 machinery plus a new gate-path hermeticity guard
REQ-P14-06 rides the Phase-13 proof exactly (`gen-finding-catalogue.py --check` exit 0 and
`test_finding_catalogue_invariant.py` count==256 AND set-identity vs the Phase-12 fixture),
re-run by the orchestrator after each plan. A new `tests/test_gate_path_hermetic.py` was
added as optional hardening.

**Rationale:** The one real mint trap for a doc/skill-only phase is adding a gate check for
the new artifacts (a DATA-DICTIONARY existence check, a learnings check, a disclosure
heading-scanner) — each would add a `report.add` in `dsx/checks/*` and fail the diff.
Standing rule: new artifacts are written and ungated (EDA.md precedent).
**Source:** 14-CONTEXT.md

---

## Lessons

### Verify against re-run gates, not task-completion counting
The phase verifier mapped each requirement to a re-run gate or a specific read locator
("verified this firing") rather than treating "the plan's tasks were marked done" as
evidence. This is the difference between goal-backward verification and a checklist audit.

**Context:** Applied across all 6 requirements in the verification pass; the full suite
(`sh scripts/check.sh`) was independently re-run rather than trusted from an earlier plan
execution.
**Source:** VERIFICATION.md

---

### Draft prose can accidentally trip its own guard assertion
An early draft of the `dsx-narrate` disclosure step contained the literal string
`dsx/checks/`, which would have tripped the plan's own `! grep dsx/checks/` assertion (meant
to prove no gate-path reference was added). It was caught and reworded to "no gate check
anywhere on the deterministic path" before gating.

**Context:** REQ-P14-03 implementation (14-03), during Task verify re-run by the
orchestrator.
**Source:** 14-03-SUMMARY.md

---

### A bare count is not sufficient to prove a catalogue is unchanged
The set-identity leg of the invariant test (comparing the actual code set against the
Phase-12 fixture, not just `len(rows)`) is what actually catches a mint-one/drop-one swap —
a count-only check would pass silently if one code were added and a different one removed.

**Context:** REQ-P14-06's zero-mint proof (14-05); re-run by the orchestrator after every
Phase-14 plan with `added=[…]`/`removed=[…]` as a hard stop.
**Source:** 14-05-SUMMARY.md

---

## Patterns

### Gate-path hermeticity guard test
A stdlib-only unittest (ast/pathlib/unittest, no third-party import) resolves the gate
modules from the live `dsx.cli.GATE_PROFILES` union, walks each module's import closure to a
fixpoint, and asserts (A) no `pandas`/`scipy`/`numpy`/`csv` reaches the union closure of all
gate roots, and (B) a named module (`dsx/profiler.py`) is absent from a specific check's
closure (`dsx/checks/dq.py`).

**When to use:** Any phase where "the gate path stays deterministic/dependency-free" is a
requirement or an implicit invariant — turns an implicit purity assumption into a standing,
automatically-checked bound instead of a one-time manual grep.
**Source:** 14-05-SUMMARY.md

---

### Documented-skip honesty for a conditional requirement
When a requirement is phrased as a disjunction ("either implement X, or document that the
platform doesn't support X and the skip is accepted"), resolve the branch by reading the
actual installed platform capability (not by preference), and if skipping, state every
supporting claim verifiably in the docs — including the decisive technical reason, the
compensating control that already exists, and a reversal condition for when the platform
gap closes.

**When to use:** Any conditional/optional requirement gated on platform capability that may
or may not exist — prevents "documented skip" from becoming silent scope-narrowing.
**Source:** 14-CONTEXT.md

---

### Write-then-leave-ungated artifact for analyst-facing docs
New analyst-facing artifacts (DATA-DICTIONARY.md, dated learnings files, the research
disclosure block) are written and read by skills but never checked by the deterministic
gate — mirroring the pre-existing `templates/EDA.md` precedent.

**When to use:** Any new markdown/YAML artifact introduced in a phase that must mint zero
finding codes — adding even an existence/schema gate check for the new artifact is the one
guaranteed way to mint a code, since the catalogue generator scans every `report.add(...)`
call under `dsx/**/*.py`.
**Source:** 14-CONTEXT.md

---

### Alias-table + shim pattern for portable command routing
A documented convention (a canonical alias table plus `Triggers:` phrases added to each
skill's frontmatter `description`) is the primary, portable routing mechanism, compatible
with `supported:["*"]`. Host-native command shims (e.g. `.claude/commands/*.md`) are layered
on top only as optional, explicitly non-load-bearing sugar.

**When to use:** Any capability that needs natural-language or slash-style entry points
across multiple host runtimes, where a manifest-level `aliases` key isn't grounded in the
installed platform schema.
**Source:** 14-CONTEXT.md

---

### Set-identity diff over bare count for invariant proofs
Pair a cardinality check (count == N) with a set-identity check against a frozen fixture
snapshot, and re-run both after every plan in a phase that must not mutate the set. Treat
any `added=[…]`/`removed=[…]` as a hard stop even when the count is unchanged.

**When to use:** Any "this phase must not change set S" proof (finding-code catalogues,
vocab enums, allow-lists) where a swap could otherwise hide behind a stable count.
**Source:** 14-05-SUMMARY.md

---

## Surprises

### GSD Core's `hooks[]` validation doesn't check the declared event against the runtime's actual hook surface
Investigating the REQ-P14-05 file-drop-hook option surfaced that a capability manifest could
declare a `FileChanged` hook and have it validated and written into `settings.json` for every
runtime, even though `FileChanged` is Claude-Code-family-only — the validator does not
cross-check the declared event against what the target runtime's hook surface actually
supports. Nothing downstream catches the mismatch; it simply no-ops silently on other
runtimes.

**Impact:** This was the decisive reason REQ-P14-05 was resolved as a documented skip rather
than a hook binding — it would have been a silent, undetected `supported:["*"]` contract
breach shipped with a green gate.
**Source:** 14-CONTEXT.md

---

### A doc/skill-only phase still produced a near-miss self-inflicted gate failure
Despite Phase 14 touching zero `dsx/**/*.py` files, the plan's own textual guard assertion
(`! grep dsx/checks/` on the skill body, proving no gate-path reference was introduced) was
almost tripped by the disclosure step's own draft prose describing what it does *not* do —
the literal string `dsx/checks/` appeared in an explanatory sentence, not in a real
reference.

**Impact:** Caught before gating by re-reading the draft against the exact assertion it had
to survive; no phase-wide consequence, but shows that even a "safe" markdown-only change can
trip a string-matching guard through incidental prose rather than actual scope violation.
**Source:** 14-03-SUMMARY.md
