---
phase: 18
slug: correlation-association-and-agreement
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-09-01
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
| REQ-P18-01 | 18-A | 1 | `recommend_association(kind)` returns the correct acceptable-coefficient SET per kind; dCor/partial catalog-only rows named in `test-selection.md` | unit + doc-presence | `python3 -m unittest tests.test_declared_association_routing -v` | ❌ W0 (new) | ⬜ pending |
| REQ-P18-02 | 18-A | 1 | agreement/reliability rows present in `test-selection.md`; Cronbach→omega named with deprecation citation | doc-presence | (assertion in the routing test module) | ❌ W0 (new) | ⬜ pending |
| REQ-P18-03 | 18-A | 1 | DSX-STA-050 fires on `pearson_correlation`+declared-ordinal(>2 levels), silent on `point_biserial`/dichotomous; DSX-STA-051 fires on any correlation-family test vs `agreement`/`method_comparison` | unit | `python3 -m unittest tests.test_correlation_scale_kind_gate -v` | ❌ W0 (new) | ⬜ pending |
| REQ-P18-04 | 18-A | 1 | DSX-STA-060 fires on missing/out-of-vocab ICC sub-field, silent on complete valid triple; DSX-STA-061 fires on missing/unrecognised `weights` (accepts explicit matrix); DSX-STA-062 fires when `p_pos` OR `p_neg` missing for any kappa-family test | unit | `python3 -m unittest tests.test_agreement_completeness_gate -v` | ❌ W0 (new) | ⬜ pending |
| REQ-P18-05 (pinned) | 18-B | 1 | report-only Krippendorff reference value = **0.7598 @ level=ordinal**; Landis-Koch band boundaries match cited published thresholds (labeled convention) | unit, numeric fixture | `python3 -m unittest tests.test_effect_size_kind -v` (or new `test_agreement_convention_bands`) | ❌ W0 (ext) | ⬜ pending |
| REQ-P18-05 (catalog-only) | 18-B | 1 | ICC/Koo-Li bands, Kendall's W bands, dCor, partial, Cronbach→omega each present as a named cited pointer row with **NO** numeric boundary asserted | doc-presence only | substring assertions, never numeric equality | ❌ W0 (ext) | ⬜ pending |
| REQ-P18-05 (report-only kind) | 18-B | 1 | `effect_size_kind: kappa` (any report-only kind) on a significant result fires neither DSX-STA-011 nor DSX-STA-012; a `report.ok(...)` names the convention | unit | `python3 -m unittest tests.test_effect_size_kind -v` | ❌ W0 (ext) | ⬜ pending |
| REQ-P18-06 | 18-A | 1 | `recommend_association` signature carries exactly one param (`estimand_kind`), no data/n/distribution flag (anti-two-stage) | unit, structural (`inspect.signature`) | `python3 -m unittest tests.test_declared_association_routing -v` | ❌ W0 (new) | ⬜ pending |
| Catalogue mint proof | 18-A | 1 | live catalogue = frozen snapshot + pre-existing mints + exactly the five new codes; declared total = **265** | unit | `python3 -m unittest tests.test_finding_catalogue_invariant -v` | ❌ W0 (ext: bump `_EXPECTED_TOTAL` 260→265, extend `_MINTED_CODES`; `_SNAPSHOT_TOTAL` 256 stays frozen) | ⬜ pending |
| D-05 citation build gate | 18-A | 1 | each of the five codes has a `Citation:` + reference/criterion line + `# D-05: <CODE>` test marker | build script | `python3 scripts/gen-finding-catalogue.py --check` | ❌ W0 (`_D05_ALLOWLIST_CODES` must add the five by exact name — prefix `DSX-STA-` is NOT allowlisted) | ⬜ pending |
| D-08 fixture silence | 18-A | 1 | `examples/good-ANALYSIS-SPEC.yaml` and `examples/bad-ANALYSIS-SPEC.yaml` fire none of the five new codes | integration | re-run `tests.test_good_fixture_phase15` / `tests.test_known_bad_corpus` | ✅ pre-existing (verify unchanged) | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_declared_association_routing.py` — new; covers REQ-P18-01, REQ-P18-06
- [ ] `tests/test_correlation_scale_kind_gate.py` — new; covers REQ-P18-03 (DSX-STA-050/051)
- [ ] `tests/test_agreement_completeness_gate.py` — new; covers REQ-P18-04 (DSX-STA-060/061/062)
- [ ] `tests/test_finding_catalogue_invariant.py` — extend (no new file): `_EXPECTED_TOTAL` 260→265, extend `_MINTED_CODES`; `_SNAPSHOT_TOTAL` 256 frozen
- [ ] `tests/test_effect_size_kind.py` — extend: REQ-P18-05 report-only-kind branch + pinned band values
- [ ] `scripts/gen-finding-catalogue.py` — add the five codes to `_D05_ALLOWLIST_CODES` by exact name (build-gate prerequisite; the family prefix `DSX-STA-` is NOT in `_D05_ALLOWLIST_PREFIXES`)
- [ ] No framework install needed — stdlib `unittest` confirmed working (Python 3.14.6).

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Row-level bibliographic citations for the printed methods (Shrout-Fleiss 1979, McGraw-Wong 1996 corrected, Feinstein-Cicchetti 1990 Parts I/II, Landis-Koch 1977, Krippendorff 0.7598@ordinal) confirmed at locator before print | REQ-P18-01/02/05 | D-05 human read (brief §4 item 1) — the granularity ruling defers row-bibliography confirmation to the execute row-pass; HQ-16 already answered the five gate-code citations | Confirm each cited value/locator at source during S2-3 row-bibliography pass; catalog-only items ship presence-only with explicit not-in-hand language |

*All programmatic behaviors above have automated verification; the only manual item is D-05 citation authenticity, which is the standing portfolio bar, not a code oracle.*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending (set by `/gsd-validate-phase 18` at S2-5)
