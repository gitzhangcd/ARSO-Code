from __future__ import annotations
from datetime import datetime
from pydantic import field_validator
from di_contracts.core.base import FrozenDIModel
from di_contracts.core.models import ActorRef, ObjectRef, TenantScope
from di_contracts.core.types import ObjectId, ObjectType, SchemaVersion, ensure_utc

class DICommand(FrozenDIModel):
    schema_version: SchemaVersion
    command_id: ObjectId
    command_type: ObjectType
    tenant_scope: TenantScope
    actor_ref: ActorRef
    requested_at: datetime
    idempotency_key: ObjectId
    correlation_id: ObjectId | None = None
    @field_validator("requested_at")
    @classmethod
    def utc(cls, v: datetime): return ensure_utc(v)

class BranchMutationCommand(DICommand):
    branch_ref: ObjectRef
    expected_head_state_ref: ObjectRef
    expected_concurrency_version: int
