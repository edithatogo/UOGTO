import unittest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.review.deduplicate import deduplicate
from scripts.review.active_screening import score_abstract
from scripts.review.snowball import fetch_citations

class TestScopingExecution(unittest.TestCase):
    def test_deduplicate(self):
        records = [
            {"doi": "10.1", "title": "First Work"},
            {"doi": "10.1", "title": "First Work (duplicate)"},
            {"doi": "10.2", "title": "First Work"}, 
            {"doi": "10.3", "title": "Unique Work"}
        ]
        res = deduplicate(records)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]["doi"], "10.1")
        self.assertEqual(res[1]["doi"], "10.3")

    def test_score_abstract(self):
        score, matches = score_abstract("Prisoner's Dilemma study", "We analyze the payoff matrix and Nash equilibrium.")
        self.assertGreater(score, 0)
        self.assertIn("normal_form", matches)

    @patch('scripts.review.snowball.fetch_url')
    def test_snowball(self, mock_fetch_url):
        mock_fetch_url.side_effect = [
            b'{"referenced_works": ["https://openalex.org/W_ref1"]}',
            b'{"id": "W_ref1", "title": "Referenced Paper", "publication_year": 2020, "authorships": []}'
        ]
        res = fetch_citations("https://openalex.org/W_seed", limit=1)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["title"], "Referenced Paper")
