"""Runtime guard that rejects condition metadata at the evaluator boundary."""

from collections.abc import Mapping

from .errors import EvaluatorBlindnessViolation


FORBIDDEN = {
    "condition",
    "condition_type",
    "diagnosis",
    "diagnosis_injection",
    "repair_reasoning",
    "matched_arm_label",
}


class EvaluatorBlindnessGuard:
    def check(self, payload: Mapping[str, object]) -> bool:
        leaked = FORBIDDEN.intersection(payload)
        if leaked:
            raise EvaluatorBlindnessViolation(
                f"forbidden evaluator metadata: {sorted(leaked)}"
            )
        return True
