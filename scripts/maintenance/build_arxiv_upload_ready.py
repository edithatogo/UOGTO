#!/usr/bin/env python3
"""Build an upload-ready arXiv source bundle with provenance metadata."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import re
import subprocess
import tarfile
from datetime import datetime, timezone
from pathlib import Path

try:
    from scripts.maintenance.clean_arxiv_source_package import (
        DEFAULT_OUTPUT_DIR as DEFAULT_CLEAN_PACKAGE_DIR,
        DEFAULT_PAPER,
        resolve_default_package_dir,
    )
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from scripts.maintenance.clean_arxiv_source_package import (
        DEFAULT_OUTPUT_DIR as DEFAULT_CLEAN_PACKAGE_DIR,
        DEFAULT_PAPER,
        resolve_default_package_dir,
    )


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = ROOT / "dist" / "arxiv"
DEFAULT_ARCHIVE_NAME = "uogto-arxiv-source.tar.gz"
DEFAULT_MANIFEST_NAME = "arxiv-submission-manifest.json"
DEFAULT_README_NAME = "00README.json"
DEFAULT_CHECKSUMS_NAME = "SHA256SUMS"
DEFAULT_COMPILER = "pdflatex"
DEFAULT_TEXLIVE_VERSION = "2025"
SAFE_COMPONENT_RE = re.compile(r"^[A-Za-z0-9_+.,=-]+$")


def project_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_value(*args: str) -> str | None:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def iter_package_files(package_dir: Path) -> list[Path]:
    return sorted((path for path in package_dir.rglob("*") if path.is_file()), key=lambda p: p.relative_to(package_dir).as_posix())


def validate_package(package_dir: Path, paper_name: str) -> list[str]:
    issues: list[str] = []
    if not (package_dir / paper_name).exists():
        issues.append(f"missing top-level manuscript: {paper_name}")

    for path in iter_package_files(package_dir):
        rel = path.relative_to(package_dir)
        for part in rel.parts:
            if part in {"", ".", ".."}:
                issues.append(f"{rel.as_posix()}: unsafe path segment")
            if part.startswith("."):
                issues.append(f"{rel.as_posix()}: hidden path segment")
            if not SAFE_COMPONENT_RE.fullmatch(part):
                issues.append(f"{rel.as_posix()}: filename contains characters outside arXiv-safe policy")
    return sorted(set(issues))


def build_00readme(paper_name: str, compiler: str, texlive_version: str) -> dict:
    return {
        "spec_version": 1,
        "process": {"compiler": compiler},
        "sources": [{"filename": paper_name, "usage": "toplevel"}],
        "texlive_version": int(texlive_version),
        "stamp": True,
    }


def add_file(tar: tarfile.TarFile, source: Path, arcname: str) -> None:
    data = source.read_bytes()
    info = tarfile.TarInfo(arcname)
    info.size = len(data)
    info.mode = 0o644
    info.mtime = 0
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    tar.addfile(info, fileobj=io.BytesIO(data))


def write_deterministic_tar_gz(package_dir: Path, archive_path: Path, readme_path: Path | None = None) -> None:
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with archive_path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode="w") as tar:
                for path in iter_package_files(package_dir):
                    add_file(tar, path, path.relative_to(package_dir).as_posix())
                if readme_path is not None:
                    add_file(tar, readme_path, DEFAULT_README_NAME)


def read_privacy_audit(path: Path, require: bool) -> dict:
    if not path.exists():
        if require:
            raise AssertionError(f"Missing arXiv privacy audit manifest: {path}")
        return {"path": project_path(path), "status": "not_found"}
    data = json.loads(path.read_text(encoding="utf-8"))
    if require and data.get("status") != "pass":
        raise AssertionError(f"arXiv privacy audit must pass before upload-ready packaging: {path}")
    return {
        "path": project_path(path),
        "status": data.get("status"),
        "generated_at_utc": data.get("generated_at_utc"),
        "summary": data.get("summary", {}),
    }


def write_checksums(output_dir: Path, paths: list[Path]) -> Path:
    checksum_path = output_dir / DEFAULT_CHECKSUMS_NAME
    lines = [f"{sha256_file(path)}  {project_path(path)}" for path in paths]
    checksum_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return checksum_path


def build_upload_bundle(
    package_dir: Path = DEFAULT_CLEAN_PACKAGE_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    paper_name: str = DEFAULT_PAPER,
    compiler: str = DEFAULT_COMPILER,
    texlive_version: str = DEFAULT_TEXLIVE_VERSION,
    include_00readme: bool = False,
    privacy_audit: Path = ROOT / "docs" / "paper" / "arxiv-source-privacy-audit.json",
    require_privacy_audit: bool = False,
) -> dict:
    package_dir = resolve_default_package_dir(package_dir)
    if not package_dir.exists():
        raise AssertionError(f"Missing cleaned arXiv source package: {package_dir}")

    issues = validate_package(package_dir, paper_name)
    if issues:
        raise AssertionError("arXiv upload-ready package validation failed:\n- " + "\n- ".join(issues))

    output_dir.mkdir(parents=True, exist_ok=True)
    readme_path = output_dir / DEFAULT_README_NAME
    readme = build_00readme(paper_name, compiler, texlive_version)
    readme_path.write_text(json.dumps(readme, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    archive_path = output_dir / DEFAULT_ARCHIVE_NAME
    write_deterministic_tar_gz(package_dir, archive_path, readme_path if include_00readme else None)

    package_files = [
        {
            "path": path.relative_to(package_dir).as_posix(),
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in iter_package_files(package_dir)
    ]
    git_status = git_value("status", "--short", "--untracked-files=no") or ""
    git_status_entries = [line for line in git_status.splitlines() if line.strip()]
    checksum_path = output_dir / DEFAULT_CHECKSUMS_NAME
    manifest = {
        "schema": "uogto.arxiv-upload-ready.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "package_dir": project_path(package_dir),
        "paper": paper_name,
        "compiler": compiler,
        "compiler_source": "intended arXiv 00README preview; not inferred from local PDF build engine",
        "texlive_version": int(texlive_version),
        "texlive_version_source": "intended arXiv 00README preview; verify in arXiv UI before final submission",
        "arxiv_processing_preview": {
            "compiler": compiler,
            "texlive_version": int(texlive_version),
            "source": project_path(readme_path),
            "included_in_archive": include_00readme,
        },
        "archive": {
            "path": project_path(archive_path),
            "sha256": sha256_file(archive_path),
            "size_bytes": archive_path.stat().st_size,
            "includes_00readme": include_00readme,
        },
        "readme_preview": {
            "path": project_path(readme_path),
            "sha256": sha256_file(readme_path),
            "included_in_archive": include_00readme,
            "note": "Review artifact by default; include only for programmatic/custom arXiv submissions.",
        },
        "checksums": {"path": project_path(checksum_path)},
        "privacy_audit": read_privacy_audit(privacy_audit, require_privacy_audit),
        "files": package_files,
        "policy": {
            "filename_component_regex": SAFE_COMPONENT_RE.pattern,
            "archive_format": "tar.gz",
            "deterministic_archive": True,
            "default_00readme_policy": "generated for review but not included unless --include-00readme is set",
        },
        "git": {
            "commit": git_value("rev-parse", "HEAD"),
            "dirty": bool(git_status),
            "dirty_file_count": len(git_status_entries),
            "dirty_entries": git_status_entries,
            "dirty_mode": "tracked-files-only",
        },
    }
    manifest_path = output_dir / DEFAULT_MANIFEST_NAME
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_checksums(output_dir, [archive_path, readme_path, manifest_path])
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-dir", type=Path, default=DEFAULT_CLEAN_PACKAGE_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--paper", default=DEFAULT_PAPER)
    parser.add_argument("--compiler", default=DEFAULT_COMPILER)
    parser.add_argument("--texlive-version", default=DEFAULT_TEXLIVE_VERSION)
    parser.add_argument("--include-00readme", action="store_true")
    parser.add_argument("--privacy-audit", type=Path, default=ROOT / "docs" / "paper" / "arxiv-source-privacy-audit.json")
    parser.add_argument("--require-privacy-audit", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    manifest = build_upload_bundle(
        package_dir=args.package_dir,
        output_dir=args.output_dir,
        paper_name=args.paper,
        compiler=args.compiler,
        texlive_version=args.texlive_version,
        include_00readme=args.include_00readme,
        privacy_audit=args.privacy_audit,
        require_privacy_audit=args.require_privacy_audit,
    )
    if args.json:
        print(json.dumps(manifest, indent=2, sort_keys=True))
    else:
        print(f"arXiv upload-ready archive: {manifest['archive']['path']}")
        print(f"SHA256: {manifest['archive']['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
