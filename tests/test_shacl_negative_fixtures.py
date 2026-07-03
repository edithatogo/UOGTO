from rdflib import Graph
from pyshacl import validate as shacl_validate


def ontology_graph() -> Graph:
    graph = Graph()
    for ttl in __import__("glob").glob("ontologies/**/*.ttl", recursive=True):
        graph.parse(ttl, format="turtle")
    return graph


def shape_graph() -> Graph:
    graph = Graph()
    for ttl in __import__("glob").glob("shapes/*.ttl"):
        graph.parse(ttl, format="turtle")
    return graph


def assert_rejected(ttl: str) -> None:
    data = Graph()
    data.parse(data=ttl, format="turtle")
    ont = ontology_graph()
    conforms, _, results_text = shacl_validate(
        ont + data,
        shacl_graph=shape_graph(),
        ont_graph=ont,
        inference="rdfs",
    )
    assert not conforms, results_text


def test_core_game_specification_requires_player() -> None:
    assert_rejected(
        """
        @prefix uogto: <https://w3id.org/uogto/core#> .
        @prefix ex: <http://example.org/> .
        ex:game a uogto:GameSpecification ;
            uogto:identifier "game" .
        """
    )


def test_game_type_markov_game_requires_transition() -> None:
    assert_rejected(
        """
        @prefix uogtox: <https://w3id.org/uogto/extensions#> .
        @prefix ex: <http://example.org/> .
        ex:markov a uogtox:MarkovGame .
        """
    )


def test_execution_llm_agent_requires_prompt_state() -> None:
    assert_rejected(
        """
        @prefix uogtox: <https://w3id.org/uogto/extensions#> .
        @prefix ex: <http://example.org/> .
        ex:agent a uogtox:LLMAgent .
        """
    )


def test_example_player_requires_identifier() -> None:
    assert_rejected(
        """
        @prefix uogto: <https://w3id.org/uogto/core#> .
        @prefix ex: <http://example.org/> .
        ex:player a uogto:Player .
        """
    )


def test_governance_mechanism_requires_rules() -> None:
    assert_rejected(
        """
        @prefix uogtox: <https://w3id.org/uogto/extensions#> .
        @prefix ex: <http://example.org/> .
        ex:mechanism a uogtox:Mechanism .
        """
    )
