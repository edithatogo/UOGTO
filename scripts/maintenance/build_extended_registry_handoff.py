import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "dist" / "extended-registry-handoff.json"
DOC_PATH = ROOT / "docs" / "registry" / "extended-discoverability-submissions.md"

CORE_NAMESPACE = "https://w3id.org/uogto/core#"
EXTENSION_NAMESPACE = "https://w3id.org/uogto/extensions#"
DOI_URL = "https://doi.org/10.5281/zenodo.20796937"
REPOSITORY_URL = "https://github.com/edithatogo/UOGTO"
DOCUMENTATION_URL = "https://edithatogo.github.io/UOGTO/"
RELEASE_URL = "https://github.com/edithatogo/UOGTO/releases/tag/v1.0.0"
RDF_ASSET_URL = "https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/uogto.ttl"

REQUIRED_DOCUMENT_FRAGMENTS = [
    "Universal Open Game Theory Ontology (UOGTO)",
    "Preferred core prefix: `uogto`",
    "Preferred extension prefix: `uogtox`",
    CORE_NAMESPACE,
    EXTENSION_NAMESPACE,
    DOI_URL,
    REPOSITORY_URL,
    DOCUMENTATION_URL,
    RELEASE_URL,
    RDF_ASSET_URL,
    "LOV submission: <https://github.com/pyvandenbussche/lov/issues/83>",
    "OLS request: <https://github.com/EBISPOT/ols4/issues/1305>",
    "w3id redirect PR: <https://github.com/perma-id/w3id.org/pull/6238>",
]


TARGETS = {
    "fairsharing": {
        "status": "prepared_account_required",
        "route": "https://fairsharing.org/",
        "blocker": "Authenticated FAIRsharing account and JavaScript submission workflow required.",
    },
    "prefix_cc": {
        "status": "partial",
        "route": "http://prefix.cc/",
        "submitted": {
            "uogto": {
                "uri": CORE_NAMESPACE,
                "evidence": "http://prefix.cc/uogto.file.txt",
            }
        },
        "pending": {
            "uogtox": {
                "uri": EXTENSION_NAMESPACE,
                "blocker": "prefix.cc one-per-day contribution limit; retry after 2026-06-24.",
            }
        },
    },
    "wikidata": {
        "status": "prepared_account_required",
        "route": "https://www.wikidata.org/",
        "blocker": "Authenticated Wikidata account and edit token required; searches found no existing UOGTO item.",
    },
    "ontobee": {
        "status": "deferred_pending_w3id",
        "route": "https://ontobee.org/",
        "blocker": "Wait for w3id redirects before requesting linked-data term indexing.",
    },
    "bioportal": {
        "status": "not_submitted_conditional",
        "route": "https://bioportal.bioontology.org/",
        "decision": "Do not submit without a defensible biomedical, clinical, public-health, behavioural-science, or health-simulation positioning note.",
    },
    "bioregistry": {
        "status": "submitted",
        "route": "https://bioregistry.io/",
        "issue": "https://github.com/biopragmatics/bioregistry/issues/1999",
    },
    "obo_foundry": {
        "status": "not_prioritized",
        "route": "https://obofoundry.org/",
        "decision": "Do not pursue unless UOGTO is repositioned for biological or biomedical ontology governance.",
    },
}


def read_doc() -> str:
    if not DOC_PATH.exists():
        raise AssertionError("Missing docs/registry/extended-discoverability-submissions.md")
    return DOC_PATH.read_text(encoding="utf-8")


def build_extended_registry_handoff() -> dict:
    doc_text = read_doc()
    missing = [fragment for fragment in REQUIRED_DOCUMENT_FRAGMENTS if fragment not in doc_text]
    if missing:
        raise AssertionError(
            "Extended registry doc missing canonical metadata fragments: " + ", ".join(missing)
        )

    blockers = []
    for name, target in TARGETS.items():
        if target["route"] not in doc_text:
            raise AssertionError(f"Extended registry doc missing route for {name}: {target['route']}")
        status = target["status"]
        if status in {"prepared_account_required", "partial", "deferred_pending_w3id"}:
            blocker = target.get("blocker") or f"{name} remains pending."
            blockers.append({"target": name, "message": blocker})

    return {
        "schema": "uogto.extended-registry-handoff.v1",
        "status": "external_actions_pending" if blockers else "complete",
        "blockers": blockers,
        "ontology": {
            "title": "Universal Open Game Theory Ontology (UOGTO)",
            "preferred_prefix": "uogto",
            "extension_prefix": "uogtox",
            "core_namespace": CORE_NAMESPACE,
            "extension_namespace": EXTENSION_NAMESPACE,
            "doi": DOI_URL,
            "repository": REPOSITORY_URL,
            "documentation": DOCUMENTATION_URL,
            "release": RELEASE_URL,
            "canonical_rdf": RDF_ASSET_URL,
        },
        "targets": TARGETS,
        "source_document": "docs/registry/extended-discoverability-submissions.md",
    }


def write_handoff(output_path: Path, packet: dict) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the UOGTO extended registry handoff packet.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="JSON output path. Defaults to dist/extended-registry-handoff.json.",
    )
    args = parser.parse_args()

    packet = build_extended_registry_handoff()
    write_handoff(args.output, packet)
    print(f"Wrote {args.output.relative_to(ROOT)} with status {packet['status']}.")


if __name__ == "__main__":
    main()
