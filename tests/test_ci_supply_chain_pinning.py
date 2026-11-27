from __future__ import annotations

import re
import tomllib
from pathlib import Path

import yaml

WORKFLOWS = Path(".github/workflows")


def test_workflows_use_environment_specific_pip_and_pinned_sourceright() -> None:
    workflow_text = "\n".join(path.read_text(encoding="utf-8") for path in WORKFLOWS.glob("*.yml"))
    assert "\n          pip install ." not in workflow_text
    assert "\n        pip install ." not in workflow_text
    assert 'python -m pip install ".[dev]"' in workflow_text
    assert "cargo install --git https://github.com/edithatogo/sourceright.git --rev " in workflow_text
    assert "cargo install --git https://github.com/edithatogo/sourceright.git sourceright" not in workflow_text


def test_pixi_and_hosted_ci_select_the_project_python() -> None:
    action_file = WORKFLOWS.parent / "actions/project-python/action.yml"
    setup = yaml.safe_load(action_file.read_text(encoding="utf-8"))["runs"]["steps"][0]
    version_file = Path(setup["with"]["python-version-file"])
    assert version_file == Path(".python-version")
    python_version = version_file.read_text(encoding="utf-8").strip()
    assert re.fullmatch(r"3\.15\.[0-9]+", python_version)
    with Path("pixi.toml").open("rb") as manifest:
        assert tomllib.load(manifest)["dependencies"]["python"] == f"=={python_version}"
    for name in ("validate.yml", "required-gate.yml"):
        workflow = (WORKFLOWS / name).read_text(encoding="utf-8")
        assert "uses: ./.github/actions/project-python" in workflow


def test_widoco_workflow_verifies_pinned_artifact_checksum() -> None:
    workflow_text = (WORKFLOWS / "widoco-pages.yml").read_text(encoding="utf-8")
    assert "WIDOCO_JAR_URL:" in workflow_text
    assert "WIDOCO_JAR_SHA256: be57a270fffb91e55810fa308717e704a44e2e7c027a3d68125a49da6c8b4e2b" in workflow_text
    assert "hashlib.sha256" in workflow_text
    assert "urlretrieve(jar_url, \"widoco.jar\")" in workflow_text


def test_supply_chain_policy_is_documented() -> None:
    policy = Path("docs/ci-supply-chain-policy.md").read_text(encoding="utf-8")
    assert "SourceRight" in policy
    assert "WIDOCO" in policy
    assert "Updating action tags" in policy
