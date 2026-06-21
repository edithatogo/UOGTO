import unittest
from unittest import mock

from scripts.maintenance import check_w3id_status


class TestW3idStatus(unittest.TestCase):
    def test_local_state_tracks_pending_merge_and_pr_url(self):
        packet = check_w3id_status.check_local_w3id_state()
        self.assertEqual(packet["status"], "pending_external_w3id_merge")
        self.assertEqual(packet["w3id_pull_request_url"], "https://github.com/perma-id/w3id.org/pull/6238")

    def test_require_merged_rejects_open_pr(self):
        with mock.patch.object(
            check_w3id_status,
            "fetch_json",
            return_value={"state": "open", "merged": False},
        ):
            with self.assertRaisesRegex(AssertionError, "not merged yet"):
                check_w3id_status.check_pr_state(require_merged=True)

    def test_require_live_rejects_non_uogto_redirect_target(self):
        with mock.patch.object(
            check_w3id_status,
            "fetch_redirect",
            return_value=check_w3id_status.RedirectCheck(
                source="https://w3id.org/uogto/core",
                final_url="https://w3id.org/uogto/core",
                status=404,
            ),
        ):
            with self.assertRaisesRegex(AssertionError, "not live yet"):
                check_w3id_status.check_redirects(require_live=True)


if __name__ == "__main__":
    unittest.main()
