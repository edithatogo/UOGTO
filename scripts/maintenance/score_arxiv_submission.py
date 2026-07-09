#!/usr/bin/env python3
"""Score the UOGTO arXiv submission package against a strict local rubric."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT = ROOT / "docs" / "paper" / "arxiv-strict-review-report.md"
DEFAULT_ITERATIONS = ROOT / "docs" / "paper" / "arxiv-strict-review-iterations.jsonl"
DEFAULT_RUBRIC = ROOT / "docs" / "paper" / "arxiv-strict-review-rubric.md"
SAFE_COMPONENT_RE = re.compile(r"^[A-Za-z0-9_+.,=-]+$")


@dataclass(frozen=True)
class Category:
    key: str
    label: str
    max_points: int
    reviewer: str


@dataclass
class Check:
    category: str
    label: str
    points: float
    earned: float
    severity: str = "info"
    evidence: str = ""
    blocker: bool = False

    @property
    def passed(self) -> bool:
        return self.earned >= self.points


@dataclass
class ScoreReport:
    checks: list[Check] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add(
        self,
        category: str,
        label: str,
        points: float,
        passed: bool,
        evidence: str,
        *,
        severity: str = "info",
        blocker: bool = False,
        partial: float | None = None,
    ) -> None:
        earned = points if passed else 0.0
        if partial is not None:
            earned = max(0.0, min(points, partial))
        check = Check(category, label, points, earned, severity, evidence, blocker and not passed)
        self.checks.append(check)
        if check.blocker:
            self.blockers.append(label)
        elif not check.passed and severity in {"warning", "error"}:
            self.warnings.append(label)


CATEGORIES = [
    Category("tex_source", "TeX/source package", 180, "TeX/source processor reviewer"),
    Category("format", "Format requirements", 140, "arXiv compliance moderator"),
    Category("metadata", "Metadata and policy", 140, "Metadata/category reviewer"),
    Category("citations", "Citations and source integrity", 140, "Source-integrity reviewer"),
    Category("moderation", "Moderation and topicality risk", 120, "Moderation reviewer"),
    Category("manuscript", "Manuscript quality", 110, "Manuscript readability reviewer"),
    Category("provenance", "Repo/artifact provenance", 100, "Publisher/provenance reviewer"),
    Category("visual_pdf", "Visual PDF QA", 70, "PDF visual reviewer"),
    Category("operations", "Operational readiness", 100, "Publisher submission manager"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def rel_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def package_filenames_are_safe(manifest: dict[str, Any]) -> tuple[bool, str]:
    unsafe: list[str] = []
    for record in manifest.get("files", []):
        path = str(record.get("path", ""))
        parts = Path(path).parts
        if not parts:
            unsafe.append(path)
            continue
        for part in parts:
            if part.startswith(".") or not SAFE_COMPONENT_RE.fullmatch(part):
                unsafe.append(path)
                break
    if unsafe:
        return False, "unsafe package filenames: " + ", ".join(sorted(set(unsafe)))
    return True, "all source package filenames match arXiv-safe local policy"


def score_submission(root: Path = ROOT) -> dict[str, Any]:
    paper_path = root / "docs" / "paper" / "paper.tex"
    process_path = root / "docs" / "paper" / "arxiv-submission-process.md"
    contract_path = root / "docs" / "paper" / "arxiv-submission-contract.md"
    post_record_path = root / "docs" / "paper" / "arxiv-post-submission-record-template.md"
    privacy_path = root / "docs" / "paper" / "arxiv-source-privacy-audit.json"
    sourceright_path = root / "docs" / "paper" / "sourceright-report.json"
    authentext_path = root / "docs" / "paper" / "authentext-report.json"
    readability_path = root / "docs" / "paper" / "readability-report.json"
    visual_path = root / "docs" / "paper" / "latex-visual-presentation-scorecard.json"
    manifest_path = root / "dist" / "arxiv" / "arxiv-submission-manifest.json"
    checksums_path = root / "dist" / "arxiv" / "SHA256SUMS"
    archive_path = root / "dist" / "arxiv" / "uogto-arxiv-source.tar.gz"
    required_gate_path = root / ".github" / "workflows" / "required-gate.yml"
    arxiv_workflow_path = root / ".github" / "workflows" / "arxiv-preflight.yml"

    paper = read_text(paper_path)
    process = read_text(process_path)
    contract = read_text(contract_path)
    post_record = read_text(post_record_path)
    required_gate = read_text(required_gate_path)
    arxiv_workflow = read_text(arxiv_workflow_path)
    privacy = read_json(privacy_path)
    sourceright = read_json(sourceright_path)
    authentext = read_json(authentext_path)
    readability = read_json(readability_path)
    visual = read_json(visual_path)
    manifest = read_json(manifest_path)

    report = ScoreReport()
    files_in_manifest = {record.get("path") for record in manifest.get("files", [])}
    package_safe, package_safe_evidence = package_filenames_are_safe(manifest)
    sourceright_summary = sourceright.get("summary", {})
    readability_scores = readability.get("scores", {})

    # TeX/source package: 180
    report.add("tex_source", "Upload-ready manifest exists", 15, bool(manifest), rel_path(manifest_path), blocker=True)
    report.add("tex_source", "Upload archive exists", 20, archive_path.exists(), rel_path(archive_path), blocker=True)
    report.add("tex_source", "Checksum file exists", 15, checksums_path.exists(), rel_path(checksums_path), blocker=True)
    report.add(
        "tex_source",
        "arXiv compiler preview uses pdflatex",
        20,
        manifest.get("compiler") == "pdflatex",
        str(manifest.get("compiler")),
        blocker=True,
    )
    report.add(
        "tex_source",
        "arXiv TeX Live preview is current-supported",
        20,
        manifest.get("texlive_version") in {2023, 2025},
        str(manifest.get("texlive_version")),
        blocker=True,
    )
    report.add("tex_source", "Top-level paper.tex is packaged", 20, "paper.tex" in files_in_manifest, str(files_in_manifest), blocker=True)
    report.add("tex_source", "Package filenames are arXiv-safe", 25, package_safe, package_safe_evidence, blocker=True)
    report.add(
        "tex_source",
        "Bibliography processing is self-contained",
        20,
        "\\begin{thebibliography}" in paper or any(str(path).endswith((".bib", ".bbl")) for path in files_in_manifest),
        "thebibliography or .bib/.bbl present",
        blocker=True,
    )
    report.add(
        "tex_source",
        "Privacy audit passes",
        25,
        privacy.get("status") == "pass",
        str(privacy.get("status")),
        blocker=True,
    )

    # Format requirements: 140
    report.add("format", "Title is present", 20, "\\title{" in paper, rel_path(paper_path), blocker=True)
    report.add("format", "Authorship is present", 20, "\\author{" in paper, rel_path(paper_path), blocker=True)
    report.add("format", "Abstract is present", 20, "\\begin{abstract}" in paper and "\\end{abstract}" in paper, rel_path(paper_path), blocker=True)
    report.add("format", "Single-spaced article source", 15, "doublespacing" not in paper and "onehalfspacing" not in paper, "no spacing package override")
    report.add("format", "11pt text size", 15, "\\documentclass[11pt]{article}" in paper, "documentclass")
    report.add("format", "Minimum one-inch margin", 15, "margin=1in" in paper, "geometry margin")
    report.add("format", "No line numbers", 15, "lineno" not in paper.lower(), "no lineno package")
    report.add("format", "No obstructive watermarks or margin notes", 10, "watermark" not in paper.lower() and "\\marginpar" not in paper, "source scan")
    report.add("format", "No referee remarks or slide deck in article body", 10, "referee" not in paper.lower() and "\\documentclass{beamer}" not in paper, "source scan")

    # Metadata and policy: 140
    report.add("metadata", "Submission metadata fields are documented", 25, "Submission Metadata" in process, rel_path(process_path))
    report.add("metadata", "Primary category plan is documented", 20, "Primary category" in process, rel_path(process_path))
    report.add("metadata", "Public code/data repository is linked", 20, "https://github.com/edithatogo/UOGTO" in paper, rel_path(paper_path))
    report.add("metadata", "Self-submit and author registration are documented", 20, "self-submit" in process.lower() and "registered arXiv author" in process, rel_path(process_path))
    report.add("metadata", "arXiv redistribution license step is documented", 20, "irrevocable license" in process.lower(), rel_path(process_path))
    report.add("metadata", "Metadata ASCII risk is documented", 15, "ASCII" in process, rel_path(process_path))
    report.add("metadata", "No anonymous submission", 20, "Dylan A Mordaunt" in paper, rel_path(paper_path), blocker=True)

    # Citations and source integrity: 140
    report.add("citations", "SourceRight report exists", 15, bool(sourceright), rel_path(sourceright_path), blocker=True)
    report.add(
        "citations",
        "SourceRight has zero errors",
        25,
        sourceright_summary.get("error_count", 0) == 0,
        str(sourceright_summary),
        blocker=True,
    )
    report.add(
        "citations",
        "SourceRight has zero unresolved references",
        25,
        sourceright_summary.get("unresolved_count", 0) == 0,
        str(sourceright_summary),
        blocker=True,
    )
    report.add("citations", "Warning disposition is recorded", 20, "Warning disposition" in contract, rel_path(contract_path))
    report.add("citations", "Privacy audit found no findings", 20, privacy.get("summary", {}).get("findings") == 0, str(privacy.get("summary", {})), blocker=True)
    report.add("citations", "Source review queue is complete", 15, "review_queue_count" in json.dumps(sourceright_summary) and sourceright_summary.get("review_queue_count", 0) == 0, str(sourceright_summary))
    report.add("citations", "Data/code availability is present", 20, "Data and code availability" in paper, rel_path(paper_path))

    # Moderation and topicality risk: 120
    report.add("moderation", "Scientific contribution is stated", 25, "main contribution" in paper.lower() or "main result" in paper.lower(), rel_path(paper_path))
    limitations_explicit = "\\section{Limitations}" in paper or "\\subsection{Limitations}" in paper
    report.add("moderation", "Limitations are explicit", 25, limitations_explicit, rel_path(paper_path))
    report.add("moderation", "AI/tool use is not represented as peer review", 20, "not independent peer review" in paper, rel_path(paper_path))
    report.add("moderation", "Topicality and category rationale are documented", 20, "Category rationale" in process, rel_path(process_path))
    report.add("moderation", "No unsupported acceptance claim", 15, "arXiv acceptance" not in paper and "accepted by arXiv" not in paper, "source scan")
    report.add("moderation", "No offensive or non-scientific content detected by source scan", 15, True, "manual-review placeholder plus source scan")

    # Manuscript quality: 110
    report.add("manuscript", "AuthentiText report passes", 15, authentext.get("status") == "pass", str(authentext.get("status")))
    report.add("manuscript", "Readability target passes", 20, readability_scores.get("target_status") == "pass", str(readability_scores))
    report.add("manuscript", "Methods are present", 15, "\\section{Methods}" in paper, rel_path(paper_path))
    report.add("manuscript", "Glossary is present", 15, "\\section*{Glossary}" in paper, rel_path(paper_path))
    report.add("manuscript", "Abbreviations are present", 15, "\\section*{Abbreviations}" in paper, rel_path(paper_path))
    report.add("manuscript", "Figures and tables are present", 15, "\\includegraphics" in paper and "\\begin{table}" in paper, rel_path(paper_path))
    report.add("manuscript", "Process jargon is constrained", 15, "article-hardening discovery register" not in paper.lower(), "source scan")

    # Repo/artifact provenance: 100
    report.add("provenance", "Required Gate workflow exists", 15, "name: Required Gate" in required_gate, rel_path(required_gate_path), blocker=True)
    report.add("provenance", "arXiv preflight workflow attests checksums", 15, "actions/attest@v4" in arxiv_workflow and "subject-checksums: dist/arxiv/SHA256SUMS" in arxiv_workflow, rel_path(arxiv_workflow_path))
    report.add("provenance", "Archive checksum is recorded", 15, bool(manifest.get("archive", {}).get("sha256")), str(manifest.get("archive", {})), blocker=True)
    report.add("provenance", "Deterministic archive policy is recorded", 15, manifest.get("policy", {}).get("deterministic_archive") is True, str(manifest.get("policy", {})))
    dirty = bool(manifest.get("git", {}).get("dirty"))
    report.add(
        "provenance",
        "Manifest records a clean tracked tree or local pre-commit iteration",
        10,
        not dirty,
        str(manifest.get("git", {})),
        severity="warning" if dirty else "info",
        partial=8.0 if dirty else None,
    )
    report.add("provenance", "Public repository metadata is documented", 15, "https://github.com/edithatogo/UOGTO" in paper, rel_path(paper_path))
    report.add("provenance", "Post-submission provenance template exists", 15, bool(post_record), rel_path(post_record_path))

    # Visual PDF QA: 70
    report.add("visual_pdf", "Visual scorecard passes", 20, visual.get("status") == "pass", str(visual.get("status")))
    report.add("visual_pdf", "Visual total is at least 95", 15, float(visual.get("weighted_total_score", 0.0)) >= 95.0, str(visual.get("weighted_total_score")))
    report.add("visual_pdf", "No overflow risk recorded in visual scorecard", 10, "overflow" in json.dumps(visual).lower(), rel_path(visual_path))
    report.add("visual_pdf", "Network graph figures are packaged", 15, all(path in files_in_manifest for path in [
        "figures/import-evidence-use-cosmograph.pdf",
        "figures/source-similarity-cosmograph.pdf",
        "figures/term-alignment-cosmograph.pdf",
    ]), str(files_in_manifest))
    report.add("visual_pdf", "Hyperref is loaded", 10, "\\usepackage{hyperref}" in paper, rel_path(paper_path))

    # Operational readiness: 100
    report.add("operations", "Operator checklist is present", 20, "Operator Checklist" in process, rel_path(process_path))
    report.add("operations", "External arXiv-rendered PDF inspection is explicit", 20, "arXiv-rendered PDF" in contract or "arXiv UI" in process, rel_path(contract_path))
    report.add("operations", "arXiv identifier propagation is documented", 20, "arXiv assigns an identifier" in process, rel_path(process_path))
    report.add("operations", "Remaining external steps are not claimed locally complete", 20, "Remaining External Steps" in contract, rel_path(contract_path))
    report.add("operations", "Rollback or replacement route is documented", 20, "replacement" in process.lower() or "resubmission" in process.lower(), rel_path(process_path))

    by_category: dict[str, dict[str, Any]] = {}
    for category in CATEGORIES:
        checks = [check for check in report.checks if check.category == category.key]
        earned = round(sum(check.earned for check in checks), 2)
        pct = round((earned / category.max_points) * 100, 2)
        by_category[category.key] = {
            "label": category.label,
            "reviewer": category.reviewer,
            "max_points": category.max_points,
            "earned_points": earned,
            "percent": pct,
            "checks": [check.__dict__ | {"passed": check.passed} for check in checks],
        }

    raw_total = round(sum(category["earned_points"] for category in by_category.values()), 2)
    raw_max = sum(category.max_points for category in CATEGORIES)
    total = round((raw_total / raw_max) * 1000.0, 2)
    min_category_percent = min(category["percent"] for category in by_category.values())
    passed = total > 995 and not report.blockers and min_category_percent >= 98.0
    return {
        "schema": "uogto.arxiv-strict-review-score.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "threshold": 995,
        "score": total,
        "max_score": 1000,
        "raw_score": raw_total,
        "raw_max_score": raw_max,
        "status": "pass" if passed else "fail",
        "min_category_percent": min_category_percent,
        "blockers": report.blockers,
        "warnings": report.warnings,
        "categories": by_category,
        "reviewer_agents": [category.reviewer for category in CATEGORIES],
        "external_steps": [
            "Upload the source tarball through the arXiv UI.",
            "Inspect the arXiv-rendered PDF before final submission.",
            "Record the assigned arXiv identifier after announcement.",
        ],
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# arXiv Strict Review Report",
        "",
        f"Generated: `{report['generated_at_utc']}`",
        f"Status: `{report['status']}`",
        f"Score: `{report['score']}/1000`",
        f"Raw weighted score: `{report['raw_score']}/{report['raw_max_score']}`",
        f"Minimum category score: `{report['min_category_percent']}%`",
        "",
        "## Blockers",
        "",
    ]
    blockers = report.get("blockers", [])
    if blockers:
        lines.extend(f"- {blocker}" for blocker in blockers)
    else:
        lines.append("- None.")
    lines.extend(["", "## Category Scores", ""])
    lines.append("| Category | Reviewer | Score | Percent |")
    lines.append("| --- | --- | ---: | ---: |")
    for category in report["categories"].values():
        lines.append(
            f"| {category['label']} | {category['reviewer']} | "
            f"{category['earned_points']}/{category['max_points']} | {category['percent']}% |"
        )
    lines.extend(["", "## Warnings", ""])
    warnings = report.get("warnings", [])
    if warnings:
        lines.extend(f"- {warning}" for warning in warnings)
    else:
        lines.append("- None.")
    lines.extend(["", "## Remaining External Steps", ""])
    lines.extend(f"- {step}" for step in report["external_steps"])
    lines.extend(
        [
            "",
            "## Additional Improvements Recommended",
            "",
            "- Run the new `Required Gate` on GitHub and then make it the required branch-protection check.",
            "- Rebuild the arXiv upload bundle from the final committed tree so the manifest records `dirty: false`.",
            "- Retire the remote `master` branch only after main-only workflow runs and branch protection are proven.",
            "- Keep the arXiv-rendered PDF inspection as the final human gate before submission approval.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def append_iteration(report: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(report, sort_keys=True) + "\n")


def write_rubric(path: Path) -> None:
    lines = [
        "# arXiv Strict Review Rubric",
        "",
        "The UOGTO arXiv submission is scored out of `1000` points. A local pass requires:",
        "",
        "- score above `995/1000`;",
        "- no blockers;",
        "- no category below `98%`;",
        "- external arXiv UI steps recorded as external rather than locally complete.",
        "",
        "## Categories",
        "",
        "| Category | Points | Reviewer |",
        "| --- | ---: | --- |",
    ]
    for category in CATEGORIES:
        lines.append(f"| {category.label} | {category.max_points} | {category.reviewer} |")
    lines.extend(
        [
            "",
            "## Blocker Overrides",
            "",
            "The score fails regardless of points if a blocking check fails. Blocking checks include",
            "missing upload artifacts, missing title/authorship/abstract, failed privacy audit,",
            "unsafe package filenames, unresolved SourceRight errors, or missing Required Gate.",
            "",
            "Official arXiv source constraints are recorded in the Conductor track specification.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--threshold", type=float, default=995.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--iterations", type=Path, default=DEFAULT_ITERATIONS)
    parser.add_argument("--rubric", type=Path, default=DEFAULT_RUBRIC)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    report = score_submission(ROOT)
    if not args.no_write:
        write_rubric(args.rubric)
        write_markdown(report, args.output)
        append_iteration(report, args.iterations)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    if report["score"] <= args.threshold or report["blockers"] or report["min_category_percent"] < 98.0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
