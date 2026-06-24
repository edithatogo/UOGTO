"""Build and validate the article-hardening Phase 2 evidence register."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "article-hardening"
BASELINE_INVENTORY = ROOT / "docs" / "ontology-comparison" / "source-inventory.json"
DEFAULT_SEARCH_LOG = DOCS / "search-log.jsonl"
DEFAULT_INVENTORY = DOCS / "source-extension-inventory.json"
DEFAULT_SUMMARY = DOCS / "source-extension-inventory.md"
REGISTER_DATE = "2026-06-24"

SURFACE_TYPES = {
    "baseline_artifact",
    "ontology_registry",
    "scholarly_index",
    "archive",
    "repository",
    "standards_body",
    "project_site",
    "web_search",
}

EVIDENCE_LEVELS = {
    "parsed_rdf_owl",
    "structured_non_rdf",
    "metadata_only",
    "literature_only",
    "excluded",
}

REQUIRED_SEARCH_FIELDS = [
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

REQUIRED_SOURCE_FIELDS = [
    "source_id",
    "source_name",
    "source_family",
    "modelling_paradigm",
    "source_type",
    "canonical_url",
    "discovery_route",
    "licence",
    "artifact_availability",
    "parseability",
    "evidence_level",
    "mapping_relevance",
    "uogto_module_relevance",
    "article_use_category",
    "inclusion_status",
    "inclusion_rationale",
    "reviewer_handoff",
    "search_record_ids",
    "baseline_status",
    "limitations",
    "source_hash",
]


EXTENSION_SOURCES = [
    {
        "source_id": "sssom",
        "source_name": "Simple Standard for Sharing Ontological Mappings (SSSOM)",
        "source_family": "mapping_standard",
        "modelling_paradigm": "ontology_mapping",
        "source_type": "mapping_standard",
        "canonical_url": "https://mapping-commons.github.io/sssom/",
        "discovery_route": "mapping standards source discovery",
        "licence": {"name": "unspecified", "disposition": "needs_licence_review", "url": None},
        "artifact_availability": "public specification and TSV/YAML serialisation guidance",
        "parseability": "structured_non_rdf",
        "evidence_level": "structured_non_rdf",
        "mapping_relevance": "high",
        "uogto_module_relevance": ["alignments", "article-hardening", "ontology-comparison"],
        "article_use_category": "mapping-publication-standard",
        "inclusion_status": "included",
        "inclusion_rationale": "SSSOM directly supports reviewable, publishable ontology mapping tables alongside UOGTO RDF/Turtle alignments.",
        "reviewer_handoff": {
            "assigned_roles": ["evidence_curation_researcher", "reproducibility_curator", "ontology_peer_reviewer"],
            "next_action": "Check SSSOM TSV/metadata outputs against accepted UOGTO mapping decisions.",
            "status": "ready_for_mapping_output_review",
        },
        "search_record_ids": ["phase2-mapping-standards"],
        "baseline_status": "new_candidate",
        "limitations": "Specification fields can evolve; TSV outputs should keep a documented SSSOM version and local validation.",
    },
    {
        "source_id": "robot",
        "source_name": "ROBOT ontology tool",
        "source_family": "ontology_quality_tool",
        "modelling_paradigm": "ontology_engineering",
        "source_type": "software_tool",
        "canonical_url": "https://robot.obolibrary.org/",
        "discovery_route": "ontology engineering tool search",
        "licence": {"name": "unspecified", "disposition": "needs_licence_review", "url": None},
        "artifact_availability": "public documentation and release artifacts",
        "parseability": "metadata_only",
        "evidence_level": "metadata_only",
        "mapping_relevance": "medium",
        "uogto_module_relevance": ["quality-metrics", "release-validation"],
        "article_use_category": "quality-method-candidate",
        "inclusion_status": "included",
        "inclusion_rationale": "ROBOT is relevant to article hardening because it can support ontology report, reasoning, and profile checks in later phases.",
        "reviewer_handoff": {
            "assigned_roles": ["reproducibility_curator", "methods_editor"],
            "next_action": "Decide whether Java-based ROBOT checks should become optional or required in Phase 4.",
            "status": "method_feasibility_review",
        },
        "search_record_ids": ["phase2-mapping-standards"],
        "baseline_status": "new_candidate",
        "limitations": "Method/tool source rather than a comparator ontology; use for methods, not overlap counts.",
    },
    {
        "source_id": "oaei",
        "source_name": "Ontology Alignment Evaluation Initiative",
        "source_family": "mapping_evaluation_benchmark",
        "modelling_paradigm": "ontology_alignment",
        "source_type": "benchmark_programme",
        "canonical_url": "https://oaei.ontologymatching.org/",
        "discovery_route": "mapping standards source discovery",
        "licence": {"name": "varies_by_track", "disposition": "needs_licence_review", "url": None},
        "artifact_availability": "public benchmark pages and track artifacts",
        "parseability": "metadata_only",
        "evidence_level": "metadata_only",
        "mapping_relevance": "medium",
        "uogto_module_relevance": ["ontology-comparison", "mapping-robustness"],
        "article_use_category": "mapping-method-context",
        "inclusion_status": "included",
        "inclusion_rationale": "OAEI is relevant background for reporting ontology mapping evaluation and manual review calibration.",
        "reviewer_handoff": {
            "assigned_roles": ["standards_landscape_researcher", "methods_editor"],
            "next_action": "Use as methodological context for mapping robustness rather than as a UOGTO comparator.",
            "status": "contextual_evidence",
        },
        "search_record_ids": ["phase2-mapping-standards"],
        "baseline_status": "new_candidate",
        "limitations": "Benchmark tracks are heterogeneous and not a single ontology source.",
    },
    {
        "source_id": "stanford_gdl",
        "source_name": "Stanford Game Description Language",
        "source_family": "game_description_language",
        "modelling_paradigm": "general_game_playing",
        "source_type": "formal_language",
        "canonical_url": "http://games.stanford.edu/gdl.html",
        "discovery_route": "game description language source discovery",
        "licence": {"name": "unspecified", "disposition": "metadata_only", "url": None},
        "artifact_availability": "public documentation and literature references",
        "parseability": "literature_or_documentation",
        "evidence_level": "literature_only",
        "mapping_relevance": "high",
        "uogto_module_relevance": ["rules", "states", "actions", "outcomes"],
        "article_use_category": "game-formalism-comparator",
        "inclusion_status": "included",
        "inclusion_rationale": "GDL captures game rules, legal moves, states, roles, goals, and terminal conditions that overlap UOGTO game specification semantics.",
        "reviewer_handoff": {
            "assigned_roles": ["game_theory_gap_researcher", "evidence_curation_researcher"],
            "next_action": "Chart GDL constructs against UOGTO rules, actions, terminal states, and payoff/outcome terms.",
            "status": "needs_construct_charting",
        },
        "search_record_ids": ["phase2-game-description"],
        "baseline_status": "new_candidate",
        "limitations": "Use metadata/literature unless a redistributable grammar or corpus is explicitly acquired later.",
    },
    {
        "source_id": "gdl_ii_iii_gdlz",
        "source_name": "GDL-II, GDL-III, and GDLZ variants",
        "source_family": "game_description_language",
        "modelling_paradigm": "general_game_playing",
        "source_type": "formal_language_family",
        "canonical_url": "https://doi.org/10.1007/978-3-319-71649-7_15",
        "discovery_route": "game description language source discovery",
        "licence": {"name": "publisher_restricted", "disposition": "metadata_only", "url": None},
        "artifact_availability": "literature and project references",
        "parseability": "literature_or_documentation",
        "evidence_level": "literature_only",
        "mapping_relevance": "high",
        "uogto_module_relevance": ["imperfect-information", "epistemic-games", "dynamic-games"],
        "article_use_category": "game-formalism-comparator",
        "inclusion_status": "included",
        "inclusion_rationale": "These GDL variants are relevant for imperfect information, epistemic, and extended game-description constructs that may expose UOGTO gaps.",
        "reviewer_handoff": {
            "assigned_roles": ["game_theory_gap_researcher"],
            "next_action": "Decide whether imperfect-information and epistemic constructs require UOGTO additions or external alignment only.",
            "status": "gap_analysis_required",
        },
        "search_record_ids": ["phase2-game-description"],
        "baseline_status": "new_candidate",
        "limitations": "Likely literature-only until a stable public specification artifact is acquired.",
    },
    {
        "source_id": "ludii",
        "source_name": "Ludii general game system",
        "source_family": "game_description_language",
        "modelling_paradigm": "general_game_playing",
        "source_type": "software_language_repository",
        "canonical_url": "https://ludii.games/",
        "discovery_route": "game AI project source discovery",
        "licence": {"name": "needs_review", "disposition": "needs_licence_review", "url": None},
        "artifact_availability": "public project site, game descriptions, and source repository references",
        "parseability": "structured_non_rdf",
        "evidence_level": "structured_non_rdf",
        "mapping_relevance": "high",
        "uogto_module_relevance": ["game-specification", "rules", "actions", "outcomes", "players"],
        "article_use_category": "game-formalism-comparator",
        "inclusion_status": "included",
        "inclusion_rationale": "Ludii game descriptions provide structured cross-game constructs useful for evaluating UOGTO rule and component coverage.",
        "reviewer_handoff": {
            "assigned_roles": ["game_theory_gap_researcher", "reproducibility_curator"],
            "next_action": "Review licence and decide whether sample Ludii descriptions can be charted without redistribution.",
            "status": "licence_and_sampling_review",
        },
        "search_record_ids": ["phase2-game-description"],
        "baseline_status": "new_candidate",
        "limitations": "Licence and corpus redistribution need review before source acquisition.",
    },
    {
        "source_id": "gvgai_vgdl",
        "source_name": "General Video Game AI and VGDL resources",
        "source_family": "game_description_language",
        "modelling_paradigm": "game_ai_benchmarking",
        "source_type": "benchmark_framework_and_language",
        "canonical_url": "https://www.gvgai.net/",
        "discovery_route": "game AI project source discovery",
        "licence": {"name": "needs_review", "disposition": "needs_licence_review", "url": None},
        "artifact_availability": "public benchmark/project pages and repositories",
        "parseability": "structured_non_rdf",
        "evidence_level": "structured_non_rdf",
        "mapping_relevance": "medium",
        "uogto_module_relevance": ["actions", "state", "game-ai", "simulation-execution"],
        "article_use_category": "game-ai-comparator",
        "inclusion_status": "included",
        "inclusion_rationale": "GVGAI/VGDL is relevant to executable game descriptions, state transitions, and agent evaluation settings.",
        "reviewer_handoff": {
            "assigned_roles": ["game_theory_gap_researcher", "standards_landscape_researcher"],
            "next_action": "Screen whether VGDL terms are article-relevant or better treated as game-AI context.",
            "status": "screening_required",
        },
        "search_record_ids": ["phase2-game-description"],
        "baseline_status": "new_candidate",
        "limitations": "Benchmark artifacts vary by version and repository; record exact release before acquisition.",
    },
    {
        "source_id": "pnml",
        "source_name": "Petri Net Markup Language",
        "source_family": "petri_net",
        "modelling_paradigm": "discrete_event_simulation",
        "source_type": "xml_standard",
        "canonical_url": "https://www.pnml.org/",
        "discovery_route": "modelling and simulation standards discovery",
        "licence": {"name": "needs_review", "disposition": "metadata_only", "url": None},
        "artifact_availability": "public standards and XML schema references",
        "parseability": "structured_non_rdf",
        "evidence_level": "structured_non_rdf",
        "mapping_relevance": "high",
        "uogto_module_relevance": ["petri-net-devs-hla", "dynamics", "execution-traces"],
        "article_use_category": "simulation-formalism-comparator",
        "inclusion_status": "included",
        "inclusion_rationale": "PNML can support more precise comparison of UOGTO Petri-net examples and discrete-event execution semantics.",
        "reviewer_handoff": {
            "assigned_roles": ["standards_landscape_researcher", "ontology_peer_reviewer"],
            "next_action": "Chart PNML place, transition, arc, marking, and net type constructs against UOGTO Petri-net terms.",
            "status": "construct_charting_required",
        },
        "search_record_ids": ["phase2-simulation-standards"],
        "baseline_status": "new_candidate",
        "limitations": "Use metadata until standard/schema licence and exact version are captured.",
    },
    {
        "source_id": "bpmn_2",
        "source_name": "Business Process Model and Notation 2.0",
        "source_family": "process_modelling",
        "modelling_paradigm": "workflow_process",
        "source_type": "standard_schema",
        "canonical_url": "https://www.omg.org/spec/BPMN/2.0.2/",
        "discovery_route": "process and workflow standards discovery",
        "licence": {"name": "OMG terms", "disposition": "metadata_only", "url": None},
        "artifact_availability": "public specification landing page",
        "parseability": "structured_non_rdf",
        "evidence_level": "structured_non_rdf",
        "mapping_relevance": "medium",
        "uogto_module_relevance": ["execution", "workflow", "actions", "events"],
        "article_use_category": "process-formalism-comparator",
        "inclusion_status": "included",
        "inclusion_rationale": "BPMN event, activity, gateway, and process constructs provide useful comparator evidence for execution/workflow semantics.",
        "reviewer_handoff": {
            "assigned_roles": ["standards_landscape_researcher", "methods_editor"],
            "next_action": "Limit claims to process/workflow comparators unless a machine-readable metamodel is acquired.",
            "status": "metadata_only_review",
        },
        "search_record_ids": ["phase2-simulation-standards"],
        "baseline_status": "new_candidate",
        "limitations": "Standards licensing may prevent local redistribution.",
    },
    {
        "source_id": "owl_s",
        "source_name": "OWL-S Semantic Markup for Web Services",
        "source_family": "process_service_ontology",
        "modelling_paradigm": "semantic_web_services",
        "source_type": "ontology_submission",
        "canonical_url": "https://www.w3.org/Submission/OWL-S/",
        "discovery_route": "process and workflow standards discovery",
        "licence": {"name": "W3C document terms", "disposition": "needs_licence_review", "url": None},
        "artifact_availability": "public ontology submission and documentation",
        "parseability": "parsed_rdf_owl_candidate",
        "evidence_level": "metadata_only",
        "mapping_relevance": "medium",
        "uogto_module_relevance": ["actions", "processes", "execution-bindings"],
        "article_use_category": "process-ontology-comparator",
        "inclusion_status": "included",
        "inclusion_rationale": "OWL-S process/service concepts are relevant to UOGTO executable action and binding semantics.",
        "reviewer_handoff": {
            "assigned_roles": ["registry_discovery_researcher", "reproducibility_curator"],
            "next_action": "Locate current redistributable OWL artifacts and confirm parseability before term extraction.",
            "status": "artifact_acquisition_candidate",
        },
        "search_record_ids": ["phase2-simulation-standards"],
        "baseline_status": "new_candidate",
        "limitations": "Recorded as metadata-only until a specific OWL file, checksum, and licence are captured.",
    },
    {
        "source_id": "pddl",
        "source_name": "Planning Domain Definition Language",
        "source_family": "planning_language",
        "modelling_paradigm": "automated_planning",
        "source_type": "formal_language",
        "canonical_url": "https://planning.wiki/ref/pddl",
        "discovery_route": "planning/action formalism discovery",
        "licence": {"name": "needs_review", "disposition": "metadata_only", "url": None},
        "artifact_availability": "documentation and benchmark references",
        "parseability": "structured_non_rdf",
        "evidence_level": "structured_non_rdf",
        "mapping_relevance": "medium",
        "uogto_module_relevance": ["actions", "state-transitions", "plans"],
        "article_use_category": "action-formalism-comparator",
        "inclusion_status": "included",
        "inclusion_rationale": "PDDL action preconditions/effects and planning constructs are useful comparators for UOGTO action and transition semantics.",
        "reviewer_handoff": {
            "assigned_roles": ["game_theory_gap_researcher", "standards_landscape_researcher"],
            "next_action": "Screen as adjacent planning formalism; avoid overclaiming game-theory overlap.",
            "status": "adjacent_formalism_review",
        },
        "search_record_ids": ["phase2-simulation-standards"],
        "baseline_status": "new_candidate",
        "limitations": "Not a game ontology; relevance should be limited to action/execution semantics.",
    },
    {
        "source_id": "sbml",
        "source_name": "Systems Biology Markup Language",
        "source_family": "systems_biology_modelling",
        "modelling_paradigm": "dynamic_systems_simulation",
        "source_type": "xml_standard",
        "canonical_url": "https://sbml.org/",
        "discovery_route": "COMBINE and systems-biology standards discovery",
        "licence": {"name": "needs_review", "disposition": "needs_licence_review", "url": None},
        "artifact_availability": "public specifications and schemas",
        "parseability": "structured_non_rdf",
        "evidence_level": "structured_non_rdf",
        "mapping_relevance": "medium",
        "uogto_module_relevance": ["dynamics", "simulation-execution", "models"],
        "article_use_category": "simulation-standard-comparator",
        "inclusion_status": "included",
        "inclusion_rationale": "SBML model/reaction/simulation ecosystem terms are relevant to UOGTO dynamic model and executable simulation semantics.",
        "reviewer_handoff": {
            "assigned_roles": ["standards_landscape_researcher", "reproducibility_curator"],
            "next_action": "Coordinate SBML with SED-ML, KiSAO, SBO, SBGN, CellML, and MIASE evidence.",
            "status": "source_family_charting_required",
        },
        "search_record_ids": ["phase2-systems-biology"],
        "baseline_status": "new_candidate",
        "limitations": "Systems-biology standard; article claims should distinguish biological modelling context from general game-theory scope.",
    },
    {
        "source_id": "sbo",
        "source_name": "Systems Biology Ontology",
        "source_family": "systems_biology_modelling",
        "modelling_paradigm": "dynamic_systems_simulation",
        "source_type": "ontology",
        "canonical_url": "https://www.ebi.ac.uk/sbo/",
        "discovery_route": "COMBINE and systems-biology standards discovery",
        "licence": {"name": "needs_review", "disposition": "needs_licence_review", "url": None},
        "artifact_availability": "public ontology/term service references",
        "parseability": "parsed_rdf_owl_candidate",
        "evidence_level": "metadata_only",
        "mapping_relevance": "medium",
        "uogto_module_relevance": ["dynamics", "simulation-execution", "models"],
        "article_use_category": "ontology-comparator",
        "inclusion_status": "included",
        "inclusion_rationale": "SBO provides controlled terms for systems biology model semantics and simulation-algorithm contexts.",
        "reviewer_handoff": {
            "assigned_roles": ["registry_discovery_researcher", "reproducibility_curator"],
            "next_action": "Acquire a specific redistributable SBO artifact or keep as metadata-only source.",
            "status": "artifact_acquisition_candidate",
        },
        "search_record_ids": ["phase2-systems-biology"],
        "baseline_status": "new_candidate",
        "limitations": "Recorded as metadata-only until artifact URL and licence are pinned.",
    },
    {
        "source_id": "cellml",
        "source_name": "CellML",
        "source_family": "systems_biology_modelling",
        "modelling_paradigm": "dynamic_systems_simulation",
        "source_type": "model_exchange_standard",
        "canonical_url": "https://www.cellml.org/",
        "discovery_route": "COMBINE and systems-biology standards discovery",
        "licence": {"name": "needs_review", "disposition": "needs_licence_review", "url": None},
        "artifact_availability": "public specifications and documentation",
        "parseability": "structured_non_rdf",
        "evidence_level": "structured_non_rdf",
        "mapping_relevance": "medium",
        "uogto_module_relevance": ["dynamics", "simulation-execution", "models"],
        "article_use_category": "simulation-standard-comparator",
        "inclusion_status": "included",
        "inclusion_rationale": "CellML is relevant for mathematical model structure and simulation context comparisons.",
        "reviewer_handoff": {
            "assigned_roles": ["standards_landscape_researcher"],
            "next_action": "Chart only model/execution semantics that generalize beyond biological models.",
            "status": "bounded_relevance_review",
        },
        "search_record_ids": ["phase2-systems-biology"],
        "baseline_status": "new_candidate",
        "limitations": "Domain-specific standard; avoid treating it as game-theory evidence.",
    },
    {
        "source_id": "sbgn",
        "source_name": "Systems Biology Graphical Notation",
        "source_family": "systems_biology_modelling",
        "modelling_paradigm": "network_process_modelling",
        "source_type": "notation_standard",
        "canonical_url": "https://sbgn.github.io/",
        "discovery_route": "COMBINE and systems-biology standards discovery",
        "licence": {"name": "needs_review", "disposition": "needs_licence_review", "url": None},
        "artifact_availability": "public specifications and schema references",
        "parseability": "structured_non_rdf",
        "evidence_level": "structured_non_rdf",
        "mapping_relevance": "low",
        "uogto_module_relevance": ["network-games", "dynamics", "visualisation"],
        "article_use_category": "notation-context",
        "inclusion_status": "included",
        "inclusion_rationale": "SBGN is relevant as a process/network notation comparator, especially for visualizing model dynamics.",
        "reviewer_handoff": {
            "assigned_roles": ["standards_landscape_researcher", "methods_editor"],
            "next_action": "Use only for notation/network-process context unless term-level evidence is acquired.",
            "status": "contextual_evidence",
        },
        "search_record_ids": ["phase2-systems-biology"],
        "baseline_status": "new_candidate",
        "limitations": "Notation standard, not a direct ontology-alignment target at this phase.",
    },
    {
        "source_id": "modelica",
        "source_name": "Modelica language and Modelica Standard Library",
        "source_family": "physical_modelling",
        "modelling_paradigm": "equation_based_modelling",
        "source_type": "modelling_language",
        "canonical_url": "https://modelica.org/",
        "discovery_route": "physical modelling standards discovery",
        "licence": {"name": "needs_review", "disposition": "metadata_only", "url": None},
        "artifact_availability": "public specification and library references",
        "parseability": "structured_non_rdf",
        "evidence_level": "structured_non_rdf",
        "mapping_relevance": "medium",
        "uogto_module_relevance": ["continuous-games", "differential-hybrid-games", "simulation-execution"],
        "article_use_category": "simulation-language-comparator",
        "inclusion_status": "included",
        "inclusion_rationale": "Modelica is relevant to equation-based continuous and hybrid simulation semantics that overlap UOGTO dynamic-game extensions.",
        "reviewer_handoff": {
            "assigned_roles": ["standards_landscape_researcher", "game_theory_gap_researcher"],
            "next_action": "Check whether continuous/hybrid constructs should inform UOGTO inclusion candidates.",
            "status": "gap_analysis_required",
        },
        "search_record_ids": ["phase2-physical-modelling"],
        "baseline_status": "new_candidate",
        "limitations": "Language/library evidence should be charted separately from ontology evidence.",
    },
    {
        "source_id": "fmi",
        "source_name": "Functional Mock-up Interface",
        "source_family": "physical_modelling",
        "modelling_paradigm": "simulation_interoperability",
        "source_type": "interface_standard",
        "canonical_url": "https://fmi-standard.org/",
        "discovery_route": "physical modelling standards discovery",
        "licence": {"name": "needs_review", "disposition": "metadata_only", "url": None},
        "artifact_availability": "public specifications and schemas",
        "parseability": "structured_non_rdf",
        "evidence_level": "structured_non_rdf",
        "mapping_relevance": "medium",
        "uogto_module_relevance": ["execution-bindings", "simulation-execution", "digital-twin-games"],
        "article_use_category": "simulation-interoperability-comparator",
        "inclusion_status": "included",
        "inclusion_rationale": "FMI is relevant to simulator coupling, model exchange, and co-simulation bindings.",
        "reviewer_handoff": {
            "assigned_roles": ["standards_landscape_researcher", "reproducibility_curator"],
            "next_action": "Chart FMI model-exchange/co-simulation constructs against UOGTO execution-binding terms.",
            "status": "construct_charting_required",
        },
        "search_record_ids": ["phase2-physical-modelling"],
        "baseline_status": "new_candidate",
        "limitations": "Interface standard, not a standalone ontology source.",
    },
    {
        "source_id": "sysml",
        "source_name": "Systems Modeling Language",
        "source_family": "systems_engineering",
        "modelling_paradigm": "systems_modelling",
        "source_type": "standard_language",
        "canonical_url": "https://www.omg.org/spec/SysML/",
        "discovery_route": "physical modelling standards discovery",
        "licence": {"name": "OMG terms", "disposition": "metadata_only", "url": None},
        "artifact_availability": "public specification landing pages",
        "parseability": "structured_non_rdf",
        "evidence_level": "structured_non_rdf",
        "mapping_relevance": "low",
        "uogto_module_relevance": ["models", "requirements", "systems"],
        "article_use_category": "systems-modelling-context",
        "inclusion_status": "included",
        "inclusion_rationale": "SysML is an adjacent systems-modelling standard useful for context around model structure and requirements.",
        "reviewer_handoff": {
            "assigned_roles": ["standards_landscape_researcher", "methods_editor"],
            "next_action": "Keep as contextual evidence unless exact semantic overlap is established.",
            "status": "contextual_evidence",
        },
        "search_record_ids": ["phase2-physical-modelling"],
        "baseline_status": "new_candidate",
        "limitations": "Likely too broad for term-level mapping without a narrow use case.",
    },
]


def _canonical(data: object) -> str:
    return json.dumps(data, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def _hash(data: object) -> str:
    return "sha256:" + hashlib.sha256(_canonical(data).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(row, ensure_ascii=True, sort_keys=True) for row in rows]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def baseline_evidence_level(source: dict) -> str:
    disposition = source.get("licence_disposition", "")
    expected = source.get("expected_format", "").lower()
    if disposition == "redistributable_artifact" and any(term in expected for term in ["owl", "rdf", "turtle"]):
        return "parsed_rdf_owl"
    if any(term in expected for term in ["xml", "json", "schema", "metamodel", "logic language"]):
        return "structured_non_rdf"
    if disposition == "metadata_only":
        return "metadata_only"
    return "metadata_only"


def baseline_parseability(source: dict) -> str:
    level = baseline_evidence_level(source)
    if level == "parsed_rdf_owl":
        return "parsed_rdf_owl_candidate"
    if level == "structured_non_rdf":
        return "structured_non_rdf"
    return "metadata_only"


def baseline_module_relevance(family: str) -> list[str]:
    mapping = {
        "simulation_algorithm": ["simulation-execution"],
        "simulation_experiment": ["simulation-execution", "execution-traces"],
        "modelling_simulation_interoperability": ["models", "execution-bindings"],
        "game_description_language": ["game-specification", "rules", "actions"],
        "system_dynamics": ["dynamics", "continuous-games"],
        "discrete_event_simulation": ["petri-net-devs-hla", "dynamics"],
        "distributed_simulation": ["petri-net-devs-hla", "execution-bindings"],
        "agent_based_modelling": ["agents", "simulation-execution"],
        "provenance": ["trust-reputation-provenance", "execution-traces"],
        "time": ["dynamics", "execution-traces"],
        "upper_ontology": ["core"],
    }
    return mapping.get(family, ["core", "article-hardening"])


def transform_baseline_sources(path: Path = BASELINE_INVENTORY) -> list[dict]:
    baseline = read_json(path)
    sources = []
    for source in baseline.get("sources", []):
        licence_disposition = source.get("licence_disposition", "needs_licence_review")
        transformed = {
            "source_id": source["id"],
            "source_name": source["name"],
            "source_family": source["family"],
            "modelling_paradigm": source["family"],
            "source_type": source["candidate_type"],
            "canonical_url": source.get("source_url"),
            "discovery_route": "baseline ontology-comparison artifact",
            "licence": {
                "name": "not_recorded",
                "disposition": licence_disposition,
                "url": None,
                "redistribution_risk": source.get("redistribution_risk"),
            },
            "artifact_availability": source.get("expected_format", "unknown"),
            "parseability": baseline_parseability(source),
            "evidence_level": baseline_evidence_level(source),
            "mapping_relevance": "high" if source.get("priority") == "high" else "medium",
            "uogto_module_relevance": baseline_module_relevance(source["family"]),
            "article_use_category": "baseline-comparator",
            "inclusion_status": "included",
            "inclusion_rationale": source.get("inclusion_rationale", ""),
            "reviewer_handoff": {
                "assigned_roles": ["evidence_curation_researcher", "reproducibility_curator"],
                "next_action": "Preserve as Phase 2 baseline and update only by appending new evidence records.",
                "status": "baseline_preserved",
            },
            "search_record_ids": ["phase2-baseline-comparison"],
            "baseline_status": "baseline_preserved",
            "limitations": "Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there.",
        }
        sources.append(transformed)
    return sources


def add_source_hashes(sources: list[dict]) -> list[dict]:
    hashed = []
    for source in sources:
        payload = dict(source)
        payload.pop("source_hash", None)
        payload["source_hash"] = _hash(payload)
        hashed.append(payload)
    return sorted(hashed, key=lambda row: row["source_id"])


def record_hash(record: dict) -> str:
    payload = dict(record)
    payload.pop("record_hash", None)
    return _hash(payload)


def add_record_hashes(records: list[dict]) -> list[dict]:
    hashed = []
    previous = None
    for record in records:
        payload = dict(record)
        payload["previous_record_hash"] = previous
        payload["record_hash"] = record_hash(payload)
        previous = payload["record_hash"]
        hashed.append(payload)
    return hashed


def route_record(
    record_id: str,
    surface: str,
    surface_type: str,
    query: str,
    sources: list[str],
    evidence_level: str,
    rationale: str,
    limitations: str,
    reviewer_roles: list[str],
    filters: dict | None = None,
) -> dict:
    return {
        "record_id": record_id,
        "searched_at": REGISTER_DATE,
        "surface": surface,
        "surface_type": surface_type,
        "query": query,
        "filters": filters or {"language": "English", "date_range": "not_limited", "artifact_type": "ontology/schema/formalism/standard"},
        "result_count": len(sources),
        "screened_count": len(sources),
        "included_count": len(sources),
        "evidence_level": evidence_level,
        "screening_decision": "included_for_phase2_register",
        "inclusion_rationale": rationale,
        "licence": {"disposition": "mixed", "note": "Per-source licence disposition is recorded in source-extension-inventory.json."},
        "reviewer_handoff": {
            "assigned_roles": reviewer_roles,
            "next_action": "Review source-level licence, evidence level, and article-use category before term acquisition.",
            "status": "ready_for_phase_review",
        },
        "route_limitations": limitations,
        "operator_notes": "Seeded deterministic Phase 2 register entry; later live searches must append new records rather than editing this record.",
        "source_ids_added": sorted(sources),
        "previous_record_hash": None,
        "record_hash": None,
    }


def build_search_records(sources: list[dict]) -> list[dict]:
    by_record: dict[str, list[str]] = defaultdict(list)
    for source in sources:
        for record_id in source["search_record_ids"]:
            by_record[record_id].append(source["source_id"])
    ordered = [
        route_record(
            "phase2-baseline-comparison",
            "docs/ontology-comparison/source-inventory.json",
            "baseline_artifact",
            "Import completed comparative simulation ontology mapping inventory as Phase 2 baseline.",
            by_record["phase2-baseline-comparison"],
            "mixed",
            "Preserves the completed comparison baseline before appending new article-hardening candidates.",
            "Baseline inventory was already curated and is not a fresh live registry search.",
            ["evidence_curation_researcher", "reproducibility_curator"],
            {"source": "repo-local baseline", "version": "2026-06-24"},
        ),
        route_record(
            "phase2-mapping-standards",
            "SSSOM, ROBOT, and OAEI mapping-method surfaces",
            "web_search",
            "SSSOM ROBOT OAEI ontology mapping standard review publication",
            by_record["phase2-mapping-standards"],
            "metadata_only",
            "Adds mapping publication, review, and quality-method sources needed to harden UOGTO mapping evidence.",
            "Method/tool records support reporting and validation design, not ontology overlap counts.",
            ["standards_landscape_researcher", "methods_editor", "ontology_peer_reviewer"],
        ),
        route_record(
            "phase2-game-description",
            "Game description language and game AI project sites",
            "project_site",
            "GDL GDL-II GDL-III GDLZ Ludii VGDL General Video Game AI game description language",
            by_record["phase2-game-description"],
            "structured_non_rdf",
            "Adds game-description and game-AI formalism sources likely to expose rule, move, state, imperfect-information, and execution gaps.",
            "Some sources are literature-only or repository-version dependent; exact artifact acquisition is deferred to Phase 3.",
            ["game_theory_gap_researcher", "evidence_curation_researcher"],
        ),
        route_record(
            "phase2-simulation-standards",
            "Simulation, process, planning, and workflow standards",
            "standards_body",
            "PNML BPMN OWL-S PDDL Petri net process planning ontology simulation standard",
            by_record["phase2-simulation-standards"],
            "structured_non_rdf",
            "Adds process, Petri-net, service/action, and planning standards adjacent to UOGTO simulation and execution semantics.",
            "Several standards have metadata-only or restricted redistribution status until licence review.",
            ["standards_landscape_researcher", "reproducibility_curator"],
        ),
        route_record(
            "phase2-systems-biology",
            "COMBINE and systems-biology modelling standards",
            "standards_body",
            "SBML SBO CellML SBGN SED-ML KiSAO MIASE simulation ontology standard",
            by_record["phase2-systems-biology"],
            "structured_non_rdf",
            "Adds systems-biology modelling standards relevant to simulation experiments, algorithms, model dynamics, and reporting.",
            "Domain-specific sources must be framed as modelling/simulation comparators, not game-theory ontologies.",
            ["standards_landscape_researcher", "methods_editor"],
        ),
        route_record(
            "phase2-physical-modelling",
            "Physical modelling, co-simulation, and systems engineering standards",
            "standards_body",
            "Modelica FMI SysML co-simulation physical modelling ontology standard",
            by_record["phase2-physical-modelling"],
            "structured_non_rdf",
            "Adds continuous, hybrid, co-simulation, and systems-modelling sources for dynamic-game and digital-twin coverage analysis.",
            "Primarily adjacent modelling-language evidence; term-level mappings require later acquisition and review.",
            ["standards_landscape_researcher", "game_theory_gap_researcher"],
        ),
    ]
    return add_record_hashes(ordered)


def build_inventory() -> dict:
    baseline_sources = transform_baseline_sources()
    sources = add_source_hashes(baseline_sources + EXTENSION_SOURCES)
    baseline_hash = _hash(read_json(BASELINE_INVENTORY))
    return {
        "schema": "uogto.article-hardening.source-extension-inventory.v1",
        "created": REGISTER_DATE,
        "description": "Living evidence register for UOGTO article-hardening Phase 2 source discovery.",
        "append_only_contract": {
            "mode": "hash_chained_search_log_plus_source_hashes",
            "immutable_fields": ["source_id", "canonical_url", "baseline_status", "search_record_ids"],
            "rule": "Append new search-log records and source records; do not delete or rewrite prior evidence without recording a protocol amendment.",
        },
        "baseline": {
            "path": "docs/ontology-comparison/source-inventory.json",
            "hash": baseline_hash,
            "source_count": len(baseline_sources),
        },
        "sources": sources,
    }


def write_summary(path: Path, inventory: dict, search_records: list[dict]) -> None:
    sources = inventory["sources"]
    by_evidence = Counter(source["evidence_level"] for source in sources)
    by_status = Counter(source["baseline_status"] for source in sources)
    by_family = Counter(source["source_family"] for source in sources)
    lines = [
        "# Article-Hardening Source Extension Inventory",
        "",
        "This generated summary mirrors `source-extension-inventory.json` and `search-log.jsonl`.",
        "",
        "## Register Contract",
        "",
        "- Search records are hash chained with `previous_record_hash` and `record_hash`.",
        "- Source rows carry immutable `source_hash` values.",
        "- Later searches should append records rather than rewriting prior evidence.",
        "",
        "## Summary Counts",
        "",
        f"- Sources: {len(sources)}",
        f"- Search records: {len(search_records)}",
        f"- Baseline-preserved sources: {by_status.get('baseline_preserved', 0)}",
        f"- New candidates: {by_status.get('new_candidate', 0)}",
        "",
        "## Evidence Levels",
        "",
    ]
    for level, count in sorted(by_evidence.items()):
        lines.append(f"- `{level}`: {count}")
    lines.extend(["", "## Source Families", ""])
    for family, count in sorted(by_family.items()):
        lines.append(f"- `{family}`: {count}")
    highlighted = sorted(
        source["source_name"] for source in sources if source["baseline_status"] == "new_candidate"
    )
    lines.extend(["", "## Highlighted New Candidates", ""])
    lines.append("SSSOM is included as the mapping-standard source for ontology alignment TSV/YAML outputs.")
    lines.append("")
    for source in sorted(
        (source for source in sources if source["baseline_status"] == "new_candidate"),
        key=lambda item: item["source_id"],
    ):
        lines.append(f"- `{source['source_id']}`: {source['source_name']}")
    lines.extend(["", "## Search Records", ""])
    lines.append("| Record | Surface type | Included | Evidence level | Hash |")
    lines.append("| --- | --- | ---: | --- | --- |")
    for record in search_records:
        lines.append(
            f"| `{record['record_id']}` | `{record['surface_type']}` | {record['included_count']} | `{record['evidence_level']}` | `{record['record_hash']}` |"
        )
    lines.extend(["", "## Reviewer Handoff", ""])
    lines.append("Phase 2 records are ready for evidence-curation, reproducibility, standards-landscape, game-theory-gap, peer-review, methods-editorial, red-team, and devil's-advocate review before Phase 3 acquisition.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_search_log(records: list[dict]) -> dict:
    if not records:
        raise AssertionError("search-log.jsonl must contain at least one record")
    previous = None
    ids = set()
    for index, record in enumerate(records):
        missing = [field for field in REQUIRED_SEARCH_FIELDS if field not in record]
        if missing:
            raise AssertionError(f"Search record {index} missing fields: {', '.join(missing)}")
        if record["record_id"] in ids:
            raise AssertionError(f"Duplicate search record_id: {record['record_id']}")
        ids.add(record["record_id"])
        if record["surface_type"] not in SURFACE_TYPES:
            raise AssertionError(f"Search record {record['record_id']} has invalid surface_type")
        if record["evidence_level"] != "mixed" and record["evidence_level"] not in EVIDENCE_LEVELS:
            raise AssertionError(f"Search record {record['record_id']} has invalid evidence_level")
        if record["previous_record_hash"] != previous:
            raise AssertionError(f"Search record {record['record_id']} breaks hash chain")
        expected_hash = record_hash(record)
        if record["record_hash"] != expected_hash:
            raise AssertionError(f"Search record {record['record_id']} has invalid record_hash")
        if not record["source_ids_added"]:
            raise AssertionError(f"Search record {record['record_id']} must add or preserve source IDs")
        if not record["inclusion_rationale"] or not record["licence"] or not record["reviewer_handoff"]:
            raise AssertionError(f"Search record {record['record_id']} lacks rationale, licence, or handoff")
        previous = record["record_hash"]
    return {"record_count": len(records), "record_ids": ids}


def validate_inventory(inventory: dict, search_records: list[dict]) -> dict:
    if inventory.get("schema") != "uogto.article-hardening.source-extension-inventory.v1":
        raise AssertionError("Unexpected source-extension inventory schema")
    search_summary = validate_search_log(search_records)
    search_ids = search_summary["record_ids"]
    source_ids = set()
    baseline_count = 0
    for index, source in enumerate(inventory.get("sources", [])):
        missing = [field for field in REQUIRED_SOURCE_FIELDS if field not in source]
        if missing:
            raise AssertionError(f"Source record {index} missing fields: {', '.join(missing)}")
        if source["source_id"] in source_ids:
            raise AssertionError(f"Duplicate source_id: {source['source_id']}")
        source_ids.add(source["source_id"])
        if source["evidence_level"] not in EVIDENCE_LEVELS:
            raise AssertionError(f"Source {source['source_id']} has invalid evidence_level")
        if not source["inclusion_rationale"] or not source["licence"] or not source["reviewer_handoff"]:
            raise AssertionError(f"Source {source['source_id']} lacks rationale, licence, or handoff")
        if not set(source["search_record_ids"]).issubset(search_ids):
            raise AssertionError(f"Source {source['source_id']} references unknown search records")
        payload = dict(source)
        payload.pop("source_hash", None)
        if source["source_hash"] != _hash(payload):
            raise AssertionError(f"Source {source['source_id']} has invalid source_hash")
        if source["baseline_status"] == "baseline_preserved":
            baseline_count += 1
    log_source_ids = {source_id for record in search_records for source_id in record["source_ids_added"]}
    missing_from_inventory = sorted(log_source_ids - source_ids)
    if missing_from_inventory:
        raise AssertionError("Search log references missing inventory sources: " + ", ".join(missing_from_inventory))
    if baseline_count != inventory.get("baseline", {}).get("source_count"):
        raise AssertionError("Baseline source count does not match preserved inventory sources")
    return {
        "source_count": len(source_ids),
        "search_record_count": len(search_records),
        "baseline_count": baseline_count,
        "new_candidate_count": len(source_ids) - baseline_count,
    }


def build_outputs(search_log: Path, inventory_path: Path, summary_path: Path) -> dict:
    inventory = build_inventory()
    search_records = build_search_records(inventory["sources"])
    write_jsonl(search_log, search_records)
    write_json(inventory_path, inventory)
    write_summary(summary_path, inventory, search_records)
    return validate_inventory(inventory, search_records)


def check_outputs(search_log: Path, inventory_path: Path) -> dict:
    search_records = read_jsonl(search_log)
    inventory = read_json(inventory_path)
    return validate_inventory(inventory, search_records)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build or validate article-hardening Phase 2 evidence register.")
    parser.add_argument("--search-log", type=Path, default=DEFAULT_SEARCH_LOG)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    summary = check_outputs(args.search_log, args.inventory) if args.check_only else build_outputs(args.search_log, args.inventory, args.summary)
    print(
        "Article-hardening source register valid: "
        f"{summary['source_count']} sources, {summary['search_record_count']} search records, "
        f"{summary['baseline_count']} baseline sources, {summary['new_candidate_count']} new candidates."
    )


if __name__ == "__main__":
    main()
