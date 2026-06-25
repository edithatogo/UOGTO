from pathlib import Path


def test_arxiv_preflight_workflow_runs_strict_gate() -> None:
    workflow = Path(".github/workflows/arxiv-preflight.yml").read_text(encoding="utf-8")
    for expected in [
        "name: arXiv Preflight",
        "actions/checkout@v7",
        "actions/setup-python@v6",
        "pip install git+https://github.com/edithatogo/sourceright.git",
        "latexmk",
        "texlive-latex-base",
        "pytest tests/test_arxiv_source_package.py",
        "make arxiv-preflight",
    ]:
        assert expected in workflow
