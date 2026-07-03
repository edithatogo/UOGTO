from pathlib import Path


def test_arxiv_preflight_workflow_runs_strict_gate() -> None:
    workflow = Path(".github/workflows/arxiv-preflight.yml").read_text(encoding="utf-8")
    for expected in [
        "name: arXiv Preflight",
        "actions/checkout@v7",
        "actions/setup-python@v6",
        "cargo install --git https://github.com/edithatogo/sourceright.git --rev f0c2c7c5dc9c2a25724e11985eb2b906d34c7c17 sourceright --locked",
        "latexmk",
        "texlive-latex-base",
        "pytest tests/test_arxiv_source_package.py tests/test_arxiv_upload_ready.py",
        'make arxiv-preflight ARXIV_PDF_FLAGS="--require-pdf --require-arxiv-engine"',
        'make arxiv-upload-ready ARXIV_PDF_FLAGS="--require-pdf --require-arxiv-engine"',
        "actions/upload-artifact@v4",
        "uogto-arxiv-upload-ready",
        "retention-days: 90",
        "artifact-metadata: write",
        "actions/attest@v4",
        "subject-checksums: dist/arxiv/SHA256SUMS",
        "docs/release-process.md",
        "conductor/agents/arxiv-submission-agents.json",
        "conductor/workflows/arxiv-submission-contract-workflow.md",
        "Makefile",
        "tests/test_arxiv_submission_contract.py",
        "tests/test_manuscript_build.py",
    ]:
        assert expected in workflow


def test_required_gate_pins_sourceright_and_builds_before_tests() -> None:
    workflow = Path(".github/workflows/required-gate.yml").read_text(encoding="utf-8")
    assert "cargo install --git https://github.com/edithatogo/sourceright.git --rev f0c2c7c5dc9c2a25724e11985eb2b906d34c7c17 sourceright --locked" in workflow
    assert "make build\n          make validate\n          make test" in workflow


def test_widoco_pages_verifies_pinned_jar_checksum() -> None:
    workflow = Path(".github/workflows/widoco-pages.yml").read_text(encoding="utf-8")
    assert "WIDOCO_VERSION: v1.4.25" in workflow
    assert "WIDOCO_SHA256: ce3071a90fe73c0860829569e79050f74c9623d6add8be3925cbdf87bedde5a5" in workflow
    assert "actual_sha256 = hashlib.sha256" in workflow
    assert "WIDOCO checksum mismatch" in workflow


def test_makefile_and_pixi_arxiv_tasks_include_upload_ready_gate() -> None:
    makefile = Path("Makefile").read_text(encoding="utf-8")
    pixi = Path("pixi.toml").read_text(encoding="utf-8")
    for expected in [
        "$(PYTHON) scripts/maintenance/audit_arxiv_source_privacy.py",
        "$(PYTHON) scripts/maintenance/build_manuscript_pdf.py --output-dir $(ARXIV_PDF_OUTPUT_DIR) $(ARXIV_PDF_FLAGS)",
        "ARXIV_PDF_OUTPUT_DIR ?= .tmp/manuscript-build-arxiv",
        '$(MAKE) arxiv-upload-ready ARXIV_PDF_FLAGS="--require-pdf --require-arxiv-engine"',
        "arxiv-upload-ready",
        "$(PYTHON) scripts/maintenance/build_arxiv_upload_ready.py --require-privacy-audit",
    ]:
        assert expected in makefile
    for expected in [
        "python scripts/maintenance/audit_arxiv_source_privacy.py",
        "arxiv-preflight-strict",
        "python scripts/maintenance/build_manuscript_pdf.py --output-dir .tmp/manuscript-build-arxiv --require-pdf --require-arxiv-engine",
        "arxiv-upload-ready",
        "arxiv-upload-ready-strict",
        "python scripts/maintenance/build_arxiv_upload_ready.py --require-privacy-audit",
    ]:
        assert expected in pixi
