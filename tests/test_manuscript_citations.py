import json
import shutil
import sys
import unittest
import uuid
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.maintenance import check_manuscript_citations


class TestManuscriptCitations(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_manuscript_citations_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True)
        self.paper = self.temp_dir / "paper.tex"
        self.csl = self.temp_dir / "references.csl.json"

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def write_files(self, tex: str, ids: list[str]):
        self.paper.write_text(tex, encoding="utf-8")
        self.csl.write_text(
            json.dumps([{"id": id_, "type": "webpage", "title": id_} for id_ in ids]),
            encoding="utf-8",
        )

    def test_check_citations_passes_when_latex_csl_and_bibitems_match(self):
        self.write_files(
            r"\cite{alpha,beta}\bibitem{alpha} A\bibitem{beta} B",
            ["alpha", "beta"],
        )
        result = check_manuscript_citations.check_citations(self.paper, self.csl)
        self.assertEqual(result["missing_from_csl"], [])
        self.assertEqual(result["missing_bibitems"], [])
        self.assertEqual(result["uncited_csl_references"], [])

    def test_check_citations_reports_drift(self):
        self.write_files(r"\cite{alpha}\bibitem{beta} B", ["gamma"])
        result = check_manuscript_citations.check_citations(self.paper, self.csl)
        self.assertEqual(result["missing_from_csl"], ["alpha"])
        self.assertEqual(result["missing_bibitems"], ["alpha"])
        self.assertEqual(result["uncited_csl_references"], ["gamma"])
        self.assertEqual(result["uncited_bibitems"], ["beta"])


if __name__ == "__main__":
    unittest.main()
