import pytest

pytestmark = [
    pytest.mark.p01_red,
    pytest.mark.xfail(strict=True, reason="I1 scientific-integrity enforcement gate"),
]


def test_evaluator_runtime_input_is_condition_blind() -> None:
    from arso.p01.runtime.integrity import EvaluatorBlindnessGuard

    guard = EvaluatorBlindnessGuard()
    assert guard.check({"candidate_ref": "candidate-1", "condition": "ORACLE"}) is False
