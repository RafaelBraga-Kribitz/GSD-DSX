---
phase: 11
slug: frequentist-admissibility-adjudicator-dsx-adm
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: 2026-08-23
---

# Phase 11 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| author/agent → repository documentation | A human or agent writes citation text (`brief.md`, `references/test-selection.md`) that later phases and the ontology treat as established fact; no parser validates the claim. | Citation prose, no credential/PII |
| documentation → ontology data | A recommendation in `references/test-selection.md` is copied by hand into `references/families.yaml`'s ranking notes. | Citation text, locator strings |
| installed ontology file → adjudicator | `references/families.yaml` sits on disk beside the package and is read at gate time; write access to the install directory changes what the gate considers admissible. | Family/rule definitions, citations |
| loader path → parsed value | The same bytes are read by two different parsers (PyYAML vs. bundled fallback) depending on installation, and they can measurably disagree on some constructs. | YAML AST |
| spec author (untrusted) → gate / scoping predicate | `validity_frame.estimand.type`, `inference.paradigm`, and `inference.primary_procedure` are analyst-declared, untrusted values that decide whether checks run and which family is selected. | Declared spec fields |
| `dsx/checks/` ↔ `dsx/frame/` | Two packages required to stay independently extractable; this phase is the first with real incentive to cross the boundary in either direction. | Import graph only |
| repository fixtures → regression suite | The committed known-bad/good specs are the corpus every exit-code guarantee is measured against; editing one silently changes what the suite proves. | Test fixtures |
| ontology data → finding text | A `condition`/`strength`/`citation` in `families.yaml` is rendered into a blocking finding an operator reads as a statistical claim. | Rendered finding prose |
| check module → decision trail | `DecisionRecord.escalate` tells a later reader the tool refused rather than decided; a missing flag silently downgrades a refusal to an ordinary choice. | Decision-record fields |
| gate registration → operator outcome | Adding a family to a gate profile changes exit codes for every spec that profile runs against, including specs outside this repository. | Exit codes |
| CLI output contract → downstream consumers | `dsx recommend-test`'s JSON is piped by callers; a changed key set or key order silently breaks them. | CLI stdout JSON |
| repository working tree → release | The build-time citation gate is the last automated point before an uncited claim ships to an operator. | Build/CI exit code |
| import-path mutation → test process | `scripts/gen-finding-catalogue.py` inserts the repo root onto `sys.path`, inside the same process that runs every other test. | `sys.path` state |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-11-01 | Repudiation | `.planning/REQUIREMENTS.md` amendment | medium | mitigate | Amendment note names amended-from value and D-01/D-02 — `REQUIREMENTS.md:135` | closed |
| T-11-02 | Tampering | `brief.md` / `test-selection.md` citations | high | mitigate (residual accepted — see AR-01) | Locators confirmed-or-caveated (`brief.md:442-464`, `test-selection.md:10,26-30`); human-read-against-source step still pending | closed |
| T-11-03 | Information disclosure | none | low | accept (see AR-05) | No credential/PII/endpoint in doc files | closed |
| T-11-04 | Denial of service | none | low | accept (see AR-06) | Documentation edits are not on any execution path | closed |
| T-11-05 | Spoofing | `validity_frame.estimand.type` value | medium | mitigate | Closed-vocabulary exact membership, no fuzzy match — `dsx/spec.py:872-995` | closed |
| T-11-06 | Tampering | `tests/test_known_bad_corpus.py` constants | high | mitigate | No phase-11 commit touched this file; git history confirms it predates all admissibility work | closed |
| T-11-07 | Denial of service | membership loop on `estimand` block | low | accept (see AR-07) | Bounded 9-row tuple iteration, no regex/recursion — `dsx/spec.py:976` | closed |
| T-11-08 | Elevation of privilege | none | low | accept (see AR-08) | No privilege boundary in a local CLI tool | closed |
| T-11-09 | Tampering | `dsx/checks/*` importing `dsx.frame` | high | mitigate | `TestChecksImportBoundary` AST scanner, proven against 3 violating strings — `tests/test_frame_boundary.py:143-188` | closed |
| T-11-10 | Spoofing | declared paradigm value | high | mitigate | Unrecognised/misspelled value widens to True (fails safe) — `dsx/frame/paradigm.py:494-500` | closed |
| T-11-11 | Repudiation | `_NOT_SHIPPED` bookkeeping | medium | mitigate | Entry removed in the same commit that shipped the codes (`f407495`); invariant enforced — `tests/test_dsx.py:3726-3773` | closed |
| T-11-12 | Denial of service | AST scan over `dsx/checks/` | low | accept (see AR-09) | Bounded one-pass walk, test-time only | closed |
| T-11-13 | Tampering | `references/families.yaml` citations | high | mitigate (residual accepted — see AR-02) | Schema requires citation + locator_status — `tests/test_families_yaml.py:157,161,167`; citation-authenticity read still pending | closed |
| T-11-14 | Spoofing | guessed-looking citation locator | high | mitigate (residual accepted — see AR-03) | No-guessed-locator prohibition + named acceptance criteria; fail-safe direction confirmed (MacKinnon/Nielsen/Webb §4 under-marked `unverified`) | closed |
| T-11-15 | Tampering | divergent parse between loader paths | high | mitigate | Dual-parser equality actually executed (PyYAML confirmed installed, not a vacuous skip) — `tests/test_families_yaml.py:92-112` | closed |
| T-11-16 | Repudiation | alias owned by two families in one axis pair | medium | mitigate | Pair-scoped alias-uniqueness assertion over committed file — `tests/test_families_yaml.py:171-183` | closed |
| T-11-17 | Denial of service | pathological nesting in data file | low | accept (see AR-10) | Flat mappings in block sequences; no recursion construct | closed |
| T-11-18 | Tampering | hand-edited `families.yaml` adding uncited family | high | mitigate | `load_ontology()` drops blank-citation entries, records dropped id — `dsx/frame/admissibility.py:200-229` | closed |
| T-11-19 | Spoofing | procedure label resembling a real alias | high | mitigate | Equality-after-`normalize()` only; 1/2-char variants proven `unresolved` — `dsx/frame/admissibility.py:363-390`, `tests/test_frame_admissibility.py:399-409` | closed |
| T-11-20 | Denial of service | absent/unreadable ontology file at gate time | medium | mitigate | Raises `CheckError` naming path, maps to exit 2 — `dsx/frame/admissibility.py:166-198`, `dsx/cli.py:863` | closed |
| T-11-21 | Repudiation | alias owned by two families, one axis pair (runtime) | medium | mitigate | `alias_index` raises `CheckError` naming both ids — `dsx/frame/admissibility.py:266-282` | closed |
| T-11-22 | Tampering | `DSX-ADM-010` detail overstating a hedged ordering | high | mitigate (residual accepted — see AR-04) | Detail interpolated from rule's own `strength` field; only `boschloo_over_fishers_exact` tagged `uniform_domination` — `dsx/frame/admissibility.py:752-756`; wording-vs-source read still pending | closed |
| T-11-23 | Elevation of privilege | refusal reaching exit 2 instead of exit 1 | high | mitigate | No `CheckError` on any refusal path; `DSX-ADM-020` uses ordinary CRITICAL emit — `dsx/frame/admissibility.py:839-849` | closed |
| T-11-24 | Repudiation | refusal recorded as an ordinary choice | high | mitigate | `escalate=True` on every refusal path, asserted for all 3 causes — `dsx/frame/admissibility.py:924`, `tests/test_frame_admissibility.py:876-903` | closed |
| T-11-25 | Spoofing | shipped code absent from published catalogue | medium | mitigate | `PREFIX_GROUPS` row landed in the same commit as first emission (`f407495`) | closed |
| T-11-26 | Denial of service | ranking cost over candidate set | low | accept (see AR-11) | ≤4 candidates × 4 rules, ontology cached — `dsx/frame/admissibility.py:162-164` | closed |
| T-11-27 | Elevation of privilege | misdeclared paradigm suppressing the family | high | mitigate | Widens to True for undeclared/unrecognised; both gate and recommend paths gate on it after CR-01 fix — `dsx/frame/paradigm.py:494-500`, `dsx/cli.py:225,465` | closed |
| T-11-28 | Tampering | corpus expectation maps edited to absorb a regression | high | mitigate | Corpus file untouched by phase-11 work; named regression class green — `tests/test_dsx.py:7681` (14 tests) | closed |
| T-11-29 | Spoofing | `recommend-test` output changing shape for existing callers | high | mitigate | Byte-identity subprocess test, 4 original keys asserted unchanged — `TestAdmissibilityRecommendComposition` | closed |
| T-11-30 | Denial of service | unreadable ontology turning every gate into exit 2 | medium | accept (see AR-12) | Designed behaviour: loud installation-defect message naming path — `dsx/frame/admissibility.py:169-175` | closed |
| T-11-31 | Information disclosure | spec content echoed into `recommend-test` output | low | accept (see AR-13) | Only already-operator-authored ids/tokens/citations/axis values echoed; no path/credential/data leaked | closed |
| T-11-32 | Repudiation | uncited family entry reaching a release | high | mitigate | Build gate fails `--check` with `D-24:` line across all 3 cited blocks — `tests/test_gen_finding_catalogue.py:376-538` | closed |
| T-11-33 | Tampering | allowlist silently not covering the new family | high | mitigate | 3 synthetic-removal tests (citation/structural-criterion/test-marker) — `tests/test_gen_finding_catalogue.py:540-622` | closed |
| T-11-34 | Spoofing | second parser disagreeing with the gate's reader | medium | mitigate | Build script imports no YAML library, reads via shipped loader only — `scripts/gen-finding-catalogue.py:16-20,371` | closed |
| T-11-35 | Tampering | import-path insertion leaking into test process | low | mitigate | Guarded insert inside function, no-duplicate test — `scripts/gen-finding-catalogue.py:368-370` | closed |
| T-11-SC | Tampering | npm/pip/cargo installs (×8 plans) | high | accept (see AR-14) | No dependency manifest exists in this repo; none added across the full phase range | closed |

*Status: open · closed · open — below {block_on} threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-01 | T-11-02 | Structural mitigation verified live; residual human-judgment read of the `brief.md` D-29 locators and `test-selection.md` D-27 row against their real sources has not yet occurred. Tracked as pending items #3–#4 in `11-UAT.md`. No automated citation-verification tooling exists in this repo (confirmed by `gsd-security-auditor`). | Rafael Braga-Kribitz (via `/gsd-secure-phase 11`) | 2026-08-23 |
| AR-02 | T-11-13 | Structural mitigation verified live (`citation`/`locator_status` schema enforced, green); residual human-judgment read of all 14 `families.yaml` citations against real sources has not yet occurred. Tracked as pending item #1 in `11-UAT.md`. | Rafael Braga-Kribitz (via `/gsd-secure-phase 11`) | 2026-08-23 |
| AR-03 | T-11-14 | Shares the same pending human-check as T-11-13 (`11-UAT.md` item #1). Fail-safe direction independently confirmed: MacKinnon/Nielsen/Webb §4 is marked `unverified` in `families.yaml` even though `11-CONTEXT.md` records it as confirmed elsewhere — the file under-claims rather than over-claims. | Rafael Braga-Kribitz (via `/gsd-secure-phase 11`) | 2026-08-23 |
| AR-04 | T-11-22 | Mechanical mitigation verified live (detail interpolates the rule's own `strength` field; only the one uniform-domination rule is tagged as such; behaviour test asserts the hedge language); residual human-judgment wording read against source has not yet occurred. Tracked as pending item #2 in `11-UAT.md` and the manual-verification row in `11-VALIDATION.md`. | Rafael Braga-Kribitz (via `/gsd-secure-phase 11`) | 2026-08-23 |
| AR-05 | T-11-03 | No credential, personal data, or endpoint exists in the documentation files this plan touches. | gsd-planner (declared at plan-authoring time, 11-01-PLAN.md) | 2026-08-22 |
| AR-06 | T-11-04 | Documentation edits are not on any execution path. | gsd-planner (declared at plan-authoring time, 11-01-PLAN.md) | 2026-08-22 |
| AR-07 | T-11-07 | Bounded fixed-size tuple iteration (9 rows), no regex/recursion/unbounded quantifier. | gsd-planner (declared at plan-authoring time, 11-02-PLAN.md) | 2026-08-22 |
| AR-08 | T-11-08 | No privilege boundary exists in a local command-line gate tool. | gsd-planner (declared at plan-authoring time, 11-02-PLAN.md) | 2026-08-22 |
| AR-09 | T-11-12 | Bounded one-pass AST walk over ~20 source files, test time only, never on the gate path. | gsd-planner (declared at plan-authoring time, 11-03-PLAN.md) | 2026-08-22 |
| AR-10 | T-11-17 | Schema is flat mappings inside block sequences; no recursion or self-reference construct exists to exploit. | gsd-planner (declared at plan-authoring time, 11-04-PLAN.md) | 2026-08-22 |
| AR-11 | T-11-26 | Ranking comparator bounded to at most 4 candidates × 4 rules per gate invocation; ontology loaded once and cached. | gsd-planner (declared at plan-authoring time, 11-06-PLAN.md) | 2026-08-22 |
| AR-12 | T-11-30 | Designed behaviour: an unreadable ontology is a loud, correctly-attributed installation defect, not a silently degraded gate. | gsd-planner (declared at plan-authoring time, 11-07-PLAN.md) | 2026-08-22 |
| AR-13 | T-11-31 | Composed `recommend-test` output echoes only family identifiers, assumption tokens, citations, and the two declared axis values — all already authored by the operator. No file path, credential, or data value is echoed. | gsd-planner (declared at plan-authoring time, 11-07-PLAN.md) | 2026-08-22 |
| AR-14 | T-11-SC | No dependency manifest exists anywhere in this repository (no `pyproject.toml`/`setup.py`/`requirements.txt`/`package.json`/`Cargo.toml`), and none was added across the full phase-11 commit range. No package-legitimacy checkpoint applies. | gsd-security-auditor (independently confirmed, 2026-08-23) | 2026-08-23 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-08-23 | 36 | 32 | 4 | gsd-security-auditor (verify pass) |
| 2026-08-23 | 36 | 36 | 0 | Claude (`/gsd-secure-phase 11`) — 4 residual human-judgment items accepted as risk per AR-01–AR-04, all traced to pending `11-UAT.md` reads |

**Process note (non-blocking):** Only `11-08-SUMMARY.md` carries the required `## Threat Flags` section; 11-01 through 11-07 omit it. The auditor ran a compensating check (diffed every phase-11 commit's file set against the threat register) and found no unregistered attack surface — this is a documentation-process gap, not a security gap. Future plans in this project should populate `## Threat Flags` in every SUMMARY.md.

**Related, non-register findings (informational):** `11-REVIEW.md` WR-02 (unreachable `DSX-ADM-010` counterfactual gap on a hypothetical two-hop domination chain) and WR-04 (dead `Resolution.detail`/`outside_axes` fields) are tracked as unfixed follow-ups but map to no threat in this register — they are quality/maintenance findings, not security gaps, per the auditor's independent read.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-08-23
