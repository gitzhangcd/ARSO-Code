from __future__ import annotations

from datetime import datetime, timezone

import pytest

from di_contracts.core.models import ActorRef, ExactObjectRef, ObjectRef, TenantScope
from di_contracts.core.types import ActorId, ActorType, ContentHash, LogicalId, ObjectId, ObjectType, TenantId, TenantScopeType

HASH = ContentHash("sha256:" + "a" * 64)
HASH_B = ContentHash("sha256:" + "b" * 64)
NOW = datetime(2026, 9, 3, 3, 17, tzinfo=timezone.utc)


def oid(seed: str = "a") -> ObjectId:
    return ObjectId((seed * 20)[:20])


def lid(seed: str = "l") -> LogicalId:
    return LogicalId((seed * 20)[:20])


def actor(seed: str = "u") -> ActorRef:
    return ActorRef(actor_type=ActorType.USER, actor_id=ActorId((seed * 20)[:20]))


def tenant(seed: str = "t") -> TenantScope:
    return TenantScope(scope_type=TenantScopeType.TENANT, tenant_id=TenantId((seed * 20)[:20]))


def exact(type_name: str, seed: str = "x", h: ContentHash = HASH) -> ExactObjectRef:
    return ExactObjectRef(object_type=ObjectType(type_name), logical_id=lid(seed), version_id=oid(seed), content_hash=h)


def ref(type_name: str, seed: str = "r", h: ContentHash = HASH) -> ObjectRef:
    return ObjectRef(object_type=ObjectType(type_name), object_id=oid(seed), content_hash=h)


@pytest.fixture
def base_kwargs():
    return dict(
        schema_version="1.0",
        id=oid("i"),
        object_type="di.test.object",
        created_at=NOW,
        created_by=actor(),
        tenant_scope=tenant(),
        provenance={},
    )
