import unittest
from unittest.mock import patch, mock_open
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.maintenance.generate_changelog import parse_commits, generate_entry, update_changelog

class TestGenerateChangelog(unittest.TestCase):
    def test_parse_commits(self):
        mock_commits = [
            "abc1234|feat: add new cooperative game module",
            "def5678|fix: resolve parsing issue in ttl parser",
            "ghi9012|docs: update product description",
            "jkl3456|chore: run validation check",
            "mno7890|style: fix whitespaces"
        ]
        categories = parse_commits(mock_commits)
        self.assertEqual(len(categories["Features"]), 1)
        self.assertEqual(len(categories["Bug Fixes"]), 1)
        self.assertEqual(len(categories["Documentation"]), 1)
        self.assertEqual(len(categories["Chores & Maintenance"]), 1)
        self.assertIn("abc1234", categories["Features"][0])

    def test_generate_entry_empty(self):
        categories = {
            "Features": [],
            "Bug Fixes": [],
            "Documentation": [],
            "Chores & Maintenance": []
        }
        entry = generate_entry(categories)
        self.assertEqual("", entry)

    @patch("builtins.open", new_callable=mock_open, read_data="# Changelog\n\nOld entries")
    @patch("os.path.exists", return_value=True)
    def test_update_changelog_skips_empty_entry(self, mock_exists, mock_file):
        update_changelog("")
        mock_file.assert_not_called()

    @patch("builtins.open", new_callable=mock_open, read_data="# Changelog\n\nOld entries")
    @patch("os.path.exists", return_value=True)
    def test_update_changelog(self, mock_exists, mock_file):
        new_entry = "## [2026-06-21]\n- feat: new stuff\n\n"
        update_changelog(new_entry)
        mock_file().write.assert_called_once()
        written = mock_file().write.call_args[0][0]
        self.assertTrue(written.startswith("# Changelog\n\n## [2026-06-21]"))
