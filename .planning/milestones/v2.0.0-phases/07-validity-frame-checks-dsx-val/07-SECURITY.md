---
phase: 7
slug: validity-frame-checks-dsx-val
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: 2026-08-14
---

# Phase 7 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

Register origin: **authored at plan time** — all eight `07-0N-PLAN.md` files carry a parseable
`<threat_model>` block. This file consolidates them into one register (union of components,
maximum severity where an ID appears in more than one plan) and records the verification pass.

Blocking severity: `high`. ASVS level 1.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| analysis-spec file to gate process | Author-controlled free text and author-controlled document shape reach every helper in `dsx/frame/val.py`. The spec is structurally validated before the frame checks run, but a wrong-typed sub-block still arrives here. | Untrusted YAML — free text, arbitrary Python types after parse |
| gate process to rendered report | Author-controlled strings are echoed into finding `detail` and `remedy` text that a reader sees. | Author free text, `!r`-formatted |
| shipped docstring to reader | A citation in a docstring is read as verified fact by anyone auditing the check. | Bibliographic claims |
| planning prose to the project's citation anchor | A locator crosses from a research document into `brief.md` section 7, which every later docstring is written against. | Citation locators |
| research record to shipped citation | A claim crosses from `07-DISCUSSION-LOG.md` into a string that ships in the package and into runtime decision records. | Confirmed-vs-unconfirmed bibliographic assertions |
| project-defined partition to reader | A project-assembled vocabulary split (constraint-source partition, missingness pairing table) crosses into a docstring a reader may take as published. | Project judgement presented as reference material |
| corpus allow-list to future maintainer | An entry in `_INCIDENTAL_GAP_CODES` tells a future reader that a blocking finding is expected and benign. | Suppression semantics |
| test assertion to future maintainer | Narrowing an assertion tells every later reader that the narrowed case is expected. | Guarantee scope |
| fix to its own test | A task judged by a test written before it — if one commit could edit both, the judgement is worthless. | Commit-boundary integrity |
| author-reachable value to gate outcome | A field an author can set to a benign-looking value could become a route past a check if the check reads it. | Potential exemption channel |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-7-01 | Denial of Service | every sub-block read in `dsx/frame/val.py` | medium | mitigate | `isinstance(..., dict)` guard on all 7 sub-blocks in both the record path (`dsx/frame/val.py:218,232,271,352,395,444,478,532`) and the check path (`:588,633,702,779,857,940,1034,1109,1203`); `known_exclusions` routes through `is_blank()` (`dsx/spec.py:369-376`). Auditor fuzzed 7 sub-blocks × 12 bad types, every inner field × 12 bad types, and a malformed `design` block — 0 exceptions | closed |
| T-7-02 | Information disclosure | finding `detail` and `remedy` text | low | accept | Local command-line report, no network sink; `!r` repr formatting applied to echoed values. See ACC-7-01 | closed |
| T-7-03 | Denial of Service | `_FALSIFIER_NUMBER_RE`, `_PLACEHOLDER_RE` | medium | mitigate | Bounded, non-nested, linear patterns (`dsx/spec.py:426,433`); 20,000-character timing test `tests/test_dsx.py:789-798` re-run by the auditor, passes under 1s | closed |
| T-7-04 | Spoofing | the illustrative design-effect number in `DSX-VAL-020` detail | high | mitigate | Both disclosures ship together in the emitted detail (`dsx/frame/val.py:730-733`); test asserts the illustration wording, not merely the number (`tests/test_frame_val.py:218-225`). **Weaker than declared** — see Residual R1 | closed (weakened) |
| T-7-05 | Repudiation | decision records at all eight judgment points | medium | mitigate | 8 `DecisionRecord` sites (`dsx/frame/val.py:253,289,329,371,421,456,508,541`); identification rule text distinguishes VAL-040 from VAL-041 (`:426-433`); family-wide shape assertion `tests/test_frame_val.py:1270`. A spec tripping all 8 produced 8 records, 0 shape violations | closed |
| T-7-06 | Tampering | build plumbing — silent catalogue drop, disjointness guarantee | high | mitigate | Prefix group `scripts/gen-finding-catalogue.py:45-48`; allow-list `:65`; family heading `references/finding-codes.md:358`; every-emitted-code assertion `tests/test_frame_val.py:1445`; disjointness by construction `:992-1029`; `design.py` content-hash pin `:1031`; `--check` exits 0. See Flag F1 | closed |
| T-7-07 | Spoofing | shipped docstrings and comments carrying citations | high | mitigate | UNVERIFIED / project-defined labels present at every named site: `dsx/mathx.py:466-468`; `dsx/spec.py:219-228` (incl. Conley non-citation, enforced by `scripts/check_brief_refs.py:45`); estimand `dsx/frame/val.py:571-579`; constraint-source in both constant comment `:133-141` and docstring `:927-932`; missingness table in both `:167-175` and `:1085-1094`; post-mortem source section `examples/known-bad/weak-identification-mmm-POSTMORTEM.md:55-87`. See Residual R2 and Human Judgement | closed |
| T-7-08 | Tampering | `.planning/research/FEATURES.md` worked example | medium | mitigate | `FEATURES.md:54-63` carries "Correction (decision D-10, 2026-08-12)"; the retired `3.45` survives only inside the retirement note; the worked example is now 1.576/Cochrane | closed |
| T-7-09 | Repudiation | research file ↔ shipped docstring correspondence | low | mitigate | `FEATURES.md:49-51` (ICC 0.02, m 29.8 → 1.576, Cochrane §23.1.4/23.1.4.1) matches `dsx/mathx.py:469-470` word for word | closed |
| T-7-10 | Elevation of privilege | the import boundary | medium | mitigate | `tests/test_frame_boundary.py:93` real-tree glob scan plus `:104` scanner self-test (fires on 3 violating forms, permits 2 controls); deny list is a single constant `_FORBIDDEN_PACKAGE` with no exception list (`:35`) | closed |
| T-7-11 | Tampering | fixture repair used to hide a check defect | medium | mitigate | Commit `8da2a8d` changed the fixture's own declaration to be internally coherent with its already-declared `observation`/`assignment`; no check trigger narrowed; rationale recorded in the fixture header | closed |
| T-7-12 | Tampering | the corpus incidental-gap allow-list | high | mitigate | All 9 `_INCIDENTAL_GAP_CODES` entries carry inline cause comments (`tests/test_known_bad_corpus.py:61-77`); `DSX-VAL-040` is in `_TARGET_DEFECT_CODES` (`:135`), never the allow-list; anti-laundering test at `:511`. See Flag F3 | closed |
| T-7-13 | Repudiation | template repair hiding a real trigger | medium | mitigate | Commit `917fa14`: `templates/ANALYSIS-SPEC.yaml` `strength` weak→strong with `constraint_source: none` **unchanged**; check not weakened; template still fails ship (`tests/test_dsx.py:1435-1440` asserts exit 1) | closed |
| T-7-14 | Elevation of privilege | author-reachable exemption — the missingness `rate` field | high | mitigate | `rate` appears in `dsx/frame/val.py` only in prose (`:519`, `:1104`), never read. Proven mechanically: for both MAR and MNAR, code/severity/detail/remedy/where are identical across 12 rate values (absent, 0, 0.0, 0.5, 42, "not-a-number", None, dict, list, True, 1e9, -5). Declared 4-way test `tests/test_frame_val.py:872` | closed |
| T-7-15 | Tampering | `_EXPECTED_VAL_CODES` drifting into a description of current behaviour | medium | mitigate | Measured-on date and measuring command at `tests/test_frame_val.py:1189-1194`, `:1202-1215`; anti-guessing text at `:1192-1194`. Glob guard independently proven to fire — auditor dropped an undocumented fixture into `examples/known-bad/` in a throwaway worktree and the discovery test failed loudly | closed |
| T-7-16 | Tampering | narrowing the corpus's positive gate assertion | high | mitigate | Named exception `_TARGET_DEFECT_CODES["weak-identification-mmm"]` (`tests/test_known_bad_corpus.py:135`); positive assertion (exit 1 **and** the named code among CRITICAL findings) via `_classify_target_defect` at `:441`; glob discovery kept at `:327`; execute-gate half intact (no `execute` key ⇒ exit 0 demanded) plus `tests/test_frame_val.py:1322` | closed |
| T-7-17 | Repudiation | requirement completion claimed before its gate passed | medium | mitigate | 07-07 Task 2 = commit `a8121a1`, touches exactly one file (`tests/test_frame_val.py`, +132/-0); no REQUIREMENTS.md edit, no checkbox changed | closed |
| T-7-18 | Spoofing | the reworded Kish disclosure (G-07-4) | high | mitigate | Confirmed set in `07-DISCUSSION-LOG.md:101-103` (§8.2 p.258 for the Deff definition, pp.161-162 for ICC, no section number for the formula) matches all four shipped passages — `dsx/frame/val.py:78-86`, `:672-678`, `dsx/mathx.py:459-468`, `brief.md:461-464`. The set does not grow | closed |
| T-7-19 | Tampering | making the invariant pass by weakening it | high | mitigate | `adc1ad2` (test) = 1 file, +160/-0. `cb074c4` (fix) = exactly 3 files — `brief.md`, `dsx/frame/val.py`, `dsx/mathx.py` — and does not touch the test file. Exactly as declared | closed |
| T-7-20 | Repudiation | a fix with no test that would have caught it | high | mitigate | Red gate reproduced independently: `adc1ad2` checked out into a temp worktree, `TestKishCitationCoherence` → `Ran 3 tests … FAILED (failures=3)`. All three assertions fail, not one | closed |
| T-7-21 | Tampering | the pages-only detector narrowed to one exact string | high | mitigate | `tests/test_frame_val.py:1483-1492` — exactly three patterns, each with a comment naming its derivation; wording-independent cross-file assertion at `:1572` compares parsed locator sets, not text | closed |
| T-7-22 | Tampering | the citation ledger drifting from the code | medium | mitigate | `cb074c4` corrects `brief.md` in the same commit as the code; third assertion `tests/test_frame_val.py:1602`; `scripts/check_brief_refs.py` exits 0 (14 checks, "unverified" ≥ 3 → found 4) | closed |
| T-7-23 | Tampering | D-05 enforcement lapsing through a docstring edit | high | mitigate | `_check_unit_triad` keeps `Citation:` (`dsx/frame/val.py:672`) and `Structural criterion:` (`:688`); `design_effect` keeps `Citation:` (`dsx/mathx.py:459`) and `Reference value:` (`:469`); `--check` exits 0; `test_real_tree_check_d05_is_empty` passes | closed |
| T-7-24 | Tampering | collateral edit to the pinned check module | medium | mitigate | `git status --porcelain dsx/checks/design.py` → empty; last touched at `86f449f` (v1.4.0, pre-Phase-7); SHA-256 pin test `tests/test_frame_val.py:1031` passes | closed |
| T-7-SC | Tampering | package-manager installs | low | accept | Zero-dependency claim verified: no `requirements.txt`, `pyproject.toml`, `setup.py`, `package.json`, `Pipfile` or `setup.cfg` anywhere in the repo; all `dsx/` imports relative or stdlib; PyYAML is a pre-existing optional import (`dsx/loader.py:20-23`) untouched by Phase 7. `07-RESEARCH.md:1055-1063` records the audit. See ACC-7-02 | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| ACC-7-01 | T-7-02 | Author-controlled spec values are echoed into finding `detail` and `remedy`. Accepted because `dsx` writes a local command-line report with no network sink, and echoed values are `!r`-formatted per the repository's existing idiom. **Note:** the plan-time rationale claimed the echoed values are closed-vocabulary members; that is not true for `DSX-VAL-020`, `DSX-VAL-021`, `DSX-VAL-050` and `DSX-VAL-070`, which echo author-controlled free text (`observation!r`, `assignment!r`, `known_exclusions!r`, `construct!r`). The acceptance rests on the local-report ground alone, which is sufficient. Revisit if any `dsx` output ever becomes a network response. | gsd-secure-phase (plan-time disposition, verified by gsd-security-auditor) | 2026-08-14 |
| ACC-7-02 | T-7-SC | Supply-chain risk from package-manager installs. Accepted because Phase 7 adds zero external dependencies and the repository declares no dependency manifest at all. No legitimacy checkpoint applies. Revisit the moment a manifest is introduced. | gsd-secure-phase (plan-time disposition, verified by gsd-security-auditor) | 2026-08-14 |

*Accepted risks do not resurface in future audit runs.*

---

## Residuals and Flags

Non-blocking. None is an open threat at or above `high`; each is recorded so it is not rediscovered as a surprise.

**R1 — T-7-04 shipped as two sentences, not one, and half of it is untested.**
The register required the "fixed illustration" and "no field to compute one from" disclosures in the
same sentence. They ship as two adjacent sentences inside one emitted `detail` string
(`dsx/frame/val.py:730-733`), so the reader-facing protection is intact. But
`tests/test_frame_val.py:224-225` asserts only `"1.576" in detail` and `"illustrat" in detail.lower()` —
the second clause could be deleted with a green build.
*Smallest fix:* add `self.assertIn("no cluster-size or intraclass-correlation field", detail)`.

**R2 — T-7-07's standing guard is thinner than its content.**
The disclosure text is present at every named site, but no test greps for the disclosure wording.
`--check` and `tests/test_frame_val.py:1418` enforce only that a `Citation:` line and a
`Reference value:`/`Structural criterion:` line exist. The "project-defined", "not a printed table"
and UNVERIFIED sentences could be deleted with a green build. The plans specified these as
execution-time acceptance criteria rather than standing tests, so the mitigation was delivered as
written.
*Smallest hardening:* assert `"project-defined"` in `_IDENTIFICATION_CITATION` and
`"not a printed table"` in the missingness comment.

**F1 — the catalogue collapses multi-declaration codes with a warning-only, exit-0 build.**
`scripts/gen-finding-catalogue.py --check` exits 0 but warns that `DSX-VAL-021` and `DSX-VAL-060`
are "declared twice with different text". Investigated in full and judged **not** an unmitigated
instance of T-7-06 or T-7-23:
- Both Phase 7 duplicates sit inside a single function each — `DSX-VAL-021` at `dsx/frame/val.py:793`
  and `:816` (both in `_check_unit_drift`), `DSX-VAL-060` at `:1155` and `:1171` (both in
  `_check_missingness`) — so the last-wins `_resolve_docstrings` path (`:238`) has nothing to lose.
- Every declared T-7-06 mitigation is present and passing; none promised per-declaration fidelity.
- The behaviour pre-dates Phase 7 (present at `bc42bfe^`); `DSX-COH-030` has the identical
  CRITICAL/HIGH strict-mode split and `DSX-SPEC-070` warns three times.
- Gating is unaffected — `dsx/cli.py:244` compares `finding.severity` at runtime; the catalogue is
  documentation and is never consulted by the gate.

*Real residual:* `collect()` dedupes last-wins (`scripts/gen-finding-catalogue.py:159-164`), so
`references/finding-codes.md:372` publishes `DSX-VAL-060 | CRITICAL` and the HIGH/MAR variant is
invisible. A reader concludes any VAL-060 blocks at plan; the MAR variant does not.
*Smallest fix:* have `collect()` keep every distinct `(code, severity, title)` row, or promote the
warning to a non-zero exit. This is a generator-level change affecting five codes repo-wide, three
of them outside Phase 7.

**F2 — `_resolve_docstrings` last-wins D-05 hole** (`scripts/gen-finding-catalogue.py:238`).
Latent, not exploitable for any Phase 7 code. A future code emitted from two *different* functions
would have only the last function's docstring checked. `tests/test_frame_val.py:1418` independently
covers every finding-emitting function in `val.py` and is strictly stronger than the script.

**F3 — T-7-12's "the test stays unchanged" is literally false at HEAD.**
Phase 8 (`b03fe0a`, D-15) rewrote `test_incidental_allowlist_names_no_slugs_own_target_code` from
family-prefix scoping to per-fixture/per-point exact-code scoping. The guarantee Phase 7 needed is
intact and arguably sharper, but the new form is more permissive in one dimension: `DSX-VAL-041` may
legitimately sit in `_INCIDENTAL_GAP_CODES` even though `DSX-VAL-040` is a target — a documented,
deliberate trade, since a family prefix cannot express multiple codes once `DSX-INT-*` ships four.
The change belongs to Phase 8, not Phase 7.

---

## Human Judgement Required

Mechanical verification cannot reach these. They are recorded as owed, not as closed.

1. **Bibliographic accuracy of every shipped citation.** The audit verified that locators are
   internally consistent, non-contradictory across files, correctly labelled UNVERIFIED where
   research could not confirm them, and identical to `brief.md`. It cannot verify that
   Kish (1965) §8.2 p.258 says what is claimed, that the Cochrane Handbook §23.1.4.1 prints 1.576,
   or the Little & Rubin, ICH E9(R1), Popper, Cronbach & Meehl, Lohr, Gelman/Simpson/Betancourt,
   Cameron & Miller, Gelman & Hill and White & Carlin locators. **This is the bulk of T-7-07's and
   T-7-18's real substance.**
2. **The Chan & Perry (2017) post-mortem attestation**
   (`examples/known-bad/weak-identification-mmm-POSTMORTEM.md:62-84`) asserts the PDF was "fetched
   and read in full, 2026-08-12" and quotes four passages verbatim. Well-formed and falsifiable, but
   unconfirmable by tooling. T-7-07's 07-07 mitigation explicitly names "a human check reads the
   section and confirms the verification statement" — **that human check is still owed.**
3. **Statistical correctness of `_MISSINGNESS_METHOD_VALIDITY`** (`dsx/frame/val.py:187-198`). The
   project-assembled MAR-deny / MNAR-allow partition is honestly disclosed as project-assembled;
   whether it is *right* is a domain judgement.

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-08-14 | 25 | 25 | 0 | gsd-security-auditor (opus) via /gsd-secure-phase |

**Verdict:** `## SECURED` — 0 open threats at or above the `high` block threshold.

Verification depth: ASVS L1 grep-depth plus, on the auditor's own initiative, executable proof for
T-7-01 (type fuzzing), T-7-05 (record probe), T-7-14 (12-value rate invariance), T-7-15 (glob guard
fired in a throwaway worktree) and T-7-20 (red gate reproduced from `adc1ad2`). Full suite at HEAD:
543 tests, OK. `scripts/gen-finding-catalogue.py --check` exit 0. `scripts/check_brief_refs.py`
exit 0. No implementation file was modified by the audit.

T-7-02 and T-7-SC were returned as OPEN pending an accepted-risks entry to record them against;
ACC-7-01 and ACC-7-02 above are that entry, which closes both.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-08-14 (automated). Three items in *Human Judgement Required* remain owed
and are not covered by this approval.
