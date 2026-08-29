# Phase 16 — Verification (S3-4, goal-backward)

**Verifier:** orchestrator-direct (opus/high, §3). **Method:** each requirement mapped to a
re-run gate or read locator, not to task-completion. Every command below was executed here (§5).
**Result: PASSED — 4/4 REQ-P16-01..04 COVERED.**

| REQ | Goal | Evidence (re-run / read) | Verdict |
|---|---|---|---|
| **P16-01** | `dsx-reproduce` exists, registered, re-runs `entrypoint` (in the skill), writes `REPRO-REPORT.md` with a machine number block + status | `skills/dsx-reproduce/SKILL.md` present (objective + 7-step process: resolve spec → run entrypoint OFF gate path via Bash → capture fresh numbers → fill template YAML block → honest `skipped/unable` on failure → stamp `reproduce_report` opt-in → surface comparison). `capability.json` registers it as the **14th** skill; `check.sh` reports "conformant … 14 skills". `templates/REPRO-REPORT.md` carries the fenced machine block + `status` vocabulary. | **COVERED** |
| **P16-02** | `dsx gate verify/ship` emits 060 (missing) / 061 (non-overlap); silent when absent or honestly skipped; imports no pandas/scipy; executes no entrypoint | `dsx/checks/repro.py::_check_reproduce_report` — declaration-only, stdlib `math`/`re`/`pathlib`, strict-only, opt-in on `reproducibility.reproduce_report`. `test_reproduce_report` **7 OK** (060 strict-only; 061 fires on disagreement + verdict-PASS does not suppress it; silent on absent/overlap/`skipped`). Both codes **HIGH**. `test_gate_path_hermetic` **2 OK**; `test_no_entrypoint_execution` **3 OK**. | **COVERED** |
| **P16-03** | Remaining Phase-12 corpus cases carry `protocol_adherence`; catch rate + FPR unchanged | 3/3 `*-ATTRIBUTION.yaml` carry the field; `test_known_bad_corpus` **45 OK** incl. `test_protocol_adherence_is_additive_and_ignored` (closed vocab; field **not** in `_headline.co_varnames`; `_headline` pinned `(0.25,0.3)`; ≥1 skipped countable). Corpus diff **0 deletions**; headline anchor test unedited. Extends REQ-P12-02, replaces nothing. | **COVERED** |
| **P16-04** | A non-vacuous test proves no `dsx/checks/`/`dsx/frame/` module executes the entrypoint | `test_no_entrypoint_execution` **3 OK** — static AST scan (not grep) over both trees; anti-vacuity (non-empty named set incl. `code.py`+`repro.py`); positive control flags `subprocess.run`/`runpy.run_path`/`os.system`/`exec`; negative control clears `ast.*`/`re.compile`. | **COVERED** |

## Catalogue closure (D-08)
`gen-finding-catalogue.py --check` exit **0** at **258**; invariant **2 OK** (258 count +
set-identity vs `phase-12 snapshot ∪ {DSX-REP-060, DSX-REP-061}`); `finding-codes-phase12.md`
byte-frozen. The three pinned artifacts moved in lockstep and no code beyond the sanctioned
delta appears.

## One cross-phase fix folded in during review (see REVIEW.md F1)
`tests/test_phase14_onboarding.py` hard-coded 13 DSX skills; Phase 16's legitimate 14th skill
made it stale. Anchor bumped 13→14; REQ-P14-04's Triggers invariant now holds across all 14.
Re-gate green.

## Gate
`sh scripts/check.sh` → **all checks passed — Ran 1254 tests OK** (determinism identical; gate
contract good passes / bad blocks / missing errors).

## Not verified here (correctly deferred)
- End-of-phase **security sign-off** + **UAT** → batched to HUMAN-QUEUE at S3-5 (as HQ-9/HQ-10).
- **D-06 numbering veto** (`DSX-REP-060/061`) → HQ-11, drains at S5-2 (non-blocking).
- The `dsx-reproduce` skill's *actual entrypoint execution* is prose/agent behaviour, not a
  deterministic gate; the gate side (what it does with the produced report) is fully tested above.
