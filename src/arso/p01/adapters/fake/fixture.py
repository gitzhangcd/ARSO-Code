"""Capability-aware local fixture provider for the synthetic P0.1 harness."""

import json
from pathlib import Path

from arso.p01.contracts.enums import DiagnosisConditionType, SealedAccessPurpose
from arso.p01.runtime.truth_firewall import TruthFirewall


class SyntheticFixtureProvider:
    def __init__(self, root: Path, firewall: TruthFirewall) -> None:
        self.root = root
        self.firewall = firewall
        self._sealed_access_log: list[tuple[str, str]] = []

    @property
    def sealed_access_log(self) -> tuple[tuple[str, str], ...]:
        return tuple(self._sealed_access_log)

    def _read(self, path: Path) -> dict[str, object]:
        return json.loads(path.read_text(encoding="utf-8"))

    def load_public(self) -> dict[str, object]:
        return {
            "task": self._read(self.root / "public" / "task.json"),
            "baseline": self._read(self.root / "public" / "baseline_state.json"),
            "evidence": self._read(self.root / "public" / "evidence.json"),
        }

    def load_oracle_diagnosis(
        self, condition: DiagnosisConditionType
    ) -> dict[str, object]:
        self.firewall.authorize(
            condition,
            SealedAccessPurpose.ORACLE_DIAGNOSIS_MATERIALIZATION,
        )
        self._sealed_access_log.append(
            (
                SealedAccessPurpose.ORACLE_DIAGNOSIS_MATERIALIZATION.value,
                condition.value,
            )
        )
        return self._read(self.root / "sealed" / "oracle_diagnosis.json")

    def load_evaluation_truth(self) -> dict[str, object]:
        self.firewall.authorize(None, SealedAccessPurpose.EVALUATION)
        self._sealed_access_log.append((SealedAccessPurpose.EVALUATION.value, "NONE"))
        return self._read(self.root / "sealed" / "expected_repair_target.json")
