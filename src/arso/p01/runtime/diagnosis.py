"""Deterministic diagnosis-treatment materialization for the P0.1 synthetic harness."""

import hashlib
import json

from arso.p01.adapters.fake.fixture import SyntheticFixtureProvider
from arso.p01.contracts.diagnosis import DiagnosisInjection
from arso.p01.contracts.enums import DiagnosisConditionType
from arso.p01.contracts.trial import P01TrialAssignment


class SyntheticDiagnosisInjector:
    def __init__(self, provider: SyntheticFixtureProvider) -> None:
        self.provider = provider

    def _public_condition_payload(self, name: str) -> str:
        data = json.loads(
            (self.provider.root / "conditions" / f"{name}.json").read_text(
                encoding="utf-8"
            )
        )
        return str(data["visible_payload"])

    @staticmethod
    def _hash(payload: str | None) -> str | None:
        if payload is None:
            return None
        return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def materialize(self, assignment: P01TrialAssignment) -> DiagnosisInjection:
        condition = assignment.condition
        if condition is DiagnosisConditionType.ORACLE:
            payload = str(self.provider.load_oracle_diagnosis(condition)["visible_payload"])
        elif condition is DiagnosisConditionType.WRONG:
            payload = self._public_condition_payload("wrong")
        elif condition is DiagnosisConditionType.IMPLICIT:
            payload = self._public_condition_payload("implicit")
        else:
            payload = None

        return DiagnosisInjection(
            injection_id=f"diag-{assignment.trial_id}",
            trial_id=assignment.trial_id,
            condition=condition,
            visible_payload=payload,
            visible_payload_hash=self._hash(payload),
            materialization_method="synthetic-frozen-treatment-v1",
            source_visibility="REPAIR_VISIBLE",
        )
