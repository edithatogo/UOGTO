from __future__ import annotations

import argparse
import csv
import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REVIEW_CSV = ROOT / "docs" / "ontology-comparison" / "mapping-review.csv"
DEFAULT_OUTPUT_DIR = ROOT / "docs" / "ontology-comparison" / "mapping-calibration"


def _normalize(value: Any) -> str:
    if value is None:
        return ""
    text = unicodedata.normalize("NFKD", str(value).strip())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.casefold()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def _text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _read_rows(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _decision(record: dict[str, Any]) -> str:
    for key in (
        "decision",
        "review_decision",
        "mapping_decision",
        "status",
        "final_status",
        "outcome",
        "label",
        "reviewer_a_decision",
        "reviewer_b_decision",
        "adjudicated_decision",
    ):
        value = _text(record.get(key))
        if value:
            return value.casefold()
    return ""


def _is_positive(record: dict[str, Any]) -> bool | None:
    decision = _decision(record)
    if not decision:
        return None
    positive = {
        "accept",
        "accepted",
        "approve",
        "approved",
        "keep",
        "kept",
        "match",
        "matched",
        "aligned",
        "align",
        "yes",
        "true",
        "1",
        "selected",
    }
    negative = {
        "reject",
        "rejected",
        "drop",
        "discard",
        "no",
        "false",
        "0",
        "nonmatch",
        "non-match",
        "mismatch",
    }
    normalized = decision.replace("_", " ").replace("-", " ")
    tokens = set(normalized.split())
    if tokens & positive:
        return True
    if tokens & negative:
        return False
    return None


def _pick_field(record: dict[str, Any], *names: str) -> str:
    for name in names:
        value = _text(record.get(name))
        if value:
            return value
    return ""


def _review_key(record: dict[str, Any]) -> tuple[str, str, str]:
    return (
        _normalize(_pick_field(record, "source_curie", "source_iri", "source_id", "left_curie", "left_id", "source_label", "left_label")),
        _normalize(_pick_field(record, "target_curie", "target_iri", "target_id", "right_curie", "right_id", "target_label", "right_label")),
        _normalize(_pick_field(record, "decision", "review_decision", "mapping_decision", "status", "final_status", "outcome")),
    )


def _agreement_metrics(left: list[str], right: list[str]) -> dict[str, float]:
    pairs = [(l, r) for l, r in zip(left, right) if l and r]
    if not pairs:
        return {"pair_count": 0, "agreement_rate": 0.0, "kappa": 0.0}

    pair_count = len(pairs)
    agreement_rate = sum(1 for l, r in pairs if l == r) / pair_count
    left_counts = Counter(l for l, _ in pairs)
    right_counts = Counter(r for _, r in pairs)
    labels = sorted(set(left_counts) | set(right_counts))
    expected = sum(
        (left_counts[label] / pair_count) * (right_counts[label] / pair_count)
        for label in labels
    )
    if math.isclose(expected, 1.0):
        kappa = 0.0
    else:
        kappa = (agreement_rate - expected) / (1.0 - expected)
    return {
        "pair_count": pair_count,
        "agreement_rate": agreement_rate,
        "kappa": kappa,
    }


def generate_report(
    review_csv: Path = DEFAULT_REVIEW_CSV,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    sample_size: int = 12,
) -> dict[str, Any]:
    rows = _read_rows(review_csv)
    reviewed_rows = [row for row in rows if _is_positive(row) is not None]
    accepted = [row for row in reviewed_rows if _is_positive(row)]
    rejected = [row for row in reviewed_rows if _is_positive(row) is False]

    accepted = sorted(accepted, key=_review_key)
    rejected = sorted(rejected, key=_review_key)
    half = max(sample_size // 2, 1)
    sample = accepted[:half] + rejected[:half]
    if len(sample) < sample_size:
        remainder = accepted[half:] + rejected[half:]
        sample.extend(remainder[: sample_size - len(sample)])

    records: list[dict[str, Any]] = []
    reviewer_a: list[str] = []
    reviewer_b: list[str] = []
    adjudicated: list[str] = []

    for index, row in enumerate(sample, start=1):
        decision = _decision(row)
        reviewer_a_decision = _pick_field(row, "reviewer_a_decision", "reviewer_1_decision", "decision")
        reviewer_b_decision = _pick_field(row, "reviewer_b_decision", "reviewer_2_decision")
        adjudicated_decision = _pick_field(row, "adjudicated_decision", "adjudication", "final_decision")
        records.append(
            {
                "sample_id": f"cal-{index:03d}",
                "sampled_decision": decision,
                "source_label": _pick_field(row, "source_label", "left_label", "candidate_source_label", "subject_label"),
                "target_label": _pick_field(row, "target_label", "right_label", "candidate_target_label", "object_label"),
                "source_id": _pick_field(row, "source_curie", "source_iri", "source_id", "left_curie", "left_id"),
                "target_id": _pick_field(row, "target_curie", "target_iri", "target_id", "right_curie", "right_id"),
                "source_definition": _pick_field(row, "source_definition", "left_definition", "definition_a", "subject_definition"),
                "target_definition": _pick_field(row, "target_definition", "right_definition", "definition_b", "object_definition"),
                "reviewer_a_decision": reviewer_a_decision,
                "reviewer_b_decision": reviewer_b_decision,
                "adjudicated_decision": adjudicated_decision,
                "adjudication_status": "adjudicated" if adjudicated_decision else "pending",
            }
        )
        reviewer_a.append(_normalize(reviewer_a_decision))
        reviewer_b.append(_normalize(reviewer_b_decision))
        adjudicated.append(_normalize(adjudicated_decision))

    agreement = _agreement_metrics(reviewer_a, reviewer_b)
    adjudicated_count = sum(1 for value in adjudicated if value)

    summary = {
        "source": {"review_csv": str(review_csv)},
        "dataset": {
            "reviewed_rows": len(reviewed_rows),
            "accepted_rows": len(accepted),
            "rejected_rows": len(rejected),
            "sample_size": len(records),
            "adjudicated_rows": adjudicated_count,
        },
        "agreement": agreement,
        "sample": records,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "mapping-review-calibration.json"
    csv_path = output_dir / "mapping-review-calibration.csv"
    md_path = output_dir / "mapping-review-calibration.md"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "sample_id",
                "sampled_decision",
                "source_label",
                "target_label",
                "source_id",
                "target_id",
                "source_definition",
                "target_definition",
                "reviewer_a_decision",
                "reviewer_b_decision",
                "adjudicated_decision",
                "adjudication_status",
            ],
        )
        writer.writeheader()
        writer.writerows(records)

    md_lines = [
        "# Reviewer calibration sample",
        "",
        "This artifact samples accepted and rejected mappings for a small manual calibration pass.",
        "Populate the reviewer B and adjudication columns to calculate agreement or final outcome rates.",
        "",
        f"- Reviewed rows: {summary['dataset']['reviewed_rows']}",
        f"- Accepted rows in sample pool: {summary['dataset']['accepted_rows']}",
        f"- Rejected rows in sample pool: {summary['dataset']['rejected_rows']}",
        f"- Sample size: {summary['dataset']['sample_size']}",
        f"- Adjudicated rows present: {summary['dataset']['adjudicated_rows']}",
        f"- Agreement rate: {agreement['agreement_rate']:.3f}",
        f"- Cohen's kappa: {agreement['kappa']:.3f}",
        "",
        "## Sample layout",
        "",
        "| sample_id | sampled_decision | source_label | target_label | reviewer_a | reviewer_b | adjudication |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in records:
        md_lines.append(
            f"| {row['sample_id']} | {row['sampled_decision']} | {row['source_label']} | {row['target_label']} | {row['reviewer_a_decision']} | {row['reviewer_b_decision']} | {row['adjudicated_decision']} |"
        )
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-csv", type=Path, default=DEFAULT_REVIEW_CSV)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--sample-size", type=int, default=12)
    args = parser.parse_args(argv)
    generate_report(args.review_csv, args.output_dir, args.sample_size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
