import sys
# Set stdout encoding to UTF-8 to prevent unicode map console output errors on windows shells
sys.stdout.reconfigure(encoding='utf-8')

import glob
import json
import re
from pathlib import Path

import rdflib
from rdflib import RDF, RDFS, OWL

SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
ROOT = Path(__file__).resolve().parents[2]
CORE_NS = "https://w3id.org/uogto/core#"
EXT_NS = "https://w3id.org/uogto/extensions#"
INSTANCE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

def audit_semantics():
    ttl_files = glob.glob("ontologies/**/*.ttl", recursive=True)
    if not ttl_files:
        print("No ontology TTL files found to audit.")
        return True

    print(f"Auditing semantic labels & definitions across {len(ttl_files)} files...")
    all_conforms = True
    
    merged = rdflib.Graph()
    for ttl in ttl_files:
        g = rdflib.Graph()
        try:
            g.parse(ttl, format="turtle")
            for triple in g:
                merged.add(triple)
        except Exception as e:
            print(f"Error parsing file {ttl}: {e}")
            all_conforms = False
            continue
            
        # Target subjects of type owl:Class, owl:ObjectProperty, owl:DatatypeProperty
        subjects = set()
        for t in [OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty]:
            for s in g.subjects(RDF.type, t):
                # Filter out external namespaces/imports
                if str(s).startswith("https://w3id.org/uogto"):
                    subjects.add(s)
                    
        for s in subjects:
            has_label = list(g.objects(s, RDFS.label))
            has_definition = list(g.objects(s, SKOS.definition))
            
            # Warn if missing metadata
            term_name = str(s).split('/')[-1].split('#')[-1]
            if not has_label:
                print(f"Missing label in {ttl} for term: {term_name} (<{s}>)")
                all_conforms = False
            if not has_definition:
                print(f"Missing definition in {ttl} for term: {term_name} (<{s}>)")
                all_conforms = False

    if not audit_namespace_policy(merged):
        all_conforms = False
    if not audit_property_separation(merged):
        all_conforms = False
    if not audit_jsonld_term_coverage(merged):
        all_conforms = False
    if not audit_instance_naming():
        all_conforms = False

    if all_conforms:
        print("Semantic completeness audit passed! Metadata, namespaces, property typing, JSON-LD coverage, and instance naming are valid.")
        return True
    else:
        print("Semantic completeness audit failed. Please add missing metadata annotations.")
        return False


def audit_namespace_policy(graph):
    conforms = True
    for subject in graph.subjects(RDF.type, OWL.Class):
        value = str(subject)
        if value.startswith("https://w3id.org/uogto/") and not (
            value.startswith(CORE_NS) or value.startswith(EXT_NS)
        ):
            print(f"Invalid UOGTO namespace for class: {subject}")
            conforms = False
    return conforms


def audit_property_separation(graph):
    object_properties = set(graph.subjects(RDF.type, OWL.ObjectProperty))
    datatype_properties = set(graph.subjects(RDF.type, OWL.DatatypeProperty))
    overlap = object_properties & datatype_properties
    for prop in sorted(overlap):
        print(f"Property is both owl:ObjectProperty and owl:DatatypeProperty: {prop}")
    return not overlap


def audit_jsonld_term_coverage(graph):
    context_terms = {}
    for context_path in [ROOT / "jsonld/core.context.jsonld", ROOT / "jsonld/extensions.context.jsonld"]:
        context = json.loads(context_path.read_text(encoding="utf-8"))["@context"]
        for term, value in context.items():
            if isinstance(value, str):
                context_terms[value] = term
            elif isinstance(value, dict) and "@id" in value:
                context_terms[value["@id"]] = term

    missing = []
    for kind in [OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty]:
        for subject in graph.subjects(RDF.type, kind):
            value = str(subject)
            if value.startswith(CORE_NS):
                compact = "uogto:" + value.removeprefix(CORE_NS)
            elif value.startswith(EXT_NS):
                compact = "uogtox:" + value.removeprefix(EXT_NS)
            else:
                continue
            if compact not in context_terms:
                missing.append(compact)

    for term in sorted(set(missing)):
        print(f"JSON-LD context missing term coverage for {term}")
    return not missing


def audit_instance_naming():
    conforms = True
    examples_dir = ROOT / "examples"
    if not examples_dir.exists():
        return True
    for path in examples_dir.iterdir():
        if not path.is_file() or path.suffix not in (".jsonld", ".ttl"):
            continue
        graph = rdflib.Graph()
        fmt = "json-ld" if path.suffix == ".jsonld" else "turtle"
        graph.parse(path, format=fmt)
        for subject in set(graph.subjects()):
            if not isinstance(subject, rdflib.URIRef):
                continue
            value = str(subject)
            if "example.org/" not in value:
                continue
            local = value.rstrip("/").split("/")[-1].split("#")[-1]
            if not INSTANCE_RE.match(local):
                print(f"Example instance is not kebab-case in {path}: {subject}")
                conforms = False
    return conforms

if __name__ == "__main__":
    if not audit_semantics():
        sys.exit(1)
