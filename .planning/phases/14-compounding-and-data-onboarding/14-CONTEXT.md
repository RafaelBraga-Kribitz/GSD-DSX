# Phase 14: Compounding and data onboarding — Context

**Gathered:** 2026-08-28 (assumptions mode; headless ceremony — AskUserQuestion gates replaced by an Architect-led 2-persona round per LOOP-BRIEF §4)
**Status:** Ready for planning
**Order:** 2nd of 4 in v2.2 execution order (13 → 14 → 16 → 15)

<domain>
## Phase Boundary

Phase 14 is a **skill / doc / template-only** phase. It steals the Data Science Plugin's
*compounding loop* (search dated learnings before framing) and DAAF's *data-onboarding* skill
(a portable data dictionary, a CSV-first start), and adds a research-domain AI-assistance
disclosure. Its entire product is markdown, YAML and one or two skill edits: a new
`docs/dsx/learnings/` directory + dated files, two `templates/*.md`, a plan:pre search
instruction, edits to `dsx-explore-data`/`dsx-narrate`, a documented alias table, and an
operating-guide subsection. **It mints ZERO new `DSX-*` finding codes and touches nothing on the
deterministic `dsx gate` path.**

Scope anchor (ROADMAP.md §"Phase 14", REQ-P14-01..06):

- REQ-P14-01 — `docs/dsx/learnings/` holds **dated YAML-frontmatter files**; the **plan-pre path
  searches them before framing** (the same compounding loop as the plugin's `/ds:plan`).
- REQ-P14-02 — A **`DATA-DICTIONARY.md`** is produced next to `DATA-PROFILE.yaml` so later
  sessions do not re-guess grain and join keys.
- REQ-P14-03 — When `dsx.domain` is `research`, `dsx-narrate` offers an **optional** AI-assistance
  disclosure block (GUIDE-LLM as a *template*, not a third-party dependency); **marketing-domain
  default unchanged**.
- REQ-P14-04 — **Slash-command aliases** exist for the DSX skills so a CSV-first conversation does
  not require knowing GSD phase names, **without a `data_storage/` special folder**.
- REQ-P14-05 — **Either** a file-drop hook runs `dsx profile`, **or** the operating guide
  documents that GSD Core exposes no overlay hooks and the skip is the accepted satisfaction.
  **(Conditional requirement — the branch is decided in D-06 below, against the installed GSD
  Core, not silently.)**
- REQ-P14-06 — **No new blocking finding codes ship** — same whole-phase scope bound as Phase 13's
  REQ-P13-06.

**Verified baseline (orchestrator re-ran, 2026-08-28):** catalogue is **256 codes**
(`references/finding-codes.md` distinct-`DSX-*` grep = 256); `python scripts/gen-finding-catalogue.py
--check` exits **0** ("finding catalogue is current"); `python -m unittest
tests.test_finding_catalogue_invariant` = **2 tests OK** (count==256 + set-identity vs
`tests/fixtures/finding-codes-phase12.md`). Gate path is stdlib-pure: **no** `pandas`/`scipy`/`numpy`
anywhere in `dsx/`; `import csv` appears **only** in `dsx/profiler.py:9` (imported lazily by
`cmd_profile`, `dsx/cli.py:397`, and never by any check). `capabilities/dsx/capability.json` carries
`"hooks": []` (`:58`) and `"supported": ["*"]` (`:13`). The pre-existing "declared twice" `--check`
warnings (DSX-SPEC-070 / VAL-021 / VAL-060 / CLM-020/021 / COH-030 / PAR-002) are the shipped-tree
noise S0-2 already flagged; `--check` still exits 0 and `len(rows)` is unchanged.

**Not in scope:** any new detection check or `report.add("DSX-…")` under `dsx/`; any change to
`CHECKS`/`GATE_PROFILES` (`dsx/cli.py:64-131`); a **gate check** for the new artifacts (a
DATA-DICTIONARY existence check, a learnings check, or a disclosure heading-scanner all mint a code
— see D-07, the one real mint trap); parsing a CSV inside any check; a file-drop hook binding (D-06);
a `data_storage/` special folder (REQ-P14-04 forbids it). Phase 15 owns new codes and vocabulary;
Phase 16 owns `dsx-reproduce`. These are named in Deferred Ideas.

**No pre-requisite structural repoint.** S1-3 already closed the "ROADMAP repoint" question: GSD's
`init` verbs resolve the phase by its **positional** form (`init <verb> 14`), and `/gsd-plan-phase`
uses `init.plan-phase` which resolves the queued phase without promoting the ROADMAP section. The
expected phase dir by convention is `.planning/phases/14-compounding-and-data-onboarding/`
(`<num>-<slug>`, unpadded), already created this firing.
</domain>

<decisions>
## Implementation Decisions

Every decision below was settled by an **Architect-led 2-persona round** (Architect
`dsx-analysis-architect` = lead, on spec/artifact shape and the operating-guide branch; Auditor
`dsx-ml-integrity-auditor` = adversary, on the zero-mint bound, gate-path purity, marketing-default
safety and the REQ-P14-05 portability veto; both opus/high, concurrent), tie-break **rigour >
reliability > flexibility**. The two personas **converged with no genuine ties**. Decisions are loud
and **vetoable via the daily summary** (LOOP-BRIEF §4); none is a HUMAN-QUEUE escalation because none
mints a D-06 finding code, changes a numbered requirement, or is destructive. Phase 14 adds no code
and no vocabulary member — it mints no irreversible artifact.

### Packaging and the no-new-code footprint

- **D-01 (skill/doc/template-only):** Phase 14's artifacts are, exhaustively: a new
  `docs/dsx/learnings/` directory + dated `*.md` files (D-02); `templates/DATA-DICTIONARY.md` (D-03);
  `templates/DISCLOSURE-research.md` (D-04); a plan:pre learnings-search instruction added to
  `skills/dsx-scope-analysis/SKILL.md` and a one-line pointer in
  `capabilities/dsx/fragments/researcher.md` (D-02); a data-dictionary authoring step in
  `skills/dsx-explore-data/SKILL.md` (D-03); an optional disclosure block in
  `skills/dsx-narrate/SKILL.md` (D-04); an alias table + a "why no file-drop hook" subsection in
  `docs/operating-guide.md` (D-05, D-06); optionally CSV-first `description` triggers on the DSX
  skills and optional `.claude/commands/*.md` shims (D-05). **Zero `dsx/**/*.py` edits are required.**
  The catalogue generator walks only `dsx/**/*.py` for `report.add(...)` first-args
  (`gen-finding-catalogue.py:226-243`), so every one of these artifacts is *structurally incapable*
  of minting a code. REQ-P14-06 holds by construction; D-07 is the closing proof.

### The learnings compounding loop (REQ-P14-01)

- **D-02 (prompt-guidance search in the framing owner; fixed frontmatter schema; no CLI):** The
  "search dated learnings before framing" behaviour is added as **plan:pre prompt guidance** to
  `dsx-scope-analysis` — the only loop-wired plan:pre step (produces `ANALYSIS-SPEC.yaml`, consumes
  `CONTEXT.md`; `capability.json:129-138`) and the framing owner — with a one-line pointer added to
  `fragments/researcher.md` (whose contract already asks "Has this been analysed before?").
  `dsx-scope-analysis` already grants `Read/Grep/Glob/Bash`, so the search needs **no new tool grant
  and no CLI**. A markdown-only `dsx learnings search` subcommand would mint nothing (no `report.add`)
  but adds `dsx/` surface and portability cost for no rigour gain — declined under rigour >
  flexibility. Learnings live at `docs/dsx/learnings/YYYY-MM-DD-<slug>.md` (date in the filename so
  a plain sort is chronological) with a **fixed frontmatter key set** so the agent grep is
  deterministic: `date`, `title`, `domain` (a `dsx.domain` enum value), `question_type` (closed
  vocab), `tags[]`, `metrics[]` (names touched — catches prior metric definitions), `phase`,
  `source_spec`, `outcome` (the one-line compounding payload), `supersedes` (optional). Body follows
  the Phase-13 What / So What / Now What shape. **Producer of the files** (so the directory is not
  born empty) is a light open item for planning — piggyback the existing `gsd-extract-learnings`
  skill or add a `dsx-narrate` close-out emit; the *read* side is all REQ-P14-01 mandates and the
  schema stands either way. Off the gate path.

### The portable data dictionary (REQ-P14-02)

- **D-03 (template authored by `dsx-explore-data`, roster copied from the profile, written+ungated):**
  Ship `templates/DATA-DICTIONARY.md` (mirroring the existing `templates/EDA.md` /
  `templates/CHART-REVIEW.md` pattern); `dsx-explore-data` authors `DATA-DICTIONARY.md` next to
  `DATA-PROFILE.yaml` right after `dsx profile`. The **column roster is copied verbatim** from
  `DATA-PROFILE.yaml` (name / dtype / null_rate / unique_count — deterministic, reusing the skill's
  existing "never invent profile numbers" discipline); the **semantics the CSV does not carry** —
  grain, join keys, per-column meaning, source table, PII — are authored, which is exactly what the
  template forces. Frontmatter: `dataset`, `profile_path: DATA-PROFILE.yaml`, `source_hash` (same
  extract as the profile), `grain` (one row = one …), `primary_key`, `join_keys[]` ({column,
  joins_to, cardinality}), `source`, `timezone`, `owner`. Column table:
  `| column | dtype | semantic_type | null_rate | unique_count | description | source | pii | notes |`
  with `semantic_type` from a small closed set {identifier, foreign_key, timestamp, categorical,
  ordinal, numeric_measure, boolean, free_text, derived}. **The gate does NOT check the dictionary**
  — even an existence check would add a `report.add` and mint a code (D-07). It is an analyst
  artifact like DATA-PROFILE: written, ungated (EDA.md precedent). If planning instead adds an
  off-gate `dsx`-CLI scaffolder, `dsx/profiler.py` must stay imported only by `cmd_profile`, **never**
  by `dsx/checks/dq.py` or any gate module.

### Research-domain AI-assistance disclosure (REQ-P14-03)

- **D-04 (additive, opt-in, gated on an explicit `research` read; marketing byte-unchanged):**
  `dsx-narrate` offers an optional disclosure block **only** when `dsx.domain == research`, read via
  the documented config reader `node ~/.claude/gsd-core/bin/gsd-tools.cjs config-get dsx.domain`
  (`dsx-narrate` already lists `Bash` in `allowed-tools`). The trigger is the **literal `research`
  value only** — the default `auto` never infers it, and `marketing_science` and every other value
  take today's code path with **no new section, no reordering, no reserved whitespace**; because
  `dsx-narrate` is a prompt skill, "marketing default byte-unchanged" is a *structural* fact, not a
  promise. The block is **opt-in even under research** (offer with a skip-with-reason, never impose),
  so it can never become a gate. Template `templates/DISCLOSURE-research.md` is GUIDE-LLM-derived
  (AI-assisted steps / human-reviewed decisions / data handling / reproducibility) and is **not a
  third-party dependency**. **No `DSX-NAR` mint, no heading-scanner gate** — it inherits the exact
  rule the What/So What/Now What layer already declares. Assertion (D-07): a golden check that
  narrate output for `dsx.domain != research` contains no disclosure heading.

### CSV-first slash aliases (REQ-P14-04)

- **D-05 (documented convention primary; host shims optional sugar; no `capability.json aliases`
  key):** The portable, `supported:["*"]`-compatible mechanism is a **documented alias convention** —
  a canonical alias table in `docs/operating-guide.md` plus CSV-first trigger phrases added to each
  DSX skill's frontmatter `description` (e.g. "profile this csv", "explore <file>.csv", "eda") — so
  intent routes to the right skill on any host that reads skill descriptions. Host-native
  `.claude/commands/*.md` shims are permitted **only as optional additive sugar** (Claude-Code-only,
  explicitly non-load-bearing), never the sole path. A `capability.json` `aliases` key is **rejected**
  — it is not grounded in the installed GSD Core schema, and the repo's Tool Version Grounding rule
  forbids writing a key that may silently no-op. Aliases take the **CSV path as an argument**
  (`explore <extract.csv>`), so **no `data_storage/` special folder** is needed — which also makes
  the alias the portable substitute for the D-06 skipped hook. Guardrails (D-07): `grep -rn
  "data_storage" commands/ skills/` empty; no absolute host paths in any shim; no `pandas`/`scipy` in
  any alias file.

### The file-drop hook — REQ-P14-05 branch decision (verify-against-GSD-Core, NOT silent)

- **D-06 (BRANCH = documented skip; `FileChanged` binding vetoed):** The ledger's S2-1 open item —
  "if GSD Core exposes no overlay hooks, the requirement is satisfied by a documented skip, NOT by
  inventing a hook channel; verify against the installed GSD Core and record which branch was taken"
  — is resolved here to the **documented-skip branch**, on evidence read directly from the installed
  GSD Core:
  - GSD Core capability manifests *can* declare `hooks[]`, written into settings.json
    `hooks[event][]` (`capability-lifecycle.cjs:438-501`). Valid events are a **portable floor**
    `{SessionStart, PreToolUse, PostToolUse, Stop, SessionEnd}` (`hook-bus.cjs:28`) plus **extended**
    events. The portable floor contains **no "a file appeared" event**.
  - `FileChanged` exists but is in `VALID_EXTENDED_HOOK_EVENTS` and `CLAUDE_FAMILY_EVENTS`
    (`capability-validator.cjs:728,759`) — **Claude-Code-family only**, gated on the runtime
    descriptor declaring it. GSD Core's *only* wired use is `gsd-config-reload.js` with a fixed
    `matcher: 'config.json'`, hot-reloading an **already-existing** file the user edits mid-session,
    matched **by filename** (`runtime-hooks-surface.cjs:1656-1693`).
  - **Decisive reason (portability contract):** the capability's own `hooks[]` validation does **not**
    check `event` against the runtime's hook surface, so a declared `FileChanged` hook would be
    written for **every** runtime and then **silently no-op on every non-Claude-Code runtime**
    (Gemini, Qwen, Codex, …) with nothing in the pipeline catching it — the exact "config that
    silently no-ops" the repo's Tool Version Grounding rule forbids, and a direct breach of the DSX
    capability's `runtimeCompat.supported: ["*"]` contract.
  - **Secondary reasons:** (b) *unverified host behaviour* — whether Claude Code fires `FileChanged`
    for a **new arbitrary CSV** appearing (matched by a `*.csv`-style pattern) is nowhere verified;
    GSD Core only exercises it on an edited, already-watched `config.json`. The project's rigour bar
    forbids building on an unverified host behaviour. (c) *REQ-P14-04 collision* — a hook that runs
    `dsx profile` "when a CSV shows up" is operationally the watched special folder REQ-P14-04
    explicitly rejects, implemented via a file-watcher instead of a named directory.
  - **The skip weakens no control.** `dsx/checks/dq.py` already fires **`DSX-DQ-001` CRITICAL** when a
    spec declares `data[].assertions` with a missing/unreadable `profile_path`, so the analyst is
    *forced* to produce the profile regardless — automation was convenience, not a guardrail. The
    portable substitute is the D-05 alias / the exact `dsx profile <csv> --out DATA-PROFILE.yaml …`
    command.
  - **Operating-guide honesty requirement (so this is satisfaction, not silent scope-narrowing).**
    `docs/operating-guide.md` must state, verifiably, all four: (1) the portable hook floor exposes no
    file-drop event and GSD Core exposes no capability-declarable file-drop overlay; (2) the only
    file-change surface, `FileChanged`, is Claude-Code-family only, runtime-descriptor-gated,
    filename-matched, used solely for `config.json` hot-reload, and its firing on a new arbitrary CSV
    is unverified; (3) DSX ships `supported:["*"]` and will not ship a hook that works on one runtime
    and no-ops elsewhere; (4) `dsx profile` therefore stays **analyst-invoked**, with the exact
    command. `capabilities/dsx/capability.json` `hooks` stays `[]`.
  - **Reversal condition (recorded for a future milestone):** if GSD Core later exposes a
    runtime-neutral file-change overlay hook, REQ-P14-05 may flip to the hook branch; until then the
    documented skip is the satisfied state.
  - This is a §4 **loud op-decision**, vetoable via the daily summary — **not** a HUMAN-QUEUE
    escalation: the requirement's own disjunction pre-authorises the skip branch, it mints no code,
    rewords no requirement, and is non-destructive.

### Zero-mint + gate-path-purity assertions (REQ-P14-06 → S2-5)

- **D-07 (reuse Phase-13 machinery; close the one mint trap; add a hermeticity guard):** REQ-P14-06
  rides the Phase-13 proof exactly: `gen-finding-catalogue.py --check` exit 0 **and**
  `tests/test_finding_catalogue_invariant.py` (count==256 **and** set-identity vs
  `tests/fixtures/finding-codes-phase12.md` — the set-identity leg catches a mint-one/drop-one swap a
  count alone would pass), re-run by the orchestrator after each Phase-14 plan; any
  `added=[…]`/`removed=[…]` is a hard stop. **The single mint trap** is adding a *gate check* for the
  new artifacts (DATA-DICTIONARY existence, a learnings check, or a disclosure heading-scanner) —
  each would add a `report.add` in `dsx/checks/*` and fail the diff. Standing rule for the planner
  and executor: **new artifacts are written and ungated** (EDA.md precedent); no `dsx/checks/*` edit
  for them. For a pure doc/skill phase, `git diff --stat` on `dsx/` should be **empty**; if a plan
  adds an off-gate CLI scaffolder for D-03, `grep -c "report.add" dsx/cli.py` must remain **0**.
  **Optional hardening (planner's call):** a new `tests/test_gate_path_hermetic.py` asserting no
  `pandas`/`scipy`/`numpy`/`csv` reaches the import closure of any `GATE_PROFILES` module and that
  `dsx.profiler` is not in `dsx.checks.dq`'s closure — a stronger, standing guard than the current
  implicit purity. It is an improvement (not demanded by any single requirement) that directly
  protects REQ-P14-06 and the D-01/D-02 gate-path bound.

### Claude's Discretion (planner)

- Exact learnings frontmatter key set and whether the search instruction sits in the
  `dsx-scope-analysis` skill, `fragments/researcher.md`, or both (D-02).
- The **producer** of `docs/dsx/learnings/*.md` — existing `gsd-extract-learnings` vs a `dsx-narrate`
  close-out emit (D-02); pick one so the directory is not born empty.
- The exact `DATA-DICTIONARY.md` column set and whether an off-gate `dsx`-CLI scaffolder is added
  (if so, it must stay off every gate module's import closure — D-03).
- Whether `.claude/commands/*.md` shims ship at all, and the exact CSV-first `description` trigger
  phrases (D-05).
- Whether `tests/test_gate_path_hermetic.py` ships this phase or is deferred (D-07).

### Folded Todos

None checked at discuss time — resolve `todo.match-phase 14` during planning (S2-2).
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents (researcher, planner) MUST read these before planning or implementing.**

- `.planning/ROADMAP.md` — §"Phase 14" (goal, 6 success criteria, the REQ-P14-05 conditional
  ordering constraint, `:90-115`).
- `.planning/REQUIREMENTS.md` — REQ-P14-01..06 (`:340-345`).
- `brief.md:386` — the v2.2 backlog row scoping the whole set "skill-only — no new blocking codes",
  naming `docs/dsx/learnings/`, `DATA-DICTIONARY.md`, the `dsx.domain==research` disclosure, slash
  aliases, and the "file-drop hook → `dsx profile` (or a documented skip if GSD Core exposes no
  overlay hooks)" disjunction.
- `.planning/research/SURFACE.md` — §3.4/§3.5 design intent for REQ-P14-01/04/05 (incl. "do not
  steal a `data_storage/` special folder").
- `capabilities/dsx/capability.json` — `"skills"` array (`:35-49`, incl. Phase-13 playbooks);
  `"hooks": []` (`:58`) and `"supported": ["*"]` (`:13`); `dsx.domain` enum incl. `research`
  (`:116-121`); the loop-wired `plan:pre` step `dsx-scope-analysis` (`:129-138`) and the plan:pre
  contributions into `fragments/planner.md`/`researcher.md` (`:150-168`).
- `capabilities/dsx/fragments/researcher.md` — the "Has this been analysed before?" framing contract
  (the D-02 pointer target).
- `dsx/cli.py` — `cmd_profile` / `dsx profile --out DATA-PROFILE.yaml` (`:396-416`, `:1078-1081`);
  `GATE_PROFILES` (`:115-131`) — **read-only**; the lazy `profiler` import (`:397`).
- `dsx/checks/dq.py` — reads a pre-written `DATA-PROFILE.yaml` via `loader.load`, **never opens a
  CSV**; fires `DSX-DQ-001` CRITICAL on a missing/unreadable `profile_path` (the D-06 compensating
  control).
- `dsx/profiler.py:9` — the only `import csv` in `dsx/`; imported only by `cmd_profile` (off-gate).
- `skills/dsx-explore-data/SKILL.md` — `dsx profile` invocation (`:832`) and the EDA.md template
  authoring pattern the DATA-DICTIONARY step mirrors (D-03).
- `skills/dsx-narrate/SKILL.md` — the fixed five-section `<structure>`, `Bash` in `allowed-tools`
  (`:9`), and the existing "mints no new narrative code and adds no heading-scanner gate" declaration
  the disclosure block inherits (D-04).
- `skills/dsx-scope-analysis/SKILL.md` — the plan:pre framing owner that gets the learnings-search
  instruction (D-02).
- `templates/EDA.md` (and `templates/CHART-REVIEW.md`) — the template precedent for
  `DATA-DICTIONARY.md` and `DISCLOSURE-research.md`.
- `docs/operating-guide.md` — where the alias table (D-05) and the "why no file-drop hook"
  honesty subsection (D-06) land.
- `scripts/gen-finding-catalogue.py` (`collect` `:226-243`) + `tests/test_finding_catalogue_invariant.py`
  + `tests/fixtures/finding-codes-phase12.md` — the REQ-P14-06 zero-mint proof (D-07).
- GSD Core hook surface (installed): `capability-validator.cjs:728,759` (`VALID_EXTENDED_HOOK_EVENTS`
  / `CLAUDE_FAMILY_EVENTS` incl. `FileChanged`); `capability-lifecycle.cjs:438-501` (how manifest
  `hooks[]` are written into settings.json); `hook-bus.cjs:28` (`PORTABLE_EVENT_FLOOR`);
  `runtime-hooks-surface.cjs:1656-1693` (the config-reload-only `FileChanged` wiring) — the D-06
  evidence.
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **`dsx profile` → `DATA-PROFILE.yaml`** (`dsx/cli.py:396-416`) — the column roster the
  DATA-DICTIONARY copies verbatim (D-03).
- **`templates/EDA.md`** — the write-then-leave-ungated template precedent for both new templates.
- **Phase-13 catalogue-invariant machinery** — `tests/test_finding_catalogue_invariant.py` +
  `tests/fixtures/finding-codes-phase12.md`, reused unchanged as the REQ-P14-06 proof (D-07).
- **`DSX-DQ-001`** (`dsx/checks/dq.py`) — the already-shipped CRITICAL that forces profile
  production, which is why the D-06 hook skip weakens no control.
- **The `gsd-tools config-get` reader** — how `dsx-narrate` reads `dsx.domain` (D-04); `dsx-narrate`
  already grants `Bash`.

### Established Patterns
- **Route-and-cite / write-then-leave-ungated (11.x + Phase-13 house style):** analyst artifacts
  (EDA.md, and now DATA-DICTIONARY.md, learnings files) are *written*, not *gated* — adding a gate
  check for them is the one way this phase mints a code (D-07).
- **Advisory, not mutating (Phase-13 D-05 carried forward):** the learnings search and the
  disclosure block *offer/read*, they never mutate config or force a section.
- **Gate-path purity by construction:** the catalogue generator walks only `dsx/**/*.py`; the gate is
  stdlib-only and reads pre-written artifacts. Every Phase-14 artifact is markdown/YAML/JSON and
  stays out of `dsx/`.
- **Portability contract (`supported:["*"]`):** the decisive constraint behind D-04 (no
  `capability.json aliases` key, host shims only as sugar) and D-06 (no single-host `FileChanged`
  hook).

### Integration Points
- **`docs/dsx/learnings/`** — new directory + dated `*.md` files (D-02).
- **`skills/dsx-scope-analysis/SKILL.md`** + **`capabilities/dsx/fragments/researcher.md`** — the
  plan:pre learnings-search instruction (D-02).
- **`skills/dsx-explore-data/SKILL.md`** + **`templates/DATA-DICTIONARY.md`** — the data-dictionary
  authoring step (D-03).
- **`skills/dsx-narrate/SKILL.md`** + **`templates/DISCLOSURE-research.md`** — the research-domain
  disclosure block (D-04).
- **`docs/operating-guide.md`** — alias table (D-05) + "why no file-drop hook" subsection (D-06);
  DSX skill `description` triggers, optional `.claude/commands/*.md` shims (D-05).
- **`dsx/cli.py:64-131`, `dsx/checks/*`, `capabilities/dsx/capability.json` `hooks`** — **read-only /
  unchanged**; Phase 14 must not edit the gate path or add a hook.
</code_context>

<specifics>
## Specific Ideas

- REQ-P14-05 is the phase's one genuinely decidable fork, and it was decided against the installed
  GSD Core, not by preference: the `FileChanged` event technically exists, but binding to it breaks
  the `supported:["*"]` contract (silent no-op on non-Claude-Code runtimes, uncaught), rests on
  unverified host behaviour, and re-introduces the watched-folder REQ-P14-04 rejects — so the
  documented skip is the rigorous branch, made honest by naming `DSX-DQ-001` as the compensating
  control and stating the four claims in the operating guide (D-06).
- REQ-P14-06's only real hazard is a *gate check for the new artifacts*: the DATA-DICTIONARY,
  learnings and disclosure are all "written, never gated." The set-identity diff (not count alone) is
  the S2-5 proof that no mint-one/drop-one swap slipped through (D-07).
- The disclosure block's "marketing default byte-unchanged" is structural, not a promise: the block
  triggers only on the literal `research` value; `auto` (the default) never infers it (D-04).
</specifics>

<deferred>
## Deferred Ideas

- **A gate check for DATA-DICTIONARY / learnings / the disclosure block** — would mint a `DSX-*`
  code; deferred to a future milestone that deliberately opens the catalogue, if ever wanted (D-03,
  D-07).
- **A real file-drop hook running `dsx profile`** — deferred pending a *runtime-neutral* file-change
  overlay hook in GSD Core; the D-06 reversal condition names the evidence that would promote it.
- **A `dsx learnings search` / `dsx data-dict` CLI subcommand** — not needed for REQ-P14-01/02
  (prompt-guidance + template suffice) and adds portability surface; only if a later phase needs
  deterministic reuse, and always off every gate module's import closure (D-02, D-03).
- **New codes / vocabulary members** — Phase 15 only, under D-05/D-06. A Phase-14 artifact that
  "needs" one is out of scope by REQ-P14-06.
- **`dsx-reproduce`** — Phase 16's skill, not Phase 14.
- **Carried v2.2 seeds:** `SEED-001` (deepen `dsx-explore-data` EDA protocol) and `SEED-002` (grow
  `data-profile` hermetic EDA artifacts) both touch the data-onboarding surface and may inform the
  DATA-DICTIONARY shape (D-03), but are dormant future work, not Phase 14 scope.

### Reviewed Todos (not folded)
None — resolve `todo.match-phase 14` at planning (S2-2).

### D-05 pre-registration note
Phase 14 mints no code and therefore owes **no** D-05 primary-source read. The milestone's only D-05
obligation remains Phase 15's (answered for the CUPED + changing-denominator citations at HQ-8; the
survivorship-bias half stays unshipped in `brief.md` §6.5). Phase 14's end-of-phase security sign-off
and UAT will be batched to HUMAN-QUEUE at S2-5, as Phase 13's were (HQ-9).
</deferred>
</content>
