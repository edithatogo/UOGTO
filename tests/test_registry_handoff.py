import json
import shutil
import sys
import unittest
import uuid
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.maintenance import build_registry_handoff


class TestRegistryHandoff(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_registry_handoff_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_pending_handoff_records_external_doi_blocker(self):
        packet = build_registry_handoff.build_registry_handoff()
        self.assertEqual(packet["schema"], "uogto.registry-handoff.v1")
        self.assertEqual(packet["status"], "pending_external_doi")
        self.assertIn("Zenodo DOI", packet["blockers"][0])
        self.assertIsNone(packet["ontology"]["doi"])
        self.assertEqual(packet["ols"]["requested_identifier"], "uogto")

    def test_require_ready_rejects_pending_doi_placeholders(self):
        with self.assertRaises(AssertionError):
            build_registry_handoff.build_registry_handoff(require_ready=True)

    def test_write_handoff_outputs_json(self):
        output = self.temp_dir / "registry-handoff.json"
        packet = build_registry_handoff.build_registry_handoff()
        build_registry_handoff.write_handoff(output, packet)
        loaded = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(loaded["artifacts"]["merged_ontology"], packet["artifacts"]["merged_ontology"])
        self.assertEqual(
            loaded["artifacts"]["registry_handoff"],
            "https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/registry-handoff.json",
        )


if __name__ == "__main__":
    unittest.main()
