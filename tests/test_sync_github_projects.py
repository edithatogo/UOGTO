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
