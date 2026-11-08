import glob
from pathlib import Path

from rdflib import Graph, Namespace, RDF, OWL, URIRef

COST = Namespace("https://w3id.org/uogto/packs/costing-valuation#")

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
        elif "reporting" in Path(ttl).parts:
            # A source catalogue is instance data using an imported vocabulary,
            # not an empty schema or a reason to invent duplicate classes.
            assert any(
                (ontology, OWL.imports, URIRef(str(COST).rstrip("#"))) in g
                for ontology in g.subjects(RDF.type, OWL.Ontology)
            ), f"Reporting catalogue {ttl} must identify and import its schema"
            for kind in (COST.ReportingDomain, COST.ReportingInstrument,
                         COST.InstrumentVersion, COST.ReportingRequirement):
                assert any(g.subjects(RDF.type, kind)), f"Reporting catalogue {ttl} has no {kind} instances"
        else:
            total_defs = len(classes) + len(obj_properties) + len(data_properties)
            assert total_defs > 0, f"Module {ttl} is completely empty!"

