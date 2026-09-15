import copy

import pytest

from arso.p01.adapters.fake.repair import DeterministicFakeRepairOperator
from arso.p01.contracts.repair import RepairRequest
from arso.p01.runtime.candidate import CandidateMaterializer
from arso.p01.runtime.errors import MutationPolicyViolation


def _request(diag_ref: str) -> RepairRequest:
    return RepairRequest(
        request_id=f"req-{diag_ref}",
        trial_id="trial-1",
        reference_task_ref="synthetic_001",
        baseline_system_ref="synthetic_001_baseline",
        visible_evidence_ref="synthetic_001_public_evidence",
        diagnosis_injection_ref=diag_ref,
        mutation_policy_ref="mapping_only_v1",
        repair_instruction_ref="synthetic_repair_instruction_v1",
        model_binding_ref="deterministic_fake_repair_v1",
        sampling_config_ref="deterministic_v1",
        output_contract_ref="repair_proposal_v1",
        budget_ref="synthetic_budget_v1",
        seed_ref="deterministic_seed_v1",
    )


def test_fake_repair_uses_visible_payload_not_hidden_condition():
    operator = DeterministicFakeRepairOperator(
        diagnosis_payloads={
            "diag-oracle": "The A↔B mapping rule in the transformation specification is reversed.",
            "diag-none": None,
        }
    )
    oracle = operator.repair(_request("diag-oracle"))
    none = operator.repair(_request("diag-none"))
    assert oracle.patch == {"a": "input.a", "b": "input.b"}
    assert none.patch == {"a": "input.b", "b": "input.a"}


def test_candidate_materialization_preserves_baseline():
    baseline = {"a": "input.b", "b": "input.a"}
    before = copy.deepcopy(baseline)
    operator = DeterministicFakeRepairOperator(
        diagnosis_payloads={
            "diag-oracle": "The A↔B mapping rule in the transformation specification is reversed."
        }
    )
    proposal = operator.repair(_request("diag-oracle"))
    candidate = CandidateMaterializer().materialize(
        base_snapshot_ref="synthetic_001_baseline",
        baseline_mapping=baseline,
        proposal=proposal,
        allowed_targets={"transformation_spec.mapping"},
    )
    assert baseline == before
    assert candidate.candidate_mapping == {"a": "input.a", "b": "input.b"}
    assert candidate.candidate_id != candidate.base_snapshot_ref


def test_candidate_rejects_out_of_policy_target():
    from arso.p01.contracts.candidate import RepairProposal

    proposal = RepairProposal(
        proposal_id="bad",
        trial_id="trial-1",
        changed_targets=("evaluator",),
        patch={"a": "input.a", "b": "input.b"},
        rationale=None,
    )
    with pytest.raises(MutationPolicyViolation):
        CandidateMaterializer().materialize(
            base_snapshot_ref="synthetic_001_baseline",
            baseline_mapping={"a": "input.b", "b": "input.a"},
            proposal=proposal,
            allowed_targets={"transformation_spec.mapping"},
        )
