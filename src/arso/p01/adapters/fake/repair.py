"""Deterministic fake repair adapter for P0.1 harness plumbing tests."""

from typing import Mapping

from arso.p01.contracts.candidate import RepairProposal
from arso.p01.contracts.repair import RepairRequest


class DeterministicFakeRepairOperator:
    def __init__(self, diagnosis_payloads: Mapping[str, str | None]) -> None:
        self._diagnosis_payloads = dict(diagnosis_payloads)

    def repair(self, request: RepairRequest) -> RepairProposal:
        payload = self._diagnosis_payloads.get(request.diagnosis_injection_ref)
        text = (payload or "").lower()
        if "mapping" in text and "reversed" in text:
            patch = {"a": "input.a", "b": "input.b"}
        else:
            patch = {"a": "input.b", "b": "input.a"}
        return RepairProposal(
            proposal_id=f"proposal-{request.request_id}",
            trial_id=request.trial_id,
            changed_targets=("transformation_spec.mapping",),
            patch=patch,
            rationale=None,
        )
