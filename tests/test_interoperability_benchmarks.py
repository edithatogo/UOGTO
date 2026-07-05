from __future__ import annotations

import json
from pathlib import Path

from rdflib import Graph, URIRef

from uogto.runner.engine import RDFGameRunner


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "docs" / "interoperability-benchmarks.json"
UOGTO = "https://w3id.org/uogto/core#"
UOGTOX = "https://w3id.org/uogto/extensions#"


def load_inventory() -> dict:
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


def parse_fixture(path: str) -> Graph:
    graph = Graph()
    graph.parse(ROOT / path, format="json-ld")
    return graph


def test_inventory_records_required_target_fields() -> None:
    inventory = load_inventory()
    assert inventory["track_id"] == "uogto_interoperability_benchmarks_20260705"

    targets = inventory["targets"]
    assert {target["id"] for target in targets} >= {
        "openspiel-matrix-game",
        "pettingzoo-aec-gridworld",
        "gambit-strategic-game",
        "gymnasium-single-agent-wrapper",
        "mesa-abm-binding",
    }

    for target in targets:
        assert target["target_tool"]
        assert target["license_spdx"]
        assert target["integration_status"] in {
            "asserted_fixture",
            "illustrative_fixture",
            "future_candidate",
        }
        assert target["mapping_claim_level"]
        assert target["priority"] >= 1
        if target["integration_status"].endswith("_fixture"):
            fixture = target["fixture_path"]
            assert fixture
            assert (ROOT / fixture).exists()
            assert target["verification_command"]
            assert target["verification"]


def test_fixture_inventory_paths_parse_and_have_execution_bindings() -> None:
    inventory = load_inventory()
    fixture_targets = [
        target for target in inventory["targets"] if target["integration_status"].endswith("_fixture")
    ]
    assert len(fixture_targets) >= 2

    for target in fixture_targets:
        graph = parse_fixture(target["fixture_path"])
        rows = list(
            graph.query(
                """
                PREFIX uogtox: <https://w3id.org/uogto/extensions#>
                SELECT ?game ?binding WHERE {
                  ?game a uogtox:ExecutableGameGraph ;
                        uogtox:hasExecutionBinding ?binding .
                  ?binding a uogtox:ExecutionBinding .
                }
                """
            )
        )
        assert rows, f"{target['fixture_path']} has no executable game binding"


def test_openspiel_fixture_is_queryable_by_runner() -> None:
    fixture = ROOT / "examples" / "openspiel-matrix-game.jsonld"
    runner = RDFGameRunner(fixture)
    game_uri = "http://example.org/uogto/interop/openspiel-matrix-game"
    row_player = "http://example.org/uogto/interop/openspiel/row-player"
    column_player = "http://example.org/uogto/interop/openspiel/column-player"

    specs = runner.get_game_specification()
    assert game_uri in {spec["uri"] for spec in specs}

    row_actions = runner.get_actions(game_uri, row_player)
    assert {action["uri"] for action in row_actions} == {
        "http://example.org/uogto/interop/openspiel/row-cooperate",
        "http://example.org/uogto/interop/openspiel/row-defect",
    }

    payoffs = runner.query_payoff(
        game_uri,
        {
            row_player: "http://example.org/uogto/interop/openspiel/row-defect",
            column_player: "http://example.org/uogto/interop/openspiel/column-cooperate",
        },
    )
    assert payoffs == {row_player: 5.0, column_player: 0.0}


def test_runner_format_detection_handles_paths_and_urls() -> None:
    class NamedFile:
        name = "examples/game.jsonld"

    assert RDFGameRunner._format_for_path(Path("examples/game.jsonld")) == "json-ld"
    assert RDFGameRunner._format_for_path("examples/game.json") == "json-ld"
    assert RDFGameRunner._format_for_path("examples/game.ttl") == "turtle"
    assert RDFGameRunner._format_for_path(NamedFile()) == "json-ld"
    assert (
        RDFGameRunner._format_for_path("https://example.org/uogto/game.jsonld?download=1")
        == "json-ld"
    )
    assert RDFGameRunner._format_for_path("https://example.org/uogto/game.ttl?download=1") == "turtle"
    assert RDFGameRunner._format_for_path("examples/game-without-extension") == "turtle"


def test_pettingzoo_fixture_exposes_markov_runtime_bindings() -> None:
    graph = parse_fixture("examples/pettingzoo-aec-gridworld.jsonld")
    rows = list(
        graph.query(
            """
            PREFIX uogto: <https://w3id.org/uogto/core#>
            PREFIX uogtox: <https://w3id.org/uogto/extensions#>
            SELECT ?game ?transition ?runtime ?simulation WHERE {
              ?game a uogtox:MarkovGame ;
                    uogto:hasTransition ?transition ;
                    uogtox:hasExecutionBinding ?binding .
              ?binding uogtox:hasRuntimeBinding ?runtime ;
                       uogtox:hasSimulationBinding ?simulation .
            }
            """
        )
    )
    assert rows == [
        (
            URIRef("http://example.org/uogto/interop/pettingzoo-aec-gridworld"),
            URIRef("http://example.org/uogto/interop/pettingzoo/gridworld-transition"),
            URIRef("http://example.org/uogto/interop/pettingzoo/aec-runtime-binding"),
            URIRef("http://example.org/uogto/interop/pettingzoo/aec-simulation-binding"),
        )
    ]
