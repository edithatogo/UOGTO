"""Validate article-hardening protocol scaffold artifacts."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "article-hardening"

REQUIRED_FILES = [
    DOCS / "protocol.md",
    DOCS / "protocol-checklist.md",
    DOCS / "search-strategy.md",
]

PROTOCOL_SECTIONS = [
    "## Title",
    "## Protocol Standards",
    "## Rationale",
    "## Objectives",
    "## Review Questions",
    "## Information Sources",
    "## Search Strategy",
    "## Eligibility Criteria",
    "## Evidence Levels",
    "## Data Charting Fields",
    "## Synthesis Plan",
    "## Missing-Element Decision Rules",
    "## Reproducibility Plan",
    "## Limitations",
    "## Protocol Amendments",
    "## Funding and Conflicts",
]

PROTOCOL_TERMS = [
    "PRISMA-ScR",
    "PRISMA-S",
    "RO-Crate 1.1",
    "parsed_rdf_owl",
    "structured_non_rdf",
    "metadata_only",
    "literature_only",
    "excluded",
    "add_to_uogto",
    "align_external_only",
    "requires_domain_review",
]

SEARCH_FIELDS = [
    "searched_at",
    "surface",
    "surface_type",
    "query",
    "filters",
    "result_count",
    "screened_count",
    "included_count",
    "route_limitations",
    "operator_notes",
    "source_ids_added",
]

CHECKLIST_STANDARDS = ["PRISMA-ScR", "PRISMA-S", "RO-Crate 1.1", "UOGTO governance"]


def _read(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"Missing required article-hardening artifact: {path}")
    return path.read_text(encoding="utf-8")


def validate_protocol() -> None:
    protocol = _read(DOCS / "protocol.md")
    missing_sections = [section for section in PROTOCOL_SECTIONS if section not in protocol]
    if missing_sections:
        raise SystemExit(f"Protocol missing sections: {', '.join(missing_sections)}")
    missing_terms = [term for term in PROTOCOL_TERMS if term not in protocol]
    if missing_terms:
        raise SystemExit(f"Protocol missing reporting terms: {', '.join(missing_terms)}")


def validate_search_strategy() -> None:
    strategy = _read(DOCS / "search-strategy.md")
    missing_fields = [field for field in SEARCH_FIELDS if f"`{field}`" not in strategy]
    if missing_fields:
        raise SystemExit(f"Search strategy missing PRISMA-S fields: {', '.join(missing_fields)}")
    for route in [
        "ontology_registry",
        "scholarly_index",
        "archive",
        "repository",
        "standards_body",
        "project_site",
        "web_search",
        "baseline_artifact",
    ]:
        if f"`{route}`" not in strategy:
            raise SystemExit(f"Search strategy missing route taxonomy: {route}")


def validate_checklist() -> None:
    checklist = _read(DOCS / "protocol-checklist.md")
    for standard in CHECKLIST_STANDARDS:
        if standard not in checklist:
            raise SystemExit(f"Protocol checklist missing standard: {standard}")
    required_artifacts = [
        "docs/article-hardening/protocol.md",
        "docs/article-hardening/search-strategy.md",
        ".conductor/runlog.md",
    ]
    for artifact in required_artifacts:
        if artifact not in checklist:
            raise SystemExit(f"Protocol checklist missing artifact reference: {artifact}")


def main() -> None:
    for path in REQUIRED_FILES:
        _read(path)
    validate_protocol()
    validate_search_strategy()
    validate_checklist()
    print(
        "Article-hardening protocol valid: "
        "PRISMA-ScR scaffold, PRISMA-S fields, RO-Crate requirements, "
        "and UOGTO inclusion reporting rules present."
    )


if __name__ == "__main__":
    main()
