---
phase: 14
slug: compounding-and-data-onboarding
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: 2026-08-28
---

# Phase 14 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> **State B run** (no prior SECURITY.md): the 16-entry register was consolidated from the
> `<threat_model>` blocks of all five 14-0x plans (`register_authored_at_plan_time: true`);
> no SUMMARY carried a `## Threat Flags` section (grep-confirmed), so nothing was added
> outside the plan-time register. `asvs_level: 1` (not set in config → the secure-phase
> default floor) + `register_authored_at_plan_time: true` + `threats_open: 0` → the
> workflow's L1 short-circuit applies (no auditor spawn; grep-depth is sufficient at
> Level 1). Every mitigation was **re-gated directly by the orchestrator** with real
> commands (brief §5 — never trusted from a report). Phase 14 is a doc/skill/template
> phase: markdown playbooks/templates + one dated exemplar + one stdlib-only test; there
> is **no executable surface and no untrusted input on any deterministic gate path**, so
> ASVS L1 injection / auth / session vectors are all N/A. The residual STRIDE surface is
> Tampering — an artifact drifting into a gate check (minting a code), a data library
> creeping into the gate closure, the disclosure block leaking into the non-research
> path, or a single-runtime file-drop hook being bound against the `supported:["*"]`
> contract.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| analyst artifacts → `dsx` gate path | The learnings files, `DATA-DICTIONARY.md`, and the research disclosure block are all **written and read, never gated** (D-07). Adding a check that opens any of them would mint a code — explicitly out of scope. No new automated trust boundary. | in-repo markdown (internal) |
| `dsx-narrate` → `dsx.domain` config read | The disclosure step reads a **closed enum** via the documented `gsd-tools config-get dsx.domain`; the read only selects whether to *offer* the block. Guarded on the literal `research` value; `auto` never infers it (D-04). | operator config (closed enum) |
| host router → DSX skill (CSV-first alias) | The alias table + `description` triggers route intent on any description-reading host; the `.claude/commands` shims add Claude-Code-only convenience. No config is mutated and no `capability.json` `hooks`/`aliases` key is written (D-05/D-06). | analyst intent (no config write) |
| new CSV → `dsx profile` | Analyst-invoked, not hook-driven; the CSV is an **argument**, so there is no watched `data_storage/` folder. `DSX-DQ-001` CRITICAL is the compensating control that forces profile production regardless (D-06). | analyst-supplied path (argument) |

---

## Threat Register

*Consolidated from the five plans' `<threat_model>` blocks; phase-unique IDs assigned by the
plan authors, plan of origin in the component column. `block_on = high`, so only OPEN threats at
high+ count toward `threats_open`.*

| Threat ID | Category | Component (plan) | Severity | Disposition | Mitigation | Status |
|-----------|----------|------------------|----------|-------------|------------|--------|
| T-14-01 | Tampering | A gate check added for the learnings directory (existence/schema scan) → a `report.add` in `dsx/checks/*` minting a code (14-01) | high | mitigate | D-07 write-then-ungated: learnings files are written+read, never gated. Re-gate: `git diff --stat 2236bb4..720ba10 -- dsx/ scripts/` **empty**; `grep -c report.add dsx/cli.py` **0**; set-identity holds. | closed |
| T-14-02 | Spoofing | The search grepping a key set the files do not carry, silently missing prior results (14-01) | medium | mitigate | D-02 single-schema link: `README.md` fixes the closed key set; the dated exemplar carries every key; `dsx-scope-analysis` cites the README as authority. Re-gate: `test_req01_*` green (README + exemplar present, producer named). | closed |
| T-14-03 | Tampering | A new tool grant or a `dsx` CLI subcommand added to power the search, widening the surface (14-01) | medium | mitigate | D-02: the search reuses already-granted Grep/Glob/Read; no `dsx/` path is shelled. Re-gate: `allowed-tools` unchanged (14-01 SUMMARY, orchestrator-confirmed); no new CLI subcommand. | closed |
| T-14-04 | Tampering | A `DATA-DICTIONARY` existence/schema gate check added under `dsx/checks/*`, minting a code (14-02) | high | mitigate | D-07 write-then-ungated: the dictionary is an ungated analyst artifact (EDA.md precedent). Re-gate: zero `dsx/` edits; set-identity `added=[] removed=[]`, 256. | closed |
| T-14-05 | Tampering | The authoring step recomputing the roster instead of copying it, producing numbers that disagree with `DATA-PROFILE.yaml` (14-02) | medium | mitigate | D-03 copy-verbatim: `templates/DATA-DICTIONARY.md` states the roster is **copied verbatim** under the "never invent profile numbers" rule. Re-gate: `test_req02_data_dictionary_template_copies_profile` green ("verbatim" + closed `semantic_type` set present). | closed |
| T-14-06 | Tampering | A CSV opened inside a check, or a gate-path import added, to populate the dictionary (14-02) | medium | mitigate | D-03: the dictionary is authored by the prompt skill from the pre-written profile; no `dsx/` path in files_modified; no new gate module/import. Re-gate: `test_gate_path_hermetic` **2 OK** (no `csv`/pandas/scipy/numpy in the gate closure). | closed |
| T-14-07 | Tampering | A disclosure heading-scanner gate or a `DSX-NAR` mint added to enforce the block, minting a code (14-03) | high | mitigate | D-04/D-07: the block inherits the existing no-new-code/no-heading-scanner rule; opt-in, so it can never become a gate. Re-gate: zero `dsx/` edits; set-identity + `--check` exit 0. | closed |
| T-14-08 | Tampering | The block leaking into the marketing/`auto` path (a reorder or an always-on section), changing today's non-research narrative (14-03) | high | mitigate | D-04 structural guard: the step is wrapped in an explicit `dsx.domain == research` **literal** check; the five `<structure>` sections are not reordered. Re-gate: `test_req03_narrate_disclosure_guarded_on_literal_research` green (`config-get dsx.domain`, literal `research`, opt-in/skip). | closed |
| T-14-09 | Spoofing | Reading `dsx.domain` via an ad-hoc/undocumented path, or inferring `research` from `auto` (14-03) | medium | mitigate | D-04: the read uses the documented `gsd-tools config-get dsx.domain`; the trigger is the literal `research` value only. Re-gate: the skill's disclosure step cites `config-get dsx.domain` and guards on `dsx.domain == research` (`skills/dsx-narrate/SKILL.md:47-59`). | closed |
| T-14-10 | Tampering | A Phase-14 artifact silently minting a code via a gate check (dictionary/learnings/disclosure heading-scanner) (14-05) | high | mitigate | D-07: `gen-finding-catalogue --check` + the two-leg invariant (count==256 AND set-identity) name any added/removed code. Re-gate: invariant **2 OK**; `--check` **exit 0**; distinct `DSX-*` = **256**. | closed |
| T-14-11 | Tampering | A data library (pandas/scipy/numpy) or the CSV-opening profiler creeping into a `GATE_PROFILES` module's import closure (14-05) | medium | mitigate | `tests/test_gate_path_hermetic.py` walks the closure of every gate module and asserts the forbidden imports and `dsx.profiler` are absent. Re-gate: `test_gate_path_hermetic` **2 OK**. | closed |
| T-14-12 | Tampering | An accidental edit to `dsx/cli.py` CHECKS/GATE_PROFILES or `dsx/checks/*` during the phase (14-05) | high | mitigate | Scope fence: files_modified is markdown/template/test only. Re-gate: `git status --porcelain -- dsx/` **empty** over the phase; `grep -c report.add dsx/cli.py` **0**. | closed |
| T-14-13 | Tampering | A `FileChanged` hook bound in `capability.json` that silently no-ops on non-Claude-Code runtimes (breaking `supported:["*"]`) (14-04) | high | mitigate | D-06 documented-skip: **no hook bound**; `capability.json` not in files_modified; `hooks` stays `[]`; the operating guide states the four claims and names `DSX-DQ-001` as compensating control. Re-gate: `hooks == []`, `runtimeCompat.supported == ["*"]`; manifest diff empty. | closed |
| T-14-14 | Tampering | A `capability.json` `aliases` key written against an unverified schema, silently no-opping (14-04) | medium | mitigate | D-05: the alias convention is documented (portable) and carried in skill descriptions; no `capability.json` edit; Tool Version Grounding honoured. Re-gate: no `aliases` key in the manifest (`test_req06` green). | closed |
| T-14-15 | Information Disclosure | An absolute host path or a `data_storage/` folder leaking into a shim or the guide, coupling the convention to one machine (14-04) | medium | mitigate | D-05 guardrails: the CSV is an argument (no `data_storage/`); the guide only documents the folder's **absence** (exempt by the 14-04 verify). Re-gate: `data_storage` **0** hits across the 13 skills + the two shims; shims carry no absolute path (14-04 Task 3 verify). | closed |
| T-14-SC | Tampering | npm/pip/cargo installs | n/a | accept | No package installs occur in this phase; the diff changes no dependency manifest; the one new test is stdlib-only. | closed |

*Status: open · closed — 16 entries, 15 threats + 1 supply-chain accept; 7 at high severity, all closed.*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on (`high`) count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-14-SC | T-14-SC | Doc/skill/template phase; no dependency manifest changed in the phase diff; no supply-chain surface. Design-time disposition recorded in every plan `<threat_model>` block; not a fresh mitigate→accept. | brief D-01 (standing) | 2026-08-28 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-08-28 | 16 | 16 | 0 | orchestrator direct re-gate (L1 short-circuit; no auditor spawn — doc/skill/template phase, asvs_level 1) |

**Independent re-gate evidence (orchestrator, brief §5 — real commands, not a report):**
- **Gate-path purity (T-14-01/04/07/10/12):** `git diff --stat 2236bb4..720ba10 -- dsx/ scripts/` → **empty** over the five feature commits (38801a0, 6ddee4c, 5e54297, 4d418b9, 720ba10); `git diff --stat 2236bb4..720ba10 -- capabilities/dsx/capability.json` → **empty** (the manifest is untouched; only the prompt fragment `capabilities/dsx/fragments/researcher.md` changed — same class as 13-04's `executor.md`). `grep -c report.add dsx/cli.py` → **0**.
- **Zero mint / set-identity (T-14-10, D-07):** `python -m unittest tests.test_finding_catalogue_invariant` → **2 OK** (set-identity `current==snapshot` AND exactly 256); `python scripts/gen-finding-catalogue.py --check` → **exit 0** ("finding catalogue is current"). The `DSX-CLM/COH/PAR/SPEC/VAL declared twice` lines are the pre-existing shipped-tree divergent-declaration noise (S0-2) — non-blocking; exit stays 0.
- **Gate-path hermeticity (T-14-06/11):** `python -m unittest tests.test_gate_path_hermetic` → **2 OK** (no pandas/scipy/numpy/csv in the union closure of all gate roots; `dsx/profiler.py` absent from `dsx/checks/dq.py`'s closure).
- **Documented-skip honesty (T-14-13/14, D-06):** `capabilities/dsx/capability.json` `hooks == []`, no `aliases` key, `runtimeCompat.supported == ["*"]` (Python-parsed). The operating guide's "Why there is no file-drop hook" subsection states all four claims and names `DSX-DQ-001` CRITICAL as the compensating control.
- **CSV-first alias discipline (T-14-04/15, D-05):** every DSX skill carries a `Triggers:` clause — **13/13** (`skills/dsx-*/SKILL.md`); `data_storage` → **0** hits across the 13 skills and the two `.claude/commands` shims (the guide is exempt: it documents the folder's *absence*).
- **Disclosure guard (T-14-08/09, D-04):** `dsx-narrate` reads `dsx.domain` via the documented `config-get` and guards the block on the literal `research` value (`skills/dsx-narrate/SKILL.md:47-59`); `auto`/`marketing_science` take today's path byte-unchanged by construction.
- **Citation authenticity:** the only new cited code, `DSX-DQ-001`, exists in `references/finding-codes.md` — **0 dangling**.
- **Full corpus gate** `sh scripts/check.sh` → **all checks passed** (`Ran 1243 tests … OK`, catalogue current at 256, capability manifest conformant — 13 skills, gate contract good/bad/missing, determinism identical). The `declared twice` warnings are the pre-existing S0-2 noise — both gates exit 0.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified (technical) 2026-08-28 — gate **SECURED**, `threats_open: 0`, 16/16 closed by orchestrator re-gate. **Human sign-off is a D-05/§4-category-4 operator item and is NOT yet granted** — queued to `HUMAN-QUEUE.md` (HQ-10) as the batched Phase 14 end-of-phase security + UAT round. Per brief §4 this is non-blocking until close-out (S5-2); the technical gate for ledger unit S2-5 is met.
