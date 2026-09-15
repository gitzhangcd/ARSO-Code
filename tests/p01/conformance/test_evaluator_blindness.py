import pytest

from arso.p01.runtime.errors import EvaluatorBlindnessViolation
from arso.p01.runtime.evaluator_blindness import EvaluatorBlindnessGuard


def test_evaluator_guard_rejects_condition_metadata():
    guard = EvaluatorBlindnessGuard()
    with pytest.raises(EvaluatorBlindnessViolation):
        guard.check({"candidate_ref": "candidate-1", "condition": "ORACLE"})


def test_evaluator_guard_accepts_condition_blind_payload():
    guard = EvaluatorBlindnessGuard()
    assert guard.check({"candidate_ref": "candidate-1", "task_ref": "synthetic_001"}) is True
