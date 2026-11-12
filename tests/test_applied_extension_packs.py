from pathlib import Path
from rdflib import Graph, URIRef
from rdflib.namespace import OWL, RDF

ROOT = Path(__file__).resolve().parents[1]


def test_each_applied_pack_is_separate_and_imports_core() -> None:
    pack_dir = ROOT / "ontologies" / "applied"
    packs = list(pack_dir.glob("*.ttl"))
    assert {pack.name for pack in packs} == {
        "health-economics-hta.ttl", "medical-decision-modelling.ttl",
        "safety-systems.ttl", "genomic-policy.ttl", "costing-valuation.ttl",
    }
    for pack in packs:
        graph = Graph().parse(pack, format="turtle")
        assert len(graph) > 0
        assert any(
            (ontology, OWL.imports, URIRef("https://w3id.org/uogto/core")) in graph
            for ontology in graph.subjects(RDF.type, OWL.Ontology)
        )


def test_applied_pack_examples_and_shapes_exist() -> None:
    for name in ("hta-payer-adoption-game.ttl", "shared-treatment-choice-game.ttl", "safety-barrier-coordination-game.ttl", "genomic-data-access-game.ttl", "newborn-screening-costing.ttl"):
        assert (ROOT / "examples" / name).exists()
    assert (ROOT / "shapes" / "applied-packs.shacl.ttl").exists()
