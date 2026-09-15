"""Capability gate for sealed synthetic fixture access."""

from arso.p01.contracts.enums import DiagnosisConditionType, SealedAccessPurpose

from .errors import SealedAccessDenied


class TruthFirewall:
    def authorize(
        self,
        condition: DiagnosisConditionType | None,
        purpose: SealedAccessPurpose,
    ) -> bool:
        if purpose is SealedAccessPurpose.ORACLE_DIAGNOSIS_MATERIALIZATION:
            if condition is not DiagnosisConditionType.ORACLE:
                raise SealedAccessDenied(
                    "only ORACLE may materialize sealed oracle diagnosis"
                )
            return True

        if purpose in {
            SealedAccessPurpose.EVALUATION,
            SealedAccessPurpose.FIXTURE_QUALIFICATION,
            SealedAccessPurpose.SCIENTIFIC_AUDIT,
        }:
            if condition is not None:
                raise SealedAccessDenied(
                    "non-repair sealed access must not carry a trial condition"
                )
            return True

        raise SealedAccessDenied(f"unsupported sealed access purpose: {purpose}")
