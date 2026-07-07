import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "dist" / "extended-registry-handoff.json"
DOC_PATH = ROOT / "docs" / "registry" / "extended-discoverability-submissions.md"

CORE_NAMESPACE = "https://w3id.org/uogto/core#"
EXTENSION_NAMESPACE = "https://w3id.org/uogto/extensions#"
DOI_URL = "https://doi.org/10.5281/zenodo.20796937"
REPOSITORY_URL = "https://github.com/edithatogo/UOGTO"
DOCUMENTATION_URL = "https://edithatogo.github.io/UOGTO/"
RELEASE_URL = "https://github.com/edithatogo/UOGTO/releases/tag/v1.0.0"
RDF_ASSET_URL = "https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/uogto.ttl"
BIOREGISTRY_RESPONSE_COMMENT = "https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4885550451"
AUTHOR_ORCID_URL = "https://orcid.org/0000-0002-9775-0603"
BIOREGISTRY_ORCID_COMMENT = "https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4885988980"
LOV_SUPPLEMENT_COMMENT = "https://github.com/pyvandenbussche/lov/issues/83#issuecomment-4902620021"
OLS_SUPPLEMENT_COMMENT = "https://github.com/EBISPOT/ols4/issues/1305#issuecomment-4902620274"
ONTOBEE_SUPPLEMENT_COMMENT = "https://github.com/OntoZoo/ontobee/issues/212#issuecomment-4902620502"

REGISTRY_METADATA_SUPPLEMENT = {
    "namespace_policy": (
        "Register uogto as the primary core prefix for https://w3id.org/uogto/core#; "
        "retain uogtox as the separate extension prefix for https://w3id.org/uogto/extensions#."
    ),
    "author_orcid": AUTHOR_ORCID_URL,
    "health_relevance": (
        "UOGTO supports game-theoretic modelling across genomics, clinical genetics, paediatrics, "
        "health economics, behavioural/public-health interaction models, mechanism design, "
        "and health-simulation settings."
    ),
    "supplement_comments": {
        "lov": LOV_SUPPLEMENT_COMMENT,
        "ols": OLS_SUPPLEMENT_COMMENT,
        "ontobee": ONTOBEE_SUPPLEMENT_COMMENT,
    },
}

REQUIRED_DOCUMENT_FRAGMENTS = [
    "Universal Open Game Theory Ontology (UOGTO)",
    "Preferred core prefix: `uogto`",
    "Preferred extension prefix: `uogtox`",
    CORE_NAMESPACE,
    EXTENSION_NAMESPACE,
    DOI_URL,
    REPOSITORY_URL,
    DOCUMENTATION_URL,
    RELEASE_URL,
    RDF_ASSET_URL,
    "LOV submission: <https://github.com/pyvandenbussche/lov/issues/83>",
    "OLS request: <https://github.com/EBISPOT/ols4/issues/1305>",
    "w3id redirect PR: <https://github.com/perma-id/w3id.org/pull/6238>",
    LOV_SUPPLEMENT_COMMENT,
    OLS_SUPPLEMENT_COMMENT,
    ONTOBEE_SUPPLEMENT_COMMENT,
]


TARGETS = {
    "fairsharing": {
        "status": "submitted_awaiting_curation",
        "route": "https://fairsharing.org/",
        "record": "https://fairsharing.org/8382",
        "review_status": "awaiting_fairsharing_curator_review",
        "recommended_fields_missing": [
            "organisation links",
            "publications",
            "citations",
            "record associations",
        ],
        "evidence": "Required data processes and conditions metadata persisted on 2026-06-24; public record reports awaiting FAIRsharing curator review.",
        "cross_registry_update_policy": "Add ORCID, namespace-policy, and health-relevance metadata only if curator guidance or the editable record schema provides appropriate fields.",
    },
    "prefix_cc": {
        "status": "submitted",
        "route": "http://prefix.cc/",
        "submitted": {
            "uogto": {
                "uri": CORE_NAMESPACE,
                "evidence": "http://prefix.cc/uogto.file.txt",
            },
            "uogtox": {
                "uri": EXTENSION_NAMESPACE,
                "evidence": "http://prefix.cc/uogtox.file.txt",
            }
        },
        "cross_registry_update_status": "No change required; live prefix mappings already encode the core and extension namespace split.",
    },
    "wikidata": {
        "status": "created_verified",
        "route": "https://www.wikidata.org/wiki/Q140323510",
        "item": "https://www.wikidata.org/wiki/Q140323510",
        "evidence": "Item Q140323510 was created through the authenticated Wikidata session and verified with DOI, documentation, repository, ontology classification, and CC-BY-4.0 license statements.",
        "cross_registry_update_policy": "Do not add author, ORCID, or health-relevance statements unless a stable citation or Wikidata property mapping makes the statement defensible.",
    },
    "ontobee": {
        "status": "submitted",
        "route": "https://ontobee.org/",
        "issue": "https://github.com/OntoZoo/ontobee/issues/212",
        "evidence": "w3id PR 6238 is merged and /uogto/core plus /uogto/extensions return 303 redirects to the UOGTO documentation.",
        "supplement_comment": ONTOBEE_SUPPLEMENT_COMMENT,
    },
    "bioportal": {
        "status": "not_submitted_conditional",
        "route": "https://bioportal.bioontology.org/",
        "decision": "Do not submit without an approved BioPortal-specific positioning note, even though the OLS request now records a defensible biomedical and health relevance summary.",
    },
    "bioregistry": {
        "status": "orcid_added_awaiting_maintainer_review",
        "route": "https://bioregistry.io/",
        "issue": "https://github.com/biopragmatics/bioregistry/issues/1999",
        "maintainer_comment": "https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4769473415",
        "template_update_comment": "https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4778481220",
        "namespace_orcid_feedback": "https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4796538000",
        "response_comment": BIOREGISTRY_RESPONSE_COMMENT,
        "orcid_comment": BIOREGISTRY_ORCID_COMMENT,
        "author_orcid": AUTHOR_ORCID_URL,
        "cross_registry_metadata_supplement": REGISTRY_METADATA_SUPPLEMENT,
        "review_status": "awaiting_bioregistry_maintainer_review_after_response",
        "namespace_decision": "Register uogto as the primary core prefix; retain uogtox as a separately documented extension prefix unless Bioregistry requires a separate compatibility decision.",
        "orcid_handling": "ORCID is approved public project metadata and is mirrored in CITATION.cff, .zenodo.json, and the Bioregistry issue body.",
        "next_action": "Monitor maintainer response; if Bioregistry requires a squashed namespace, open a separate ontology-compatibility track.",
    },
    "obo_foundry": {
        "status": "not_prioritized",
        "route": "https://obofoundry.org/",
        "decision": "Do not pursue unless UOGTO is repositioned for biological or biomedical ontology governance.",
    },
}


def read_doc() -> str:
    if not DOC_PATH.exists():
        raise AssertionError("Missing docs/registry/extended-discoverability-submissions.md")
    return DOC_PATH.read_text(encoding="utf-8")


def build_extended_registry_handoff() -> dict:
    doc_text = read_doc()
    missing = [fragment for fragment in REQUIRED_DOCUMENT_FRAGMENTS if fragment not in doc_text]
    if missing:
        raise AssertionError(
            "Extended registry doc missing canonical metadata fragments: " + ", ".join(missing)
        )

    blockers = []
    for name, target in TARGETS.items():
        if target["route"] not in doc_text:
            raise AssertionError(f"Extended registry doc missing route for {name}: {target['route']}")
        status = target["status"]
        if status in {"prepared_account_required", "partial", "deferred_pending_w3id"}:
            blocker = target.get("blocker") or f"{name} remains pending."
            blockers.append({"target": name, "message": blocker})

    review_pending = [
        name
        for name, target in TARGETS.items()
        if target.get("review_status", "").startswith("awaiting_")
    ]

    return {
        "schema": "uogto.extended-registry-handoff.v1",
        "status": "external_actions_pending" if blockers else "external_review_pending" if review_pending else "complete",
        "blockers": blockers,
        "review_pending": review_pending,
        "ontology": {
            "title": "Universal Open Game Theory Ontology (UOGTO)",
            "preferred_prefix": "uogto",
            "extension_prefix": "uogtox",
            "core_namespace": CORE_NAMESPACE,
            "extension_namespace": EXTENSION_NAMESPACE,
            "doi": DOI_URL,
            "repository": REPOSITORY_URL,
            "documentation": DOCUMENTATION_URL,
            "release": RELEASE_URL,
            "canonical_rdf": RDF_ASSET_URL,
            "author_orcid": AUTHOR_ORCID_URL,
        },
        "cross_registry_metadata_supplement": REGISTRY_METADATA_SUPPLEMENT,
        "targets": TARGETS,
        "source_document": "docs/registry/extended-discoverability-submissions.md",
    }


def write_handoff(output_path: Path, packet: dict) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")



def display_path(output_path: Path) -> str:
    resolved = output_path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(output_path)

def main() -> None:
    parser = argparse.ArgumentParser(description="Build the UOGTO extended registry handoff packet.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="JSON output path. Defaults to dist/extended-registry-handoff.json.",
    )
    args = parser.parse_args()

    packet = build_extended_registry_handoff()
    write_handoff(args.output, packet)
    print(f"Wrote {display_path(args.output)} with status {packet['status']}.")


if __name__ == "__main__":
    main()
