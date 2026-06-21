import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.maintenance import update_dependencies


class TestUpdateDependencies(unittest.TestCase):
    def test_repo_root_is_importable_when_script_runs_by_path(self):
        self.assertIn(str(update_dependencies.ROOT), sys.path)
        self.assertTrue((update_dependencies.ROOT / "scripts" / "maintenance" / "disk_guard.py").exists())

    def test_pixi_command_falls_back_to_pixi_name(self):
        self.assertIn(Path(update_dependencies.pixi_command()).name.lower(), {"pixi", "pixi.exe"})


if __name__ == "__main__":
    unittest.main()
