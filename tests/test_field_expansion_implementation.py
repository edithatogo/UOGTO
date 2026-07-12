from __future__ import annotations

import csv
from pathlib import Path

from pyshacl import validate as shacl_validate
from rdflib import Graph, Namespace, RDF

ROOT = Path(__file__).resolve().parents[1]
UOGTOX = Namespace("https://w3id.org/uogto/extensions#")

EXAMPLES = {
    "mean-field-routing-game.ttl": UOGTOX.MeanFieldGame,
    "two-route-congestion-game.ttl": UOGTOX.RoutingGame,
    "evolutionary-hawk-dove-game.ttl": UOGTOX.EvolutionaryGame,
    "institutional-information-design-games.ttl": UOGTOX.InformationDesignGame,
    "marl-learning-episode.ttl": UOGTOX.MarkovGame,
    "reputation-trust-game.ttl": None,
}


def test_field_examples_parse_and_conform() -> None:
    ontology = Graph()
    for path in (ROOT / "ontologies").rglob("*.ttl"):
        ontology.parse(path, format="turtle")
    shapes = Graph().parse(ROOT / "shapes" / "field-expansions.shacl.ttl", format="turtle")
    for filename, expected_type in EXAMPLES.items():
        example = Graph().parse(ROOT / "examples" / filename, format="turtle")
        if expected_type is not None:
            assert any(example.subjects(RDF.type, expected_type)), filename
        conforms, _results, report = shacl_validate(
            ontology + example, shacl_graph=shapes, ont_graph=ontology, inference="rdfs"
        )
        assert conforms, f"{filename}: {report}"


def test_decision_ledger_covers_every_field_issue_and_disposition() -> None:
    with (ROOT / "docs" / "roadmap" / "field-expansion-decision-ledger.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert {row["issue"] for row in rows} == {"77", "78", "79", "80", "81", "82"}
    assert {row["disposition"] for row in rows} >= {"accepted", "external", "deferred"}
    for row in rows:
        assert (ROOT / row["evidence"]).exists(), row


def test_applied_pack_backlog_names_all_four_pack_families() -> None:
    text = (ROOT / "docs" / "roadmap" / "applied-extension-pack-backlog.md").read_text(
        encoding="utf-8"
    )
    for phrase in ("Health economics", "Medical decision", "Safety systems", "Genomic policy"):
        assert phrase in text
