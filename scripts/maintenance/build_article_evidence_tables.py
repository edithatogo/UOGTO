#!/usr/bin/env python3
"""Build article-facing ontology and evidence tables for UOGTO."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "article-hardening" / "article-facing-tables"
LEGACY_OUT = ROOT / "docs" / "article-hardening" / "article-tables"
QUALITY = ROOT / "docs" / "article-hardening" / "quality-metrics.json"
INCLUSION_JSON = ROOT / "docs" / "article-hardening" / "uogto-inclusion-candidates.json"
INCLUSION_CSV = ROOT / "docs" / "article-hardening" / "uogto-inclusion-candidates.csv"
ROBUSTNESS = ROOT / "docs" / "ontology-comparison" / "mapping-robustness" / "mapping-robustness-ablation.json"
CALIBRATION = ROOT / "docs" / "ontology-comparison" / "mapping-calibration" / "mapping-review-calibration.json"
NETWORK = ROOT / "docs" / "ontology-comparison" / "network-sensitivity.json"
SSSOM = ROOT / "docs" / "ontology-comparison" / "accepted-alignments.sssom.tsv"
SSSOM_META = ROOT / "docs" / "ontology-comparison" / "accepted-alignments.sssom.yml"
REVIEW = ROOT / "docs" / "ontology-comparison" / "mapping-review.csv"


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_json(path: Path, rows: list[dict[str, Any]], schema: str, sources: list[str]) -> None:
    payload = {
        "schema": schema,
        "generated_at_utc": "deterministic-local-preflight",
        "row_count": len(rows),
        "sources": sources,
        "rows": rows,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, rows: list[dict[str, Any]], fields: list[str], note: str) -> None:
    lines = [f"# {title}", "", note, "", "| " + " | ".join(fields) + " |", "| " + " | ".join(["---"] * len(fields)) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "-") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def status(value: Any) -> str:
    if isinstance(value, bool):
        return "pass" if value else "missing"
    if value in (None, ""):
        return "missing"
    return str(value)


def build_module_audit() -> list[dict[str, Any]]:
    q = load_json(QUALITY, {})
    annotations = q.get("annotation_completeness", {}).get("modules", {})
    examples = q.get("examples_per_module", {}).get("modules", {})
    cqs = q.get("competency_query_coverage", {}).get("modules", {})
    import_depth = q.get("import_depth", {}).get("modules", {})
    hierarchy = q.get("hierarchy_depth", {})
    shacl_module = q.get("shacl_example_module_coverage", {})
    shape_links = shacl_module.get("module_shape_links", {})
    owl = q.get("owl_profile_reasoner_status", {})
    rows: list[dict[str, Any]] = []
    for module in sorted(annotations):
        ann = annotations.get(module, {})
        ex = examples.get(module, [])
        cq_paths = cqs.get(module, [])
        shapes = shape_links.get(module, [])
        rows.append({
            "module": module,
            "classes": ann.get("class_count", 0),
            "properties": ann.get("property_count", 0),
            "label_completeness": ann.get("label_completeness", ""),
            "definition_completeness": ann.get("definition_completeness", ""),
            "missing_labels": len(ann.get("missing_labels", [])),
            "missing_definitions": len(ann.get("missing_definitions", [])),
            "shacl_shape_links": len(shapes),
            "examples": len(ex),
            "competency_queries": len(cq_paths),
            "import_depth": import_depth.get(module, {}).get("local_import_depth", import_depth.get(module, {}).get("depth", "")) if isinstance(import_depth.get(module), dict) else "",
            "hierarchy_max_depth_global": hierarchy.get("max_depth", ""),
            "rdf_parse_status": owl.get("rdf_parse_status", ""),
            "pyshacl_examples_status": owl.get("pyshacl_examples_rdfs_status", ""),
            "owl_profile_status": owl.get("owl_profile_screen", {}).get("status", ""),
            "reasoner_status": owl.get("reasoner", {}).get("owlrl_status", ""),
            "evidence_level": "repo-derived",
            "source_artifact": "docs/article-hardening/quality-metrics.json",
        })
    return rows


def inclusion_records() -> list[dict[str, Any]]:
    data = load_json(INCLUSION_JSON, None)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("rows", "candidates", "items", "records"):
            if isinstance(data.get(key), list):
                return data[key]
    return read_csv(INCLUSION_CSV)


def pick(row: dict[str, Any], *names: str) -> Any:
    for name in names:
        value = row.get(name)
        if value not in (None, ""):
            return value
    return ""


def build_disposition_table() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    allowed = {"add to uogto", "align externally only", "defer", "reject duplicate", "reject out of scope", "domain review"}
    for i, row in enumerate(inclusion_records(), start=1):
        disp = str(pick(row, "disposition", "decision", "recommended_disposition", "triage_decision", "status")).strip()
        norm = disp.lower() if disp else "domain review"
        if norm not in allowed:
            norm = "domain review"
        rows.append({
            "candidate_id": pick(row, "candidate_id", "id", "term_id") or f"candidate-{i:03d}",
            "candidate_label": pick(row, "candidate_label", "label", "term", "concept", "name"),
            "source_family": pick(row, "source_family", "family", "source", "source_name"),
            "source_artifact": pick(row, "source_artifact", "artifact", "source_path") or "docs/article-hardening/uogto-inclusion-candidates.json",
            "evidence_level": pick(row, "evidence_level", "evidence", "evidence_strength") or "curated",
            "disposition": norm,
            "rationale": pick(row, "rationale", "inclusion_rationale", "decision_rationale", "notes"),
            "uogto_target": pick(row, "uogto_target", "target_module", "module", "proposed_module"),
            "external_alignment": pick(row, "external_alignment", "alignment", "mapping", "mapped_to"),
            "reviewer_handoff": pick(row, "reviewer_handoff", "reviewer", "owner") or "game_theory_gap_researcher/domain reviewer",
        })
    return rows


def sssom_count() -> int:
    if not SSSOM.exists():
        return 0
    return max(0, sum(1 for _ in SSSOM.open(encoding="utf-8")) - 1)


def build_mapping_table() -> list[dict[str, Any]]:
    robustness = load_json(ROBUSTNESS, {})
    calibration = load_json(CALIBRATION, {})
    network = load_json(NETWORK, {})
    review_rows = read_csv(REVIEW)
    accepted = sum(1 for r in review_rows if str(pick(r, "mapping_decision", "decision", "status")).lower() in {"accept", "accepted"})
    rejected = sum(1 for r in review_rows if str(pick(r, "mapping_decision", "decision", "status")).lower() in {"reject", "rejected"})
    rows: list[dict[str, Any]] = []
    rows.append({
        "analysis_component": "SSSOM publication surface",
        "artifact": "docs/ontology-comparison/accepted-alignments.sssom.tsv",
        "method": "Accepted TTL alignments exported to SSSOM TSV plus YAML metadata",
        "primary_metric": "mapping_count",
        "primary_value": sssom_count(),
        "sensitivity_or_ablation": "n/a",
        "calibration_or_adjudication": "reviewed mappings only",
        "article_use": "Inspectable mapping evidence and reusable supplement table",
        "status": "complete" if SSSOM.exists() and SSSOM_META.exists() else "missing",
    })
    for name, item in sorted(robustness.get("ablations", {}).items()):
        rows.append({
            "analysis_component": f"mapping robustness ablation: {name}",
            "artifact": "docs/ontology-comparison/mapping-robustness/mapping-robustness-ablation.json",
            "method": item.get("description", robustness.get("methods", {}).get("aggregation", "feature ablation")),
            "primary_metric": pick(item, "f1", "balanced_accuracy", "precision", "recall") and "performance",
            "primary_value": json.dumps({k: item.get(k) for k in ["precision", "recall", "f1", "balanced_accuracy", "accepted_predictions", "rejected_predictions"] if k in item}, sort_keys=True),
            "sensitivity_or_ablation": name,
            "calibration_or_adjudication": "n/a",
            "article_use": "Shows dependence of accepted/rejected mapping calls on lexical, semantic, hierarchy, property-signature, and embedding signals",
            "status": "complete",
        })
    agreement = calibration.get("agreement", {})
    rows.append({
        "analysis_component": "reviewer calibration",
        "artifact": "docs/ontology-comparison/mapping-calibration/mapping-review-calibration.json",
        "method": "Accepted/rejected/adjudicated mapping sample agreement",
        "primary_metric": "agreement_rate/kappa/pair_count",
        "primary_value": json.dumps({k: agreement.get(k) for k in ["agreement_rate", "kappa", "pair_count"]}, sort_keys=True),
        "sensitivity_or_ablation": "n/a",
        "calibration_or_adjudication": f"accepted={calibration.get('dataset', {}).get('accepted_rows', accepted)}; rejected={calibration.get('dataset', {}).get('rejected_rows', rejected)}; adjudicated={calibration.get('dataset', {}).get('adjudicated_rows', '')}",
        "article_use": "Reviewer agreement and adjudication evidence for mapping claims",
        "status": "complete" if calibration else "missing",
    })
    for name, item in sorted(network.get("scenarios", {}).items()):
        rows.append({
            "analysis_component": f"network sensitivity: {name}",
            "artifact": "docs/ontology-comparison/network-sensitivity.json",
            "method": "Community/bridge analysis under source and mapping-inclusion scenarios",
            "primary_metric": "nodes/edges/communities/bridges",
            "primary_value": json.dumps({k: item.get(k) for k in ["node_count", "edge_count", "community_count", "bridge_count", "metadata_only_sources_excluded"] if k in item}, sort_keys=True),
            "sensitivity_or_ablation": name,
            "calibration_or_adjudication": "n/a",
            "article_use": "Tests whether community and bridge claims survive metadata-only exclusion and accepted-vs-related mapping choices",
            "status": "complete",
        })
    return rows


def emit_table(stem: str, title: str, rows: list[dict[str, Any]], fields: list[str], note: str, schema: str, sources: list[str]) -> None:
    write_csv(OUT / f"{stem}.csv", rows, fields)
    write_json(OUT / f"{stem}.json", rows, schema, sources)
    write_md(OUT / f"{stem}.md", title, rows, fields, note)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    LEGACY_OUT.mkdir(parents=True, exist_ok=True)
    module_fields = ["module", "classes", "properties", "label_completeness", "definition_completeness", "missing_labels", "missing_definitions", "shacl_shape_links", "examples", "competency_queries", "import_depth", "hierarchy_max_depth_global", "rdf_parse_status", "pyshacl_examples_status", "owl_profile_status", "reasoner_status", "evidence_level", "source_artifact"]
    disposition_fields = ["candidate_id", "candidate_label", "source_family", "source_artifact", "evidence_level", "disposition", "rationale", "uogto_target", "external_alignment", "reviewer_handoff"]
    mapping_fields = ["analysis_component", "artifact", "method", "primary_metric", "primary_value", "sensitivity_or_ablation", "calibration_or_adjudication", "article_use", "status"]
    module_rows = build_module_audit()
    disposition_rows = build_disposition_table()
    mapping_rows = build_mapping_table()
    emit_table("module-audit-table", "Module Audit Table", module_rows, module_fields, "Article-facing module quality table derived from the ontology quality metrics artifact.", "uogto.article.module-audit-table.v1", [str(QUALITY.relative_to(ROOT))])
    emit_table("missing-game-theory-element-dispositions", "Missing Game-Theory Element Disposition Table", disposition_rows, disposition_fields, "Disposition table for game-theory concepts considered before any UOGTO expansion.", "uogto.article.missing-game-theory-element-dispositions.v1", [str(INCLUSION_JSON.relative_to(ROOT)), str(INCLUSION_CSV.relative_to(ROOT))])
    emit_table("mapping-robustness-table", "Mapping Robustness, Sensitivity, Calibration, and SSSOM Table", mapping_rows, mapping_fields, "Mapping-method evidence table spanning SSSOM publication surfaces, feature ablations, reviewer calibration, adjudication, and network sensitivity.", "uogto.article.mapping-robustness-table.v1", [str(p.relative_to(ROOT)) for p in [ROBUSTNESS, CALIBRATION, NETWORK, SSSOM, SSSOM_META, REVIEW]])
    index = ["# Article-Facing Ontology and Evidence Tables", "", "Generated tables for manuscript and supplement claims.", "", "| Table | CSV | JSON | Markdown |", "| --- | --- | --- | --- |"]
    for stem, label in [("module-audit-table", "Module audit"), ("missing-game-theory-element-dispositions", "Missing game-theory element dispositions"), ("mapping-robustness-table", "Mapping robustness")]:
        index.append(f"| {label} | `{stem}.csv` | `{stem}.json` | `{stem}.md` |")
    index.append("")
    (OUT / "README.md").write_text("\n".join(index), encoding="utf-8")
    for path in OUT.iterdir():
        if path.is_file():
            (LEGACY_OUT / path.name).write_bytes(path.read_bytes())
    print(f"Wrote article-facing tables to {OUT.relative_to(ROOT)}")
    print(f"Mirrored article table compatibility outputs to {LEGACY_OUT.relative_to(ROOT)}")
    print(f"module_rows={len(module_rows)} disposition_rows={len(disposition_rows)} mapping_rows={len(mapping_rows)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
