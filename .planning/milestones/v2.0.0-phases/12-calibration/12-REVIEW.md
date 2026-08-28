---
phase: 12
reviewed: 2026-08-27T22:02:38Z
depth: deep
reviewer: gsd-code-reviewer (opus/high, adversarial)
diff_base: 297bdd2
files_reviewed: 5
files_reviewed_list:
  - dsx/cli.py
  - examples/good-corpus/_control_readout.py
  - examples/good-corpus/*-ANALYSIS-SPEC.yaml
  - examples/known-bad/*-ATTRIBUTION.yaml
  - examples/known-bad/*-ANALYSIS-SPEC.yaml
findings:
  critical: 1
  warning: 1
  info: 2
  total: 4
status: resolved
resolution:
  fixed: [CR-01, WR-01]
  by_design: [IN-01, IN-02]
  fix_commit: 4e8d1ff
---

# Phase 12: Calibration — Code Review Report

**Reviewed:** 2026-08-27T22:02:38Z
**Depth:** deep (cross-file, empirically exercised)
**Diff base:** `297bdd2..HEAD`
**Files reviewed:** `dsx/cli.py` (`cmd_stats` + `_discover_operator_trails` + subparser wiring), `examples/good-corpus/_control_readout.py`, 12 good-corpus specs, 3 known-bad ATTRIBUTION sidecars + their specs.
**Status:** issues_found

## Summary

One BLOCKER: the D-13 negative-source boundary — the single integrity control the whole
paradigm readout turns on — is **defeated for a documented invocation**. When `--root` is
pointed at or inside the `examples`/`templates` tree, the exclusion predicate strips the very
path component it filters on, so the polluted known-bad floor is counted. Reproduced live:
`dsx stats --paradigm --root examples/known-bad` reports **20 % Bayesian (> 15 %)**, which is
exactly the false auto-promotion of §6.5 item-4 that D-13/D-14 exist to prevent. The command
still returns 0, so the pollution is silent and indistinguishable from an honest split.

Everything else is sound. The dedup-by-`frame_digest` arithmetic is correct (repeated
invocations collapse; 1/(N+1) holds), the always-return-0 contract is robustly held (no raw
`KeyError`/`TypeError`/`OSError`/`JSONDecodeError` escapes to `main`), `CHECKS`/`GATE_PROFILES`
are untouched, and the catalogue stays at 256. All 12 good-corpus specs are genuinely clean
(CRITICAL = 0, HIGH = 0 under `dsx audit`, the strongest check set), and all 3 known-bad
`absent_code`s are verified genuinely non-firing on their fixtures. The remaining findings are
one Warning (a guard test whose coverage gap masks the BLOCKER) and two Info items.

## Critical Issues

### CR-01: D-13 exclusion is defeated when `--root` resolves at/inside the `examples`/`templates` tree — the polluted known-bad floor is counted, tripping the §6.5 item-4 gate

**File:** `dsx/cli.py:657-664` (`_discover_operator_trails`)

**Contract violated:** D-13 ("MUST hard-exclude any path under `examples/**` or `templates/**`";
"the harness carries a negative assertion that the command never sources the known-bad floor")
and the plan-12-02 **must-hold** prohibition "`dsx stats --paradigm` never sources the known-bad
fixture floor (`examples/known-bad/DECISIONS.jsonl`)."

**Root cause:** the exclusion tests membership of `"examples"`/`"templates"` in the trail's
**root-relative** parts:

```python
parts = trail.relative_to(root_path).parts   # strips the root prefix
if "examples" in parts or "templates" in parts:
    continue
```

`relative_to(root_path)` removes the root prefix from the component tuple. So when `root_path`
is itself the excluded directory (or a descendant of it), the `examples`/`templates` component
has already been stripped and the guard never matches — the floor is **included**.

**Failure scenario (reproduced live, this repo):**

| invocation | trails_read | distinct_frames | Bayesian share | sources the floor? |
|---|---|---|---|---|
| `dsx stats --paradigm --root .planning` (default) | 0 | 0 | — | no (safe) |
| `dsx stats --paradigm --root .` | (floor excluded) | — | — | no (safe) |
| `dsx stats --paradigm --root examples` | 2 | 20 | **15.0 %** | **YES** |
| `dsx stats --paradigm --root examples/known-bad` | 1 | 15 | **20.0 %** | **YES** |

The `--root examples/known-bad` case reports **Bayesian = 20 % > 15 %**, i.e. it would **falsely
satisfy the §6.5 item-4 promotion gate** using the exact ~45.8 %-raw / 15-distinct-frame polluted
floor D-13 was written to keep out. `--root` is a first-class, documented flag ("operator trail
search root") with no guard or warning; an operator exploring the corpus, or any script that
mis-anchors `--root`, silently gets a polluted number that is indistinguishable from an honest
operator split. The command returns 0 throughout, so nothing signals the pollution.

**Why the fallback branch does not save it:** the `except ValueError: parts = trail.parts`
branch only triggers when `relative_to` raises (cross-drive / non-descendant paths). In every
reproduced case above `relative_to` **succeeds**, so the stripped-relative parts are used.

**Suggested direction (do not apply — review only):** match the excluded components against the
trail's **resolved absolute** path, not its root-relative parts — e.g. test
`"examples" in trail.resolve().parts or "templates" in trail.resolve().parts` (optionally union
with the current relative check). That way an `examples`/`templates` component anywhere in the
real filesystem path is caught regardless of where `--root` is anchored, restoring D-13 as an
absolute boundary rather than one contingent on the caller's `--root` choice.

## Warnings

### WR-01: The `test_never_sources_the_known_bad_floor` guard has a coverage gap that masks CR-01

**File:** `tests/test_cli_stats.py` (the `test_never_sources_the_known_bad_floor` guard, per
12-02-PLAN task 1) — reliability of the D-13 guard, not production code.

**Issue:** per the plan, the guard "seed[s] a root … to contain a known-bad-shaped trail file at
an `examples/known-bad`-style path plus a `templates`-style path" **under** a synthetic root. In
that layout `relative_to(root)` keeps the `examples`/`templates` component, so the exclusion
fires and the test passes — while never exercising the one vector that defeats it: `--root`
pointed **at** the `examples`/`templates` tree (CR-01). The green guard therefore gives false
confidence that "the command never sources the known-bad floor" when in fact it does for a
documented invocation.

**Suggested direction:** add a case that sets `--root` to the excluded directory itself
(`root = <tmp>/examples`, seed `<tmp>/examples/known-bad/DECISIONS.jsonl`) and assert those
frames are still excluded. That case fails today and pins the CR-01 fix.

## Info

### IN-01: `--paradigm` is a decorative no-op flag

**File:** `dsx/cli.py:668-755` (`cmd_stats`); flag defined at `dsx/cli.py:1008-1009`.

**Issue:** `cmd_stats` never reads `args.paradigm`. `dsx stats` (bare) and `dsx stats
--paradigm` produce byte-identical output (verified: bare `dsx stats` in this repo prints the
paradigm split and exits 0). No incorrect behavior today, but the documented contract
"`--paradigm` selects the split" is unenforced, and if a second `stats` sub-report is ever added
keyed on another flag, bare `stats` will still emit the paradigm split unconditionally.

**Suggested direction:** either gate the paradigm report on `args.paradigm` (and print usage /
a report menu when absent), or drop the flag and document that `dsx stats` reports the paradigm
split by default. Low priority.

### IN-02: `retracted-fabricated-field-experiment` attribution — `absent_code` is one the sidecar itself says would not catch the miss

**File:** `examples/known-bad/retracted-fabricated-field-experiment-ATTRIBUTION.yaml:12-21`

**Issue:** `absent_code: DSX-REP-020` is verified genuinely non-firing on the fixture (confirmed:
the fixture fires `DSX-REP-010/011/030/050` but **not** `DSX-REP-020`), so it satisfies D-07
mechanically. But D-05 polarity requires the tag name a code that **would have caught** the miss,
and the sidecar's own rationale states DSX-REP-020 would **not** catch the fabrication ("the
fabrication is downstream of what the declaration exposes … which a declaration-only gate
structurally cannot do"). As a "would-have-caught" attribution promoting §6.5 item-7 it is a
stretch: the code named is the *nearest* provenance code, not one whose presence would flip the
outcome. Contrast the other two sidecars (DSX-EXP-051, DSX-VAL-080), whose rationales credibly
tie the absent code to the specific undetected pathology.

**Suggested direction:** either recast the rationale to name item-7's provenance work as the
genuine absent capability (and treat DSX-REP-020 as the "nearest shipped anchor" explicitly), or
confirm with the Statistician that "nearest-anchor" polarity is acceptable for the item-7 count.
Judgment call, not a mechanical defect.

## Adversarial cases tried that did NOT break the code (reproduce to confirm)

- **Dedup arithmetic (D-14):** N distinct frequentist frames each repeated many times as
  invocation records + 1 Bayesian frame ⇒ share is 1/(N+1) over distinct `frame_digest`, not the
  raw-record proportion. `digests_seen` is a `set`, `local_inv` is reset per file so cross-file
  `invocation_id` collisions cannot cross-contaminate, and `digest_paradigm` keyed on the content
  hash is collision-safe because paradigm lives inside the digest-hashed `inference` block. Holds.
- **Always-return-0 (D-12):** empty root, missing `.planning`, undecodable/half-written
  `DECISIONS.jsonl`, invocation records lacking `frame_digest`, decision records with
  `choice="paradigm="` (empty) or out-of-vocab values, and zero distinct frames all degrade to an
  honest "no operator history yet" with no division by zero. `read_all` never raises; the whole
  aggregation is wrapped in `except Exception` (control-flow signals left to propagate) and
  `result["root"]` is set before the guarded block, so the fallback `_print_stats` cannot
  `KeyError`. No raw `KeyError`/`TypeError`/`OSError`/`JSONDecodeError` reaches `main`.
- **Substring vs component exclusion:** a directory named `examples-archive` is correctly **not**
  excluded (the guard uses `in <parts-tuple>`, exact component match, not substring). This part of
  the predicate is right — the defect (CR-01) is the *relative_to* stripping, a different bug.
- **`--block-on` rejection (D-18):** `dsx stats --paradigm --block-on high` exits 2 (argparse
  rejects the unknown flag); `stats` is absent from `CHECKS` and `GATE_PROFILES` (diff confirms
  only comment/docstring hits). No gate registration.
- **Catalogue invariant (D-18):** total remains **256**; all three `absent_code`s
  (`DSX-EXP-051`, `DSX-VAL-080`, `DSX-REP-020`) are shipped catalogue codes, so no code is minted.
- **Good-corpus cleanliness (D-04):** all 12 specs yield CRITICAL = 0, HIGH = 0 under
  `dsx audit --spec … --json` (audit runs every check ⊇ any gate profile, so they are clean at
  every gate point too). The FPR denominator is a genuinely-clean set; none silently fires.
- **`_control_readout.py`:** a pure `return 0` no-op — it resolves **no** paths, so the
  hypothesized "breaks when run from a different cwd" vector does not exist. The `reproducibility.
  entrypoint` string resolves from repo root (good specs do not fire `DSX-REP-030/031`). Clean.

---

## Resolution (2026-08-27, S3-5 — orchestrator, §4 persona round)

Every finding was independently reproduced by the orchestrator before any change
(§5 — the reviewer's claim was never trusted). Dispositions settled by a §4
persona round (**Auditor** `dsx-ml-integrity-auditor` + **Architect**
`dsx-analysis-architect`, both opus; tie-break rigour > reliability > flexibility).

| # | Disposition | Detail |
|---|---|---|
| **CR-01** | **FIXED** (`4e8d1ff`) | Confirmed live: `--root examples/known-bad` → 20% Bayesian (sourced the D-13-forbidden floor), `--root examples` → 15%; default `--root .planning` safe, recorded readout unaffected. Both personas voted FIX-NOW (unanimous): a *never-leak* boundary defeatable through a documented flag, with a green guard test masking it, is an evaluation defect in the terminal calibration phase. **Fix-form was the split vote** — Auditor: F-resolve (fail-safe on leakage, closes symlink + Windows-case aliasing); Architect: F-asgiven (minimal correction, no dependence on absolute checkout location). **Resolved on rigour → F-resolve + case-fold:** D-13 is fundamentally a no-leak invariant, so the residual must fail SAFE (over-exclude → empty readout) not UNSAFE (leak via alias). Match `{examples, templates}` against `{p.lower() for p in trail.resolve().parts}`. Architect's reproducibility concern captured as a documented known-limit: a repo checked out under an ancestor literally named `examples`/`templates` over-excludes (fails safe). Live after fix: all three `--root`-at-floor invocations report "no operator history … (examples/ and templates/ excluded)"; default stays empty/exit 0. |
| **WR-01** | **FIXED** (`4e8d1ff`) | The guard test only ever placed the floor UNDER a synthetic root, never pointed `--root` AT it — the exact CR-01 vector. Added `test_root_pointed_at_the_floor_still_excludes_it` (the CR-01 vector: 20% Bayesian before, excluded after) + `test_excluded_component_match_is_case_folded`. Folded into the same commit. |
| **IN-01** | **BY-DESIGN** (intent comment added, `4e8d1ff`) | Both personas voted BY-DESIGN. `--paradigm`'s help text is *accurate* (unlike the `--block-on` false-safety precedent) — the split IS what the command reports, so bare `dsx stats` reporting the same split is not a false contract, merely a forward-compat report selector with one current value. Tightening it would alter a shipped, tested surface in the terminal phase for no correctness gain. One-line intent comment added so the no-op reads as intentional. |
| **IN-02** | **BY-DESIGN / already-disclosed** | `retracted-fabricated` sidecar's `absent_code: DSX-REP-020` references a shipped code (D-18-clean) and is verified genuinely non-firing (D-07 mechanically satisfied). The "nearest-anchor not would-have-caught" polarity concern is *transparently stated in the sidecar's own rationale* ("the fabrication is downstream of what the declaration exposes … which a declaration-only gate structurally cannot do") and was already adjudicated — ledger S3-3 Wave 1 flagged it as the least-bad honest fit for a structurally-uncatchable authenticity class, and 12-READOUT.md F2 qualified it ("only retracted-fabricated is uncatchable regardless of authoring"). No change; the honest flag stands. |

**Residual vectors recorded (not fixed — documented limits):** (a) a repo checked
out under an ancestor named `examples`/`templates` over-excludes (fails safe);
(b) a floor copied under a filename other than `DECISIONS.jsonl` is invisible to
both discovery and guard — out of CR-01 scope, worth a D-13 note. **This whole
disposition set is loud and vetoable via the daily summary / HQ veto window** —
it is a reversible code decision, not a HUMAN-QUEUE category.

_Reviewed: 2026-08-27T22:02:38Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep_
_Resolved: 2026-08-27 (S3-5) — CR-01/WR-01 fixed, IN-01/IN-02 by-design_
