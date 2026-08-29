---
phase: 15-cuped-and-bi-declaration-checks-new-codes-d-05
plan: 06
status: complete
requirements: [REQ-P15-07]
---

# 15-06 SUMMARY — catalogue regen to 260, D-05 allowlist, additive invariant rebaseline

## What shipped
- **`scripts/gen-finding-catalogue.py`** — added `DSX-EXP-070` and `DSX-MET-021` to
  `_D05_ALLOWLIST_CODES` as **exact strings** (never `_D05_ALLOWLIST_PREFIXES`, which stays byte-unchanged),
  with a Phase-15 comment mirroring the DSX-COH-040 rationale. This turns the two new codes' D-05
  obligations (Citation + Structural-criterion docstring lines from 15-02/15-04, `# D-05:` test markers)
  into an enforced build gate.
- **`references/finding-codes.md`** — REGENERATED via `--write` to **Total: 260 codes** (258 → +DSX-EXP-070
  CRITICAL in the EXP group, +DSX-MET-021 HIGH in the MET group), not hand-edited.
- **`tests/test_finding_catalogue_invariant.py`** — additive D-08 rebaseline: `_EXPECTED_TOTAL` 258→260;
  `_MINTED_CODES = {DSX-REP-060, DSX-REP-061, DSX-EXP-070, DSX-MET-021}`; `_SNAPSHOT_TOTAL` held at 256;
  both methods renamed (`..._260_codes`, `..._plus_the_phase15_and_phase16_mints`) with prose/messages
  updated to read honestly at 260. Byte-frozen Phase-12 snapshot untouched.

## Gate evidence (all re-run by the orchestrator, brief §5)
- `python scripts/gen-finding-catalogue.py --write` then `--check` → exit 0 at 260 (only the pre-existing
  "declared twice" shipped-tree warnings on stderr; they do not change the exit code). `Total: 260` and both
  new rows present.
- `_D05_ALLOWLIST_CODES ⊇ {DSX-EXP-070, DSX-MET-021}`; `_D05_ALLOWLIST_PREFIXES` byte-unchanged.
- `python -m unittest tests.test_finding_catalogue_invariant` → 2 OK (count 260 + set-identity vs
  snapshot ∪ {REP-060, REP-061, EXP-070, MET-021}); `_SNAPSHOT_TOTAL == 256`.
- `git status --porcelain -- tests/fixtures/finding-codes-phase12.md` empty (snapshot byte-frozen).
