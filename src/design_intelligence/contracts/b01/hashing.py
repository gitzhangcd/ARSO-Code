"""Frozen B01 owner-specific canonical payload and content hashing."""

from __future__ import annotations

from typing import TypeAlias

from design_intelligence.contracts.core import ContentHash, JsonValue, compute_content_hash

from .models import (
    DesignContextBinding,
    DesignDecision,
    DesignRoute,
    DesignSpec,
    DesignTaskBinding,
    ReferenceIntentBinding,
    StyleBrief,
)

B01CanonicalObject: TypeAlias = (
    StyleBrief
    | ReferenceIntentBinding
    | DesignContextBinding
    | DesignDecision
    | DesignRoute
    | DesignSpec
    | DesignTaskBinding
)

_COMMON_PAYLOAD_FIELDS = ("schema_version", "object_type")

_OWNER_FIELDS: dict[type[B01CanonicalObject], tuple[str, ...]] = {
    StyleBrief: (
        "category",
        "customer_segments",
        "market_channels",
        "season_occasions",
        "commercial_role",
        "price_positioning",
        "style_intent",
        "mood_aesthetic",
        "design_focus",
        "reference_intent_refs",
        "material_context",
        "fit_silhouette_direction",
        "novelty_expectation",
        "requirements",
    ),
    ReferenceIntentBinding: (
        "reference_asset_ref",
        "intent_codes",
        "application_scope",
        "preserve",
        "allow_change",
        "strength",
    ),
    DesignContextBinding: (
        "style_brief_ref",
        "bindings",
    ),
    DesignDecision: (
        "brief_ref",
        "context_binding_ref",
        "primary_focus",
        "secondary_focus",
        "visual_hierarchy",
        "silhouette_strategy",
        "volume_distribution",
        "construction_emphasis",
        "surface_complexity",
        "material_expression",
        "novelty_allocation",
        "commercial_risk_allocation",
    ),
    DesignRoute: (
        "decision_ref",
        "route_name",
        "mechanisms",
        "constraints",
        "rationale",
    ),
    DesignSpec: (
        "route_ref",
        "semantic_parameter_space_ref",
        "assignments",
        "reference_intent_refs",
        "constraints",
    ),
    DesignTaskBinding: (
        "design_state_ref",
        "style_brief_ref",
        "evaluation_contract_ref",
        "enterprise_hard_policy_refs",
        "risk_policy_ref",
        "budget_policy_ref",
        "intervention_policy_ref",
        "reference_task_spec_ref",
    ),
}


def b01_canonical_payload(obj: B01CanonicalObject) -> dict[str, JsonValue]:
    """Select exactly the frozen B01 semantic payload for one canonical object."""

    owner_fields = _OWNER_FIELDS.get(type(obj))
    if owner_fields is None:
        raise TypeError(f"B01 canonical payload is undefined for {type(obj).__name__}")

    dumped = obj.model_dump(mode="json")
    field_order = (*_COMMON_PAYLOAD_FIELDS, *owner_fields, "extensions")
    return {field: dumped[field] for field in field_order}


def compute_b01_content_hash(obj: B01CanonicalObject) -> ContentHash:
    """Compute the RFC8785/SHA-256 hash over the frozen B01 CanonicalPayload."""

    return compute_content_hash(b01_canonical_payload(obj))
