import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOI_PATTERN = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$", re.IGNORECASE)
DOI_DOCS = [
    ROOT / "docs/releases/v1.0.md",
    ROOT / "docs/registry/metadata-checklist.md",
    ROOT / "docs/registry/lov-submission.md",
    ROOT / "docs/registry/ols-indexing.md",
]
PLACEHOLDERS = [
    "`TBD after v1.0.0 release archiving`",
    "`TBD after Zenodo archiving`",
    "`TBD after the v1.0.0 GitHub release is archived by Zenodo`",
]
CHECKLIST_REPLACEMENTS = {
    "- [ ] Zenodo DOI is minted and recorded.": "- [x] Zenodo DOI is minted and recorded.",
    "- [ ] Confirm the Zenodo DOI resolves.": "- [x] Confirm the Zenodo DOI resolves.",
    "- [ ] WIDOCO documentation and DOI links are live.": "- [x] WIDOCO documentation and DOI links are live.",
    "- [ ] Zenodo DOI is recorded after release archiving.": "- [x] Zenodo DOI is recorded after release archiving.",
}


def normalize_doi(value: str) -> str:
    doi = value.strip().removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    doi = doi.rstrip(".,;:")
    if not DOI_PATTERN.match(doi):
        raise ValueError(f"Invalid DOI: {value}")
    return doi


def doi_url(doi: str) -> str:
    return f"https://doi.org/{doi}"


def update_markdown_text(text: str, doi: str) -> str:
    replacement = f"<{doi_url(doi)}>"
    updated = text
    for placeholder in PLACEHOLDERS:
        updated = updated.replace(placeholder, replacement)
    for old, new in CHECKLIST_REPLACEMENTS.items():
        updated = updated.replace(old, new)
    return updated


def update_citation_text(text: str, doi: str) -> str:
    lines = text.splitlines()
    if any(line.startswith("doi:") for line in lines):
        return "\n".join(
            f"doi: {doi}" if line.startswith("doi:") else line
            for line in lines
        ) + "\n"

    output = []
    inserted = False
    for line in lines:
        output.append(line)
        if not inserted and line.startswith("title:"):
            output.append(f"doi: {doi}")
            inserted = True
    if not inserted:
        output.append(f"doi: {doi}")
    return "\n".join(output) + "\n"


def update_zenodo_metadata(metadata: dict, doi: str) -> dict:
    updated = dict(metadata)
    related = [dict(item) for item in updated.get("related_identifiers", [])]
    if not any(item.get("scheme") == "doi" and item.get("identifier") == doi for item in related):
        related.append(
            {
                "identifier": doi,
                "relation": "isIdenticalTo",
                "resource_type": "dataset",
                "scheme": "doi",
            }
        )
    updated["related_identifiers"] = related
    return updated


def write_if_changed(path: Path, text: str, *, dry_run: bool) -> bool:
    existing = path.read_text(encoding="utf-8")
    if existing == text:
        return False
    if not dry_run:
        path.write_text(text, encoding="utf-8")
    return True


def record_doi(doi_value: str, *, dry_run: bool = False) -> list[Path]:
    doi = normalize_doi(doi_value)
    changed: list[Path] = []

    for path in DOI_DOCS:
        updated = update_markdown_text(path.read_text(encoding="utf-8"), doi)
        if write_if_changed(path, updated, dry_run=dry_run):
            changed.append(path)

    citation_path = ROOT / "CITATION.cff"
    citation = update_citation_text(citation_path.read_text(encoding="utf-8"), doi)
    if write_if_changed(citation_path, citation, dry_run=dry_run):
        changed.append(citation_path)

    zenodo_path = ROOT / ".zenodo.json"
    with zenodo_path.open("r", encoding="utf-8") as handle:
        zenodo = json.load(handle)
    updated_zenodo = update_zenodo_metadata(zenodo, doi)
    zenodo_text = json.dumps(updated_zenodo, indent=2, ensure_ascii=False) + "\n"
    if write_if_changed(zenodo_path, zenodo_text, dry_run=dry_run):
        changed.append(zenodo_path)

    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description="Record a minted Zenodo DOI across UOGTO release metadata.")
    parser.add_argument("doi", help="Minted Zenodo DOI, for example 10.5281/zenodo.1234567")
    parser.add_argument("--dry-run", action="store_true", help="Report files that would change without writing.")
    args = parser.parse_args()

    changed = record_doi(args.doi, dry_run=args.dry_run)
    prefix = "Would update" if args.dry_run else "Updated"
    if changed:
        for path in changed:
            print(f"{prefix}: {path.relative_to(ROOT)}")
    else:
        print("DOI metadata already up to date.")


if __name__ == "__main__":
    main()
