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

    def test_manuscript_pdf_workflow_runs_strict_gate(self):
        workflow = Path('.github/workflows/manuscript-pdf.yml').read_text(encoding='utf-8')
        for expected in [
            'name: Build Manuscript PDF',
            'actions/checkout@v7',
            'actions/setup-python@v6',
            'latexmk',
            'texlive-latex-base',
            'make manuscript-pdf',
        ]:
            self.assertIn(expected, workflow)

    def test_build_check_fails_without_engine_when_pdf_required(self):
        self.write_valid_paper()
        with mock.patch("scripts.maintenance.build_manuscript_pdf.find_latex_engine", return_value=None):
            result = build_manuscript_pdf.build_manuscript(
                self.paper,
                self.temp_dir / "out",
                require_pdf=True,
            )
        self.assertFalse(result["ok"])

    def test_find_latex_engine_uses_bundled_tectonic_fallback(self):
        bundled = self.temp_dir / "tectonic.exe"
        bundled.write_text("", encoding="utf-8")
        with mock.patch("scripts.maintenance.build_manuscript_pdf.shutil.which", return_value=None):
            with mock.patch(
                "scripts.maintenance.build_manuscript_pdf.bundled_tectonic_candidates",
                return_value=[bundled],
            ):
                self.assertEqual(build_manuscript_pdf.find_latex_engine(), str(bundled))

    def test_build_check_rejects_tectonic_for_strict_arxiv_engine(self):
        self.write_valid_paper()
        with mock.patch(
            "scripts.maintenance.build_manuscript_pdf.find_latex_engine",
            return_value=r"C:\tools\tectonic.exe",
        ):
            result = build_manuscript_pdf.build_manuscript(
                self.paper,
                self.temp_dir / "out",
                require_pdf=True,
                require_arxiv_engine=True,
            )
        self.assertFalse(result["ok"])
        self.assertIn("arXiv-compatible PDF engine required", result["skipped"])

    def test_blocking_build_warnings_detect_unresolved_references(self):
        warnings = build_manuscript_pdf.blocking_build_warnings(
            "LaTeX Warning: Reference `fig:architecture' on page 2 undefined on input line 50.\n"
            "LaTeX Warning: There were undefined references.\n"
        )
        self.assertTrue(any("fig:architecture" in warning for warning in warnings))
        self.assertTrue(any("undefined references" in warning for warning in warnings))

    def test_build_prefers_final_log_for_blocking_warnings(self):
        self.write_valid_paper()
        output_dir = self.temp_dir / "out"

        completed = mock.Mock()
        completed.returncode = 0
        completed.stdout = (
            "LaTeX Warning: Reference `tab:module-audit' on page 7 undefined\n"
            "There were undefined references\n"
        )
        completed.stderr = ""

        def fake_run(*_args, **_kwargs):
            output_dir.mkdir(parents=True, exist_ok=True)
            (output_dir / "paper.pdf").write_bytes(b"%PDF-1.4\n")
            (output_dir / "paper.log").write_text("Final resolved LaTeX log\n", encoding="utf-8")
            return completed

        with mock.patch("scripts.maintenance.build_manuscript_pdf.find_latex_engine", return_value="latexmk"):
            with mock.patch("scripts.maintenance.build_manuscript_pdf.subprocess.run", side_effect=fake_run):
                result = build_manuscript_pdf.build_manuscript(self.paper, output_dir, require_pdf=True)

        self.assertTrue(result["ok"])
        self.assertEqual(result["blocking_warnings"], [])


if __name__ == "__main__":
    unittest.main()
