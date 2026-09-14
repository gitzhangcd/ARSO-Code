# ARSO P0.1 I0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first isolated ARSO P0.1 implementation slice: strict experiment contracts, protocol skeletons, a synthetic public/sealed fixture, and intentionally red scientific-integrity conformance tests without running Batch-001 or calling a real model provider.

**Architecture:** Add `src/arso/p01` beside the frozen `src/design_intelligence` implementation. Reuse the existing repository-level exact-reference/hash support types instead of duplicating shared canonical-shell identities. Keep P0.1-specific treatment and trial types experimental; do not claim they are universal ARSO primitives. The default test suite stays green while `p01_red` tests can be forced red with `--runxfail` to define I1 enforcement work.

**Tech Stack:** Python 3.12, Pydantic 2.12+, RFC 8785 support already present in the repository, pytest 8.

**Spec:** `docs/superpowers/specs/2026-09-14-arso-p0-1-i0-design.md`

## Global Constraints

- Do not modify frozen files under `src/design_intelligence/contracts`.
- Do not introduce a new runtime dependency.
- Do not create shadow copies of existing `ExactObjectRef`, `ObjectRef`, `ContentHash`, or canonical-shell types.
- P0.1 treatment vocabulary is exactly `ORACLE | WRONG | NONE | IMPLICIT`.
- `RepairRequest` must not expose sealed truth, expected repair target, evaluation answer, or raw condition type.
- Synthetic fixture is harness-only and must not be described as P0.1 scientific evidence.
- Default `pytest` must remain green.
- `pytest -m p01_red --runxfail` must expose the intentionally unimplemented integrity gates.

---

### Task 1: Bootstrap the isolated `arso.p01` package and strict experimental base types

**Files:**
- Create: `src/arso/__init__.py`
- Create: `src/arso/p01/__init__.py`
- Create: `src/arso/p01/contracts/__init__.py`
- Create: `src/arso/p01/contracts/base.py`
- Create: `src/arso/p01/contracts/enums.py`
- Test: `tests/p01/contracts/test_base_and_enums.py`

**Interfaces:**
- Produces: `P01Model`, `FrozenP01Model`, `DiagnosisConditionType`, `ExecutionState`, `ValidationState`, `ScientificAdmissionState`, `IntegrityStatus`, `SealedAccessPurpose`.
- Consumes: only Pydantic and stdlib.

- [ ] **Step 1: Write the failing test**

```python
from pydantic import ValidationError

from arso.p01.contracts.base import FrozenP01Model
from arso.p01.contracts.enums import DiagnosisConditionType


class Example(FrozenP01Model):
    value: str


def test_p01_models_are_strict_and_frozen():
    obj = Example(value="x")
    try:
        obj.value = "y"
    except ValidationError:
        pass
    else:
        raise AssertionError("frozen contract accepted mutation")


def test_diagnosis_condition_vocabulary_is_exact():
    assert {member.value for member in DiagnosisConditionType} == {
        "ORACLE", "WRONG", "NONE", "IMPLICIT"
    }
```

- [ ] **Step 2: Run test to verify RED**

Run: `pytest tests/p01/contracts/test_base_and_enums.py -q`
Expected: import failure because `arso.p01` does not exist.

- [ ] **Step 3: Implement the minimal package and enums**

```python
# src/arso/p01/contracts/base.py
from pydantic import BaseModel, ConfigDict


class P01Model(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, validate_default=True)


class FrozenP01Model(P01Model):
    model_config = ConfigDict(
        extra="forbid", strict=True, validate_default=True, frozen=True
    )
```

```python
# src/arso/p01/contracts/enums.py
from enum import StrEnum


class DiagnosisConditionType(StrEnum):
    ORACLE = "ORACLE"
    WRONG = "WRONG"
    NONE = "NONE"
    IMPLICIT = "IMPLICIT"


class ExecutionState(StrEnum):
    CREATED = "CREATED"
    LOCK_VERIFIED = "LOCK_VERIFIED"
    FIXTURE_RESOLVED = "FIXTURE_RESOLVED"
    ASSIGNED = "ASSIGNED"
    INPUT_MATERIALIZED = "INPUT_MATERIALIZED"
    REPAIR_RUNNING = "REPAIR_RUNNING"
    REPAIR_RETURNED = "REPAIR_RETURNED"
    CANDIDATE_MATERIALIZED = "CANDIDATE_MATERIALIZED"
    EVALUATION_RUNNING = "EVALUATION_RUNNING"
    EVALUATED = "EVALUATED"
    VALIDATION_RUNNING = "VALIDATION_RUNNING"
    FINALIZED = "FINALIZED"
    EXECUTION_FAILED = "EXECUTION_FAILED"
    CANCELLED = "CANCELLED"
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"


class ValidationState(StrEnum):
    NOT_EVALUATED = "NOT_EVALUATED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    INCONCLUSIVE = "INCONCLUSIVE"


class ScientificAdmissionState(StrEnum):
    PENDING = "PENDING"
    INTEGRITY_CHECKING = "INTEGRITY_CHECKING"
    ADMITTED = "ADMITTED"
    EXCLUDED_PREDEFINED = "EXCLUDED_PREDEFINED"
    INVALID_CONTAMINATION = "INVALID_CONTAMINATION"
    INCOMPLETE = "INCOMPLETE"


class IntegrityStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    INCOMPLETE = "INCOMPLETE"


class SealedAccessPurpose(StrEnum):
    ORACLE_DIAGNOSIS_MATERIALIZATION = "ORACLE_DIAGNOSIS_MATERIALIZATION"
    EVALUATION = "EVALUATION"
    FIXTURE_QUALIFICATION = "FIXTURE_QUALIFICATION"
    SCIENTIFIC_AUDIT = "SCIENTIFIC_AUDIT"
```

- [ ] **Step 4: Verify GREEN**

Run: `pytest tests/p01/contracts/test_base_and_enums.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

Commit: `feat(p01): bootstrap strict experimental contracts`

---

### Task 2: Add the exact I0 contract skeleton

**Files:**
- Create: `src/arso/p01/contracts/lock.py`
- Create: `src/arso/p01/contracts/trial.py`
- Create: `src/arso/p01/contracts/diagnosis.py`
- Create: `src/arso/p01/contracts/repair.py`
- Create: `src/arso/p01/contracts/integrity.py`
- Create: `src/arso/p01/contracts/fixture.py`
- Modify: `src/arso/p01/contracts/__init__.py`
- Test: `tests/p01/contracts/test_i0_contracts.py`

**Interfaces:**
- Consumes: `FrozenP01Model`, enums from Task 1, and existing `design_intelligence.contracts.core.ContentHash` / `ExactObjectRef` for exact repository-level refs.
- Produces: `P01PreRunLock`, `P01MatchedBlock`, `P01TrialAssignment`, `DiagnosisConditionSpec`, `DiagnosisInjection`, `RepairRequest`, `P01IntegrityReport`, `PublicQualifiedFixture`, `SealedFixtureTruth`, `FixtureQualificationRecord`.

- [ ] **Step 1: Write failing contract tests**

```python
from pydantic import ValidationError

from arso.p01.contracts import DiagnosisConditionType, DiagnosisInjection, RepairRequest


def test_repair_request_has_no_raw_condition_field():
    assert "condition_type" not in RepairRequest.model_fields


def test_repair_request_rejects_expected_repair_target():
    payload = {
        "request_id": "req-1",
        "trial_id": "trial-1",
        "reference_task_ref": "task-1",
        "baseline_system_ref": "snapshot-1",
        "visible_evidence_ref": "evidence-1",
        "diagnosis_injection_ref": "diag-1",
        "mutation_policy_ref": "mutation-1",
        "repair_instruction_ref": "instruction-1",
        "model_binding_ref": "model-1",
        "sampling_config_ref": "sampling-1",
        "output_contract_ref": "output-1",
        "budget_ref": "budget-1",
        "seed_ref": "seed-1",
        "expected_repair_target": "forbidden",
    }
    try:
        RepairRequest.model_validate(payload)
    except ValidationError:
        pass
    else:
        raise AssertionError("RepairRequest accepted sealed repair target")


def test_diagnosis_injection_materializes_visible_payload_only():
    injection = DiagnosisInjection(
        injection_id="diag-1",
        trial_id="trial-1",
        condition=DiagnosisConditionType.NONE,
        visible_payload=None,
        visible_payload_hash=None,
        materialization_method="frozen-template",
        source_visibility="REPAIR_VISIBLE",
    )
    assert injection.visible_payload is None
```

- [ ] **Step 2: Verify RED**

Run: `pytest tests/p01/contracts/test_i0_contracts.py -q`
Expected: import failures for missing contract classes.

- [ ] **Step 3: Implement minimal strict models**

Use focused files. Keep reference fields as strict opaque identifiers in I0 where the upstream ARSO canonical primitive has not yet been implemented; do not invent a shadow canonical object model. Use the existing shared `ContentHash` type for stored SHA-256 values.

Core `RepairRequest` fields must be exactly:

```python
class RepairRequest(FrozenP01Model):
    request_id: str
    trial_id: str
    reference_task_ref: str
    baseline_system_ref: str
    visible_evidence_ref: str
    diagnosis_injection_ref: str
    mutation_policy_ref: str
    repair_instruction_ref: str
    model_binding_ref: str
    sampling_config_ref: str
    output_contract_ref: str
    budget_ref: str
    seed_ref: str
```

`P01IntegrityReport` must contain boolean checks for lock/fixture/fingerprint/truth-firewall/diagnosis-visibility/retry/budget/raw-record completeness, `violations: tuple[str, ...]`, and `final_status: IntegrityStatus`.

- [ ] **Step 4: Verify GREEN**

Run: `pytest tests/p01/contracts -q`
Expected: PASS.

- [ ] **Step 5: Commit**

Commit: `feat(p01): add I0 trial and integrity contract skeleton`

---

### Task 3: Declare D3 port skeletons without implementing orchestration

**Files:**
- Create: `src/arso/p01/ports/__init__.py`
- Create: `src/arso/p01/ports/fixture.py`
- Create: `src/arso/p01/ports/diagnosis.py`
- Create: `src/arso/p01/ports/repair.py`
- Create: `src/arso/p01/ports/evaluation.py`
- Create: `src/arso/p01/ports/integrity.py`
- Test: `tests/p01/contracts/test_port_signatures.py`

**Interfaces:**
- Produces Protocols: `FixtureProvider`, `DiagnosisInjector`, `RepairRequestBuilder`, `RepairOperator`, `Evaluator`, `IntegrityChecker`.
- I0 intentionally does not provide concrete provider adapters.

- [ ] **Step 1: Write failing signature tests**

```python
import inspect

from arso.p01.ports.repair import RepairRequestBuilder
from arso.p01.ports.evaluation import Evaluator


def test_repair_request_builder_does_not_accept_sealed_truth():
    signature = inspect.signature(RepairRequestBuilder.build)
    assert "sealed_truth" not in signature.parameters


def test_evaluator_signature_does_not_accept_condition_type():
    signature = inspect.signature(Evaluator.evaluate)
    assert "condition" not in signature.parameters
    assert "condition_type" not in signature.parameters
```

- [ ] **Step 2: Verify RED**

Run: `pytest tests/p01/contracts/test_port_signatures.py -q`
Expected: missing module/import failure.

- [ ] **Step 3: Implement Protocol definitions**

Example:

```python
from typing import Protocol

from arso.p01.contracts.diagnosis import DiagnosisInjection
from arso.p01.contracts.fixture import PublicQualifiedFixture
from arso.p01.contracts.repair import RepairRequest
from arso.p01.contracts.trial import P01TrialAssignment


class RepairRequestBuilder(Protocol):
    def build(
        self,
        assignment: P01TrialAssignment,
        fixture: PublicQualifiedFixture,
        diagnosis: DiagnosisInjection,
    ) -> RepairRequest: ...
```

Keep evaluator input condition-blind by signature.

- [ ] **Step 4: Verify GREEN**

Run: `pytest tests/p01/contracts/test_port_signatures.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

Commit: `feat(p01): declare scientific harness ports`

---

### Task 4: Add the harness-only synthetic fixture with public/sealed qualification split

**Files:**
- Create: `experiments/p0_1_oracle_diagnosis/README.md`
- Create: `experiments/p0_1_oracle_diagnosis/manifests/synthetic_001.yaml`
- Create: `experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001/public/task.json`
- Create: `experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001/public/baseline_state.json`
- Create: `experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001/public/evidence.json`
- Create: `experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001/sealed/planted_fault.json`
- Create: `experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001/sealed/causal_truth.json`
- Create: `experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001/sealed/oracle_diagnosis.json`
- Create: `experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001/sealed/expected_repair_target.json`
- Create: `experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001/qualification/qualification_record.json`
- Create: `experiments/p0_1_oracle_diagnosis/locks/synthetic_pre_run_lock.json`
- Test: `tests/p01/fixtures/test_synthetic_fixture_layout.py`

**Interfaces:**
- Produces the I0 dry-run fixture only; it is not Batch-001.

- [ ] **Step 1: Write the failing layout test**

```python
from pathlib import Path


ROOT = Path("experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001")


def test_synthetic_fixture_has_public_sealed_and_qualification_boundaries():
    assert (ROOT / "public" / "task.json").is_file()
    assert (ROOT / "public" / "baseline_state.json").is_file()
    assert (ROOT / "public" / "evidence.json").is_file()
    assert (ROOT / "sealed" / "causal_truth.json").is_file()
    assert (ROOT / "sealed" / "oracle_diagnosis.json").is_file()
    assert (ROOT / "qualification" / "qualification_record.json").is_file()
```

- [ ] **Step 2: Verify RED**

Run: `pytest tests/p01/fixtures/test_synthetic_fixture_layout.py -q`
Expected: missing files.

- [ ] **Step 3: Add deterministic fixture contents**

Public task: preserve `a` and `b` fields. Baseline behavior: swaps `a` and `b`. Public evidence: two examples exhibiting the swap. Sealed fault: reversed mapping rule. Oracle diagnosis: `The A↔B mapping rule in the transformation specification is reversed.` Expected repair target: replace the reversed mapping with identity mapping. Qualification status: harness-only synthetic fixture, no scientific claim.

- [ ] **Step 4: Verify GREEN**

Run: `pytest tests/p01/fixtures/test_synthetic_fixture_layout.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

Commit: `test(p01): add qualified synthetic harness fixture`

---

### Task 5: Land the first intentionally red scientific-integrity conformance tests

**Files:**
- Modify: `pyproject.toml`
- Create: `tests/p01/conformance_red/test_truth_firewall_red.py`
- Create: `tests/p01/conformance_red/test_matched_control_red.py`
- Create: `tests/p01/conformance_red/test_evaluator_blindness_red.py`
- Create: `tests/p01/conformance_red/test_admission_gate_red.py`

**Interfaces:**
- Defines the I1 implementation gates; no production enforcement is added in I0.

- [ ] **Step 1: Register the marker**

Add to pytest configuration:

```toml
markers = [
  "p01_red: intentionally red P0.1 scientific-integrity conformance gate",
]
```

- [ ] **Step 2: Add strict xfail tests**

Each file must use:

```python
import pytest

pytestmark = [
    pytest.mark.p01_red,
    pytest.mark.xfail(strict=True, reason="I1 scientific-integrity enforcement gate"),
]
```

Representative test bodies should call a deliberately missing enforcement API such as `TruthFirewall.authorize(...)`, `MatchedControlChecker.check(...)`, or `ScientificAdmissionGate.admit(...)`, so `--runxfail` fails for the intended missing capability rather than due to syntax/setup errors.

- [ ] **Step 3: Verify the default suite stays green**

Run: `pytest -q`
Expected: existing tests PASS; P0.1 red gates are reported as XFAIL, not failures.

- [ ] **Step 4: Verify the red suite is truly red**

Run: `pytest -m p01_red --runxfail -q`
Expected: FAIL on the missing I1 enforcement APIs.

- [ ] **Step 5: Commit**

Commit: `test(p01): freeze first red scientific integrity gates`

---

### Task 6: I0 verification and checkpoint record

**Files:**
- Create: `docs/arso/p0_1/I0_VERIFICATION.md`

**Interfaces:**
- Records exact I0 scope and verification evidence; does not claim P0.1 empirical success.

- [ ] **Step 1: Run focused green tests**

Run: `pytest tests/p01/contracts tests/p01/fixtures -q`
Expected: PASS.

- [ ] **Step 2: Run the full repository baseline**

Run: `pytest -q`
Expected: PASS with only expected P0.1 XFAIL entries.

- [ ] **Step 3: Run the forced-red integrity suite**

Run: `pytest -m p01_red --runxfail -q`
Expected: FAIL only for the intentionally missing I1 enforcement behavior.

- [ ] **Step 4: Write the checkpoint record**

The document must state:

```text
I0 status: IMPLEMENTED / VERIFIED
Scientific experiment status: NOT STARTED
Batch-001 status: NOT EXECUTED
Real provider calls: NONE
Frozen DI Exact-V1 contract modifications: NONE
Next gate: I1 integrity enforcement + deterministic fake adapters + E2E synthetic matched block
```

Include the exact commands and observed counts.

- [ ] **Step 5: Commit**

Commit: `docs(p01): record I0 verification checkpoint`

## Self-review

- Spec coverage: I0 includes repository isolation, strict contract skeleton, ports, synthetic fixture, red integrity gates, and verification. Full D2/D3 runtime orchestration is intentionally deferred to I1+.
- Placeholder scan: no implementation step depends on TBD/TODO behavior.
- Type consistency: P0.1 treatment is represented by `DiagnosisConditionType` and materialized `DiagnosisInjection`; repair-visible APIs do not accept raw sealed truth.
