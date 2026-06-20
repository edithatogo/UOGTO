import os
import sys
import glob
from rdflib import Graph
from pyshacl import validate as shacl_validate

def main():
    print("Validating UOGTO Repository...")
    
    # 1. Parse all Turtle files
    g = Graph()
    ttl_files = glob.glob("ontologies/**/*.ttl", recursive=True)
    for ttl in ttl_files:
        try:
            g.parse(ttl, format="turtle")
            print(f"OK: Parsed {ttl}")
        except Exception as e:
            print(f"FAIL: Parse error in {ttl}: {e}")
            sys.exit(1)
            
    # 2. Parse SHACL files
    shacl_g = Graph()
    shacl_files = glob.glob("shapes/*.ttl")
    for shacl in shacl_files:
        try:
            shacl_g.parse(shacl, format="turtle")
            print(f"OK: Parsed SHACL shape {shacl}")
        except Exception as e:
            print(f"FAIL: Parse error in SHACL {shacl}: {e}")
            sys.exit(1)

    # 3. Validate examples with SHACL
    example_files = glob.glob("examples/*")
    for ex in example_files:
        ex_g = Graph()
        fmt = "turtle" if ex.endswith(".ttl") else "json-ld"
        try:
            ex_g.parse(ex, format=fmt)
            print(f"OK: Parsed example {ex} as {fmt}")
        except Exception as e:
            print(f"FAIL: Parse error in example {ex}: {e}")
            sys.exit(1)
            
        # Validate against SHACL
        # Combine example graph and ontologies to resolve types correctly
        combined = g + ex_g
        conforms, results_graph, results_text = shacl_validate(
            combined,
            shacl_graph=shacl_g,
            ont_graph=g,
            inference='rdfs'
        )
        if conforms:
            print(f"OK: Example {ex} validated successfully with SHACL.")
        else:
            print(f"FAIL: Example {ex} failed SHACL validation:\\n{results_text}")
            sys.exit(1)

    # 4. Run basic SPARQL queries
    cq_files = glob.glob("competency-questions/*.rq")
    for cq in cq_files:
        try:
            with open(cq, "r", encoding="utf-8") as f:
                query_text = f.read()
            # Test query execution on the combined graph
            res = g.query(query_text)
            print(f"OK: Executed competency query {cq} (returned {len(res)} results)")
        except Exception as e:
            print(f"FAIL: Competency query {cq} failed to execute: {e}")
            sys.exit(1)

    print("All validations completed successfully!")

if __name__ == "__main__":
    main()
