---
phase: 26-per-skill-read-contracts
verified: 2026-09-07T08:51:00Z
status: passed
verdict: PASSED
score: 3/3 requirements MET (REQ-P26-01/02/03); all four hard invariants proven; 3 review findings dispositioned (0 fixed, 3 accepted latent-robustness residuals documented)
behavior_unverified: 0
overrides_applied: 0
re_verification: false
gaps: []
human_verification:
  - "End-of-phase security sign-off (S2-5 /gsd-secure-phase 26) — batched to HUMAN-QUEUE, non-blocking until S7-2 per brief §6."
  - "End-of-phase UAT round (S2-5 /gsd-validate-phase 26) — batched, non-blocking until S7-2."
---

# Phase 26: Per-skill read contracts — Verification Report

**Phase Goal:** Each of the five downstream skills — `dsx-scope-analysis`,
`dsx-define-metrics`, `dsx-design-experiment`, `dsx-build-model`, `dsx-narrate` —
gains one named-input read step at its head, stating the `EDA.md` front-matter keys
and the `DATA-PROFILE.yaml` keys it reads, what each changes in its output, and the
recorded fallback when the artifact is absent (`eda_artifact: none`), mirroring the
executor fragment's existing rule; an off-gate-path repo-integrity guard asserts
every named key resolves against the live templates (CRLF-tolerant) so a renamed key
fails the suite instead of silently orphaning a read step; the phase is skill-only —
`dsx/` byte-identical, zero new finding codes, installed copies re-synced.

**Verified:** 2026-09-07 (orchestrator, gates re-run on real Python 3.12.10)
**Status:** passed — 3/3 requirements MET

## Verdict

`passed`. All three phase requirements are met, all four hard invariants are proven
by independently re-run gates (not trusted from a subagent report), and the code
review returned **0 HIGH / 0 MEDIUM / 3 LOW** — the three LOW findings are
latent-robustness notes about hypothetical future template shapes, none triggered by
the current templates or skills, all accepted as documented residuals with their
reasoning recorded. No requirement is provisional.

## Requirement verdicts

### REQ-P26-01 — MET
Each of the five skills carries exactly one `<inputs>` block immediately after its
`<objective>` (head position, D-26-01), naming its `EDA.md` front-matter keys and its
`DATA-PROFILE.yaml` fallback keys one backtick-wrapped key per bullet, a "These set:"
clause stating what each key changes in the skill's output, and a `When absent:`
fallback that records `eda_artifact: none` before sourcing from the profile (D-26-03,
mirroring the executor fragment's honesty ladder). Evidence:
`test_every_skill_carries_at_least_one_key_region` (`checked == 5`) and
`test_when_absent_names_eda_artifact_none` both green in the full suite (1590 OK);
confirmed by inspection of the `818fb7c..HEAD -- skills/` diff (5 blocks, +521 lines,
zero `dsx/`/`templates/` change).

### REQ-P26-02 — MET
`tests/test_skill_read_contracts.py` (off-gate-path, stdlib-only) parses the live
templates and asserts every EDA key a skill names is a member of `templates/EDA.md`'s
front-matter block and every profile key is a member of `templates/DATA-PROFILE.yaml`
(uncommenting the `#` example lines first so the per-column/flag-gated keys
`columns[].*`, `unit.*`, `target.*` count), splitting on `\r?\n` for the mixed
CRLF/bare-LF templates. A renamed or fabricated key **fails** the suite:
`test_negative_control_orphan_key_is_rejected` rejects `grain.__orphan__` /
`columns[].__orphan__` while its positive-sibling assertions prove the rejection is
discrimination, not a degenerate empty set. The code review's exhaustive rename probe
(every leaf key, every parent — `columns`/`time`/`target`/`unit`/`grain`/
`implied_dependence`/`dependence`/`base_rate` — and the `column_name` placeholder)
confirmed each rename leaves **zero surviving referenced keys**, so the load-bearing
property holds robustly rather than by happenstance. Anti-vacuity anchored
(`test_anchor_non_vacuity`: ≥30 EDA keys, profile non-empty, `columns[].null_rate`
present only after the uncomment step ran); parse determinism / order-independence
proven (`test_parse_is_deterministic_and_order_independent`); the ratified D-26-02
matrix is drift-guarded (`named == expected` in
`test_skill_keys_are_members_of_live_templates`).

### REQ-P26-03 — MET
Skill-only. `git diff --stat 818fb7c..HEAD -- dsx/` is **empty** (byte-identical for
the phase); `dsx/checks/`, `dsx/frame` and the `data[].assertions` vocabulary are
untouched. Catalogue set-identity **276 → 276**, re-measured live
(`scripts/gen-finding-catalogue.py --check` → "finding catalogue is current"; 276 code
rows counted; `tests/test_finding_catalogue_invariant.py` green). `node install.mjs
--check` passed (6/6 agents, 14/14 skills, 5 gates, self-test passed) after S2-3's
`node install.mjs` re-sync — the installed copies match the repo. Zero new finding
codes. The skills live as a single copy under `skills/` (not mirrored inside `dsx/`),
so byte-identical-`dsx/` and installer-synced do not conflict.

## Hard-invariant proof (gates re-run by the orchestrator on real 3.12.10)

| Invariant | Evidence | Result |
|---|---|---|
| Full test suite green | `python312 -m unittest discover -s tests -q` | **Ran 1590 tests — OK** (62 s; explain tests did not false-fail on the clean tree) |
| One `<inputs>` block per skill, at the head | `test_every_skill_carries_at_least_one_key_region` (`checked == 5`) + head-position inspection (after `<objective>`) | PASS |
| Every named key resolves live; every rename caught | `test_skill_keys_are_members_of_live_templates` + `test_negative_control_orphan_key_is_rejected` + reviewer's exhaustive leaf+parent+placeholder rename probe | PASS |
| Also-consult prose stays unparsed (zero backticks) | `test_also_consult_line_has_zero_backticks` (`dsx-define-metrics:40`, `dsx-build-model:40`) | PASS |
| Guard stdlib-only, zero `dsx` import | imports `re`/`unittest`/`pathlib`/`__future__` only; structurally outside `test_gate_path_hermetic`'s import closure (`tests/` never in it) | PASS |
| CRLF tolerance | `\r?\n` split; EDA.md CRLF / DATA-PROFILE.yaml bare-LF both parse to non-degenerate sets | PASS |
| `dsx/` byte-identical for the phase | `git diff --stat 818fb7c..HEAD -- dsx/` empty | PASS |
| Catalogue set-identity 276 → 276 | `gen-finding-catalogue.py --check` "current"; 276 rows; `test_finding_catalogue_invariant` | PASS |
| Installed copies re-synced | `node install.mjs --check` passed (6/6 agents, 14/14 skills, self-test) | PASS |

## Code review disposition (`26-REVIEW.md` — 0 HIGH / 0 MEDIUM / 3 LOW)

All three findings are latent-robustness notes about hypothetical **future** template
shapes; none is triggered by the current templates or skills. Each was verified
against the test file by the orchestrator before disposition. All **ACCEPTED as
documented residuals** — no code change is owed, and hardening now would be
gold-plating with no shipped input exercising it (mirroring the S1-4 L-01 disposition
pattern).

- **IN-01 (positional `#` stripping) — ACCEPTED.** `_INLINE_COMMENT_RE` and the
  profile uncomment (`ln.replace("#", " ", 1)`) treat `#` positionally, not YAML-aware.
  But the extractor uses a line's value **only** to test emptiness (`value == ""` → can
  host children) and never records the value, so a `#`-in-value could corrupt a key path
  only if it flipped a non-empty value to empty (spurious parent) — impossible for the
  current templates, where no value embeds `#`. The constraint is already documented in
  the test module's docstring; a quoted-string guard is the fix if a template ever needs
  a literal `#` in a value.
- **IN-02 (`_KEY_RE` drops hyphenated key names) — ACCEPTED.** The name class
  `[A-Za-z_][A-Za-z0-9_]*` excludes `-`. Current templates use underscore keys
  exclusively; were a hyphenated key ever named, the failure mode is a **loud** spurious
  membership failure (false-non-membership → the guard fails), **not** a silent orphan —
  the safe direction for REQ-P26-02, whose whole purpose is to never silently miss an
  orphaned read step. No hardening owed until the project adopts hyphenated YAML keys.
- **IN-03 (intermediate map-header paths accepted as members) — ACCEPTED.** By design
  the extractor records every dotted path including parents, which is precisely what
  stops a parent rename from being masked by a same-named leaf elsewhere (the leaf-only
  design was rejected in D-26-04). No current skill names a bare parent, and the
  `named == expected` drift guard would force any future bare-parent addition to be a
  conscious edit of the ratified matrix. A leaf-only assertion would add strictness the
  matrix does not need.

## Human Verification Required

Batched, non-blocking until S7-2 (per brief §6): the Phase 26 `/gsd-secure-phase 26`
security sign-off and `/gsd-validate-phase 26` UAT round (both S2-5). Neither gates
this `passed` verdict — Phase 26 has no user-facing runtime behaviour beyond the
agent-facing skill prose and the static repo-integrity guard, so its acceptance test
is the automated invariant set proven above.

---

_Verified: 2026-09-07 by the autonomous ceremony orchestrator (gates re-run on real Python 3.12.10)._
