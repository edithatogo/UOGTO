import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.review.query_databases import query_openalex, query_europepmc, query_arxiv, query_crossref

class TestQueryDatabases(unittest.TestCase):
    @patch('scripts.review.query_databases.fetch_url')
    def test_query_openalex(self, mock_fetch_url):
        mock_fetch_url.return_value = b'''{
            "results": [
                {
                    "id": "https://openalex.org/W1",
                    "doi": "https://doi.org/1",
                    "title": "OpenAlex Test Work",
                    "publication_year": 2026,
                    "authorships": [{"author": {"display_name": "Author A"}}]
                }
            ]
        }'''
        results = query_openalex("test", limit=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "OpenAlex Test Work")
        self.assertEqual(results[0]["source"], "openalex")

    @patch('scripts.review.query_databases.fetch_url')
    def test_query_europepmc(self, mock_fetch_url):
        mock_fetch_url.return_value = b'''{
            "resultList": {
                "result": [
                    {
                        "id": "PMC1",
                        "doi": "10.1",
                        "title": "PMC Test Work",
                        "pubYear": "2026",
                        "authorList": {"author": [{"fullName": "Author B"}]}
                    }
                ]
            }
        }'''
        results = query_europepmc("test", limit=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "PMC Test Work")

    @patch('scripts.review.query_databases.fetch_url')
    def test_query_arxiv(self, mock_fetch_url):
        mock_fetch_url.return_value = b'''<?xml version="1.0" encoding="utf-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
            <entry>
                <id>http://arxiv.org/abs/1</id>
                <title>arXiv Test Work</title>
                <summary>Abstract test summary</summary>
                <published>2026-06-21T00:00:00Z</published>
                <author><name>Author C</name></author>
            </entry>
        </feed>'''
        results = query_arxiv("test", limit=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "arXiv Test Work")

    @patch('scripts.review.query_databases.fetch_url')
    def test_query_crossref(self, mock_fetch_url):
        mock_fetch_url.return_value = b'''{
            "message": {
                "items": [
                    {
                        "DOI": "10.2",
                        "title": ["Crossref Test Work"],
                        "published-print": {"date-parts": [[2026]]},
                        "author": [{"given": "Given", "family": "Family"}]
                    }
                ]
            }
        }'''
        results = query_crossref("test", limit=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Crossref Test Work")
