.PHONY: install build validate test coverage conductor all

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

conductor:
	python scripts/conductor.py
