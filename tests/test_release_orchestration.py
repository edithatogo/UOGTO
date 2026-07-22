from pathlib import Path

import json


ROOT = Path(__file__).resolve().parents[1]


def test_release_please_tracks_release_metadata():
    config = json.loads((ROOT / "release-please-config.json").read_text())
    assert config["release-type"] == "python"
    assert "CITATION.cff" in config["packages"]["."]["extra-files"]
    assert ".zenodo.json" in config["packages"]["."]["extra-files"]


def test_signed_tag_gate_keeps_external_publication_separate():
    workflow = (ROOT / ".github/workflows/release-metadata-gate.yml").read_text()
    assert "RELEASE_TAGGER_EMAIL" in workflow
    assert "verification.verified" in workflow
    assert "make release-preflight" in workflow
    assert "publish" not in workflow.lower()
