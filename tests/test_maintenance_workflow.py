from pathlib import Path

import yaml


def test_maintenance_workflow_uploads_live_publication_status_artifact():
    workflow_path = Path(".github/workflows/maintenance.yml")
    workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    steps = workflow["jobs"]["validate-and-update"]["steps"]
    step_names = {step.get("name") for step in steps}
    assert "Build Live Publication Status" in step_names
    assert "Upload Live Publication Status Artifact" in step_names
    checkout = steps[0]
    assert checkout["uses"] == "actions/checkout@v7"
    assert checkout["with"]["persist-credentials"] is False
    pr_step = next(step for step in steps if step.get("name") == "Create Maintenance Pull Request")
    assert pr_step["continue-on-error"] is True

    workflow_text = workflow_path.read_text(encoding="utf-8")
    expected_fragments = [
        "pixi run python scripts/maintenance/build_publication_status.py --live --output dist/publication-status-live.json",
        "uses: actions/upload-artifact@v5",
        "name: publication-status-live",
        "path: dist/publication-status-live.json",
    ]
    for fragment in expected_fragments:
        assert fragment in workflow_text
