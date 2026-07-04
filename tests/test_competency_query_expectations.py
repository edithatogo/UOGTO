from __future__ import annotations

import json
from pathlib import Path

from rdflib import Graph


ROOT = Path(__file__).resolve().parents[1]


def test_competency_query_expectation_manifest_is_satisfied() -> None:
    manifest = json.loads(
        (ROOT / "validation" / "competency-query-expectations.json").read_text(encoding="utf-8")
    )
    ontology = Graph()
    for path in (ROOT / "ontologies").rglob("*.ttl"):
        ontology.parse(path, format="turtle")

    for entry in manifest["queries"]:
        graph = Graph()
        graph += ontology
        for example in entry.get("example_graphs", []):
            path = ROOT / example
            graph.parse(path, format="json-ld" if path.suffix == ".jsonld" else "turtle")

        rows = list(graph.query((ROOT / "competency-questions" / entry["query"]).read_text()))
        assert len(rows) >= entry.get("min_count", 0), entry["query"]
        labels = [str(var) for var in rows[0].labels] if rows else []
        bindings = [{labels[index]: str(value) for index, value in enumerate(row)} for row in rows]
        for required in entry.get("required_bindings", []):
            assert any(
                all(row.get(binding) == value for binding, value in required.items())
                for row in bindings
            ), entry["query"]


def test_every_competency_query_has_expected_results() -> None:
    manifest = json.loads(
        (ROOT / "validation" / "competency-query-expectations.json").read_text(encoding="utf-8")
    )
    expected_queries = {entry["query"] for entry in manifest["queries"]}
    actual_queries = {path.name for path in (ROOT / "competency-questions").glob("*.rq")}

    assert expected_queries == actual_queries


def test_no_legacy_competency_expectation_manifest() -> None:
    assert not (ROOT / "competency-questions" / "expected-results.json").exists()
