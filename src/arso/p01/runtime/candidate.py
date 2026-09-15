"""Immutable candidate materialization for the P0.1 synthetic harness."""

from collections.abc import Mapping, Set

from arso.p01.contracts.candidate import CandidateChangeRecord, RepairProposal

from .errors import MutationPolicyViolation


class CandidateMaterializer:
    def materialize(
        self,
        base_snapshot_ref: str,
        baseline_mapping: Mapping[str, str],
        proposal: RepairProposal,
        allowed_targets: Set[str],
    ) -> CandidateChangeRecord:
        if not set(proposal.changed_targets).issubset(set(allowed_targets)):
            raise MutationPolicyViolation(
                "repair proposal targets outside the frozen mutation policy"
            )

        candidate_mapping = dict(baseline_mapping)
        candidate_mapping.update(dict(proposal.patch))
        return CandidateChangeRecord(
            candidate_id=f"candidate:{proposal.trial_id}:{proposal.proposal_id}",
            trial_id=proposal.trial_id,
            base_snapshot_ref=base_snapshot_ref,
            changed_targets=proposal.changed_targets,
            patch=dict(proposal.patch),
            candidate_mapping=candidate_mapping,
            materialization_status="MATERIALIZED",
        )
