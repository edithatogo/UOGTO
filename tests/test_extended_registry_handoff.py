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
        self.assertEqual(packet["status"], "external_review_pending")
        self.assertEqual(packet["targets"]["prefix_cc"]["submitted"]["uogto"]["uri"], "https://w3id.org/uogto/core#")
        self.assertEqual(packet["targets"]["prefix_cc"]["submitted"]["uogtox"]["uri"], "https://w3id.org/uogto/extensions#")
        self.assertEqual(packet["targets"]["fairsharing"]["record"], "https://fairsharing.org/8382")
        self.assertEqual(packet["targets"]["fairsharing"]["review_status"], "awaiting_fairsharing_curator_review")
        self.assertEqual(packet["targets"]["wikidata"]["status"], "created_verified")
        self.assertEqual(packet["targets"]["wikidata"]["item"], "https://www.wikidata.org/wiki/Q140323510")
        self.assertEqual(packet["targets"]["ontobee"]["issue"], "https://github.com/OntoZoo/ontobee/issues/212")
        self.assertEqual(packet["targets"]["bioregistry"]["issue"], "https://github.com/biopragmatics/bioregistry/issues/1999")
        self.assertEqual(
            packet["targets"]["bioregistry"]["template_update_comment"],
            "https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4778481220",
        )
        self.assertEqual(
            packet["targets"]["bioregistry"]["status"],
            "orcid_added_awaiting_maintainer_review",
        )
        self.assertEqual(
            packet["targets"]["bioregistry"]["namespace_orcid_feedback"],
            "https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4796538000",
        )
        self.assertEqual(
            packet["targets"]["bioregistry"]["response_comment"],
            build_extended_registry_handoff.BIOREGISTRY_RESPONSE_COMMENT,
        )
        self.assertEqual(
            packet["targets"]["bioregistry"]["orcid_comment"],
            build_extended_registry_handoff.BIOREGISTRY_ORCID_COMMENT,
        )
        self.assertEqual(
            packet["targets"]["bioregistry"]["author_orcid"],
            build_extended_registry_handoff.AUTHOR_ORCID_URL,
        )
        self.assertIn("primary core prefix", packet["targets"]["bioregistry"]["namespace_decision"])
        self.assertIn("approved public project metadata", packet["targets"]["bioregistry"]["orcid_handling"])
        self.assertIn("bioregistry", packet["review_pending"])
        self.assertEqual(packet["targets"]["obo_foundry"]["status"], "not_prioritized")
        self.assertIn("10.5281/zenodo.20796937", packet["ontology"]["doi"])

    def test_packet_records_actionable_blockers(self):
        packet = build_extended_registry_handoff.build_extended_registry_handoff()
        blockers = {item["target"]: item["message"] for item in packet["blockers"]}
        self.assertNotIn("fairsharing", blockers)
        self.assertNotIn("prefix_cc", blockers)
        self.assertNotIn("wikidata", blockers)
        self.assertNotIn("ontobee", blockers)
        self.assertNotIn("bioportal", blockers)
        self.assertNotIn("obo_foundry", blockers)

    def test_rejects_doc_missing_canonical_metadata(self):
        with mock.patch.object(build_extended_registry_handoff, "read_doc", return_value="https://fairsharing.org/"):
            with self.assertRaisesRegex(AssertionError, "canonical metadata"):
                build_extended_registry_handoff.build_extended_registry_handoff()

    def test_display_path_accepts_relative_output(self):
        self.assertEqual(
            build_extended_registry_handoff.display_path(Path("dist/extended-registry-handoff.json")),
            str(Path("dist/extended-registry-handoff.json")),
        )

    def test_write_handoff_outputs_json(self):
        output = self.temp_dir / "extended-registry-handoff.json"
        packet = build_extended_registry_handoff.build_extended_registry_handoff()
        build_extended_registry_handoff.write_handoff(output, packet)
        loaded = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(loaded["targets"]["prefix_cc"]["status"], "submitted")


if __name__ == "__main__":
    unittest.main()
