from pathlib import Path

from scripts.maintenance.score_arxiv_submission import CATEGORIES, score_submission


def test_arxiv_strict_review_score_passes_threshold() -> None:
    report = score_submission()

    assert report["schema"] == "uogto.arxiv-strict-review-score.v1"
    assert report["max_score"] == 1000
    assert report["raw_max_score"] == 1100
    assert report["score"] > 995
    assert report["status"] == "pass"
    assert report["blockers"] == []
    assert report["min_category_percent"] >= 98.0
    assert len(report["categories"]) == len(CATEGORIES)


def test_arxiv_strict_review_artifacts_are_written() -> None:
    for path in [
        "docs/paper/arxiv-strict-review-rubric.md",
        "docs/paper/arxiv-strict-review-report.md",
        "docs/paper/arxiv-strict-review-iterations.jsonl",
    ]:
        assert Path(path).exists()

    report = Path("docs/paper/arxiv-strict-review-report.md").read_text(encoding="utf-8")
    assert "Score: `998.18/1000`" in report
    assert "Blockers" in report
    assert "- None." in report


def test_required_gate_runs_validation_and_strict_arxiv_score() -> None:
    workflow = Path(".github/workflows/required-gate.yml").read_text(encoding="utf-8")
    for expected in [
        "name: Required Gate",
        "make validate",
        "make test",
        "make publishing-metadata",
        "make registry-links",
        "make manuscript-pdf",
        'make arxiv-upload-ready ARXIV_PDF_FLAGS="--require-pdf --require-arxiv-engine"',
        "scripts/maintenance/score_arxiv_submission.py",
        "--threshold 995",
        "actions/upload-artifact@v4",
    ]:
        assert expected in workflow


def test_arxiv_process_documents_metadata_and_external_steps() -> None:
    process = Path("docs/paper/arxiv-submission-process.md").read_text(encoding="utf-8")
    for expected in [
        "Submission Metadata",
        "Primary category",
        "cs.AI",
        "self-submit",
        "registered arXiv author",
        "irrevocable license",
        "ASCII",
        "Replacement and Rollback Notes",
    ]:
        assert expected in process
