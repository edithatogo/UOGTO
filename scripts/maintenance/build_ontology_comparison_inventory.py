import argparse
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "docs" / "ontology-comparison" / "source-inventory.json"
DEFAULT_MARKDOWN = ROOT / "docs" / "ontology-comparison" / "source-inventory.md"
DEFAULT_LOG = ROOT / "docs" / "ontology-comparison" / "inclusion-exclusion-log.jsonl"

REQUIRED_SCHEMA = "uogto.ontology-comparison.source-inventory.v1"
REQUIRED_FIELDS = {
    "id",
    "name",
    "family",
    "candidate_type",
    "source_url",
    "expected_format",
    "licence_disposition",
    "redistribution_risk",
    "discovery_route",
    "inclusion_rationale",
    "review_status",
    "priority",
}
LICENCE_DISPOSITIONS = {
    "redistributable_artifact",
    "metadata_only",
    "transformed_summary_only",
    "excluded",
    "needs_licence_review",
}
REVIEW_STATUSES = {"seeded", "included", "metadata_only", "excluded", "needs_review"}
PRIORITIES = {"high", "medium", "low"}
REDISTRIBUTION_RISKS = {"low", "medium", "high"}


def load_inventory(path: Path = DEFAULT_INPUT) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def assert_url(value: str, field: str, source_id: str) -> None:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise AssertionError(f"{source_id}.{field} must be an absolute HTTP(S) URL")


def validate_inventory(packet: dict) -> dict:
    if packet.get("schema") != REQUIRED_SCHEMA:
        raise AssertionError(f"Unexpected inventory schema: {packet.get('schema')}")
    sources = packet.get("sources")
    if not isinstance(sources, list) or not sources:
        raise AssertionError("Inventory must contain a non-empty sources list")

    seen_ids = set()
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            raise AssertionError(f"Source at index {index} must be an object")
        missing = sorted(REQUIRED_FIELDS - set(source))
        if missing:
            raise AssertionError(f"Source {source.get('id', index)} missing fields: {', '.join(missing)}")
        source_id = source["id"]
        if source_id in seen_ids:
            raise AssertionError(f"Duplicate source id: {source_id}")
        seen_ids.add(source_id)
        assert_url(source["source_url"], "source_url", source_id)
        if source.get("artifact_url") is not None:
            assert_url(source["artifact_url"], "artifact_url", source_id)
        if source["licence_disposition"] not in LICENCE_DISPOSITIONS:
            raise AssertionError(f"{source_id} has invalid licence_disposition")
        if source["review_status"] not in REVIEW_STATUSES:
            raise AssertionError(f"{source_id} has invalid review_status")
        if source["priority"] not in PRIORITIES:
            raise AssertionError(f"{source_id} has invalid priority")
        if source["redistribution_risk"] not in REDISTRIBUTION_RISKS:
            raise AssertionError(f"{source_id} has invalid redistribution_risk")
        if not source["inclusion_rationale"].strip():
            raise AssertionError(f"{source_id} must include an inclusion_rationale")

    by_family = Counter(source["family"] for source in sources)
    by_status = Counter(source["review_status"] for source in sources)
    by_licence = Counter(source["licence_disposition"] for source in sources)
    return {
        "source_count": len(sources),
        "family_count": len(by_family),
        "by_family": dict(sorted(by_family.items())),
        "by_review_status": dict(sorted(by_status.items())),
        "by_licence_disposition": dict(sorted(by_licence.items())),
    }


def render_markdown(packet: dict, summary: dict) -> str:
    sources = sorted(packet["sources"], key=lambda item: (item["family"], item["id"]))
    lines = [
        "# Comparative Ontology Source Inventory",
        "",
        "This file is generated from `source-inventory.json` by "
        "`scripts/maintenance/build_ontology_comparison_inventory.py`.",
        "",
        "## Summary",
        f"- Sources: `{summary['source_count']}`",
        f"- Families: `{summary['family_count']}`",
        "",
        "### By Review Status",
    ]
    for key, value in summary["by_review_status"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "### By Licence Disposition"])
    for key, value in summary["by_licence_disposition"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Sources", ""])
    for source in sources:
        artifact = source.get("artifact_url") or "not identified"
        lines.extend(
            [
                f"### {source['name']}",
                f"- ID: `{source['id']}`",
                f"- Family: `{source['family']}`",
                f"- Candidate type: `{source['candidate_type']}`",
                f"- Source URL: <{source['source_url']}>",
                f"- Artifact URL: {artifact if artifact == 'not identified' else f'<{artifact}>'}",
                f"- Expected format: `{source['expected_format']}`",
                f"- Licence disposition: `{source['licence_disposition']}`",
                f"- Redistribution risk: `{source['redistribution_risk']}`",
                f"- Review status: `{source['review_status']}`",
                f"- Priority: `{source['priority']}`",
                f"- Discovery route: {source['discovery_route']}",
                f"- Inclusion rationale: {source['inclusion_rationale']}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def validate_inclusion_log(path: Path = DEFAULT_LOG, source_ids: set[str] | None = None) -> int:
    if not path.exists():
        raise AssertionError("Missing docs/ontology-comparison/inclusion-exclusion-log.jsonl")
    count = 0
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                record = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise AssertionError(f"Inclusion log line {line_number} is not valid JSON") from exc
            for field in ["timestamp", "source_id", "decision", "rationale", "reviewer"]:
                if field not in record or not str(record[field]).strip():
                    raise AssertionError(f"Inclusion log line {line_number} missing {field}")
            if source_ids is not None and record["source_id"] not in source_ids:
                raise AssertionError(f"Inclusion log line {line_number} references unknown source_id")
            count += 1
    if count == 0:
        raise AssertionError("Inclusion log must contain at least one decision record")
    return count


def write_markdown(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and render ontology comparison source inventory.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    packet = load_inventory(args.input)
    summary = validate_inventory(packet)
    validate_inclusion_log(DEFAULT_LOG, {source["id"] for source in packet["sources"]})
    if not args.check_only:
        write_markdown(args.output, render_markdown(packet, summary))
    print(
        f"Ontology comparison inventory valid: {summary['source_count']} sources, "
        f"{summary['family_count']} families."
    )


if __name__ == "__main__":
    main()
