"""Public, sealed, and qualification fixture contracts for ARSO P0.1."""

from design_intelligence.contracts.core import ContentHash

from .base import FrozenP01Model


class PublicQualifiedFixture(FrozenP01Model):
    fixture_id: str
    task_ref: str
    baseline_state_ref: str
    evidence_ref: str
    qualification_ref: str
    public_content_hash: ContentHash


class SealedFixtureTruth(FrozenP01Model):
    fixture_id: str
    planted_fault_ref: str
    causal_truth_ref: str
    oracle_diagnosis_ref: str
    expected_repair_target_ref: str
    sealed_content_hash: ContentHash


class FixtureQualificationRecord(FrozenP01Model):
    qualification_id: str
    fixture_id: str
    status: str
    harness_only: bool
    statement: str
    qualified_at: str
