"""Release-version agreement (v2.6.1).

`dsx --version`, the capability manifest and every example spec's
`reproducibility.repro_lock.dsx_version` must name the same release. The gate
compares a spec's declared lock version to the running package
(`dsx/checks/repro.py`, DSX-REP-053 MEDIUM on mismatch) and every decision record
carries `dsx_version` as provenance -- so a release that bumps one place and not
the others either makes the good corpus noisy or, as happened from v2.0.0 to
v2.6.0, leaves every trail claiming the wrong version. Cutting a release means
changing `dsx/__init__.py`, `capabilities/dsx/capability.json`, the 46 example
specs and `templates/ANALYSIS-SPEC.yaml` together; this module is what makes
forgetting one of them a failing test instead of a silent drift.
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dsx import __version__  # noqa: E402

_SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
# Text-level, not a YAML load: this is exactly the line a release bump edits, and
# the template carries the key inside an otherwise partly-commented block.
_DECLARED = re.compile(r'^\s*dsx_version:\s*"([^"]+)"', re.MULTILINE)


class TestReleaseVersionAgreement(unittest.TestCase):
    def test_package_version_is_semver(self):
        self.assertRegex(__version__, _SEMVER)

    def test_capability_manifest_names_the_package_version(self):
        manifest = json.loads((ROOT / "capabilities" / "dsx" / "capability.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], __version__)

    def test_every_example_spec_and_the_template_declare_the_package_version(self):
        paths = sorted((ROOT / "examples").rglob("*.yaml")) + [ROOT / "templates" / "ANALYSIS-SPEC.yaml"]
        declaring = 0
        for path in paths:
            for declared in _DECLARED.findall(path.read_text(encoding="utf-8")):
                declaring += 1
                with self.subTest(path=str(path.relative_to(ROOT))):
                    self.assertEqual(declared, __version__)
        # Anti-vacuity: the corpus declares the lock version in dozens of specs.
        self.assertGreaterEqual(declaring, 40, declaring)


if __name__ == "__main__":
    unittest.main()
