from __future__ import annotations

import email
import importlib.metadata
import json
import subprocess
import sys
import zipfile
from pathlib import Path

from packaging.requirements import Requirement


def _dependency_roots(requirements):
    """Resolve the wheel's runtime dependency closure from this test environment.

    The smoke test is offline: expose installed dependency directories explicitly,
    because a nested venv's system-site-packages does not inherit its parent venv.
    Missing or incompatible dependencies fail instead of skipping the test.
    """
    pending = list(requirements)
    checked = set()
    roots = set()
    while pending:
        requirement = Requirement(pending.pop())
        if requirement.marker and not requirement.marker.evaluate({"extra": ""}):
            continue
        distribution = importlib.metadata.distribution(requirement.name)
        assert distribution.version in requirement.specifier, str(requirement)
        if distribution.metadata["Name"] in checked:
            continue
        checked.add(distribution.metadata["Name"])
        roots.add(str(Path(distribution.locate_file("")).resolve()))
        pending.extend(distribution.requires or [])
    return sorted(roots)


def test_isolated_wheel_install_imports_runner_and_playground(tmp_path) -> None:
    checkout = Path(__file__).resolve().parents[1]
    wheel_dir = tmp_path / "wheel"
    wheel_dir.mkdir()
    build_command = (
        "from setuptools.build_meta import build_wheel\n"
        f"build_wheel({str(wheel_dir)!r})\n"
    )
    subprocess.run(
        [sys.executable, "-c", build_command],
        cwd=checkout, check=True, capture_output=True, text=True, timeout=120,
    )
    wheel = next(wheel_dir.glob("uogto-*.whl"))
    with zipfile.ZipFile(wheel) as archive:
        metadata_file = next(name for name in archive.namelist() if name.endswith(".dist-info/METADATA"))
        metadata = email.message_from_bytes(archive.read(metadata_file))
    dependency_roots = _dependency_roots(metadata.get_all("Requires-Dist", []))
    assert str(checkout) not in dependency_roots

    venv = tmp_path / "venv"
    subprocess.run(
        [sys.executable, "-m", "venv", "--without-pip", str(venv)],
        check=True, timeout=60,
    )
    python = venv / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    site_packages = Path(subprocess.check_output(
        [str(python), "-I", "-c", "import sysconfig; print(sysconfig.get_paths()['purelib'])"],
        text=True, timeout=30,
    ).strip())
    site_packages.mkdir(parents=True, exist_ok=True)
    # A wheel is an installable zip; this avoids bootstrapping pip or network access.
    with zipfile.ZipFile(wheel) as archive:
        archive.extractall(site_packages)
    (site_packages / "smoke_dependencies.pth").write_text(
        "\n".join(dependency_roots) + "\n", encoding="utf-8",
    )
    outside_checkout = tmp_path / "outside-checkout"
    outside_checkout.mkdir()
    declaration = checkout / "tests/fixtures/paignia-static-declaration-v1.json"
    code = """
import json
import sys
from pathlib import Path
import uogto
import uogto.interchange
import uogto.runner
import uogto.playground.app
import rdflib, pyshacl, yaml, jsonschema
from uogto.interchange import UnsupportedExecutableSubset, validate_executable_subset

declaration = json.load(sys.stdin)
assert validate_executable_subset(declaration)["status"] == "profile_declaration_compatible"
for invalid_uri in ("", "relative-game-id"):
    declaration["game"]["specification_iri"] = invalid_uri
    try:
        validate_executable_subset(declaration)
    except UnsupportedExecutableSubset as exc:
        assert exc.code == "unsupported_subset"
        assert exc.path == "game.specification_iri"
    else:
        raise AssertionError(f"Accepted invalid specification URI {invalid_uri!r}")

modules = [uogto, uogto.interchange, uogto.runner, uogto.playground.app]
print(json.dumps([str(Path(module.__file__).resolve()) for module in modules]))
"""
    result = subprocess.run(
        [str(python), "-I", "-c", code], cwd=outside_checkout,
        input=declaration.read_text(encoding="utf-8"),
        check=True, capture_output=True, text=True, timeout=60,
    )
    for origin in json.loads(result.stdout):
        assert Path(origin).is_relative_to(site_packages), origin
        assert not Path(origin).is_relative_to(checkout), origin
