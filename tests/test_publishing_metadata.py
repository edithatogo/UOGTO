import os
import sys
import unittest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.maintenance import check_publishing_metadata


class TestPublishingMetadata(unittest.TestCase):
    def test_required_files_exist(self):
        check_publishing_metadata.check_required_files()

    def test_citation_metadata(self):
        check_publishing_metadata.check_citation()

    def test_zenodo_metadata(self):
        check_publishing_metadata.check_zenodo()

    def test_widoco_workflow(self):
        check_publishing_metadata.check_workflow()

    def test_registry_annotations(self):
        check_publishing_metadata.check_registry_annotations()

    def test_registry_docs(self):
        check_publishing_metadata.check_registry_docs()

    def test_rejects_incomplete_citation_schema(self):
        with self.assertRaises(AssertionError):
            check_publishing_metadata.validate_citation_schema(
                {
                    "cff-version": "1.2.0",
                    "message": "Cite this.",
                    "title": "Incomplete",
                }
            )

    def test_rejects_invalid_citation_url_format(self):
        with self.assertRaises(AssertionError):
            check_publishing_metadata.validate_citation_schema(
                {
                    "cff-version": "1.2.0",
                    "message": "Cite this.",
                    "authors": [{"name": "UOGTO Contributors"}],
                    "title": "Universal Open Game Theory Ontology (UOGTO)",
                    "version": "1.0.0",
                    "date-released": "2026-06-22",
                    "url": "not-a-url",
                    "repository-code": "https://github.com/edithatogo/UOGTO",
                    "license": "CC-BY-4.0",
                    "keywords": ["game theory", "ontology", "semantic web"],
                    "abstract": "A test abstract.",
                }
            )

    def test_rejects_incomplete_zenodo_schema(self):
        with self.assertRaises(AssertionError):
            check_publishing_metadata.validate_zenodo_schema(
                {
                    "title": "Incomplete",
                    "upload_type": "dataset",
                    "creators": [],
                }
            )

    def test_rejects_invalid_zenodo_language(self):
        with self.assertRaises(AssertionError):
            check_publishing_metadata.validate_zenodo_schema(
                {
                    "title": "Universal Open Game Theory Ontology (UOGTO)",
                    "upload_type": "dataset",
                    "description": "A test description.",
                    "creators": [{"name": "UOGTO Contributors"}],
                    "license": "cc-by-4.0",
                    "keywords": ["game theory", "ontology", "semantic web"],
                    "related_identifiers": [
                        {
                            "identifier": "https://github.com/edithatogo/UOGTO",
                            "relation": "isSupplementTo",
                            "resource_type": "software",
                            "scheme": "url",
                        }
                    ],
                    "version": "1.0.0",
                    "language": "en",
                    "access_right": "open",
                }
            )


if __name__ == "__main__":
    unittest.main()
