from pathlib import Path

import yaml


def test_public_issue_templates_cover_external_contribution_paths() -> None:
    template_dir = Path(".github/ISSUE_TEMPLATE")
    expected = {
        "ontology-change-proposal.yml": "ontology-change",
        "validation-failure.yml": "validation",
        "documentation-fix.yml": "documentation",
        "bug-report.yml": "bug",
        "question.yml": "question",
    }
    for filename, label in expected.items():
        data = yaml.safe_load((template_dir / filename).read_text(encoding="utf-8"))
        assert data["name"]
        assert label in data["labels"]
        assert data["body"]


def test_pull_request_template_requires_ontology_and_submission_checks() -> None:
    template = Path(".github/pull_request_template.md").read_text(encoding="utf-8")
    for expected in [
        "Ontology Contract",
        "SHACL shapes cover any changed validation invariants",
        "Competency queries cover changed retrieval behavior",
        "make arxiv-upload-ready",
        "GitHub Actions `Required Gate`",
        "RI-HERO impact",
    ]:
        assert expected in template


def test_reuse_metadata_preserves_dual_license_split() -> None:
    dep5 = Path(".reuse/dep5").read_text(encoding="utf-8")
    for expected in [
        "License: CC-BY-4.0",
        "License: MIT",
        "Files: ontologies/* shapes/* jsonld/* examples/* competency-questions/* docs/* conductor/*",
        "Files: scripts/* tests/* pyproject.toml pixi.toml pixi.lock Makefile .github/*",
    ]:
        assert expected in dep5


def test_workflows_target_main_not_master_for_active_pushes() -> None:
    for workflow in [
        ".github/workflows/validate.yml",
        ".github/workflows/manuscript-pdf.yml",
        ".github/workflows/widoco-pages.yml",
    ]:
        text = Path(workflow).read_text(encoding="utf-8")
        assert "branches: [ main ]" in text
        assert "branches: [ main, master ]" not in text
        assert "branches: [ master ]" not in text
