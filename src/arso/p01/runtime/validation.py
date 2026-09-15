"""Deterministic validation for the P0.1 synthetic harness."""

from arso.p01.contracts.enums import ValidationState
from arso.p01.contracts.synthetic import SyntheticValidationResult


class SyntheticValidator:
    def validate(
        self,
        trial_id: str,
        target_behavior_pass: bool,
        hard_constraints_pass: bool,
        baseline_immutable: bool,
        mutation_policy_pass: bool,
    ) -> SyntheticValidationResult:
        ok = all(
            (
                target_behavior_pass,
                hard_constraints_pass,
                baseline_immutable,
                mutation_policy_pass,
            )
        )
        state = ValidationState.ACCEPTED if ok else ValidationState.REJECTED
        reasons = (
            ()
            if ok
            else tuple(
                name
                for name, value in (
                    ("target_behavior", target_behavior_pass),
                    ("hard_constraints", hard_constraints_pass),
                    ("baseline_immutable", baseline_immutable),
                    ("mutation_policy", mutation_policy_pass),
                )
                if not value
            )
        )
        return SyntheticValidationResult(
            validation_id=f"validation-{trial_id}",
            trial_id=trial_id,
            state=state,
            target_behavior_pass=target_behavior_pass,
            hard_constraints_pass=hard_constraints_pass,
            baseline_immutable=baseline_immutable,
            mutation_policy_pass=mutation_policy_pass,
            reasons=reasons,
        )
