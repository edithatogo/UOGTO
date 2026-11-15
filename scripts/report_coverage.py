import sys
import glob
from pathlib import Path

from rdflib import Graph, Namespace, RDF, OWL, URIRef

COST = Namespace("https://w3id.org/uogto/packs/costing-valuation#")
COST_SCHEMA = URIRef(str(COST).rstrip("#"))
REPORTING_INSTANCE_TYPES = (
    COST.ReportingDomain,
    COST.ReportingInstrument,
    COST.InstrumentVersion,
    COST.ReportingRequirement,
)


def coverage_error(path: str | Path, graph: Graph) -> str | None:
    """Require populated schemas, alignments or schema-backed instance catalogues.

    Reporting catalogues use the costing schema instead of redefining its
    classes. Their full semantic constraints are checked by SHACL separately;
    this gate requires identifying/import metadata and meaningful typed content.
    """
    parts = Path(path).parts
    module_name = Path(path).name
    if "alignments" in parts:
        if not graph:
            return f"Alignment module {module_name} is completely empty!"
    elif "reporting" in parts:
        if not any(
            (ontology, OWL.imports, COST_SCHEMA) in graph
            for ontology in graph.subjects(RDF.type, OWL.Ontology)
        ):
            return f"Reporting catalogue {module_name} must identify and import its schema"
        for kind in REPORTING_INSTANCE_TYPES:
            if not any(graph.subjects(RDF.type, kind)):
                return f"Reporting catalogue {module_name} has no {kind} instances"
    else:
        if not any(
            any(graph.subjects(RDF.type, kind))
            for kind in (OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty)
        ):
            return f"Module {module_name} is completely empty!"
    return None


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
        
        module_name = Path(ttl).name
        print(f"Module: {module_name}")
        print(f"  Classes: {len(classes)}")
        print(f"  Object Properties: {len(obj_properties)}")
        print(f"  Datatype Properties: {len(data_properties)}")
        
        error = coverage_error(ttl, g)
        if error:
            print(f"FAIL: {error}")
            sys.exit(1)

            
    print("Coverage thresholds checking complete. All modules are populated.")

if __name__ == "__main__":
    main()
