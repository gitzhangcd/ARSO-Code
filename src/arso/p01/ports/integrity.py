"""Scientific-integrity checking port for ARSO P0.1."""

from typing import Protocol

from arso.p01.contracts.integrity import P01IntegrityReport


class IntegrityChecker(Protocol):
    """Evaluates whether a recorded trial is scientifically admissible."""

    def check_trial(self, trial_ref: str) -> P01IntegrityReport:
        ...
