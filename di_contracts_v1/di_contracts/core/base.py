from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class DIModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        validate_default=True,
        str_strip_whitespace=False,
        allow_inf_nan=False,
    )


class FrozenDIModel(DIModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        validate_default=True,
        str_strip_whitespace=False,
        allow_inf_nan=False,
        frozen=True,
    )
