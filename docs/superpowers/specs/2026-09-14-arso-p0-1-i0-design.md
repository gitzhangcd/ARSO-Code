# ARSO P0.1 I0 Implementation Design

## Status

`FREEZE CANDIDATE` for the I0 implementation slice only.

## Goal

Turn the approved D1-D3 design into the smallest executable repository slice that can carry exact P0.1 trial contracts, a sealed/public synthetic fixture, interface skeletons, and intentionally red scientific-integrity conformance tests without executing Batch-001 or calling a real model provider.

## Scientific boundary

I0 is infrastructure preparation for the P0.1 Oracle Diagnosis Value Pilot. It does **not** implement a diagnosis engine, probe policy, adaptive search, memory, meta-optimization, production deployment, or any empirical Batch-001 run.

The implementation must preserve these invariants:

```text
DiagnosisCondition = the only intended treatment difference.
Trial != Attempt.
ExecutionState != ValidationState != ScientificAdmissionState.
SealedTruth must not enter the repair-visible path.
Repair must not consume evaluation results.
Behavior-changing candidate state must not mutate the baseline state.
Scientific admission requires an integrity pass.
Reproducible != deterministic.
```

## Existing repository boundary

The repository already contains a frozen Design Intelligence / Exact-V1 implementation under `src/design_intelligence`. I0 must not modify frozen B01 or shared-shell wire contracts.

I0 adds an isolated experimental namespace:

```text
src/arso/p01/
```

It may import the existing frozen shared support types from `design_intelligence.contracts.core` where identity reuse is required, but it must not import B01 business/domain models and must not create shadow copies of `ExactObjectRef`, `ObjectRef`, `ContentHash`, or canonical-shell classes.

This dependency is a repository compatibility bridge for I0, not a claim that ARSO semantically belongs to Design Intelligence.

## I0 package layout

```text
src/arso/
├── __init__.py
└── p01/
    ├── __init__.py
    ├── contracts/
    │   ├── __init__.py
    │   ├── base.py
    │   ├── enums.py
    │   ├── lock.py
    │   ├── trial.py
    │   ├── diagnosis.py
    │   ├── repair.py
    │   ├── integrity.py
    │   └── fixture.py
    └── ports/
        ├── __init__.py
        ├── fixture.py
        ├── diagnosis.py
        ├── repair.py
        ├── evaluation.py
        └── integrity.py

experiments/p0_1_oracle_diagnosis/
├── README.md
├── manifests/
│   └── synthetic_001.yaml
├── fixtures/
│   └── synthetic_001/
│       ├── public/
│       │   ├── task.json
│       │   ├── baseline_state.json
│       │   └── evidence.json
│       ├── sealed/
│       │   ├── planted_fault.json
│       │   ├── causal_truth.json
│       │   ├── oracle_diagnosis.json
│       │   └── expected_repair_target.json
│       └── qualification/
│           └── qualification_record.json
└── locks/
    └── synthetic_pre_run_lock.json

tests/p01/
├── contracts/
├── fixtures/
└── conformance_red/
```

## Exact I0 contract surface

I0 freezes only the contract skeleton required to write tests. It intentionally does not implement the full D2 persistent object set.

### Enumerations

```text
DiagnosisConditionType = ORACLE | WRONG | NONE | IMPLICIT
ExecutionState = CREATED | LOCK_VERIFIED | FIXTURE_RESOLVED | ASSIGNED | INPUT_MATERIALIZED | REPAIR_RUNNING | REPAIR_RETURNED | CANDIDATE_MATERIALIZED | EVALUATION_RUNNING | EVALUATED | VALIDATION_RUNNING | FINALIZED | EXECUTION_FAILED | CANCELLED | BUDGET_EXCEEDED
ValidationState = NOT_EVALUATED | ACCEPTED | REJECTED | INCONCLUSIVE
ScientificAdmissionState = PENDING | INTEGRITY_CHECKING | ADMITTED | EXCLUDED_PREDEFINED | INVALID_CONTAMINATION | INCOMPLETE
IntegrityStatus = PASS | FAIL | INCOMPLETE
SealedAccessPurpose = ORACLE_DIAGNOSIS_MATERIALIZATION | EVALUATION | FIXTURE_QUALIFICATION | SCIENTIFIC_AUDIT
```

### Models implemented in I0

```text
P01PreRunLock
P01MatchedBlock
P01TrialAssignment
DiagnosisConditionSpec
DiagnosisInjection
RepairRequest
P01IntegrityReport
PublicQualifiedFixture
SealedFixtureTruth
FixtureQualificationRecord
```

All models are strict (`extra='forbid'`, strict validation). Record-like models are frozen.

### Important negative boundary

`RepairRequest` must not contain any of these fields or aliases:

```text
ground_truth_fault
causal_truth
oracle_truth
expected_repair_target
evaluation_answer
condition_type
```

The repair-visible treatment is represented only by the materialized `DiagnosisInjection.visible_payload`.

## Port skeletons

I0 declares Protocols only; it does not provide production adapters.

```text
FixtureProvider
DiagnosisInjector
RepairRequestBuilder
RepairOperator
Evaluator
IntegrityChecker
```

The protocol types establish the D3 dependency direction. I0 does not yet implement runtime orchestration, retry, budgeting, state transitions, or candidate materialization.

## Synthetic fixture

`synthetic_001` is deliberately trivial and deterministic. The baseline transformation swaps fields `a` and `b` instead of preserving them.

Public evidence contains the task, baseline behavior, and observed examples. Sealed truth contains the planted mapping fault, oracle diagnosis, and expected repair target. The qualification record asserts that the fixture is synthetic and qualified only for harness testing.

The fixture must never be interpreted as scientific evidence for the P0.1 hypothesis.

## I0 red conformance suite

I0 lands executable tests for the highest-risk D3 invariants. They are marked `p01_red` and `xfail(strict=True)` so the repository's default suite remains green while `pytest -m p01_red --runxfail` demonstrates the missing enforcement.

The first red tests cover:

```text
R01 non-Oracle sealed access must be blocked
R02 RepairRequest must reject sealed truth / expected target fields
R03 matched-control mismatch must invalidate a block
R04 evaluator-facing API must not require or expose diagnosis condition
R05 finalized trial cannot be scientifically admitted without an integrity pass
```

I0 is complete when these tests exist, fail for the intended missing behavior under `--runxfail`, and the pre-existing test suite remains green.

## Non-goals

```text
No real provider SDK.
No Batch-001 data.
No model calls.
No database.
No queue or workflow framework.
No learned diagnosis engine.
No P0.1 statistical analysis.
No modification of frozen DI Exact-V1 contracts.
```

## I0 acceptance criteria

1. `src/arso/p01` imports successfully under Python 3.12.
2. Exact I0 models reject extra fields and invalid enum values.
3. Synthetic fixture has a clean public/sealed/qualification split.
4. Port signatures compile and do not accept sealed truth in repair-visible inputs.
5. Default repository tests remain green.
6. `pytest -m p01_red --runxfail` fails specifically on the five missing scientific-integrity enforcement behaviors.
7. No files under frozen `src/design_intelligence/contracts` are modified by I0.
