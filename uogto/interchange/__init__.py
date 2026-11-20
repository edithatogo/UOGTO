"""Versioned, language-neutral game semantic declaration contracts."""

from .game_contract import (
    EXPORT_SCHEMA, PROFILE_ID, PROVIDER_REVISION,
    UnsupportedExecutableSubset, validate_executable_subset,
)

__all__ = [
    "EXPORT_SCHEMA", "PROFILE_ID", "PROVIDER_REVISION",
    "UnsupportedExecutableSubset", "validate_executable_subset",
]
