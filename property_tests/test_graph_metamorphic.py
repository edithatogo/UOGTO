"""Synthetic payoff lookup invariants; no simulation or solver claims."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF

from uogto.runner.engine import RDFGameRunner

UOGTO = Namespace("https://w3id.org/uogto/core#")
_EXAMPLES = int(os.environ.get("GRAPH_PROPERTY_EXAMPLES", "50"))
if not 1 <= _EXAMPLES <= 500:
    raise ValueError("GRAPH_PROPERTY_EXAMPLES must be between 1 and 500")
_BOUNDED = settings(max_examples=_EXAMPLES, deadline=2000)
_PAYOFFS = st.lists(st.integers(-10000, 10000), min_size=2, max_size=4)
_NAMES = st.text(alphabet="abcdefghijklmnopqrstuvwxyz0123456789", min_size=1, max_size=16)


def _game_graph(namespace: str, payoffs: list[int]) -> tuple[Graph, dict[str, str]]:
    """Two games share a profile's player/action pairs but have distinct utilities."""
    nodes = Namespace(namespace)
    graph = Graph()
    choices = {}
    for index, value in enumerate(payoffs):
        player, action, space = (nodes[f"{kind}-{index}"] for kind in ("player", "action", "space"))
        choices[str(player)] = str(action)
        graph.add((player, RDF.type, UOGTO.Player))
        graph.add((action, RDF.type, UOGTO.Action))
        graph.add((action, UOGTO.belongsToPlayer, player))
        graph.add((space, UOGTO.belongsToPlayer, player))
        graph.add((space, UOGTO.hasAction, action))
        for game_id, offset in (("a", 0), ("b", 100001)):
            game = nodes[f"game-{game_id}"]
            profile = nodes[f"profile-{game_id}"]
            payoff_profile = nodes[f"payoffs-{game_id}"]
            link = nodes[f"link-{game_id}-{index}"]
            graph.add((game, RDF.type, UOGTO.GameSpecification))
            graph.add((game, UOGTO.hasPlayer, player))
            graph.add((game, UOGTO.hasActionSpace, space))
            graph.add((game, UOGTO.hasStrategyProfile, profile))
            graph.add((profile, UOGTO.hasAction, action))
            graph.add((profile, UOGTO.hasPayoff, payoff_profile))
            graph.add((payoff_profile, UOGTO.hasPayoffForPlayer, link))
            graph.add((link, UOGTO.payoffPlayer, player))
            graph.add((link, UOGTO.payoffValue, Literal(value + offset)))
    return graph, choices


def _lookup(
    graph: Graph, choices: dict[str, str], namespace: str, format_name: str
) -> dict[str, float]:
    suffix = ".jsonld" if format_name == "json-ld" else ".ttl"
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / ("synthetic" + suffix)
        # RDFLib emits an inline JSON-LD graph without a remote context.
        graph.serialize(destination=path, format=format_name)
        runner = RDFGameRunner(path)
        assert len(runner.get_game_specification()) == 2
        for player, action in choices.items():
            assert {entry["uri"] for entry in runner.get_actions(namespace + "game-a", player)} == {
                action
            }
        return runner.query_payoff(namespace + "game-a", choices)


@_BOUNDED
@given(payoffs=_PAYOFFS, name=_NAMES)
def test_iri_renaming_and_serialization_preserve_signed_scoped_payoffs(
    payoffs: list[int], name: str
) -> None:
    namespace = "https://example.invalid/synthetic/" + name + "/"
    graph, choices = _game_graph(namespace, payoffs)
    expected = {namespace + f"player-{index}": float(value) for index, value in enumerate(payoffs)}
    assert _lookup(graph, choices, namespace, "turtle") == expected
    assert _lookup(graph, choices, namespace, "json-ld") == expected
    renamed = "https://example.invalid/renamed/" + name + "/"
    renamed_graph, renamed_choices = _game_graph(renamed, payoffs)
    renamed_actual = _lookup(renamed_graph, renamed_choices, renamed, "turtle")
    assert renamed_actual == {
        renamed + f"player-{index}": float(value) for index, value in enumerate(payoffs)
    }


@_BOUNDED
@given(payoffs=_PAYOFFS, reverse=st.booleans(), repetitions=st.integers(1, 4))
def test_triple_order_and_duplicate_insertion_cannot_change_payoff_identity(
    payoffs: list[int], reverse: bool, repetitions: int
) -> None:
    namespace = "https://example.invalid/synthetic/"
    graph, choices = _game_graph(namespace, payoffs)
    reordered = Graph()
    triples = sorted(graph, key=lambda triple: tuple(map(str, triple)), reverse=reverse)
    for _ in range(repetitions):
        for triple in triples:
            reordered.add(triple)
    assert len(reordered) == len(graph)
    expected = {namespace + f"player-{index}": float(value) for index, value in enumerate(payoffs)}
    assert _lookup(reordered, choices, namespace, "turtle") == expected


@_BOUNDED
@given(payoffs=_PAYOFFS)
def test_swapping_player_action_identity_cannot_match_a_stored_profile(payoffs: list[int]) -> None:
    namespace = "https://example.invalid/synthetic/"
    graph, choices = _game_graph(namespace, payoffs)
    players = list(choices)
    choices[players[0]], choices[players[1]] = choices[players[1]], choices[players[0]]
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "synthetic.ttl"
        graph.serialize(destination=path, format="turtle")
        runner = RDFGameRunner(path)
        assert runner.query_payoff(namespace + "game-a", choices) == {}
        # A changed numeric literal must change exactly its own player's payoff.
        link = URIRef(namespace + "link-a-0")
        runner.graph.set((link, UOGTO.payoffValue, Literal(payoffs[0] + 1)))
        choices[players[0]], choices[players[1]] = choices[players[1]], choices[players[0]]
        actual = runner.query_payoff(namespace + "game-a", choices)
        expected = {
            namespace + f"player-{index}": float(value) for index, value in enumerate(payoffs)
        }
        expected[players[0]] += 1
        assert actual == expected
