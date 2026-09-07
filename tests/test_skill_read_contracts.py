"""Off-gate-path repo-integrity guard (REQ-P26-02, D-26-04): the ``<inputs>`` block
each of the five downstream skills carries must name only keys that exist in the
live templates. A renamed or fabricated template key FAILS this suite instead of
silently orphaning a skill's read step.

Rationale (corrected from 26-CONTEXT.md's premise, per 26-RESEARCH.md "Correction
to CONTEXT's premise"): CONTEXT said PyYAML "won't load" these templates. That is
false — ``yaml.safe_load`` parses both cleanly. The real, stronger reason a straight
YAML parse fails is that the per-column and flag-gated keys the skills read
(``columns[].*``, ``unit.*``, ``target.*``) live behind a leading ``#`` — a YAML
*comment* — and every conformant parser (PyYAML, the stdlib, dsx/loader.py's own
bundled fallback) discards comments by design. So an uncomment pre-processing step
is mandatory regardless of parser. Independently, PyYAML is an *optional* dependency
in this repo's own pattern (dsx/loader.py wraps its PyYAML import in try/except); a
test that pulled PyYAML in unconditionally would be the repo's first hard
third-party test dependency. Therefore this module is stdlib-only (re, unittest,
pathlib) and pulls in nothing out of the dsx/ package (D-26-04): a hand-rolled,
line-oriented, indent-stack key-path extractor scoped to path extraction only — no
value parsing, no anchors, no multi-document support.

CRLF discipline: templates/EDA.md is CRLF (206 CRLF / 0 bare-LF), while
templates/DATA-PROFILE.yaml is bare-LF (0 CRLF / 72 bare-LF) — verified live, the
two templates do NOT share one line-ending convention. Every split therefore uses
the pattern ``\\r?\\n`` (never a bare ``\\n`` nor a ``\\r\\n``-only pattern), which
matches both; a ``\\r\\n``-only split would silently return zero lines for the
bare-LF profile (a vacuous pass), which the anti-vacuity anchors below are designed
to catch.

DATA-PROFILE placeholder token: the per-element key placeholder the profile template
uses today is literally ``column_name`` (templates/DATA-PROFILE.yaml line 20:
``  # column_name:``). The profile parser normalizes ``columns.column_name.*`` to
``columns[].*``. This single-token assumption is documented here (26-CONTEXT.md
residual #5) so a future second placeholder token is not missed.

Off gate path: this module is structurally outside test_gate_path_hermetic's import
closure (that walk starts only at the dsx.cli.GATE_PROFILES-resolved dsx/checks and
dsx/frame files; tests/ is never in it), so the zero-dsx-import rule is additional
safety margin, not a load-bearing requirement of that other test.

Run: python -m unittest tests.test_skill_read_contracts -v
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EDA_TEMPLATE = ROOT / "templates" / "EDA.md"
PROFILE_TEMPLATE = ROOT / "templates" / "DATA-PROFILE.yaml"

FIVE_SKILLS = (
    "dsx-scope-analysis",
    "dsx-define-metrics",
    "dsx-design-experiment",
    "dsx-build-model",
    "dsx-narrate",
)

# Region header openers (matched by stripped-line startswith; the profile header
# carries a parenthetical suffix in the skills, so we match on the stable prefix).
EDA_REGION = "EDA front-matter keys read"
PROFILE_REGION = "DATA-PROFILE keys read"

# The D-26-02 grounded per-skill mapping — the ratified matrix of keys each skill
# reads, per region. The membership tests iterate this structure and cross-check it
# against (a) the keys each skill's live <inputs> block actually names and (b) the
# live template key sets.
D26_02 = {
    "dsx-scope-analysis": {
        EDA_REGION: [
            "grain.verdict",
            "grain.implied_dependence.structure",
            "grain.implied_dependence.cluster_var",
            "missingness[]",
            "base_rate.verdict",
            "contradictions",
            "stop_triggered",
        ],
        PROFILE_REGION: [
            "primary_key_unique",
            "duplicate_rate",
            "unit.rows_per_unit",
            "unit.largest_unit_share",
            "columns[].null_rate",
            "target.verdict",
        ],
    },
    "dsx-define-metrics": {
        EDA_REGION: [
            "grain.declared",
            "grain.observed",
            "grain.verdict",
            "grain.duplicate_rate",
        ],
        PROFILE_REGION: [
            "primary_key",
            "primary_key_unique",
            "duplicate_rate",
            "columns[].n_unique",
            "columns[].dtype",
        ],
    },
    "dsx-design-experiment": {
        EDA_REGION: [
            "dependence.icc",
            "dependence.outcome_sd",
            "dependence.weekly_cycle_amplitude",
            "base_rate.overall",
            "grain.implied_dependence.structure",
            "grain.implied_dependence.cluster_var",
        ],
        PROFILE_REGION: [
            "target.overall",
            "target.weekly_range",
            "unit.rows_per_unit",
            "unit.largest_unit_share",
        ],
    },
    "dsx-build-model": {
        EDA_REGION: [
            "leakage_suspects[]",
            "grain.implied_dependence.structure",
            "grain.implied_dependence.cluster_var",
            "segments_candidates[]",
        ],
        PROFILE_REGION: [
            "columns[].n_unique",
            "columns[].dtype",
            "columns[].categorical",
            "unit.rows_per_unit",
            "time.column",
            "time.max_gap_days",
        ],
    },
    "dsx-narrate": {
        EDA_REGION: [
            "dataset",
            "base_rate.overall",
            "base_rate.metric",
            "segments_candidates[]",
            "comparisons_looked_at",
            "artifact_status",
        ],
        PROFILE_REGION: [
            "row_count",
            "time.min",
            "time.max",
            "target.overall",
        ],
    },
}

_INPUTS_RE = re.compile(r"<inputs>(.*?)</inputs>", re.DOTALL)
_BULLET_KEY_RE = re.compile(r"^\s*-\s+`([^`]+)`\s*$")
_LINE_SPLIT_RE = re.compile(r"\r?\n")
# A YAML-ish key line: leading spaces, an identifier, a colon, then the value.
_KEY_RE = re.compile(r"^(?P<indent> *)(?P<name>[A-Za-z_][A-Za-z0-9_]*):(?P<value>.*)$")
# A trailing inline ``# ...`` comment (whitespace-anchored so it never eats a key
# at column 0 — those are full-comment lines, handled separately).
_INLINE_COMMENT_RE = re.compile(r"\s+#.*$")
# The single per-element placeholder token the profile template uses today
# (26-CONTEXT.md residual #5): ``columns.column_name.*`` normalizes to ``columns[].*``.
_PROFILE_PLACEHOLDER = ".column_name"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _lines(text: str) -> list[str]:
    """Split on ``\\r?\\n`` so both CRLF (EDA.md) and bare-LF (DATA-PROFILE.yaml)
    templates yield real lines. A ``\\r\\n``-only split would silently return one
    giant line for the bare-LF profile — the vacuous-pass failure mode."""
    return _LINE_SPLIT_RE.split(text)


def _extract_paths(lines, normalize=lambda p: p) -> set[str]:
    """Indent-stack key-path extractor. Records EVERY dotted path — intermediates
    included, never leaf-only — with ``[]`` marking a list-of-map element. Full
    dotted-path recording is what keeps a parent rename from being masked by a
    same-named leaf elsewhere (leaf-only matching is rejected by D-26-04).

    ``normalize`` rewrites a freshly built path (identity for EDA; the
    ``column_name -> []`` rule for DATA-PROFILE)."""
    stack: list[tuple[int, str]] = []  # (indent, already-normalized path)
    keys: set[str] = set()
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue  # blank or full-comment line
        line = _INLINE_COMMENT_RE.sub("", line)
        content = line.strip()
        if not content:
            continue
        indent = len(line) - len(line.lstrip(" "))
        if content == "-" or content.startswith("- "):
            # A sequence item: the current parent is a list. Re-key it as ``P[]``.
            if stack:
                pind, ppath = stack[-1]
                if not ppath.endswith("[]"):
                    keys.discard(ppath)
                    listed = ppath + "[]"
                    keys.add(listed)
                    stack[-1] = (pind, listed)
            continue
        m = _KEY_RE.match(line)
        if not m:
            continue
        name = m.group("name")
        value = m.group("value").strip()
        while stack and stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1] if stack else ""
        path = normalize(f"{parent}.{name}" if parent else name)
        if value.startswith("[") and "{" in value:
            keys.add(path + "[]")          # inline list-of-maps -> ``key[]``
        else:
            keys.add(path)                 # scalar, scalar-list, map header, or parent
        # Only an empty-valued key can host block children; push it as a potential
        # parent. Scalars / scalar-lists / flow-maps are self-contained, so they must
        # NOT become parents — otherwise a fully-commented block whose header
        # uncomments to a nonzero indent (unit:, target:) would nest under the
        # preceding top-level scalar (e.g. sentinels_found) instead of the root.
        if value == "":
            stack.append((indent, path))
    return keys


def parse_eda_keys(text: str) -> set[str]:
    """Every dotted path in the EDA front-matter block — the lines strictly between
    the first two ``---`` fences — skipping ``#`` comment lines and stripping inline
    ``# ...``, splitting on ``\\r?\\n``."""
    lines = _lines(text)
    fences = [i for i, ln in enumerate(lines) if ln.strip() == "---"]
    if len(fences) < 2:
        return set()
    return _extract_paths(lines[fences[0] + 1:fences[1]])


def _normalize_profile(path: str) -> str:
    return path.replace(_PROFILE_PLACEHOLDER, "[]")


def parse_profile_keys(text: str) -> set[str]:
    """Every dotted path in DATA-PROFILE.yaml. FIRST uncomment every ``#`` example
    line (replace the first ``#`` with a single space — length-preserving, so the
    indent hierarchy survives), THEN the shared extractor strips any remaining
    trailing inline ``# ...`` and builds paths, normalizing the ``column_name``
    placeholder to ``[]``. The uncomment step is what lets the per-column /
    flag-gated example keys (``columns[].*``, ``unit.*``, ``target.*``) count as
    existing — a straight YAML parse would discard them as comments."""
    uncommented = [ln.replace("#", " ", 1) for ln in _lines(text)]
    return _extract_paths(uncommented, normalize=_normalize_profile)


def extract_inputs_block(skill_text: str) -> str:
    """The single ``<inputs>...</inputs>`` body (DOTALL, ``\\r?\\n`` tolerant);
    raises if the skill does not carry exactly one block."""
    matches = _INPUTS_RE.findall(skill_text)
    if len(matches) != 1:
        raise ValueError(f"expected exactly one <inputs> block, found {len(matches)}")
    return matches[0]


def extract_key_region(inputs_text: str, header: str) -> list[str]:
    """The contiguous run of one-key-per-bullet keys following a region ``header``.
    Each bullet must match ``^\\s*-\\s+`key`\\s*$``; the region ends at the first
    line that does not (blank line, prose, or the next header)."""
    keys: list[str] = []
    in_region = False
    for ln in _lines(inputs_text):
        if not in_region:
            if ln.strip().startswith(header):
                in_region = True
            continue
        m = _BULLET_KEY_RE.match(ln)
        if m:
            keys.append(m.group(1))
        else:
            break
    return keys


class TestSkillReadContracts(unittest.TestCase):
    # ---- REQ-P26-02: negative control (the load-bearing anti-silent-orphan proof) ----
    def test_negative_control_orphan_key_is_rejected(self):
        eda = parse_eda_keys(_read(EDA_TEMPLATE))
        prof = parse_profile_keys(_read(PROFILE_TEMPLATE))
        # Fabricated keys, fed through the SAME matcher the real checks use, are
        # NOT members — and the parser did not invent them.
        self.assertNotIn("grain.__orphan__", eda,
                         "parser invented a fabricated EDA key")
        self.assertNotIn("columns[].__orphan__", prof,
                         "parser invented a fabricated DATA-PROFILE key")
        # Same matcher genuinely accepts a real sibling of each orphan (proves the
        # non-membership above is discrimination, not a degenerate empty set).
        self.assertIn("grain.verdict", eda)
        self.assertIn("columns[].null_rate", prof)

    # ---- REQ-P26-02: anti-vacuity anchors on BOTH templates ----
    def test_anchor_non_vacuity(self):
        eda = parse_eda_keys(_read(EDA_TEMPLATE))
        self.assertGreaterEqual(len(eda), 30,
                                f"EDA key set degenerate ({len(eda)} < 30) — mis-split?")
        self.assertIn("grain.verdict", eda)
        prof = parse_profile_keys(_read(PROFILE_TEMPLATE))
        self.assertTrue(prof, "DATA-PROFILE key set is empty (vacuous parse)")
        # columns[].null_rate exists ONLY because the uncomment step recovered the
        # commented per-column example block — its membership proves that step ran.
        self.assertIn("columns[].null_rate", prof,
                      "uncomment pre-processor did not recover the commented column keys")

    # ---- REQ-P26-01: every skill carries exactly one <inputs> block, >=1 region ----
    def test_every_skill_carries_at_least_one_key_region(self):
        checked = 0
        for name in FIVE_SKILLS:
            text = _read(SKILLS / name / "SKILL.md")
            self.assertEqual(len(_INPUTS_RE.findall(text)), 1,
                             f"{name}: expected exactly one <inputs> block")
            inputs = extract_inputs_block(text)
            regions = [r for r in (EDA_REGION, PROFILE_REGION)
                       if extract_key_region(inputs, r)]
            self.assertTrue(regions, f"{name}: <inputs> block has no populated key region")
            checked += 1
        self.assertEqual(checked, 5)

    # ---- REQ-P26-02: every named key resolves against the live templates ----
    def test_skill_keys_are_members_of_live_templates(self):
        eda = parse_eda_keys(_read(EDA_TEMPLATE))
        prof = parse_profile_keys(_read(PROFILE_TEMPLATE))
        template_sets = {EDA_REGION: eda, PROFILE_REGION: prof}
        for name in FIVE_SKILLS:
            inputs = extract_inputs_block(_read(SKILLS / name / "SKILL.md"))
            for region, expected in D26_02[name].items():
                named = extract_key_region(inputs, region)
                # The skill names exactly the ratified D-26-02 matrix (drift guard).
                self.assertEqual(named, expected,
                                 f"{name} / {region}: skill keys drifted from the "
                                 f"D-26-02 matrix")
                # Each named key MUST exist in the live template key set (the guard).
                for key in named:
                    self.assertIn(
                        key, template_sets[region],
                        f"{name} / {region}: orphaned key `{key}` — was the "
                        f"template key renamed or removed?")

    # ---- REQ-P26-01: the fallback line names the recorded-absence tier ----
    def test_when_absent_names_eda_artifact_none(self):
        for name in FIVE_SKILLS:
            inputs = extract_inputs_block(_read(SKILLS / name / "SKILL.md"))
            absent = [ln for ln in _lines(inputs) if ln.strip().startswith("When absent:")]
            self.assertTrue(absent, f"{name}: no `When absent:` line in <inputs>")
            self.assertIn("eda_artifact: none", " ".join(_lines(inputs)),
                          f"{name}: fallback must record `eda_artifact: none`")

    # ---- D-26-01: Also-consult prose stays honest-but-unparsed (zero backticks) ----
    def test_also_consult_line_has_zero_backticks(self):
        seen = 0
        for name in FIVE_SKILLS:
            inputs = extract_inputs_block(_read(SKILLS / name / "SKILL.md"))
            for ln in _lines(inputs):
                if ln.strip().startswith("Also consult"):
                    self.assertNotIn("`", ln,
                                     f"{name}: `Also consult:` line must carry zero "
                                     f"backticks (prose ref, never a parsed key)")
                    seen += 1
        # define-metrics and build-model carry an Also-consult line; anti-vacuity.
        self.assertGreaterEqual(seen, 2,
                                "expected at least the two Also-consult lines "
                                "(define-metrics, build-model)")

    # ---- REQ-P26-02: parse is deterministic and set-membership is order-independent ----
    def test_parse_is_deterministic_and_order_independent(self):
        eda_text = _read(EDA_TEMPLATE)
        prof_text = _read(PROFILE_TEMPLATE)
        self.assertEqual(parse_eda_keys(eda_text), parse_eda_keys(eda_text))
        self.assertEqual(parse_profile_keys(prof_text), parse_profile_keys(prof_text))
        # Reordering bullets within a region yields the same key SET.
        a = "EDA front-matter keys read:\n- `a.x`\n- `b.y`\n"
        b = "EDA front-matter keys read:\n- `b.y`\n- `a.x`\n"
        self.assertEqual(set(extract_key_region(a, EDA_REGION)),
                         set(extract_key_region(b, EDA_REGION)))


if __name__ == "__main__":
    unittest.main()
