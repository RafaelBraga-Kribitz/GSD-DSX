"""Nyquist validation for Phase 13 (task-playbooks-that-fill-the-spec).

Phase 13 is skill-only: the playbooks are prose guidance, so these tests assert
the *structural* invariants each requirement promises — file existence,
registration, route-and-cite discipline (no self-stated statistical thresholds),
and the presence of the required shapes/citations — rather than runtime
behaviour. They crystallise the greps and hand-checks S1-4 ran into a standing
regression guard.

Coverage map (see 13-VALIDATION.md):
  REQ-P13-01  four router skills exist + registered + cite only real codes
  REQ-P13-02  dsx-explore-data hypothesis register routes to existing carriers
  REQ-P13-03  dsx-narrate uses the What / So What / Now What shape
  REQ-P13-04  dsx-scope-analysis tier routing (advisory, matches docs/gsd-tiers.md)
  REQ-P13-05  executor fragment prefers a scripts/*.py entrypoint
  REQ-P13-06  covered separately by tests/test_finding_catalogue_invariant.py

CRLF-safe: files are read as text and iterated with str.splitlines().
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ROUTER_SKILLS = ["dsx-cohort", "dsx-funnel", "dsx-root-cause", "dsx-segment"]

# Every Phase-13 file that cites finding codes in prose. Pins S1-4's 21/21 check.
CITING_FILES = [
    "skills/dsx-cohort/SKILL.md",
    "skills/dsx-funnel/SKILL.md",
    "skills/dsx-root-cause/SKILL.md",
    "skills/dsx-segment/SKILL.md",
    "skills/dsx-explore-data/SKILL.md",
    "skills/dsx-narrate/SKILL.md",
    "capabilities/dsx/fragments/executor.md",
]

CODE_RE = re.compile(r"DSX-[A-Z]{2,6}-\d{2,3}")

# Mirror of the plans' anti-parallel-advice grep (13-01/02/04): a statistical
# threshold or correction-method name stated by the playbook itself.
PARALLEL_ADVICE_RE = re.compile(
    r"(p ?[<>=]|\balpha\b|α|[0-9]+ ?%|[<>]=? ?0?\.[0-9]"
    r"|\bbonferroni\b|\bholm\b|\bbenjamini\b|\bfdr\b|\bsidak\b)",
    re.IGNORECASE,
)


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


class TestPhase13Playbooks(unittest.TestCase):
    def test_req01_four_router_skills_exist_and_registered(self):
        for name in ROUTER_SKILLS:
            self.assertTrue(
                (ROOT / "skills" / name / "SKILL.md").is_file(),
                f"{name}/SKILL.md is missing",
            )
        cap = json.loads(read("capabilities/dsx/capability.json"))
        registered = {
            (s.get("name") if isinstance(s, dict) else s) for s in cap.get("skills", [])
        }
        for name in ROUTER_SKILLS:
            self.assertIn(
                name, registered, f"{name} is not registered in capability.json"
            )

    def test_req01_cited_codes_all_exist_in_catalogue(self):
        catalogue = set(CODE_RE.findall(read("references/finding-codes.md")))
        for rel in CITING_FILES:
            cited = set(CODE_RE.findall(read(rel)))
            dangling = sorted(cited - catalogue)
            self.assertEqual(
                dangling, [], f"{rel} cites codes absent from the catalogue: {dangling}"
            )

    def test_req02_router_skills_route_and_cite_no_parallel_advice(self):
        # D-02: a playbook may name a gate + code and route to it, but may not
        # state a statistical threshold/correction of its own. dsx-scope-analysis
        # is excluded (13-04: it carries a legitimate `dsx power --alpha 0.05`
        # tool-command example unrelated to any check rule).
        for name in ROUTER_SKILLS:
            offenders = [
                ln
                for ln in read(f"skills/{name}/SKILL.md").splitlines()
                if PARALLEL_ADVICE_RE.search(ln) and "DSX-" not in ln
            ]
            self.assertEqual(
                offenders, [], f"{name} states unattributed advice: {offenders}"
            )

    def test_req02_explore_data_hypothesis_register(self):
        text = read("skills/dsx-explore-data/SKILL.md")
        self.assertIn("Hypothesis register", text)
        self.assertIn("assumptions[]", text)
        self.assertIn("design.multiplicity.family", text)
        for code in ("DSX-COH-030", "DSX-COH-031"):
            self.assertIn(code, text)

    def test_req03_narrate_what_so_what_now_what(self):
        text = read("skills/dsx-narrate/SKILL.md")
        self.assertIn("What / So What / Now What", text)
        for code in ("DSX-COH-040", "DSX-CLM-080"):
            self.assertIn(code, text)

    def test_req04_scope_tier_routing_matches_doc(self):
        text = read("skills/dsx-scope-analysis/SKILL.md")
        for token in ("Tier 0", "Tier 1", "Tier 2", "lookup", "ad-hoc", "full pipeline"):
            self.assertIn(token, text)
        self.assertIn("gsd-tier.ps1", text)  # emits the advisory helper
        self.assertIn("gsd-tiers.md", text)  # cites the authority doc
        self.assertTrue((ROOT / "docs" / "gsd-tiers.md").is_file())
        self.assertTrue((ROOT / "scripts" / "gsd-tier.ps1").is_file())

    def test_req04_scope_routing_is_advisory_not_mutating(self):
        # D-05: the skill EMITS the helper for the operator to run; it must not
        # itself invoke a configuration-set command.
        text = read("skills/dsx-scope-analysis/SKILL.md")
        for forbidden in ("config set", "config-set", "--set "):
            self.assertNotIn(forbidden, text)

    def test_req05_executor_prefers_py_entrypoint(self):
        text = read("capabilities/dsx/fragments/executor.md")
        self.assertIn("scripts/*.py", text)
        self.assertIn("reproducibility.entrypoint", text)
        self.assertIn("DSX-REP-040", text)


if __name__ == "__main__":
    unittest.main()
