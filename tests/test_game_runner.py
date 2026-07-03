from __future__ import annotations

from pathlib import Path

from uogto.runner.engine import RDFGameRunner
from uogto.runner.llm_player import LLMPlayerBench


def test_runner_scopes_actions_and_reified_payoffs_by_game(tmp_path: Path) -> None:
    ttl_path = tmp_path / "games.ttl"
    ttl_path.write_text(_scoped_reified_games(), encoding="utf-8")
    runner = RDFGameRunner(ttl_path)

    specs = runner.get_game_specification()
    assert {spec["uri"] for spec in specs} == {
        "http://example.org/game-a",
        "http://example.org/game-b",
    }

    alice_actions = runner.get_actions("http://example.org/game-a", "http://example.org/alice")
    bob_actions = runner.get_actions("http://example.org/game-a", "http://example.org/bob")
    assert [action["uri"] for action in alice_actions] == ["http://example.org/a-cooperate"]
    assert [action["uri"] for action in bob_actions] == ["http://example.org/b-cooperate"]

    payoffs = runner.query_payoff(
        "http://example.org/game-a",
        {
            "http://example.org/alice": "http://example.org/a-cooperate",
            "http://example.org/bob": "http://example.org/b-cooperate",
        },
    )
    assert payoffs == {
        "http://example.org/alice": 5.0,
        "http://example.org/bob": 1.0,
    }

    assert runner.query_payoff(
        "http://example.org/game-b",
        {
            "http://example.org/alice": "http://example.org/a-cooperate",
            "http://example.org/bob": "http://example.org/b-cooperate",
        },
    ) == {}


def test_runner_keeps_legacy_payoff_mapping_support(tmp_path: Path) -> None:
    ttl_path = tmp_path / "legacy.ttl"
    ttl_path.write_text(_legacy_mapping_game(), encoding="utf-8")
    runner = RDFGameRunner(ttl_path)

    payoffs = runner.query_payoff(
        "http://example.org/legacy-game",
        {
            "http://example.org/alice": "http://example.org/cooperate",
            "http://example.org/bob": "http://example.org/cooperate",
        },
    )
    assert payoffs == {
        "http://example.org/alice": 3.0,
        "http://example.org/bob": 3.0,
    }


def test_llm_player_bench_uses_runner_payoffs(tmp_path: Path) -> None:
    ttl_path = tmp_path / "games.ttl"
    ttl_path.write_text(_scoped_reified_games(), encoding="utf-8")
    bench = LLMPlayerBench(ttl_path)

    result = bench.run_session("http://example.org/game-a")
    assert result["choices"] == {
        "http://example.org/alice": "http://example.org/a-cooperate",
        "http://example.org/bob": "http://example.org/b-cooperate",
    }
    assert result["payoffs"]["http://example.org/alice"] == 5.0


def _scoped_reified_games() -> str:
    return """
        @prefix uogto: <https://w3id.org/uogto/core#> .
        @prefix ex: <http://example.org/> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        ex:game-a a uogto:GameSpecification ;
            rdfs:label "Game A" ;
            uogto:hasPlayer ex:alice, ex:bob ;
            uogto:hasActionSpace ex:alice-space, ex:bob-space ;
            uogto:hasStrategyProfile ex:profile-a .

        ex:game-b a uogto:GameSpecification ;
            rdfs:label "Game B" ;
            uogto:hasPlayer ex:alice, ex:bob ;
            uogto:hasStrategyProfile ex:profile-b .

        ex:alice a uogto:Player ; rdfs:label "Alice" .
        ex:bob a uogto:Player ; rdfs:label "Bob" .

        ex:alice-space a uogto:ActionSpace ;
            uogto:belongsToPlayer ex:alice ;
            uogto:hasAction ex:a-cooperate .
        ex:bob-space a uogto:ActionSpace ;
            uogto:belongsToPlayer ex:bob ;
            uogto:hasAction ex:b-cooperate .

        ex:a-cooperate a uogto:Action ;
            rdfs:label "Cooperate" ;
            uogto:belongsToPlayer ex:alice .
        ex:b-cooperate a uogto:Action ;
            rdfs:label "Cooperate" ;
            uogto:belongsToPlayer ex:bob .
        ex:other-action a uogto:Action ;
            rdfs:label "Cooperate" ;
            uogto:belongsToPlayer ex:alice .

        ex:profile-a a uogto:StrategyProfile ;
            uogto:hasAction ex:a-cooperate, ex:b-cooperate ;
            uogto:hasPayoff ex:payoff-profile-a .
        ex:payoff-profile-a a uogto:PayoffProfile ;
            uogto:hasPayoffForPlayer ex:alice-payoff-a, ex:bob-payoff-a .
        ex:alice-payoff-a a uogto:PlayerPayoffLink ;
            uogto:payoffPlayer ex:alice ;
            uogto:payoffValue 5.0 .
        ex:bob-payoff-a a uogto:PlayerPayoffLink ;
            uogto:payoffPlayer ex:bob ;
            uogto:payoffValue 1.0 .

        ex:profile-b a uogto:StrategyProfile ;
            uogto:hasAction ex:other-action, ex:b-cooperate ;
            uogto:hasPayoff ex:payoff-profile-b .
        ex:payoff-profile-b a uogto:PayoffProfile ;
            uogto:hasPayoffForPlayer ex:alice-payoff-b, ex:bob-payoff-b .
        ex:alice-payoff-b a uogto:PlayerPayoffLink ;
            uogto:payoffPlayer ex:alice ;
            uogto:payoffValue 9.0 .
        ex:bob-payoff-b a uogto:PlayerPayoffLink ;
            uogto:payoffPlayer ex:bob ;
            uogto:payoffValue 9.0 .
    """


def _legacy_mapping_game() -> str:
    return """
        @prefix uogto: <https://w3id.org/uogto/core#> .
        @prefix ex: <http://example.org/> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        ex:legacy-game a uogto:GameSpecification ;
            rdfs:label "Legacy" ;
            uogto:hasPlayer ex:alice, ex:bob ;
            uogto:hasPayoffMapping ex:mapping-alice, ex:mapping-bob .
        ex:alice a uogto:Player ; rdfs:label "Alice" .
        ex:bob a uogto:Player ; rdfs:label "Bob" .
        ex:cooperate a uogto:Action ; uogto:belongsToPlayer ex:alice, ex:bob .
        ex:profile a uogto:ActionProfile ; uogto:hasAction ex:cooperate .
        ex:mapping-alice a uogto:PayoffMapping ;
            uogto:hasActionProfile ex:profile ;
            uogto:belongsToPlayer ex:alice ;
            uogto:payoffValue 3.0 .
        ex:mapping-bob a uogto:PayoffMapping ;
            uogto:hasActionProfile ex:profile ;
            uogto:belongsToPlayer ex:bob ;
            uogto:payoffValue 3.0 .
    """
