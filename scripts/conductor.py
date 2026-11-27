"""Report registered active Conductor tracks and historical bootstrap phases."""

import argparse
import json
from pathlib import Path
import re
import sys

import yaml


DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[1]
TRACK_HEADING = re.compile(r"^## \[([ x~])\] (Archived Track|Track): (\S+)\s*$", re.MULTILINE)
TRACK_LINK = re.compile(r"^- \*\*Link\*\*: \[[^\]]+\]\(([^)]+)\)\s*$", re.MULTILINE)


def load_report(repo_root):
    """Use the registry's active entries, never a scan of track directories."""
    tasks_path = repo_root / ".conductor/tasks.yaml"
    with tasks_path.open(encoding="utf-8") as handle:
        legacy = yaml.safe_load(handle)
    if not isinstance(legacy, dict) or not isinstance(legacy.get("phases"), list):
        raise ValueError(f"{tasks_path}: expected a mapping with a phases list")

    registry_name = legacy.get("canonical_registry", "conductor/tracks.md")
    if not isinstance(registry_name, str) or not registry_name.strip():
        raise ValueError(f"{tasks_path}: canonical_registry must be a nonempty path")
    registry_path = repo_root / registry_name
    registry = registry_path.read_text(encoding="utf-8")
    headings = list(TRACK_HEADING.finditer(registry))
    if not headings:
        raise ValueError(f"{registry_path}: no registered track headings found")

    tracks = []
    seen = set()
    for index, heading in enumerate(headings):
        marker, kind, track_id = heading.groups()
        if marker == "x" or kind == "Archived Track":
            continue
        if track_id in seen:
            raise ValueError(f"{registry_path}: duplicate active track {track_id}")
        seen.add(track_id)
        end = headings[index + 1].start() if index + 1 < len(headings) else len(registry)
        link = TRACK_LINK.search(registry[heading.end():end])
        if link is None:
            raise ValueError(f"{registry_path}: active track {track_id} has no Link")
        metadata_path = (registry_path.parent / link.group(1) / "metadata.json").resolve()
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ValueError(f"Active track {track_id}: cannot load {metadata_path}: {exc}") from exc
        if not isinstance(metadata, dict) or metadata.get("track_id") != track_id:
            raise ValueError(f"Active track {track_id}: {metadata_path} must identify that track_id")
        for field in ("status", "execution_status"):
            if field == "execution_status" and field not in metadata:
                continue
            value = metadata.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Active track {track_id}: {metadata_path} needs a nonempty {field}")
        track = {
            "track_id": track_id,
            "path": link.group(1),
            "status": metadata["status"],
        }
        for field in ("execution_status", "description"):
            if field in metadata:
                track[field] = metadata[field]
        tracks.append(track)

    return {
        **legacy,
        "canonical_registry": registry_name,
        "tracks": tracks,
        "legacy_phases_status": "historical",
    }


def main():
    parser = argparse.ArgumentParser(description="Conductor task status reporter.")
    parser.add_argument("--json", action="store_true", help="Output status in JSON format.")
    parser.add_argument("--repo-root", type=Path, default=DEFAULT_REPO_ROOT,
                        help="Repository root (defaults to this script's checkout).")
    args = parser.parse_args()

    try:
        data = load_report(args.repo_root)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"Error loading Conductor status: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(data, indent=2))
        return 0

    print("=== Conductor Task Status Report ===")
    print(f"\nCanonical active tracks: {data['canonical_registry']}")
    if not data["tracks"]:
        print("No active tracks registered.")
    for track in data["tracks"]:
        print(f"  Track: {track['track_id']}")
        print(f"      Status: {track['status']}")
        if "execution_status" in track:
            print(f"      Execution status: {track['execution_status']}")
        print(f"      Path: {track['path']}")

    print("\nHistorical legacy phases (.conductor/tasks.yaml)")
    for phase in data["phases"]:
        print(f"\nPhase: {phase.get('name')} (ID: {phase.get('id')})")
        print(f"Status: {phase.get('status')}")
        for task in phase.get("tasks", []):
            status_icon = "[x]" if task.get("status") == "completed" else "[ ]"
            print(f"  {status_icon} Task: {task.get('id')} ({task.get('status')})")
            print(f"      Owner: {task.get('owner_role')}")
            print(f"      Expected Outputs: {', '.join(task.get('outputs', []))}")
            print(f"      Validation Command: {task.get('validation_command')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
