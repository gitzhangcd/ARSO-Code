from arso.p01.adapters.fake.evaluator import SyntheticExactEvaluator
from arso.p01.contracts.candidate import CandidateChangeRecord
from arso.p01.contracts.enums import ValidationState
from arso.p01.contracts.synthetic import SyntheticEvaluationContext
from arso.p01.runtime.validation import SyntheticValidator


def _candidate(mapping):
    return CandidateChangeRecord(
        candidate_id="candidate-1",
        trial_id="trial-1",
        base_snapshot_ref="baseline",
        changed_targets=("transformation_spec.mapping",),
        patch=mapping,
        candidate_mapping=mapping,
        materialization_status="MATERIALIZED",
    )


def test_exact_evaluator_scores_identity_and_reversed_mapping():
    evaluator = SyntheticExactEvaluator()
    context = SyntheticEvaluationContext(
        context_id="ctx-1",
        task_ref="synthetic_001",
        expected_mapping={"a": "input.a", "b": "input.b"},
    )
    assert evaluator.evaluate(
        _candidate({"a": "input.a", "b": "input.b"}), context
    ).passed is True
    assert evaluator.evaluate(
        _candidate({"a": "input.b", "b": "input.a"}), context
    ).passed is False


def test_validator_accepts_only_all_passes():
    validator = SyntheticValidator()
    accepted = validator.validate("trial-1", True, True, True, True)
    rejected = validator.validate("trial-1", False, True, True, True)
    assert accepted.state is ValidationState.ACCEPTED
    assert rejected.state is ValidationState.REJECTED
