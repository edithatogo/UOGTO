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
