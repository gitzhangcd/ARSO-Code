"""P0 base-model policy for Design Intelligence contracts."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class DIModel(BaseModel):
    """Base model for Design Intelligence contract DTOs."""

    model_config = ConfigDict(extra="forbid", strict=True, validate_default=True)


class FrozenDIModel(DIModel):
    """Base model for immutable canonical contract models."""

    model_config = ConfigDict(extra="forbid", strict=True, validate_default=True, frozen=True)
