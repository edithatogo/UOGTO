import json
import shutil
import unittest
import uuid
from pathlib import Path

from scripts.maintenance import analyse_ontology_networks as networks
from scripts.maintenance import extract_comparison_terms


class TestOntologyNetworks(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_ontology_networks_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_graph_metrics_reports_components_and_orphans(self):
        metrics = networks.graph_metrics({"a", "b", "c"}, [("a", "b", "related")])
        self.assertEqual(metrics["node_count"], 3)
        self.assertEqual(metrics["edge_count"], 1)
        self.assertEqual(metrics["component_count"], 2)
        self.assertEqual(metrics["degree"]["a"], 1)
        self.assertIn("c", metrics["orphan_nodes"])

    def test_alignment_graph_uses_review_accepted_rows_only(self):
        rows = [
            {
                "source_term_iri": "https://example.org/A",
                "uogto_term_iri": "https://w3id.org/uogto/core#A",
                "decision_predicate": "skos:exactMatch",
                "candidate_predicate": "skos:closeMatch",
                "review_status": "accepted",
            },
            {
                "source_term_iri": "https://example.org/B",
                "uogto_term_iri": "https://w3id.org/uogto/core#B",
                "decision_predicate": "skos:closeMatch",
                "candidate_predicate": "skos:closeMatch",
                "review_status": "rejected",
            },
        ]
        graph = networks.term_alignment_graph(rows)
        self.assertEqual(graph["metrics"]["edge_count"], 1)
        self.assertEqual(len(graph["bridge_terms"]), 2)

    def test_similarity_graph_is_deterministic(self):
        terms = [
            extract_comparison_terms.make_row("left", "Left", "family", "external_rdf", None, "https://e/left/Game", "class", "Game theory"),
            extract_comparison_terms.make_row("right", "Right", "family", "external_rdf", None, "https://e/right/Game", "class", "Game model"),
            extract_comparison_terms.make_row("isolated", "Isolated", "family", "external_rdf", None, "https://e/isolated/Clock", "class", "Clock"),
        ]
        graph = networks.source_similarity_graph(terms, threshold=0.1)
        self.assertEqual(graph["edges"], [("left", "right", 0.3333)])
        self.assertIn("isolated", graph["metrics"]["orphan_nodes"])

    def test_build_network_analysis_separates_graph_levels(self):
        terms = [
            extract_comparison_terms.make_row("ext", "External", "demo", "external_rdf", None, "https://e/Game", "class", "Game"),
            extract_comparison_terms.make_row("uogto_core", "UOGTO Core", "core", "uogto", None, "https://w3id.org/uogto/core#Game", "class", "Game"),
        ]
        review = [
            {
                "source_id": "ext",
                "source_term_iri": "https://e/Game",
                "uogto_source_id": "uogto_core",
                "uogto_term_iri": "https://w3id.org/uogto/core#Game",
                "decision_predicate": "skos:exactMatch",
                "candidate_predicate": "skos:closeMatch",
                "review_status": "accepted",
            }
        ]
        provenance = {"sources": [{"id": "ext", "retrieval_mode": "downloaded", "rdf_format": "turtle"}]}
        packet = networks.build_network_analysis(terms, review, provenance)
        self.assertEqual(packet["schema"], "uogto.ontology-comparison.network-analysis.v1")
        self.assertIn("source_ontology_graph", packet)
        self.assertIn("term_alignment_bipartite_graph", packet)
        self.assertEqual(packet["summary"]["alignment_graph_edges"], 1)
        self.assertEqual(networks.validate_network_analysis(packet)["alignment_edges"], 1)

    def test_generated_repo_network_analysis_validates(self):
        terms = extract_comparison_terms.read_jsonl(networks.DEFAULT_TERMS)
        review = networks.load_review(networks.DEFAULT_REVIEW)
        provenance = json.loads(networks.DEFAULT_PROVENANCE.read_text(encoding="utf-8"))
        packet = networks.build_network_analysis(terms, review, provenance)
        summary = networks.validate_network_analysis(packet)
        self.assertEqual(summary["alignment_edges"], 12)
        self.assertGreaterEqual(summary["similarity_edges"], 1)
        self.assertIn("central_source_families", packet)
        self.assertIn("isolated_modelling_paradigms", packet)

    def test_write_json_round_trips(self):
        packet = {
            "schema": "uogto.ontology-comparison.network-analysis.v1",
            "source_ontology_graph": {"metrics": {}},
            "term_alignment_bipartite_graph": {"metrics": {"edge_count": 1}},
            "source_similarity_graph": {"metrics": {"edge_count": 0}},
            "import_uses_graph": {"metrics": {}},
            "uogto_module_coverage_graph": {"metrics": {}},
        }
        output = self.temp_dir / "network.json"
        networks.write_json(output, packet)
        loaded = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(loaded["schema"], packet["schema"])
        self.assertEqual(networks.validate_network_analysis(loaded)["alignment_edges"], 1)


if __name__ == "__main__":
    unittest.main()
