import os
import subprocess
import sys
from pathlib import Path

import pytest


def test_pyproject_packages_uogto_modules_and_optional_playground_dependencies() -> None:
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    assert '[project.optional-dependencies]' in text
    assert 'playground = [' in text
    assert '[project.scripts]' in text
    assert 'uogto-runner-bench = "uogto.runner.llm_player:main"' in text
    assert '[tool.setuptools.packages.find]' in text
    assert 'include = ["uogto*"]' in text


def test_installed_package_imports_runner_without_repo_pythonpath(tmp_path: Path) -> None:
    if subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True).returncode:
        pytest.skip("pip is not installed in this local interpreter")
    target = tmp_path / "install"
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--quiet", "--target", str(target), "."],
        check=True,
        cwd=Path.cwd(),
    )
    code = "from uogto.runner import RDFGameRunner; print(RDFGameRunner.__name__)"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(target)
    result = subprocess.run(
        [sys.executable, "-c", code],
        check=True,
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == "RDFGameRunner"
