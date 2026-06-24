import json
import shutil
import unittest
import uuid
from pathlib import Path

from scripts.maintenance import harvest_comparison_sources


class TestOntologyComparisonHarvest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_ontology_comparison_harvest_{uuid.uuid4().hex}"
        self.source_dir = self.temp_dir / "sources"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_metadata_only_record_for_non_redistributable_source(self):
        source = {
            "id": "demo_doc",
            "name": "Demo documentation",
            "family": "demo",
            "source_url": "https://example.test/demo",
            "artifact_url": None,
            "expected_format": "documentation",
            "licence_disposition": "metadata_only",
        }
        record = harvest_comparison_sources.harvest_source(source, self.source_dir, "2026-06-24T00:00:00Z")
        self.assertEqual(record["retrieval_mode"], "metadata_only")
        self.assertEqual(record["format_classification"], "non_rdf_or_documentation")
        self.assertIsNone(record["checksum_sha256"])
        self.assertFalse(self.source_dir.exists())

    def test_redistributable_rdf_source_is_downloaded_and_parsed(self):
        source = {
            "id": "demo_rdf",
            "name": "Demo RDF",
            "family": "demo",
            "source_url": "https://example.test/demo",
            "artifact_url": "https://example.test/demo.ttl",
            "expected_format": "OWL/RDF",
            "licence_disposition": "redistributable_artifact",
        }

        data = b"@prefix ex: <https://example.test/> .\nex:a ex:b ex:c .\n"

        def fake_fetcher(url):
            self.assertEqual(url, "https://example.test/demo.ttl")
            return data, {
                "http_status": 200,
                "content_type": "text/turtle",
                "canonical_url": "https://example.test/demo.ttl",
            }

        record = harvest_comparison_sources.harvest_source(
            source,
            self.source_dir,
            "2026-06-24T00:00:00Z",
            fetcher=fake_fetcher,
        )
        self.assertEqual(record["retrieval_mode"], "downloaded")
        self.assertEqual(record["parse_status"], "parsed")
        self.assertEqual(record["rdf_format"], "turtle")
        self.assertGreaterEqual(record["triple_count"], 1)
        self.assertEqual(record["byte_size"], len(data))
        self.assertTrue(Path(record["local_path"]).as_posix().endswith("demo_rdf.ttl"))

    def test_validate_provenance_requires_full_inventory_coverage(self):
        inventory = {"sources": [{"id": "one"}, {"id": "two"}]}
        packet = {
            "schema": "uogto.ontology-comparison.source-provenance.v1",
            "sources": [
                {
                    "id": "one",
                    "retrieval_timestamp": "2026-06-24T00:00:00Z",
                    "retrieval_mode": "metadata_only",
                    "canonical_url": "https://example.test/one",
                    "format_classification": "non_rdf_or_documentation",
                    "parse_status": "not_attempted",
                    "manual_review_note": "metadata only",
                }
            ],
        }
        with self.assertRaisesRegex(AssertionError, "cover every inventory source"):
            harvest_comparison_sources.validate_provenance(packet, inventory)

    def test_write_json_outputs_file(self):
        output = self.temp_dir / "source-provenance.json"
        packet = {
            "schema": "uogto.ontology-comparison.source-provenance.v1",
            "sources": [{"id": "b"}, {"id": "a"}],
        }
        harvest_comparison_sources.write_json(output, packet)
        written = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(written["schema"], packet["schema"])


if __name__ == "__main__":
    unittest.main()
