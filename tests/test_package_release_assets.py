import json
import os
import shutil
import sys
import unittest
import uuid
from pathlib import Path


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.maintenance import package_release_assets


class TestPackageReleaseAssets(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_release_assets_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True)

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def write_required_assets(self):
        for name in package_release_assets.REQUIRED_RELEASE_ASSETS:
            (self.temp_dir / name).write_text(f"{name}\n", encoding="utf-8")

    def test_collect_release_assets(self):
        self.write_required_assets()
        assets = package_release_assets.collect_release_assets(self.temp_dir)
        self.assertEqual(
            [asset["name"] for asset in assets],
            package_release_assets.REQUIRED_RELEASE_ASSETS,
        )
        self.assertTrue(all(len(asset["sha256"]) == 64 for asset in assets))

    def test_rejects_missing_release_asset(self):
        (self.temp_dir / "uogto.ttl").write_text("ontology\n", encoding="utf-8")
        with self.assertRaises(AssertionError):
            package_release_assets.collect_release_assets(self.temp_dir)

    def test_write_release_manifest_and_checksums(self):
        self.write_required_assets()
        manifest = package_release_assets.write_release_manifest(self.temp_dir, "1.0.0")
        self.assertEqual(manifest["version"], "1.0.0")

        manifest_path = self.temp_dir / "release-assets-manifest.json"
        checksums_path = self.temp_dir / "SHA256SUMS"
        self.assertTrue(manifest_path.exists())
        self.assertTrue(checksums_path.exists())

        parsed = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(len(parsed["assets"]), len(package_release_assets.REQUIRED_RELEASE_ASSETS))
        self.assertIn("uogto.ttl", checksums_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
