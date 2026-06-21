import sys
# Set stdout encoding to UTF-8 to prevent unicode map console output errors on windows shells
sys.stdout.reconfigure(encoding='utf-8')

import glob
import rdflib
from rdflib import RDF, RDFS, OWL

SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")

def audit_semantics():
    ttl_files = glob.glob("ontologies/**/*.ttl", recursive=True)
    if not ttl_files:
        print("No ontology TTL files found to audit.")
        return True

    print(f"Auditing semantic labels & definitions across {len(ttl_files)} files...")
    all_conforms = True
    
    for ttl in ttl_files:
        g = rdflib.Graph()
        try:
            g.parse(ttl, format="turtle")
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
                
    if all_conforms:
        print("Semantic completeness audit passed! All terms have rdfs:label and skos:definition.")
        return True
    else:
        print("Semantic completeness audit failed. Please add missing metadata annotations.")
        return False

if __name__ == "__main__":
    if not audit_semantics():
        sys.exit(1)
