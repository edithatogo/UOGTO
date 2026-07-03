from __future__ import annotations

from pathlib import Path

from pyshacl import validate as shacl_validate
from rdflib import Graph


ROOT = Path(__file__).resolve().parents[1]


def test_representative_negative_shacl_fixtures_are_rejected() -> None:
    cases = [
        ("core", "ex:g a uogto:GameSpecification ."),
        ("game-types", "ex:g a uogtox:SecurityGame ."),
        ("execution", "ex:a a uogtox:LLMAgent ."),
        ("examples", "ex:p a uogto:Player ."),
        ("governance", "ex:m a uogtox:Mechanism ."),
    ]
    for shape_name, body in cases:
        data_graph = Graph()
        data_graph.parse(data=_ttl(body), format="turtle")
        shape_graph = Graph()
        shape_graph.parse(ROOT / "shapes" / f"{shape_name}.shacl.ttl", format="turtle")
        conforms, _results_graph, _results_text = shacl_validate(
            data_graph,
            shacl_graph=shape_graph,
            inference="rdfs",
        )
        assert not conforms, shape_name


def _ttl(body: str) -> str:
    return f"""
        @prefix ex: <http://example.org/> .
        @prefix uogto: <https://w3id.org/uogto/core#> .
        @prefix uogtox: <https://w3id.org/uogto/extensions#> .
        {body}
    """
