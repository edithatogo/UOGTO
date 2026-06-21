import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIST_DIR = ROOT / "dist"
REQUIRED_RELEASE_ASSETS = [
    "uogto.ttl",
    "uogto-shapes.ttl",
    "context.jsonld",
    "core.context.jsonld",
    "extensions.context.jsonld",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_release_assets(dist_dir: Path) -> list[dict]:
    missing = [name for name in REQUIRED_RELEASE_ASSETS if not (dist_dir / name).exists()]
    if missing:
        raise AssertionError(f"Missing release assets in {dist_dir}: {', '.join(missing)}")

    assets = []
    for name in REQUIRED_RELEASE_ASSETS:
        path = dist_dir / name
        assets.append(
            {
                "name": name,
                "path": str(path.as_posix()),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return assets


def write_release_manifest(dist_dir: Path, version: str) -> dict:
    assets = collect_release_assets(dist_dir)
    manifest = {
        "name": "UOGTO release assets",
        "version": version,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "assets": assets,
    }

    manifest_path = dist_dir / "release-assets-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    checksums = "\n".join(f"{asset['sha256']}  {asset['name']}" for asset in assets) + "\n"
    (dist_dir / "SHA256SUMS").write_text(checksums, encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Package UOGTO generated release assets.")
    parser.add_argument("--dist-dir", default=str(DEFAULT_DIST_DIR), help="Generated dist directory.")
    parser.add_argument("--version", default="1.0.0", help="Release version for the manifest.")
    args = parser.parse_args()

    write_release_manifest(Path(args.dist_dir), args.version)
    print("Release asset manifest and checksums written.")


if __name__ == "__main__":
    main()
