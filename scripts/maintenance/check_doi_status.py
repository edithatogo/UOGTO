import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_TITLE = "Universal Open Game Theory Ontology"
EXPECTED_REPOSITORY = "https://github.com/edithatogo/UOGTO"
ZENODO_RECORDS_API = "https://zenodo.org/api/records"
DOI_PLACEHOLDERS = [
    "TBD after v1.0.0 release archiving",
    "TBD after Zenodo archiving",
    "TBD after the v1.0.0 GitHub release is archived by Zenodo",
]
DOI_DEPENDENT_DOCS = [
    ROOT / "docs/registry/metadata-checklist.md",
    ROOT / "docs/registry/lov-submission.md",
    ROOT / "docs/registry/ols-indexing.md",
    ROOT / "docs/releases/v1.0.md",
]


def read_doi_docs() -> str:
    missing = [str(path.relative_to(ROOT)) for path in DOI_DEPENDENT_DOCS if not path.exists()]
    if missing:
        raise AssertionError("Missing DOI-dependent docs: " + ", ".join(missing))
    return "\n".join(path.read_text(encoding="utf-8") for path in DOI_DEPENDENT_DOCS)


def has_doi_placeholder(text: str) -> bool:
    return any(placeholder in text for placeholder in DOI_PLACEHOLDERS)


def extract_dois_from_docs(text: str) -> list[str]:
    dois = []
    for token in text.replace("`", " ").replace("<", " ").replace(">", " ").split():
        normalized = token.rstrip(".,;:")
        if normalized.startswith("10."):
            dois.append(normalized)
        elif normalized.startswith("https://doi.org/10."):
            dois.append(normalized.removeprefix("https://doi.org/"))
    return sorted(set(dois))


def build_zenodo_query_url(query: str = EXPECTED_TITLE) -> str:
    params = urllib.parse.urlencode({"q": query, "size": "10"})
    return f"{ZENODO_RECORDS_API}?{params}"


def fetch_json(url: str, timeout: int = 20) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "UOGTO-doi-check"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def record_matches_uogto(record: dict) -> bool:
    metadata = record.get("metadata", {})
    title = metadata.get("title", "")
    related = metadata.get("related_identifiers", []) or []
    repository_match = any(item.get("identifier") == EXPECTED_REPOSITORY for item in related)
    return EXPECTED_TITLE.lower() in title.lower() or repository_match


def extract_record_doi(record: dict) -> str | None:
    metadata = record.get("metadata", {})
    doi = metadata.get("doi") or record.get("doi")
    if doi:
        return str(doi)
    links = record.get("links", {})
    doi_link = links.get("doi")
    if isinstance(doi_link, str) and doi_link.startswith("https://doi.org/"):
        return doi_link.removeprefix("https://doi.org/")
    return None


def find_uogto_zenodo_dois(payload: dict) -> list[str]:
    hits = payload.get("hits", {}).get("hits", [])
    dois = []
    for record in hits:
        if record_matches_uogto(record):
            doi = extract_record_doi(record)
            if doi:
                dois.append(doi)
    return sorted(set(dois))


def check_local_doi_state(*, require_doi: bool = False) -> list[str]:
    text = read_doi_docs()
    dois = extract_dois_from_docs(text)
    if require_doi:
        if has_doi_placeholder(text):
            raise AssertionError("DOI placeholders remain in DOI-dependent docs")
        if not dois:
            raise AssertionError("No DOI is recorded in DOI-dependent docs")
    elif not has_doi_placeholder(text):
        raise AssertionError("DOI placeholders are absent; run with --require-doi after recording the DOI")
    return dois


def check_live_zenodo(*, require_doi: bool = False, timeout: int = 20) -> list[str]:
    payload = fetch_json(build_zenodo_query_url(), timeout=timeout)
    dois = find_uogto_zenodo_dois(payload)
    if require_doi and not dois:
        raise AssertionError("No matching UOGTO DOI found in public Zenodo records")
    return dois


def main() -> None:
    parser = argparse.ArgumentParser(description="Check UOGTO Zenodo DOI publication state.")
    parser.add_argument("--live", action="store_true", help="Query public Zenodo records.")
    parser.add_argument("--require-doi", action="store_true", help="Fail unless DOI docs and live lookup show a DOI.")
    parser.add_argument("--timeout", type=int, default=20, help="Per-request timeout in seconds.")
    args = parser.parse_args()

    local_dois = check_local_doi_state(require_doi=args.require_doi)
    live_dois: list[str] = []
    if args.live:
        live_dois = check_live_zenodo(require_doi=args.require_doi, timeout=args.timeout)

    if local_dois:
        print("Recorded DOI(s): " + ", ".join(local_dois))
    elif live_dois:
        print("Public Zenodo DOI(s): " + ", ".join(live_dois))
    else:
        print("Zenodo DOI is not recorded locally and has not been required by this gate.")


if __name__ == "__main__":
    main()
