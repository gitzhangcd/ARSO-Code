"""Strict base-model policy for ARSO P0.1 experimental contracts."""

from pydantic import BaseModel, ConfigDict


class P01Model(BaseModel):
    """Strict mutable base for P0.1 DTOs when mutability is intentional."""

    model_config = ConfigDict(extra="forbid", strict=True, validate_default=True)


class FrozenP01Model(P01Model):
    """Strict immutable base for P0.1 records and specifications."""

    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        validate_default=True,
        frozen=True,
    )
