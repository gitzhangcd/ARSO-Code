"""Core contract namespace with P1 public exports preserved exactly."""

from .base import DIModel, FrozenDIModel
from .hashing import canonical_json_bytes, compute_content_hash
from .refs import CanonicalRef, ContentHash, ExactObjectRef, LogicalObjectRef, ObjectRef
from .shell import (
    ActorRef,
    CanonicalObject,
    CanonicalRevision,
    ImmutableFact,
    JsonValue,
    Provenance,
    TenantScope,
)
from .types import (
    ActorId,
    ActorType,
    CanonicalObjectClass,
    LogicalId,
    ObjectId,
    ObjectRevision,
    ObjectType,
    SchemaVersion,
    TenantId,
    TenantScopeType,
)

# P1 froze this public star-export surface. P2 shared-shell symbols remain
# explicit attributes of this module but are intentionally not added here.
__all__ = [
    "CanonicalObjectClass",
    "CanonicalRef",
    "ContentHash",
    "DIModel",
    "ExactObjectRef",
    "FrozenDIModel",
    "LogicalId",
    "LogicalObjectRef",
    "ObjectId",
    "ObjectRef",
    "ObjectType",
    "SchemaVersion",
    "canonical_json_bytes",
    "compute_content_hash",
]
