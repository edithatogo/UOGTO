import argparse
import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.maintenance import build_w3id_redirect_handoff

PR_URL = build_w3id_redirect_handoff.W3ID_PULL_REQUEST_URL
PR_API_URL = "https://api.github.com/repos/perma-id/w3id.org/pulls/6238"
W3ID_DOC = ROOT / "docs" / "registry" / "w3id-submission.md"
EXPECTED_REDIRECT_TARGET = "https://edithatogo.github.io/UOGTO/"


@dataclass(frozen=True)
class RedirectCheck:
    source: str
    final_url: str
    status: int


def fetch_json(url: str, *, timeout: int = 20) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "UOGTO-w3id-status-check"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def fetch_redirect(url: str, *, timeout: int = 20) -> RedirectCheck:
    request = urllib.request.Request(url, method="GET", headers={"User-Agent": "UOGTO-w3id-status-check"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return RedirectCheck(source=url, final_url=response.url, status=response.status)


def check_local_w3id_state() -> dict:
    if not W3ID_DOC.exists():
        raise AssertionError("Missing docs/registry/w3id-submission.md")
    text = W3ID_DOC.read_text(encoding="utf-8")
    if PR_URL not in text:
        raise AssertionError("w3id submission document does not record the upstream pull request URL")

    packet = build_w3id_redirect_handoff.build_w3id_handoff()
    if packet.get("status") != "pending_external_w3id_merge":
        raise AssertionError("w3id handoff packet must remain pending_external_w3id_merge until live redirects work")
    if packet.get("w3id_pull_request_url") != PR_URL:
        raise AssertionError("w3id handoff packet pull request URL does not match the submission record")
    return packet


def check_pr_state(*, require_merged: bool = False, timeout: int = 20) -> dict:
    payload = fetch_json(PR_API_URL, timeout=timeout)
    state = payload.get("state")
    merged = bool(payload.get("merged"))
    if require_merged and not merged:
        raise AssertionError(f"w3id pull request is not merged yet; current state is {state!r}")
    return payload


def check_redirects(*, require_live: bool = False, timeout: int = 20) -> list[RedirectCheck]:
    checks = []
    for redirect in build_w3id_redirect_handoff.NAMESPACE_REDIRECTS:
        source = redirect["source"].rstrip("#")
        try:
            result = fetch_redirect(source, timeout=timeout)
        except urllib.error.HTTPError as exc:
            result = RedirectCheck(source=source, final_url=exc.geturl(), status=exc.code)
        except urllib.error.URLError as exc:
            if require_live:
                raise AssertionError(f"w3id redirect check failed for {source}: {exc}") from exc
            continue
        checks.append(result)

    if require_live:
        missing = [item.source for item in checks if not item.final_url.startswith(EXPECTED_REDIRECT_TARGET)]
        if missing:
            raise AssertionError("w3id redirects are not live yet: " + ", ".join(missing))
    return checks


def main() -> None:
    parser = argparse.ArgumentParser(description="Check UOGTO w3id pull request and redirect status.")
    parser.add_argument("--live", action="store_true", help="Query GitHub and w3id live endpoints.")
    parser.add_argument("--require-merged", action="store_true", help="Fail unless the w3id PR is merged.")
    parser.add_argument("--require-live", action="store_true", help="Fail unless w3id redirects resolve to UOGTO Pages.")
    parser.add_argument("--timeout", type=int, default=20, help="Per-request timeout in seconds.")
    args = parser.parse_args()

    check_local_w3id_state()
    messages = ["Local w3id submission state is pending upstream merge."]

    if args.live or args.require_merged:
        pr = check_pr_state(require_merged=args.require_merged, timeout=args.timeout)
        messages.append(f"w3id PR {PR_URL} is {pr.get('state')} with merged={bool(pr.get('merged'))}.")

    if args.live or args.require_live:
        redirects = check_redirects(require_live=args.require_live, timeout=args.timeout)
        if redirects:
            rendered = ", ".join(f"{item.source} -> {item.final_url} ({item.status})" for item in redirects)
            messages.append("w3id redirect observations: " + rendered)
        else:
            messages.append("No live w3id redirect observations were recorded.")

    print(" ".join(messages))


if __name__ == "__main__":
    main()
