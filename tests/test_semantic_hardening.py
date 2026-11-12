from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from pyshacl import validate
from rdflib import Graph, Namespace, OWL, RDF, RDFS, SKOS

ROOT = Path(__file__).resolve().parents[1]
CORE = Namespace("https://w3id.org/uogto/core#")
EXT = Namespace("https://w3id.org/uogto/extensions#")


@pytest.fixture(scope="module")
def ontology() -> Graph:
    graph = Graph()
    for path in (ROOT / "ontologies").rglob("*.ttl"):
        graph.parse(path)
    return graph


def test_results_criteria_and_computational_problems_have_distinct_hierarchies(ontology):
    expected = {
        CORE.Equilibrium: CORE.GameSolution,
        CORE.AllocationSolution: CORE.GameSolution,
        EXT.EquilibriumComputationProblem: EXT.ComputationalProblem,
        EXT.EquilibriumPredicate: CORE.SolutionConcept,
        EXT.ShapleyValue: CORE.AllocationSolution,
        EXT.CoreSolution: CORE.AllocationSolution,
        EXT.BargainingSolution: CORE.AllocationSolution,
        EXT.NashBargainingSolution: EXT.BargainingSolution,
        EXT.KalaiSmorodinskySolution: EXT.BargainingSolution,
    }
    for term, parent in expected.items():
        assert (term, RDFS.subClassOf, parent) in ontology
    for term in [EXT.EquilibriumComputationProblem, EXT.EquilibriumPredicate,
                 EXT.ShapleyValue, EXT.CoreSolution, EXT.BargainingSolution,
                 EXT.NashBargainingSolution, EXT.KalaiSmorodinskySolution]:
        assert CORE.Equilibrium not in ontology.transitive_objects(term, RDFS.subClassOf)
    assert "relative to the disagreement point" in str(next(ontology.objects(EXT.NashBargainingSolution, SKOS.definition)))


def test_structural_equation_definition_has_causal_inputs_and_endogenous_output(ontology):
    definitions = list(ontology.objects(EXT.StructuralEquation, SKOS.definition))
    assert len(definitions) == 1
    definition = str(definitions[0])
    assert "determining an endogenous variable" in definition
    assert "causal parent variables and exogenous factors" in definition


def test_every_runner_core_term_is_declared_and_annotated(ontology):
    source = (ROOT / "uogto/runner/engine.py").read_text()
    terms = set(re.findall(r"uogto:([A-Za-z]+)", source))
    for name in terms:
        term = CORE[name]
        assert any((term, RDF.type, kind) in ontology for kind in (OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty)), name
        assert list(ontology.objects(term, RDFS.label)), name
        assert list(ontology.objects(term, SKOS.definition)), name
    assert (CORE.hasActionSpace, OWL.equivalentProperty, EXT.hasActionSpace) not in ontology
    assert not list(ontology.objects(CORE.hasActionSpace, RDFS.domain))


def test_probability_does_not_impose_a_double_only_range(ontology):
    # Integer, decimal and float probabilities are valid SHACL controls below.
    # A double-only OWL range would contradict that documented numeric policy.
    assert not list(ontology.objects(CORE.probability, RDFS.range))


def test_new_core_terms_are_available_in_the_core_jsonld_context(ontology):
    context = json.loads((ROOT / "jsonld/core.context.jsonld").read_text())["@context"]
    for name in ("SolutionConcept", "GameSolution", "AllocationSolution", "hasSolutionConcept",
                 "hasActionSpace", "hasAction", "belongsToPlayer", "hasPayoffMapping", "hasActionProfile"):
        value = context[name]
        assert (value if isinstance(value, str) else value["@id"]) == f"uogto:{name}"
        if (CORE[name], RDF.type, OWL.ObjectProperty) in ontology:
            assert value["@type"] == "@id"



def test_aggregate_context_preserves_both_action_space_predicates():
    # The original short alias belongs to the MARL extension in the aggregate
    # context. An explicit core alias avoids silently changing existing graphs.
    context_path = (ROOT / "jsonld/context.jsonld").as_uri()
    graph = Graph().parse(data=json.dumps({
        "@context": context_path,
        "@id": "http://example.org/g",
        "coreHasActionSpace": "http://example.org/core-space",
        "hasActionSpace": "http://example.org/agent-space",
    }), format="json-ld")
    assert len(list(graph.triples((None, CORE.hasActionSpace, None)))) == 1
    assert len(list(graph.triples((None, EXT.hasActionSpace, None)))) == 1


def _conforms(body: str) -> bool:
    data = Graph().parse(data=f'''@prefix uogto: <{CORE}> .
        @prefix ex: <http://example.org/> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
        {body}''', format="turtle")
    shapes = Graph()
    for path in (ROOT / "shapes").glob("*.ttl"):
        shapes.parse(path)
    return validate(data, shacl_graph=shapes, inference="rdfs")[0]


@pytest.mark.parametrize("body", [
    'ex:g a uogto:GameSpecification ; uogto:hasPlayer "literal-player" .',
    'ex:g uogto:hasPlayer "literal-player" .',
    'ex:t uogto:probability 7.0 .',
    'ex:t uogto:probability -0.01 .',
    'ex:t uogto:probability "0.5" .',
    'ex:t uogto:probability "NaN"^^xsd:double .',
    'ex:t uogto:probability "INF"^^xsd:double .',
])
def test_default_shapes_reject_malformed_values(body):
    assert not _conforms(body)


@pytest.mark.parametrize("body", [
    'ex:g a uogto:GameSpecification ; uogto:hasPlayer ex:p .',
    'ex:g a uogto:GameSpecification ; uogto:hasPlayer [] .',
    'ex:t uogto:probability 0.0, 0.5, 1.0 .',
    'ex:t uogto:probability 0, 1 .',
    'ex:t uogto:probability "0.5"^^xsd:double, "0.5"^^xsd:float .',
    'ex:t uogto:probability "1"^^xsd:nonNegativeInteger .',
])
def test_default_shapes_accept_valid_values_without_executable_completeness(body):
    assert _conforms(body)
