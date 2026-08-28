# Phase 12: Calibration - Pattern Map

**Mapped:** 2026-08-27
**Files analyzed:** 9 (grouped; corpus/control specs are glob-discovered instances of one pattern, not individually enumerated)
**Analogs found:** 8 / 9 (1 has no direct analog: the ATTRIBUTION.yaml sidecar itself, D-06/D-07 — closest available precedents noted below)

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `dsx/cli.py` (+`p_stats` subparser, +`cmd_stats`) | controller/CLI reader | request-response (aggregating read) | `cmd_explain` (`dsx/cli.py:563-637`) | role-match, **data-flow diverges** (single-root vs. multi-file tree walk — see landmine note) |
| `tests/test_known_bad_corpus.py` — coverage predicates (D-01) | test | batch/assertion | `test_corpus_includes_an_interference_case_and_a_bayesian_continuous_case` (`:634-643`) | exact |
| `tests/test_known_bad_corpus.py` — sidecar sibling-integrity + falsifiability tests (D-07/D-08) | test | batch/assertion + live event-driven verification | `test_every_spec_has_a_sibling_postmortem_and_vice_versa` (`:618-625`) for pairing; `_INCIDENTAL_GAP_CODES` (`:64-88`) for the allowlist-with-documented-reason shape; `_gate_findings` (`:555-616`) for the live-verification call | exact (pairing) / role-match (falsifiability, no direct precedent — new code per RESEARCH Pattern 2) |
| `tests/test_known_bad_corpus.py` — stratified rate + friction column (D-10/D-11) | test | transform/aggregation over live data | `_gate_findings` (`:555-616`) + `_classify_target_defect` (`:251-306`, cited in RESEARCH, not yet read directly — trust RESEARCH excerpt) | role-match |
| `tests/test_known_bad_corpus.py` — catalogue-invariant test (D-18) | test | batch/assertion | `test_corpus_holds_at_least_three_pairs` (`:627-632`) — same "count something, assert a floor/exact value" shape | exact |
| `examples/known-bad/<slug>-ATTRIBUTION.yaml` (new sidecar) | config/fixture data | file-I/O (YAML sidecar, glob-discovered) | **No direct analog.** Closest available precedents: the spec+postmortem pairing convention (`:618-625`) for glob-discovery-by-slug mechanics, and `dsx.loader.load` (used for every other spec-adjacent YAML) for parsing discipline | role-match only (new file *kind*, not a variant of an existing file kind) |
| New corpus cases `examples/known-bad/<slug>-{ANALYSIS-SPEC.yaml,POSTMORTEM.md}` | test fixture data | file-I/O | existing 8 pairs, e.g. `full-frame-cleaning-ANALYSIS-SPEC.yaml` / `full-frame-cleaning-POSTMORTEM.md` | exact |
| Good-side control corpus specs (D-04, new location e.g. `examples/good/<slug>-ANALYSIS-SPEC.yaml`) | test fixture data | file-I/O | `examples/good-ANALYSIS-SPEC.yaml` (the current n=1 baseline) | exact (same file kind, new multiplicity) |
| `brief.md` §6.5 + `.planning/REVERSALS.md` (REV-002) | planning document | transform (prose reclassification + append) | `.planning/REVERSALS.md` REV-001 record (`:60-81`) + Template (`:18-38`) | exact |

## Pattern Assignments

### `dsx/cli.py` — `p_stats` subparser + `cmd_stats` (controller, request-response)

**Analog:** `cmd_explain`, `dsx/cli.py:563-637`

**Core "always return 0" reader pattern** (`dsx/cli.py:563-637`, read in full):
```python
def cmd_explain(args: argparse.Namespace) -> int:
    path: "Path | None" = None
    try:
        path = find_spec(args.spec, args.phase_dir)
        root = args.phase_dir or str(path.parent)
    except CheckError:
        root = args.phase_dir or "."

    try:
        records = read_all(decisions_path(root))
        ...
        if args.json:
            print(json.dumps(selected, indent=2, sort_keys=True))
        elif not_found_message:
            print(not_found_message)
        else:
            print(_render_decision_trail(selected, spec_data))
    except Exception as exc:
        print("dsx: no readable decision trail was found", file=sys.stdout)
        if args.verbose:
            print(f"dsx: {exc}", file=sys.stderr)
    return 0
```

**What to copy directly:**
- The outer `try/except CheckError` root-resolution guard shape (defensive root fallback, not an error).
- The inner `try/except Exception` wrapping everything from read through print, with control-flow signals (`KeyboardInterrupt`/`SystemExit`) left to propagate — this is what makes "always returns 0" a structural property, not an enumerated one.
- `--json` flag handling: `json.dumps(selected, indent=2, sort_keys=True)`.
- Never importing `Severity`, `GATE_THRESHOLDS`, or `Report` — `cmd_stats` must stay a pure reader, same as `cmd_explain`.

**MANDATORY DIVERGENCE (RESEARCH landmine 3, Pitfall 3):** `cmd_explain` resolves exactly ONE root (`args.phase_dir or str(path.parent)`) and reads exactly ONE `DECISIONS.jsonl` via `decisions_path(root)`. `cmd_stats --paradigm` (D-13) must aggregate across potentially MANY `DECISIONS.jsonl` files under a search root — there is no existing multi-file-aggregation precedent to copy verbatim. Model it as `Path(root).rglob("DECISIONS.jsonl")` feeding each discovered file through the existing `dsx.decisions.read_all()`, aggregated in memory, deduplicated by `frame_digest` (D-14) before computing the paradigm split. The single-root reader is the template for *shape and safety discipline only* — not for the aggregation logic, which is new. Handle the zero-history case explicitly (this repo currently has zero `DECISIONS.jsonl` under `.planning/` — report "no operator history yet", never divide by zero).

**Also required:** the D-13 negative assertion that `cmd_stats` never sources `examples/known-bad/DECISIONS.jsonl`, `examples/DECISIONS.jsonl`, or `templates/DECISIONS.jsonl` — this has no prior-art analog in `cmd_explain` (which has no exclusion list at all); it is new guard logic modelled structurally on the allowlist-with-documented-reason shape of `_INCIDENTAL_GAP_CODES` below.

**Paradigm-choice read pattern** (`dsx/frame/paradigm.py:604-617`, per RESEARCH excerpt — three-way vocabulary `frequentist`/`bayesian`/`undeclared`, not binary):
```python
if paradigm:
    choice = f"paradigm={paradigm}"
else:
    choice = "paradigm=undeclared"
report.context.setdefault("decisions", []).append(
    DecisionRecord(id="", invocation_id="", layer="deterministic", choice=choice, ...)
)
```

**Dedup key** (`dsx/decisions.py:241-250`):
```python
def frame_digest(spec: "dict[str, Any]") -> str:
    payload = json.dumps(
        {"validity_frame": spec.get("validity_frame"), "inference": spec.get("inference")},
        sort_keys=True,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
```

---

### `tests/test_known_bad_corpus.py` — coverage predicates (D-01)

**Analog:** `test_corpus_includes_an_interference_case_and_a_bayesian_continuous_case`, `:634-643`

```python
def test_corpus_includes_an_interference_case_and_a_bayesian_continuous_case(self):
    spec_slugs = _slugs(f"*{SPEC_SUFFIX}", SPEC_SUFFIX)
    self.assertTrue(
        any("interference" in slug for slug in spec_slugs),
        f"no slug names an interference case: {sorted(spec_slugs)}",
    )
    self.assertTrue(
        any("bayesian" in slug and "continuous" in slug for slug in spec_slugs),
        f"no slug names a Bayesian continuous-monitoring case: {sorted(spec_slugs)}",
    )
```
Copy this exact shape for the three new D-01 class predicates (retracted-paper+postmortem, documented p-hacking, operator-known-answer): glob-discover slugs via `_slugs(...)`, assert `any(...)` a substring/marker is present, never hardcode the slug list itself. This is a *falsifiable-by-class-presence* predicate, not a count — matches D-01's "full is falsifiable by class present, not arbitrary count" requirement exactly.

---

### `tests/test_known_bad_corpus.py` — sidecar sibling-integrity + falsifiability tests (D-07/D-08)

**Analog (pairing enforcement):** `test_every_spec_has_a_sibling_postmortem_and_vice_versa`, `:618-625`

```python
def test_every_spec_has_a_sibling_postmortem_and_vice_versa(self):
    spec_slugs = _slugs(f"*{SPEC_SUFFIX}", SPEC_SUFFIX)
    postmortem_slugs = _slugs(f"*{POSTMORTEM_SUFFIX}", POSTMORTEM_SUFFIX)
    unmatched = spec_slugs ^ postmortem_slugs
    self.assertEqual(
        unmatched, set(),
        f"orphaned spec or post-mortem (no matching sibling): {sorted(unmatched)}",
    )
```
Copy the `spec_slugs ^ postmortem_slugs` symmetric-difference idiom for the sidecar sibling-integrity test: every `<slug>-ATTRIBUTION.yaml` names a real slug (subset check, not symmetric-difference, since sidecars are optional per D-03), a code in the D-07 validated union, and a real §6.5 item id.

**Analog (allowlist-with-documented-reason shape):** `_INCIDENTAL_GAP_CODES`, `:64-88`
```python
_INCIDENTAL_GAP_CODES = {
    "DSX-CLM-031",  # claims[].evidence points at "RESULTS.md#..." — a file this corpus never commits
    "DSX-COH-031",  # assumptions[0] is declared but neither checked: true nor waived
    ...
}
```
This is the house style for "a set of codes, each with an inline comment explaining exactly why it's in the set" — reuse it if Pitfall 1's tempdir-artifact-stripping noise (`DSX-DQ-001`, `DSX-CLM-031`, `DSX-FIG-001`, `DSX-NAR-010` on the D-04 good-control corpus) is handled via allowlist-exclusion rather than sibling-artifact seeding.

**Falsifiability verification (D-08) — no direct precedent; new code, structural template from RESEARCH Pattern 2, built on `_gate_findings`:**
```python
def _verify_attribution_falsifiable(slug, sidecar, spec_path):
    absent_code = sidecar["absent_code"]
    kind = sidecar.get("kind", "miss")
    all_critical = set()
    for point in ("plan", "execute", "verify", "ship"):
        _, findings = self._gate_findings(spec_path, point)
        all_critical |= {f["code"] for f in findings if f["severity"] == "CRITICAL"}
    if kind == "miss":
        assert absent_code not in all_critical, (
            f"{slug!r} attribution claims {absent_code!r} is absent, but it fires CRITICAL"
        )
    elif kind == "caught":
        assert absent_code in all_critical, (
            f"{slug!r} attribution claims {absent_code!r} is caught, but it never fires CRITICAL"
        )
```
Reuse `_gate_findings` itself verbatim (see below) — do not reimplement live-gate invocation.

**Live-gate measurement substrate to call, not reimplement** (`tests/test_known_bad_corpus.py:555-616`):
```python
def _gate_findings(self, spec_path: Path, point: str) -> tuple[int, list[dict]]:
    with tempfile.TemporaryDirectory() as tmp:
        _seed_entrypoint(tmp, spec_path)
        if point in ("verify", "ship"):
            seed_plan_header(tmp, spec_path)
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(
                ["gate", point, "--spec", str(spec_path), "--phase-dir", tmp, "--json"]
            )
        raw = err.getvalue() or out.getvalue()
        report = json.loads(raw)
    return code, report["findings"]
```

---

### `tests/test_known_bad_corpus.py` — stratified rate + friction column (D-10/D-11)

**Analog:** `_gate_findings` (`:555-616`) as the sole live-data source; `_classify_target_defect` (cited RESEARCH `:251-306`) for the per-(slug,point) pass/fail classification pattern; `_TARGET_DEFECT_CODES` (`:172-248` per RESEARCH/CONTEXT) and `_INCIDENTAL_GAP_CODES` (`:64-88`, read above) for the two-map naming-vs-noise convention.

**Guards to replicate (D-11 three-guard structure):**
(a) synthetic arithmetic proof — filesystem-independent, over a fabricated finding dict (no direct precedent; write as a plain unit test of the `raw − own = net` arithmetic function in isolation).
(b) live-source proof — friction MUST consume the same `_gate_findings` call already used by the golden test (`tests/test_causal_verb_golden.py`) and by `_classify_target_defect`; do not introduce a second gate-invocation path.
(c) incidental→own relabel closure — every `_TARGET_DEFECT_CODES` entry must be positively verified firing CRITICAL live AND named in that fixture's postmortem/attribution; model this check on the `_INCIDENTAL_GAP_CODES` allowlist-guard's existing pattern of asserting it names no slug's own target code (cited in CONTEXT `code_context`, "Established Patterns").

---

### `tests/test_known_bad_corpus.py` — catalogue-invariant test (D-18)

**Analog:** `test_corpus_holds_at_least_three_pairs`, `:627-632`
```python
def test_corpus_holds_at_least_three_pairs(self):
    spec_slugs = _slugs(f"*{SPEC_SUFFIX}", SPEC_SUFFIX)
    self.assertGreaterEqual(
        len(spec_slugs), 3,
        f"expected at least three known-bad pairs, found {sorted(spec_slugs)}",
    )
```
Copy this "count something derived from disk/catalogue, assert a fixed bound" shape for the catalogue-invariant test: parse `references/finding-codes.md`'s Total (cited at `:16`) or enumerate the catalogue programmatically, `assertEqual(count, 256)`.

---

### `examples/known-bad/<slug>-ATTRIBUTION.yaml` (new sidecar — NO direct analog)

No existing file in this repo is a "verified claim about an absent code, living outside the spec, glob-discovered by slug." The closest available precedents, per RESEARCH and CONTEXT, are:
- Glob-discovery-by-slug mechanics: the spec+postmortem pairing test above (`:618-625`).
- Parsing discipline: `dsx.loader.load(path)` — the same bundled-YAML-subset parser used for every other spec-adjacent YAML file (ANALYSIS-SPEC, DATA-PROFILE); do NOT hand-roll a parser or import PyYAML, per D-01 hermeticity and RESEARCH's "Don't Hand-Roll" table.
- Placement-outside-content-lock precedent: **cite `dsx/decisions.py:99-121`'s `InvocationHeader.spec_id` docstring / 11.2 CONTEXT.md D-08** (`spec_id` placement) — **NOT** 11.3 D-08, which is the opposite decision (`validity_frame.exclusions` placed INSIDE `validity_frame` deliberately so it IS digest-covered). This corrects a mis-citation present in `12-CONTEXT.md`'s own D-06/canonical_refs (RESEARCH Pitfall 5) — the planner and any code comment/docstring written for the sidecar must cite **11.2 D-08**, not 11.3 D-08.

Schema (D-07, locked): `{ absent_code (required), promotes_backlog_item (required), rationale? (optional), kind? (optional, default "miss") }`.

---

### `brief.md` §6.5 + `.planning/REVERSALS.md` (REV-002)

**Analog:** REV-001 record, `.planning/REVERSALS.md:60-81`; Template, `:18-38`
```markdown
### Reversal record REV-001 (D-14)

**Date:** 2026 (during brief drafting, prior to Phase 6 planning)

**Reversed:** the blanket deferral of the prior family under D-12a.

**New evidence:** the identification-strength framing supplies a writable
frequentist mirror for two of the four deferred items. ...

**What would have made the original correct:** if prior choice had no
frequentist analogue, which is false for regularisation and true only for
genuine subjective-belief priors.

**What did not change:** `DSX-PAR-021` (sensitivity) and `DSX-PAR-030`
(convergence) stay deferred. ...
```

**Critical constraint for REV-002 (D-17, SELF-001 guard, `.planning/REVERSALS.md:40-56`):** the **New evidence** field must NOT restate the determinism doctrine (D-01/D-02) as if newly discovered — it pre-dates the original deferral. Frame **New evidence** as: "Phase 12's systematic REQ-P12-05 re-evaluation of all nine §6.5 rows against measured entry conditions is what surfaces, for item 6 specifically, that its entry condition requires a computation the doctrine structurally forbids on the gate path — not merely that the doctrine exists." **What did not change** must explicitly list: D-01/D-02 stand, `DSX-INT-030` stays shipped, items 4 and 5 stay carried. **Mechanism:** relocate (not delete) the §6.5 row into a new "Removed / permanently out of scope (D-14)" subsection, preserving verbatim the substrings pinned by `tests/test_known_bad_corpus.py:1043-1069`: "Ratio-metric dilution for trigger analysis", "Formula (3)", "per-unit trigger and outcome data reaching the gate" — or update that pin test in the same commit.

## Shared Patterns

### Live-gate measurement (no lifted numbers)
**Source:** `tests/test_known_bad_corpus.py:555-616` (`_gate_findings`)
**Apply to:** every D-09/D-10/D-11 computation, the D-08 falsifiability check, and the D-04 good-control FPR count. Never read from `_INCIDENTAL_GAP_CODES` (stale, `:64-88`) or `_GOLDEN_SHIP_FINDINGS` (stale, `tests/test_causal_verb_golden.py:82-142`) as a source of truth for a reported number — those are snapshots, not live data.

### Allowlist-with-documented-reason
**Source:** `_INCIDENTAL_GAP_CODES`, `tests/test_known_bad_corpus.py:64-88`
**Apply to:** any new exclusion set this phase needs (tempdir-artifact-stripping noise codes for D-04 control specs, if that Pitfall-1 mitigation route is chosen over sibling-artifact seeding).

### Glob-discovery-by-slug (never hardcode)
**Source:** `_slugs`, `CORPUS_DIR.glob(...)` (cited throughout `tests/test_known_bad_corpus.py`)
**Apply to:** all new corpus cases, the good-control corpus, and the ATTRIBUTION.yaml sidecars — none may appear in a hardcoded list anywhere in the harness.

### Pure-reader-returns-0-by-construction
**Source:** `cmd_explain`, `dsx/cli.py:563-637`
**Apply to:** `cmd_stats` — outer/inner exception-guard shape, never imports block-contract primitives, `--json` flag handling.

## No Analog Found

| File | Role | Data Flow | Reason |
|---|---|---|---|
| `examples/known-bad/<slug>-ATTRIBUTION.yaml` | config/fixture data | file-I/O (sidecar) | No existing file kind combines "verified claim about an absent finding code" + "lives outside the spec content-lock" + "glob-discovered." Nearest precedents are structural only (pairing mechanics, YAML-load discipline, placement precedent) — the schema and falsifiability-check content are new. Planner should treat this as new-code design guided by RESEARCH Pattern 2, not a copy-edit of an existing file. |
| `dsx/cli.py` `cmd_stats` aggregation body (post-template) | controller | event-driven/batch tree-walk aggregation | `cmd_explain`'s single-root read model does not generalize (RESEARCH Pitfall 3, landmine 3) — the outer safety/shape is copyable, the aggregation logic (`Path(root).rglob("DECISIONS.jsonl")` + per-file `read_all()` + `frame_digest` dedup) has no precedent in this codebase and must be written fresh, exercised primarily by the D-14 synthetic-trail test since this repo has zero real `.planning/`-rooted `DECISIONS.jsonl` files today. |

## Metadata

**Analog search scope:** `dsx/cli.py`, `tests/test_known_bad_corpus.py`, `tests/test_causal_verb_golden.py` (referenced via RESEARCH, not independently re-read), `dsx/decisions.py`, `dsx/frame/paradigm.py`, `.planning/REVERSALS.md`, `examples/known-bad/`, `examples/good-ANALYSIS-SPEC.yaml`.
**Files scanned (direct Read calls this session):** `dsx/cli.py:563-642`, `tests/test_known_bad_corpus.py:60-100`, `tests/test_known_bad_corpus.py:605-644`, `.planning/REVERSALS.md` (full), plus CONTEXT.md/RESEARCH.md (full) which independently verified all other cited line ranges live at research time (zero anchor drift, per RESEARCH.md's own verification pass).
**Pattern extraction date:** 2026-08-27
