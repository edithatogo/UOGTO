import json
import tarfile
from pathlib import Path

import pytest

from scripts.maintenance import build_arxiv_upload_ready


def test_upload_ready_bundle_writes_manifest_readme_checksums_and_deterministic_archive(tmp_path: Path) -> None:
    package = tmp_path / "pkg"
    package.mkdir()
    (package / "paper.tex").write_text("\\documentclass{article}\n\\begin{document}Hello\\end{document}\n", encoding="utf-8")
    (package / "figure-1.pdf").write_bytes(b"%PDF-1.4\n")
    output = tmp_path / "out"

    first = build_arxiv_upload_ready.build_upload_bundle(package_dir=package, output_dir=output)
    second = build_arxiv_upload_ready.build_upload_bundle(package_dir=package, output_dir=output)

    archive = output / "uogto-arxiv-source.tar.gz"
    manifest = json.loads((output / "arxiv-submission-manifest.json").read_text(encoding="utf-8"))
    readme = json.loads((output / "00README.json").read_text(encoding="utf-8"))
    checksums = (output / "SHA256SUMS").read_text(encoding="utf-8")

    assert first["archive"]["sha256"] == second["archive"]["sha256"]
    assert manifest["schema"] == "uogto.arxiv-upload-ready.v1"
    assert manifest["archive"]["includes_00readme"] is False
    assert manifest["compiler_source"].startswith("intended arXiv 00README preview")
    assert manifest["git"]["dirty_mode"] == "tracked-files-only"
    assert isinstance(manifest["git"]["dirty_entries"], list)
    assert manifest["arxiv_processing_preview"]["source"].endswith("00README.json")
    assert readme["process"]["compiler"] == "pdflatex"
    assert readme["texlive_version"] == 2025
    assert "dist/arxiv" not in checksums
    assert "uogto-arxiv-source.tar.gz" in checksums
    assert "arxiv-submission-manifest.json" in checksums

    with tarfile.open(archive, "r:gz") as tar:
        names = tar.getnames()
    assert names == ["figure-1.pdf", "paper.tex"]


def test_upload_ready_bundle_can_include_00readme_for_programmatic_submission(tmp_path: Path) -> None:
    package = tmp_path / "pkg"
    package.mkdir()
    (package / "paper.tex").write_text("\\documentclass{article}\n\\begin{document}Hello\\end{document}\n", encoding="utf-8")
    output = tmp_path / "out"

    build_arxiv_upload_ready.build_upload_bundle(package_dir=package, output_dir=output, include_00readme=True)

    with tarfile.open(output / "uogto-arxiv-source.tar.gz", "r:gz") as tar:
        names = tar.getnames()
    assert names == ["paper.tex", "00README.json"]


def test_upload_ready_bundle_rejects_unsafe_filenames(tmp_path: Path) -> None:
    package = tmp_path / "pkg"
    package.mkdir()
    (package / "paper.tex").write_text("\\documentclass{article}\n\\begin{document}Hello\\end{document}\n", encoding="utf-8")
    (package / "bad name.tex").write_text("unsafe", encoding="utf-8")

    with pytest.raises(AssertionError, match="filename contains characters"):
        build_arxiv_upload_ready.build_upload_bundle(package_dir=package, output_dir=tmp_path / "out")
