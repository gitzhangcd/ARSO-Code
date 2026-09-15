"""Explicit error taxonomy for the P0.1 I1 synthetic harness."""


class P01HarnessError(RuntimeError):
    pass


class SealedAccessDenied(P01HarnessError):
    pass


class RepairVisibilityViolation(P01HarnessError):
    pass


class MatchedControlViolation(P01HarnessError):
    pass


class EvaluatorBlindnessViolation(P01HarnessError):
    pass


class MutationPolicyViolation(P01HarnessError):
    pass


class ScientificAdmissionDenied(P01HarnessError):
    pass


class SyntheticFixtureError(P01HarnessError):
    pass
