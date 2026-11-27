"""Run the UOGTO RDF projection through the immutable native Paignia consumer."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from rdflib import Graph, URIRef

from uogto.interchange.information_sets import project_information_sets

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures"
SPECIFICATION = "https://example.org/doors#specification"
INFORMATION_SET = "https://example.org/doors#choix-privé"
LEFT = "https://example.org/doors/left#choice"
RIGHT = "https://example.org/doors/right#choice"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cargo", default="cargo")
    args = parser.parse_args()

    graph = Graph().parse(FIXTURES / "paignia-information-set-v1.ttl", format="turtle")
    projection = project_information_sets(graph, URIRef(SPECIFICATION))
    native = subprocess.run(
        [
            args.cargo, "run", "--quiet", "--locked",
            "--manifest-path", str(FIXTURES / "paignia-information-set-native/Cargo.toml"),
            "--target-dir", str(ROOT / "target/paignia-information-set-native"),
        ],
        input=json.dumps(projection),
        encoding="utf-8",
        stdout=subprocess.PIPE,
        check=True,
    )
    actual = json.loads(native.stdout)
    expected = {
        "specification_iri": SPECIFICATION,
        "id": INFORMATION_SET,
        "player": "https://example.org/doors#décideur",
        "members": [LEFT, RIGHT],
        "actions": ["play", "pass"],
        "assignments": {LEFT: INFORMATION_SET, RIGHT: INFORMATION_SET},
        "rejections": [
            "information_set_player_mismatch",
            "unassigned_information_set_decision",
            "information_set_action_mismatch",
            "imperfect_recall",
        ],
    }
    if actual != expected:
        raise SystemExit(f"Unexpected native information-set result: {actual!r}")
    print(json.dumps(actual, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
