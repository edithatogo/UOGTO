from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any


def load_sync_module() -> Any:
    if "sync_github_projects_under_test" in sys.modules:
        return sys.modules["sync_github_projects_under_test"]
    path = Path(__file__).resolve().parents[1] / "scripts" / "maintenance" / "sync_github_projects.py"
    spec = importlib.util.spec_from_file_location("sync_github_projects_under_test", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_ensure_project_item_adds_missing_item_when_apply(monkeypatch: Any) -> None:
    module = load_sync_module()
    url = "https://github.com/edithatogo/UOGTO/pull/67"
    calls: list[list[str]] = []

    def fake_gh_json(args: list[str]) -> dict[str, Any]:
        calls.append(args)
        return {"id": "PVTI_test", "content": {"url": url}}

    monkeypatch.setattr(module, "gh_json", fake_gh_json)
    cache: dict[str, dict[str, Any]] = {}

    item = module.ensure_project_item(8, url, True, cache)

    assert item == {"id": "PVTI_test", "content": {"url": url}}
    assert cache[url] == item
    assert calls == [
        [
            "project",
            "item-add",
            "8",
            "--owner",
            "edithatogo",
            "--url",
            url,
            "--format",
            "json",
        ]
    ]


def test_ensure_project_item_dry_run_does_not_add(monkeypatch: Any) -> None:
    module = load_sync_module()

    def fail_gh_json(args: list[str]) -> None:
        raise AssertionError(f"unexpected gh_json call: {args}")

    monkeypatch.setattr(module, "gh_json", fail_gh_json)

    assert module.ensure_project_item(8, "https://github.com/edithatogo/UOGTO/pull/67", False, {}) is None


def test_discover_tracks_derives_active_state_from_tracks_registry(tmp_path: Path) -> None:
    module = load_sync_module()
    conductor = tmp_path / "conductor"
    tracks = conductor / "tracks"
    archive = conductor / "archive"
    for track_id, parent in {
        "active_track_20260706": tracks,
        "completed_but_unarchived_track_20260706": tracks,
        "archived_track_20260706": archive,
    }.items():
        (parent / track_id).mkdir(parents=True)
    (conductor / "tracks.md").write_text(
        "\n".join(
            [
                "# Project Tracks",
                "",
                "## [~] Track: active_track_20260706",
                "- **Description**: Active test track.",
                "- **Status**: In Progress",
                "",
                "## [x] Track: completed_but_unarchived_track_20260706",
                "- **Description**: Completed test track still retained in tracks.",
                "- **Status**: Completed",
                "",
                "## [x] Archived Track: archived_track_20260706",
                "- **Description**: Archived test track.",
                "- **Status**: Completed and archived.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    discovered = {track.track_id: track for track in module.discover_tracks(tmp_path)}

    assert discovered["active_track_20260706"].status == module.STATUS_IN_PROGRESS
    assert discovered["active_track_20260706"].issue_state == "open"
    assert discovered["completed_but_unarchived_track_20260706"].status == module.STATUS_DONE
    assert discovered["completed_but_unarchived_track_20260706"].issue_state == "closed"
    assert discovered["archived_track_20260706"].status == module.STATUS_DONE
    assert discovered["archived_track_20260706"].issue_state == "closed"
