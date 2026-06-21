import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_URL = "https://github.com/edithatogo/UOGTO"
CORE_NAMESPACE = "https://w3id.org/uogto/core#"
CC_BY_4 = "https://creativecommons.org/licenses/by/4.0/"


REQUIRED_FILES = [
    "CITATION.cff",
    ".zenodo.json",
    "docs/releases/v1.0.md",
    "docs/widoco/widoco.properties",
    "docs/widoco/README.md",
    "docs/registry/metadata-checklist.md",
    "docs/registry/lov-submission.md",
    "docs/registry/ols-indexing.md",
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
        "url": {"type": "string", "format": "uri"},
        "repository-code": {"type": "string", "format": "uri"},
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
                "properties": {"name": {"type": "string", "minLength": 1}},
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
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda err: err.path)
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


def check_zenodo():
    with (ROOT / ".zenodo.json").open("r", encoding="utf-8") as handle:
        zenodo = json.load(handle)
    validate_zenodo_schema(zenodo)
    if zenodo["title"] != "Universal Open Game Theory Ontology (UOGTO)":
        raise AssertionError(".zenodo.json title does not match release title")
    if zenodo["version"] != "1.0.0":
        raise AssertionError(".zenodo.json version must match v1.0.0 release metadata")
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
        "releases/tags/{version}",
        "actions/deploy-pages@v4",
        "dist/uogto.ttl",
    ]:
        if expected not in workflow_text:
            raise AssertionError(f"WIDOCO workflow missing expected gate or command: {expected}")


def check_registry_docs():
    metadata = (ROOT / "docs/registry/metadata-checklist.md").read_text(encoding="utf-8")
    lov = (ROOT / "docs/registry/lov-submission.md").read_text(encoding="utf-8")
    ols = (ROOT / "docs/registry/ols-indexing.md").read_text(encoding="utf-8")
    release = (ROOT / "docs/releases/v1.0.md").read_text(encoding="utf-8")
    for expected in [
        REPOSITORY_URL,
        CORE_NAMESPACE,
        CC_BY_4,
        "TBD after",
    ]:
        if expected not in metadata + lov + ols + release:
            raise AssertionError(f"Registry documentation missing expected text: {expected}")


def main():
    check_required_files()
    check_citation()
    check_zenodo()
    check_workflow()
    check_registry_docs()
    print("Publishing metadata checks passed.")


if __name__ == "__main__":
    main()
