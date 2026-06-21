.PHONY: install build validate test coverage publishing-metadata registry-links manuscript-sources manuscript-check manuscript-build manuscript-pdf manuscript-sourcecheck release-assets conductor all

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

conductor:
	python scripts/conductor.py


manuscript-sourcecheck: manuscript-sources
	python scripts/maintenance/check_manuscript_citations.py
	python scripts/maintenance/build_manuscript_pdf.py
	sourceright validate-csl --json docs/paper/references.csl.json
	sourceright report .sourceright
	sourceright citations docs/paper/manuscript-citations.txt .sourceright
