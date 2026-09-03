from __future__ import annotations
from datetime import datetime
from di_contracts.core.models import ImmutableFact, ObjectRef
from di_contracts.core.types import ensure_utc
from pydantic import field_validator

class ReviewSessionClosedEvent(ImmutableFact):
    session_ref: ObjectRef
    closing_reason: str
    final_round_ref: ObjectRef | None = None
    occurred_at: datetime
    @field_validator("occurred_at")
    @classmethod
    def utc(cls, v: datetime): return ensure_utc(v)
