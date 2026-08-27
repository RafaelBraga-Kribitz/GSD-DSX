---
phase: 12-calibration
plan: 07
subsystem: planning-docs / backlog-hygiene
status: complete
requirements: [REQ-P12-05]
tags: [backlog-re-evaluation, reversal, self-001, D-14, D-15, D-16, D-17, closing-gate]
dependency_graph:
  requires:
    - "plan 12-02 — measured operator paradigm split (empty; item-4 non-promotion evidence)"
    - "plan 12-05 — measured (miss-rate, FPR) headline = (1.0, 0.0)"
    - "plan 12-06 — per-family friction column (raw+net) + catalogue-invariant(256)"
    - "brief.md §6.5 nine-item gated backlog + REV-001; .planning/REVERSALS.md template + SELF-001 convention"
  provides:
    - "§6.5 disposed: carry 8, remove 1 (item 6 relocated to Removed/permanently-out-of-scope)"
    - "REV-002 (D-14) — honest reclassification surviving SELF-001"
    - "Phase-12 corpus-green closing gate (full suite + catalogue)"
  affects:
    - "S3-4 (catch-rate/FPR readout + Statistician adversarial review) — the backlog is now disposed"
tech_stack:
  added: []
  patterns:
    - "D-14 reversal-as-relocation: a test-pinned row is moved, never deleted, so the pin passes unmodified"
    - "SELF-001-safe reversal: New evidence names the systematic REQ-P12-05 re-evaluation event, not the pre-existing determinism doctrine"
key_files:
  created:
    - ".planning/phases/12-calibration/12-07-SUMMARY.md"
  modified:
    - "brief.md (§6.5 restructure)"
    - ".planning/REVERSALS.md (REV-002 appended)"
metrics:
  finding_codes_minted: 0
  completed: 2026-08-27
  tasks: 2
  files: 2
---

# Phase 12 Plan 07: §6.5 Re-evaluation + REV-002 Summary

The readout the whole phase's measurement exists to make honest: every §6.5 gated-backlog
item re-evaluated against its stated entry condition using the numbers plans 12-02/12-05/12-06
measured — **carry eight, remove one** — plus the phase's corpus-green closing gate. This is a
**docs-only** plan (`files_modified: brief.md + .planning/REVERSALS.md`); it authors no code and
mints no finding code. Because the closing gate IS the plan's content, the orchestrator executed
it directly and gated it first-hand (no subagent-trust gap), matching the S2-3-Wave-5 precedent.

## Task 1 — §6.5 re-evaluated; item 6 relocated

The nine rows were disposed against the measured evidence, each disposition citing the count/rate/split it rests on (no case manufactured, D-02/D-15):

| Item | Disposition | Grounding |
|------|-------------|-----------|
| 1 — prior justification/sensitivity | **carry** | frequentist mirror unwritten (D-12a); no corpus count promotes a paradigm-mirror item |
| 2 — prior predictive `DSX-PAR-022` | **already promoted** | REV-001 (row records it) |
| 3 — convergence `DSX-PAR-030` | **carry** | frequentist mirror unwritten (D-12a) |
| 4 — Bayesian admissibility (2nd axis) | **carry; NOT auto-promoted** | plan 12-02: operator paradigm split **empty (0 distinct frames)** → below the 15% Bayesian gate; the non-promotion is the point of the number (brief §6) |
| 5 — `dsx quiz` fading | **carry, prerequisite-pending** | ships on M5; M5 not shipped |
| 6 — ratio-metric dilution | **REMOVE** | structurally unevaluable — Formula (3) is a per-user sum with no declaration-readable scalar (D-16) |
| 7 — feature-provenance | **carry** | plan 12-05: the 3 ABSENT misses (forking / fabrication / selective-exclusion; 3/3) are not a feature-origin-only attribution; not manufactured |
| 8 — magnitude-without-computed-effect | **carry; likely none** | no corpus case passes all claims checks while asserting an uncomputed magnitude (paper instances already fire `DSX-CLM-070`) |
| 9 — subgroup-harm declaration | **carry** | needs an admissible D-05 source **and** a corpus case; neither is in the measured corpus |

Item 6 was **relocated verbatim** — not deleted, not softened back to the access premise D-12
proved false — into a new **"Removed / permanently out of scope (D-14)"** subsection under §6.5.
The three pin-test substrings ("Ratio-metric dilution for trigger analysis", "Formula (3)",
"per-unit trigger and outcome data reaching the gate") remain present verbatim (the unicode
formula was moved by reading it from the file, never retyped). The main table now carries **eight**
items. A **Phase 12 re-evaluation** subsection records the dispositions above with the measured
`(miss-rate 1.0, FPR 0.0)` headline as backdrop.

**Gate (pin test, unmodified):** `python -m unittest tests.test_known_bad_corpus.TestKnownBadCorpus.test_brief_states_the_ratio_metric_dilution_entry_condition_as_a_falsifiable_blocker -v` → **OK** (the pin test file was not touched).

## Task 2 — REV-002 filed; corpus-green closing gate

`REV-002` was appended to `.planning/REVERSALS.md` (next id after REV-001, no reuse) with all four
template fields:

- **Reversed:** the D-13 gated-backlog *deferral* of item 6 → **permanently out of scope**.
- **New evidence:** the completed REQ-P12-05 systematic re-evaluation of all nine rows under one
  uniform rule (*evaluable-and-unmet ⇒ carry; structurally-unreachable ⇒ remove*), which sorts item
  6 as the **only** structurally-unreachable row. This is **explicitly not** the D-01/D-02
  determinism doctrine restated as novelty — the record names the doctrine as pre-existing and the
  re-evaluation event as what resolves the row's original hedge ("may be … not merely deferred")
  into a decision (D-17, SELF-001-safe).
- **What would have made the original deferral correct:** a declaration-evaluable scalar (Formula (3) has none).
- **What did not change:** D-01/D-02 stand; the additive `DSX-INT-030` case **stays shipped**; items 4 and 5 **stay carried**.

SELF-001 survivability is a human-review bar at ship (no mechanical gate); the New evidence field is written to be self-evidently non-laundering.

**Closing gate:** `bash scripts/check.sh` → **all checks passed** — full suite `Ran 1219 tests ... OK` (unchanged; docs-only), `python scripts/gen-finding-catalogue.py --check` current, **catalogue Total: 256 codes** (D-18 held, zero minted), capability manifest conformant, gate contract good/bad/missing, determinism identical.

## Deviations from Plan

None substantive. The plan's Task-2 automated verify is `python -m unittest discover -s tests -p "test_*.py" && python scripts/gen-finding-catalogue.py --check`; the canonical aggregate `bash scripts/check.sh` (a superset that also checks manifest conformance, the gate contract and determinism) was run as the equivalent closing gate, exactly as the plan's `<verification>` note permits. `discover` was also run standalone → `Ran 1219 tests ... OK`.

## Boundary compliance

- **Touched only** `brief.md` and `.planning/REVERSALS.md` (the plan's `files_modified`) plus this SUMMARY; `git status --short` shows no other tracked changes.
- **No code, no test, no catalogue change** — `dsx/`, `tests/`, `references/finding-codes.md`, `scripts/gen-finding-catalogue.py` untouched. **Zero finding codes minted (D-18)**; catalogue verified at **256**.
- **CRLF preserved** in both edited files (the repo checks out CRLF; edits applied via a CRLF-preserving writer).
- Shared tracking files (STATE.md, ROADMAP.md, LOOP-LEDGER.md) written serially by the orchestrator after the gate, per the single-writer rule.

## D-05 note

The D-05 primary-source reads for the new Phase-12 corpus cases (plans 12-01/12-04) remain owed at the Phase-12 UAT/ship round (pre-registered per 12-CONTEXT `<deferred>`), non-blocking here.

## Self-Check: PASSED

- §6.5 carries eight items; the "Removed / permanently out of scope (D-14)" subsection holds the item-6 row.
- The three pinned substrings are present verbatim; the pin test passes unmodified.
- `.planning/REVERSALS.md` contains REV-002 (next id) with all four fields; New evidence names the systematic re-evaluation, not the doctrine.
- Full suite 1219 OK; catalogue current at 256.

---
*Phase: 12-calibration*
*Completed: 2026-08-27*
