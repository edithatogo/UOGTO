"""Proof limits for a newly discovered game-ontology comparator."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

RECEIPT = Path(__file__).resolve().parents[1] / "docs/research/ontouml-value-risk-candidate-20261118.json"


def check_receipt(record):
    assert record["schema"] == "uogto.source-candidate.ontouml-value-risk.v1"
    assert record["as_of_date"] == "2026-11-18"
    assert record["candidate_id"] == "amaral2021-game-value-risk-ontouml"
    assert record["source_kind"] == "conceptual_game_ontology_publication"
    assert record["discovery"]["new_to_20261108_seed_register"] is True
    assert record["discovery"]["historical_seed_count_modified"] is False
    assert record["publication"]["year"] == 2021
    assert record["publication"]["doi"] == "10.1007/978-3-030-74196-9_5"
    assert record["publication"]["authors"] == [
        "Glenda Amaral", "Daniele Porello", "Tiago Prince Sales", "Giancarlo Guizzardi"
    ]
    assert record["evidence"] == {
        "institutional_metadata_verified": True,
        "author_pdf_content_inspected": True,
        "raw_pdf_bytes_hashed": False,
        "full_original_ontouml_model_acquired": False,
        "rdf_owl_serialization_acquired": False,
        "rdf_owl_parsed": False,
        "equivalence_mapping_accepted": False,
        "runtime_or_solver_executed": False,
        "licence_certified_for_redistribution": False,
        "independent_validation_completed": False,
    }
    assert record["rights"]["source_pdf_redistributed"] is False
    assert record["rights"]["source_pdf_licence"] == "not_verified"
    assert record["source_identifiers"]["author_pdf_url"].startswith("https://")
    assert record["source_identifiers"]["institutional_metadata_url"].startswith("https://")
    assert record["source_identifiers"]["content_sha256"] is None
    assert len(record["construct_comparisons"]) >= 5
    assert all(row["mapping_decision"] == "comparison_only_no_equivalence" for row in record["construct_comparisons"])
    assert len({row["construct_id"] for row in record["construct_comparisons"]}) == len(record["construct_comparisons"])
    assert all(row["source_locator"] and row["uogto_question"] for row in record["construct_comparisons"])
    assert record["closure"]["ocs09_complete"] is False
    assert record["closure"]["ocs11_complete"] is False
    assert record["closure"]["world_coverage_claim"] is False


def test_candidate_is_registered_without_unearned_status():
    check_receipt(json.loads(RECEIPT.read_text(encoding="utf-8")))


@pytest.mark.parametrize("flag", [
    "raw_pdf_bytes_hashed", "full_original_ontouml_model_acquired",
    "rdf_owl_serialization_acquired", "rdf_owl_parsed",
    "equivalence_mapping_accepted", "runtime_or_solver_executed",
    "licence_certified_for_redistribution", "independent_validation_completed",
])
def test_no_automatic_evidence_promotion(flag):
    record = json.loads(RECEIPT.read_text(encoding="utf-8"))
    bad = copy.deepcopy(record)
    bad["evidence"][flag] = True
    with pytest.raises(AssertionError):
        check_receipt(bad)


def test_unreviewed_mapping_is_not_an_accepted_equivalence():
    record = json.loads(RECEIPT.read_text(encoding="utf-8"))
    bad = copy.deepcopy(record)
    bad["construct_comparisons"][0]["mapping_decision"] = "owl:equivalentClass"
    with pytest.raises(AssertionError):
        check_receipt(bad)


def test_publication_2021_is_not_relabelled_as_a_2025_thesis():
    record = json.loads(RECEIPT.read_text(encoding="utf-8"))
    bad = copy.deepcopy(record)
    bad["publication"]["year"] = 2025
    with pytest.raises(AssertionError):
        check_receipt(bad)


def test_duplicate_construct_row_is_rejected():
    record = json.loads(RECEIPT.read_text(encoding="utf-8"))
    bad = copy.deepcopy(record)
    bad["construct_comparisons"][1]["construct_id"] = bad["construct_comparisons"][0]["construct_id"]
    with pytest.raises(AssertionError):
        check_receipt(bad)
