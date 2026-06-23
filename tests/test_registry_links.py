import os
import sys
import unittest
from unittest.mock import patch


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.maintenance import check_registry_links


class TestRegistryLinks(unittest.TestCase):
    def test_required_registry_urls_exist(self):
        text = check_registry_links.read_registry_text()
        urls = check_registry_links.check_required_urls(text)
        self.assertIn("https://github.com/edithatogo/UOGTO", urls)
        self.assertIn("https://creativecommons.org/licenses/by/4.0/", urls)
        self.assertIn(
            "https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/registry-handoff.json",
            urls,
        )
        self.assertIn("https://w3id.org/uogto/core#", urls)

    def test_no_pending_publication_markers_after_release(self):
        text = check_registry_links.read_registry_text()
        self.assertFalse(check_registry_links.has_pending_publication_markers(text))

    def test_rejects_missing_required_url(self):
        text = "\n".join(check_registry_links.REQUIRED_STABLE_URLS)
        with self.assertRaises(AssertionError):
            check_registry_links.check_required_urls(text)

    @patch("scripts.maintenance.check_registry_links.open_url", return_value=200)
    def test_live_check_can_skip_unpublished_urls(self, mock_open_url):
        urls = (
            check_registry_links.REQUIRED_STABLE_URLS
            | check_registry_links.REQUIRED_PUBLICATION_URLS
            | check_registry_links.REQUIRED_NAMESPACE_URLS
        )
        checked = check_registry_links.check_live_urls(urls, allow_unpublished=True)
        self.assertEqual(set(checked), urls)
        called_urls = {call.args[0] for call in mock_open_url.call_args_list}
        self.assertEqual(called_urls, check_registry_links.REQUIRED_STABLE_URLS)

    @patch("scripts.maintenance.check_registry_links.open_url", side_effect=[200, 404])
    def test_live_check_rejects_http_failure(self, _mock_open_url):
        with self.assertRaises(AssertionError):
            check_registry_links.check_live_urls(
                {
                    "https://creativecommons.org/licenses/by/4.0/",
                    "https://github.com/edithatogo/UOGTO",
                }
            )


if __name__ == "__main__":
    unittest.main()
