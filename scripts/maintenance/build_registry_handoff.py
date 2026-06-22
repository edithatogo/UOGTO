import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.maintenance import check_doi_status, check_registry_links

DEFAULT_OUTPUT = ROOT / "dist" / "registry-handoff.json"
VERSION = "1.0.0"
RELEASE_TAG = "v1.0.0"
ONTOLOGY_TITLE = "Universal Open Game Theory Ontology"
PREFERRED_PREFIX = "uogto"
CORE_NAMESPACE = "https://w3id.org/uogto/core#"
EXTENSION_NAMESPACE = "https://w3id.org/uogto/extensions#"
HOMEPAGE = "https://github.com/edithatogo/UOGTO"
DOCUMENTATION_URL = "https://edithatogo.github.io/UOGTO/"
RELEASE_URL = "https://github.com/edithatogo/UOGTO/releases/tag/v1.0.0"
RELEASE_ASSET_BASE = "https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/"
LICENSE_URL = "https://creativecommons.org/licenses/by/4.0/"
LOV_SUBMISSION_URL = "https://github.com/pyvandenbussche/lov/issues/83"
OLS_REQUEST_URL = "https://github.com/EBISPOT/ols4/issues/1305"
SUBMISSION_DATE = "2026-06-22"


def doi_state() -> tuple[list[str], bool]:
    text = check_doi_status.read_doi_docs()
    return check_doi_status.extract_dois_from_docs(text), check_doi_status.has_doi_placeholder(text)


def registry_urls() -> list[str]:
    text = check_registry_links.read_registry_text()
    return sorted(check_registry_links.check_required_urls(text))


def build_registry_handoff(*, require_ready: bool = False) -> dict:
    dois, has_placeholder = doi_state()
    blockers = []
    if has_placeholder or not dois:
        blockers.append("Zenodo DOI is not recorded in DOI-dependent registry documents.")

    if require_ready and blockers:
        raise AssertionError("Registry handoff is not ready: " + "; ".join(blockers))

    doi = dois[0] if dois else None
    status = "submitted_to_registries" if not blockers else "pending_external_doi"
    doi_value = f"https://doi.org/{doi}" if doi else None

    return {
        "schema": "uogto.registry-handoff.v1",
        "status": status,
        "blockers": blockers,
        "ontology": {
            "title": ONTOLOGY_TITLE,
            "version": VERSION,
            "release_tag": RELEASE_TAG,
            "preferred_prefix": PREFERRED_PREFIX,
            "core_namespace": CORE_NAMESPACE,
            "extension_namespace": EXTENSION_NAMESPACE,
            "homepage": HOMEPAGE,
            "documentation": DOCUMENTATION_URL,
            "release": RELEASE_URL,
            "doi": doi_value,
            "license": LICENSE_URL,
        },
        "artifacts": {
            "merged_ontology": RELEASE_ASSET_BASE + "uogto.ttl",
            "shacl_shapes": RELEASE_ASSET_BASE + "uogto-shapes.ttl",
            "checksums": RELEASE_ASSET_BASE + "SHA256SUMS",
            "manifest": RELEASE_ASSET_BASE + "release-assets-manifest.json",
            "registry_handoff": RELEASE_ASSET_BASE + "registry-handoff.json",
        },
        "lov": {
            "status": "submitted" if not blockers else "blocked_until_doi_recorded",
            "submission_document": "docs/registry/lov-submission.md",
            "submission_date": SUBMISSION_DATE if not blockers else None,
            "submission_url": LOV_SUBMISSION_URL if not blockers else None,
            "review_status": "awaiting_maintainer_review" if not blockers else "not_submitted",
        },
        "ols": {
            "status": "submitted" if not blockers else "blocked_until_doi_recorded",
            "submission_document": "docs/registry/ols-indexing.md",
            "requested_identifier": PREFERRED_PREFIX,
            "request_date": SUBMISSION_DATE if not blockers else None,
            "request_url": OLS_REQUEST_URL if not blockers else None,
            "review_status": "awaiting_maintainer_review" if not blockers else "not_submitted",
        },
        "required_urls": registry_urls(),
    }


def write_handoff(output_path: Path, packet: dict) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the UOGTO LOV/OLS registry handoff packet.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="JSON output path. Defaults to dist/registry-handoff.json.",
    )
    parser.add_argument(
        "--require-ready",
        action="store_true",
        help="Fail unless DOI-dependent registry metadata is ready for submission.",
    )
    args = parser.parse_args()

    packet = build_registry_handoff(require_ready=args.require_ready)
    write_handoff(args.output, packet)
    print(f"Wrote {args.output.relative_to(ROOT)} with status {packet['status']}.")


if __name__ == "__main__":
    main()
