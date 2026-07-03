from __future__ import annotations

import subprocess
import sys


def test_isolated_wheel_install_imports_runner_and_playground(tmp_path) -> None:
    venv = tmp_path / "venv"
    subprocess.run([sys.executable, "-m", "venv", "--system-site-packages", str(venv)], check=True)
    python = venv / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    subprocess.run(
        [str(python), "-m", "pip", "install", "--no-deps", "."],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    subprocess.run(
        [
            str(python),
            "-c",
            "import uogto; import uogto.runner; import uogto.playground.app",
        ],
        check=True,
    )
