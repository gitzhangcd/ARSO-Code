from pathlib import Path


ROOT = Path("experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001")


def test_synthetic_fixture_has_public_sealed_and_qualification_boundaries() -> None:
    assert (ROOT / "public" / "task.json").is_file()
    assert (ROOT / "public" / "baseline_state.json").is_file()
    assert (ROOT / "public" / "evidence.json").is_file()
    assert (ROOT / "sealed" / "planted_fault.json").is_file()
    assert (ROOT / "sealed" / "causal_truth.json").is_file()
    assert (ROOT / "sealed" / "oracle_diagnosis.json").is_file()
    assert (ROOT / "sealed" / "expected_repair_target.json").is_file()
    assert (ROOT / "qualification" / "qualification_record.json").is_file()
