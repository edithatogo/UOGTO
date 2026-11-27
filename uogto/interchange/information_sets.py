"""Project one asserted UOGTO game scope to a Paignia information-set declaration."""
from __future__ import annotations

from importlib.resources import files

from pyshacl import validate
from rdflib import RDF, SH, Graph, Namespace, URIRef
from rdflib.graph import ConjunctiveGraph
from rfc3987_syntax import is_valid_syntax_iri

from .game_contract import UnsupportedExecutableSubset

SCHEMA_VERSION = "1.0.0"
SEMANTIC_PROFILE = "paignia/static-finite-information-set-perfect-recall/1.0.0"
PROVIDER_REVISION = "d4047c0648a89f2aee4461ff70bbc9641e5320cd"

_UOGTO = Namespace("https://w3id.org/uogto/core#")
_NODE_KINDS = (_UOGTO.DecisionNode, _UOGTO.ChanceNode, _UOGTO.TerminalNode)
_DISJOINT_ROLES = frozenset((
    *_NODE_KINDS,
    _UOGTO.GameSpecification,
    _UOGTO.GameInstance,
    _UOGTO.PlaySession,
    _UOGTO.EventTrace,
    _UOGTO.ExtensiveFormRepresentation,
    _UOGTO.NormalFormRepresentation,
    _UOGTO.Player,
    _UOGTO.InformationSet,
))
_SPECIFICATION_SHAPE = URIRef("urn:uogto:shapes:information-set:1.0.0#Specification")


def _validate_identity(graph: Graph, term: URIRef, role: URIRef, field: str) -> None:
    if not isinstance(term, URIRef) or not is_valid_syntax_iri(str(term)):
        raise UnsupportedExecutableSubset("invalid_information_set_iri", field, "expected an absolute IRI")
    asserted_roles = _DISJOINT_ROLES.intersection(graph.objects(term, RDF.type))
    if asserted_roles - {role}:
        raise UnsupportedExecutableSubset(
            "conflicting_information_set_role", field, "resource has another asserted profile role"
        )


def project_information_sets(
    graph: Graph,
    specification: URIRef,
    *,
    schema_version: str = SCHEMA_VERSION,
    semantic_profile: str = SEMANTIC_PROFILE,
) -> dict[str, object]:
    """Return the exact scoped identities and Paignia declaration for native admission."""
    if schema_version != SCHEMA_VERSION:
        raise UnsupportedExecutableSubset(
            "unsupported_information_set_schema", "schema_version", f"expected {SCHEMA_VERSION}"
        )
    if semantic_profile != SEMANTIC_PROFILE:
        raise UnsupportedExecutableSubset(
            "unsupported_information_set_profile", "semantic_profile", f"expected {SEMANTIC_PROFILE}"
        )

    if not isinstance(graph, Graph) or isinstance(graph, ConjunctiveGraph):
        raise UnsupportedExecutableSubset(
            "unsupported_information_set_graph_context", "graph", "select one RDF graph context"
        )

    _validate_identity(graph, specification, _UOGTO.GameSpecification, "specification_iri")
    shape = files("uogto.interchange").joinpath("information-set-profile-v1.ttl")
    shapes = Graph().parse(data=shape.read_text(encoding="utf-8"), format="turtle")
    shapes.add((_SPECIFICATION_SHAPE, SH.targetNode, specification))
    conforms, _, _ = validate(graph, shacl_graph=shapes, inference="none", inplace=False)
    if not conforms:
        raise UnsupportedExecutableSubset(
            "invalid_information_set_graph",
            "specification",
            "expected an extensive representation, named players and complete decision bindings",
        )

    representations = sorted(graph.objects(specification, _UOGTO.hasRepresentation))
    representation = next(
        term for term in representations if (term, RDF.type, _UOGTO.ExtensiveFormRepresentation) in graph
    )
    for term in representations:
        role = (
            _UOGTO.ExtensiveFormRepresentation if term == representation
            else _UOGTO.NormalFormRepresentation
        )
        _validate_identity(graph, term, role, "specification.representations")

    players = set(graph.objects(specification, _UOGTO.hasPlayer))
    states = set(graph.objects(specification, _UOGTO.hasState))
    root = next(graph.objects(specification, _UOGTO.hasInitialState))
    if root not in states:
        raise UnsupportedExecutableSubset(
            "foreign_information_set_root", "root_iri", "root falls outside the declared game"
        )
    for player in sorted(players):
        _validate_identity(graph, player, _UOGTO.Player, "specification.players")

    state_types = {}
    sets: dict[URIRef, tuple[URIRef, list[str]]] = {}
    for node in sorted(states):
        kind = next(kind for kind in _NODE_KINDS if (node, RDF.type, kind) in graph)
        _validate_identity(graph, node, kind, "specification.states")
        state_types[str(node)] = str(kind)
        alternative_sets = set(graph.objects(node, _UOGTO.hasInformationSet))
        if kind != _UOGTO.DecisionNode:
            if alternative_sets:
                raise UnsupportedExecutableSubset(
                    "conflicting_information_set_membership", str(node), "only decisions may be members"
                )
            continue
        player = next(graph.subjects(_UOGTO.controlsNode, node))
        if player not in players:
            raise UnsupportedExecutableSubset(
                "foreign_information_set_player", str(node), "controller falls outside the declared game"
            )
        set_id = next(graph.objects(node, _UOGTO.belongsToInformationSet))
        if alternative_sets - {set_id}:
            raise UnsupportedExecutableSubset(
                "conflicting_information_set_membership", str(node), "membership predicates disagree"
            )
        owner, members = sets.setdefault(set_id, (player, []))
        if owner != player:
            raise UnsupportedExecutableSubset(
                "mixed_information_set_owners", str(set_id), "all member nodes must share one controller"
            )
        members.append(str(node))

    declarations = []
    for set_id, (owner, members) in sorted(sets.items()):
        _validate_identity(graph, set_id, _UOGTO.InformationSet, "declaration.sets.id")
        canonical_members = set(graph.subjects(_UOGTO.belongsToInformationSet, set_id))
        alternate_members = set(graph.subjects(_UOGTO.hasInformationSet, set_id)) - {specification}
        if (canonical_members | alternate_members) - states:
            raise UnsupportedExecutableSubset(
                "foreign_information_set_member", str(set_id), "member falls outside the declared game"
            )
        declarations.append({"id": str(set_id), "player": str(owner), "members": members})

    return {
        "specification_iri": str(specification),
        "representation_iri": str(representation),
        "root_iri": str(root),
        "state_types": state_types,
        "provider_revision": PROVIDER_REVISION,
        "declaration": {
            "schema_version": schema_version,
            "semantic_profile": semantic_profile,
            "sets": declarations,
        },
    }
