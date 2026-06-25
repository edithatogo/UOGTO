from pathlib import Path
from scripts.maintenance.audit_arxiv_source_privacy import audit_package

def test_privacy_audit_passes_clean_minimal_package(tmp_path: Path) -> None:
    package = tmp_path / "pkg"; package.mkdir()
    (package / "paper.tex").write_text("\\documentclass{article}\n\\begin{document}\nHello.\n\\end{document}\n", encoding="utf-8")
    manifest = audit_package(package)
    assert manifest["status"] == "pass"
    assert manifest["summary"]["failures"] == 0
    assert manifest["checks"]["credentials"]["status"] == "pass"

def test_privacy_audit_fails_private_comment_and_local_path(tmp_path: Path) -> None:
    package = tmp_path / "pkg"; package.mkdir()
    (package / "paper.tex").write_text("\\documentclass{article}\n% TODO remove private reviewer note from C:\\\\Users\\\\Example\\\\draft.tex\n\\begin{document}\nHello.\n\\end{document}\n", encoding="utf-8")
    manifest = audit_package(package)
    categories = {finding["category"] for finding in manifest["findings"]}
    assert manifest["status"] == "fail"
    assert "comments" in categories
    assert "private_urls" in categories

def test_privacy_audit_fails_auxiliary_and_hidden_files(tmp_path: Path) -> None:
    package = tmp_path / "pkg"; package.mkdir()
    (package / "paper.tex").write_text("\\documentclass{article}\n", encoding="utf-8")
    (package / "paper.aux").write_text("aux", encoding="utf-8")
    hidden = package / ".secret"; hidden.mkdir()
    (hidden / "note.tex").write_text("hidden", encoding="utf-8")
    manifest = audit_package(package)
    categories = {finding["category"] for finding in manifest["findings"]}
    assert manifest["status"] == "fail"
    assert "aux_log_output_files" in categories
    assert "hidden_files" in categories
