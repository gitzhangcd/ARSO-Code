"""P0-P2 nominal core types for Design Intelligence contracts."""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated

from pydantic import ConfigDict, Field, RootModel


class _NominalString(RootModel[str]):
    """Strict immutable runtime shell for nominal string identities."""

    model_config = ConfigDict(strict=True, frozen=True)


class ObjectId(_NominalString):
    """Opaque identity of one exact immutable object/version."""


class LogicalId(_NominalString):
    """Long-lived identity of one logical entity."""


class SchemaVersion(_NominalString):
    """Nominal schema-version identity."""


class ObjectType(_NominalString):
    """Nominal canonical object-type identity."""


class ActorId(RootModel[Annotated[str, Field(min_length=1)]]):
    """Strict non-empty nominal identity for an attributed actor."""

    model_config = ConfigDict(strict=True, frozen=True)


class ActorType(RootModel[Annotated[str, Field(min_length=1)]]):
    """Strict non-empty open vocabulary for actor attribution type."""

    model_config = ConfigDict(strict=True, frozen=True)


class TenantId(RootModel[Annotated[str, Field(min_length=1)]]):
    """Strict non-empty nominal tenant-isolation identity."""

    model_config = ConfigDict(strict=True, frozen=True)


class ObjectRevision(RootModel[Annotated[int, Field(ge=1)]]):
    """Server-assigned revision ordering metadata, never identity or parentage."""

    model_config = ConfigDict(strict=True, frozen=True)


class TenantScopeType(StrEnum):
    """Frozen tenant-isolation discriminator values."""

    GLOBAL = "GLOBAL"
    TENANT = "TENANT"


class CanonicalObjectClass(StrEnum):
    """Frozen canonical object-class wire values."""

    CANONICAL_REVISION = "CANONICAL_REVISION"
    IMMUTABLE_FACT = "IMMUTABLE_FACT"
    IMMUTABLE_ROOT = "IMMUTABLE_ROOT"
    IMMUTABLE_GRAPH_NODE = "IMMUTABLE_GRAPH_NODE"
    SNAPSHOT = "SNAPSHOT"
    OPERATIONAL_CONTROL_STATE = "OPERATIONAL_CONTROL_STATE"
    DERIVED_VIEW = "DERIVED_VIEW"
