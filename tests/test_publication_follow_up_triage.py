from __future__ import annotations

import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRIAGE_PATH = ROOT / "docs" / "registry" / "publication-follow-up-triage.json"
BIOREGISTRY_DECISION_PATH = ROOT / "docs" / "registry" / "bioregistry-namespace-response.md"


def load_triage() -> dict:
    return json.loads(TRIAGE_PATH.read_text(encoding="utf-8"))


def test_publication_follow_up_triage_has_required_fields() -> None:
    triage = load_triage()
    assert triage["schema"] == "uogto.publication-follow-up-triage.v1"
    date.fromisoformat(triage["last_verified"])
    assert triage["verification_summary"]["publication_status_live"] == "published"
    assert triage["verification_summary"]["w3id_redirects_live"] is True
    assert triage["verification_summary"]["prefix_cc_mappings_live"] is True
    assert (
        triage["verification_summary"]["cross_registry_supplements"]["lov"]
        == "https://github.com/pyvandenbussche/lov/issues/83#issuecomment-4902620021"
    )
    assert "health economics" in triage["learned_metadata_bundle"]["health_relevance"]

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
    assert items["ols-indexing-1305"]["supplement_comment_url"].endswith("4902620274")
    assert items["lov-review-83"]["supplement_comment_url"].endswith("4902620021")
    assert (
        items["ontobee-indexing-212"]["target_artifact"]
        == "docs/registry/extended-discoverability-submissions.md"
    )
    assert items["ontobee-indexing-212"]["supplement_comment_url"].endswith("4902620502")
    assert items["bioregistry-prefix-1999"]["status"] == "orcid_added_awaiting_maintainer_review"
    assert (
        items["bioregistry-prefix-1999"]["target_artifact"]
        == "docs/registry/bioregistry-namespace-response.md"
    )
    assert "primary core prefix" in items["bioregistry-prefix-1999"]["namespace_decision"]
    assert "https://orcid.org/0000-0002-9775-0603" in items["bioregistry-prefix-1999"]["orcid_handling"]
    assert "issuecomment-4885988980" in items["bioregistry-prefix-1999"]["evidence_url"]
    assert "squashed-namespace compatibility decision" in items["bioregistry-prefix-1999"]["acceptance_criterion"]


def test_bioregistry_namespace_response_decision_is_recorded() -> None:
    decision = BIOREGISTRY_DECISION_PATH.read_text(encoding="utf-8")

    assert "https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4885550451" in decision
    assert "https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4885988980" in decision
    assert "Retain the published UOGTO `v1.0.0` two-namespace design" in decision
    assert "https://w3id.org/uogto/core#$1" in decision
    assert "https://orcid.org/0000-0002-9775-0603" in decision
    assert "ontology-compatibility Conductor track" in decision
