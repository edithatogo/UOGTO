import os
import sys
import glob
from rdflib import Graph, RDF, OWL

def main():
    print("Generating Coverage Report...")
    ttl_files = glob.glob("ontologies/**/*.ttl", recursive=True)
    if not ttl_files:
        print("No ontology files found.")
        sys.exit(1)
        
    for ttl in ttl_files:
        g = Graph()
        g.parse(ttl, format="turtle")
        classes = list(g.subjects(RDF.type, OWL.Class))
        obj_properties = list(g.subjects(RDF.type, OWL.ObjectProperty))
        data_properties = list(g.subjects(RDF.type, OWL.DatatypeProperty))
        
        module_name = os.path.basename(ttl)
        print(f"Module: {module_name}")
        print(f"  Classes: {len(classes)}")
        print(f"  Object Properties: {len(obj_properties)}")
        print(f"  Datatype Properties: {len(data_properties)}")
        
        # Check constraints
        if "alignments" in ttl:
            if len(g) == 0:
                print(f"FAIL: Alignment module {module_name} is completely empty!")
                sys.exit(1)
        else:
            if len(classes) == 0 and len(obj_properties) == 0 and len(data_properties) == 0:
                print(f"FAIL: Module {module_name} is completely empty!")
                sys.exit(1)

            
    print("Coverage thresholds checking complete. All modules are populated.")

if __name__ == "__main__":
    main()
