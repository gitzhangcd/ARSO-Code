# ARSO P0.1 I1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the smallest deterministic P0.1 scientific harness that turns the I0 contract skeleton into an executable four-condition synthetic matched block with enforceable truth isolation, condition-blind evaluation, matched-control checking, immutable candidate materialization, and scientific-admission gating.

**Architecture:** Extend `src/arso/p01` only on branch `arso-p0-1-i1`, preserving the I0 branch as an immutable checkpoint. Implement a thin local runtime plus fake adapters; all four diagnosis conditions traverse the same path, and only `DiagnosisInjection.visible_payload` may differ as treatment. Real provider calls, Batch-001 execution, retry/budget/resume engines, and full D2/D3 orchestration remain deferred.

**Tech Stack:** Python 3.12, Pydantic 2.12+, pytest 8, repository-local JSON/YAML fixture files, stdlib only for new runtime logic.

**Spec:** `docs/superpowers/specs/2026-09-14-arso-p0-1-i1-design.md`

## Global Constraints

- Start from I0 checkpoint `cf7a974346ffe685f6c5ed809651690055eb3643`; do not mutate branch `arso-p0-1-i0`.
- P0.1 treatment vocabulary remains exactly `ORACLE | WRONG | NONE | IMPLICIT`.
- `DiagnosisCondition = only intended treatment difference`.
- Non-Oracle repair flow must never obtain sealed oracle diagnosis or any other sealed truth.
- Oracle materialization may expose only the approved oracle diagnosis payload, never full causal truth, expected repair target, or scoring truth.
- Repair must never consume evaluator output.
- Evaluator must be condition-blind by both signature and runtime guard.
- Candidate materialization must preserve baseline immutability and reject changes outside `transformation_spec.mapping`.
- Validation acceptance must never imply scientific admission.
- Matched-block integrity must enforce shared non-treatment controls across all four arms.
- Synthetic fixture execution is harness verification only; it must never produce a P0.1 treatment-effect claim.
- No real provider SDK, network model call, Batch-001 data, database, queue, workflow framework, retry engine, budget manager, crash resume, statistical treatment-effect analysis, or production deployment.
- Do not modify frozen `src/design_intelligence/contracts/` or `di_contracts_v1/`.
- Add no new runtime dependency.
- Follow strict TDD: each task begins with a failing test, verifies the intended failure, implements the minimum behavior, reruns tests, and commits.

---

## File Structure Locked by This Plan

```text
src/arso/p01/
├── contracts/
│   ├── candidate.py
│   └── synthetic.py
├── runtime/
│   ├── __init__.py
│   ├── errors.py
│   ├── truth_firewall.py
│   ├── diagnosis.py
│   ├── repair_request.py
│   ├── candidate.py
│   ├── evaluator_blindness.py
│   ├── validation.py
│   ├── admission.py
│   ├── integrity.py
│   ├── matched_control.py
│   └── matched_block.py
└── adapters/
    └── fake/
        ├── __init__.py
        ├── fixture.py
        ├── repair.py
        └── evaluator.py

experiments/p0_1_oracle_diagnosis/
└── fixtures/synthetic_001/
    └── conditions/
        ├── wrong.json
        └── implicit.json

tests/p01/
├── conformance/
├── runtime/
└── e2e/
```

I1 may keep existing I0 contract files and ports, but it must not create a second competing repair/evaluation pipeline.

---

### Task 1: Harden the I1 harness contracts and typed port surface

**Files:**
- Create: `src/arso/p01/contracts/candidate.py`
- Create: `src/arso/p01/contracts/synthetic.py`
- Modify: `src/arso/p01/contracts/__init__.py`
- Modify: `src/arso/p01/ports/repair.py`
- Modify: `src/arso/p01/ports/evaluation.py`
- Test: `tests/p01/runtime/test_i1_contracts_and_ports.py`

**Interfaces:**
- Consumes: `FrozenP01Model`, `RepairRequest`, `ValidationState`, `IntegrityStatus`, `DiagnosisConditionType`.
- Produces: `RepairProposal`, `CandidateChangeRecord`, `SyntheticEvaluationContext`, `SyntheticEvaluationRecord`, `SyntheticValidationResult`, `SyntheticTrialOutcome`, `MatchedBlockIntegrityReport`, `SyntheticMatchedBlockResult`.
- Refines `RepairOperator.repair(request: RepairRequest) -> RepairProposal`.
- Refines `Evaluator.evaluate(candidate: CandidateChangeRecord, context: SyntheticEvaluationContext) -> SyntheticEvaluationRecord` while remaining condition-blind.

- [ ] **Step 1: Write failing contract/port tests**

```python
import inspect

from pydantic import ValidationError

from arso.p01.contracts import ValidationState


def test_i1_candidate_and_synthetic_contracts_are_importable():
    from arso.p01.contracts import (
        CandidateChangeRecord,
        MatchedBlockIntegrityReport,
        RepairProposal,
        SyntheticEvaluationContext,
        SyntheticEvaluationRecord,
        SyntheticMatchedBlockResult,
        SyntheticTrialOutcome,
        SyntheticValidationResult,
    )

    assert CandidateChangeRecord is not None
    assert MatchedBlockIntegrityReport is not None
    assert RepairProposal is not None
    assert SyntheticEvaluationContext is not None
    assert SyntheticEvaluationRecord is not None
    assert SyntheticMatchedBlockResult is not None
    assert SyntheticTrialOutcome is not None
    assert SyntheticValidationResult is not None


def test_evaluation_context_rejects_condition_metadata():
    from arso.p01.contracts import SyntheticEvaluationContext

    try:
        SyntheticEvaluationContext(
            context_id="ctx-1",
            task_ref="task-1",
            expected_mapping={"a": "input.a", "b": "input.b"},
            condition="ORACLE",
        )
    except ValidationError:
        pass
    else:
        raise AssertionError("evaluation context accepted condition metadata")


def test_evaluator_signature_has_no_condition_or_diagnosis_parameter():
    from arso.p01.ports.evaluation import Evaluator

    signature = inspect.signature(Evaluator.evaluate)
    assert "condition" not in signature.parameters
    assert "condition_type" not in signature.parameters
    assert "diagnosis" not in signature.parameters


def test_validation_result_uses_frozen_vocab():
    from arso.p01.contracts import SyntheticValidationResult

    result = SyntheticValidationResult(
        validation_id="val-1",
        trial_id="trial-1",
        state=ValidationState.ACCEPTED,
        target_behavior_pass=True,
        hard_constraints_pass=True,
        baseline_immutable=True,
        mutation_policy_pass=True,
        reasons=(),
    )
    assert result.state is ValidationState.ACCEPTED
```

- [ ] **Step 2: Run test to verify RED**

Run:

```bash
pytest tests/p01/runtime/test_i1_contracts_and_ports.py -q
```

Expected: FAIL during import because I1 contract classes do not yet exist.

- [ ] **Step 3: Implement the minimal typed contracts**

`src/arso/p01/contracts/candidate.py`:

```python
from typing import Mapping

from .base import FrozenP01Model


class RepairProposal(FrozenP01Model):
    proposal_id: str
    trial_id: str
    changed_targets: tuple[str, ...]
    patch: Mapping[str, str]
    rationale: str | None = None


class CandidateChangeRecord(FrozenP01Model):
    candidate_id: str
    trial_id: str
    base_snapshot_ref: str
    changed_targets: tuple[str, ...]
    patch: Mapping[str, str]
    candidate_mapping: Mapping[str, str]
    materialization_status: str
```

`src/arso/p01/contracts/synthetic.py`:

```python
from typing import Mapping

from .base import FrozenP01Model
from .enums import DiagnosisConditionType, IntegrityStatus, ScientificAdmissionState, ValidationState


class SyntheticEvaluationContext(FrozenP01Model):
    context_id: str
    task_ref: str
    expected_mapping: Mapping[str, str]


class SyntheticEvaluationRecord(FrozenP01Model):
    evaluation_id: str
    trial_id: str
    candidate_ref: str
    passed: bool
    observations: tuple[str, ...]
    condition_metadata_present: bool = False


class SyntheticValidationResult(FrozenP01Model):
    validation_id: str
    trial_id: str
    state: ValidationState
    target_behavior_pass: bool
    hard_constraints_pass: bool
    baseline_immutable: bool
    mutation_policy_pass: bool
    reasons: tuple[str, ...]


class SyntheticTrialOutcome(FrozenP01Model):
    trial_id: str
    condition: DiagnosisConditionType
    matched_control_fingerprint: str
    candidate_ref: str
    evaluation_ref: str
    validation_ref: str
    integrity_status: IntegrityStatus
    admission_state: ScientificAdmissionState


class MatchedBlockIntegrityReport(FrozenP01Model):
    block_id: str
    all_required_conditions_present: bool
    shared_fixture: bool
    shared_visible_evidence: bool
    shared_repair_operator: bool
    shared_mutation_policy: bool
    shared_evaluator: bool
    shared_budget_policy: bool
    shared_seed_policy: bool
    shared_pre_run_lock: bool
    shared_matched_control_fingerprint: bool
    condition_is_only_intended_difference: bool
    violations: tuple[str, ...]
    final_status: IntegrityStatus


class SyntheticMatchedBlockResult(FrozenP01Model):
    block_id: str
    trial_outcomes: tuple[SyntheticTrialOutcome, ...]
    block_integrity: MatchedBlockIntegrityReport
    scientific_interpretation: None = None
```

Update `contracts/__init__.py` to export all eight classes.

Refine `ports/repair.py`:

```python
from arso.p01.contracts.candidate import RepairProposal

class RepairOperator(Protocol):
    def repair(self, request: RepairRequest) -> RepairProposal:
        ...
```

Refine `ports/evaluation.py`:

```python
from typing import Protocol

from arso.p01.contracts.candidate import CandidateChangeRecord
from arso.p01.contracts.synthetic import SyntheticEvaluationContext, SyntheticEvaluationRecord


class Evaluator(Protocol):
    def evaluate(
        self,
        candidate: CandidateChangeRecord,
        context: SyntheticEvaluationContext,
    ) -> SyntheticEvaluationRecord:
        ...
```

- [ ] **Step 4: Run tests to verify GREEN**

Run:

```bash
pytest tests/p01/runtime/test_i1_contracts_and_ports.py tests/p01/contracts -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/arso/p01/contracts src/arso/p01/ports tests/p01/runtime/test_i1_contracts_and_ports.py
git commit -m "feat(p01): harden I1 harness contracts"
```

---

### Task 2: Implement Truth Firewall enforcement and a capability-aware synthetic fixture provider

**Files:**
- Create: `src/arso/p01/runtime/__init__.py`
- Create: `src/arso/p01/runtime/errors.py`
- Create: `src/arso/p01/runtime/truth_firewall.py`
- Create: `src/arso/p01/adapters/fake/__init__.py`
- Create: `src/arso/p01/adapters/fake/fixture.py`
- Move/replace: `tests/p01/conformance_red/test_truth_firewall_red.py` -> `tests/p01/conformance/test_truth_firewall.py`
- Test: `tests/p01/runtime/test_fake_fixture_provider.py`

**Interfaces:**
- Produces: `SealedAccessDenied`, `SyntheticFixtureError`, `TruthFirewall`, `SyntheticFixtureProvider`.
- `TruthFirewall.authorize(condition: DiagnosisConditionType | None, purpose: SealedAccessPurpose) -> bool`.
- `SyntheticFixtureProvider.load_public() -> dict[str, object]`.
- `SyntheticFixtureProvider.load_oracle_diagnosis(condition: DiagnosisConditionType) -> dict[str, object]`.
- `SyntheticFixtureProvider.load_evaluation_truth() -> dict[str, object]`.
- `SyntheticFixtureProvider.sealed_access_log -> tuple[tuple[str, str], ...]` records purpose/condition for audit only.

- [ ] **Step 1: Replace the I0 xfail with real failing tests**

`tests/p01/conformance/test_truth_firewall.py`:

```python
import pytest

from arso.p01.contracts.enums import DiagnosisConditionType, SealedAccessPurpose
from arso.p01.runtime.errors import SealedAccessDenied
from arso.p01.runtime.truth_firewall import TruthFirewall


def test_oracle_may_materialize_only_oracle_diagnosis():
    firewall = TruthFirewall()
    assert firewall.authorize(
        DiagnosisConditionType.ORACLE,
        SealedAccessPurpose.ORACLE_DIAGNOSIS_MATERIALIZATION,
    ) is True


@pytest.mark.parametrize(
    "condition",
    [DiagnosisConditionType.WRONG, DiagnosisConditionType.NONE, DiagnosisConditionType.IMPLICIT],
)
def test_non_oracle_may_not_materialize_oracle_diagnosis(condition):
    firewall = TruthFirewall()
    with pytest.raises(SealedAccessDenied):
        firewall.authorize(
            condition,
            SealedAccessPurpose.ORACLE_DIAGNOSIS_MATERIALIZATION,
        )


def test_evaluation_access_is_not_repair_condition_access():
    firewall = TruthFirewall()
    assert firewall.authorize(None, SealedAccessPurpose.EVALUATION) is True
```

`tests/p01/runtime/test_fake_fixture_provider.py`:

```python
from pathlib import Path

import pytest

from arso.p01.adapters.fake.fixture import SyntheticFixtureProvider
from arso.p01.contracts.enums import DiagnosisConditionType
from arso.p01.runtime.errors import SealedAccessDenied
from arso.p01.runtime.truth_firewall import TruthFirewall


ROOT = Path("experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001")


def test_provider_denies_non_oracle_sealed_diagnosis_access():
    provider = SyntheticFixtureProvider(ROOT, TruthFirewall())
    with pytest.raises(SealedAccessDenied):
        provider.load_oracle_diagnosis(DiagnosisConditionType.NONE)


def test_provider_audits_oracle_access_without_exposing_full_truth():
    provider = SyntheticFixtureProvider(ROOT, TruthFirewall())
    diagnosis = provider.load_oracle_diagnosis(DiagnosisConditionType.ORACLE)
    assert set(diagnosis) == {
        "diagnosis_id",
        "visible_payload",
        "allowed_use",
        "repair_visible_only_after_materialization",
        "harness_only",
    }
    assert provider.sealed_access_log == (("ORACLE_DIAGNOSIS_MATERIALIZATION", "ORACLE"),)
```

Delete the old strict-xfail truth-firewall file after the replacement test exists.

- [ ] **Step 2: Run tests to verify RED**

Run:

```bash
pytest tests/p01/conformance/test_truth_firewall.py tests/p01/runtime/test_fake_fixture_provider.py -q
```

Expected: FAIL because `runtime.errors`, `TruthFirewall`, and fake provider do not exist.

- [ ] **Step 3: Implement minimal enforcement**

`src/arso/p01/runtime/errors.py`:

```python
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
```

`src/arso/p01/runtime/truth_firewall.py`:

```python
from arso.p01.contracts.enums import DiagnosisConditionType, SealedAccessPurpose
from .errors import SealedAccessDenied


class TruthFirewall:
    def authorize(
        self,
        condition: DiagnosisConditionType | None,
        purpose: SealedAccessPurpose,
    ) -> bool:
        if purpose is SealedAccessPurpose.ORACLE_DIAGNOSIS_MATERIALIZATION:
            if condition is not DiagnosisConditionType.ORACLE:
                raise SealedAccessDenied("only ORACLE may materialize sealed oracle diagnosis")
            return True
        if purpose in {
            SealedAccessPurpose.EVALUATION,
            SealedAccessPurpose.FIXTURE_QUALIFICATION,
            SealedAccessPurpose.SCIENTIFIC_AUDIT,
        }:
            if condition is not None:
                raise SealedAccessDenied("non-repair sealed access must not carry a trial condition")
            return True
        raise SealedAccessDenied(f"unsupported sealed access purpose: {purpose}")
```

`src/arso/p01/adapters/fake/fixture.py`:

```python
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

    def load_oracle_diagnosis(self, condition: DiagnosisConditionType) -> dict[str, object]:
        self.firewall.authorize(condition, SealedAccessPurpose.ORACLE_DIAGNOSIS_MATERIALIZATION)
        self._sealed_access_log.append((SealedAccessPurpose.ORACLE_DIAGNOSIS_MATERIALIZATION.value, condition.value))
        return self._read(self.root / "sealed" / "oracle_diagnosis.json")

    def load_evaluation_truth(self) -> dict[str, object]:
        self.firewall.authorize(None, SealedAccessPurpose.EVALUATION)
        self._sealed_access_log.append((SealedAccessPurpose.EVALUATION.value, "NONE"))
        return self._read(self.root / "sealed" / "expected_repair_target.json")
```

- [ ] **Step 4: Run tests to verify GREEN**

Run:

```bash
pytest tests/p01/conformance/test_truth_firewall.py tests/p01/runtime/test_fake_fixture_provider.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/arso/p01/runtime src/arso/p01/adapters/fake tests/p01/conformance tests/p01/runtime
git rm tests/p01/conformance_red/test_truth_firewall_red.py
git commit -m "feat(p01): enforce synthetic truth firewall"
```

---

### Task 3: Freeze WRONG/IMPLICIT payloads and implement one diagnosis-materialization path plus repair request builder

**Files:**
- Create: `experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001/conditions/wrong.json`
- Create: `experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001/conditions/implicit.json`
- Create: `src/arso/p01/runtime/diagnosis.py`
- Create: `src/arso/p01/runtime/repair_request.py`
- Test: `tests/p01/runtime/test_diagnosis_and_repair_request.py`

**Interfaces:**
- Consumes: `SyntheticFixtureProvider`, `P01TrialAssignment`, `DiagnosisInjection`, `RepairRequest`.
- Produces: `SyntheticDiagnosisInjector.materialize(assignment) -> DiagnosisInjection` and `SyntheticRepairRequestBuilder.build(assignment, fixture, diagnosis) -> RepairRequest`.
- WRONG and IMPLICIT payloads are loaded from frozen public condition files only; they must not invoke sealed-truth APIs.

- [ ] **Step 1: Write failing tests**

```python
from pathlib import Path

from arso.p01.adapters.fake.fixture import SyntheticFixtureProvider
from arso.p01.contracts.enums import DiagnosisConditionType
from arso.p01.runtime.diagnosis import SyntheticDiagnosisInjector
from arso.p01.runtime.truth_firewall import TruthFirewall


ROOT = Path("experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001")


def _assignment(condition):
    from arso.p01.contracts.trial import P01TrialAssignment
    return P01TrialAssignment(
        trial_id=f"trial-{condition.value.lower()}",
        batch_ref="synthetic-harness-only",
        scenario_ref="synthetic_001",
        matched_block_id="block-1",
        condition=condition,
        replicate_index=0,
        fixture_ref="synthetic_001",
        fixture_qualification_ref="synthetic_001_qualification",
        reference_task_ref="synthetic_001",
        base_snapshot_ref="synthetic_001_baseline",
        visible_evidence_ref="synthetic_001_public_evidence",
        diagnosis_condition_ref=f"condition-{condition.value.lower()}",
        repair_operator_ref="deterministic_fake_repair_v1",
        repair_instruction_ref="synthetic_repair_instruction_v1",
        mutation_policy_ref="mapping_only_v1",
        evaluator_binding_ref="synthetic_exact_evaluator_v1",
        validation_plan_ref="synthetic_validation_v1",
        budget_policy_ref="synthetic_budget_v1",
        retry_policy_ref="no_retry_v1",
        seed_assignment_ref="deterministic_seed_v1",
        pre_run_lock_hash="sha256:" + "1" * 64,
        matched_control_fingerprint="sha256:" + "2" * 64,
        created_at="2026-09-15T00:00:00Z",
    )


def test_none_materializes_null_payload_without_sealed_access():
    provider = SyntheticFixtureProvider(ROOT, TruthFirewall())
    injector = SyntheticDiagnosisInjector(provider)
    injection = injector.materialize(_assignment(DiagnosisConditionType.NONE))
    assert injection.visible_payload is None
    assert provider.sealed_access_log == ()


def test_wrong_uses_frozen_wrong_payload_without_sealed_access():
    provider = SyntheticFixtureProvider(ROOT, TruthFirewall())
    injector = SyntheticDiagnosisInjector(provider)
    injection = injector.materialize(_assignment(DiagnosisConditionType.WRONG))
    assert "formatting" in injection.visible_payload.lower()
    assert "reversed" not in injection.visible_payload.lower()
    assert provider.sealed_access_log == ()


def test_oracle_exposes_only_approved_visible_payload():
    provider = SyntheticFixtureProvider(ROOT, TruthFirewall())
    injector = SyntheticDiagnosisInjector(provider)
    injection = injector.materialize(_assignment(DiagnosisConditionType.ORACLE))
    assert injection.visible_payload == "The A↔B mapping rule in the transformation specification is reversed."
    assert "expected_patch" not in injection.model_dump()


def test_implicit_has_no_explicit_fault_locus_or_mechanism():
    provider = SyntheticFixtureProvider(ROOT, TruthFirewall())
    injector = SyntheticDiagnosisInjector(provider)
    injection = injector.materialize(_assignment(DiagnosisConditionType.IMPLICIT))
    text = injection.visible_payload.lower()
    assert "mapping" not in text
    assert "reversed" not in text
    assert "fault" not in text
```

- [ ] **Step 2: Run tests to verify RED**

Run:

```bash
pytest tests/p01/runtime/test_diagnosis_and_repair_request.py -q
```

Expected: FAIL because condition artifacts and runtime diagnosis module do not exist.

- [ ] **Step 3: Add frozen condition artifacts and minimal materializer/builder**

`wrong.json`:

```json
{
  "condition_id": "synthetic_001_wrong",
  "visible_payload": "The formatting/serialization stage is corrupting field order; repair that stage.",
  "explicit_fault_locus": false,
  "explicit_causal_mechanism": false,
  "harness_only": true
}
```

`implicit.json`:

```json
{
  "condition_id": "synthetic_001_implicit",
  "visible_payload": "Inspect the public task, baseline behavior, and observed examples, then propose one allowed repair.",
  "explicit_fault_locus": false,
  "explicit_causal_mechanism": false,
  "harness_only": true
}
```

`runtime/diagnosis.py` must use one `materialize` method for all four conditions. Only the ORACLE branch may call `load_oracle_diagnosis`; WRONG/IMPLICIT read the frozen condition files directly; NONE returns null payload.

The materialized `DiagnosisInjection` must always use `source_visibility="REPAIR_VISIBLE"` and must never contain sealed object refs other than the approved materialized visible payload hash/ref semantics already present in the I0 contract.

`runtime/repair_request.py` must build the existing strict `RepairRequest` and must not add any field outside that contract.

- [ ] **Step 4: Run tests to verify GREEN and preserve I0 negative boundary**

Run:

```bash
pytest tests/p01/runtime/test_diagnosis_and_repair_request.py tests/p01/contracts/test_i0_contracts.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001/conditions src/arso/p01/runtime tests/p01/runtime
git commit -m "feat(p01): materialize frozen diagnosis treatments"
```

---

### Task 4: Implement deterministic fake repair and immutable candidate materialization

**Files:**
- Create: `src/arso/p01/adapters/fake/repair.py`
- Create: `src/arso/p01/runtime/candidate.py`
- Test: `tests/p01/runtime/test_fake_repair_and_candidate.py`

**Interfaces:**
- Consumes: `RepairRequest`, `RepairProposal`, `CandidateChangeRecord`, a repair-visible `diagnosis_payloads: Mapping[str, str | None]` injected into the fake adapter constructor.
- Produces: `DeterministicFakeRepairOperator.repair(request) -> RepairProposal` and `CandidateMaterializer.materialize(base_snapshot_ref, baseline_mapping, proposal, allowed_targets) -> CandidateChangeRecord`.
- Fake repair adapter must not receive or store `DiagnosisConditionType`.

- [ ] **Step 1: Write failing tests**

```python
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
        diagnosis_payloads={"diag-oracle": "The A↔B mapping rule in the transformation specification is reversed."}
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
```

- [ ] **Step 2: Run tests to verify RED**

Run:

```bash
pytest tests/p01/runtime/test_fake_repair_and_candidate.py -q
```

Expected: FAIL because fake repair and candidate materializer do not exist.

- [ ] **Step 3: Implement deterministic repair and mutation guard**

`DeterministicFakeRepairOperator` must hold only `Mapping[str, str | None]` keyed by diagnosis injection ref. It must return the identity-mapping patch only when the visible payload contains both `mapping` and `reversed`; all other payloads return a deterministic no-op/baseline mapping patch.

`CandidateMaterializer` must:

```python
if not set(proposal.changed_targets).issubset(allowed_targets):
    raise MutationPolicyViolation(...)
```

and construct a fresh `candidate_mapping = dict(baseline_mapping)` before applying the patch. Candidate identity must be deterministic from trial/proposal content, for example `candidate:{trial_id}:{proposal_id}`.

- [ ] **Step 4: Run tests to verify GREEN**

Run:

```bash
pytest tests/p01/runtime/test_fake_repair_and_candidate.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/arso/p01/adapters/fake/repair.py src/arso/p01/runtime/candidate.py tests/p01/runtime/test_fake_repair_and_candidate.py
git commit -m "feat(p01): materialize deterministic repair candidates"
```

---

### Task 5: Implement condition-blind evaluation and deterministic synthetic validator

**Files:**
- Create: `src/arso/p01/runtime/evaluator_blindness.py`
- Create: `src/arso/p01/adapters/fake/evaluator.py`
- Create: `src/arso/p01/runtime/validation.py`
- Move/replace: `tests/p01/conformance_red/test_evaluator_blindness_red.py` -> `tests/p01/conformance/test_evaluator_blindness.py`
- Test: `tests/p01/runtime/test_evaluation_and_validation.py`

**Interfaces:**
- Produces: `EvaluatorBlindnessGuard.check(payload: Mapping[str, object]) -> bool`, `SyntheticExactEvaluator.evaluate(candidate, context) -> SyntheticEvaluationRecord`, and `SyntheticValidator.validate(...) -> SyntheticValidationResult`.

- [ ] **Step 1: Write failing tests**

```python
import pytest

from arso.p01.runtime.errors import EvaluatorBlindnessViolation
from arso.p01.runtime.evaluator_blindness import EvaluatorBlindnessGuard


def test_evaluator_guard_rejects_condition_metadata():
    guard = EvaluatorBlindnessGuard()
    with pytest.raises(EvaluatorBlindnessViolation):
        guard.check({"candidate_ref": "candidate-1", "condition": "ORACLE"})


def test_evaluator_guard_accepts_condition_blind_payload():
    guard = EvaluatorBlindnessGuard()
    assert guard.check({"candidate_ref": "candidate-1", "task_ref": "synthetic_001"}) is True
```

`tests/p01/runtime/test_evaluation_and_validation.py` must construct one identity-mapping candidate and one reversed-mapping candidate and assert:

```python
assert evaluator.evaluate(identity_candidate, context).passed is True
assert evaluator.evaluate(reversed_candidate, context).passed is False
```

Then assert validator returns `ACCEPTED` only when target behavior, hard constraints, baseline immutability, and mutation policy all pass; otherwise it returns `REJECTED`.

Delete the old evaluator xfail file after these tests exist.

- [ ] **Step 2: Run tests to verify RED**

Run:

```bash
pytest tests/p01/conformance/test_evaluator_blindness.py tests/p01/runtime/test_evaluation_and_validation.py -q
```

Expected: FAIL because guard/evaluator/validator are missing.

- [ ] **Step 3: Implement the minimal evaluator firewall and exact evaluator**

`EvaluatorBlindnessGuard` must reject these keys at any top level of evaluator input payload:

```python
FORBIDDEN = {
    "condition",
    "condition_type",
    "diagnosis",
    "diagnosis_injection",
    "repair_reasoning",
    "matched_arm_label",
}
```

`SyntheticExactEvaluator` must compare `candidate.candidate_mapping` against `context.expected_mapping` and set `condition_metadata_present=False` unconditionally because condition data is not part of its typed input.

`SyntheticValidator` must not accept a condition argument. It must compute `ValidationState.ACCEPTED` iff all four booleans are true, otherwise `REJECTED`; I1 does not need an automatic `INCONCLUSIVE` branch for deterministic local evaluation.

- [ ] **Step 4: Run tests to verify GREEN**

Run:

```bash
pytest tests/p01/conformance/test_evaluator_blindness.py tests/p01/runtime/test_evaluation_and_validation.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/arso/p01/runtime/evaluator_blindness.py src/arso/p01/runtime/validation.py src/arso/p01/adapters/fake/evaluator.py tests/p01/conformance tests/p01/runtime
git rm tests/p01/conformance_red/test_evaluator_blindness_red.py
git commit -m "feat(p01): enforce condition blind evaluation"
```

---

### Task 6: Implement trial integrity and scientific-admission separation

**Files:**
- Create: `src/arso/p01/runtime/integrity.py`
- Create: `src/arso/p01/runtime/admission.py`
- Move/replace: `tests/p01/conformance_red/test_admission_gate_red.py` -> `tests/p01/conformance/test_admission_gate.py`
- Test: `tests/p01/runtime/test_trial_integrity.py`

**Interfaces:**
- Produces: `TrialIntegrityChecker.check(...) -> P01IntegrityReport` and `ScientificAdmissionGate.admit(integrity: P01IntegrityReport, validation: SyntheticValidationResult) -> ScientificAdmissionState`.

- [ ] **Step 1: Write failing tests**

`tests/p01/conformance/test_admission_gate.py`:

```python
from arso.p01.contracts.enums import IntegrityStatus, ScientificAdmissionState, ValidationState
from arso.p01.runtime.admission import ScientificAdmissionGate


def test_validation_acceptance_does_not_bypass_failed_integrity():
    from arso.p01.contracts.integrity import P01IntegrityReport
    from arso.p01.contracts.synthetic import SyntheticValidationResult

    integrity = P01IntegrityReport(
        integrity_report_id="ir-1",
        trial_id="trial-1",
        lock_hash_valid=True,
        fixture_hash_valid=True,
        matched_control_valid=True,
        model_match=True,
        evidence_match=True,
        repair_operator_match=True,
        mutation_policy_match=True,
        evaluator_match=True,
        budget_policy_match=True,
        seed_policy_match=True,
        truth_firewall_pass=False,
        diagnosis_visibility_pass=True,
        evaluator_leakage_pass=True,
        retry_policy_pass=True,
        budget_accounting_pass=True,
        raw_record_complete=True,
        violations=("truth-firewall",),
        final_status=IntegrityStatus.FAIL,
    )
    validation = SyntheticValidationResult(
        validation_id="v-1",
        trial_id="trial-1",
        state=ValidationState.ACCEPTED,
        target_behavior_pass=True,
        hard_constraints_pass=True,
        baseline_immutable=True,
        mutation_policy_pass=True,
        reasons=(),
    )
    assert ScientificAdmissionGate().admit(integrity, validation) is ScientificAdmissionState.INVALID_CONTAMINATION
```

`tests/p01/runtime/test_trial_integrity.py` must assert a clean set of checks yields `IntegrityStatus.PASS` and any truth-firewall/evaluator-leakage/mutation-policy failure yields `IntegrityStatus.FAIL` with a violation code.

- [ ] **Step 2: Run tests to verify RED**

Run:

```bash
pytest tests/p01/conformance/test_admission_gate.py tests/p01/runtime/test_trial_integrity.py -q
```

Expected: FAIL because integrity/admission runtime classes do not exist.

- [ ] **Step 3: Implement checker and admission gate**

`TrialIntegrityChecker.check` should receive explicit booleans for the I1 checks and build `P01IntegrityReport`; it must derive `final_status` from the conjunction of required checks rather than accepting a caller-supplied final status.

`ScientificAdmissionGate.admit` semantics:

```python
if integrity.final_status is not IntegrityStatus.PASS:
    return ScientificAdmissionState.INVALID_CONTAMINATION
if validation.state is ValidationState.INCONCLUSIVE:
    return ScientificAdmissionState.INCOMPLETE
return ScientificAdmissionState.ADMITTED
```

A scientifically admitted trial may have validation `REJECTED`; admission means valid evidence, not successful repair.

Delete the old admission xfail file.

- [ ] **Step 4: Run tests to verify GREEN**

Run:

```bash
pytest tests/p01/conformance/test_admission_gate.py tests/p01/runtime/test_trial_integrity.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/arso/p01/runtime/integrity.py src/arso/p01/runtime/admission.py tests/p01/conformance tests/p01/runtime
git rm tests/p01/conformance_red/test_admission_gate_red.py
git commit -m "feat(p01): separate integrity from scientific admission"
```

---

### Task 7: Implement matched-control enforcement and block-level integrity

**Files:**
- Create: `src/arso/p01/runtime/matched_control.py`
- Move/replace: `tests/p01/conformance_red/test_matched_control_red.py` -> `tests/p01/conformance/test_matched_control.py`
- Test: `tests/p01/runtime/test_matched_block_integrity.py`

**Interfaces:**
- Produces: `MatchedControlChecker.check(assignments: tuple[P01TrialAssignment, ...]) -> MatchedBlockIntegrityReport`.
- Shared-control equality includes fixture, task, base snapshot, evidence, repair operator, repair instruction, mutation policy, evaluator, validation plan, budget policy, retry policy identity, seed policy, pre-run lock, and `matched_control_fingerprint`.
- `condition` and diagnosis payload are intentionally excluded from shared equality.

- [ ] **Step 1: Write failing tests**

```python
from arso.p01.contracts.enums import IntegrityStatus
from arso.p01.runtime.matched_control import MatchedControlChecker


def test_clean_block_passes_matched_control_check(four_assignments):
    report = MatchedControlChecker().check(tuple(four_assignments))
    assert report.final_status is IntegrityStatus.PASS
    assert report.condition_is_only_intended_difference is True


def test_evidence_mismatch_invalidates_block(four_assignments):
    bad = list(four_assignments)
    bad[1] = bad[1].model_copy(update={"visible_evidence_ref": "different-evidence"})
    report = MatchedControlChecker().check(tuple(bad))
    assert report.final_status is IntegrityStatus.FAIL
    assert report.shared_visible_evidence is False


def test_missing_condition_invalidates_block(four_assignments):
    report = MatchedControlChecker().check(tuple(four_assignments[:-1]))
    assert report.final_status is IntegrityStatus.FAIL
    assert report.all_required_conditions_present is False
```

Use a local pytest fixture in the same test file that constructs the exact four I1 assignments with identical non-treatment fields and the four condition enum values.

- [ ] **Step 2: Run tests to verify RED**

Run:

```bash
pytest tests/p01/conformance/test_matched_control.py tests/p01/runtime/test_matched_block_integrity.py -q
```

Expected: FAIL because checker does not exist.

- [ ] **Step 3: Implement explicit shared-field comparison**

Do not compare `model_dump()` wholesale because condition-specific fields are supposed to differ. Define an explicit immutable tuple of shared field names:

```python
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
```

Require exactly one of each `DiagnosisConditionType`. Build block booleans and violations from explicit equality checks. Never include `condition` or `diagnosis_condition_ref` in `SHARED_FIELDS`.

Delete the old matched-control xfail file.

- [ ] **Step 4: Run tests to verify GREEN**

Run:

```bash
pytest tests/p01/conformance/test_matched_control.py tests/p01/runtime/test_matched_block_integrity.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/arso/p01/runtime/matched_control.py tests/p01/conformance tests/p01/runtime
git rm tests/p01/conformance_red/test_matched_control_red.py
git commit -m "feat(p01): enforce matched block controls"
```

---

### Task 8: Build the thin synthetic matched-block runner and clean/contaminated E2E tests

**Files:**
- Create: `src/arso/p01/runtime/matched_block.py`
- Test: `tests/p01/e2e/test_synthetic_matched_block.py`
- Test: `tests/p01/e2e/test_contaminated_matched_block.py`

**Interfaces:**
- Produces: `SyntheticMatchedBlockRunner.run() -> SyntheticMatchedBlockResult`.
- Runner composes only the I1 runtime/adapters created in Tasks 2–7; it is not a general workflow engine.

- [ ] **Step 1: Write failing clean-block E2E test**

```python
from arso.p01.contracts.enums import DiagnosisConditionType, IntegrityStatus, ScientificAdmissionState
from arso.p01.runtime.matched_block import SyntheticMatchedBlockRunner


def test_clean_synthetic_matched_block_executes_all_four_conditions():
    result = SyntheticMatchedBlockRunner.default().run()

    assert {outcome.condition for outcome in result.trial_outcomes} == set(DiagnosisConditionType)
    assert len(result.trial_outcomes) == 4
    assert len({outcome.matched_control_fingerprint for outcome in result.trial_outcomes}) == 1
    assert result.block_integrity.final_status is IntegrityStatus.PASS
    assert all(
        outcome.admission_state is ScientificAdmissionState.ADMITTED
        for outcome in result.trial_outcomes
    )
    assert result.scientific_interpretation is None
```

Add assertions that only the ORACLE trial generated an `ORACLE_DIAGNOSIS_MATERIALIZATION` access event; evaluation access may occur condition-independently but must never be passed back into a repair request.

- [ ] **Step 2: Write failing contaminated-block E2E test**

```python
from arso.p01.contracts.enums import IntegrityStatus
from arso.p01.runtime.matched_block import SyntheticMatchedBlockRunner


def test_contaminated_block_is_rejected_when_one_arm_uses_different_evidence():
    runner = SyntheticMatchedBlockRunner.default()
    result = runner.run(contamination={
        "WRONG": {"visible_evidence_ref": "different-evidence"}
    })
    assert result.block_integrity.final_status is IntegrityStatus.FAIL
```

The contamination hook is test-only harness functionality. It must mutate the constructed assignment before execution, never modify the frozen fixture files.

- [ ] **Step 3: Run E2E tests to verify RED**

Run:

```bash
pytest tests/p01/e2e -q
```

Expected: FAIL because matched-block runner does not exist.

- [ ] **Step 4: Implement the thin runner**

The runner must perform exactly this sequence for each of the four assignments:

```text
load public fixture
materialize diagnosis
register diagnosis visible payload by injection ref
build RepairRequest
fake repair
candidate materialization
construct condition-blind SyntheticEvaluationContext
EvaluatorBlindnessGuard.check on evaluator payload
exact evaluation
validation
trial integrity report
scientific admission
SyntheticTrialOutcome
```

After all four trials:

```text
MatchedControlChecker.check(assignments)
→ SyntheticMatchedBlockResult
```

Important implementation rules:

```text
- the fake repair operator constructor receives only injection-ref -> visible-payload mapping;
- no hidden condition map may be passed to the fake repair operator;
- evaluator context contains only task/expected mapping, never diagnosis/condition;
- trial integrity PASS does not depend on whether repair succeeded;
- block integrity is computed from assignments, not outcomes;
- scientific_interpretation is always None;
- contamination injection is available only through `run(contamination=...)` and only mutates assignment fields before the matched-control check.
```

- [ ] **Step 5: Run I1 focused tests to verify GREEN**

Run:

```bash
pytest tests/p01/contracts tests/p01/runtime tests/p01/conformance tests/p01/e2e tests/p01/fixtures -q
```

Expected: PASS with no XFAIL among the four former I0 integrity gates.

- [ ] **Step 6: Verify old red gate directory is empty/removed**

Run:

```bash
find tests/p01/conformance_red -type f -name 'test_*.py' -print
```

Expected: no output. Remove the directory if empty.

- [ ] **Step 7: Commit**

```bash
git add src/arso/p01/runtime/matched_block.py tests/p01/e2e
git commit -m "feat(p01): run deterministic synthetic matched block"
```

---

### Task 9: Full I1 verification, frozen-source non-regression, and checkpoint record

**Files:**
- Create: `docs/arso/p0_1/I1_VERIFICATION.md`
- Modify: `pyproject.toml` only if the `p01_red` marker is now unused; remove the marker registration when no `p01_red` tests remain.

**Interfaces:**
- Records exact verification evidence and the scientific boundary. Does not introduce new runtime behavior.

- [ ] **Step 1: Run the focused I1 suite**

Run:

```bash
pytest tests/p01/contracts tests/p01/runtime tests/p01/conformance tests/p01/e2e tests/p01/fixtures -q
```

Expected: PASS, zero XFAIL for the four I0 enforcement gates.

- [ ] **Step 2: Run the full repository suite**

Run:

```bash
PYTHONPATH=src python -m pytest -q
```

Expected: PASS.

- [ ] **Step 3: Re-run the frozen DI candidate baseline**

Run:

```bash
cd di_contracts_v1 && PYTHONPATH=. python -m pytest -q
```

Expected: PASS.

- [ ] **Step 4: Verify frozen contract/source paths were not modified**

Run from repository root:

```bash
git diff --name-only arso-p0-1-i0...HEAD -- src/design_intelligence/contracts di_contracts_v1
```

Expected: no output.

Also run the repository checksum gate already used by CI:

```bash
sha256sum -c specs/SPEC_SOURCE_CHECKSUMS.sha256
```

Expected: all registered frozen sources report `OK`.

- [ ] **Step 5: Verify no real provider/network implementation entered the I1 code path**

Run:

```bash
grep -R -n -E 'openai|anthropic|requests\.|httpx|urllib\.request|aiohttp' src/arso/p01 experiments/p0_1_oracle_diagnosis || true
```

Expected: no provider/network implementation in executable I1 source. Documentation strings mentioning provider non-goals are acceptable only outside executable imports/calls.

- [ ] **Step 6: Write `I1_VERIFICATION.md` from observed results**

The document must contain these status lines exactly:

```text
I1 status: IMPLEMENTED / VERIFIED
Synthetic matched block: EXECUTED / DETERMINISTIC
Scientific-integrity enforcement: ACTIVE FOR SYNTHETIC HARNESS
Batch-001: NOT EXECUTED
Real provider calls: NONE
P0.1 empirical hypothesis: OPEN
```

It must record:

```text
- exact branch and commit SHA
- focused I1 test command and observed pass/fail counts
- full repository test command and observed counts
- DI baseline regression command and observed counts
- checksum/drift results
- clean synthetic block integrity status
- contaminated synthetic block rejection evidence
- confirmation that former TruthFirewall/MatchedControl/EvaluatorBlindness/Admission gates are ordinary green tests
- explicit statement that synthetic outcomes are not P0.1 empirical evidence
```

Do not write expected counts before running the commands; copy only observed counts from fresh verification output.

- [ ] **Step 7: Commit verification checkpoint**

```bash
git add docs/arso/p0_1/I1_VERIFICATION.md pyproject.toml
git commit -m "docs(p01): record I1 verification checkpoint"
```

---

## Implementation Order and Stop Conditions

Execute strictly in order:

```text
Task 1 typed harness contracts
→ Task 2 Truth Firewall
→ Task 3 diagnosis materialization
→ Task 4 fake repair + candidate
→ Task 5 blind evaluation + validation
→ Task 6 trial integrity + admission
→ Task 7 matched controls
→ Task 8 clean/contaminated E2E
→ Task 9 fresh verification
```

Stop immediately if any of these occurs:

```text
- a non-Oracle path requires sealed truth to make tests pass;
- repair code needs condition_type or a hidden condition map;
- evaluator code needs diagnosis/condition metadata;
- a candidate mutation must touch evaluator/task/budget/sealed data;
- matched-control PASS requires excluding an unapproved shared field;
- full repository tests regress frozen DI behavior;
- implementation begins to require retry/budget/resume/general workflow machinery.
```

Any such event is an architecture/spec issue, not a reason to widen I1 ad hoc.

## Self-Review

### Spec coverage

Every I1 design requirement maps to an implementation task:

```text
Truth Firewall                         → Task 2
Frozen WRONG/NONE/IMPLICIT/ORACLE     → Task 3
Repair visibility boundary            → Tasks 1, 3, 4
Fake repair without hidden condition  → Task 4
Immutable candidate/mutation policy   → Task 4
Condition-blind evaluation            → Task 5
Validation != admission               → Tasks 5, 6
Trial integrity                       → Task 6
Matched-control enforcement           → Task 7
Clean synthetic E2E                   → Task 8
Contaminated rejection E2E            → Task 8
No real provider / no Batch-001       → Global constraints + Task 9
Fresh verification/non-regression     → Task 9
```

### Placeholder scan

No `TBD`, `TODO`, unspecified implementation step, or undefined future helper is required by the plan. Retry/budget/resume/full state-machine persistence are explicitly out of scope rather than left incomplete.

### Type consistency

The plan uses one typed chain throughout:

```text
P01TrialAssignment
→ DiagnosisInjection
→ RepairRequest
→ RepairProposal
→ CandidateChangeRecord
→ SyntheticEvaluationRecord
→ SyntheticValidationResult
→ P01IntegrityReport
→ ScientificAdmissionState
→ SyntheticTrialOutcome
→ MatchedBlockIntegrityReport
→ SyntheticMatchedBlockResult
```

The four scientific treatment arms remain experimental `DiagnosisConditionType` values and are not promoted to ARSO `DiagnosticBelief` objects.
