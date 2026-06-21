import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.maintenance.check_github import get_via_gh, get_via_api, write_summary

import os

class TestCheckGithub(unittest.TestCase):
    @patch('scripts.maintenance.check_github.run_cmd')
    def test_get_via_gh(self, mock_run_cmd):
        mock_run_cmd.side_effect = [
            "Authenticated", 
            '[{"number": 1, "title": "Test Issue", "state": "open", "url": "http://x", "updatedAt": "now"}]', 
            '[{"number": 2, "title": "Test PR", "state": "open", "url": "http://y", "updatedAt": "now"}]' 
        ]
        issues, prs = get_via_gh()
        self.assertIsNotNone(issues)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["title"], "Test Issue")
        self.assertEqual(prs[0]["title"], "Test PR")

    @patch('urllib.request.urlopen')
    def test_get_via_api(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b'''[
            {"number": 1, "title": "API Issue", "state": "open", "html_url": "http://x", "updated_at": "now"},
            {"number": 2, "title": "API PR", "state": "open", "html_url": "http://y", "updated_at": "now", "pull_request": {}}
        ]'''
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        issues, prs = get_via_api()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["title"], "API Issue")
        self.assertEqual(len(prs), 1)
        self.assertEqual(prs[0]["title"], "API PR")

    def test_write_summary(self):
        issues = [{"number": 1, "title": "A", "url": "u1", "updatedAt": "t1"}]
        prs = [{"number": 2, "title": "B", "url": "u2", "updatedAt": "t2"}]
        
        with patch('scripts.maintenance.check_github.OUTPUT_FILE', 'conductor/test_remote_status.md'):
            write_summary(issues, prs)
            self.assertTrue(os.path.exists('conductor/test_remote_status.md'))
            with open('conductor/test_remote_status.md', 'r') as f:
                content = f.read()
                self.assertIn("A", content)
                self.assertIn("B", content)
            os.remove('conductor/test_remote_status.md')
