---
phase: 13
slug: task-playbooks-that-fill-the-spec
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: 2026-08-28
---

# Phase 13 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> **State B run** (no prior SECURITY.md): the 14-threat register was consolidated from the
> `<threat_model>` blocks of all five 13-0x plans (`register_authored_at_plan_time: true`);
> no SUMMARY carried a `## Threat Flags` section (grep-confirmed), so nothing was added
> outside the plan-time register. `asvs_level: 1` + `register_authored_at_plan_time: true` +
> `threats_open: 0` → the workflow's L1 short-circuit applies (no auditor spawn; grep-depth is
> sufficient at Level 1). Every mitigation was **re-gated directly by the orchestrator** with
> real commands (brief §5 — never trusted from a report). Phase 13 is skill-only: markdown
> playbooks + `capability.json` + one Python test + one fixture; there is **no executable
> surface, no untrusted input on any deterministic gate path**, so ASVS L1 injection / auth /
> session vectors are all N/A. The residual STRIDE surface is Tampering — a playbook drifting
> into stating its own numbers, silently editing the gate path, or minting/laundering a code.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| analyst → `ANALYSIS-SPEC.yaml` (playbook prose) | The router playbooks are prose read by an analyst; the spec they produce is adjudicated only by the existing deterministic `dsx` gates. No new automated trust boundary. | analyst-authored spec (YAML) |
| `dsx-scope-analysis` → global GSD configuration | The tier routing must stay **advisory**: the skill prints `pwsh scripts/gsd-tier.ps1 -Tier N` for the operator to run; it must never mutate `workflow.*` / `dsx.enforce` / `mode` itself (D-05). | operator-run helper only |
| catalogue generator output → frozen snapshot | `tests/fixtures/finding-codes-phase12.md` is a byte-copy of the generated catalogue, read only by the invariant test; the test is the assertion, not a product surface. | in-repo artifacts (internal) |

---

## Threat Register

*Consolidated from the five plans' `<threat_model>` blocks; phase-unique IDs assigned, plan of origin in the component column. `block_on = high`, so only OPEN threats at high+ count toward `threats_open`.*

| Threat ID | Category | Component (plan) | Severity | Disposition | Mitigation | Status |
|-----------|----------|------------------|----------|-------------|------------|--------|
| T-13-01 | Tampering | `dsx-cohort`/`dsx-funnel` SKILL.md stating a threshold/correction of its own — parallel-advice drift (13-01) | medium | mitigate | D-02 route-and-cite: name a gate + `DSX-` code, never a bare number. Re-gate: anti-parallel-advice grep on both files → **0** unattributed lines. | closed |
| T-13-02 | Tampering | Accidental edit to the deterministic gate path or a JSON edit minting/loop-wiring a check (13-01) | high | mitigate | D-01/D-08 scope fence: name-append only. Re-gate: `git diff --stat 4e83dd7~1 HEAD -- dsx/ scripts/` → **empty**; catalogue set-identity holds. | closed |
| T-13-03 | Tampering | `dsx-root-cause`/`dsx-segment` stating a threshold/correction method — esp. `dsx-segment` naming a correction (13-02) | medium | mitigate | D-02 route-and-cite to `DSX-SPEC-043` / `DSX-EXP-050..053`. Re-gate: anti-parallel-advice grep on both files → **0** unattributed lines. | closed |
| T-13-04 | Tampering | Accidental gate-path edit (13-02) | high | mitigate | D-01/D-08 scope fence; certified by the 13-05 set-identity diff. Re-gate: zero `dsx/`/`scripts/` edits. | closed |
| T-13-05 | Tampering | `dsx-narrate` adding a heading-scanner narrative gate or a new `DSX-NAR-0xx` shape code (would move the catalogue off 256) (13-03) | high | mitigate | D-04 template-only: the 3-part shape maps onto the existing 5-part structure and cites only existing codes (`DSX-COH-040`, `DSX-CLM-080`, `DSX-NAR-030`); **no code minted**. Re-gate: catalogue set-identity `added=[] removed=[]`, 256. | closed |
| T-13-06 | Tampering | Hypothesis-register edit declaring a NEW schema field instead of routing to existing carriers — parallel-schema drift (13-03) | medium | mitigate | D-03 mapping rule: untested belief → `assumptions[]` (`DSX-COH-030/031`); promoted test → `design.multiplicity.family[]` → `results.tests[]` (`DSX-EXP-050..053`); no new spec field. Re-gate: `test_req02_explore_data_hypothesis_register` green. | closed |
| T-13-07 | Tampering | Accidental gate-path edit (`dsx/checks/narrative.py` or any `dsx/`) (13-03) | high | mitigate | Scope fence: markdown only. Re-gate: zero `dsx/` edits. | closed |
| T-13-08 | Tampering | `dsx-scope-analysis` silently mutating global `workflow.*` / `dsx.enforce` / `mode` as an ungated side effect of scoping (the exact D-05 hazard) | high | mitigate | D-05 advisory boundary: the skill **emits** `pwsh scripts/gsd-tier.ps1 -Tier N` and states the helper is what flips the keys, and only when the operator runs it; it performs no mutation itself. Re-gate: `test_req04_scope_routing_is_advisory_not_mutating` green (no `config set` / `--set`). | closed |
| T-13-09 | Tampering | Executor bullet overstating the `.py` preference as leakage prevention, restating a check rule, or being read as a notebook-blocking gate (13-04) | medium | mitigate | D-06 route-and-cite: name `DSX-REP-040` + the `DSX-CODE` scan, frame the benefit as ordering fidelity NOT leakage, gate stays suffix-neutral. Re-gate: anti-parallel-advice grep on `executor.md` → **0**; `test_req05_executor_prefers_py_entrypoint` green. | closed |
| T-13-10 | Tampering | Accidental gate-path edit (`dsx/cli.py` CHECKS/GATE_PROFILES, `dsx/checks/*`) or minting a code (13-04) | high | mitigate | D-08 scope fence: markdown edits only. Re-gate: zero `dsx/`/`scripts/` edits; catalogue 256. | closed |
| T-13-11 | Tampering | A silently minted/dropped code laundered through a cardinality-preserving mint-one/drop-one swap the count invariant alone passes (13-05) | high | mitigate | D-07 set-identity diff: compare distinct-code SETS (strictly stronger than count), assert `current_set == snapshot_set`. Re-gate: `test_finding_catalogue_invariant` → 2 OK (set-identity + 256). | closed |
| T-13-12 | Tampering | A hand-edited/drifted snapshot masking a real catalogue change — false pass (13-05) | medium | mitigate | D-07: snapshot is a byte-copy of the *generated* catalogue (`--check` exit 0 before copy); CRLF-safe `_ROW_RE` compares distinct codes so formatting noise cannot mask a change. Re-gate: `gen-finding-catalogue.py --check` exit 0. | closed |
| T-13-13 | Tampering | A CRLF checkout breaking the row parse so the diff reads an empty/partial set and passes on a stale read (13-05) | medium | mitigate | Reuse the shipped `\r?\n`-tolerant `_ROW_RE`; the 256-row count cross-check on the same parser fails loudly if it ever reads nothing. Re-gate: count invariant green (256). | closed |
| T-13-SC | Tampering | npm/pip/cargo installs | n/a | accept | No package installs occur in this phase; the diff changes no dependency manifest; new imports are stdlib/internal only. | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on (`high`) count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-13-SC | T-13-SC | Skill-only phase; no dependency manifest changed in the phase diff; no supply-chain surface. Design-time disposition recorded in every plan `<threat_model>` block; not a fresh mitigate→accept. | brief D-01 (standing) | 2026-08-28 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-08-28 | 14 | 14 | 0 | orchestrator direct re-gate (L1 short-circuit; no auditor spawn — skill-only, asvs_level 1) |

**Independent re-gate evidence (orchestrator, brief §5 — real commands, not a report):**
- **Gate-path purity (T-13-02/04/07/10):** `git diff --stat 4e83dd7~1 HEAD -- dsx/ scripts/` → **empty** (no `dsx/` or `scripts/*.py` edit anywhere in the phase). Phase diff touches only `skills/`, `capabilities/dsx/`, `tests/`, `.planning/`.
- **Route-and-cite discipline (T-13-01/03/09):** the plans' anti-parallel-advice grep `grep -hEi '(p ?[<>=]|\balpha\b|α|[0-9]+ ?%|[<>]=? ?0?\.[0-9]|\bbonferroni\b|\bholm\b|\bbenjamini\b|\bfdr\b|\bsidak\b)' <file> | grep -v 'DSX-'` → **0** unattributed lines for `dsx-cohort`, `dsx-funnel`, `dsx-root-cause`, `dsx-segment`, and `executor.md`.
- **Zero mint / set-identity (T-13-05/11/12/13, D-04/D-07):** `python -m unittest tests.test_finding_catalogue_invariant` → **2 OK** (set-identity `current==snapshot`, and exactly 256); `python scripts/gen-finding-catalogue.py --check` → exit **0** ("finding catalogue is current"); distinct `DSX-*` = **256**.
- **D-05 advisory boundary (T-13-08):** `dsx-scope-analysis` emits `pwsh scripts/gsd-tier.ps1 -Tier N` (`:69`) and states the helper is what flips the global keys (`:72`); no `config set` / `--set` command in the skill (`test_req04_scope_routing_is_advisory_not_mutating` green).
- **Citation authenticity:** every `DSX-*` code cited across the eight Phase-13 files exists in `references/finding-codes.md` — **0 dangling** (`test_req01_cited_codes_all_exist_in_catalogue` green; corroborates S1-4's 21/21 hand-check).
- **Full corpus gate** `sh scripts/check.sh` → **all checks passed** (`Ran 1230 tests … OK`, catalogue current at 256, capability manifest conformant — 13 skills, gate contract good/bad/missing, determinism identical). The `DSX-* declared twice` warnings are the pre-existing shipped-tree divergent-declaration set (S0-2) — non-blocking; both gates exit 0.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified (technical) 2026-08-28 — gate **SECURED**, `threats_open: 0`, 14/14 closed by orchestrator re-gate. **Human sign-off granted 2026-08-29 (operator verdict recorded in HUMAN-QUEUE.md, item HQ-9):** the sign-off line above is approved as written, and REQ-P13-01..06's UAT is confirmed. Phase 13 is now both technically verified and human-approved.
