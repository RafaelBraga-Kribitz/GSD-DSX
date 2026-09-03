---
phase: 23
phase_name: "style-snippet-layer"
project: "gsd-dsx"
generated: "2026-09-03"
counts:
  decisions: 7
  lessons: 5
  patterns: 5
  surprises: 4
missing_artifacts:
  - "UAT.md"
---

# Phase 23 Learnings: style-snippet-layer

## Decisions

### Four-file style set with a distinct license posture per file
Exactly four `.mplstyle` files ship in `styles/`: `dsx-538` (fork of matplotlib's bundled
`fivethirtyeight`, Matplotlib License, vendored verbatim), `dsx-urban` (Urban Institute
palette hexes + rcParams, house default), and `dsx-econ` / `dsx-bbc` (reimplemented from
published doctrine only — no PDF embed, no GPL port, no proprietary font).

**Rationale:** narrows license risk to exactly three genuinely vendored assets (the mpl
fork, the Urban hexes, the Lato font) that need at-locator confirmation; the
reimplement-from-doctrine posture for dsx-econ/dsx-bbc is safe under any license the
source carries since nothing is copied, so their license facts are load-bearing only for
header wording, not for shipping safety.
**Source:** 23-CONTEXT.md (GA-1, Auditor robustness note)

---

### One vendored OFL font (Lato) as the universal deterministic house face
Vendor exactly one OFL family — Lato (SIL OFL 1.1), registered via `font_manager` — and
have every style, including `dsx-econ`/`dsx-bbc` (standing in for the proprietary Econ
Sans/Milo and Reith faces), resolve `font.family` to it, with a header note stating the
substitution.

**Rationale:** one font family means one determinism surface to prove; a second OFL
family for closer aesthetic fidelity was explicitly named and deferred as a "plan-level
nicety." Keeps all four styles deterministic without ever touching a proprietary or GPL
asset.
**Source:** 23-CONTEXT.md (GA-1, "Font strategy")

---

### dsx_plotstyle.py's three keyword-explicit signatures, with `source` mandatory
`finalise_figure(fig, *, title, source, subtitle=None, note=None)`,
`direct_label(ax, *, ...)`, and `save_deterministic(fig, path, *, metadata=None,
**savefig_kwargs)` were pinned as the public surface. `source` is a required keyword with
**no default** — a call omitting it raises `TypeError` at call binding.

**Rationale:** keyword-only params make each call self-describing (documentation by
signature) and prevent positional-argument mistakes; making `source` mandatory-by-signature
enforces the "every figure cites its source" doctrine mechanically instead of by
convention, mirroring `DSX-VIZ-062`.
**Source:** 23-CONTEXT.md (GA-2); 23-02-PLAN.md

---

### `save_deterministic` writes, `dsx seal` hashes — single-hasher rule
`save_deterministic` was deliberately given no hashing responsibility; it writes the SVG
and returns a `Path`. Hashing stays exclusively with `dsx seal` (stdlib `hashlib`).

**Rationale:** the rejected alternative — returning a sha256 from `save_deterministic` —
would create a second hasher that could silently diverge from `dsx seal`. Keeping one
source of truth for the hash was chosen over the convenience of a one-call write-and-hash
API. Rigour over convenience.
**Source:** 23-CONTEXT.md (GA-2)

---

### The GA-3 determinism recipe's five pinned elements
`svg.fonttype: path` + a fixed `svg.hashsalt` + `metadata={'Date': None}` + Lato registered
via `font_manager.addfont` before `font.family` resolves + a pinned matplotlib version
recorded in `FIGURE-MANIFEST.yaml`, proven by an off-gate-path double-render
hash-equality test.

**Rationale:** each element closes one specific, named non-determinism source (font
substitution, per-process random id salt, per-render timestamp, a font-resolution race,
cross-matplotlib-version path-rendering drift) rather than being a generic best-practice
bundle. Recording the pinned version states the reproducibility bound honestly instead of
pretending cross-version stability.
**Source:** 23-CONTEXT.md (GA-3)

---

### Add "matplotlib" to `test_gate_path_hermetic`'s FORBIDDEN set
Even though the helper's location in `templates/` already keeps it structurally outside the
`dsx/` AST closure the hermeticity test walks, the team additionally added `"matplotlib"`
to the guard's `FORBIDDEN` set (D-P23-03).

**Rationale:** a cheap, strictly-strengthening structural guard that turns a future "just
render inline on the gate path" regression red instead of letting it ship silently; safe
to add today because no gate module imports matplotlib (`figures.py` is `hashlib`-only).
**Source:** 23-CONTEXT.md (D-P23-03); 23-02-PLAN.md / 23-02-SUMMARY.md

---

### Zero-mint phase: route to codes, defer the palette gate behind D-13
The snippet catalog routes to existing finding codes instead of restating gate thresholds;
the determinism test carries no `report.add`; and the WCAG-AA palette gate is deferred
behind a D-13 entry condition rather than minted this phase. Phase 23 mints zero new codes,
proven by a `276 → 276` set-identity diff.

**Rationale:** keeps the phase additive-only per D-06; a palette-*enforcing* gate would
need its own entry condition and calibration that was out of this phase's scope; contrast
verification is treated as a repo-integrity property, not a `report.add` code.
**Source:** 23-CONTEXT.md (D-P23-04)

---

## Lessons

### The Urban Institute license was GPL-3.0, not Apache-2.0 — and only half the vendored hexes are Urban's own
The phase's binding upstream research (Scope §3.3) assumed Apache-2.0 for the Urban
Institute source and carried that as a load-bearing fact through discuss and plan. An
at-locator re-read (HQ-33) found Urban's own README states "Code released under the GNU
General Public License v3.0"; the Apache-2.0 reading traced to GitHub's license detector
picking up an unmodified Jekyll-theme LICENSE file whose copyright line names an unrelated
party ("Iron Summit Media Strategies, LLC"). Of the six vendored hexes in `dsx-urban`'s
cycle, the phase's own correction note (filed same-day as HQ-33) identified only 2
(`1696d2`, `ec008b`) as genuinely Urban's own published palette and 3 (`1b7837`, `b35806`,
`762a83`) as ColorBrewer's PRGn/PuOr diverging-palette stops, originally mislabeled as
"Urban shade equivalents"; a later refinement reclassified the 6th hex (`5c5859`) as
Urban's own gray-ramp stock value, settling the final split at 3 Urban / 3 ColorBrewer.

**Context:** All six colors were kept unchanged — bare hex values are not independently
copyrightable in most jurisdictions regardless of license terms — but the header's factual
claims were corrected. Automated GitHub license-detector badges are not a substitute for
reading a repo's own human-written licensing statement when the fact is load-bearing.
**Source:** 23-CONTEXT.md (CORRECTION note, HQ-33); 23-01-SUMMARY.md (six-point checklist item 2)

---

### `metadata={'Date': None}` is required — `metadata=None` alone does not suppress the timestamp
matplotlib's `_write_metadata` only auto-stamps a `<dc:date>` creation timestamp when the
`'Date'` key is entirely **absent** from the metadata dict passed to `savefig`. The helper
therefore has to own the merge `{'Date': None, **(metadata or {})}` itself, so a caller
passing `metadata=None` (or omitting the argument) cannot accidentally re-introduce the
per-render timestamp that would break hash reproducibility.

**Context:** Surfaced during research into matplotlib's savefig internals ahead of
planning and encoded as a mandatory helper behavior ("Pitfall 2") rather than left to
caller discipline.
**Source:** 23-02-PLAN.md (key_links, Pitfall 2)

---

### matplotlib's SVG element IDs are seeded by a per-process random salt unless `svg.hashsalt` is pinned
matplotlib's default `svg.hashsalt` is `None`, which seeds SVG element `id`/clip-path
generation from a per-process random value in `RendererSVG._make_id` — meaning the *same*
figure rendered twice in different processes produces different byte content even with
everything else held constant. A fixed salt makes those ids a pure function of content.

**Context:** The least obvious of the recipe's non-determinism sources — not a font or
timestamp issue but an internal SVG-backend ID-generation mechanism specific to
matplotlib.
**Source:** 23-CONTEXT.md (GA-3); 23-REVIEW.md (Risk 3)

---

### Off-the-shelf dataviz palettes commonly fail WCAG-AA out of the box
Both the FiveThirtyEight cycle and the Urban Institute's own lighter categorical hues fell
below the 3:1 series-vs-facecolor contrast threshold as originally published. Shipping
WCAG-AA-verified palettes required darkening specific hues to the nearest AA-passing shade
the same source publishes (or dropping the hue), not just relabeling the existing cycle.

**Context:** Learned empirically while authoring the four style files against the WCAG
test oracle written RED-first in Task 1; each adjustment is documented in the file's own
`# Palette:` header line so the provenance stays honest rather than silently altered.
**Source:** 23-01-PLAN.md (Task 3 action); 23-01-SUMMARY.md

---

### Reimplement-from-doctrine makes the exact source license non-load-bearing for shipping safety
For `dsx-econ` and `dsx-bbc`, a "reimplemented from doctrine, nothing copied" posture is
safe under **any** license the source carries — the exact license fact only affects the
accuracy of the header's wording ("cite, never embed/copy"), not whether the asset can be
shipped safely. This reframes where real legal risk concentrates: only the three genuinely
vendored assets (the mpl fork, the Urban hexes, the Lato font) needed at-locator license
confirmation before shipping.

**Context:** This is precisely what let the Urban Institute license correction be absorbed
as a same-day documentation fix rather than a shipping blocker — the vendored hexes
themselves were unaffected because bare hex values aren't independently copyrightable.
**Source:** 23-CONTEXT.md (GA-1, "Robustness note")

---

## Patterns

### Off-gate-path double-render hash-equality oracle
To prove a rendering recipe is byte-deterministic without adding a gate dependency, render
the same figure twice through the real production write path into a temp directory, then
assert the two output hashes are equal using the **same** hasher the real gate/seal command
uses (never a second, hand-rolled one). Guard the test with `@unittest.skipIf` on the
optional dependency's absence and keep it entirely off any `GATE_PROFILES` path (no
`report.add`).

**When to use:** Whenever a tool must prove reproducibility of a heavy analyst-side
dependency (matplotlib here) without pulling that dependency onto a hermetic/CI-critical
gate path.
**Source:** 23-CONTEXT.md (GA-3); 23-02-PLAN.md; 23-REVIEW.md (Risk 3)

---

### Machine-testable per-file license/attribution header block
Each vendored/derived asset opens with a fixed-shape comment header (`Source:` with URL,
`License:`, `Vendoring:`, `Font:`, plus a fixed disclaimer phrase for reimplemented-not-
vendored assets) that a stdlib text-parsing test asserts line-by-line, with a non-vacuity
anchor (`assertEqual(checked, N)`) so a missing or renamed file cannot pass silently.

**When to use:** Any phase vendoring or deriving from externally-licensed material, where
the license-audit gate needs machine-checkable evidence rather than a one-time manual read.
**Source:** 23-01-PLAN.md (Task 1); 23-REVIEW.md (Risk 2)

---

### Single-hasher discipline (writer/hasher separation)
Split "write the deterministic artifact" from "compute its seal hash" into two different
owners, and never let the writer also hash — even when returning the hash inline would be
convenient. Enforce it by grepping the writer's source for the hashing library/import and
asserting it appears only in docstring prose, never as a real import or call.

**When to use:** Any pipeline where a single canonical hasher already exists (here, `dsx
seal`/`hashlib`) and a new component could tempt a second, potentially-diverging hash
computation.
**Source:** 23-CONTEXT.md (GA-2); 23-02-SUMMARY.md ("Single-hasher rule — verified")

---

### Vendored-OFL-font-as-universal-stand-in
When multiple style variants reference different proprietary fonts that cannot be
vendored, register exactly one openly-licensed font family and have every variant's
`font.family` resolve to it, with a header note stating it stands in for the proprietary
face. Avoids vendoring N proprietary fonts by vendoring one open one and being honest
about the substitution.

**When to use:** Building a multi-brand style/theme system where some source brands carry
proprietary typefaces that cannot legally be shipped.
**Source:** 23-CONTEXT.md (GA-1, "Font strategy")

---

### Live-constant-derived forbidden-pattern test (anti-drift threshold guard)
When a document must reference a gate's numeric threshold without restating it (to avoid a
second source of truth that can silently drift), write the "don't restate" test by
importing the actual constant from the code and building the forbidden regex from that
live value at runtime — never transcribing the number as a literal in the test itself. If
the code's threshold changes later, the guard's forbidden pattern changes with it
automatically.

**When to use:** Any documentation/snippet catalog that must cite governing thresholds by
name/code rather than by value, where docs-vs-code drift is a real risk.
**Source:** 23-03-PLAN.md (Task 1); 23-REVIEW.md (Risk 2)

---

## Surprises

### A GitHub license-detector misattribution went undetected through research, discuss, and plan
The Apache-2.0 assumption for the Urban Institute source was carried as a "binding input"
from the 2026-08-29 research round through discuss (S3-1) and plan-review (S3-2) without
being challenged, even though it was flagged as an at-locator confirmation still owed.

**Impact:** The load-bearing license claim for the house-default style's palette was wrong
from the initial research pass all the way through plan-review; it was caught only at the
human at-locator confirmation step (HQ-33), not by any automated gate — a reminder that a
GitHub license badge/detector reading is not a substitute for reading the repo's own
licensing statement when the fact is load-bearing.
**Source:** 23-CONTEXT.md (CORRECTION note, HQ-33); 23-01-SUMMARY.md

---

### The plan's own header-test spec and its per-file authoring prose disagreed
23-01-PLAN.md's Task 1 test-writing instructions require a `Source:` line carrying a URL
for **all four** style files, but the same plan's Task 3 per-file content guidance gave
`dsx-econ`/`dsx-bbc` source lines with no URL specified.

**Impact:** Caught during execution as a "loud execution decision" — the executor treated
the test (the REQ-P23-01 oracle) as authoritative and gave all four files real
public-provenance URLs (cite-only doctrine URLs for econ/bbc), rather than softening the
test to match the under-specified prose. When a plan's prose and its own test disagree, the
test — not the prose — should win.
**Source:** 23-01-SUMMARY.md ("Loud execution decision")

---

### A "ran, not skipped" determinism-test claim briefly looked false during sign-off
23-SECURITY.md recorded the off-gate-path double-render determinism test as having run
(not skipped) under matplotlib 3.11.1. During the independent HQ-34 sign-off
re-verification, a first re-run showed the test **skipped** — which looked like either a
regression or a false original claim.

**Impact:** Traced to an interpreter-resolution artifact in the verifying shell (a bare
Python stub with no packages on `PATH` ahead of the real interpreter), not a defect in the
test or the recipe; re-running against the correct interpreter reproduced "ran, passed,"
and the original claim held. `skipIf`-guarded tests can silently mask an environment/PATH
problem as a legitimate skip, so an unexpected skip during a re-verification pass should
prompt checking *which* interpreter ran before trusting the skip.
**Source:** 23-SECURITY.md (Approval / human sign-off note, HQ-34)

---

### A style file's "forked verbatim" claim and its palette edit looked contradictory at first read
Code review flagged, as an observation rather than a defect, that `dsx-538`'s header reads
"forked verbatim" from matplotlib's `fivethirtyeight` style while the same file also
documents a WCAG-AA-driven palette adjustment — an apparent tension between "verbatim" and
"adjusted."

**Impact:** No fix was needed: the header's explicit `# Changes:` line reconciles the two
(structural keys kept verbatim, an audited palette change), which is exactly what the
Matplotlib License §3 requires when forking — but a reviewer had to specifically check that
this was honest provenance rather than a silent contradiction.
**Source:** 23-REVIEW.md (OBS-3)
