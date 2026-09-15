"""Deterministic condition-blind evaluator for the synthetic P0.1 harness."""

from arso.p01.contracts.candidate import CandidateChangeRecord
from arso.p01.contracts.synthetic import SyntheticEvaluationContext, SyntheticEvaluationRecord


class SyntheticExactEvaluator:
    def evaluate(
        self,
        candidate: CandidateChangeRecord,
        context: SyntheticEvaluationContext,
    ) -> SyntheticEvaluationRecord:
        passed = dict(candidate.candidate_mapping) == dict(context.expected_mapping)
        return SyntheticEvaluationRecord(
            evaluation_id=f"eval-{candidate.trial_id}",
            trial_id=candidate.trial_id,
            candidate_ref=candidate.candidate_id,
            passed=passed,
            observations=("mapping-match" if passed else "mapping-mismatch",),
            condition_metadata_present=False,
        )
