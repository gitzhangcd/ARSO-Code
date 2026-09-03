from datetime import datetime

import pytest
from pydantic import ValidationError

from di_contracts.core.hashing import compute_content_hash
from di_contracts.core.models import CanonicalRevision, ExactObjectRef, ImmutableFact, LogicalObjectRef, ObjectRef, TenantScope
from di_contracts.core.types import ContentHash, LogicalId, ObjectId, ObjectType, SchemaVersion, TenantScopeType
from conftest import HASH, NOW, actor, exact, lid, oid, tenant


class DemoRevision(CanonicalRevision):
    value: str

class DemoFact(ImmutableFact):
    value: str


def demo_revision(**overrides):
    data = dict(
        schema_version="1.0", id=oid("v"), object_type="di.test.demo_revision",
        created_at=NOW, created_by=actor(), tenant_scope=tenant(), provenance={},
        logical_id=lid("d"), revision=1, parent_refs=(), value="alpha"
    )
    data.update(overrides)
    return DemoRevision(**data)


def test_extra_forbid():
    with pytest.raises(ValidationError):
        demo_revision(extra_field=1)


def test_strict_rejects_string_revision():
    with pytest.raises(ValidationError):
        demo_revision(revision="1")


def test_nominal_ids_are_distinct_types():
    assert ObjectId is not LogicalId
    assert isinstance(oid("o"), ObjectId)
    assert isinstance(lid("l"), LogicalId)


def test_schema_version_only_major_minor():
    assert SchemaVersion("1.0").root == "1.0"
    for bad in ["v1", "1", "1.0.0", "latest"]:
        with pytest.raises(ValidationError):
            SchemaVersion(bad)


def test_namespaced_object_type_required():
    assert ObjectType("di.b01.design_spec").root == "di.b01.design_spec"
    with pytest.raises(ValidationError):
        ObjectType("DesignSpec")


def test_hash_wire_format():
    assert ContentHash("sha256:" + "0" * 64).root.startswith("sha256:")
    with pytest.raises(ValidationError):
        ContentHash("abc")


def test_naive_datetime_rejected():
    with pytest.raises(ValidationError):
        demo_revision(created_at=datetime(2026, 9, 3, 3, 0))


def test_tenant_scope_invariant():
    with pytest.raises(ValidationError):
        TenantScope(scope_type=TenantScopeType.GLOBAL, tenant_id="t" * 20)
    with pytest.raises(ValidationError):
        TenantScope(scope_type=TenantScopeType.TENANT, tenant_id=None)


def test_refs_are_distinct_models():
    e = exact("di.test.demo_revision")
    o = ObjectRef(object_type="di.test.fact", object_id=oid("f"), content_hash=HASH)
    l = LogicalObjectRef(object_type="di.test.demo_revision", logical_id=lid("d"))
    assert type(e) is ExactObjectRef
    assert type(o) is ObjectRef
    assert type(l) is LogicalObjectRef


def test_version_id_is_object_id():
    e = exact("di.test.demo_revision")
    assert isinstance(e.version_id, ObjectId)


def test_revision_ge_one():
    with pytest.raises(ValidationError):
        demo_revision(revision=0)


def test_frozen_canonical_object():
    x = demo_revision()
    with pytest.raises(ValidationError):
        x.value = "beta"


def test_semantic_hash_excludes_identity_fields():
    a = demo_revision(id=oid("a"), revision=1, created_by=actor("a"))
    b = demo_revision(id=oid("b"), revision=9, created_by=actor("b"))
    assert compute_content_hash(a) == compute_content_hash(b)


def test_semantic_hash_changes_on_semantics():
    a = demo_revision(value="alpha")
    b = demo_revision(value="beta")
    assert compute_content_hash(a) != compute_content_hash(b)
