import csv
import json
import shutil
import sys
import uuid
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.maintenance import build_candidate_decision_ledger as ledger


def test_candidate_decision_ledger_rows_cover_expected_surfaces() -> None:
    rows = ledger.build_rows()
    scopes = {row["candidate_scope"] for row in rows}

    assert len(rows) == 511
    assert {
        "search_route",
        "source_candidate",
        "mapping_candidate",
        "ontology_inclusion_candidate",
    } <= scopes
    assert any(row["decision_class"] == "excluded" for row in rows)
    assert any(row["decision_class"] == "included" for row in rows)
    assert all(row["rationale"] for row in rows)
    assert all(row["assumptions_or_heuristics"] for row in rows)


def test_candidate_decision_ledger_outputs_are_consistent() -> None:
    temp_dir = Path(".tmp") / f"candidate_ledger_{uuid.uuid4().hex}"
    temp_dir.mkdir(parents=True)
    old_csv, old_json, old_md = ledger.CSV_PATH, ledger.JSON_PATH, ledger.MD_PATH
    try:
        ledger.CSV_PATH = temp_dir / "ledger.csv"
        ledger.JSON_PATH = temp_dir / "ledger.json"
        ledger.MD_PATH = temp_dir / "ledger.md"

        payload = ledger.build_outputs()
        csv_rows = list(csv.DictReader(ledger.CSV_PATH.open(encoding="utf-8")))
        json_payload = json.loads(ledger.JSON_PATH.read_text(encoding="utf-8"))
        markdown = ledger.MD_PATH.read_text(encoding="utf-8")

        assert payload["row_count"] == 511
        assert len(csv_rows) == payload["row_count"]
        assert json_payload["row_count"] == payload["row_count"]
        assert "Assumptions and heuristics" in markdown
        assert "Mapping-candidate decisions" in markdown
    finally:
        ledger.CSV_PATH, ledger.JSON_PATH, ledger.MD_PATH = old_csv, old_json, old_md
        shutil.rmtree(temp_dir, ignore_errors=True)
