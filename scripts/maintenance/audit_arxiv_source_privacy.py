#!/usr/bin/env python3
"""Audit cleaned arXiv source packages for source-leak and privacy risks."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

try:
    from scripts.maintenance.build_arxiv_source_package import build_package
    from scripts.maintenance.clean_arxiv_source_package import (
        AUXILIARY_SUFFIXES,
        DEFAULT_OUTPUT_DIR,
        parse_tex_references,
        resolve_default_package_dir,
    )
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from scripts.maintenance.build_arxiv_source_package import build_package
    from scripts.maintenance.clean_arxiv_source_package import (
        AUXILIARY_SUFFIXES,
        DEFAULT_OUTPUT_DIR,
        parse_tex_references,
        resolve_default_package_dir,
    )


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JSON = Path("docs/paper/arxiv-source-privacy-audit.json")
DEFAULT_MD = Path("docs/paper/arxiv-source-privacy-audit.md")
TEXT_SUFFIXES = {".tex", ".bib", ".bbl", ".sty", ".cls", ".cfg", ".def", ".md", ".txt"}
FIGURE_SUFFIXES = {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".eps"}
METADATA_SUFFIXES = FIGURE_SUFFIXES
PRIVATE_NAME_RE = re.compile(
    r"(^|[-_.])(private|confidential|referee|referees|reviewer|journal[-_]?template|hidden|notes?[-_]?to[-_]?self)([-_.]|$)",
    re.I,
)
SUSPICIOUS_COMMENT_RE = re.compile(
    r"\b(todo|fixme|note to self|private|confidential|internal|referee|reviewer|password|passwd|secret|token|"
    r"api[-_ ]?key|client[-_ ]?secret|access[-_ ]?token|bearer|localhost|127\.0\.0\.1|one ?drive|dropbox)\b|"
    r"file://|[A-Za-z]:\\",
    re.I,
)
CREDENTIAL_RE = re.compile(
    r"(ghp_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|"
    r"xox[baprs]-[A-Za-z0-9-]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|"
    r"\b(?:password|passwd|api[_-]?key|client[_-]?secret|access[_-]?token|secret)\s*[:=]\s*[^\s{}]{6,}|"
    r"\bBearer\s+[A-Za-z0-9._~+/=-]{12,})",
    re.I,
)
PRIVATE_URL_RE = re.compile(
    r"(https?://(?:localhost|127\.0\.0\.1|10\.|192\.168\.|172\.(?:1[6-9]|2[0-9]|3[01])\.)[^\s{}<>]*|"
    r"file://[^\s{}<>]*|[A-Za-z]:[\\/](?:Users|tmp|Temp|Windows|Program Files)[^\s{}<>]*|"
    r"(?<![A-Za-z0-9_.-])/(?:Users|home|tmp|var/tmp)/[^\s{}<>]*|(?<![A-Za-z0-9])\\\\[A-Za-z0-9_.-]+\\[^\s{}<>]+)",
    re.I,
)
PDF_METADATA_RE = re.compile(
    rb"/(Author|Creator|Producer|Title|Subject|Keywords|CreationDate|ModDate)\s*(?:\(([^)]{0,160})\)|<([^>]{0,320})>)"
)
IMAGE_METADATA_RE = re.compile(rb"(Exif|XMP|tEXt|iTXt|zTXt|Software|Author|Creator|Description)")


@dataclass
class Finding:
    category: str
    severity: str
    path: str
    detail: str
    line: int | None = None


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def display_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return resolved.name


def iter_files(package_dir: Path):
    for path in sorted(package_dir.rglob("*")):
        if path.is_file():
            yield path


def is_escaped_percent(line: str, idx: int) -> bool:
    backslashes = 0
    pos = idx - 1
    while pos >= 0 and line[pos] == "\\":
        backslashes += 1
        pos -= 1
    return backslashes % 2 == 1


def latex_comment_text(line: str) -> str | None:
    for idx, char in enumerate(line):
        if char == "%" and not is_escaped_percent(line, idx):
            return line[idx + 1 :].strip()
    return None


def collect_tex_references(package_dir: Path) -> set[str]:
    refs: set[str] = set()
    for tex in package_dir.rglob("*.tex"):
        try:
            parsed = parse_tex_references(tex)
            if isinstance(parsed, tuple):
                for group in parsed:
                    refs.update(group)
            else:
                refs.update(parsed)
        except Exception:
            pass
    return refs


def referenced_figure(path: Path, package_dir: Path, references: set[str]) -> bool:
    relative = rel(path, package_dir)
    no_suffix = str(Path(relative).with_suffix(""))
    return bool({relative, no_suffix, path.name, path.stem} & references)


def audit_package(package_dir: Path, cleaner_manifest: Path | None = None) -> dict:
    findings: list[Finding] = []
    files = list(iter_files(package_dir))
    text_files = [p for p in files if p.suffix.lower() in TEXT_SUFFIXES]
    metadata_files = [p for p in files if p.suffix.lower() in METADATA_SUFFIXES]
    comment_lines = 0
    suspicious_comment_lines = 0
    metadata_records = []
    references = collect_tex_references(package_dir)

    for path in files:
        relative_path = rel(path, package_dir)
        if any(part.startswith(".") for part in path.relative_to(package_dir).parts):
            findings.append(Finding("hidden_files", "fail", relative_path, "Hidden path present in arXiv package"))
        if PRIVATE_NAME_RE.search(path.name):
            findings.append(
                Finding(
                    "private_notes",
                    "fail",
                    relative_path,
                    "Filename matches private/referee/journal-template deny pattern",
                )
            )
        if path.suffix.lower() in AUXILIARY_SUFFIXES:
            findings.append(
                Finding("aux_log_output_files", "fail", relative_path, "Auxiliary, log, or generated output file present")
            )
        if path.suffix.lower() in FIGURE_SUFFIXES and not referenced_figure(path, package_dir, references):
            findings.append(Finding("unused_figures", "fail", relative_path, "Figure asset is not referenced by package TeX sources"))

    for path in text_files:
        relative_path = rel(path, package_dir)
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(text.splitlines(), start=1):
            comment = latex_comment_text(line) if path.suffix.lower() in {".tex", ".sty", ".cls", ".bib", ".bbl"} else None
            if comment:
                comment_lines += 1
                if SUSPICIOUS_COMMENT_RE.search(comment):
                    suspicious_comment_lines += 1
                    findings.append(
                        Finding(
                            "comments",
                            "fail",
                            relative_path,
                            "Suspicious LaTeX/comment text: " + comment[:140],
                            line_no,
                        )
                    )
            if CREDENTIAL_RE.search(line):
                findings.append(Finding("credentials", "fail", relative_path, "Credential-like token or assignment detected", line_no))
            for match in PRIVATE_URL_RE.finditer(line):
                findings.append(
                    Finding(
                        "private_urls",
                        "fail",
                        relative_path,
                        "Private URL, local path, or UNC path detected: " + match.group(0)[:140],
                        line_no,
                    )
                )

    for path in metadata_files:
        relative_path = rel(path, package_dir)
        data = path.read_bytes()
        keys = []
        private_hits = []
        if path.suffix.lower() == ".pdf":
            for match in PDF_METADATA_RE.finditer(data[:262144]):
                key = match.group(1).decode("ascii", errors="replace")
                value = (match.group(2) or match.group(3) or b"").decode("utf-8", errors="replace")
                keys.append(key)
                if CREDENTIAL_RE.search(value) or PRIVATE_URL_RE.search(value) or SUSPICIOUS_COMMENT_RE.search(value):
                    private_hits.append(f"{key}={value[:80]}")
        elif IMAGE_METADATA_RE.search(data[:262144]):
            keys.append("image_metadata_marker")
            head = data[:262144].decode("latin-1", errors="ignore")
            if CREDENTIAL_RE.search(head) or PRIVATE_URL_RE.search(head):
                private_hits.append("image metadata contains private-looking text")
        if keys:
            metadata_records.append(
                {
                    "path": relative_path,
                    "metadata_keys": sorted(set(keys)),
                    "private_hits": private_hits,
                }
            )
        for hit in private_hits:
            findings.append(Finding("embedded_metadata", "fail", relative_path, "Private-looking embedded metadata: " + hit[:140]))

    cleaner_data = None
    if cleaner_manifest and cleaner_manifest.exists():
        cleaner_data = json.loads(cleaner_manifest.read_text(encoding="utf-8"))

    checks = {
        key: {"status": "pass", "count": 0}
        for key in [
            "hidden_files",
            "private_notes",
            "unused_figures",
            "aux_log_output_files",
            "credentials",
            "private_urls",
        ]
    }
    checks["comments"] = {
        "status": "pass" if suspicious_comment_lines == 0 else "fail",
        "comment_lines": comment_lines,
        "suspicious_comment_lines": suspicious_comment_lines,
    }
    checks["embedded_metadata"] = {
        "status": "not_applicable" if len(metadata_files) == 0 else "pass",
        "metadata_files_reviewed": len(metadata_files),
        "metadata_bearing_files": len(metadata_records),
        "private_metadata_hits": 0,
    }

    for category in checks:
        failures = [finding for finding in findings if finding.category == category]
        if failures:
            checks[category]["status"] = "fail"
            checks[category]["count"] = len(failures)
            if category == "embedded_metadata":
                checks[category]["private_metadata_hits"] = len(failures)

    fail_count = sum(1 for finding in findings if finding.severity == "fail")
    return {
        "schema": "uogto.arxiv-source-privacy-audit.v1",
        "generated_at_utc": "deterministic-local-preflight",
        "package_dir": display_path(package_dir),
        "cleaner_manifest": display_path(cleaner_manifest) if cleaner_manifest else None,
        "status": "pass" if fail_count == 0 else "fail",
        "summary": {
            "files_reviewed": len(files),
            "text_files_reviewed": len(text_files),
            "metadata_files_reviewed": len(metadata_files),
            "comment_lines_reviewed": comment_lines,
            "findings": len(findings),
            "failures": fail_count,
            "metadata_bearing_files": len(metadata_records),
        },
        "checks": checks,
        "metadata_records": metadata_records,
        "cleaner_summary": cleaner_data.get("summary") if isinstance(cleaner_data, dict) else None,
        "findings": [asdict(finding) for finding in findings],
        "policy": {
            "failure_categories": [
                "comments",
                "hidden_files",
                "private_notes",
                "unused_figures",
                "aux_log_output_files",
                "embedded_metadata",
                "credentials",
                "private_urls",
            ],
            "embedded_metadata_rule": (
                "Metadata keys are recorded; only private-looking embedded values fail the audit."
            ),
            "scope": "Cleaned arXiv source package plus cleaner manifest evidence.",
        },
    }


def write_markdown(manifest: dict, path: Path) -> None:
    labels = {
        "comments": "Comments and disabled/draft blocks",
        "hidden_files": "Hidden files and directories",
        "private_notes": "Private notes, referee material, journal templates",
        "unused_figures": "Unused figures",
        "aux_log_output_files": "Auxiliary, log, and output files",
        "embedded_metadata": "Embedded PDF/image metadata",
        "credentials": "Credentials, private keys, and tokens",
        "private_urls": "Private URLs, local paths, and UNC paths",
    }
    rows = []
    for key, label in labels.items():
        check = manifest["checks"][key]
        detail = ", ".join(f"{k}={v}" for k, v in check.items() if k != "status") or "reviewed"
        rows.append(f"| {label} | {check['status']} | {detail} |")

    findings = manifest.get("findings", [])
    if findings:
        finding_lines = [
            f"- `{item['category']}` `{item['severity']}` `{item['path']}`"
            + (f":{item['line']}" if item.get("line") else "")
            + f" - {item['detail']}"
            for item in findings
        ]
    else:
        finding_lines = ["No failing source-leak or privacy findings were detected."]

    metadata = manifest.get("metadata_records", [])
    if metadata:
        metadata_lines = [
            f"- `{item['path']}`: {', '.join(item['metadata_keys'])}; private hits={len(item.get('private_hits', []))}"
            for item in metadata
        ]
    else:
        metadata_lines = ["No embedded metadata markers were detected in package figures/PDFs."]

    text = "\n".join(
        [
            "# arXiv Source-Leak and Privacy Audit",
            "",
            f"Generated: `{manifest['generated_at_utc']}`",
            f"Status: `{manifest['status']}`",
            f"Package: `{manifest['package_dir']}`",
            f"Cleaner manifest: `{manifest.get('cleaner_manifest')}`",
            "",
            "## Summary",
            "",
            "| Check | Status | Evidence |",
            "| --- | --- | --- |",
            *rows,
            "",
            "## Findings",
            "",
            *finding_lines,
            "",
            "## Embedded Metadata Review",
            "",
            *metadata_lines,
            "",
            "## Scope and Policy",
            "",
            "This manifest audits the cleaned arXiv source package, not the full working tree. The repository-native "
            "cleaner remains the authoritative packaging gate. Benign PDF/image metadata keys are recorded for "
            "reviewer inspection; credential-like or private-location values are treated as failing source-leak findings.",
            "",
        ]
    )
    path.write_text(text, encoding="utf-8")


def resolve_package(package_dir: Path | None, build_if_missing: bool) -> tuple[Path, Path | None]:
    if package_dir is not None:
        resolved = package_dir.resolve()
    else:
        try:
            resolved = resolve_default_package_dir(DEFAULT_OUTPUT_DIR).resolve()
        except FileNotFoundError:
            if not build_if_missing:
                raise
            resolved = build_package().package_dir.resolve()
    manifests = sorted(
        resolved.parent.glob(resolved.name + ".manifest.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return resolved, manifests[0] if manifests else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-dir", type=Path, default=None)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MD)
    parser.add_argument("--no-build", action="store_true")
    args = parser.parse_args(argv)

    package_dir, cleaner_manifest = resolve_package(args.package_dir, build_if_missing=not args.no_build)
    manifest = audit_package(package_dir, cleaner_manifest)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(manifest, args.markdown)
    print(f"arXiv source privacy audit {manifest['status']}: {args.json}")
    return 0 if manifest["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
