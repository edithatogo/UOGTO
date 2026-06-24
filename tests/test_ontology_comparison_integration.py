import shutil
import unittest
import uuid
from pathlib import Path

from scripts.maintenance import check_ontology_comparison_artifacts as check


class TestOntologyComparisonIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_ontology_comparison_integration_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_repo_artifact_contract_is_complete(self):
        summary = check.validate_artifacts()
        self.assertEqual(summary["sources"], 21)
        self.assertEqual(summary["accepted_mappings"], 10)
        self.assertEqual(summary["figures"], len(check.REQUIRED_FIGURES))
        self.assertEqual(summary["sssom_rows"], 10)
        self.assertGreater(summary["terms"], 1000)
        self.assertGreater(summary["candidates"], 100)

    def test_missing_artifact_fails_validation(self):
        comparison = self.temp_dir / "ontology-comparison"
        comparison.mkdir()
        with self.assertRaisesRegex(AssertionError, "Missing ontology comparison artifacts"):
            check.validate_artifacts(comparison)

    def test_makefile_and_pixi_expose_phase9_targets(self):
        makefile = Path("Makefile").read_text(encoding="utf-8")
        pixi = Path("pixi.toml").read_text(encoding="utf-8")
        self.assertIn("ontology-comparison-check", makefile)
        self.assertIn("ontology-comparison-sssom", makefile)
        self.assertIn("ontology-comparison-all", makefile)
        self.assertIn("ontology-comparison-check", pixi)
        self.assertIn("ontology-comparison-sssom", pixi)
        self.assertIn("ontology-comparison-all", pixi)

    def test_readme_links_comparison_report(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        self.assertIn("docs/ontology-comparison/report.md", readme)

    def test_report_contains_required_method_sections(self):
        report = Path("docs/ontology-comparison/report.md").read_text(encoding="utf-8")
        self.assertIn("## Inclusion and Exclusion Summary", report)
        self.assertIn("## Mapping Methods", report)


if __name__ == "__main__":
    unittest.main()
