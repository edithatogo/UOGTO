from pathlib import Path


def test_field_expansion_roadmap_covers_open_issues() -> None:
    roadmap = Path("docs/roadmap/uogto-field-expansion-roadmap.md").read_text(encoding="utf-8")
    for issue in range(76, 84):
        assert f"#{issue}" in roadmap
    for phrase in [
        "worked example graph",
        "SHACL coverage",
        "competency query",
        "decision ledger",
        "external alignment",
    ]:
        assert phrase in roadmap


def test_applied_extension_pack_pattern_preserves_uogto_boundary() -> None:
    pattern = Path("docs/roadmap/applied-extension-pack-pattern.md").read_text(encoding="utf-8").lower()
    for phrase in [
        "shared game layer",
        "domain-local semantics",
        "health economics",
        "medical decision modelling",
        "safety systems",
        "genomic policy",
    ]:
        assert phrase in pattern


def test_conductor_track_links_roadmap_artifacts() -> None:
    track_id = "uogto_field_expansion_examples_validation_20260709"
    candidates = [
        Path("conductor/tracks") / track_id / "index.md",
        Path("conductor/archive") / track_id / "index.md",
    ]
    track_path = next((path for path in candidates if path.exists()), None)
    assert track_path is not None
    track = track_path.read_text(encoding="utf-8")
    assert "docs/roadmap/uogto-field-expansion-roadmap.md" in track
    assert "docs/roadmap/applied-extension-pack-pattern.md" in track
