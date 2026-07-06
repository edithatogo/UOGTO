"""Synchronize UOGTO Conductor tracks with GitHub Projects.

This script is intentionally GitHub-CLI backed because GitHub Projects v2
field and subissue support is broader in the local `gh` CLI than in the
connector surface used by Codex.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


OWNER = "edithatogo"
REPO = "edithatogo/UOGTO"
UOGTO_PROJECT = 8
RIHERO_PROJECT = 9
TODAY = date.today().isoformat()

STATUS_DONE = "Done"
STATUS_IN_PROGRESS = "In Progress"

UOGTO_PROJECT_FIELDS: dict[str, tuple[str, list[str]]] = {
    "Workstream": (
        "SINGLE_SELECT",
        [
            "RI-HERO synthesis",
            "Conductor",
            "Ontology",
            "Validation",
            "Publishing",
            "Registry",
            "Research",
            "Manuscript",
            "Maintenance",
        ],
    ),
    "Exposure": (
        "SINGLE_SELECT",
        ["Internal", "Repo", "External", "Published", "Monitoring"],
    ),
    "Layer": (
        "SINGLE_SELECT",
        ["Epic", "Workstream", "Track", "Pull request", "External dependency", "Monitoring"],
    ),
    "Gate Type": (
        "SINGLE_SELECT",
        ["Repo-local", "CI/validation", "External review", "External submission", "Monitoring", "Historical"],
    ),
    "Issue Role": (
        "SINGLE_SELECT",
        ["Umbrella", "Workstream", "Conductor track", "Development PR", "Registry follow-up", "External gate"],
    ),
    "Track ID": ("TEXT", []),
    "Track Location": ("TEXT", []),
    "Synced": ("DATE", []),
}

LABELS = {
    "conductor-track": ("Mirror of a local Conductor track.", "7C3AED"),
    "track-complete": ("Completed Conductor track.", "2DA44E"),
    "track-active": ("Active or in-progress Conductor track.", "D97706"),
    "track-archived": ("Archived Conductor track retained for audit history.", "6B7280"),
    "project-ledger": ("GitHub Projects synchronization ledger item.", "0969DA"),
}

PARENT_ISSUES = {
    "Conductor": 5,
    "Maintenance": 6,
    "Ontology": 8,
    "Validation": 11,
    "Publishing": 13,
    "Registry": 13,
    "Research": 10,
    "Manuscript": 14,
}

MILESTONES = {
    "Conductor": "RI-HERO - implementation",
    "Maintenance": "RI-HERO - monitoring and maintenance",
    "Ontology": "RI-HERO - implementation",
    "Validation": "RI-HERO - implementation",
    "Publishing": "RI-HERO - publication and registry",
    "Registry": "RI-HERO - publication and registry",
    "Research": "RI-HERO - implementation",
    "Manuscript": "RI-HERO - implementation",
}

WORKSTREAM_LABELS = {
    "Conductor": ["ri-hero", "ri-hero-conductor"],
    "Maintenance": ["ri-hero", "ri-hero-maintenance"],
    "Ontology": ["ri-hero", "ri-hero-ontology", "ontology-change"],
    "Validation": ["ri-hero", "ri-hero-validation", "validation"],
    "Publishing": ["ri-hero", "ri-hero-publishing"],
    "Registry": ["ri-hero", "ri-hero-publishing", "ri-hero-registry"],
    "Research": ["ri-hero", "ri-hero-research"],
    "Manuscript": ["ri-hero", "ri-hero-research", "documentation"],
}

TRACK_OVERRIDES: dict[str, dict[str, str]] = {
    "uogto_bootstrap_20260620": {
        "workstream": "Conductor",
        "gate_type": "Repo-local",
        "description": "Bootstrap the UOGTO repository, ontology scaffold, examples, validation, and initial track context.",
    },
    "uogto_core_ontology_20260620": {"workstream": "Ontology", "gate_type": "Repo-local", "parent_issue": "7"},
    "uogto_classical_cooperative_20260620": {"workstream": "Ontology", "gate_type": "Repo-local"},
    "uogto_information_epistemic_20260620": {"workstream": "Ontology", "gate_type": "Repo-local"},
    "uogto_dynamics_simulation_20260620": {"workstream": "Ontology", "gate_type": "Repo-local"},
    "uogto_mechanism_design_20260620": {"workstream": "Ontology", "gate_type": "Repo-local"},
    "uogto_marl_learning_20260620": {"workstream": "Ontology", "gate_type": "Repo-local"},
    "uogto_network_continuous_20260620": {"workstream": "Ontology", "gate_type": "Repo-local"},
    "uogto_norms_contracts_20260620": {"workstream": "Ontology", "gate_type": "Repo-local"},
    "uogto_llm_twins_20260620": {"workstream": "Ontology", "gate_type": "Repo-local"},
    "uogto_release_validation_20260620": {"workstream": "Validation", "gate_type": "CI/validation"},
    "repo_maintenance_20260621": {"workstream": "Maintenance", "gate_type": "Monitoring"},
    "maintenance_improvements_20260621": {"workstream": "Maintenance", "gate_type": "Historical"},
    "executable_simulation_visualizer_20260621": {"workstream": "Maintenance", "gate_type": "Historical"},
    "scoping_review_protocol_20260621": {"workstream": "Research", "gate_type": "Historical"},
    "systematic_literature_review_20260621": {"workstream": "Research", "gate_type": "Historical"},
    "scoping_review_execution_paper_20260621": {"workstream": "Research", "gate_type": "Repo-local"},
    "uogto_publishing_discoverability_20260622": {"workstream": "Publishing", "gate_type": "External review"},
    "conductor_state_reconciliation_20260622": {"workstream": "Conductor", "gate_type": "Repo-local"},
    "manuscript_source_verification_20260622": {"workstream": "Manuscript", "gate_type": "Repo-local"},
    "uogto_extended_discoverability_registries_20260622": {"workstream": "Registry", "gate_type": "External review"},
    "uogto_comparative_simulation_ontology_mapping_20260624": {"workstream": "Research", "gate_type": "Repo-local", "parent_issue": "12"},
    "uogto_article_hardening_protocol_20260624": {"workstream": "Research", "gate_type": "Repo-local"},
    "uogto_nature_presubmission_evaluation_20260625": {"workstream": "Manuscript", "gate_type": "External submission"},
    "repo_arxiv_submission_hardening_20260702": {"workstream": "Publishing", "gate_type": "External submission"},
    "repo_validation_runtime_hardening_20260703": {"workstream": "Validation", "gate_type": "CI/validation"},
    "uogto_validation_contract_coherence_20260705": {"workstream": "Validation", "gate_type": "CI/validation"},
    "uogto_registry_publication_followthrough_20260705": {"workstream": "Registry", "gate_type": "External review"},
    "uogto_interoperability_benchmarks_20260705": {"workstream": "Validation", "gate_type": "Repo-local"},
    "uogto_alignment_evidence_expansion_20260705": {"workstream": "Ontology", "gate_type": "Repo-local"},
    "uogto_manuscript_submission_revision_20260705": {"workstream": "Manuscript", "gate_type": "External submission"},
    "uogto_bioregistry_namespace_response_20260705": {"workstream": "Registry", "gate_type": "External review"},
}

EXISTING_TRACK_ISSUES = {
    "uogto_validation_contract_coherence_20260705": 27,
    "uogto_registry_publication_followthrough_20260705": 28,
    "uogto_interoperability_benchmarks_20260705": 29,
    "uogto_alignment_evidence_expansion_20260705": 30,
    "uogto_manuscript_submission_revision_20260705": 31,
    "uogto_bioregistry_namespace_response_20260705": 34,
}

WORKSTREAM_ISSUES = list(range(4, 17))


@dataclass
class Track:
    track_id: str
    title: str
    description: str
    location: str
    path: str
    status: str
    issue_state: str
    workstream: str
    gate_type: str


def run(args: list[str], *, input_text: str | None = None) -> str:
    completed = subprocess.run(
        args,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"{' '.join(args)} failed with exit code {completed.returncode}\n"
            f"stdout:\n{completed.stdout}\n\nstderr:\n{completed.stderr}"
        )
    return completed.stdout.strip()


def gh_json(args: list[str]) -> Any:
    output = run(["gh", *args])
    return json.loads(output) if output else None


def require_json(value: Any, context: str) -> Any:
    if value is None:
        raise RuntimeError(f"GitHub CLI returned no JSON for {context}")
    return value


def human_title(track_id: str) -> str:
    parts = track_id.split("_")
    if parts and re.fullmatch(r"20\d{6}", parts[-1]):
        parts = parts[:-1]
    words = []
    for part in parts:
        if part.lower() == "uogto":
            words.append("UOGTO")
        elif part.lower() == "llm":
            words.append("LLM")
        elif part.lower() == "marl":
            words.append("MARL")
        elif part.lower() == "arxiv":
            words.append("arXiv")
        else:
            words.append(part.capitalize())
    return " ".join(words)


def parse_track_registry(root: Path) -> dict[str, dict[str, str]]:
    text = (root / "conductor" / "tracks.md").read_text(encoding="utf-8")
    registry: dict[str, dict[str, str]] = {}
    pattern = re.compile(
        r"^## \[(?P<marker>[ x~])\] (?P<archived>Archived )?Track: (?P<track>[A-Za-z0-9_]+)\n"
        r"(?P<body>.*?)(?=^## \[[ x~]\] (?:Archived )?Track:|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    for match in pattern.finditer(text):
        body = match.group("body")
        description_match = re.search(r"^- \*\*Description\*\*: (?P<description>.+)$", body, re.MULTILINE)
        status_match = re.search(r"^- \*\*Status\*\*: (?P<status>.+)$", body, re.MULTILINE)
        registry[match.group("track")] = {
            "description": description_match.group("description").strip() if description_match else "",
            "marker": match.group("marker"),
            "status": status_match.group("status").strip() if status_match else "",
            "archived_heading": "true" if match.group("archived") else "false",
        }
    return registry


def parse_track_descriptions(root: Path) -> dict[str, str]:
    return {
        track_id: data["description"]
        for track_id, data in parse_track_registry(root).items()
        if data["description"]
    }


def metadata_status(path: Path) -> str:
    metadata_path = path / "metadata.json"
    if not metadata_path.exists():
        return ""
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ""
    return str(metadata.get("status", "")).strip().lower()


def is_active_track(track_id: str, registry: dict[str, dict[str, str]], location: str, path: Path) -> bool:
    entry = registry.get(track_id)
    if entry:
        if entry["marker"] == "~":
            return True
        if entry["marker"] == "x" or entry["archived_heading"] == "true":
            return False
        status = entry["status"].lower()
        if "active" in status or "in progress" in status:
            return True
        if "completed" in status or "archived" in status:
            return False
    status = metadata_status(path)
    if status in {"active", "in-progress", "in_progress", "in progress"}:
        return True
    if status in {"complete", "completed", "archived"}:
        return False
    return location == "tracks" and entry is None


def discover_tracks(root: Path) -> list[Track]:
    registry = parse_track_registry(root)
    descriptions = {track_id: data["description"] for track_id, data in registry.items() if data["description"]}
    tracks_dir = root / "conductor" / "tracks"
    archive_dir = root / "conductor" / "archive"
    ids: set[str] = set()
    if tracks_dir.exists():
        ids.update(path.name for path in tracks_dir.iterdir() if path.is_dir())
    if archive_dir.exists():
        ids.update(path.name for path in archive_dir.iterdir() if path.is_dir())

    tracks: list[Track] = []
    for track_id in sorted(ids):
        archive_path = archive_dir / track_id
        active_path = tracks_dir / track_id
        if archive_path.exists() and (
            track_id in TRACK_OVERRIDES or not active_path.exists() or track_id in descriptions
        ):
            location = "archive"
            path = f"conductor/archive/{track_id}/"
        else:
            location = "tracks"
            path = f"conductor/tracks/{track_id}/"

        override = TRACK_OVERRIDES.get(track_id, {})
        workstream = override.get("workstream", "Conductor")
        gate_type = override.get("gate_type", "Repo-local")
        track_path = archive_path if location == "archive" else active_path
        active = is_active_track(track_id, registry, location, track_path)
        status = STATUS_IN_PROGRESS if active else STATUS_DONE
        issue_state = "open" if active else "closed"
        description = override.get("description") or descriptions.get(track_id) or f"Mirror local Conductor track `{track_id}`."
        tracks.append(
            Track(
                track_id=track_id,
                title=f"track: {human_title(track_id)}",
                description=description,
                location=location,
                path=path,
                status=status,
                issue_state=issue_state,
                workstream=workstream,
                gate_type=gate_type,
            )
        )
    return tracks


def ensure_labels(apply: bool) -> None:
    labels_list = gh_json(["label", "list", "--repo", REPO, "--limit", "200", "--json", "name"]) or []
    existing = {label["name"] for label in labels_list}
    for name, (description, color) in LABELS.items():
        if name in existing:
            continue
        print(f"create label {name}")
        if apply:
            run(["gh", "label", "create", name, "--repo", REPO, "--description", description, "--color", color])


def load_issues() -> dict[int, dict[str, Any]]:
    issues = gh_json(
        [
            "api",
            "--paginate",
            f"repos/{REPO}/issues?state=all&per_page=100",
        ]
    ) or []
    normalized: dict[int, dict[str, Any]] = {}
    for issue in issues:
        if "pull_request" in issue:
            continue
        normalized[int(issue["number"])] = {
            "number": issue["number"],
            "title": issue["title"],
            "body": issue.get("body") or "",
            "state": issue["state"].upper(),
            "url": issue["html_url"],
            "labels": issue.get("labels", []),
            "projectItems": [],
        }
    return normalized


def issue_track_id(issue: dict[str, Any]) -> str | None:
    body = issue.get("body") or ""
    marker = re.search(r"uogto-conductor-track-id:\s*([A-Za-z0-9_]+)", body)
    if marker:
        return marker.group(1)
    old_marker = re.search(r"Conductor track:\s*`([^`]+)`", body)
    if old_marker:
        return old_marker.group(1)
    return None


def fetch_issue(number: int) -> dict[str, Any]:
    issue = require_json(gh_json(["api", f"repos/{REPO}/issues/{number}"]), f"issue #{number}")
    return {
        "number": issue["number"],
        "title": issue["title"],
        "body": issue.get("body") or "",
        "state": issue["state"].upper(),
        "url": issue["html_url"],
        "labels": issue.get("labels", []),
        "projectItems": [],
    }


def set_issue_state(number: int, state: str) -> None:
    if state == "closed":
        run(
            [
                "gh",
                "api",
                "-X",
                "PATCH",
                f"repos/{REPO}/issues/{number}",
                "-f",
                "state=closed",
                "-f",
                "state_reason=completed",
            ]
        )
    elif state == "open":
        run(["gh", "api", "-X", "PATCH", f"repos/{REPO}/issues/{number}", "-f", "state=open"])
    else:
        raise ValueError(f"unsupported issue state: {state}")


def build_issue_body(track: Track, existing_body: str | None = None) -> str:
    marker = f"<!-- uogto-conductor-track-id: {track.track_id} -->"
    if existing_body and marker in existing_body:
        return existing_body
    metadata = (
        "\n\n## Project sync metadata\n"
        f"- Track ID: `{track.track_id}`\n"
        f"- Local path: `{track.path}`\n"
        f"- Local status: `{track.status}`\n"
        f"- Workstream: `{track.workstream}`\n"
        f"- Gate type: `{track.gate_type}`\n"
        "\n"
        "Local Conductor files remain the detailed specification, plan, and evidence source of truth. "
        "This issue exists so GitHub Projects can mirror the complete local track ledger.\n"
        f"\n{marker}\n"
    )
    if existing_body:
        return existing_body.rstrip() + metadata
    return (
        "This issue mirrors one local UOGTO Conductor track into GitHub Projects.\n\n"
        f"Track ID: `{track.track_id}`\n"
        f"Local path: `{track.path}`\n"
        f"Local status: `{track.status}`\n"
        f"Workstream: `{track.workstream}`\n"
        f"Gate type: `{track.gate_type}`\n\n"
        f"Summary: {track.description}\n\n"
        "Local Conductor files remain the source of truth for detailed plan/spec/evidence. "
        "This issue exists so the GitHub Projects layer can reflect the complete track inventory and "
        "synchronize with the RI-HERO umbrella board.\n\n"
        f"{marker}\n"
    )


def label_args(labels: list[str]) -> list[str]:
    args: list[str] = []
    for label in labels:
        args.extend(["--add-label", label])
    return args


def set_parent_issue(issue_number: int, parent: int, apply: bool) -> None:
    if not apply:
        return
    completed = subprocess.run(
        [
            "gh",
            "issue",
            "edit",
            str(issue_number),
            "--repo",
            REPO,
            "--parent",
            str(parent),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode == 0:
        return
    if "duplicate sub-issues" in completed.stderr:
        return
    raise RuntimeError(
        f"gh issue edit {issue_number} --parent {parent} failed with exit code {completed.returncode}\n"
        f"stdout:\n{completed.stdout}\n\nstderr:\n{completed.stderr}"
    )


def ensure_track_issues(tracks: list[Track], apply: bool) -> dict[str, dict[str, Any]]:
    issues = load_issues()
    by_track: dict[str, dict[str, Any]] = {}
    for issue in issues.values():
        track_id = issue_track_id(issue)
        if track_id:
            by_track[track_id] = issue
    for track_id, issue_number in EXISTING_TRACK_ISSUES.items():
        if track_id not in by_track and issue_number in issues:
            by_track[track_id] = issues[issue_number]

    for track in tracks:
        labels = [
            "project-ledger",
            "conductor-track",
            "track-active" if track.issue_state == "open" else "track-complete",
        ]
        if track.location == "archive":
            labels.append("track-archived")
        labels.extend(WORKSTREAM_LABELS[track.workstream])
        parent = int(TRACK_OVERRIDES.get(track.track_id, {}).get("parent_issue", PARENT_ISSUES[track.workstream]))
        milestone = MILESTONES[track.workstream]
        issue = by_track.get(track.track_id)

        if issue is None:
            print(f"create issue for {track.track_id}")
            if apply:
                output = run(
                    [
                        "gh",
                        "issue",
                        "create",
                        "--repo",
                        REPO,
                        "--title",
                        track.title,
                        "--body",
                        build_issue_body(track),
                        "--parent",
                        str(parent),
                        "--milestone",
                        milestone,
                        "--label",
                        ",".join(dict.fromkeys(labels)),
                    ]
                )
                number = int(output.rstrip("/").split("/")[-1])
                issue = {
                    "number": number,
                    "title": track.title,
                    "body": build_issue_body(track),
                    "state": "OPEN",
                    "url": f"https://github.com/{REPO}/issues/{number}",
                    "labels": [{"name": label} for label in labels],
                    "projectItems": [],
                }
                by_track[track.track_id] = issue
        else:
            number = int(issue["number"])
            body = build_issue_body(track, issue.get("body") or "")
            already_synced = f"uogto-conductor-track-id: {track.track_id}" in (issue.get("body") or "")
            if already_synced:
                print(f"reuse issue #{number} for {track.track_id}")
            else:
                print(f"update issue #{number} for {track.track_id}")
            if apply and not already_synced:
                run(
                    [
                        "gh",
                        "issue",
                        "edit",
                        str(number),
                        "--repo",
                        REPO,
                        "--body",
                        body,
                        "--milestone",
                        milestone,
                        *label_args(list(dict.fromkeys(labels))),
                    ]
                )
                set_parent_issue(number, parent, apply)
                issue["body"] = body

        if apply:
            current = by_track[track.track_id]
            desired_state = "CLOSED" if track.issue_state == "closed" else "OPEN"
            if current["state"] != desired_state:
                set_issue_state(int(current["number"]), track.issue_state)
                current["state"] = desired_state
            by_track[track.track_id] = current

    return by_track


def ensure_project_fields(project_number: int, apply: bool) -> dict[str, dict[str, Any]]:
    fields = require_json(
        gh_json(["project", "field-list", str(project_number), "--owner", OWNER, "--format", "json"]),
        f"project {project_number} field list",
    )["fields"]
    existing = {field["name"]: field for field in fields}
    for name, (data_type, options) in UOGTO_PROJECT_FIELDS.items():
        if name in existing:
            continue
        print(f"create project field {name}")
        if apply:
            args = [
                "project",
                "field-create",
                str(project_number),
                "--owner",
                OWNER,
                "--name",
                name,
                "--data-type",
                data_type,
                "--format",
                "json",
            ]
            if options:
                args.extend(["--single-select-options", ",".join(options)])
            require_json(gh_json(args), f"project {project_number} field creation for {name}")
    fields = require_json(
        gh_json(["project", "field-list", str(project_number), "--owner", OWNER, "--format", "json"]),
        f"project {project_number} field list",
    )["fields"]
    return {field["name"]: field for field in fields}


def project_info(project_number: int) -> dict[str, Any]:
    return require_json(
        gh_json(["project", "view", str(project_number), "--owner", OWNER, "--format", "json"]),
        f"project {project_number} view",
    )


def project_items(project_number: int) -> list[dict[str, Any]]:
    return require_json(
        gh_json(["project", "item-list", str(project_number), "--owner", OWNER, "--format", "json", "--limit", "500"]),
        f"project {project_number} item list",
    )[
        "items"
    ]


def content_url(item: dict[str, Any]) -> str | None:
    content = item.get("content") or {}
    return content.get("url")


def ensure_project_item(project_number: int, url: str, apply: bool, cache: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    item = cache.get(url)
    if item:
        return item
    print(f"add to project {project_number}: {url}")
    if not apply:
        return None
    item = require_json(
        gh_json(
            [
                "project",
                "item-add",
                str(project_number),
                "--owner",
                OWNER,
                "--url",
                url,
                "--format",
                "json",
            ]
        ),
        f"project {project_number} add item {url}",
    )
    cache[url] = item
    return item


def option_id(field: dict[str, Any], option_name: str) -> str:
    for option in field.get("options", []):
        if option["name"] == option_name:
            return option["id"]
    raise KeyError(f"option {option_name!r} not found for field {field['name']!r}")


def set_select(project_id: str, item_id: str, field: dict[str, Any], value: str, apply: bool) -> None:
    if not apply:
        return
    run(
        [
            "gh",
            "project",
            "item-edit",
            "--id",
            item_id,
            "--project-id",
            project_id,
            "--field-id",
            field["id"],
            "--single-select-option-id",
            option_id(field, value),
        ]
    )


def set_text(project_id: str, item_id: str, field: dict[str, Any], value: str, apply: bool) -> None:
    if not value:
        return
    if not apply:
        return
    run(
        [
            "gh",
            "project",
            "item-edit",
            "--id",
            item_id,
            "--project-id",
            project_id,
            "--field-id",
            field["id"],
            "--text",
            value,
        ]
    )


def set_date(project_id: str, item_id: str, field: dict[str, Any], value: str, apply: bool) -> None:
    if not apply:
        return
    run(
        [
            "gh",
            "project",
            "item-edit",
            "--id",
            item_id,
            "--project-id",
            project_id,
            "--field-id",
            field["id"],
            "--date",
            value,
        ]
    )


def rihero_workstream(workstream: str) -> str:
    return "Research" if workstream == "Manuscript" else workstream


def delete_draft_items(project_number: int, apply: bool) -> int:
    deleted = 0
    for item in project_items(project_number):
        if (item.get("content") or {}).get("type") == "DraftIssue":
            deleted += 1
            print(f"delete stale draft item from project {project_number}: {item['title']}")
            if apply:
                run(["gh", "project", "item-delete", str(project_number), "--owner", OWNER, "--id", item["id"]])
    return deleted


def pr_workstream(title: str) -> str:
    lower = title.lower()
    if "bioregistry" in lower or "registry" in lower or "orcid" in lower:
        return "Registry"
    if "validation" in lower or "widoco" in lower or "benchmark" in lower:
        return "Validation"
    if "ontology" in lower or "alignment" in lower:
        return "Ontology"
    if "manuscript" in lower or "arxiv" in lower or "affiliation" in lower:
        return "Publishing"
    if "article" in lower or "hardening" in lower:
        return "Research"
    return "Maintenance"


def mirror_items(
    tracks: list[Track],
    track_issues: dict[str, dict[str, Any]],
    apply: bool,
) -> dict[str, int]:
    uogto_info = project_info(UOGTO_PROJECT)
    rihero_info = project_info(RIHERO_PROJECT)
    uogto_fields = ensure_project_fields(UOGTO_PROJECT, apply)
    rihero_fields = {field["name"]: field for field in gh_json(["project", "field-list", str(RIHERO_PROJECT), "--owner", OWNER, "--format", "json"])["fields"]}
    uogto_cache = {url: item for item in project_items(UOGTO_PROJECT) if (url := content_url(item))}
    rihero_cache = {url: item for item in project_items(RIHERO_PROJECT) if (url := content_url(item))}

    deleted_drafts = delete_draft_items(UOGTO_PROJECT, apply)

    all_issues = load_issues()
    issue_urls: dict[int, str] = {}
    for number in WORKSTREAM_ISSUES:
        issue = all_issues.get(number)
        if issue:
            issue_urls[number] = issue["url"]
    for issue in track_issues.values():
        issue_urls[int(issue["number"])] = issue["url"]

    for number, url in sorted(issue_urls.items()):
        item = ensure_project_item(UOGTO_PROJECT, url, apply, uogto_cache)
        ri_item = ensure_project_item(RIHERO_PROJECT, url, apply, rihero_cache)
        if not apply:
            continue
        issue = all_issues.get(number)
        track_id = issue_track_id(issue) if issue else None
        track = next((candidate for candidate in tracks if candidate.track_id == track_id), None)
        if track:
            status = track.status
            workstream = track.workstream
            exposure = "Monitoring" if track.status == STATUS_IN_PROGRESS else ("External" if track.gate_type.startswith("External") else "Repo")
            gate_type = track.gate_type
            role = "Conductor track"
            layer_8 = "Track"
            layer_9 = "Deliverable"
            track_location = track.path
        else:
            status = STATUS_DONE
            workstream = {
                4: "RI-HERO synthesis",
                5: "Conductor",
                6: "Maintenance",
                7: "Ontology",
                8: "Ontology",
                9: "RI-HERO synthesis",
                10: "Research",
                11: "Validation",
                12: "Research",
                13: "Publishing",
                14: "Research",
                15: "RI-HERO synthesis",
                16: "RI-HERO synthesis",
            }.get(number, "Conductor")
            exposure = "Internal" if workstream == "RI-HERO synthesis" else "Repo"
            gate_type = "Repo-local"
            role = "Umbrella" if number == 4 else "Workstream"
            layer_8 = "Epic" if number == 4 else "Workstream"
            layer_9 = layer_8
            track_location = ""

        if item:
            set_select(uogto_info["id"], item["id"], uogto_fields["Status"], status, apply)
            set_select(uogto_info["id"], item["id"], uogto_fields["Workstream"], workstream, apply)
            set_select(uogto_info["id"], item["id"], uogto_fields["Exposure"], exposure, apply)
            set_select(uogto_info["id"], item["id"], uogto_fields["Layer"], layer_8, apply)
            set_select(uogto_info["id"], item["id"], uogto_fields["Gate Type"], gate_type, apply)
            set_select(uogto_info["id"], item["id"], uogto_fields["Issue Role"], role, apply)
            set_text(uogto_info["id"], item["id"], uogto_fields["Track ID"], track_id or "", apply)
            set_text(uogto_info["id"], item["id"], uogto_fields["Track Location"], track_location, apply)
            set_date(uogto_info["id"], item["id"], uogto_fields["Synced"], TODAY, apply)
        if ri_item and workstream in {"RI-HERO synthesis", "Conductor", "Ontology", "Validation", "Publishing", "Registry", "Research", "Manuscript", "Maintenance"}:
            set_select(rihero_info["id"], ri_item["id"], rihero_fields["Status"], status, apply)
            if "Workstream" in rihero_fields:
                set_select(rihero_info["id"], ri_item["id"], rihero_fields["Workstream"], rihero_workstream(workstream), apply)
            if "Exposure" in rihero_fields:
                set_select(rihero_info["id"], ri_item["id"], rihero_fields["Exposure"], exposure, apply)
            if "Layer" in rihero_fields:
                set_select(rihero_info["id"], ri_item["id"], rihero_fields["Layer"], layer_9, apply)

    prs = gh_json(
        [
            "pr",
            "list",
            "--repo",
            REPO,
            "--state",
            "all",
            "--limit",
            "100",
            "--json",
            "number,title,state,mergedAt,url",
        ]
    ) or []
    merged_prs = [pr for pr in prs if pr.get("state") == "MERGED"]
    for pr in merged_prs:
        workstream = pr_workstream(pr["title"])
        exposure = "External" if workstream in {"Registry", "Publishing"} else "Repo"
        item = ensure_project_item(UOGTO_PROJECT, pr["url"], apply, uogto_cache)
        ri_item = ensure_project_item(RIHERO_PROJECT, pr["url"], apply, rihero_cache)
        if item and apply:
            set_select(uogto_info["id"], item["id"], uogto_fields["Status"], STATUS_DONE, apply)
            set_select(uogto_info["id"], item["id"], uogto_fields["Workstream"], workstream, apply)
            set_select(uogto_info["id"], item["id"], uogto_fields["Exposure"], exposure, apply)
            set_select(uogto_info["id"], item["id"], uogto_fields["Layer"], "Pull request", apply)
            set_select(uogto_info["id"], item["id"], uogto_fields["Gate Type"], "Repo-local", apply)
            set_select(uogto_info["id"], item["id"], uogto_fields["Issue Role"], "Development PR", apply)
            set_date(uogto_info["id"], item["id"], uogto_fields["Synced"], TODAY, apply)
        if ri_item and apply:
            set_select(rihero_info["id"], ri_item["id"], rihero_fields["Status"], STATUS_DONE, apply)
            set_select(rihero_info["id"], ri_item["id"], rihero_fields["Workstream"], rihero_workstream(workstream), apply)
            set_select(rihero_info["id"], ri_item["id"], rihero_fields["Exposure"], exposure, apply)
            set_select(rihero_info["id"], ri_item["id"], rihero_fields["Layer"], "Deliverable", apply)

    return {
        "tracks": len(tracks),
        "track_issues": len(track_issues),
        "workstream_issues": len(WORKSTREAM_ISSUES),
        "merged_prs": len(merged_prs),
        "deleted_drafts": deleted_drafts,
    }


def project_readme(summary: dict[str, int]) -> str:
    return f"""# UOGTO Conductor Roadmap

This GitHub Project mirrors the local UOGTO Conductor system, track history,
issue hierarchy, and merged development ledger.

Local source of truth:
- `conductor/index.md`
- `conductor/tracks.md`
- `conductor/archive/index.md`
- `conductor/status.md`
- `conductor/runlog.md`
- `conductor/tracks/*/spec.md`
- `conductor/tracks/*/plan.md`
- `conductor/archive/*/spec.md`
- `conductor/archive/*/plan.md`

Operating rules:
- Local Conductor files remain the detailed specification, plan, and evidence source of truth.
- One GitHub issue mirrors each local Conductor track using a hidden `uogto-conductor-track-id` marker.
- Native GitHub subissues carry the hierarchy: RI-HERO umbrella -> UOGTO workstream -> Conductor track.
- Completed and archived tracks are closed issues and appear as `Done`.
- Active or externally gated tracks remain open and appear as `In Progress` or monitoring items.
- Merged pull requests are included as Done development ledger items.
- RI-HERO Meta-Program mirrors these UOGTO issue and pull-request items at the item level because GitHub Projects cannot nest projects.

Current synchronized state as of {TODAY}:
- {summary['tracks']} Conductor track issues mirrored from local track/archive folders.
- {summary['workstream_issues']} umbrella/workstream issues included.
- {summary['merged_prs']} merged pull requests included as development ledger items.
- Stale draft seed items have been replaced by issue-backed project items.
- Custom fields are populated for Workstream, Exposure, Layer, Gate Type, Issue Role, Track ID, Track Location, and Synced date.

Sibling/meta board:
- RI-HERO Meta-Program: https://github.com/users/{OWNER}/projects/{RIHERO_PROJECT}
"""


def rihero_readme(summary: dict[str, int]) -> str:
    return f"""# RI-HERO Meta-Program

RI-HERO frames UOGTO and related health-economics infrastructure work through a
health economics research on outcomes lens.

## Program map
- Umbrella issue: #4 RI-HERO meta-program: health economics outcomes roadmap
- Synthesis issue: #9 RI-HERO: outcomes framing and synthesis
- Governance epic: #15 RI-HERO: program governance and operating model
- Evidence epic: #16 RI-HERO: health economics outcomes evidence map

## UOGTO mirror
The UOGTO Conductor Roadmap is mirrored here at the item level because GitHub
Projects cannot nest projects.

Dedicated UOGTO board:
- https://github.com/users/{OWNER}/projects/{UOGTO_PROJECT}

Mirrored UOGTO state as of {TODAY}:
- {summary['tracks']} local Conductor tracks represented as GitHub issues with hidden `uogto-conductor-track-id` markers.
- {summary['workstream_issues']} UOGTO umbrella/workstream issues represented.
- {summary['merged_prs']} merged UOGTO pull requests represented as completed development ledger items.
- Native subissues link UOGTO workstream issues to their track issues.
- Repo-local completion is separated from external registry, publication, and arXiv gates through Workstream, Exposure, and Layer fields.

## MCHS mirror
The MCHS Conductor Roadmap is also mirrored here at the item level.

Dedicated MCHS board:
- https://github.com/users/{OWNER}/projects/15

## Intake forms
- .github/ISSUE_TEMPLATE/ri-hero-meta-program.yml
- .github/ISSUE_TEMPLATE/ri-hero-publication-registry.yml
- .github/ISSUE_TEMPLATE/ri-hero-implementation-validation.yml
"""


def update_project_readmes(summary: dict[str, int], apply: bool) -> None:
    print("update project readmes")
    if not apply:
        return
    run(
        [
            "gh",
            "project",
            "edit",
            str(UOGTO_PROJECT),
            "--owner",
            OWNER,
            "--description",
            "Issue-backed UOGTO Conductor roadmap: local tracks, subissue hierarchy, merged PR ledger, and external gates.",
            "--readme",
            project_readme(summary),
        ]
    )
    run(
        [
            "gh",
            "project",
            "edit",
            str(RIHERO_PROJECT),
            "--owner",
            OWNER,
            "--readme",
            rihero_readme(summary),
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write changes to GitHub")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    tracks = discover_tracks(args.root)
    print(f"discovered {len(tracks)} unique Conductor tracks")
    ensure_labels(args.apply)
    track_issues = ensure_track_issues(tracks, args.apply)
    summary = mirror_items(tracks, track_issues, args.apply)
    update_project_readmes(summary, args.apply)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
