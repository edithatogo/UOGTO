from pathlib import Path


def test_generate_html_report_uses_stable_file_order():
    source = Path("scripts/maintenance/generate_html_report.py").read_text(encoding="utf-8")

    assert 'ttl_files = sorted(glob.glob("ontologies/**/*.ttl", recursive=True))' in source
    assert 'shacl_files = sorted(glob.glob("shapes/*.ttl"))' in source
    assert 'example_files = sorted(glob.glob("examples/*"))' in source
