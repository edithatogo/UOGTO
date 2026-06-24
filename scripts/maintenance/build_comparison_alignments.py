import argparse, csv, hashlib, json, sys
from collections import Counter
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import DCTERMS, OWL, SKOS, XSD

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.maintenance import generate_ontology_mapping_candidates as candidates

DEFAULT_CANDIDATES = ROOT / "docs" / "ontology-comparison" / "mapping-candidates.jsonl"
DEFAULT_REVIEW = ROOT / "docs" / "ontology-comparison" / "mapping-review.csv"
DEFAULT_ALIGNMENTS = ROOT / "docs" / "ontology-comparison" / "accepted-alignments.ttl"
UOGTO_ALIGN = Namespace("https://w3id.org/uogto/alignments/comparison#")
APPROVED_PREDICATES = {
    "skos:exactMatch": SKOS.exactMatch,
    "skos:closeMatch": SKOS.closeMatch,
    "skos:broadMatch": SKOS.broadMatch,
    "skos:narrowMatch": SKOS.narrowMatch,
    "skos:relatedMatch": SKOS.relatedMatch,
    "owl:equivalentClass": OWL.equivalentClass,
    "owl:equivalentProperty": OWL.equivalentProperty,
    "rdfs:subClassOf": RDFS.subClassOf,
    "rdfs:subPropertyOf": RDFS.subPropertyOf,
}
REVIEW_STATUSES = {"accepted", "rejected", "needs_domain_review", "out_of_scope", "defer_until_source_clarified"}
FIELDNAMES = [
    "candidate_id", "source_id", "source_term_iri", "source_label", "source_term_type",
    "uogto_source_id", "uogto_term_iri", "uogto_label", "uogto_term_type", "candidate_predicate",
    "confidence", "review_status", "decision_predicate", "reviewer", "review_rationale", "review_flags", "evidence_json"
]


def read_candidates(path=DEFAULT_CANDIDATES):
    return candidates.read_jsonl(path)


def candidate_id(candidate):
    raw = "|".join([candidate["source_term_iri"], candidate["uogto_term_iri"], candidate["candidate_predicate"]])
    return "candidate-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def prefill_decision(candidate):
    predicate = candidate["candidate_predicate"]
    confidence = float(candidate["confidence"])
    flags = set(candidate.get("review_flags", []))
    if predicate == "no_match":
        return "rejected", "", "automation_prefill", "Rejected because candidate generator classified this pair as no_match."
    if "metadata_only_source" in flags:
        return "defer_until_source_clarified", "", "automation_prefill", "Deferred until source artifact or domain review is available for metadata-only source."
    if confidence >= 0.53 and predicate in {"owl:equivalentClass", "owl:equivalentProperty", "skos:exactMatch"}:
        return "accepted", predicate, "automation_prefill", "Accepted by deterministic exact/equivalent prefill; high-impact rows remain flagged for reviewer attention."
    if confidence >= 0.55:
        return "needs_domain_review", predicate, "automation_prefill", "Needs domain review because confidence is plausible but below automatic acceptance threshold."
    return "needs_domain_review", predicate, "automation_prefill", "Needs domain review because confidence is low or evidence is incomplete."


def review_rows(candidate_rows):
    rows = []
    for candidate in sorted(candidate_rows, key=lambda c: (c["source_id"], -float(c["confidence"]), c["source_term_iri"], c["uogto_term_iri"])):
        status, decision_predicate, reviewer, rationale = prefill_decision(candidate)
        rows.append({
            "candidate_id": candidate_id(candidate),
            "source_id": candidate["source_id"],
            "source_term_iri": candidate["source_term_iri"],
            "source_label": candidate["source_label"],
            "source_term_type": candidate["source_term_type"],
            "uogto_source_id": candidate["uogto_source_id"],
            "uogto_term_iri": candidate["uogto_term_iri"],
            "uogto_label": candidate["uogto_label"],
            "uogto_term_type": candidate["uogto_term_type"],
            "candidate_predicate": candidate["candidate_predicate"],
            "confidence": candidate["confidence"],
            "review_status": status,
            "decision_predicate": decision_predicate,
            "reviewer": reviewer,
            "review_rationale": rationale,
            "review_flags": ";".join(candidate.get("review_flags", [])),
            "evidence_json": json.dumps(candidate["evidence"], sort_keys=True),
        })
    return rows


def write_review_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader(); writer.writerows(rows)


def read_review_csv(path=DEFAULT_REVIEW):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_review_rows(rows):
    if not rows:
        raise AssertionError("Mapping review CSV must contain rows")
    statuses = Counter()
    for index, row in enumerate(rows):
        missing = [field for field in FIELDNAMES if field not in row]
        if missing:
            raise AssertionError(f"Review row {index} missing fields: {missing}")
        if row["review_status"] not in REVIEW_STATUSES:
            raise AssertionError(f"Review row {index} has invalid status")
        if row["decision_predicate"] and row["decision_predicate"] not in APPROVED_PREDICATES:
            raise AssertionError(f"Review row {index} has invalid decision predicate")
        if row["review_status"] == "accepted" and not row["decision_predicate"]:
            raise AssertionError(f"Accepted review row {index} requires decision_predicate")
        statuses[row["review_status"]] += 1
    return {"row_count": len(rows), "by_status": dict(sorted(statuses.items()))}


def build_alignment_graph(rows):
    graph = Graph()
    graph.bind("uogtoalign", UOGTO_ALIGN)
    graph.bind("skos", SKOS)
    graph.bind("owl", OWL)
    graph.bind("rdfs", RDFS)
    graph.bind("dcterms", DCTERMS)
    graph.add((UOGTO_ALIGN.accepted_alignments, RDF.type, OWL.Ontology))
    graph.add((UOGTO_ALIGN.accepted_alignments, RDFS.label, Literal("UOGTO comparative ontology accepted alignments", lang="en")))
    graph.add((UOGTO_ALIGN.accepted_alignments, DCTERMS.description, Literal("Accepted review-backed alignments generated from docs/ontology-comparison/mapping-review.csv.", lang="en")))
    for row in rows:
        if row["review_status"] != "accepted":
            continue
        predicate = APPROVED_PREDICATES[row["decision_predicate"]]
        source = URIRef(row["source_term_iri"])
        target = URIRef(row["uogto_term_iri"])
        graph.add((source, predicate, target))
        assertion = UOGTO_ALIGN[row["candidate_id"].replace("candidate-", "mapping-")]
        graph.add((assertion, RDF.type, UOGTO_ALIGN.MappingAssertion))
        graph.add((assertion, UOGTO_ALIGN.sourceTerm, source))
        graph.add((assertion, UOGTO_ALIGN.uogtoTerm, target))
        graph.add((assertion, UOGTO_ALIGN.mappingPredicate, URIRef(predicate)))
        graph.add((assertion, UOGTO_ALIGN.confidence, Literal(row["confidence"], datatype=XSD.decimal)))
        graph.add((assertion, UOGTO_ALIGN.reviewStatus, Literal(row["review_status"])))
        graph.add((assertion, UOGTO_ALIGN.reviewRationale, Literal(row["review_rationale"])))
    return graph


def write_alignment_ttl(path, rows):
    graph = build_alignment_graph(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(graph.serialize(format="turtle"), encoding="utf-8")
    parsed = Graph(); parsed.parse(path, format="turtle")
    return len(graph)


def validate_alignment_ttl(path=DEFAULT_ALIGNMENTS):
    graph = Graph(); graph.parse(path, format="turtle")
    allowed = set(APPROVED_PREDICATES.values())
    mapping_count = 0
    for _, predicate, _ in graph:
        if predicate in allowed:
            mapping_count += 1
    if mapping_count == 0:
        raise AssertionError("Accepted alignment TTL must contain at least one accepted mapping triple")
    return {"triple_count": len(graph), "mapping_count": mapping_count}


def main():
    parser = argparse.ArgumentParser(description="Build mapping review CSV and accepted alignment TTL.")
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--alignments", type=Path, default=DEFAULT_ALIGNMENTS)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    rows = read_review_csv(args.review) if args.check_only else review_rows(read_candidates(args.candidates))
    if not args.check_only:
        write_review_csv(args.review, rows)
        write_alignment_ttl(args.alignments, rows)
    review_summary = validate_review_rows(rows)
    ttl_summary = validate_alignment_ttl(args.alignments)
    print(f"Ontology mapping review valid: {review_summary['row_count']} rows; accepted alignment triples: {ttl_summary['mapping_count']}.")

if __name__ == "__main__":
    main()
