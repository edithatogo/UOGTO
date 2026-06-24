import argparse, json, re, sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote
from rdflib import Graph, Literal, RDF, RDFS, OWL, SKOS, URIRef

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
DEFAULT_INVENTORY = ROOT / "docs" / "ontology-comparison" / "source-inventory.json"
DEFAULT_PROVENANCE = ROOT / "docs" / "ontology-comparison" / "source-provenance.json"
DEFAULT_OUTPUT = ROOT / "docs" / "ontology-comparison" / "term-inventory.jsonl"
UOGTO_DIRS = [ROOT / "ontologies" / "core", ROOT / "ontologies" / "extensions", ROOT / "ontologies" / "alignments"]
TERM_TYPES = {OWL.Class:"class", RDFS.Class:"class", OWL.ObjectProperty:"object_property", OWL.DatatypeProperty:"datatype_property", OWL.AnnotationProperty:"annotation_property", RDF.Property:"property", OWL.NamedIndividual:"individual", SKOS.Concept:"skos_concept", OWL.Ontology:"ontology_metadata"}
LABELS = [RDFS.label, SKOS.prefLabel]
DEFS = [SKOS.definition, URIRef("http://purl.org/dc/terms/description")]
COMMENTS = [RDFS.comment]
SYNONYMS = [SKOS.altLabel, URIRef("http://www.geneontology.org/formats/oboInOwl#hasExactSynonym")]
PARENTS = [RDFS.subClassOf, RDFS.subPropertyOf, SKOS.broader]
STOPWORDS = {"a","an","and","are","as","by","for","from","in","into","is","of","on","or","the","to","with"}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def local_name(value):
    text = str(value)
    text = text.rsplit("#", 1)[-1] if "#" in text else text.rstrip("/").rsplit("/", 1)[-1]
    return unquote(text)


def split_identifier(text):
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text or "")
    return re.findall(r"[A-Za-z][A-Za-z0-9]*|[0-9]+", text.replace("_", " ").replace("-", " "))


def tokens(*values):
    seen, out = set(), []
    for value in values:
        for token in split_identifier(value):
            low = token.lower()
            if low and low not in STOPWORDS and low not in seen:
                seen.add(low); out.append(low)
    return out


def literals(graph, subject, predicates):
    return sorted({str(obj) for pred in predicates for obj in graph.objects(subject, pred) if isinstance(obj, Literal)})


def iris(graph, subject, predicates):
    return sorted({str(obj) for pred in predicates for obj in graph.objects(subject, pred) if isinstance(obj, URIRef)})


def infer_type(graph, subject):
    rdf_types = set(graph.objects(subject, RDF.type))
    for rdf_type, label in TERM_TYPES.items():
        if rdf_type in rdf_types:
            return label
    if any(graph.objects(subject, RDFS.subClassOf)):
        return "class"
    if any(graph.objects(subject, RDFS.subPropertyOf)):
        return "property"
    return None


def make_row(source_id, source_name, family, source_kind, artifact_path, term_iri, term_type, label, definitions=None, comments=None, synonyms=None, parents=None, domains=None, ranges=None, imports=None):
    definitions, comments, synonyms = definitions or [], comments or [], synonyms or []
    normalised = tokens(label, local_name(term_iri), " ".join(synonyms))
    return {"source_id":source_id, "source_name":source_name, "source_family":family, "source_kind":source_kind, "artifact_path":artifact_path, "term_iri":term_iri, "local_name":local_name(term_iri), "term_type":term_type, "label":label, "definitions":definitions, "comments":comments, "synonyms":synonyms, "parents":parents or [], "domains":domains or [], "ranges":ranges or [], "imports":imports or [], "normalised_label":" ".join(normalised), "tokens":normalised, "language":"en"}


def extract_rdf(path, source_id, source_name, family, source_kind):
    graph = Graph(); graph.parse(path)
    artifact = path.resolve().relative_to(ROOT).as_posix()
    subjects = sorted({s for s in graph.subjects() if isinstance(s, URIRef) and (infer_type(graph, s) or literals(graph, s, LABELS + DEFS + COMMENTS))}, key=str)
    rows = []
    for subject in subjects:
        labels = literals(graph, subject, LABELS)
        rows.append(make_row(source_id, source_name, family, source_kind, artifact, str(subject), infer_type(graph, subject) or "resource", labels[0] if labels else local_name(subject), literals(graph, subject, DEFS), literals(graph, subject, COMMENTS), literals(graph, subject, SYNONYMS), iris(graph, subject, PARENTS), iris(graph, subject, [RDFS.domain]), iris(graph, subject, [RDFS.range]), iris(graph, subject, [OWL.imports])))
    return rows


def metadata_row(source, provenance):
    iri = source.get("artifact_url") or source["source_url"]
    return make_row(source["id"], source["name"], source["family"], "external_metadata", provenance.get("local_path") if provenance else None, iri, "source_metadata", source["name"], [source.get("inclusion_rationale", "")], [f"Expected format: {source.get('expected_format','')}", f"Candidate type: {source.get('candidate_type','')}", f"Licence disposition: {source.get('licence_disposition','')}"] , [source["family"], source.get("candidate_type", "")])


def uogto_files():
    for directory in UOGTO_DIRS:
        for path in sorted(directory.glob("*.ttl")):
            yield path, f"uogto_{directory.name}_{path.stem}", directory.name


def build_terms(inventory, provenance):
    by_id = {r["id"]: r for r in provenance["sources"]}
    rows = []
    for path, source_id, family in uogto_files():
        rows.extend(extract_rdf(path, source_id, path.stem, family, "uogto"))
    for source in inventory["sources"]:
        record = by_id.get(source["id"], {})
        if record.get("retrieval_mode") == "downloaded" and record.get("local_path"):
            rows.extend(extract_rdf(ROOT / record["local_path"], source["id"], source["name"], source["family"], "external_rdf"))
        else:
            rows.append(metadata_row(source, record))
    return sorted(rows, key=lambda r: (r["source_kind"], r["source_id"], r["term_type"], r["term_iri"]))


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate_rows(rows):
    required = {"source_id","source_name","source_family","source_kind","artifact_path","term_iri","term_type","label","definitions","comments","synonyms","parents","domains","ranges","imports","normalised_label","tokens","language"}
    if not rows:
        raise AssertionError("Term inventory must not be empty")
    for idx, row in enumerate(rows):
        missing = required - set(row)
        if missing:
            raise AssertionError(f"Row {idx} missing fields: {sorted(missing)}")
        if not row["source_id"] or not row["term_iri"] or not row["term_type"]:
            raise AssertionError(f"Row {idx} has blank identifiers")
        if not isinstance(row["tokens"], list):
            raise AssertionError(f"Row {idx} tokens must be a list")
    return {"row_count":len(rows), "source_count":len({r['source_id'] for r in rows}), "by_kind":dict(sorted(Counter(r["source_kind"] for r in rows).items()))}


def main():
    parser = argparse.ArgumentParser(description="Extract and normalise UOGTO/external comparison terms.")
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--provenance", type=Path, default=DEFAULT_PROVENANCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    rows = read_jsonl(args.output) if args.check_only else build_terms(load_json(args.inventory), load_json(args.provenance))
    if not args.check_only:
        write_jsonl(args.output, rows)
    summary = validate_rows(rows)
    print(f"Ontology comparison term inventory valid: {summary['row_count']} rows, {summary['source_count']} sources.")

if __name__ == "__main__":
    main()
