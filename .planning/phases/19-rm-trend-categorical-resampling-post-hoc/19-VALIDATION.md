---
phase: 19
slug: rm-trend-categorical-resampling-post-hoc
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-09-02
---

# Phase 19 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Seeded from 19-RESEARCH.md §Validation Architecture (2026-09-02, plan preflight S3-2).
> Per-task IDs finalize when the D-08 wave-split plans are written by the planner at
> S3-2. Phase 19 mints **ten** HIGH codes; catalogue **265 → 275**. Wave 1 is **19-A
> alone** (research verdict: no new mathx band → no 19-B); Wave 2 is **19-C** (gates +
> fixtures). All oracles below are **pending** until the plans are written and executed.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib `unittest` (NO pytest anywhere in this repo) |
| **Config file** | none — discovered via `unittest discover -s tests` |
| **Quick run command** | `python3 -m unittest tests.<module_name> -v` |
| **Full suite command** | `python3 -m unittest discover -s tests -q` |
| **Estimated runtime** | ~60 seconds (est.; 1367-test baseline from Phase 18 close) |
| **Python** | 3.14.6 (verified this session) |

---

## Sampling Rate

- **After every task commit:** the single new test module the task touched (e.g.
  `python3 -m unittest tests.test_rm_sphericity_gate -v`), **plus**
  `python3 -m unittest tests.test_finding_catalogue_invariant -v` on any task that
  adds a `report.add(...)` call site.
- **After every plan wave:** `python3 -m unittest discover -s tests -q`. **Wave 1
  (19-A) asserts catalogue == 265** (rows/recommend/vocab mint no codes); **Wave 2
  (19-C) asserts catalogue == 275** (the ten new codes).
- **Before `/gsd-verify-work`:** `scripts/check.sh` in full — exercises
  `scripts/gen-finding-catalogue.py --check` (catches a missing
  `_D05_ALLOWLIST_CODES` entry AND a stale `finding-codes.md`) and the good/bad
  fixture gate smoke test at all four gate points.
- **Max feedback latency:** ~60 seconds (full suite).

---

## Per-Task Verification Map

Seeded at REQ granularity from 19-RESEARCH.md §Validation Architecture. The planner
binds each row to concrete task IDs across the D-08 waves (Wave 1 = **19-A** routing +
vocab + rows + no-autoswitch, catalogue stays 265; Wave 2 = **19-C** the ten `_check_*`
gates + `_D05_ALLOWLIST_CODES` additions + fixtures, catalogue → 275). No 19-B (research
verdict: no new report-only band required — `mathx.py` already carries Kendall's W
catalog-only, and no REQ-P19-01…07 names a band).

| Req / Proof | Plan | Wave | Behavior (oracle) | Test Type | Automated Command | Status |
|---|---|---|---|---|---|---|
| REQ-P19-01 | 19-C (routing 19-A) | 1→2 | DSX-STA-070 fires on declared `mauchly_conditional` (two-stage sphericity), silent on `unconditional_gg`/absent; **never** fires on mere repeated-measures presence | unit + structural | `python3 -m unittest tests.test_rm_sphericity_gate -v` | ⬜ pending |
| REQ-P19-02 | 19-C (routing 19-A) | 1→2 | DSX-STA-080 fires on `cochran_armitage` + blank dose-scores; DSX-STA-081 fires on `mann_kendall`/`sens_slope` + blank autocorrelation-handling, **SILENT on a declared `none`/`independent`** (`is_blank` predicate, not membership) | unit | `python3 -m unittest tests.test_trend_gate -v` | ⬜ pending |
| REQ-P19-03 | 19-A | 1 | DEPRECATED Yates row + log-linear pointer row + CMH surfaced field + Fisher-Freeman-Halton footnote present in `test-selection.md`; **ZERO new codes minted** (catalogue stays 265 at Wave 1) | doc-presence + catalogue count | `python3 -m unittest tests.test_finding_catalogue_invariant -v` + substring asserts | ⬜ pending |
| REQ-P19-04 | 19-C (routing 19-A) | 1→2 | DSX-STA-090 fires on an incomplete `{method, seed, B, unit}` quadruple, message names the missing member; silent on the complete quadruple (ONE code, not four) | unit | `python3 -m unittest tests.test_resampling_gate -v` | ⬜ pending |
| REQ-P19-05 | 19-C (routing 19-A) | 1→2 | DSX-STA-100 fires on declared post-hoc family ∉ declared omnibus family-map; silent on a matched pair; deprecated post-hocs (SNK, unprotected-LSD-k>3) never selected as a default | unit | `python3 -m unittest tests.test_posthoc_gate -v` | ⬜ pending |
| REQ-P19-06 | 19-C (routing 19-A) | 1→2 | DSX-STA-110 fires on a variance test declared with role = precondition-to-location (or blank role) AND scale not the declared estimand, silent on `scale_estimand`; DSX-STA-111 fires on power-reporting type ∈ {observed, post_hoc} only (a-priori/design/MDE-sensitivity do not fire — narrow) | unit | `python3 -m unittest tests.test_variance_role_gate -v` / `tests.test_power_reporting_gate -v` | ⬜ pending |
| REQ-P19-07 | 19-C (routing 19-A) | 1→2 | DSX-STA-120 fires on `wald` proportion-CI (n-independent, no hard-coded n≤40); DSX-STA-121 fires on declared exposure + blank offset; DSX-STA-122 fires on declared nnt + blank nnt-CI companion | unit | `python3 -m unittest tests.test_proportion_count_gate -v` | ⬜ pending |
| No-autoswitch (REQ-P18-06 doctrine, extended) | 19-A | 1 | every new `recommend_*` signature takes NO data/n/distribution flag (the anti-two-stage structural proof) | unit, structural (`inspect.signature`) | `python3 -m unittest tests.test_declared_rm_trend_routing -v` / `tests.test_declared_resampling_posthoc_routing -v` | ⬜ pending |
| Catalogue mint proof (Wave 1) | 19-A | 1 | rows/recommend/vocab mint no codes: live catalogue declared total == **265** (unchanged) | unit | `python3 -m unittest tests.test_finding_catalogue_invariant -v` | ⬜ pending |
| Catalogue mint proof (Wave 2) | 19-C | 2 | live set == frozen snapshot ∪ four prior ∪ five Phase-18 ∪ **ten Phase-19**; declared total == **275**; set-identity (no drift) | unit | `python3 -m unittest tests.test_finding_catalogue_invariant -v` | ⬜ pending |
| D-05 citation build gate (ten codes) | 19-C | 2 | each of the ten codes has a `Citation:` line, a `Structural criterion:`/`Reference value:` line, and a `# D-05: <CODE>` test marker; `_D05_ALLOWLIST_CODES` carries all ten by exact name | build script | `python3 scripts/gen-finding-catalogue.py --check` | ⬜ pending |
| D-08 fixture discipline | 19-C | 2 | `examples/good-ANALYSIS-SPEC.yaml` fires none of the ten; `examples/bad-ANALYSIS-SPEC.yaml` (extended) fires all ten; `_SNAPSHOT_TOTAL`/phase12 fixture stay byte-frozen at 256 | integration | `dsx audit --spec examples/good-ANALYSIS-SPEC.yaml` / same for `bad` | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements (test files — all NEW or EXTENDED, none exist yet)

- [ ] `tests/test_declared_rm_trend_routing.py` — new; no-autoswitch for `recommend_rm`/`recommend_trend`/`recommend_variance_role` (REQ-P18-06 doctrine)
- [ ] `tests/test_declared_resampling_posthoc_routing.py` — new; no-autoswitch for `recommend_resampling`/`recommend_posthoc`/`recommend_power`/`recommend_proportion_ci`
- [ ] `tests/test_rm_sphericity_gate.py` — new; REQ-P19-01 (DSX-STA-070)
- [ ] `tests/test_trend_gate.py` — new; REQ-P19-02 (DSX-STA-080/081)
- [ ] `tests/test_resampling_gate.py` — new; REQ-P19-04 (DSX-STA-090)
- [ ] `tests/test_posthoc_gate.py` — new; REQ-P19-05 (DSX-STA-100)
- [ ] `tests/test_variance_role_gate.py` — new; REQ-P19-06a (DSX-STA-110)
- [ ] `tests/test_power_reporting_gate.py` — new; REQ-P19-06b (DSX-STA-111)
- [ ] `tests/test_proportion_count_gate.py` — new; REQ-P19-07 (DSX-STA-120/121/122)
- [ ] `tests/test_finding_catalogue_invariant.py` — extended (no new file): `_EXPECTED_TOTAL` 265→275, `_MINTED_CODES` +10, method rename + 275-mentioning docstrings; `_SNAPSHOT_TOTAL` 256 byte-frozen
- [ ] `scripts/gen-finding-catalogue.py` — the ten codes added to `_D05_ALLOWLIST_CODES` by exact name (build-gate prerequisite for the D-05 checks to mean anything)
- [ ] REQ-P19-03 doc-presence asserts (Yates DEPRECATED / log-linear pointer / CMH field / FFH footnote) — folded into the routing or catalogue test module
- [ ] No framework install needed — stdlib `unittest` confirmed working (baseline `--check` green this session, Python 3.14.6).

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Each of the ten gate CODEs' D-05 citation confirmed at locator (Greenhouse-Geisser 1959; Cochran-Armitage; Hamed-Rao 1998; Davidson-MacKinnon 2000; Efron 1987; Hayter 1986 JASA; Games-Howell 1976; Zimmerman 2004; Hoenig-Heisey 2001; Lakens 2022; Brown-Cai-DasGupta 2001; Newcombe 1998 Paper B; McCullagh-Nelder 1989) | REQ-P19-01…07 | D-05 human read (brief §4 item 1) — **already answered via HQ-17** (16 citations, 2026-09-01) for all shipping gate codes | HQ-17 answered; row-bibliography (Altman-Deeks-Sackett 1998 NNT CI + the non-gated row citations) confirmed at the S3-3 row-bibliography pass |
| No fabricated numeric locator/boundary for any D-07 not-in-hand item (Hamed-Rao lag threshold, BCD n≤40, Campbell expected-count≥1, M&N §6.2, Hayter α, GG ε, DM 19/99-vs-399/1499) | REQ-P19-01…07 | D-05 authenticity + the portfolio hard-code prohibition | Gates check declared-field PRESENCE only — nothing numeric ships; catalog-only rows carry explicit "confirm-at-source"/"not-in-hand" language |

*All programmatic behaviors above have automated verification; the only manual items are D-05 citation authenticity (HQ-17-answered) and the hard-code prohibition, both the standing portfolio bar, not a code oracle.*

---

## Validation Sign-Off (pending — set at S3-5 `/gsd-validate-phase 19`)

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references (the new gate/routing test modules)
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s (full suite)
- [ ] `nyquist_compliant: true` set in frontmatter (after execute + validate)

**Approval:** PENDING — this is the plan-phase seed (`status: draft`). Set to
NYQUIST-COMPLIANT by `/gsd-validate-phase 19` at S3-5 once the ten gates + their test
modules exist and all REQ-P19-01…07 oracles are green from a clean tree.
