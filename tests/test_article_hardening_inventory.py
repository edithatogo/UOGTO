import copy
from pathlib import Path

import pytest

from scripts.maintenance import build_article_hardening_inventory as inventory


ROOT = Path(__file__).resolve().parents[1]


def test_article_hardening_register_outputs_validate():
    summary = inventory.check_outputs(
        ROOT / "docs" / "article-hardening" / "search-log.jsonl",
        ROOT / "docs" / "article-hardening" / "source-extension-inventory.json",
    )
    assert summary["source_count"] >= 39
    assert summary["baseline_count"] == 21
    assert summary["new_candidate_count"] >= 18
    assert summary["search_record_count"] >= 6


def test_search_log_is_hash_chained_and_has_required_evidence_fields():
    records = inventory.read_jsonl(ROOT / "docs" / "article-hardening" / "search-log.jsonl")
    inventory.validate_search_log(records)
    previous = None
    for record in records:
        assert record["previous_record_hash"] == previous
        assert record["query"]
        assert record["result_count"] is not None
        assert record["evidence_level"]
        assert record["inclusion_rationale"]
        assert record["licence"]
        assert record["reviewer_handoff"]["assigned_roles"]
        previous = record["record_hash"]


def test_source_inventory_records_licence_rationale_and_handoff():
    data = inventory.read_json(ROOT / "docs" / "article-hardening" / "source-extension-inventory.json")
    sssom = next(source for source in data["sources"] if source["source_id"] == "sssom")
    assert sssom["licence"]["disposition"]
    assert "SSSOM" in sssom["source_name"]
    assert sssom["inclusion_rationale"]
    assert sssom["reviewer_handoff"]["assigned_roles"]
    assert sssom["baseline_status"] == "new_candidate"


def test_inventory_validation_rejects_modified_source_hash():
    data = inventory.read_json(ROOT / "docs" / "article-hardening" / "source-extension-inventory.json")
    records = inventory.read_jsonl(ROOT / "docs" / "article-hardening" / "search-log.jsonl")
    modified = copy.deepcopy(data)
    modified["sources"][0]["inclusion_rationale"] = "silently changed"
    with pytest.raises(AssertionError, match="invalid source_hash"):
        inventory.validate_inventory(modified, records)


def test_search_log_validation_rejects_broken_hash_chain():
    records = inventory.read_jsonl(ROOT / "docs" / "article-hardening" / "search-log.jsonl")
    modified = copy.deepcopy(records)
    modified[1]["previous_record_hash"] = "sha256:broken"
    with pytest.raises(AssertionError, match="breaks hash chain"):
        inventory.validate_search_log(modified)


def test_source_extension_summary_mentions_append_only_contract():
    summary = (ROOT / "docs" / "article-hardening" / "source-extension-inventory.md").read_text(
        encoding="utf-8"
    )
    assert "hash chained" in summary
    assert "Later searches should append records" in summary
