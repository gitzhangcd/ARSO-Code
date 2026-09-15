from arso.p01.contracts.enums import IntegrityStatus
from arso.p01.runtime.matched_block import SyntheticMatchedBlockRunner


def test_contaminated_block_is_rejected_when_one_arm_uses_different_evidence():
    runner = SyntheticMatchedBlockRunner.default()
    result = runner.run(
        contamination={
            "WRONG": {"visible_evidence_ref": "different-evidence"},
        }
    )
    assert result.block_integrity.final_status is IntegrityStatus.FAIL
    assert result.block_integrity.shared_visible_evidence is False
