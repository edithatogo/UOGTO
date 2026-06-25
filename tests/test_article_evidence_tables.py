import json
from pathlib import Path

from scripts.maintenance import build_article_evidence_tables as tables


def test_article_evidence_tables_have_required_rows_and_columns() -> None:
    module_rows = tables.build_module_audit()
    disposition_rows = tables.build_disposition_table()
    mapping_rows = tables.build_mapping_table()

    assert len(module_rows) >= 40
    assert {"module", "label_completeness", "definition_completeness", "shacl_shape_links", "examples", "competency_queries", "owl_profile_status", "reasoner_status"} <= set(module_rows[0])
    assert disposition_rows
    assert {"candidate_label", "disposition", "rationale", "reviewer_handoff"} <= set(disposition_rows[0])
    assert any(row["analysis_component"] == "SSSOM publication surface" for row in mapping_rows)
    assert any(row["analysis_component"].startswith("mapping robustness ablation") for row in mapping_rows)
    assert any(row["analysis_component"] == "reviewer calibration" for row in mapping_rows)
    assert any(row["analysis_component"].startswith("network sensitivity") for row in mapping_rows)


def test_article_evidence_tables_main_writes_csv_json_markdown() -> None:
    assert tables.main() == 0
    out = Path("docs/article-hardening/article-facing-tables")
    for stem in ["module-audit-table", "missing-game-theory-element-dispositions", "mapping-robustness-table"]:
        assert (out / f"{stem}.csv").exists()
        json_path = out / f"{stem}.json"
        assert json_path.exists()
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        assert payload["row_count"] == len(payload["rows"])
        assert (out / f"{stem}.md").exists()
    assert (out / "README.md").exists()
