import os
import sys
import unittest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.maintenance import check_release_readiness


class TestReleaseReadiness(unittest.TestCase):
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
