# Phase 27 — Feature-origin-only leak mint: harness-wiring RESEARCH

**Researched:** 2026-09-07
**Domain:** dsx corpus-fixture promotion + single-code mint (DSX-ML-034) + finding-catalogue/harness wiring
**Confidence:** HIGH (every claim carries a `path:line` locator read this session; interpreter used for nothing here — pure static read, no gate re-run)

> Scope: this is the S3-2 *plan-input* research. It describes HOW to wire the mint so the
> full suite stays green and the catalogue goes 276 → 277. It authors NO source/test code
> and proposes NO change to the frozen contract (27-CONTEXT.md D-27-01/02, guardrail 1).

---

## User Constraints (frozen contract — DO NOT re-open)

Locked in `27-CONTEXT.md` and `27-MEASUREMENT.md`:

- **D-27-01 (FROZEN case shape):** churn fixture, leaky column `account_health_index`
  (matches none of the 10 `LEAKAGE_PATTERNS`), honest declarations incl. **both**
  `train_score` AND `test_score`, temporal split, complete `selection_ledger`, beaten
  baseline, declared calibration. `27-CONTEXT.md:58-86`.
- **D-27-02 (FROZEN pass/fail rule):** LIVE MISS confirmed. `27-CONTEXT.md:88-116`.
- **LIVE MISS measured** at four points; ship residuals = `DSX-CLM-031, DSX-COH-031,
  DSX-MET-040, DSX-NAR-001`, all swap-invariant incidental corpus gaps. `27-MEASUREMENT.md:46-95`.
- **BINDING marker honesty (§S3-1-CLOSE):** the `# D-05:` marker AND the DSX-ML-034
  docstring MUST describe Kaufman as **"secondary-corroborated, primary PDF paywalled"**
  and MUST NOT claim a first-hand read of the ACM PDF. `27-CONTEXT.md:196-200`.
- **Mint scope (§S3-1-CLOSE):** `model.feature_provenance[]` vocab ADOPTED
  `{feature, source, available_at, derived_from}`, `available_at ∈
  before_prediction|at_prediction|after_prediction|unknown`; CRITICAL on
  `after_prediction`, HIGH on `unknown` without a waiver; attribution NOT detection (a
  spec that lies still passes). `27-CONTEXT.md:202-214`.
- **`dsx/checks/dq.py` stays byte-frozen** (brief standing rule). The mint touches
  `dsx/checks/ml.py` only; dq.py is not in scope — confirmed nothing in this plan reads
  or writes dq.py.

---

## Phase Requirements

| ID | Description (`.planning/REQUIREMENTS.md:71-91`) | Research support |
|----|-------------------------------------------------|------------------|
| REQ-P27-01 | Known-bad case — spec, entrypoint, **postmortem**, ATTRIBUTION sidecar; leak attributable only through feature origin; measured live before any check designed | §A (fixture files), §B (sidecar), measurement already recorded in `27-MEASUREMENT.md` |
| REQ-P27-02 | On live miss: optional `model.feature_provenance[]` + declaration-only check (CRITICAL `after_prediction`, HIGH `unknown`); D-05 Kaufman confirmed; D-06 next-free `DSX-ML-*` number | §D (check idiom + placement), §B/§C (DSX-ML-034 slot free) |
| REQ-P27-03 | Corpus harness entries complete (target maps, golden ship ledger, validity-frame map, spec count, sidecar with reserved `absent_code`); §6.5 item 7 row rewritten with measured evidence | §C (every harness map + count) |

---

## Summary

The spike fixture is already MEASURED as a LIVE MISS. S3-2/S3-3 is almost pure wiring:
(1) copy three spike files into `examples/known-bad/` under a corpus basename plus a NEW
`-POSTMORTEM.md` (postmortems are REQUIRED by the corpus pairing test); (2) add a
declaration-only `_check_feature_provenance` to `dsx/checks/ml.py` emitting **DSX-ML-034**;
(3) register the fixture as a **MISS** in four harness maps and bump three count pins;
(4) add DSX-ML-034 to the generator's `_D05_ALLOWLIST_CODES` and regenerate the catalogue
(276 → 277, auto-generated — never hand-edited); (5) write the ATTRIBUTION sidecar.

**Primary recommendation:** corpus basename **`feature-origin-only-leak`** (aligns REQ §6.5
item 7 wording + phase dir; spike used the shorter `feature-origin-leak`). The catalogue is
generated from `report.add(...)` AST call-sites, so the row and total move automatically.

**Three contract-vs-harness discrepancies (top risks — see end):** the `promotes_backlog_item`
id and the `_SECTION_65_BACKLOG_CODES` placement stated in 27-CONTEXT.md's authoring notes
both contradict the FROZEN harness; and DSX-ML-034 at two severities collides in the
one-code-one-row catalogue generator. All three are wiring-note conflicts, not case-shape
edits (guardrail 1 intact).

---

## A. Fixture promotion — naming, files, placement

**Sibling convention** (`ls examples/known-bad | grep full-frame`): a known-bad fixture
carries exactly three companion files:
- `full-frame-cleaning-ANALYSIS-SPEC.yaml`
- `full-frame-cleaning-entrypoint.py`
- `full-frame-cleaning-POSTMORTEM.md`

**Which are REQUIRED (verified against the harness):**
- **ANALYSIS-SPEC.yaml — REQUIRED.** Discovered by glob; must load and pass `dsx validate`
  exit 0 (`tests/test_known_bad_corpus.py:1107-1123`).
- **POSTMORTEM.md — REQUIRED.** Symmetric pairing: `spec_slugs ^ postmortem_slugs` must be
  empty (`tests/test_known_bad_corpus.py:1056-1063`). It MUST contain at least one
  `DSX-<LETTERS>-<digits>` code (`:1125-1134`, regex `_FINDING_CODE_RE` at `:51`). The spike
  has NO postmortem — one must be **authored new** (record the four-point measured table +
  the absent DSX-ML-034 attribution).
- **ATTRIBUTION.yaml — REQUIRED here (optional in general).** Sidecars are optional per D-03,
  discovered by `*-ATTRIBUTION.yaml` glob; needed because this is a MISS (§B).
- **NARRATIVE.md — NOT required.** No corpus test references a narrative sibling; the
  ship-time `DSX-NAR-001` (missing `narrative.path`) is an accepted incidental gap, not a
  missing-file failure.
- **No CSV / data extract needed.** The entrypoint is read as **text**, never executed
  (`spike/feature-origin-leak-entrypoint.py:2-3`; harness seeds only the declared entrypoint
  into the tempdir — `tests/test_known_bad_corpus.py` `_seed_entrypoint` mirrors
  `spike/...MEASURE.py:43-55`). The declared `account_churn_features.csv` is synthetic in
  narrative only; the reproducibility check tests that the declared path *exists*, not that
  it runs.

**Exact file list the plan must create** (basename `feature-origin-only-leak`):

| Spike source | → Promoted target |
|---|---|
| `spike/feature-origin-leak-ANALYSIS-SPEC.yaml` | `examples/known-bad/feature-origin-only-leak-ANALYSIS-SPEC.yaml` |
| `spike/feature-origin-leak-entrypoint.py` | `examples/known-bad/feature-origin-only-leak-entrypoint.py` |
| — (author new) | `examples/known-bad/feature-origin-only-leak-POSTMORTEM.md` |
| — (author new) | `examples/known-bad/feature-origin-only-leak-ATTRIBUTION.yaml` |

**Edits inside the promoted spec** (vs spike `feature-origin-leak-ANALYSIS-SPEC.yaml`):
- `spec_id: "feature-origin-leak"` → `spec_id: "feature-origin-only-leak"` (spike line 25;
  full-frame precedent `spec_id` == basename at `full-frame-cleaning-ANALYSIS-SPEC.yaml:38`).
- `reproducibility.entrypoint: feature-origin-leak-entrypoint.py` (spike line 124) →
  `feature-origin-only-leak-entrypoint.py`.
- Strip the "spike / NOT a committed corpus fixture" header (spike lines 1-21); replace with
  a corpus header naming REQ-P27-01/02/03 (full-frame precedent header at
  `full-frame-cleaning-ANALYSIS-SPEC.yaml:1-34`).
- **Do NOT add a `model.feature_provenance[]` block.** The fixture must stay a MISS: DSX-ML-034
  fires only on a *declared* `after_prediction`/`unknown`, so omitting the block keeps it
  silent (see §C falsifiability). Adding the block would turn the miss into a catch and break
  `kind: miss`.

**Determinism:** the spec/entrypoint are static text; no timestamps or nondeterministic
content. Byte-stability is automatic once committed.

---

## B. ATTRIBUTION sidecar — exact schema

All three existing sidecars share one schema (read verbatim):
- `retracted-fabricated-field-experiment-ATTRIBUTION.yaml:14-21`
- `operator-known-answer-selective-exclusion-ATTRIBUTION.yaml:14-21`
- `garden-of-forking-paths-p-hacking-ATTRIBUTION.yaml:18-25`

**Fields** (from the sidecar comment blocks + the enforcing test at
`tests/test_known_bad_corpus.py:1584-1657`):

| Field | Required? | Convention |
|---|---|---|
| `absent_code` | **REQUIRED** | Must be in the validated union = 256+ catalogue codes ∪ `_SECTION_65_BACKLOG_CODES` (`:1640-1645`). Value form `DSX-[A-Z]+-\d+`. |
| `promotes_backlog_item` | **REQUIRED** | Must be one of the nine ids in `_SECTION_65_ITEM_IDS` (`:1646-1651`, frozenset at `:832-842`). |
| `kind` | optional (default `"miss"`) | `"miss"` or `"caught"` only (`:1652-1657`). |
| `protocol_adherence` | optional but **de-facto required** | Closed vocab `adhered|skipped|not_applicable`; every sidecar must carry it and at least one must be `skipped` (`tests/test_known_bad_corpus.py:1659-1710`). Use `skipped`. |
| `rationale` | optional | Free prose; the existing three all include it. |

**How `absent_code` is read + what it means:** an `absent_code` is *the code that SHOULD
catch the miss but did not*. For `kind: miss` the live-falsifiability test asserts the code
fires **NOWHERE CRITICAL** across all four gate points (`tests/test_known_bad_corpus.py:
1712-1760`, esp. `:1753-1760`). A named §6.5 backlog code (unshipped) trivially satisfies this
by being absent from the catalogue; a **shipped** code satisfies it only if the live gate does
not raise it CRITICAL on the fixture.

**Exact sidecar the plan must write:**
```yaml
absent_code: DSX-ML-034
promotes_backlog_item: "6.5-item-7-feature-provenance"   # see RISK 1 — this is the
                                                          # harness-valid id, NOT the
                                                          # "-feature-origin-only-leak"
                                                          # string in 27-CONTEXT.md:214
kind: miss
protocol_adherence: skipped
rationale: >
  ...the leak is attributable only through feature origin; the minted DSX-ML-034 reads
  declared model.feature_provenance[] and this honest spec declares no such block, so the
  code correctly stays silent — attribution, not detection (a spec that lies still passes).
```

**Canonical id list — the EXACT string for item 7** (`tests/test_known_bad_corpus.py:832-842`):
```
6.5-item-1-prior-justification-and-sensitivity
6.5-item-2-prior-predictive-check
6.5-item-3-convergence-declarations
6.5-item-4-bayesian-admissibility
6.5-item-5-quiz-fading-mode
6.5-item-6-ratio-metric-dilution
6.5-item-7-feature-provenance          ← item 7, line 839
6.5-item-8-magnitude-without-computed-effect
6.5-item-9-subgroup-harm-declaration
```
So `promotes_backlog_item` **MUST equal `6.5-item-7-feature-provenance`** — the same id the
existing `retracted-fabricated-field-experiment-ATTRIBUTION.yaml:15` already uses. Two
sidecars promoting the same item is allowed (no uniqueness constraint in `:1584-1657`).

---

## C. Harness entries — every file, symbol, locator, edit

Slug used below = corpus basename `feature-origin-only-leak`. Every map is glob-discovered
and enforces key parity, so a missing entry fails the suite loudly.

### C1 — `tests/test_known_bad_corpus.py`
- **`_EXPECTED_CAUGHT_DEFECTS`** (`:432-540`) — add `"feature-origin-only-leak": frozenset()`.
  Empty by design (a MISS), exactly like the three coverage-class misses at `:475-477`.
  Key-parity enforced at `test_expected_caught_defects_keys_match_the_corpus_on_disk`
  (`:1342-1354`).
- **`_TARGET_DEFECT_CODES`** (`:185-274`) — **NO entry.** The fixture catches nothing at any
  point; misses are absent from this map (the three coverage misses are not keyed here). Key
  set is a subset of disk (`:1356-1372`), so omission is legal.
- **`_INCIDENTAL_GAP_CODES`** (`:65-101`) — **NO edit.** All four ship residuals already
  present: `DSX-CLM-031` (`:66`), `DSX-COH-031` (`:67`), `DSX-MET-040` (`:84`), `DSX-NAR-001`
  (`:85`). The ship-completeness test (`:1279-1320`) passes because every verify/ship residual
  is already documented.
- **`_SECTION_65_BACKLOG_CODES`** (`:819-824`) — **NO edit.** DSX-ML-034 ships in the catalogue,
  so it must NOT be added here: the disjointness assertion `_SECTION_65_BACKLOG_CODES ∩
  catalogue == ∅` (`:1606-1611`) would fail. (Contradicts 27-CONTEXT.md wording — RISK 2.)
- **Falsifiability** (`test_attribution_tags_are_falsifiable_against_live_gate`, `:1712-1760`):
  the plan must confirm DSX-ML-034 does NOT fire CRITICAL on the promoted fixture at any of the
  four points. Guaranteed because the fixture declares no `feature_provenance` block.

### C2 — `tests/test_frame_val.py`
- **`_EXPECTED_VAL_CODES`** (`:1363-1466`) — add
  `"feature-origin-only-leak-ANALYSIS-SPEC.yaml": set()`. Discovery globs
  `examples/known-bad/*-ANALYSIS-SPEC.yaml` (`:610`); `test_discovered_fixture_set_equals_the_
  expected_dictionarys_key_set` (`:1482-1500`) fails if the fixture is found with no entry.
  Value is **measured, not guessed** — run `dsx.frame.val.check(load(spec))` on the promoted
  fixture; expected `set()` because the validity_frame is a wholesale clone of full-frame's
  (which measured `set()` at `:1398`) and DSX-ML-034 is a `DSX-ML-*` code, not `DSX-VAL-*`.

### C3 — `tests/test_causal_verb_golden.py`
- **`_GOLDEN_SHIP_FINDINGS`** (`:82-...`, keyed by repo-relative posix path) — add
  `"examples/known-bad/feature-origin-only-leak-ANALYSIS-SPEC.yaml":
  frozenset({"DSX-CLM-031", "DSX-COH-031", "DSX-MET-040", "DSX-NAR-001"})`.
  This is the measured ship set from `27-MEASUREMENT.md:52` (ship row). It is **smaller** than
  full-frame's golden set (`:161-164`) because this fixture has no code defect (no
  DSX-CODE-020/021/030), a complete `selection_ledger` (no DSX-ML-090), and declares **no**
  `comparisons_looked_at` (verified absent in spike spec) so DSX-EXP-051 does not fire.
  Key parity enforced at `test_golden_keys_match_the_examples_tree_on_disk` (`:357-370`);
  per-fixture equality re-measured live at `:372-394` (must MEASURE the promoted fixture after
  the mint — DSX-ML-034 must not appear, which holds since no provenance block is declared).

### C4 — `tests/test_dsx.py` (spec count)
- **Live number is 42**, not asserted elsewhere: `self.assertEqual(len(paths), 42, ...)` at
  `tests/test_dsx.py:579`. Glob = `examples/*-ANALYSIS-SPEC.yaml` (2) + `examples/known-bad/
  *-ANALYSIS-SPEC.yaml` (39 on disk) + `templates/ANALYSIS-SPEC.yaml` (1) = 42 (`:574-577`).
  Promoting one corpus fixture → **43**. Edit `42` → `43` and update the running-tally comment
  at `:565-569`. The test also asserts every fixture has `validity_frame.estimand.type ∈
  ESTIMAND_TYPES` (`:582-585`); the cloned `difference_in_proportions` (spike spec line 162)
  already passes for full-frame, so no risk.

### C5 — `scripts/gen-finding-catalogue.py`
- **`_D05_ALLOWLIST_CODES`** (`:183-203`) — **add `"DSX-ML-034"`** (exact-code, NOT a
  `"DSX-ML-"` prefix — `DSX-ML-*` is a pre-existing family whose legacy codes carry no
  citation; prefix-adding would fail the build red, per the precedent comment at `:111-137`).
  This is the ONLY generator edit.
- **`_SECTION_65_BACKLOG_CODES` does NOT exist in this script.** The task brief was inaccurate
  here — grepped the whole file; the only §6.5 backlog constant lives in
  `tests/test_known_bad_corpus.py:819`, and DSX-ML-034 must not go there (§C1 / RISK 2).
- The catalogue is **generated** from `report.add(...)` AST call-sites (`collect()` `:275-292`,
  `render()` `:295-325`); `references/finding-codes.md` is not hand-edited ("Do not edit by
  hand", `:299`). Adding the check's `report.add("DSX-ML-034", ...)` + running
  `--write` produces the new row and bumps `Total:` automatically.

### C6 — `tests/test_phase20_zero_mint_close.py` (precedent + a REQUIRED count edit)
- **Pattern to mirror:** Phase 20 minted zero codes; the module pins the LIVE catalogue total
  and proves the zero-mint via an untouched reserve band, not the absolute total (`:1-38`).
- **REQUIRED edit:** `self.assertEqual(_declared_total(_CATALOGUE), 276, ...)` at
  `tests/test_phase20_zero_mint_close.py:98-102` must become **277** (this is a real mint).
  Docstring/method-name literals mention 276 (cosmetic; update for honesty).
- **Invariant a MINT must satisfy:** the DSX-STA reserve-band test (`:135-151`, max STA == 122,
  123+ absent) stays GREEN because DSX-ML-034 is in the `DSX-ML` family, not `DSX-STA` — so
  Phase 20's zero-mint tell is undisturbed; only the count-pin moves.

### C6b — `tests/test_finding_catalogue_invariant.py` (REQUIRED count edit, not in brief)
- `_EXPECTED_TOTAL = 276` at `tests/test_finding_catalogue_invariant.py:39` → **277**. The
  test reads `Total:` and the enumerated row count and requires both == `_EXPECTED_TOTAL`
  (`:65-93`). Method name `test_finding_catalogue_stays_at_276_codes` (`:65`) is cosmetic. The
  Phase-12 snapshot pin (256) is unrelated and stays frozen.

### C7 — `references/finding-codes.md`
- **034 slot is FREE.** The leakage-features 03x family runs 030/031/032/033 then jumps to
  040 (`references/finding-codes.md:159-163`); 034-039 unused. A `feature_provenance`/
  feature-availability check belongs in 03x, so DSX-ML-034 is the next-free-in-family slot
  (matches D-27-03 `27-CONTEXT.md:120-126`).
- **Row format** (surrounding rows verbatim): `| \`DSX-ML-033\` | MEDIUM | model.prediction_time_definition is not declared |` (`:162`); the generated DSX-ML-034 row will slot between 033 (`:162`) and 040 (`:163`) because `collect()` sorts by code string (`gen-finding-catalogue.py:286`). Title text comes from the `report.add` third arg.
- **Total row** `**Total: 276 codes.**` (`:16`) → **277** after `--write`. Post-mint
  expectation confirmed: **276 → 277**.

---

## D. The check itself — placement and idiom (`dsx/checks/ml.py`)

**Dispatcher:** `check()` at `dsx/checks/ml.py:122-156` calls per-concern helpers; add a
`_check_feature_provenance(model, report)` call in the model-present block (alongside
`_check_features` at `:148`). It must **return early when `model.get("feature_provenance")`
is absent/empty** so every existing spec (and the fixture) still validates — additive/optional.

**Read idiom** (mirror `_check_features` `:473-527`): read the list off the parsed spec
(`model.get(...)`), `normalize()` string fields, iterate entries. No warehouse/data access —
declaration-only, consistent with the whole gate path (`27-CONTEXT.md:34-43`).

**Emit idiom** (severity is a **string literal** — required by the catalogue extractor, which
skips any `report.add` whose severity arg is not a literal, `gen-finding-catalogue.py:237-241`):
```
report.add("DSX-ML-034", "CRITICAL", "<title>", detail=..., remedy=..., where="spec.model.feature_provenance")   # available_at == after_prediction
report.add("DSX-ML-034", "HIGH",     "<title>", detail=..., remedy=..., where=...)                                # available_at == unknown, no waiver
```
Example severity/`report.add` shapes to copy: `_check_features` DSX-ML-031 CRITICAL (`:491-497`)
and DSX-ML-032 HIGH (`:510-525`).

**Severity map (per §S3-1-CLOSE consequence 1, `27-CONTEXT.md:206-209`):**
- `available_at: after_prediction` → **CRITICAL**.
- `available_at: unknown` **and** no waiver → **HIGH**.
- `before_prediction` / `at_prediction` → no finding (optionally `report.ok(...)`).
- Standing limit: **attribution, not detection** — a spec that omits or lies in the block still
  passes; the check reads declarations only (`27-CONTEXT.md:208-209`).

**D-05 docstring gate** (`check_d05` `gen-finding-catalogue.py:385-415`) requires the enclosing
function's docstring to contain:
1. a `Citation:` line (regex `^\s*Citation:\s*\S`, `:205`), and
2. a `Reference value:` OR `Structural criterion:` line (`:206-208`), and
3. a `# D-05: DSX-ML-034` marker somewhere under `tests/` (regex `:209`).

**Kaufman citation format to mirror + the BINDING honesty add:** `_check_cleaning` already
cites Kaufman for DSX-ML-023 at `dsx/checks/ml.py:328-340`, and already hedges the locator
("the ACM Digital Library PDF was not independently paginated in this session; do not invent a
locator", `:337-340`). DSX-ML-034's docstring must go further per `27-CONTEXT.md:196-200`:
describe the citation as **"secondary-corroborated, primary PDF paywalled"** and NOT claim a
first-hand read, in BOTH the docstring `Citation:` block AND beside the `# D-05: DSX-ML-034`
test marker. (The existing -023 citation is out of scope — do not touch it.)

`# D-05:` marker precedent for the ML family (comment in a test file): `tests/test_dsx.py:1223`
`# D-05: DSX-ML-043`, `:1334` `-052`, `:1521` `-090`. The plan adds a
`# D-05: DSX-ML-034` marker in the new DSX-ML-034 unit test.

**ANALYSIS-SPEC schema validator — no change REQUIRED to validate the block.**
`_validate_model_shape` (`dsx/spec.py:1254-1282`) only checks `task`, `split`, `target`; it
does NOT enumerate allowed model keys, so a `feature_provenance` block is silently accepted and
existing specs without it still validate (additive/optional, confirmed). The closed
`available_at` vocabulary is enforced by the new check in `ml.py`, not by the spec-shape
validator. (Optional: a `feature_provenance` vocabulary entry could be added to `spec.py`'s
`_VOCABULARIES` at `:707`, but it is not required for the mint to pass — treat as discretionary.)

**`dsx/checks/dq.py` byte-frozen:** confirmed the mint touches only `ml.py`; dq.py is not read
or written by any step above.

---

## E. Gate / count expectations the plan must pin

| Pin | From | To | Locator |
|---|---|---|---|
| Finding catalogue total | 276 | **277** | `references/finding-codes.md:16` (regenerated) |
| `_EXPECTED_TOTAL` | 276 | **277** | `tests/test_finding_catalogue_invariant.py:39` |
| Phase-20 total assert | 276 | **277** | `tests/test_phase20_zero_mint_close.py:99` |
| Spec-count assert | 42 | **43** | `tests/test_dsx.py:579` |
| Corpus fixtures on disk | 39 | 40 | (no hard count assert; map key-parity only) |

- **Full-suite count:** last recorded green was 1590 OK for Phase 26 (per Log). Promoting the
  fixture + minting the check ADD several tests (new golden/val/caught-defect subtests via
  glob-discovery, plus the new DSX-ML-034 unit test with its `# D-05:` marker). Exact delta is
  **UNVERIFIED — needs plan-time `python312 -m unittest` count** after the fixture+check land.
- **`node install.mjs --check`** must pass at phase end. install.mjs syncs `dsx`, `references`,
  `templates`, `examples` into the overlay (`install.mjs:42-46`). This phase edits `dsx/`
  (ml.py), `references/` (regenerated catalogue), and `examples/` (new fixture+sidecar+
  postmortem) — all three are synced, so `--force` re-install then `--check` is required.
  `tests/` and `scripts/` are NOT synced, so editing them does not affect `install --check`.
  `templates/` is only touched if the plan chooses to add the optional provenance field to the
  template (NOT required).
- **Determinism / byte-stability:** the fixture is static text (no timestamps). The catalogue
  is deterministically regenerated (`collect()` sorts by code, `:286`). The one caveat is the
  duplicate-severity warning in RISK 3.

---

## Runtime State Inventory (rename/refactor categories)

This is an additive mint, not a rename — but the basename choice touches several map keys:

| Category | Items | Action |
|---|---|---|
| Stored data | None — no datastore keys on the fixture name | None |
| Live service config | None | None |
| OS-registered state | None | None |
| Secrets/env vars | None | None |
| Build artifacts / map keys | Corpus slug `feature-origin-only-leak` is load-bearing in 4 map keys + golden path + sidecar/postmortem siblings + `spec_id` | Use ONE basename everywhere; spike used `feature-origin-leak` (shorter) — plan must not mix the two |

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Python `unittest` (stdlib), CPython 3.12.10 real interpreter `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe` |
| Config file | none — discovery via `python -m unittest` |
| Quick run | `python312 -m unittest tests.test_known_bad_corpus tests.test_causal_verb_golden -q` |
| Full suite | `python312 -m unittest discover -s tests -q` + `python312 scripts/gen-finding-catalogue.py --check` + `node install.mjs --check` |

### Phase Requirements → Test Map
| Req | Behaviour | Test type | Command | Exists? |
|---|---|---|---|---|
| REQ-P27-01 | Fixture pair present, validates, postmortem names a code, sidecar falsifiable | corpus | `python312 -m unittest tests.test_known_bad_corpus` (`:1056-1134`, `:1584-1760`) | ✅ (fixture+postmortem+sidecar are Wave-0 authoring) |
| REQ-P27-02 | DSX-ML-034 fires CRITICAL on `after_prediction`, HIGH on `unknown`; silent when block absent; D-05 gate satisfied | unit + build | new `tests/test_ml_feature_provenance.py` with `# D-05: DSX-ML-034`; `python312 scripts/gen-finding-catalogue.py --check` | ❌ Wave 0 (new unit test) |
| REQ-P27-03 | All harness maps + counts consistent; golden ship set pinned; catalogue 277 | corpus + invariant | `tests.test_causal_verb_golden`, `tests.test_frame_val`, `tests.test_finding_catalogue_invariant`, `tests.test_phase20_zero_mint_close`, `tests.test_dsx` | ✅ (edits to existing maps/pins) |

### Sampling
- Per task commit: `python312 -m unittest tests.test_known_bad_corpus -q`
- Per wave merge: full `discover` + `gen-finding-catalogue.py --check`
- Phase gate: full suite green + `node install.mjs --check` before `/gsd-verify-work`

### Wave 0 Gaps
- [ ] `examples/known-bad/feature-origin-only-leak-POSTMORTEM.md` — new (REQ-P27-01)
- [ ] `examples/known-bad/feature-origin-only-leak-ATTRIBUTION.yaml` — new (REQ-P27-01/03)
- [ ] `tests/test_ml_feature_provenance.py` (or add to `tests/test_dsx.py`) — new unit test carrying `# D-05: DSX-ML-034` (REQ-P27-02)

---

## Assumptions Log

| # | Claim | Section | Risk if wrong |
|---|---|---|---|
| A1 | Promoted-fixture `_EXPECTED_VAL_CODES` value is `set()` | C2 | Low — measured clone of full-frame (`set()`); plan MUST re-measure, not assume |
| A2 | Golden ship set is exactly the 4 codes from `27-MEASUREMENT.md:52` after the mint | C3 | Low — DSX-ML-034 stays silent (no provenance block); plan MUST re-measure the promoted fixture |
| A3 | Full-suite test-count delta unknown | E | Low — cosmetic; measured at plan time |

---

## Open risks for the plan-checker

1. **`promotes_backlog_item` id conflict (BLOCKING if followed literally).**
   `27-CONTEXT.md:214` instructs `6.5-item-7-feature-origin-only-leak`, but the FROZEN harness
   `_SECTION_65_ITEM_IDS` (`tests/test_known_bad_corpus.py:839`) contains only
   `6.5-item-7-feature-provenance`, and `:1646-1651` asserts membership. **Use
   `6.5-item-7-feature-provenance`** (also the id the existing retracted sidecar uses at
   `retracted-...-ATTRIBUTION.yaml:15`). Renaming the frozenset instead would break that
   existing sidecar. This is an authoring-note conflict, not a case-shape edit (guardrail 1
   intact) — surface to the human.

2. **`_SECTION_65_BACKLOG_CODES` placement conflict.** `27-CONTEXT.md:129-130,213` says
   DSX-ML-034 is "reserved in `_SECTION_65_BACKLOG_CODES`". Since it is being MINTED (shipped
   to catalogue), the disjointness test (`:1606-1611`) forbids it there. DSX-ML-034 goes in the
   catalogue (via `report.add`) and in the generator's `_D05_ALLOWLIST_CODES` only; the sidecar
   references it as a shipped code. The "reserved in backlog" wording describes the pre-mint
   RESERVE-INACTIVE state and is now superseded.

3. **One code, two severities vs one-row catalogue.** DSX-ML-034 emitted CRITICAL
   (`after_prediction`) and HIGH (`unknown`) needs two literal-severity `report.add` sites (the
   extractor needs literals, `gen-finding-catalogue.py:237-241`). `collect()` dedupes by code
   and prints `warning: DSX-ML-034 declared twice with different text` to stderr, keeping the
   last-seen row (`:287-292`). `--check` does NOT fail on that warning (only staleness/D-05/
   citation failures do), and I found no test asserting zero generator warnings — but the
   committed catalogue will show only ONE severity for 034. Plan must fix the AST/source order
   so the committed row is deterministic, run `--write`, and decide which severity the catalogue
   row displays. (No existing catalogue code is emitted at two severities — this is novel.)

4. **First shipped-code miss sidecar.** All three existing miss sidecars name codes that were
   *unshipped backlog* codes (trivially absent live). DSX-ML-034 is a **shipped** code used as a
   `kind: miss` absent_code — the falsifiability test (`:1712-1760`) will actually run the gate
   and require it silent CRITICAL on the fixture. Holds only while the fixture declares no
   `feature_provenance` block; the plan must guard that the promoted spec never gains one.

5. **Corpus auto-discovery.** Every relevant map (`_EXPECTED_CAUGHT_DEFECTS`,
   `_EXPECTED_VAL_CODES`, `_GOLDEN_SHIP_FINDINGS`) is glob-discovered with key-parity tests, so
   adding the fixture WITHOUT its four map entries fails loudly (good), but promoting it also
   forces the `test_dsx.py:579` count 42→43 and the two catalogue-total pins 276→277 — miss any
   one and the suite goes red. No OTHER fixture's expected counts change (the new fixture's ship
   set is disjoint additions only; incidental codes already documented).
