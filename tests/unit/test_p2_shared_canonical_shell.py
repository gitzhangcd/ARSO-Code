from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from design_intelligence.contracts.core import (
    ActorId,
    ActorRef,
    ActorType,
    CanonicalObject,
    CanonicalRevision,
    ExactObjectRef,
    ImmutableFact,
    LogicalObjectRef,
    ObjectRevision,
    Provenance,
    TenantId,
    TenantScope,
    TenantScopeType,
)


def _actor() -> ActorRef:
    return ActorRef(actor_type=ActorType("USER"), actor_id=ActorId("actor-1"))


def _global_scope() -> TenantScope:
    return TenantScope(scope_type=TenantScopeType.GLOBAL, tenant_id=None)


def _provenance() -> Provenance:
    return Provenance(source_refs=(), external_source_refs=())


def _canonical_kwargs(*, created_at: datetime) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "id": "object-1",
        "object_type": "di.test.object",
        "created_at": created_at,
        "created_by": _actor(),
        "tenant_scope": _global_scope(),
        "provenance": _provenance(),
        "extensions": {},
    }


def test_actor_id_and_tenant_id_are_strict_non_empty_nominal_strings() -> None:
    assert ActorId("actor-1").root == "actor-1"
    assert TenantId("tenant-1").root == "tenant-1"
    with pytest.raises(ValidationError):
        ActorId("")
    with pytest.raises(ValidationError):
        TenantId("")
    with pytest.raises(ValidationError):
        ActorId(123)


def test_actor_type_is_open_but_non_empty() -> None:
    assert ActorType("USER").root == "USER"
    assert ActorType("SERVICE").root == "SERVICE"
    assert ActorType("AGENT").root == "AGENT"
    assert ActorType("SYSTEM").root == "SYSTEM"
    assert ActorType("EXTERNAL").root == "EXTERNAL"
    assert ActorType("CUSTOM_INTEGRATION").root == "CUSTOM_INTEGRATION"
    with pytest.raises(ValidationError):
        ActorType("")


def test_actor_ref_has_exact_attribution_shape() -> None:
    actor = _actor()
    assert set(actor.model_fields) == {"actor_type", "actor_id"}
    with pytest.raises(ValidationError):
        ActorRef(
            actor_type=ActorType("USER"),
            actor_id=ActorId("actor-1"),
            display_name="not-frozen",
        )


def test_tenant_scope_type_is_closed_to_global_and_tenant() -> None:
    assert {member.value for member in TenantScopeType} == {"GLOBAL", "TENANT"}
    with pytest.raises(ValueError):
        TenantScopeType("PROJECT")


def test_tenant_scope_enforces_discriminator_coupling() -> None:
    global_scope = TenantScope(scope_type=TenantScopeType.GLOBAL, tenant_id=None)
    tenant_scope = TenantScope(
        scope_type=TenantScopeType.TENANT,
        tenant_id=TenantId("tenant-1"),
    )
    assert global_scope.tenant_id is None
    assert tenant_scope.tenant_id == TenantId("tenant-1")

    with pytest.raises(ValidationError):
        TenantScope(
            scope_type=TenantScopeType.GLOBAL,
            tenant_id=TenantId("tenant-1"),
        )
    with pytest.raises(ValidationError):
        TenantScope(scope_type=TenantScopeType.TENANT, tenant_id=None)


def test_provenance_accepts_only_persistent_canonical_refs() -> None:
    exact_ref = ExactObjectRef(
        object_type="di.test.revision",
        logical_id="logical-1",
        version_id="version-1",
        content_hash="sha256:" + "1" * 64,
    )
    provenance = Provenance(
        source_refs=(exact_ref,),
        external_source_refs=("external-source-1",),
    )
    assert provenance.source_refs == (exact_ref,)
    assert set(provenance.model_fields) == {"source_refs", "external_source_refs"}

    logical_ref = LogicalObjectRef(
        object_type="di.test.revision",
        logical_id="logical-1",
    )
    with pytest.raises(ValidationError):
        Provenance(source_refs=(logical_ref,), external_source_refs=())
    with pytest.raises(ValidationError):
        Provenance(source_refs=(), external_source_refs=("",))


def test_object_revision_is_integer_at_least_one() -> None:
    assert ObjectRevision(1).root == 1
    assert ObjectRevision(5).root == 5
    with pytest.raises(ValidationError):
        ObjectRevision(0)
    with pytest.raises(ValidationError):
        ObjectRevision("1")


def test_canonical_object_structural_field_set_is_exact() -> None:
    expected = {
        "schema_version",
        "id",
        "object_type",
        "created_at",
        "created_by",
        "tenant_scope",
        "provenance",
        "extensions",
    }
    assert set(CanonicalObject.model_fields) == expected
    assert set(ImmutableFact.model_fields) == expected
    assert set(CanonicalRevision.model_fields) == expected | {
        "logical_id",
        "revision",
        "parent_refs",
    }


def test_created_at_rejects_naive_datetime() -> None:
    with pytest.raises(ValidationError):
        CanonicalObject(**_canonical_kwargs(created_at=datetime(2026, 9, 5, 1, 2, 3)))


def test_created_at_normalizes_aware_datetime_to_utc() -> None:
    plus_eight = timezone(timedelta(hours=8))
    value = CanonicalObject(
        **_canonical_kwargs(created_at=datetime(2026, 9, 5, 9, 2, 3, tzinfo=plus_eight))
    )
    assert value.created_at == datetime(2026, 9, 5, 1, 2, 3, tzinfo=timezone.utc)
    assert value.created_at.tzinfo is timezone.utc


def test_canonical_revision_requires_explicit_revision_and_parent_refs() -> None:
    kwargs = _canonical_kwargs(created_at=datetime(2026, 9, 5, 1, 2, 3, tzinfo=timezone.utc))
    revision = CanonicalRevision(
        **kwargs,
        logical_id="logical-1",
        revision=1,
        parent_refs=(),
    )
    assert revision.revision == ObjectRevision(1)
    assert revision.parent_refs == ()

    with pytest.raises(ValidationError):
        CanonicalRevision(**kwargs, logical_id="logical-1", revision=1)
