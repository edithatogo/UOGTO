from __future__ import annotations

import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRIAGE_PATH = ROOT / "docs" / "registry" / "publication-follow-up-triage.json"


def load_triage() -> dict:
    return json.loads(TRIAGE_PATH.read_text(encoding="utf-8"))


def test_publication_follow_up_triage_has_required_fields() -> None:
    triage = load_triage()
    assert triage["schema"] == "uogto.publication-follow-up-triage.v1"
    date.fromisoformat(triage["last_verified"])
    assert triage["verification_summary"]["publication_status_live"] == "published"
    assert triage["verification_summary"]["w3id_redirects_live"] is True
    assert triage["verification_summary"]["prefix_cc_mappings_live"] is True

    required = {
        "id",
        "registry",
        "status",
        "classification",
        "owner",
        "external_owner",
        "target_artifact",
        "evidence_url",
        "latest_observation",
        "acceptance_criterion",
        "next_action",
    }
    for item in triage["items"]:
        assert required <= item.keys()
        assert item["owner"] == "UOGTO maintainer"
        assert (ROOT / item["target_artifact"]).exists()
        assert item["evidence_url"].startswith("https://")
        assert item["acceptance_criterion"].endswith(".")


def test_publication_follow_up_triage_records_current_external_feedback() -> None:
    items = {item["id"]: item for item in load_triage()["items"]}
    assert items["ols-indexing-1305"]["status"] == "accepted_pending_indexing"
    assert "will add the ontology" in items["ols-indexing-1305"]["latest_observation"]
    assert items["bioregistry-prefix-1999"]["status"] == "maintainer_feedback_needs_response"
    assert "two-namespace design" in items["bioregistry-prefix-1999"]["acceptance_criterion"]
    assert "do not invent ORCID" in items["bioregistry-prefix-1999"]["next_action"]
