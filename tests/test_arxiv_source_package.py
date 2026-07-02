import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.maintenance import build_arxiv_source_package, clean_arxiv_source_package


def test_build_package_manifest_points_to_cleaned_stage_dir(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    source_root.mkdir()
    (source_root / "paper.tex").write_text("Hello\n", encoding="utf-8")
    (source_root / "notes.txt").write_text("private draft\n", encoding="utf-8")

    package_dir = tmp_path / "arxiv-source-package"
    manifest = build_arxiv_source_package.build_package(source_root, package_dir)

    built_dir = Path(manifest["package_dir"])
    assert built_dir.name == "arxiv-source-package"
    assert (built_dir / "paper.tex").exists()
    assert not (built_dir / "notes.txt").exists()
    assert manifest["kept"] == ["paper.tex"]


def test_default_clean_prefers_deterministic_default_package(tmp_path: Path, monkeypatch) -> None:
    default_dir = tmp_path / "arxiv-source-package"
    default_dir.mkdir()
    (default_dir / "paper.tex").write_text("fresh deterministic\n", encoding="utf-8")

    package_dir = tmp_path / "arxiv-source-package-abc12345"
    package_dir.mkdir()
    (package_dir / "paper.tex").write_text("old random\n", encoding="utf-8")
    manifest = tmp_path / "arxiv-source-package-abc12345.manifest.json"
    manifest.write_text('{"package_dir": "' + package_dir.as_posix() + '"}\n', encoding="utf-8")

    monkeypatch.setattr(clean_arxiv_source_package, "DEFAULT_OUTPUT_DIR", default_dir)
    resolved = clean_arxiv_source_package.resolve_default_package_dir(default_dir)

    assert resolved == default_dir


def test_default_clean_resolves_latest_legacy_generated_manifest(tmp_path: Path, monkeypatch) -> None:
    default_dir = tmp_path / "arxiv-source-package"
    package_dir = tmp_path / "arxiv-source-package-abc12345"
    package_dir.mkdir()
    (package_dir / "paper.tex").write_text("fresh\n", encoding="utf-8")
    manifest = tmp_path / "arxiv-source-package-abc12345.manifest.json"
    manifest.write_text('{"package_dir": "' + package_dir.as_posix() + '"}\n', encoding="utf-8")

    monkeypatch.setattr(clean_arxiv_source_package, "DEFAULT_OUTPUT_DIR", default_dir)
    resolved = clean_arxiv_source_package.resolve_default_package_dir(default_dir)

    assert resolved == package_dir
