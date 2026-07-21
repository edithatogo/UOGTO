from __future__ import annotations

import zipfile
import subprocess
import sys
from pathlib import Path


def test_isolated_wheel_install_imports_runner_and_playground(tmp_path) -> None:
    venv = tmp_path / "venv"
    # Avoid ensurepip here: on some Windows/Pixi combinations it can hang while
    # bootstrapping pip even though the interpreter and wheel are usable.
    subprocess.run(
        [sys.executable, "-m", "venv", "--system-site-packages", "--without-pip", str(venv)],
        check=True,
        timeout=60,
    )
    python = venv / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    wheel_dir = tmp_path / "wheel"
    wheel_dir.mkdir()
    subprocess.run(
        [
            sys.executable,
            "-c",
            "from setuptools.build_meta import build_wheel; build_wheel(r'{}')".format(wheel_dir),
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=120,
    )
    site_packages = Path(
        subprocess.check_output(
            [str(python), "-c", "import sysconfig; print(sysconfig.get_paths()['purelib'])"],
            text=True,
            timeout=30,
        ).strip()
    )
    site_packages.mkdir(parents=True, exist_ok=True)
    wheel = next(wheel_dir.glob("uogto-*.whl"))
    with zipfile.ZipFile(wheel) as archive:
        archive.extractall(site_packages)
    subprocess.run(
        [
            str(python),
            "-c",
            "import uogto; import uogto.runner; import uogto.playground.app",
        ],
        check=True,
        timeout=60,
    )
