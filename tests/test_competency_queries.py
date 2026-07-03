import glob
from rdflib import Graph
from scripts.validate import validate_competency_expectations

def test_competency_queries():
    graph = Graph()
    for ttl in glob.glob("ontologies/**/*.ttl", recursive=True):
        graph.parse(ttl, format="turtle")
    for example in glob.glob("examples/*"):
        fmt = "turtle" if example.endswith(".ttl") else "json-ld"
        graph.parse(example, format=fmt)

    for query_file in glob.glob("competency-questions/*.rq"):
        with open(query_file, "r", encoding="utf-8") as f:
            query_text = f.read()
        try:
            graph.query(query_text)
        except Exception as e:
            assert False, f"Competency query {query_file} failed to compile/run: {e}"

    validate_competency_expectations(graph)
