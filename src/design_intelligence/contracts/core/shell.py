"""P2 frozen shared canonical-shell support types and structural bases."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, TypeAlias

from pydantic import Field, FiniteFloat, field_validator, model_validator

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

JsonScalar: TypeAlias = None | bool | int | FiniteFloat | str
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
NonEmptyString = Annotated[str, Field(min_length=1)]


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


class CanonicalRevision(CanonicalObject):
    """Canonical object revision with explicit logical identity and parentage."""

    logical_id: LogicalId
    revision: ObjectRevision
    parent_refs: tuple[ExactObjectRef, ...]


class ImmutableFact(CanonicalObject):
    """Non-versioned immutable fact structural shell."""
