from pathlib import Path

import pytest
from rdflib import Graph, OWL, RDF, URIRef

from scripts.maintenance import audit_semantics as audit


@pytest.mark.parametrize("namespace", audit.TERM_NAMESPACES.values())
def test_registered_namespaces_are_accepted(namespace) -> None:
    graph = Graph()
    graph.add((URIRef(namespace + "ExampleClass"), RDF.type, OWL.Class))
    assert audit.audit_namespace_policy(graph)


@pytest.mark.parametrize(
    "namespace",
    [
        "https://w3id.org/uogto/packs/unregistered#",
        "https://w3id.org/uogto/bridges/unregistered#",
        "https://w3id.org/uogto/packs/costing-valuations#",
        "https://w3id.org/uogto/core/",
    ],
)
def test_unregistered_or_misspelled_namespaces_are_rejected(namespace, capsys) -> None:
    graph = Graph()
    graph.add((URIRef(namespace + "ExampleClass"), RDF.type, OWL.Class))
    assert not audit.audit_namespace_policy(graph)
    assert "Invalid UOGTO namespace" in capsys.readouterr().out


def test_costing_pack_and_bridge_have_audited_jsonld_coverage() -> None:
    graph = Graph()
    for path in ("ontologies/applied/costing-valuation.ttl", "ontologies/bridges/costing-hta.ttl"):
        graph.parse(audit.ROOT / path, format="turtle")
    assert audit.audit_jsonld_term_coverage(graph)


@pytest.mark.parametrize("namespace", [audit.PACK_NAMESPACES["cost"], audit.BRIDGE_NAMESPACES["costhta"]])
def test_missing_new_module_context_terms_are_rejected(namespace, capsys) -> None:
    graph = Graph()
    graph.add((URIRef(namespace + "UndocumentedClass"), RDF.type, OWL.Class))
    assert not audit.audit_jsonld_term_coverage(graph)
    assert "JSON-LD context missing term coverage" in capsys.readouterr().out


def write_example(tmp_path: Path, monkeypatch, body: str) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    examples = tmp_path / "examples"
    examples.mkdir()
    (examples / "fixture.ttl").write_text(
        """
        @prefix ex: <https://example.org/audit/> .
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        """ + body,
        encoding="utf-8",
    )


def test_example_schema_and_individuals_follow_distinct_naming_rules(tmp_path, monkeypatch) -> None:
    write_example(tmp_path, monkeypatch, """
        ex:Infant a owl:Class .
        ex:Specimen a rdfs:Class .
        ex:hasSpecimen a owl:ObjectProperty .
        ex:specimenCount a owl:DatatypeProperty .
        ex:infant-a a ex:Infant ; ex:hasSpecimen ex:specimen-a .
        ex:specimen-a a ex:Specimen .
    """)
    assert audit.audit_instance_naming()


@pytest.mark.parametrize(
    ("body", "message"),
    [
        ("ex:Infant a owl:Class . ex:BadInstance a ex:Infant .", "instance is not kebab-case"),
        ("ex:bad-class a owl:Class .", "class is not UpperCamelCase"),
        ("ex:BadProperty a owl:ObjectProperty .", "property is not lowerCamelCase"),
    ],
)
def test_example_naming_does_not_exempt_invalid_terms(tmp_path, monkeypatch, capsys, body, message) -> None:
    write_example(tmp_path, monkeypatch, body)
    assert not audit.audit_instance_naming()
    assert message in capsys.readouterr().out


def test_repository_examples_pass_type_aware_naming_audit() -> None:
    assert audit.audit_instance_naming()
