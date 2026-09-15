import inspect

from pydantic import ValidationError

from arso.p01.contracts import ValidationState


def test_i1_candidate_and_synthetic_contracts_are_importable():
    from arso.p01.contracts import (
        CandidateChangeRecord,
        MatchedBlockIntegrityReport,
        RepairProposal,
        SyntheticEvaluationContext,
        SyntheticEvaluationRecord,
        SyntheticMatchedBlockResult,
        SyntheticTrialOutcome,
        SyntheticValidationResult,
    )

    assert CandidateChangeRecord is not None
    assert MatchedBlockIntegrityReport is not None
    assert RepairProposal is not None
    assert SyntheticEvaluationContext is not None
    assert SyntheticEvaluationRecord is not None
    assert SyntheticMatchedBlockResult is not None
    assert SyntheticTrialOutcome is not None
    assert SyntheticValidationResult is not None


def test_evaluation_context_rejects_condition_metadata():
    from arso.p01.contracts import SyntheticEvaluationContext

    try:
        SyntheticEvaluationContext(
            context_id="ctx-1",
            task_ref="task-1",
            expected_mapping={"a": "input.a", "b": "input.b"},
            condition="ORACLE",
        )
    except ValidationError:
        pass
    else:
        raise AssertionError("evaluation context accepted condition metadata")


def test_evaluator_signature_has_no_condition_or_diagnosis_parameter():
    from arso.p01.ports.evaluation import Evaluator

    signature = inspect.signature(Evaluator.evaluate)
    assert "condition" not in signature.parameters
    assert "condition_type" not in signature.parameters
    assert "diagnosis" not in signature.parameters


def test_validation_result_uses_frozen_vocab():
    from arso.p01.contracts import SyntheticValidationResult

    result = SyntheticValidationResult(
        validation_id="val-1",
        trial_id="trial-1",
        state=ValidationState.ACCEPTED,
        target_behavior_pass=True,
        hard_constraints_pass=True,
        baseline_immutable=True,
        mutation_policy_pass=True,
        reasons=(),
    )
    assert result.state is ValidationState.ACCEPTED
