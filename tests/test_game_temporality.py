from __future__ import annotations

import json
from pathlib import Path

import pytest
from pyshacl import validate
from rdflib import Graph, Namespace, RDF, RDFS, SKOS

ROOT = Path(__file__).resolve().parents[1]
CORE = Namespace("https://w3id.org/uogto/core#")
EX = Namespace("http://example.org/temporality/")


@pytest.fixture(scope="module")
def ontology():
    graph = Graph()
    for path in (ROOT / "ontologies").rglob("*.ttl"):
        graph.parse(path)
    return graph


def _validate(ontology, body):
    graph = Graph().parse(data=f'''@prefix uogto: <{CORE}> .
        @prefix ex: <{EX}> . {body}''', format="turtle")
    shapes = Graph()
    for path in (ROOT / "shapes").glob("*.ttl"):
        shapes.parse(path)
    conforms, _, report = validate(graph, shacl_graph=shapes, ont_graph=ontology, inference="rdfs")
    return conforms, report


@pytest.mark.parametrize("temporal_class", ["StaticGame", "DynamicGame"])
@pytest.mark.parametrize("representation_class", ["NormalFormRepresentation", "ExtensiveFormRepresentation"])
def test_temporality_and_representation_are_independent(ontology, temporal_class, representation_class):
    conforms, report = _validate(ontology, f'''ex:g a uogto:{temporal_class} ;
        uogto:hasPlayer ex:p ; uogto:hasRepresentation ex:r ;
        uogto:compiledToExecutionModel ex:e .
        ex:r a uogto:{representation_class} .
        ex:e a uogto:ExecutionModel .''')
    assert conforms, report
    for representation in (CORE.NormalFormRepresentation, CORE.ExtensiveFormRepresentation):
        ancestors = set(ontology.transitive_objects(representation, RDFS.subClassOf))
        assert not ancestors & {CORE.StaticGame, CORE.DynamicGame}


def test_conflicting_temporality_and_invalid_representation_are_rejected(ontology):
    assert not _validate(ontology, '''ex:g a uogto:StaticGame, uogto:DynamicGame ; uogto:hasPlayer ex:p .''')[0]
    assert not _validate(ontology, '''ex:g uogto:hasRepresentation "normal form" .''')[0]
    assert not _validate(ontology, '''ex:g uogto:hasRepresentation ex:untyped .''')[0]


def test_temporality_terms_have_annotations_and_jsonld_mappings(ontology):
    context = json.loads((ROOT / "jsonld/core.context.jsonld").read_text())["@context"]
    for name in ("StaticGame", "DynamicGame", "GameRepresentation", "NormalFormRepresentation",
                 "ExtensiveFormRepresentation", "hasRepresentation"):
        assert list(ontology.objects(CORE[name], RDFS.label)), name
        assert list(ontology.objects(CORE[name], SKOS.definition)), name
        entry = context[name]
        assert (entry if isinstance(entry, str) else entry["@id"]) == f"uogto:{name}"
    assert context["hasRepresentation"]["@type"] == "@id"


def test_dynamic_simultaneous_stochastic_example_and_competency_bindings(ontology):
    data = Graph().parse(ROOT / "examples/dynamic-normal-form-game.ttl")
    shapes = Graph()
    for path in (ROOT / "shapes").glob("*.ttl"):
        shapes.parse(path)
    conforms, _, report = validate(data, shacl_graph=shapes, ont_graph=ontology, inference="rdfs")
    assert conforms, report
    assert (EX["two-stage-stochastic-game"], RDF.type, CORE.DynamicGame) in data
    assert len(set(data.subjects(RDF.type, CORE.SimultaneousAction))) == 4
    assert len(list(data.triples((None, CORE.probability, None)))) == 2
    graph = ontology + data
    query = (ROOT / "competency-questions/cq21-dynamic-game-representations.rq").read_text()
    rows = list(graph.query(query))
    assert {(str(row.game), str(row.representation), str(row.action)) for row in rows} == {
        (str(EX["two-stage-stochastic-game"]), str(EX["normal-form"]), str(EX[action]))
        for action in ("alice-first-choice", "bob-first-choice", "alice-later-choice", "bob-later-choice")
    }
    manifest = json.loads((ROOT / "validation/competency-query-expectations.json").read_text())
    entry = next(item for item in manifest["queries"] if item["query"] == "cq21-dynamic-game-representations.rq")
    for expected in entry["required_bindings"]:
        assert any(all(str(row.asdict()[key]) == value for key, value in expected.items()) for row in rows)
