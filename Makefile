.PHONY: install build validate test coverage publishing-metadata registry-links manuscript-sources release-assets conductor all

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

release-assets: build
	python scripts/maintenance/package_release_assets.py

conductor:
	python scripts/conductor.py
