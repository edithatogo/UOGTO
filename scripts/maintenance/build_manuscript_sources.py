import argparse
import json
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[2]
PAPER_DIR = ROOT / "docs" / "paper"
SOURCERIGHT_DIR = ROOT / ".sourceright"
DEEP_RESEARCH_FILES = sorted((ROOT / "docs").glob("deep_research_part*.md"))
REVIEW_DATA_FILES = [
    ROOT / "data" / "processed" / "deduplicated_results.json",
    ROOT / "data" / "processed" / "screened_results.json",
    ROOT / "data" / "processed" / "snowballed_results.json",
]
MANUSCRIPT_REFERENCE_IDS = [
    "arxiv-2006-06580v3",
    "arxiv-api",
    "crossref",
    "open-spiel-2019",
    "openalex",
    "rapoport-chammah-1965",
    "w3c-json-ld11",
    "w3c-owl2-overview",
    "w3c-rdf11-concepts",
    "w3c-shacl",
    "w3c-sparql11-query",
]

MARKDOWN_REFERENCE_RE = re.compile(r'^\[(?P<num>\d+)\]:\s+(?P<url>\S+)\s+"(?P<title>[^"]+)"')

CURATED_REFERENCES = [
    {
        "id": "open-spiel-2019",
        "type": "article",
        "title": "OpenSpiel: A Framework for Reinforcement Learning in Games",
        "URL": "https://arxiv.org/abs/1908.09453",
        "issued": {"date-parts": [[2019]]},
        "author": [{"literal": "OpenSpiel Contributors"}],
        "source_note": "Reference implementation and game-learning toolkit cited by the manuscript.",
    },
    {
        "id": "w3c-owl2-overview",
        "type": "webpage",
        "title": "OWL 2 Web Ontology Language Document Overview (Second Edition)",
        "URL": "https://www.w3.org/TR/owl2-overview/",
        "issued": {"date-parts": [[2012, 12, 11]]},
        "author": [{"literal": "W3C OWL Working Group"}],
        "source_note": "Core ontology language standard cited by the manuscript.",
    },
    {
        "id": "w3c-shacl",
        "type": "webpage",
        "title": "Shapes Constraint Language (SHACL)",
        "URL": "https://www.w3.org/TR/shacl/",
        "issued": {"date-parts": [[2017, 7, 20]]},
        "author": [{"literal": "W3C Data Shapes Working Group"}],
        "source_note": "Validation language standard cited by the manuscript.",
    },
    {
        "id": "w3c-rdf11-concepts",
        "type": "webpage",
        "title": "RDF 1.1 Concepts and Abstract Syntax",
        "URL": "https://www.w3.org/TR/rdf11-concepts/",
        "issued": {"date-parts": [[2014, 2, 25]]},
        "author": [{"literal": "W3C RDF Working Group"}],
        "source_note": "RDF graph model standard cited by the manuscript.",
    },
    {
        "id": "w3c-json-ld11",
        "type": "webpage",
        "title": "JSON-LD 1.1",
        "URL": "https://www.w3.org/TR/json-ld11/",
        "issued": {"date-parts": [[2020, 7, 16]]},
        "author": [{"literal": "W3C JSON-LD Working Group"}],
        "source_note": "Linked data serialization standard relevant to UOGTO contexts.",
    },
    {
        "id": "w3c-sparql11-query",
        "type": "webpage",
        "title": "SPARQL 1.1 Query Language",
        "URL": "https://www.w3.org/TR/sparql11-query/",
        "issued": {"date-parts": [[2013, 3, 21]]},
        "author": [{"literal": "W3C SPARQL Working Group"}],
        "source_note": "Competency-query language standard cited by the manuscript.",
    },
    {
        "id": "openalex",
        "type": "webpage",
        "title": "OpenAlex: The Open Catalog to the Global Research System",
        "URL": "https://openalex.org/",
        "author": [{"literal": "OpenAlex"}],
        "source_note": "Literature search metadata source cited by the manuscript.",
    },
    {
        "id": "arxiv-api",
        "type": "webpage",
        "title": "arXiv API User Manual",
        "URL": "https://info.arxiv.org/help/api/index.html",
        "author": [{"literal": "arXiv"}],
        "source_note": "Literature search metadata source cited by the manuscript.",
    },
    {
        "id": "crossref",
        "type": "webpage",
        "title": "Crossref",
        "URL": "https://www.crossref.org/",
        "author": [{"literal": "Crossref"}],
        "source_note": "DOI and publication metadata source cited by the manuscript.",
    },
]


def clean_url(url: str) -> str:
    split = urlsplit(url.strip())
    query = [
        (key, value)
        for key, value in parse_qsl(split.query, keep_blank_values=True)
        if not key.lower().startswith("utm_")
    ]
    return urlunsplit((split.scheme, split.netloc, split.path, urlencode(query), split.fragment))


def slugify(value: str, *, max_words: int = 8) -> str:
    words = re.findall(r"[a-z0-9]+", value.lower())
    return "-".join(words[:max_words]) or "source"


def normalize_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    value = doi.strip()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value, flags=re.IGNORECASE)
    return value.lower()


def person_from_name(name: str) -> dict:
    parts = [part for part in name.strip().split() if part]
    if not parts:
        return {}
    if len(parts) == 1:
        return {"literal": parts[0]}
    return {"given": " ".join(parts[:-1]), "family": parts[-1]}


def issued_from_year(year) -> dict | None:
    if year in (None, ""):
        return None
    match = re.search(r"\d{4}", str(year))
    if not match:
        return None
    return {"date-parts": [[int(match.group(0))]]}


def stable_review_id(record: dict) -> str:
    doi = normalize_doi(record.get("doi"))
    url = clean_url(record.get("url") or record.get("id") or "")
    title = record.get("title") or "source"
    year = str(record.get("year") or "")
    if doi == "10.3998/mpub.20269":
        return "rapoport-chammah-1965"
    if "arxiv.org/abs/2006.06580" in url:
        return "arxiv-2006-06580v3"
    if doi:
        return "doi-" + slugify(doi.replace("/", "-"), max_words=12)
    if "arxiv.org/abs/" in url:
        return "arxiv-" + slugify(url.rsplit("/", 1)[-1], max_words=12)
    return "-".join(part for part in [slugify(title), year[:4]] if part)


def csl_type_for(record: dict) -> str:
    source = str(record.get("source") or "").lower()
    title = str(record.get("title") or "").lower()
    if "prisoner's dilemma" == title and record.get("doi"):
        return "book"
    if source == "arxiv":
        return "article"
    return "article-journal"


def review_record_to_csl(record: dict) -> dict:
    csl = {
        "id": stable_review_id(record),
        "type": csl_type_for(record),
        "title": record.get("title") or "Untitled source",
        "URL": clean_url(record.get("url") or record.get("id") or ""),
        "source_note": f"Imported from {record.get('source', 'review data')}.",
    }
    doi = normalize_doi(record.get("doi"))
    if doi:
        csl["DOI"] = doi
    issued = issued_from_year(record.get("year"))
    if issued:
        csl["issued"] = issued
    authors = [person_from_name(author) for author in record.get("authors") or []]
    authors = [author for author in authors if author]
    if authors:
        csl["author"] = authors
    abstract = record.get("abstract")
    if abstract:
        csl["abstract"] = abstract
    return csl


def markdown_reference_to_csl(path: Path, line_number: int, url: str, title: str) -> dict:
    clean = clean_url(url)
    return {
        "id": f"{path.stem}-{line_number}-{slugify(title, max_words=5)}",
        "type": "webpage",
        "title": title,
        "URL": clean,
        "source_note": f"Markdown reference from {path.relative_to(ROOT)}:{line_number}.",
    }


def load_review_records() -> list[dict]:
    records = []
    for path in REVIEW_DATA_FILES:
        if path.exists():
            records.extend(json.loads(path.read_text(encoding="utf-8")))
    return records


def load_markdown_reference_records() -> list[dict]:
    records = []
    for path in DEEP_RESEARCH_FILES:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            match = MARKDOWN_REFERENCE_RE.match(line.strip())
            if match:
                records.append(
                    markdown_reference_to_csl(
                        path,
                        line_number,
                        match.group("url"),
                        match.group("title"),
                    )
                )
    return records


def build_csl_references() -> list[dict]:
    seen = set()
    references = []
    candidates = (
        [dict(record) for record in CURATED_REFERENCES]
        + [review_record_to_csl(record) for record in load_review_records()]
        + load_markdown_reference_records()
    )
    for record in candidates:
        key = (
            normalize_doi(record.get("DOI")),
            clean_url(record.get("URL", "")),
            record.get("title", "").casefold(),
        )
        if key in seen:
            continue
        seen.add(key)
        references.append(record)
    return sorted(references, key=lambda item: item["id"])


def review_queue_entries(references: list[dict]) -> list[dict]:
    entries = []
    for record in references:
        reasons = []
        url = record.get("URL", "")
        if "wikipedia.org" in url:
            reasons.append("non-scholarly tertiary web reference")
        if "chatgpt.com" in url or "utm_" in url:
            reasons.append("generated tracking URL was not fully normalized")
        if record["type"] in {"article", "article-journal", "book"} and not record.get("author"):
            reasons.append("missing author metadata")
        if not record.get("issued"):
            reasons.append("missing issued date")
        if reasons:
            entries.append(
                {
                    "id": record["id"],
                    "title": record.get("title"),
                    "url": url,
                    "reasons": reasons,
                    "review_status": "needs-manual-review",
                }
            )
    return entries


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_source_artifacts(
    paper_dir: Path = PAPER_DIR,
    sourceright_dir: Path = SOURCERIGHT_DIR,
) -> dict:
    references = build_csl_references()
    manuscript_ids = set(MANUSCRIPT_REFERENCE_IDS)
    manuscript_references = [record for record in references if record["id"] in manuscript_ids]
    missing_manuscript_ids = sorted(manuscript_ids - {record["id"] for record in manuscript_references})
    if missing_manuscript_ids:
        raise AssertionError(
            "Missing manuscript references: " + ", ".join(missing_manuscript_ids)
        )

    queue = review_queue_entries(manuscript_references)
    inventory_queue = review_queue_entries(references)
    queued_ids = {item["id"] for item in queue}
    verification = {
        "schema_version": "sourceright.verification.v1",
        "references": {
            record["id"]: {
                "provider_candidates": [
                    {
                        "provider": "uogto-local-source-inventory",
                        "confidence": 1.0,
                        "retrieved_at": "2026-06-22T00:00:00Z",
                        "data": {
                            "id": record["id"],
                            "title": record.get("title"),
                            "URL": record.get("URL"),
                            "DOI": record.get("DOI"),
                        },
                    }
                ],
                "review_status": "queued" if record["id"] in queued_ids else "not_required",
            }
            for record in manuscript_references
        },
    }
    inventory = {
        "schema_version": "uogto.manuscript_sources.v1",
        "reference_count": len(references),
        "manuscript_reference_count": len(manuscript_references),
        "review_queue_count": len(inventory_queue),
        "sourceright_review_queue_count": len(queue),
        "references": references,
    }

    write_json(paper_dir / "references.csl.json", manuscript_references)
    write_json(paper_dir / "source-inventory.json", inventory)
    write_json(sourceright_dir / "references.csl.json", manuscript_references)
    write_json(sourceright_dir / "references.verification.json", verification)

    review_queue_text = "".join(
        json.dumps(item, ensure_ascii=False) + "\n" for item in inventory_queue
    )
    (paper_dir / "source-review-queue.jsonl").write_text(review_queue_text, encoding="utf-8")
    sourceright_queue_text = "".join(
        json.dumps(
            {
                "id": item["id"],
                "extraction": {
                    "source": "uogto-local-source-inventory",
                    "original_text": item["title"],
                },
                "conflicts": [
                    {
                        "field": "source_metadata",
                        "severity": "review",
                        "source": "uogto-local-source-inventory",
                        "reasons": item["reasons"],
                    }
                ],
                "review_status": "queued",
            },
            ensure_ascii=False,
        )
        + "\n"
        for item in queue
    )
    (sourceright_dir / "review-queue.jsonl").write_text(sourceright_queue_text, encoding="utf-8")

    numeric_citations = " ".join(
        f"[{index}]" for index, _record in enumerate(manuscript_references, start=1)
    )
    manuscript_text = (
        "SourceRight numeric citation export for the current UOGTO manuscript bibliography: "
        f"{numeric_citations}\n"
    )
    (paper_dir / "manuscript-citations.txt").write_text(manuscript_text, encoding="utf-8")
    return inventory


def main() -> None:
    parser = argparse.ArgumentParser(description="Build UOGTO manuscript SourceRight inputs.")
    parser.add_argument("--paper-dir", default=str(PAPER_DIR))
    parser.add_argument("--sourceright-dir", default=str(SOURCERIGHT_DIR))
    args = parser.parse_args()
    inventory = write_source_artifacts(Path(args.paper_dir), Path(args.sourceright_dir))
    print(
        f"Wrote {inventory['reference_count']} source inventory references, "
        f"{inventory['manuscript_reference_count']} manuscript references, "
        f"and {inventory['sourceright_review_queue_count']} SourceRight review-queue entries."
    )


if __name__ == "__main__":
    main()
