from pathlib import Path

import pytest

from scripts.maintenance import check_article_hardening_protocol as checker


ROOT = Path(__file__).resolve().parents[1]


def test_protocol_scaffold_contains_required_reporting_sections():
    protocol = (ROOT / "docs" / "article-hardening" / "protocol.md").read_text(
        encoding="utf-8"
    )
    for section in checker.PROTOCOL_SECTIONS:
        assert section in protocol


def test_search_strategy_declares_prisma_s_fields_and_route_taxonomy():
    strategy = (ROOT / "docs" / "article-hardening" / "search-strategy.md").read_text(
        encoding="utf-8"
    )
    for field in checker.SEARCH_FIELDS:
        assert f"`{field}`" in strategy
    for route in [
        "ontology_registry",
        "scholarly_index",
        "archive",
        "repository",
        "standards_body",
        "project_site",
        "web_search",
        "baseline_artifact",
    ]:
        assert f"`{route}`" in strategy


def test_protocol_check_script_passes_for_repo_artifacts(capsys):
    checker.main()
    captured = capsys.readouterr()
    assert "Article-hardening protocol valid" in captured.out


def test_protocol_check_fails_when_required_file_is_missing(monkeypatch):
    monkeypatch.setattr(checker, "DOCS", ROOT / "__missing_article_hardening__")
    with pytest.raises(SystemExit, match="Missing required article-hardening artifact"):
        checker.main()


def test_review_agent_registry_declares_required_review_roles():
    import json

    registry = json.loads((ROOT / "conductor" / "agents" / "article-hardening-review-agents.json").read_text(encoding="utf-8"))
    role_ids = {role["id"] for role in registry["review_roles"]}
    for role in checker.REQUIRED_REVIEWERS + checker.OPTIONAL_PHASE_REVIEWERS:
        assert role in role_ids
    for role in checker.REQUIRED_REVIEWERS:
        assert role in registry["minimum_phase_review_set"]


def test_review_workflow_and_skill_are_present_and_role_aware():
    workflow = (ROOT / "conductor" / "workflows" / "article-hardening-phase-review.md").read_text(encoding="utf-8")
    skill = (ROOT / ".agents" / "skills" / "article-hardening-review" / "SKILL.md").read_text(encoding="utf-8")
    for role in checker.REQUIRED_REVIEWERS:
        assert role in workflow
        assert role in skill
    assert "phase-review-log.jsonl" in workflow
    assert "red-team" in workflow
    assert "devil" in workflow


def test_research_agent_registry_declares_required_research_roles():
    import json

    registry = json.loads(
        (ROOT / "conductor" / "agents" / "article-hardening-research-agents.json").read_text(
            encoding="utf-8"
        )
    )
    role_ids = {role["id"] for role in registry["research_roles"]}
    for role in checker.REQUIRED_RESEARCHERS + checker.OPTIONAL_PHASE_RESEARCHERS:
        assert role in role_ids
    for role in checker.REQUIRED_RESEARCHERS:
        assert role in registry["minimum_phase_research_set"]


def test_research_workflow_and_skill_are_present_and_role_aware():
    workflow = (
        ROOT / "conductor" / "workflows" / "article-hardening-research-workflow.md"
    ).read_text(encoding="utf-8")
    skill = (
        ROOT / ".agents" / "skills" / "article-hardening-research" / "SKILL.md"
    ).read_text(encoding="utf-8")
    for role in checker.REQUIRED_RESEARCHERS:
        assert role in workflow
        assert role in skill
    assert "phase-research-log.jsonl" in workflow
    assert "evidence" in workflow
    assert "reproducibility" in workflow
