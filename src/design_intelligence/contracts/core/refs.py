"""P1 exact reference contracts."""

from __future__ import annotations

from typing import Annotated, TypeAlias

from pydantic import ConfigDict, Field, RootModel

from .base import FrozenDIModel
from .types import LogicalId, ObjectId, ObjectType


class ContentHash(RootModel[Annotated[str, Field(pattern=r"^sha256:[0-9a-f]{64}$")]]):
    """Self-describing SHA-256 content hash wire value."""

    model_config = ConfigDict(strict=True, frozen=True)


class ExactObjectRef(FrozenDIModel):
    """Persistent exact reference for one canonical revision."""

    object_type: ObjectType
    logical_id: LogicalId
    version_id: ObjectId
    content_hash: ContentHash


class ObjectRef(FrozenDIModel):
    """Persistent reference for one non-versioned immutable object."""

    object_type: ObjectType
    object_id: ObjectId
    content_hash: ContentHash


class LogicalObjectRef(FrozenDIModel):
    """Authoring-only logical reference that must resolve before runtime use."""

    object_type: ObjectType
    logical_id: LogicalId


CanonicalRef: TypeAlias = ExactObjectRef | ObjectRef
