"""Fail-closed source-side admission of UOGTO's bounded Paignia profile.

This checks a declaration, **not** a graph, provider adapter or execution receipt.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any, Mapping

from jsonschema import Draft202012Validator, FormatChecker

PROFILE_ID = "paignia/static-finite-perfect-information-sparse-zero/1.0.0"
PROVIDER_REVISION = "bd880dd756d2ba56cc5f479bc078cea31b53c1d1"

# Canonical public JSON Schema is mirrored to validation/ and regression-checked.
# Keep an inline copy so an installed wheel never requires source-checkout files.
EXPORT_SCHEMA = json.loads(r'''{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://w3id.org/uogto/contracts/executable-game-subset-v1.json",
  "title": "UOGTO source-to-Paignia finite-game subset declaration v1",
  "description": "Declaration-level semantic admission only. Does not inspect a graph, verify solver correctness, run Rust, or qualify a native adapter or release.",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "contract_version",
    "profile_id",
    "provider",
    "game"
  ],
  "properties": {
    "contract_version": {
      "const": "1.0.0"
    },
    "profile_id": {
      "const": "paignia/static-finite-perfect-information-sparse-zero/1.0.0"
    },
    "provider": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "repository",
        "revision",
        "core_package",
        "solver_package",
        "package_version"
      ],
      "properties": {
        "repository": {
          "const": "edithatogo/paignia"
        },
        "revision": {
          "const": "bd880dd756d2ba56cc5f479bc078cea31b53c1d1"
        },
        "core_package": {
          "const": "paignia-core"
        },
        "solver_package": {
          "const": "paignia-solve"
        },
        "package_version": {
          "const": "0.1.0"
        }
      }
    },
    "game": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "specification_iri",
        "specification_class",
        "representation_class",
        "game_class",
        "information_structure",
        "chance_rule",
        "payoff_rule",
        "selection_rule",
        "selection_tolerance",
        "native_execution_claim"
      ],
      "properties": {
        "specification_iri": {
          "type": "string",
          "format": "uri"
        },
        "specification_class": {
          "const": "https://w3id.org/uogto/core#GameSpecification"
        },
        "representation_class": {
          "const": "https://w3id.org/uogto/core#ExtensiveFormRepresentation"
        },
        "game_class": {
          "const": "FiniteAcyclicExtensive"
        },
        "information_structure": {
          "const": "PerfectInformation"
        },
        "chance_rule": {
          "const": "AllowZeroAndValidateEveryBranch"
        },
        "payoff_rule": {
          "const": "IntentionalSparseZero"
        },
        "selection_rule": {
          "const": "InputOrderPairwiseToleranceThenLexicographic"
        },
        "selection_tolerance": {
          "type": "number",
          "minimum": 0
        },
        "strategic_timing": {
          "enum": [
            "StaticGame",
            "DynamicGame"
          ]
        },
        "native_execution_claim": {
          "const": false
        }
      }
    }
  }
}''')


@dataclass(frozen=True)
class UnsupportedExecutableSubset(ValueError):
    """Stable named rejection; does not mutate an unsupported source record."""

    code: str
    path: str
    detail: str

    def __str__(self) -> str:
        return f"{self.code} at {self.path}: {self.detail}"


def validate_executable_subset(record: Mapping[str, Any]) -> dict[str, object]:
    """Admit only a v1 profile *declaration*; never infer native execution.

    Supported Paignia source semantics are identified by exact package/revision,
    not by a runtime call. The graph itself must be independently qualified.
    """
    if isinstance(record, Mapping):
        game = record.get("game")
        if isinstance(game, Mapping):
            tolerance = game.get("selection_tolerance")
            if isinstance(tolerance, (float, int)) and not isinstance(tolerance, bool):
                if not math.isfinite(tolerance):
                    raise UnsupportedExecutableSubset(
                        "invalid_tolerance", "game.selection_tolerance", "must be finite"
                    )

    validator = Draft202012Validator(EXPORT_SCHEMA, format_checker=FormatChecker())
    error = next(iter(validator.iter_errors(record)), None)
    if error is not None:
        path = ".".join(str(part) for part in error.absolute_path) or "$"
        raise UnsupportedExecutableSubset("unsupported_subset", path, error.message)

    return {
        "status": "profile_declaration_compatible",
        "profile_id": PROFILE_ID,
        "provider_revision": PROVIDER_REVISION,
        "native_execution_qualified": False,
    }
