# Code Review — Phase 13: Task playbooks that fill the spec

**Verdict: PASS — 0 blocking, 0 non-blocking-requiring-fix. No auto-fix applied (nothing to fix).**

Reviewer: orchestrator (opus/high, LOOP-BRIEF §3 routing). Review done directly rather than via a
`gsd-code-reviewer` subagent — a loud operational decision consistent with the S1-3 precedent: the
diff is small and well-bounded (skill markdown + one Python test + one JSON manifest + one fixture),
and every gate below was re-run by the orchestrator itself, not trusted from a subagent report
(brief §5). Date: 2026-08-28.

## Review surface

Phase 13 diff `4e83dd7^..bf5748e` (execution commits only; excludes tracking/SUMMARY files):

| File | Kind | Change |
|---|---|---|
| `skills/dsx-cohort/SKILL.md` | new | router skill (retention/cohort → metric + chart-matrix + coherence gates) |
| `skills/dsx-funnel/SKILL.md` | new | router skill (ordered step-conversion → metric + chart-matrix gates) |
| `skills/dsx-root-cause/SKILL.md` | new | router skill (diagnostic → decomposition + Simpson + causal-guard gates) |
| `skills/dsx-segment/SKILL.md` | new | router skill (multi-cut → multiplicity + Simpson gates) |
| `skills/dsx-explore-data/SKILL.md` | edit | hypothesis register (rides `assumptions[]` / `results.tests[]`) |
| `skills/dsx-narrate/SKILL.md` | edit | What / So What / Now What template over the 5-part structure |
| `skills/dsx-scope-analysis/SKILL.md` | edit | advisory ceremony-tier routing table |
| `capabilities/dsx/fragments/executor.md` | edit | `scripts/*.py`-over-notebook entrypoint preference |
| `capabilities/dsx/capability.json` | edit | registers the 4 new skills |
| `tests/test_finding_catalogue_invariant.py` | edit | set-identity diff vs frozen Phase-12 snapshot (D-07) |
| `tests/fixtures/finding-codes-phase12.md` | new | byte-copy of the generated catalogue (D-07 snapshot) |

The only executable code is the Python test; everything else is prompt guidance, one JSON manifest,
and one fixture. The load-bearing review risks for a skill-only phase are therefore **citation
authenticity** and **gate-path purity**, not algorithmic correctness.

## Findings

### 1. Citation authenticity — 21/21 cited codes real (PASS)
Every `DSX-*` code cited across all Phase-13-touched skills + the executor fragment exists in
`references/finding-codes.md`. Checked each of the 21 distinct cited codes by literal grep against
the catalogue — **zero dangling citations**:
`DSX-COH-040, DSX-SPEC-020, DSX-SPEC-026, DSX-VIZ-013, DSX-CAU-001, DSX-CAU-010, DSX-COH-001,
DSX-COH-010, DSX-MET-030, DSX-MET-031, DSX-EXP-050, DSX-EXP-051, DSX-EXP-053, DSX-SPEC-043,
DSX-COH-030, DSX-COH-031, DSX-VAL-020, DSX-CLM-080, DSX-NAR-030, DSX-MET-040, DSX-REP-040`.
(`DSX-CODE` in the executor fragment is the `dsx check code` gate name, not a finding code — correctly
not in the catalogue.)

### 2. Locator fidelity — 3/3 spot-checked source locators accurate (PASS)
The skills cite source lines, not just codes. Spot-checked the three load-bearing ones:
- `dsx/spec.py:22-28` → the `QUESTION_TYPES` dict (descriptive < diagnostic < causal < prescriptive);
  matches `dsx-root-cause`'s claim that `diagnostic` is strictly weaker than `causal`/`prescriptive`.
- `dsx/spec.py:1046-1055` → the `DSX-SPEC-043` "correction not recognised" check; matches `dsx-segment`.
- `dsx/checks/design.py:362-412` → `_check_multiplicity` / `DSX-EXP-053`; matches `dsx-segment` and
  the `dsx-explore-data` register.

### 3. File-reference authenticity (PASS)
`dsx-scope-analysis`'s tier block cites `docs/gsd-tiers.md` (exists, 126 lines) and emits
`scripts/gsd-tier.ps1` (exists, 129 lines). The script flips exactly the keys the tier table claims
(`dsx.enforce`; `mode=interactive` at Tier 2) — no dangling file reference.

### 4. Gate-path purity — D-01 (PASS)
`git diff --stat 4e83dd7^..bf5748e` shows **zero `dsx/` and zero `scripts/*.py` check-code edits**.
No new gate, no pandas/scipy import, no analysis entrypoint executed. The skills route to existing
gates; they do not add or alter one.

### 5. Zero minted codes — D-07 / REQ-P13-06 (PASS, asserted by diff not review)
`tests/test_finding_catalogue_invariant.py::test_code_set_is_set_identical_to_phase12_snapshot`
green: `added=[] removed=[]`, catalogue held at 256. This is a set-identity diff, strictly stronger
than the count invariant (it catches a cardinality-preserving swap) — exactly what REQ-P13-06 asks
for ("asserted by a catalogue diff against the Phase 12 catalogue").

### 6. Route-and-cite discipline — D-02 (PASS)
Every new skill opens "ROUTER, not an author" and closes with a `<what_this_skill_does_not_do>` fence
that forbids restating any gate threshold. No skill states a retention floor, a conversion floor, a
reversal magnitude, a correction method, or a mark whitelist — each defers to the owning gate. The
D-02 chart-admissibility concern (S1-2 nit 4, "no automated catch") was hand-checked here: `dsx-cohort`
and `dsx-funnel` route mark admissibility to `DSX-VIZ-013` under the declared `data_input_type` rather
than restating an allowed-mark list — clean.

### 7. Coherence-not-Cohort caveat — D-08 (PASS)
`dsx-cohort` carries an explicit `<naming_caveat>`: `DSX-COH-*` is the **Coherence** family, not
short for "cohort"; it routes `revisit_when` to `DSX-COH-040` as a consequence of a shared need, not a
cohort-specific family. Prevents a future reader misciting the family.

### 8. capability.json (PASS)
`scripts/validate-capability.py`: `capability 'dsx' v2.0.0 is conformant: 2 steps, 5 contributions,
5 gates, 13 skills, 6 agents, 13 config keys`. All four new skills are in the `skills[]` array.

### 9. Python test quality (PASS)
`tests/test_finding_catalogue_invariant.py` is CRLF-safe by construction (whitespace-collapse for the
Total line, non-line-anchored `_ROW_RE` for rows — repo CLAUDE.md line-endings rule), holds two
independent readings to 256, and gives specific failure messages naming the added/removed codes.
Clean; no fix needed.

## Carried S1-2 nits — all resolved
1. Anti-parallel-advice verify grep over-rejects — errs safe (over-rejects, never false-passes); all
   plans executed green in S1-3, so it never bit. Moot for shipped code (it was a plan-verify-block
   quality nit, not a shipped-code defect).
2. `13-03` DSX-NAR count check would false-fail on a pre-existing second `DSX-NAR` — confirmed
   `dsx-narrate` cites exactly one (`DSX-NAR-030`); the check was correct.
3. `13-04` anti-mutation check greps only literal `config-set` — confirmed the shipped tier block only
   *prints* `pwsh scripts/gsd-tier.ps1` as an operator instruction and executes no `config-set` /
   `mode=` / `workflow.` mutation. Advisory-only, as REQ-P13-04 requires.
4. Chart-admissibility manual read — done under finding 6 above; PASS.

## Gate evidence
- `sh scripts/check.sh` → **all checks passed** (1222 unit tests OK; catalogue current; capability
  conformant; gate contract holds; determinism holds).
- `python -m unittest tests.test_finding_catalogue_invariant -v` → **2 tests OK** (D-18 count = 256;
  D-07 set-identity `added=[] removed=[]`).
- Independent grep: 256 distinct `DSX-*` codes in `references/finding-codes.md`.

**No auto-fix commits: the review found nothing to fix.**
