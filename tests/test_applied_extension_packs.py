from pathlib import Path
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]


def test_each_applied_pack_is_separate_and_imports_core() -> None:
    pack_dir = ROOT / "ontologies" / "applied"
    packs = list(pack_dir.glob("*.ttl"))
    assert len(packs) == 4
    for pack in packs:
        graph = Graph().parse(pack, format="turtle")
        assert len(graph) > 0
        assert "owl:imports <https://w3id.org/uogto/core>" in pack.read_text(encoding="utf-8")


def test_applied_pack_examples_and_shapes_exist() -> None:
    for name in ("hta-payer-adoption-game.ttl", "shared-treatment-choice-game.ttl", "safety-barrier-coordination-game.ttl", "genomic-data-access-game.ttl"):
        assert (ROOT / "examples" / name).exists()
    assert (ROOT / "shapes" / "applied-packs.shacl.ttl").exists()
