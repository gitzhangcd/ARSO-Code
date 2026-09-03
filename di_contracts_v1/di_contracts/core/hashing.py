from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, RootModel

from .models import CanonicalObject
from .types import ContentHash

_EXCLUDE = {"id", "logical_id", "revision", "parent_refs", "created_at", "created_by", "content_hash"}


def _plain(value: Any) -> Any:
    if isinstance(value, RootModel):
        return _plain(value.root)
    if isinstance(value, BaseModel):
        return {k: _plain(v) for k, v in value.__dict__.items() if k not in _EXCLUDE}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, tuple):
        return [_plain(v) for v in value]
    if isinstance(value, list):
        return [_plain(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    return value


def semantic_payload(obj: CanonicalObject) -> dict[str, Any]:
    return _plain(obj)


def canonical_json_bytes(payload: Any) -> bytes:
    # Deterministic JSON candidate. RFC 8785 compatibility requires an external cross-language fixture gate.
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return text.encode("utf-8")


def compute_content_hash(obj: CanonicalObject) -> ContentHash:
    digest = hashlib.sha256(canonical_json_bytes(semantic_payload(obj))).hexdigest()
    return ContentHash(f"sha256:{digest}")
