"""Build a semantic snapshot from standards_check's sourced costing catalogue.

This importer does not fetch sources or assert that editorial mappings are
consensus standards. The source commit and input digests identify the exact
catalogue used; source URLs identify the external authorities.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

from rdflib import DCTERMS, OWL, RDF, RDFS, SKOS, XSD, Graph, Literal, Namespace, URIRef

ROOT = Path(__file__).resolve().parents[2]
COST = Namespace("https://w3id.org/uogto/packs/costing-valuation#")
CAT = Namespace("https://w3id.org/uogto/costing-reporting/")
SOURCE_REPO = "https://github.com/edithatogo/standards_check"
CONTEXT_CATEGORIES = {"development_protocol", "study_protocol", "evidence_review"}

PROFILES = {
    "general-costing": (
        "General costing reporting",
        ["cheers_2022", "ghcc_2017"],
        "Starting selection for a costing study; assess individual applicability, "
        "especially outcome requirements in cost-only studies.",
    ),
    "newborn-screening": (
        "Newborn screening costing",
        ["cheers_2022", "ghcc_2017", "agreedt_2018"],
        "Project-defined composition for screening programmes, not an endorsed "
        "newborn-screening checklist. Add jurisdiction, capacity or budget "
        "profiles only when applicable; document programme boundaries and denominators.",
    ),
    "time-driven-costing": (
        "Time-driven activity-based costing",
        ["cheers_2022", "ghcc_2017", "tdabc_2020"],
        "Adds workflow, timing and practical-capacity concerns; TDABC item extraction is pending.",
    ),
    "diagnostic-strategy": (
        "Diagnostic strategy costing",
        ["cheers_2022", "ghcc_2017", "agreedt_2018"],
        "Use when comparing diagnostic strategies, including downstream management.",
    ),
    "value-of-information": (
        "Value of information reporting",
        ["cheers_2022", "cheers_voi_2023"],
        "Use for a VOI study. The six supplemental items are mapped; inherited "
        "item elaborations still require their source wording.",
    ),
    "ai-intervention": (
        "AI intervention economic reporting",
        ["cheers_2022", "cheers_ai_2024"],
        "Applies when the intervention uses AI; analyst use of an AI assistant "
        "does not itself establish applicability.",
    ),
    "budget-impact": (
        "Budget impact methods and reporting",
        ["ispor_bia_2014"],
        "Separate budget-holder profile; CHEERS alone does not cover budget impact.",
    ),
    "australian-hospital-costing": (
        "Australian hospital costing",
        ["ahpcs_4_2"],
        "Optional Australian patient-costing conduct/reconciliation profile, "
        "not an economic opportunity-cost or reimbursement equivalence.",
    ),
    "england-patient-costing": (
        "England patient costing",
        ["nhs_acg_2026"],
        "Optional release-specific England patient-costing profile.",
    ),
    "validation-reporting": (
        "Model validation reporting",
        ["advishe_2016"],
        "Records validation evidence; structural validity is not empirical validation.",
    ),
    "cost-of-illness-appraisal": (
        "Cost-of-illness appraisal",
        ["coi_appraisal_2023"],
        "An appraisal profile, distinct from reporting completeness.",
    ),
    "economic-methods-appraisal": (
        "Economic methods appraisal",
        ["chec_2005", "philips_2004"],
        "Select an appropriate appraisal instrument for the study design; "
        "this composition does not create a combined numerical score.",
    ),
}


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9.-]+", "-", value.lower()).strip("-")


def identifier(kind: str, value: str) -> URIRef:
    return CAT[f"{kind}/{slug(value)}"]


def add_text(graph: Graph, subject: URIRef, predicate: URIRef, text: str) -> None:
    graph.add((subject, predicate, Literal(text)))


def verify_source_files_at_commit(paths: list[Path], source_commit: str) -> None:
    """Reject mismatched local inputs rather than inventing commit provenance."""
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("source_commit must identify an exact 40-character Git commit")
    repositories = set()
    for path in paths:
        path = path.resolve()
        try:
            repository = Path(subprocess.check_output(
                ["git", "-C", str(path.parent), "rev-parse", "--show-toplevel"],
                text=True, stderr=subprocess.PIPE,
            ).strip()).resolve()
            relative = path.relative_to(repository).as_posix()
            committed = subprocess.check_output(
                ["git", "-C", str(repository), "show", f"{source_commit}:{relative}"],
                stderr=subprocess.PIPE,
            )
        except (subprocess.CalledProcessError, OSError, ValueError) as error:
            raise ValueError(f"Cannot verify source commit for {path.name}") from error
        if committed != path.read_bytes():
            raise ValueError(f"Source input differs from claimed commit: {path.name}")
        repositories.add(repository)
    if len(repositories) != 1:
        raise ValueError("Source inputs must belong to the same catalogue repository")


def build(registry: dict, mappings: dict, source_commit: str) -> tuple[Graph, dict]:
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("source_commit must identify an exact 40-character Git commit")
    instruments = {row["id"]: row for row in registry["instruments"]}
    if len(instruments) != len(registry["instruments"]):
        raise ValueError("duplicate instrument IDs")
    domain_ids = {row["id"] for row in registry["domains"]}
    if len(domain_ids) != len(registry["domains"]):
        raise ValueError("duplicate domain IDs")
    mapped_keys = set()
    for row in mappings["mappings"]:
        key = (row["instrument_id"], row["item_id"])
        if key in mapped_keys:
            raise ValueError(f"duplicate item: {key}")
        mapped_keys.add(key)
        record = instruments[row["instrument_id"]]
        if record["category"] in CONTEXT_CATEGORIES:
            raise ValueError(f"context publication cannot supply instrument items: {key}")
        if not row["item_identifier_verified"] or not record["item_level_verified"]:
            raise ValueError(f"unverified item identifier: {key}")
        if not row["domain_ids"] or not set(row["domain_ids"]) <= domain_ids:
            raise ValueError(f"unknown or absent mapping domain: {key}")

    counts = Counter(row["instrument_id"] for row in mappings["mappings"])
    for key, record in instruments.items():
        scope = record.get("verification_scope", {})
        if scope.get("verified_mapping_count") != counts[key]:
            raise ValueError(f"declared mapping count differs from input: {key}")
        if scope.get("full_checklist_transcription_added") is not False:
            raise ValueError(f"catalogue must not claim full checklist transcription: {key}")
    summary = registry.get("verification_summary", {})
    for key, value in {
        "instrument_count": len(instruments), "domain_count": len(domain_ids),
        "verified_mapping_count": len(mapped_keys), "mapped_instrument_count": len(counts),
        "mapping_counts": dict(counts), "full_checklist_transcriptions_added": 0,
    }.items():
        if summary.get(key) != value:
            raise ValueError(f"catalogue verification summary disagrees with input: {key}")

    graph = Graph()
    for prefix, namespace in {
        "cost": COST, "cat": CAT, "dcterms": DCTERMS, "owl": OWL,
        "rdfs": RDFS, "skos": SKOS, "xsd": XSD,
    }.items():
        graph.bind(prefix, namespace)
    root = URIRef(str(CAT).rstrip("/"))
    graph.add((root, RDF.type, OWL.Ontology))
    graph.add((root, OWL.imports, URIRef(str(COST).rstrip("#"))))
    add_text(graph, root, RDFS.label, "Costing reporting reconciliation snapshot")
    add_text(graph, root, OWL.versionInfo, registry["schema_version"])
    add_text(graph, root, DCTERMS.description, registry["coverage_statement"])
    graph.add((root, DCTERMS.date, Literal(registry["searched_through"], datatype=XSD.date)))
    graph.add((root, DCTERMS.source, URIRef(f"{SOURCE_REPO}/tree/{source_commit}/reconciliations/costing")))
    add_text(graph, root, RDFS.comment,
             "Editorial semantic mappings preserve source identities. They do not "
             "replace official wording, establish consensus, supply a checklist "
             "score or prove methodological, computational or empirical validity.")

    for row in registry["domains"]:
        node = identifier("domain", row["id"])
        graph.add((node, RDF.type, COST.ReportingDomain))
        add_text(graph, node, RDFS.label, row["id"].replace("_", " ").capitalize())
        add_text(graph, node, SKOS.definition, row["definition"])

    for key, row in instruments.items():
        is_context = row["category"] in CONTEXT_CATEGORIES
        node = identifier("source" if is_context else "instrument", key)
        graph.add((node, RDF.type, COST.EvidenceArtifact if is_context else COST.ReportingInstrument))
        add_text(graph, node, RDFS.label, row["title"])
        add_text(graph, node, SKOS.definition, row["summary"])
        add_text(graph, node, DCTERMS.type if is_context else COST.instrumentKind, row["category"])
        version = node if is_context else identifier("version", key)
        if not is_context:
            graph.add((version, RDF.type, COST.InstrumentVersion))
            graph.add((version, COST.belongsToInstrument, node))
            graph.add((node, COST.hasVersion, version))
            add_text(graph, version, RDFS.label, f"{row['title']} — {row['version']}")
            add_text(graph, version, COST.verificationScope,
                     "item_mapping" if row["item_level_verified"] else "domain_mapping")
            scope = row["verification_scope"]
            add_text(graph, version, DCTERMS.description,
                     f"Identifier coverage: {scope['mapping_coverage']}; "
                     f"verified mappings: {scope['verified_mapping_count']}; "
                     "no full checklist transcription. " + scope.get("qualification", ""))
        add_text(graph, version, COST.versionLabel, row["version"])
        add_text(graph, version, COST.evidenceStatus, row["status"])
        add_text(graph, version, COST.validationStatus, "editorial_mapping_review_required")
        add_text(graph, version, COST.accessStatus, "source_linked; reuse_terms_must_be_checked")
        add_text(graph, version, COST.citation, row.get("doi") or row["primary_url"])
        graph.add((version, COST.sourceURL, URIRef(row["primary_url"])))
        graph.add((version, DCTERMS.date, Literal(row["checked_on"], datatype=XSD.date)))
        for domain in row["domains"]:
            if domain not in domain_ids:
                raise ValueError(f"unknown domain on {key}: {domain}")
            graph.add((version, COST.coversDomain, identifier("domain", domain)))
        for relation, predicate in (("supersedes", DCTERMS.replaces), ("extends", DCTERMS.requires)):
            for target in row.get(relation, []):
                if target not in instruments:
                    raise ValueError(f"unknown source relation: {target}")
                graph.add((version, predicate, identifier("version", target)))

    for row in mappings["mappings"]:
        key = f"{row['instrument_id']}-{row['item_id']}"
        node = identifier("requirement", key)
        version = identifier("version", row["instrument_id"])
        graph.add((node, RDF.type, COST.ReportingRequirement))
        graph.add((node, COST.belongsToVersion, version))
        graph.add((version, COST.hasRequirement, node))
        add_text(graph, node, RDFS.label, row["topic"])
        add_text(graph, node, COST.itemIdentifier, row["item_id"])
        add_text(graph, node, COST.requirementText, row["topic"])
        add_text(graph, node, RDFS.comment, "Original topic paraphrase; consult the source for full wording and applicability.")
        add_text(graph, node, DCTERMS.description, row["source_locator"])
        graph.add((node, COST.sourceURL, URIRef(row.get("source_url") or instruments[row["instrument_id"]]["primary_url"])))
        for domain in row["domain_ids"]:
            mapping = identifier("mapping", f"{key}-{domain}")
            graph.add((mapping, RDF.type, COST.RequirementMapping))
            graph.add((mapping, COST.sourceRequirement, node))
            graph.add((mapping, COST.mappedConcept, identifier("domain", domain)))
            add_text(graph, mapping, COST.mappingRelation, row["relation"])
            add_text(graph, mapping, COST.mappingRationale,
                     "Editorial topic association from the identified source item; "
                     "does not assert equivalence, complete wording or automatic compliance.")
            add_text(graph, mapping, COST.validationStatus, "editorial_mapping_review_required")

    for key, (title, selected, note) in PROFILES.items():
        node = identifier("profile", key)
        graph.add((node, RDF.type, COST.ReportingProfile))
        add_text(graph, node, RDFS.label, title)
        add_text(graph, node, SKOS.definition, note)
        add_text(graph, node, COST.authority, "UOGTO project-defined composition; source authorities remain separate")
        add_text(graph, node, COST.validationStatus, "editorial_mapping_review_required")
        for source in selected:
            record = instruments[source]
            if record["category"] in CONTEXT_CATEGORIES or record["status"] in {"legacy", "superseded", "protocol_only_verified"}:
                raise ValueError(f"inactive or contextual source in operational profile: {source}")
            graph.add((node, COST.includesInstrumentVersion, identifier("version", source)))
            for row in mappings["mappings"]:
                if row["instrument_id"] == source:
                    graph.add((node, COST.includesRequirement, identifier("requirement", f"{source}-{row['item_id']}")))

    manifest = {
        "schema_version": "0.1.0",
        "source_repository": SOURCE_REPO,
        "source_commit": source_commit,
        "source_commit_content_verified": False,
        "searched_through": registry["searched_through"],
        "coverage_statement": registry["coverage_statement"],
        "source_records": len(instruments),
        "instrument_versions": len(set(graph.subjects(RDF.type, COST.InstrumentVersion))),
        "context_publications": len(set(graph.subjects(RDF.type, COST.EvidenceArtifact))),
        "domains": len(domain_ids),
        "requirements": len(mapped_keys),
        "requirement_mappings": len(set(graph.subjects(RDF.type, COST.RequirementMapping))),
        "profiles": len(PROFILES),
        "requirement_counts_by_source": dict(sorted(Counter(row["instrument_id"] for row in mappings["mappings"]).items())),
        "mapping_review_status": "editorial_mapping_review_required",
        "complete_checklist_transcriptions": 0,
    }
    return graph, manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--mappings", required=True, type=Path)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    verify_source_files_at_commit([args.registry, args.mappings], args.source_commit)
    graph, manifest = build(json.loads(args.registry.read_text()), json.loads(args.mappings.read_text()), args.source_commit)
    manifest["source_commit_content_verified"] = True
    manifest["input_sha256"] = {
        "registry": hashlib.sha256(args.registry.read_bytes()).hexdigest(),
        "mappings": hashlib.sha256(args.mappings.read_bytes()).hexdigest(),
    }
    output = ROOT / "ontologies/reporting/costing-profiles.ttl"
    output.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=output, format="turtle")
    (ROOT / "validation/costing-reporting-import.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({key: manifest[key] for key in ("source_records", "domains", "requirements", "requirement_mappings", "profiles")}, sort_keys=True))


if __name__ == "__main__":
    main()
