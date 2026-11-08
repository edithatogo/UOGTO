"""Check source identity, maturity boundaries and profile graph integrity."""

import json
import re
import subprocess
from pathlib import Path

import pytest
from pyshacl import validate
from rdflib import DCTERMS, OWL, RDF, Literal, URIRef

from scripts.maintenance.import_costing_profiles import (
    CAT, COST, build, identifier, verify_source_files_at_commit,
)

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def profiles():
    from rdflib import Graph

    return Graph().parse(ROOT / "ontologies/reporting/costing-profiles.ttl")


def test_reporting_snapshot_conforms_to_pack(profiles):
    from rdflib import Graph

    ontology = Graph().parse(ROOT / "ontologies/applied/costing-valuation.ttl")
    shapes = Graph().parse(ROOT / "shapes/costing-valuation.shacl.ttl")
    conforms, _, report = validate(profiles, shacl_graph=shapes, ont_graph=ontology, inference="rdfs")
    assert conforms, report


def test_exact_catalogue_provenance_and_counts(profiles):
    manifest = json.loads((ROOT / "validation/costing-reporting-import.json").read_text())
    assert re.fullmatch(r"[0-9a-f]{40}", manifest["source_commit"])
    assert manifest["source_commit_content_verified"] is True
    assert all(re.fullmatch(r"[0-9a-f]{64}", value) for value in manifest["input_sha256"].values())
    for field, type_iri in {
        "instrument_versions": COST.InstrumentVersion,
        "context_publications": COST.EvidenceArtifact,
        "domains": COST.ReportingDomain,
        "requirements": COST.ReportingRequirement,
        "requirement_mappings": COST.RequirementMapping,
        "profiles": COST.ReportingProfile,
    }.items():
        assert len(set(profiles.subjects(RDF.type, type_iri))) == manifest[field]
    assert manifest["complete_checklist_transcriptions"] == 0
    assert not list(profiles.subjects(COST.verificationScope, Literal("full_checklist")))
    sources = list(profiles.objects(URIRef(str(CAT).rstrip("/")), DCTERMS.source))
    assert sources == [URIRef(f"{manifest['source_repository']}/tree/{manifest['source_commit']}/reconciliations/costing")]


def test_default_profiles_exclude_protocols_and_superseded_sources(profiles):
    for selected in profiles.objects(None, COST.includesInstrumentVersion):
        assert (selected, RDF.type, COST.InstrumentVersion) in profiles
        assert str(profiles.value(selected, COST.evidenceStatus)) not in {
            "legacy", "superseded", "protocol_only_verified"
        }
    protocol = identifier("source", "microcosting_protocol_2016")
    climate = identifier("source", "cheers_climate_protocol_2025")
    assert (protocol, RDF.type, COST.EvidenceArtifact) in profiles
    assert (climate, RDF.type, COST.EvidenceArtifact) in profiles
    assert (protocol, RDF.type, COST.ReportingInstrument) not in profiles
    assert (climate, RDF.type, COST.ReportingInstrument) not in profiles


def test_newborn_profile_preserves_diagnostic_source_items(profiles):
    newborn = identifier("profile", "newborn-screening")
    for item in ("3.3", "3.4", "3.5", "3.7"):
        requirement = identifier("requirement", f"agreedt_2018-{item}")
        assert (newborn, COST.includesRequirement, requirement) in profiles
        assert profiles.value(requirement, COST.itemIdentifier) == Literal(item)
        assert profiles.value(requirement, COST.belongsToVersion) == identifier("version", "agreedt_2018")
    assert not list(profiles.triples((None, OWL.sameAs, None)))
    assert not list(profiles.triples((None, OWL.equivalentClass, None)))


def test_partial_catalogue_keeps_explicit_item_scope(profiles):
    assert profiles.value(identifier("version", "ghcc_2017"), COST.verificationScope) == Literal("item_mapping")
    assert profiles.value(identifier("version", "tdabc_2020"), COST.verificationScope) == Literal("domain_mapping")
    assert not list(profiles.objects(identifier("version", "tdabc_2020"), COST.hasRequirement))
    for mapping in profiles.subjects(RDF.type, COST.RequirementMapping):
        assert profiles.value(mapping, COST.sourceRequirement) is not None
        assert profiles.value(mapping, COST.mappedConcept) is not None
        assert profiles.value(mapping, COST.validationStatus) == Literal("editorial_mapping_review_required")


@pytest.mark.parametrize("category, verified", [("development_protocol", True), ("reporting_guideline", False)])
def test_importer_rejects_protocol_or_unverified_item_promotion(category, verified):
    registry = {
        "instruments": [{"id": "test", "category": category, "item_level_verified": verified}],
        "domains": [{"id": "resource_measurement"}],
    }
    mappings = {"mappings": [{
        "instrument_id": "test", "item_id": "1", "item_identifier_verified": verified,
        "domain_ids": ["resource_measurement"],
    }]}
    with pytest.raises(ValueError, match="context publication|unverified item"):
        build(registry, mappings, "a" * 40)


def test_importer_rejects_catalogue_mismatched_to_real_commit(tmp_path):
    def git(*arguments):
        return subprocess.check_output(["git", "-C", str(tmp_path), *arguments], text=True)

    git("init", "-q")
    source = tmp_path / "catalogue.json"
    source.write_text('{"version": 1}\n')
    git("add", "catalogue.json")
    git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture")
    commit = git("rev-parse", "HEAD").strip()
    verify_source_files_at_commit([source], commit)
    source.write_text('{"version": 2}\n')
    with pytest.raises(ValueError, match="differs from claimed commit"):
        verify_source_files_at_commit([source], commit)
