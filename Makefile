.PHONY: install build validate test coverage publishing-metadata conductor all

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

conductor:
	python scripts/conductor.py
