import pytest

from arso.p01.contracts.enums import DiagnosisConditionType, SealedAccessPurpose
from arso.p01.runtime.errors import SealedAccessDenied
from arso.p01.runtime.truth_firewall import TruthFirewall


def test_oracle_may_materialize_only_oracle_diagnosis():
    firewall = TruthFirewall()
    assert firewall.authorize(
        DiagnosisConditionType.ORACLE,
        SealedAccessPurpose.ORACLE_DIAGNOSIS_MATERIALIZATION,
    ) is True


@pytest.mark.parametrize(
    "condition",
    [
        DiagnosisConditionType.WRONG,
        DiagnosisConditionType.NONE,
        DiagnosisConditionType.IMPLICIT,
    ],
)
def test_non_oracle_may_not_materialize_oracle_diagnosis(condition):
    firewall = TruthFirewall()
    with pytest.raises(SealedAccessDenied):
        firewall.authorize(
            condition,
            SealedAccessPurpose.ORACLE_DIAGNOSIS_MATERIALIZATION,
        )


def test_evaluation_access_is_not_repair_condition_access():
    firewall = TruthFirewall()
    assert firewall.authorize(None, SealedAccessPurpose.EVALUATION) is True
