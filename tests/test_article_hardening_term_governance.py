from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "docs" / "article-hardening" / "deprecation-policy.md"
CHANGELOG_PATH = ROOT / "docs" / "article-hardening" / "term-changelog.md"


def test_deprecation_policy_covers_required_event_types() -> None:
    policy = POLICY_PATH.read_text(encoding="utf-8")
    for phrase in [
        "new term",
        "changed definition",
        "deprecated term",
        "replacement IRI",
        "migration note",
    ]:
        assert phrase in policy


def test_term_changelog_has_required_columns() -> None:
    changelog = CHANGELOG_PATH.read_text(encoding="utf-8")
    for phrase in [
        "new term",
        "changed definition",
        "deprecated term",
        "replacement IRI",
        "migration note",
        "Term-Level Changelog",
    ]:
        assert phrase in changelog
