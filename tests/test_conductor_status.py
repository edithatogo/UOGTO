import json
from pathlib import Path
import subprocess
import sys

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/conductor.py"


def make_repository(tmp_path):
    (tmp_path / ".conductor").mkdir()
    (tmp_path / ".conductor/tasks.yaml").write_text(
        "canonical_registry: conductor/current.md\n"
        "phases:\n  - id: bootstrap\n    status: completed\n    tasks: []\n",
        encoding="utf-8",
    )
    track = tmp_path / "conductor/tracks/pending_contract"
    track.mkdir(parents=True)
    (track / "metadata.json").write_text(json.dumps({
        "track_id": "pending_contract", "status": "new", "execution_status": "pending",
    }), encoding="utf-8")
    (tmp_path / "conductor/current.md").write_text(
        "# Project Tracks\n\n## [ ] Track: pending_contract\n"
        "- **Link**: [./tracks/pending_contract/](./tracks/pending_contract/)\n\n"
        "## [x] Archived Track: historical\n"
        "- **Link**: [./archive/historical/](./archive/historical/)\n",
        encoding="utf-8",
    )
    # Unregistered directories must never introduce work or metadata errors.
    unregistered = tmp_path / "conductor/tracks/unregistered"
    unregistered.mkdir()
    (unregistered / "metadata.json").write_text("not json", encoding="utf-8")
    return track / "metadata.json"


def run_report(repo_root, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", str(repo_root), *args],
        cwd=repo_root.parent, capture_output=True, text=True, check=False,
    )


def test_pending_canonical_tracks_visible_alongside_historical_phases(tmp_path):
    make_repository(tmp_path)
    result = run_report(tmp_path, "--json")
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["canonical_registry"] == "conductor/current.md"
    assert report["tracks"] == [{
        "track_id": "pending_contract", "path": "./tracks/pending_contract/",
        "status": "new", "execution_status": "pending",
    }]
    assert report["phases"] == [{"id": "bootstrap", "status": "completed", "tasks": []}]
    assert report["legacy_phases_status"] == "historical"
    text_result = run_report(tmp_path)
    assert text_result.returncode == 0, text_result.stderr
    assert "Track: pending_contract" in text_result.stdout
    assert "Execution status: pending" in text_result.stdout
    assert "Historical legacy phases" in text_result.stdout


@pytest.mark.parametrize("metadata", [None, "not json", "[]", '{}',
                                      '{"track_id": "pending_contract", "status": null}'])
def test_invalid_registered_metadata_fails_clearly(tmp_path, metadata):
    metadata_path = make_repository(tmp_path)
    if metadata is None:
        metadata_path.unlink()
    else:
        metadata_path.write_text(metadata, encoding="utf-8")
    result = run_report(tmp_path, "--json")
    assert result.returncode == 1
    assert not result.stdout
    assert "Active track pending_contract" in result.stderr
    assert "metadata.json" in result.stderr


def test_default_repository_is_independent_of_working_directory(tmp_path):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--json"], cwd=tmp_path,
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["canonical_registry"] == "conductor/tracks.md"
    assert any(track["track_id"] == "semantic_game_contracts_20261107"
               for track in report["tracks"])
