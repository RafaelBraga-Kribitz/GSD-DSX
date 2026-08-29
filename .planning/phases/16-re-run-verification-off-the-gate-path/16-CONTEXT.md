# Phase 16: Re-run verification (off the gate path) — Context

**Gathered:** 2026-08-29 (assumptions mode; headless ceremony — AskUserQuestion gates replaced by an Architect-led + Auditor 2-persona round per LOOP-BRIEF §4)
**Status:** Ready for planning
**Order:** 3rd of 4 in v2.2 execution order (13 → 14 → **16** → 15)
**Distinguishing feature:** unlike Phases 13 and 14 (both zero-mint), **Phase 16 mints TWO new finding codes** — `DSX-REP-060` and `DSX-REP-061` — so it carries a D-06 irreversible-numbering decision (§4) recorded loudly below and filed to HUMAN-QUEUE (HQ-11) for the operator's veto window. It carries **no D-05** (its codes are engineering-hygiene checks with no primary-source citation; brief.md line 389 assigns none).

<domain>
## Phase Boundary

Phase 16 steals DAAF's *"reproduced" verdict* without putting analysis libraries on the deterministic gate. A **skill** (`dsx-reproduce`) re-runs `reproducibility.entrypoint` and writes `REPRO-REPORT.md`; the **gate** only checks — as a pure declaration check — that the report exists (when the skill is declared in use) and that its named numbers overlap `results.tests`. Phase 12's corpus tags gain `protocol_adherence` so "the agent skipped the skill" is countable. Catch rate and false-positive rate remain the calibration numbers.

The product is: one new skill (`skills/dsx-reproduce/…` + `capabilities/dsx/capability.json` register), a new declaration-only check function in `dsx/checks/repro.py` emitting two new `DSX-REP-06x` codes, one new opt-in spec field, a `REPRO-REPORT.md` template, an additive `protocol_adherence` corpus tag, and tests (including a non-vacuous "no gate module executes the entrypoint" guard). **The gate path stays stdlib-pure; the skill — and only the skill — may execute the entrypoint.**

Scope anchor (ROADMAP.md §"Phase 16", REQ-P16-01..04):

- REQ-P16-01 — Skill `dsx-reproduce` re-runs `reproducibility.entrypoint`, compares declared `results.tests` to a fresh run, and writes `REPRO-REPORT.md`. (The **skill** may execute the entrypoint — off the gate path.)
- REQ-P16-02 — `dsx gate` at verify/ship checks that `REPRO-REPORT.md` exists (when the skill is in use) **and** that named numbers overlap `results.tests`; it **does not import pandas, scipy, or the entrypoint**. A missing interpreter on a reproduce *skill* run is **not** a gate exit 1.
- REQ-P16-03 — Remaining Phase 12 corpus cases carry a `protocol_adherence` field so skipped-skill failures are countable; **extends** REQ-P12-02 and **does not replace** catch rate or false-positive rate.
- REQ-P16-04 — A test asserts **no** `dsx/checks/` or `dsx/frame/` module executes the analysis entrypoint.

**Verified baseline (orchestrator re-ran, 2026-08-29, real commands per brief §5):**
- Catalogue = **256 codes** (`references/finding-codes.md` distinct-`DSX-*` grep = 256); `python scripts/gen-finding-catalogue.py --check` exits **0** ("finding catalogue is current"); the "declared twice" warnings (DSX-CLM-020/021, COH-030, PAR-002, SPEC-070, VAL-021/060) are the shipped-tree noise S0-2 flagged — `--check` still exits 0.
- `DSX-REP-*` family has **11 codes**, max = **`DSX-REP-053`** → the **`06x` band is free** and catalogue-consistent for a reproduce-verification code (00x seed, 01x env, 02x data, 03x entrypoint, 04x notebook, 05x repro_lock, **06x reproduce-report**).
- `dsx/checks/repro.py` is a **pure declaration check** — imports only `pathlib`, `..findings`, `..spec`; reads the spec dict + `phase_dir` (file-existence via `Path.exists`, exactly as `DSX-REP-031` already does); emits codes via `report.add`; **never** imports pandas/scipy/numpy/csv, **never** executes the entrypoint. It is already called `strict=strict` where `strict = gate_point in {verify,ship}` (`dsx/cli.py:186`), with `phase_dir` passed (`:190-191`). The new check slots into the existing `if strict:` branch beside `_check_repro_lock`.
- `repro` is in the `execute`, `verify`, and `ship` gate profiles (`dsx/cli.py:120-129`); **`verify`/`ship` block threshold = HIGH** (`:138-139`). A sub-HIGH finding cannot flip exit code at verify/ship.
- `dsx-reproduce` skill is **ABSENT**; `REPRO-REPORT` appears nowhere in `dsx/`; `reproducibility.reproduce_report` field is **free** (no collision); `protocol_adherence` field appears **nowhere** yet.
- `grep` across `dsx/` for `subprocess|runpy|exec(|import_module|__import__|os.system|popen|check_output|.run(` = **zero matches** — no gate module executes anything today; REQ-P16-04's assertion is *currently true but untested*.
- Catalogue invariant `tests/test_finding_catalogue_invariant.py` pins **`_EXPECTED_TOTAL = 256`** AND set-identity against the byte-frozen snapshot `tests/fixtures/finding-codes-phase12.md` (present, 25287 bytes). This is the guard Phases 13/14 asserted zero-mint through — **the additive-rebaseline hazard below (D-08) is real.**

**Dependency:** Phase 16 hard-depends **only** on Phase 12 (shipped). It is a *sibling* of Phase 15 with **no** declared 15↔16 edge (ROADMAP line 218). This is why it runs early — nothing waits on it and no human answer gates it (except the non-blocking D-06 veto).

**Not in scope:** any recomputation on the gate path; any tabular parser (`pandas.read_*`, stdlib `csv`) or heavy import inside a check; any `subprocess`/`runpy`/`os.system`/`exec` in a gate module; shelling the entrypoint "just to check it runs" (that is the D-02 violation the phase exists to forbid — REQ-P16-04); trusting a skill-authored PASS/FAIL verdict line instead of independently checking overlap; keying "skill in use" on `entrypoint`-presence (D-02 below); a `protocol_adherence` field on `ANALYSIS-SPEC.yaml` (D-10); mutating the Phase-12 snapshot anchor (D-08). Phase 15 owns CUPED/BI-declaration codes and their D-05 citations — Phase 16 does not touch them.
</domain>

## Persona round (LOOP-BRIEF §4)

Ran the relevant two personas concurrently, both **opus / high** (§3), on the single gray-area decision (the S3-1 open item: does REQ-P16-02's gate check need a new finding code, and if so, minted where):

- **Architect** (`dsx-analysis-architect`) — contract shape, decision rules, Phase-16-vs-15 placement.
- **Auditor** (`dsx-ml-integrity-auditor`) — gate-path-purity / leakage / calibration threat model.

**Outcome: both voted Option A unanimously.** The tie-break axis (rigour > reliability > flexibility) was **not needed** — they converged. Each raised its own questions, answered them, and voted; full reasoning is distilled into the decisions below. The orchestrator independently re-verified every load-bearing fact each persona relied on (baseline block above), not trusting the reports (brief §5).

### The decision, stated plainly

REQ-P16-02's gate must **emit a finding** to fail (exit 1) when `REPRO-REPORT.md` is missing or its declared numbers don't overlap `results.tests`. **No existing code covers this** (the 11 `DSX-REP-*` codes are all about *declarations* — seed, env, entrypoint-declared/exists, repro_lock schema — none about a *produced report existing and its numbers matching*). Three options were weighed:

- **Option A — mint in Phase 16** (extend `DSX-REP-*` with the minimum new codes, keep skill + gate together, amend the ROADMAP "only Phase 15" prose). **← CHOSEN.**
- **Option B — move REQ-P16-02's gate to Phase 15** (the designated catalogue phase). **Rejected:** fragments produce (P16-01) from enforce (P16-02) across a phase boundary, leaving a window where a reproduce report is written and believed with no gate asserting it; contaminates Phase 15's **D-05 regime** with a code that has *no* statistical citation and no reference value; mismatches family/phase (a `DSX-REP` code grafted onto a CUPED/BI phase); and *inverts* the documented dependency (P16 depends only on P12, not P15).
- **Option C — don't mint / reuse an existing code / make it advisory. Rejected:** no existing code names these defects, so reuse emits **false** finding text; the catalogue generator **dedupes by code**, so a reused code with new text leaves the count at 256 and the set-identity snapshot green — the corruption would be *invisible to both invariants*; and a sub-HIGH/advisory code cannot exit 1 at verify/ship (threshold is HIGH), so REQ-P16-02's enforcement is silently unmet.

## Decisions (loud, vetoable — LOOP-BRIEF §4)

**D-01 — Gate-path purity is inviolable (inherits D-01/D-02).** REQ-P16-02's check is **declaration-only**: `Path.exists()` + `re`/`str`/`set`/`math.isclose` over the report text, living inside `dsx/checks/repro.py`. It must never import pandas/scipy/numpy/csv, never `subprocess`/`runpy`/`os.system`/`exec`/`runpy.run_path`, and never execute the entrypoint. The **skill** (REQ-P16-01) runs the entrypoint — off the gate path. Threats to guard (from the Auditor's model): parsing the report with a tabular library (T1 — caught by the hermetic import test); a report-parser *helper* that imports pandas reached via a **dotted** `import dsx.x` (T2 — the known N1 gap in `test_gate_path_hermetic.py`; use relative `from ..x import` so its imports are walked, and/or close N1); shelling/`runpy`-ing the entrypoint (T3 — **stdlib, NOT caught by the import-based hermetic test**, which is exactly why REQ-P16-04 needs its own guard, D-09); trusting a skill verdict line (T4 — D-04); probing the interpreter to decide "in use" (T7 — D-02 forbids it).

**D-02 — "Skill is in use" is a NEW explicit opt-in field `reproducibility.reproduce_report` (a path string), NOT `entrypoint`-presence.** `entrypoint` already exists in the good D-08 fixture and most real specs; keying on it would retroactively demand `REPRO-REPORT.md` from every spec that ever declared one — a false-positive explosion and a backward-incompatible gate change that breaks the D-08 good fixture. **Absent → gate silent** (skill not in use). **Present → gate checks file-exists + numbers-overlap.** This is also what makes "a missing interpreter on a reproduce skill run is not a gate exit 1" **true by construction** — the gate never inspects interpreters, only the declared artifact. The `dsx-reproduce` skill both writes the file and stamps this field.

**D-03 — The check is strict-only (verify/ship) and early-returns on empty `results.tests`,** mirroring `_check_repro_lock`. Implement as a new helper `_check_reproduce_report(spec, repro, report, phase_dir)` called from the existing `if strict:` branch of `repro.check`. Execute-time stays silent (no results yet to reproduce). No `CHECKS`/`GATE_PROFILES` edit — `repro` is already registered.

**D-04 — "Named numbers overlap" is set-membership over a machine-readable block, not prose.** The skill writes a fenced **YAML block** in `REPRO-REPORT.md` carrying its fresh-run headline numbers keyed by metric. The gate reads that block (**CRLF-safe `\r?\n`**), and for the **lead metric** (minimum bar) asserts the report's declared value appears in / within a fixed tolerance (`math.isclose`, stdlib) of the spec's `results.tests` value. "Overlap" is deliberately **weaker than equality** (the ROADMAP says *overlap*): the smallest provable claim = the lead-claim number the human wrote in `results.tests` appears, at declared precision, in the report's machine block. **The gate recomputes nothing and independently checks overlap — it does NOT trust a skill-authored PASS/FAIL verdict line** (Auditor T4: a report whose verdict says PASS but whose numbers don't overlap must still fail the gate).

**D-05 — Two new codes, both HIGH.** `DSX-REP-060` (report **declared but missing**) and `DSX-REP-061` (report **present but numbers don't overlap**). **Two, not one:** the catalogue's own style splits "declaration absent" from "declaration points at nothing" (030/031) and repro_lock states (050–053); these two defects have **different remedies** (run the skill vs investigate why the fresh run disagrees) and **different meaning** (a process gap vs the analysis genuinely does not reproduce — the DAAF "reproduced" signal). Folding both into one code produces finding text that lies about what failed. **Both HIGH** because verify/ship block threshold is HIGH (`cli.py:138-139`) — a MEDIUM code cannot flip exit 1, silently failing REQ-P16-02.

**D-06 — [IRREVERSIBLE NUMBERING, §4] Mint `DSX-REP-060` & `DSX-REP-061` in Phase 16.** Next free numbers in the REP family (max was 053; 06x band free), catalogue-consistent. Decided by the persona round using "next free number in family, catalogue-consistent" (§4) — **not** escalated as a blocker. Proposed catalogue rows (final text finalised at S3-3):

| Code | Severity | Finding |
|---|---|---|
| `DSX-REP-060` | HIGH | Reproduce report declared (`reproducibility.reproduce_report`) but `REPRO-REPORT.md` is missing — the reproduced verdict is unsubstantiated. |
| `DSX-REP-061` | HIGH | `REPRO-REPORT.md` present but its declared re-run numbers do not overlap `results.tests` — the analysis does not reproduce. |

Recorded loudly here and **filed to HUMAN-QUEUE as HQ-11 for the D-06 veto window** (non-blocking to S3-2..S3-5; the operator may veto via the daily summary before the phase ships — §4).

**D-07 — ROADMAP "only Phase 15 extends the gate catalogue" is amended (recorded).** Phase 15 **and** Phase 16 both extend the catalogue. That line was a planning-time prose assertion, not a load-bearing invariant (the 256 snapshot was always to be rebaselined by a check-shipping phase; the requirements REQ-P16-01/02 already imply an enforcing code). The orchestrator applies a one-line recorded note at ROADMAP.md line 119 (single-writer). **This is not a §4-cat-3 scope change** — no requirement is dropped or reworded; it is a factual reconciliation of prose the requirements already contradicted.

**D-08 — Catalogue rebaseline is ADDITIVE; the Phase-12 snapshot anchor is NEVER mutated.** The invariant's set-identity test compares the current catalogue set against `finding-codes-phase12.md`. Phase 16 mints, so that test must be updated to compare current against an **explicit expected-set = phase12_set ∪ {DSX-REP-060, DSX-REP-061}** (a small, explicit delta), with `_EXPECTED_TOTAL` bumped **256 → 258**. The phase-12 snapshot file **stays byte-frozen** (it is the historical anchor Phases 13/14's git-frozen zero-mint claims reference; corrupting it would retroactively falsify them). Any code beyond `{phase12 ∪ 060 ∪ 061}` still trips the test. The mint **cannot be silent** — three pinned artifacts must move in lockstep (regen `references/finding-codes.md`, bump `_EXPECTED_TOTAL`, extend the expected-set), and S3-4 verification asserts all three moved as one. **Cross-phase note:** Phase 15 runs *after* 16 and also mints; its own rebaseline must include 060/061.

**D-09 — REQ-P16-04's test is a non-vacuous static AST scan with a positive control — distinct from the hermetic import test.** They are orthogonal: the hermetic test forbids a forbidden *import* reaching the gate closure; REQ-P16-04 forbids a gate module *executing* the entrypoint — and `subprocess`/`runpy`/`os.system` are **stdlib**, so they sail through the import-based test (Auditor T3). Design: **AST-walk every module under `dsx/checks/` and `dsx/frame/`** (this scope is *wider* than the hermetic test's GATE_PROFILES-derived roots — correctly, since a check off-profile today may be added tomorrow) and denylist the execution-primitive family: `subprocess.*`, `os.system`/`popen`/`exec*`/`spawn*`, `runpy.run_path`/`run_module`, `exec`/`eval`/`compile`, `importlib.import_module`/`__import__` on dynamic args. **Must not** confuse `ast.parse`/`ast.walk`/`ast.unparse` (legitimately used by `code.py`) with `exec`, and must not be a bare substring grep (`code.py`'s docstring contains the strings `exec`/`!pip`). **Anti-vacuity (load-bearing):** (a) assert the scan examined a **non-empty named set including `dsx/checks/code.py` and `dsx/checks/repro.py`**; (b) a **positive control** — a synthetic known-bad module calling `subprocess.run([entrypoint])` (and one `runpy.run_path(entrypoint)`) that the scanner is asserted to **flag**. Optional behavioural complement: point `entrypoint` at a poisoned script that writes a `SENTINEL`, run the verify gate, assert `SENTINEL` was never created.

**D-10 — REQ-P16-03's `protocol_adherence` is additive; the calibration numbers are pinned.** The field lives on the existing `*-ATTRIBUTION.yaml` sidecars (or a new suffix the attribution glob does **not** match) — **never** an `ANALYSIS-SPEC.yaml` key (a spec key could change gate findings or trip unknown-key schema checks). It must **not** enter the catch-rate / FPR denominators or `_headline`. Pins for "provably additive": (a) per-fixture gate-finding sets **byte-unchanged**; (b) the ABSENT denominator (`*-ATTRIBUTION.yaml` count and its `kind`-partition) and the good-corpus count **unchanged**; (c) `_headline` still returns the same `(miss_rate, fpr)` pair and `protocol_adherence` is **not** an argument to it — it is a third, independently-reported statistic, accepted-but-ignored exactly as `present` is today (`test_known_bad_corpus.py:701-714`). The existing `test_headline_is_the_absent_miss_rate_and_fpr_pair` (exact `(0.25, 0.3)`) and the invariance test stay unedited. This **extends** REQ-P12-02.

**D-11 — The "missing interpreter ≠ exit 1" ↔ `DSX-REP-061` interaction (the subtlest trap).** A legitimately skipped reproduce (interpreter absent) that still writes a report has **no fresh numbers** → a naive `061` would fire on empty overlap and produce the very exit 1 the ROADMAP forbids. The report must carry an explicit **SKIPPED/UNABLE status** (tied to `protocol_adherence`), and `061` must **short-circuit** on it — an honest opt-out analogous to `DSX-REP-051` (null repro_lock). This state must be defined in the `REPRO-REPORT.md` template and the check, or the ROADMAP's own guarantee is violated.

## Escalations & queue

- **HUMAN-QUEUE HQ-11 (filed this unit):** D-06 numbering veto window for `DSX-REP-060`/`061`. Non-blocking to S3-2..S3-5; only S5-2 drains it.
- **No D-05 owed by Phase 16.** Its codes are engineering-hygiene checks (report existence / number overlap), not statistical findings; brief.md line 389 assigns no citation, and the existing `DSX-REP-*` codes carry none. (Contrast Phase 15, which does owe D-05 reads — see HQ-8.)
- **No §4-cat-3 scope escalation.** The ROADMAP amendment (D-07) reconciles prose; it drops/rewords no requirement.
- **End-of-phase security sign-off + UAT** will be batched to HUMAN-QUEUE at S3-5, as for Phases 13/14 (HQ-9/HQ-10).

## Traps the plan (S3-2) must not paper over

1. **Trigger back-compat (D-02):** opt-in via `reproducibility.reproduce_report`, never entrypoint-presence; keep the good D-08 fixture silent; update good/bad canonical fixtures coherently.
2. **"Overlap" is load-bearing (D-04):** machine-readable YAML block, lead-metric set-membership at declared precision, explicit `math.isclose` tolerance, CRLF-safe parse — not a fragile prose regex.
3. **Catalogue-invariant collision (D-08):** additive rebaseline via an explicit `phase12 ∪ {060,061}` expected-set; do **not** mutate the phase-12 anchor; three artifacts move in lockstep.
4. **Severity (D-05):** both codes HIGH, or verify/ship won't block and REQ-P16-02's "exit 1" is silently unmet.
5. **Missing-interpreter short-circuit (D-11):** define the SKIPPED status and make `061` honour it, or the "not a gate exit 1" guarantee breaks.
6. **REQ-P16-04 must have teeth (D-09):** positive control + non-empty named scan set; static AST, not a grep; wider than GATE_PROFILES roots.
7. **`protocol_adherence` must not move calibration (D-10):** on sidecars not specs; pin catch-rate/FPR and `_headline`.
8. **Sequencing of the two catalogue-extending phases:** Phase 15 (which also mints) runs after 16; its rebaseline must include 060/061.

## Deferred / out of scope (named so they are not silently pulled in)

- Executing the entrypoint anywhere on the gate path — permanently forbidden (D-01/D-02, REQ-P16-04).
- Ratio-metric dilution / any recomputed metric on the gate — brief.md line 450, permanently out of scope (D-14).
- Phase 15's CUPED / survivorship / changing-denominator codes and their D-05 citations — Phase 15 owns them (HQ-8).
- Byte-replay reproduction guarantees — repro_lock is honest-null by design (D-locked in STATE.md); `061` checks *overlap*, not byte-identity.

## What "done" means for Phase 16 (goal-backward, for S3-4/S3-5)

REQ-P16-01: `dsx-reproduce` exists, registered, re-runs the entrypoint (in the skill), writes `REPRO-REPORT.md` with a machine-readable number block + status field. REQ-P16-02: `dsx gate verify`/`ship` emits `DSX-REP-060` when `reproduce_report` is declared but the file is missing, and `DSX-REP-061` when present-but-non-overlapping; emits neither when the field is absent or the report is honestly SKIPPED; imports no pandas/scipy and executes no entrypoint. REQ-P16-03: remaining Phase-12 corpus cases carry `protocol_adherence`; catch rate + FPR provably unchanged. REQ-P16-04: a non-vacuous, positive-controlled test proves no `dsx/checks/` or `dsx/frame/` module executes the entrypoint. Catalogue: `--check` exit 0 at **258**, invariant updated additively, phase-12 anchor untouched.
