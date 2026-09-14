"""Diagnosis-treatment materialization port for ARSO P0.1."""

from typing import Protocol

from arso.p01.contracts.diagnosis import DiagnosisInjection
from arso.p01.contracts.fixture import PublicQualifiedFixture
from arso.p01.contracts.trial import P01TrialAssignment


class DiagnosisInjector(Protocol):
    """Materializes only the repair-visible diagnosis treatment payload."""

    def materialize(
        self,
        assignment: P01TrialAssignment,
        fixture: PublicQualifiedFixture,
    ) -> DiagnosisInjection:
        ...
