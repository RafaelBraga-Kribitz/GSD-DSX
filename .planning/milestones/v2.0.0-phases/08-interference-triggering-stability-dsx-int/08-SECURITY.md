---
phase: 08
slug: interference-triggering-stability-dsx-int
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: 2026-08-14
---

# Phase 08 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

Register origin: authored at plan time. All ten `08-NN-PLAN.md` files carried a
`<threat_model>` block; the register below is their union, deduplicated by threat
identifier. No threat was constructed retroactively.

Blocking threshold: `high` (`workflow.security_block_on`). Application Security
Verification Standard (ASVS) level 1.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| spec author to gate | An `ANALYSIS-SPEC.yaml` is untrusted input written by the person the gate exists to check. Any field value can be malformed, misspelled or chosen adversarially. | Author-controlled document shape and free text |
| vocabulary membership to check logic | Whether a declared string is a recognised member of a closed vocabulary decides which check judges it. A string belonging to no vocabulary can fall between two checks and be judged by neither. | Enumerated field values |
| one check's guard to its sibling's guard | Two checks that between them cover an input space each assume the other handles what they return early on. An input both return early on is judged by neither, and neither check's own tests can see it. | Control flow, not data |
| finding severity to gate threshold | Only a CRITICAL finding blocks `dsx gate plan`. Sub-CRITICAL findings are reported and the gate still exits 0. A defect that leaves only sub-CRITICAL findings standing is a bypass even though nothing was silenced. | Finding severity labels |
| gate process to rendered report | Author-controlled strings are echoed into finding `detail` and `remedy` text a reader sees. | Author-controlled free text |
| code to its own decision trail | `dsx explain` reports the `DecisionRecord` rule text, not the code. If they disagree, an operator auditing a blocked or cleared spec is given a false account of why. | Rule prose |
| rendered report text to structured findings | An assertion against rendered text cannot tell a finding that fired from a finding code quoted inside another finding's prose. A test reading the wrong one is a control that is absent while reading as present. | Test assertions |
| test suite to the guarantees it claims to hold | A test that cannot fail is a control that is not present, while reading in the log as though it is. | Executable guarantees |
| a recorded rationale to the code it justifies | A scoping decision written into a plan and repeated in a summary becomes the reason a later round does not look again. If the rationale is false and untested, it protects the defect it was written about. | Planning prose |
| shipped docstring to reader | A citation in a docstring is read as verified fact by anyone auditing the check that points at it. | Citations and reference values |
| planning document to verifier and to future planner | Roadmap success criteria are what verification checks the phase against; requirement entry conditions are what a later milestone reads to decide what is available to build. | Tracking-file content |
| caller to math kernel | `diluted_effect` accepts two floats from any future caller. Nothing validates them upstream. | Numeric arguments |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-8-01 | Denial of Service | every `validity_frame` sub-block read, `dsx/frame/interference.py` | high | mitigate | Reads via `section()`/`items()`/`get()` with `isinstance(spec, dict)` guard, never direct indexing (`interference.py:452,484,642,757,760`). 25-cell shape table `tests/test_frame_interference.py:940-985`; AST test at `:1010` proves zero `try` nodes, so no crash is converted to a silent clean report | closed |
| T-8-02 | Denial of Service | the dispatcher's frame guard | high | mitigate | `interference.py:760-764` returns an empty report when `section(spec, "validity_frame")` is falsy and when the causal-block condition is false, before any sub-block is touched | closed |
| T-8-03 | Tampering | `dsx.mathx.diluted_effect` | high | mitigate | Closed-interval guard raising `ValueError` with the offending value echoed, `dsx/mathx.py:509-510`; both directions and both endpoints covered at `tests/test_dsx.py:180-190` | closed |
| T-8-04 | Repudiation | `Citation:` / `Reference value:` docstring paragraphs | medium | mitigate | Explicit `UNVERIFIED` marker and no-back-solving instruction, `dsx/mathx.py:497-501`; escalation recorded in `08-01-SUMMARY.md`. Test uses arbitrary inputs, not a back-solved pair | closed |
| T-8-05 | Denial of Service | the corpus test suite | medium | mitigate | Two synthetic-input proofs, `tests/test_known_bad_corpus.py:781-801`. Deviation: the map shipped with one migrated entry rather than empty, preserving a Phase 7 guarantee — documented in `08-02-SUMMARY.md` and strengthening rather than weakening the control | closed |
| T-8-06 | Repudiation | `_INCIDENTAL_GAP_CODES` | medium | mitigate | Codes measured from a real gate run and recorded verbatim; executable guard at `tests/test_known_bad_corpus.py:468`. No phase-08 commit edited the constant | closed |
| T-8-07 | Tampering | the three edited fixtures | low | accept | `git show 26c2992 --stat` → 3 files, 6 insertions / 6 deletions, all on `novelty_primacy_assessed` and `evidence`. No interference, mitigation, residual-note or window line in the diff | closed |
| T-8-08 | Spoofing | the Kohavi Chapter 22 citation | high | mitigate | `interference.py:52-61,305-318` claims the chapter for the existence and naming of the technique set only, cites the publisher index, states the running text is unreachable and that no cell in the admissibility table is quoted from the book | closed |
| T-8-09 | Information Disclosure | finding `detail` and `remedy` text | low | accept | Author-controlled local spec content echoed with the repository-wide `!r` idiom, `interference.py:217-218,357-358`. No privilege boundary crossed | closed |
| T-8-10 | Elevation of Privilege | the undeclared metric type path | medium | accept | Both declared visibility controls present: per-metric skip `DecisionRecord` at `interference.py:498-516`, and the limit stated in the finding's own `detail` at `:543-546` | closed |
| T-8-11 | Repudiation | the `brief.md` section 6.5 entry condition | medium | mitigate | `tests/test_known_bad_corpus.py:694-720` pins three required substrings with carriage-return-safe whitespace collapse | closed |
| T-8-12 | Spoofing | the Sadeghi citation | medium | mitigate | `interference.py:616-626` states the p-value attaches to Equation (9) not Equation (13), and that the Technometrics version is cited for provenance only | closed |
| T-8-13 | Elevation of Privilege | severity-to-gate-point mapping | medium | mitigate | `GATE_THRESHOLDS` (`dsx/cli.py:107-112`) untouched by phase 08; gate-level assertion at both points, `tests/test_frame_interference.py:876-905` | closed |
| T-8-14 | Tampering | `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md` | high | mitigate | `git show cb3c455` → one hunk in the ROADMAP Phase 8 block, two single-line hunks in REQUIREMENTS. Scoped replacement, no whole-file write | closed |
| T-8-15 | Repudiation | the amended success criteria | high | mitigate | Commit `cb3c455` body labels both as corrections, naming the previous claim, the falsifying source and decisions D-10 / D-12 | closed |
| T-8-16 | Denial of Service | single-writer rule for tracking files | medium | mitigate | `08-06-PLAN.md` is the only plan of the ten naming either file; tracking-file history shows no concurrent writer | closed |
| **T-8-17** | Tampering | `_check_interference_unaddressed` | **critical** | mitigate | `interference.py:202-205` — a mitigation outside `INTERFERENCE_MITIGATIONS` counts as absent. Reproduced at the real gate: `mitigation: buget_isolation` → exit 1, DSX-INT-010 CRITICAL | closed |
| T-8-18 | Tampering | `_check_interference_mitigation_admissibility` (deliberately unchanged) | high | mitigate | `git show f669607 -- dsx/frame/interference.py` → all four hunks carry context function `_check_interference_unaddressed`; no hunk inside the mirrored function. Disjointness grid `tests/test_frame_interference.py:214` | closed |
| T-8-19 | Tampering | corpus expectation maps | high | mitigate | `git show --stat f669607` → `dsx/frame/interference.py` only. Map literals unchanged | closed |
| T-8-20 | Repudiation | three controls asserting less than their names claim | high | mitigate | All three closed: positive gate assertion `tests/test_known_bad_corpus.py:446-467`; on-disk subset guard `:545`; dilution test rewritten against real partition constants `tests/test_dsx.py:164-178`, with no literal-vs-literal comparison remaining | closed |
| T-8-21 | Repudiation | `_check_triggering_dilution` decision trail | medium | mitigate | `interference.py:495-517` reads raw then normalizes only when non-blank; `None` and `""` covered at `tests/test_frame_interference.py:431` | closed |
| T-8-22 | Tampering | `examples/bad-ANALYSIS-SPEC.yaml` | medium | mitigate | `git show 7c5cfec -- examples/bad-ANALYSIS-SPEC.yaml` → exactly one line, an inline comment on a line that already carried one | closed |
| T-8-23 | Information Disclosure | the whole gate path | low | accept | Partly closed. The privilege claim holds: no credential, no personal data, no network egress on this path. The trail-location claim did not — see the Accepted Risks Log entry and the residual note below | open — below `high` threshold (non-blocking) |
| T-8-24 | Elevation of Privilege | the command-line entry point | low | accept | Repository-wide grep across `dsx/` for `subprocess`, `os.system`, `eval(`, `exec(`, `__import__`, `importlib`, `pickle.loads` → zero hits | closed |
| T-8-25 | Denial of Service | the check functions | low | accept | `interference.py` has zero `while` loops, one linear `for` over `items(spec, "metrics")`, no self-recursion; `check()` calls each helper once | closed |
| **T-8-26** | Tampering | risk guard in `_check_interference_unaddressed` | **critical** | mitigate | `interference.py:186-195` — guard is `normalized_risk == "none"` only; membership term removed. Reproduced at the real gate: `risk: shared_buget` → exit 1, DSX-INT-010 CRITICAL | closed |
| T-8-27 | Tampering | mirrored risk guard (deliberately unchanged) | high | mitigate | `git show cf4da61 -- dsx/frame/interference.py` → three hunks, all with context function `_check_interference_unaddressed` | closed |
| T-8-28 | Repudiation | the new gate-level regression test | high | mitigate | Asserts against the parsed `--json` finding list via `_gate_findings` (`tests/test_frame_interference.py:39-69`), with `where` pinned to `spec.validity_frame.interference.risk` at `:726`. Non-vacuity proved: on the committed fixture DSX-INT-010 fires and its `detail` contains the literal `DSX-SPEC-082` while `DSX-SPEC-082` is absent from the structured list — the old substring form would have passed | closed |
| T-8-29 | Tampering | corpus expectation maps | high | mitigate | `cf4da61` touched `dsx/frame/interference.py` only | closed |
| T-8-30 | Repudiation | decision trail of `_check_interference_unaddressed` | medium | mitigate | `interference.py:251-260` rule text names "a recognised member of `INTERFERENCE_RISKS` or an unrecognised string"; disjointness paragraph restated in both docstrings (`:154-167`, `:295-303`) | closed |
| T-8-31 | Denial of Service | the check functions | low | accept | As T-8-25; `_gate_findings` opens and closes one temporary directory per call | closed |
| T-8-32 | Information Disclosure | the whole gate path | low | accept | `tests/test_frame_interference.py:61-69` — `--phase-dir` points at a temporary directory on every `_gate_findings` call | closed |
| T-8-33 | Elevation of Privilege | the command-line entry point | low | accept | As T-8-24 | closed |
| **T-8-34** | Tampering | population guard in `_check_triggering_dilution` | **critical** | mitigate | `interference.py:456-463` — early return only for `triggered` or not-declared. Reproduced at the real gate: `analysis_population: eligable` → exit 1, DSX-INT-030 CRITICAL | closed |
| T-8-35 | Tampering | the corrected population guard, over-widened | high | mitigate | All five inverse cases run directly against `interference.check()` — absent, `""`, `"   "`, `"\t\n"`, `None` → no findings in every case. Full 6×5×4 risk × mitigation × note grid: zero cells fire both DSX-INT-010 and DSX-INT-011 | closed |
| T-8-36 | Tampering | `dsx.spec.ANALYSIS_POPULATIONS` as a moving target | medium | mitigate | Contract test `tests/test_frame_interference.py:475` pins the vocabulary to exactly its two members; guard comment `interference.py:464-471` names both the vocabulary and the test | closed |
| T-8-37 | Repudiation | gate-level assertions (the WR-01 defect) | high | mitigate | Positive rewritten `tests/test_frame_interference.py:541-554` with `where` pinned to `...triggering.analysis_population`; negative rewritten `:574-605` against the structured list with per-fixture exit codes | closed |
| T-8-38 | Repudiation | decision trail of `_check_triggering_dilution` | medium | mitigate | Docstring `interference.py:406-416` and `DecisionRecord.rule` `:573-579` both state the corrected condition | closed |
| T-8-39 | Tampering | corpus expectation maps | high | mitigate | `ef9fc65` touched `dsx/frame/interference.py` only; `tests/test_known_bad_corpus.py` byte-identical across 08-08, 08-09 and 08-10 | closed |
| T-8-40 | Tampering | committed fixtures under `examples/` | medium | mitigate | `_mutated_triggering_fixture` copies the tree to a temporary directory, `tests/test_frame_interference.py:335-357`; `git status --porcelain examples/` clean after a full run | closed |
| T-8-41 | Denial of Service | the check functions | low | accept | As T-8-25 | closed |
| T-8-42 | Information Disclosure | the whole gate path | low | accept | Every gate test owned by plan 08-09 routes through `_gate_findings`; `git show 12d5c56` shows only removals of inline phase-dir blocks in its favour | closed |
| T-8-43 | Elevation of Privilege | the command-line entry point | low | accept | As T-8-24 | closed |
| **T-8-44** | Tampering | risk guard in `_check_interference_mitigation_admissibility` | **critical** | mitigate | `interference.py:328-338` — vocabulary clause removed, only `== "none"` returns early; `_RISK_MITIGATION_MAP.get(..., frozenset())` at `:346`. Reproduced at the real gate: `risk: shared_buget` + `mitigation: geo_split` → exit 1, DSX-INT-011 CRITICAL, DSX-INT-010 absent | closed |
| T-8-45 | Tampering | the mitigation guard, over-widened by the same edit | high | mitigate | Surviving guard `interference.py:342` intact. All five no-mitigation shapes (absent, `""`, `None`, `none`, `"  "`) → DSX-INT-010 only, never DSX-INT-011. Grid tests `:214` (unit) and `:763` (8 real gate runs) pass | closed |
| T-8-46 | Repudiation | the prose-only rationale carried from 08-08 | high | mitigate | The unfalsified claim is now two permanent executable tests, `tests/test_frame_interference.py:214` and `:763`, both passing. This is the phase's own anti-repudiation control and it holds | closed |
| T-8-47 | Tampering | the three prose sites describing the routing | medium | mitigate | All three corrected: DSX-INT-011 docstring `:295-303`, DSX-INT-010 docstring `:154-167`, `DecisionRecord.rule` `:381-389`, which now names the `.get(..., frozenset())` lookup the code actually performs | closed |
| T-8-48 | Tampering | corpus expectation maps | high | mitigate | `5d95091` touched `dsx/frame/interference.py` only | closed |
| T-8-49 | Tampering | committed fixtures under `examples/` | medium | mitigate | `_copied_fixture` `tests/test_frame_interference.py:636-639`; `git status` clean | closed |
| T-8-50 | Repudiation | gate-level assertions in the two new gate tests | high | mitigate | Both use `_gate_findings` (`:741-757`, `:763-791`); `where` pinned to `...interference.risk` at `:755` | closed |
| T-8-51 | Denial of Service | check functions and the new gate grid | low | accept | Gate grid is exactly 2 risks × 4 mitigations = 8 real invocations (`:773-774`), one temporary directory each; unit grid bounded | closed |
| T-8-52 | Information Disclosure | the whole gate path | low | accept | Every gate test owned by plan 08-10 routes through `_gate_findings` | closed |
| T-8-53 | Elevation of Privilege | the command-line entry point | low | accept | As T-8-24 | closed |
| T-8-SC | Tampering | package-manager installs | low | accept | No `pyproject.toml`, `setup.py`, `requirements*.txt` or `setup.cfg` exists anywhere in the tree; `interference.py` imports only `__future__` and relative modules. Zero new external dependencies | closed |

*Status: open · closed · open — below `high` threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above `workflow.security_block_on` count toward `threats_open`*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-08-01 | T-8-24, T-8-33, T-8-43, T-8-53 | There is no privilege model. The command runs as the invoking user with no escalation path, no setuid component and no dynamic code execution. Verified by repository-wide grep across `dsx/` for `subprocess`, `os.system`, `eval(`, `exec(`, `__import__`, `importlib` and `pickle.loads` — zero hits. | Rafael Braga-Kribitz | 2026-08-14 |
| AR-08-02 | T-8-25, T-8-31, T-8-41, T-8-51 | Every function touched is a bounded pass over a parsed mapping with no recursion, no unbounded loop and no external call. Verified: `interference.py` has zero `while` loops and one linear `for` over the declared metrics. | Rafael Braga-Kribitz | 2026-08-14 |
| AR-08-03 | T-8-09 | Author-controlled spec content is echoed into finding `detail` and `remedy` with the repository-wide `!r` idiom. This is a local command-line report over a file the author already owns; no privilege boundary is crossed. | Rafael Braga-Kribitz | 2026-08-14 |
| AR-08-04 | T-8-10 | A metric with no declared `type` is not adjudicated, so deleting one line is a live escape from a CRITICAL check. Accepted for this milestone because firing on an undeclared type is a new requiredness rule that would newly block pre-existing configuration files — a migration decision, not a check decision. Mitigated in visibility: a per-metric skip decision record (`interference.py:498-516`) and the limit stated in the finding's own `detail` (`:543-546`). Both verified present. | Rafael Braga-Kribitz | 2026-08-14 |
| AR-08-05 | T-8-07 | The three fixture edits are bounded to six lines across three files, mechanically confirmed by `git show 26c2992 --stat`. No interference, mitigation, residual-note or window line changed. | Rafael Braga-Kribitz | 2026-08-14 |
| AR-08-06 | T-8-SC | Zero new external dependencies. No `pyproject.toml`, `setup.py`, `requirements*.txt` or `setup.cfg` exists in the tree, so no package legitimacy checkpoint applies. | Rafael Braga-Kribitz | 2026-08-14 |
| AR-08-07 | T-8-23 | **Corrected wording — the original rationale was falsified during this audit.** The privilege half stands: the tool reads a local specification file and writes findings to standard output or standard error plus a local decision-record trail; no credential, no personal data and no network egress exists on this path. The trail half did not stand. The original wording claimed "every test that writes a trail points `--phase-dir` at a fresh temporary directory, an idiom already established in both affected test modules". That was false in both modules named. The phase-08 instance is now fixed (commit `572240b`); the residual in `tests/test_dsx.py` is pre-existing and is recorded below rather than accepted silently. | Rafael Braga-Kribitz | 2026-08-14 |

---

## Residual — T-8-23, tracked and non-blocking

**What was found.** `test_good_fixture_clears_ship_resolving_sibling_artifacts_from_its_own_directory`
ran `gate ship` with no `--phase-dir` against the committed fixture. `dsx/cli.py:259`
resolves `root = args.phase_dir or str(path.parent)`, so each run appended 13,638
bytes to `examples/DECISIONS.jsonl`. That file is listed in `.gitignore:7`, so
`git status` read clean and the growth went unnoticed; it stood at 10,167,397 bytes
when this audit began.

**What was fixed.** Commit `572240b`. The omission of `--phase-dir` stays deliberate —
the good fixture's sibling artifacts must resolve from the spec's own directory — but
the whole `examples/` tree is now copied to a temporary directory first, so the
siblings come with it and the trail lands in the copy. `DECISIONS.jsonl` is excluded
from the copy so the new positive assertion proves this run wrote the trail rather
than the copy having carried it across. A second assertion pins the committed file's
size across the test. Measured after the fix: `tests.test_frame_interference` 64/64
pass, trail delta 0 bytes.

**What remains.** `tests/test_dsx.py` still appends 128,023 bytes per full-suite run
through `self._run(["gate", point, "--spec", str(fixture)])` call sites that pass no
`--phase-dir` (lines 1391, 1396, 1402, 1439, 1588, 1632, 1649, 1858 among others).
Measured per module: `test_dsx` is the only remaining writer; the other eight modules
each produce a delta of 0. Those call sites originate in the root commit `22d1b43`
and in phase 06 commits `bc2f28e`, `79fc9bb` and `34df912`, so they are outside phase
08's implementation surface and outside this register's scope. They are recorded here
rather than closed, because closing T-8-23 while the behaviour continues would repeat
exactly the failure T-8-46 exists to prevent.

**Why it does not block.** Severity `low` against a blocking threshold of `high`. The
exposure is a gitignored local file with no credential, no personal data and no
network egress on the path.

**What would close it.** Give `tests/test_dsx.py` the same temporary-directory idiom
at its remaining phase-dir-less gate call sites, then re-measure the per-module delta.

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-08-14 | 54 | 53 | 1 (low, non-blocking) | gsd-security-auditor (opus), orchestrated by `/gsd-secure-phase 08` |

### Method

- Register built from the union of ten plan-time `<threat_model>` blocks, deduplicated
  by threat identifier. No threat was constructed retroactively; no scan for new
  threats was performed, per the workflow constraint for a plan-time register.
- The four critical fail-open bypasses were each reproduced independently at the real
  gate level with a mutated fixture, rather than being accepted on the strength of the
  phase's own tests.
- The vacuous-assertion class (T-8-28, T-8-37, T-8-50) was proved non-vacuous on a
  control input, not merely confirmed present.
- Summary-only evidence was treated as insufficient for any threat at `high` or
  `critical`.
- No implementation file was modified by the auditor. The single code change in this
  audit (`572240b`) was made by the orchestrator after an explicit user decision.
- Test evidence: `python -m unittest discover -s tests -q` → 540 tests, OK.

### Unregistered observations (non-blocking, no threat mapping)

- None of the ten summaries carries a `## Threat Flags` section, so the executor
  declared no new attack surface in flight.
- `08-REVIEW.md` WR-01 concerns the DSX-INT-011 remedy rendering at
  `dsx/frame/interference.py:349-366` — output text on a reachable path, a quality
  defect rather than a control gap. Logged so it is not lost.
- `08-REVIEW.md` WR-02 (`dsx/frame/paradigm.py:219`, `alpha = as_number(...) or 0.05`
  discarding a declared `alpha: 0`) is phase 09 surface and outside this register.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed — no open threat reaches the `high` blocking threshold
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-08-14
