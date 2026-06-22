import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.maintenance import check_doi_status


DEFAULT_OUTPUT = ROOT / "dist" / "zenodo-handoff.json"
REPOSITORY_URL = "https://github.com/edithatogo/UOGTO"
RELEASE_URL = "https://github.com/edithatogo/UOGTO/releases/tag/v1.0.0"
RELEASE_ASSET_BASE = "https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/"


def build_zenodo_handoff() -> dict:
    docs_text = check_doi_status.read_doi_docs()
    local_dois = check_doi_status.extract_dois_from_docs(docs_text)
    pending = check_doi_status.has_doi_placeholder(docs_text)
    blockers = []
    if pending:
        blockers.append("Zenodo DOI is not recorded in DOI-dependent release and registry documents.")
    if not local_dois:
        blockers.append("No UOGTO Zenodo DOI has been detected or recorded locally.")

    return {
        "schema": "uogto.zenodo-handoff.v1",
        "status": "pending_external_zenodo_doi" if blockers else "doi_recorded",
        "blockers": blockers,
        "repository_url": REPOSITORY_URL,
        "release_url": RELEASE_URL,
        "release_tag": "v1.0.0",
        "release_assets": {
            "uogto.ttl": RELEASE_ASSET_BASE + "uogto.ttl",
            "uogto-shapes.ttl": RELEASE_ASSET_BASE + "uogto-shapes.ttl",
            "release-assets-manifest.json": RELEASE_ASSET_BASE + "release-assets-manifest.json",
            "SHA256SUMS": RELEASE_ASSET_BASE + "SHA256SUMS",
        },
        "metadata_files": [
            "CITATION.cff",
            ".zenodo.json",
            "docs/releases/v1.0.md",
            "docs/registry/metadata-checklist.md",
            "docs/registry/lov-submission.md",
            "docs/registry/ols-indexing.md",
        ],
        "account_side_cli": {
            "command": "python scripts/maintenance/check_zenodo_depositions.py --json",
            "token_env": "ZENODO_ACCESS_TOKEN",
            "strict_command": "python scripts/maintenance/check_zenodo_depositions.py --require-token --require-uogto",
        },
        "local_dois": local_dois,
        "verification_actions": [
            "Run python scripts/maintenance/check_doi_status.py --live --require-doi to verify the recorded DOI.",
            "Run python scripts/maintenance/check_zenodo_depositions.py --json with ZENODO_ACCESS_TOKEN for account-side deposition inspection.",
            "Run python scripts/maintenance/record_zenodo_doi.py <doi> when minting a future release DOI.",
        ],
    }


def write_handoff(output_path: Path, packet: dict) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the UOGTO Zenodo DOI handoff packet.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="JSON output path. Defaults to dist/zenodo-handoff.json.",
    )
    args = parser.parse_args()

    packet = build_zenodo_handoff()
    write_handoff(args.output, packet)
    print(f"Wrote {args.output.relative_to(ROOT)} with status {packet['status']}.")


if __name__ == "__main__":
    main()
