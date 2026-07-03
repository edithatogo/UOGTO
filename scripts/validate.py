import sys
import glob
import json
from pathlib import Path

from rdflib import Graph
from pyshacl import validate as shacl_validate


ROOT = Path(__file__).resolve().parents[1]


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

    validate_competency_query_expectations(g)

    print("All validations completed successfully!")


def validate_competency_query_expectations(ontology_graph):
    manifest_path = ROOT / "validation" / "competency-query-expectations.json"
    if not manifest_path.exists():
        print(f"FAIL: Missing competency-query expectation manifest {manifest_path}")
        sys.exit(1)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for entry in manifest.get("queries", []):
        query_path = ROOT / "competency-questions" / entry["query"]
        if not query_path.exists():
            print(f"FAIL: Expected competency query is missing: {query_path}")
            sys.exit(1)
        query_graph = Graph()
        query_graph += ontology_graph
        for example in entry.get("example_graphs", []):
            example_path = ROOT / example
            if not example_path.exists():
                print(f"FAIL: Example graph is missing: {example_path}")
                sys.exit(1)
            fmt = "json-ld" if example_path.suffix == ".jsonld" else "turtle"
            query_graph.parse(example_path, format=fmt)
        rows = list(query_graph.query(query_path.read_text(encoding="utf-8")))
        min_count = int(entry.get("min_count", 0))
        if len(rows) < min_count:
            print(
                f"FAIL: Competency query {entry['query']} returned {len(rows)} "
                f"rows; expected at least {min_count}."
            )
            sys.exit(1)
        binding_names = [str(var) for var in rows[0].labels] if rows else []
        row_bindings = [
            {binding_names[index]: str(value) for index, value in enumerate(row)}
            for row in rows
        ]
        for required in entry.get("required_bindings", []):
            if required not in row_bindings:
                print(
                    f"FAIL: Competency query {entry['query']} did not return "
                    f"required binding {required}."
                )
                sys.exit(1)
        print(
            f"OK: Competency query {entry['query']} satisfied expected "
            f"results ({len(rows)} rows)."
        )


def validate_competency_expectations(ontology_graph):
    validate_competency_query_expectations(ontology_graph)


if __name__ == "__main__":
    main()
