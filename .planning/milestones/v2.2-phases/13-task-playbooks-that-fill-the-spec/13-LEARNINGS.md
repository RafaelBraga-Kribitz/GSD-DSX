---
phase: 13
phase_name: "Task playbooks that fill the spec"
project: "gsd-dsx"
generated: "2026-08-29"
counts:
  decisions: 8
  lessons: 3
  patterns: 4
  surprises: 2
missing_artifacts:
  - "UAT.md"
---

# Phase 13 Learnings: Task playbooks that fill the spec

## Decisions

### D-01: Skill packaging — pure prompt-guidance, name-only registration
The four playbooks (`dsx-cohort`, `dsx-funnel`, `dsx-root-cause`, `dsx-segment`) are one
`skills/<name>/SKILL.md` each, plus a four-line append to `capability.json`'s flat `"skills"`
array. No `steps`/`contributions`/`gates`/`agents` entry is added for any of them; only
`dsx-scope-analysis` is loop-wired. No Python is added under `skills/` or `capabilities/`.

**Rationale:** Only `dsx-scope-analysis` is loop-wired; the other eight registered skills appear only in the flat `"skills"` array and are invoked by name — matching that pattern is the whole point of an on-demand playbook. Loop-wiring an advisory playbook would fire it unconditionally at a loop point, an unrequested behaviour change. Since both `skills/` and `capabilities/` trees are Python-free and the catalogue generator only walks `dsx/**/*.py`, markdown/JSON here is structurally incapable of minting a finding code.
**Source:** 13-CONTEXT.md

---

### D-02: Field→gate contract — route-and-cite, never restate
Each playbook is expressed as *which existing `ANALYSIS-SPEC.yaml` field it writes* and *which
already-shipped gate reads that field* — zero parallel advice. A playbook may name a gate + its
finding code and tell the analyst to run `dsx gate/check`; it may not state a numeric threshold,
correction method, or admissible-chart rule of its own.

**Rationale:** Mirrors the house style already used in the executor fragment, which cites `DSX-MET-040` rather than restating the SQL rule. The enforcement mechanism is a plan-checker/review step asserting every threshold/number in the four `SKILL.md` files is either absent or immediately attributed to a `DSX-*` code, preventing the skills from becoming a second, drifting copy of the deterministic checks' advice.
**Source:** 13-CONTEXT.md

---

### D-03: Hypothesis register carrier — both existing carriers, keyed by shape
`dsx-explore-data`'s hypothesis register is a deterministic router, not a new schema: an untested
belief the analysis rests on maps to `assumptions[]` (adjudicated by `DSX-COH-030`/`DSX-COH-031`);
a hypothesis promoted to a confirmatory test is declared in `design.multiplicity.family[]` at scope
time and filled into `results.tests[]` at execute (adjudicated by `DSX-EXP-050..053`).

**Rationale:** The "register" itself is the existing `EDA.md` findings/comparisons ledgers — REQ-P13-02 is a mapping rule, not a new carrier, and it reuses the candidate→confirmatory promotion path the skill already ships ("promoted only by a spec amendment adding the test to `design.multiplicity.family`; never promotes a candidate into `decision.replay`"). Mints nothing.
**Source:** 13-CONTEXT.md

---

### D-04: Narrative shape — template-only mapping, no DSX-NAR mint
`dsx-narrate`'s What/So What/Now What shape is layered onto the skill's existing five-part
structure (What=§1 the answer, So What=§2 the decision-rule action, Now What=§4 what would change
it) rather than becoming a new gate. It explicitly does not add a heading-scanner `DSX-NAR-0xx`
code.

**Rationale:** `dsx/checks/narrative.py` has no section/shape check to ride — it only emits `DSX-NAR-001`/`-010` (path), a claim⊆deliverable check, and a forbidden-wording scan. Adding a new shape code would move the catalogue off 256 and fail the REQ-P13-06 scope-bound gate (S1-5). The shape gets as much teeth as the existing codes allow (`decision.revisit_when`/`DSX-COH-040`, non-empty `limitations[]`/`DSX-CLM-080`) and no more.
**Source:** 13-CONTEXT.md

---

### D-05: Tier routing — advisory recommendation, not a config mutation
`dsx-scope-analysis` classifies the engagement and recommends a ceremony tier (lookup→Tier 0,
ad-hoc→Tier 1, full pipeline→Tier 2) and emits the exact command `pwsh scripts/gsd-tier.ps1 -Tier
N` — it does not call `config-set` itself.

**Rationale:** `gsd-tier.ps1` flips global `workflow.*`, `granularity`, `model_profile` and `mode` in one shot; a spec-scoping skill silently switching the whole project to `interactive`/`quality` mid-loop would be an unauditable side effect outside its remit. Rigour forbids the side effect while the deterministic mapping still matches `docs/gsd-tiers.md`.
**Source:** 13-CONTEXT.md

---

### D-06: Executor entrypoint preference — one fragment bullet, ordering fidelity not leakage
Added a single prose bullet to `capabilities/dsx/fragments/executor.md` preferring a
`scripts/*.py` entrypoint over a notebook, citing `DSX-REP-040` (fires HIGH on an `.ipynb`
entrypoint unless it runs clean top-to-bottom) and the `DSX-CODE` fit-order scan (reads notebook
JSON offsets a user cannot usefully open, versus `.py` source directly).

**Rationale:** The deterministic gate stays suffix-neutral (`code.py` reads `.py` and `.ipynb` identically) — no code minted, no gate behaviour changed. The benefit must be stated as *ordering fidelity* (a linear `.py` is a faithful record of execution order) and explicitly **not** sold as a leakage-detection claim.
**Source:** 13-CONTEXT.md

---

### D-07: Scope-bound gate — assert by set-identity diff, not count alone
REQ-P13-06's S1-5 gate rides both (a) the existing count invariant (`_EXPECTED_TOTAL = 256`) and
`gen-finding-catalogue.py --check` exit 0, and (b) a new set-identity diff against a frozen
Phase-12 code-set snapshot (a byte-copy of the *generated* catalogue, not hand-edited), asserting
`current_code_set == phase12_code_set`.

**Rationale:** A count invariant catches any pure addition but leaves a swap hole — a mint-one/drop-one that preserves cardinality passes it. A diff is a set comparison, strictly stronger than a count, which is the required assertion under the tie-break rigour > reliability > flexibility. Regex must be CRLF-tolerant (`\r?\n`) since the repo checks out CRLF.
**Source:** 13-CONTEXT.md

---

### D-08: Finding-code footprint — zero mint, with DSX-COH naming caveat
Phase 13 mints zero `DSX-*` codes; the catalogue stays at 256. `dsx-cohort` routes to the existing
*coherence* `revisit_when` check `DSX-COH-040` but must not imply a `DSX-COH-*` "cohort" code
family exists.

**Rationale:** `DSX-COH-*` stands for "Coherence", not "Cohort" — a `dsx-cohort` playbook casually asserting a `DSX-COH-*` cohort family would read as minting a new family even though no code changes. The correct framing is: cohort points at the existing coherence `revisit_when` check.
**Source:** 13-CONTEXT.md

---

## Lessons

### An over-eager literal verify block was sidestepped, not fixed
Both `dsx-cohort`/`dsx-funnel` (13-01) and `dsx-root-cause`/`dsx-segment` (13-02) were authored
with **zero** threshold-shaped prose (no percentages, decimal comparisons, p-value syntax, alpha,
or correction-method names) anywhere in the file, rather than relying on same-line `DSX-`
attribution to survive the anti-parallel-advice grep. Both summaries flag this as deliberately
avoiding a "KNOWN VERIFY-BLOCK NIT": the plan's literal `<verify>` block ends in
`grep -q 'DSX-\|.'`, which over-matches *any* non-empty line surviving the pipe — including a
threshold correctly attributed to a `DSX-*` code on the same line — so it could false-fail a
compliant file. Writing no threshold-shaped prose at all is a strictly stronger compliance than
attributing every number, and it happens to dodge the buggy verify block too.

**Context:** Both executors chose the same workaround independently across two plans in the same wave, rather than either plan author fixing the verify-block regex itself.
**Source:** 13-01-SUMMARY.md, 13-02-SUMMARY.md

---

### Avoid literal substrings an automated grep could misread as the assertion being negated
`dsx-cohort/SKILL.md`'s naming caveat (D-08) needed to state that no `DSX-COH-*` "cohort" code
family exists, but the executor deliberately avoided writing the literal substring "cohort code"
anywhere in the file (even inside a negation like "not because a cohort code family exists"),
because an automated grep for that phrase would find a hit and could misread the negation as an
assertion.

**Context:** A manual-read acceptance criterion ("grep `cohort code` returns no hit implying a new family") could be satisfied more robustly by never emitting the flagged substring at all, rather than trusting a reviewer or grep to correctly interpret a negated sentence.
**Source:** 13-01-SUMMARY.md

---

### Advisory content belongs in the file matching its audience, not the nearest shared file
The tier-routing table (REQ-P13-04) was placed in `skills/dsx-scope-analysis/SKILL.md`, not in
`capabilities/dsx/fragments/scope-analysis.md`, even though the fragment was a plausible
alternate home ("possibly scope-analysis.md" per 13-CONTEXT's integration-points note).

**Context:** The fragment is a terse planner-facing instruction ("produce ANALYSIS-SPEC.yaml before planning"); tier routing is analyst-facing scope guidance and belongs in the skill the analyst actually reaches for. This choice also kept `files_modified` minimal and avoided editing a planner-injected file for analyst-facing content.
**Source:** 13-04-PLAN.md

---

## Patterns

### Route-and-cite skill authoring
A `SKILL.md` names the `ANALYSIS-SPEC.yaml` field it fills and the existing `DSX-*` gate/code that
adjudicates it; it states no threshold, correction method, or admissible-chart rule of its own.
Mirrors the pre-existing executor fragment style that cites `DSX-MET-040` instead of restating the
SQL rule.

**When to use:** Any prompt-guidance skill or fragment that touches a spec field already governed by a deterministic check — prevents the skill from becoming a second, drifting source of truth for a rule the gate already owns.
**Source:** 13-CONTEXT.md (D-02); corroborated by 13-01-SUMMARY.md, 13-02-SUMMARY.md

---

### Router SKILL.md structural template
`<objective>` (states it is a router, not an author) → `<when_to_reach_for_this>` →
`<field_to_gate_routing>` (table: spec field | example | existing gate) → skill-specific routing
section(s) → `<what_this_skill_does_not_do>` (explicit no-threshold disclaimer). Established by
13-01 and deliberately mirrored by 13-02 for cross-playbook consistency, even though the plan
prose did not mandate that exact section layout.

**When to use:** Authoring any new prompt-guidance playbook skill intended to sit alongside others in a named family — gives every playbook in the family the same shape so an analyst or reviewer knows where to look.
**Source:** 13-01-SUMMARY.md, 13-02-SUMMARY.md

---

### Gate-path purity by construction, certified by scope-fence diff
The finding-catalogue generator only walks `dsx/**/*.py`; markdown skills and JSON registry
entries are structurally incapable of minting a code. A phase-wide zero-mint claim is certified not
by trusting each plan's self-report but by an end-of-phase `git diff --stat` scope-fence check
confirming zero `dsx/` files and zero `scripts/*.py` check-code files changed.

**When to use:** Any phase that must guarantee zero collateral change to a deterministic/generated surface — identify the generator's actual input surface first, then certify by diff at the end rather than by review.
**Source:** 13-CONTEXT.md; VERIFICATION.md (scope-fence confirmation)

---

### Set-identity diff over count invariant for zero-mint certification
A bare count invariant (`_EXPECTED_TOTAL`) passes a cardinality-preserving mint-one/drop-one swap.
Extending it with a CRLF-safe set-identity diff against a frozen, generator-produced snapshot
(never hand-authored, to avoid formatting false-fails) closes that hole and reports
added/removed codes explicitly on failure. The set-diff reuses the same row parser as the count
invariant (no parser drift) and lives co-located in the same test file.

**When to use:** Whenever a phase's scope bound is "adds nothing" against an enumerable, generated artifact (a finding-code catalogue, an API surface list, a schema field list) — a diff is strictly stronger than a count.
**Source:** 13-CONTEXT.md (D-07); 13-05-SUMMARY.md

---

## Surprises

### The plan's own literal automated verify block was over-eager
The anti-parallel-advice `<verify>` block shipped in both 13-01-PLAN.md and 13-02-PLAN.md ends
with `grep -q 'DSX-\|.'`, which matches on any non-empty line surviving the preceding pipe —
meaning it could false-fail a threshold correctly attributed to a `DSX-*` code on the same line,
the exact case the acceptance criteria intended to allow. Both plans' executors independently
recognized this and worked around it by authoring zero threshold-shaped prose at all, rather than
by exercising (or fixing) the edge case the verify block was nominally checking.

**Impact:** The literal verify blocks passed on first attempt in both plans, but the phase never actually exercised the "threshold present and correctly attributed to a DSX- code" case the acceptance criteria describe as compliant — that edge case remains unverified by the automated gate, only argued in prose.
**Source:** 13-01-SUMMARY.md, 13-02-SUMMARY.md

---

### Pre-existing shipped-tree duplicate-declaration noise does not move the catalogue count or set
The shipped tree carries known double-declare warnings (`DSX-CLM-020/021`, `DSX-COH-030`,
`DSX-PAR-002`, `DSX-SPEC-070`, `DSX-VAL-021`, `DSX-VAL-060`) that predate Phase 13, yet
`gen-finding-catalogue.py --check` still exits 0 and the Phase-13 set-identity diff still reports
`added=[] removed=[]` against the frozen Phase-12 snapshot — the noise is cosmetic and does not
change `len(rows)` or the distinct-code set.

**Impact:** Confirms the warnings are pre-existing shipped-tree debt unrelated to Phase 13's zero-mint guarantee, but leaves a latent inconsistency (codes declared twice) in the catalogue generator's output that a future phase auditing the generator itself may need to investigate.
**Source:** 13-CONTEXT.md, 13-05-SUMMARY.md
