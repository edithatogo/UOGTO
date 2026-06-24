import argparse
import hashlib
import json
import mimetypes
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from rdflib import Graph


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.maintenance import build_ontology_comparison_inventory
DEFAULT_INVENTORY = ROOT / "docs" / "ontology-comparison" / "source-inventory.json"
DEFAULT_PROVENANCE = ROOT / "docs" / "ontology-comparison" / "source-provenance.json"
DEFAULT_SOURCE_DIR = ROOT / "docs" / "ontology-comparison" / "sources"

REDISTRIBUTABLE = "redistributable_artifact"
CONTENT_TYPE_EXTENSIONS = {
    "text/turtle": ".ttl",
    "application/rdf+xml": ".owl",
    "application/ld+json": ".jsonld",
}

RDF_FORMAT_HINTS = {
    ".ttl": "turtle",
    ".nt": "nt",
    ".n3": "n3",
    ".rdf": "xml",
    ".owl": "xml",
    ".xml": "xml",
    ".jsonld": "json-ld",
    ".json": "json-ld",
}
NON_RDF_FORMAT_HINTS = (
    "XML schema",
    "JSON schema",
    "CSV",
    "documentation",
    "standard",
    "logic language",
    "metamodel",
)


class HarvestError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def safe_source_filename(source_id: str, url: str, content_type: str | None = None) -> str:
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if not suffix or len(suffix) > 10:
        normalized_type = (content_type or "").split(";")[0].strip().lower()
        suffix = CONTENT_TYPE_EXTENSIONS.get(normalized_type) or mimetypes.guess_extension(normalized_type) or ".dat"
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", f"{source_id}{suffix}")


def checksum_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def classify_expected_format(expected_format: str) -> str:
    lowered = expected_format.lower()
    if any(token.lower() in lowered for token in NON_RDF_FORMAT_HINTS):
        return "non_rdf_or_documentation"
    if "rdf" in lowered or "owl" in lowered or "skos" in lowered or "turtle" in lowered:
        return "rdf_candidate"
    return "unknown"


def infer_rdflib_format(path: Path, content_type: str | None) -> str | None:
    suffix = path.suffix.lower()
    if suffix in RDF_FORMAT_HINTS:
        return RDF_FORMAT_HINTS[suffix]
    lowered = (content_type or "").lower()
    if "turtle" in lowered:
        return "turtle"
    if "json" in lowered and "ld" in lowered:
        return "json-ld"
    if "rdf+xml" in lowered or "xml" in lowered:
        return "xml"
    return None


def parse_rdf_file(path: Path, content_type: str | None = None) -> dict:
    graph = Graph()
    guessed_format = infer_rdflib_format(path, content_type)
    attempts = [guessed_format] if guessed_format else []
    attempts.extend(fmt for fmt in ["turtle", "xml", "json-ld", "nt", "n3"] if fmt not in attempts)
    errors = []
    for fmt in attempts:
        try:
            graph.parse(path, format=fmt)
            return {"parse_status": "parsed", "rdf_format": fmt, "triple_count": len(graph)}
        except Exception as exc:
            errors.append(f"{fmt}: {exc}")
    return {"parse_status": "parse_failed", "rdf_format": guessed_format, "triple_count": 0, "parse_error": errors[0]}


def fetch_bytes(url: str, timeout: int = 60) -> tuple[bytes, dict]:
    request = Request(
        url,
        headers={
            "Accept": "text/turtle, application/rdf+xml, application/ld+json, application/xml;q=0.8, */*;q=0.5",
            "User-Agent": "UOGTO ontology comparison harvester/0.1",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        return response.read(), {
            "http_status": getattr(response, "status", 200),
            "content_type": response.headers.get("Content-Type"),
            "canonical_url": response.geturl(),
        }


def metadata_only_record(source: dict, timestamp: str, reason: str) -> dict:
    return {
        "id": source["id"],
        "name": source["name"],
        "family": source["family"],
        "source_url": source["source_url"],
        "artifact_url": source.get("artifact_url"),
        "licence_disposition": source["licence_disposition"],
        "retrieval_timestamp": timestamp,
        "retrieval_mode": "metadata_only",
        "http_status": None,
        "content_type": None,
        "canonical_url": source.get("artifact_url") or source["source_url"],
        "checksum_sha256": None,
        "byte_size": None,
        "local_path": None,
        "format_classification": classify_expected_format(source["expected_format"]),
        "parse_status": "not_attempted",
        "rdf_format": None,
        "triple_count": 0,
        "manual_review_note": reason,
    }


def harvest_source(source: dict, source_dir: Path, timestamp: str, fetcher: Callable[[str], tuple[bytes, dict]] = fetch_bytes) -> dict:
    if source["licence_disposition"] != REDISTRIBUTABLE or not source.get("artifact_url"):
        return metadata_only_record(source, timestamp, "No artifact was downloaded because the source is not currently classified as redistributable.")
    url = source["artifact_url"]
    try:
        data, response_meta = fetcher(url)
    except HTTPError as exc:
        record = metadata_only_record(source, timestamp, f"Harvest failed with HTTP {exc.code}; retry or review manually.")
        record["http_status"] = exc.code
        record["retrieval_mode"] = "failed"
        return record
    except (URLError, TimeoutError, OSError) as exc:
        record = metadata_only_record(source, timestamp, f"Harvest failed: {exc}; retry or review manually.")
        record["retrieval_mode"] = "failed"
        return record
    source_dir.mkdir(parents=True, exist_ok=True)
    filename = safe_source_filename(source["id"], response_meta.get("canonical_url") or url, response_meta.get("content_type"))
    output_path = source_dir / filename
    output_path.write_bytes(data)
    parse_result = {"parse_status": "not_attempted", "rdf_format": None, "triple_count": 0}
    if classify_expected_format(source["expected_format"]) == "rdf_candidate":
        parse_result = parse_rdf_file(output_path, response_meta.get("content_type"))
    return {
        "id": source["id"],
        "name": source["name"],
        "family": source["family"],
        "source_url": source["source_url"],
        "artifact_url": url,
        "licence_disposition": source["licence_disposition"],
        "retrieval_timestamp": timestamp,
        "retrieval_mode": "downloaded",
        "http_status": response_meta.get("http_status"),
        "content_type": response_meta.get("content_type"),
        "canonical_url": response_meta.get("canonical_url") or url,
        "checksum_sha256": checksum_bytes(data),
        "byte_size": len(data),
        "local_path": output_path.resolve().relative_to(ROOT).as_posix(),
        "format_classification": classify_expected_format(source["expected_format"]),
        "manual_review_note": "Downloaded because licence_disposition is redistributable_artifact.",
        **parse_result,
    }


def validate_provenance(packet: dict, inventory: dict) -> dict:
    records = packet.get("sources")
    if packet.get("schema") != "uogto.ontology-comparison.source-provenance.v1":
        raise AssertionError("Unexpected provenance schema")
    if not isinstance(records, list):
        raise AssertionError("Provenance packet must contain a sources list")
    expected_ids = {source["id"] for source in inventory["sources"]}
    seen_ids = {record.get("id") for record in records}
    if seen_ids != expected_ids:
        raise AssertionError("Provenance records must cover every inventory source exactly once")
    downloaded = 0
    metadata_only = 0
    for record in records:
        for field in ["id", "retrieval_timestamp", "retrieval_mode", "canonical_url", "format_classification", "parse_status", "manual_review_note"]:
            if field not in record or record[field] in {"", None}:
                raise AssertionError(f"{record.get('id')} missing provenance field {field}")
        if record["retrieval_mode"] == "downloaded":
            downloaded += 1
            for field in ["http_status", "content_type", "checksum_sha256", "byte_size", "local_path"]:
                if field not in record or record[field] in {"", None}:
                    raise AssertionError(f"{record['id']} downloaded record missing {field}")
        elif record["retrieval_mode"] == "metadata_only":
            metadata_only += 1
        elif record["retrieval_mode"] != "failed":
            raise AssertionError(f"{record['id']} has invalid retrieval_mode")
    return {"record_count": len(records), "downloaded": downloaded, "metadata_only": metadata_only}


def harvest_inventory(inventory: dict, source_dir: Path = DEFAULT_SOURCE_DIR, timestamp: str | None = None) -> dict:
    timestamp = timestamp or utc_now()
    records = [harvest_source(source, source_dir, timestamp) for source in inventory["sources"]]
    return {
        "schema": "uogto.ontology-comparison.source-provenance.v1",
        "created": timestamp,
        "description": "Harvest/provenance manifest for comparative ontology mapping sources.",
        "sources": sorted(records, key=lambda item: item["id"]),
    }


def write_json(path: Path, packet: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Harvest redistributable ontology comparison sources and record provenance.")
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--output", type=Path, default=DEFAULT_PROVENANCE)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    inventory = build_ontology_comparison_inventory.load_inventory(args.inventory)
    build_ontology_comparison_inventory.validate_inventory(inventory)
    if args.check_only:
        if not args.output.exists():
            raise HarvestError(f"Missing provenance output: {args.output}")
        packet = json.loads(args.output.read_text(encoding="utf-8"))
    else:
        packet = harvest_inventory(inventory, args.source_dir)
        write_json(args.output, packet)
        build_ontology_comparison_inventory.write_markdown(
            build_ontology_comparison_inventory.DEFAULT_MARKDOWN,
            build_ontology_comparison_inventory.render_markdown(
                inventory,
                build_ontology_comparison_inventory.validate_inventory(inventory),
            ),
        )
    summary = validate_provenance(packet, inventory)
    print(
        "Ontology comparison provenance valid: "
        f"{summary['record_count']} records, {summary['downloaded']} downloaded, "
        f"{summary['metadata_only']} metadata-only."
    )


if __name__ == "__main__":
    try:
        main()
    except HarvestError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc
