"""Frozen P2 B01 exact canonical schemas."""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated, ClassVar

from pydantic import Field, field_validator, model_validator

from design_intelligence.contracts.core import (
    CanonicalRef,
    CanonicalRevision,
    ExactObjectRef,
    FrozenDIModel,
    ImmutableFact,
    JsonValue,
    ObjectRef,
    ObjectType,
)
from design_intelligence.contracts.core.shell import ensure_finite_json_value


class RequirementStrength(StrEnum):
    """Frozen B01 requirement-strength wire vocabulary."""

    MUST = "MUST"
    PREFER = "PREFER"
    EXPLORE = "EXPLORE"
    AVOID = "AVOID"
    FORBID = "FORBID"


STANDARD_REFERENCE_INTENT_CODES = frozenset(
    {
        "SILHOUETTE_REFERENCE",
        "DETAIL_REFERENCE",
        "MATERIAL_REFERENCE",
        "COLOR_REFERENCE",
        "STRUCTURE_REFERENCE",
        "MOOD_REFERENCE",
        "KEEP_REFERENCE",
        "EDIT_REFERENCE",
    }
)


class BriefRequirement(FrozenDIModel):
    """One authored B01 brief constraint or preference."""

    statement: str
    strength: RequirementStrength
    dimension: str | None


class ContextRefBinding(FrozenDIModel):
    """Role-bearing binding to persistent canonical context."""

    context_ref: CanonicalRef
    role: str


class DesignSpecAssignment(FrozenDIModel):
    """One semantic parameter assignment owned by a DesignSpec."""

    parameter_key: str
    value: JsonValue
    strength: RequirementStrength | None

    @field_validator("value")
    @classmethod
    def validate_finite_json_value(cls, value: JsonValue) -> JsonValue:
        return ensure_finite_json_value(value)


class _B01CanonicalRevision(CanonicalRevision):
    """Internal guard for the fixed object_type of a B01 canonical revision."""

    _EXPECTED_OBJECT_TYPE: ClassVar[str]

    @model_validator(mode="after")
    def validate_b01_object_type(self) -> "_B01CanonicalRevision":
        if self.object_type.root != self._EXPECTED_OBJECT_TYPE:
            raise ValueError(
                f"object_type must be {self._EXPECTED_OBJECT_TYPE!r} for {type(self).__name__}"
            )
        return self


class _B01ImmutableFact(ImmutableFact):
    """Internal guard for the fixed object_type of a B01 immutable fact."""

    _EXPECTED_OBJECT_TYPE: ClassVar[str]

    @model_validator(mode="after")
    def validate_b01_object_type(self) -> "_B01ImmutableFact":
        if self.object_type.root != self._EXPECTED_OBJECT_TYPE:
            raise ValueError(
                f"object_type must be {self._EXPECTED_OBJECT_TYPE!r} for {type(self).__name__}"
            )
        return self


def _fixed_object_type_schema(value: str):
    """Keep ObjectType runtime validation while publishing the fixed schema constant."""
    return Field(json_schema_extra={"const": value})


class StyleBrief(_B01CanonicalRevision):
    """B01 authored task brief and requirement envelope."""

    _EXPECTED_OBJECT_TYPE = "di.b01.style_brief"

    object_type: ObjectType = _fixed_object_type_schema(_EXPECTED_OBJECT_TYPE)
    category: str | None
    customer_segments: tuple[str, ...]
    market_channels: tuple[str, ...]
    season_occasions: tuple[str, ...]
    commercial_role: str | None
    price_positioning: str | None
    style_intent: tuple[str, ...]
    mood_aesthetic: tuple[str, ...]
    design_focus: tuple[str, ...]
    reference_intent_refs: tuple[ExactObjectRef, ...]
    material_context: tuple[str, ...]
    fit_silhouette_direction: tuple[str, ...]
    novelty_expectation: str | None
    requirements: tuple[BriefRequirement, ...]


class ReferenceIntentBinding(_B01CanonicalRevision):
    """Authored semantic intent for how one reference asset may be used."""

    _EXPECTED_OBJECT_TYPE = "di.b01.reference_intent_binding"

    object_type: ObjectType = _fixed_object_type_schema(_EXPECTED_OBJECT_TYPE)
    reference_asset_ref: CanonicalRef
    intent_codes: Annotated[tuple[str, ...], Field(min_length=1)]
    application_scope: tuple[str, ...]
    preserve: tuple[str, ...]
    allow_change: tuple[str, ...]
    strength: RequirementStrength


class DesignContextBinding(_B01CanonicalRevision):
    """Authored persistent context bindings for one StyleBrief revision."""

    _EXPECTED_OBJECT_TYPE = "di.b01.design_context_binding"

    object_type: ObjectType = _fixed_object_type_schema(_EXPECTED_OBJECT_TYPE)
    style_brief_ref: ExactObjectRef
    bindings: tuple[ContextRefBinding, ...]


class DesignDecision(_B01CanonicalRevision):
    """B01 semantic design decision derived from a brief and bound context."""

    _EXPECTED_OBJECT_TYPE = "di.b01.design_decision"

    object_type: ObjectType = _fixed_object_type_schema(_EXPECTED_OBJECT_TYPE)
    brief_ref: ExactObjectRef
    context_binding_ref: ExactObjectRef
    primary_focus: str | None
    secondary_focus: tuple[str, ...]
    visual_hierarchy: tuple[str, ...]
    silhouette_strategy: str | None
    volume_distribution: tuple[str, ...]
    construction_emphasis: tuple[str, ...]
    surface_complexity: str | None
    material_expression: tuple[str, ...]
    novelty_allocation: str | None
    commercial_risk_allocation: str | None


class DesignRoute(_B01CanonicalRevision):
    """One authored mechanism route implementing a DesignDecision."""

    _EXPECTED_OBJECT_TYPE = "di.b01.design_route"

    object_type: ObjectType = _fixed_object_type_schema(_EXPECTED_OBJECT_TYPE)
    decision_ref: ExactObjectRef
    route_name: str
    mechanisms: Annotated[tuple[str, ...], Field(min_length=1)]
    constraints: tuple[BriefRequirement, ...]
    rationale: str | None


class DesignSpec(_B01CanonicalRevision):
    """B01 semantic parameter assignment contract before compilation/execution."""

    _EXPECTED_OBJECT_TYPE = "di.b01.design_spec"

    object_type: ObjectType = _fixed_object_type_schema(_EXPECTED_OBJECT_TYPE)
    route_ref: ExactObjectRef
    semantic_parameter_space_ref: CanonicalRef
    assignments: Annotated[tuple[DesignSpecAssignment, ...], Field(min_length=1)]
    reference_intent_refs: tuple[ExactObjectRef, ...]
    constraints: tuple[BriefRequirement, ...]


class DesignTaskBinding(_B01ImmutableFact):
    """Immutable binding between a design state/brief and external task policy contracts."""

    _EXPECTED_OBJECT_TYPE = "di.b01.design_task_binding"

    object_type: ObjectType = _fixed_object_type_schema(_EXPECTED_OBJECT_TYPE)
    design_state_ref: ObjectRef
    style_brief_ref: ExactObjectRef
    evaluation_contract_ref: CanonicalRef
    enterprise_hard_policy_refs: tuple[CanonicalRef, ...]
    risk_policy_ref: CanonicalRef | None
    budget_policy_ref: CanonicalRef | None
    intervention_policy_ref: CanonicalRef | None
    reference_task_spec_ref: ExactObjectRef
