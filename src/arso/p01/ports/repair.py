"""Repair-visible ports for ARSO P0.1."""

from typing import Protocol

from arso.p01.contracts.diagnosis import DiagnosisInjection
from arso.p01.contracts.fixture import PublicQualifiedFixture
from arso.p01.contracts.repair import RepairRequest
from arso.p01.contracts.trial import P01TrialAssignment


class RepairRequestBuilder(Protocol):
    """Builds the only request shape visible to a repair operator."""

    def build(
        self,
        assignment: P01TrialAssignment,
        fixture: PublicQualifiedFixture,
        diagnosis: DiagnosisInjection,
    ) -> RepairRequest:
        ...


class RepairOperator(Protocol):
    """Executes one repair request without evaluating its scientific success."""

    def repair(self, request: RepairRequest) -> str:
        ...
