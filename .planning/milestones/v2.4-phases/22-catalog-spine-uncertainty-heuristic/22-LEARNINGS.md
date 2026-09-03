---
phase: 22
phase_name: "catalog-spine-uncertainty-heuristic"
project: "gsd-dsx"
generated: "2026-09-03"
counts:
  decisions: 7
  lessons: 7
  patterns: 6
  surprises: 6
missing_artifacts:
  - "UAT.md"
---

# Phase 22 Learnings: catalog-spine-uncertainty-heuristic

## Decisions

### GA-1 — catalog entry-set derivation and count (75-90 band, target ~80)
The merged catalog composition is: 50 DSX-admissible marks (Phase 21's closed set) + 10
uncertainty marks (frozen core = 60) + 7 refusal rows + a tunable set of reference-only
rows (spine chart types not in DSX's admissible vocabulary), sized to land the total in
the 75-90 band. The DSX-admissible + uncertainty core is frozen; reference-only rows are
the tunable remainder, chosen to fill genuine function-coverage gaps across the nine FT
categories. Actual delivered total: 81 rows (60 + 14 + 7).

**Rationale:** the requirement author set the 75-90 band expecting spine chart types
beyond DSX's gate vocabulary (FT has 66 distinct, DVC 60); reaching the band via
reference-only rows — explicitly flagged "reference-only, not in the DSX admissible
set" — documents those types without ever letting the catalog silently widen what the
gate admits. Promoting all spine types into the gate vocabulary instead was rejected
because it would balloon Phase 21's every-mark-has-a-home invariant with marks that have
no verified data-signature home, and would widen gate admission on the strength of a
reference catalog rather than a decided admissibility rule.
**Source:** 22-CONTEXT.md

---

### GA-2 — uncertainty vocabulary shape: 11th RELATIONSHIP_CHARTS key, not new input-type ids
Uncertainty enters the live chart vocabulary as an 11th `RELATIONSHIP_CHARTS` key
`"uncertainty"` carrying Wilke's ten §5.6 marks — not as new `data_input_type` /
`CHART_CAPABILITIES` family ids. The property-based `DSX-VIZ-070` check is retained,
unchanged, as a complementary verification surface ("did you show uncertainty at all?"
vs. the new key's "which mark communicates it?").

**Rationale:** Wilke's own directory (ch.5) lists Uncertainty as a peer top-level
category, so an 11th key is the paradigm-faithful modeling; it gives every one of the 10
marks a relationship home without exemptions to Phase 21's invariant; and the frozen
tuple spans frequentist marks (error bars, graded error bars, confidence strips,
confidence band) and Bayesian marks (eye, half-eye, quantile dot plot, graded confidence
band, fitted draws) symmetrically, so D-12a paradigm symmetry is expressed as one
function by construction rather than a bolted-on check. Admitting the marks via new
input-type ids was rejected because it would scatter the family across data families and
make the frequentist/Bayesian symmetry an emergent property instead of a stated one.
**Source:** 22-CONTEXT.md

---

### GA-3 — DSX-VIZ-071 minted; DSX-VIZ-072 deliberately withheld
New gate codes take the next-free number in the 07x uncertainty band. `DSX-VIZ-071` is
minted for the uncertainty-vocabulary membership check. `DSX-VIZ-072`, reserved
contingently at discuss time "only if plan finds a second distinct uncertainty check
warranted," was decided at plan time to NOT be minted.

**Rationale:** the ten §5.6 marks are deliberately paradigm-symmetric — several marks
(error bars, graded error bars) legitimately render either a frequentist confidence
interval or a Bayesian credible interval, so there is no clean mark→paradigm partition
to check against. A paradigm-mismatch gate would manufacture a false constraint and
contradict the very symmetry the family exists to express; REQ-P22-02's "D-12a-clean" is
already satisfied by construction (the 11th-key structure), needing no enforcement code.
Phase 22's blocking-code footprint is therefore exactly one code, and the set-identity
diff proves 275→276, additive-only.
**Source:** 22-CONTEXT.md; 22-02-PLAN.md; 22-02-SUMMARY.md

---

### D-1 — perceptual rank axis corrected to six ranks with ties, not a seven-item strict order
The Cleveland-McGill (1984) ordering used throughout the catalog and
`chart-selection.md` is 6 ranks over 10 tasks WITH TIES (p.536 for the list, p.537 for
the tie caveat), not a 7-item strict order: rank1 position_common, rank2
position_nonaligned, rank3 {length, direction/slope, angle} tied, rank4 area, rank5
{volume, curvature} tied, rank6 {shading, colour_saturation} tied. "density" does not
appear in the 1984 paper and must not ship as a ranked channel. The structural-criterion
test asserts `rank(a) <= rank(b)`, never a strict `<`, across tied members.

**Rationale:** this is a binding, previously-signed correction (HQ-27 pack) applied as a
hard constraint this phase, not re-opened; Heer & Bostock independently declines
`length > angle`. Shipping the old strict ordering would make an encoding-accuracy claim
the primary source does not support.
**Source:** 22-CONTEXT.md

---

### D-2 — uncertainty vocabulary corrected to Wilke's actual ten §5.6 marks
The uncertainty family ships exactly Wilke's §5.6 ten marks (error bars, graded error
bars, 2D error bars, confidence strips, eyes, half-eyes, quantile dot plot, confidence
band, graded confidence band, fitted draws) — not the four terms ("fan chart," "gradient
CI band," among others) named in the original SCOPE doc, which do not exist in Wilke's
book. "eye" (violin+error bar) is distinct from "half-eye" (ridgeline+error bar).

**Rationale:** a previously-signed correction (HQ-27 pack, D-2) applied as a hard
constraint; REQ-P22-02's original text is read "as amended" by this decision rather than
literally, since the literal text named non-existent chart terms.
**Source:** 22-CONTEXT.md

---

### Ten uncertainty marks homed into the existing `CHART_CAPABILITIES["interval-range"]` family
Rather than creating a new coarse family or a new input-type id, the ten uncertainty
marks were added to the existing `interval-range` capability (which already held box,
violin, histogram, density, ecdf, strip, kde).

**Rationale:** an uncertainty band, an error bar, and a box plot are all interval-shaped
renderings of a distribution or estimate, making `interval-range` the honest
data-signature home; this keeps GA-2's rejection of new input-type ids intact while
satisfying Phase 21's every-mark-has-a-home invariant (a mark named in
`RELATIONSHIP_CHARTS` must also appear in some `CHART_CAPABILITIES`/`EXTRA_MARKS` value).
**Source:** 22-01-PLAN.md; 22-01-SUMMARY.md

---

### gauge and word_cloud refusals reuse DSX-VIZ-001; radar citation swapped to Duan et al. 2023
`gauge` and `word_cloud` were added to `BANNED_TYPES` as complete `{reason, code,
citation}` records reusing the existing `DSX-VIZ-001` code (zero new code minted for
refusal completion), bringing the refusal set to 7. `radar`'s PROVISIONAL citation
placeholder was replaced with the signed "Duan et al. 2023 (J Clin Epidemiol 156:85-94)."

**Rationale:** the catalog's refusal rows must be backed by a live `BANNED_TYPES` entry
or they claim a ban the gate does not enforce (the drift surface Phase 21's doctrine
forbids); reusing the existing type-ban code for two more principled exclusions named in
the ROADMAP avoids minting new codes for what is structurally the same kind of refusal.
**Source:** 22-CONTEXT.md; 22-01-PLAN.md; 22-01-SUMMARY.md

---

## Lessons

### A relationship home does not imply a capability home
Adding `RELATIONSHIP_CHARTS["uncertainty"]` with its ten marks, without also adding those
marks to a `CHART_CAPABILITIES` value, would silently break Phase 21's live, currently-green
`test_every_mark_has_a_capability_home` invariant — a requirement GA-2's decision text
(which focuses on rejecting a new *input-type family*) does not itself flag. This was
discovered only by reading the existing invariant test in full, not by reasoning from the
decision record alone.

**Context:** identified as "Pitfall 1" during research and confirmed as the first
concrete task in Plan 22-01 (home the ten marks into `interval-range` before anything
else, and run the invariant test as the very first verification step after adding the key).
**Source:** 22-RESEARCH.md

---

### Minting a gate code ripples into multiple hard-coded lockstep count files, not just the obvious one
Minting `DSX-VIZ-071` required bumping `tests/test_finding_catalogue_invariant.py`'s
`_EXPECTED_TOTAL`/`_MINTED_CODES` (275→276) in the same wave, or the whole suite goes
red — this file's pinned total is not auto-derived from the catalogue at test time. Less
obviously, two *sibling* files that independently hard-code the live catalogue total for
their own zero-mint proofs — `tests/test_p19_categorical_rows.py` and
`tests/test_phase20_zero_mint_close.py` — also needed the same 275→276 bump to stay
internally consistent, even though neither was in Plan 22-02's original `files_modified`
list.

**Context:** the ripple was recorded loudly in the 22-02 summary as a necessary
consequence of a legitimate mint, not a scope violation. This is the actual mechanism
behind "prove the additive-only set-identity diff," not a separate manual proof.
**Source:** 22-RESEARCH.md; 22-02-SUMMARY.md

---

### D-05 citation enforcement is off by default for the DSX-VIZ-* family and must be turned on per-code
`gen-finding-catalogue.py`'s `_D05_ALLOWLIST_PREFIXES` does not include `"DSX-VIZ-"` (the
family has 20 pre-existing, uncited legacy codes) — so a new `DSX-VIZ-071` code would
ship with an unenforced citation unless explicitly added, by exact string, to
`_D05_ALLOWLIST_CODES`. Adding the family prefix instead would retroactively fail-red
all 20 legacy uncited codes.

**Context:** this is an established, repeatedly-used precedent from prior phases
(15/18/19), but it is easy to miss because the docstring convention (`Citation:` /
`Structural criterion:` lines) looks sufficient on its own — it is only enforced once the
exact-string allowlist entry exists.
**Source:** 22-RESEARCH.md

---

### chart-selection.md already shipped the pre-HQ-27 error and had to be actively corrected, not left alone
`references/chart-selection.md`'s "Encoding accuracy" section read "position on a common
scale → length → angle → area → colour saturation → volume" — the exact superseded
7-item strict ordering (with the false `length > angle` relation and a non-existent
"density" term) that D-1 corrected. Because REQ-P22-05 was scoped as "gate extensions,"
it could have been read as not touching this prose file, but leaving it as-is would have
shipped a repo that contradicts its own new perceptual tie-break test.

**Context:** flagged as "Pitfall 3" in research and treated as an in-scope correction
within the REQ-P22-04 edit rather than a separate ticket; the old arrow chain was removed
entirely, not left alongside the correction.
**Source:** 22-RESEARCH.md; 22-04-SUMMARY.md

---

### The visualize skill's relationship enumeration is an undocumented ripple point
`skills/dsx-visualize/SKILL.md`'s `<method>` step 1 hand-enumerates all relationship
names (comparison … composition_over_time) — a surface CONTEXT.md's bound list does not
name at all. Adding the 11th `"uncertainty"` key to `RELATIONSHIP_CHARTS` obliges an
eleventh name here, or the skill and the live vocabulary silently disagree.

**Context:** found only by reading the skill file in full during research, not inferred
from the decision record; became an explicit Plan 22-04 task and a doc-conformance test
assertion.
**Source:** 22-RESEARCH.md

---

### DVC URLs are not mechanically derivable from chart names
The Data Visualisation Catalogue's URL pattern (`datavizcatalogue.com/methods/{name}.html`)
looks mechanical but isn't — `treemap.html` has no underscore, so a
`.replace(" ","_").lower()`-style transform would silently ship some fraction of broken
links for reference-only rows attested by DVC.

**Context:** flagged in research (Pitfall 4, sourced from HQ-27's T2-4) as requiring
build-time URL resolution/confirmation, never name-generation. In execution, the phase
avoided the risk entirely by not asserting any per-method DVC URL (see the related
Decision on reference-only sourcing), which was recorded as a deliberate,
more-provable-claim choice.
**Source:** 22-RESEARCH.md

---

### Two heuristic-layer citations (Abela 2008, Few's Graph Selection Matrix) were never HQ-27-verified at all
Unlike the "8 still-unverified" items HQ-27 explicitly flags, Abela 2008 and Few's Graph
Selection Matrix — named in the original SCOPE doc as provenance for the L1/L2 heuristic
layers — do not appear anywhere in the signed HQ-27 pack, not even among the
still-unverified rows. They were simply never submitted for verification, which is a
different (and stricter) category than "verified but flagged uncertain."

**Context:** this distinction drove the decision to drop both sources entirely from the
shipped heuristic edits (option (a) of the research's Open Question 1) rather than
citing them as background attribution.
**Source:** 22-RESEARCH.md

---

## Patterns

### Additive dict-value promotion, never a parallel structure
When a check needs richer or additional metadata than an existing dict/tuple provides,
promote the value in place (e.g., add a key to `RELATIONSHIP_CHARTS`, extend
`BANNED_TYPES`'s per-entry shape) rather than introducing a second lookup table that
tracks the same membership information under a different name.

**When to use:** any time a new mark/type/rule is tempting to track in a purpose-built
parallel dict "for clarity" — the single existing structure should remain the one source
of truth, avoiding a second invariant to police for consistency with the first.
**Source:** 22-RESEARCH.md

---

### Fenced JSON-in-Markdown for a reference doc a test must parse
A Markdown reference file carries both a human-readable table and a single fenced
` ```json ` block with the same content in machine-parseable form; a test or generator
extracts it with `re.search(r"```json\s*(\{.*?\})\s*```", text, re.S)`.

**When to use:** any reference doc that needs to be both human-readable and structurally
parseable for several semantically distinct fields per row (here: function axis,
data-signature, perceptual channel, citation, flag) — table-cell regex parsing is
fragile once a field (like a citation string) can itself contain `|`.
**Source:** 22-RESEARCH.md; 22-03-PLAN.md

---

### Exact-code D-05 allowlisting into a family with legacy uncited codes
When a new finding code lives inside a large pre-existing family that has legacy uncited
codes, add the new code by exact string to `_D05_ALLOWLIST_CODES`, never add the
family's prefix to `_D05_ALLOWLIST_PREFIXES`.

**When to use:** minting any new gate code whose family (e.g. `DSX-VIZ-*`) already ships
older codes without a citation — an established precedent across five prior phases in
this repo.
**Source:** 22-RESEARCH.md; 22-02-PLAN.md

---

### Catalog-generated-from-live-source with bidirectional set-identity conformance
A reference catalog's rows for a live-gated concept (admissible marks, banned types) are
generated from the live authority dict/function (e.g., `_mark_universe()`,
`BANNED_TYPES`), not hand-transcribed, and a repo-integrity test asserts set-equality in
both directions (every live item has exactly one catalog row; every flagged catalog row
names a live item).

**When to use:** any reference/documentation artifact that claims to describe a live,
gate-enforced vocabulary — this is the mechanism that makes "the catalog conforms to the
vocabulary" a runnable guarantee rather than a claim that can silently drift.
**Source:** 22-03-PLAN.md; 22-03-SUMMARY.md; 22-REVIEW.md

---

### Pure ordering / tie-break structural criterion kept off the gate path
An ordinal claim that includes ties (here, the Cleveland-McGill perceptual ranks) is
encoded as `rank(a) <= rank(b)` — never a strict `<` across tied members — and lives as a
repo-integrity test in `tests/`, not as a `report.add(...)` gate check, because it
performs no computation and adjudicates nothing about a user's spec.

**When to use:** whenever a source's finding includes ties or partial orders; asserting
a strict total order where the primary source only supports a partial one with ties is a
common way to overclaim an encoding-accuracy finding.
**Source:** 22-CONTEXT.md; 22-03-PLAN.md

---

### CRLF-safe, non-line-anchored regex for Markdown-reading tests
Every new test reading a `.md` file (chart-catalog, chart-selection, question-taxonomy,
SKILL.md) uses whitespace-collapsing, non-`^`/`$`-anchored matching so a phrase spanning
a wrapped line or a `\r\n` line ending still matches.

**When to use:** any repo-integrity test asserting presence/absence of a substring in a
Markdown file in a repo that checks out CRLF on Windows — a bare `\n`-anchored pattern
will silently fail to catch what it's meant to guard against.
**Source:** 22-RESEARCH.md

---

## Surprises

### The "three independent" spine sources are actually one design lineage
The Financial Times poster, the Graphic Continuum, and the Data Visualisation Catalogue
are not three independent authorities: Ribecca authored both the Graphic Continuum and
the Data Visualisation Catalogue, and the FT poster itself credits the Graphic Continuum
as its inspiration.

**Impact:** the catalog must never claim triangulation across FT/GC/DVC as independent
corroboration for a reference-only row — citations attested only by this lineage must
name it as one source. Genuine independence for the catalog's other two axes comes only
from Munzner's task taxonomy and Cleveland-McGill's encoding work.
**Source:** 22-CONTEXT.md

---

### "fan chart" and "gradient CI band" are not real Wilke terms
The original SCOPE doc named these as part of the uncertainty vocabulary, but neither
term exists in Wilke's book at all — the actual §5.6 vocabulary is ten different named
marks (error bars, graded error bars, 2D error bars, confidence strips, eyes, half-eyes,
quantile dot plot, confidence band, graded confidence band, fitted draws).

**Impact:** any code, docstring, or catalog row that had used the SCOPE doc's original
names would be citing chart types that do not exist in the cited source; REQ-P22-02's
literal text had to be read "as amended" by the D-2 correction rather than at face value.
**Source:** 22-CONTEXT.md; 22-VERIFICATION.md

---

### The repo was already shipping an unsupported strict perceptual ordering before this phase
`chart-selection.md`'s pre-existing "Encoding accuracy" line asserted a strict 7-item
total order (including `length > angle` and a "density" channel) that the primary 1984
source does not actually support — the source is 6 ranks over 10 tasks with ties, and
"density" is absent from the paper entirely.

**Impact:** this was a live, already-shipped correctness gap discovered only via the
signed HQ-27 verification pass, not something introduced by this phase — it had to be
actively corrected in the same pass that added the new tie-break test, or the repo would
ship self-contradicting guidance.
**Source:** 22-CONTEXT.md; 22-RESEARCH.md

---

### Prior planning docs had the wrong counts for DVC and FT
The Data Visualisation Catalogue was believed to have ~77 methods; the verified count is
60. The FT poster was believed to have 72 named entries; the verified count is 74 named /
66 distinct.

**Impact:** any prose elsewhere in the repo (SCOPE doc, ROADMAP) citing the old counts is
now known-stale relative to the signed pack, and the corrected counts had to be used in
the catalog's own intro prose.
**Source:** 22-RESEARCH.md

---

### Few's actual grounds for banning gauges do not include "arbitrary maximum"
Few's cited grounds for excluding gauge charts are wasted space, missing context, and an
unlabeled scale — the "arbitrary maximum" criticism commonly associated with gauge
criticism turned out to be DSX's own reasoning, not something Few argued.

**Impact:** the gauge refusal record's reason string had to explicitly separate what is
attributed to Few from what is the project's own claim, to avoid misattributing an
argument to a cited source (a repudiation-class risk the phase's threat model tracked
directly as T-22-02).
**Source:** 22-CONTEXT.md; 22-01-PLAN.md

---

### radar's citation had been shipping as an unresolved PROVISIONAL placeholder
Before this phase, `BANNED_TYPES["radar"]`'s citation was a PROVISIONAL placeholder
loosely gesturing at "Tufte 1983 / Munzner 2014" rather than a specific, verifiable
source — a gap that had been live in the shipped gate vocabulary until the HQ-27
verification pass surfaced and resolved it with a specific paper (Duan et al. 2023,
J Clin Epidemiol 156:85-94).

**Impact:** confirms that PROVISIONAL citation placeholders can persist in a shipped,
gate-enforced vocabulary for multiple phases until a dedicated verification pass catches
them — a repudiation-class gap the phase's own citation-traceability tests now guard
against recurring.
**Source:** 22-RESEARCH.md

---
