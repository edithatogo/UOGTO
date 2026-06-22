import shutil
import unittest
import uuid
from pathlib import Path
from unittest import mock

from scripts.maintenance import build_publication_status


class TestPublicationStatus(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_publication_status_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_status_aggregates_external_publication_blockers(self):
        packet = build_publication_status.build_publication_status()
        self.assertEqual(packet["schema"], "uogto.publication-status.v1")
        self.assertEqual(packet["status"], "pending_external_publication_steps")
        self.assertEqual(packet["checks"]["doi"]["status"], "recorded")
        self.assertEqual(packet["checks"]["doi"]["local_dois"], ["10.5281/zenodo.20796937"])
        self.assertEqual(packet["checks"]["lov"]["status"], "submitted")
        self.assertEqual(packet["checks"]["lov"]["submission_url"], "https://github.com/pyvandenbussche/lov/issues/83")
        self.assertEqual(packet["checks"]["ols"]["status"], "submitted")
        self.assertEqual(packet["checks"]["ols"]["request_url"], "https://github.com/EBISPOT/ols4/issues/1305")
        self.assertEqual(packet["checks"]["w3id"]["status"], "pending_external_w3id_merge")
        self.assertIn("publication-status.json", packet["assets"])

    def test_write_status_outputs_json(self):
        output = self.temp_dir / "publication-status.json"
        packet = build_publication_status.build_publication_status()
        build_publication_status.write_status(output, packet)
        self.assertIn('"schema": "uogto.publication-status.v1"', output.read_text(encoding="utf-8"))

    def test_display_path_accepts_relative_output(self):
        self.assertEqual(
            build_publication_status.display_path(Path("dist/publication-status-live.json")),
            str(Path("dist/publication-status-live.json")),
        )

    def test_live_status_records_url_observations(self):
        with (
            mock.patch.object(
                build_publication_status,
                "fetch_url",
                return_value=build_publication_status.UrlObservation(
                    url="https://example.test/",
                    status=200,
                    final_url="https://example.test/",
                    ok=True,
                ),
            ),
            mock.patch.object(
                build_publication_status.check_doi_status,
                "check_live_zenodo",
                return_value=[],
            ),
            mock.patch.object(
                build_publication_status.check_w3id_status,
                "check_pr_state",
                return_value={"state": "open", "merged": False},
            ),
            mock.patch.object(
                build_publication_status.check_w3id_status,
                "check_redirects",
                return_value=[],
            ),
        ):
            packet = build_publication_status.build_publication_status(include_live=True)
        self.assertIn("live", packet)
        self.assertTrue(packet["live"]["documentation"]["ok"])
        self.assertEqual(packet["live"]["zenodo_dois"], [])
        self.assertEqual(packet["live"]["w3id"]["pull_request"]["state"], "open")

    def test_require_live_rejects_failed_public_url(self):
        with (
            mock.patch.object(
                build_publication_status,
                "fetch_url",
                return_value=build_publication_status.UrlObservation(
                    url="https://example.test/missing",
                    status=404,
                    final_url="https://example.test/missing",
                    ok=False,
                ),
            ),
            mock.patch.object(
                build_publication_status.check_doi_status,
                "check_live_zenodo",
                return_value=[],
            ),
            mock.patch.object(
                build_publication_status.check_w3id_status,
                "check_pr_state",
                return_value={"state": "open", "merged": False},
            ),
            mock.patch.object(
                build_publication_status.check_w3id_status,
                "check_redirects",
                return_value=[],
            ),
        ):
            with self.assertRaisesRegex(AssertionError, "Live publication status check failed"):
                build_publication_status.build_publication_status(require_live=True)

    def test_require_live_rejects_unmerged_w3id_pr(self):
        with (
            mock.patch.object(
                build_publication_status,
                "fetch_url",
                return_value=build_publication_status.UrlObservation(
                    url="https://example.test/",
                    status=200,
                    final_url="https://example.test/",
                    ok=True,
                ),
            ),
            mock.patch.object(
                build_publication_status.check_doi_status,
                "check_live_zenodo",
                return_value=[],
            ),
            mock.patch.object(
                build_publication_status.check_w3id_status,
                "check_pr_state",
                return_value={"state": "open", "merged": False},
            ),
            mock.patch.object(
                build_publication_status.check_w3id_status,
                "check_redirects",
                return_value=[],
            ),
        ):
            with self.assertRaisesRegex(AssertionError, "pull/6238"):
                build_publication_status.build_publication_status(require_live=True)


if __name__ == "__main__":
    unittest.main()
