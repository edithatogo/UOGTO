import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_registry_enrichment_decisions_are_fail_closed() -> None:
    data = json.loads((ROOT / "docs/registry/registry-enrichment-decision.json").read_text())
    assert data["schema"] == "uogto.registry-enrichment-decision.v1"
    assert data["fairsharing"]["status"] == "awaiting_curator_review"
    assert all(item["decision"].startswith("deferred") for item in data["fairsharing"]["candidates"])
    assert all(item["decision"] == "deferred" or item["decision"].startswith("deferred") for item in data["wikidata"]["candidates"])


def test_namespace_compatibility_preserves_published_contract() -> None:
    decision = (ROOT / "docs/registry/namespace-compatibility-decision.md").read_text()
    assert "https://w3id.org/uogto/core#" in decision
    assert "https://w3id.org/uogto/extensions#" in decision
    assert "Reject for v1.0.0" in decision


def test_biomedical_positioning_does_not_claim_automatic_eligibility() -> None:
    decision = (ROOT / "docs/registry/biomedical-registry-positioning.md").read_text()
    assert "Defer" in decision
    assert "not automatic eligibility" in decision
    assert "No BioPortal or OBO Foundry submission" in decision
