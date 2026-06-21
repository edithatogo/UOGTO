import os
import sys
import unittest
from pathlib import Path


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.maintenance import check_release_readiness
from scripts.maintenance import package_release_assets


class TestReleaseReadiness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dist = Path("dist")
        dist.mkdir(exist_ok=True)
        for asset in package_release_assets.REQUIRED_RELEASE_ASSETS:
            path = dist / asset
            if not path.exists():
                path.write_text(f"test fixture for {asset}\n", encoding="utf-8")
        package_release_assets.write_release_manifest(dist, "1.0.0")

    def test_local_release_readiness_passes(self):
        check_release_readiness.check_local_release_readiness()

    def test_manifest_checks_release_assets(self):
        check_release_readiness.check_release_manifest()

    def test_release_workflow_contains_required_gates(self):
        check_release_readiness.check_release_workflow()

    def test_release_notes_contain_preflight_evidence(self):
        check_release_readiness.check_release_notes()

    def test_registry_packets_track_external_placeholders(self):
        check_release_readiness.check_registry_packets()

    def test_published_mode_rejects_pending_external_markers(self):
        with self.assertRaises(AssertionError):
            check_release_readiness.check_registry_packets(require_published=True)


if __name__ == "__main__":
    unittest.main()
