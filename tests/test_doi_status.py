import os
import sys
import unittest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.maintenance import check_doi_status


class TestDoiStatus(unittest.TestCase):
    def test_local_docs_track_pending_doi(self):
        dois = check_doi_status.check_local_doi_state()
        self.assertEqual(dois, [])

    def test_require_doi_rejects_placeholders(self):
        with self.assertRaises(AssertionError):
            check_doi_status.check_local_doi_state(require_doi=True)

    def test_extracts_doi_tokens(self):
        text = "DOI: `10.5281/zenodo.12345` and <https://doi.org/10.5281/zenodo.67890>."
        self.assertEqual(
            check_doi_status.extract_dois_from_docs(text),
            ["10.5281/zenodo.12345", "10.5281/zenodo.67890"],
        )

    def test_matches_title_or_related_repository(self):
        self.assertTrue(
            check_doi_status.record_matches_uogto(
                {"metadata": {"title": "Universal Open Game Theory Ontology (UOGTO)"}}
            )
        )
        self.assertTrue(
            check_doi_status.record_matches_uogto(
                {
                    "metadata": {
                        "title": "Other title",
                        "related_identifiers": [
                            {"identifier": "https://github.com/edithatogo/UOGTO"}
                        ],
                    }
                }
            )
        )

    def test_extracts_matching_zenodo_dois(self):
        payload = {
            "hits": {
                "hits": [
                    {
                        "metadata": {
                            "title": "Universal Open Game Theory Ontology (UOGTO)",
                            "doi": "10.5281/zenodo.12345",
                        }
                    },
                    {"metadata": {"title": "Unrelated record", "doi": "10.5281/zenodo.00000"}},
                ]
            }
        }
        self.assertEqual(check_doi_status.find_uogto_zenodo_dois(payload), ["10.5281/zenodo.12345"])

    def test_live_requires_matching_doi(self):
        original_fetch = check_doi_status.fetch_json
        try:
            check_doi_status.fetch_json = lambda _url, timeout=20: {"hits": {"hits": []}}
            with self.assertRaises(AssertionError):
                check_doi_status.check_live_zenodo(require_doi=True)
        finally:
            check_doi_status.fetch_json = original_fetch


if __name__ == "__main__":
    unittest.main()
