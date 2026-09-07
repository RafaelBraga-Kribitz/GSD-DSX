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


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------------------- #
# Parser helpers — STUBS in the RED commit; implemented in the GREEN commit.
# Each raises NotImplementedError so the behaviour-bearing tests error until the
# key-path parser exists (the RED lever, per the 26-03 plan).
# --------------------------------------------------------------------------- #
def _lines(text: str) -> list[str]:
    """Split on ``\\r?\\n`` so both CRLF and bare-LF templates yield real lines."""
    raise NotImplementedError


def parse_eda_keys(text: str) -> set[str]:
    """Every dotted path (incl. intermediates, ``[]`` for list-of-map elements) in
    the EDA front-matter block (strictly between the first two ``---`` fences)."""
    raise NotImplementedError


def parse_profile_keys(text: str) -> set[str]:
    """Every dotted path in DATA-PROFILE.yaml AFTER uncommenting the ``#`` example
    lines, normalizing the ``columns.column_name.*`` placeholder to ``columns[].*``."""
    raise NotImplementedError


def extract_inputs_block(skill_text: str) -> str:
    """The single ``<inputs>...</inputs>`` body; raises if not exactly one."""
    raise NotImplementedError


def extract_key_region(inputs_text: str, header: str) -> list[str]:
    """The contiguous run of one-key-per-bullet keys following a region header."""
    raise NotImplementedError


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
