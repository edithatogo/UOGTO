"""Validate article-hardening protocol scaffold artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.maintenance import build_article_hardening_inventory as inventory_builder
from scripts.maintenance import build_article_hardening_quality as quality_builder

DOCS = ROOT / "docs" / "article-hardening"
REVIEW_AGENTS = ROOT / "conductor" / "agents" / "article-hardening-review-agents.json"
RESEARCH_AGENTS = ROOT / "conductor" / "agents" / "article-hardening-research-agents.json"
REVIEW_WORKFLOW = ROOT / "conductor" / "workflows" / "article-hardening-phase-review.md"
RESEARCH_WORKFLOW = ROOT / "conductor" / "workflows" / "article-hardening-research-workflow.md"
REVIEW_SKILL = ROOT / ".agents" / "skills" / "article-hardening-review" / "SKILL.md"
RESEARCH_SKILL = ROOT / ".agents" / "skills" / "article-hardening-research" / "SKILL.md"
REVIEWS = DOCS / "reviews"
RESEARCH = DOCS / "research"
SEARCH_LOG = DOCS / "search-log.jsonl"
SOURCE_EXTENSION_INVENTORY = DOCS / "source-extension-inventory.json"
SOURCE_EXTENSION_SUMMARY = DOCS / "source-extension-inventory.md"
QUALITY_METRICS = DOCS / "quality-metrics.json"
REASONER_REPORT = DOCS / "reasoner-report.md"
ROBOT_DIR = DOCS / "robot"
EVIDENCE_FILES = [
    DOCS / "search-log.jsonl",
    DOCS / "source-extension-inventory.json",
    DOCS / "source-extension-inventory.md",
    DOCS / "quality-metrics.json",
    DOCS / "reasoner-report.md",
    DOCS / "case-studies.md",
    DOCS / "case-studies.json",
    DOCS / "manual-review-sample.csv",
    DOCS / "uogto-inclusion-candidates.csv",
    DOCS / "uogto-inclusion-decisions.md",
    DOCS / "competency-benchmark.md",
    DOCS / "use-case-coverage-matrix.csv",
    DOCS / "ro-crate-metadata.json",
    DOCS / "protocol-checklist.md",
    DOCS / "structured-summary.md",
    DOCS / "prisma-scr-artifact-map.md",
]
REVIEW_AGENTS = ROOT / "conductor" / "agents" / "article-hardening-review-agents.json"
RESEARCH_AGENTS = ROOT / "conductor" / "agents" / "article-hardening-research-agents.json"
REVIEW_WORKFLOW = ROOT / "conductor" / "workflows" / "article-hardening-phase-review.md"
RESEARCH_WORKFLOW = ROOT / "conductor" / "workflows" / "article-hardening-research-workflow.md"
REVIEW_SKILL = ROOT / ".agents" / "skills" / "article-hardening-review" / "SKILL.md"
RESEARCH_SKILL = ROOT / ".agents" / "skills" / "article-hardening-research" / "SKILL.md"
REVIEWS = DOCS / "reviews"
RESEARCH = DOCS / "research"
SEARCH_LOG = DOCS / "search-log.jsonl"
SOURCE_EXTENSION_INVENTORY = DOCS / "source-extension-inventory.json"
SOURCE_EXTENSION_SUMMARY = DOCS / "source-extension-inventory.md"
QUALITY_METRICS = DOCS / "quality-metrics.json"
REASONER_REPORT = DOCS / "reasoner-report.md"
ROBOT_DIR = DOCS / "robot"
ROBOT_REQUIRED_FILES = [
    ROBOT_DIR / "status.json",
    ROBOT_DIR / "reasoner-check.md",
    ROBOT_DIR / "report.md",
    ROBOT_DIR / "merged-ontology.ttl",
    ROBOT_DIR / "merge-diff.md",
    ROBOT_DIR / "import-extraction.ttl",
    ROBOT_DIR / "import-extraction.md",
]

REQUIRED_FILES = [
    DOCS / "protocol.md",
    DOCS / "protocol-checklist.md",
    DOCS / "structured-summary.md",
    DOCS / "prisma-scr-artifact-map.md",
    DOCS / "search-strategy.md",
    REVIEW_AGENTS,
    RESEARCH_AGENTS,
    REVIEW_WORKFLOW,
    RESEARCH_WORKFLOW,
    REVIEW_SKILL,
    RESEARCH_SKILL,
    REVIEWS / "README.md",
    REVIEWS / "phase-review-log.jsonl",
    RESEARCH / "README.md",
    RESEARCH / "phase-research-log.jsonl",
    SEARCH_LOG,
    SOURCE_EXTENSION_INVENTORY,
    SOURCE_EXTENSION_SUMMARY,
    QUALITY_METRICS,
    REASONER_REPORT,
    *ROBOT_REQUIRED_FILES,
    *EVIDENCE_FILES,
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
    "record_id",
    "searched_at",
    "surface",
    "surface_type",
    "query",
    "filters",
    "result_count",
    "screened_count",
    "included_count",
    "evidence_level",
    "screening_decision",
    "inclusion_rationale",
    "licence",
    "reviewer_handoff",
    "route_limitations",
    "operator_notes",
    "source_ids_added",
    "previous_record_hash",
    "record_hash",
]

CHECKLIST_STANDARDS = ["PRISMA-ScR", "PRISMA-S", "RO-Crate 1.1", "UOGTO governance"]


REQUIRED_REVIEWERS = [
    "ontology_peer_reviewer",
    "methods_editor",
    "evidence_red_team",
    "devils_advocate_reviewer",
]

OPTIONAL_PHASE_REVIEWERS = ["simulation_modelling_peer_reviewer"]


REQUIRED_RESEARCHERS = [
    "evidence_curation_researcher",
    "reproducibility_curator",
]

OPTIONAL_PHASE_RESEARCHERS = [
    "registry_discovery_researcher",
    "standards_landscape_researcher",
    "game_theory_gap_researcher",
]


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
        "docs/article-hardening/structured-summary.md",
        "docs/article-hardening/prisma-scr-artifact-map.md",
        "docs/article-hardening/search-strategy.md",
        ".conductor/runlog.md",
    ]
    for artifact in required_artifacts:
        if artifact not in checklist:
            raise SystemExit(f"Protocol checklist missing artifact reference: {artifact}")
    if checklist.count("| PRISMA-ScR |") < 22:
        raise SystemExit("Protocol checklist must map all 20 essential and 2 optional PRISMA-ScR items")
    for item in [
        "Structured summary",
        "Protocol and registration",
        "Critical appraisal of individual sources of evidence",
        "Critical appraisal within sources of evidence",
        "Summary of evidence",
        "Conclusions",
        "Funding",
    ]:
        if item not in checklist:
            raise SystemExit(f"Protocol checklist missing PRISMA-ScR item: {item}")



def validate_review_agents() -> None:
    registry = json.loads(_read(REVIEW_AGENTS))
    role_ids = {role.get("id") for role in registry.get("review_roles", [])}
    missing = [role for role in REQUIRED_REVIEWERS + OPTIONAL_PHASE_REVIEWERS if role not in role_ids]
    if missing:
        raise SystemExit(f"Review agent registry missing roles: {', '.join(missing)}")
    minimum = registry.get("minimum_phase_review_set", [])
    missing_minimum = [role for role in REQUIRED_REVIEWERS if role not in minimum]
    if missing_minimum:
        raise SystemExit(f"Minimum phase review set missing roles: {', '.join(missing_minimum)}")
    for role in registry.get("review_roles", []):
        for field in ["label", "review_type", "phase_scope", "focus", "required_output"]:
            if not role.get(field):
                raise SystemExit(f"Review role {role.get('id')} missing field: {field}")

    workflow = _read(REVIEW_WORKFLOW)
    skill = _read(REVIEW_SKILL)
    review_readme = _read(REVIEWS / "README.md")
    review_log = _read(REVIEWS / "phase-review-log.jsonl")
    for role in REQUIRED_REVIEWERS:
        if role not in workflow or role not in skill or role not in review_log:
            raise SystemExit(f"Review workflow/skill/log missing required role: {role}")
    for term in ["peer", "editorial", "red-team", "devil", "phase-review-log.jsonl"]:
        if term not in workflow and term not in review_readme:
            raise SystemExit(f"Review workflow missing reporting term: {term}")


def validate_research_agents() -> None:
    registry = json.loads(_read(RESEARCH_AGENTS))
    role_ids = {role.get("id") for role in registry.get("research_roles", [])}
    missing = [
        role for role in REQUIRED_RESEARCHERS + OPTIONAL_PHASE_RESEARCHERS if role not in role_ids
    ]
    if missing:
        raise SystemExit(f"Research agent registry missing roles: {', '.join(missing)}")
    minimum = registry.get("minimum_phase_research_set", [])
    missing_minimum = [role for role in REQUIRED_RESEARCHERS if role not in minimum]
    if missing_minimum:
        raise SystemExit(f"Minimum phase research set missing roles: {', '.join(missing_minimum)}")
    for role in registry.get("research_roles", []):
        for field in ["label", "research_type", "phase_scope", "focus", "required_output"]:
            if not role.get(field):
                raise SystemExit(f"Research role {role.get('id')} missing field: {field}")

    workflow = _read(RESEARCH_WORKFLOW)
    skill = _read(RESEARCH_SKILL)
    research_readme = _read(RESEARCH / "README.md")
    research_log = _read(RESEARCH / "phase-research-log.jsonl")
    for role in REQUIRED_RESEARCHERS:
        if role not in workflow or role not in skill or role not in research_log:
            raise SystemExit(f"Research workflow/skill/log missing required role: {role}")
    for term in ["research", "evidence", "reproducibility", "phase-research-log.jsonl"]:
        if term not in workflow and term not in research_readme:
            raise SystemExit(f"Research workflow missing reporting term: {term}")


def validate_source_extension_register() -> None:
    summary = inventory_builder.check_outputs(SEARCH_LOG, SOURCE_EXTENSION_INVENTORY)
    if summary["source_count"] < 39:
        raise SystemExit("Source-extension inventory has too few sources")
    if summary["search_record_count"] < 6:
        raise SystemExit("Search log has too few records")
    summary_text = _read(SOURCE_EXTENSION_SUMMARY)
    for term in ["hash chained", "Later searches should append records", "SSSOM"]:
        if term not in summary_text:
            raise SystemExit(f"Source-extension summary missing term: {term}")



def validate_quality_benchmark() -> None:
    summary = quality_builder.check_outputs(QUALITY_METRICS, REASONER_REPORT)
    if summary["classes"] < 100 or summary["properties"] < 50:
        raise SystemExit("Quality metrics have unexpectedly low ontology term counts")


def main() -> None:
    for path in REQUIRED_FILES:
        _read(path)
    validate_protocol()
    validate_search_strategy()
    validate_checklist()
    validate_review_agents()
    validate_research_agents()
    validate_source_extension_register()
    validate_quality_benchmark()
    print(
        "Article-hardening protocol valid: "
        "PRISMA-ScR scaffold, PRISMA-S fields, RO-Crate requirements, "
        "UOGTO inclusion reporting rules, Phase 2 source register, ontology-quality benchmark, phase-research agents, and phase-review agents present."
    )


if __name__ == "__main__":
    main()
