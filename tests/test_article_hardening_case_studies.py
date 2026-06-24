from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "docs" / "article-hardening" / "case-studies.json"
MARKDOWN_PATH = ROOT / "docs" / "article-hardening" / "case-studies.md"


def test_case_study_register_has_expected_cases() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    case_ids = [case["case_id"] for case in payload["cases"]]

    assert payload["version"] == "1.0"
    assert len(case_ids) == 8
    assert case_ids == [
        "auction-mechanism-design",
        "voting-social-choice",
        "security-stackelberg",
        "marl-markov-game",
        "abm-policy-simulation",
        "system-dynamics-feedback",
        "llm-agent-tool-use",
        "executable-trace-provenance",
    ]


def test_case_study_markdown_mentions_all_cases() -> None:
    markdown = MARKDOWN_PATH.read_text(encoding="utf-8")
    for phrase in [
        "Auction and mechanism design",
        "Voting and social choice",
        "Security and Stackelberg games",
        "Multi-agent reinforcement learning and Markov games",
        "Agent-based policy simulation",
        "System-dynamics feedback game",
        "LLM-agent and tool-use game",
        "Executable trace and provenance",
    ]:
        assert phrase in markdown
