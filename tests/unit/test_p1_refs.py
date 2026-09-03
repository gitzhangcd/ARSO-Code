from __future__ import annotations

import pytest
from pydantic import ValidationError


def _core():
    import design_intelligence.contracts.core as core
    return core


def test_content_hash_accepts_exact_sha256_wire_form() -> None:
    core = _core()
    value = "sha256:" + "a" * 64
    assert core.ContentHash(value).root == value


@pytest.mark.parametrize(
    "value",
    [
        "a" * 64,
        "sha256:" + "A" * 64,
        "sha256:" + "a" * 63,
        "md5:" + "a" * 64,
    ],
)
def test_content_hash_rejects_noncanonical_wire_forms(value: str) -> None:
    core = _core()
    with pytest.raises(ValidationError):
        core.ContentHash(value)


def test_exact_object_ref_has_exact_fields() -> None:
    core = _core()
    ref = core.ExactObjectRef(
        object_type="di.test.object",
        logical_id="logical-id",
        version_id="version-id",
        content_hash="sha256:" + "1" * 64,
    )
    assert set(ref.model_dump()) == {"object_type", "logical_id", "version_id", "content_hash"}


def test_object_ref_has_exact_fields() -> None:
    core = _core()
    ref = core.ObjectRef(
        object_type="di.test.object",
        object_id="object-id",
        content_hash="sha256:" + "2" * 64,
    )
    assert set(ref.model_dump()) == {"object_type", "object_id", "content_hash"}


def test_logical_object_ref_has_exact_fields() -> None:
    core = _core()
    ref = core.LogicalObjectRef(object_type="di.test.object", logical_id="logical-id")
    assert set(ref.model_dump()) == {"object_type", "logical_id"}


def test_refs_forbid_extra_fields() -> None:
    core = _core()
    with pytest.raises(ValidationError):
        core.LogicalObjectRef(object_type="di.test.object", logical_id="logical-id", latest=True)


def test_refs_are_frozen() -> None:
    core = _core()
    ref = core.ObjectRef(
        object_type="di.test.object",
        object_id="object-id",
        content_hash="sha256:" + "3" * 64,
    )
    with pytest.raises(ValidationError):
        ref.object_id = core.ObjectId("changed")


def test_refs_reject_cross_nominal_identity_instances() -> None:
    core = _core()
    logical_id = core.LogicalId("logical-id")
    with pytest.raises(ValidationError):
        core.ObjectRef(
            object_type="di.test.object",
            object_id=logical_id,
            content_hash="sha256:" + "4" * 64,
        )
