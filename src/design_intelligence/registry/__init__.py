"""Registry namespace with the frozen P1 star-export surface preserved."""

from .b01 import B01_REGISTRY_MANIFEST
from .index import RegistryIndex
from .models import (
    ObjectRegistryEntry,
    ObjectRegistryManifest,
    PrimitiveOwner,
    ReferenceKind,
    StateDomain,
)

# P1 froze this public star-export surface. The P2 B01 manifest is available
# as an explicit module attribute but is intentionally not added to __all__.
__all__ = [
    "ObjectRegistryEntry",
    "ObjectRegistryManifest",
    "PrimitiveOwner",
    "ReferenceKind",
    "RegistryIndex",
    "StateDomain",
]
