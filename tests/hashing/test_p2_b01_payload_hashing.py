from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from design_intelligence.contracts.b01 import (
    DesignSpec,
    DesignSpecAssignment,
    DesignTaskBinding,
    StyleBrief,
    b01_canonical_payload,
    compute_b01_content_hash,
)
from design_intelligence.contracts.core import (
    ActorId,
    ActorRef,
    ActorType,
    CanonicalObject,
    ExactObjectRef,
    ObjectRef,
    Provenance,
    TenantId,
    TenantScope,
    TenantScopeType,
)


STYLE_OWNER_FIELDS = {
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
SPEC_OWNER_FIELDS = {
    "route_ref",
    "semantic_parameter_space_ref",
    "assignments",
    "reference_intent_refs",
    "constraints",
}
TASK_BINDING_OWNER_FIELDS = {
    "design_state_ref",
    "style_brief_ref",
    "evaluation_contract_ref",
    "enterprise_hard_policy_refs",
    "risk_policy_ref",
    "budget_policy_ref",
    "intervention_policy_ref",
    "reference_task_spec_ref",
}
EXCLUDED_SHELL_FIELDS = {
    "id",
    "logical_id",
    "revision",
    "parent_refs",
    "created_at",
    "created_by",
    "tenant_scope",
    "provenance",
    "content_hash",
}


def _exact_ref(object_type: str, digit: str) -> ExactObjectRef:
    return ExactObjectRef(
        object_type=object_type,
        logical_id=f"logical-{digit}",
        version_id=f"version-{digit}",
        content_hash="sha256:" + digit * 64,
    )


def _object_ref(object_type: str, digit: str) -> ObjectRef:
    return ObjectRef(
        object_type=object_type,
        object_id=f"object-{digit}",
        content_hash="sha256:" + digit * 64,
    )


def _actor(actor_id: str = "actor-1") -> ActorRef:
    return ActorRef(actor_type=ActorType("USER"), actor_id=ActorId(actor_id))


def _global_scope() -> TenantScope:
    return TenantScope(scope_type=TenantScopeType.GLOBAL, tenant_id=None)


def _tenant_scope() -> TenantScope:
    return TenantScope(scope_type=TenantScopeType.TENANT, tenant_id=TenantId("tenant-9"))


def _style_brief(
    *,
    object_id: str = "version-1",
    logical_id: str = "logical-1",
    revision: int = 1,
    created_at: datetime = datetime(2026, 9, 5, 1, 0, tzinfo=timezone.utc),
    created_by: ActorRef | None = None,
    tenant_scope: TenantScope | None = None,
    provenance: Provenance | None = None,
    parent_refs: tuple[ExactObjectRef, ...] = (),
    category: str | None = "dress",
    extensions: dict[str, object] | None = None,
) -> StyleBrief:
    return StyleBrief(
        schema_version="1.0",
        id=object_id,
        object_type="di.b01.style_brief",
        created_at=created_at,
        created_by=created_by or _actor(),
        tenant_scope=tenant_scope or _global_scope(),
        provenance=provenance or Provenance(source_refs=(), external_source_refs=()),
        extensions=extensions or {},
        logical_id=logical_id,
        revision=revision,
        parent_refs=parent_refs,
        category=category,
        customer_segments=(),
        market_channels=(),
        season_occasions=(),
        commercial_role=None,
        price_positioning=None,
        style_intent=("clean",),
        mood_aesthetic=(),
        design_focus=(),
        reference_intent_refs=(),
        material_context=(),
        fit_silhouette_direction=(),
        novelty_expectation=None,
        requirements=(),
    )


def _design_spec() -> DesignSpec:
    return DesignSpec(
        schema_version="1.0",
        id="version-6",
        object_type="di.b01.design_spec",
        created_at=datetime(2026, 9, 5, 1, 0, tzinfo=timezone.utc),
        created_by=_actor(),
        tenant_scope=_global_scope(),
        provenance=Provenance(source_refs=(), external_source_refs=()),
        extensions={"owner_extension": {"enabled": True}},
        logical_id="logical-6",
        revision=1,
        parent_refs=(),
        route_ref=_exact_ref("di.b01.design_route", "5"),
        semantic_parameter_space_ref=_object_ref("di.b02.semantic_parameter_space", "6"),
        assignments=(
            DesignSpecAssignment(parameter_key="silhouette.volume", value="moderate", strength=None),
        ),
        reference_intent_refs=(),
        constraints=(),
    )


def _task_binding() -> DesignTaskBinding:
    return DesignTaskBinding(
        schema_version="1.0",
        id="object-7",
        object_type="di.b01.design_task_binding",
        created_at=datetime(2026, 9, 5, 1, 0, tzinfo=timezone.utc),
        created_by=_actor(),
        tenant_scope=_global_scope(),
        provenance=Provenance(source_refs=(), external_source_refs=()),
        extensions={},
        design_state_ref=_object_ref("di.b03.design_state", "7"),
        style_brief_ref=_exact_ref("di.b01.style_brief", "1"),
        evaluation_contract_ref=_object_ref("arso.evaluation_contract", "7"),
        enterprise_hard_policy_refs=(),
        risk_policy_ref=None,
        budget_policy_ref=None,
        intervention_policy_ref=None,
        reference_task_spec_ref=_exact_ref("arso.reference_task_spec", "7"),
    )


@pytest.mark.parametrize(
    ("obj", "owner_fields"),
    [
        (_style_brief(), STYLE_OWNER_FIELDS),
        (_design_spec(), SPEC_OWNER_FIELDS),
        (_task_binding(), TASK_BINDING_OWNER_FIELDS),
    ],
)
def test_b01_payload_has_exact_owner_semantic_shape(obj, owner_fields: set[str]) -> None:
    payload = b01_canonical_payload(obj)
    assert set(payload) == {"schema_version", "object_type", "extensions"} | owner_fields
    assert set(payload).isdisjoint(EXCLUDED_SHELL_FIELDS)
    assert payload["schema_version"] == "1.0"
    assert payload["object_type"] == obj.object_type.root


def test_b01_revision_hash_ignores_identity_order_and_audit_metadata() -> None:
    baseline = _style_brief()
    metadata_changed = _style_brief(
        object_id="version-99",
        logical_id="logical-99",
        revision=9,
        created_at=datetime(2026, 9, 6, 9, 30, tzinfo=timezone(timedelta(hours=8))),
        created_by=_actor("actor-99"),
        tenant_scope=_tenant_scope(),
        provenance=Provenance(
            source_refs=(_object_ref("di.external.source", "8"),),
            external_source_refs=("external-99",),
        ),
        parent_refs=(_exact_ref("di.b01.style_brief", "8"),),
    )
    assert compute_b01_content_hash(baseline) == compute_b01_content_hash(metadata_changed)


def test_b01_hash_changes_when_owner_semantics_or_extensions_change() -> None:
    baseline = _style_brief()
    category_changed = _style_brief(category="jacket")
    extension_changed = _style_brief(extensions={"experiment": {"arm": 2}})

    baseline_hash = compute_b01_content_hash(baseline)
    assert baseline_hash != compute_b01_content_hash(category_changed)
    assert baseline_hash != compute_b01_content_hash(extension_changed)


def test_b01_immutable_fact_payload_excludes_fact_audit_shell() -> None:
    payload = b01_canonical_payload(_task_binding())
    assert set(payload).isdisjoint(EXCLUDED_SHELL_FIELDS)
    assert "design_state_ref" in payload
    assert "reference_task_spec_ref" in payload


def test_b01_payload_rejects_non_b01_canonical_objects() -> None:
    generic = CanonicalObject(
        schema_version="1.0",
        id="object-x",
        object_type="di.other.object",
        created_at=datetime(2026, 9, 5, 1, 0, tzinfo=timezone.utc),
        created_by=_actor(),
        tenant_scope=_global_scope(),
        provenance=Provenance(source_refs=(), external_source_refs=()),
        extensions={},
    )
    with pytest.raises(TypeError):
        b01_canonical_payload(generic)
    with pytest.raises(TypeError):
        compute_b01_content_hash(generic)
