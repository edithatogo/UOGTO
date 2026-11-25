"""Query and validate the exact release catalogues on the public RDF surface."""

import json
from collections import Counter
from pathlib import Path

from pyshacl import validate
from rdflib import RDF, Graph, Namespace, URIRef
from rdflib.namespace import OWL

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "data/processed/external-games"
DCT = Namespace("http://purl.org/dc/terms/")
BASE = "https://w3id.org/uogto/catalogues/"
EXPECTED = {
    "EFG": 32,
    "NFG": 6,
    "GAMUT": 35,
    "OpenSpiel C++": 116,
    "OpenSpiel Python": 20,
    "OpenSpiel transform": 10,
}


def test_external_catalogue_profile():
    graph = Graph().parse(CATALOGUE / "catalogues.jsonld", format="json-ld")
    conforms, _, report = validate(graph, shacl_graph=str(CATALOGUE / "catalogue-shapes.ttl"))
    assert conforms, report

    rows = list(
        graph.query(
            """
            SELECT ?release ?key ?format ?subject ?source
            WHERE {
                ?entry dct:isPartOf ?release ; dct:identifier ?key ;
                       dct:format ?format ; dct:subject ?subject ;
                       prov:wasDerivedFrom ?source .
            }
            """,
            initNs={"dct": DCT, "prov": Namespace("http://www.w3.org/ns/prov#")},
        )
    )
    assert Counter(str(row.format) for row in rows) == EXPECTED
    assert len({(row.release, row.key) for row in rows}) == sum(EXPECTED.values())

    classes = Graph()
    for directory in ("ontologies/core", "ontologies/extensions"):
        for path in sorted((ROOT / directory).glob("*.ttl")):
            classes.parse(path)
    assert all((row.subject, RDF.type, OWL.Class) in classes for row in rows)

    # These cases bind the two model formats, optional native registrations,
    # Python registrations and transforms to the same provenance shape.
    ids = {(str(row.release).removeprefix(BASE), str(row.key)) for row in rows}
    assert {
        ("gambit/16.7.0/models", "books/myerson1991/fig2_1"),
        ("gambit/16.7.0/gamut", "CongestionGame"),
        ("openspiel/2.0.2", "matrix_pd"),
        ("openspiel/2.0.2", "hanabi"),
        ("openspiel/2.0.2", "universal_poker"),
        ("openspiel/2.0.2", "python_kuhn_poker"),
        ("openspiel/2.0.2", "turn_based_simultaneous_game"),
    } <= ids
    assert not set(graph.subjects(RDF.type, URIRef("https://w3id.org/uogto/core#GameInstance")))


def test_frozen_catalogue_identifiers_are_unique_before_rdf_parsing():
    document = json.loads((CATALOGUE / "catalogues.jsonld").read_bytes())
    ids = [entry["@id"] for entry in document["@graph"]]
    assert len(ids) == len(set(ids))
