PYTHON ?= $(firstword $(wildcard .pixi/envs/default/python.exe .pixi/envs/default/bin/python) python)
ARXIV_PDF_FLAGS ?= --require-pdf
ARXIV_PDF_OUTPUT_DIR ?= .tmp/manuscript-build-arxiv

.PHONY: install build validate test coverage publishing-metadata registry-links registry-packet extended-registry-packet ontology-comparison-inventory ontology-comparison-harvest ontology-comparison-terms ontology-comparison-mappings ontology-comparison-alignments ontology-comparison-sssom ontology-comparison-overlap ontology-comparison-networks ontology-comparison-visuals ontology-comparison-check ontology-comparison-all article-hardening-protocol article-hardening-inventory article-hardening-source-acquisition article-hardening-quality article-hardening-robot article-hardening-figures article-hardening-tabular article-hardening-duckdb article-hardening-dashboard article-hardening-all article-facing-tables candidate-decision-ledger ontology-snapshot-supplement figure-caption-freeze zenodo-packet zenodo-depositions w3id-packet publication-status w3id-status doi-status record-doi manuscript-sources manuscript-check manuscript-build manuscript-pdf manuscript-sourcecheck arxiv-source-package arxiv-source-clean arxiv-preflight arxiv-preflight-strict arxiv-upload-ready arxiv-upload-ready-strict arxiv-strict-review required-gate release-assets release-preflight conductor all

all: build validate test coverage

install:
	pip install -e .

build:
	$(PYTHON) scripts/build.py

validate:
	$(PYTHON) scripts/validate.py

test:
	$(PYTHON) -m pytest $(PYTEST_ARGS)

coverage:
	$(PYTHON) scripts/report_coverage.py

publishing-metadata:
	$(PYTHON) scripts/maintenance/check_publishing_metadata.py

registry-links:
	$(PYTHON) scripts/maintenance/check_registry_links.py

registry-packet:
	$(PYTHON) scripts/maintenance/build_registry_handoff.py

extended-registry-packet:
	$(PYTHON) scripts/maintenance/build_extended_registry_handoff.py

ontology-comparison-inventory:
	$(PYTHON) scripts/maintenance/build_ontology_comparison_inventory.py

ontology-comparison-harvest:
	$(PYTHON) scripts/maintenance/harvest_comparison_sources.py

ontology-comparison-terms:
	$(PYTHON) scripts/maintenance/extract_comparison_terms.py

ontology-comparison-mappings:
	$(PYTHON) scripts/maintenance/generate_ontology_mapping_candidates.py

ontology-comparison-alignments:
	$(PYTHON) scripts/maintenance/build_comparison_alignments.py

ontology-comparison-sssom: ontology-comparison-alignments

ontology-comparison-overlap:
	$(PYTHON) scripts/maintenance/analyse_ontology_overlap.py

ontology-comparison-networks:
	$(PYTHON) scripts/maintenance/analyse_ontology_networks.py

ontology-comparison-visuals:
	$(PYTHON) scripts/maintenance/visualise_ontology_comparison.py

ontology-comparison-check:
	$(PYTHON) scripts/maintenance/check_ontology_comparison_artifacts.py

ontology-comparison-all: ontology-comparison-inventory ontology-comparison-harvest ontology-comparison-terms ontology-comparison-mappings ontology-comparison-alignments ontology-comparison-sssom ontology-comparison-overlap ontology-comparison-networks ontology-comparison-visuals ontology-comparison-check

article-hardening-protocol:
	$(PYTHON) scripts/maintenance/check_article_hardening_protocol.py

article-hardening-inventory:
	$(PYTHON) scripts/maintenance/build_article_hardening_inventory.py

article-hardening-source-acquisition:
	$(PYTHON) scripts/maintenance/build_article_source_acquisition_manifest.py

article-hardening-quality:
	$(PYTHON) scripts/maintenance/build_article_hardening_quality.py

article-hardening-robot:
	$(PYTHON) scripts/maintenance/build_article_hardening_robot_reports.py

article-hardening-figures:
	$(PYTHON) scripts/maintenance/render_article_hardening_figures.py

article-hardening-tabular:
	$(PYTHON) scripts/maintenance/export_tabular_artifacts.py
	$(PYTHON) scripts/maintenance/build_article_evidence_tables.py
	$(PYTHON) scripts/maintenance/build_candidate_decision_ledger.py

article-hardening-duckdb:
	$(PYTHON) scripts/maintenance/build_article_hardening_duckdb.py

article-hardening-dashboard: article-hardening-duckdb article-hardening-tabular article-hardening-figures
	$(PYTHON) scripts/maintenance/build_article_evidence_dashboard.py

article-hardening-all: article-hardening-inventory article-hardening-source-acquisition article-hardening-quality article-hardening-robot article-hardening-tabular article-hardening-figures article-hardening-dashboard article-hardening-protocol

zenodo-packet:
	$(PYTHON) scripts/maintenance/build_zenodo_handoff.py

zenodo-depositions:
	$(PYTHON) scripts/maintenance/check_zenodo_depositions.py

w3id-packet:
	$(PYTHON) scripts/maintenance/build_w3id_redirect_handoff.py

publication-status:
	$(PYTHON) scripts/maintenance/build_publication_status.py

publication-status-live:
	$(PYTHON) scripts/maintenance/build_publication_status.py --live --output dist/publication-status-live.json

w3id-status:
	$(PYTHON) scripts/maintenance/check_w3id_status.py

doi-status:
	$(PYTHON) scripts/maintenance/check_doi_status.py

record-doi:
	$(PYTHON) scripts/maintenance/record_zenodo_doi.py "$(DOI)"

manuscript-sources:
	$(PYTHON) scripts/maintenance/build_manuscript_sources.py

manuscript-check:
	$(PYTHON) scripts/maintenance/check_manuscript_citations.py

manuscript-build: manuscript-check
	$(PYTHON) scripts/maintenance/build_manuscript_pdf.py

manuscript-pdf: manuscript-check
	$(PYTHON) scripts/maintenance/build_manuscript_pdf.py --require-pdf

release-assets: build
	$(PYTHON) scripts/maintenance/package_release_assets.py

release-preflight: release-assets registry-packet extended-registry-packet zenodo-packet w3id-packet publication-status
	$(PYTHON) scripts/maintenance/check_release_readiness.py

conductor:
	$(PYTHON) scripts/conductor.py

manuscript-sourcecheck: manuscript-sources
	$(PYTHON) scripts/maintenance/check_manuscript_citations.py
	$(PYTHON) scripts/maintenance/build_manuscript_pdf.py
	sourceright validate-csl --json docs/paper/references.csl.json
	sourceright report .sourceright
	sourceright citations docs/paper/manuscript-citations.txt .sourceright

arxiv-source-package: manuscript-sources
	$(PYTHON) scripts/maintenance/build_arxiv_source_package.py

arxiv-source-clean: arxiv-source-package
	$(PYTHON) scripts/maintenance/clean_arxiv_source_package.py

arxiv-preflight: manuscript-sources
	$(PYTHON) scripts/maintenance/check_manuscript_citations.py
	$(PYTHON) scripts/maintenance/build_manuscript_pdf.py --output-dir $(ARXIV_PDF_OUTPUT_DIR) $(ARXIV_PDF_FLAGS)
	$(PYTHON) scripts/maintenance/build_arxiv_source_package.py
	$(PYTHON) scripts/maintenance/clean_arxiv_source_package.py
	$(PYTHON) scripts/maintenance/audit_arxiv_source_privacy.py
	sourceright validate-csl --json docs/paper/references.csl.json
	sourceright report .sourceright
	sourceright citations docs/paper/manuscript-citations.txt .sourceright

arxiv-upload-ready: arxiv-preflight
	$(PYTHON) scripts/maintenance/build_arxiv_upload_ready.py --require-privacy-audit

arxiv-preflight-strict:
	$(MAKE) arxiv-preflight ARXIV_PDF_FLAGS="--require-pdf --require-arxiv-engine"

arxiv-upload-ready-strict:
	$(MAKE) arxiv-upload-ready ARXIV_PDF_FLAGS="--require-pdf --require-arxiv-engine"

arxiv-strict-review:
	$(PYTHON) scripts/maintenance/score_arxiv_submission.py --threshold 995

required-gate: validate test publishing-metadata registry-links manuscript-pdf arxiv-upload-ready arxiv-strict-review
article-facing-tables:
	$(PYTHON) scripts/maintenance/build_article_evidence_tables.py

candidate-decision-ledger:
	$(PYTHON) scripts/maintenance/build_candidate_decision_ledger.py

ontology-snapshot-supplement: release-assets
	$(PYTHON) scripts/maintenance/build_ontology_snapshot_supplement.py

figure-caption-freeze:
	$(PYTHON) scripts/maintenance/build_figure_caption_freeze.py

.PHONY: arxiv-privacy-audit
arxiv-privacy-audit: arxiv-source-package
	$(PYTHON) scripts/maintenance/audit_arxiv_source_privacy.py
