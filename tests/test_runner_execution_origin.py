from __future__ import annotations

import json
import sys

from uogto.runner.engine import RDFGameRunner, main as inspection_main
from uogto.runner.llm_player import (
    FirstActionPlayer, FirstActionPlayerBench, LLMPlayer, LLMPlayerBench,
    main as baseline_main,
)


def test_legacy_names_are_explicit_first_action_baseline():
    assert LLMPlayer is FirstActionPlayer
    assert LLMPlayerBench is FirstActionPlayerBench
    player = LLMPlayer("Alice", model_name="compatibility-only")
    assert player.model_name == "compatibility-only"
    assert player.make_choice("ignored", ["b", "a"]) == "b"
    assert player.make_choice("ignored", []) is None
    assert player.execution_origin == "deterministic_first_action_baseline"
    assert RDFGameRunner.execution_origin == "reference_graph_inspection"


def test_baseline_cli_emits_one_json_document_with_execution_origin(tmp_path, monkeypatch, capsys):
    graph = tmp_path / "game.ttl"
    graph.write_text('''
@prefix u: <https://w3id.org/uogto/core#> .
@prefix ex: <https://example.org/> .
ex:game a u:GameSpecification ; u:hasPlayer ex:p ; u:hasActionSpace ex:s .
ex:s u:belongsToPlayer ex:p ; u:hasAction ex:action .
''', encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["uogto-runner-bench", str(graph), "https://example.org/game"])
    baseline_main()
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert captured.err == ""
    assert result["execution_origin"] == "deterministic_first_action_baseline"
    assert result["model_request_performed"] is False
    assert result["native_solver_performed"] is False
    assert result["payoff_origin"] == "stored_graph_lookup"
    assert result["choices"] == {"https://example.org/p": "https://example.org/action"}


def test_inspection_cli_preserves_tabular_output(tmp_path, monkeypatch, capsys):
    graph = tmp_path / "game.ttl"
    graph.write_text('''
@prefix u: <https://w3id.org/uogto/core#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
<https://example.org/game> a u:GameSpecification ; rdfs:label "Example" .
''', encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["uogto-runner", str(graph)])
    inspection_main()
    captured = capsys.readouterr()
    assert captured.out == "https://example.org/game\tExample\n"
    assert captured.err == ""
