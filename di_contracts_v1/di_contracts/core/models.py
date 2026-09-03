from __future__ import annotations

from datetime import datetime
from typing import ClassVar

from pydantic import Field, field_validator, model_validator

from .base import DIModel, FrozenDIModel
from .types import (
    ActorId,
    ActorType,
    CanonicalObjectClass,
    ConcurrencyVersion,
    ContentHash,
    JsonValue,
    LogicalId,
    ObjectId,
    ObjectRevision,
    ObjectType,
    SchemaVersion,
    TenantId,
    TenantScopeType,
    ensure_utc,
)


class ActorRef(FrozenDIModel):
    actor_type: ActorType
    actor_id: ActorId


class TenantScope(FrozenDIModel):
    scope_type: TenantScopeType
    tenant_id: TenantId | None = None

    @model_validator(mode="after")
    def validate_scope(self):
        if self.scope_type == TenantScopeType.GLOBAL and self.tenant_id is not None:
            raise ValueError("GLOBAL scope cannot contain tenant_id")
        if self.scope_type == TenantScopeType.TENANT and self.tenant_id is None:
            raise ValueError("TENANT scope requires tenant_id")
        return self


class ExactObjectRef(FrozenDIModel):
    object_type: ObjectType
    logical_id: LogicalId
    version_id: ObjectId
    content_hash: ContentHash


class ObjectRef(FrozenDIModel):
    object_type: ObjectType
    object_id: ObjectId
    content_hash: ContentHash


class LogicalObjectRef(FrozenDIModel):
    object_type: ObjectType
    logical_id: LogicalId


CanonicalRef = ExactObjectRef | ObjectRef


class Provenance(FrozenDIModel):
    source_refs: tuple[CanonicalRef, ...] = ()
    command_ref: ObjectRef | None = None
    run_ref: ObjectRef | None = None
    external_source_refs: tuple[str, ...] = ()


class CanonicalObject(FrozenDIModel):
    schema_version: SchemaVersion
    id: ObjectId
    object_type: ObjectType
    created_at: datetime
    created_by: ActorRef
    tenant_scope: TenantScope
    provenance: Provenance = Field(default_factory=Provenance)
    extensions: dict[str, JsonValue] = Field(default_factory=dict)

    OBJECT_CLASS: ClassVar[CanonicalObjectClass]

    @field_validator("created_at")
    @classmethod
    def normalize_time(cls, value: datetime) -> datetime:
        return ensure_utc(value)


class CanonicalRevision(CanonicalObject):
    logical_id: LogicalId
    revision: ObjectRevision
    parent_refs: tuple[ExactObjectRef, ...] = ()
    OBJECT_CLASS: ClassVar[CanonicalObjectClass] = CanonicalObjectClass.CANONICAL_REVISION


class ImmutableFact(CanonicalObject):
    OBJECT_CLASS: ClassVar[CanonicalObjectClass] = CanonicalObjectClass.IMMUTABLE_FACT


class ImmutableRoot(CanonicalObject):
    OBJECT_CLASS: ClassVar[CanonicalObjectClass] = CanonicalObjectClass.IMMUTABLE_ROOT


class ImmutableGraphNode(CanonicalObject):
    OBJECT_CLASS: ClassVar[CanonicalObjectClass] = CanonicalObjectClass.IMMUTABLE_GRAPH_NODE


class SnapshotObject(CanonicalObject):
    OBJECT_CLASS: ClassVar[CanonicalObjectClass] = CanonicalObjectClass.SNAPSHOT


class OperationalControlState(FrozenDIModel):
    schema_version: SchemaVersion
    id: ObjectId
    object_type: ObjectType
    tenant_scope: TenantScope
    concurrency_version: ConcurrencyVersion
    updated_at: datetime
    updated_by: ActorRef
    extensions: dict[str, JsonValue] = Field(default_factory=dict)

    @field_validator("updated_at")
    @classmethod
    def normalize_time(cls, value: datetime) -> datetime:
        return ensure_utc(value)


class DerivedView(DIModel):
    pass
