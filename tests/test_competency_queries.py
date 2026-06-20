import glob
from rdflib import Graph

def test_competency_queries():
    # Load all ontology files
    ont_g = Graph()
    for ttl in glob.glob("ontologies/**/*.ttl", recursive=True):
        ont_g.parse(ttl, format="turtle")
        
    for query_file in glob.glob("competency-questions/*.rq"):
        with open(query_file, "r", encoding="utf-8") as f:
            query_text = f.read()
        try:
            ont_g.query(query_text)
        except Exception as e:
            assert False, f"Competency query {query_file} failed to compile/run: {e}"
