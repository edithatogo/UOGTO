import json
import shutil
import sys
import unittest
import uuid
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.maintenance import build_registry_handoff


class TestRegistryHandoff(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_registry_handoff_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_submitted_handoff_records_registry_issue_urls(self):
        packet = build_registry_handoff.build_registry_handoff()
        self.assertEqual(packet["schema"], "uogto.registry-handoff.v1")
        self.assertEqual(packet["status"], "submitted_to_registries")
        self.assertEqual(packet["blockers"], [])
        self.assertEqual(packet["ontology"]["doi"], "https://doi.org/10.5281/zenodo.20796937")
        self.assertEqual(packet["lov"]["status"], "submitted")
        self.assertEqual(packet["lov"]["submission_url"], "https://github.com/pyvandenbussche/lov/issues/83")
        self.assertEqual(packet["ols"]["status"], "submitted")
        self.assertEqual(packet["ols"]["request_url"], "https://github.com/EBISPOT/ols4/issues/1305")
        self.assertEqual(packet["ols"]["requested_identifier"], "uogto")

    def test_require_ready_rejects_pending_doi_placeholders(self):
        with mock.patch.object(build_registry_handoff, "doi_state", return_value=([], True)):
            with self.assertRaises(AssertionError):
                build_registry_handoff.build_registry_handoff(require_ready=True)

    def test_write_handoff_outputs_json(self):
        output = self.temp_dir / "registry-handoff.json"
        packet = build_registry_handoff.build_registry_handoff()
        build_registry_handoff.write_handoff(output, packet)
        loaded = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(loaded["artifacts"]["merged_ontology"], packet["artifacts"]["merged_ontology"])
        self.assertEqual(loaded["status"], "submitted_to_registries")
        self.assertEqual(
            loaded["artifacts"]["registry_handoff"],
            "https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/registry-handoff.json",
        )


if __name__ == "__main__":
    unittest.main()
