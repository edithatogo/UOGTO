import glob
from rdflib import Graph
from pyshacl import validate as shacl_validate

def test_shacl_validation():
    # Load all ontology files
    ont_g = Graph()
    for ttl in glob.glob("ontologies/**/*.ttl", recursive=True):
        ont_g.parse(ttl, format="turtle")
        
    # Load all SHACL shape files
    shacl_g = Graph()
    for shape in glob.glob("shapes/*.ttl"):
        shacl_g.parse(shape, format="turtle")
        
    # Validate each example
    for ex in glob.glob("examples/*"):
        ex_g = Graph()
        fmt = "turtle" if ex.endswith(".ttl") else "json-ld"
        ex_g.parse(ex, format=fmt)
        
        # Combine
        combined = ont_g + ex_g
        conforms, results_graph, results_text = shacl_validate(
            combined,
            shacl_graph=shacl_g,
            ont_graph=ont_g,
            inference='rdfs'
        )
        assert conforms, f"Example {ex} failed SHACL validation:\\n{results_text}"
