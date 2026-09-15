from arso.p01.runtime.matched_control import SHARED_FIELDS


def test_treatment_fields_are_not_part_of_shared_fingerprint_fields():
    assert "condition" not in SHARED_FIELDS
    assert "diagnosis_condition_ref" not in SHARED_FIELDS
    assert "visible_evidence_ref" in SHARED_FIELDS
    assert "matched_control_fingerprint" in SHARED_FIELDS
