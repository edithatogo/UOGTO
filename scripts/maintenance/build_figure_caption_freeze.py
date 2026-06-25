from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRACK = ROOT / "conductor" / "tracks" / "uogto_nature_presubmission_evaluation_20260625"
IMAGE_SCORES = TRACK / "image_scores.csv"
PAPER = ROOT / "docs" / "paper" / "paper.tex"
SUPPLEMENT = ROOT / "docs" / "paper" / "supplement-package.md"
OUT_JSON = ROOT / "docs" / "paper" / "figure-caption-freeze-manifest.json"
OUT_MD = ROOT / "docs" / "paper" / "figure-caption-freeze-manifest.md"

EXPECTED_SUPPLEMENT_FIGURES = {
    "Supplementary Figure S1": "docs/article-hardening/figures/prisma-2020-source-discovery-flow.svg",
    "Supplementary Figure S2": "docs/article-hardening/figures/prisma-2020-screening-flow.svg",
    "Supplementary Figure S3": "docs/ontology-comparison/figures/source_family_evidence_heatmap.svg",
    "Supplementary Figure S4": "docs/ontology-comparison/figures/mapping_flow_sankey.svg",
    "Supplementary Figure S5": "docs/ontology-comparison/figures/source_module_overlap_heatmap.svg",
    "Supplementary Figure S6": "docs/ontology-comparison/figures/source_similarity_network.svg",
    "Supplementary Figure S7": "docs/ontology-comparison/figures/reviewer_workload.svg",
}

MAIN_MANUSCRIPT_CALLOUTS = {
    "fig:architecture": "Semantic separation among game specifications, sessions, traces, strategies, actions, payoffs, outcomes, mechanisms, and execution bindings.",
    "fig:mapping-flow": "Candidate-to-review-to-alignment flow for conservative ontology mappings.",
    "fig:evidence-heatmap": "Source-family evidence levels separating parsed RDF from structured non-RDF, metadata-only, and literature-only evidence.",
    "fig:network-sensitivity": "Network-sensitivity view showing bridge concepts and evidence limits.",
    "fig:reproducibility": "Reproducibility chain from ontology source to validation, mapping, tables, and submission gates.",
}

RERUN_TRIGGERS = [
    "manuscript Figure~\\ref callouts change",
    "supplementary figure numbering S1-S7 changes",
    "caption/title text changes",
    "source_path or rendered_path changes in image_scores.csv",
    "any source or rendered figure file hash changes",
    "any image score drops below 100/100",
    "manuscript, supplement, or deck placement changes",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_scores() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with IMAGE_SCORES.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            source = ROOT / row["source_path"]
            rendered = ROOT / row["rendered_path"]
            score = int(row["total_score"])
            rows.append(
                {
                    "image_id": row["image_id"],
                    "source_path": row["source_path"],
                    "rendered_path": row["rendered_path"],
                    "usage": row["usage"],
                    "caption_or_slide": row["caption_or_slide"],
                    "total_score": score,
                    "status": row["status"],
                    "source_sha256": sha256(source),
                    "rendered_sha256": sha256(rendered),
                    "source_exists": source.exists(),
                    "rendered_exists": rendered.exists(),
                }
            )
    return rows


def extract_supplement_figures() -> list[dict[str, str]]:
    text = SUPPLEMENT.read_text(encoding="utf-8")
    in_table = False
    figures: list[dict[str, str]] = []
    for line in text.splitlines():
        if line.strip() == "## Supplementary figures":
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if in_table and line.startswith("| Supplementary Figure"):
            parts = [part.strip() for part in line.strip().strip("|").split("|")]
            if len(parts) >= 3:
                file_match = re.search(r"`([^`]+)`", parts[2])
                figures.append(
                    {
                        "number": parts[0],
                        "title": parts[1],
                        "primary_file": file_match.group(1) if file_match else parts[2],
                    }
                )
    return figures


def extract_main_callouts() -> list[str]:
    text = PAPER.read_text(encoding="utf-8")
    return sorted(set(re.findall(r"Figure~\\ref\{([^}]+)\}", text)))


def validate(rows: list[dict[str, object]], supplement_figures: list[dict[str, str]], callouts: list[str]) -> list[str]:
    errors: list[str] = []
    for row in rows:
        if row["total_score"] != 100:
            errors.append(f"{row['image_id']} score is {row['total_score']}, expected 100")
        if not row["source_exists"]:
            errors.append(f"{row['image_id']} source missing: {row['source_path']}")
        if not row["rendered_exists"]:
            errors.append(f"{row['image_id']} rendered output missing: {row['rendered_path']}")
    found = {fig["number"]: fig["primary_file"] for fig in supplement_figures}
    if set(found) != set(EXPECTED_SUPPLEMENT_FIGURES):
        errors.append(f"supplementary figure numbers changed: {sorted(found)}")
    for number, expected_path in EXPECTED_SUPPLEMENT_FIGURES.items():
        if found.get(number) != expected_path:
            errors.append(f"{number} primary file is {found.get(number)!r}, expected {expected_path!r}")
    if set(callouts) != set(MAIN_MANUSCRIPT_CALLOUTS):
        errors.append(f"main manuscript figure callouts changed: {callouts}")
    return errors


def build_manifest() -> dict[str, object]:
    rows = read_scores()
    supplement_figures = extract_supplement_figures()
    callouts = extract_main_callouts()
    errors = validate(rows, supplement_figures, callouts)
    status = "frozen" if not errors else "needs-rescore"
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": status,
        "freeze_scope": "manuscript and supplement figure numbering, captions, placement callouts, source/rendered file hashes, and image score loop status",
        "rerun_required_when": RERUN_TRIGGERS,
        "main_manuscript_callouts": [
            {"label": label, "frozen_caption_intent": MAIN_MANUSCRIPT_CALLOUTS[label]} for label in sorted(MAIN_MANUSCRIPT_CALLOUTS)
        ],
        "supplementary_figures": supplement_figures,
        "image_score_rows": rows,
        "validation_errors": errors,
    }
    OUT_JSON.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    write_markdown(manifest)
    if errors:
        raise SystemExit("Figure/caption freeze requires rescore: " + "; ".join(errors))
    return manifest


def write_markdown(manifest: dict[str, object]) -> None:
    lines = [
        "# Figure and Caption Freeze Manifest",
        "",
        f"Generated: `{manifest['generated_at_utc']}`",
        f"Status: `{manifest['status']}`",
        "",
        "This manifest freezes manuscript and supplement figure numbering, caption intent, placement callouts, rendered/source file hashes, and image score-loop status. If any frozen surface changes, rerun the image scoring loop before submission.",
        "",
        "## Rerun Triggers",
        "",
    ]
    for item in manifest["rerun_required_when"]:  # type: ignore[index]
        lines.append(f"- {item}")
    lines += ["", "## Main Manuscript Figure Callouts", "", "| Label | Frozen caption intent |", "| --- | --- |"]
    for item in manifest["main_manuscript_callouts"]:  # type: ignore[index]
        lines.append(f"| `{item['label']}` | {item['frozen_caption_intent']} |")
    lines += ["", "## Supplementary Figures", "", "| Number | Title | Primary file |", "| --- | --- | --- |"]
    for fig in manifest["supplementary_figures"]:  # type: ignore[index]
        lines.append(f"| {fig['number']} | {fig['title']} | `{fig['primary_file']}` |")
    lines += ["", "## Image Score Freeze", "", "| Image ID | Rendered path | Score | Source SHA-256 | Rendered SHA-256 |", "| --- | --- | ---: | --- | --- |"]
    for row in manifest["image_score_rows"]:  # type: ignore[index]
        lines.append(
            f"| `{row['image_id']}` | `{row['rendered_path']}` | {row['total_score']} | `{row['source_sha256']}` | `{row['rendered_sha256']}` |"
        )
    lines += ["", "## Validation", ""]
    errors = manifest["validation_errors"]  # type: ignore[index]
    if errors:
        for error in errors:
            lines.append(f"- FAIL: {error}")
    else:
        lines.append("- PASS: all frozen image score rows are 100/100, source/rendered files exist, supplement figures S1-S7 match the frozen numbering, and manuscript callouts match the frozen labels.")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    manifest = build_manifest()
    print(f"Figure/caption freeze {manifest['status']}: {rel(OUT_JSON)}")
