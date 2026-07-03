from __future__ import annotations

import csv
import json

from scripts.maintenance.build_mapping_robustness_ablation import generate_report


def test_mapping_robustness_ablation_generates_feature_family_outputs(tmp_path) -> None:
    review_csv = tmp_path / "mapping-review.csv"
    with review_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source_label",
                "target_label",
                "source_definition",
                "target_definition",
                "source_hierarchy",
                "target_hierarchy",
                "source_properties",
                "target_properties",
                "decision",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "source_label": "Strategy",
                "target_label": "Strategy",
                "source_definition": "A plan of action.",
                "target_definition": "A plan of action.",
                "source_hierarchy": "Game theory>Strategy",
                "target_hierarchy": "Game theory>Strategy",
                "source_properties": "hasPlayer hasAction",
                "target_properties": "hasPlayer hasAction",
                "decision": "accepted",
            }
        )
        writer.writerow(
            {
                "source_label": "Payoff",
                "target_label": "Outcome",
                "source_definition": "Reward assigned to an action.",
                "target_definition": "Result of a game.",
                "source_hierarchy": "Game theory>Payoff",
                "target_hierarchy": "Game theory>Outcome",
                "source_properties": "hasValue hasUnit",
                "target_properties": "hasValue hasUnit",
                "decision": "rejected",
            }
        )

    output_dir = tmp_path / "out"
    summary = generate_report(review_csv=review_csv, candidate_jsonl=None, output_dir=output_dir)

    assert summary["dataset"]["reviewed_rows"] == 2
    assert summary["dataset"]["scored_rows"] == 2
    assert set(summary["features"]) == {
        "exact_label",
        "normalized_label",
        "definition_similarity",
        "hierarchy_context",
        "property_signature",
        "embedding_similarity",
    }
    assert "all_features" in summary["ablations"]
    assert "minus_exact_label" in summary["ablations"]
    assert "only_embedding_similarity" in summary["ablations"]

    report_json = json.loads((output_dir / "mapping-robustness-ablation.json").read_text(encoding="utf-8"))
    report_md = (output_dir / "mapping-robustness.md").read_text(encoding="utf-8")
    report_csv = (output_dir / "mapping-robustness-ablation.csv").read_text(encoding="utf-8")

    assert report_json["methods"]["aggregation"] == "mean feature score"
    assert "Mapping robustness experiments" in report_md
    assert "embedding_similarity" in report_md
    assert "ablation" in report_csv
