import argparse
import json
import os
import shutil
import stat
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.maintenance.clean_arxiv_source_package import DEFAULT_OUTPUT_DIR, DEFAULT_SOURCE_ROOT, clean_package


def copy_source_tree(source_root: Path, package_dir: Path) -> None:
    package_dir.mkdir(parents=True, exist_ok=True)
    for path in sorted(source_root.rglob('*'), key=lambda p: p.as_posix()):
        if path.is_file() and path.suffix.lower() not in {'.tex', '.ltx', '.cls', '.sty', '.cfg', '.cbx', '.def', '.dtx', '.ins', '.bib', '.bbl', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.eps', '.ps'}:
            continue
        rel = path.relative_to(source_root)
        destination = package_dir / rel
        if path.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            if os.system(f'copy /y "{path}" "{destination}" >nul') != 0:
                raise OSError(f'Failed to copy {path} to {destination}')

def build_package(source_root: Path = DEFAULT_SOURCE_ROOT, package_dir: Path = DEFAULT_OUTPUT_DIR) -> dict:
    stage_dir = package_dir.parent / f'{package_dir.name}-{uuid.uuid4().hex[:8]}'
    if os.system(f'mkdir "{stage_dir}"') != 0:
        raise OSError(f'Failed to create staging directory: {stage_dir}')
    copy_source_tree(source_root, stage_dir)
    manifest = clean_package(stage_dir, source_root)
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
