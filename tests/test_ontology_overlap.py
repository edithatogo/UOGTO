import json
import shutil
import unittest
import uuid
from pathlib import Path

from scripts.maintenance import analyse_ontology_overlap as overlap
from scripts.maintenance import extract_comparison_terms


class TestOntologyOverlap(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_ontology_overlap_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_review_summaries_compute_precision(self):
        rows = [
            {"source_id": "ext", "uogto_source_id": "uogto_core", "review_status": "accepted"},
            {"source_id": "ext", "uogto_source_id": "uogto_core", "review_status": "rejected"},
            {"source_id": "ext", "uogto_source_id": "uogto_ext", "review_status": "needs_domain_review"},
        ]
        by_source, by_pair = overlap.review_summaries(rows)
        self.assertEqual(by_source["ext"]["candidate_count"], 3)
        self.assertEqual(by_source["ext"]["review_precision"], 0.5)
        self.assertEqual(len(by_pair), 2)

    def test_source_summary_reports_annotation_and_density(self):
        rows = [
            extract_comparison_terms.make_row("ext", "External", "family", "external_rdf", None, "https://e/Game", "class", "Game", ["Definition"]),
            extract_comparison_terms.make_row("ext", "External", "family", "external_rdf", None, "https://e/hasPlayer", "object_property", "has player"),
        ]
        summary = overlap.source_summary("ext", rows, {"name": "External", "family": "family", "licence_disposition": "redistributable_artifact"}, {"parse_status": "parsed", "retrieval_mode": "downloaded"})
        self.assertEqual(summary["term_count"], 2)
        self.assertEqual(summary["annotation_completeness"], 0.5)
        self.assertEqual(summary["property_density"], 0.5)
        self.assertEqual(summary["parse_status"], "parsed")

    def test_build_metrics_separates_source_and_uogto_coverage(self):
        terms = [
            extract_comparison_terms.make_row("uogto_core_games", "games", "core", "uogto", None, "https://w3id.org/uogto/core#Game", "class", "Game"),
            extract_comparison_terms.make_row("uogto_core_games", "games", "core", "uogto", None, "https://w3id.org/uogto/core#Strategy", "class", "Strategy"),
            extract_comparison_terms.make_row("ext", "External", "demo", "external_rdf", None, "https://e/Game", "class", "Game"),
            extract_comparison_terms.make_row("ext", "External", "demo", "external_rdf", None, "https://e/Other", "class", "Other"),
        ]
        review = [{"source_id": "ext", "source_term_iri": "https://e/Game", "uogto_source_id": "uogto_core_games", "uogto_term_iri": "https://w3id.org/uogto/core#Game", "review_status": "accepted"}]
        inventory = {"sources": [{"id": "ext", "name": "External", "family": "demo", "licence_disposition": "redistributable_artifact"}]}
        provenance = {"sources": [{"id": "ext", "parse_status": "parsed", "retrieval_mode": "downloaded"}]}
        packet = overlap.build_metrics(terms, review, inventory, provenance)
        self.assertEqual(packet["source_coverage"]["ext"]["accepted_term_count"], 1)
        self.assertEqual(packet["uogto_coverage"]["accepted_term_count"], 1)
        self.assertEqual(packet["summary"]["accepted_mapping_count"], 1)
        self.assertTrue(packet["unmatched_source_concepts"])
        self.assertTrue(packet["uogto_unique_concepts"])

    def test_generated_repo_metrics_validate(self):
        terms = extract_comparison_terms.read_jsonl(overlap.DEFAULT_TERMS)
        review = overlap.load_review(overlap.DEFAULT_REVIEW)
        inventory = json.loads(overlap.DEFAULT_INVENTORY.read_text(encoding="utf-8"))
        provenance = json.loads(overlap.DEFAULT_PROVENANCE.read_text(encoding="utf-8"))
        packet = overlap.build_metrics(terms, review, inventory, provenance)
        summary = overlap.validate_metrics(packet)
        self.assertEqual(summary["external_sources"], 21)
        self.assertGreaterEqual(summary["accepted_mapping_count"], 1)
        self.assertIn("source_by_uogto", packet["bidirectional_overlap"])

    def test_write_json_round_trips(self):
        packet = {"schema": "uogto.ontology-comparison.overlap-metrics.v1", "summary": {"external_source_count": 1, "uogto_term_count": 1, "accepted_mapping_count": 0}, "source_coverage": {}, "uogto_coverage": {}, "bidirectional_overlap": {"source_by_uogto": []}, "term_type_coverage": {}, "descriptive_summaries": {}}
        output = self.temp_dir / "metrics.json"
        overlap.write_json(output, packet)
        self.assertEqual(overlap.validate_metrics(json.loads(output.read_text(encoding="utf-8")))["external_sources"], 1)


if __name__ == "__main__":
    unittest.main()
