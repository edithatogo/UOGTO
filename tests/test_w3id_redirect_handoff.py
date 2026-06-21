import json
import shutil
import sys
import unittest
import uuid
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.maintenance import build_w3id_redirect_handoff


class TestW3idRedirectHandoff(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_w3id_redirect_handoff_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_handoff_records_pending_external_pr(self):
        packet = build_w3id_redirect_handoff.build_w3id_handoff()
        self.assertEqual(packet["schema"], "uogto.w3id-redirect-handoff.v1")
        self.assertEqual(packet["status"], "pending_external_w3id_pr")
        self.assertEqual(packet["w3id_path"], "uogto/.htaccess")
        self.assertIn("URL fragments", packet["namespace_note"])

    def test_htaccess_covers_core_and_extensions(self):
        htaccess = build_w3id_redirect_handoff.render_htaccess()
        self.assertIn("RewriteEngine On", htaccess)
        self.assertIn("RewriteRule ^core/?$", htaccess)
        self.assertIn("RewriteRule ^extensions/?$", htaccess)
        self.assertIn("[R=303,L]", htaccess)

    def test_write_handoff_outputs_json(self):
        output = self.temp_dir / "w3id-redirect-handoff.json"
        packet = build_w3id_redirect_handoff.build_w3id_handoff()
        build_w3id_redirect_handoff.write_handoff(output, packet)
        loaded = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(loaded["htaccess"], packet["htaccess"])


if __name__ == "__main__":
    unittest.main()
