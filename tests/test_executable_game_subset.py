"""Versioned finite-game declaration admission; not Rust execution certification."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from uogto.interchange.game_contract import (
    EXPORT_SCHEMA,
    PROFILE_ID,
    UnsupportedExecutableSubset,
    validate_executable_subset,
)

ROOT = Path(__file__).resolve().parents[1]


def valid_record() -> dict:
    return json.loads(
        (ROOT / "tests/fixtures/paignia-static-declaration-v1.json").read_text(encoding="utf-8")
    )


def test_admit_qualified_declaration_without_execution_claim():
    record = valid_record()
    result = validate_executable_subset(record)
    assert result["status"] == "profile_declaration_compatible"
    assert result["profile_id"] == PROFILE_ID
    assert result["native_execution_qualified"] is False
    assert record == valid_record()


@pytest.mark.parametrize("timing", ["StaticGame", "DynamicGame"])
def test_strategic_timing_is_independent_of_finite_extensive_representation(timing):
    record = valid_record()
    record["game"]["strategic_timing"] = timing
    assert validate_executable_subset(record)["native_execution_qualified"] is False


@pytest.mark.parametrize("path,bad", [
    (("contract_version",), "1.1.0"),
    (("profile_id",), "unknown-profile"),
    (("provider", "core_package"), "uogto-game-core"),
    (("provider", "solver_package"), "unverified-solver"),
    (("provider", "package_version"), "0.2.0"),
    (("provider", "revision"), "new-unreviewed-commit"),
    (("game", "game_class"), "SimultaneousNormalForm"),
    (("game", "representation_class"), "https://w3id.org/uogto/core#NormalFormRepresentation"),
    (("game", "information_structure"), "ImperfectInformation"),
    (("game", "chance_rule"), "StrictlyPositiveWeightsOnly"),
    (("game", "payoff_rule"), "CompletePayoffOnly"),
    (("game", "selection_rule"), "FirstMaximum"),
    (("game", "native_execution_claim"), True),
    (("game", "specification_class"), "https://w3id.org/uogto/core#GameInstance"),
    (("game", "specification_iri"), "relative-game-id"),
])
def test_unsupported_contracts_fail_closed(path, bad):
    record = valid_record()
    obj = record
    for key in path[:-1]:
        obj = obj[key]
    obj[path[-1]] = bad
    with pytest.raises(UnsupportedExecutableSubset) as exc:
        validate_executable_subset(record)
    assert exc.value.code in ("unsupported_subset", "invalid_tolerance")


@pytest.mark.parametrize(
    "value", [-1, float("nan"), float("inf"), -float("inf"), 10**400, -(10**400), True, "0", None]
)
def test_invalid_tolerances_fail_without_coercion(value):
    record = valid_record()
    record["game"]["selection_tolerance"] = value
    with pytest.raises(UnsupportedExecutableSubset):
        validate_executable_subset(record)


def test_required_fields_and_extra_claims_fail_closed():
    record = valid_record()
    del record["game"]["selection_rule"]
    with pytest.raises(UnsupportedExecutableSubset):
        validate_executable_subset(record)
    record = valid_record()
    record["executed_by_rust"] = True
    with pytest.raises(UnsupportedExecutableSubset):
        validate_executable_subset(record)


def test_schema_document_matches_python_validator_contract():
    published = json.loads((ROOT / "validation" / "executable-game-subset-v1.json").read_text())
    assert published == EXPORT_SCHEMA
    assert published["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert published["properties"]["profile_id"]["const"] == PROFILE_ID


@pytest.mark.parametrize(
    "value",
    ["../game-one", "//w3id.org/uogto/examples#game-one", "urn:example:game with space", "urn:example:game\n"],
)
def test_invalid_absolute_specification_uri_has_a_typed_field_error(value):
    record = valid_record()
    record["game"]["specification_iri"] = value
    with pytest.raises(UnsupportedExecutableSubset) as exc:
        validate_executable_subset(record)
    assert exc.value.code == "unsupported_subset"
    assert exc.value.path == "game.specification_iri"


def test_absolute_urn_specification_is_supported():
    record = valid_record()
    record["game"]["specification_iri"] = "urn:example:game-one"
    assert validate_executable_subset(record)["status"] == "profile_declaration_compatible"


def test_validator_does_not_mutate_caller_record():
    record = valid_record()
    original = copy.deepcopy(record)
    assert validate_executable_subset(record)
    assert record == original
