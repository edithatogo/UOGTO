import argparse, csv, json, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.maintenance import extract_comparison_terms
from scripts.maintenance import build_ontology_comparison_inventory
from scripts.maintenance import harvest_comparison_sources

DEFAULT_TERMS = ROOT / "docs" / "ontology-comparison" / "term-inventory.jsonl"
DEFAULT_REVIEW = ROOT / "docs" / "ontology-comparison" / "mapping-review.csv"
DEFAULT_INVENTORY = ROOT / "docs" / "ontology-comparison" / "source-inventory.json"
DEFAULT_PROVENANCE = ROOT / "docs" / "ontology-comparison" / "source-provenance.json"
DEFAULT_OUTPUT = ROOT / "docs" / "ontology-comparison" / "overlap-metrics.json"


def load_review(path=DEFAULT_REVIEW):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_lookup(inventory):
    return {source["id"]: source for source in inventory["sources"]}


def provenance_lookup(provenance):
    return {record["id"]: record for record in provenance["sources"]}


def term_index(rows):
    by_source = defaultdict(list)
    by_iri = {}
    for row in rows:
        by_source[row["source_id"]].append(row)
        by_iri[row["term_iri"]] = row
    return by_source, by_iri


def annotation_complete(row):
    return bool(row.get("label")) and bool(row.get("definitions"))


def source_summary(source_id, rows, source_meta=None, provenance=None):
    type_counts = Counter(row["term_type"] for row in rows)
    annotated = sum(1 for row in rows if annotation_complete(row))
    with_parents = sum(1 for row in rows if row.get("parents"))
    properties = sum(1 for row in rows if "property" in row["term_type"])
    imports = sum(len(row.get("imports") or []) for row in rows)
    return {
        "source_id": source_id,
        "source_name": source_meta.get("name", source_id) if source_meta else rows[0].get("source_name", source_id),
        "family": source_meta.get("family", rows[0].get("source_family")) if source_meta else rows[0].get("source_family"),
        "source_kind": rows[0].get("source_kind"),
        "term_count": len(rows),
        "term_type_distribution": dict(sorted(type_counts.items())),
        "annotation_completeness": round(annotated / len(rows), 4) if rows else 0,
        "hierarchy_parent_term_count": with_parents,
        "property_density": round(properties / len(rows), 4) if rows else 0,
        "import_count": imports,
        "licence_disposition": source_meta.get("licence_disposition") if source_meta else None,
        "parse_status": provenance.get("parse_status") if provenance else None,
        "retrieval_mode": provenance.get("retrieval_mode") if provenance else None,
    }


def review_summaries(review_rows):
    by_source = defaultdict(Counter)
    by_pair = defaultdict(Counter)
    for row in review_rows:
        by_source[row["source_id"]][row["review_status"]] += 1
        by_pair[(row["source_id"], row["uogto_source_id"])][row["review_status"]] += 1
    source_summary_rows = {}
    for source_id, counts in sorted(by_source.items()):
        total = sum(counts.values())
        accepted = counts.get("accepted", 0)
        reviewed = accepted + counts.get("rejected", 0)
        source_summary_rows[source_id] = {
            "candidate_count": total,
            "accepted": accepted,
            "rejected": counts.get("rejected", 0),
            "needs_domain_review": counts.get("needs_domain_review", 0),
            "deferred": counts.get("defer_until_source_clarified", 0),
            "accepted_candidate_rate": round(accepted / total, 4) if total else 0,
            "review_precision": round(accepted / reviewed, 4) if reviewed else None,
        }
    pair_rows = []
    for (source_id, uogto_source_id), counts in sorted(by_pair.items()):
        pair_rows.append({"source_id": source_id, "uogto_source_id": uogto_source_id, "candidate_count": sum(counts.values()), "accepted": counts.get("accepted", 0), "needs_domain_review": counts.get("needs_domain_review", 0), "rejected": counts.get("rejected", 0)})
    return source_summary_rows, pair_rows


def overlap_sets(review_rows):
    source_terms = defaultdict(set)
    uogto_terms = set()
    accepted_source_terms = defaultdict(set)
    accepted_uogto_terms = set()
    candidate_source_terms = defaultdict(set)
    candidate_uogto_terms = set()
    for row in review_rows:
        candidate_source_terms[row["source_id"]].add(row["source_term_iri"])
        candidate_uogto_terms.add(row["uogto_term_iri"])
        if row["review_status"] == "accepted":
            accepted_source_terms[row["source_id"]].add(row["source_term_iri"])
            accepted_uogto_terms.add(row["uogto_term_iri"])
    return candidate_source_terms, candidate_uogto_terms, accepted_source_terms, accepted_uogto_terms


def build_metrics(terms, review_rows, inventory, provenance):
    by_source, by_iri = term_index(terms)
    sources = source_lookup(inventory)
    provenance_by_id = provenance_lookup(provenance)
    review_by_source, pair_rows = review_summaries(review_rows)
    candidate_source_terms, candidate_uogto_terms, accepted_source_terms, accepted_uogto_terms = overlap_sets(review_rows)
    external_sources = sorted(sources)
    uogto_terms = [row for row in terms if row["source_kind"] == "uogto"]
    external_terms = [row for row in terms if row["source_kind"] != "uogto"]
    source_coverage = {}
    for source_id in external_sources:
        rows = by_source.get(source_id, [])
        source_coverage[source_id] = {
            "term_count": len(rows),
            "candidate_term_count": len(candidate_source_terms.get(source_id, set())),
            "accepted_term_count": len(accepted_source_terms.get(source_id, set())),
            "candidate_coverage": round(len(candidate_source_terms.get(source_id, set())) / len(rows), 4) if rows else 0,
            "accepted_coverage": round(len(accepted_source_terms.get(source_id, set())) / len(rows), 4) if rows else 0,
        }
    uogto_coverage = {
        "term_count": len(uogto_terms),
        "candidate_term_count": len(candidate_uogto_terms),
        "accepted_term_count": len(accepted_uogto_terms),
        "candidate_coverage": round(len(candidate_uogto_terms) / len(uogto_terms), 4) if uogto_terms else 0,
        "accepted_coverage": round(len(accepted_uogto_terms) / len(uogto_terms), 4) if uogto_terms else 0,
    }
    unmatched_source_concepts = []
    for row in external_terms:
        if row["term_iri"] not in candidate_source_terms.get(row["source_id"], set()):
            unmatched_source_concepts.append({"source_id": row["source_id"], "term_iri": row["term_iri"], "label": row["label"], "term_type": row["term_type"]})
    uogto_unique = []
    for row in uogto_terms:
        if row["term_iri"] not in candidate_uogto_terms:
            uogto_unique.append({"source_id": row["source_id"], "term_iri": row["term_iri"], "label": row["label"], "term_type": row["term_type"]})
    family_counts = defaultdict(Counter)
    for row in review_rows:
        family = sources.get(row["source_id"], {}).get("family", row["source_id"])
        family_counts[family][row["review_status"]] += 1
    source_summaries = {sid: source_summary(sid, rows, sources.get(sid), provenance_by_id.get(sid)) for sid, rows in sorted(by_source.items())}
    enhancement_candidates = sorted([
        {"source_id": sid, "unmatched_terms": source_coverage[sid]["term_count"] - source_coverage[sid]["candidate_term_count"], "candidate_coverage": source_coverage[sid]["candidate_coverage"]}
        for sid in external_sources
    ], key=lambda item: (-item["unmatched_terms"], item["source_id"]))[:10]
    stronger_uogto_areas = Counter(row["source_id"] for row in uogto_unique).most_common(10)
    return {
        "schema": "uogto.ontology-comparison.overlap-metrics.v1",
        "summary": {"external_source_count": len(external_sources), "external_term_count": len(external_terms), "uogto_term_count": len(uogto_terms), "review_candidate_count": len(review_rows), "accepted_mapping_count": sum(1 for row in review_rows if row["review_status"] == "accepted")},
        "source_coverage": source_coverage,
        "uogto_coverage": uogto_coverage,
        "bidirectional_overlap": {"source_by_uogto": pair_rows, "source_review_summaries": review_by_source},
        "term_type_coverage": {"external": dict(sorted(Counter(row["term_type"] for row in external_terms).items())), "uogto": dict(sorted(Counter(row["term_type"] for row in uogto_terms).items()))},
        "domain_module_coverage": dict(sorted(Counter(row["uogto_source_id"] for row in review_rows if row["review_status"] == "accepted").items())),
        "source_cluster_overlap": {family: dict(sorted(counts.items())) for family, counts in sorted(family_counts.items())},
        "unmatched_source_concepts": unmatched_source_concepts[:250],
        "uogto_unique_concepts": uogto_unique[:250],
        "descriptive_summaries": source_summaries,
        "licence_coverage": dict(sorted(Counter(source.get("licence_disposition") for source in sources.values()).items())),
        "parse_status_coverage": dict(sorted(Counter(record.get("parse_status") for record in provenance.get("sources", [])).items())),
        "recommended_uogto_enhancement_areas": enhancement_candidates,
        "uogto_stronger_coverage_areas": [{"uogto_source_id": sid, "unique_terms": count} for sid, count in stronger_uogto_areas],
    }


def write_json(path, packet):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_metrics(packet):
    if packet.get("schema") != "uogto.ontology-comparison.overlap-metrics.v1":
        raise AssertionError("Unexpected overlap metrics schema")
    for key in ["source_coverage", "uogto_coverage", "bidirectional_overlap", "term_type_coverage", "descriptive_summaries"]:
        if key not in packet:
            raise AssertionError(f"Missing metrics section {key}")
    if packet["summary"]["external_source_count"] <= 0 or packet["summary"]["uogto_term_count"] <= 0:
        raise AssertionError("Metrics must include external and UOGTO terms")
    if "source_by_uogto" not in packet["bidirectional_overlap"]:
        raise AssertionError("Missing source_by_uogto overlap rows")
    return {"external_sources": packet["summary"]["external_source_count"], "accepted_mapping_count": packet["summary"]["accepted_mapping_count"]}


def main():
    parser = argparse.ArgumentParser(description="Analyse ontology overlap and descriptive coverage metrics.")
    parser.add_argument("--terms", type=Path, default=DEFAULT_TERMS)
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--provenance", type=Path, default=DEFAULT_PROVENANCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if args.check_only:
        packet = json.loads(args.output.read_text(encoding="utf-8"))
    else:
        inventory = build_ontology_comparison_inventory.load_inventory(args.inventory)
        provenance = harvest_comparison_sources.load_json(args.provenance) if hasattr(harvest_comparison_sources, "load_json") else json.loads(args.provenance.read_text(encoding="utf-8"))
        packet = build_metrics(extract_comparison_terms.read_jsonl(args.terms), load_review(args.review), inventory, provenance)
        write_json(args.output, packet)
    summary = validate_metrics(packet)
    print(f"Ontology overlap metrics valid: {summary['external_sources']} external sources, {summary['accepted_mapping_count']} accepted mappings.")

if __name__ == "__main__":
    main()
