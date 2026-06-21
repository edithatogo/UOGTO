import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.maintenance import (
    check_doi_status,
    check_publishing_metadata,
    check_registry_links,
    package_release_assets,
)


EXPECTED_RELEASE_TAG = "v1.0.0"
EXPECTED_VERSION = "1.0.0"
EXPECTED_PAGES_URL = "https://edithatogo.github.io/UOGTO/"
EXPECTED_RELEASE_URL = "https://github.com/edithatogo/UOGTO/releases/tag/v1.0.0"
EXPECTED_RELEASE_ASSET_BASE = "https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/"
EXPECTED_RELEASE_ASSETS = set(package_release_assets.REQUIRED_RELEASE_ASSETS) | {
    "release-assets-manifest.json",
    "SHA256SUMS",
    "registry-handoff.json",
    "w3id-redirect-handoff.json",
}
PENDING_EXTERNAL_MARKERS = [
    "TBD after Zenodo archiving",
    "TBD after the v1.0.0 GitHub release is archived by Zenodo",
    "Not yet submitted",
]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def load_release_manifest() -> dict:
    manifest_path = ROOT / "dist" / "release-assets-manifest.json"
    if not manifest_path.exists():
        raise AssertionError("Missing dist/release-assets-manifest.json; run make release-assets first")
    with manifest_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def check_release_manifest() -> None:
    manifest = load_release_manifest()
    if manifest.get("version") != EXPECTED_VERSION:
        raise AssertionError("Release asset manifest version must be 1.0.0")

    manifest_assets = {asset.get("name") for asset in manifest.get("assets", [])}
    missing_manifest_assets = sorted(set(package_release_assets.REQUIRED_RELEASE_ASSETS) - manifest_assets)
    if missing_manifest_assets:
        raise AssertionError(
            "Release asset manifest missing assets: " + ", ".join(missing_manifest_assets)
        )

    missing_files = [
        name for name in EXPECTED_RELEASE_ASSETS if not (ROOT / "dist" / name).exists()
    ]
    if missing_files:
        raise AssertionError("Missing generated release files: " + ", ".join(sorted(missing_files)))

    checksums = read_text("dist/SHA256SUMS")
    for name in package_release_assets.REQUIRED_RELEASE_ASSETS:
        if name not in checksums:
            raise AssertionError(f"dist/SHA256SUMS missing checksum entry for {name}")

    check_registry_handoff_packet(ROOT / "dist" / "registry-handoff.json")
    check_w3id_handoff_packet(ROOT / "dist" / "w3id-redirect-handoff.json")


def check_registry_handoff_packet(path: Path) -> None:
    if not path.exists():
        raise AssertionError("Missing dist/registry-handoff.json; run make registry-packet first")
    with path.open("r", encoding="utf-8") as handle:
        packet = json.load(handle)
    if packet.get("schema") != "uogto.registry-handoff.v1":
        raise AssertionError("Registry handoff packet has an unexpected schema")


def check_w3id_handoff_packet(path: Path) -> None:
    if not path.exists():
        raise AssertionError("Missing dist/w3id-redirect-handoff.json; run make w3id-packet first")
    with path.open("r", encoding="utf-8") as handle:
        packet = json.load(handle)
    if packet.get("schema") != "uogto.w3id-redirect-handoff.v1":
        raise AssertionError("w3id redirect handoff packet has an unexpected schema")


def check_release_workflow() -> None:
    workflow = read_text(".github/workflows/release-assets.yml")
    required_fragments = [
        "types: [published]",
        "workflow_dispatch",
        "make validate",
        "make test",
        "audit_semantics.py",
        "make publishing-metadata",
        "make registry-links",
        "make release-assets",
        "make registry-packet",
        "make w3id-packet",
        "gh release upload",
        "dist/release-assets-manifest.json",
        "dist/SHA256SUMS",
        "dist/registry-handoff.json",
        "dist/w3id-redirect-handoff.json",
        "check_release_readiness.py",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in workflow]
    if missing:
        raise AssertionError("Release asset workflow missing fragments: " + ", ".join(missing))


def check_release_notes() -> None:
    release_notes = read_text("docs/releases/v1.0.md")
    required_fragments = [
        EXPECTED_RELEASE_TAG,
        EXPECTED_PAGES_URL,
        "make validate",
        "make test",
        "python scripts/maintenance/audit_semantics.py",
        "python scripts/maintenance/check_publishing_metadata.py",
        "python scripts/maintenance/check_registry_links.py",
        "python scripts/maintenance/build_registry_handoff.py",
        "python scripts/maintenance/check_doi_status.py",
        "python scripts/maintenance/record_zenodo_doi.py",
        "python scripts/maintenance/package_release_assets.py",
        "make release-preflight",
        "Zenodo DOI: `TBD after the v1.0.0 GitHub release is archived by Zenodo`",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in release_notes]
    if missing:
        raise AssertionError("Release notes missing fragments: " + ", ".join(missing))


def check_registry_packets(*, require_published: bool = False) -> None:
    registry_text = check_registry_links.read_registry_text()
    check_registry_links.check_required_urls(registry_text)

    for relative_path in [
        "docs/registry/lov-submission.md",
        "docs/registry/ols-indexing.md",
    ]:
        text = read_text(relative_path)
        for fragment in [
            EXPECTED_PAGES_URL,
            EXPECTED_RELEASE_URL,
            EXPECTED_RELEASE_ASSET_BASE + "uogto.ttl",
            EXPECTED_RELEASE_ASSET_BASE + "uogto-shapes.ttl",
            EXPECTED_RELEASE_ASSET_BASE + "registry-handoff.json",
            "DOI: `TBD after Zenodo archiving`",
        ]:
            if fragment not in text:
                raise AssertionError(f"{relative_path} missing fragment: {fragment}")

    if require_published:
        pending = [marker for marker in PENDING_EXTERNAL_MARKERS if marker in registry_text]
        if pending:
            raise AssertionError(
                "Published-release readiness cannot contain pending markers: "
                + ", ".join(sorted(set(pending)))
            )


def check_local_release_readiness(*, require_published: bool = False) -> None:
    check_publishing_metadata.check_required_files()
    check_publishing_metadata.check_citation()
    check_publishing_metadata.check_zenodo()
    check_publishing_metadata.check_workflow()
    check_publishing_metadata.check_registry_annotations()
    check_publishing_metadata.check_registry_docs()
    check_doi_status.check_local_doi_state(require_doi=require_published)
    check_release_manifest()
    check_release_workflow()
    check_release_notes()
    check_registry_packets(require_published=require_published)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate local UOGTO v1.0 release readiness.")
    parser.add_argument(
        "--require-published",
        action="store_true",
        help="Fail if DOI, LOV, or OLS placeholders remain after publication.",
    )
    args = parser.parse_args()
    check_local_release_readiness(require_published=args.require_published)
    if args.require_published:
        print("Published-release readiness checks passed.")
    else:
        print("Local release readiness checks passed; DOI, LOV, and OLS remain external gates.")


if __name__ == "__main__":
    main()
