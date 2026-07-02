import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "docs" / "article-hardening"
CSV_PATH = OUT_DIR / "candidate-decision-ledger.csv"
JSON_PATH = OUT_DIR / "candidate-decision-ledger.json"
MD_PATH = OUT_DIR / "candidate-decision-ledger.md"


ASSUMPTIONS_AND_HEURISTICS = [
    {
        "area": "search-route screening",
        "statement": (
            "Routes were screened at the evidence-surface level. A route can be included even when "
            "individual sources remain metadata-only, licence-constrained, or deferred for later acquisition."
        ),
    },
    {
        "area": "source inclusion",
        "statement": (
            "Sources were retained when they exposed game, agent, simulation, execution, provenance, "
            "time, process, planning, system-modelling, mapping, or ontology-quality semantics relevant "
            "to UOGTO. Retention does not imply parsed RDF availability or semantic equivalence."
        ),
    },
    {
        "area": "source exclusion",
        "statement": (
            "The negative-evidence route records searched-but-not-found evidence. Exclusion means no "
            "additional releasable source was found for that route, not that the domain was unsearched."
        ),
    },
    {
        "area": "mapping-candidate generation",
        "statement": (
            "Mapping candidates were generated from deterministic lexical, normalized-label, definition, "
            "embedding, structural, property-signature, source-reliability, synonym, exact-IRI, exact-label, "
            "and type-compatibility signals."
        ),
    },
    {
        "area": "mapping acceptance",
        "statement": (
            "Accepted mappings are intentionally conservative. Rejected rows remain audit evidence and "
            "should not be counted as missing UOGTO concepts without domain review."
        ),
    },
    {
        "area": "ontology-inclusion dispositions",
        "statement": (
            "Candidate ontology additions are triaged into add, align externally, defer, duplicate reject, "
            "out-of-scope reject, or domain review. A domain-review disposition is a stop signal for direct "
            "assertion, not a rejection of relevance."
        ),
    },
]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def compact_json(value) -> str:
    if value in (None, "", [], {}):
        return ""
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def decision_class(scope: str, status: str) -> str:
    normalized = (status or "").lower()
    if normalized in {"included", "accepted", "add_to_uogto", "align_external_only"}:
        return "included"
    if normalized in {"rejected", "reject_out_of_scope", "reject_as_duplicate", "negative_evidence_no_relevant_ontology_found"}:
        return "excluded"
    if "review" in normalized or "defer" in normalized:
        return "needs_review"
    if scope == "search_route" and "included" in normalized:
        return "included"
    return "documented"


def route_rows() -> list[dict]:
    rows = []
    for record in read_jsonl(ROOT / "docs" / "article-hardening" / "search-log.jsonl"):
        status = record.get("screening_decision", "")
        rows.append(
            {
                "candidate_scope": "search_route",
                "candidate_id": record.get("record_id", ""),
                "candidate_label": record.get("query", ""),
                "source_id": "",
                "source_family": record.get("surface_type", ""),
                "evidence_level": record.get("evidence_level", ""),
                "candidate_type": record.get("surface_type", ""),
                "decision_status": status,
                "decision_class": decision_class("search_route", status),
                "decision_predicate": "",
                "rationale": record.get("inclusion_rationale", ""),
                "assumptions_or_heuristics": record.get("route_limitations", ""),
                "reviewer_or_role": ",".join(record.get("reviewer_handoff", {}).get("assigned_roles", [])),
                "source_artifact": "docs/article-hardening/search-log.jsonl",
                "linked_artifact": record.get("surface", ""),
                "evidence_detail": compact_json(
                    {
                        "filters": record.get("filters", {}),
                        "result_count": record.get("result_count"),
                        "screened_count": record.get("screened_count"),
                        "included_count": record.get("included_count"),
                        "source_ids_added": record.get("source_ids_added", []),
                    }
                ),
            }
        )
    return rows


def source_rows() -> list[dict]:
    inventory = read_json(ROOT / "docs" / "article-hardening" / "source-extension-inventory.json")
    rows = []
    for source in inventory["sources"]:
        status = source.get("inclusion_status", "")
        rows.append(
            {
                "candidate_scope": "source_candidate",
                "candidate_id": source.get("source_id", ""),
                "candidate_label": source.get("source_name", ""),
                "source_id": source.get("source_id", ""),
                "source_family": source.get("source_family", ""),
                "evidence_level": source.get("evidence_level", ""),
                "candidate_type": source.get("source_type", ""),
                "decision_status": status,
                "decision_class": decision_class("source_candidate", status),
                "decision_predicate": source.get("article_use_category", ""),
                "rationale": source.get("inclusion_rationale", ""),
                "assumptions_or_heuristics": source.get("limitations", ""),
                "reviewer_or_role": ",".join(source.get("reviewer_handoff", {}).get("assigned_roles", [])),
                "source_artifact": "docs/article-hardening/source-extension-inventory.json",
                "linked_artifact": source.get("canonical_url", ""),
                "evidence_detail": compact_json(
                    {
                        "parseability": source.get("parseability"),
                        "licence": source.get("licence", {}),
                        "mapping_relevance": source.get("mapping_relevance"),
                        "uogto_module_relevance": source.get("uogto_module_relevance", []),
                        "search_record_ids": source.get("search_record_ids", []),
                    }
                ),
            }
        )
    return rows


def mapping_rows() -> list[dict]:
    path = ROOT / "docs" / "ontology-comparison" / "mapping-review.csv"
    rows = []
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            status = row.get("review_status", "")
            rows.append(
                {
                    "candidate_scope": "mapping_candidate",
                    "candidate_id": row.get("candidate_id", ""),
                    "candidate_label": f"{row.get('source_label', '')} -> {row.get('uogto_label', '')}",
                    "source_id": row.get("source_id", ""),
                    "source_family": row.get("uogto_source_id", ""),
                    "evidence_level": "mapping_review",
                    "candidate_type": row.get("candidate_predicate", ""),
                    "decision_status": status,
                    "decision_class": decision_class("mapping_candidate", status),
                    "decision_predicate": row.get("decision_predicate", "") or row.get("candidate_predicate", ""),
                    "rationale": row.get("review_rationale", ""),
                    "assumptions_or_heuristics": "Candidate score combines lexical, definitional, structural, property-signature, embedding, source-reliability, and type-compatibility signals.",
                    "reviewer_or_role": row.get("reviewer", ""),
                    "source_artifact": "docs/ontology-comparison/mapping-review.csv",
                    "linked_artifact": row.get("source_term_iri", ""),
                    "evidence_detail": row.get("evidence_json", ""),
                }
            )
    return rows


def inclusion_rows() -> list[dict]:
    payload = read_json(ROOT / "docs" / "article-hardening" / "uogto-inclusion-candidates.json")
    rows = []
    for row in payload["rows"]:
        status = row.get("disposition", "")
        rows.append(
            {
                "candidate_scope": "ontology_inclusion_candidate",
                "candidate_id": row.get("candidate_id", ""),
                "candidate_label": row.get("candidate_label", ""),
                "source_id": "",
                "source_family": row.get("source_family", ""),
                "evidence_level": row.get("evidence_level", ""),
                "candidate_type": "uogto_inclusion_candidate",
                "decision_status": status,
                "decision_class": decision_class("ontology_inclusion_candidate", status),
                "decision_predicate": row.get("mapped_to", ""),
                "rationale": row.get("rationale", ""),
                "assumptions_or_heuristics": "Disposition follows docs/article-hardening/uogto-inclusion-decisions.md.",
                "reviewer_or_role": row.get("reviewer_handoff", ""),
                "source_artifact": "docs/article-hardening/uogto-inclusion-candidates.json",
                "linked_artifact": row.get("source_title", ""),
                "evidence_detail": compact_json(
                    {
                        "uogto_target": row.get("uogto_target", ""),
                        "mapped_to": row.get("mapped_to", ""),
                    }
                ),
            }
        )
    return rows


def build_rows() -> list[dict]:
    return route_rows() + source_rows() + mapping_rows() + inclusion_rows()


def write_csv(rows: list[dict], path: Path | None = None) -> None:
    path = path or CSV_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def build_payload(rows: list[dict]) -> dict:
    return {
        "schema": "uogto.article-hardening.candidate-decision-ledger.v1",
        "generated_at_utc": "deterministic-local-preflight",
        "row_count": len(rows),
        "candidate_scope_counts": dict(sorted(Counter(row["candidate_scope"] for row in rows).items())),
        "decision_class_counts": dict(sorted(Counter(row["decision_class"] for row in rows).items())),
        "assumptions_and_heuristics": ASSUMPTIONS_AND_HEURISTICS,
        "source_artifacts": sorted({row["source_artifact"] for row in rows}),
        "rows": rows,
    }


def write_json(payload: dict, path: Path | None = None) -> None:
    path = path or JSON_PATH
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell).replace("|", "\\|") for cell in row) + " |")
    return "\n".join(lines)


def write_markdown(payload: dict, path: Path | None = None) -> None:
    path = path or MD_PATH
    rows = payload["rows"]
    scope_rows = [[scope, count] for scope, count in payload["candidate_scope_counts"].items()]
    decision_rows = [[status, count] for status, count in payload["decision_class_counts"].items()]
    source_route_rows = [
        [row["candidate_id"], row["decision_status"], row["rationale"]]
        for row in rows
        if row["candidate_scope"] == "search_route"
    ]
    source_candidate_rows = [
        [row["candidate_id"], row["candidate_label"], row["decision_status"], row["rationale"]]
        for row in rows
        if row["candidate_scope"] == "source_candidate"
    ]
    mapping_decisions = Counter(
        (row["decision_status"], row["decision_predicate"]) for row in rows if row["candidate_scope"] == "mapping_candidate"
    )
    mapping_rows_md = [[status, predicate, count] for (status, predicate), count in sorted(mapping_decisions.items())]

    content = [
        "# Candidate decision ledger",
        "",
        "Date: 2026-07-02",
        "",
        "This repository-only supplement joins the article-hardening source register, search log, mapping-review table, and UOGTO inclusion-candidate table into one decision ledger. It is intended to answer four audit questions:",
        "",
        "1. What candidates were considered?",
        "2. Which candidates were included, excluded, or left for review?",
        "3. What reason was recorded for each decision?",
        "4. What assumptions or heuristics governed those decisions?",
        "",
        "The full row-level ledger is available in:",
        "",
        "- `docs/article-hardening/candidate-decision-ledger.csv`",
        "- `docs/article-hardening/candidate-decision-ledger.json`",
        "",
        "## Scope counts",
        "",
        markdown_table(["Candidate scope", "Rows"], scope_rows),
        "",
        "## Decision-class counts",
        "",
        markdown_table(["Decision class", "Rows"], decision_rows),
        "",
        "## Assumptions and heuristics",
        "",
    ]
    for item in payload["assumptions_and_heuristics"]:
        content.append(f"- `{item['area']}`: {item['statement']}")

    content.extend(
        [
            "",
            "## Search-route decisions",
            "",
            markdown_table(["Route ID", "Decision", "Recorded rationale"], source_route_rows),
            "",
            "## Source-candidate decisions",
            "",
            "All source candidates are shown here because this table is short enough for review. Licence disposition, parseability, module relevance, and search-record links are retained in the CSV/JSON ledger.",
            "",
            markdown_table(["Source ID", "Source name", "Decision", "Recorded rationale"], source_candidate_rows),
            "",
            "## Mapping-candidate decisions",
            "",
            "The 460 mapping candidates are stored row-by-row in the CSV/JSON ledger. The summary below preserves the decision distribution without making the Markdown supplement unwieldy.",
            "",
            markdown_table(["Review status", "Decision predicate", "Rows"], mapping_rows_md),
            "",
            "## Ontology-inclusion candidate decisions",
            "",
            markdown_table(
                ["Candidate ID", "Candidate label", "Disposition", "Rationale"],
                [
                    [row["candidate_id"], row["candidate_label"], row["decision_status"], row["rationale"]]
                    for row in rows
                    if row["candidate_scope"] == "ontology_inclusion_candidate"
                ],
            ),
            "",
            "## Interpretation limits",
            "",
            "- `included` source rows describe retained evidence surfaces, not necessarily parsed RDF artefacts.",
            "- `excluded` mapping rows are negative evidence against a specific asserted mapping, not evidence that the source concept is irrelevant.",
            "- `needs_review` rows should not be promoted to ontology assertions without domain review and examples.",
            "- Candidate generation scores are deterministic heuristics; final ontology claims should use reviewed decisions, not raw similarity scores alone.",
            "",
            "## Source artefacts",
            "",
        ]
    )
    for artifact in payload["source_artifacts"]:
        content.append(f"- `{artifact}`")
    path.write_text("\n".join(content) + "\n", encoding="utf-8")


def build_outputs() -> dict:
    rows = build_rows()
    payload = build_payload(rows)
    write_csv(rows)
    write_json(payload)
    write_markdown(payload)
    return payload


def main() -> int:
    payload = build_outputs()
    print(f"Wrote candidate decision ledger with {payload['row_count']} rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
