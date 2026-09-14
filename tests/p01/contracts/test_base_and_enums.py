from pydantic import ValidationError

from arso.p01.contracts.base import FrozenP01Model
from arso.p01.contracts.enums import DiagnosisConditionType


class Example(FrozenP01Model):
    value: str


def test_p01_models_are_strict_and_frozen() -> None:
    obj = Example(value="x")
    try:
        obj.value = "y"
    except ValidationError:
        pass
    else:
        raise AssertionError("frozen contract accepted mutation")


def test_p01_models_forbid_extra_fields() -> None:
    try:
        Example(value="x", hidden="forbidden")
    except ValidationError:
        pass
    else:
        raise AssertionError("strict contract accepted an extra field")


def test_diagnosis_condition_vocabulary_is_exact() -> None:
    assert {member.value for member in DiagnosisConditionType} == {
        "ORACLE",
        "WRONG",
        "NONE",
        "IMPLICIT",
    }
