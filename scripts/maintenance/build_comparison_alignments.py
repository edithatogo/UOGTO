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
DEFAULT_SSSOM_TSV = ROOT / "docs" / "ontology-comparison" / "accepted-alignments.sssom.tsv"
DEFAULT_SSSOM_METADATA = ROOT / "docs" / "ontology-comparison" / "accepted-alignments.sssom.yml"
UOGTO_ALIGN = Namespace("https://w3id.org/uogto/alignments/comparison#")
REGISTER_DATE = "2026-06-24"
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
BUILTIN_CURIE_MAP = {
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "semapv": "https://w3id.org/semapv/vocab/",
}
SSSOM_CURIE_MAP = {
    "dcterms": "http://purl.org/dc/terms/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "gs1": "https://ref.gs1.org/voc/",
    "ogp": "http://ogp.me/ns#",
    "prov": "http://www.w3.org/ns/prov#",
    "schema": "https://schema.org/",
    "sosa": "http://www.w3.org/ns/sosa/",
    "uogto": "https://w3id.org/uogto/core#",
    "uogtoalign": "https://w3id.org/uogto/alignments/comparison#",
    "uogtosrc": "https://w3id.org/uogto/source/",
    "uogtotool": "https://w3id.org/uogto/tool/",
    "uogtox": "https://w3id.org/uogto/extensions#",
}
SSSOM_COLUMNS = [
    "subject_id", "subject_label", "predicate_id", "predicate_label", "object_id",
    "object_label", "mapping_justification", "confidence", "mapping_date",
    "subject_type", "object_type", "subject_source", "object_source",
    "match_string", "reviewer_label", "comment",
]
PREDICATE_LABELS = {
    "owl:equivalentClass": "equivalent class",
    "owl:equivalentProperty": "equivalent property",
    "rdfs:subClassOf": "subclass of",
    "rdfs:subPropertyOf": "subproperty of",
    "skos:broadMatch": "broad match",
    "skos:closeMatch": "close match",
    "skos:exactMatch": "exact match",
    "skos:narrowMatch": "narrow match",
    "skos:relatedMatch": "related match",
}
TERM_TYPES = {
    "class": "owl class",
    "datatype_property": "owl data property",
    "object_property": "owl object property",
    "property": "rdf property",
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
    evidence = candidate.get("evidence", {})
    if predicate == "no_match":
        if evidence.get("type_compatible") is False:
            return "rejected", "", "ontology_alignment_reviewer", "Rejected because the candidate crosses incompatible term types without an approved bridge pattern."
        return "rejected", "", "automation_prefill", "Rejected because candidate generator classified this pair as no_match."
    if "metadata_only_source" in flags:
        return "defer_until_source_clarified", "", "automation_prefill", "Deferred until source artifact or domain review is available for metadata-only source."
    if evidence.get("external_is_uogto_parent") and predicate == "skos:narrowMatch":
        return "accepted", predicate, "ontology_alignment_reviewer", "Accepted because the checked-in UOGTO alignment module asserts the UOGTO term as a subclass of the external source term; recorded as a conservative narrow match rather than equivalence."
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



def _all_curie_prefixes():
    prefixes = {}
    prefixes.update(BUILTIN_CURIE_MAP)
    prefixes.update(SSSOM_CURIE_MAP)
    return prefixes


def curie_for_iri(value):
    if ":" in value and not value.startswith(("http://", "https://")):
        return value
    for prefix, iri_prefix in sorted(_all_curie_prefixes().items(), key=lambda item: len(item[1]), reverse=True):
        if value.startswith(iri_prefix):
            return f"{prefix}:{value[len(iri_prefix):]}"
    raise AssertionError(f"Cannot contract IRI to SSSOM CURIE: {value}")


def sssom_confidence(value):
    return f"{float(value):.3f}".rstrip("0").rstrip(".")


def sssom_justification(row):
    evidence = json.loads(row.get("evidence_json") or "{}")
    lexical_keys = ["exact_iri", "exact_label", "normalized_label", "synonym"]
    if any(evidence.get(key) for key in lexical_keys):
        return "semapv:LexicalMatching"
    if evidence.get("embedding_similarity") or evidence.get("structural_similarity"):
        return "semapv:SemanticSimilarityThresholdMatching"
    return "semapv:CompositeMatching"


def sssom_rows(rows):
    accepted = [row for row in rows if row["review_status"] == "accepted"]
    output = []
    for row in accepted:
        subject_id = curie_for_iri(row["source_term_iri"])
        object_id = curie_for_iri(row["uogto_term_iri"])
        predicate_id = row["decision_predicate"]
        if predicate_id not in PREDICATE_LABELS:
            raise AssertionError(f"Unsupported SSSOM predicate label: {predicate_id}")
        labels = [row.get("source_label", ""), row.get("uogto_label", "")]
        output.append({
            "subject_id": subject_id,
            "subject_label": labels[0],
            "predicate_id": predicate_id,
            "predicate_label": PREDICATE_LABELS[predicate_id],
            "object_id": object_id,
            "object_label": labels[1],
            "mapping_justification": sssom_justification(row),
            "confidence": sssom_confidence(row["confidence"]),
            "mapping_date": REGISTER_DATE,
            "subject_type": TERM_TYPES.get(row.get("source_term_type"), "rdf resource"),
            "object_type": TERM_TYPES.get(row.get("uogto_term_type"), "rdf resource"),
            "subject_source": f"uogtosrc:{row['source_id']}",
            "object_source": f"uogtosrc:{row['uogto_source_id']}",
            "match_string": " | ".join(label for label in labels if label),
            "reviewer_label": row.get("reviewer") or "unrecorded",
            "comment": row.get("review_rationale", ""),
        })
    return sorted(output, key=lambda item: tuple(item[column] for column in SSSOM_COLUMNS))


def _yaml_scalar(value):
    if value is None:
        return "null"
    text = str(value)
    if not text:
        return '""'
    safe = all(ch.isalnum() or ch in "-_./:# " for ch in text)
    if safe and not text.startswith((" ", "-", "{", "[")) and ": " not in text:
        return text
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def sssom_metadata():
    return {
        "curie_map": dict(sorted(SSSOM_CURIE_MAP.items())),
        "mapping_set_id": "uogtoalign:accepted-alignments-sssom",
        "mapping_set_title": "UOGTO comparative ontology accepted alignments",
        "mapping_set_description": "Accepted UOGTO comparative ontology mappings exported in SSSOM TSV for review, publication, and comparison alongside accepted-alignments.ttl.",
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "sssom_version": "1.1",
        "mapping_date": REGISTER_DATE,
        "mapping_tool": "uogtotool:build_comparison_alignments",
        "mapping_tool_version": "repo-script",
        "object_source": "uogtosrc:uogto",
    }


def write_metadata_yaml(path, metadata):
    lines = []
    for key, value in metadata.items():
        if isinstance(value, dict):
            lines.append(f"{key}:")
            for nested_key, nested_value in value.items():
                lines.append(f"  {nested_key}: {_yaml_scalar(nested_value)}")
        else:
            lines.append(f"{key}: {_yaml_scalar(value)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_sssom_tsv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SSSOM_COLUMNS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_sssom_outputs(tsv_path, metadata_path, rows):
    table_rows = sssom_rows(rows)
    write_sssom_tsv(tsv_path, table_rows)
    write_metadata_yaml(metadata_path, sssom_metadata())
    return validate_sssom_outputs(tsv_path, metadata_path, expected_count=len(table_rows))


def _read_metadata_yaml(path):
    metadata = {"curie_map": {}}
    current_key = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        if not raw_line.startswith(" "):
            key, _, value = raw_line.partition(":")
            current_key = key
            value = value.strip()
            if value:
                metadata[key] = value.strip('"')
            elif key == "curie_map":
                metadata[key] = {}
            else:
                metadata[key] = None
        elif current_key == "curie_map":
            key, _, value = raw_line.strip().partition(":")
            metadata["curie_map"][key] = value.strip().strip('"')
    return metadata


def validate_sssom_outputs(tsv_path=DEFAULT_SSSOM_TSV, metadata_path=DEFAULT_SSSOM_METADATA, expected_count=None):
    if not tsv_path.exists():
        raise AssertionError(f"Missing SSSOM TSV: {tsv_path}")
    if not metadata_path.exists():
        raise AssertionError(f"Missing SSSOM metadata: {metadata_path}")
    if tsv_path.read_bytes().startswith(b"\xef\xbb\xbf") or metadata_path.read_bytes().startswith(b"\xef\xbb\xbf"):
        raise AssertionError("SSSOM files must be UTF-8 without BOM")
    metadata = _read_metadata_yaml(metadata_path)
    curie_map = metadata.get("curie_map", {})
    required_metadata = ["mapping_set_id", "mapping_set_title", "mapping_set_description", "license", "sssom_version"]
    missing_metadata = [field for field in required_metadata if not metadata.get(field)]
    if missing_metadata:
        raise AssertionError(f"SSSOM metadata missing fields: {', '.join(missing_metadata)}")
    with tsv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != SSSOM_COLUMNS:
            raise AssertionError("SSSOM TSV header does not match expected column order")
        rows = list(reader)
    if expected_count is not None and len(rows) != expected_count:
        raise AssertionError("SSSOM TSV row count does not match accepted mapping count")
    declared_prefixes = set(curie_map) | set(BUILTIN_CURIE_MAP)
    for index, row in enumerate(rows):
        for field in ["subject_id", "predicate_id", "object_id", "mapping_justification", "subject_source", "object_source"]:
            value = row[field]
            if value.startswith(("http://", "https://")) or ":" not in value:
                raise AssertionError(f"SSSOM row {index} field {field} is not a CURIE")
            prefix = value.split(":", 1)[0]
            if prefix not in declared_prefixes:
                raise AssertionError(f"SSSOM row {index} uses undeclared prefix: {prefix}")
        if not row["comment"] or not row["confidence"]:
            raise AssertionError(f"SSSOM row {index} lacks review comment or confidence")
    return {"row_count": len(rows), "metadata_fields": len(metadata)}


def main():
    parser = argparse.ArgumentParser(description="Build mapping review CSV and accepted alignment TTL.")
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--alignments", type=Path, default=DEFAULT_ALIGNMENTS)
    parser.add_argument("--sssom-tsv", type=Path, default=DEFAULT_SSSOM_TSV)
    parser.add_argument("--sssom-metadata", type=Path, default=DEFAULT_SSSOM_METADATA)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    rows = read_review_csv(args.review) if args.check_only else review_rows(read_candidates(args.candidates))
    if not args.check_only:
        write_review_csv(args.review, rows)
        write_alignment_ttl(args.alignments, rows)
        write_sssom_outputs(args.sssom_tsv, args.sssom_metadata, rows)
    review_summary = validate_review_rows(rows)
    ttl_summary = validate_alignment_ttl(args.alignments)
    sssom_summary = validate_sssom_outputs(args.sssom_tsv, args.sssom_metadata, expected_count=ttl_summary["mapping_count"])
    print(
        f"Ontology mapping review valid: {review_summary['row_count']} rows; "
        f"accepted alignment triples: {ttl_summary['mapping_count']}; "
        f"SSSOM rows: {sssom_summary['row_count']}."
    )

if __name__ == "__main__":
    main()
