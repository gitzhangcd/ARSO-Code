"""Explicit matched-control enforcement for the P0.1 synthetic block."""

from arso.p01.contracts.enums import DiagnosisConditionType, IntegrityStatus
from arso.p01.contracts.synthetic import MatchedBlockIntegrityReport
from arso.p01.contracts.trial import P01TrialAssignment


SHARED_FIELDS = (
    "fixture_ref",
    "reference_task_ref",
    "base_snapshot_ref",
    "visible_evidence_ref",
    "repair_operator_ref",
    "repair_instruction_ref",
    "mutation_policy_ref",
    "evaluator_binding_ref",
    "validation_plan_ref",
    "budget_policy_ref",
    "retry_policy_ref",
    "seed_assignment_ref",
    "pre_run_lock_hash",
    "matched_control_fingerprint",
)


def _same(assignments: tuple[P01TrialAssignment, ...], field: str) -> bool:
    if not assignments:
        return False
    first = getattr(assignments[0], field)
    return all(getattr(item, field) == first for item in assignments[1:])


class MatchedControlChecker:
    def check(
        self, assignments: tuple[P01TrialAssignment, ...]
    ) -> MatchedBlockIntegrityReport:
        conditions = [item.condition for item in assignments]
        expected = set(DiagnosisConditionType)
        all_required = (
            len(conditions) == len(expected)
            and set(conditions) == expected
            and len(set(conditions)) == len(expected)
        )

        field_equal = {field: _same(assignments, field) for field in SHARED_FIELDS}
        violations: list[str] = []
        if not all_required:
            violations.append("required_conditions")
        violations.extend(field for field, ok in field_equal.items() if not ok)

        all_shared = all(field_equal.values())
        final_status = (
            IntegrityStatus.PASS
            if all_required and all_shared
            else IntegrityStatus.FAIL
        )
        return MatchedBlockIntegrityReport(
            block_id=(assignments[0].matched_block_id if assignments else "missing-block"),
            all_required_conditions_present=all_required,
            shared_fixture=field_equal["fixture_ref"],
            shared_visible_evidence=field_equal["visible_evidence_ref"],
            shared_repair_operator=(
                field_equal["repair_operator_ref"]
                and field_equal["repair_instruction_ref"]
            ),
            shared_mutation_policy=field_equal["mutation_policy_ref"],
            shared_evaluator=(
                field_equal["evaluator_binding_ref"]
                and field_equal["validation_plan_ref"]
            ),
            shared_budget_policy=(
                field_equal["budget_policy_ref"] and field_equal["retry_policy_ref"]
            ),
            shared_seed_policy=field_equal["seed_assignment_ref"],
            shared_pre_run_lock=field_equal["pre_run_lock_hash"],
            shared_matched_control_fingerprint=field_equal[
                "matched_control_fingerprint"
            ],
            condition_is_only_intended_difference=all_shared,
            violations=tuple(violations),
            final_status=final_status,
        )
