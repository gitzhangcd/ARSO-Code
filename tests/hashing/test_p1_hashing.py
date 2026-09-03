from __future__ import annotations

import hashlib

import pytest

from design_intelligence.contracts.core import ContentHash


def _hashing():
    import design_intelligence.contracts.core.hashing as hashing
    return hashing


def test_canonical_json_orders_object_properties() -> None:
    assert _hashing().canonical_json_bytes({"b": 1, "a": 2}) == b'{"a":2,"b":1}'


def test_canonical_json_preserves_unicode_utf8() -> None:
    assert _hashing().canonical_json_bytes({"name": "服装"}) == '{"name":"服装"}'.encode("utf-8")


def test_canonical_json_handles_nested_json_values() -> None:
    payload = {"z": [True, None, {"b": 2, "a": 1}], "a": "x"}
    assert _hashing().canonical_json_bytes(payload) == b'{"a":"x","z":[true,null,{"a":1,"b":2}]}'


def test_compute_content_hash_is_sha256_of_canonical_bytes() -> None:
    payload = {"b": 1, "a": 2}
    expected = "sha256:" + hashlib.sha256(b'{"a":2,"b":1}').hexdigest()
    result = _hashing().compute_content_hash(payload)
    assert isinstance(result, ContentHash)
    assert result.root == expected


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_canonical_json_rejects_nonfinite_numbers(value: float) -> None:
    with pytest.raises(Exception):
        _hashing().canonical_json_bytes({"value": value})


def test_canonical_json_rejects_non_string_object_keys() -> None:
    with pytest.raises(Exception):
        _hashing().canonical_json_bytes({1: "not-json-object-key"})
