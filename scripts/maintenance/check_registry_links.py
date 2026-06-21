import argparse
import re
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_DOCS = [
    ROOT / "docs/registry/metadata-checklist.md",
    ROOT / "docs/registry/lov-submission.md",
    ROOT / "docs/registry/ols-indexing.md",
    ROOT / "docs/releases/v1.0.md",
]

REQUIRED_STABLE_URLS = {
    "https://github.com/edithatogo/UOGTO",
    "https://creativecommons.org/licenses/by/4.0/",
}

REQUIRED_PUBLICATION_URLS = {
    "https://edithatogo.github.io/UOGTO/",
    "https://github.com/edithatogo/UOGTO/releases/tag/v1.0.0",
    "https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/uogto.ttl",
    "https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/uogto-shapes.ttl",
    "https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/SHA256SUMS",
}

PENDING_MARKERS = [
    "TBD after v1.0.0 release",
    "TBD after Zenodo archiving",
    "TBD after the v1.0.0 GitHub release is archived by Zenodo",
    "Not yet submitted",
]

URL_PATTERN = re.compile(r"https?://[^\s>)`]+")


def read_registry_text() -> str:
    missing = [str(path.relative_to(ROOT)) for path in REGISTRY_DOCS if not path.exists()]
    if missing:
        raise AssertionError(f"Missing registry documentation files: {', '.join(missing)}")
    return "\n".join(path.read_text(encoding="utf-8") for path in REGISTRY_DOCS)


def extract_urls(text: str) -> set[str]:
    return {match.group(0).rstrip(".,;:") for match in URL_PATTERN.finditer(text)}


def check_required_urls(text: str) -> set[str]:
    urls = extract_urls(text)
    required = REQUIRED_STABLE_URLS | REQUIRED_PUBLICATION_URLS
    missing = sorted(url for url in required if url not in urls)
    if missing:
        raise AssertionError(f"Registry docs missing required URLs: {', '.join(missing)}")
    return urls


def has_pending_publication_markers(text: str) -> bool:
    return any(marker in text for marker in PENDING_MARKERS)


def open_url(url: str, timeout: int = 10) -> int:
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "UOGTO-link-check"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status
    except urllib.error.HTTPError as error:
        if error.code == 405:
            request = urllib.request.Request(url, headers={"User-Agent": "UOGTO-link-check"})
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.status
        raise


def check_live_urls(
    urls: set[str],
    *,
    allow_unpublished: bool = False,
    timeout: int = 10,
) -> list[str]:
    failures = []
    for url in sorted(urls):
        if allow_unpublished and url in REQUIRED_PUBLICATION_URLS:
            continue
        try:
            status = open_url(url, timeout=timeout)
        except Exception as error:  # pragma: no cover - concrete exception varies by platform/network.
            failures.append(f"{url}: {error}")
            continue
        if status >= 400:
            failures.append(f"{url}: HTTP {status}")
    if failures:
        raise AssertionError("Registry live link checks failed: " + "; ".join(failures))
    return sorted(urls)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate UOGTO registry documentation links.")
    parser.add_argument("--live", action="store_true", help="Perform HTTP checks for registry URLs.")
    parser.add_argument(
        "--allow-unpublished",
        action="store_true",
        help="Skip live checks for URLs that are expected to exist only after v1.0 publication.",
    )
    parser.add_argument("--timeout", type=int, default=10, help="Per-URL timeout in seconds.")
    args = parser.parse_args()

    text = read_registry_text()
    urls = check_required_urls(text)
    if args.allow_unpublished and not has_pending_publication_markers(text):
        raise AssertionError("--allow-unpublished was used, but no pending publication markers remain")
    if args.live:
        check_live_urls(urls, allow_unpublished=args.allow_unpublished, timeout=args.timeout)
    print("Registry link checks passed.")


if __name__ == "__main__":
    main()
