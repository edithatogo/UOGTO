from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATTERNS = ROOT / "docs" / "ontology-design-patterns.md"


def test_ontology_design_patterns_cover_core_modeling_concepts() -> None:
    text = PATTERNS.read_text(encoding="utf-8")
    for phrase in [
        "Game Pattern",
        "Session Pattern",
        "Trace Pattern",
        "Strategy and Action Pattern",
        "Payoff and Outcome Pattern",
        "Mechanism Pattern",
        "Execution Binding Pattern",
        "Mapping Pattern",
        "uogto:GameSpecification",
        "uogto:PlaySession",
        "uogto:EventTrace",
        "uogto:StrategyProfile",
        "uogto:ActionProfile",
        "uogto:PayoffProfile",
        "uogto:ExecutionModel",
    ]:
        assert phrase in text

