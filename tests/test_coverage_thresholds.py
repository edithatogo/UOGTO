import glob
import subprocess
import sys
from pathlib import Path

import pytest
from rdflib import Graph

from scripts.report_coverage import coverage_error

ROOT = Path(__file__).resolve().parents[1]
PREFIXES = """
@prefix cost: <https://w3id.org/uogto/packs/costing-valuation#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix ex: <https://example.org/coverage/> .
"""
IMPORT = """
ex:catalogue a owl:Ontology ;
    owl:imports <https://w3id.org/uogto/packs/costing-valuation> .
"""
INSTANCES = """
ex:domain a cost:ReportingDomain .
ex:instrument a cost:ReportingInstrument .
ex:version a cost:InstrumentVersion .
ex:requirement a cost:ReportingRequirement .
"""


def test_coverage_thresholds():
    ttl_files = glob.glob("ontologies/**/*.ttl", recursive=True)
    assert len(ttl_files) >= 30, f"Expected at least 30 ontology files, found {len(ttl_files)}"
    for ttl in ttl_files:
        g = Graph()
        g.parse(ttl, format="turtle")
        assert coverage_error(ttl, g) is None, ttl


def run_coverage(tmp_path: Path, relative_path: str, turtle: str):
    path = tmp_path / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(turtle, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts/report_coverage.py")],
        cwd=tmp_path, capture_output=True, text=True, timeout=30,
    )


def test_coverage_command_accepts_real_instance_catalogue(tmp_path) -> None:
    catalogue = ROOT / "ontologies/reporting/costing-profiles.ttl"
    result = run_coverage(tmp_path, "ontologies/reporting/costing-profiles.ttl",
                          catalogue.read_text(encoding="utf-8"))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Classes: 0" in result.stdout
    assert "All modules are populated" in result.stdout


@pytest.mark.parametrize(
    ("relative_path", "turtle", "message"),
    [
        ("ontologies/reporting/blank.ttl", "", "must identify and import its schema"),
        ("ontologies/reporting/no-import.ttl", PREFIXES + INSTANCES,
         "must identify and import its schema"),
        ("ontologies/reporting/metadata-only.ttl", PREFIXES + IMPORT,
         "ReportingDomain"),
        ("ontologies/reporting/no-requirements.ttl",
         PREFIXES + IMPORT + INSTANCES.replace("ex:requirement a cost:ReportingRequirement .", ""),
         "ReportingRequirement"),
        ("ontologies/core/blank.ttl", "", "is completely empty"),
        ("ontologies/alignments/blank.ttl", "", "is completely empty"),
    ],
)
def test_coverage_command_rejects_empty_or_incomplete_modules(
    tmp_path, relative_path, turtle, message
) -> None:
    result = run_coverage(tmp_path, relative_path, turtle)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "FAIL:" in result.stdout
    assert message in result.stdout

