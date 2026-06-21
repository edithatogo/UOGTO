import argparse
import json
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
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


@dataclass(frozen=True)
class UrlObservation:
    url: str
    status: int
    final_url: str
    ok: bool


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


def fetch_url(url: str, *, timeout: int = 20) -> UrlObservation:
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "UOGTO-publication-status"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return UrlObservation(url=url, status=response.status, final_url=response.url, ok=response.status < 400)
    except urllib.error.HTTPError as exc:
        return UrlObservation(url=url, status=exc.code, final_url=exc.geturl(), ok=False)
    except urllib.error.URLError:
        return UrlObservation(url=url, status=0, final_url=url, ok=False)


def live_observations(*, timeout: int = 20) -> dict:
    assets = {name: asdict(fetch_url(url, timeout=timeout)) for name, url in release_asset_urls().items()}
    pages = asdict(fetch_url(PAGES_URL, timeout=timeout))
    doi_live = check_doi_status.check_live_zenodo(require_doi=False, timeout=timeout)
    return {
        "documentation": pages,
        "release_assets": assets,
        "zenodo_dois": doi_live,
    }


def build_publication_status(*, include_live: bool = False, require_live: bool = False, timeout: int = 20) -> dict:
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

    packet = {
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
    if include_live or require_live:
        observations = live_observations(timeout=timeout)
        packet["live"] = observations
        failed_urls = []
        if not observations["documentation"]["ok"]:
            failed_urls.append(observations["documentation"]["url"])
        failed_urls.extend(
            item["url"] for item in observations["release_assets"].values() if not item["ok"]
        )
        if failed_urls:
            packet["status"] = "live_publication_check_failed"
            for url in failed_urls:
                packet["blockers"].append({"source": "live", "message": f"Live URL check failed for {url}"})
        if require_live and failed_urls:
            raise AssertionError("Live publication status check failed for: " + ", ".join(failed_urls))
    return packet


def write_status(output_path: Path, packet: dict) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def display_path(output_path: Path) -> str:
    resolved = output_path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the UOGTO publication status packet.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="JSON output path. Defaults to dist/publication-status.json.",
    )
    parser.add_argument("--live", action="store_true", help="Record live URL and Zenodo DOI observations.")
    parser.add_argument("--require-live", action="store_true", help="Fail if Pages or release asset URLs are not live.")
    parser.add_argument("--timeout", type=int, default=20, help="Per-request timeout in seconds.")
    args = parser.parse_args()

    packet = build_publication_status(
        include_live=args.live,
        require_live=args.require_live,
        timeout=args.timeout,
    )
    write_status(args.output, packet)
    print(f"Wrote {display_path(args.output)} with status {packet['status']}.")


if __name__ == "__main__":
    main()
