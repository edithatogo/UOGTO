import json
from pathlib import Path

from scripts.maintenance.audit_arxiv_source_privacy import audit_package, write_markdown

def test_privacy_audit_passes_clean_minimal_package(tmp_path: Path) -> None:
    package = tmp_path / "pkg"
    package.mkdir()
    (package / "paper.tex").write_text("\\documentclass{article}\n\\begin{document}\nHello.\n\\end{document}\n", encoding="utf-8")
    manifest = audit_package(package)
    assert manifest["status"] == "pass"
    assert manifest["summary"]["failures"] == 0
    assert manifest["checks"]["credentials"]["status"] == "pass"

def test_privacy_audit_fails_private_comment_and_local_path(tmp_path: Path) -> None:
    package = tmp_path / "pkg"
    package.mkdir()
    (package / "paper.tex").write_text("\\documentclass{article}\n% TODO remove private reviewer note from C:\\\\Users\\\\Example\\\\draft.tex\n\\begin{document}\nHello.\n\\end{document}\n", encoding="utf-8")
    manifest = audit_package(package)
    categories = {finding["category"] for finding in manifest["findings"]}
    assert manifest["status"] == "fail"
    assert "comments" in categories
    assert "private_urls" in categories


def test_privacy_audit_fails_forward_slash_local_paths(tmp_path: Path) -> None:
    package = tmp_path / "pkg"
    package.mkdir()
    (package / "paper.tex").write_text(
        "\\documentclass{article}\n"
        "% private local draft at C:/Users/Example/draft.tex and /home/example/token.txt\n"
        "\\begin{document}\nHello.\n\\end{document}\n",
        encoding="utf-8",
    )
    manifest = audit_package(package)
    categories = {finding["category"] for finding in manifest["findings"]}
    assert manifest["status"] == "fail"
    assert "private_urls" in categories

def test_privacy_audit_fails_auxiliary_and_hidden_files(tmp_path: Path) -> None:
    package = tmp_path / "pkg"
    package.mkdir()
    (package / "paper.tex").write_text("\\documentclass{article}\n", encoding="utf-8")
    (package / "paper.aux").write_text("aux", encoding="utf-8")
    hidden = package / ".secret"
    hidden.mkdir()
    (hidden / "note.tex").write_text("hidden", encoding="utf-8")
    manifest = audit_package(package)
    categories = {finding["category"] for finding in manifest["findings"]}
    assert manifest["status"] == "fail"
    assert "aux_log_output_files" in categories
    assert "hidden_files" in categories

def test_privacy_audit_redacts_local_package_paths(tmp_path: Path) -> None:
    package = tmp_path / "pkg"
    package.mkdir()
    cleaner_manifest = tmp_path / "pkg.manifest.json"
    (package / "paper.tex").write_text("\\documentclass{article}\n", encoding="utf-8")
    cleaner_manifest.write_text('{"summary": {"kept_count": 1}}\n', encoding="utf-8")

    manifest = audit_package(package, cleaner_manifest)
    markdown_path = tmp_path / "audit.md"
    write_markdown(manifest, markdown_path)
    serialized = json.dumps(manifest) + markdown_path.read_text(encoding="utf-8")

    assert str(tmp_path) not in serialized
    assert manifest["package_dir"] == "pkg"
    assert manifest["cleaner_manifest"] == "pkg.manifest.json"
