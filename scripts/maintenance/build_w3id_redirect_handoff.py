import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


DEFAULT_OUTPUT = ROOT / "dist" / "w3id-redirect-handoff.json"
W3ID_REPOSITORY = "https://github.com/perma-id/w3id.org"
W3ID_PULL_REQUEST_URL = "https://github.com/perma-id/w3id.org/pull/6238"
W3ID_PATH = "uogto/.htaccess"
DOCUMENTATION_URL = "https://edithatogo.github.io/UOGTO/"
RELEASE_ASSET_URL = "https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/uogto.ttl"
NAMESPACE_REDIRECTS = [
    {
        "source": "https://w3id.org/uogto/",
        "path": "",
        "target": DOCUMENTATION_URL,
        "http_status": 303,
    },
    {
        "source": "https://w3id.org/uogto/core",
        "path": "core/?",
        "target": DOCUMENTATION_URL,
        "http_status": 303,
    },
    {
        "source": "https://w3id.org/uogto/extensions",
        "path": "extensions/?",
        "target": DOCUMENTATION_URL,
        "http_status": 303,
    },
]


def render_htaccess() -> str:
    lines = [
        "RewriteEngine On",
        f"RewriteRule ^$ {DOCUMENTATION_URL} [R=303,L]",
    ]
    for redirect in NAMESPACE_REDIRECTS[1:]:
        lines.append(f"RewriteRule ^{redirect['path']}$ {redirect['target']} [R=303,L]")
    return "\n".join(lines) + "\n"


def build_w3id_handoff() -> dict:
    return {
        "schema": "uogto.w3id-redirect-handoff.v1",
        "status": "live_redirects_verified",
        "blockers": [],
        "w3id_repository": W3ID_REPOSITORY,
        "w3id_pull_request_url": W3ID_PULL_REQUEST_URL,
        "merged_at": "2026-06-22T12:29:07Z",
        "w3id_path": W3ID_PATH,
        "documentation_url": DOCUMENTATION_URL,
        "release_asset_url": RELEASE_ASSET_URL,
        "namespace_note": "URL fragments are not sent to the server; redirects cover /uogto/core and /uogto/extensions for hash namespaces.",
        "redirects": NAMESPACE_REDIRECTS,
        "htaccess": render_htaccess(),
    }


def write_handoff(output_path: Path, packet: dict) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")



def display_path(output_path: Path) -> str:
    resolved = output_path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(output_path)

def main() -> None:
    parser = argparse.ArgumentParser(description="Build the UOGTO w3id redirect handoff packet.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="JSON output path. Defaults to dist/w3id-redirect-handoff.json.",
    )
    args = parser.parse_args()

    packet = build_w3id_handoff()
    write_handoff(args.output, packet)
    print(f"Wrote {display_path(args.output)} with status {packet['status']}.")


if __name__ == "__main__":
    main()
