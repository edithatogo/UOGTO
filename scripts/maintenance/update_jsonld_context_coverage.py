from __future__ import annotations

import json
from pathlib import Path

from rdflib import Graph, OWL, RDF


ROOT = Path(__file__).resolve().parents[2]
CONTEXTS = [
    (ROOT / "jsonld" / "core.context.jsonld", "https://w3id.org/uogto/core#", "uogto"),
    (ROOT / "jsonld" / "extensions.context.jsonld", "https://w3id.org/uogto/extensions#", "uogtox"),
]


def main() -> None:
    graph = Graph()
    for path in (ROOT / "ontologies").rglob("*.ttl"):
        graph.parse(path, format="turtle")

    for context_path, namespace, prefix in CONTEXTS:
        data = json.loads(context_path.read_text(encoding="utf-8"))
        context = data["@context"]
        for kind in [OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty]:
            for subject in sorted(set(graph.subjects(RDF.type, kind)), key=str):
                value = str(subject)
                if not value.startswith(namespace):
                    continue
                local = value.removeprefix(namespace)
                if local in context:
                    continue
                compact = f"{prefix}:{local}"
                if kind == OWL.Class:
                    context[local] = compact
                elif kind == OWL.ObjectProperty:
                    context[local] = {"@id": compact, "@type": "@id"}
                else:
                    context[local] = {"@id": compact}
        context_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
