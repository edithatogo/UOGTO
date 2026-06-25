.PHONY: install build validate test coverage publishing-metadata registry-links registry-packet extended-registry-packet ontology-comparison-inventory ontology-comparison-harvest ontology-comparison-terms ontology-comparison-mappings ontology-comparison-alignments ontology-comparison-sssom ontology-comparison-overlap ontology-comparison-networks ontology-comparison-visuals ontology-comparison-check ontology-comparison-all article-hardening-protocol article-hardening-inventory article-hardening-quality article-hardening-robot article-hardening-figures article-facing-tables zenodo-packet zenodo-depositions w3id-packet publication-status w3id-status doi-status record-doi manuscript-sources manuscript-check manuscript-build manuscript-pdf manuscript-sourcecheck arxiv-source-package arxiv-source-clean arxiv-preflight release-assets release-preflight conductor all

all: build validate test coverage

install:
	pip install -e .

build:
	python scripts/build.py

validate:
	python scripts/validate.py

test:
	pytest

coverage:
	python scripts/report_coverage.py

publishing-metadata:
	python scripts/maintenance/check_publishing_metadata.py

registry-links:
	python scripts/maintenance/check_registry_links.py

registry-packet:
	python scripts/maintenance/build_registry_handoff.py

extended-registry-packet:
	python scripts/maintenance/build_extended_registry_handoff.py

ontology-comparison-inventory:
	python scripts/maintenance/build_ontology_comparison_inventory.py

ontology-comparison-harvest:
	python scripts/maintenance/harvest_comparison_sources.py

ontology-comparison-terms:
	python scripts/maintenance/extract_comparison_terms.py

ontology-comparison-mappings:
	python scripts/maintenance/generate_ontology_mapping_candidates.py

ontology-comparison-alignments:
	python scripts/maintenance/build_comparison_alignments.py

ontology-comparison-sssom: ontology-comparison-alignments

ontology-comparison-overlap:
	python scripts/maintenance/analyse_ontology_overlap.py

ontology-comparison-networks:
	python scripts/maintenance/analyse_ontology_networks.py

ontology-comparison-visuals:
	python scripts/maintenance/visualise_ontology_comparison.py

ontology-comparison-check:
	python scripts/maintenance/check_ontology_comparison_artifacts.py

ontology-comparison-all: ontology-comparison-inventory ontology-comparison-harvest ontology-comparison-terms ontology-comparison-mappings ontology-comparison-alignments ontology-comparison-sssom ontology-comparison-overlap ontology-comparison-networks ontology-comparison-visuals ontology-comparison-check

article-hardening-protocol:
	python scripts/maintenance/check_article_hardening_protocol.py

article-hardening-inventory:
	python scripts/maintenance/build_article_hardening_inventory.py

article-hardening-quality:
	python scripts/maintenance/build_article_hardening_quality.py

article-hardening-robot:
	python scripts/maintenance/build_article_hardening_robot_reports.py

article-hardening-figures:
	python scripts/maintenance/render_article_hardening_figures.py

zenodo-packet:
	python scripts/maintenance/build_zenodo_handoff.py

zenodo-depositions:
	python scripts/maintenance/check_zenodo_depositions.py

w3id-packet:
	python scripts/maintenance/build_w3id_redirect_handoff.py

publication-status:
	python scripts/maintenance/build_publication_status.py

publication-status-live:
	python scripts/maintenance/build_publication_status.py --live --output dist/publication-status-live.json

w3id-status:
	python scripts/maintenance/check_w3id_status.py

doi-status:
	python scripts/maintenance/check_doi_status.py

record-doi:
	python scripts/maintenance/record_zenodo_doi.py "$(DOI)"

manuscript-sources:
	python scripts/maintenance/build_manuscript_sources.py

manuscript-check:
	python scripts/maintenance/check_manuscript_citations.py

manuscript-build: manuscript-check
	python scripts/maintenance/build_manuscript_pdf.py

manuscript-pdf: manuscript-check
	python scripts/maintenance/build_manuscript_pdf.py --require-pdf

release-assets: build
	python scripts/maintenance/package_release_assets.py

release-preflight: release-assets registry-packet extended-registry-packet zenodo-packet w3id-packet publication-status
	python scripts/maintenance/check_release_readiness.py

conductor:
	python scripts/conductor.py

manuscript-sourcecheck: manuscript-sources
	python scripts/maintenance/check_manuscript_citations.py
	python scripts/maintenance/build_manuscript_pdf.py
	sourceright validate-csl --json docs/paper/references.csl.json
	sourceright report .sourceright
	sourceright citations docs/paper/manuscript-citations.txt .sourceright

arxiv-source-package: manuscript-sources
	python scripts/maintenance/build_arxiv_source_package.py

arxiv-source-clean: arxiv-source-package
	python scripts/maintenance/clean_arxiv_source_package.py

arxiv-preflight: manuscript-sources
	python scripts/maintenance/check_manuscript_citations.py
	python scripts/maintenance/build_manuscript_pdf.py --require-pdf
	python scripts/maintenance/build_arxiv_source_package.py
	python scripts/maintenance/clean_arxiv_source_package.py
	python scripts/maintenance/audit_arxiv_source_privacy.py
	sourceright validate-csl --json docs/paper/references.csl.json
	sourceright report .sourceright
	sourceright citations docs/paper/manuscript-citations.txt .sourceright
article-facing-tables:
	python scripts/maintenance/build_article_evidence_tables.py

.PHONY: arxiv-privacy-audit
arxiv-privacy-audit: arxiv-source-package
	python scripts/maintenance/audit_arxiv_source_privacy.py
