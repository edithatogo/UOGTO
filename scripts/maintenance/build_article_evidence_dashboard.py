from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from html import escape
from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "article-hardening"
DB_PATH = DOCS / "article-hardening.duckdb"
DEFAULT_JSON = DOCS / "article-evidence-dashboard.json"
DEFAULT_MD = DOCS / "article-evidence-dashboard.md"
DEFAULT_HTML = DOCS / "article-evidence-dashboard.html"

VALIDATED_TABLES = [
    {
        "name": "Source extension inventory",
        "artifact_group": "source-extension-inventory",
        "formats": [
            DOCS / "source-extension-inventory.json",
            DOCS / "source-extension-inventory.md",
        ],
        "validation_gate": "scripts/maintenance/check_article_hardening_protocol.py",
        "purpose": "Living evidence register for search routes, source families, and evidence levels.",
    },
    {
        "name": "Search log",
        "artifact_group": "search-log",
        "formats": [DOCS / "search-log.jsonl"],
        "validation_gate": "scripts/maintenance/check_article_hardening_protocol.py",
        "purpose": "Append-only search history with hash-chained evidence records.",
    },
    {
        "name": "Quality metrics",
        "artifact_group": "quality-metrics",
        "formats": [DOCS / "quality-metrics.json", DOCS / "reasoner-report.md"],
        "validation_gate": "scripts/maintenance/build_article_hardening_quality.py",
        "purpose": "Ontology-quality benchmark and reasoner report for the article-hardening track.",
    },
    {
        "name": "Manual review sample",
        "artifact_group": "manual-review-sample",
        "formats": [
            DOCS / "manual-review-sample.csv",
            DOCS / "manual-review-sample.md",
            DOCS / "manual-review-sample.json",
            DOCS / "manual-review-sample.parquet",
        ],
        "validation_gate": "scripts/maintenance/export_tabular_artifacts.py",
        "purpose": "Manually reviewed source sample for reviewer calibration and dual screening.",
    },
    {
        "name": "Dual screening sample",
        "artifact_group": "dual-screening-sample",
        "formats": [
            DOCS / "dual-screening-sample.csv",
            DOCS / "dual-screening-sample.md",
            DOCS / "dual-screening-sample.json",
            DOCS / "dual-screening-sample.parquet",
        ],
        "validation_gate": "scripts/maintenance/export_tabular_artifacts.py",
        "purpose": "Researcher, peer reviewer, and red-team adjudication sample.",
    },
    {
        "name": "UOGTO inclusion candidates",
        "artifact_group": "uogto-inclusion-candidates",
        "formats": [
            DOCS / "uogto-inclusion-candidates.csv",
            DOCS / "uogto-inclusion-candidates.md",
            DOCS / "uogto-inclusion-candidates.json",
            DOCS / "uogto-inclusion-candidates.parquet",
        ],
        "validation_gate": "scripts/maintenance/export_tabular_artifacts.py",
        "purpose": "Triage table for add-to-UOGTO, align-external-only, defer, reject, or domain-review outcomes.",
    },
    {
        "name": "Use-case coverage matrix",
        "artifact_group": "use-case-coverage-matrix",
        "formats": [
            DOCS / "use-case-coverage-matrix.csv",
            DOCS / "use-case-coverage-matrix.md",
            DOCS / "use-case-coverage-matrix.json",
            DOCS / "use-case-coverage-matrix.parquet",
        ],
        "validation_gate": "scripts/maintenance/export_tabular_artifacts.py",
        "purpose": "Coverage matrix for the article-hardened case studies and ontology examples.",
    },
]

VALIDATED_FIGURES = [
    {
        "name": "PRISMA 2020 source discovery flow source",
        "path": DOCS / "figures" / "prisma-2020-source-discovery-flow.md",
        "purpose": "Source discovery count and route summary in editable Mermaid Markdown.",
    },
    {
        "name": "PRISMA 2020 source discovery flow SVG",
        "path": DOCS / "figures" / "prisma-2020-source-discovery-flow.svg",
        "purpose": "Journal-scale rendered source discovery flow with accessible SVG metadata.",
    },
    {
        "name": "PRISMA 2020 source discovery flow PDF",
        "path": DOCS / "figures" / "prisma-2020-source-discovery-flow.pdf",
        "purpose": "PDFLaTeX-compatible rendered source discovery flow.",
    },
    {
        "name": "PRISMA 2020 screening flow source",
        "path": DOCS / "figures" / "prisma-2020-screening-flow.md",
        "purpose": "Screening, inclusion, and exclusion flow in editable Mermaid Markdown.",
    },
    {
        "name": "PRISMA 2020 screening flow SVG",
        "path": DOCS / "figures" / "prisma-2020-screening-flow.svg",
        "purpose": "Journal-scale rendered screening flow with accessible SVG metadata.",
    },
    {
        "name": "PRISMA 2020 screening flow PDF",
        "path": DOCS / "figures" / "prisma-2020-screening-flow.pdf",
        "purpose": "PDFLaTeX-compatible rendered screening flow.",
    },
]

SOURCE_LEVEL_LABELS = {
    "parsed_rdf_owl": "Parsed RDF",
    "structured_non_rdf": "Structured non-RDF",
    "metadata_only": "Metadata-only",
    "literature_only": "Literature-only",
    "excluded": "Excluded",
}


def load_sources() -> list[dict]:
    if DB_PATH.exists():
        con = duckdb.connect(str(DB_PATH), read_only=True)
        try:
            payloads = [row[0] for row in con.execute("SELECT payload_json FROM sources ORDER BY source_path, payload_json").fetchall()]
        finally:
            con.close()
        return [json.loads(payload) for payload in payloads]
    inventory = json.loads((DOCS / "source-extension-inventory.json").read_text(encoding="utf-8"))
    return list(inventory.get("sources", []))


def load_search_log() -> list[dict]:
    path = DOCS / "search-log.jsonl"
    rows = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_quality_metrics() -> dict:
    return json.loads((DOCS / "quality-metrics.json").read_text(encoding="utf-8"))


def validate_artifacts() -> None:
    for item in VALIDATED_TABLES:
        for path in item["formats"]:
            if not path.exists():
                raise FileNotFoundError(path)
    for item in VALIDATED_FIGURES:
        if not item["path"].exists():
            raise FileNotFoundError(item["path"])


def sources_by_level(sources: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for source in sources:
        level = source.get("evidence_level", "metadata_only")
        grouped[level].append(source)
    for level in SOURCE_LEVEL_LABELS:
        grouped.setdefault(level, [])
    return grouped


def source_summary_counts(grouped: dict[str, list[dict]]) -> list[dict]:
    ordered = []
    for level in ["parsed_rdf_owl", "structured_non_rdf", "metadata_only", "literature_only", "excluded"]:
        ordered.append(
            {
                "level": level,
                "label": SOURCE_LEVEL_LABELS[level],
                "count": len(grouped.get(level, [])),
            }
        )
    return ordered


def format_source_row(source: dict) -> dict:
    source_id = source.get("source_id") or source.get("id") or source.get("name")
    name = source.get("source_name") or source.get("name")
    family = source.get("source_family") or source.get("family")
    rationale = source.get("inclusion_rationale") or source.get("reason") or ""
    status = source.get("inclusion_status") or source.get("status") or "included"
    return {
        "source_id": source_id,
        "name": name,
        "family": family,
        "status": status,
        "rationale": rationale,
        "licence": source.get("licence", {}),
        "search_record_ids": source.get("search_record_ids", []),
        "artefact": source,
    }


def grouped_source_rows(grouped: dict[str, list[dict]]) -> dict[str, list[dict]]:
    rows = {}
    for level, source_list in grouped.items():
        rows[level] = sorted((format_source_row(source) for source in source_list), key=lambda row: (row["family"] or "", row["source_id"] or ""))
    return rows


def negative_evidence_rows(search_log: list[dict]) -> list[dict]:
    rows = []
    for record in search_log:
        if record.get("screening_decision") == "negative_evidence_no_relevant_ontology_found" or record.get("included_count") == 0:
            rows.append(
                {
                    "record_id": record.get("record_id"),
                    "surface": record.get("surface"),
                    "surface_type": record.get("surface_type"),
                    "query": record.get("query"),
                    "result_count": record.get("result_count"),
                    "rationale": record.get("inclusion_rationale"),
                }
            )
    return rows


def build_manifest() -> dict:
    validate_artifacts()
    sources = load_sources()
    search_log = load_search_log()
    metrics = load_quality_metrics()
    grouped = sources_by_level(sources)
    evidence_rows = grouped_source_rows(grouped)
    counts = source_summary_counts(grouped)
    validated_tables = [
        {
            "name": item["name"],
            "artifact_group": item["artifact_group"],
            "formats": [path.relative_to(DOCS).as_posix() for path in item["formats"]],
            "validation_gate": item["validation_gate"],
            "purpose": item["purpose"],
        }
        for item in VALIDATED_TABLES
    ]
    validated_figures = [
        {
            "name": item["name"],
            "path": item["path"].relative_to(DOCS).as_posix(),
            "purpose": item["purpose"],
        }
        for item in VALIDATED_FIGURES
    ]
    manifest = {
        "schema": "uogto.article-hardening.article-evidence-dashboard.v1",
        "title": "Article Evidence Dashboard",
        "validated_tables": validated_tables,
        "validated_figures": validated_figures,
        "source_evidence_summary": counts,
        "sources_by_evidence_level": evidence_rows,
        "negative_evidence": negative_evidence_rows(search_log),
        "quality_metrics_reference": {
            "path": "quality-metrics.json",
            "summary": {
                "classes": metrics["annotation_completeness"]["global"]["class_count"],
                "properties": metrics["annotation_completeness"]["global"]["property_count"],
                "example_count": metrics["examples_per_module"]["example_count"],
                "query_count": metrics["competency_query_coverage"]["query_count"],
            },
        },
        "generated_from": {
            "duckdb": "article-hardening.duckdb",
            "source_inventory": "source-extension-inventory.json",
            "search_log": "search-log.jsonl",
            "quality_metrics": "quality-metrics.json",
        },
    }
    return manifest


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def format_formats(items: list[str]) -> str:
    return ", ".join(f"`{item}`" for item in items)


def render_markdown(manifest: dict) -> str:
    lines = [
        "# Article Evidence Dashboard",
        "",
        "This dashboard exposes only validated tables and figures from the article-hardening evidence package.",
        "The source lists are separated by evidence level: parsed RDF, structured non-RDF, metadata-only, literature-only, and excluded.",
        "",
        "## Summary",
        "",
    ]
    for item in manifest["source_evidence_summary"]:
        lines.append(f"- **{item['label']}**: {item['count']}")
    lines.extend(["", "## Validated Tables", "", "| Table | Formats | Validation gate | Purpose |", "| --- | --- | --- | --- |"])
    for item in manifest["validated_tables"]:
        lines.append(
            f"| {item['name']} | {format_formats(item['formats'])} | `{item['validation_gate']}` | {item['purpose']} |"
        )
    lines.extend(["", "## Validated Figures", "", "| Figure | Path | Purpose |", "| --- | --- | --- |"])
    for item in manifest["validated_figures"]:
        lines.append(f"| {item['name']} | `{item['path']}` | {item['purpose']} |")
    lines.extend(["", "## Source Evidence Categories", ""])
    for item in manifest["source_evidence_summary"]:
        lines.append(f"### {item['label']}")
        rows = manifest["sources_by_evidence_level"].get(item["level"], [])
        lines.append("")
        lines.append(f"- Count: {item['count']}")
        if rows:
            lines.append("")
            lines.append("| Source | Family | Status | Rationale |")
            lines.append("| --- | --- | --- | --- |")
            for row in rows:
                lines.append(
                    f"| `{row['source_id']}` | `{row['family']}` | `{row['status']}` | {row['rationale']} |"
                )
        else:
            if item["level"] == "excluded":
                lines.append("- No excluded sources are recorded in the current source inventory.")
            else:
                lines.append("- No sources recorded in this category.")
        lines.append("")
    lines.extend(["## Negative Evidence", ""])
    if manifest["negative_evidence"]:
        lines.append("These search records found no relevant ontology to include and are preserved in the register.")
        lines.append("")
        lines.append("| Record | Surface | Surface type | Query | Results |")
        lines.append("| --- | --- | --- | --- | --- |")
        for row in manifest["negative_evidence"]:
            lines.append(
                f"| `{row['record_id']}` | `{row['surface']}` | `{row['surface_type']}` | {row['query']} | {row['result_count']} |"
            )
    else:
        lines.append("No negative-evidence search records are currently present.")
    lines.extend(
        [
            "",
            "## Quality Reference",
            "",
            f"- Ontology classes: {manifest['quality_metrics_reference']['summary']['classes']}",
            f"- Ontology properties: {manifest['quality_metrics_reference']['summary']['properties']}",
            f"- Example files: {manifest['quality_metrics_reference']['summary']['example_count']}",
            f"- Competency queries: {manifest['quality_metrics_reference']['summary']['query_count']}",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def markdown_table(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    header = rows[0]
    lines = ["| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * len(header)) + " |"]
    for row in rows[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def html_table(rows: list[list[str]], class_name: str = "") -> str:
    if not rows:
        return "<p>No rows.</p>"
    header, body = rows[0], rows[1:]
    parts = [f'<table class="{class_name}">', "<thead><tr>"]
    parts.extend(f"<th>{escape(cell)}</th>" for cell in header)
    parts.append("</tr></thead><tbody>")
    for row in body:
        parts.append("<tr>")
        parts.extend(f"<td>{cell}</td>" for cell in row)
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts)


def render_html(manifest: dict) -> str:
    summary_cards = []
    for item in manifest["source_evidence_summary"]:
        summary_cards.append(
            f'<div class="card"><div class="card-label">{escape(item["label"])}</div><div class="card-value">{item["count"]}</div></div>'
        )
    table_rows = [["Table", "Formats", "Validation gate", "Purpose"]]
    for item in manifest["validated_tables"]:
        table_rows.append([item["name"], escape(format_formats(item["formats"])), escape(item["validation_gate"]), escape(item["purpose"])])
    figure_rows = [["Figure", "Path", "Purpose"]]
    for item in manifest["validated_figures"]:
        figure_rows.append([item["name"], escape(item["path"]), escape(item["purpose"])])
    sections = []
    for item in manifest["source_evidence_summary"]:
        rows = manifest["sources_by_evidence_level"].get(item["level"], [])
        if rows:
            body = [["Source", "Family", "Status", "Rationale"]]
            for row in rows:
                body.append([
                    row["source_id"],
                    escape(row["family"] or ""),
                    escape(row["status"] or ""),
                    escape(row["rationale"] or ""),
                ])
            category_block = html_table(body, "data")
        else:
            note = "No excluded sources are recorded in the current source inventory." if item["level"] == "excluded" else "No sources recorded in this category."
            category_block = f"<p>{escape(note)}</p>"
        sections.append(
            f'<section class="category"><h3>{escape(item["label"])}</h3><p class="count">Count: {item["count"]}</p>{category_block}</section>'
        )
    neg_rows = manifest["negative_evidence"]
    if neg_rows:
        neg_body = [["Record", "Surface", "Surface type", "Query", "Results"]]
        for row in neg_rows:
            neg_body.append([
                row["record_id"],
                escape(row["surface"] or ""),
                escape(row["surface_type"] or ""),
                escape(row["query"] or ""),
                str(row["result_count"]),
            ])
        negative_block = html_table(neg_body, "data")
    else:
        negative_block = "<p>No negative-evidence search records are currently present.</p>"
    chart_max = max((item["count"] for item in manifest["source_evidence_summary"]), default=1) or 1
    chart_bars = []
    for item in manifest["source_evidence_summary"]:
        width = max(4, int((item["count"] / chart_max) * 100)) if chart_max else 4
        chart_bars.append(
            f'<div class="bar-row"><span class="bar-label">{escape(item["label"])}</span><div class="bar-track"><div class="bar-fill" style="width:{width}%"></div></div><span class="bar-value">{item["count"]}</span></div>'
        )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Article Evidence Dashboard</title>
  <style>
    body {{ font-family: Segoe UI, Arial, sans-serif; margin: 24px; background: #f7f8fb; color: #1f2937; }}
    h1, h2, h3 {{ margin: 0 0 12px 0; }}
    .lede {{ max-width: 980px; margin-bottom: 16px; }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; margin: 16px 0 24px; }}
    .card {{ background: white; border: 1px solid #dde3ea; border-radius: 8px; padding: 12px 14px; }}
    .card-label {{ font-size: 12px; text-transform: uppercase; letter-spacing: .02em; color: #6b7280; }}
    .card-value {{ font-size: 28px; font-weight: 700; margin-top: 6px; }}
    .panel {{ background: white; border: 1px solid #dde3ea; border-radius: 8px; padding: 16px; margin: 0 0 16px 0; }}
    .chart {{ display: grid; gap: 8px; margin-top: 8px; }}
    .bar-row {{ display: grid; grid-template-columns: 180px 1fr 48px; gap: 12px; align-items: center; }}
    .bar-track {{ height: 12px; background: #e5e7eb; border-radius: 999px; overflow: hidden; }}
    .bar-fill {{ height: 100%; background: #2563eb; }}
    table.data {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
    table.data th, table.data td {{ border: 1px solid #e5e7eb; padding: 8px 10px; vertical-align: top; text-align: left; }}
    table.data th {{ background: #f3f4f6; }}
    .category {{ margin-top: 14px; }}
    .count {{ color: #6b7280; margin-top: -6px; }}
    code {{ background: #f3f4f6; padding: 2px 4px; border-radius: 4px; }}
  </style>
</head>
<body>
  <h1>Article Evidence Dashboard</h1>
  <p class="lede">This dashboard exposes only validated tables and figures from the article-hardening evidence package. Source lists are separated by parsed RDF, structured non-RDF, metadata-only, literature-only, and excluded evidence levels.</p>
  <div class="cards">{''.join(summary_cards)}</div>
  <div class="panel">
    <h2>Evidence-Level Profile</h2>
    <div class="chart">{''.join(chart_bars)}</div>
  </div>
  <div class="panel">
    <h2>Validated Tables</h2>
    {html_table(table_rows, "data")}
  </div>
  <div class="panel">
    <h2>Validated Figures</h2>
    {html_table(figure_rows, "data")}
  </div>
  <div class="panel">
    <h2>Source Evidence Categories</h2>
    {''.join(sections)}
  </div>
  <div class="panel">
    <h2>Negative Evidence</h2>
    {negative_block}
  </div>
  <div class="panel">
    <h2>Quality Reference</h2>
    <ul>
      <li>Ontology classes: {manifest['quality_metrics_reference']['summary']['classes']}</li>
      <li>Ontology properties: {manifest['quality_metrics_reference']['summary']['properties']}</li>
      <li>Example files: {manifest['quality_metrics_reference']['summary']['example_count']}</li>
      <li>Competency queries: {manifest['quality_metrics_reference']['summary']['query_count']}</li>
    </ul>
  </div>
</body>
</html>
"""
    return html


def main() -> None:
    manifest = build_manifest()
    md = render_markdown(manifest)
    html = render_html(manifest)
    write_json(DEFAULT_JSON, manifest)
    DEFAULT_MD.write_text(md, encoding="utf-8")
    DEFAULT_HTML.write_text(html, encoding="utf-8")
    print(f"Wrote {DEFAULT_MD.name}, {DEFAULT_HTML.name}, and {DEFAULT_JSON.name}")


if __name__ == "__main__":
    main()
