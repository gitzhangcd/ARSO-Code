from __future__ import annotations

from datetime import datetime, timezone
import math

import pytest
from pydantic import ValidationError

from design_intelligence.contracts.core import (
    ActorId,
    ActorRef,
    ActorType,
    CanonicalRevision,
    ExactObjectRef,
    ImmutableFact,
    LogicalObjectRef,
    ObjectRef,
    Provenance,
    TenantScope,
    TenantScopeType,
)
from design_intelligence.contracts.b01 import (
    STANDARD_REFERENCE_INTENT_CODES,
    BriefRequirement,
    ContextRefBinding,
    DesignContextBinding,
    DesignDecision,
    DesignRoute,
    DesignSpec,
    DesignSpecAssignment,
    DesignTaskBinding,
    ReferenceIntentBinding,
    RequirementStrength,
    StyleBrief,
)


REVISION_FIELDS = {
    "schema_version",
    "id",
    "object_type",
    "created_at",
    "created_by",
    "tenant_scope",
    "provenance",
    "extensions",
    "logical_id",
    "revision",
    "parent_refs",
}
FACT_FIELDS = {
    "schema_version",
    "id",
    "object_type",
    "created_at",
    "created_by",
    "tenant_scope",
    "provenance",
    "extensions",
}

STYLE_BRIEF_FIELDS = {
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
}
REFERENCE_INTENT_FIELDS = {
    "reference_asset_ref",
    "intent_codes",
    "application_scope",
    "preserve",
    "allow_change",
    "strength",
}
CONTEXT_BINDING_FIELDS = {"style_brief_ref", "bindings"}
DESIGN_DECISION_FIELDS = {
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
}
DESIGN_ROUTE_FIELDS = {
    "decision_ref",
    "route_name",
    "mechanisms",
    "constraints",
    "rationale",
}
DESIGN_SPEC_FIELDS = {
    "route_ref",
    "semantic_parameter_space_ref",
    "assignments",
    "reference_intent_refs",
    "constraints",
}
DESIGN_TASK_BINDING_FIELDS = {
    "design_state_ref",
    "style_brief_ref",
    "evaluation_contract_ref",
    "enterprise_hard_policy_refs",
    "risk_policy_ref",
    "budget_policy_ref",
    "intervention_policy_ref",
    "reference_task_spec_ref",
}


def _actor() -> ActorRef:
    return ActorRef(actor_type=ActorType("USER"), actor_id=ActorId("actor-1"))


def _scope() -> TenantScope:
    return TenantScope(scope_type=TenantScopeType.GLOBAL, tenant_id=None)


def _provenance() -> Provenance:
    return Provenance(source_refs=(), external_source_refs=())


def _exact_ref(object_type: str, suffix: str = "1") -> ExactObjectRef:
    return ExactObjectRef(
        object_type=object_type,
        logical_id=f"logical-{suffix}",
        version_id=f"version-{suffix}",
        content_hash="sha256:" + suffix[-1] * 64,
    )


def _object_ref(object_type: str, suffix: str = "2") -> ObjectRef:
    return ObjectRef(
        object_type=object_type,
        object_id=f"object-{suffix}",
        content_hash="sha256:" + suffix[-1] * 64,
    )


def _revision_kwargs(object_type: str, suffix: str = "1") -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "id": f"version-{suffix}",
        "object_type": object_type,
        "created_at": datetime(2026, 9, 5, 1, 0, tzinfo=timezone.utc),
        "created_by": _actor(),
        "tenant_scope": _scope(),
        "provenance": _provenance(),
        "extensions": {},
        "logical_id": f"logical-{suffix}",
        "revision": 1,
        "parent_refs": (),
    }


def _fact_kwargs(object_type: str, suffix: str = "7") -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "id": f"object-{suffix}",
        "object_type": object_type,
        "created_at": datetime(2026, 9, 5, 1, 0, tzinfo=timezone.utc),
        "created_by": _actor(),
        "tenant_scope": _scope(),
        "provenance": _provenance(),
        "extensions": {},
    }


def _brief_requirement() -> BriefRequirement:
    return BriefRequirement(
        statement="Preserve the clean silhouette",
        strength=RequirementStrength.MUST,
        dimension="silhouette",
    )


def _style_brief(**overrides: object) -> StyleBrief:
    values: dict[str, object] = {
        **_revision_kwargs("di.b01.style_brief", "1"),
        "category": None,
        "customer_segments": (),
        "market_channels": (),
        "season_occasions": (),
        "commercial_role": None,
        "price_positioning": None,
        "style_intent": (),
        "mood_aesthetic": (),
        "design_focus": (),
        "reference_intent_refs": (),
        "material_context": (),
        "fit_silhouette_direction": (),
        "novelty_expectation": None,
        "requirements": (),
    }
    values.update(overrides)
    return StyleBrief(**values)


def _reference_intent_binding(**overrides: object) -> ReferenceIntentBinding:
    values: dict[str, object] = {
        **_revision_kwargs("di.b01.reference_intent_binding", "2"),
        "reference_asset_ref": _object_ref("di.asset.reference", "2"),
        "intent_codes": ("SILHOUETTE_REFERENCE",),
        "application_scope": (),
        "preserve": (),
        "allow_change": (),
        "strength": RequirementStrength.MUST,
    }
    values.update(overrides)
    return ReferenceIntentBinding(**values)


def _context_binding(**overrides: object) -> DesignContextBinding:
    values: dict[str, object] = {
        **_revision_kwargs("di.b01.design_context_binding", "3"),
        "style_brief_ref": _exact_ref("di.b01.style_brief", "1"),
        "bindings": (),
    }
    values.update(overrides)
    return DesignContextBinding(**values)


def _decision(**overrides: object) -> DesignDecision:
    values: dict[str, object] = {
        **_revision_kwargs("di.b01.design_decision", "4"),
        "brief_ref": _exact_ref("di.b01.style_brief", "1"),
        "context_binding_ref": _exact_ref("di.b01.design_context_binding", "3"),
        "primary_focus": None,
        "secondary_focus": (),
        "visual_hierarchy": (),
        "silhouette_strategy": None,
        "volume_distribution": (),
        "construction_emphasis": (),
        "surface_complexity": None,
        "material_expression": (),
        "novelty_allocation": None,
        "commercial_risk_allocation": None,
    }
    values.update(overrides)
    return DesignDecision(**values)


def _route(**overrides: object) -> DesignRoute:
    values: dict[str, object] = {
        **_revision_kwargs("di.b01.design_route", "5"),
        "decision_ref": _exact_ref("di.b01.design_decision", "4"),
        "route_name": "volume-led route",
        "mechanisms": ("controlled_volume",),
        "constraints": (),
        "rationale": None,
    }
    values.update(overrides)
    return DesignRoute(**values)


def _spec(**overrides: object) -> DesignSpec:
    values: dict[str, object] = {
        **_revision_kwargs("di.b01.design_spec", "6"),
        "route_ref": _exact_ref("di.b01.design_route", "5"),
        "semantic_parameter_space_ref": _object_ref("di.b02.semantic_parameter_space", "6"),
        "assignments": (
            DesignSpecAssignment(
                parameter_key="silhouette.volume",
                value="moderate",
                strength=None,
            ),
        ),
        "reference_intent_refs": (),
        "constraints": (),
    }
    values.update(overrides)
    return DesignSpec(**values)


def _task_binding(**overrides: object) -> DesignTaskBinding:
    values: dict[str, object] = {
        **_fact_kwargs("di.b01.design_task_binding", "7"),
        "design_state_ref": _object_ref("di.b03.design_state", "7"),
        "style_brief_ref": _exact_ref("di.b01.style_brief", "1"),
        "evaluation_contract_ref": _object_ref("arso.evaluation_contract", "7"),
        "enterprise_hard_policy_refs": (),
        "risk_policy_ref": None,
        "budget_policy_ref": None,
        "intervention_policy_ref": None,
        "reference_task_spec_ref": _exact_ref("arso.reference_task_spec", "7"),
    }
    values.update(overrides)
    return DesignTaskBinding(**values)


def test_requirement_strength_has_exact_frozen_values() -> None:
    assert {member.value for member in RequirementStrength} == {
        "MUST",
        "PREFER",
        "EXPLORE",
        "AVOID",
        "FORBID",
    }


def test_standard_reference_intent_codes_are_recognized_without_closing_vocabulary() -> None:
    assert {
        "SILHOUETTE_REFERENCE",
        "DETAIL_REFERENCE",
        "MATERIAL_REFERENCE",
        "COLOR_REFERENCE",
        "STRUCTURE_REFERENCE",
        "MOOD_REFERENCE",
        "KEEP_REFERENCE",
        "EDIT_REFERENCE",
    } <= STANDARD_REFERENCE_INTENT_CODES
    custom = _reference_intent_binding(intent_codes=("CUSTOM_REFERENCE_INTENT",))
    assert custom.intent_codes == ("CUSTOM_REFERENCE_INTENT",)


def test_nested_value_shapes_are_exact() -> None:
    assert set(BriefRequirement.model_fields) == {"statement", "strength", "dimension"}
    assert set(ContextRefBinding.model_fields) == {"context_ref", "role"}
    assert set(DesignSpecAssignment.model_fields) == {"parameter_key", "value", "strength"}


def test_b01_object_classification_is_exact() -> None:
    for cls in (
        StyleBrief,
        ReferenceIntentBinding,
        DesignContextBinding,
        DesignDecision,
        DesignRoute,
        DesignSpec,
    ):
        assert issubclass(cls, CanonicalRevision)
    assert issubclass(DesignTaskBinding, ImmutableFact)
    assert not issubclass(DesignTaskBinding, CanonicalRevision)


@pytest.mark.parametrize(
    ("model", "expected_fields"),
    [
        (StyleBrief, REVISION_FIELDS | STYLE_BRIEF_FIELDS),
        (ReferenceIntentBinding, REVISION_FIELDS | REFERENCE_INTENT_FIELDS),
        (DesignContextBinding, REVISION_FIELDS | CONTEXT_BINDING_FIELDS),
        (DesignDecision, REVISION_FIELDS | DESIGN_DECISION_FIELDS),
        (DesignRoute, REVISION_FIELDS | DESIGN_ROUTE_FIELDS),
        (DesignSpec, REVISION_FIELDS | DESIGN_SPEC_FIELDS),
        (DesignTaskBinding, FACT_FIELDS | DESIGN_TASK_BINDING_FIELDS),
    ],
)
def test_b01_model_field_surfaces_are_exact(model: type, expected_fields: set[str]) -> None:
    assert set(model.model_fields) == expected_fields
    assert all(field.is_required() for field in model.model_fields.values())


def test_all_seven_b01_models_accept_minimal_frozen_wire_shapes() -> None:
    assert _style_brief().object_type.root == "di.b01.style_brief"
    assert _reference_intent_binding().object_type.root == "di.b01.reference_intent_binding"
    assert _context_binding().object_type.root == "di.b01.design_context_binding"
    assert _decision().object_type.root == "di.b01.design_decision"
    assert _route().object_type.root == "di.b01.design_route"
    assert _spec().object_type.root == "di.b01.design_spec"
    assert _task_binding().object_type.root == "di.b01.design_task_binding"


@pytest.mark.parametrize(
    ("factory", "wrong_type"),
    [
        (_style_brief, "di.b01.design_route"),
        (_reference_intent_binding, "di.b01.style_brief"),
        (_context_binding, "di.b01.design_decision"),
        (_decision, "di.b01.design_spec"),
        (_route, "di.b01.design_decision"),
        (_spec, "di.b01.design_route"),
        (_task_binding, "di.b01.style_brief"),
    ],
)
def test_each_b01_model_rejects_mismatched_object_type(factory, wrong_type: str) -> None:
    with pytest.raises(ValidationError):
        factory(object_type=wrong_type)


def test_three_frozen_non_empty_owner_sequences_are_enforced() -> None:
    with pytest.raises(ValidationError):
        _reference_intent_binding(intent_codes=())
    with pytest.raises(ValidationError):
        _route(mechanisms=())
    with pytest.raises(ValidationError):
        _spec(assignments=())


def test_other_b01_tuple_fields_may_be_empty() -> None:
    assert _style_brief().requirements == ()
    assert _context_binding().bindings == ()
    assert _route().constraints == ()
    assert _spec().reference_intent_refs == ()
    assert _task_binding().enterprise_hard_policy_refs == ()


def test_design_spec_assignment_rejects_non_finite_json_number() -> None:
    assert math.isnan(float("nan"))
    with pytest.raises(ValidationError):
        DesignSpecAssignment(parameter_key="x", value=float("nan"), strength=None)


def test_b01_committed_canonical_refs_reject_logical_authoring_refs() -> None:
    logical_ref = LogicalObjectRef(object_type="di.asset.reference", logical_id="logical-asset")
    with pytest.raises(ValidationError):
        _reference_intent_binding(reference_asset_ref=logical_ref)
    with pytest.raises(ValidationError):
        _task_binding(evaluation_contract_ref=logical_ref)


def test_runtime_and_b03_fields_are_rejected_as_extra_input() -> None:
    with pytest.raises(ValidationError):
        _route(selected=True)
    with pytest.raises(ValidationError):
        _spec(prompt="not-owned-by-b01")
    with pytest.raises(ValidationError):
        _task_binding(current_node="runtime-state")
