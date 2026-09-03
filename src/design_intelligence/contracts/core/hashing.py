"""RFC 8785 canonical JSON and SHA-256 hashing for prepared payloads."""

from __future__ import annotations

import hashlib
from typing import TypeAlias

import rfc8785

from .refs import ContentHash

JsonScalar: TypeAlias = None | bool | int | float | str
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]


def canonical_json_bytes(payload: JsonValue) -> bytes:
    """Return RFC 8785 canonical UTF-8 bytes for a prepared JSON-native payload."""

    return rfc8785.dumps(payload)


def compute_content_hash(payload: JsonValue) -> ContentHash:
    """Hash a prepared canonical payload as SHA-256 over RFC 8785 bytes."""

    digest = hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
    return ContentHash(f"sha256:{digest}")
