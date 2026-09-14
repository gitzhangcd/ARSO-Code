"""Condition-blind evaluation port for ARSO P0.1."""

from typing import Protocol


class Evaluator(Protocol):
    """Evaluates a frozen candidate without receiving diagnosis-condition metadata."""

    def evaluate(
        self,
        candidate_ref: str,
        evaluation_context_ref: str,
    ) -> str:
        ...
