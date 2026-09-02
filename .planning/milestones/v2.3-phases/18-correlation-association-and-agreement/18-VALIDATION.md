---
phase: 18
slug: correlation-association-and-agreement
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-09-01
validated: 2026-09-02
---

# Phase 18 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Seeded from 18-RESEARCH.md §Validation Architecture (2026-09-01). Per-task IDs
> finalize when the D-08 wave-split plans (18-A / 18-B) are written at S2-2.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib `unittest` |
| **Config file** | none — discovered via `unittest discover -s tests` |
| **Quick run command** | `python3 -m unittest tests.<module_name> -v` |
| **Full suite command** | `python3 -m unittest discover -s tests -q` |
| **Estimated runtime** | ~60 seconds (est.; 1323-test baseline from Phase 17 close) |

---

## Sampling Rate

- **After every task commit:** the single new test module the task touched (e.g.
  `python3 -m unittest tests.test_correlation_scale_kind_gate -v`), **plus**
  `python3 -m unittest tests.test_finding_catalogue_invariant -v` on any task that
  adds a `report.add(...)` call site.
- **After every plan wave:** `python3 -m unittest discover -s tests -q`.
- **Before `/gsd-verify-work`:** `scripts/check.sh` in full — exercises
  `scripts/gen-finding-catalogue.py --check` (catches a missing
  `_D05_ALLOWLIST_CODES` entry AND a stale `finding-codes.md`) and the good/bad
  fixture gate smoke test at all four gate points.
- **Max feedback latency:** ~60 seconds (full suite).

---

## Per-Task Verification Map

Seeded at REQ granularity; the planner binds each row to concrete task IDs across
the two D-08 waves (Plan 18-A routing+gates+doc/catalogue lockstep ∥ Plan 18-B
effect-size convention bands).

| Req / Proof | Plan | Wave | Behavior (oracle) | Test Type | Automated Command | File | Status |
|---|---|---|---|---|---|---|---|
| REQ-P18-01 | 18-A | 1 | `recommend_association(kind)` returns the correct acceptable-coefficient SET per kind; dCor/partial catalog-only rows named in `test-selection.md` | unit + doc-presence | `python3 -m unittest tests.test_declared_association_routing -v` | ✅ exists | ✅ green (re-run 2026-09-02) |
| REQ-P18-02 | 18-A | 1 | agreement/reliability rows present in `test-selection.md`; Cronbach→omega named with deprecation citation | doc-presence | (assertion in the routing test module) | ✅ exists | ✅ green (re-run 2026-09-02) |
| REQ-P18-03 | 18-A | 1 | DSX-STA-050 fires on `pearson_correlation`+declared-ordinal(>2 levels), silent on `point_biserial`/dichotomous; DSX-STA-051 fires on any correlation-family test vs `agreement`/`method_comparison` | unit | `python3 -m unittest tests.test_correlation_scale_kind_gate -v` | ✅ exists | ✅ green (re-run 2026-09-02) |
| REQ-P18-04 | 18-A | 1 | DSX-STA-060 fires on missing/out-of-vocab ICC sub-field, silent on complete valid triple; DSX-STA-061 fires on missing/unrecognised `weights` (accepts explicit matrix); DSX-STA-062 fires when `p_pos` OR `p_neg` missing for any kappa-family test | unit | `python3 -m unittest tests.test_agreement_completeness_gate -v` | ✅ exists | ✅ green (re-run 2026-09-02) |
| REQ-P18-05 (pinned) | 18-B | 1 | report-only Krippendorff reference value = **0.7598 @ level=ordinal**; Landis-Koch band boundaries match cited published thresholds (labeled convention) | unit, numeric fixture | `python3 -m unittest tests.test_effect_size_kind -v` | ✅ exists | ✅ green (re-run 2026-09-02) |
| REQ-P18-05 (catalog-only) | 18-B | 1 | ICC/Koo-Li bands, Kendall's W bands, dCor, partial, Cronbach→omega each present as a named cited pointer row with **NO** numeric boundary asserted | doc-presence only | substring assertions, never numeric equality | ✅ exists | ✅ green (re-run 2026-09-02) |
| REQ-P18-05 (report-only kind) | 18-B | 1 | `effect_size_kind: kappa` (any report-only kind) on a significant result fires neither DSX-STA-011 nor DSX-STA-012; a `report.ok(...)` names the convention | unit | `python3 -m unittest tests.test_effect_size_kind -v` | ✅ exists | ✅ green (seam oracle `test_report_only_kappa_fires_neither_011_nor_012_and_reports_ok`, re-run 2026-09-02) |
| REQ-P18-06 | 18-A | 1 | `recommend_association` signature carries exactly one param (`estimand_kind`), no data/n/distribution flag (anti-two-stage) | unit, structural (`inspect.signature`) | `python3 -m unittest tests.test_declared_association_routing -v` | ✅ exists | ✅ green (re-run 2026-09-02) |
| Catalogue mint proof | 18-A | 1 | live catalogue = frozen snapshot + pre-existing mints + exactly the five new codes; declared total = **265** | unit | `python3 -m unittest tests.test_finding_catalogue_invariant -v` | ✅ exists (`_EXPECTED_TOTAL` 265, `_MINTED_CODES` extended, `_SNAPSHOT_TOTAL` 256 frozen) | ✅ green (re-run 2026-09-02) |
| D-05 citation build gate | 18-A | 1 | each of the five codes has a `Citation:` + reference/criterion line + `# D-05: <CODE>` test marker | build script | `python3 scripts/gen-finding-catalogue.py --check` | ✅ (`_D05_ALLOWLIST_CODES` carries the five by exact name) | ✅ green (exit 0 "finding catalogue is current", re-run 2026-09-02) |
| D-08 fixture silence | 18-A | 1 | `examples/good-ANALYSIS-SPEC.yaml` and `examples/bad-ANALYSIS-SPEC.yaml` fire none of the five new codes | integration | re-run `tests.test_good_fixture_phase15` / `tests.test_known_bad_corpus` | ✅ pre-existing (verified unchanged) | ✅ green (in full suite 1367 OK) |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `tests/test_declared_association_routing.py` — new; covers REQ-P18-01, REQ-P18-06 (exists, green)
- [x] `tests/test_correlation_scale_kind_gate.py` — new; covers REQ-P18-03 (DSX-STA-050/051) (exists, green)
- [x] `tests/test_agreement_completeness_gate.py` — new; covers REQ-P18-04 (DSX-STA-060/061/062) (exists, green)
- [x] `tests/test_finding_catalogue_invariant.py` — extended (no new file): `_EXPECTED_TOTAL` 260→265, `_MINTED_CODES` extended; `_SNAPSHOT_TOTAL` 256 frozen (green at 265)
- [x] `tests/test_effect_size_kind.py` — extended: REQ-P18-05 report-only-kind branch + pinned band values + firewall + seam oracle (green)
- [x] `scripts/gen-finding-catalogue.py` — the five codes added to `_D05_ALLOWLIST_CODES` by exact name (`--check` exit 0)
- [x] No framework install needed — stdlib `unittest` confirmed working (Python 3.14.6).

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Row-level bibliographic citations for the printed methods (Shrout-Fleiss 1979, McGraw-Wong 1996 corrected, Feinstein-Cicchetti 1990 Parts I/II, Landis-Koch 1977, Krippendorff 0.7598@ordinal) confirmed at locator before print | REQ-P18-01/02/05 | D-05 human read (brief §4 item 1) — the granularity ruling defers row-bibliography confirmation to the execute row-pass; HQ-16 already answered the five gate-code citations | Confirm each cited value/locator at source during S2-3 row-bibliography pass; catalog-only items ship presence-only with explicit not-in-hand language |

*All programmatic behaviors above have automated verification; the only manual item is D-05 citation authenticity, which is the standing portfolio bar, not a code oracle.*

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies (10 automated oracles + 1 manual-only D-05 citation item)
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references (5 test modules — all exist and green)
- [x] No watch-mode flags
- [x] Feedback latency < 60s (full suite 35.996s from a clean tree)
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** NYQUIST-COMPLIANT 2026-09-02 (orchestrator, State A audit). All 6 requirements
(REQ-P18-01…06) have automated verification: 10 automated test oracles re-run green
(52 targeted Phase-18 tests + `gen-finding-catalogue.py --check` exit 0 at 265 + the
firewall/seam oracles, all inside a full suite of **1367 OK** from a clean tree) plus 1
manual-only item (D-05 citation authenticity — the standing portfolio bar, already answered
for the five gate codes via HQ-16; row-bibliography confirmed at the S2-3 row-pass). Zero gaps
→ no nyquist-auditor spawn required (workflow §3). `nyquist_compliant: true`, `status: validated`.

---

## Validation Audit 2026-09-02

| Metric | Count |
|--------|-------|
| Requirements | 6 (REQ-P18-01…06) |
| COVERED (automated, green) | 6 |
| PARTIAL | 0 |
| MISSING | 0 |
| Manual-only (D-05 citation authenticity) | 1 (HQ-16-answered for the five gate codes) |
| Gaps found | 0 |
| Resolved | 0 (none to resolve — all oracles present and green) |
| Escalated | 0 |

State A audit: every mapped oracle re-run by the orchestrator from a clean tree (brief §5;
stray `DECISIONS.jsonl` ledgers cleared first per the HUMAN-QUEUE standing note). No new test
files generated — the seeded Wave-0 modules already exist and pass. `nyquist_compliant: true`,
`status: validated`.
