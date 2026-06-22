import json
import shutil
import unittest
import uuid
from pathlib import Path
from unittest import mock

from scripts.maintenance import build_extended_registry_handoff


class TestExtendedRegistryHandoff(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_extended_registry_handoff_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_packet_records_second_wave_statuses(self):
        packet = build_extended_registry_handoff.build_extended_registry_handoff()
        self.assertEqual(packet["schema"], "uogto.extended-registry-handoff.v1")
        self.assertEqual(packet["status"], "external_actions_pending")
        self.assertEqual(packet["targets"]["prefix_cc"]["submitted"]["uogto"]["uri"], "https://w3id.org/uogto/core#")
        self.assertEqual(packet["targets"]["bioregistry"]["issue"], "https://github.com/biopragmatics/bioregistry/issues/1999")
        self.assertEqual(packet["targets"]["obo_foundry"]["status"], "not_prioritized")
        self.assertIn("10.5281/zenodo.20796937", packet["ontology"]["doi"])

    def test_packet_records_actionable_blockers(self):
        packet = build_extended_registry_handoff.build_extended_registry_handoff()
        blockers = {item["target"]: item["message"] for item in packet["blockers"]}
        self.assertIn("fairsharing", blockers)
        self.assertIn("prefix_cc", blockers)
        self.assertIn("wikidata", blockers)
        self.assertIn("ontobee", blockers)
        self.assertNotIn("bioportal", blockers)
        self.assertNotIn("obo_foundry", blockers)

    def test_rejects_doc_missing_canonical_metadata(self):
        with mock.patch.object(build_extended_registry_handoff, "read_doc", return_value="https://fairsharing.org/"):
            with self.assertRaisesRegex(AssertionError, "canonical metadata"):
                build_extended_registry_handoff.build_extended_registry_handoff()

    def test_write_handoff_outputs_json(self):
        output = self.temp_dir / "extended-registry-handoff.json"
        packet = build_extended_registry_handoff.build_extended_registry_handoff()
        build_extended_registry_handoff.write_handoff(output, packet)
        loaded = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(loaded["targets"]["prefix_cc"]["status"], "partial")


if __name__ == "__main__":
    unittest.main()
