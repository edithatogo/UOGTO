import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.maintenance import (
    build_registry_handoff,
    build_w3id_redirect_handoff,
    build_zenodo_handoff,
    check_doi_status,
)


DEFAULT_OUTPUT = ROOT / "dist" / "publication-status.json"
RELEASE_TAG = "v1.0.0"
PAGES_URL = "https://edithatogo.github.io/UOGTO/"
RELEASE_URL = "https://github.com/edithatogo/UOGTO/releases/tag/v1.0.0"
RELEASE_ASSET_BASE = "https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/"
PUBLICATION_ASSETS = [
    "release-assets-manifest.json",
    "SHA256SUMS",
    "registry-handoff.json",
    "zenodo-handoff.json",
    "w3id-redirect-handoff.json",
    "publication-status.json",
]


def doi_summary() -> dict:
    docs_text = check_doi_status.read_doi_docs()
    local_dois = check_doi_status.extract_dois_from_docs(docs_text)
    placeholders = check_doi_status.has_doi_placeholder(docs_text)
    return {
        "status": "recorded" if local_dois and not placeholders else "pending_external_zenodo_doi",
        "local_dois": local_dois,
        "placeholders_present": placeholders,
    }


def release_asset_urls() -> dict:
    return {asset: RELEASE_ASSET_BASE + asset for asset in PUBLICATION_ASSETS}


def build_publication_status() -> dict:
    registry = build_registry_handoff.build_registry_handoff()
    zenodo = build_zenodo_handoff.build_zenodo_handoff()
    w3id = build_w3id_redirect_handoff.build_w3id_handoff()
    doi = doi_summary()

    blockers = []
    for source, packet in [
        ("registry", registry),
        ("zenodo", zenodo),
        ("w3id", w3id),
    ]:
        for blocker in packet.get("blockers", []):
            blockers.append({"source": source, "message": blocker})

    if doi["status"] != "recorded":
        blockers.append(
            {
                "source": "doi",
                "message": "Zenodo DOI is not recorded locally; DOI-dependent LOV and OLS submissions remain blocked.",
            }
        )

    return {
        "schema": "uogto.publication-status.v1",
        "status": "published" if not blockers else "pending_external_publication_steps",
        "release_tag": RELEASE_TAG,
        "release_url": RELEASE_URL,
        "documentation_url": PAGES_URL,
        "assets": release_asset_urls(),
        "checks": {
            "documentation": {
                "status": "published",
                "url": PAGES_URL,
            },
            "release_assets": {
                "status": "published",
                "release_url": RELEASE_URL,
            },
            "doi": doi,
            "registry": {
                "status": registry["status"],
                "packet": "dist/registry-handoff.json",
            },
            "zenodo": {
                "status": zenodo["status"],
                "packet": "dist/zenodo-handoff.json",
            },
            "w3id": {
                "status": w3id["status"],
                "packet": "dist/w3id-redirect-handoff.json",
                "pull_request_url": w3id["w3id_pull_request_url"],
            },
            "lov": {
                "status": "blocked_until_doi_recorded" if doi["status"] != "recorded" else "ready_for_submission",
                "document": "docs/registry/lov-submission.md",
            },
            "ols": {
                "status": "blocked_until_doi_recorded" if doi["status"] != "recorded" else "ready_for_submission",
                "document": "docs/registry/ols-indexing.md",
            },
        },
        "blockers": blockers,
    }


def write_status(output_path: Path, packet: dict) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the UOGTO publication status packet.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="JSON output path. Defaults to dist/publication-status.json.",
    )
    args = parser.parse_args()

    packet = build_publication_status()
    write_status(args.output, packet)
    print(f"Wrote {args.output.relative_to(ROOT)} with status {packet['status']}.")


if __name__ == "__main__":
    main()
