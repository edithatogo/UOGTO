import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.maintenance import disk_guard


class TestDiskGuard(unittest.TestCase):
    def test_default_disk_path_uses_current_filesystem_anchor(self):
        self.assertTrue(disk_guard.default_disk_path())

    def test_check_disk_space_uses_default_path_when_none(self):
        with mock.patch.object(disk_guard, "default_disk_path", return_value="."):
            with mock.patch.object(disk_guard.shutil, "disk_usage", return_value=(100, 50, 50)):
                self.assertTrue(disk_guard.check_disk_space(threshold_mb=0))


if __name__ == "__main__":
    unittest.main()
