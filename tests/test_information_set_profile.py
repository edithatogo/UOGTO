"""Source-profile and competency controls for the Paignia information-set handoff."""
from __future__ import annotations

from pathlib import Path

import pytest
from rdflib import RDF, BNode, Dataset, Graph, Literal, Namespace, URIRef

from uogto.interchange.game_contract import UnsupportedExecutableSubset
from uogto.interchange.information_sets import project_information_sets

UOGTO = Namespace("https://w3id.org/uogto/core#")
GAME = Namespace("https://example.org/doors#")
LEFT = URIRef("https://example.org/doors/left#choice")
RIGHT = URIRef("https://example.org/doors/right#choice")
OWNER = GAME["décideur"]
SET = GAME["choix-privé"]
FIXTURE = Path(__file__).parent / "fixtures" / "paignia-information-set-v1.ttl"


@pytest.fixture
def graph() -> Graph:
    return Graph().parse(FIXTURE, format="turtle")


def test_complete_partition_preserves_full_identifiers_and_source(graph):
    before = set(graph)
    projected = project_information_sets(graph, GAME.specification)

    assert projected == {
        "specification_iri": str(GAME.specification),
        "representation_iri": str(GAME.extensive),
        "root_iri": str(GAME.deal),
        "state_types": {
            str(GAME.deal): str(UOGTO.ChanceNode),
            str(GAME["pass"]): str(UOGTO.TerminalNode),
            str(GAME.play): str(UOGTO.TerminalNode),
            str(LEFT): str(UOGTO.DecisionNode),
            str(RIGHT): str(UOGTO.DecisionNode),
        },
        "provider_revision": "d4047c0648a89f2aee4461ff70bbc9641e5320cd",
        "declaration": {
            "schema_version": "1.0.0",
            "semantic_profile": "paignia/static-finite-information-set-perfect-recall/1.0.0",
            "sets": [{
                "id": str(SET),
                "player": str(OWNER),
                "members": [str(LEFT), str(RIGHT)],
            }],
        },
    }
    assert set(graph) == before

    # Which nodes does this player control in the selected set and game?
    matches = graph.query(
        """
        SELECT ?node WHERE {
          ?game uogto:hasState ?node ; uogto:hasPlayer ?player .
          ?player uogto:controlsNode ?node .
          ?node a uogto:DecisionNode ; uogto:belongsToInformationSet ?set .
        }
        ORDER BY ?node
        """,
        initNs={"uogto": UOGTO},
        initBindings={"game": GAME.specification, "player": OWNER, "set": SET},
    )
    assert [node for (node,) in matches] == [LEFT, RIGHT]


@pytest.mark.parametrize(
    "kwargs,field",
    [
        ({"schema_version": "2.0.0"}, "schema_version"),
        ({"semantic_profile": "paignia/static-finite-perfect-information-sparse-zero/1.0.0"},
         "semantic_profile"),
    ],
)
def test_unsupported_version_or_profile_fails_closed(graph, kwargs, field):
    with pytest.raises(UnsupportedExecutableSubset) as failure:
        project_information_sets(graph, GAME.specification, **kwargs)
    assert failure.value.path == field


@pytest.mark.parametrize(
    "remove,add",
    [
        ((LEFT, UOGTO.belongsToInformationSet, SET), None),
        (None, (LEFT, UOGTO.belongsToInformationSet, GAME.second_set)),
        ((OWNER, UOGTO.controlsNode, LEFT), None),
        (None, (GAME.outsider, UOGTO.controlsNode, LEFT)),
        (None, (GAME.deal, UOGTO.belongsToInformationSet, SET)),
        (None, (LEFT, RDF.type, UOGTO.TerminalNode)),
        ((SET, RDF.type, UOGTO.InformationSet), None),
        ((GAME.extensive, RDF.type, UOGTO.ExtensiveFormRepresentation), None),
        (None, (GAME.specification, UOGTO.hasState, BNode())),
        ((GAME.specification, UOGTO.hasInitialState, GAME.deal), None),
        (None, (GAME.specification, UOGTO.hasInitialState, GAME.play)),
    ],
)
def test_graph_must_satisfy_the_selected_profile(graph, remove, add):
    if remove is not None:
        graph.remove(remove)
    if add is not None:
        graph.add(add)
    with pytest.raises(UnsupportedExecutableSubset, match="invalid_information_set_graph"):
        project_information_sets(graph, GAME.specification)


@pytest.mark.parametrize("predicate", [UOGTO.belongsToInformationSet, UOGTO.hasInformationSet])
def test_set_cannot_import_an_unscoped_member(graph, predicate):
    graph.add((GAME.foreign_node, RDF.type, UOGTO.DecisionNode))
    graph.add((GAME.foreign_node, predicate, SET))
    with pytest.raises(UnsupportedExecutableSubset, match="foreign_information_set_member"):
        project_information_sets(graph, GAME.specification)


@pytest.mark.parametrize("declared_in_game", [False, True])
def test_player_scope_and_single_owner_are_checked(graph, declared_in_game):
    graph.remove((OWNER, UOGTO.controlsNode, RIGHT))
    graph.add((GAME.outsider, RDF.type, UOGTO.Player))
    graph.add((GAME.outsider, UOGTO.controlsNode, RIGHT))
    if declared_in_game:
        graph.add((GAME.specification, UOGTO.hasPlayer, GAME.outsider))
    expected = "mixed_information_set_owners" if declared_in_game else "foreign_information_set_player"
    with pytest.raises(UnsupportedExecutableSubset, match=expected):
        project_information_sets(graph, GAME.specification)


@pytest.mark.parametrize("foreign", [URIRef("relative-player"), URIRef("https://example.org/%zz")])
def test_malformed_identity_is_rejected_without_rewriting(graph, foreign):
    graph.remove((GAME.specification, UOGTO.hasPlayer, OWNER))
    graph.remove((OWNER, UOGTO.controlsNode, None))
    graph.add((GAME.specification, UOGTO.hasPlayer, foreign))
    graph.add((foreign, RDF.type, UOGTO.Player))
    graph.add((foreign, UOGTO.controlsNode, LEFT))
    graph.add((foreign, UOGTO.controlsNode, RIGHT))
    with pytest.raises(UnsupportedExecutableSubset, match="invalid_information_set_iri"):
        project_information_sets(graph, GAME.specification)


def test_chance_only_source_has_an_empty_partition(graph):
    for node in [LEFT, RIGHT]:
        graph.remove((GAME.specification, UOGTO.hasState, node))
        graph.remove((node, None, None))
        graph.remove((OWNER, UOGTO.controlsNode, node))
    assert project_information_sets(graph, GAME.specification)["declaration"]["sets"] == []


def test_root_must_resolve_to_a_declared_state(graph):
    graph.set((GAME.specification, UOGTO.hasInitialState, GAME.foreign_node))
    with pytest.raises(UnsupportedExecutableSubset, match="foreign_information_set_root"):
        project_information_sets(graph, GAME.specification)


def test_active_representation_must_have_an_unambiguous_kind(graph):
    graph.add((GAME.extensive, RDF.type, UOGTO.NormalFormRepresentation))
    with pytest.raises(UnsupportedExecutableSubset, match="invalid_information_set_graph"):
        project_information_sets(graph, GAME.specification)


def test_two_sets_remain_distinct_and_have_canonical_order(graph):
    separate = GAME["another-set"]
    graph.add((separate, RDF.type, UOGTO.InformationSet))
    graph.set((RIGHT, UOGTO.belongsToInformationSet, separate))
    projection = project_information_sets(graph, GAME.specification)
    assert projection["declaration"]["sets"] == [
        {"id": str(separate), "player": str(OWNER), "members": [str(RIGHT)]},
        {"id": str(SET), "player": str(OWNER), "members": [str(LEFT)]},
    ]


@pytest.mark.parametrize("default_union", [False, True])
def test_dataset_does_not_combine_assertions_or_mutate_the_caller(graph, default_union):
    dataset = Dataset(default_union=default_union)
    selected = dataset.graph(GAME.selected)
    split = (GAME.extensive, RDF.type, UOGTO.ExtensiveFormRepresentation)
    for triple in graph:
        selected.add(triple)
    selected.remove(split)
    dataset.graph(GAME.foreign).add(split)
    before = set(dataset.quads((None, None, None, None)))

    with pytest.raises(UnsupportedExecutableSubset, match="invalid_information_set_graph"):
        project_information_sets(selected, GAME.specification)
    with pytest.raises(UnsupportedExecutableSubset, match="unsupported_information_set_graph_context"):
        project_information_sets(dataset, GAME.specification)
    assert dataset.default_union is default_union
    assert set(dataset.quads((None, None, None, None))) == before


@pytest.mark.parametrize("malformed", [Literal("second representation"), GAME.untyped])
def test_additional_representation_references_are_validated(graph, malformed):
    graph.add((GAME.specification, UOGTO.hasRepresentation, malformed))
    with pytest.raises(UnsupportedExecutableSubset, match="invalid_information_set_graph"):
        project_information_sets(graph, GAME.specification)


def test_normal_form_sibling_preserves_the_selected_extensive_representation(graph):
    original = project_information_sets(graph, GAME.specification)
    graph.add((GAME.normal, RDF.type, UOGTO.NormalFormRepresentation))
    graph.add((GAME.specification, UOGTO.hasRepresentation, GAME.normal))
    assert project_information_sets(graph, GAME.specification) == original


@pytest.mark.parametrize(
    "resource,additional_role",
    [
        (GAME.specification, UOGTO.PlaySession),
        (OWNER, UOGTO.PlaySession),
        (LEFT, UOGTO.EventTrace),
        (SET, UOGTO.GameInstance),
        (GAME.extensive, UOGTO.Player),
        (LEFT, UOGTO.InformationSet),
    ],
)
def test_projected_roles_are_exclusive(graph, resource, additional_role):
    graph.add((resource, RDF.type, additional_role))
    with pytest.raises(UnsupportedExecutableSubset, match="conflicting_information_set_role"):
        project_information_sets(graph, GAME.specification)


def test_supertype_and_equivalent_membership_assertions_are_supported(graph):
    original = project_information_sets(graph, GAME.specification)
    graph.add((LEFT, RDF.type, UOGTO.GameNode))
    graph.add((LEFT, UOGTO.hasInformationSet, SET))
    assert project_information_sets(graph, GAME.specification) == original


@pytest.mark.parametrize("resource,set_id", [(LEFT, GAME.second_set), (GAME["pass"], SET)])
def test_conflicting_state_information_assertions_fail_closed(graph, resource, set_id):
    graph.add((GAME.second_set, RDF.type, UOGTO.InformationSet))
    graph.add((resource, UOGTO.hasInformationSet, set_id))
    with pytest.raises(UnsupportedExecutableSubset, match="conflicting_information_set_membership"):
        project_information_sets(graph, GAME.specification)


def test_specification_may_enumerate_its_information_set(graph):
    original = project_information_sets(graph, GAME.specification)
    graph.add((GAME.specification, UOGTO.hasInformationSet, SET))
    assert project_information_sets(graph, GAME.specification) == original
