"""Scientific-admission gate kept separate from repair validation."""

from arso.p01.contracts.enums import (
    IntegrityStatus,
    ScientificAdmissionState,
    ValidationState,
)
from arso.p01.contracts.integrity import P01IntegrityReport
from arso.p01.contracts.synthetic import SyntheticValidationResult


class ScientificAdmissionGate:
    def admit(
        self,
        integrity: P01IntegrityReport,
        validation: SyntheticValidationResult,
    ) -> ScientificAdmissionState:
        if integrity.final_status is not IntegrityStatus.PASS:
            return ScientificAdmissionState.INVALID_CONTAMINATION
        if validation.state is ValidationState.INCONCLUSIVE:
            return ScientificAdmissionState.INCOMPLETE
        return ScientificAdmissionState.ADMITTED
