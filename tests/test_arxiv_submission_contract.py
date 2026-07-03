import json
from pathlib import Path


def test_arxiv_submission_agents_cover_editor_reviewer_and_publisher_roles() -> None:
    registry = json.loads(Path("conductor/agents/arxiv-submission-agents.json").read_text(encoding="utf-8"))

    assert registry["schema"] == "uogto.arxiv-submission-agents.v1"
    for group in ["editor_agents", "reviewer_agents", "publisher_agents"]:
        assert registry[group], f"{group} must not be empty"
        for agent in registry[group]:
            assert agent["id"]
            assert agent["skills"]
            assert agent["required_inputs"]
            assert agent["required_output"].startswith("docs/paper/arxiv-submission-contract.md")

    reviewer_ids = {agent["id"] for agent in registry["reviewer_agents"]}
    assert "red_team_reviewer" in reviewer_ids
    assert "devils_advocate_reviewer" in reviewer_ids

    assert registry["blocking_gate"]["local_command"] == "make arxiv-upload-ready"
    assert "make validate" in registry["blocking_gate"]["required_validation"]
    assert "make test" in registry["blocking_gate"]["required_validation"]


def test_arxiv_submission_contract_workflow_enforces_strict_gates() -> None:
    workflow = Path("conductor/workflows/arxiv-submission-contract-workflow.md").read_text(encoding="utf-8")
    contract = Path("docs/paper/arxiv-submission-contract.md").read_text(encoding="utf-8")

    for expected in [
        "editor agents",
        "reviewer agents",
        "publisher agents",
        "executed Codex agent run ids",
        "make arxiv-upload-ready",
        "make validate",
        "make test",
        "docs/paper/arxiv-source-privacy-audit.json",
        "SourceRight citation reconciliation reports 0 issues",
    ]:
        assert expected in workflow

    for expected in [
        "Editorial Contract",
        "Review Contract",
        "Publisher Contract",
        "Executed Codex Agent Runs",
        "Devil's Advocate Contract",
        "019f20ab-621a-70a3-9436-75b2744190bd",
        "019f20ab-9dd4-7e02-8556-03e3665876b7",
        "019f20ab-cbc4-7961-86f5-25c1753acaaf",
        "019f20ca-bbe7-7e93-831b-b906d7c50f63",
        "019f20c7-9208-7702-af6b-36d441a50041",
        "docs/paper/reviews/arxiv-red-team-review-2026-07-02.md",
        "docs/paper/reviews/arxiv-devils-advocate-review-2026-07-02.md",
        "make arxiv-upload-ready",
        "219 passed, 1 skipped, 21 warnings",
        "latest successful current-branch",
        "pass-attested",
        "pass-ci-strict",
        "dirty_entries: []",
        "pass-for-arxiv-upload",
        "docs/paper/arxiv-post-submission-record-template.md",
    ]:
        assert expected in contract
