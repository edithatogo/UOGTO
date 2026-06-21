import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


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


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def check_required_files():
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        raise AssertionError(f"Missing publishing metadata files: {', '.join(missing)}")


def check_citation():
    citation = load_yaml(ROOT / "CITATION.cff")
    assert citation["cff-version"] == "1.2.0"
    assert citation["title"] == "Universal Open Game Theory Ontology (UOGTO)"
    assert citation["version"] == "1.0.0"
    assert citation["url"] == "https://github.com/edithatogo/UOGTO"
    assert citation["repository-code"] == "https://github.com/edithatogo/UOGTO"
    assert citation["license"] == "CC-BY-4.0"
    assert citation["authors"]


def check_zenodo():
    with (ROOT / ".zenodo.json").open("r", encoding="utf-8") as handle:
        zenodo = json.load(handle)
    assert zenodo["title"] == "Universal Open Game Theory Ontology (UOGTO)"
    assert zenodo["version"] == "1.0.0"
    assert zenodo["license"] == "cc-by-4.0"
    assert zenodo["upload_type"] == "dataset"
    assert zenodo["creators"]
    assert any(item["identifier"] == "https://github.com/edithatogo/UOGTO" for item in zenodo["related_identifiers"])


def check_workflow():
    workflow = load_yaml(ROOT / ".github/workflows/widoco-pages.yml")
    assert workflow["name"] == "Build WIDOCO Pages"
    assert "build" in workflow["jobs"]
    assert "deploy" in workflow["jobs"]
    workflow_text = (ROOT / ".github/workflows/widoco-pages.yml").read_text(encoding="utf-8")
    for expected in ["make build", "dgarijo/Widoco", "actions/deploy-pages@v4", "dist/uogto.ttl"]:
        assert expected in workflow_text


def check_registry_docs():
    metadata = (ROOT / "docs/registry/metadata-checklist.md").read_text(encoding="utf-8")
    lov = (ROOT / "docs/registry/lov-submission.md").read_text(encoding="utf-8")
    ols = (ROOT / "docs/registry/ols-indexing.md").read_text(encoding="utf-8")
    release = (ROOT / "docs/releases/v1.0.md").read_text(encoding="utf-8")
    for expected in [
        "https://github.com/edithatogo/UOGTO",
        "https://w3id.org/uogto/core#",
        "https://creativecommons.org/licenses/by/4.0/",
        "TBD after",
    ]:
        assert expected in metadata + lov + ols + release


def main():
    check_required_files()
    check_citation()
    check_zenodo()
    check_workflow()
    check_registry_docs()
    print("Publishing metadata checks passed.")


if __name__ == "__main__":
    main()
