import argparse
import hashlib
import json
from pathlib import Path

from rdflib import Graph


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "article-hardening"
DEFAULT_MANIFEST = DOCS / "ontology-snapshot-manifest.json"
DEFAULT_SUPPLEMENT = DOCS / "ontology-snapshot-supplement.md"
DEFAULT_CITATION_JSON = DOCS / "ontology-citation-register.json"
DEFAULT_CITATION_MD = DOCS / "ontology-citation-register.md"

ONTOLOGY_COPY_ASSETS = [
    ROOT / "dist" / "uogto.ttl",
    ROOT / "dist" / "uogto-shapes.ttl",
    ROOT / "dist" / "context.jsonld",
    ROOT / "dist" / "core.context.jsonld",
    ROOT / "dist" / "extensions.context.jsonld",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def collect_files(paths: list[Path]) -> list[dict]:
    rows = []
    for path in sorted(paths, key=lambda item: rel(item)):
        if not path.exists():
            raise AssertionError(f"Missing expected snapshot file: {rel(path)}")
        rows.append(
            {
                "path": rel(path),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return rows


def graph_summary(path: Path) -> dict:
    graph = Graph()
    graph.parse(path, format="turtle")
    return {"path": rel(path), "triple_count": len(graph)}


def load_references(path: Path) -> list[dict]:
    references = json.loads(path.read_text(encoding="utf-8"))
    return sorted(references, key=lambda item: item["id"])


def compact_reference(record: dict) -> dict:
    authors = []
    for author in record.get("author", []):
        if "literal" in author:
            authors.append(author["literal"])
        else:
            name = " ".join(part for part in [author.get("given"), author.get("family")] if part)
            if name:
                authors.append(name)
    issued = record.get("issued", {}).get("date-parts", [[None]])[0][0]
    return {
        "id": record["id"],
        "type": record.get("type"),
        "title": record.get("title"),
        "authors": authors,
        "year": issued,
        "doi": record.get("DOI"),
        "url": record.get("URL"),
        "source_note": record.get("source_note"),
    }


def build_manifest() -> dict:
    ontology_sources = collect_files(list((ROOT / "ontologies").glob("**/*.ttl")))
    release_assets = collect_files(ONTOLOGY_COPY_ASSETS)
    source_graphs = [graph_summary(ROOT / row["path"]) for row in ontology_sources]
    release_graphs = [
        graph_summary(ROOT / "dist" / "uogto.ttl"),
        graph_summary(ROOT / "dist" / "uogto-shapes.ttl"),
    ]
    references = [compact_reference(record) for record in load_references(ROOT / "docs" / "paper" / "references.csl.json")]
    manifest = {
        "schema": "uogto.ontology-snapshot-supplement.v1",
        "generated_at_utc": "deterministic-local-preflight",
        "purpose": "Repository-only ontology snapshot and citation register for manuscript evidence traceability.",
        "submission_policy": "Do not include in arXiv or journal submission unless requested by reviewers.",
        "ontology_copy_assets": release_assets,
        "ontology_source_files": ontology_sources,
        "graph_summaries": {
            "release_graphs": release_graphs,
            "source_graphs": source_graphs,
        },
        "citation_source": "docs/paper/references.csl.json",
        "citation_count": len(references),
        "citations": references,
    }
    return manifest


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def render_snapshot_markdown(manifest: dict) -> str:
    source_count = len(manifest["ontology_source_files"])
    merged = next(item for item in manifest["graph_summaries"]["release_graphs"] if item["path"] == "dist/uogto.ttl")
    shapes = next(item for item in manifest["graph_summaries"]["release_graphs"] if item["path"] == "dist/uogto-shapes.ttl")
    lines = [
        "# Repository-only ontology snapshot supplement",
        "",
        "Date: 2026-07-02",
        "",
        "This supplement identifies the exact ontology copy and modular ontology source files that correspond to the manuscript and raw-search evidence package. It is a repository evidence artefact only. It does not need to be submitted with the arXiv preprint or a journal manuscript unless a reviewer asks for a raw ontology snapshot ledger.",
        "",
        "## Snapshot Summary",
        "",
        f"- Modular ontology source files: {source_count}",
        f"- Merged ontology copy: `dist/uogto.ttl` ({merged['triple_count']} triples)",
        f"- Merged SHACL copy: `dist/uogto-shapes.ttl` ({shapes['triple_count']} triples)",
        f"- Citation register entries: {manifest['citation_count']}",
        "- Machine-readable manifest: `docs/article-hardening/ontology-snapshot-manifest.json`",
        "- Citation register: `docs/article-hardening/ontology-citation-register.md` and `.json`",
        "",
        "## Ontology Copy Assets",
        "",
        "| Path | Bytes | SHA-256 |",
        "| --- | ---: | --- |",
    ]
    for asset in manifest["ontology_copy_assets"]:
        lines.append(f"| `{asset['path']}` | {asset['bytes']} | `{asset['sha256']}` |")
    lines += [
        "",
        "## Modular Ontology Source Files",
        "",
        "These are the version-controlled Turtle files merged into the release ontology copy.",
        "",
        "| Path | Bytes | SHA-256 |",
        "| --- | ---: | --- |",
    ]
    for asset in manifest["ontology_source_files"]:
        lines.append(f"| `{asset['path']}` | {asset['bytes']} | `{asset['sha256']}` |")
    lines += [
        "",
        "## Use In The Evidence Trail",
        "",
        "- Cite `dist/uogto.ttl` as the compact ontology copy for repository review.",
        "- Cite `ontologies/` when reviewers need module-level provenance.",
        "- Cite `docs/article-hardening/ontology-citation-register.md` for the corresponding final reference list.",
        "- Keep this supplement repository-facing unless a submission venue requests raw ontology assets.",
        "",
    ]
    return "\n".join(lines)


def render_citation_markdown(manifest: dict) -> str:
    lines = [
        "# Repository-only ontology citation register",
        "",
        "Date: 2026-07-02",
        "",
        "This register lists the final citation set corresponding to the UOGTO ontology snapshot and manuscript evidence package. The machine-readable source is `docs/paper/references.csl.json`; the preferred ontology citation is recorded in `CITATION.cff` and `docs/how-to-cite-and-reuse-uogto.md`.",
        "",
        "## Preferred Ontology Citation",
        "",
        "> Dylan A Mordaunt. *Universal Open Game Theory Ontology: A semantic resource for strategic-interaction evidence*. Version 1.0.0. Zenodo. DOI: 10.5281/zenodo.20796937.",
        "",
        "## Final Reference Set",
        "",
        "| ID | Type | Citation target | DOI/URL | Role in ontology evidence |",
        "| --- | --- | --- | --- | --- |",
    ]
    for ref in manifest["citations"]:
        target = ref["title"].replace("|", "/") if ref.get("title") else ref["id"]
        doi_or_url = ref.get("doi") or ref.get("url") or ""
        role = (ref.get("source_note") or "").replace("|", "/")
        lines.append(f"| `{ref['id']}` | `{ref.get('type')}` | {target} | {doi_or_url} | {role} |")
    lines += [
        "",
        "## Expanded Source Context",
        "",
        "For broader search context beyond the final cited reference set, use `docs/paper/source-inventory.json` and `docs/article-hardening/raw-search-output-supplement.md`.",
        "",
    ]
    return "\n".join(lines)


def build_outputs(
    manifest_path: Path = DEFAULT_MANIFEST,
    supplement_path: Path = DEFAULT_SUPPLEMENT,
    citation_json_path: Path = DEFAULT_CITATION_JSON,
    citation_md_path: Path = DEFAULT_CITATION_MD,
) -> dict:
    manifest = build_manifest()
    write_json(manifest_path, manifest)
    write_json(citation_json_path, {"schema": "uogto.ontology-citation-register.v1", "citations": manifest["citations"]})
    supplement_path.write_text(render_snapshot_markdown(manifest), encoding="utf-8")
    citation_md_path.write_text(render_citation_markdown(manifest), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build repository-only ontology snapshot supplement and citation register.")
    parser.add_argument("--check-only", action="store_true", help="Validate generated inputs without writing outputs.")
    args = parser.parse_args()
    manifest = build_manifest()
    if not args.check_only:
        build_outputs()
    print(
        "Ontology snapshot supplement ready: "
        f"{len(manifest['ontology_source_files'])} source files, "
        f"{len(manifest['ontology_copy_assets'])} copy assets, "
        f"{manifest['citation_count']} citation records."
    )


if __name__ == "__main__":
    main()
