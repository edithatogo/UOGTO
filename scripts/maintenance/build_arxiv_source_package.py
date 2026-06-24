import argparse
import json
import os
import shutil
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.maintenance.clean_arxiv_source_package import DEFAULT_OUTPUT_DIR, DEFAULT_SOURCE_ROOT, clean_package


def copy_source_tree(source_root: Path, package_dir: Path) -> None:
    package_dir.mkdir(parents=True, exist_ok=True)
    for path in sorted(source_root.rglob("*"), key=lambda p: p.as_posix()):
        rel = path.relative_to(source_root)
        destination = package_dir / rel
        if path.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)


def build_package(source_root: Path = DEFAULT_SOURCE_ROOT, package_dir: Path = DEFAULT_OUTPUT_DIR) -> dict:
    copy_source_tree(source_root, package_dir)
    manifest = clean_package(package_dir, source_root)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a cleaned arXiv source package for the UOGTO manuscript.")
    parser.add_argument("--source-root", default=str(DEFAULT_SOURCE_ROOT))
    parser.add_argument("--package-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    manifest = build_package(Path(args.source_root), Path(args.package_dir))
    if args.json:
        print(json.dumps(manifest, indent=2))
    else:
        print(
            f"Built cleaned arXiv source package in {manifest['package_dir']}: removed {manifest['removed_count']} files, kept {manifest['kept_count']} files."
        )


if __name__ == "__main__":
    main()