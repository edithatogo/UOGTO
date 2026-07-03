from __future__ import annotations

import csv
import json

from scripts.maintenance.build_mapping_reviewer_calibration import generate_report


def test_mapping_reviewer_calibration_generates_balanced_sample(tmp_path) -> None:
    review_csv = tmp_path / "mapping-review.csv"
    with review_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source_label",
                "target_label",
                "source_id",
                "target_id",
                "source_definition",
                "target_definition",
                "decision",
                "reviewer_a_decision",
                "reviewer_b_decision",
                "adjudicated_decision",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "source_label": "Strategy",
                "target_label": "Strategy",
                "source_id": "uogto:Strategy",
                "target_id": "ext:Strategy",
                "source_definition": "A plan of action.",
                "target_definition": "A plan of action.",
                "decision": "accepted",
                "reviewer_a_decision": "accepted",
                "reviewer_b_decision": "accepted",
                "adjudicated_decision": "accepted",
            }
        )
        writer.writerow(
            {
                "source_label": "Payoff",
                "target_label": "Outcome",
                "source_id": "uogto:Payoff",
                "target_id": "ext:Outcome",
                "source_definition": "Reward assigned to an action.",
                "target_definition": "Result of a game.",
                "decision": "rejected",
                "reviewer_a_decision": "rejected",
                "reviewer_b_decision": "accepted",
                "adjudicated_decision": "rejected",
            }
        )
        writer.writerow(
            {
                "source_label": "Action",
                "target_label": "Move",
                "source_id": "uogto:Action",
                "target_id": "ext:Move",
                "source_definition": "A discrete choice.",
                "target_definition": "A discrete move.",
                "decision": "accepted",
                "reviewer_a_decision": "accepted",
                "reviewer_b_decision": "accepted",
                "adjudicated_decision": "accepted",
            }
        )

    output_dir = tmp_path / "calibration"
    summary = generate_report(review_csv=review_csv, output_dir=output_dir, sample_size=4)

    assert summary["dataset"]["reviewed_rows"] == 3
    assert summary["dataset"]["accepted_rows"] == 2
    assert summary["dataset"]["rejected_rows"] == 1
    assert summary["agreement"]["pair_count"] == 3
    assert summary["agreement"]["agreement_rate"] == 2 / 3
    assert summary["dataset"]["adjudicated_rows"] == 3

    report_json = json.loads((output_dir / "mapping-review-calibration.json").read_text(encoding="utf-8"))
    report_csv = (output_dir / "mapping-review-calibration.csv").read_text(encoding="utf-8")
    report_md = (output_dir / "mapping-review-calibration.md").read_text(encoding="utf-8")

    assert report_json["dataset"]["sample_size"] == 3
    assert "Reviewer calibration sample" in report_md
    assert "sample_id" in report_csv
