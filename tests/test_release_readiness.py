import os
import sys
import unittest
from pathlib import Path


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.maintenance import check_release_readiness
from scripts.maintenance import build_registry_handoff
from scripts.maintenance import build_extended_registry_handoff
from scripts.maintenance import build_zenodo_handoff
from scripts.maintenance import build_w3id_redirect_handoff
from scripts.maintenance import build_publication_status
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
        build_registry_handoff.write_handoff(
            dist / "registry-handoff.json",
            build_registry_handoff.build_registry_handoff(),
        )
        build_extended_registry_handoff.write_handoff(
            dist / "extended-registry-handoff.json",
            build_extended_registry_handoff.build_extended_registry_handoff(),
        )
        build_zenodo_handoff.write_handoff(
            dist / "zenodo-handoff.json",
            build_zenodo_handoff.build_zenodo_handoff(),
        )
        build_w3id_redirect_handoff.write_handoff(
            dist / "w3id-redirect-handoff.json",
            build_w3id_redirect_handoff.build_w3id_handoff(),
        )
        build_publication_status.write_status(
            dist / "publication-status.json",
            build_publication_status.build_publication_status(),
        )

    def test_local_release_readiness_passes(self):
        check_release_readiness.check_local_release_readiness()

    def test_manifest_checks_release_assets(self):
        check_release_readiness.check_release_manifest()

    def test_release_workflow_contains_required_gates(self):
        check_release_readiness.check_release_workflow()

    def test_release_preflight_requires_registry_handoff(self):
        missing = Path(".tmp") / "missing-registry-handoff.json"
        with self.assertRaises(AssertionError):
            check_release_readiness.check_registry_handoff_packet(missing)

    def test_release_preflight_requires_extended_registry_handoff(self):
        missing = Path(".tmp") / "missing-extended-registry-handoff.json"
        with self.assertRaises(AssertionError):
            check_release_readiness.check_extended_registry_handoff_packet(missing)

    def test_release_preflight_requires_w3id_handoff(self):
        missing = Path(".tmp") / "missing-w3id-redirect-handoff.json"
        with self.assertRaises(AssertionError):
            check_release_readiness.check_w3id_handoff_packet(missing)

    def test_release_preflight_requires_zenodo_handoff(self):
        missing = Path(".tmp") / "missing-zenodo-handoff.json"
        with self.assertRaises(AssertionError):
            check_release_readiness.check_zenodo_handoff_packet(missing)

    def test_release_preflight_requires_publication_status(self):
        missing = Path(".tmp") / "missing-publication-status.json"
        with self.assertRaises(AssertionError):
            check_release_readiness.check_publication_status_packet(missing)

    def test_release_notes_contain_preflight_evidence(self):
        check_release_readiness.check_release_notes()

    def test_registry_packets_track_external_placeholders(self):
        check_release_readiness.check_registry_packets()

    def test_published_mode_rejects_pending_w3id_markers(self):
        with self.assertRaises(AssertionError):
            check_release_readiness.check_registry_packets(require_published=True)


if __name__ == "__main__":
    unittest.main()
