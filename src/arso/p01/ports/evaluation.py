"""Condition-blind evaluation port for ARSO P0.1."""

from typing import Protocol

from arso.p01.contracts.candidate import CandidateChangeRecord
from arso.p01.contracts.synthetic import SyntheticEvaluationContext, SyntheticEvaluationRecord


class Evaluator(Protocol):
    """Evaluates a frozen candidate without receiving diagnosis-condition metadata."""

    def evaluate(
        self,
        candidate: CandidateChangeRecord,
        context: SyntheticEvaluationContext,
    ) -> SyntheticEvaluationRecord:
        ...
