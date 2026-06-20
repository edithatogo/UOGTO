import glob
from rdflib import Graph, RDF, OWL

def test_coverage_thresholds():
    ttl_files = glob.glob("ontologies/**/*.ttl", recursive=True)
    assert len(ttl_files) >= 30, f"Expected at least 30 ontology files, found {len(ttl_files)}"
    for ttl in ttl_files:
        g = Graph()
        g.parse(ttl, format="turtle")
        classes = list(g.subjects(RDF.type, OWL.Class))
        obj_properties = list(g.subjects(RDF.type, OWL.ObjectProperty))
        data_properties = list(g.subjects(RDF.type, OWL.DatatypeProperty))
        
        # Every module should have some content
        if "alignments" in ttl:
            assert len(g) > 0, f"Alignment module {ttl} is completely empty!"
        else:
            total_defs = len(classes) + len(obj_properties) + len(data_properties)
            assert total_defs > 0, f"Module {ttl} is completely empty!"

