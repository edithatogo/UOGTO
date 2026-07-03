import os
import sys
import glob
import json
from rdflib import Graph
from pyshacl import validate as shacl_validate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CQ_EXPECTATIONS = os.path.join(ROOT, "competency-questions", "expected-results.json")


def parse_example(path):
    graph = Graph()
    fmt = "turtle" if path.endswith(".ttl") else "json-ld"
    graph.parse(path, format=fmt)
    return graph, fmt


def query_rows(graph, query_text):
    rows = []
    for row in graph.query(query_text):
        item = {}
        for key, value in row.asdict().items():
            item[key] = str(value)
        rows.append(item)
    return rows


def row_matches(row, expected):
    return all(row.get(key) == value for key, value in expected.items())


def validate_competency_expectations(graph):
    with open(CQ_EXPECTATIONS, "r", encoding="utf-8") as handle:
        packet = json.load(handle)

    for expectation in packet.get("queries", []):
        query_name = expectation["query"]
        query_path = os.path.join(ROOT, "competency-questions", query_name)
        with open(query_path, "r", encoding="utf-8") as handle:
            query_text = handle.read()
        rows = query_rows(graph, query_text)
        min_results = int(expectation.get("min_results", 0))
        if len(rows) < min_results:
            raise AssertionError(
                f"{query_name} returned {len(rows)} rows, expected at least {min_results}"
            )
        for binding in expectation.get("required_bindings", []):
            if not any(row_matches(row, binding) for row in rows):
                raise AssertionError(
                    f"{query_name} missing required binding {binding}; observed rows: {rows[:5]}"
                )
        print(f"OK: Competency query {query_name} met expected results ({len(rows)} rows)")


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
    examples_g = Graph()
    for ex in example_files:
        try:
            ex_g, fmt = parse_example(ex)
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
        examples_g += ex_g

    # 4. Run basic SPARQL queries
    competency_graph = g + examples_g
    cq_files = glob.glob("competency-questions/*.rq")
    for cq in cq_files:
        try:
            with open(cq, "r", encoding="utf-8") as f:
                query_text = f.read()
            # Test query execution on the combined graph
            res = competency_graph.query(query_text)
            print(f"OK: Executed competency query {cq} (returned {len(res)} results)")
        except Exception as e:
            print(f"FAIL: Competency query {cq} failed to execute: {e}")
            sys.exit(1)

    try:
        validate_competency_expectations(competency_graph)
    except Exception as e:
        print(f"FAIL: Competency query expected-result validation failed: {e}")
        sys.exit(1)

    print("All validations completed successfully!")

if __name__ == "__main__":
    main()
