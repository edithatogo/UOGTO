import unittest
from urllib.error import HTTPError

from scripts.maintenance import check_zenodo_depositions


class TestZenodoDepositions(unittest.TestCase):
    def test_missing_token_is_nonfatal_pending_status(self):
        status = check_zenodo_depositions.build_account_status(token=None)
        self.assertEqual(status["schema"], "uogto.zenodo-account-status.v1")
        self.assertEqual(status["status"], "missing_token")
        self.assertIn("ZENODO_ACCESS_TOKEN", status["blockers"][0])

    def test_matches_deposition_by_title(self):
        def fake_fetcher(_token, api_base, timeout):
            return [
                {
                    "id": 10,
                    "state": "done",
                    "submitted": True,
                    "metadata": {
                        "title": "Universal Open Game Theory Ontology",
                        "doi": "10.5281/zenodo.12345",
                    },
                    "links": {"record": "https://zenodo.org/records/12345"},
                },
                {"id": 11, "metadata": {"title": "Other"}},
            ]

        status = check_zenodo_depositions.build_account_status(
            token="token", fetcher=fake_fetcher
        )
        self.assertEqual(status["status"], "uogto_deposition_found")
        self.assertEqual(status["uogto_depositions"][0]["doi"], "10.5281/zenodo.12345")
        self.assertEqual(
            status["uogto_depositions"][0]["record_url"],
            "https://zenodo.org/records/12345",
        )

    def test_matches_deposition_by_repository_related_identifier(self):
        deposition = {
            "metadata": {
                "title": "Other",
                "related_identifiers": [
                    {"identifier": "https://github.com/edithatogo/UOGTO"}
                ],
            }
        }
        self.assertTrue(check_zenodo_depositions.deposition_matches_uogto(deposition))

    def test_no_matching_deposition_is_reported(self):
        def fake_fetcher(_token, api_base, timeout):
            return [{"id": 1, "metadata": {"title": "Other"}}]

        status = check_zenodo_depositions.build_account_status(
            token="token", fetcher=fake_fetcher
        )
        self.assertEqual(status["status"], "no_uogto_deposition_found")
        self.assertEqual(status["uogto_depositions"], [])

    def test_rejected_token_is_structured_status(self):
        def fake_fetcher(_token, api_base, timeout):
            raise HTTPError("https://zenodo.org/api/deposit/depositions", 401, "Unauthorized", {}, None)

        status = check_zenodo_depositions.build_account_status(
            token="token", fetcher=fake_fetcher
        )
        self.assertEqual(status["status"], "invalid_or_rejected_token")
        self.assertIn("HTTP 401", status["blockers"][0])


if __name__ == "__main__":
    unittest.main()
