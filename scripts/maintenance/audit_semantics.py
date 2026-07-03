import sys
# Set stdout encoding to UTF-8 to prevent unicode map console output errors on windows shells
sys.stdout.reconfigure(encoding='utf-8')

import glob
import json
import re
import rdflib
from rdflib import RDF, RDFS, OWL

SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
ROOT = "https://w3id.org/uogto/"
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def local_name(uri):
    return str(uri).rstrip("/").split("/")[-1].split("#")[-1]


def context_terms():
    terms = set()
    for path in ["jsonld/core.context.jsonld", "jsonld/extensions.context.jsonld"]:
        with open(path, "r", encoding="utf-8") as handle:
            terms.update(json.load(handle).get("@context", {}).keys())
    return terms


def jsonld_example_terms():
    used = set()

    def visit(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key == "@type":
                    if isinstance(item, list):
                        used.update(str(entry) for entry in item)
                    else:
                        used.add(str(item))
                elif not key.startswith("@"):
                    used.add(key)
                visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    for path in glob.glob("examples/*.jsonld"):
        with open(path, "r", encoding="utf-8") as handle:
            visit(json.load(handle))
    return used

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
            merged += g
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

    object_properties = set(merged.subjects(RDF.type, OWL.ObjectProperty))
    datatype_properties = set(merged.subjects(RDF.type, OWL.DatatypeProperty))
    overlap = {prop for prop in object_properties & datatype_properties if str(prop).startswith(ROOT)}
    if overlap:
        print("Properties typed as both ObjectProperty and DatatypeProperty:")
        for prop in sorted(overlap, key=str):
            print(f"  - {prop}")
        all_conforms = False

    allowed_uogto_roots = (
        "https://w3id.org/uogto/core",
        "https://w3id.org/uogto/core#",
        "https://w3id.org/uogto/core/",
        "https://w3id.org/uogto/extensions",
        "https://w3id.org/uogto/extensions#",
        "https://w3id.org/uogto/extensions/",
        "https://w3id.org/uogto/alignments/",
    )
    for subject in set(merged.subjects()):
        value = str(subject)
        if value.startswith("https://w3id.org/uogto/") and not value.startswith(allowed_uogto_roots):
            print(f"Unexpected UOGTO namespace outside core/extensions: {subject}")
            all_conforms = False

    missing_context_terms = sorted(jsonld_example_terms() - context_terms())
    if missing_context_terms:
        print(f"JSON-LD examples use terms missing from contexts: {missing_context_terms}")
        all_conforms = False

    for path in glob.glob("examples/*"):
        g = rdflib.Graph()
        fmt = "turtle" if path.endswith(".ttl") else "json-ld"
        g.parse(path, format=fmt)
        for subject in g.subjects():
            if isinstance(subject, rdflib.term.URIRef) and str(subject).startswith("http://example.org/"):
                name = local_name(subject)
                if not KEBAB.match(name):
                    print(f"Example instance is not kebab-case in {path}: {subject}")
                    all_conforms = False

    if all_conforms:
        print("Semantic completeness audit passed! All terms have rdfs:label and skos:definition.")
        return True
    else:
        print("Semantic completeness audit failed. Please add missing metadata annotations.")
        return False

if __name__ == "__main__":
    if not audit_semantics():
        sys.exit(1)
