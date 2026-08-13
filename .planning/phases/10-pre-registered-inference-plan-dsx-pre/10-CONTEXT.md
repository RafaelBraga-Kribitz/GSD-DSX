# Phase 10: Pre-registered inference plan (`DSX-PRE-*`) - Context

**Gathered:** 2026-08-13 (assumptions mode)
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 10 delivers the **pre-registration reconciliation family** — the checks that hold a declared
inference plan to the executed one.

It ships:

- A fallback-rule mini-language that resolves a declared rule to exactly one branch against the
  declared observed facts, where an unparseable rule exits `2` — could not run — and never `0`
  (REQ-P10-01).
- `declared_at` provenance recorded and **named as the unverifiable operator self-declaration it is**,
  in both the finding remedy and the README, rather than presented as a guarantee (REQ-P10-02).
- A reconciliation check blocking a run whose executed procedure differs from the branch the declared
  rule selects, naming **both** the declared branch and the executed branch in the finding text
  (REQ-P10-03).
- Proof — by fixture, not by a second code — that the block does not consult the substitute's merit:
  a procedure switched after seeing the data blocks even when the substitution is strictly more
  conservative (REQ-P10-04).

**Registered at `verify` and `ship` only.** There is no executed branch to reconcile against at
`plan` or `execute` (`ROADMAP.md:444-445`). This is the first frame family whose gate points differ
from `paradigm`'s, so unlike Phase 9 it *does* require `GATE_PROFILES` edits.

**Out of this phase's boundary:** `DSX-VAL-*` (Phase 7, shipped), `DSX-INT-*` (Phase 8, shipped),
`DSX-PAR-*` (Phase 9), `DSX-ADM-*` (Phase 11). **No procedure ranking, admissibility, power or
conservatism ordering on the gate path** — that is Phase 11's job and brief D-02 bars it here.
`references/families.yaml` is not created in this phase (brief §6.6 — an empty ontology accumulates
speculative structure).

Requirements: REQ-P10-01 … REQ-P10-04 (4 requirements, `.planning/REQUIREMENTS.md:125-130`).

</domain>

<decisions>
## Implementation Decisions

> **Numbering note.** `D-nn` below are **phase-local** decision ids for Phase 10, following the
> precedent set by `06-CONTEXT.md`, `07-CONTEXT.md` and `09-CONTEXT.md`. The project-wide decision
> table in `brief.md` §4 is referenced throughout as **brief D-nn**, and `PROJECT.md`'s milestone
> table as **M-nn**. They are different namespaces; do not conflate `D-05` here (the procedure
> vocabulary) with brief D-05 (the citation rule).

### Locked upstream — do NOT re-litigate

- `brief.md` §4 (brief D-01…D-14) and §5 (contract shape) are binding inputs (`PROJECT.md` §Context).
- **brief D-01**: stdlib only on the gate path. The mini-language parser is hand-written stdlib.
- **brief D-02**: no test statistic or posterior computed on the gate path. This is what makes
  procedure *ranking* impossible here and pushes REQ-P10-04 onto a fixture.
- **brief D-04**: never block to teach — emit decision records; `dsx explain` renders them.
- **brief D-05**: primary-source citation naming the exact formulation, plus a published reference
  value **or a named structural criterion**. ROADMAP SC 5 states the disjunction explicitly.
- **brief D-06**: finding codes are never renumbered. This makes D-11 below irreversible.
- **brief D-11**: frame-layer checks never read `paradigm`. `DSX-PRE-*` is frame-layer and
  paradigm-independent — `_PARADIGM_INDEPENDENT` already lists `"DSX-PRE-"`
  (`dsx/frame/paradigm.py:47`, **verified**). A test asserting no `DSX-PRE-*` check reads
  `inference.paradigm` mirrors REQ-P7-09 and REQ-P8-06 and should ship even though Phase 10 has no
  numbered requirement demanding it.
- Exit codes are the contract: `0` pass, `1` block, `2` could not run.
- Phase 11 is not pre-built. No `references/families.yaml`, no `dsx/frame/admissibility.py`.

### The mini-language: trigger, scope, and how it fails

- **D-01: the mini-language is opt-in, discriminated by the literal arrow `->`.** A `fallback_rule`
  containing `->` is a rule and must parse. A `fallback_rule` without `->` is free prose, is outside
  the mini-language entirely, and produces no finding and no error.
  - **Verified during discuss:** every `fallback_rule` committed today is English prose and **none
    contains `->`**. The eight values are `examples/good-ANALYSIS-SPEC.yaml:362-364`,
    `templates/ANALYSIS-SPEC.yaml:358`, `examples/bad-ANALYSIS-SPEC.yaml:242` (empty),
    `examples/known-bad/frequentist-uncontrolled-continuous-…:184` (empty),
    `…/bayesian-continuous-monitoring-…:198-201`, `…/weak-identification-mmm-…:190-193`,
    `…/interference-shared-budget-…:183-185`, `…/triggering-dilution-…:182-184`.
  - **Why not an `if`-prefix trigger:** six of the eight begin with "If". An `if`-prefix trigger
    over-matches the entire corpus, including the template and the good fixture.
  - **The blast radius of getting this wrong** is two guards at once:
    `tests/test_dsx.py:1390-1393` (the template still passes `dsx gate plan`) and
    `scripts/check.sh:15-23` (`good-ANALYSIS-SPEC.yaml` exits `0` everywhere).
  - The arrow is the brief's own grammar token (`brief.md:204-205`) and has zero collisions in any
    `fallback_rule` value.

- **D-02: exit `2` is produced by raising `CheckError` from inside the check. There is no
  finding-based route, and the plan must say so rather than discovering it.**
  - **Verified during discuss, by direct read:** `Report.exit_code()` returns only `EXIT_BLOCK` or
    `EXIT_PASS` (`dsx/findings.py:181-182`). `EXIT_ERROR = 2` (`dsx/findings.py:23`) is returned in
    exactly two places, both exception handlers in `main()` (`dsx/cli.py:765`, `:768`). **No
    `report.add(...)` at any severity can ever yield exit 2.**
  - The working precedent is `apply_suppressions`, which raises `CheckError` from inside the check
    run for an unknown suppression code, documented in `templates/ANALYSIS-SPEC.yaml` as "Unknown
    codes abort the run (exit 2)".
  - **D-03 (accepted consequence, decided not discovered):** `CheckError` aborts the whole gate run
    and prints no findings. An unparseable rule at `verify` therefore suppresses every other finding
    in that run. **This is accepted**, on the grounds that the suppressions feature already behaves
    exactly this way and a could-not-run gate is honest about not having run. The planner must not
    treat this as a defect to work around, and the finding-free output must be legible enough that an
    operator can tell an aborted run from a clean one.

- **D-04: the mini-language coins NO new contract field. Its fact namespace is restricted to a
  closed, tested registry of fields that already exist.**
  - **Verified during discuss:** `clusters` — the brief's own example fact
    (`brief.md:204-205`, `if clusters < 30 -> wild cluster bootstrap`) — **appears in zero `.yaml`
    files in this repository.** `validity_frame.dependence` holds `structure`, `cluster_var` and
    `method_family_required`, and no count. There is also **no `results:` shape validator at all** —
    `REQUIRED_TOP_LEVEL` is `("spec_version", "title", "question_type", "decision")`.
  - **The brief's `clusters` example is therefore illustrative, not binding.** §5's *structure*
    binds; its phrasing does not bind at the token level — the precedent is `09-CONTEXT.md`
    `<specifics>`, where the primary source beat the brief's framing.
  - **Rejected alternative:** coin `results.clusters` or `validity_frame.dependence.n_clusters`.
    Rejected because it repeats the Phase 9 D-05 trap — a new key that no template scaffolds, no
    `dsx vocab` dumps, and no unknown-key check catches (`dsx/spec.py:973-980` states in prose that
    there is no unknown-key check under `inference:`). A Phase 6 contract change arriving in Phase 10
    is the wrong shape for a phase whose job is reconciliation.
  - **What the planner must build instead:** an explicit fact registry, so an unknown fact name is a
    **decidable error** rather than a silent pass. Candidate members are numeric fields already read
    by shipped checks — `results.observed_n`, `results.interim_looks`,
    `results.comparisons_looked_at`, `design.alpha`. **The planner selects the final membership after
    confirming each field is actually populated in a fixture that reaches `verify`**, and documents
    the registry where `dsx vocab` or the README will show it. A rule referencing a name outside the
    registry resolves to no branch and is a `DSX-PRE-010` finding — not an exit-2 parse failure,
    because the rule parsed fine; it referenced something that does not exist.

### Reconciling the declared procedure against the executed one

- **D-05: the declared side is `inference.primary_procedure`; the executed side is `analysis.test`.
  Both are free strings, and the existing `normalize()` is the brittleness fix — Phase 10 builds no
  procedure vocabulary.**
  - `_INFERENCE_MEMBERSHIP` vocabulary-checks only `paradigm`, `paradigm_justification` and
    `declared_at` (`dsx/spec.py:990-994`), so `primary_procedure` is unconstrained free text.
  - `results.tests[]` entries carry `metric`, `p_value`, `effect`, `standardized_effect`, `ci`,
    `interpretation`, `minimum_practical_effect` (`examples/good-ANALYSIS-SPEC.yaml:231-255`) and
    **no procedure name at all**. `analysis.test` does hold one, and in every fixture the declared and
    executed values already agree by construction (`two_proportion_z`/`two_proportion_z` in the good
    and frequentist-uncontrolled fixtures, `bayesian_ab`/`bayesian_ab` in the Bayesian one).
  - `normalize()` (`dsx/spec.py:409-410`) is `str().strip().lower().replace("-","_").replace(" ","_")`
    — it maps `wild cluster bootstrap` to `wild_cluster_bootstrap`, which is exactly the free-string
    brittleness this decision has to solve, already shipped and already imported by every
    `dsx/frame/` module.
  - **Honest caveat the planner must carry into the finding text and the README:** `analysis.test` is
    scaffolded in `templates/ANALYSIS-SPEC.yaml:129` and is therefore a *plan-time* declaration too.
    "Executed" is a convention imposed by the gate point, not a property of the field. This is the
    same class of limit as `declared_at` and belongs beside it, not hidden.
  - **Rejected alternative:** coin `results.procedure`. It would make the plan/verify asymmetry
    structural rather than conventional, but it means coining a contract field — which D-04 already
    declined — and editing a list every shipped check iterates (`stats.py`, `metrics.py`,
    `decision.py`, `claims.py`, `repro.py`).

- **D-06: there is no importable procedure vocabulary, and building one is out of scope.**
  - The only snake_case procedure lexicon in the repo is embedded in `recommend_test()`
    (`dsx/checks/stats.py:40-127`). **`dsx/frame/` may not import `dsx.checks`** — the D-03a boundary,
    stated at `dsx/frame/__init__.py:16-31` and enforced by `tests/test_frame_boundary.py`.
  - `VARIANCE_ADJUSTMENTS` (`dsx/spec.py:108`) is about variance adjustment, not procedure identity —
    M-09 reuses it for `dependence.method_family_required`, which is a different axis.
  - A planner reaching for `stats.recommend_test` turns the boundary scanner red; a planner reaching
    for `families.yaml` pre-builds the ontology brief §6.6 forbids.

- **D-07: REQ-P10-03 and REQ-P10-04 are one code with two fixtures, not two codes.**
  - The check cannot know a substitute is "more conservative" without ranking procedures, which is
    Phase 11's `DSX-ADM-*` job (`ROADMAP.md:472-483`) and is barred from the gate path by brief D-02.
  - REQ-P10-04's content is therefore a **property of the trigger** — the check does not consult
    defensibility — which is provable by a fixture whose substitution is strictly more conservative
    and which still blocks. That is exactly ROADMAP SC 3's wording.
  - The house habit is one stable fact per code: `09-CONTEXT.md:169-172` rejected a second code that
    would emit two codes for one defect, and `dsx/frame/interference.py:1-9` refuses to re-report what
    `DSX-SPEC-080/081` already own.

### The content lock and `declared_at` provenance

- **D-08: the plan-time content lock already exists and already ships. Phase 10 reads it; it does not
  build it.**
  - **Verified during discuss, by direct read:** `frame_digest(spec)` (`dsx/decisions.py:181-190`) is
    a sha256 over `json.dumps({"validity_frame": …, "inference": …}, sort_keys=True)`, documented as
    "Key-order invariant … unchanged by edits elsewhere in the spec. Change-detection, not a security
    control." It is carried on `InvocationHeader` and appended by `_write_decision_trail`
    (`dsx/cli.py:302-313`) on **every** gate point. The committed `examples/DECISIONS.jsonl` proves it
    in the artifact: line 1 is a `record_type: invocation` row carrying `frame_digest` and
    `gate_point: plan`.
  - This is precisely what `.planning/research/PITFALLS.md:88-92` prescribed and `:721` mapped to M3
    as "reconciliation checks the lock, not the string".
  - **A second lock artifact must not be built.** Two digests over the same bytes immediately raises
    the question of which is authoritative.

- **D-09: reading that lock promotes `DECISIONS.jsonl` from side channel to gate input. The
  unconditional invariant in `_write_decision_trail`'s docstring is narrowed to the WRITE path, with
  the reason stated in the docstring itself.**
  - **Verified during discuss, by direct read:** `_write_decision_trail` is wrapped in
    `except Exception` and swallowed, and its docstring states the invariant without qualification —
    "the write is a side channel, never part of the block contract, so it can never change `point`'s
    exit code" (`dsx/cli.py:288-290`).
  - **The narrowing is real and must be legible.** After Phase 10 the true statement is: *the write
    is a side channel and can never change an exit code; the plan-time header, once written, is a
    gate input at verify and ship.* Editing that docstring without stating why would leave a comment
    that contradicts the code — the failure this project's honesty controls exist to prevent.
  - **Mechanically it is a signature change.** `run_checks` calls `CHECKS[name](spec)` for frame
    modules (`dsx/cli.py:176-177`); both `val.check(spec)` (`dsx/frame/val.py:200`) and
    `interference.check(spec)` (`dsx/frame/interference.py:643`) take `spec` alone. `prereg.check`
    needs a `root` argument via a new `elif` branch — precedent exists for `dq`, `code`, `figures`
    and `narrative` (`dsx/cli.py:156-175`). The D-03a boundary permits importing `dsx.decisions`
    (`dsx/frame/__init__.py:17-18`), so `read_all` and `decisions_path` are legal imports.
  - **A `verify` run with no recorded plan-time header exits `2` — could not run — not `0`.** This is
    consistent with the exit-code contract and with ROADMAP SC 4's conditional wording ("*where* a
    content lock … is captured at plan"). Silently passing is the failure PITFALLS Pitfall 1 exists to
    prevent.
    - **Consequence the planner must handle explicitly:** this collides with the M-07 grandfather
      path. A pre-v2.0.0 spec that legitimately never ran `dsx gate plan` now cannot reach `verify`
      without a could-not-run. The exit-2 message must name `suppressions[]` with its ADR/SPEC
      authority requirement as the intended route, so the grandfather path stays walkable and
      attributable. **Do not solve this by making the missing header pass.**

- **D-10: `declared_at: post_data` on its own stays legal and silent. Phase 10 documents its limit; it
  does not block on it.**
  - REQ-P10-02 says "recorded and its limits are documented", not "blocked". Blocking honest
    post-hoc declaration would make honesty more expensive than dishonesty — the exact brief-D-10
    incentive distortion this project keeps closing, arriving through a different door.
  - **The documentation half is already half written:** `DECLARATION_POINTS` (`dsx/spec.py:279-285`)
    already describes `post_data` as "an unverifiable operator self-declaration (Phase 10 REQ-P10-02
    documents this limit)". The forward reference is committed and waiting to be honoured.
  - **ROADMAP SC 4 has two halves — finding remedy AND README.** `README.md:309-323` ("## Known
    limits", whose first line is "**a frame that lies passes**") is the anchor, with "### Two tiers of
    evidentiary rigour" at `README.md:338` adjacent. Satisfying only the remedy half leaves SC 4
    unmet even with correct code.
  - Where `declared_at: pre_data` is claimed **and** the recorded plan-time digest differs from the
    verify-time bytes, that is `DSX-PRE-020` — the claim is contradicted by the recorded bytes. That
    is a different fact from `post_data` being declared honestly.

### Module, registration, severity, numbering

- **D-11: a new `dsx/frame/prereg.py`, registered as `CHECKS["prereg"]` in `verify` and `ship` only,
  at `CRITICAL`. Registration and severity are complementary here, not redundant.**
  - **Verified during discuss, by direct read:** `GATE_PROFILES` (`dsx/cli.py:90-103`) has no
    `prereg` entry; `verify` and `ship` carry identical tuples. `GATE_THRESHOLDS` (`dsx/cli.py:107-112`)
    is CRITICAL at plan/execute and HIGH at verify/ship. **Registration is what keeps the check off
    plan and execute; severity is a separate knob.** `.planning/research/ARCHITECTURE.md:231` says
    exactly this — "**verify, ship only** | **CRITICAL**".
  - **CRITICAL is not optional.** `tests/test_known_bad_corpus.py:176` filters
    `f.get("severity") == "CRITICAL"` when validating an expected target code, so a HIGH
    `DSX-PRE-*` would exit `1` as SC 2 demands **and still fail the corpus classifier**.
  - The pattern to copy is `test_interference_registered_in_plan_verify_ship_absent_from_execute`
    plus `test_every_dsx_int_code_reachable_from_a_gate_profile`
    (`tests/test_frame_interference.py:169-185`). That pair is what ROADMAP SC 5's reachability test
    must assert, with `execute` **and** `plan` as the absent points.

- **D-12: three codes — `DSX-PRE-010`, `DSX-PRE-020`, `DSX-PRE-030`. Irreversible under brief D-06.**
  - **Correction to note:** STATE.md's standing "final numeric code assignments" open item names
    **Phases 7, 8 and 11 — not Phase 10** (`.planning/STATE.md:57`, **verified**), and ROADMAP's
    Phase 10 entry carries no "Open items" line at all (**verified**). So this was never a recorded
    open item for this phase. It is settled here anyway, deliberately: brief D-06 makes numbering
    irreversible regardless of which phase the tracker happened to name, and a phase that coins three
    permanent codes without recording why should not exist. STATE.md gains a Phase 10 line recording
    the resolution.
  - Follows the one-decade-per-concept convention `07-CONTEXT.md:69-88` set as a user decision, with
    `-001` reserved (in this catalogue's convention `-001` denotes structural absence of a whole
    block). Shipped families confirm the convention: `DSX-VAL-010/011/020/021/030/040/041/050/060/070`,
    `DSX-INT-010/011/030/040`, `DSX-PAR-001/002/010/011`.
  - **`DSX-PRE-010`** ← REQ-P10-01, the finding half: a rule in mini-language form that does not
    resolve to exactly one branch against the declared facts — including a rule referencing a fact
    outside D-04's registry, and a rule whose conditions resolve to zero branches or to more than one.
    **The unparseable half of REQ-P10-01 carries no code at all** — it is exit 2 via D-02.
  - **`DSX-PRE-020`** ← REQ-P10-02 + SC 4: the recorded plan-time `frame_digest` differs from the
    verify-time bytes while the spec claims `declared_at: pre_data`.
  - **`DSX-PRE-030`** ← REQ-P10-03 + REQ-P10-04: the executed procedure differs from the branch the
    declared rule selects. Both branch labels named in the finding text.
  - **A syntactically valid rule referencing an undeclared fact folds into `-010`** rather than
    taking `-011`. Rationale: the remedy is the same in both cases — declare the fact or fix the
    rule. If the phase discovers during planning that the remedies genuinely diverge, `-011` is
    available; **but the decade must not be spent speculatively.** Getting the count wrong is worse
    than getting the digits wrong.

- **D-13: five specific guards go red in the landing commit. Each is a designed forcing edit, not a
  defect, and each must be fixed in the same commit that lands its code.**
  1. `_NOT_SHIPPED` names `"DSX-PRE-"` (`dsx/frame/paradigm.py:66`, **verified**) and
     `tests/test_dsx.py:2849-2850` asserts every `_NOT_SHIPPED` prefix resolves to **zero** known
     codes. The entry must be deleted.
  2. `_PARADIGM_INDEPENDENT` already lists `"DSX-PRE-"` (`dsx/frame/paradigm.py:47`, **verified**)
     and `tests/test_dsx.py:2830-2834` asserts every *applied* prefix resolves to at least one known
     code. The same commit satisfies it — these two guards are a matched pair and flip together.
  3. `PREFIX_GROUPS` (`scripts/gen-finding-catalogue.py:25-52`) has **no `DSX-PRE` entry**, and
     `render()` silently skips unmatched prefixes while still counting them in the total
     (`:184-190`). `tests/test_gen_finding_catalogue.py:174-181` catches this.
  4. **The quiet one.** `_D05_ALLOWLIST_PREFIXES` is `("DSX-PAR-", "DSX-VAL-", "DSX-INT-")`
     (`scripts/gen-finding-catalogue.py:65`, **verified**) and it is the **inclusion** list, not an
     exemption list — `check_d05` only checks codes matching it. **Without adding `"DSX-PRE-"`, the
     brief-D-05 citation obligation in ROADMAP SC 5 is documented but never enforced, and
     `--check` passes.** Unlike Phase 9, where the allow-list already covered `DSX-PAR-`, this phase
     must edit the script.
  5. `tests/test_gen_finding_catalogue.py:227` pins the covered code set against the real tree and
     must be updated with it.

### Citation — external research applied

- **D-14: the brief-D-05 anchor is Gelman & Loken (2014), and Phase 10 takes ROADMAP SC 5's
  `Structural criterion:` branch rather than `Reference value:`.**
  - **The anchor.** Gelman, A. & Loken, E. (2014), "The Statistical Crisis in Science", *American
    Scientist*, volume 102, issue 6, pages 460-465. Full text read during discuss from two
    independent free copies (the authors' copy at `sites.stat.columbia.edu` and a second at
    `psychology.mcmaster.ca`); page numbers taken from the printed running footers and mapped page by
    page. **Not paywalled.**
    - **Why this source and not the others:** it is the only candidate whose stated claim is
      *isomorphic to what the check mechanically does*. Page 460, unnumbered section "How to Test a
      Hypothesis", distinguishes "(2) a classical test prechosen from a set of possible tests,
      yielding T(y;φ), with preregistered φ" from "(3) … computing a single test based on the data,
      but in an environment where a different test would have been performed given different data …
      T(y;φ(y))". **The declared fallback rule is φ; the executed procedure is φ(y).**
    - **The sentence that makes the block unconditional on the substitute's merit** (page 463, opening
      the unnumbered section "Menstrual Cycles and Voting"): *"For a p-value to be interpreted as
      evidence, it requires a strong claim that the same analysis would have been performed had the
      data been different."*
  - **Two locator warnings that must be honoured, not smoothed over.**
    - **The article has no numbered sections, tables or theorems.** Naming one would be the
      fabricated locator brief D-05 exists to prevent. Cite page plus unnumbered section heading.
    - **The symbol φ is garbled by optical character recognition in both available scans** (one
      renders it "cp", the other "[phi]"). The prose is cross-verified word for word between the two
      independent copies; **the symbol is not**, and is taken from the authors' 2013 Columbia working
      paper of the same argument (§1.1-1.2, pages 1-3), which typesets it natively. That working paper
      is unpublished, has no DOI, venue or pagination, and must be **named as a notation source
      only, never as the published record.**
  - **`Structural criterion:`, not `Reference value:`.** Three grounded reasons:
    - brief D-02 forbids computing anything on this gate path — the check parses, hash-compares and
      label-compares, so there is no computed quantity a reference value could pin.
    - House precedent exists for exactly this shape: `dsx/frame/paradigm.py:350` and `:442`, and
      `dsx/spec.py:868` and `:1015`, carry `Structural criterion:` alone. The enforcement regex
      accepts it: `^\s*(?:Reference value|Structural criterion):\s*\S`
      (`scripts/gen-finding-catalogue.py:78-80`).
    - The one available number is off-target (below).
  - **Proposed structural criterion wording**, to be refined but not weakened in planning:
    *"Branch identity, never procedure merit — the check resolves the declared fallback rule to
    exactly one branch against the declared observed facts and blocks on any inequality between that
    branch label and the executed procedure label, reading no admissibility, power or conservatism
    ordering on the gate path (D-02); it is falsified by any fixture whose substituted procedure is
    strictly more conservative and passes."*
  - **Secondary citation for REQ-P10-04 and SC 3's fixture:** Simmons, J. P., Nelson, L. D. &
    Simonsohn, U. (2011), "False-Positive Psychology", *Psychological Science* 22(11):1359-1366, DOI
    `10.1177/0956797611417632`, page 1365, "General Discussion" → "Nonsolutions" → "Correcting alpha
    levels." Read during discuss from the publisher-typeset PDF (native text, no scanning risk).
    Verbatim: *"…unless there is an explicit rule about exactly how to adjust alphas for each degree
    of freedom … the additional ambiguity may make things worse by introducing new degrees of
    freedom."* That is a published rejection of "I swapped in a more conservative test, so it is
    fine": the substitution is itself a new degree of freedom.
  - **Secondary citation for REQ-P10-02's remedy wording only:** Nosek, B. A., Ebersole, C. R.,
    DeHaven, A. C. & Mellor, D. T. (2018), "The preregistration revolution", *PNAS* 115(11):2600-2606,
    DOI `10.1073/pnas.1708274114`, read via PubMed Central PMC5856500, section "Preregistration in
    Practice": *"Deviations from data collection and analysis plans are common, even in the most
    predictable investigations. Deviations do not necessarily rule out testing predictions
    effectively."* **Page numbers for individual Nosek sentences were NOT verified — section headings
    only.** This source supports D-10's "declared deviation stays legal"; it is the **wrong** anchor
    for REQ-P10-03/04, because its own text argues deviations do not necessarily invalidate.
  - **`brief.md` §7 names no pre-registration source today** — verified during discuss. §7's own
    instruction is to anchor D-05 citations there rather than let them sprawl, so **§7 must be
    amended in this phase** with the Gelman & Loken record. This is a citation addition, not a
    brief-D-14 reversal: it adds an anchor where none existed rather than reversing a D-table row.

- **D-15: no published number is asserted, and the reason is recorded so a future reader does not
  "helpfully" add one.**
  - Simmons et al. Table 1, page 1361 gives a **verified 60.7%** false-positive rate at p<.05 for the
    combination of all four researcher degrees of freedom, over 15,000 simulated samples with a
    two-condition baseline of 20 observations per cell. (The paper's own prose rounds this to 61%;
    the table value is 60.7%.) **It quantifies four named researcher choices, not substitution between
    two branches of a declared rule.** Asserting it as `DSX-PRE-*`'s reference value would attribute
    to Simmons a number about a different quantity — the same class of error `09-CONTEXT.md` D-10
    caught in the Deng attribution.
  - Adherence audits give real, verified figures — Claesen, Gomes, Tuerlinckx & Vanpaemel (2021),
    *Royal Society Open Science* 8(10):211037, §3.3: 89% of studies had at least one undisclosed
    discrepancy; Goldacre et al. (2019), *Trials* 20:118, Results: 87% of trials had discrepancies
    requiring a correction letter. These are **prevalence rates of a behaviour in a literature, not
    properties of this code.** A test asserting one would pass by hard-coding a constant, which is the
    citation laundering brief D-05 exists to prevent. **They belong in the finding remedy and the
    README as motivation, never in a `Reference value:` line.**
  - Chan, Hróbjartsson et al. (2004), *JAMA* 291(20):2457-2465 was reached at **abstract level only**
    — the full text is paywalled. Do not cite a table or page from it.

### Fixtures

- **D-16: one new known-bad fixture carrying a post-hoc procedure switch, registered in the
  per-gate-point map. The strictly-more-conservative case lives as a synthetic spec in the unit
  suite.**
  - `tests/test_known_bad_corpus.py` now carries **two** live maps whose comment at `:243-253` states
    plainly that "neither shape subsumes the other": `_TARGET_DEFECT_CODES` (`:134-138`), keyed by
    gate point, for a check registered at some points but not others — `weak-identification-mmm` uses
    `{"plan": "DSX-VAL-040", "verify": "DSX-INT-030"}`; and `_EXPECTED_CAUGHT_DEFECTS` (`:259-265`),
    the both-CRITICAL-points form. **Since `prereg` is verify/ship-only, the per-gate-point shape is
    the right one** — `{"verify": "DSX-PRE-030"}`.
  - `test_expected_caught_defects_keys_match_the_corpus_on_disk` requires **every** fixture on disk to
    have a key in `_EXPECTED_CAUGHT_DEFECTS`, so the new fixture needs an entry there too, even if it
    is an empty frozenset.
  - **Adding `DSX-PRE-*` to `_INCIDENTAL_GAP_CODES` is explicitly forbidden** by
    `test_incidental_allowlist_names_no_slugs_own_target_code`. A planner taking that shortcut would
    neutralise the phase's own check by allow-list. **Do not weaken that guard.**
  - Every committed fixture must also satisfy the post-mortem and catch-attribution invariants at
    `tests/test_known_bad_corpus.py:270-326`, which is why the more-conservative case is a unit-suite
    synthetic rather than a second committed corpus pair.

### Claude's Discretion

The researcher and planner may settle these without returning to discuss:

- **Plan slicing across the four requirements.** There is no atomicity constraint in this phase —
  unlike Phase 9's `DSX-PAR-010/011` pair, the three `DSX-PRE-*` codes are independent and may land
  separately, provided each landing commit fixes the D-13 guards its own code trips.
- **The exact grammar of the mini-language beyond the `->` trigger** — comparison operators, whether
  a rule may carry more than one condition, whether an `else` branch is expressible. Keep it as small
  as the four requirements need. `brief.md:204-205` is the one worked example that must parse.
- **The final membership of D-04's fact registry**, subject to confirming each field is actually
  populated in a fixture that reaches `verify`.
- **Where the fact registry is surfaced to an operator** — `dsx vocab`, the README, or both.
- **Whether `DSX-PRE-020` compares the digest against the most recent `plan` header or the earliest**,
  and what a trail containing several `plan` headers means. State the choice; do not leave it implicit.
- **The exact `elif` shape for threading `root` into `prereg.check`** (D-09), following the existing
  `dq`/`code`/`figures`/`narrative` precedent at `dsx/cli.py:156-175`.
- **Whether the paradigm-independence test for `DSX-PRE-*` is written as a source-level assertion or
  a behavioural one**, following whichever of REQ-P7-09 and REQ-P8-06 shipped the cleaner idiom.

### Folded Todos

None — `todo.match-phase 10` returned zero matches.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Binding inputs — not re-litigable

- `brief.md` §4 — brief D-01…D-14. D-01, D-02, D-04, D-05, D-06, D-10 and D-11 are directly
  load-bearing here.
- `brief.md` §5.2 (the `inference:` block, lines 188-215 — note M-02 removed `stopping_rule`),
  §5.5 (the decision record), §6 M3 (lines 338-343), §6.6 (why Phase 11's ontology is not pre-built),
  §7 (reference sources — **names no pre-registration source today; D-14 amends it**).
- `.planning/PROJECT.md` — Key Decisions M-01…M-09, Constraints, Out of Scope, Known limits.
- `.planning/REQUIREMENTS.md:125-130` — REQ-P10-01…REQ-P10-04.
- `.planning/ROADMAP.md:432-470` — Phase 10 goal, dependencies, the verify/ship-only ordering
  constraint, and the five success criteria. `:579-592` — the dependency graph and the soft
  sequencing after Phase 7.
- `.planning/STATE.md:54-60` — open items to resolve at discuss. **Note: the numbering item at `:57`
  names Phases 7, 8 and 11, not Phase 10** (verified). D-12 above settles Phase 10's numeric code
  assignments anyway, and STATE.md gains a line recording it.
- `.planning/phases/07-.../07-CONTEXT.md:69-88` — the one-decade-per-concept numbering convention,
  set as a user decision and binding on D-12.
- `.planning/phases/09-.../09-CONTEXT.md` — the house style for this milestone's decisions; §Citations
  for the locator discipline D-14 inherits; `:169-172` for the one-fact-per-code habit D-07 applies.
- `.planning/phases/08-.../08-CONTEXT.md` — Phase 8's numbering and fixture habits.

### Source files this phase modifies or must not disturb

- `dsx/frame/prereg.py` — **new**, the module all three codes land in.
- `dsx/frame/__init__.py:13` (the family table naming Phase 10), `:16-31` (the D-03a allow-list prose
  — `dsx.decisions` is permitted, `dsx.checks` is not).
- `dsx/frame/paradigm.py:43-49` `_PARADIGM_INDEPENDENT` (lists `"DSX-PRE-"` at `:47`, **verified**);
  `:65-68` `_NOT_SHIPPED` (lists `"DSX-PRE-"` at `:66`, **verified**). Both flip in the landing commit.
- `dsx/cli.py:90-103` `GATE_PROFILES` — **`prereg` added to `verify` and `ship` only**, absent from
  `plan` and `execute` (**verified: no `prereg` entry exists today**); `:107-112` `GATE_THRESHOLDS`
  (**verified**); `:156-177` `run_checks` and the `root`-threading `elif` precedent; `:277-315`
  `_write_decision_trail` and the docstring invariant at `:288-290` that D-09 narrows (**verified**);
  `:763-768` the only two `EXIT_ERROR` returns (**verified**).
- `dsx/findings.py:23` `EXIT_ERROR = 2`; `:181-182` `exit_code()` returning only 1 or 0
  (**both verified**); `CheckError` and `require()`.
- `dsx/decisions.py:181-190` `frame_digest()` (**verified**); `:91-108` `InvocationHeader`;
  `decisions_path()` and `read_all()` — the read side D-09 needs.
- `dsx/spec.py:279-285` `DECLARATION_POINTS` and its committed forward reference to REQ-P10-02;
  `:409-410` `normalize()`; `:466` `REQUIRED_TOP_LEVEL`; `:973-980` the prose stating there is no
  unknown-key check under `inference:`; `:990-994` `_INFERENCE_MEMBERSHIP`.
- `dsx/checks/stats.py:40-127` — `recommend_test()`'s procedure lexicon. **Must not be imported**
  (D-06); named here so a planner does not rediscover it and reach for it.
- `dsx/frame/val.py:200` and `dsx/frame/interference.py:643` — the `check(spec)` signature `prereg`
  deviates from, and the module idiom to copy otherwise.
- `templates/ANALYSIS-SPEC.yaml:129` (`analysis.test`), `:355` (`declared_at`), `:358`
  (`fallback_rule`) — the scaffold, and the suppressions comment documenting the exit-2 precedent.
- `examples/good-ANALYSIS-SPEC.yaml:150` (`analysis.test`), `:231-255` (`results.tests[]` — **no
  procedure field**), `:359-364` (the `inference:` block).
- `examples/DECISIONS.jsonl` — the committed artifact proving `frame_digest` reaches disk.
- `examples/known-bad/*` — the five existing fixtures; one new fixture joins them (D-16).
- `tests/test_known_bad_corpus.py:134-138` `_TARGET_DEFECT_CODES`; `:176` the CRITICAL filter that
  makes D-11's severity load-bearing; `:243-253` the comment on why both maps exist; `:259-265`
  `_EXPECTED_CAUGHT_DEFECTS`; `:270-326` the post-mortem invariants; the incidental-allow-list guard
  that must not be weakened.
- `tests/test_dsx.py:1390-1393` (template passes `gate plan` — D-01's blast radius);
  `:2830-2834` and `:2849-2850` (the matched `_PARADIGM_INDEPENDENT` / `_NOT_SHIPPED` invariants).
- `tests/test_frame_interference.py:169-185` — the registration + reachability test pair ROADMAP
  SC 5 must copy.
- `tests/test_frame_boundary.py` — the D-03a scanner. `dsx.decisions` is a legal import; `dsx.checks`
  is not.
- `scripts/gen-finding-catalogue.py:25-52` `PREFIX_GROUPS` (**no `DSX-PRE` entry — verified**);
  `:65` `_D05_ALLOWLIST_PREFIXES` (**does not cover `DSX-PRE-` — verified; this is the quiet guard**);
  `:77-81` the `Citation:` / `Reference value:` / `Structural criterion:` regexes and the
  `# D-05: <CODE>` test-marker requirement; `:184-190` the silent-skip behaviour.
- `tests/test_gen_finding_catalogue.py:174-181`, `:227` — the guards that catch a missing prefix group
  and pin the covered code set.
- `references/finding-codes.md` — regenerate via `scripts/gen-finding-catalogue.py --write`.
- `README.md:309-323` "## Known limits"; `:338` "### Two tiers of evidentiary rigour" — the anchors
  for ROADMAP SC 4's README half.
- `scripts/check.sh:6-7` (the suite entrypoint), `:15-23` (the good-fixture exits-0-everywhere
  assertion that surfaces any accidental widening of D-01's trigger).

### Research — advisory, superseded where this file says so

- `.planning/research/ARCHITECTURE.md:165` (`prereg.py`), `:206-210`, `:231` (the verify/ship-only
  CRITICAL row — consistent with D-11), `:579-582` (M3 depends only on M1's fields, not on M2a/b/c).
- `.planning/research/PITFALLS.md:54-61` (the `declared_at` cheapest-lie problem), `:88-92` (the
  content-hash lock, now shipped — D-08), `:721` (the milestone mapping: "M3 — reconciliation checks
  the lock").
- `.planning/research/SUMMARY.md:44` — the cheapest-lie field list.

### Primary sources verified during discuss

- **Gelman, A. & Loken, E. (2014)**, "The Statistical Crisis in Science", *American Scientist*
  102(6):460-465. Full text read from two independent free copies; page numbers from printed running
  footers. **No numbered sections, tables or theorems — cite page plus unnumbered heading.** The
  symbol φ is OCR-garbled in both scans.
- **Gelman, A. & Loken, E. (2013)**, "The garden of forking paths…", Columbia University working
  paper, 14 Nov 2013, §1.1-1.2, pp. 1-3. Natively typeset. **Unpublished, no DOI or venue — a
  notation source only.**
- **Simmons, Nelson & Simonsohn (2011)**, *Psychological Science* 22(11):1359-1366, DOI
  10.1177/0956797611417632. Publisher-typeset PDF read; Table 1 (p. 1361) and the "Nonsolutions"
  passage (p. 1365) transcribed verbatim.
- **Wagenmakers et al. (2012)**, *Perspectives on Psychological Science* 7(6):632-638, DOI
  10.1177/1745691612463078. Read; p. 632 carries "the data may be used only once". Not selected as
  anchor — its remedy is labelling, not reconciliation.
- **Nosek et al. (2018)**, *PNAS* 115(11):2600-2606, DOI 10.1073/pnas.1708274114, via PMC5856500.
  **Section headings verified; per-sentence page numbers NOT verified.**
- **Claesen et al. (2021)**, *Royal Society Open Science* 8(10):211037, §3.3 — 89% figure verified.
- **Goldacre et al. (2019)**, *Trials* 20:118, via PMC6375128 — 87% figure verified.
- **Chan et al. (2004)**, *JAMA* 291(20):2457-2465 — **abstract only, paywalled. No internal locator
  verified.**

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- **`frame_digest()`** (`dsx/decisions.py:181-190`) — the content lock, shipped in Phase 6, written on
  every gate run, and provably reaching disk (`examples/DECISIONS.jsonl`). Phase 10's single largest
  saving: ROADMAP SC 4's hardest clause is already built.
- **`normalize()`** (`dsx/spec.py:409-410`) — solves the free-string comparison brittleness between
  `wild cluster bootstrap` and `wild_cluster_bootstrap` without coining a vocabulary.
- **`CheckError` raised from inside a check** — the only route to exit 2, with `apply_suppressions` as
  the working precedent and its behaviour already documented to operators in the template.
- **`DECLARATION_POINTS`'s committed forward reference** (`dsx/spec.py:279-285`) — the REQ-P10-02
  documentation is half written and waiting.
- **The registration + reachability test pair** (`tests/test_frame_interference.py:169-185`) — a
  direct template for ROADMAP SC 5's second clause.
- **The two-map corpus structure** (`tests/test_known_bad_corpus.py:134-138`, `:259-265`) — Phase 9's
  restructuring already built the per-gate-point shape a verify/ship-only family needs. Phase 10
  inherits it rather than restructuring again.
- **`Structural criterion:` as a first-class D-05 satisfier** — four shipped precedents
  (`dsx/frame/paradigm.py:350`, `:442`; `dsx/spec.py:868`, `:1015`) and an enforcement regex that
  accepts it.
- **`suppressions[]` with its ADR/SPEC authority requirement** — the M-07 grandfather path, and the
  route D-09's exit-2 message must name for a spec that never ran `gate plan`.

### Established Patterns

- **Registration and severity are independent knobs.** `GATE_PROFILES` selects where a check runs;
  `GATE_THRESHOLDS` selects what blocks there. A verify/ship-only family needs both set correctly, and
  CRITICAL is required for reasons beyond blocking — the corpus classifier filters on it.
- **Titles passed to `report.add` must be literal at the call site** — the catalogue's extractor
  requires it, and a dynamic segment collapses to `<…>`.
- **`Citation:` and `Structural criterion:` go on the ENCLOSING function's docstring**, not the
  module. This trap already bit plan 06-07.
- **Findings carry `detail` / `remedy` / `where`, with the specifics in `detail`.** `DSX-PRE-030` must
  name both branch labels in `detail`, which is ROADMAP SC 2's literal requirement.
- **Check for name collisions before coining a term** — the habit that caught the `run_id` collision
  in Phase 6. Applies to whatever D-04's fact registry is named.
- **A prefix stays in `_NOT_SHIPPED` until the phase that ships it lands**, with matched invariant
  tests on both sides. The dict is an honesty control, not bookkeeping.

### Integration Points

- `dsx/frame/prereg.py` — new module, three codes.
- `dsx/cli.py` — `GATE_PROFILES` gains `prereg` at `verify` and `ship`; `run_checks` gains a `root`
  branch for `prereg.check`; `_write_decision_trail`'s docstring invariant is narrowed to the write
  path with a stated reason.
- `dsx/frame/paradigm.py` — `_NOT_SHIPPED` loses its `DSX-PRE-` entry; `_PARADIGM_INDEPENDENT` keeps
  its one and starts resolving.
- `scripts/gen-finding-catalogue.py` — `PREFIX_GROUPS` gains a `DSX-PRE` heading;
  `_D05_ALLOWLIST_PREFIXES` gains `"DSX-PRE-"`. **The second edit is the one that is easy to miss and
  silently disables the citation gate for this family.**
- `tests/test_known_bad_corpus.py` — one new fixture, one `_TARGET_DEFECT_CODES` entry, one
  `_EXPECTED_CAUGHT_DEFECTS` key.
- `README.md` — the `declared_at` limit and the `analysis.test` plan-time caveat, under "Known limits".
- `brief.md` §7 — the Gelman & Loken anchor added.
- `references/finding-codes.md` — regenerated.
- `.planning/STATE.md` — Phase 10's numeric code assignments move from open item to resolved.

</code_context>

<specifics>
## Specific Ideas

- **"The declared fallback rule is φ; the executed procedure is φ(y)."** This one line is the phase's
  conceptual spine and should appear in the module docstring. It is what makes `DSX-PRE-030` legible
  to a reviewer in thirty seconds rather than reading as an arbitrary string comparison.
- **The block is on branch identity, never on procedure merit.** Whoever writes the `DSX-PRE-030`
  remedy must make it explicit that a *better* substituted procedure still blocks, and why — the
  substitution is itself a new researcher degree of freedom (Simmons et al. 2011, p. 1365). An
  operator who reads "your more conservative test was rejected" without that sentence will read the
  gate as broken.
- **When a locator cannot be verified, flag it — never invent it.** Carried forward from Phase 6 and
  Phase 9. D-14 carries three live flags: Gelman & Loken has no numbered structure, its φ is
  OCR-garbled, and Nosek's per-sentence pages are unverified. A future editor "tidying" these into
  confident locators would be reintroducing exactly what this discipline prevents.
- **Traceability to the brief's own wording is worth little where the brief was illustrative.** §5's
  *structure* binds; its phrasing does not bind at the token level. D-04 is this phase's instance —
  the brief's `clusters` example names a field that has never existed.
- **An inclusion list is not an exemption list.** `_D05_ALLOWLIST_PREFIXES` reads like a way to *skip*
  checking and is in fact the way to *start* checking. Whoever touches it should leave a comment
  saying so, because the next family will hit the same trap.
- **Check for name collisions before coining a term.** Applies to D-04's fact registry name and to any
  new test or helper name in `prereg.py`.

</specifics>

<deferred>
## Deferred Ideas

- **Coining `results.clusters` or a `results:` shape validator.** Declined under D-04. If a later
  phase needs the brief's `clusters` example to be expressible, it is a Phase 6 contract change with
  a template edit, a `dsx vocab` entry and an unknown-key story — not a Phase 10 side effect.
- **`DSX-PRE-011` for "rule references an unknown fact" as distinct from "rule does not resolve".**
  The decade has room; the number is deliberately unspent until a real case shows the remedies
  diverge (brief D-13's shape — an entry condition, not a wish).
- **Procedure ranking, admissibility, and any conservatism ordering.** Phase 11's `DSX-ADM-*`.
  Barred here by brief D-02, and the bar is what REQ-P10-04 is built on.
- **Asserting a published number for `DSX-PRE-*`.** Declined under D-15 with the reason recorded.
  If the phase later wants a number, the only honest framing is a seeded off-gate-path reproduction of
  Simmons Table 1 under `tests/` (the REQ-P9-07 pattern) whose `Reference value:` line states plainly
  that 60.7% bounds the *class* of defect the family prevents and explicitly not the specific mismatch
  the check detects.
- **Obtaining Chan et al. (2004) full text**, and a natively typeset copy of the published Gelman &
  Loken article that renders φ correctly. Either would close a live locator flag. Worth doing whenever
  access appears; not worth blocking this phase.
- **Making `analysis.test` structurally post-data** rather than conventionally so. Named as a known
  limit under D-05 instead. It is the same class of limit as `declared_at`, and the project's answer
  to that class is documentation plus human frame review, not more contract surface.

### Reviewed Todos (not folded)

None — `todo.match-phase 10` returned zero matches.

</deferred>

---

*Phase: 10-pre-registered-inference-plan-dsx-pre*
*Context gathered: 2026-08-13 (assumptions mode)*
