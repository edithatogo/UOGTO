import shutil
import unittest
import uuid
from pathlib import Path

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
        self.assertEqual(packet["checks"]["doi"]["status"], "pending_external_zenodo_doi")
        self.assertEqual(packet["checks"]["lov"]["status"], "blocked_until_doi_recorded")
        self.assertEqual(packet["checks"]["ols"]["status"], "blocked_until_doi_recorded")
        self.assertEqual(packet["checks"]["w3id"]["status"], "pending_external_w3id_merge")
        self.assertIn("publication-status.json", packet["assets"])

    def test_write_status_outputs_json(self):
        output = self.temp_dir / "publication-status.json"
        packet = build_publication_status.build_publication_status()
        build_publication_status.write_status(output, packet)
        self.assertIn('"schema": "uogto.publication-status.v1"', output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
