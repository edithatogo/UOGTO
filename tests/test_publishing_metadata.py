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

    def test_rejects_incomplete_zenodo_schema(self):
        with self.assertRaises(AssertionError):
            check_publishing_metadata.validate_zenodo_schema(
                {
                    "title": "Incomplete",
                    "upload_type": "dataset",
                    "creators": [],
                }
            )


if __name__ == "__main__":
    unittest.main()
