"""Generic P1 registry invariants derived from the persistence/reference matrix."""

from __future__ import annotations

from design_intelligence.contracts.core import CanonicalObjectClass


_HISTORICAL_OBJECT_REF_CLASSES = {
    CanonicalObjectClass.IMMUTABLE_FACT,
    CanonicalObjectClass.IMMUTABLE_ROOT,
    CanonicalObjectClass.IMMUTABLE_GRAPH_NODE,
    CanonicalObjectClass.SNAPSHOT,
}


def validate_persistence_policy(
    *,
    object_class: CanonicalObjectClass,
    historical_ssot: bool,
    versioned: bool,
    persistent_ref_kind: str,
) -> None:
    """Validate only generic class/history/version/reference invariants."""

    if object_class is CanonicalObjectClass.CANONICAL_REVISION:
        expected = (True, True, "EXACT_OBJECT_REF")
    elif object_class in _HISTORICAL_OBJECT_REF_CLASSES:
        expected = (True, False, "OBJECT_REF")
    elif object_class in {
        CanonicalObjectClass.OPERATIONAL_CONTROL_STATE,
        CanonicalObjectClass.DERIVED_VIEW,
    }:
        expected = (False, False, "NONE")
    else:  # pragma: no cover - enum exhaustiveness guard
        raise ValueError(f"unsupported canonical object class: {object_class}")

    actual = (historical_ssot, versioned, persistent_ref_kind)
    if actual != expected:
        raise ValueError(
            "registry persistence policy mismatch for "
            f"{object_class.value}: expected {expected}, got {actual}"
        )
