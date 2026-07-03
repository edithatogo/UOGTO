from __future__ import annotations

import json
from pathlib import Path

from scripts.maintenance import build_article_source_acquisition_manifest as manifest


ROOT = Path(__file__).resolve().parents[1]


def test_source_acquisition_manifest_covers_inventory_and_checked_in_artifacts() -> None:
    payload = manifest.build_manifest()
    manifest.validate_manifest(payload)

    inventory = json.loads(
        (ROOT / "docs" / "article-hardening" / "source-extension-inventory.json").read_text(
            encoding="utf-8"
        )
    )
    inventory_ids = {source["source_id"] for source in inventory["sources"]}
    manifest_ids = {
        source["source_id"]
        for source in payload["artifacts"] + payload["reference_only_sources"]
    }

    assert payload["schema"] == "uogto.article-hardening.source-acquisition-manifest.v1"
    assert manifest_ids == inventory_ids
    assert payload["artifact_count"] >= 4
    assert payload["reference_only_count"] >= 30
    for artifact in payload["artifacts"]:
        assert artifact["checksum"].startswith("sha256:")
        assert artifact["content_type"]
        assert (ROOT / artifact["path"]).exists()


def test_source_acquisition_main_writes_json_and_markdown() -> None:
    assert manifest.main() == 0
    json_path = ROOT / "docs" / "article-hardening" / "source-acquisition-manifest.json"
    md_path = ROOT / "docs" / "article-hardening" / "source-acquisition-manifest.md"
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    markdown = md_path.read_text(encoding="utf-8")

    assert payload["artifact_count"] >= 4
    assert "Reference-Only Sources" in markdown
    assert "sha256:" in markdown
