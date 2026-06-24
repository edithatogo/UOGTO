from __future__ import annotations

import argparse
import csv
import json
import math
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REVIEW_CSV = ROOT / "docs" / "ontology-comparison" / "mapping-review.csv"
DEFAULT_CANDIDATES_JSONL = ROOT / "docs" / "ontology-comparison" / "mapping-candidates.jsonl"
DEFAULT_OUTPUT_DIR = ROOT / "docs" / "ontology-comparison" / "mapping-robustness"

FEATURES = (
    "exact_label",
    "normalized_label",
    "definition_similarity",
    "hierarchy_context",
    "property_signature",
    "embedding_similarity",
)


def _norm_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.casefold()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def _raw_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _tokenize(value: Any) -> set[str]:
    text = _norm_text(value)
    if not text:
        return set()
    return {token for token in text.split() if token}


def _jaccard(left: Any, right: Any) -> float:
    lset = _tokenize(left)
    rset = _tokenize(right)
    if not lset and not rset:
        return 0.0
    if not lset or not rset:
        return 0.0
    return len(lset & rset) / len(lset | rset)


def _char_ngrams(value: Any, n: int = 3) -> Counter[str]:
    text = _norm_text(value).replace(" ", "")
    grams: Counter[str] = Counter()
    if not text:
        return grams
    if len(text) <= n:
        grams[text] += 1
        return grams
    for idx in range(len(text) - n + 1):
        grams[text[idx : idx + n]] += 1
    return grams


def _cosine(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0
    numerator = sum(left[key] * right.get(key, 0) for key in left)
    left_norm = math.sqrt(sum(count * count for count in left.values()))
    right_norm = math.sqrt(sum(count * count for count in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def _feature_text(record: dict[str, Any], aliases: Iterable[str]) -> str:
    for alias in aliases:
        value = record.get(alias)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def _candidate_key(record: dict[str, Any]) -> tuple[str, str]:
    left = _norm_text(
        _feature_text(
            record,
            (
                "source_curie",
                "source_iri",
                "source_id",
                "left_id",
                "left_curie",
                "source_label",
                "left_label",
            ),
        )
    )
    right = _norm_text(
        _feature_text(
            record,
            (
                "target_curie",
                "target_iri",
                "target_id",
                "right_id",
                "right_curie",
                "target_label",
                "right_label",
            ),
        )
    )
    return left, right


def _load_review_rows(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _load_candidates(path: Path | None) -> dict[tuple[str, str], dict[str, Any]]:
    if path is None or not path.exists():
        return {}
    candidates: dict[tuple[str, str], dict[str, Any]] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            candidates[_candidate_key(record)] = record
    return candidates


def _merge_record(row: dict[str, Any], candidates: dict[tuple[str, str], dict[str, Any]]) -> dict[str, Any]:
    key = _candidate_key(row)
    merged = dict(candidates.get(key, {}))
    merged.update(row)
    return merged


def _decision_value(record: dict[str, Any]) -> str:
    for key in (
        "decision",
        "review_decision",
        "mapping_decision",
        "status",
        "final_status",
        "outcome",
        "label",
    ):
        value = record.get(key)
        if value is not None and str(value).strip():
            return str(value).strip().casefold()
    return ""


def _is_positive(record: dict[str, Any]) -> bool | None:
    decision = _decision_value(record)
    if not decision:
        return None
    positive_tokens = {
        "accept",
        "accepted",
        "approve",
        "approved",
        "keep",
        "kept",
        "match",
        "matched",
        "true",
        "yes",
        "1",
        "aligned",
        "align",
        "selected",
    }
    negative_tokens = {
        "reject",
        "rejected",
        "drop",
        "discard",
        "false",
        "no",
        "0",
        "nonmatch",
        "non-match",
        "mismatch",
    }
    decision = decision.replace("_", " ").replace("-", " ")
    tokens = set(decision.split())
    if tokens & positive_tokens:
        return True
    if tokens & negative_tokens:
        return False
    return None


def _first_nonempty(record: dict[str, Any], aliases: Iterable[str]) -> str:
    return _feature_text(record, aliases)


def _feature_scores(record: dict[str, Any]) -> dict[str, float]:
    source_label = _first_nonempty(
        record,
        ("source_label", "left_label", "candidate_source_label", "subject_label", "label_a"),
    )
    target_label = _first_nonempty(
        record,
        ("target_label", "right_label", "candidate_target_label", "object_label", "label_b"),
    )
    source_definition = _first_nonempty(
        record,
        ("source_definition", "left_definition", "definition_a", "subject_definition"),
    )
    target_definition = _first_nonempty(
        record,
        ("target_definition", "right_definition", "definition_b", "object_definition"),
    )
    source_hierarchy = _first_nonempty(
        record,
        (
            "source_hierarchy",
            "left_hierarchy",
            "source_ancestors",
            "left_ancestors",
            "source_broader",
            "source_context",
        ),
    )
    target_hierarchy = _first_nonempty(
        record,
        (
            "target_hierarchy",
            "right_hierarchy",
            "target_ancestors",
            "right_ancestors",
            "target_broader",
            "target_context",
        ),
    )
    source_signature = _first_nonempty(
        record,
        (
            "source_signature",
            "left_signature",
            "source_properties",
            "left_properties",
            "source_property_signature",
            "left_property_signature",
        ),
    )
    target_signature = _first_nonempty(
        record,
        (
            "target_signature",
            "right_signature",
            "target_properties",
            "right_properties",
            "target_property_signature",
            "right_property_signature",
        ),
    )

    embedding_source = _first_nonempty(
        record,
        (
            "source_embedding_text",
            "left_embedding_text",
            "source_semantic_text",
            "left_semantic_text",
            "source_label",
            "left_label",
            "source_definition",
            "left_definition",
        ),
    )
    embedding_target = _first_nonempty(
        record,
        (
            "target_embedding_text",
            "right_embedding_text",
            "target_semantic_text",
            "right_semantic_text",
            "target_label",
            "right_label",
            "target_definition",
            "right_definition",
        ),
    )

    exact_label = 1.0 if source_label and target_label and _raw_text(source_label) == _raw_text(target_label) else 0.0
    normalized_label = 1.0 if _norm_text(source_label) and _norm_text(source_label) == _norm_text(target_label) else 0.0
    definition_similarity = _jaccard(source_definition, target_definition)
    hierarchy_context = _jaccard(source_hierarchy, target_hierarchy)
    property_signature = _jaccard(source_signature, target_signature)

    try:
        from sentence_transformers import SentenceTransformer  # type: ignore

        model_name = record.get("_embedding_model") or "all-MiniLM-L6-v2"
        model = SentenceTransformer(model_name)
        left_vector = model.encode([embedding_source], normalize_embeddings=True)[0]
        right_vector = model.encode([embedding_target], normalize_embeddings=True)[0]
        embedding_similarity = float(sum(l * r for l, r in zip(left_vector, right_vector)))
        embedding_method = f"sentence-transformers:{model_name}"
    except Exception:
        embedding_similarity = _cosine(_char_ngrams(embedding_source), _char_ngrams(embedding_target))
        embedding_method = "character-trigram-cosine-proxy"

    return {
        "exact_label": exact_label,
        "normalized_label": normalized_label,
        "definition_similarity": definition_similarity,
        "hierarchy_context": hierarchy_context,
        "property_signature": property_signature,
        "embedding_similarity": embedding_similarity,
        "_embedding_method": embedding_method,
    }


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def _metrics(truth: list[bool], predicted: list[bool]) -> dict[str, float]:
    tp = sum(1 for t, p in zip(truth, predicted) if t and p)
    fp = sum(1 for t, p in zip(truth, predicted) if not t and p)
    tn = sum(1 for t, p in zip(truth, predicted) if not t and not p)
    fn = sum(1 for t, p in zip(truth, predicted) if t and not p)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if precision + recall else 0.0
    accuracy = (tp + tn) / len(truth) if truth else 0.0
    return {
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "accuracy": accuracy,
    }


def _predict(scores: dict[str, float], active_features: Iterable[str], threshold: float = 0.5) -> bool:
    active = [scores[name] for name in active_features]
    if not active:
        return False
    return _mean(active) >= threshold


def generate_report(
    review_csv: Path = DEFAULT_REVIEW_CSV,
    candidate_jsonl: Path | None = DEFAULT_CANDIDATES_JSONL,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    review_rows = _load_review_rows(review_csv)
    candidates = _load_candidates(candidate_jsonl)

    records: list[dict[str, Any]] = []
    for row in review_rows:
        merged = _merge_record(row, candidates)
        positive = _is_positive(merged)
        if positive is None:
            continue
        scores = _feature_scores(merged)
        records.append(
            {
                "positive": positive,
                "scores": scores,
                "record": merged,
            }
        )

    truth = [entry["positive"] for entry in records]
    feature_summary: dict[str, Any] = {}
    for feature in FEATURES:
        values = [entry["scores"][feature] for entry in records]
        positives = [entry["scores"][feature] for entry in records if entry["positive"]]
        negatives = [entry["scores"][feature] for entry in records if not entry["positive"]]
        feature_summary[feature] = {
            "mean_score": _mean(values),
            "mean_positive_score": _mean(positives),
            "mean_negative_score": _mean(negatives),
            "positive_support_rate": sum(1 for value in positives if value >= 0.5) / len(positives) if positives else 0.0,
            "negative_support_rate": sum(1 for value in negatives if value >= 0.5) / len(negatives) if negatives else 0.0,
        }

    ablations: dict[str, Any] = {}
    full_predictions = [_predict(entry["scores"], FEATURES) for entry in records]
    ablations["all_features"] = {
        **_metrics(truth, full_predictions),
        "active_features": list(FEATURES),
    }
    for feature in FEATURES:
        active = [name for name in FEATURES if name != feature]
        ablations[f"minus_{feature}"] = {
            **_metrics(truth, [_predict(entry["scores"], active) for entry in records]),
            "active_features": active,
        }
        ablations[f"only_{feature}"] = {
            **_metrics(truth, [_predict(entry["scores"], [feature]) for entry in records]),
            "active_features": [feature],
        }

    embedding_method = records[0]["scores"].get("_embedding_method", "character-trigram-cosine-proxy") if records else "character-trigram-cosine-proxy"

    summary = {
        "source": {
            "review_csv": str(review_csv),
            "candidate_jsonl": str(candidate_jsonl) if candidate_jsonl else None,
        },
        "dataset": {
            "reviewed_rows": len(review_rows),
            "scored_rows": len(records),
            "positive_rows": sum(1 for value in truth if value),
            "negative_rows": sum(1 for value in truth if not value),
            "skipped_rows": len(review_rows) - len(records),
        },
        "methods": {
            "embedding_similarity": embedding_method,
            "threshold": 0.5,
            "aggregation": "mean feature score",
        },
        "features": feature_summary,
        "ablations": ablations,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "mapping-robustness-ablation.json"
    csv_path = output_dir / "mapping-robustness-ablation.csv"
    md_path = output_dir / "mapping-robustness.md"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["ablation", "precision", "recall", "f1", "accuracy", "tp", "fp", "tn", "fn", "active_features"],
        )
        writer.writeheader()
        for name, metrics in ablations.items():
            writer.writerow(
                {
                    "ablation": name,
                    "precision": metrics["precision"],
                    "recall": metrics["recall"],
                    "f1": metrics["f1"],
                    "accuracy": metrics["accuracy"],
                    "tp": metrics["tp"],
                    "fp": metrics["fp"],
                    "tn": metrics["tn"],
                    "fn": metrics["fn"],
                    "active_features": ", ".join(metrics["active_features"]),
                }
            )

    lines = [
        "# Mapping robustness experiments",
        "",
        "This experiment evaluates the mapping review set with a simple feature-ablation scaffold.",
        "The goal is to measure how much each signal contributes to reviewed mapping decisions.",
        "",
        f"- Review rows: {summary['dataset']['reviewed_rows']}",
        f"- Scored rows: {summary['dataset']['scored_rows']}",
        f"- Positive rows: {summary['dataset']['positive_rows']}",
        f"- Negative rows: {summary['dataset']['negative_rows']}",
        f"- Embedding method: {embedding_method}",
        "",
        "## Feature families",
        "",
        "- exact_label",
        "- normalized_label",
        "- definition_similarity",
        "- hierarchy_context",
        "- property_signature",
        "- embedding_similarity",
        "",
        "## Ablations",
        "",
        "| ablation | precision | recall | f1 | accuracy | active features |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for name, metrics in ablations.items():
        lines.append(
            f"| {name} | {metrics['precision']:.3f} | {metrics['recall']:.3f} | {metrics['f1']:.3f} | {metrics['accuracy']:.3f} | {', '.join(metrics['active_features'])} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-csv", type=Path, default=DEFAULT_REVIEW_CSV)
    parser.add_argument("--candidate-jsonl", type=Path, default=DEFAULT_CANDIDATES_JSONL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args(argv)
    generate_report(args.review_csv, args.candidate_jsonl, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
