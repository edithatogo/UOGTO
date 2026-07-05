import argparse, json, math, sys
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.maintenance import extract_comparison_terms

DEFAULT_TERMS = ROOT / "docs" / "ontology-comparison" / "term-inventory.jsonl"
DEFAULT_OUTPUT = ROOT / "docs" / "ontology-comparison" / "mapping-candidates.jsonl"
APPROVED_PREDICATES = {"skos:exactMatch", "skos:closeMatch", "skos:broadMatch", "skos:narrowMatch", "skos:relatedMatch", "owl:equivalentClass", "owl:equivalentProperty", "rdfs:subClassOf", "rdfs:subPropertyOf", "no_match"}
TYPE_COMPAT = {
    "class": {"class", "skos_concept", "source_metadata", "resource"},
    "skos_concept": {"class", "skos_concept", "source_metadata", "resource"},
    "object_property": {"object_property", "property", "datatype_property", "resource"},
    "datatype_property": {"datatype_property", "property", "object_property", "resource"},
    "property": {"property", "object_property", "datatype_property", "resource"},
    "source_metadata": {"class", "skos_concept", "ontology_metadata", "resource"},
    "ontology_metadata": {"ontology_metadata", "class", "resource"},
}


def read_terms(path=DEFAULT_TERMS):
    return extract_comparison_terms.read_jsonl(path)


def token_set(row):
    return set(row.get("tokens") or [])


def text_blob(row, fields=("label", "normalised_label", "definitions", "comments", "synonyms")):
    parts = []
    for field in fields:
        value = row.get(field)
        if isinstance(value, list):
            parts.extend(str(item) for item in value)
        elif value:
            parts.append(str(value))
    return " ".join(parts).lower()


def jaccard(left, right):
    if not left and not right:
        return 0.0
    return len(left & right) / len(left | right) if (left | right) else 0.0


def cosine_counter(left, right):
    if not left or not right:
        return 0.0
    dot = sum(left[k] * right.get(k, 0) for k in left)
    left_norm = math.sqrt(sum(v * v for v in left.values()))
    right_norm = math.sqrt(sum(v * v for v in right.values()))
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0


def token_counter(row):
    return Counter((row.get("tokens") or []) + extract_comparison_terms.tokens(text_blob(row)))


def type_compatible(external, uogto):
    allowed = TYPE_COMPAT.get(external.get("term_type"), {external.get("term_type"), "resource"})
    return uogto.get("term_type") in allowed


def signature_score(external, uogto):
    left = token_set({"tokens": extract_comparison_terms.tokens(" ".join(external.get("domains", []) + external.get("ranges", [])))})
    right = token_set({"tokens": extract_comparison_terms.tokens(" ".join(uogto.get("domains", []) + uogto.get("ranges", [])))})
    return jaccard(left, right)


def hierarchy_score(external, uogto):
    left = token_set({"tokens": extract_comparison_terms.tokens(" ".join(external.get("parents", [])))})
    right = token_set({"tokens": extract_comparison_terms.tokens(" ".join(uogto.get("parents", [])))})
    return jaccard(left, right)


def evidence_features(external, uogto):
    ext_tokens, uogto_tokens = token_set(external), token_set(uogto)
    exact_iri = external["term_iri"] == uogto["term_iri"]
    exact_label = external["label"].strip().lower() == uogto["label"].strip().lower()
    normalized_label = external.get("normalised_label") and external.get("normalised_label") == uogto.get("normalised_label")
    external_is_uogto_parent = external["term_iri"] in set(uogto.get("parents", []))
    synonym_match = bool({s.lower() for s in external.get("synonyms", [])} & ({uogto["label"].lower()} | {s.lower() for s in uogto.get("synonyms", [])}))
    lexical = max(SequenceMatcher(None, external.get("normalised_label", ""), uogto.get("normalised_label", "")).ratio(), jaccard(ext_tokens, uogto_tokens))
    definition = SequenceMatcher(None, text_blob(external, ("definitions",)), text_blob(uogto, ("definitions",))).ratio() if external.get("definitions") and uogto.get("definitions") else 0.0
    structural = max(hierarchy_score(external, uogto), signature_score(external, uogto))
    embedding = cosine_counter(token_counter(external), token_counter(uogto))
    compatible = type_compatible(external, uogto)
    reliability = 1.0 if external.get("source_kind") == "external_rdf" else 0.62
    return {"exact_iri": exact_iri, "exact_label": exact_label, "normalized_label": bool(normalized_label), "synonym": synonym_match, "lexical_similarity": round(lexical, 4), "definition_similarity": round(definition, 4), "structural_similarity": round(max(structural, 1.0 if external_is_uogto_parent else 0.0), 4), "property_signature_similarity": round(signature_score(external, uogto), 4), "embedding_similarity": round(embedding, 4), "type_compatible": compatible, "source_reliability": reliability, "external_is_uogto_parent": external_is_uogto_parent}


def confidence(features):
    score = 0.0
    score += 0.46 if features["external_is_uogto_parent"] else 0
    score += 0.25 if features["exact_iri"] else 0
    score += 0.18 if features["exact_label"] else 0
    score += 0.15 if features["normalized_label"] else 0
    score += 0.10 if features["synonym"] else 0
    score += 0.14 * features["lexical_similarity"]
    score += 0.08 * features["definition_similarity"]
    score += 0.05 * features["structural_similarity"]
    score += 0.05 * features["embedding_similarity"]
    score += 0.03 if features["type_compatible"] else -0.08
    score *= features["source_reliability"]
    return round(max(0.0, min(1.0, score)), 4)


def classify(external, uogto, features, score):
    if not features["type_compatible"]:
        return "no_match"
    if features["exact_iri"]:
        return "owl:equivalentProperty" if "property" in external["term_type"] else "owl:equivalentClass"
    if features["external_is_uogto_parent"]:
        return "skos:narrowMatch"
    if score >= 0.50 and features["type_compatible"] and (features["exact_label"] or features["normalized_label"]):
        return "owl:equivalentProperty" if "property" in external["term_type"] else "owl:equivalentClass"
    if score >= 0.62:
        return "skos:exactMatch" if features["exact_label"] or features["normalized_label"] else "skos:closeMatch"
    if score >= 0.42:
        if external["term_type"] == "source_metadata":
            return "skos:relatedMatch"
        if len(token_set(external)) > len(token_set(uogto)) + 1:
            return "skos:narrowMatch"
        if len(token_set(uogto)) > len(token_set(external)) + 1:
            return "skos:broadMatch"
        return "skos:relatedMatch"
    return "no_match"


def index_uogto(rows):
    index = defaultdict(set)
    uogto_rows = [row for row in rows if row["source_kind"] == "uogto"]
    for i, row in enumerate(uogto_rows):
        for key in [row.get("normalised_label"), row.get("local_name", "").lower(), row.get("label", "").lower()]:
            if key:
                index[("text", key)].add(i)
        for token in row.get("tokens", []):
            index[("token", token)].add(i)
        for parent in row.get("parents", []):
            index[("parent_iri", parent)].add(i)
        for synonym in row.get("synonyms", []):
            index[("text", synonym.lower())].add(i)
        index[("type", row.get("term_type"))].add(i)
    return uogto_rows, index


def plausible_uogto_indices(external, uogto_rows, index, max_candidates=80):
    hits = Counter()
    for key in [external.get("normalised_label"), external.get("local_name", "").lower(), external.get("label", "").lower()]:
        for idx in index.get(("text", key), set()):
            hits[idx] += 6
    for synonym in external.get("synonyms", []):
        for idx in index.get(("text", synonym.lower()), set()):
            hits[idx] += 4
    for idx in index.get(("parent_iri", external["term_iri"]), set()):
        hits[idx] += 10
    for token in external.get("tokens", []):
        for idx in index.get(("token", token), set()):
            hits[idx] += 2
    for idx in index.get(("type", external.get("term_type")), set()):
        hits[idx] += 1
    if not hits:
        return []
    return [idx for idx, _ in sorted(hits.items(), key=lambda item: (-item[1], uogto_rows[item[0]]["term_iri"]))[:max_candidates]]


def make_candidate(external, uogto):
    features = evidence_features(external, uogto)
    score = confidence(features)
    predicate = classify(external, uogto, features, score)
    review_flags = []
    if score < 0.5:
        review_flags.append("low_confidence")
    if external["source_kind"] == "external_metadata":
        review_flags.append("metadata_only_source")
    if predicate in {"owl:equivalentClass", "owl:equivalentProperty", "skos:exactMatch"} and score < 0.8:
        review_flags.append("high_impact_requires_review")
    return {"source_id": external["source_id"], "source_term_iri": external["term_iri"], "source_label": external["label"], "source_term_type": external["term_type"], "uogto_source_id": uogto["source_id"], "uogto_term_iri": uogto["term_iri"], "uogto_label": uogto["label"], "uogto_term_type": uogto["term_type"], "candidate_predicate": predicate, "confidence": score, "evidence": features, "review_flags": review_flags, "status": "candidate"}


def generate_candidates(rows, per_source_limit=120):
    uogto_rows, index = index_uogto(rows)
    external_rows = [row for row in rows if row["source_kind"] != "uogto"]
    candidates = []
    per_source = Counter()
    seen = set()
    for external in sorted(external_rows, key=lambda r: (r["source_id"], r["term_iri"])):
        local = []
        for idx in plausible_uogto_indices(external, uogto_rows, index):
            candidate = make_candidate(external, uogto_rows[idx])
            if candidate["candidate_predicate"] != "no_match" or candidate["confidence"] >= 0.12:
                local.append(candidate)
        local.sort(key=lambda c: (-c["confidence"], c["source_term_iri"], c["uogto_term_iri"]))
        emitted_for_external = 0
        for candidate in local:
            key = (candidate["source_term_iri"], candidate["uogto_term_iri"])
            if key not in seen and per_source[candidate["source_id"]] < per_source_limit:
                seen.add(key); per_source[candidate["source_id"]] += 1; candidates.append(candidate)
                emitted_for_external += 1
                if emitted_for_external >= 10:
                    break
    return sorted(candidates, key=lambda c: (c["source_id"], -c["confidence"], c["source_term_iri"], c["uogto_term_iri"]))


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate_candidates(rows):
    required = {"source_id", "source_term_iri", "source_label", "source_term_type", "uogto_source_id", "uogto_term_iri", "uogto_label", "uogto_term_type", "candidate_predicate", "confidence", "evidence", "review_flags", "status"}
    if not rows:
        raise AssertionError("Mapping candidates must not be empty")
    for index, row in enumerate(rows):
        missing = required - set(row)
        if missing:
            raise AssertionError(f"Candidate {index} missing fields: {sorted(missing)}")
        if row["candidate_predicate"] not in APPROVED_PREDICATES:
            raise AssertionError(f"Candidate {index} has invalid predicate")
        if not 0 <= row["confidence"] <= 1:
            raise AssertionError(f"Candidate {index} confidence out of range")
        for feature in ["lexical_similarity", "definition_similarity", "structural_similarity", "property_signature_similarity", "embedding_similarity", "source_reliability"]:
            if feature not in row["evidence"]:
                raise AssertionError(f"Candidate {index} missing evidence feature {feature}")
    return {"candidate_count": len(rows), "source_count": len({r["source_id"] for r in rows}), "by_predicate": dict(sorted(Counter(r["candidate_predicate"] for r in rows).items()))}


def main():
    parser = argparse.ArgumentParser(description="Generate deterministic ontology mapping candidates.")
    parser.add_argument("--terms", type=Path, default=DEFAULT_TERMS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    rows = read_jsonl(args.output) if args.check_only else generate_candidates(read_terms(args.terms))
    if not args.check_only:
        write_jsonl(args.output, rows)
    summary = validate_candidates(rows)
    print(f"Ontology mapping candidates valid: {summary['candidate_count']} candidates across {summary['source_count']} sources.")

if __name__ == "__main__":
    main()
