import argparse
import ctypes
import os
import stat
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE_ROOT = ROOT / "docs" / "paper"
DEFAULT_OUTPUT_DIR = ROOT / ".tmp" / "arxiv-source-package"
DEFAULT_PAPER = "paper.tex"

AUXILIARY_SUFFIXES = {
    ".aux",
    ".bbl",
    ".blg",
    ".bcf",
    ".brf",
    ".fdb_latexmk",
    ".fls",
    ".lof",
    ".log",
    ".lot",
    ".nav",
    ".out",
    ".run.xml",
    ".snm",
    ".synctex",
    ".synctex.gz",
    ".toc",
    ".vrb",
}
PRESERVE_EXTENSIONS = {
    ".tex",
    ".bib",
    ".bst",
    ".cls",
    ".sty",
    ".def",
    ".cfg",
    ".png",
    ".jpg",
    ".jpeg",
    ".pdf",
    ".eps",
    ".tif",
    ".tiff",
}
DENY_NAME_PATTERNS = [
    re.compile(r"(^|[._-])(referee|referees)([._-]|$)", re.IGNORECASE),
    re.compile(r"(^|[._-])journal([._-]|$).*template", re.IGNORECASE),
    re.compile(r"(^|[._-])template([._-]|$)", re.IGNORECASE),
    re.compile(r"(^|[._-])private([._-]|$)", re.IGNORECASE),
    re.compile(r"(^|[._-])hidden([._-]|$)", re.IGNORECASE),
]
GRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]+)\}")
BIB_RE = re.compile(r"\\(?:bibliography|addbibresource)(?:\[[^\]]*\])?\{([^}]+)\}")


def is_auxiliary(path: Path) -> bool:
    suffix = "".join(path.suffixes).lower()
    if suffix in AUXILIARY_SUFFIXES:
        return True
    return any(path.name.lower().endswith(sfx) for sfx in AUXILIARY_SUFFIXES)


def is_hidden(path: Path) -> bool:
    return any(part.startswith(".") for part in path.parts)


def is_denied_name(path: Path) -> bool:
    return any(pattern.search(path.name) for pattern in DENY_NAME_PATTERNS)


def parse_tex_references(tex_path: Path) -> tuple[set[str], set[str], set[str]]:
    text = tex_path.read_text(encoding="utf-8")
    graphics = {match.group(1).strip() for match in GRAPHICS_RE.finditer(text)}
    includes = {match.group(1).strip() for match in INPUT_RE.finditer(text)}
    bibs = set()
    for match in BIB_RE.finditer(text):
        for item in match.group(1).split(","):
            cleaned = item.strip()
            if cleaned:
                bibs.add(cleaned)
    return graphics, includes, bibs


def candidate_variants(value: str) -> list[str]:
    path = Path(value)
    variants = [path.as_posix(), path.name]
    if not path.suffix:
        for ext in [".tex", ".bib", ".bst", ".sty", ".cls"]:
            variants.append(f"{path.as_posix()}{ext}")
            variants.append(f"{path.name}{ext}")
    return variants


def is_referenced(path: Path, *, graphics: set[str], includes: set[str], bibs: set[str], package_dir: Path) -> bool:
    rel = path.relative_to(package_dir).as_posix()
    name = path.name
    stem = path.stem
    if name == DEFAULT_PAPER:
        return True
    if rel in includes or name in includes or stem in includes:
        return True
    if rel in bibs or name in bibs or stem in bibs:
        return True
    for item in graphics:
        for variant in candidate_variants(item):
            variant_path = Path(variant)
            if rel == variant or name == variant_path.name or stem == variant_path.stem:
                return True
    return False


def should_keep(path: Path, *, package_dir: Path, graphics: set[str], includes: set[str], bibs: set[str]) -> tuple[bool, str]:
    rel = path.relative_to(package_dir)
    if is_hidden(rel) or is_denied_name(rel):
        return False, "hidden_or_private_source_junk"
    if is_auxiliary(path):
        return False, "auxiliary_or_output_file"
    if path.name == DEFAULT_PAPER:
        return True, "primary_manuscript"
    if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".pdf", ".eps", ".tif", ".tiff"}:
        if is_referenced(path, graphics=graphics, includes=includes, bibs=bibs, package_dir=package_dir):
            return True, "referenced_figure_or_asset"
        return False, "unused_figure"
    if path.suffix.lower() in PRESERVE_EXTENSIONS:
        if is_referenced(path, graphics=graphics, includes=includes, bibs=bibs, package_dir=package_dir):
            return True, "referenced_source_or_asset"
        return False, "unused_or_unreferenced_source_file"
    return False, "extraneous_file"




def remove_file(path: Path) -> None:
    try:
        path.unlink()
        return
    except PermissionError:
        try:
            path.chmod(0o666)
        except OSError:
            pass
        try:
            path.unlink()
            return
        except PermissionError:
            if os.name != "nt":
                raise
            target = str(path)
            kernel32 = ctypes.windll.kernel32
            try:
                kernel32.SetFileAttributesW(target, 0x80)
            except Exception:
                pass
            if not kernel32.DeleteFileW(target):
                raise PermissionError(f'Unable to remove {path}')

def clean_package(package_dir: Path, source_root: Path | None = None, paper_name: str = DEFAULT_PAPER) -> dict:
    source_root = source_root or package_dir
    tex_path = package_dir / paper_name
    if not tex_path.exists():
        raise AssertionError(f"Missing manuscript root file: {tex_path}")
    graphics, includes, bibs = parse_tex_references(tex_path)
    removed = []
    kept = []
    for path in sorted(package_dir.rglob("*"), key=lambda p: (p.is_file(), len(p.parts), p.as_posix())):
        if path.is_dir():
            continue
        keep, reason = should_keep(path, package_dir=package_dir, graphics=graphics, includes=includes, bibs=bibs)
        rel = path.relative_to(package_dir).as_posix()
        if keep:
            kept.append(rel)
        else:
            remove_file(path)
            removed.append({"path": rel, "reason": reason})
    for path in sorted([p for p in package_dir.rglob("*") if p.is_dir()], key=lambda p: len(p.parts), reverse=True):
        try:
            path.rmdir()
        except OSError:
            pass
    manifest_path = package_dir.parent / f"{package_dir.name}.manifest.json"
    manifest = {
        "schema": "uogto.arxiv-source-package-cleaner.v1",
        "package_dir": str(package_dir),
        "source_root": str(source_root),
        "paper": paper_name,
        "manifest_path": str(manifest_path),
        "removed_count": len(removed),
        "kept_count": len(kept),
        "removed": removed,
        "kept": kept,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def resolve_default_package_dir(package_dir: Path) -> Path:
    """Resolve the latest generated package when the default path is requested."""
    if package_dir != DEFAULT_OUTPUT_DIR:
        return package_dir
    if package_dir.exists() and (package_dir / DEFAULT_PAPER).exists():
        return package_dir
    manifests = sorted(
        package_dir.parent.glob(f"{package_dir.name}-*.manifest.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    for manifest_path in manifests:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        candidate = Path(manifest.get("package_dir", ""))
        if candidate.exists() and (candidate / DEFAULT_PAPER).exists():
            return candidate
    return package_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean an arXiv source package by removing extraneous files.")
    parser.add_argument("--package-dir", default=str(DEFAULT_OUTPUT_DIR), help="Path to the source package tree to clean.")
    parser.add_argument("--source-root", default=str(DEFAULT_SOURCE_ROOT), help="Original source root used for reference matching.")
    parser.add_argument("--paper", default=DEFAULT_PAPER, help="Main TeX file name inside the package.")
    parser.add_argument("--json", action="store_true", help="Print the cleaning manifest as JSON.")
    args = parser.parse_args()
    manifest = clean_package(resolve_default_package_dir(Path(args.package_dir)), Path(args.source_root), args.paper)
    if args.json:
        print(json.dumps(manifest, indent=2))
    else:
        print(f"Cleaned arXiv source package: removed {manifest['removed_count']} files, kept {manifest['kept_count']} files.")


if __name__ == "__main__":
    main()
