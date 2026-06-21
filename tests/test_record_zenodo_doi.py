import json
import os
import sys
import unittest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.maintenance import record_zenodo_doi


class TestRecordZenodoDoi(unittest.TestCase):
    def test_normalizes_doi_url(self):
        self.assertEqual(
            record_zenodo_doi.normalize_doi("https://doi.org/10.5281/zenodo.12345"),
            "10.5281/zenodo.12345",
        )

    def test_rejects_invalid_doi(self):
        with self.assertRaises(ValueError):
            record_zenodo_doi.normalize_doi("not-a-doi")

    def test_updates_markdown_placeholders_and_checklists(self):
        text = "\n".join(
            [
                "Zenodo DOI: `TBD after Zenodo archiving`",
                "- [ ] Zenodo DOI is minted and recorded.",
                "- [ ] Confirm the Zenodo DOI resolves.",
            ]
        )
        updated = record_zenodo_doi.update_markdown_text(text, "10.5281/zenodo.12345")
        self.assertIn("<https://doi.org/10.5281/zenodo.12345>", updated)
        self.assertIn("- [x] Zenodo DOI is minted and recorded.", updated)
        self.assertIn("- [x] Confirm the Zenodo DOI resolves.", updated)
        self.assertNotIn("TBD after Zenodo archiving", updated)

    def test_updates_existing_citation_doi(self):
        citation = "title: Example\ndoi: 10.5281/zenodo.old\nversion: 1.0.0\n"
        updated = record_zenodo_doi.update_citation_text(citation, "10.5281/zenodo.12345")
        self.assertIn("doi: 10.5281/zenodo.12345", updated)
        self.assertNotIn("10.5281/zenodo.old", updated)

    def test_inserts_citation_doi_after_title(self):
        citation = "cff-version: 1.2.0\ntitle: Example\nversion: 1.0.0\n"
        updated = record_zenodo_doi.update_citation_text(citation, "10.5281/zenodo.12345")
        self.assertEqual(
            updated.splitlines(),
            ["cff-version: 1.2.0", "title: Example", "doi: 10.5281/zenodo.12345", "version: 1.0.0"],
        )

    def test_adds_zenodo_related_identifier_once(self):
        metadata = {"related_identifiers": []}
        updated = record_zenodo_doi.update_zenodo_metadata(metadata, "10.5281/zenodo.12345")
        updated_again = record_zenodo_doi.update_zenodo_metadata(updated, "10.5281/zenodo.12345")
        doi_entries = [
            item
            for item in updated_again["related_identifiers"]
            if item.get("scheme") == "doi" and item.get("identifier") == "10.5281/zenodo.12345"
        ]
        self.assertEqual(len(doi_entries), 1)
        self.assertEqual(json.dumps(updated_again, sort_keys=True).count("10.5281/zenodo.12345"), 1)


if __name__ == "__main__":
    unittest.main()
