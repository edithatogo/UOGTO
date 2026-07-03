"""Build the article-hardening source acquisition manifest.

The manifest separates checked-in redistributable source artifacts from
metadata-only or licence-constrained source references. It is intentionally
deterministic so article-hardening closeout does not depend on live downloads.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "article-hardening"
INVENTORY = DOCS / "source-extension-inventory.json"
MANIFEST_JSON = DOCS / "source-acquisition-manifest.json"
MANIFEST_MD = DOCS / "source-acquisition-manifest.md"
SOURCE_DIR = ROOT / "docs" / "ontology-comparison" / "sources"

LOCAL_SOURCE_MAP = {
    "owl_time": SOURCE_DIR / "owl_time.ttl",
    "prov_o": SOURCE_DIR / "prov_o.owl",
    "schema_org": SOURCE_DIR / "schema_org.ttl",
    "ssn_sosa": SOURCE_DIR / "ssn_sosa.ttl",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def read_inventory() -> dict:
    return json.loads(INVENTORY.read_text(encoding="utf-8"))


def local_artifact_record(source: dict, path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    suffix = path.suffix.lower()
    content_type = {
        ".ttl": "text/turtle",
        ".owl": "application/rdf+xml",
        ".rdf": "application/rdf+xml",
        ".json": "application/json",
        ".jsonld": "application/ld+json",
        ".xml": "application/xml",
    }.get(suffix, "application/octet-stream")
    return {
        "source_id": source["source_id"],
        "source_name": source["source_name"],
        "status": "checked_in_artifact",
        "path": rel(path),
        "canonical_url": source.get("canonical_url"),
        "content_type": content_type,
        "checksum": sha256(path),
        "retrieved_at": "preserved_from_comparative_baseline",
        "licence": source.get("licence", {}),
        "parseability": source.get("parseability"),
        "evidence_level": source.get("evidence_level"),
    }


def reference_record(source: dict) -> dict:
    return {
        "source_id": source["source_id"],
        "source_name": source["source_name"],
        "status": "reference_only_no_redistribution",
        "canonical_url": source.get("canonical_url"),
        "licence": source.get("licence", {}),
        "parseability": source.get("parseability"),
        "evidence_level": source.get("evidence_level"),
        "reason": source.get("limitations")
        or "No redistributable artifact is checked into the article-hardening source package.",
    }


def build_manifest() -> dict:
    inventory = read_inventory()
    artifacts = []
    references = []
    for source in sorted(inventory["sources"], key=lambda item: item["source_id"]):
        source_id = source["source_id"]
        if source_id in LOCAL_SOURCE_MAP:
            artifacts.append(local_artifact_record(source, LOCAL_SOURCE_MAP[source_id]))
        else:
            references.append(reference_record(source))
    return {
        "schema": "uogto.article-hardening.source-acquisition-manifest.v1",
        "generated_at_utc": "deterministic-local-preflight",
        "source_inventory": rel(INVENTORY),
        "artifact_directory": rel(SOURCE_DIR),
        "artifact_count": len(artifacts),
        "reference_only_count": len(references),
        "artifacts": artifacts,
        "reference_only_sources": references,
        "policy": (
            "Only redistributable or already checked-in comparator artifacts are represented as local "
            "files. Licence-constrained, metadata-only, literature-only, and structured non-RDF sources "
            "remain as source references with canonical URLs and licence dispositions."
        ),
    }


def write_manifest(payload: dict) -> None:
    MANIFEST_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Source Acquisition Manifest",
        "",
        payload["policy"],
        "",
        f"- Local artifacts: {payload['artifact_count']}",
        f"- Reference-only sources: {payload['reference_only_count']}",
        f"- Source inventory: `{payload['source_inventory']}`",
        f"- Artifact directory: `{payload['artifact_directory']}`",
        "",
        "## Checked-In Artifacts",
        "",
        "| Source | Path | Content type | Checksum |",
        "| --- | --- | --- | --- |",
    ]
    for artifact in payload["artifacts"]:
        lines.append(
            f"| `{artifact['source_id']}` | `{artifact['path']}` | `{artifact['content_type']}` | `{artifact['checksum']}` |"
        )
    lines.extend(["", "## Reference-Only Sources", "", "| Source | Evidence level | Reason |", "| --- | --- | --- |"])
    for source in payload["reference_only_sources"]:
        reason = str(source["reason"]).replace("|", "-")
        lines.append(f"| `{source['source_id']}` | `{source['evidence_level']}` | {reason} |")
    lines.append("")
    MANIFEST_MD.write_text("\n".join(lines), encoding="utf-8")


def validate_manifest(payload: dict) -> None:
    if payload["artifact_count"] < 4:
        raise AssertionError("Expected at least the four checked-in comparator RDF/OWL artifacts")
    source_ids = {item["source_id"] for item in payload["artifacts"] + payload["reference_only_sources"]}
    inventory_ids = {item["source_id"] for item in read_inventory()["sources"]}
    if source_ids != inventory_ids:
        raise AssertionError("Source acquisition manifest does not cover every inventory source")
    for artifact in payload["artifacts"]:
        if not artifact["checksum"].startswith("sha256:"):
            raise AssertionError(f"Artifact missing checksum: {artifact['source_id']}")
        if not artifact["content_type"]:
            raise AssertionError(f"Artifact missing content type: {artifact['source_id']}")


def main() -> int:
    payload = build_manifest()
    validate_manifest(payload)
    write_manifest(payload)
    print(
        "Source acquisition manifest ready: "
        f"{payload['artifact_count']} artifacts, {payload['reference_only_count']} reference-only sources."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
