from arso.p01.contracts.enums import (
    DiagnosisConditionType,
    IntegrityStatus,
    ScientificAdmissionState,
)
from arso.p01.runtime.matched_block import SyntheticMatchedBlockRunner


def test_clean_synthetic_matched_block_executes_all_four_conditions():
    runner = SyntheticMatchedBlockRunner.default()
    result = runner.run()

    assert {outcome.condition for outcome in result.trial_outcomes} == set(
        DiagnosisConditionType
    )
    assert len(result.trial_outcomes) == 4
    assert len(
        {outcome.matched_control_fingerprint for outcome in result.trial_outcomes}
    ) == 1
    assert result.block_integrity.final_status is IntegrityStatus.PASS
    assert all(
        outcome.admission_state is ScientificAdmissionState.ADMITTED
        for outcome in result.trial_outcomes
    )
    assert result.scientific_interpretation is None

    oracle_events = [
        event
        for event in runner.provider.sealed_access_log
        if event[0] == "ORACLE_DIAGNOSIS_MATERIALIZATION"
    ]
    assert oracle_events == [("ORACLE_DIAGNOSIS_MATERIALIZATION", "ORACLE")]
