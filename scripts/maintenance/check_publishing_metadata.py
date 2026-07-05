import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS


ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_URL = "https://github.com/edithatogo/UOGTO"
CORE_NAMESPACE = "https://w3id.org/uogto/core#"
CC_BY_4 = "https://creativecommons.org/licenses/by/4.0/"
AUTHOR_ORCID = "0000-0002-9775-0603"
AUTHOR_ORCID_URL = f"https://orcid.org/{AUTHOR_ORCID}"
PRIMARY_ONTOLOGY_URI = URIRef("https://w3id.org/uogto/core")
DCTERMS = Namespace("http://purl.org/dc/terms/")
VANN = Namespace("http://purl.org/vocab/vann/")


REQUIRED_FILES = [
    "CITATION.cff",
    ".zenodo.json",
    "docs/releases/v1.0.md",
    "docs/widoco/widoco.properties",
    "docs/widoco/README.md",
    "docs/registry/metadata-checklist.md",
    "docs/registry/lov-submission.md",
    "docs/registry/ols-indexing.md",
    "docs/registry/extended-discoverability-submissions.md",
    "docs/registry/w3id-submission.md",
    ".github/workflows/widoco-pages.yml",
]

CITATION_SCHEMA = {
    "type": "object",
    "required": [
        "cff-version",
        "message",
        "authors",
        "title",
        "version",
        "date-released",
        "url",
        "repository-code",
        "license",
        "keywords",
        "abstract",
    ],
    "properties": {
        "cff-version": {"const": "1.2.0"},
        "message": {"type": "string", "minLength": 1},
        "authors": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "anyOf": [
                    {"required": ["name"]},
                    {"required": ["family-names"]},
                ],
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "family-names": {"type": "string", "minLength": 1},
                    "given-names": {"type": "string", "minLength": 1},
                    "orcid": {"type": "string", "pattern": "^https://orcid.org/[0-9X-]+$"},
                },
            },
        },
        "title": {"type": "string", "minLength": 1},
        "version": {"type": "string", "minLength": 1},
        "date-released": {"type": "string", "format": "date"},
        "url": {"type": "string", "format": "uri", "pattern": "^https?://"},
        "repository-code": {"type": "string", "format": "uri", "pattern": "^https?://"},
        "license": {"const": "CC-BY-4.0"},
        "keywords": {
            "type": "array",
            "minItems": 3,
            "items": {"type": "string", "minLength": 1},
        },
        "abstract": {"type": "string", "minLength": 1},
    },
}

ZENODO_SCHEMA = {
    "type": "object",
    "required": [
        "title",
        "upload_type",
        "description",
        "creators",
        "license",
        "keywords",
        "related_identifiers",
        "version",
        "language",
        "access_right",
    ],
    "properties": {
        "title": {"type": "string", "minLength": 1},
        "upload_type": {"enum": ["dataset", "software"]},
        "description": {"type": "string", "minLength": 1},
        "creators": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["name"],
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "orcid": {
                        "type": "string",
                        "pattern": "^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9X]{4}$",
                    },
                },
            },
        },
        "license": {"const": "cc-by-4.0"},
        "keywords": {
            "type": "array",
            "minItems": 3,
            "items": {"type": "string", "minLength": 1},
        },
        "related_identifiers": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["identifier", "relation", "resource_type", "scheme"],
                "properties": {
                    "identifier": {"type": "string", "minLength": 1},
                    "relation": {"type": "string", "minLength": 1},
                    "resource_type": {"type": "string", "minLength": 1},
                    "scheme": {"type": "string", "minLength": 1},
                },
            },
        },
        "version": {"type": "string", "minLength": 1},
        "language": {"const": "eng"},
        "access_right": {"const": "open"},
    },
}


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate_with_schema(instance, schema, name):
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda err: err.path)
    if errors:
        details = "; ".join(
            f"{'.'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
            for error in errors
        )
        raise AssertionError(f"{name} schema validation failed: {details}")


def validate_citation_schema(citation):
    normalized = dict(citation)
    if hasattr(normalized.get("date-released"), "isoformat"):
        normalized["date-released"] = normalized["date-released"].isoformat()
    validate_with_schema(normalized, CITATION_SCHEMA, "CITATION.cff")


def validate_zenodo_schema(zenodo):
    validate_with_schema(zenodo, ZENODO_SCHEMA, ".zenodo.json")


def check_required_files():
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        raise AssertionError(f"Missing publishing metadata files: {', '.join(missing)}")


def check_citation():
    citation = load_yaml(ROOT / "CITATION.cff")
    validate_citation_schema(citation)
    if citation["title"] != "Universal Open Game Theory Ontology (UOGTO)":
        raise AssertionError("CITATION.cff title does not match release title")
    if citation["version"] != "1.0.0":
        raise AssertionError("CITATION.cff version must match v1.0.0 release metadata")
    if citation["url"] != REPOSITORY_URL or citation["repository-code"] != REPOSITORY_URL:
        raise AssertionError("CITATION.cff repository URLs must point to edithatogo/UOGTO")
    if not any(author.get("orcid") == AUTHOR_ORCID_URL for author in citation["authors"]):
        raise AssertionError("CITATION.cff must publish the approved author ORCID")


def check_zenodo():
    with (ROOT / ".zenodo.json").open("r", encoding="utf-8") as handle:
        zenodo = json.load(handle)
    validate_zenodo_schema(zenodo)
    if zenodo["title"] != "Universal Open Game Theory Ontology (UOGTO)":
        raise AssertionError(".zenodo.json title does not match release title")
    if zenodo["version"] != "1.0.0":
        raise AssertionError(".zenodo.json version must match v1.0.0 release metadata")
    if not any(creator.get("orcid") == AUTHOR_ORCID for creator in zenodo["creators"]):
        raise AssertionError(".zenodo.json must publish the approved creator ORCID")
    if not any(item["identifier"] == REPOSITORY_URL for item in zenodo["related_identifiers"]):
        raise AssertionError(".zenodo.json related_identifiers must include the GitHub repository")


def check_workflow():
    workflow = load_yaml(ROOT / ".github/workflows/widoco-pages.yml")
    if workflow["name"] != "Build WIDOCO Pages":
        raise AssertionError("WIDOCO workflow has an unexpected name")
    if "build" not in workflow["jobs"] or "deploy" not in workflow["jobs"]:
        raise AssertionError("WIDOCO workflow must define build and deploy jobs")
    if workflow.get("env", {}).get("WIDOCO_VERSION") != "v1.4.25":
        raise AssertionError("WIDOCO workflow must pin WIDOCO_VERSION to v1.4.25")
    workflow_text = (ROOT / ".github/workflows/widoco-pages.yml").read_text(encoding="utf-8")
    for expected in [
        "make validate",
        "make test",
        "audit_semantics.py",
        "make publishing-metadata",
        "make build",
        "WIDOCO_JAR_URL",
        "WIDOCO_JAR_SHA256",
        "hashlib.sha256",
        "actions/deploy-pages@v5",
        "dist/uogto.ttl",
    ]:
        if expected not in workflow_text:
            raise AssertionError(f"WIDOCO workflow missing expected gate or command: {expected}")


def check_registry_annotations():
    ttl_files = sorted((ROOT / "ontologies").glob("**/*.ttl"))
    if not ttl_files:
        raise AssertionError("No ontology Turtle files found under ontologies/")

    graph = Graph()
    module_headers = []
    for ttl_file in ttl_files:
        module_graph = Graph()
        module_graph.parse(ttl_file, format="turtle")
        graph += module_graph
        module_headers.extend(module_graph.subjects(RDF.type, OWL.Ontology))

    if PRIMARY_ONTOLOGY_URI not in module_headers:
        raise AssertionError("Primary UOGTO ontology header is missing from source modules")

    required_primary_values = {
        DCTERMS.title: Literal("Universal Open Game Theory Ontology (UOGTO)", lang="en"),
        DCTERMS.creator: Literal("UOGTO Contributors"),
        DCTERMS.license: URIRef(CC_BY_4),
        OWL.versionInfo: Literal("1.0.0"),
        VANN.preferredNamespacePrefix: Literal("uogto"),
        VANN.preferredNamespaceUri: Literal(CORE_NAMESPACE),
    }
    for predicate, expected_value in required_primary_values.items():
        if (PRIMARY_ONTOLOGY_URI, predicate, expected_value) not in graph:
            raise AssertionError(
                f"Primary ontology header missing expected {predicate.n3(graph.namespace_manager)} value"
            )

    for predicate in [RDFS.label, SKOS.definition, DCTERMS.description]:
        if not list(graph.objects(PRIMARY_ONTOLOGY_URI, predicate)):
            raise AssertionError(f"Primary ontology header missing {predicate.n3(graph.namespace_manager)}")

    unlabeled = sorted(
        str(subject)
        for subject in set(module_headers)
        if not list(graph.objects(subject, RDFS.label))
    )
    if unlabeled:
        raise AssertionError(f"Ontology module headers missing rdfs:label: {', '.join(unlabeled)}")


def check_registry_docs():
    metadata = (ROOT / "docs/registry/metadata-checklist.md").read_text(encoding="utf-8")
    lov = (ROOT / "docs/registry/lov-submission.md").read_text(encoding="utf-8")
    ols = (ROOT / "docs/registry/ols-indexing.md").read_text(encoding="utf-8")
    w3id = (ROOT / "docs/registry/w3id-submission.md").read_text(encoding="utf-8")
    extended = (ROOT / "docs/registry/extended-discoverability-submissions.md").read_text(encoding="utf-8")
    release = (ROOT / "docs/releases/v1.0.md").read_text(encoding="utf-8")
    for expected in [
        REPOSITORY_URL,
        CORE_NAMESPACE,
        CC_BY_4,
        "https://doi.org/10.5281/zenodo.20796937",
        "https://github.com/pyvandenbussche/lov/issues/83",
        "https://github.com/EBISPOT/ols4/issues/1305",
        "https://github.com/biopragmatics/bioregistry/issues/1999",
        "http://prefix.cc/uogto.file.txt",
        "http://prefix.cc/uogtox.file.txt",
        "https://github.com/OntoZoo/ontobee/issues/212",
        "https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4778481220",
    ]:
        if expected not in metadata + lov + ols + w3id + extended + release:
            raise AssertionError(f"Registry documentation missing expected text: {expected}")


def main():
    check_required_files()
    check_citation()
    check_zenodo()
    check_workflow()
    check_registry_annotations()
    check_registry_docs()
    print("Publishing metadata checks passed.")


if __name__ == "__main__":
    main()
