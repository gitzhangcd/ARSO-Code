from __future__ import annotations

import re
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any, Annotated

from pydantic import Field, RootModel, field_validator, JsonValue

_OPAQUE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{15,127}$")
_OBJECT_TYPE_RE = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+$")
_SCHEMA_VERSION_RE = re.compile(r"^[1-9][0-9]*\.[0-9]+$")
_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


class _OpaqueString(RootModel[str]):
    @field_validator("root")
    @classmethod
    def validate_value(cls, value: str) -> str:
        if not _OPAQUE_ID_RE.fullmatch(value):
            raise ValueError("invalid opaque identifier")
        return value


class ObjectId(_OpaqueString):
    pass


class LogicalId(_OpaqueString):
    pass


class ActorId(_OpaqueString):
    pass


class TenantId(_OpaqueString):
    pass


class SchemaVersion(RootModel[str]):
    @field_validator("root")
    @classmethod
    def validate_value(cls, value: str) -> str:
        if not _SCHEMA_VERSION_RE.fullmatch(value):
            raise ValueError("schema_version must be MAJOR.MINOR")
        return value


class ObjectType(RootModel[str]):
    @field_validator("root")
    @classmethod
    def validate_value(cls, value: str) -> str:
        if not _OBJECT_TYPE_RE.fullmatch(value):
            raise ValueError("invalid namespaced object_type")
        return value


class ContentHash(RootModel[str]):
    @field_validator("root")
    @classmethod
    def validate_value(cls, value: str) -> str:
        if not _HASH_RE.fullmatch(value):
            raise ValueError("invalid sha256 content hash")
        return value


ObjectRevision = Annotated[int, Field(ge=1)]
ConcurrencyVersion = Annotated[int, Field(ge=0)]



class ActorType(StrEnum):
    USER = "USER"
    SERVICE = "SERVICE"
    AGENT = "AGENT"
    SYSTEM = "SYSTEM"
    EXTERNAL = "EXTERNAL"


class TenantScopeType(StrEnum):
    GLOBAL = "GLOBAL"
    TENANT = "TENANT"


class CanonicalObjectClass(StrEnum):
    CANONICAL_REVISION = "CANONICAL_REVISION"
    IMMUTABLE_FACT = "IMMUTABLE_FACT"
    IMMUTABLE_ROOT = "IMMUTABLE_ROOT"
    IMMUTABLE_GRAPH_NODE = "IMMUTABLE_GRAPH_NODE"
    SNAPSHOT = "SNAPSHOT"
    OPERATIONAL_CONTROL_STATE = "OPERATIONAL_CONTROL_STATE"
    DERIVED_VIEW = "DERIVED_VIEW"


class StateDomain(StrEnum):
    TASK = "TASK"
    SYSTEM = "SYSTEM"
    KNOWLEDGE = "KNOWLEDGE"
    REVIEW = "REVIEW"
    RUNTIME = "RUNTIME"
    INFRASTRUCTURE = "INFRASTRUCTURE"


class PrimitiveOwner(StrEnum):
    ARSO_CORE = "ARSO_CORE"
    DI_B01 = "DI_B01"
    DI_B02 = "DI_B02"
    DI_B03 = "DI_B03"
    DI_B04 = "DI_B04"
    DI_B05 = "DI_B05"
    DI_B06 = "DI_B06"
    DI_B07 = "DI_B07"
    DI_B08 = "DI_B08"
    INFRASTRUCTURE = "INFRASTRUCTURE"


class ReferenceKind(StrEnum):
    EXACT_OBJECT_REF = "EXACT_OBJECT_REF"
    OBJECT_REF = "OBJECT_REF"
    NONE = "NONE"


def ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("naive datetime is forbidden")
    return value.astimezone(timezone.utc)
