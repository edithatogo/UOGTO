from fractions import Fraction
from hashlib import sha256
from importlib.resources import files
from itertools import permutations
from math import inf, nextafter
from pathlib import Path
from random import Random

import pytest
from pyshacl import validate
from rdflib import RDF, BNode, Dataset, Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS

from uogto.interchange import UnsupportedExecutableSubset
from uogto.interchange.discounted_markov import (
    FROZEN_REPRESENTATION_IRI,
    FROZEN_SPECIFICATION_IRI,
    PROFILE_IRI,
    _distribution,
    project_game,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "recurring-funding-discounted-markov-v1.ttl"
CORE = Namespace("https://w3id.org/uogto/core#")
EXT = Namespace("https://w3id.org/uogto/extensions#")
EX = Namespace("https://example.org/uogto/recurring-funding/v1/")
SPEC = FROZEN_SPECIFICATION_IRI
REP = FROZEN_REPRESENTATION_IRI


@pytest.fixture
def graph() -> Graph:
    return Graph().parse(FIXTURE, format="turtle")


def test_frozen_game_projects_complete_payload(graph):
    assert sha256(FIXTURE.read_bytes()).hexdigest() == (
        "2502af2adff68ff9b41e11c68f28ba93a9c452baa0b0f74831fec5ac768f8552"
    )
    assert set(graph.objects(SPEC, CORE.hasRepresentation)) == {REP}
    assert set(graph.objects(REP, DCTERMS.conformsTo)) == {PROFILE_IRI}
    assert project_game(graph, SPEC) == {
        "kind": "discounted",
        "players": [
            {"id": str(EX.commissioner), "actions": [str(EX.settle), str(EX.defer)]},
            {"id": str(EX.provider), "actions": [str(EX.accept), str(EX.contend)]},
        ],
        "states": [
            {
                "id": str(EX.stable),
                "outcomes": [
                    [
                        {"reward": 2.0, "transition": [0.5, 0.5]},
                        {"reward": 3.0, "transition": [1.0, 0.0]},
                    ],
                    [
                        {"reward": 0.0, "transition": [0.0, 1.0]},
                        {"reward": 1.0, "transition": [0.5, 0.5]},
                    ],
                ],
            },
            {
                "id": str(EX.pressure),
                "outcomes": [
                    [
                        {"reward": -1.0, "transition": [0.25, 0.75]},
                        {"reward": -1.0, "transition": [1.0, 0.0]},
                    ],
                    [
                        {"reward": -2.0, "transition": [0.0, 1.0]},
                        {"reward": 1.0, "transition": [0.0, 1.0]},
                    ],
                ],
            },
        ],
        "initial": [0.75, 0.25],
        "discount": 0.75,
        "method": {"kind": "evaluate", "policy": [[[1.0, 0.0], [1.0, 0.0]]] * 2},
        "max_iterations": 300,
        "value_tolerance": 1e-10,
    }


def test_frozen_policy_satisfies_exact_bellman_reference(graph):
    payload = project_game(graph, SPEC)
    values = [Fraction(32, 13), Fraction(-16, 13)]
    discount = Fraction(payload["discount"])
    for state, policy, value in zip(
        payload["states"], payload["method"]["policy"], values, strict=True
    ):
        row = state["outcomes"][policy[0].index(1.0)][policy[1].index(1.0)]
        continuation = sum(
            Fraction(weight) * following
            for weight, following in zip(row["transition"], values, strict=True)
        )
        assert value == Fraction(row["reward"]) + discount * continuation
    assert sum(
        Fraction(weight) * value for weight, value in zip(payload["initial"], values, strict=True)
    ) == Fraction(20, 13)


def test_projection_uses_only_selected_graph_scope_and_has_stable_order(graph):
    expected = project_game(graph, SPEC)
    triples = list(graph)
    Random(22).shuffle(triples)
    shuffled = Graph()
    for triple in triples:
        shuffled.add(triple)
    # A different incomplete representation does not affect the selected game.
    shuffled.add((EX.unrelated, RDF.type, EXT.DiscountedZeroSumMarkovRepresentation))
    before = set(shuffled)
    assert project_game(shuffled, SPEC) == expected
    assert set(shuffled) == before


def test_reordered_axes_move_labelled_values_and_probabilities(graph):
    for owner, predicate in ((REP, EXT.stateOrder), (EX.commissioner, EXT.actionOrder)):
        head = graph.value(owner, predicate)
        tail = graph.value(head, RDF.rest)
        first, second = graph.value(head, RDF.first), graph.value(tail, RDF.first)
        graph.set((head, RDF.first, second))
        graph.set((tail, RDF.first, first))

    payload = project_game(graph, SPEC)
    assert [state["id"] for state in payload["states"]] == [str(EX.pressure), str(EX.stable)]
    assert payload["initial"] == [0.25, 0.75]
    assert payload["players"][0]["actions"] == [str(EX.defer), str(EX.settle)]
    assert payload["states"][0]["outcomes"][1][0] == {
        "reward": -1.0,
        "transition": [0.75, 0.25],
    }
    assert payload["method"]["policy"] == [[[0.0, 1.0], [1.0, 0.0]]] * 2


def test_distinct_iris_with_same_local_name_remain_distinct(graph):
    renamed = URIRef("https://example.org/elsewhere/accept")
    rewritten = Graph()
    for subject, predicate, obj in graph:
        rewritten.add(
            (
                renamed if subject == EX.settle else subject,
                predicate,
                renamed if obj == EX.settle else obj,
            )
        )
    payload = project_game(rewritten, SPEC)
    assert payload["players"][0]["actions"][0] == str(renamed)
    assert payload["players"][1]["actions"][0] == str(EX.accept)
    assert payload["states"][0]["outcomes"][0][0]["reward"] == 2.0


def test_shape_targets_the_typed_representation(graph):
    resource = files("uogto.interchange").joinpath("discounted-markov-profile-v1.ttl")
    shape = Graph().parse(data=resource.read_text(encoding="utf-8"), format="turtle")
    assert validate(graph, shacl_graph=shape)[0]
    graph.remove((EX["stable-settle-accept"], EXT.stageReward, None))
    assert not validate(graph, shacl_graph=shape)[0]


@pytest.mark.parametrize(
    ("subject", "predicate", "old", "new", "detail"),
    [
        (REP, EXT.hasInitialWeight, EX["initial-pressure"], None, "incomplete bindings"),
        (
            EX["stable-settle-contend"],
            CORE.hasTransition,
            EX["ssc-pressure"],
            None,
            "incomplete bindings",
        ),
        (
            EX["commissioner-stable"],
            EXT.hasActionWeight,
            EX["weight-defer"],
            None,
            "incomplete bindings",
        ),
        (
            EX["stationary-profile"],
            EXT.hasPolicyRow,
            EX["provider-pressure"],
            None,
            "incomplete bindings",
        ),
        (
            EX["transition-kernel"],
            EXT.hasStageDecision,
            EX["pressure-defer-contend"],
            None,
            "incomplete bindings",
        ),
        (EX["ssc-pressure"], CORE.transitionsTo, EX.pressure, EX.stable, "duplicate binding"),
        (EX["ssc-pressure"], CORE.transitionsTo, EX.pressure, EX.foreign, "foreign binding"),
        (EX["ssa-stable"], CORE.transitionsFrom, EX.stable, EX.pressure, "transition source"),
        (EX["weight-defer"], CORE.hasAction, EX.defer, EX.settle, "duplicate binding"),
        (EX["weight-defer"], CORE.hasAction, EX.defer, EX.accept, "foreign binding"),
        (EX["initial-pressure"], EXT.atState, EX.pressure, EX.stable, "duplicate binding"),
        (EX.commissioner, CORE.observes, EX.pressure, None, "observe the complete state axis"),
        (EX.settle, CORE.belongsToPlayer, EX.commissioner, EX.provider, "different player"),
        (EX.stable, CORE.hasAvailableAction, EX.defer, None, "legal actions differ"),
        (REP, DCTERMS.conformsTo, PROFILE_IRI, EX.unknown, "expected profile"),
        (REP, EXT.modelDiscountFactor, None, Literal(1.0), "SHACL shape"),
        (
            REP,
            EXT.hasInitialWeight,
            EX["initial-pressure"],
            BNode("anonymous"),
            "SHACL shape",
        ),
    ],
)
def test_projector_fails_closed_under_changed_bindings(graph, subject, predicate, old, new, detail):
    graph.remove((subject, predicate, old))
    if new is not None:
        graph.add((subject, predicate, new))
    with pytest.raises(UnsupportedExecutableSubset, match=detail):
        project_game(graph, SPEC)


def test_duplicate_joint_actions_cannot_hide_behind_a_new_profile_iri(graph):
    alternate = EX["alternate-joint-action"]
    graph.add((alternate, RDF.type, CORE.ActionProfile))
    graph.add((alternate, CORE.hasAction, EX.settle))
    graph.add((alternate, CORE.hasAction, EX.accept))
    graph.set((EX["stable-defer-accept"], CORE.hasActionProfile, alternate))
    with pytest.raises(UnsupportedExecutableSubset, match="duplicate binding"):
        project_game(graph, SPEC)


def test_learning_discount_cannot_substitute_for_model_discount(graph):
    graph.remove((REP, EXT.modelDiscountFactor, None))
    graph.add((REP, EXT.discountFactor, Literal(0.75)))
    with pytest.raises(UnsupportedExecutableSubset, match="SHACL shape"):
        project_game(graph, SPEC)


def test_nonfinite_stage_reward_is_rejected(graph):
    graph.set((EX["stable-settle-accept"], EXT.stageReward, Literal(inf)))
    with pytest.raises(UnsupportedExecutableSubset, match="finite binary64"):
        project_game(graph, SPEC)


def test_cyclic_axis_is_rejected(graph):
    head = graph.value(REP, EXT.stateOrder)
    graph.set((head, RDF.rest, head))
    with pytest.raises(UnsupportedExecutableSubset, match="cyclic RDF list"):
        project_game(graph, SPEC)


def test_dataset_must_be_scoped_to_one_graph():
    dataset = Dataset()
    context = dataset.graph(EX.context).parse(FIXTURE, format="turtle")
    with pytest.raises(UnsupportedExecutableSubset, match="select one RDF graph context"):
        project_game(dataset, SPEC)
    assert project_game(context, SPEC)["discount"] == 0.75


# Both components stay in [0, 1]. The exact mass is one plus or minus the
# parsed tolerance, and a single binary64 step puts the case inside or outside.
TOLERANCE = 1e-12
STEP = 2.0**-39
DEFICIT_TAIL = STEP - TOLERANCE


@pytest.mark.parametrize(
    ("weights", "admitted"),
    [
        ((1.0, nextafter(TOLERANCE, 0.0)), True),
        ((1.0, TOLERANCE), True),
        ((1.0, nextafter(TOLERANCE, inf)), False),
        ((1.0 - STEP, nextafter(DEFICIT_TAIL, inf)), True),
        ((1.0 - STEP, DEFICIT_TAIL), True),
        ((1.0 - STEP, nextafter(DEFICIT_TAIL, 0.0)), False),
    ],
)
def test_exact_binary64_mass_bound_includes_only_admitted_weights(graph, weights, admitted):
    stable, pressure = weights
    graph.set((EX["initial-stable"], CORE.probability, Literal(stable)))
    graph.set((EX["initial-pressure"], CORE.probability, Literal(pressure)))
    if admitted:
        assert project_game(graph, SPEC)["initial"] == list(weights)
    else:
        with pytest.raises(UnsupportedExecutableSubset, match="distribution mass"):
            project_game(graph, SPEC)


def test_three_weight_mass_admission_does_not_depend_on_axis_order():
    small = 2.0**-54
    by_state = {EX.stable: 1.0, EX.pressure: small, EX.third: TOLERANCE - small}
    # A sequence of rounded additions can move this exact boundary case.
    assert (1.0 + small) + by_state[EX.third] != 1.0 + (small + by_state[EX.third])
    graph = Graph()
    for index, (state, weight) in enumerate(by_state.items()):
        entry = EX[f"initial-weight-{index}"]
        graph.add((REP, EXT.hasInitialWeight, entry))
        graph.add((entry, EXT.atState, state))
        graph.add((entry, CORE.probability, Literal(weight)))

    for order in permutations(by_state):
        axis = list(order)
        assert _distribution(graph, REP, EXT.hasInitialWeight, EXT.atState, axis) == [
            by_state[state] for state in axis
        ]
