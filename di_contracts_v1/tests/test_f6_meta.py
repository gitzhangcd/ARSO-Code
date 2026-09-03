from di_contracts.registry.manifest import REGISTRY_ENTRIES
from di_contracts.core.types import CanonicalObjectClass as C, PrimitiveOwner as O

FORBIDDEN_CANONICAL_NAMES = {
    "SystemCandidate", "Candidate", "Validation", "Knowledge", "State",
    "di.EvidenceBundle", "di.DiagnosticBelief", "di.ProbePlan", "di.ActionDecision",
    "DiagnosticHypothesis", "InterventionValidationResult", "DesignExecutionRecord",
}


def test_no_forbidden_canonical_names():
    names = {e.object_type.root for e in REGISTRY_ENTRIES}
    assert not (names & FORBIDDEN_CANONICAL_NAMES)


def test_no_di_shadow_of_arso_primitives():
    names = {e.object_type.root for e in REGISTRY_ENTRIES}
    for forbidden in ["di.evidence_bundle", "di.diagnostic_belief", "di.probe_plan", "di.action_decision", "di.validation_result"]:
        assert forbidden not in names


def test_all_registered_types_have_one_owner():
    assert all(e.primitive_owner in set(O) for e in REGISTRY_ENTRIES)


def test_derived_or_operational_never_historical_ssot():
    for e in REGISTRY_ENTRIES:
        if e.object_class in {C.OPERATIONAL_CONTROL_STATE, C.DERIVED_VIEW}:
            assert not e.historical_ssot


def test_review_session_closed_not_canonical_primitive():
    assert "di.b07.review_session_closed" not in {e.object_type.root for e in REGISTRY_ENTRIES}


def test_intervention_transaction_is_operational_not_second_truth():
    e = next(x for x in REGISTRY_ENTRIES if x.object_type.root == "di.b06.intervention_transaction")
    assert e.object_class == C.OPERATIONAL_CONTROL_STATE
    assert not e.historical_ssot
