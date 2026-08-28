"""Test suite for ``references/families.yaml`` — the frequentist estimator
ontology ``dsx/frame/admissibility.py`` (a later plan) reads. This module pins
the data file's schema mechanically, ahead of any code being written against
it (REQ-P11-01, D-06 through D-11, D-13).

Four concerns, four classes, so a failure names itself:

- ``TestFamiliesYamlParsesOnBothLoaderPaths`` — D-08's dual-parser hazard.
- ``TestFamiliesYamlSchema`` — per-entry shape, citations, honesty, aliases.
- ``TestFamiliesYamlRankingRules`` — the four cited pairwise orderings.
- ``TestFamiliesYamlTraceability`` — every family and every committed spec
  resolves.

Every load in this module goes through ``dsx.loader.load()`` — the only
parser REQ-P11-01 permits. No second parser is written here, and PyYAML's
``safe_load`` is never called directly.

Run:  python3 -m unittest tests.test_families_yaml -v
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dsx import loader  # noqa: E402
from dsx.spec import DEPENDENCE_STRUCTURES, ESTIMAND_TYPES, normalize  # noqa: E402

FAMILIES_PATH = ROOT / "references" / "families.yaml"

# Source of the literal 14 below: .planning/REQUIREMENTS.md REQ-P11-01, as
# amended by plan 11-01 (D-02) from the original "25-35" to the real,
# fixture-traced count this phase ships. If that requirement text changes,
# this literal must change with it.
EXPECTED_FAMILY_COUNT = 14

_FAMILY_KEYS = {
    "id",
    "estimand",
    "family",
    "inference_method",
    "dependence",
    "aliases",
    "buys",
    "charges",
    "traceability",
    "citation",
    "locator_status",
    "notes",
}

_VOCAB_KEYS = {"token", "citation", "locator_status", "notes"}

_RULE_KEYS = {
    "id",
    "prefers",
    "over",
    "condition",
    "strength",
    "citation",
    "locator_status",
    "notes",
}

_VALID_LOCATOR_STATUS = {"verified", "unverified"}
_VALID_STRENGTHS = {"uniform_domination", "reliability_hedged", "default_preference"}
_VALID_OPERATING_CONTEXTS = {
    "clustered_dependence",
    "sequential_monitoring",
    "ratio_metrics",
}


def _nonblank(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _candidate_families(families: list, estimand: str, dependence: str) -> list:
    return [f for f in families if f.get("estimand") == estimand and f.get("dependence") == dependence]


def _resolve_alias(procedure: str, candidates: list) -> list:
    target = normalize(procedure)
    return [f for f in candidates if any(normalize(a) == target for a in f.get("aliases", []))]


class TestFamiliesYamlParsesOnBothLoaderPaths(unittest.TestCase):
    """D-08: the same bytes must parse identically whether or not PyYAML is
    importable — a citation is not allowed to carry two different values
    depending on the operator's environment."""

    def test_both_loader_paths_produce_equal_output(self):
        if loader._pyyaml is None:
            self.skipTest(
                "dsx.loader._pyyaml is already None in this environment — both "
                "loader paths are the same path here, so a dual-parser "
                "comparison would pass vacuously rather than proving anything "
                "(D-08's exact named failure mode)."
            )
        via_pyyaml = loader.load(FAMILIES_PATH)
        original = loader._pyyaml
        try:
            loader._pyyaml = None
            via_bundled = loader.load(FAMILIES_PATH)
        finally:
            loader._pyyaml = original
        self.assertEqual(via_pyyaml, via_bundled, "the two loader paths disagree on the committed file")

    def test_top_level_has_exactly_the_four_expected_keys(self):
        data = loader.load(FAMILIES_PATH)
        self.assertEqual(
            set(data.keys()),
            {"vocabulary_is_not_exhaustive", "assumption_vocabulary", "families", "ranking_rules"},
        )

    def test_vocabulary_is_not_exhaustive_is_boolean_true(self):
        data = loader.load(FAMILIES_PATH)
        self.assertIs(data["vocabulary_is_not_exhaustive"], True)


class TestFamiliesYamlSchema(unittest.TestCase):
    def setUp(self) -> None:
        self.data = loader.load(FAMILIES_PATH)
        self.families = self.data["families"]
        self.vocab = self.data["assumption_vocabulary"]

    # ── families: ────────────────────────────────────────────────────────

    def test_exactly_14_families(self):
        self.assertEqual(len(self.families), EXPECTED_FAMILY_COUNT, self.families)

    def test_every_family_has_exactly_the_expected_keys(self):
        for entry in self.families:
            self.assertEqual(set(entry.keys()), _FAMILY_KEYS, entry.get("id"))

    def test_every_family_id_is_unique(self):
        ids = [entry["id"] for entry in self.families]
        self.assertEqual(len(ids), len(set(ids)), ids)

    def test_every_estimand_is_a_member_of_estimand_types(self):
        for entry in self.families:
            self.assertIn(entry["estimand"], ESTIMAND_TYPES, entry["id"])

    def test_every_dependence_is_a_member_of_dependence_structures(self):
        for entry in self.families:
            self.assertIn(entry["dependence"], DEPENDENCE_STRUCTURES, entry["id"])

    def test_every_inference_method_is_exactly_frequentist(self):
        for entry in self.families:
            self.assertEqual(entry["inference_method"], "frequentist", entry["id"])

    def test_every_family_citation_is_nonblank(self):
        for entry in self.families:
            self.assertTrue(_nonblank(entry["citation"]), entry["id"])

    def test_every_family_locator_status_is_valid_and_notes_present_when_unverified(self):
        for entry in self.families:
            self.assertIn(entry["locator_status"], _VALID_LOCATOR_STATUS, entry["id"])
            if entry["locator_status"] == "unverified":
                self.assertTrue(_nonblank(entry["notes"]), f"{entry['id']} unverified with blank notes")

    def test_every_family_notes_is_nonblank_verified_or_not(self):
        for entry in self.families:
            self.assertTrue(_nonblank(entry["notes"]), entry["id"])

    def test_no_alias_collision_within_an_estimand_dependence_pair(self):
        groups: dict[tuple, set] = {}
        for entry in self.families:
            key = (entry["estimand"], entry["dependence"])
            seen = groups.setdefault(key, set())
            for alias in entry["aliases"]:
                normalized = normalize(alias)
                self.assertNotIn(
                    normalized,
                    seen,
                    f"alias {alias!r} collides within pair {key} at family {entry['id']}",
                )
                seen.add(normalized)

    def test_every_alias_is_nonblank_and_equals_its_own_normalize_output(self):
        for entry in self.families:
            for alias in entry["aliases"]:
                self.assertTrue(_nonblank(alias), entry["id"])
                self.assertEqual(alias, normalize(alias), f"{entry['id']}: alias {alias!r} needs normalizing")

    def test_every_buys_and_charges_token_exists_in_assumption_vocabulary(self):
        tokens = {v["token"] for v in self.vocab}
        for entry in self.families:
            for token in list(entry["buys"]) + list(entry["charges"]):
                self.assertIn(token, tokens, f"{entry['id']} references unknown token {token!r}")

    # ── assumption_vocabulary: ──────────────────────────────────────────

    def test_every_vocabulary_entry_has_exactly_the_expected_keys(self):
        for entry in self.vocab:
            self.assertEqual(set(entry.keys()), _VOCAB_KEYS, entry.get("token"))

    def test_every_vocabulary_citation_is_nonblank(self):
        for entry in self.vocab:
            self.assertTrue(_nonblank(entry["citation"]), entry["token"])

    def test_every_vocabulary_locator_status_is_valid(self):
        for entry in self.vocab:
            self.assertIn(entry["locator_status"], _VALID_LOCATOR_STATUS, entry["token"])

    def test_vocabulary_holds_between_16_and_19_entries_with_unique_tokens(self):
        self.assertGreaterEqual(len(self.vocab), 16, self.vocab)
        self.assertLessEqual(len(self.vocab), 19, self.vocab)
        tokens = [entry["token"] for entry in self.vocab]
        self.assertEqual(len(tokens), len(set(tokens)), tokens)

    # ── raw text constraints (D-06/D-08) ────────────────────────────────
    # This repository checks out CRLF on Windows (project CLAUDE.md), so any
    # line-anchored pattern here uses \r?\n rather than a bare \n.

    def test_raw_text_has_no_document_marker_no_anchor_no_merge_key(self):
        text = FAMILIES_PATH.read_text(encoding="utf-8")
        lines = re.split(r"\r?\n", text)
        self.assertFalse(any(line.strip() == "---" for line in lines), "found a '---' document marker")
        self.assertNotIn("<<:", text, "found a merge key")
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            self.assertNotIn(" &", line, f"possible anchor on: {line!r}")

    def test_raw_text_has_no_trailing_block_scalar_introducer(self):
        text = FAMILIES_PATH.read_text(encoding="utf-8")
        lines = re.split(r"\r?\n", text)
        for line in lines:
            rstripped = line.rstrip()
            self.assertFalse(rstripped.endswith("|"), f"block scalar '|' introducer on: {line!r}")
            self.assertFalse(
                rstripped.endswith(">") and not rstripped.endswith('"'),
                f"block scalar '>' introducer on: {line!r}",
            )


class TestFamiliesYamlRankingRules(unittest.TestCase):
    def setUp(self) -> None:
        self.data = loader.load(FAMILIES_PATH)
        self.families = self.data["families"]
        self.rules = self.data["ranking_rules"]
        self.by_id = {entry["id"]: entry for entry in self.families}

    def test_exactly_4_ranking_rules(self):
        self.assertEqual(len(self.rules), 4, self.rules)

    def test_every_rule_has_exactly_the_expected_keys(self):
        for rule in self.rules:
            self.assertEqual(set(rule.keys()), _RULE_KEYS, rule.get("id"))

    def test_every_rule_prefers_and_over_are_existing_different_same_pair_families(self):
        for rule in self.rules:
            self.assertIn(rule["prefers"], self.by_id, f"{rule['id']}: prefers {rule['prefers']!r} unknown")
            self.assertIn(rule["over"], self.by_id, f"{rule['id']}: over {rule['over']!r} unknown")
            self.assertNotEqual(rule["prefers"], rule["over"], rule["id"])
            prefers_entry = self.by_id[rule["prefers"]]
            over_entry = self.by_id[rule["over"]]
            self.assertEqual(
                (prefers_entry["estimand"], prefers_entry["dependence"]),
                (over_entry["estimand"], over_entry["dependence"]),
                f"{rule['id']}: prefers/over do not share an (estimand, dependence) pair",
            )

    def test_every_rule_strength_is_valid(self):
        for rule in self.rules:
            self.assertIn(rule["strength"], _VALID_STRENGTHS, rule["id"])

    def test_every_rule_citation_nonblank_and_locator_status_valid(self):
        for rule in self.rules:
            self.assertTrue(_nonblank(rule["citation"]), rule["id"])
            self.assertIn(rule["locator_status"], _VALID_LOCATOR_STATUS, rule["id"])
            if rule["locator_status"] == "unverified":
                self.assertTrue(_nonblank(rule["notes"]), rule["id"])


class TestFamiliesYamlTraceability(unittest.TestCase):
    def setUp(self) -> None:
        self.data = loader.load(FAMILIES_PATH)
        self.families = self.data["families"]
        self.ranking_rule_ids = {rule["id"] for rule in self.data["ranking_rules"]}

    def test_every_family_traceability_resolves(self):
        for entry in self.families:
            value = entry["traceability"]
            self.assertTrue(_nonblank(value), entry["id"])
            if value.startswith("spec:"):
                spec_path = ROOT / value[len("spec:") :]
                self.assertTrue(spec_path.exists(), f"{entry['id']}: {value} does not exist on disk")
            elif value.startswith("ranking_rule:"):
                rule_id = value[len("ranking_rule:") :]
                self.assertIn(rule_id, self.ranking_rule_ids, f"{entry['id']}: unknown ranking_rule {rule_id!r}")
            elif value.startswith("operating_context:"):
                cluster = value[len("operating_context:") :]
                self.assertIn(
                    cluster,
                    _VALID_OPERATING_CONTEXTS,
                    f"{entry['id']}: unknown operating_context {cluster!r}",
                )
            else:
                self.fail(f"{entry['id']}: traceability {value!r} matches none of the three permitted forms")

    def test_every_committed_frequentist_spec_resolves_its_declared_procedure(self):
        # Glob rather than hardcode, per this plan's action text — a globbing
        # mistake must fail loudly (the >=6 assertion below) rather than
        # silently passing over an empty set.
        spec_paths = sorted(ROOT.glob("examples/*-ANALYSIS-SPEC.yaml"))
        spec_paths += sorted(ROOT.glob("examples/known-bad/*-ANALYSIS-SPEC.yaml"))
        spec_paths.append(ROOT / "templates" / "ANALYSIS-SPEC.yaml")

        checked = 0
        for path in spec_paths:
            spec = loader.load(path)

            inference = spec.get("inference", {}) if isinstance(spec, dict) else {}
            paradigm = inference.get("paradigm") if isinstance(inference, dict) else None
            if isinstance(paradigm, str) and normalize(paradigm) == "bayesian":
                continue  # D-22: out of this family's scope

            validity_frame = spec.get("validity_frame", {}) if isinstance(spec, dict) else {}
            estimand_block = validity_frame.get("estimand", {}) if isinstance(validity_frame, dict) else {}
            dependence_block = validity_frame.get("dependence", {}) if isinstance(validity_frame, dict) else {}
            estimand_type = estimand_block.get("type") if isinstance(estimand_block, dict) else None
            dependence_structure = (
                dependence_block.get("structure") if isinstance(dependence_block, dict) else None
            )
            primary_procedure = inference.get("primary_procedure") if isinstance(inference, dict) else None

            if not (_nonblank(estimand_type) and _nonblank(dependence_structure) and _nonblank(primary_procedure)):
                continue  # missing one of the three required fields — skip, not a failure

            checked += 1
            candidates = _candidate_families(self.families, estimand_type, dependence_structure)
            matches = _resolve_alias(primary_procedure, candidates)
            self.assertEqual(
                len(matches),
                1,
                f"{path.name}: declared procedure {primary_procedure!r} under "
                f"({estimand_type!r}, {dependence_structure!r}) resolved to {matches!r}, expected exactly one",
            )

        self.assertGreaterEqual(
            checked,
            6,
            f"only {checked} specs were checked — a globbing mistake would silently pass over an empty set",
        )


if __name__ == "__main__":
    unittest.main()
