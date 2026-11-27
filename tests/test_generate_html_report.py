from pathlib import Path


def test_generate_html_report_uses_stable_file_order():
    source = Path("scripts/maintenance/generate_html_report.py").read_text(encoding="utf-8")

    assert 'ttl_files = sorted(glob.glob("ontologies/**/*.ttl", recursive=True))' in source
    assert 'shacl_files = sorted(glob.glob("shapes/*.ttl"))' in source
    assert 'example_files = sorted(glob.glob("examples/*"))' in source

import os
import tempfile
import html
from unittest.mock import patch, MagicMock

def test_generate_html_report_escapes_xss():
    from scripts.maintenance.generate_html_report import generate_html_report

    with patch('scripts.maintenance.generate_html_report.glob.glob') as mock_glob, \
         patch('scripts.maintenance.generate_html_report.shacl_validate') as mock_validate, \
         patch('scripts.maintenance.generate_html_report.Graph.parse') as mock_parse:

        # Since os.path.basename handles '<' character weirdly if it's the start of a "redirect" when run inside bash somehow?
        # Actually it's probably just a normal string here, wait, `glob.glob` mock returns the string.
        # Oh, in `generate_html_report.py`, it doesn't escape before `os.path.basename` but inside.
        def fake_glob(pattern, **kwargs):
            if pattern == "examples/*":
                # Let's use a simple malicious name without `<` just to test escaping
                # wait we want to test HTML escaping so we need `<` and `>`
                # the issue was os.path.basename splits on '<' ? No it doesn't.
                return ["examples/malicious.ttl"]
            return []

        mock_glob.side_effect = fake_glob

        # Mock validation to return a malicious string
        mock_validate.return_value = (False, None, "<script>alert('XSS')</script>")

        with patch('scripts.maintenance.generate_html_report.os.path.basename') as mock_basename:
            mock_basename.return_value = "<script>alert(1)</script>.ttl"

            with tempfile.TemporaryDirectory() as tmpdir:
                output_file = os.path.join(tmpdir, "report.html")
                generate_html_report(output_file)

                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Verify malicious strings are escaped
                assert "<script>" not in content
                assert html.escape("<script>alert(1)</script>.ttl") in content

                assert "<script>alert('XSS')</script>" not in content
                assert html.escape("<script>alert('XSS')</script>") in content
