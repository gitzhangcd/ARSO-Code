from pathlib import Path

import pytest

from arso.p01.adapters.fake.fixture import SyntheticFixtureProvider
from arso.p01.contracts.enums import DiagnosisConditionType
from arso.p01.runtime.errors import SealedAccessDenied
from arso.p01.runtime.truth_firewall import TruthFirewall


ROOT = Path("experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001")


def test_provider_denies_non_oracle_sealed_diagnosis_access():
    provider = SyntheticFixtureProvider(ROOT, TruthFirewall())
    with pytest.raises(SealedAccessDenied):
        provider.load_oracle_diagnosis(DiagnosisConditionType.NONE)


def test_provider_audits_oracle_access_without_exposing_full_truth():
    provider = SyntheticFixtureProvider(ROOT, TruthFirewall())
    diagnosis = provider.load_oracle_diagnosis(DiagnosisConditionType.ORACLE)
    assert set(diagnosis) == {
        "diagnosis_id",
        "visible_payload",
        "allowed_use",
        "repair_visible_only_after_materialization",
        "harness_only",
    }
    assert provider.sealed_access_log == (
        ("ORACLE_DIAGNOSIS_MATERIALIZATION", "ORACLE"),
    )
