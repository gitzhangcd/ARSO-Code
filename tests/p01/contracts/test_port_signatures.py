import inspect

from arso.p01.ports.evaluation import Evaluator
from arso.p01.ports.repair import RepairRequestBuilder


def test_repair_request_builder_does_not_accept_sealed_truth() -> None:
    signature = inspect.signature(RepairRequestBuilder.build)
    assert "sealed_truth" not in signature.parameters
    assert "expected_repair_target" not in signature.parameters


def test_evaluator_signature_is_condition_blind() -> None:
    signature = inspect.signature(Evaluator.evaluate)
    assert "condition" not in signature.parameters
    assert "condition_type" not in signature.parameters
    assert "diagnosis" not in signature.parameters
