import json
import shutil
import sys
import unittest
import uuid
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.maintenance import build_ontology_snapshot_supplement as snapshot


class TestOntologySnapshotSupplement(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_ontology_snapshot_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True)

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_manifest_contains_release_copy_sources_and_citations(self):
        manifest = snapshot.build_manifest()
        copy_paths = {asset["path"] for asset in manifest["ontology_copy_assets"]}
        self.assertIn("dist/uogto.ttl", copy_paths)
        self.assertIn("dist/uogto-shapes.ttl", copy_paths)
        self.assertGreaterEqual(len(manifest["ontology_source_files"]), 40)
        self.assertEqual(manifest["citation_count"], len(manifest["citations"]))
        self.assertEqual(manifest["citation_count"], 19)
        self.assertTrue(all(len(asset["sha256"]) == 64 for asset in manifest["ontology_copy_assets"]))

    def test_outputs_link_copy_and_citation_register(self):
        manifest_path = self.temp_dir / "manifest.json"
        supplement_path = self.temp_dir / "snapshot.md"
        citation_json_path = self.temp_dir / "citation.json"
        citation_md_path = self.temp_dir / "citation.md"

        snapshot.build_outputs(
            manifest_path=manifest_path,
            supplement_path=supplement_path,
            citation_json_path=citation_json_path,
            citation_md_path=citation_md_path,
        )

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        supplement = supplement_path.read_text(encoding="utf-8")
        citation_md = citation_md_path.read_text(encoding="utf-8")
        citation_json = json.loads(citation_json_path.read_text(encoding="utf-8"))

        self.assertEqual(manifest["schema"], "uogto.ontology-snapshot-supplement.v1")
        self.assertIn("dist/uogto.ttl", supplement)
        self.assertIn("ontology-citation-register.md", supplement)
        self.assertIn("10.5281/zenodo.20796937", citation_md)
        self.assertEqual(len(citation_json["citations"]), 19)


if __name__ == "__main__":
    unittest.main()
