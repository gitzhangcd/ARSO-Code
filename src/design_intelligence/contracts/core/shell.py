"""P2 frozen shared canonical-shell support types and structural bases."""

from __future__ import annotations

from datetime import datetime, timezone
import math
from typing import Annotated, TypeAlias

from pydantic import Field, field_validator, model_validator
from pydantic.types import JsonValue as PydanticJsonValue

from .base import FrozenDIModel
from .refs import CanonicalRef, ExactObjectRef
from .types import (
    ActorId,
    ActorType,
    LogicalId,
    ObjectId,
    ObjectRevision,
    ObjectType,
    SchemaVersion,
    TenantId,
    TenantScopeType,
)

JsonValue: TypeAlias = PydanticJsonValue
NonEmptyString = Annotated[str, Field(min_length=1)]


def ensure_finite_json_value(value: JsonValue) -> JsonValue:
    """Reject non-finite floats while preserving the frozen JSON-native shape."""

    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("JSONValue numbers must be finite")
    if isinstance(value, list):
        for item in value:
            ensure_finite_json_value(item)
    elif isinstance(value, dict):
        for item in value.values():
            ensure_finite_json_value(item)
    return value


class ActorRef(FrozenDIModel):
    """Exact two-part actor attribution reference."""

    actor_type: ActorType
    actor_id: ActorId


class TenantScope(FrozenDIModel):
    """Infrastructure-level GLOBAL or single-TENANT isolation scope."""

    scope_type: TenantScopeType
    tenant_id: TenantId | None

    @model_validator(mode="after")
    def validate_scope_coupling(self) -> "TenantScope":
        if self.scope_type is TenantScopeType.GLOBAL and self.tenant_id is not None:
            raise ValueError("GLOBAL tenant scope requires tenant_id=null")
        if self.scope_type is TenantScopeType.TENANT and self.tenant_id is None:
            raise ValueError("TENANT tenant scope requires a tenant_id")
        return self


class Provenance(FrozenDIModel):
    """Immutable source basis using only persistent canonical references."""

    source_refs: tuple[CanonicalRef, ...]
    external_source_refs: tuple[NonEmptyString, ...]


class CanonicalObject(FrozenDIModel):
    """Exact shared structural shell for canonical objects."""

    schema_version: SchemaVersion
    id: ObjectId
    object_type: ObjectType
    created_at: datetime
    created_by: ActorRef
    tenant_scope: TenantScope
    provenance: Provenance
    extensions: dict[str, JsonValue]

    @field_validator("created_at")
    @classmethod
    def normalize_created_at_to_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("created_at must be timezone-aware")
        return value.astimezone(timezone.utc)

    @field_validator("extensions")
    @classmethod
    def validate_extensions_are_finite_json(
        cls, value: dict[str, JsonValue]
    ) -> dict[str, JsonValue]:
        for item in value.values():
            ensure_finite_json_value(item)
        return value


class CanonicalRevision(CanonicalObject):
    """Canonical object revision with explicit logical identity and parentage."""

    logical_id: LogicalId
    revision: ObjectRevision
    parent_refs: tuple[ExactObjectRef, ...]


class ImmutableFact(CanonicalObject):
    """Non-versioned immutable fact structural shell."""
