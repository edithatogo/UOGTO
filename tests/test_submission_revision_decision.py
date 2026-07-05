import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_submission_revision_memo_records_target_path_and_external_limits() -> None:
    memo = read("docs/paper/submission-revision-decision-memo.md")

    for expected in [
        "Complete the arXiv preprint path first",
        "Nature Human Behaviour",
        "Resource-style submission",
        "Medical Decision Making",
        "arXiv identifier: not assigned",
        "arXiv-rendered PDF: not inspected",
        "Do not fabricate arXiv, publisher, reviewer, or acceptance evidence",
        "https://info.arxiv.org/help/faq/texlive.html",
        "https://www.nature.com/nathumbehav/content",
        "https://www.journals.smdm.org/manuscript-types/",
    ]:
        assert expected in memo


def test_submission_revision_backlog_has_acceptance_criteria() -> None:
    rows = list(csv.DictReader((ROOT / "docs/paper/submission-revision-backlog.csv").open(encoding="utf-8")))

    assert rows
    assert {row["priority"] for row in rows} >= {"must-fix", "should-fix", "stretch", "watch"}
    assert any(row["status"] == "external_blocker" for row in rows)
    for row in rows:
        assert row["item_id"].startswith("SRB-")
        assert row["recommendation"]
        assert row["acceptance_criterion"]
        assert row["source_evidence"]


def test_arxiv_submission_state_keeps_identifier_and_pdf_approval_external() -> None:
    state = read("docs/paper/arxiv-submission-state.md")
    process = read("docs/paper/arxiv-submission-process.md")
    contract = read("docs/paper/arxiv-submission-contract.md")

    for expected in [
        "Submission state | `not_submitted`",
        "arXiv identifier | `not assigned`",
        "arXiv-rendered PDF inspected | `no`",
        "pending the successful clean CI arXiv Preflight artifact",
        "identifier assignment and rendered-PDF inspection require an external",
    ]:
        assert expected in state

    assert "docs/paper/arxiv-submission-state.md" in process
    assert "docs/paper/arxiv-submission-state.md" in contract
