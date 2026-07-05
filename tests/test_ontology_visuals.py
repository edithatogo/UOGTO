import csv
import json
import shutil
import unittest
import uuid
from pathlib import Path

from scripts.maintenance import visualise_ontology_comparison as visuals


class TestOntologyComparisonVisuals(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_ontology_visuals_{uuid.uuid4().hex}"
        self.figures_dir = self.temp_dir / "figures"
        self.cosmograph_dir = self.temp_dir / "cosmograph"
        self.report = self.temp_dir / "report.md"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_build_visualisation_data_counts_review_statuses(self):
        inventory = {"sources": [{"id": "ext", "name": "External"}]}
        review = [
            {"source_id": "ext", "uogto_source_id": "uogto_core", "review_status": "accepted", "decision_predicate": "skos:exactMatch"},
            {"source_id": "ext", "uogto_source_id": "uogto_core", "review_status": "rejected", "decision_predicate": "skos:closeMatch"},
        ]
        overlap = {"descriptive_summaries": {"ext": {"source_kind": "external_rdf", "term_count": 2}}, "bidirectional_overlap": {"source_by_uogto": []}, "uogto_stronger_coverage_areas": []}
        network = {"source_similarity_graph": {"nodes": [], "edges": [], "metrics": {"degree": {}}}}
        data = visuals.build_visualisation_data(inventory, review, overlap, network)
        self.assertEqual(data["source_sizes"], [{"label": "External", "value": 2, "source_id": "ext"}])
        self.assertEqual(data["review_workload"][0], {"label": "accepted", "value": 1})

    def test_publication_labels_expand_source_ids(self):
        self.assertEqual(visuals.publication_label("bfo"), "Basic Formal Ontology")
        self.assertEqual(visuals.publication_label("uogto_core"), "UOGTO Core")
        self.assertEqual(visuals.publication_label("https://example.org/first-price-auction"), "First Price Auction")
        self.assertEqual(visuals.clip_label("A very long publication label", 15), "A Very Long...")

    def test_generated_repo_visuals_and_report_validate(self):
        inventory = visuals.load_json(visuals.DEFAULT_INVENTORY)
        review = visuals.load_review(visuals.DEFAULT_REVIEW)
        overlap = visuals.load_json(visuals.DEFAULT_OVERLAP)
        network = visuals.load_json(visuals.DEFAULT_NETWORK)
        visuals.build_outputs(inventory, review, overlap, network, self.figures_dir, self.report)
        summary = visuals.validate_outputs(self.figures_dir, self.report, self.cosmograph_dir)
        self.assertEqual(summary["figure_count"], len(visuals.REQUIRED_FIGURES))
        self.assertEqual(summary["cosmograph_image_count"], len(visuals.REQUIRED_COSMOGRAPH_IMAGES))
        report = self.report.read_text(encoding="utf-8")
        self.assertIn("Accepted mappings: 12", report)
        self.assertIn("Source-similarity edges: 391", report)
        self.assertIn("## Inclusion and Exclusion Summary", report)
        self.assertIn("## Mapping Methods", report)
        self.assertIn("## Cosmograph Network Images and Interactive Exports", report)

    def test_report_links_all_required_figures(self):
        inventory = {"sources": [{"id": "ext", "name": "External"}]}
        review = [{"source_id": "ext", "uogto_source_id": "uogto_core", "review_status": "accepted", "decision_predicate": "skos:exactMatch"}]
        overlap = {
            "summary": {"external_term_count": 1, "uogto_term_count": 1, "review_candidate_count": 1},
            "descriptive_summaries": {"ext": {"source_kind": "external_rdf", "term_count": 1}},
            "bidirectional_overlap": {"source_by_uogto": [{"source_id": "ext", "uogto_source_id": "uogto_core", "candidate_count": 1}]},
            "uogto_stronger_coverage_areas": [{"uogto_source_id": "uogto_core", "unique_terms": 1}],
            "recommended_uogto_enhancement_areas": [{"source_id": "ext", "unmatched_terms": 0, "candidate_coverage": 1.0}],
        }
        network = {"summary": {"source_graph_nodes": 2, "alignment_graph_edges": 1, "similarity_graph_edges": 0, "coverage_graph_edges": 1}, "source_similarity_graph": {"nodes": ["ext"], "edges": [], "metrics": {"degree": {"ext": 0}}}, "central_source_families": [{"source_id": "ext", "centrality_score": 1}]}
        visuals.build_outputs(inventory, review, overlap, network, self.figures_dir, self.report)
        visuals.validate_outputs(self.figures_dir, self.report, self.cosmograph_dir)
        for name in visuals.REQUIRED_FIGURES:
            self.assertIn(f"figures/{name}", self.report.read_text(encoding="utf-8"))
        for name in visuals.REQUIRED_COSMOGRAPH_IMAGES:
            self.assertIn(f"cosmograph/{name}", self.report.read_text(encoding="utf-8"))

    def test_check_only_validates_repo_outputs(self):
        visuals.validate_outputs(visuals.DEFAULT_FIGURES, visuals.DEFAULT_REPORT)


if __name__ == "__main__":
    unittest.main()
