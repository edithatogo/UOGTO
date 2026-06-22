import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.maintenance import check_doi_status


ZENODO_API_BASE = "https://zenodo.org/api"
TOKEN_ENV = "ZENODO_ACCESS_TOKEN"


def build_depositions_url(api_base: str = ZENODO_API_BASE, query: str | None = None) -> str:
    params = {"size": "100"}
    if query:
        params["q"] = query
    return f"{api_base.rstrip('/')}/deposit/depositions?{urllib.parse.urlencode(params)}"


def fetch_depositions(token: str, *, api_base: str = ZENODO_API_BASE, timeout: int = 20) -> list[dict]:
    request = urllib.request.Request(
        build_depositions_url(api_base, check_doi_status.EXPECTED_TITLE),
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "UOGTO-zenodo-depositions-check",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.load(response)
    if not isinstance(payload, list):
        raise AssertionError("Zenodo depositions API returned an unexpected payload")
    return payload


def deposition_matches_uogto(deposition: dict) -> bool:
    metadata = deposition.get("metadata") or {}
    title = str(metadata.get("title") or "")
    related = metadata.get("related_identifiers") or []
    repository_match = any(item.get("identifier") == check_doi_status.EXPECTED_REPOSITORY for item in related)
    return check_doi_status.EXPECTED_TITLE.lower() in title.lower() or repository_match


def summarize_deposition(deposition: dict) -> dict:
    metadata = deposition.get("metadata") or {}
    links = deposition.get("links") or {}
    return {
        "id": deposition.get("id"),
        "conceptrecid": deposition.get("conceptrecid"),
        "record_id": deposition.get("record_id"),
        "state": deposition.get("state"),
        "submitted": deposition.get("submitted"),
        "title": metadata.get("title"),
        "doi": metadata.get("doi") or deposition.get("doi"),
        "record_url": links.get("record") or links.get("html"),
    }


def build_account_status(
    *,
    token: str | None,
    api_base: str = ZENODO_API_BASE,
    timeout: int = 20,
    fetcher=fetch_depositions,
) -> dict:
    if not token:
        return {
            "schema": "uogto.zenodo-account-status.v1",
            "status": "missing_token",
            "token_env": TOKEN_ENV,
            "uogto_depositions": [],
            "blockers": [f"{TOKEN_ENV} is not set; account-side Zenodo depositions cannot be inspected."],
        }

    try:
        depositions = fetcher(token, api_base=api_base, timeout=timeout)
    except HTTPError as error:
        status = "invalid_or_rejected_token" if error.code in {400, 401, 403} else "zenodo_api_error"
        return {
            "schema": "uogto.zenodo-account-status.v1",
            "status": status,
            "token_env": TOKEN_ENV,
            "uogto_depositions": [],
            "blockers": [f"Zenodo depositions API returned HTTP {error.code}; token was not printed."],
        }
    except (TimeoutError, URLError) as error:
        return {
            "schema": "uogto.zenodo-account-status.v1",
            "status": "zenodo_api_error",
            "token_env": TOKEN_ENV,
            "uogto_depositions": [],
            "blockers": [f"Zenodo depositions API request failed: {error.__class__.__name__}."],
        }

    matches = [summarize_deposition(item) for item in depositions if deposition_matches_uogto(item)]
    return {
        "schema": "uogto.zenodo-account-status.v1",
        "status": "uogto_deposition_found" if matches else "no_uogto_deposition_found",
        "token_env": TOKEN_ENV,
        "uogto_depositions": matches,
        "blockers": [] if matches else ["No UOGTO deposition was found in the authenticated Zenodo account."],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect authenticated Zenodo depositions for UOGTO.")
    parser.add_argument("--api-base", default=os.environ.get("ZENODO_API_BASE", ZENODO_API_BASE))
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument("--require-token", action="store_true", help="Fail if ZENODO_ACCESS_TOKEN is not set.")
    parser.add_argument("--require-uogto", action="store_true", help="Fail unless a UOGTO deposition is found.")
    args = parser.parse_args()

    token = os.environ.get(TOKEN_ENV)
    status = build_account_status(token=token, api_base=args.api_base, timeout=args.timeout)

    if args.json:
        print(json.dumps(status, indent=2, sort_keys=True))
    else:
        print(f"Zenodo account status: {status['status']}")
        for item in status["uogto_depositions"]:
            print(
                "UOGTO deposition: "
                + ", ".join(
                    part
                    for part in [
                        f"id={item.get('id')}",
                        f"state={item.get('state')}",
                        f"submitted={item.get('submitted')}",
                        f"doi={item.get('doi')}",
                        f"record_url={item.get('record_url')}",
                    ]
                    if not part.endswith("=None")
                )
            )
        for blocker in status["blockers"]:
            print(blocker)

    if args.require_token and status["status"] == "missing_token":
        raise SystemExit(1)
    if args.require_uogto and not status["uogto_depositions"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
