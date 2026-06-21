import shutil
import sys
import unittest
import uuid
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.maintenance import build_manuscript_pdf


class TestManuscriptBuild(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_manuscript_build_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True)
        self.paper = self.temp_dir / "paper.tex"

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def write_valid_paper(self):
        self.paper.write_text(
            r"""\documentclass{article}
\begin{document}
\maketitle
\begin{thebibliography}{9}
\bibitem{alpha} Alpha.
\end{thebibliography}
\end{document}
""",
            encoding="utf-8",
        )

    def test_structure_check_reports_missing_tokens(self):
        self.paper.write_text(r"\begin{document}\end{document}", encoding="utf-8")
        issues = build_manuscript_pdf.check_tex_structure(self.paper)
        self.assertIn(r"missing required token: \documentclass", issues)

    def test_build_check_passes_without_engine_when_pdf_not_required(self):
        self.write_valid_paper()
        with mock.patch("scripts.maintenance.build_manuscript_pdf.find_latex_engine", return_value=None):
            result = build_manuscript_pdf.build_manuscript(self.paper, self.temp_dir / "out")
        self.assertTrue(result["ok"])
        self.assertFalse(result["compiled"])
        self.assertIn("No LaTeX engine found", result["skipped"])

    def test_build_check_fails_without_engine_when_pdf_required(self):
        self.write_valid_paper()
        with mock.patch("scripts.maintenance.build_manuscript_pdf.find_latex_engine", return_value=None):
            result = build_manuscript_pdf.build_manuscript(
                self.paper,
                self.temp_dir / "out",
                require_pdf=True,
            )
        self.assertFalse(result["ok"])


if __name__ == "__main__":
    unittest.main()
