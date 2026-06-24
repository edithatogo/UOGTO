import json
import shutil
import unittest
import uuid
from pathlib import Path

from scripts.maintenance import build_ontology_comparison_inventory


class TestOntologyComparisonInventory(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_ontology_comparison_inventory_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_seed_inventory_validates(self):
        packet = build_ontology_comparison_inventory.load_inventory()
        summary = build_ontology_comparison_inventory.validate_inventory(packet)
        self.assertGreaterEqual(summary["source_count"], 20)
        self.assertGreaterEqual(summary["family_count"], 10)
        self.assertIn("simulation_algorithm", summary["by_family"])
        self.assertIn("agent_based_modelling", summary["by_family"])
        self.assertIn("system_dynamics", summary["by_family"])
        self.assertIn("redistributable_artifact", summary["by_licence_disposition"])

    def test_inclusion_log_references_known_sources(self):
        packet = build_ontology_comparison_inventory.load_inventory()
        source_ids = {source["id"] for source in packet["sources"]}
        count = build_ontology_comparison_inventory.validate_inclusion_log(source_ids=source_ids)
        self.assertGreaterEqual(count, len(source_ids))

    def test_render_markdown_contains_key_sources(self):
        packet = build_ontology_comparison_inventory.load_inventory()
        summary = build_ontology_comparison_inventory.validate_inventory(packet)
        markdown = build_ontology_comparison_inventory.render_markdown(packet, summary)
        self.assertIn("Kinetic Simulation Algorithm Ontology", markdown)
        self.assertIn("Simulation Experiment Description Markup Language", markdown)
        self.assertIn("European Materials and Modelling Ontology", markdown)
        self.assertIn("PROV-O", markdown)

    def test_duplicate_source_ids_are_rejected(self):
        packet = build_ontology_comparison_inventory.load_inventory()
        duplicate = json.loads(json.dumps(packet))
        duplicate["sources"].append(dict(duplicate["sources"][0]))
        with self.assertRaisesRegex(AssertionError, "Duplicate source id"):
            build_ontology_comparison_inventory.validate_inventory(duplicate)

    def test_write_markdown_outputs_file(self):
        packet = build_ontology_comparison_inventory.load_inventory()
        summary = build_ontology_comparison_inventory.validate_inventory(packet)
        output = self.temp_dir / "source-inventory.md"
        build_ontology_comparison_inventory.write_markdown(
            output,
            build_ontology_comparison_inventory.render_markdown(packet, summary),
        )
        self.assertIn("# Comparative Ontology Source Inventory", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
