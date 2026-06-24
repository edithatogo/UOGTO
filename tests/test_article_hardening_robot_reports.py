from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROBOT_DIR = ROOT / "docs" / "article-hardening" / "robot"


def test_robot_style_status_tracks_portable_baseline() -> None:
    status = json.loads((ROBOT_DIR / "status.json").read_text(encoding="utf-8"))
    assert status["schema"] == "uogto.article-hardening.robot-style.v1"
    assert "java_available" in status["toolchain"]
    assert status["mode"] in {"portable-baseline", "robot"}
    assert status["reasoner"]["reasoner"]["owlrl_status"] == "passed"


def test_robot_style_reports_exist() -> None:
    for filename in [
        "reasoner-check.md",
        "report.md",
        "merged-ontology.ttl",
        "merge-diff.md",
        "import-extraction.ttl",
        "import-extraction.md",
    ]:
        path = ROBOT_DIR / filename
        assert path.exists(), path

