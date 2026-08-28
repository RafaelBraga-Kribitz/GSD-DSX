"""Nyquist validation for Phase 14 (compounding-and-data-onboarding).

Phase 14 is a doc/skill/template phase: the deliverables are prose playbooks,
markdown templates and one dated exemplar, so these tests assert the *structural*
invariants each requirement promises — file existence, the presence of the
required guarded steps, and the honesty claims of the documented-skip branch —
rather than runtime behaviour. They crystallise the greps and hand-checks S2-4
ran into a standing regression guard (S1-5 precedent: tests/test_phase13_playbooks.py).

Coverage map (see 14-VALIDATION.md):
  REQ-P14-01  dated-learnings compounding loop: dsx-scope-analysis searches
              docs/dsx/learnings/ before framing; README schema + dated exemplar exist
  REQ-P14-02  DATA-DICTIONARY.md template sits next to DATA-PROFILE.yaml, roster
              copied verbatim; dsx-explore-data authors it
  REQ-P14-03  dsx-narrate offers the AI-assistance disclosure ONLY on literal
              dsx.domain == research; non-research paths unchanged
  REQ-P14-04  CSV-first alias table routes all 13 DSX skills with no data_storage/
              folder; every DSX skill carries a Triggers: clause
  REQ-P14-05  documented-skip of the file-drop hook: operating guide names the
              DSX-DQ-001 compensating control and hooks stays []
  REQ-P14-06  zero-mint: capability.json hooks stays [] with no aliases key
              (catalogue set-identity + gate-path hermeticity live in
              tests/test_finding_catalogue_invariant.py + tests/test_gate_path_hermetic.py)

CRLF-safe: files are read as text; anchors are single-line substrings so the
line-ending convention (this repo checks out CRLF) cannot break a match.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# The 13 DSX skills (dsx-* dirs); must match capability.json's skill count.
DSX_SKILLS = sorted(p.name for p in (ROOT / "skills").glob("dsx-*") if p.is_dir())

DATED_LEARNING_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$")


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


class TestPhase14Onboarding(unittest.TestCase):
    # ---- REQ-P14-01 : compounding loop (search dated learnings before framing) ----
    def test_req01_learnings_readme_and_dated_exemplar_exist(self):
        d = ROOT / "docs" / "dsx" / "learnings"
        self.assertTrue((d / "README.md").is_file(), "learnings schema README missing")
        dated = [p.name for p in d.glob("*.md")
                 if DATED_LEARNING_RE.match(p.name)]
        self.assertTrue(dated, "no YYYY-MM-DD-<slug>.md dated exemplar present")
        # README fixes the closed key set and names the producer.
        readme = read("docs/dsx/learnings/README.md")
        self.assertIn("gsd-extract-learnings", readme,
                      "README must name gsd-extract-learnings as the producer")

    def test_req01_scope_analysis_searches_learnings_before_framing(self):
        s = read("skills/dsx-scope-analysis/SKILL.md")
        self.assertIn("Search dated learnings before framing", s)
        self.assertIn("docs/dsx/learnings/", s)
        self.assertIn("gsd-extract-learnings", s)

    # ---- REQ-P14-02 : DATA-DICTIONARY next to DATA-PROFILE.yaml ----
    def test_req02_data_dictionary_template_copies_profile(self):
        t = read("templates/DATA-DICTIONARY.md")
        self.assertIn("profile_path: DATA-PROFILE.yaml", t)
        self.assertIn("verbatim", t.lower(),
                      "template must state the roster is copied verbatim, not recomputed")
        # Column header carries the closed semantic_type vocabulary column.
        self.assertIn("semantic_type", t)
        for member in ("identifier", "foreign_key", "timestamp", "categorical",
                       "numeric_measure", "boolean", "free_text", "derived"):
            self.assertIn(member, t, f"semantic_type closed-set member {member!r} missing")

    def test_req02_explore_data_authors_dictionary(self):
        s = read("skills/dsx-explore-data/SKILL.md")
        self.assertIn("DATA-DICTIONARY.md", s)
        self.assertIn("templates/DATA-DICTIONARY.md", s)
        self.assertIn("DATA-PROFILE.yaml", s)

    # ---- REQ-P14-03 : opt-in research-domain disclosure (guarded) ----
    def test_req03_disclosure_template_exists(self):
        t = read("templates/DISCLOSURE-research.md")
        self.assertIn("## AI-assistance disclosure", t)

    def test_req03_narrate_disclosure_guarded_on_literal_research(self):
        s = read("skills/dsx-narrate/SKILL.md")
        self.assertIn("config-get dsx.domain", s,
                      "disclosure must read dsx.domain via the documented config-get")
        self.assertIn("templates/DISCLOSURE-research.md", s)
        # The guard is the literal `research` value; auto must never infer it.
        self.assertIn("dsx.domain ==", s)
        self.assertIn("research", s)
        low = s.lower()
        self.assertTrue("opt-in" in low or "skip" in low,
                        "disclosure must be opt-in / skippable, never imposed")

    # ---- REQ-P14-04 : CSV-first alias table + Triggers on every DSX skill ----
    def test_req04_operating_guide_alias_table_csv_as_argument(self):
        g = read("docs/operating-guide.md")
        self.assertIn("CSV-first aliases", g)
        # The CSV is passed as an argument, NOT dropped into a watched folder.
        self.assertIn("as an argument", g)
        # The guide DOCUMENTS the absence of a data_storage/ folder (does not create one):
        # the 14-04 Task 1 verify positively requires the "without a data_storage" phrase.
        self.assertIn("without a", g)
        self.assertIn("data_storage", g)
        # capability.json aliases key is deliberately NOT used (documented in the guide).
        self.assertIn("aliases", g)

    def test_req04_all_dsx_skills_carry_triggers(self):
        self.assertEqual(len(DSX_SKILLS), 13, f"expected 13 DSX skills, found {DSX_SKILLS}")
        missing = [name for name in DSX_SKILLS
                   if "Triggers:" not in read(f"skills/{name}/SKILL.md")]
        self.assertEqual(missing, [], f"DSX skills missing a Triggers: clause: {missing}")

    def test_req04_no_data_storage_in_skills_or_shims(self):
        # The watched-folder string must not leak into skills or the host shims.
        # The operating guide is EXEMPT (it documents the folder's ABSENCE — 14-04
        # plan guardrail note, Task 1 verify requires "without a data_storage").
        hits = []
        for name in DSX_SKILLS:
            if "data_storage" in read(f"skills/{name}/SKILL.md"):
                hits.append(f"skills/{name}/SKILL.md")
        for shim in ("dsx-scope.md", "dsx-eda.md"):
            p = ROOT / ".claude" / "commands" / shim
            if p.is_file() and "data_storage" in p.read_text(encoding="utf-8", errors="replace"):
                hits.append(f".claude/commands/{shim}")
        self.assertEqual(hits, [], f"data_storage leaked into skills/shims: {hits}")

    # ---- REQ-P14-05 : documented-skip of the file-drop hook ----
    def test_req05_documented_skip_names_dq001_and_keeps_hooks_empty(self):
        g = read("docs/operating-guide.md")
        self.assertIn("Why there is no file-drop hook", g)
        self.assertIn("DSX-DQ-001", g,
                      "the documented skip must name DSX-DQ-001 as the compensating control")
        # DSX-DQ-001 must actually exist in the catalogue (not an invented citation).
        self.assertIn("DSX-DQ-001", read("references/finding-codes.md"))

    # ---- REQ-P14-06 : zero-mint — hooks stays [], no aliases key ----
    def test_req06_capability_hooks_empty_no_aliases_key(self):
        cap = json.loads(read("capabilities/dsx/capability.json"))
        self.assertEqual(cap.get("hooks"), [], "capability.json hooks must stay []")
        self.assertNotIn("aliases", cap,
                         "no capability.json aliases key (unverified schema — would no-op)")
        self.assertEqual(cap.get("runtimeCompat", {}).get("supported"), ["*"],
                         "runtimeCompat.supported must stay ['*'] (the portable contract)")


if __name__ == "__main__":
    unittest.main()
