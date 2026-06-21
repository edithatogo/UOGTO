import json
import shutil
import sys
import unittest
import uuid
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.maintenance import build_manuscript_sources


class TestManuscriptSources(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_manuscript_sources_{uuid.uuid4().hex}"
        self.paper_dir = self.temp_dir / "paper"
        self.sourceright_dir = self.temp_dir / ".sourceright"
        self.temp_dir.mkdir(parents=True)

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_clean_url_removes_tracking_parameters(self):
        clean = build_manuscript_sources.clean_url(
            "https://example.org/source?utm_source=chatgpt.com&id=1&utm_medium=test"
        )
        self.assertEqual(clean, "https://example.org/source?id=1")

    def test_build_csl_references_contains_required_manuscript_sources(self):
        refs = build_manuscript_sources.build_csl_references()
        ids = {ref["id"] for ref in refs}
        cited_ids = {
            "rapoport-chammah-1965",
            "open-spiel-2019",
            "w3c-rdf11-concepts",
            "w3c-owl2-overview",
            "w3c-shacl",
            "w3c-json-ld11",
            "w3c-sparql11-query",
            "openalex",
            "arxiv-api",
            "crossref",
            "arxiv-2006-06580v3",
        }
        self.assertTrue(cited_ids.issubset(ids))
        self.assertIn("w3c-owl2-overview", ids)
        self.assertIn("w3c-shacl", ids)
        self.assertFalse(any("utm_source" in ref.get("URL", "") for ref in refs))

    def test_write_source_artifacts(self):
        inventory = build_manuscript_sources.write_source_artifacts(
            self.paper_dir,
            self.sourceright_dir,
        )
        self.assertGreaterEqual(inventory["reference_count"], 6)
        self.assertTrue((self.paper_dir / "references.csl.json").exists())
        self.assertTrue((self.paper_dir / "source-review-queue.jsonl").exists())
        self.assertTrue((self.sourceright_dir / "references.verification.json").exists())

        refs = json.loads((self.paper_dir / "references.csl.json").read_text(encoding="utf-8"))
        self.assertEqual(refs, json.loads((self.sourceright_dir / "references.csl.json").read_text(encoding="utf-8")))

        verification = json.loads(
            (self.sourceright_dir / "references.verification.json").read_text(encoding="utf-8")
        )
        self.assertEqual(verification["schema_version"], "sourceright.verification.v1")
        for record in verification["references"].values():
            self.assertIn(record["review_status"], {"not_required", "queued"})
            self.assertEqual(record["provider_candidates"][0]["provider"], "uogto-local-source-inventory")

        review_queue = (self.sourceright_dir / "review-queue.jsonl").read_text(encoding="utf-8")
        self.assertEqual(review_queue, "")


if __name__ == "__main__":
    unittest.main()
