import json
import shutil
import unittest
import uuid
from pathlib import Path

from scripts.maintenance import extract_comparison_terms


class TestOntologyComparisonTerms(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_ontology_comparison_terms_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_split_identifier_and_tokens_are_deterministic(self):
        self.assertEqual(extract_comparison_terms.split_identifier("NormalFormGame"), ["Normal", "Form", "Game"])
        self.assertEqual(extract_comparison_terms.tokens("The Normal-Form_Game"), ["normal", "form", "game"])

    def test_extract_rdf_terms_preserves_annotations_and_context(self):
        ttl = self.temp_dir / "fixture.ttl"
        ttl.write_text(
            """@prefix ex: <https://example.test/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
ex:Game a owl:Class ; rdfs:label "Game" ; skos:definition "A strategic interaction." .
ex:hasPlayer a owl:ObjectProperty ; rdfs:label "has player" ; rdfs:domain ex:Game ; rdfs:range ex:Player .
""",
            encoding="utf-8",
        )
        rows = extract_comparison_terms.extract_rdf(ttl, "fixture", "Fixture", "demo", "external_rdf")
        by_iri = {row["term_iri"]: row for row in rows}
        self.assertEqual(by_iri["https://example.test/Game"]["term_type"], "class")
        self.assertIn("A strategic interaction.", by_iri["https://example.test/Game"]["definitions"])
        self.assertEqual(by_iri["https://example.test/hasPlayer"]["domains"], ["https://example.test/Game"])
        self.assertEqual(by_iri["https://example.test/hasPlayer"]["ranges"], ["https://example.test/Player"])

    def test_metadata_source_gets_comparable_source_row(self):
        source = {
            "id": "demo_doc",
            "name": "Demo Documentation Standard",
            "family": "documentation_family",
            "source_url": "https://example.test/demo",
            "artifact_url": None,
            "candidate_type": "documentation",
            "expected_format": "documentation",
            "licence_disposition": "metadata_only",
            "inclusion_rationale": "Useful structured reporting concepts.",
        }
        row = extract_comparison_terms.metadata_row(source, {})
        self.assertEqual(row["source_kind"], "external_metadata")
        self.assertEqual(row["term_type"], "source_metadata")
        self.assertIn("documentation", row["tokens"])
        self.assertIn("Useful structured reporting concepts.", row["definitions"])

    def test_generated_inventory_contains_uogto_and_external_sources(self):
        inventory = extract_comparison_terms.load_json(extract_comparison_terms.DEFAULT_INVENTORY)
        provenance = extract_comparison_terms.load_json(extract_comparison_terms.DEFAULT_PROVENANCE)
        rows = extract_comparison_terms.build_terms(inventory, provenance)
        summary = extract_comparison_terms.validate_rows(rows)
        self.assertGreater(summary["row_count"], 100)
        self.assertIn("uogto", summary["by_kind"])
        self.assertIn("external_rdf", summary["by_kind"])
        self.assertIn("external_metadata", summary["by_kind"])
        source_ids = {row["source_id"] for row in rows}
        self.assertIn("schema_org", source_ids)
        self.assertIn("game_ontology_project", source_ids)

    def test_write_and_read_jsonl_round_trips(self):
        rows = [
            extract_comparison_terms.make_row(
                "demo", "Demo", "family", "external_metadata", None, "https://example.test/demo", "source_metadata", "Demo Label"
            )
        ]
        output = self.temp_dir / "terms.jsonl"
        extract_comparison_terms.write_jsonl(output, rows)
        loaded = extract_comparison_terms.read_jsonl(output)
        self.assertEqual(loaded[0]["source_id"], "demo")
        self.assertEqual(extract_comparison_terms.validate_rows(loaded)["row_count"], 1)


if __name__ == "__main__":
    unittest.main()
