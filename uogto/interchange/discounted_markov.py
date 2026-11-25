"""Project the bounded UOGTO discounted Markov game profile to Paignia JSON."""

from collections.abc import Callable, Iterable
from fractions import Fraction
from importlib.resources import files
from itertools import product
from math import isfinite
from typing import NoReturn

from pyshacl import validate
from rdflib import RDF, SH, BNode, Graph, Namespace, URIRef
from rdflib.graph import ConjunctiveGraph
from rdflib.namespace import DCTERMS
from rfc3987_syntax import is_valid_syntax_iri

from .game_contract import UnsupportedExecutableSubset

PROFILE_IRI = URIRef("urn:uogto:profile:discounted-markov:1.0.0")
FROZEN_SPECIFICATION_IRI = URIRef("https://example.org/uogto/recurring-funding/v1/specification")
FROZEN_REPRESENTATION_IRI = URIRef("https://example.org/uogto/recurring-funding/v1/representation")

_MASS_TOLERANCE = Fraction.from_float(1e-12)
_CORE = Namespace("https://w3id.org/uogto/core#")
_EXT = Namespace("https://w3id.org/uogto/extensions#")
_REPRESENTATION_SHAPE = URIRef("urn:uogto:shapes:discounted-markov:1.0.0#Representation")


def _reject(path: str, detail: str) -> NoReturn:
    raise UnsupportedExecutableSubset("invalid_discounted_markov_graph", path, detail)


def _named(term, path: str) -> URIRef:
    if not isinstance(term, URIRef) or not is_valid_syntax_iri(str(term)):
        _reject(path, "expected an absolute IRI")
    return term


def _one(graph: Graph, node, predicate: URIRef):
    values = list(graph.objects(node, predicate))
    if len(values) != 1:
        _reject(str(node), f"expected exactly one {predicate}")
    return values[0]


def _ref(graph: Graph, node, predicate: URIRef) -> URIRef:
    return _named(_one(graph, node, predicate), str(node))


def _refs(graph: Graph, node: URIRef, predicate: URIRef) -> list[URIRef]:
    return [_named(term, str(node)) for term in sorted(graph.objects(node, predicate), key=str)]


def _axis(graph: Graph, owner: URIRef, predicate: URIRef) -> list[URIRef]:
    node = _one(graph, owner, predicate)
    visited = set()
    members = []
    while node != RDF.nil:
        if not isinstance(node, BNode):
            _named(node, str(owner))
        if node in visited:
            _reject(str(owner), f"cyclic RDF list for {predicate}")
        visited.add(node)
        members.append(_ref(graph, node, RDF.first))
        node = _one(graph, node, RDF.rest)
    if (RDF.nil, RDF.first, None) in graph or (RDF.nil, RDF.rest, None) in graph:
        _reject(str(owner), "rdf:nil must terminate the axis")
    if not members or len(set(members)) != len(members):
        _reject(str(owner), f"expected a nonempty axis of distinct IRIs for {predicate}")
    return members


def _bindings[K](
    entries: list[URIRef],
    key: Callable[[URIRef], K],
    expected: Iterable[K],
    path: str,
) -> dict[K, URIRef]:
    expected_keys = set(expected)
    bindings = {}
    for entry in entries:
        label = key(entry)
        if label not in expected_keys:
            _reject(path, f"foreign binding at {entry}")
        if label in bindings:
            _reject(path, f"duplicate binding at {entry}")
        bindings[label] = entry
    if bindings.keys() != expected_keys:
        _reject(path, "incomplete bindings for the declared axes")
    return bindings


def _number(graph: Graph, node: URIRef, predicate: URIRef) -> float:
    # SHACL has already checked the datatype. Binary64 further requires finiteness.
    value = _one(graph, node, predicate).toPython()
    if not isinstance(value, float) or not isfinite(value):
        _reject(str(node), f"expected a finite binary64 value for {predicate}")
    return value


def _distribution(
    graph: Graph, owner: URIRef, entries: URIRef, label: URIRef, axis: list[URIRef]
) -> list[float]:
    bindings = _bindings(
        _refs(graph, owner, entries), lambda entry: _ref(graph, entry, label), axis, str(owner)
    )
    weights = [_number(graph, bindings[member], _CORE.probability) for member in axis]
    if any(weight < 0.0 or weight > 1.0 for weight in weights):
        _reject(str(owner), "expected weights in [0, 1]")
    # Compare parsed binary64 values exactly, including the tolerance itself.
    mass = sum(Fraction.from_float(weight) for weight in weights)
    if abs(mass - 1) > _MASS_TOLERANCE:
        _reject(str(owner), "distribution mass differs from one by more than binary64 1e-12")
    return weights


def _representation(graph: Graph, specification: URIRef) -> URIRef:
    if not isinstance(graph, Graph) or isinstance(graph, ConjunctiveGraph):
        _reject("graph", "select one RDF graph context")
    _named(specification, "specification_iri")
    representation = _ref(graph, specification, _CORE.hasRepresentation)
    if _ref(graph, representation, DCTERMS.conformsTo) != PROFILE_IRI:
        _reject(str(representation), f"expected profile {PROFILE_IRI}")

    shape = files("uogto.interchange").joinpath("discounted-markov-profile-v1.ttl")
    shapes = Graph().parse(data=shape.read_text(encoding="utf-8"), format="turtle")
    shapes.remove((_REPRESENTATION_SHAPE, SH.targetClass, None))
    shapes.add((_REPRESENTATION_SHAPE, SH.targetNode, representation))
    conforms, _, _ = validate(graph, shacl_graph=shapes, inference="none", inplace=False)
    if not conforms:
        _reject(str(representation), "RDF does not conform to the discounted Markov SHACL shape")
    return representation


def _stage_key(
    graph: Graph, decision: URIRef, action_axes: list[list[URIRef]]
) -> tuple[URIRef, URIRef, URIRef]:
    profile = _ref(graph, decision, _CORE.hasActionProfile)
    choices = set(_refs(graph, profile, _CORE.hasAction))
    first, second = (choices.intersection(axis) for axis in action_axes)
    if len(first) != 1 or len(second) != 1:
        _reject(str(decision), "expected one action from each player in the joint action")
    return _ref(graph, decision, _EXT.atState), next(iter(first)), next(iter(second))


def _outcome(
    graph: Graph, decision: URIRef, state: URIRef, states: list[URIRef]
) -> dict[str, object]:
    for transition in _refs(graph, decision, _CORE.hasTransition):
        if _ref(graph, transition, _CORE.transitionsFrom) != state:
            _reject(str(transition), "transition source differs from the decision state")
    return {
        "reward": _number(graph, decision, _EXT.stageReward),
        "transition": _distribution(
            graph, decision, _CORE.hasTransition, _CORE.transitionsTo, states
        ),
    }


def project_game(graph: Graph, specification: URIRef) -> dict[str, object]:
    """Validate one asserted RDF game and return the Paignia policy evaluation payload."""
    representation = _representation(graph, specification)
    players = _axis(graph, representation, _EXT.playerOrder)
    states = _axis(graph, representation, _EXT.stateOrder)
    if set(players) != set(_refs(graph, specification, _CORE.hasPlayer)):
        _reject(str(representation), "player axis differs from the declared players")
    if set(states) != set(_refs(graph, specification, _CORE.hasState)):
        _reject(str(representation), "state axis differs from the declared states")

    action_axes = [_axis(graph, player, _EXT.actionOrder) for player in players]
    first_actions, second_actions = action_axes
    kernel = _ref(graph, specification, _CORE.hasTransition)
    identities = [
        specification,
        representation,
        kernel,
        *players,
        *states,
        *first_actions,
        *second_actions,
    ]
    if len(set(identities)) != len(identities):
        _reject(
            str(representation),
            "specification, representation, kernel and axis identities must be distinct",
        )
    for player, actions in zip(players, action_axes, strict=True):
        if set(_refs(graph, player, _CORE.observes)) != set(states):
            _reject(str(player), "every player must observe the complete state axis")
        for action in actions:
            if _ref(graph, action, _CORE.belongsToPlayer) != player:
                _reject(str(action), "action belongs to a different player")
    all_actions = set().union(*action_axes)
    for state in states:
        if set(_refs(graph, state, _CORE.hasAvailableAction)) != all_actions:
            _reject(str(state), "legal actions differ from the fixed action axes")

    stage_decisions = _refs(graph, kernel, _EXT.hasStageDecision)
    expected_decisions = len(states) * len(first_actions) * len(second_actions)
    if len(stage_decisions) < expected_decisions:
        _reject(str(kernel), "incomplete bindings for the declared axes")
    decisions = _bindings(
        stage_decisions,
        lambda decision: _stage_key(graph, decision, action_axes),
        product(states, *action_axes),
        str(kernel),
    )
    stationary = _ref(graph, representation, _EXT.hasStationaryProfile)
    policy = _bindings(
        _refs(graph, stationary, _EXT.hasPolicyRow),
        lambda row: (_ref(graph, row, _EXT.atState), _ref(graph, row, _CORE.belongsToPlayer)),
        product(states, players),
        str(stationary),
    )
    discount = _number(graph, representation, _EXT.modelDiscountFactor)
    if not 0.0 <= discount < 1.0:
        _reject(str(representation), "model discount must be in [0, 1)")

    return {
        "kind": "discounted",
        "players": [
            {"id": str(player), "actions": [str(action) for action in actions]}
            for player, actions in zip(players, action_axes, strict=True)
        ],
        "states": [
            {
                "id": str(state),
                "outcomes": [
                    [
                        _outcome(graph, decisions[state, first, second], state, states)
                        for second in second_actions
                    ]
                    for first in first_actions
                ],
            }
            for state in states
        ],
        "initial": _distribution(
            graph, representation, _EXT.hasInitialWeight, _EXT.atState, states
        ),
        "discount": discount,
        "method": {
            "kind": "evaluate",
            "policy": [
                [
                    _distribution(
                        graph, policy[state, player], _EXT.hasActionWeight, _CORE.hasAction, actions
                    )
                    for player, actions in zip(players, action_axes, strict=True)
                ]
                for state in states
            ],
        },
        "max_iterations": 300,
        "value_tolerance": 1e-10,
    }
