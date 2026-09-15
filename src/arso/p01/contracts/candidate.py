"""Candidate and repair-proposal contracts for the P0.1 synthetic harness."""

from typing import Mapping

from .base import FrozenP01Model


class RepairProposal(FrozenP01Model):
    proposal_id: str
    trial_id: str
    changed_targets: tuple[str, ...]
    patch: Mapping[str, str]
    rationale: str | None = None


class CandidateChangeRecord(FrozenP01Model):
    candidate_id: str
    trial_id: str
    base_snapshot_ref: str
    changed_targets: tuple[str, ...]
    patch: Mapping[str, str]
    candidate_mapping: Mapping[str, str]
    materialization_status: str
