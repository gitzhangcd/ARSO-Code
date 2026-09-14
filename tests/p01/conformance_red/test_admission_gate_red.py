import pytest

pytestmark = [
    pytest.mark.p01_red,
    pytest.mark.xfail(strict=True, reason="I1 scientific-integrity enforcement gate"),
]


def test_scientific_admission_requires_integrity_pass() -> None:
    from arso.p01.runtime.integrity import ScientificAdmissionGate

    gate = ScientificAdmissionGate()
    assert gate.admit(integrity_status="FAIL") is False
