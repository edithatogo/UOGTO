"""Bounded GTO source evidence checks: never promote an abstract to formal source."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/research/gto-predecessor-evidence-20261118.json"


def load_record():
    return json.loads(EVIDENCE.read_text(encoding="utf-8"))


def validate_record(record):
    assert record["schema"] == "uogto.gto-predecessor-evidence.v1"
    assert record["as_of_date"] == "2026-11-18"
    original = record["original_2013"]
    assert original["source_id"] == "mejbri_gto"
    assert original["title"] == "A Domain Ontology of Game Theory Applied to Game Based Learning"
    assert original["year"] == 2013
    assert original["page_start"] == 666
    assert original["conference"] == "7th European Conference on Games Based Learning"
    assert original["abstract_authors"] == ["Yemna Mejbri", "Maha Khemaja", "Rafik Braham"]
    assert original["toc_authors"] != original["abstract_authors"]
    assert original["author_discrepancy_unresolved"] is True
    assert original["doi"] is None
    followup = record["2018_followup"]
    assert followup["doi"] == "10.4108/eai.4-1-2018.153533"
    assert followup["full_paper_text_inspected"] is True
    assert followup["journal_article_licence"] == "CC-BY-3.0"
    assert followup["licence_does_not_transfer_to_2013_or_ontology"] is True
    assert record["evidence_state"] == {
        "2013_toc_verified": True,
        "2013_abstract_inspected": True,
        "2013_full_paper_bytes_acquired": False,
        "2013_full_text_charted": False,
        "standalone_gto_artifact_acquired": False,
        "source_content_hash_verified": False,
        "gto_rdf_parsed": False,
        "gto_iri_mapping_reviewed": False,
        "gto_adapter_executed": False,
        "source_licence_certified": False,
    }
    rights = record["2013_rights"]
    assert rights["declared_proceedings_status"] == "all-rights-reserved"
    assert rights["ontology_rights"] == "unverified"
    assert rights["paper_or_ontology_bytes_redistributed"] is False
    assert record["claims"][0]["source_ids"] == [
        "proceedings-2013-toc", "ecgbl-2013-abstract"
    ]
    assert len(record["acquisition_leads"]) >= 3
    assert record["closure"]["ocs02_complete"] is False
    assert record["closure"]["broad_discovery_complete"] is False
    assert record["closure"]["proposed_ontology_mapping_accepted"] is False
    for source in record["sources"]:
        assert source["url"].startswith("https://")
        assert source["observed_part"]
        assert source["asserted_access"] in {
            "toc_inspected", "abstract_inspected", "publisher_full_text_inspected"
        }
    assert len({s["source_id"] for s in record["sources"]}) == len(record["sources"])


def test_original_source_is_a_limited_evidence_receipt():
    validate_record(load_record())


def test_source_status_cannot_be_upgraded_from_abstract_only():
    record = load_record()
    for key in (
        "2013_full_paper_bytes_acquired", "2013_full_text_charted",
        "standalone_gto_artifact_acquired", "source_content_hash_verified",
        "gto_rdf_parsed", "gto_iri_mapping_reviewed", "gto_adapter_executed",
        "source_licence_certified",
    ):
        changed = copy.deepcopy(record)
        changed["evidence_state"][key] = True
        with pytest.raises(AssertionError):
            validate_record(changed)


def test_discrepancy_and_rights_holds_are_not_silently_removed():
    record = load_record()
    changed = copy.deepcopy(record)
    changed["original_2013"]["author_discrepancy_unresolved"] = False
    with pytest.raises(AssertionError):
        validate_record(changed)
    changed = copy.deepcopy(record)
    changed["2013_rights"]["ontology_rights"] = "CC-BY-3.0"
    with pytest.raises(AssertionError):
        validate_record(changed)
    changed = copy.deepcopy(record)
    changed["closure"]["ocs02_complete"] = True
    with pytest.raises(AssertionError):
        validate_record(changed)


def test_evidence_links_are_not_missing_and_sources_are_distinct():
    record = load_record()
    changed = copy.deepcopy(record)
    changed["sources"][1]["source_id"] = changed["sources"][0]["source_id"]
    with pytest.raises(AssertionError):
        validate_record(changed)
