import unittest
import uuid
import shutil
from pathlib import Path

from scripts.maintenance import build_zenodo_handoff


class TestZenodoHandoff(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_zenodo_handoff_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_pending_handoff_records_external_doi_blocker(self):
        packet = build_zenodo_handoff.build_zenodo_handoff()
        self.assertEqual(packet["schema"], "uogto.zenodo-handoff.v1")
        self.assertEqual(packet["status"], "pending_external_zenodo_doi")
        self.assertIn("Zenodo DOI", packet["blockers"][0])
        self.assertEqual(packet["release_tag"], "v1.0.0")
        self.assertIn("uogto.ttl", packet["release_assets"])
        self.assertEqual(packet["account_side_cli"]["token_env"], "ZENODO_ACCESS_TOKEN")

    def test_write_handoff_outputs_json(self):
        output = self.temp_dir / "zenodo-handoff.json"
        packet = build_zenodo_handoff.build_zenodo_handoff()
        build_zenodo_handoff.write_handoff(output, packet)
        self.assertIn('"schema": "uogto.zenodo-handoff.v1"', output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
