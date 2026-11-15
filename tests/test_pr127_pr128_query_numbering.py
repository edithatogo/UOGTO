"""Prevent the PR127/128 query-ID collision without importing another lane."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parents[1]
RESERVED = {
    21: "cq21-costing-batch-conservation.rq",
    22: "cq22-costing-reporting-evidence.rq",
    23: "cq23-costing-infant-attribution.rq",
    24: "cq24-costing-rate-provenance.rq",
    25: "cq25-dynamic-game-representations.rq",
}
OLD_TEMPORALITY_NAME = "cq21-dynamic-game-representations.rq"


def _checked_ids(names):
    """Check naming/ownership only; this does not execute or qualify queries."""
    seen = {}
    for name in names:
        match = re.fullmatch(r"cq([0-9]{2,})-[a-z0-9-]+\.rq", name)
        assert match is not None, f"invalid query filename: {name}"
        number = int(match.group(1))
        assert number not in seen, f"duplicate CQ{number}: {seen.get(number)} / {name}"
        assert number not in RESERVED or name == RESERVED[number], (
            f"reserved CQ{number} belongs to {RESERVED.get(number)}, not {name}"
        )
        seen[number] = name
    return seen


def _manifest_names():
    manifest = json.loads((ROOT / "validation/competency-query-expectations.json").read_text(encoding="utf-8"))
    assert manifest["schema"] == "uogto.competency-query-expectations.v1"
    return [entry["query"] for entry in manifest["queries"]]


def test_manifest_has_unique_ids_and_respects_lane_reservations():
    names = _manifest_names()
    _checked_ids(names)
    assert RESERVED[25] in names
    assert OLD_TEMPORALITY_NAME not in names


def test_manifest_matches_query_files():
    """Full-tree check: no absent costing query receives a manifest entry."""
    names = _manifest_names()
    files = [path.name for path in (ROOT / "competency-questions").glob("*.rq")]
    _checked_ids(files)
    assert set(names) == set(files)
    assert len(names) == len(files)


def test_temporality_query_is_an_exact_content_preserving_rename():
    query = ROOT / "competency-questions" / RESERVED[25]
    assert query.is_file(), "temporality query must migrate to CQ25"
    assert not (query.parent / OLD_TEMPORALITY_NAME).exists()
    data = query.read_bytes()
    # Original PR127 query blob; this pins the migration, not solver execution.
    digest = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    assert digest == "9b6ee8deed098919bcba437f097acb6cded059fb"


def test_reservation_record_preserves_both_lane_identities():
    path = ROOT / "validation/competency-query-id-reservations.json"
    assert path.is_file(), "missing durable query-ID reservation record"
    record = json.loads(path.read_text(encoding="utf-8"))
    assert record["schema"] == "uogto.competency-query-id-reservations.v1"
    entries = record["reservations"]
    assert len(entries) == len(RESERVED)
    assert {entry["number"]: entry["query"] for entry in entries} == RESERVED
    assert {entry["owner_pr"] for entry in entries if entry["number"] < 25} == {128}
    temporal = next(entry for entry in entries if entry["number"] == 25)
    assert temporal["owner_pr"] == 127
    assert temporal["previous_query"] == OLD_TEMPORALITY_NAME
    assert record["reservation_is_implementation_evidence"] is False


def test_pending_costing_slots_do_not_block_the_temporality_manifest():
    assert _checked_ids([RESERVED[25]]) == {25: RESERVED[25]}


def test_the_declared_union_preserves_all_five_queries():
    assert _checked_ids(list(RESERVED.values())) == RESERVED


@pytest.mark.parametrize("names", [
    [OLD_TEMPORALITY_NAME, RESERVED[21]],
    ["cq21-unrelated-query.rq"],
    ["cq25-costing-batch-conservation.rq"],
    ["cq01-first.rq", "cq01-second.rq"],
    [RESERVED[25], RESERVED[25]],
    ["unregistered-query.rq"],
])
def test_collisions_and_reserved_slot_reuse_are_rejected(names):
    with pytest.raises(AssertionError):
        _checked_ids(names)
